#!/usr/bin/env python3
"""Find eGovFrame SQL rule violations in MyBatis/iBatis mapper XML files.

Read-only. Reports only the group A rules of references/sql-rules.md that a
pattern match can detect reliably; everything else still needs a review.

Usage:
    python check_sql.py <path> [<path> ...] [--dbms mysql]

<path> is a mapper XML file or a directory searched recursively for *.xml.
--dbms keeps only files whose name ends with _<dbms>.xml, for projects that
keep one SQL file per DBMS (e.g. EgovBoard_SQL_mysql.xml).

Exit code: 0 when nothing is found, 1 when findings exist, 2 on bad usage.
"""

import argparse
import re
import sys
from pathlib import Path

STATEMENT = re.compile(
    r"<(select|insert|update|delete|sql|statement)\b[^>]*>(.*?)</\1\s*>",
    re.IGNORECASE | re.DOTALL,
)
XML_COMMENT = re.compile(r"<!--.*?-->", re.DOTALL)
TAG = re.compile(r"<[^>]+>")
BIND = re.compile(r"#\{[^}]*\}|\$\{[^}]*\}|#[A-Za-z_][\w.]*#")
QUOTED = re.compile(r"'(?:[^']|'')*'")
SQL_COMMENT = re.compile(r"/\*.*?\*/", re.DOTALL)
KEYWORDS = re.compile(
    r"\b(select|from|where|and|or|insert|into|values|update|set|delete"
    r"|union|order\s+by|group\s+by|having|join|on|as|case|when|then|else|end)\b"
)
MAX_COLUMNS = 120
# Build output and tool folders that hold copies of the mapper files.
SKIPPED_DIRS = {"target", "build", "bin", "out", ".git", "node_modules"}


def blank(match):
    """Replace a match with spaces, keeping newlines so offsets stay valid."""
    return re.sub(r"[^\n]", " ", match.group(0))


def line_of(text, offset):
    return text.count("\n", 0, offset) + 1


def check_file(path):
    raw = path.read_text(encoding="utf-8", errors="replace")
    text = XML_COMMENT.sub(blank, raw)
    findings = []

    def add(offset, rule, message):
        findings.append((line_of(text, offset), rule, message))

    for stmt in STATEMENT.finditer(text):
        kind = stmt.group(1).lower()
        start = stmt.start(2)
        body = stmt.group(2)
        # SQL text without XML tags, binds, string literals or /* */ comments,
        # padded to the same length so offsets map back to the file.
        sql = TAG.sub(blank, body)
        sql_no_comments = SQL_COMMENT.sub(blank, sql)
        plain = QUOTED.sub(blank, BIND.sub(blank, sql_no_comments))

        for m in re.finditer(r"\$\{", body):
            add(start + m.start(), "SQL rule 10",
                "${} builds literal SQL (also an SQL injection risk); use #{}")
        for m in re.finditer(r"\t", sql):
            add(start + m.start(), "SQL rule 3", "tab character; indent with spaces")
            break
        for m in re.finditer(r"--", plain):
            add(start + m.start(), "SQL rule 8", "'--' comment; use /* */")
        for m in re.finditer(r"\bSELECT\s+(?:DISTINCT\s+)?(?:\w+\.)?\*", plain, re.IGNORECASE):
            add(start + m.start(), "SQL rule 4", "SELECT *; list the columns")
        for m in re.finditer(r"(?<![\w(])\w+\.\*", plain):
            add(start + m.start(), "SQL rule 4", f"'{m.group(0)}'; list the columns")
        for m in re.finditer(r"\bUNION\b(?!\s+ALL\b)", plain, re.IGNORECASE):
            add(start + m.start(), "performance principle 14",
                "UNION without ALL; use UNION ALL unless rows must be deduplicated")
        if kind == "delete" and not re.search(r"\bWHERE\b", sql, re.IGNORECASE) \
                and not re.search(r"<where\b", body, re.IGNORECASE):
            add(start, "DELETE example", "DELETE without WHERE")
        lowercase = KEYWORDS.search(plain)
        if lowercase:
            add(start + lowercase.start(), "SQL rule 2",
                f"lowercase keyword '{lowercase.group(0)}'; write SQL keywords in uppercase")

        # Line length counts only lines that carry SQL text, not tag-only lines.
        offset = start
        for line in body.split("\n"):
            if TAG.sub("", line).strip() and len(line.expandtabs(4)) > MAX_COLUMNS:
                add(offset, "SQL rule 1", f"line longer than {MAX_COLUMNS} columns")
            offset += len(line) + 1

    return sorted(set(findings))


def mapper_files(paths, dbms):
    for p in paths:
        p = Path(p)
        candidates = [p] if p.is_file() else sorted(p.rglob("*.xml"))
        for f in candidates:
            if SKIPPED_DIRS.intersection(f.parts[:-1]) and not p.is_file():
                continue
            if dbms and not f.stem.lower().endswith("_" + dbms.lower()):
                continue
            head = f.read_text(encoding="utf-8", errors="replace")[:2000]
            if "<mapper" in head or "<sqlMap" in head:
                yield f


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("paths", nargs="+")
    parser.add_argument("--dbms", help="only check files named *_<dbms>.xml")
    args = parser.parse_args()

    files = list(mapper_files(args.paths, args.dbms))
    if not files:
        print("No mapper XML files found.", file=sys.stderr)
        return 2

    total = 0
    for f in files:
        for line, rule, message in check_file(f):
            print(f"{f}:{line}: [{rule}] {message}")
            total += 1
    print(f"{total} finding(s) in {len(files)} file(s).", file=sys.stderr)
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main())
