#!/usr/bin/env python3
"""Repository checks for skill-zip.

1. Every Markdown document has a Korean pair (<name>_ko.md) and vice versa,
   and each pair has the same number of headings, table rows, and code fences.
2. Every skill directory (one containing SKILL.md) is listed in
   .claude-plugin/plugin.json, and every listed path has a SKILL.md whose
   frontmatter `name` matches the directory name.

Exits with status 1 if any check fails.
"""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
IGNORED_DIRS = {".git", ".github", ".claude-plugin", ".omc", "node_modules"}
KO_SUFFIX = "_ko"


def iter_markdown():
    for path in sorted(ROOT.rglob("*.md")):
        if not IGNORED_DIRS.intersection(path.relative_to(ROOT).parts):
            yield path


def structure(path):
    """Count headings (outside code blocks), table rows, and code fences."""
    headings = rows = fences = 0
    in_code = False
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("```"):
            fences += 1
            in_code = not in_code
        elif in_code:
            continue
        elif line.startswith("#"):
            headings += 1
        elif line.startswith("|"):
            rows += 1
    return {"headings": headings, "table rows": rows, "code fences": fences}


def check_pairs(errors):
    for path in iter_markdown():
        rel = path.relative_to(ROOT).as_posix()
        if path.stem.endswith(KO_SUFFIX):
            original = path.with_name(path.stem[: -len(KO_SUFFIX)] + ".md")
            if not original.exists():
                errors.append(f"{rel}: no English original ({original.name})")
            continue

        korean = path.with_name(path.stem + KO_SUFFIX + ".md")
        if not korean.exists():
            errors.append(f"{rel}: no Korean pair ({korean.name})")
            continue

        en, ko = structure(path), structure(korean)
        for key in en:
            if en[key] != ko[key]:
                errors.append(f"{rel}: {key} differ (en {en[key]}, ko {ko[key]})")


def frontmatter_name(skill_md):
    text = skill_md.read_text(encoding="utf-8")
    match = re.match(r"---\r?\n(.*?)\r?\n---", text, re.DOTALL)
    if not match:
        return None
    for line in match.group(1).splitlines():
        if line.startswith("name:"):
            return line.split(":", 1)[1].strip().strip("\"'")
    return None


def check_plugin(errors):
    manifest = ROOT / ".claude-plugin" / "plugin.json"
    try:
        listed = json.loads(manifest.read_text(encoding="utf-8")).get("skills", [])
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f".claude-plugin/plugin.json: cannot read ({exc})")
        return

    listed_dirs = set()
    for entry in listed:
        skill_dir = (ROOT / entry).resolve()
        listed_dirs.add(skill_dir)
        if not (skill_dir / "SKILL.md").exists():
            errors.append(f"plugin.json: {entry} has no SKILL.md")

    for skill_md in ROOT.rglob("SKILL.md"):
        if IGNORED_DIRS.intersection(skill_md.relative_to(ROOT).parts):
            continue
        skill_dir = skill_md.parent
        rel = skill_dir.relative_to(ROOT).as_posix()
        if skill_dir.resolve() not in listed_dirs:
            errors.append(f"{rel}: skill is not listed in plugin.json")
        name = frontmatter_name(skill_md)
        if name != skill_dir.name:
            errors.append(
                f"{rel}/SKILL.md: frontmatter name '{name}' "
                f"does not match directory '{skill_dir.name}'"
            )


def main():
    errors = []
    check_pairs(errors)
    check_plugin(errors)
    if errors:
        print(f"{len(errors)} problem(s) found:")
        for error in errors:
            print(f"  - {error}")
        return 1
    print("All checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
