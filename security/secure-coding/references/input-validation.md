# Input Data Validation and Representation (입력데이터 검증 및 표현)

Weaknesses 1 to 17. They arise when input is not validated, is validated incompletely, or is formatted wrongly before it reaches a query, command, path, page, header or memory buffer.

Each item has the same parts:

- **Find**: what to search for to list candidates
- **Vulnerable** (정탐) and **Not vulnerable** (오탐): how the diagnostic guide judges a candidate
- **Fix**: the guides' countermeasure, with a short example
- **Related**: CWE number, matching design criterion (`design-phase.md`), and the `egovframe` skill rule if one exists

"External input" means any value the user or another system can change: request parameters, headers, cookies, hidden fields, uploaded files, environment variables, socket data, files outside the program, and DB values that users wrote.

## 1. SQL 삽입 (SQL injection)

Unvalidated external input changes the structure of an SQL query, so an attacker can read or modify the database.

- **Find**: `Statement.executeQuery`/`execute` with a concatenated string; `createQuery`, `createNativeQuery`, JDO `newQuery` with concatenation; MyBatis `${}`; iBatis `$name$`; DAO methods that take a SQL fragment (`where`, `orderBy`) as a parameter
- **Vulnerable** `R`
  - External input is concatenated into the query string, even when the object is a `PreparedStatement`. A prepared statement built from a non-constant string is not safe
  - Input passes through layers before it is concatenated: for example a JSP reads `projectid` and passes `"where projectid=" + pid` to a DAO that appends it to its SQL. Follow the call chain
  - MyBatis `${}` or iBatis `$...$` with input; Hibernate or JPA queries built by concatenation
- **Not vulnerable** `R`
  - The query is a constant string and every input is bound: `?` with `setString`, named parameters with `setParameter`, MyBatis `#{}`. The diagnostic guide calls this "basically safe", then adds that a filtering module for query-related input must exist, or the framework must handle it
- **Filter module** `D`: apply the filter requirement to input that changes the query structure (table or column names, sort direction), which binding cannot protect. Do not report a fully bound query only because no filter module exists: the guide's own false-positive examples are bound queries with no filter. Expect a diagnoser to cite the filter sentence, and answer with those examples
- **Fix** `G`: send a constant, precompiled query and bind every value. In MyBatis use `#{}`, never `${}`
- **Fix** `D`: when input must choose an identifier (sort column, table), map it through an allowlist of fixed values. Do not propose a character-stripping filter such as a `SQLFilter(...)` call as the fix: the guides list special characters and keywords to strip, but stripping is bypassable and binding already removes the weakness

```java
// Vulnerable
String sql = "SELECT * FROM board WHERE b_gubun = '" + gubun + "'";
rs = con.createStatement().executeQuery(sql);

// Safe
PreparedStatement ps = con.prepareStatement("SELECT * FROM board WHERE b_gubun = ?");
ps.setString(1, gubun);

// Safe: identifier through an allowlist
String column = Map.of("date", "REG_DT", "title", "TITLE").getOrDefault(sort, "REG_DT");
```

```xml
<!-- Vulnerable -->  WHERE title LIKE '%${keyword}%'
<!-- Safe -->        WHERE title LIKE '%' || #{keyword} || '%'          (Oracle, PostgreSQL)
<!-- Safe -->        WHERE title LIKE CONCAT('%', #{keyword}, '%')      (MySQL, MariaDB)
```

- **Related**: CWE-89 · SR1-1 · `egovframe` SQL rule 10

## 2. 코드 삽입 (code injection)

Input is executed as code by the language's own dynamic execution feature. Unlike OS command injection, it is limited only by what the language can do.

