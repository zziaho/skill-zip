#!/usr/bin/env python3
"""List candidate security weaknesses (구현단계 보안약점) in source code.

Read-only. Each match is a candidate, not a finding: judge it with the
Vulnerable and Not vulnerable lines of the weakness in references/*.md.
Weaknesses that need data-flow analysis (for example 18, 26, 33, 35, 40 to 42)
are not searched; review them by reading the code.

Usage:
    python find_candidates.py <path> [<path> ...] [--only 1,23,36] [--summary]
                              [--include-tests]

<path> is a file or a directory searched recursively. Scanned files: Java,
JSP, MyBatis/iBatis mapper XML, Spring Security XML, C/C++, and
.properties/.yml configuration. Test folders are skipped unless
--include-tests is given.

Exit code: 0 when nothing is found, 1 when candidates exist, 2 on bad usage.
"""

import argparse
import re
import sys
from pathlib import Path

NAMES = {
    1: "SQL 삽입", 2: "코드 삽입", 3: "경로 조작 및 자원 삽입", 4: "크로스사이트 스크립트",
    5: "운영체제 명령어 삽입", 6: "위험한 형식 파일 업로드",
    7: "신뢰되지 않는 URL 주소로 자동접속 연결", 8: "부적절한 XML 외부개체 참조",
    9: "XML 삽입", 10: "LDAP 삽입", 11: "크로스사이트 요청 위조", 12: "서버사이드 요청 위조",
    13: "HTTP 응답분할", 14: "정수형 오버플로우", 15: "보안기능 결정에 사용되는 부적절한 입력값",
    16: "메모리 버퍼 오버플로우", 17: "포맷 스트링 삽입", 19: "부적절한 인가",
    20: "중요한 자원에 대한 잘못된 권한 설정", 21: "취약한 암호화 알고리즘 사용",
    22: "암호화되지 않은 중요정보", 23: "하드코드된 중요정보", 24: "충분하지 않은 키 길이 사용",
    25: "적절하지 않은 난수값 사용", 27: "부적절한 전자서명 확인", 28: "부적절한 인증서 유효성 검증",
    29: "사용자 하드디스크에 저장되는 쿠키를 통한 정보노출", 30: "주석문 안에 포함된 시스템 주요정보",
    31: "솔트 없이 일방향 해쉬함수 사용", 32: "무결성 검사 없는 코드 다운로드",
    34: "경쟁조건: 검사시점과 사용시점", 36: "오류 메시지 정보노출", 37: "오류 상황 대응 부재",
    38: "부적절한 예외 처리", 39: "Null Pointer 역참조", 43: "신뢰할 수 없는 데이터의 역직렬화",
    44: "잘못된 세션에 의한 데이터 정보노출", 45: "제거되지 않고 남은 디버그 코드",
    46: "Public 메소드부터 반환된 Private 배열", 47: "Private 배열에 Public 데이터 할당",
    48: "DNS lookup에 의존한 보안결정", 49: "취약한 API 사용",
}

JAVA = {".java"}
JSP = {".jsp", ".jspx", ".jspf", ".tag"}
C = {".c", ".h", ".cc", ".cpp", ".cxx", ".hpp", ".hh"}
XML = {".xml"}
CONFIG = {".properties", ".yml", ".yaml"}
SKIPPED_DIRS = {"target", "build", "bin", "out", ".git", "node_modules", ".gradle", ".idea"}
TEST_DIRS = {"test", "tests"}

INPUT = r"(?:getParameter|getHeader|getQueryString|getCookies|getInputStream|getReader|getAttribute)\s*\("


def rx(pattern, flags=0):
    return re.compile(pattern, flags)


