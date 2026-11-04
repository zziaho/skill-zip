# 입력데이터 검증 및 표현

보안약점 1번부터 17번까지입니다. 입력을 검증하지 않거나 불완전하게 검증하거나 잘못된 형식으로 처리한 채로, 그 입력이 쿼리, 명령어, 경로, 페이지, 헤더, 메모리 버퍼에 도달할 때 발생합니다.

각 항목은 같은 구성을 따릅니다.

- **탐색**: 후보를 나열하려고 검색할 대상
- **정탐**(Vulnerable)과 **오탐**(Not vulnerable): 진단가이드가 후보를 판단하는 방법
- **조치**: 가이드가 제시하는 대응 방안과 짧은 예시
- **관련**: CWE 번호, 대응하는 설계 기준(`design-phase_ko.md`), `egovframe` 스킬에 해당 규칙이 있으면 그 규칙

"외부 입력"은 사용자나 다른 시스템이 바꿀 수 있는 모든 값을 뜻합니다. 요청 파라미터, 헤더, 쿠키, hidden 필드, 업로드 파일, 환경 변수, 소켓 데이터, 프로그램 밖의 파일, 사용자가 작성한 DB 값이 여기에 해당합니다.

## 1. SQL 삽입

검증되지 않은 외부 입력이 SQL 쿼리의 구조를 바꾸기 때문에, 공격자가 데이터베이스를 읽거나 수정할 수 있습니다.

- **탐색**: 문자열을 이어 붙인 `Statement.executeQuery`/`execute`, 문자열을 이어 붙인 `createQuery`, `createNativeQuery`, JDO `newQuery`, MyBatis `${}`, iBatis `$name$`, SQL 조각(`where`, `orderBy`)을 파라미터로 받는 DAO 메서드
- **정탐** `R`
  - 외부 입력을 쿼리 문자열에 이어 붙입니다. 객체가 `PreparedStatement`여도 마찬가지입니다. 상수가 아닌 문자열로 만든 prepared statement는 안전하지 않습니다
  - 입력이 여러 계층을 거친 뒤에 이어 붙여집니다. 예를 들어 JSP가 `projectid`를 읽어 `"where projectid=" + pid`를 DAO에 넘기고, DAO가 이를 SQL에 덧붙이는 경우입니다. 호출 경로를 끝까지 따라갑니다
  - 입력이 들어가는 MyBatis `${}`나 iBatis `$...$`, 문자열을 이어 붙여 만든 Hibernate나 JPA 쿼리
- **오탐** `R`
  - 쿼리가 상수 문자열이고 모든 입력이 바인딩됩니다. `?`와 `setString`, 이름 있는 파라미터와 `setParameter`, MyBatis `#{}`가 해당합니다. 진단가이드는 이를 "기본적으로 안전하다"고 하면서, 쿼리와 관련된 입력에 대한 필터링 모듈이 있거나 프레임워크가 이를 처리해야 한다는 조건을 덧붙입니다
- **필터링 모듈** `D`: 필터링 요구사항은 테이블 이름, 컬럼 이름, 정렬 방향처럼 쿼리 구조를 바꾸는 입력에 적용합니다. 이런 입력은 바인딩으로 보호할 수 없기 때문입니다. 모든 값을 바인딩한 쿼리를 필터링 모듈이 없다는 이유만으로 보고하지 않습니다. 가이드의 오탐 예시도 필터가 없는 바인딩 쿼리입니다. 진단원이 필터에 대한 문장을 인용할 것으로 예상하고, 그 예시로 대응합니다
- **조치** `G`: 상수로 된 사전 컴파일 쿼리를 보내고 모든 값을 바인딩합니다. MyBatis에서는 `${}`를 쓰지 말고 `#{}`를 사용합니다
- **조치** `D`: 입력이 식별자(정렬 컬럼, 테이블)를 선택해야 한다면 고정된 값의 허용 목록으로 매핑합니다. `SQLFilter(...)` 호출 같은 문자 제거 필터를 조치 방법으로 제안하지 않습니다. 가이드는 제거할 특수문자와 키워드를 나열하지만, 제거 방식은 우회할 수 있고 바인딩만으로도 보안약점이 이미 사라지기 때문입니다

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

