# 캡슐화, API 오용

보안약점 44번부터 49번까지입니다.

| 유형 | 번호 | 원인 |
|------|------|------|
| 캡슐화 | 44번부터 47번 | 중요한 데이터나 기능을 캡슐화하지 않거나 잘못 사용해서 정보노출이나 권한 문제가 발생함 |
| API 오용 | 48번, 49번 | 의도된 용도와 다르게 API를 사용하거나, 안전하지 않은 API를 사용함 |

항목의 구성은 `input-validation_ko.md`와 같습니다.

## 44. 잘못된 세션에 의한 데이터 정보노출

여러 요청을 동시에 처리하는 객체(서블릿, JSP 선언부, Spring 컨트롤러와 그 밖의 싱글톤 빈)가 요청 데이터를 필드에 보관하므로, 한 사용자의 데이터가 다른 세션에 전달됩니다.

- **탐색**: `HttpServlet` 하위 클래스의 `final`이 아닌 인스턴스 필드, JSP `<%! %>` 블록에 선언한 변수, `@Controller`, `@Service` 또는 그 밖의 싱글톤 빈의 요청 처리 메서드 안에서 값을 할당하는 필드, 변경 가능한 static 필드
- **정탐** `R`
  - 서블릿(JSP 포함)이 `final`이 아닌 멤버 필드를 선언합니다
  - Spring 컨트롤러가 요청 데이터를 필드에 저장합니다. 예를 들어 `currentPage = Integer.parseInt(request.getParameter("page"))`가 해당합니다
- **오탐** `R`
  - JSP나 서블릿 안에 선언한 내부 클래스입니다(멤버 필드가 아닙니다)
  - 상수로 사용하는 `final` 필드입니다
  - 프레임워크가 주입한 빈(`@Resource`, `@Autowired`)을 담은 필드입니다. eGovFrame과 Spring은 이런 빈을 상태가 없는 공유 인스턴스로 관리합니다
  - JSP 스크립틀릿 `<% %>`의 변수입니다. 이는 `_jspService`의 지역 변수입니다
- **조치** `G`: 싱글톤에서는 변수의 범위에 주의합니다. 요청 데이터는 지역 변수로 선언하고, 사용자별 데이터는 세션에 보관합니다

```java
@Controller
public class TrendForecastController {
    private int currentPage = 1;                                        // Vulnerable: shared by all requests
    public String list(HttpServletRequest request) {
        int currentPage = Integer.parseInt(request.getParameter("page"));  // Safe: local variable
        ...
    }
}
```

```jsp
<%! String imagePath = "/img/"; %>   <%-- Vulnerable: shared by every user of this JSP --%>
<%  String imagePath = "/img/"; %>   <%-- Safe: local to the request --%>
```

- **관련**: CWE-488, CWE-543 · SR4-1

## 45. 제거되지 않고 남은 디버그 코드

디버깅을 위해 넣은 코드가 배포본에 남아서 정보나 제어권을 노출합니다.

- **탐색**: 웹 애플리케이션 클래스(서블릿, 컨트롤러, 서비스)의 `main` 메서드, 내부 값을 출력하는 `System.out`/`System.err` 같은 디버그 출력, `if (debug)` 블록, 테스트용 엔드포인트, 배포본에 컴파일되어 들어가는 C `backtrace` 출력과 `#ifdef DEBUG` 구간
- **정탐** `R`: 서블릿이나 그 밖의 J2EE 클래스에 테스트용 `main()`이나 디버그 출력문이 있습니다. J2EE 표준은 이런 클래스에 `main`을 두지 못하게 하므로, 그곳의 `main`은 대부분 디버그 코드입니다. J2EE가 아닌 환경에서는 정적 도구가 이를 제대로 판단하지 못하므로 수동으로 검토합니다
- 가이드는 오탐 예시를 제시하지 않습니다
- **조치** `G`: 배포하기 전에 디버그 코드가 있는지 확인하고 제거합니다. 디버깅을 마치면 웹 애플리케이션 클래스에서 `main()`을 삭제하고, C에서는 배포용 빌드에서 디버그 코드를 제거합니다