# (weakness, file kinds, pattern, message). Patterns run on code with comments blanked.
CODE_RULES = [
    # 1 SQL injection
    (1, JAVA | JSP, rx(r"\b(?:executeQuery|executeUpdate|execute|addBatch|prepareStatement|prepareCall"
                        r"|createQuery|createNativeQuery|createSQLQuery|newQuery)\s*\((?=[^;]*\+)[^;]*;"),
     "query built by concatenation; check that every value is bound (?, :name, #{})"),
    (1, JAVA | JSP, rx(r"\bcreateStatement\s*\("),
     "java.sql.Statement; check that no external input reaches the query string"),
    # 2 code injection
    (2, JAVA | JSP, rx(r"\.eval\s*\((?!\s*\")|\bparseExpression\s*\((?!\s*\")"),
     "dynamic code execution with a non-literal argument"),
    (2, JSP, rx(r"new\s+Function\s*\([^)]*<%="), "JavaScript Function() built from a server-side value"),
    # 3 path traversal
    (3, JAVA | JSP, rx(r"new\s+(?:File|FileInputStream|FileOutputStream|FileReader|FileWriter|RandomAccessFile)"
                        r"\s*\((?=[^;]*(?:\+|" + INPUT + r"))[^;]*;|\bPaths\.get\s*\((?=[^;]*(?:\+|" + INPUT + r"))"),
     "file path built from a variable; check for .. / \\ and that it stays inside the base directory"),
    (3, C, rx(r"\bfopen\s*\(\s*(?!\")"), "fopen with a non-literal path"),
    # 4 XSS
    (4, JSP, rx(r"<%=(?!\s*request\.getContextPath\(\))"), "scriptlet output; check encoding of external or user-written values"),
    (4, JSP, rx(r"escapeXml\s*=\s*\"false\"", re.IGNORECASE), "<c:out escapeXml=\"false\">"),
    (4, JAVA | JSP, rx(r"getWriter\s*\(\s*\)\s*\.\s*(?:print|println|write|append)\s*\((?!\s*\")"),
     "response written directly; check encoding"),
    (4, JSP, rx(r"\.innerHTML\s*=|document\.write\s*\("), "DOM sink; check that request values are encoded"),
    # 5 OS command
    (5, JAVA | JSP, rx(r"\.exec\s*\(|new\s+ProcessBuilder\s*\("), "OS command execution; check where the command and arguments come from"),
    (5, C, rx(r"\b(?:system|popen|execl|execlp|execle|execv|execvp|execve)\s*\((?!\s*\")"), "OS command with a non-literal argument"),
    # 6 upload
    (6, JAVA | JSP, rx(r"\bgetOriginalFilename\s*\(|\bgetFilesystemName\s*\(|\btransferTo\s*\("),
     "file upload; check the extension allowlist, storage path and stored name"),
    # 7 open redirect
    (7, JAVA | JSP, rx(r"\bsendRedirect\s*\((?!\s*\"[^\"]*\"\s*\))(?!\s*[\w.()]*getContextPath\(\)\s*(?:\+\s*\"[^\"]*\"\s*)?\))"
                        r"|\"redirect:\"\s*\+"),
     "redirect to a non-literal target; check against an allowlist"),
    # 9 XPath / XQuery
    (9, JAVA, rx(r"\b\w*[Xx][Pp]ath\w*\s*\.\s*(?:compile|evaluate)\s*\(\s*\"[^\"]*\"\s*\+|\bprepareExpression\s*\(\s*\"[^\"]*\"\s*\+"),
     "XPath/XQuery built by concatenation"),
    # 10 LDAP
    (10, JAVA, rx(r"\.search\s*\((?=[^;]*\"\s*\(?[&|]?\(\w+=)(?=[^;]*\+)"), "LDAP filter built by concatenation"),
    (10, JAVA, rx(r"String\s+\w*[Ff]ilter\w*\s*=\s*\"\s*\(.*\+"), "LDAP filter string built by concatenation"),
    # 11 CSRF
    (11, JAVA, rx(r"csrf\s*\(\s*\)\s*\.\s*disable\s*\(|csrf\s*\(\s*(?:AbstractHttpConfigurer::disable|\w+\s*->\s*\w+\.disable\(\))"),
     "Spring Security CSRF protection disabled"),
    (11, XML, rx(r"<csrf\s+disabled\s*=\s*\"true\"", re.IGNORECASE), "Spring Security CSRF protection disabled"),
    # 12 SSRF
    (12, JAVA | JSP, rx(r"new\s+URL\s*\(\s*(?!\")|\.openConnection\s*\(|\.openStream\s*\("),
     "server-side request; check that the URL or host is not taken from input"),
    (12, JAVA, rx(r"\b(?:getForObject|getForEntity|postForObject|postForEntity|exchange)\s*\(\s*(?!\")"),
     "RestTemplate call with a non-literal URL"),
    # 13 response splitting
    (13, JAVA | JSP, rx(r"\b(?:addHeader|setHeader)\s*\((?=[^;]*" + INPUT + r")|new\s+Cookie\s*\((?=[^;]*" + INPUT + r")"),
     "request value placed in a header or cookie; check CR/LF removal"),
    # 14 integer overflow
    (14, JAVA | JSP, rx(r"new\s+\w+\s*\[\s*(?:Integer|Long|Short)\.(?:parseInt|parseLong|valueOf|parseShort)\s*\("),
     "array size parsed from input; check the range"),
    (14, C, rx(r"\b(?:malloc|calloc|alloca)\s*\([^;]*\batoi\s*\("), "allocation size from atoi; check the range"),
    # 15 security decision
    (15, JAVA | JSP, rx(r"getParameter\s*\(\s*\"(?:price|amount|role|isAdmin|admin|authenticated|isLogin|level|grade|userId|memberId)\"\s*\)",
                         re.IGNORECASE),
     "security-relevant value read from the request; check that the decision uses server-side data"),
    # 17 format string
    (17, C, rx(r"\b(?:printf|vprintf|syslog)\s*\(\s*(?!\")[A-Za-z_]|\b(?:fprintf|sprintf|vfprintf|vsprintf|dprintf)\s*\(\s*[^,]+,\s*(?!\")[A-Za-z_]"
               r"|\bsnprintf\s*\(\s*[^,]+,\s*[^,]+,\s*(?!\")[A-Za-z_]"),
     "format string is not a literal"),
    (17, JAVA | JSP, rx(r"\b(?:String\.format|printf|MessageFormat\.format)\s*\(\s*(?!\")[A-Za-z_][\w.\[\]]*\s*(?:\+|,)"),
     "format string is not a literal"),
    # 19 authorization
    (19, JAVA, rx(r"SECURITY_AUTHENTICATION\s*,\s*\"none\""), "anonymous LDAP bind"),
    # 20 permissions
    (20, JAVA | JSP, rx(r"\bset(?:Readable|Writable|Executable)\s*\(\s*true\s*,\s*false\s*\)"), "permission granted to every user"),
    (20, JAVA | JSP, rx(r"\"umask\s+0+\"|chmod\s+(?:-R\s+)?7[0-7]7|\"rwxrwxrwx\"|\"rw-rw-rw-\""), "world-accessible permission"),
    (20, C, rx(r"\bumask\s*\(\s*0+\s*\)|\bchmod\s*\([^,]+,\s*0?7[0-7]7\s*\)"), "world-accessible permission"),
    # 21 weak algorithms
    (21, JAVA | JSP, rx(r"getInstance\s*\(\s*\"(?:DES|DESede|TripleDES|RC2|RC4|ARCFOUR|RC5|MD2|MD4|MD5|SHA-?1|SHA)(?:/[^\"]*)?\"",
                         re.IGNORECASE), "weak algorithm (21 lists RC2, RC4, RC5, RC6, MD4, MD5, SHA1, DES)"),
    (21, JAVA | JSP, rx(r"getInstance\s*\(\s*\"[^\"]*/ECB/", re.IGNORECASE), "ECB mode"),
    (21, C, rx(r"\bEVP_(?:des_\w+|rc4\w*|rc2_\w+|md4|md5|sha1)\s*\(|\b(?:MD4|MD5|SHA1)\s*\("), "weak algorithm"),
    # 22 plaintext
    # (?<!=) skips attribute values such as taglib uri="http://..."; the list skips namespaces and parser feature names.
    (22, JAVA | JSP, rx(r"(?<!=)\"http://(?=[A-Za-z0-9])(?!localhost|127\.0\.0\.1|www\.w3\.org|java\.sun\.com|xmlns\.jcp\.org"
                         r"|www\.springframework\.org|mybatis\.org|ibatis\.apache\.org|tiles\.apache\.org|www\.egovframe\.go\.kr/schema"
                         r"|apache\.org/xml/|xml\.org/sax/|javax\.xml|jakarta\.xml)[^\"]*\""),
     "plain HTTP URL; check whether sensitive data travels over it"),
    (22, JAVA | JSP, rx(r"\.setSecure\s*\(\s*false\s*\)"), "cookie without the secure attribute"),
    # 23 hard-coded secrets
    (23, JAVA | JSP, rx(r"(?<![\w\"?&.])(?:\w*(?i:password|passwd|pwd|secret|apikey|api_key|privatekey|private_key|credential)\w*"
                         r"|[A-Z_]*PASS[A-Z_]*|PW)"
                         r"\s*=\s*\"[^\"$\n]{4,}\"\s*[;,)]"), "string literal assigned to a secret-like name"),
    (23, JAVA | JSP, rx(r"\bgetConnection\s*\([^;]*,\s*\"[^\"]+\"\s*\)"), "DB password as a literal"),
    (23, JAVA | JSP, rx(r"new\s+SecretKeySpec\s*\(\s*(?:\"|new\s+byte\s*\[\s*\]\s*\{)|byte\s*\[\s*\]\s*\w*[Kk]ey\w*\s*=\s*\{"),
     "cryptographic key as a literal"),
    (23, C, rx(r"\b\w*(?:password|passwd|pwd|secret)\w*\s*(?:\[\s*\])?\s*=\s*\"[^\"]+\"", re.IGNORECASE), "secret as a literal"),
    # 24 key length
    (24, JAVA | JSP, rx(r"\binitialize\s*\(\s*(?:512|768|1024)\b|\bKeyGenerator\b[^;]*;\s*\w+\.init\s*\(\s*(?:40|56|64)\b"),
     "key shorter than the minimum (RSA 2048, symmetric 128)"),
    (24, C, rx(r"\bRSA_generate_key(?:_ex)?\s*\([^,]*?\b(?:512|768|1024)\b"), "RSA key shorter than 2048 bits"),
    # 25 random
    (25, JAVA | JSP, rx(r"\bMath\.random\s*\(|new\s+(?:java\.util\.)?Random\s*\("), "predictable random; check whether it is used for a security value"),
    (25, C, rx(r"\b(?:rand|random)\s*\(\s*\)"), "predictable random; check whether it is used for a security value"),
    # 27 signatures
    (27, JAVA, rx(r"new\s+JarFile\s*\(\s*[^,()]+\)|new\s+JarFile\s*\([^,]+,\s*false\s*\)"), "JAR opened without signature verification"),
    # 28 certificates
    (28, JAVA, rx(r"implements\s+(?:\w+\s*,\s*)*X509TrustManager|ALLOW_ALL_HOSTNAME_VERIFIER|NoopHostnameVerifier"
                  r"|TrustAllStrategy|TrustSelfSignedStrategy|setHostnameVerifier\s*\([^;]*->\s*true"),
     "custom or disabled certificate or host name verification"),
    (28, C, rx(r"\bSSL_VERIFY_NONE\b|X509_V_ERR_SELF_SIGNED_CERT_IN_CHAIN"), "certificate verification disabled or relaxed"),
    # 32 code download
    (32, JAVA, rx(r"new\s+URLClassLoader\s*\(|\bdefineClass\s*\("), "code loaded at run time; check integrity verification"),
    # 34 TOCTOU
    (34, JAVA | JSP, rx(r"if\s*\(\s*!?\s*[\w.]+\.(?:exists|isFile|canRead|canWrite)\s*\(\s*\)"), "check-then-use on a file"),
    (34, C, rx(r"\baccess\s*\("), "access() before use"),
    # 36 error exposure
    (36, JAVA | JSP, rx(r"\.printStackTrace\s*\(\s*\)"), "printStackTrace()"),
    (36, JAVA | JSP, rx(r"\b(?:print|println|write|append|addAttribute|setMessage)\s*\([^;]*\b(?:e|ex|e\d|exc|exception|t|th|throwable|err)\.(?:getMessage|toString|getLocalizedMessage)\s*\(\s*\)"),
     "exception text sent to the user"),
    # 38 broad catch
    (38, JAVA | JSP, rx(r"catch\s*\(\s*(?:final\s+)?(?:Exception|Throwable|RuntimeException)\s+\w+\s*\)"), "broad catch"),
    # 39 null check after use
    (39, JAVA | JSP, rx(r"\b(\w+)\.\w+\s*\([^()]*\)[^|&;]*(?:\|\||&&)\s*\1\s*[!=]=\s*null"), "null check after the dereference"),
    # 43 deserialization
    (43, JAVA, rx(r"new\s+ObjectInputStream\s*\(|new\s+XMLDecoder\s*\(|\benableDefaultTyping\s*\(|\bactivateDefaultTyping\s*\("),
     "deserialization; check the data source and class allowlist"),
    # 45 debug code
    (45, JAVA, rx(r"\bSystem\.(?:out|err)\.print"), "console output; check for leftover debug code"),
    # 48 DNS
    (48, JAVA | JSP, rx(r"\.getCanonicalHostName\s*\(|\.getHostName\s*\(|\bgetRemoteHost\s*\("), "host name lookup; check it is not used for a security decision"),
    (48, C, rx(r"\bgethostbyaddr\s*\(|\bgetnameinfo\s*\("), "host name lookup; check it is not used for a security decision"),
    # 49 dangerous API
    (49, C, rx(r"\b(?:gets|strcpy|strcat|sprintf|vsprintf|strncpy|strncat)\s*\("), "banned C function (also check weakness 16)"),
    (49, C, rx(r"\bscanf\s*\(\s*\"[^\"]*%s"), "unbounded %s in scanf (also check weakness 16)"),
    (49, JAVA | JSP, rx(r"\bSystem\.exit\s*\("), "System.exit in a J2EE application"),
]

