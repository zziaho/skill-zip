# Time and State, Error Handling, Code Errors (시간 및 상태, 에러처리, 코드오류)

Weaknesses 34 to 43:

| Type | Numbers | Cause |
|------|---------|-------|
| 시간 및 상태 (time and state) | 34, 35 | Time and state managed wrongly in parallel or multi-process environments |
| 에러처리 (error handling) | 36 to 38 | Errors not handled, or handled so that sensitive information leaks |
| 코드오류 (code errors) | 39 to 43 | Coding mistakes such as type errors and wrongly released resources |

The item format is the same as in `input-validation.md`. Only weaknesses 36 and 39 map to a design criterion (SR3-1 and SR1-9). The development guide (chapter 3) notes that some weaknesses can be removed by following coding rules alone.

## 34. 경쟁조건: 검사시점과 사용시점 (TOCTOU race condition)

A resource is checked and then used, and its state changes in between because another process or thread uses it at the same time.

- **Find**: `File.exists()`, `canRead()`, `isFile()` followed by open, read or delete; C `access()` followed by `fopen()`; shared files, sockets or devices used by several threads or processes; unsynchronized updates of shared variables in C
- **Vulnerable** `R`: one shared resource can be accessed by several threads or processes at once without synchronization (for example one thread reads a file after `exists()` while another deletes it after `exists()`)
- **Not vulnerable** `R`
  - Access is synchronized, or goes through a pool-style module that manages the shared resource
  - No race actually occurs, for example code that only lists files and formats their names and sizes
  - In Java, opening a stream after `exists()` throws `IOException` if the file has gone; handling that exception is enough (per the diagnostic guide)
- **Fix** `G`: let one process at a time access the shared resource with a synchronization construct (`synchronized`, mutex), and synchronize only the critical section
- **Fix** `D`: the guides' examples cover threads in one process. Between processes, use an atomic operation instead of check-then-use (`Files.createFile`, `Files.delete` and handle the exception, `O_CREAT | O_EXCL` in C) or a file lock

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

- **Related**: CWE-367

## 35. 종료되지 않는 반복문 또는 재귀함수 (infinite loop or uncontrolled recursion)

A loop or recursion has no reachable exit, so it exhausts memory or stack and stops the service.

- **Find**: methods that call themselves with the same name, number and types of parameters; `while (true)` and loops whose exit depends on input
- **Vulnerable** `R`: a recursive call (same name, parameter count and parameter types) with no control statement that can return, for example `return n * factorial(n - 1);`
- **Not vulnerable** `R`
  - A condition returns before recursing (for example returning when the child list is empty)
  - The call has the same name but different parameter types, so it calls an overload, not itself
- **Fix** `G`: implement the base case of every recursion, and limit recursion by a count or a constant
- The guides' diagnosis covers recursion only. Judge loops by the same rule (`D`): a loop whose exit condition can never become true, or depends on input with no bound, is vulnerable

```c
int factorial(int i) {
    if (i <= 1) return 1;          /* base case */
    return i * factorial(i - 1);
}
```

- **Related**: CWE-674, CWE-835

## 36. 오류 메시지 정보노출 (information exposure through error messages)

Error messages or stack traces show the execution environment, users or internal data.

