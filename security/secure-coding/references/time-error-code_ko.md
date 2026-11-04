# 시간 및 상태, 에러처리, 코드오류

보안약점 34번부터 43번까지입니다.

| 유형 | 번호 | 원인 |
|------|------|------|
| 시간 및 상태 | 34번, 35번 | 병렬 환경이나 다중 프로세스 환경에서 시간과 상태를 잘못 관리함 |
| 에러처리 | 36번부터 38번 | 오류를 처리하지 않거나, 중요정보가 유출되는 방식으로 처리함 |
| 코드오류 | 39번부터 43번 | 타입 오류, 잘못 해제한 자원 같은 코딩 실수 |

항목의 구성은 `input-validation_ko.md`와 같습니다. 설계 기준에 대응하는 보안약점은 36번(SR3-1)과 39번(SR1-9)뿐입니다. 개발보안 가이드(제3장)는 일부 보안약점이 코딩 규칙을 따르는 것만으로 제거할 수 있다고 설명합니다.

## 34. 경쟁조건: 검사시점과 사용시점

자원을 검사한 뒤에 사용하는데, 다른 프로세스나 스레드가 동시에 그 자원을 사용해서 그 사이에 상태가 바뀝니다.

- **탐색**: 열기, 읽기, 삭제가 뒤따르는 `File.exists()`, `canRead()`, `isFile()`, `fopen()`이 뒤따르는 C `access()`, 여러 스레드나 프로세스가 사용하는 공유 파일, 소켓, 장치, C에서 동기화하지 않은 공유 변수 갱신
- **정탐** `R`: 하나의 공유 자원에 여러 스레드나 프로세스가 동기화 없이 동시에 접근할 수 있습니다(예: 한 스레드가 `exists()` 뒤에 파일을 읽는 사이에 다른 스레드가 `exists()` 뒤에 그 파일을 삭제함)
- **오탐** `R`
  - 접근이 동기화되어 있거나, 공유 자원을 관리하는 풀 방식의 모듈을 거칩니다
  - 실제로 경쟁이 발생하지 않습니다. 예를 들어 파일을 나열하고 이름과 크기의 형식만 지정하는 코드입니다
  - Java에서는 `exists()` 뒤에 스트림을 열 때 파일이 사라졌다면 `IOException`이 발생하므로, 그 예외를 처리하면 충분합니다(진단가이드 기준)
- **조치** `G`: 동기화 구문(`synchronized`, 뮤텍스)으로 한 번에 하나의 프로세스만 공유 자원에 접근하게 하고, 임계 구역만 동기화합니다
- **조치** `D`: 가이드의 예시는 한 프로세스 안의 스레드를 다룹니다. 프로세스 사이에서는 검사한 뒤에 사용하는 방식 대신 원자적 연산(`Files.createFile`, `Files.delete`와 예외 처리, C의 `O_CREAT | O_EXCL`)이나 파일 잠금을 사용합니다

```java
private static final Object LOCK = new Object();
synchronized (LOCK) {                       // critical section only
    if (f.exists()) Files.delete(f.toPath());
}
```

```c
mtx_lock(&account_lock);
account += amount;
mtx_unlock(&account_lock);
```

- **관련**: CWE-367

## 35. 종료되지 않는 반복문 또는 재귀함수

반복문이나 재귀에 도달할 수 있는 종료 지점이 없어서 메모리나 스택이 고갈되고 서비스가 중단됩니다.

- **탐색**: 같은 이름, 같은 개수와 타입의 파라미터로 자기 자신을 호출하는 메서드, `while (true)`와 종료 조건이 입력에 달려 있는 반복문
- **정탐** `R`: 반환할 수 있는 제어문이 없는 재귀 호출(이름, 파라미터 개수, 파라미터 타입이 같음)입니다. 예를 들어 `return n * factorial(n - 1);`가 해당합니다
- **오탐** `R`
  - 재귀하기 전에 조건에 따라 반환합니다(예: 자식 목록이 비어 있으면 반환)
  - 이름은 같지만 파라미터 타입이 달라서, 자기 자신이 아니라 오버로드된 다른 메서드를 호출합니다
- **조치** `G`: 모든 재귀에 종료 조건(base case)을 구현하고, 횟수나 상수로 재귀를 제한합니다
- 가이드의 진단은 재귀만 다룹니다. 반복문도 같은 규칙으로 판단합니다(`D`). 종료 조건이 참이 될 수 없거나, 상한 없이 입력에 따라 달라지는 반복문은 정탐입니다

```c
int factorial(int i) {
    if (i <= 1) return 1;          /* base case */
    return i * factorial(i - 1);
}
```

- **관련**: CWE-674, CWE-835

## 36. 오류 메시지 정보노출

오류 메시지나 스택 트레이스가 실행 환경, 사용자, 내부 데이터를 보여 줍니다.