WEB_CLASS = rx(r"@(?:Rest)?Controller\b|extends\s+(?:Http)?Servlet\b|@Service\b|@Component\b|@WebServlet\b")
WEB_SOCKET = rx(r"new\s+Socket\s*\(")
MAIN = rx(r"public\s+static\s+void\s+main\s*\(")
XXE_FACTORY = rx(r"\b(?:DocumentBuilderFactory|SAXParserFactory|XMLInputFactory|SchemaFactory|TransformerFactory)\s*\.\s*new(?:Instance|Factory)\s*\("
                 r"|\bcreateUnmarshaller\s*\(|new\s+SAXBuilder\s*\(|new\s+SAXReader\s*\(")
XXE_GUARD = rx(r"disallow-doctype-decl|ACCESS_EXTERNAL_DTD|SUPPORT_DTD|external-general-entities|FEATURE_SECURE_PROCESSING")
DIGEST = rx(r"MessageDigest\s*\.\s*getInstance\s*\(")
EMPTY_CATCH = rx(r"catch\s*\([^)]*\)\s*\{\s*\}")
MUTABLE_FIELD = rx(r"^[ \t]*(?:private|protected|public)?[ \t]*(?!static\b)(?!final\b)(?:transient[ \t]+|volatile[ \t]+)?"
                   r"(?!return\b|class\b|interface\b|enum\b|import\b|package\b)"
                   r"[A-Za-z_][\w.<>,\[\] ?]*[ \t]+[A-Za-z_]\w*[ \t]*(?:=[^;]*)?;", re.MULTILINE)