```java
public class Base64 {
    public static void main(String[] args) { if (debug) { ... } }   // Vulnerable: delete
}
```

- **관련**: CWE-489 · `egovframe` PMD 규칙 34 SystemPrintln (콘솔 출력 부분에서 일부 겹칩니다)

## 46. Public 메소드부터 반환된 Private 배열

public 메서드가 private 배열을 반환하기 때문에, 호출자가 참조를 얻어서 객체의 상태를 변경할 수 있습니다.

- **탐색**: 배열 필드를 `return`하는 `public` 메서드, 배열 필드의 getter
- **정탐** `R`
  - 메서드가 배열 필드 자체를 반환합니다
  - 메서드가 배열을 복사하지만, 요소가 변경 가능한 객체여서 참조만 복사됩니다
- **오탐** `R`: 배열이 private이 아닙니다. 예를 들어 `public static final String[] XML_TAG = {...}`가 해당합니다(이 보안약점의 대상이 아닙니다)
- **조치** `G`: public 메서드에서 private 배열을 반환하지 않습니다. 복사본을 반환하며, 요소가 변경 가능하다면 각 요소를 `clone()`합니다. `String`처럼 변경할 수 없는 요소라면 배열만 복사해도 충분합니다. 메서드를 private으로 바꾸는 방법도 있습니다
- **조치** `D`: `public static final` 배열은 보안약점 46의 대상이 아니지만, 누구나 요소를 바꿀 수 있습니다. 보안약점 번호를 붙이지 않고, 일반적인 개선 사항으로 수정할 수 없는 리스트(`List.of(...)`)를 권장합니다

```java
private Color[] colors;
public Color[] getColors() { return colors; }                       // Vulnerable

public Color[] getColors() {                                        // Safe: deep copy (Color is a Cloneable class of the project)
    Color[] copy = new Color[colors.length];
    for (int i = 0; i < colors.length; i++) copy[i] = colors[i].clone();
    return copy;
}
public String[] getNames() { return names.clone(); }                // Safe for immutable elements
```

- **관련**: CWE-495 · `egovframe` PMD 규칙 27 MethodReturnsInternalArray (eGovFrame 가이드는 2번 규칙과 27번 규칙을 서로 반대로 연결합니다)

## 47. Private 배열에 Public 데이터 할당

public 메서드의 배열 인자를 private 필드에 그대로 저장하므로, 호출자가 그 배열을 계속 변경할 수 있습니다.

- **탐색**: 배열 파라미터를 필드에 할당하는 setter와 생성자(`this.roles = roles;`)
- **정탐** `R`
  - 인자로 받은 배열을 필드에 직접 할당합니다
  - 메서드가 배열을 복사하지만, 요소가 변경 가능한 객체여서 참조만 복사됩니다
- 가이드는 오탐 예시를 제시하지 않습니다
- **조치** `G`: 인자의 복사본을 저장하고, 변경 가능한 요소는 `clone()`합니다. 변경할 수 없는 요소라면 배열만 복사해도 충분합니다

```java
public void setUserRoles(UserRole[] userRoles) { this.userRoles = userRoles; }   // Vulnerable

public void setUserRoles(UserRole[] userRoles) {                                 // Safe (UserRole implements a public clone())
    this.userRoles = new UserRole[userRoles.length];
    for (int i = 0; i < userRoles.length; i++) this.userRoles[i] = userRoles[i].clone();
}
```

- **관련**: CWE-496 · `egovframe` PMD 규칙 2 ArrayIsStoredDirectly

## 48. DNS lookup에 의존한 보안결정

인증이나 접근 통제가 호스트 이름을 신뢰하는데, 공격자는 DNS를 오염시켜서 이를 위조할 수 있습니다.