- **탐색**: `printStackTrace()`, 응답이나 페이지에 출력하는 `e.getMessage()`나 `e.toString()`, `System.err.print(e...)`, JSP 오류 출력, `server.error.include-stacktrace`나 `include-message`를 활성화한 Spring 오류 페이지, `error-page`가 없는 `web.xml`
- **정탐** `R`: 오류 출력이 환경, 사용자, 내부 데이터를 드러냅니다. 예를 들어 서블릿이나 JSP의 `catch (Exception e) { e.printStackTrace(); }`가 해당합니다
- **오탐** `R`: 예외를 서버 측 로거로 보냅니다(진단가이드의 오탐 예시는 `logger.error(e, e)`를 사용합니다)
- **조치** `G`: 예외를 내부에서 처리하고, 사용자에게는 중요정보가 없는 미리 정의한 메시지만 보여 줍니다. 오류 코드를 정의하고 필요한 내용만 로그로 남깁니다. 설계 기준 SR3-1은 `web.xml`이나 서버 설정에서 `java.lang.Throwable`, 404, 500에 대한 기본 오류 페이지를 추가로 요구합니다

```java
catch (IOException e) { e.printStackTrace(); }                 // Vulnerable
catch (IOException e) { logger.error("ERROR-01: file open failed", e); }   // Safe: server log only
```

- **관련**: CWE-209, CWE-497 · SR3-1 · `egovframe` PMD 규칙 7 AvoidPrintStackTrace

## 37. 오류 상황 대응 부재

오류를 감지하고도 아무 조치를 하지 않아서, 프로그램이 개발자가 의도하지 않은 상태로 계속 실행됩니다.

- **탐색**: 비어 있는 `catch` 블록, 주석만 있는 catch 블록, C에서 오류를 알리는 함수의 반환값 무시
- **정탐** `R`: 예외를 잡고도 이어지는 조치가 없어서, 프로그램이 무슨 일이 일어났는지 모른 채 계속 실행됩니다. 가이드의 예시에서는 패스워드가 없으면 `NullPointerException`이 발생하고, 비어 있는 catch가 이를 삼키며, 사용자가 인증된 것으로 처리됩니다; 진단가이드의 예시는 DB 연결 메서드에서 `SQLException`을 잡는 비어 있는 catch입니다
- 가이드는 오탐 예시를 제시하지 않습니다
- **조치** `G`: 제어문(`try-catch`, `if`, `switch`)으로 오류를 처리하고, 예외마다 적절한 조치를 취합니다
- **조치** `D`: 가이드의 안전한 예시는 `e.getMessage()`를 사용자에게 보여 주는 메시지에 넣는데, 이는 보안약점 36과 충돌할 수 있습니다. 예외는 로그로 남기고 고정된 메시지를 보여 줍니다

```java
catch (SQLException e) { }                                      // Vulnerable: error swallowed
catch (SQLException e) {                                        // Safe: logged and reported
    logger.error("ERROR-03: DB connection failed", e);
    throw new ServiceException("ERROR-03", e);
}
```

- **관련**: CWE-390 · `egovframe` PMD 규칙 16 EmptyCatchBlock

## 38. 부적절한 예외 처리

반환값이나 예외 상황을 제대로 확인하지 않거나, 예외를 지나치게 넓게 잡습니다.

- **탐색**: 특정 연산을 감싸는 `catch (Exception e)`, `catch (Throwable t)`, `catch (RuntimeException e)`, 무시한 반환값
- **정탐** `R`: 구체적인 예외를 지정할 수 있는 곳에서 넓은 범위의 catch를 사용합니다. 예를 들어 파일 읽기를 감싸는 `catch (Exception ex)`가 해당합니다
- 가이드는 명시적인 오탐 규칙을 제시하지 않습니다. `D`: 가장 바깥 경계(전역 예외 처리기, 스레드의 최상위 루프)에서 예외를 로그로 남기고 일반적인 오류를 반환하는 넓은 catch는 통상적인 방식입니다. 특정 연산을 감싸는 넓은 catch를 보고합니다
- **조치** `G`: 값을 반환하는 모든 함수의 결과를 확인하고, 넓은 예외 대신 구체적인 예외를 잡으며, 예외가 발생할 수 있는 순서대로 처리합니다

```java
catch (Exception e) { ... }                                     // Vulnerable
catch (MalformedURLException e) { ... }                         // Safe
catch (IOException e) { ... }
catch (ParseException e) { ... }
```

- **관련**: CWE-754 · `egovframe` PMD 규칙 6 AvoidCatchingGenericException

## 39. Null Pointer 역참조

null이 될 수 없다고 가정한 객체를 null인 상태에서 역참조합니다.