INJECTED = rx(r"@(?:Autowired|Resource|Inject|Value|PersistenceContext)\b")
ARRAY_FIELD = rx(r"\bprivate\s+(?:static\s+)?(?!final\b)[\w.<>]+\s*\[\s*\]\s+(\w+)\s*[;=]")
COOKIE_AGE = rx(r"\bsetMaxAge\s*\(\s*([\d\s*()]+)\)")
# The last key segment ends with a secret word, and the value is one printable ASCII token:
# screen messages such as "cop.password=비밀번호" have Korean text or spaces and are skipped.
CONFIG_SECRET = rx(r"^[ \t]*(?:[\w-]+\.)*[\w-]*(?:password|passwd|pwd|secret)[ \t]*[:=][ \t]*[\"']?(?!ENC\()(?!\$\{)[!-~]+[ \t]*$",
                   re.IGNORECASE | re.MULTILINE)
CONFIG_ERROR = rx(r"include-(?:stacktrace|exception|message)[ \t]*[:=][ \t]*(?:always|true)", re.IGNORECASE)
# The value is an ASCII token that does not look like commented-out code (request.getParameter(...)).
COMMENT_SECRET = rx(r"(?:password|passwd|pwd|비밀번호|패스워드|암호)\s*(?:is|:|=|/|는|은)\s*(?![\w.]*\()[!-:<-~]{3,}", re.IGNORECASE)
MAPPER_DOLLAR = rx(r"\$\{")
IBATIS_DOLLAR = rx(r"\$[A-Za-z_][\w.]*\$")
XML_COMMENT = rx(r"<!--.*?-->", re.DOTALL)