- **관련**: CWE-89 · SR1-1 · `egovframe` SQL 규칙 10

## 2. 코드 삽입

입력이 언어 자체의 동적 실행 기능으로 코드처럼 실행됩니다. 운영체제 명령어 삽입과 달리, 그 언어가 할 수 있는 일이라면 무엇이든 가능합니다.

- **탐색**: `ScriptEngine.eval`, JSP에서 서버 측 값으로 만든 `new Function(...)`이나 `eval`, 입력으로 평가되는 표현 언어(SpEL, OGNL) (SpEL과 OGNL에 대해서만 `D`: 가이드는 Java `ScriptEngine.eval`, JSP `new Function(<%=name%>)`, PHP `eval`을 제시합니다)
- **정탐** `R`: 입력이 검증 없이 동적 실행 함수에 도달합니다(진단가이드의 PHP 예시에는 요청 파라미터에 대한 `eval`과, 파일에 저장한 사용자 텍스트를 PHP가 나중에 파싱하는 경우가 있습니다)
- **오탐** `R`: 동적 함수가 외부 입력을 전혀 받지 않습니다. 사용하기 전에 입력을 검증합니다(예: 단어 문자만 허용). 입력이 고정된 스크립트 중 하나를 선택하는 데에만 쓰입니다
- **조치** `G`: 동적 실행을 사용하지 않습니다. 꼭 필요하다면 허용 목록에 있는 값만 받습니다

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

- **관련**: CWE-94, CWE-95 · SR1-4

## 3. 경로 조작 및 자원 삽입

입력이 파일, 디렉터리, 소켓 포트 같은 시스템 자원을 선택하기 때문에, 공격자가 시스템이 보호하는 자원에 접근할 수 있습니다.

