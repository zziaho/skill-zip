# Encapsulation and API Misuse (캡슐화, API 오용)

Weaknesses 44 to 49:

| Type | Numbers | Cause |
|------|---------|-------|
| 캡슐화 (encapsulation) | 44 to 47 | Important data or functions are not encapsulated, or are used wrongly, causing information exposure or permission problems |
| API 오용 (API misuse) | 48, 49 | APIs used against their intended use, or APIs that are insecure |

The item format is the same as in `input-validation.md`.

## 44. 잘못된 세션에 의한 데이터 정보노출 (data exposure through the wrong session)

Objects that serve many requests at once (servlets, JSP declarations, Spring controllers and other singleton beans) keep request data in fields, so one user's data reaches another session.

- **Find**: non-`final` instance fields in `HttpServlet` subclasses; variables declared in JSP `<%! %>` blocks; fields assigned inside request-handling methods of `@Controller`, `@Service` or other singleton beans; static mutable fields
- **Vulnerable** `R`
  - A servlet (including a JSP) declares a member field that is not `final`
  - A Spring controller stores request data in a field, for example `currentPage = Integer.parseInt(request.getParameter("page"))`
- **Not vulnerable** `R`
  - An inner class declared in a JSP or servlet (it is not a member field)
  - `final` fields used as constants
  - Fields that hold beans injected by the framework (`@Resource`, `@Autowired`), which eGovFrame and Spring manage as shared, stateless instances
  - Variables in JSP scriptlets `<% %>`, which are locals of `_jspService`
- **Fix** `G`: watch variable scope in singletons. Declare request data as local variables, or keep per-user data in the session

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

- **Related**: CWE-488, CWE-543 · SR4-1

## 45. 제거되지 않고 남은 디버그 코드 (leftover debug code)

Code inserted for debugging stays in the release and exposes information or control.

- **Find**: `main` methods in web application classes (servlets, controllers, services); debug output such as `System.out`/`System.err` printing of internal values; `if (debug)` blocks; test endpoints; C `backtrace` output and `#ifdef DEBUG` sections that are compiled into releases
- **Vulnerable** `R`: a servlet or other J2EE class contains a test `main()` or debug print statements. The J2EE standard forbids `main` in such classes, so a `main` there is most likely debug code. Outside J2EE, static tools cannot judge this well; review manually
- The guides give no false-positive example
- **Fix** `G`: check for and remove debug code before release. Delete `main()` from web application classes when debugging is done; in C, remove debug code for release builds

```java
public class Base64 {
    public static void main(String[] args) { if (debug) { ... } }   // Vulnerable: delete
}
```

- **Related**: CWE-489 · `egovframe` PMD rule 34 SystemPrintln (partial overlap: console printing)

## 46. Public 메소드부터 반환된 Private 배열 (private array returned from a public method)

A public method returns a private array, so callers get the reference and can change the object's state.

- **Find**: `public` methods that `return` an array field; getters for array fields
- **Vulnerable** `R`
  - A method returns the array field itself
  - The method copies the array, but the elements are mutable objects and only their references are copied
- **Not vulnerable** `R`: the array is not private, for example `public static final String[] XML_TAG = {...}` (it is outside this weakness)
- **Fix** `G`: do not return private arrays from public methods. Return a copy; if the elements are mutable, `clone()` each element. For immutable elements such as `String`, copying the array is enough. Alternatively, make the method private
- **Fix** `D`: a `public static final` array is outside weakness 46, but its elements can still be changed by anyone. Recommend an unmodifiable list (`List.of(...)`) as a general improvement, without a weakness number

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

- **Related**: CWE-495 · `egovframe` PMD rule 27 MethodReturnsInternalArray (the eGovFrame guide maps rules 2 and 27 the other way round)

## 47. Private 배열에 Public 데이터 할당 (public data assigned to a private array)

An array argument of a public method is stored directly in a private field, so the caller can still change it.

- **Find**: setters and constructors that assign an array parameter to a field (`this.roles = roles;`)
- **Vulnerable** `R`
  - The argument array is assigned to the field directly
  - The method copies the array, but the elements are mutable objects and only their references are copied