def blank(text):
    return re.sub(r"[^\n]", " ", text)


def split_comments(text, kind):
    """Return (code, comments): code with comments blanked, and a list of (offset, comment text)."""
    out, comments = list(text), []
    i, n = 0, len(text)
    while i < n:
        c = text[i]
        if c in "\"'":
            j = i + 1
            while j < n and text[j] != c and text[j] != "\n":
                j += 2 if text[j] == "\\" else 1
            i = j + 1
        elif text.startswith("//", i) and not (kind in JSP and text[i - 1:i] == ":"):
            j = text.find("\n", i)
            j = n if j < 0 else j
            comments.append((i, text[i:j]))
            out[i:j] = blank(text[i:j])
            i = j
        elif text.startswith("/*", i) or (kind in JSP and text.startswith("<%--", i)):
            end = "--%>" if text.startswith("<%--", i) else "*/"
            j = text.find(end, i + 2)
            j = n if j < 0 else j + len(end)
            comments.append((i, text[i:j]))
            out[i:j] = blank(text[i:j])
            i = j
        else:
            i += 1
    return "".join(out), comments


def line_of(text, offset):
    return text.count("\n", 0, offset) + 1


def cookie_seconds(expr):
    if not re.fullmatch(r"[\d\s*()]+", expr):
        return None
    total = 1
    for part in re.findall(r"\d+", expr):
        total *= int(part)
    return total