- **탐색**: 일부라도 입력에서 온 `new File`, `FileInputStream`, `FileReader`, `FileOutputStream`, `Paths.get`, `Files.*`, `ServerSocket`/`Socket` 포트, C `fopen`
- **정탐** `R`
  - 입력이 경로의 일부이고 경로 순회 문자열(`..`, `/`, `\`)을 검사하지 않습니다
  - 경로 순회 문자를 필터링하지만 경로가 여전히 컨텍스트 디렉터리에 도달할 수 있어서, 웹 설정 파일이나 서블릿 설정 파일을 읽을 수 있습니다
  - 매핑 테이블이나 목록 없이 입력이 자원 이름을 직접 지정합니다
- **오탐** `R`
  - 경로가 `getRealPath()`나 `getContextPath()` 같은 컨테이너 함수에서 옵니다
  - 입력이 매핑 테이블이나 고정된 목록에서 선택하는 데에만 쓰입니다
  - 값이 공용 시스템 프로퍼티에서 옵니다. 프로젝트 전용 프로퍼티 파일은 정탐으로 판단합니다(가이드는 이를 외부에서 변경할 수 있는 값으로 봅니다)
- **조치** `G`: 미리 정의한 목록에서 자원을 선택하게 하거나, null 검사를 한 뒤에 파일 이름에서 `/`, `\`, `..`를 제거합니다
- **조치** `D`: 가이드의 예시는 `.`를 모두 제거하므로 파일 확장자까지 깨집니다. 대신 경로를 해석한 뒤에 기준 디렉터리 안에 머무르는지 확인합니다

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

- **관련**: CWE-22, CWE-99 · SR1-4 (SR1-10 요구사항 3은 다운로드 파일 이름을 다루지만, 대응표에는 SR1-4만 나열되어 있습니다)

## 4. 크로스사이트 스크립트

입력을 인코딩하지 않고 페이지에 출력하기 때문에, 열람하는 사용자의 권한으로 스크립트가 실행됩니다. 가이드는 반사형, 저장형, DOM 기반 XSS를 설명합니다.

- **탐색**: JSP `<%= %>`, `<c:out>` 밖의 `${...}`, `<c:out escapeXml="false">`, `response.getWriter().print`, 입력으로 만든 `document.write`나 `innerHTML`, `getQueryString()`에서 가져온 값
- **정탐** `R`
  - 웹 페이지에 출력하는 값이 입력에서 오거나 사용자가 작성한 DB 컬럼(게시판 제목, 내용, 프로필)에서 오는데, 적절한 필터를 거치지 않습니다
  - `@ModelAttribute` 값을 응답에 그대로 씁니다
  - `<script>`만 제거하는 필터입니다(`<sc<script>ript>`로 우회됩니다)
  - HTML 주석 안에 입력을 출력합니다(`-->`로 주석을 닫을 수 있습니다)
  - DOM 기반: 요청 파라미터로 `document.write` 인자를 만듭니다. `;`, `%`, `-`를 걸러 내지 못하는 DOM 필터입니다
- **오탐** `R`
  - JSTL `<c:out>`이나 `escapeXml`을 켠 상태로 출력하거나, 인코딩을 수행하는 프레임워크로 출력합니다
  - 값이 문자열이 아니거나(숫자), 프로그램이 고정한 값이거나, `substring`으로 몇 글자만 잘라 낸 값이거나, 페이지가 아니라 콘솔에 출력합니다
  - 입력이 브라우저가 이동할 URL의 일부로만 쓰입니다(가이드 기준). `D`: 입력이 스킴을 지정할 수 없을 때만 성립합니다. 입력이 `href`나 `src` 전체가 되면 `javascript:...`가 될 수 있으므로 이 경우는 보고합니다
  - 메뉴 이름처럼 사용자가 바꿀 수 없는 DB 값입니다. 가이드는 정적 도구가 이를 구분하지 못한다고 설명하므로, 해당 컬럼이 어디에서 기록되는지 확인합니다
- **조치** `G`: JSTL이나 검증된 라이브러리(NAVER Lucy-XSS-Filter, OWASP ESAPI, OWASP Java Encoder)로 출력 문맥에 맞게 인코딩합니다. HTML을 허용하는 게시판은 허용 목록에 있는 태그만 허용합니다
- **조치** `D`: 가이드의 `replaceAll` 예시는 올바르지 않은 정규식(`"("`)을 사용합니다. 직접 작성한 치환 대신 인코더 라이브러리를 사용합니다

```jsp
<%-- Vulnerable --%>  검색어 : <%= keyword %>
<%-- Safe --%>        검색어 : <c:out value="${keyword}"/>
<script>document.write("keyword:" + "<%= Encode.forJavaScript(keyword) %>");</script>
```

- **관련**: CWE-79 · SR1-5

## 5. 운영체제 명령어 삽입

입력이 운영체제 명령어의 전체나 일부가 됩니다.

- **탐색**: `Runtime.getRuntime().exec`, `ProcessBuilder`, C `system`, `popen`, `exec*`
- **정탐** `R`: 입력이 직접, 혹은 다른 메서드를 거쳐서(예: 요청에서 읽은 프로세스 ID) 실행되는 명령어의 일부가 됩니다
- **오탐** `R`: 명령어를 고정된 허용 목록에서 선택합니다. 값이 공용 시스템 프로퍼티입니다. 값을 프로그램이 만들어 내므로 구분자나 `..`를 포함할 수 없습니다(예: 프로그램이 나열한 파일의 `File.getName()`)
- **조치** `G`: 웹 인터페이스에서 서버로 명령어를 넘기지 않습니다. 입력이 명령어에 영향을 줘야 한다면 미리 정의한 값 중에서 선택하게 합니다. 가이드는 `| ; & :`와 `> >>`를 제거하는 방법도 제시합니다
- **조치** `D`: 가이드의 필터 예시 `replaceAll("|", "")`는 `|`를 정규식 연산자로 취급하므로 아무것도 제거하지 못합니다. 허용 목록을 우선 사용하고, 인자를 목록으로 전달해서 셸이 해석하지 않게 합니다

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

- **관련**: CWE-78 · SR1-4

## 6. 위험한 형식 파일 업로드

서버에서 실행되는 파일(jsp, php, asp 등)을 업로드한 뒤에 직접 요청할 수 있습니다.

- **탐색**: `MultipartFile`, `getOriginalFilename`, `MultipartRequest.getFilesystemName`, `transferTo`, 웹 루트 아래의 업로드 디렉터리
- **정탐** `R`: 요청에서 받은 파일 이름을 사용하고 확장자를 검사하지 않습니다. 확장자 검사가 대소문자를 구분하므로 `JSP`, `Jsp`, `PHP`가 통과합니다
- **오탐** `R`: 허용된 확장자만 받습니다. 저장하는 파일 이름을 외부인이 추측할 수 없는 이름으로 바꿉니다. `getOriginalFilename()`을 호출하지만 그 값으로 파일을 저장하지 않습니다
- **조치** `G`: 확장자 허용 목록을 사용합니다(마지막 `.` 뒤의 부분을 소문자로 바꿔서 비교합니다). 파일을 웹 문서 루트 밖에 무작위 이름으로 저장하고, 원래 이름과 저장한 이름의 대응 관계를 DB에 기록하며, 실행 권한을 제거하고, 크기를 제한합니다(SR1-10의 예시: Spring `maxUploadSize` 20 MB). MIME 타입과 확장자를 함께 검사합니다

```java
String ext = name.substring(name.lastIndexOf('.') + 1).toLowerCase(Locale.ROOT);
if (!Set.of("gif", "jpg", "png").contains(ext)) throw new IllegalArgumentException();
Path stored = UPLOAD_DIR.resolve(UUID.randomUUID().toString());   // outside web root
```

- **관련**: CWE-434 · SR1-10

## 7. 신뢰되지 않는 URL 주소로 자동접속 연결

입력이 서버가 사용자를 이동시키는 위치를 결정하므로 피싱에 악용됩니다.

- **탐색**: `response.sendRedirect`, Spring의 `"redirect:" + ...`, `RedirectView`, 입력으로 만든 `Location` 헤더
- **정탐** `R`: 리다이렉트 대상(또는 대상을 만드는 코드와 동작 값)이 허용 목록 없이 입력에서 옵니다
- **오탐** `R`: 대상이 외부 입력이 아닙니다(예: `getContextPath()`). 또는 입력을 허용 목록과 대조해서 검사합니다
- **조치** `G`: 허용하는 URL과 도메인을 허용 목록에 보관하고, 입력은 그 목록의 항목을 선택하는 데에만 사용합니다

```java
private static final String[] ALLOWED = { "/main.do", "/login.jsp", "/list.do" };
String target = ALLOWED[Integer.parseInt(request.getParameter("redirect"))];  // catch NumberFormat and index errors
response.sendRedirect(target);
```

- **관련**: CWE-601 · SR1-7

## 8. 부적절한 XML 외부개체 참조

파서가 신뢰할 수 없는 XML 문서의 외부 개체를 처리하기 때문에, 서버 파일이 노출되거나 자원이 소모됩니다.

- **탐색**: 업로드하거나 수신한 XML을 처리하는 `DocumentBuilderFactory`, `SAXParserFactory`, `XMLInputFactory`, `SchemaFactory`, `Validator`, `TransformerFactory`, JAXB `Unmarshaller`
- **정탐** `R`: 신뢰할 수 없는 XML을 파싱하면서 외부 개체나 DTD를 비활성화하는 코드가 없습니다
- **오탐** `R`: 파서가 `XMLConstants.ACCESS_EXTERNAL_DTD`와 `ACCESS_EXTERNAL_SCHEMA`를 `""`로 설정하거나, StAX에서 `SUPPORT_DTD`와 `IS_SUPPORTING_EXTERNAL_ENTITIES`를 `false`로 설정합니다
- **조치** `G`: DTD를 완전히 비활성화합니다. 그럴 수 없다면 각 파서가 지원하는 방식으로 외부 개체와 외부 DTD 로딩을 비활성화합니다

```java
DocumentBuilderFactory dbf = DocumentBuilderFactory.newInstance();
dbf.setFeature("http://apache.org/xml/features/disallow-doctype-decl", true);
dbf.setFeature("http://xml.org/sax/features/external-general-entities", false);
dbf.setFeature("http://xml.org/sax/features/external-parameter-entities", false);
dbf.setXIncludeAware(false);
dbf.setExpandEntityReferences(false);
```

- **관련**: CWE-611 · SR1-2

## 9. XML 삽입

입력이 XPath나 XQuery 표현식의 구조를 바꾸기 때문에, 데이터가 노출되거나 인증이 우회됩니다.

- **탐색**: 문자열을 이어 붙인 표현식을 사용하는 `XPath.compile`/`evaluate`, `prepareExpression`, XQuery 실행
- **정탐** `R`: 입력을 표현식에 이어 붙이고(예: 패스워드에 `' or ''='` 입력), 필터링 모듈이나 프레임워크의 보호가 없습니다
- **오탐** `R`: 표현식이 입력을 변수로 바인딩하거나, 필터링 모듈이 XPath 메타 문자를 제거합니다
- **조치** `G`: 파라미터화한 XQuery를 사용합니다(`declare variable ... external`과 바인딩한 값, 또는 `bindString`). 그럴 수 없다면 표현식을 만들기 전에 `' [ ] ( ) : , * /` 같은 문자를 제거합니다

```java
// Vulnerable
xpath.compile("//users/user[login/text()='" + id + "' and password/text()='" + pw + "']");

// Safe: XQuery with external variables
XQPreparedExpression expr = conn.prepareExpression(
    "declare variable $id external; doc('users.xml')/userlist/user[uname=$id]");
expr.bindString(new QName("id"), id, null);
```

- **관련**: CWE-643, CWE-652 · SR1-2

## 10. LDAP 삽입

입력이 LDAP 필터나 기준 DN을 바꿉니다.

- **탐색**: `DirContext.search`, `LdapTemplate.search`, 입력으로 만든 필터나 DN 문자열, C `ldap_search_ext_s`
- **정탐** `R`: 필터링 모듈 없이 입력으로 검색 필터를 만들거나(예: `*`를 넣으면 `(name=*)`이 항상 참이 됩니다) 검색 기준을 만듭니다
- **오탐** `R`: 필터링 모듈이나 프레임워크가 LDAP 특수문자를 이스케이프하거나 거부합니다
- **조치** `G`: 필터와 DN에 사용하는 값에서 `= + < > # ; \`와 `* ( )`를 제거하거나 이스케이프합니다. 개발보안 가이드는 문자를 제거하는 방식이 위험을 일부 줄일 뿐 완전한 조치는 아니라고 설명합니다. 익명 바인드를 사용하지 않습니다
- **조치** `D`: 직접 작성한 검사보다 라이브러리의 인코더(Spring LDAP의 `LdapEncoder.filterEncode`, 또는 `EqualsFilter`로 만든 필터)를 우선 사용합니다

```java
// Vulnerable
String filter = "(&(sn=" + userSN + ")(userPassword=" + userPassword + "))";

// Safe
if (!userSN.matches("[\\w\\s]*") || !userPassword.matches("\\w*")) throw new IllegalArgumentException();
```

- **관련**: CWE-90 · SR1-3

## 11. 크로스사이트 요청 위조

로그인한 사용자의 브라우저가 사용자가 의도하지 않은 상태 변경 요청을 보내게 됩니다.

- **탐색**: 데이터나 권한을 변경하는 핸들러(등록, 수정, 삭제, 패스워드 변경, 권한 부여), 이런 동작에 GET을 사용하는 폼, Spring Security의 CSRF 설정
- **정탐** `R`: 중요한 기능에 요청의 유효성을 검사하는 절차가 없거나, 브라우저가 자동으로 보내는 자격 증명(세션 쿠키, 클라이언트 IP, TLS 클라이언트 인증서)에만 의존합니다
- **오탐** `R`: 폼을 제공할 때 무작위 토큰을 세션에 저장하고, hidden 필드로 전송한 뒤, 제출할 때 비교합니다
- **오탐** `G`: 프레임워크의 CSRF 보호가 해당 요청을 보호합니다. SR1-6은 이를 제공하는 라이브러리 중 하나로 Spring Security 3.2 이상을 제시합니다. 이 기능이 활성화되어 있고 해당 URL에서 비활성화되지 않았는지 확인합니다
- **조치** `G`: 입력 폼에는 POST를 사용하고, 세션별 토큰을 사용하며, 중요한 기능에는 재인증을 요구합니다. XSS로 토큰을 탈취할 수 있는 곳에는 CAPTCHA를 권장합니다

```java
session.setAttribute("CSRF_TOKEN", UUID.randomUUID().toString());     // when serving the form
// <input type="hidden" name="csrf_token" value="${CSRF_TOKEN}"/>
String p = request.getParameter("csrf_token");
String s = (String) session.getAttribute("CSRF_TOKEN");
if (p == null || s == null || !MessageDigest.isEqual(p.getBytes(), s.getBytes())) throw new AccessDeniedException("CSRF");
```

- **관련**: CWE-352 · SR1-6

## 12. 서버사이드 요청 위조

입력이 서버가 호출할 URL이나 호스트를 결정하기 때문에, 공격자가 내부 서비스에 접근합니다.

- **탐색**: 입력이나 수정 가능한 프로퍼티 파일에서 가져온 URL이나 호스트를 사용하는 `URL.openConnection`, `openStream`, `RestTemplate`, `WebClient`, `HttpClient`
- **정탐** `R`
  - 입력(또는 변조될 수 있다고 가이드가 판단하는 프로퍼티 값)을 검증 없이 호출에 전달합니다
  - 호스트 파라미터가 `192.168.x.x:8080/secrets.txt` 같은 내부 주소를 가리키도록 조작할 수 있습니다
- **오탐** `R`: 입력이 미리 정의한 URL 중에서 선택하는 데에만 쓰입니다. 가이드의 예시에서는 클라우드 메타데이터 주소 `169.254.169.254`를 차단 목록으로 막은 경우를 오탐으로 판단합니다
- **검토 필요** `R`: 내부 대역의 차단 목록(`isPrivateIP()` 검사)이라고 해서 자동으로 안전하지는 않습니다. 가이드는 우회 방법에 대해서도 확인하라고 요구합니다. 10진수, 16진수, 8진수, 오버플로우된 IP 표기, 점이 없는 형태, 유니코드와 IDN 정규화, `@`와 `#`를 이용한 기법, 다른 스킴(`file://`, `ldap://`)이 해당합니다
- **조치** `G`: 서버가 호출할 수 있는 서비스를 허용 목록으로 관리합니다. 임의의 URL을 허용하는 것이 요구사항이라면 내부 주소를 차단 목록으로 막습니다. 내부망 안에서도 요청을 인증합니다

```java
private static final Map<String, URI> SERVICES = Map.of("weather", URI.create("https://api.example.go.kr/weather"));
URI target = SERVICES.get(request.getParameter("svc"));
if (target == null) throw new IllegalArgumentException();
```

- **관련**: CWE-918 · SR1-4, SR2-1

## 13. HTTP 응답분할

응답 헤더에 들어가는 입력의 CR이나 LF가 응답을 분할하므로, XSS와 캐시 오염이 가능해집니다.

- **탐색**: 입력을 사용하는 `addCookie`, `setHeader`, `addHeader`, `sendRedirect`
- **정탐** `R`: CR/LF를 제거하지 않은 입력이 헤더(리다이렉트 URL이나 `Content-Disposition` 파일 이름 포함)에 도달합니다
- **오탐** `R`: `\r`과 `\n`을 먼저 제거합니다. 값이 `getContextPath()`에서 옵니다. 값이 숫자입니다
- **조치** `G`: null을 검사한 뒤, 헤더에 입력을 사용하기 전에 CR과 LF를 제거합니다

```java
String lastLogin = request.getParameter("last_login");
if (lastLogin == null) lastLogin = "";
response.addCookie(new Cookie("LASTLOGIN", lastLogin.replaceAll("[\\r\\n]", "")));
```

- **관련**: CWE-113 · SR1-7

## 14. 정수형 오버플로우

정수 타입의 범위를 벗어난 값이 작은 값이나 음수로 되돌아갑니다. 반복문의 경계, 메모리 할당, 복사 크기에서 특히 문제가 됩니다.

- **탐색**: 파싱한 입력(`Integer.parseInt`, `atoi`)을 사용하는 배열 크기, 반복문 한계, `malloc` 크기, 인덱스 연산
- **정탐** `R`: 입력이 범위 검사 없이(음수 포함) 배열 크기나 인덱스를 결정합니다. 카운터가 검사 없이 한계를 넘어 증가할 수 있습니다
- **오탐** `R`: 결과가 범위를 벗어나지 않는 메서드에서 값을 가져옵니다(예: `InputStream.available()`). 입력에 자연스러운 한계가 있습니다(HTTP 헤더 값). 값이 프로그램 인자의 개수여서 정수 한계에 현실적으로 도달할 수 없습니다. 값이 외부 입력이 아닙니다
- **조치** `G`: 각 타입의 범위를 파악하고, 연산 결과의 범위를 검사하며, 할당에 사용하는 입력을 검사합니다
- **조치** `D`: 가이드의 Java 예시는 `< 0`만 검사합니다. 상한도 함께 적용하고, 입력에 대한 산술에는 `Math.addExact`나 `Math.multiplyExact`를 사용합니다

```java
int count = Integer.parseInt(param);
if (count < 0 || count > MAX_ITEMS) throw new IllegalArgumentException();
String[] items = new String[count];
```

```c
int idx = atoi(argv[1]);
if (idx >= 0 && idx < (int)(sizeof(table) / sizeof(table[0]))) value = table[idx];
```

- **관련**: CWE-190 · SR1-9

## 15. 보안기능 결정에 사용되는 부적절한 입력값

인증, 인가, 가격 결정이 쿠키, 환경 변수, 파라미터, hidden 필드처럼 클라이언트가 제어하는 값을 신뢰합니다.

- **탐색**: 로그인 상태, 역할, 사용자 신원, 가격을 결정하는 변수. 그 결정 근처에서 쿠키, hidden 필드, 헤더를 읽는 코드
- **정탐** `R`: 결정에 외부 입력을 그대로 사용합니다. 예를 들어 `authenticated=true`나 일반 쿠키에 저장된 사용자 ID, hidden 필드로 전송한 가격이 해당합니다
- **오탐** `R`: 결정에 서버에서 검증한 값(세션, DB)을 사용합니다. 가이드의 예시에서는 hidden `price` 필드를 받지만 가격은 서버에서 조회합니다
- **조치** `G`: 상태와 보안 관련 데이터는 서버(세션이나 DB)에 보관하고 검사도 서버에서 수행합니다. 외부 인증 서비스가 신원을 넘겨줄 때는 클라이언트의 사용자 ID를 신뢰하지 말고 토큰(서명과 만료)을 검증합니다. 쿠키에 이런 데이터를 담아야 한다면 서버에서 암호화하고 MAC으로 보호합니다

```java
// Vulnerable: trusts the client's member ID
String tokenB = tokenService.issue(request.getParameter("memberId"));

// Safe: identity comes from a verified token
String memberId = tokenService.verifyAndExtract(request.getParameter("tokenA"));  // checks signature and expiry
String tokenB = tokenService.issue(memberId);

// Safe: price from the server, not the hidden field
int total = quantity * productService.getPrice(itemId);
```

- **관련**: CWE-807 · SR1-9

## 16. 메모리 버퍼 오버플로우

프로그램이 스택이나 힙에 할당된 버퍼의 바깥을 읽거나 씁니다. 주로 C와 C++에 해당합니다.

- **탐색**: `gets`, `strcpy`, `strcat`, `sprintf`, `memcpy`, `scanf("%s")`, 반복문 안의 배열 쓰기, 입력으로 채우는 고정 크기 버퍼
- **정탐** `R`
  - 버퍼에 들어가는지 확인하지 않고 데이터를 씁니다. 입력으로 정한 크기나 길이를 버퍼 크기와 비교하지 않습니다
  - 길이를 검사하지 않고 입력을 고정 버퍼(예: 16바이트, 또는 64바이트 호스트 이름)에 복사합니다
  - 반복문에서 인덱스가 감소하는데(예: 뒤쪽 공백 제거) 0 이상인지 검사하지 않습니다
  - 문자열 버퍼에 종료 널이 없을 수 있습니다
- **오탐** `R`: 모든 쓰기 전에 크기를 비교하고, 인덱스의 양쪽 경계(음수 포함)를 검사하고, 반복문의 경계를 검사하며, 문자열을 버퍼 안에서 널로 종료합니다
- **조치** `G`: 버퍼를 충분한 크기로 만들고, 그 범위 안에서만 읽고 쓰며, 종료 널을 버퍼 안에 씁니다. 설계 기준 SR1-8은 플랫폼 보호 기능(실행 불가능 스택, ASLR, StackGuard)과 사용 금지 함수 목록(보안약점 49)을 추가로 제시합니다

```c
/* Vulnerable: copies the size of the whole struct into field x */
memcpy(cv_struct.x, SRC_STR, sizeof(cv_struct));

/* Safe: copy at most the field size, never past the source string, and terminate */
strncpy(cv_struct.x, SRC_STR, sizeof(cv_struct.x) - 1);
cv_struct.x[sizeof(cv_struct.x) - 1] = '\0';

/* Vulnerable */ gets(message);
/* Safe */       fgets(message, sizeof(message), stdin);
```

- Java에서는 범위를 벗어난 배열 접근이 메모리를 손상시키지 않고 예외를 일으킵니다. 인덱스나 크기가 입력에서 온 Java 코드는 16번이 아니라 보안약점 14번이나 39번으로 보고합니다(`D`: 가이드는 16번에 Java 예시를 제시하지 않습니다)
- **관련**: CWE-119 · SR1-8

## 17. 포맷 스트링 삽입

입력이 출력 함수의 포맷 스트링으로 사용되므로, 공격자가 메모리를 읽거나 C에서는 메모리에 쓸 수 있습니다(`%n`). 가이드는 Java도 영향을 받는다고 설명합니다. 포맷 지정자가 다른 인자를 노출할 수 있기 때문입니다.

- **탐색**: 리터럴이 아닌 포맷을 사용하는 C `printf`, `fprintf`, `sprintf`, `snprintf`, `syslog`. 입력으로 만든 포맷을 사용하는 Java `String.format`, `printf`, `MessageFormat.format`
- **정탐** `R`: 입력으로 포맷 스트링을 만듭니다. 예를 들어 Java에서 `%1$tY-%1$tm-%1$te`를 입력하면 날짜 인자가 노출됩니다
- **오탐** `R`: 포맷 스트링이 리터럴 인자이고, 입력이 이를 만들지 않으며, 포맷 지정자의 개수가 인자의 개수와 일치하고, 출력 길이를 제한합니다
- **조치** `G`: 입력을 포맷 스트링으로 사용하지 않습니다. `%s`를 사용하고 입력은 뒤쪽 인자로 전달합니다. `%n`과 `%hn`은 절대 사용하지 않습니다

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

- **관련**: CWE-134 · SR1-8