- **Find**: `ScriptEngine.eval`, `new Function(...)` or `eval` built from server-side values in JSP, expression language evaluated from input (SpEL, OGNL) (`D` for SpEL and OGNL: the guides show Java `ScriptEngine.eval`, JSP `new Function(<%=name%>)` and PHP `eval`)
- **Vulnerable** `R`: input reaches a dynamic execution function without validation (the diagnostic guide's PHP examples include `eval` on a request parameter, and user text saved to a file that PHP later parses)
- **Not vulnerable** `R`: the dynamic function never receives external input; input is validated before use (for example only word characters allowed); or input only selects among fixed scripts
- **Fix** `G`: do not use dynamic execution. If it is required, accept only allowlisted values

```java
// Vulnerable
return (String) engine.eval(request.getParameter("src"));

// Safe: input only selects a fixed script
String script = switch (request.getParameter("op")) {
    case "sum" -> SUM_SCRIPT;
    case "avg" -> AVG_SCRIPT;
    default -> throw new IllegalArgumentException();
};
```

- **Related**: CWE-94, CWE-95 · SR1-4

## 3. 경로 조작 및 자원 삽입 (path traversal and resource injection)

Input chooses a file, directory, socket port or other system resource, so an attacker can reach resources the system protects.

- **Find**: `new File`, `FileInputStream`, `FileReader`, `FileOutputStream`, `Paths.get`, `Files.*`, `ServerSocket`/`Socket` ports, C `fopen`, where any part comes from input
- **Vulnerable** `R`
  - Input is part of a path with no check for traversal sequences (`..`, `/`, `\`)
  - Traversal characters are filtered, but the path can still reach the context directory, so web or servlet configuration files can be read
  - Input names a resource directly with no mapping table or list
- **Not vulnerable** `R`
  - The path comes from container functions such as `getRealPath()` or `getContextPath()`
  - Input only selects from a mapping table or fixed list
  - The value comes from a shared system property. A project-specific property file is judged vulnerable (the guide treats it as changeable from outside)
- **Fix** `G`: select resources from a predefined list, or remove `/`, `\` and `..` from file names after a null check
- **Fix** `D`: the guides' example strips every `.`, which also breaks file extensions. Resolve the path and check that it stays inside the base directory instead

```java
// Vulnerable
new FileInputStream("C:/datas/" + request.getParameter("P"));

// Safe
Path base = Paths.get("/data/files").toRealPath();
Path target = base.resolve(fileName).normalize();
if (!target.startsWith(base)) throw new SecurityException("invalid path");
```

```c
/* C: reject traversal and absolute paths before fopen (the guide uses regcomp/regexec for "..") */
if (filename == NULL || strstr(filename, "..") != NULL || strpbrk(filename, "/\\") != NULL) { /* error */ }
```

- **Related**: CWE-22, CWE-99 · SR1-4 (SR1-10 requirement 3 covers download file names, though the mapping table lists only SR1-4)

## 4. 크로스사이트 스크립트 (cross-site scripting, XSS)

Input is written into a page without encoding, so script runs with the viewer's rights. The guides describe reflected, stored and DOM-based XSS.

- **Find**: JSP `<%= %>`, `${...}` outside `<c:out>`, `<c:out escapeXml="false">`, `response.getWriter().print`, `document.write` or `innerHTML` built from input, values from `getQueryString()`
- **Vulnerable** `R`
  - A value printed to a web page comes from input, or from a DB column that users wrote (board titles, contents, profiles), and passes no adequate filter
  - `@ModelAttribute` values written straight to the response
  - A filter that only removes `<script>` (bypassed by `<sc<script>ript>`)
  - Input printed inside an HTML comment (closed with `-->`)
  - DOM-based: a request parameter builds a `document.write` argument; a DOM filter that misses `;`, `%` or `-`
- **Not vulnerable** `R`
  - Output through JSTL `<c:out>` or with `escapeXml` on, or through a framework that encodes
  - The value is not a string (a number), is fixed by the program, is cut to a few characters with `substring`, or is printed to the console rather than a page
  - Input is used only as part of a URL the browser navigates to (per the guide). `D`: this holds only when the input cannot set the scheme; input that becomes the whole `href` or `src` can be `javascript:...`, so report that case
  - A DB value that users cannot change, such as a menu name. The guide notes that static tools cannot tell this apart, so check where the column is written
- **Fix** `G`: encode output for its context, with JSTL or an established library (NAVER Lucy-XSS-Filter, OWASP ESAPI, OWASP Java Encoder). For boards that allow HTML, allow only an allowlist of tags
- **Fix** `D`: the guides' `replaceAll` example uses invalid regular expressions (`"("`). Use an encoder library rather than hand-written replacement

```jsp
<%-- Vulnerable --%>  검색어 : <%= keyword %>
<%-- Safe --%>        검색어 : <c:out value="${keyword}"/>
<script>document.write("keyword:" + "<%= Encode.forJavaScript(keyword) %>");</script>
```

- **Related**: CWE-79 · SR1-5

## 5. 운영체제 명령어 삽입 (OS command injection)

Input becomes all or part of an operating system command.

- **Find**: `Runtime.getRuntime().exec`, `ProcessBuilder`, C `system`, `popen`, `exec*`
- **Vulnerable** `R`: input, directly or through another method (for example a process ID read from a request), is part of the executed command
- **Not vulnerable** `R`: the command is chosen from a fixed allowlist; the value is a shared system property; the value is produced by the program and cannot contain separators or `..` (for example `File.getName()` of a file the program listed)
- **Fix** `G`: do not pass commands from the web interface to the server. If input must affect the command, choose among predefined values. The guides also show removing `| ; & :` and `> >>`
- **Fix** `D`: the guides' filter example `replaceAll("|", "")` treats `|` as a regex operator and removes nothing. Prefer an allowlist and pass arguments as a list so no shell parses them

```java
// Vulnerable
Runtime.getRuntime().exec("cmd.exe /c backuplog.bat " + request.getParameter("date"));

// Safe
if (!DATE.matcher(date).matches()) throw new IllegalArgumentException();
new ProcessBuilder("/opt/app/bin/backuplog", date).start();   // argument list, no shell
// Windows .bat/.cmd files always run through cmd.exe, which parses arguments: validate them even with ProcessBuilder
```

```c
/* C: refuse any shell metacharacter before system() */
if (strpbrk(cmd_data, "|&;:>") != NULL) return -1;
```

- **Related**: CWE-78 · SR1-4

## 6. 위험한 형식 파일 업로드 (unrestricted upload of dangerous file types)

Server-executable files (jsp, php, asp and so on) can be uploaded and then requested directly.

- **Find**: `MultipartFile`, `getOriginalFilename`, `MultipartRequest.getFilesystemName`, `transferTo`, upload directories under the web root
- **Vulnerable** `R`: a file name from the request is used and the extension is not checked; the extension check is case-sensitive, so `JSP`, `Jsp` or `PHP` pass
- **Not vulnerable** `R`: only allowed extensions are accepted; the stored file name is changed to one outsiders cannot guess; `getOriginalFilename()` is called but its value is not used to store the file
- **Fix** `G`: allowlist extensions (compare the part after the last `.` in lower case), store files outside the web document root under random names, map original and stored names in the DB, remove execute permission, and limit size (the example in SR1-10: Spring `maxUploadSize` 20 MB). Check MIME type and extension together

```java
String ext = name.substring(name.lastIndexOf('.') + 1).toLowerCase(Locale.ROOT);
if (!Set.of("gif", "jpg", "png").contains(ext)) throw new IllegalArgumentException();
Path stored = UPLOAD_DIR.resolve(UUID.randomUUID().toString());   // outside web root
```

- **Related**: CWE-434 · SR1-10

## 7. 신뢰되지 않는 URL 주소로 자동접속 연결 (open redirect)

Input decides where the server redirects the user, which enables phishing.

- **Find**: `response.sendRedirect`, `"redirect:" + ...` in Spring, `RedirectView`, `Location` headers built from input
- **Vulnerable** `R`: the redirect target (or the code and action values that build it) comes from input without an allowlist
- **Not vulnerable** `R`: the target is not external input (for example `getContextPath()`), or input is checked against an allowlist
- **Fix** `G`: keep allowed URLs and domains in an allowlist; let input only select an entry

```java
private static final String[] ALLOWED = { "/main.do", "/login.jsp", "/list.do" };
String target = ALLOWED[Integer.parseInt(request.getParameter("redirect"))];  // catch NumberFormat and index errors
response.sendRedirect(target);
```

- **Related**: CWE-601 · SR1-7

## 8. 부적절한 XML 외부개체 참조 (XML external entity, XXE)

A parser processes external entities in an untrusted XML document, exposing server files or consuming resources.

- **Find**: `DocumentBuilderFactory`, `SAXParserFactory`, `XMLInputFactory`, `SchemaFactory`, `Validator`, `TransformerFactory`, JAXB `Unmarshaller` on uploaded or received XML
- **Vulnerable** `R`: untrusted XML is parsed with no code that disables external entities or DTDs
- **Not vulnerable** `R`: the parser sets `XMLConstants.ACCESS_EXTERNAL_DTD` and `ACCESS_EXTERNAL_SCHEMA` to `""`, or for StAX `SUPPORT_DTD` and `IS_SUPPORTING_EXTERNAL_ENTITIES` to `false`
- **Fix** `G`: disable DTDs completely; if that is not possible, disable external entities and external DTD loading in the way each parser supports

```java
DocumentBuilderFactory dbf = DocumentBuilderFactory.newInstance();
dbf.setFeature("http://apache.org/xml/features/disallow-doctype-decl", true);
dbf.setFeature("http://xml.org/sax/features/external-general-entities", false);
dbf.setFeature("http://xml.org/sax/features/external-parameter-entities", false);
dbf.setXIncludeAware(false);
dbf.setExpandEntityReferences(false);
```

- **Related**: CWE-611 · SR1-2

## 9. XML 삽입 (XPath and XQuery injection)

Input changes the structure of an XPath or XQuery expression, exposing data or bypassing authentication.

- **Find**: `XPath.compile`/`evaluate`, `prepareExpression`, XQuery execution with a concatenated expression
- **Vulnerable** `R`: input is concatenated into the expression (for example `' or ''='` as a password) and no filtering module or framework protection exists
- **Not vulnerable** `R`: the expression binds input as a variable, or a filtering module removes XPath metacharacters
- **Fix** `G`: use parameterized XQuery (`declare variable ... external` with bound values, or `bindString`). If that is impossible, remove characters such as `' [ ] ( ) : , * /` before building the expression

```java
// Vulnerable
xpath.compile("//users/user[login/text()='" + id + "' and password/text()='" + pw + "']");

// Safe: XQuery with external variables
XQPreparedExpression expr = conn.prepareExpression(
    "declare variable $id external; doc('users.xml')/userlist/user[uname=$id]");
expr.bindString(new QName("id"), id, null);
```

- **Related**: CWE-643, CWE-652 · SR1-2

## 10. LDAP 삽입 (LDAP injection)

Input changes an LDAP filter or base DN.

- **Find**: `DirContext.search`, `LdapTemplate.search`, filter or DN strings built from input; C `ldap_search_ext_s`
- **Vulnerable** `R`: input builds the search filter (for example `*` makes `(name=*)` always true) or the search base, with no filtering module
- **Not vulnerable** `R`: a filtering module or framework escapes or rejects LDAP special characters
- **Fix** `G`: remove or escape `= + < > # ; \` and `* ( )` in values used in filters and DNs. The development guide calls character removal a partial reduction of risk, not a full fix. Do not use anonymous binds
- **Fix** `D`: prefer the library's encoder (`LdapEncoder.filterEncode` in Spring LDAP, or a filter built with `EqualsFilter`) over hand-written checks

```java
// Vulnerable
String filter = "(&(sn=" + userSN + ")(userPassword=" + userPassword + "))";

// Safe
if (!userSN.matches("[\\w\\s]*") || !userPassword.matches("\\w*")) throw new IllegalArgumentException();
```

- **Related**: CWE-90 · SR1-3

## 11. 크로스사이트 요청 위조 (cross-site request forgery, CSRF)

A logged-in user's browser is made to send a state-changing request the user did not intend.

- **Find**: handlers that change data or permissions (register, modify, delete, change password, grant role), forms that use GET for such actions, CSRF configuration in Spring Security
- **Vulnerable** `R`: the important function has no request validity check, or relies only on credentials the browser sends automatically (session cookie, client IP, TLS client certificate)
- **Not vulnerable** `R`: a random token is stored in the session when the form is served, sent as a hidden field, and compared on submission
- **Not vulnerable** `G`: the framework's CSRF protection covers the request. SR1-6 names Spring Security 3.2 and later among the libraries that provide it; confirm that it is enabled and not disabled for the URL
- **Fix** `G`: use POST for input forms, use a per-session token, and require re-authentication for important functions. CAPTCHA is suggested where XSS could steal tokens

```java
session.setAttribute("CSRF_TOKEN", UUID.randomUUID().toString());     // when serving the form
// <input type="hidden" name="csrf_token" value="${CSRF_TOKEN}"/>
String p = request.getParameter("csrf_token");
String s = (String) session.getAttribute("CSRF_TOKEN");
if (p == null || s == null || !MessageDigest.isEqual(p.getBytes(), s.getBytes())) throw new AccessDeniedException("CSRF");
```

- **Related**: CWE-352 · SR1-6

## 12. 서버사이드 요청 위조 (server-side request forgery, SSRF)

Input decides which URL or host the server calls, so an attacker reaches internal services.

- **Find**: `URL.openConnection`, `openStream`, `RestTemplate`, `WebClient`, `HttpClient` with a URL or host from input or from an editable properties file
- **Vulnerable** `R`
  - Input (or a properties value, which the guide treats as possibly tampered) is passed to the call with no validation
  - A host parameter can be pointed at an internal address such as `192.168.x.x:8080/secrets.txt`
- **Not vulnerable** `R`: input only selects from predefined URLs. A blocklist of the cloud metadata address `169.254.169.254` is judged not vulnerable in the guide's example
- **Needs review** `R`: a blocklist of internal ranges (an `isPrivateIP()` check) is not automatically safe. The guide asks you to check it against bypasses: decimal, hex, octal or overflowed IP notation, forms without dots, Unicode and IDN normalization, `@` and `#` tricks, and other schemes (`file://`, `ldap://`)
- **Fix** `G`: allowlist the services the server may call. If arbitrary URLs are a requirement, blocklist internal addresses. Authenticate requests even inside the internal network

```java
private static final Map<String, URI> SERVICES = Map.of("weather", URI.create("https://api.example.go.kr/weather"));
URI target = SERVICES.get(request.getParameter("svc"));
if (target == null) throw new IllegalArgumentException();
```

- **Related**: CWE-918 · SR1-4, SR2-1

## 13. HTTP 응답분할 (HTTP response splitting)

CR or LF in input placed in a response header splits the response, enabling XSS and cache poisoning.

- **Find**: `addCookie`, `setHeader`, `addHeader`, `sendRedirect` with input
- **Vulnerable** `R`: input reaches a header (including a redirect URL or a `Content-Disposition` file name) with no CR/LF removal
- **Not vulnerable** `R`: `\r` and `\n` are removed first; the value comes from `getContextPath()`; the value is numeric
- **Fix** `G`: null-check, then remove CR and LF before using input in a header

```java
String lastLogin = request.getParameter("last_login");
if (lastLogin == null) lastLogin = "";
response.addCookie(new Cookie("LASTLOGIN", lastLogin.replaceAll("[\\r\\n]", "")));
```

- **Related**: CWE-113 · SR1-7

## 14. 정수형 오버플로우 (integer overflow)

A value outside the range of its integer type wraps to a small or negative number. It matters most in loop bounds, memory allocation and copy sizes.

- **Find**: array sizes, loop limits, `malloc` sizes and index arithmetic that use parsed input (`Integer.parseInt`, `atoi`)
- **Vulnerable** `R`: input decides an array size or index with no range check (including negative values); a counter can grow past its limit unchecked
- **Not vulnerable** `R`: the value comes from a method whose result stays within range (for example `InputStream.available()`); the input has a natural bound (an HTTP header value); the value is the number of program arguments, which cannot realistically reach the integer limit; the value is not external input
- **Fix** `G`: know the range of each type, check the range of results, and check input used for allocation
- **Fix** `D`: the guides' Java example checks only `< 0`. Also enforce an upper bound, and use `Math.addExact` or `Math.multiplyExact` for arithmetic on input

```java
int count = Integer.parseInt(param);
if (count < 0 || count > MAX_ITEMS) throw new IllegalArgumentException();
String[] items = new String[count];
```

```c
int idx = atoi(argv[1]);
if (idx >= 0 && idx < (int)(sizeof(table) / sizeof(table[0]))) value = table[idx];
```

- **Related**: CWE-190 · SR1-9

## 15. 보안기능 결정에 사용되는 부적절한 입력값 (untrusted input in a security decision)

Authentication, authorization or pricing decisions trust values the client controls: cookies, environment variables, parameters and hidden fields.

- **Find**: variables that decide login state, role, user identity or price; reads of cookies, hidden fields and headers near those decisions
- **Vulnerable** `R`: the decision uses external input as it is, for example `authenticated=true` or the user ID stored in a plain cookie, or a price sent in a hidden field
- **Not vulnerable** `R`: the decision uses values verified on the server (session, DB). In the guide's example the hidden `price` field is received but the price is looked up on the server
- **Fix** `G`: keep state and security-relevant data on the server (session or DB) and run checks there. When an external authentication service hands over an identity, verify its token (signature and expiry) instead of trusting a user ID from the client. If a cookie must carry such data, encrypt it on the server and protect it with a MAC

```java
// Vulnerable: trusts the client's member ID
String tokenB = tokenService.issue(request.getParameter("memberId"));

// Safe: identity comes from a verified token
String memberId = tokenService.verifyAndExtract(request.getParameter("tokenA"));  // checks signature and expiry
String tokenB = tokenService.issue(memberId);

// Safe: price from the server, not the hidden field
int total = quantity * productService.getPrice(itemId);
```

- **Related**: CWE-807 · SR1-9

## 16. 메모리 버퍼 오버플로우 (memory buffer overflow)

A program reads or writes outside an allocated buffer, on the stack or the heap. It mainly concerns C and C++.

- **Find**: `gets`, `strcpy`, `strcat`, `sprintf`, `memcpy`, `scanf("%s")`, array writes in loops, fixed-size buffers filled from input
- **Vulnerable** `R`
  - Data is written to a buffer without checking that it fits; input decides a size or length that is not checked against the buffer
  - Input is copied into a fixed buffer (for example 16 bytes, or a 64-byte host name) with no length check
  - An index decreases in a loop (for example trimming trailing spaces) without a check that it stays at or above 0
  - A string buffer may be left without a terminating null
- **Not vulnerable** `R`: sizes are compared before every write, indexes are checked for both bounds (including negative values), loop bounds are checked, and strings are null-terminated inside the buffer
- **Fix** `G`: give buffers an adequate size, read and write only within it, and write the terminating null inside the buffer. The design criterion SR1-8 adds platform protections (non-executable stack, ASLR, StackGuard) and a list of banned functions (weakness 49)

```c
/* Vulnerable: copies the size of the whole struct into field x */
memcpy(cv_struct.x, SRC_STR, sizeof(cv_struct));

/* Safe: copy at most the field size, never past the source string, and terminate */
strncpy(cv_struct.x, SRC_STR, sizeof(cv_struct.x) - 1);
cv_struct.x[sizeof(cv_struct.x) - 1] = '\0';

/* Vulnerable */ gets(message);
/* Safe */       fgets(message, sizeof(message), stdin);
```

- In Java, out-of-range array access raises an exception instead of corrupting memory. Report Java code under weakness 14 or 39 when its index or size comes from input, not under 16 (`D`: the guides give no Java example for 16)
- **Related**: CWE-119 · SR1-8

## 17. 포맷 스트링 삽입 (format string injection)

Input is used as the format string of an output function, so an attacker can read memory or, in C, write it (`%n`). The guides note that Java is affected too: format specifiers can expose other arguments.

- **Find**: C `printf`, `fprintf`, `sprintf`, `snprintf`, `syslog` with a non-literal format; Java `String.format`, `printf`, `MessageFormat.format` with a format built from input
- **Vulnerable** `R`: input builds the format string, for example `%1$tY-%1$tm-%1$te` entered in Java exposes a date argument
- **Not vulnerable** `R`: the format string is a literal argument, input does not build it, the number of specifiers matches the number of arguments, and output length is limited
- **Fix** `G`: never use input as a format string; use `%s` and pass input as a later argument. Never use `%n` or `%hn`

```java
// Vulnerable
System.out.printf(args[0] + " did not match! HINT: It was issued on %1$terd of some month", validDate);
// Safe
System.out.printf("%s did not match! HINT: It was issued on %2$terd of some month", args[0], validDate);
```

```c
/* Vulnerable */ fprintf(stderr, msg);
/* Safe */       fputs(msg, stderr);     /* or fprintf(stderr, "%s", msg); */
```

- **Related**: CWE-134 · SR1-8