def scan(path, suffix):
    text = path.read_text(encoding="utf-8", errors="replace")
    found = []

    def add(offset, weakness, message):
        found.append((line_of(text, offset), weakness, message))

    if suffix in CONFIG:
        if path.name.lower().startswith("message"):
            return found
        for m in CONFIG_SECRET.finditer(text):
            add(m.start(), 22, "plaintext secret in configuration (also weakness 23)")
        for m in CONFIG_ERROR.finditer(text):
            add(m.start(), 36, "error details included in responses")
        return found

    if suffix in XML:
        code = XML_COMMENT.sub(lambda m: blank(m.group(0)), text)
        head = code[:3000]
        if "<mapper" in head:
            for m in MAPPER_DOLLAR.finditer(code):
                add(m.start(), 1, "MyBatis ${} inserts text into SQL; use #{} or an allowlist")
        if "<sqlMap" in head:
            for m in IBATIS_DOLLAR.finditer(code):
                add(m.start(), 1, "iBatis $...$ inserts text into SQL; use #...# or an allowlist")
        for weakness, kinds, pattern, message in CODE_RULES:
            if suffix in kinds:
                for m in pattern.finditer(code):
                    add(m.start(), weakness, message)
        return found

    code, comments = split_comments(text, suffix)

    for weakness, kinds, pattern, message in CODE_RULES:
        if suffix in kinds:
            for m in pattern.finditer(code):
                add(m.start(), weakness, message)

    for offset, comment in comments:
        for m in COMMENT_SECRET.finditer(comment):
            add(offset + m.start(), 30, "comment may contain a password or account")

    if suffix in JAVA | JSP:
        if XXE_FACTORY.search(code) and not XXE_GUARD.search(code):
            for m in XXE_FACTORY.finditer(code):
                add(m.start(), 8, "XML parser with no DTD or external entity setting in this file")
        if DIGEST.search(code) and not re.search(r"salt", code, re.IGNORECASE):
            for m in DIGEST.finditer(code):
                add(m.start(), 31, "hash in a file that never mentions a salt")
        for m in EMPTY_CATCH.finditer(code):
            add(m.start(), 37, "empty catch block")
        for m in COOKIE_AGE.finditer(code):
            seconds = cookie_seconds(m.group(1))
            if seconds is not None and seconds > 60 * 60 * 24:
                add(m.start(), 29, f"cookie kept {seconds // 86400} day(s); check that the lifetime is the minimum needed")
        if suffix in JSP:
            for m in re.finditer(r"<%!", code):
                add(m.start(), 44, "JSP declaration: variables here are shared by every user")

    if suffix in JAVA:
        web = WEB_CLASS.search(code)
        if web:
            for m in MAIN.finditer(code):
                add(m.start(), 45, "main() in a web component")
            for m in WEB_SOCKET.finditer(code):
                add(m.start(), 49, "direct socket in a J2EE component")
            add_mutable_fields(code, add)
        add_private_arrays(code, add)

    return found