- **탐색**: 검사 없이 사용하는, null일 수 있는 값(`getParameter`, `getAttribute`, `System.getProperty`, `Map.get`, DAO 결과, `return null`하는 메서드, `null`로 초기화한 변수), C에서 함수가 반환하는 포인터
- **값이 null일 수 있는 경우** `R`(진단가이드의 목록): null로 초기화했습니다. 선언만 하고 생성하지 않았습니다. null 객체의 필드 접근이나 메서드 호출 결과입니다. 문자열처럼 null일 수 있는 객체에 연산한 결과입니다
- **정탐** `R`
  - null일 수 있는 값을 null 검사 없이 사용합니다. 예를 들어 `System.getProperty("cmd").trim()`이 해당합니다
  - null로 초기화한 변수를 일부 분기에서만 할당하고 모든 분기에서 사용합니다
  - DB 자원(`ResultSet`, `Statement`)을 null 검사 없이 `finally`에서 닫습니다
  - null을 반환할 수 있는 메서드의 결과를 바로 사용합니다
  - null 검사가 역참조 뒤에 나옵니다. `if (str.length() == 0 || str == null)`가 해당합니다
- **오탐** `R`
  - null을 반환하지 않는다고 문서화된 API나 프로젝트 메서드입니다(Javadoc을 확인합니다). 예를 들어 `StringTokenizer`가 해당합니다
  - catch 블록이 예외를 다시 던져서, 그 뒤의 코드가 null 값으로 실행되지 않습니다
  - 단락 평가 순서를 지킨 `if (a == null || a.length() == 0)`입니다
  - 역참조가 할당과 같은 `try` 안에 있어서, 할당이 실패하면 실행되지 않습니다
  - JSP 내장 객체(EL의 `pageContext.request.contextPath`)
  - `Integer.parseInt(value)` 같은 static 메서드 호출입니다(클래스는 null 객체가 아닙니다)
  - 하나의 메서드 안에서 호출자가 null을 넘긴다는 데이터 흐름이 없는, null일 수 있는 파라미터입니다. 이는 호출자가 검사해야 합니다
  - 문서에 null 반환이 명시되지 않은 JRE 클래스의 생성자
  - 같은 null 변수를 연속된 줄에서 역참조하면 첫 번째 역참조에서 실행이 멈춥니다. 첫 번째만 보고합니다
- **조치** `G`: null일 수 있는 참조는 사용하기 전에 검사합니다

```java
if ((obj == null && elt == null) || (obj != null && obj.equals(elt))) { ... }
String url = request.getParameter("url");
if (url != null && url.equals("")) { ... }      // the guides print || here, which is a typo
```

```c
int *p = IntegerAddressReturn();
if (p != NULL) *p = count;
```

- **관련**: CWE-476 · SR1-9 · `egovframe` PMD 규칙 13 BrokenNullCheck, 28 MisplacedNullCheck

## 40. 부적절한 자원 해제

파일 디스크립터, 힙 메모리, 소켓, DB 커넥션을 사용한 뒤에 반환하지 않아서 자원이 고갈됩니다.

- **탐색**: try-with-resources 없이 연 `Connection`, `Statement`, `ResultSet`, 스트림, 리더, 소켓, 채널, `finally`가 아니라 `try` 안에서 호출한 `close()`, 조기 반환이 있는 C `fopen`, `malloc`, `socket`
- **정탐** `R`
  - 자원을 해제하지 않는 분기(제어문이나 예외)가 있습니다. 모든 제어 흐름을 확인합니다
  - `finally` 안의 한 `try` 블록에서 `close()` 호출이 여러 개 있어서, 첫 번째에서 예외가 발생하면 나머지를 건너뜁니다
- **오탐** `R`
  - 모든 자원을 `finally`에서 닫고, 각 자원을 별도의 try-catch에서 null 검사와 함께 닫습니다
  - 메서드의 역할이 자원을 반환하는 것입니다(`getConnection()`). 호출자가 자원을 해제합니다
- **조치** `G`: 사용한 모든 자원을 `finally`에서 null 검사와 예외 처리를 함께 수행하며 하나씩 해제합니다
- **조치** `D`: Java 7 이상에서는 try-with-resources가 이를 올바르게 처리하며 더 간단합니다

```java
try (InputStream in = new FileInputStream(src);
     OutputStream out = new FileOutputStream(dst)) {
    in.transferTo(out);
}
```

```c
FILE *f = fopen(filename, "r");
if (f == NULL) return;
if (!checkSomething()) { fclose(f); return; }   /* release on the error path too */
fclose(f);
```

- **관련**: CWE-404 · `egovframe` PMD 규칙 14 CloseResource

## 41. 해제된 자원 사용

메모리(또는 다른 자원)를 해제한 뒤에 사용합니다. 가이드의 예시는 C입니다.