- **탐색**: 보안 결정에서 비교하는 `getCanonicalHostName()`, `getHostName()`, `InetAddress.getByName`의 결과, `request.getRemoteHost()`, 신뢰를 부여하는 데 사용하는 C `gethostbyaddr`, `getnameinfo`
- **정탐** `R`: DNS 조회를 수행하고 그 결과로 신뢰 여부를 결정합니다. 예를 들어 `addr.getCanonicalHostName().endsWith("trustme.com")`가 해당합니다
- 가이드는 오탐 예시를 제시하지 않습니다
- **조치** `G`: 보안 결정에 DNS 이름을 사용하지 않고 IP 주소를 직접 비교합니다
- **조치** `D`: 가이드의 C "안전한" 예시는 여전히 `gethostbyaddr`이 반환한 이름을 `"127.0.0.1"`과 비교합니다. 상대방의 주소 자체를 비교합니다. 프록시 뒤에서는 프록시를 신뢰할 수 있고 프록시가 그 주소를 설정하는 경우에만 전달된 주소를 사용합니다

```java
String ip = request.getRemoteAddr();
if (TRUSTED_IPS.contains(ip)) { doTrustedWork(); }     // compare addresses, not names
```

- **관련**: CWE-247, CWE-350 · SR2-1

## 49. 취약한 API 사용

사용이 금지된 함수나 오용하기 쉬운 함수를 필요한 검사 없이 호출합니다.

- **탐색**: 아래 목록에 있는 API
- **정탐** `R`: 목록에 있는 API를 사용합니다. 대체할 수 있는 API가 없다면 인자와 반환값을 검사하지 않는 한 그 호출은 정탐입니다. 개발 조직이 자체 금지 API 목록을 가지고 있다면 그 목록을 따라야 합니다
- **오탐** `R`: 대체할 수 있는 API가 없고, 인자와 반환값을 검사합니다
- **조치** `G`: 금지된 함수를 대체하고, J2EE에서는 프레임워크의 메서드를 사용합니다

| 언어 | 금지 또는 위험한 함수 | 가이드의 대체 방법 |
|------|-----------------------|---------------------|
| C | `gets()` | `gets_s()` 또는 `fgets()` |
| C | `strcpy()`, `strcat()`, `strncpy()`, `strncat()`, `sprintf()` | `strcpy_s()`, `strcat_s()`, `strncpy_s()`, `strncat_s()`, `sprintf_s()` |
| C | 작은 부호 있는 타입(`int`, `short`, `char`)에 대입하는 `strtol()` | 결과의 범위를 검사합니다 |
| Java (J2EE) | 서블릿이나 그 밖의 J2EE 컴포넌트에서 직접 사용하는 `java.net.Socket` | `URL.openConnection()` 또는 프레임워크가 제공하는 다른 통신 방식 |
| Java (J2EE) | `System.exit()` | 제거합니다. 오류를 처리하고 컨테이너가 계속 실행되게 합니다 |

- 진단가이드의 부록(PART5)에 있는 설계 기준 SR1-8의 안전한 함수 표는 같은 C 함수에 대해 다른 계열의 대체 함수(`strlcpy`, `strlcat`, `snprintf`, `vsnprintf`, `asprintf`, `vasprintf`, `fgets`)를 제시합니다. 어느 계열이든 보안약점을 제거하므로 플랫폼이 제공하는 쪽을 따릅니다(`D`: `*_s` 함수는 선택 사항인 C11 Annex K에 속하며 모든 컴파일러에서 사용할 수 있지는 않습니다)
- 진단가이드의 목록에는 `gets()`가 빠져 있지만 가이드 자체의 예시는 이를 대체합니다. `gets()`는 금지 함수로 취급합니다

```c
char str[100];
gets(str);                          /* Vulnerable: no length limit */
fgets(str, sizeof(str), stdin);     /* Safe */
```

```java
catch (IOException e) { System.exit(1); }            // Vulnerable in a J2EE application
catch (IOException e) { logger.error("ERROR-02", e); }   // Safe
```

- **관련**: CWE-242, CWE-246, CWE-382, CWE-676 · SR1-8 요구사항 2 (가이드의 대응표는 어떤 기준에도 보안약점 49를 나열하지 않습니다)