def add_mutable_fields(code, add):
    """Non-final instance fields of controllers, servlets and services (weakness 44).

    Only lines directly in the body of the first class are considered.
    """
    depth, first_class = 0, None
    pos = 0
    for line in code.split("\n"):
        if first_class is not None and depth == first_class and MUTABLE_FIELD.match(line) \
                and "(" not in line and not re.search(r"\b(?:static|final)\b", line):
            before = code[max(0, pos - 200):pos]
            last = [l for l in before.split("\n") if l.strip()][-1:] or [""]
            if not INJECTED.search(last[0]) and not INJECTED.search(line):
                add(pos + len(line) - len(line.lstrip()), 44, "mutable field in a shared component; check that it holds no request or user data")
        if first_class is None and re.search(r"\bclass\s+\w+", line):
            first_class = depth + 1
        depth += line.count("{") - line.count("}")
        pos += len(line) + 1


def add_private_arrays(code, add):
    """Private array fields returned or assigned directly (weaknesses 46, 47)."""
    fields = set(ARRAY_FIELD.findall(code))
    for name in fields:
        for m in re.finditer(r"\breturn\s+(?:this\.)?" + re.escape(name) + r"\s*;", code):
            add(m.start(), 46, f"private array '{name}' returned directly")
        for m in re.finditer(r"\bthis\." + re.escape(name) + r"\s*=\s*(?!new\b|null\b)(\w+)\s*;", code):
            add(m.start(), 47, f"argument stored in private array '{name}' directly")


def source_files(paths, include_tests):
    kinds = JAVA | JSP | C | XML | CONFIG
    for p in paths:
        p = Path(p)
        if p.is_file():
            if p.suffix.lower() in kinds:
                yield p
            continue
        for f in sorted(p.rglob("*")):
            if not f.is_file() or f.suffix.lower() not in kinds:
                continue
            parts = {x.lower() for x in f.relative_to(p).parts[:-1]}
            if parts & SKIPPED_DIRS or (not include_tests and parts & TEST_DIRS):
                continue
            yield f


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("paths", nargs="+")
    parser.add_argument("--only", help="comma-separated weakness numbers to report, e.g. 1,23,36")
    parser.add_argument("--summary", action="store_true", help="print counts per weakness instead of each line")
    parser.add_argument("--include-tests", action="store_true", help="also scan test folders")
    args = parser.parse_args()

    only = None
    if args.only:
        try:
            only = {int(x) for x in args.only.split(",") if x.strip()}
        except ValueError:
            parser.error("--only takes comma-separated numbers")

    files = list(source_files(args.paths, args.include_tests))
    if not files:
        print("No source files found.", file=sys.stderr)
        return 2

    counts, total = {}, 0
    for f in files:
        for line, weakness, message in sorted(set(scan(f, f.suffix.lower()))):
            if only and weakness not in only:
                continue
            counts[weakness] = counts.get(weakness, 0) + 1
            total += 1
            if not args.summary:
                print(f"{f}:{line}: [보안약점 {weakness} {NAMES[weakness]}] {message}")
    if args.summary:
        for weakness in sorted(counts):
            print(f"보안약점 {weakness} {NAMES[weakness]}: {counts[weakness]}")
    print(f"{total} candidate(s) in {len(files)} file(s).", file=sys.stderr)
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main())