- **탐색**: 일부 경로에서 `free(p)` 뒤에 `p`를 사용하는 코드, 이중 `free`, 닫힌 스트림이나 커넥션을 사용하는 Java의 대응 사례(`D`)
- **정탐** `R`: 일부 제어 흐름 경로에서 해제가 사용보다 먼저 발생합니다. 예를 들어 오류 분기에서 메시지 버퍼를 해제한 뒤에 로그로 남깁니다
- **오탐** `R`: 해제에서 사용으로 이어지는 경로가 없습니다
- **함께 확인할 사항** `R`: 자원 포인터에 대한 포인터 연산이 유효한 메모리를 가리키는지, 사용한 뒤에 포인터를 NULL로 설정하는지 확인합니다
- **조치** `G`: 해제된 메모리를 사용하지 않습니다. `free` 직후에 포인터에 NULL을 저장하면 이중 해제도 막을 수 있습니다

```c
char *temp = malloc(BUFFER_SIZE);
strncpy(temp, argv[1], BUFFER_SIZE - 1);
temp[BUFFER_SIZE - 1] = '\0';
/* ... use temp ... */
free(temp);
temp = NULL;                     /* a later free(temp) or use is now harmless or detectable */
```

- **관련**: CWE-416

## 42. 초기화되지 않은 변수 사용

지역 변수에 값을 할당하기 전에 사용하면, 스택에 남아 있던 값을 그대로 가지게 됩니다. 가이드의 예시는 C와 C++입니다.

- **탐색**: 초기화 없이 선언하고 일부 분기에서만 할당하는 C와 C++ 지역 변수(완전한 `default`가 없는 `switch`), 모든 필드를 초기화하지 않는 C++ 생성자
- **정탐** `R`: 변수를 선언할 때 초기화하지 않았거나, C++ 필드를 생성자에서 초기화하지 않았습니다(예: 필드를 설정하지 않은 채로 두는 기본 생성자)
- **오탐** `R`: 선언할 때 초기화했거나, 모든 생성자가 해당 필드를 초기화합니다
- **조치** `G`: 모든 변수에 사용하기 전에 올바른 초깃값을 부여합니다
- Java에서는 컴파일러가 할당되지 않은 지역 변수의 읽기를 거부하고 필드에는 기본값이 들어가므로 이 보안약점이 적용되는 경우가 드뭅니다(`D`: 가이드는 Java를 다루지 않습니다)

```c
int x = 1, y = 1;                /* initialized at declaration */
switch (position) {
case 0: x = base; y = base; break;
case 1: x = base + i; y = base - i; break;
default: x = 1; break;
}
setCursorPosition(x, y);
```

- **관련**: CWE-457

## 43. 신뢰할 수 없는 데이터의 역직렬화

신뢰할 수 없는 출처의 직렬화된 데이터를 검증 없이 역직렬화하기 때문에, 무결성 상실, 원격 코드 실행, 서비스 거부가 발생할 수 있습니다.

- **탐색**: `ObjectInputStream.readObject`, `XMLDecoder.readObject`, `readUnshared`, 요청 본문, 업로드 파일, 소켓, 쿠키, 캐시의 역직렬화, Python `pickle.loads`
- **정탐** `R`: 데이터가 사용자나 소켓(또는 다른 신뢰할 수 없는 출처)에서 오고 검증 단계가 없습니다. 예를 들어 `new ObjectInputStream(req.getInputStream()).readObject()`나 사용자가 제공한 XML에 사용한 `XMLDecoder`가 해당합니다
- **오탐** `R`: 역직렬화하기 전에 무결성을 검증합니다. 예를 들어 송신자가 계산한 HMAC을 수신자가 다시 계산해서 비교합니다
- **조치** `G`: 신뢰할 수 없는 데이터를 역직렬화하지 않습니다. 그렇지 않으면 송신 측에서 데이터에 서명하고 수신 측에서 서명을 검증하거나, 예상하는 클래스만 허용하거나(허용 목록으로 `resolveClass`를 재정의), 제한된 권한으로 역직렬화합니다
- **조치** `D`: Java 9 이상에서는 `ObjectInputFilter`가 서브클래스를 만들지 않고도 같은 허용 목록을 제공합니다. 타입 정보가 없는 데이터 형식(알려진 클래스에 매핑하는 일반 JSON)을 우선 사용합니다

```java
class AllowlistObjectInputStream extends ObjectInputStream {
    private final Set<String> allowed;
    AllowlistObjectInputStream(InputStream in, Set<String> allowed) throws IOException { super(in); this.allowed = allowed; }
    @Override protected Class<?> resolveClass(ObjectStreamClass desc) throws IOException, ClassNotFoundException {
        if (!allowed.contains(desc.getName())) throw new InvalidClassException("Unexpected class", desc.getName());
        return super.resolveClass(desc);
    }
}
```

- **관련**: CWE-502 (진단가이드는 CWE-918을 인용하는데, 이는 복사 오류입니다)