- **Find**: `printStackTrace()`, `e.getMessage()` or `e.toString()` written to the response or page, `System.err.print(e...)`, JSP error output, Spring error pages with `server.error.include-stacktrace` or `include-message` enabled, `web.xml` without `error-page`
- **Vulnerable** `R`: an error output reveals environment, user or internal data, for example `catch (Exception e) { e.printStackTrace(); }` in a servlet or JSP
- **Not vulnerable** `R`: the exception goes to a server-side logger (the diagnostic guide's false-positive example uses `logger.error(e, e)`)
- **Fix** `G`: handle exceptions internally and show users only a predefined message without sensitive information. Define error codes and log only what is needed. The design criterion SR3-1 adds a default error page for `java.lang.Throwable`, 404 and 500 in `web.xml` or the server settings

```java
catch (IOException e) { e.printStackTrace(); }                 // Vulnerable
catch (IOException e) { logger.error("ERROR-01: file open failed", e); }   // Safe: server log only
```

- **Related**: CWE-209, CWE-497 · SR3-1 · `egovframe` PMD rule 7 AvoidPrintStackTrace

## 37. 오류 상황 대응 부재 (no action on error condition)

An error is detected but nothing is done, so the program continues in a state the developer did not intend.

- **Find**: empty `catch` blocks, catch blocks with only a comment, ignored return values of error-reporting functions in C
- **Vulnerable** `R`: an exception is caught and no action follows, so the program goes on without knowing what happened. In the development guide's example a missing password raises `NullPointerException`, the empty catch swallows it, and the user is treated as authenticated; the diagnostic guide's example is an empty `catch (SQLException e)` in a DB connection method
- The guides give no false-positive example
- **Fix** `G`: handle errors with a control statement (`try-catch`, `if`, `switch`) and take a suitable action for each exception
- **Fix** `D`: the guides' safe example puts `e.getMessage()` into the user's message, which can conflict with weakness 36. Log the exception and show a fixed message

```java
catch (SQLException e) { }                                      // Vulnerable: error swallowed
catch (SQLException e) {                                        // Safe: logged and reported
    logger.error("ERROR-03: DB connection failed", e);
    throw new ServiceException("ERROR-03", e);
}
```

- **Related**: CWE-390 · `egovframe` PMD rule 16 EmptyCatchBlock

## 38. 부적절한 예외 처리 (improper exception handling)

Return values or exceptional conditions are not checked properly, or exceptions are caught too broadly.

- **Find**: `catch (Exception e)`, `catch (Throwable t)`, `catch (RuntimeException e)` around specific operations; ignored return values
- **Vulnerable** `R`: a broad catch where specific exceptions can be named, for example `catch (Exception ex)` around file reading
- The guides give no explicit false-positive rule. `D`: a broad catch at the outermost boundary (a global exception handler, a thread's top loop) that logs and returns a generic error is normal practice; report broad catches around specific operations
- **Fix** `G`: check the result of every function that returns a value, catch specific exceptions instead of broad ones, and handle them in the order they can occur

```java
catch (Exception e) { ... }                                     // Vulnerable
catch (MalformedURLException e) { ... }                         // Safe
catch (IOException e) { ... }
catch (ParseException e) { ... }
```

- **Related**: CWE-754 · `egovframe` PMD rule 6 AvoidCatchingGenericException

## 39. Null Pointer 역참조 (null pointer dereference)

An object assumed never to be null is dereferenced while null.

- **Find**: values that can be null used without a check: `getParameter`, `getAttribute`, `System.getProperty`, `Map.get`, DAO results, methods that `return null`, variables initialized to `null`; C pointers returned by functions
- **When a value can be null** `R` (the diagnostic guide's list): it was initialized to null; it was declared but never created; it is the result of a field access or method call on a null object; it is the result of operations on nullable objects such as strings
- **Vulnerable** `R`
  - A value that can be null is used with no null check, for example `System.getProperty("cmd").trim()`
  - A variable initialized to null is assigned only in some branches and used in all of them
  - DB resources (`ResultSet`, `Statement`) are closed in `finally` without a null check
  - The result of a method that can return null is used directly
  - The null check comes after the dereference: `if (str.length() == 0 || str == null)`
- **Not vulnerable** `R`
  - APIs or project methods documented never to return null (check the Javadoc), for example `StringTokenizer`
  - The catch block rethrows, so code after it does not run with a null value
  - Short-circuit order: `if (a == null || a.length() == 0)`
  - The dereference is inside the same `try` as the assignment, so it does not run when the assignment fails
  - JSP implicit objects (`pageContext.request.contextPath` in EL)
  - Static method calls such as `Integer.parseInt(value)` (the class is not a null object)
  - A parameter that might be null inside a single method with no data flow showing a null caller; the caller should check
  - Constructors of JRE classes, unless documented to return null
  - When the same null variable is dereferenced on consecutive lines, the first dereference stops execution: report only the first
- **Fix** `G`: check references that can be null before use

```java
if ((obj == null && elt == null) || (obj != null && obj.equals(elt))) { ... }
String url = request.getParameter("url");
if (url != null && url.equals("")) { ... }      // the guides print || here, which is a typo
```

```c
int *p = IntegerAddressReturn();
if (p != NULL) *p = count;
```

- **Related**: CWE-476 · SR1-9 · `egovframe` PMD rules 13 BrokenNullCheck, 28 MisplacedNullCheck

## 40. 부적절한 자원 해제 (improper resource release)

File descriptors, heap memory, sockets and DB connections are not returned after use, so resources run out.

- **Find**: `Connection`, `Statement`, `ResultSet`, streams, readers, sockets, channels opened without try-with-resources; `close()` called inside `try` instead of `finally`; C `fopen`, `malloc`, `socket` with early returns
- **Vulnerable** `R`
  - A branch (control statement or exception) exists where the resource is not released. Check every control flow
  - Several `close()` calls share one `try` in `finally`, so an exception from the first skips the rest
- **Not vulnerable** `R`
  - Every resource is closed in `finally`, each in its own try-catch with a null check
  - The method's job is to return the resource (`getConnection()`); the caller releases it
- **Fix** `G`: release every resource after use, in `finally`, with a null check and exception handling for each
- **Fix** `D`: in Java 7 and later, try-with-resources does this correctly and is simpler

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

- **Related**: CWE-404 · `egovframe` PMD rule 14 CloseResource

## 41. 해제된 자원 사용 (use after free)

Memory (or another resource) is used after it has been released. The guides' examples are C.

- **Find**: `free(p)` followed by any use of `p` on some path; double `free`; Java equivalents such as using a closed stream or connection (`D`)
- **Vulnerable** `R`: a release happens before a use on some control flow path, for example a message buffer freed on an error branch and then logged
- **Not vulnerable** `R`: no path from the release reaches a use
- **Also check** `R`: pointer arithmetic on resource pointers refers to valid memory, and pointers are set to NULL after use
- **Fix** `G`: do not use freed memory; store NULL in the pointer right after `free`, which also prevents double free

```c
char *temp = malloc(BUFFER_SIZE);
strncpy(temp, argv[1], BUFFER_SIZE - 1);
temp[BUFFER_SIZE - 1] = '\0';
/* ... use temp ... */
free(temp);
temp = NULL;                     /* a later free(temp) or use is now harmless or detectable */
```

- **Related**: CWE-416

## 42. 초기화되지 않은 변수 사용 (use of uninitialized variable)

A local variable is used before it is given a value, so it holds whatever was on the stack. The guides' examples are C and C++.

- **Find**: C and C++ locals declared without initializers and assigned only in some branches (`switch` without a full `default`); C++ constructors that do not initialize every field
- **Vulnerable** `R`: a variable is not initialized at declaration, or a C++ field is not initialized in a constructor (for example a default constructor that leaves a field unset)
- **Not vulnerable** `R`: initialized at declaration, or every constructor initializes the field
- **Fix** `G`: give every variable a correct initial value before use
- In Java the compiler rejects reads of unassigned locals and fields get default values; this weakness rarely applies (`D`: the guides do not discuss Java)

```c
int x = 1, y = 1;                /* initialized at declaration */
switch (position) {
case 0: x = base; y = base; break;
case 1: x = base + i; y = base - i; break;
default: x = 1; break;
}
setCursorPosition(x, y);
```

- **Related**: CWE-457

## 43. 신뢰할 수 없는 데이터의 역직렬화 (deserialization of untrusted data)

Serialized data from an untrusted source is deserialized without validation, enabling integrity loss, remote code execution or denial of service.

- **Find**: `ObjectInputStream.readObject`, `XMLDecoder.readObject`, `readUnshared`; deserialization of request bodies, uploaded files, sockets, cookies or caches; Python `pickle.loads`
- **Vulnerable** `R`: the data comes from a user or a socket (or another untrusted source) and there is no validation step, for example `new ObjectInputStream(req.getInputStream()).readObject()` or `XMLDecoder` on user-provided XML
- **Not vulnerable** `R`: integrity is verified before deserialization, for example an HMAC computed by the sender and recomputed and compared by the receiver
- **Fix** `G`: do not deserialize untrusted data. Otherwise, sign the data on the sending side and verify the signature on the receiving side, allow only expected classes (override `resolveClass` with an allowlist), or deserialize with limited privileges
- **Fix** `D`: on Java 9 and later, `ObjectInputFilter` provides the same allowlist without subclassing. Prefer data formats without type information (plain JSON mapped to known classes)

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

- **Related**: CWE-502 (the diagnostic guide cites CWE-918, which is a copying error)