- The guides give no false-positive example
- **Fix** `G`: store a copy of the argument; `clone()` mutable elements. For immutable elements, copying the array is enough

```java
public void setUserRoles(UserRole[] userRoles) { this.userRoles = userRoles; }   // Vulnerable

public void setUserRoles(UserRole[] userRoles) {                                 // Safe (UserRole implements a public clone())
    this.userRoles = new UserRole[userRoles.length];
    for (int i = 0; i < userRoles.length; i++) this.userRoles[i] = userRoles[i].clone();
}
```

- **Related**: CWE-496 · `egovframe` PMD rule 2 ArrayIsStoredDirectly

## 48. DNS lookup에 의존한 보안결정 (security decision based on a DNS lookup)

Authentication or access control trusts a host name, which an attacker can spoof by poisoning DNS.

- **Find**: `getCanonicalHostName()`, `getHostName()`, `InetAddress.getByName` results compared in a security decision; `request.getRemoteHost()`; C `gethostbyaddr`, `getnameinfo` used to grant trust
- **Vulnerable** `R`: a DNS lookup exists and its result decides trust, for example `addr.getCanonicalHostName().endsWith("trustme.com")`
- The guides give no false-positive example
- **Fix** `G`: do not use DNS names for security decisions; compare IP addresses directly
- **Fix** `D`: the guides' C "safe" example still compares the name returned by `gethostbyaddr` with `"127.0.0.1"`. Compare the peer address itself. Behind a proxy, use the forwarded address only if the proxy is trusted and sets it

```java
String ip = request.getRemoteAddr();
if (TRUSTED_IPS.contains(ip)) { doTrustedWork(); }     // compare addresses, not names
```

- **Related**: CWE-247, CWE-350 · SR2-1

## 49. 취약한 API 사용 (use of dangerous API)

Banned functions, or functions that are easily misused, are called without the needed checks.

- **Find**: the APIs in the lists below
- **Vulnerable** `R`: a listed API is used. When no replacement exists, the call is vulnerable unless its arguments and return value are checked. If the development organization has its own list of banned APIs, it must be followed
- **Not vulnerable** `R`: no replacement exists and the arguments and return value are checked
- **Fix** `G`: replace the banned functions, and use framework methods in J2EE

| Language | Banned or dangerous | Replacement in the guides |
|----------|---------------------|---------------------------|
| C | `gets()` | `gets_s()` or `fgets()` |
| C | `strcpy()`, `strcat()`, `strncpy()`, `strncat()`, `sprintf()` | `strcpy_s()`, `strcat_s()`, `strncpy_s()`, `strncat_s()`, `sprintf_s()` |
| C | `strtol()` into small signed types (`int`, `short`, `char`) | Check the range of the result |
| Java (J2EE) | `java.net.Socket` used directly in a servlet or other J2EE component | `URL.openConnection()` or other framework communication |
| Java (J2EE) | `System.exit()` | Remove; handle the error and let the container keep running |

- The diagnostic guide's appendix (PART5), in its table of safe functions for design criterion SR1-8, gives a different family of replacements for the same C functions: `strlcpy`, `strlcat`, `snprintf`, `vsnprintf`, `asprintf`, `vasprintf`, `fgets`. Either family removes the weakness; follow what the platform provides (`D`: `*_s` functions belong to the optional C11 Annex K and are not available on every compiler)
- The diagnostic guide's list leaves out `gets()`, but its own example replaces it; treat `gets()` as banned

```c
char str[100];
gets(str);                          /* Vulnerable: no length limit */
fgets(str, sizeof(str), stdin);     /* Safe */
```

```java
catch (IOException e) { System.exit(1); }            // Vulnerable in a J2EE application
catch (IOException e) { logger.error("ERROR-02", e); }   // Safe
```

- **Related**: CWE-242, CWE-246, CWE-382, CWE-676 · SR1-8 requirement 2 (the guides' mapping table does not list weakness 49 under any criterion)
