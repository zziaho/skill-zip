# 보안기능

보안약점 18번부터 33번까지입니다. 인증, 접근 통제, 기밀성, 암호화, 권한 관리를 잘못 구현했을 때 발생합니다. 가이드는 이 유형 안에서 1번부터 16번까지 번호를 붙이지만, 이 파일은 전체 번호인 18번부터 33번까지를 사용합니다.

항목의 구성은 `input-validation_ko.md`와 같습니다. **탐색**, **정탐**(Vulnerable), **오탐**(Not vulnerable), **조치**, **관련**으로 이루어집니다.

이 파일의 항목 중에는 정적 도구로 판단할 수 없는 것이 많습니다. 진단가이드에 따르면 무엇을 중요정보나 중요 기능으로 볼지는 진단원이 결정해야 합니다. 검토하기 전에 프로젝트의 중요정보(패스워드, 주민등록번호, 여권번호와 외국인등록번호, 카드번호와 계좌번호, 인증 데이터)와 중요 기능(결제, 이체, 개인정보나 패스워드 변경, 권한 부여, 관리자 기능, 게시물 수정이나 삭제)을 나열해 둡니다.

## 18. 적절한 인증 없는 중요기능 허용

적절한 인증 없이 중요정보를 읽거나 변경할 수 있습니다.

- **탐색**: 위에서 나열한 중요 기능의 핸들러, JavaScript로 수행하는 인증 검사, 해당 URL을 `permitAll()`로 허용하는 Spring Security 설정
- **정탐** `R`
  - 중요 기능이 재인증 없이 실행됩니다. 예를 들어 이체 요청이 송금 서비스를 직접 호출합니다
  - 검사가 클라이언트에서만 실행되어(`if (allowedIp == false) { alert(...); history.back(); }`) 우회할 수 있습니다
  - 요청한 사용자가 로그인한 사용자와 같은지 확인하지 않고 수정 요청을 처리합니다
- **오탐** `R`: 기능이 실행되기 전에 서버가 인증을 확인하고, 중요 기능은 재인증합니다
- **조치** `G`: 클라이언트 측 검사를 우회할 수 없도록 설계하고, 중요한 페이지에서 재인증하며, 보안 기능에는 검증된 프레임워크나 라이브러리를 사용합니다
- **`D`**: 개발보안 가이드의 안전한 예시는 두 ID 중 하나가 null이면 비교를 건너뛰고 수정을 진행합니다. 아래 예시처럼 요청을 거부합니다

```java
String loginId = (String) session.getAttribute("userId");
if (loginId == null || !loginId.equals(member.getUserId())) {
    throw new AccessDeniedException("not the owner");      // compare before modifying
}
service.modifyMember(member);
```

- **관련**: CWE-306 · SR2-1

## 19. 부적절한 인가

모든 실행 경로에서 접근 통제를 검사하지 않거나 불완전하게 검사하기 때문에, 공격자가 접근할 수 있는 경로로 정보가 유출됩니다.

- **탐색**: 역할이나 ACL 검사(`@PreAuthorize`, `@Secured`, 보안 설정의 `hasRole`, 또는 직접 작성한 검사) 없이 데이터를 읽거나 생성, 변경, 삭제하는 핸들러, 익명 LDAP 바인드(`Context.SECURITY_AUTHENTICATION`을 `"none"`으로 설정), JavaScript로 수행하는 접근 통제
- **정탐** `R`
  - 데이터를 읽거나 변경하는 기능이 호출자가 미리 정의된 권한을 가졌는지 확인하지 않습니다. 예를 들어 `if ("delete".equals(action)) boardDao.delete(id);`가 해당합니다
  - 접근 통제를 클라이언트에서만 수행합니다
  - LDAP 쿼리를 익명 바인드로 실행하면서 별도의 접근 통제가 없습니다
- **오탐** `R`: 권한을 검사한 뒤에만 기능이 실행됩니다. 예를 들어 `"delete".equals(action) && checkAccessControlList(user, action)`가 해당합니다
- **데이터 수준 검사** `G`: 진단가이드의 SR2-4 설계 예시는 접근 통제를 화면, 기능, 데이터 수준으로 나눕니다. 데이터 수준에서는 기능을 호출할 수 있는 사용자라도 해당 레코드에 대한 권한을 검사해야 합니다. 개발보안 가이드의 부록(Top 10)은 ID만으로 요청을 처리해서 다른 사용자의 데이터가 노출되는 사례를 제시합니다
- **보안약점 19로 보는 데이터 수준 검사** `D`: 핸들러가 요청의 ID로 레코드를 불러오면서 사용자의 권한을 확인하지 않으면(IDOR) 보안약점 19로 보고합니다. 가이드는 데이터 수준 규칙에 보안약점 번호를 붙이지 않지만, 19의 정의(실행 경로에서 접근 통제를 불완전하게 검사함)에 이 경우도 포함됩니다
- **조치** `G`: 역할별로 기능을 부여해서 공격 표면을 줄이고 사용자별로 ACL을 관리합니다. 가이드는 JAAS Authorization Framework와 OWASP ESAPI Access Control을 제시하고, 개발보안 가이드 제3장은 Spring Security(ACL 모듈 포함)를 제시합니다

```java
@PreAuthorize("hasRole('BOARD_ADMIN') or @boardAuth.isOwner(#id, authentication)")
@PostMapping("/board/{id}/delete")
public String delete(@PathVariable long id) { boardService.delete(id); return "redirect:/board"; }
```

- **관련**: CWE-285 · SR2-4

## 20. 중요한 자원에 대한 잘못된 권한 설정

보안과 관련된 자원(설정 파일, 실행 파일, 라이브러리, 업로드 파일)에 의도하지 않게 읽기나 쓰기 권한이 부여됩니다.

- **탐색**: 두 번째 인자가 `false`인 `setReadable`, `setWritable`, `setExecutable`, `Files.setPosixFilePermissions`, `umask(0)`, `chmod 777`, `Runtime.exec("umask 0")`, 공유 디렉터리에 생성하는 파일
- **정탐** `R`: 프로그램이 생성한 파일을 모든 사용자가 읽거나 쓸 수 있습니다. 설정 파일이나 문서 파일에 실행 권한이 있습니다
- **오탐** `R`: 실행 권한과 쓰기 권한을 제거하고 읽기 권한을 소유자로 제한합니다. 예를 들어 `setExecutable(false); setReadable(true); setWritable(false);`가 해당합니다
- **조치** `G`: 설정 파일, 실행 파일, 라이브러리는 소프트웨어 관리자만 읽고 쓸 수 있게 하고, 파일에는 최소 권한(소유자만 읽기)을 부여합니다

```java
file.setReadable(true, false);   // Vulnerable: every user
// Safe: set the full permission set; setReadable(true) alone only adds the owner's bit
Files.setPosixFilePermissions(file.toPath(), PosixFilePermissions.fromString("rw-------"));
```

```c
umask(0);     /* Vulnerable: files readable and writable by everyone */
umask(077);   /* Safe: no permission for group and others */
```

- **관련**: CWE-732 · SR2-4

## 21. 취약한 암호화 알고리즘 사용

취약하거나 표준이 아닌 알고리즘을 사용하거나, 인코딩을 암호화로 착각합니다.

- **탐색**: `DES`, `RC2`, `RC4`, `RC5`, `RC6`, `MD4`, `MD5`, `SHA1`을 사용하는 `Cipher.getInstance`, `MessageDigest.getInstance`, `Mac.getInstance`, `KeyGenerator`. 패스워드를 "보호"하려고 사용한 Base64, 직접 만든 암호 코드, OpenSSL `EVP_des_*`
- **정탐** `R`
  - 가이드가 나열한 취약한 알고리즘 중 하나입니다: RC2, RC4, RC5, RC6, MD4, MD5, SHA1, DES
  - 직접 구현한 알고리즘입니다(암호 전문가가 보증하는 경우는 제외합니다)
  - 설정 파일에 Base64로 인코딩해서 저장한 패스워드입니다. Base64 자체는 취약한 알고리즘이 아니지만, 개발자가 데이터를 보호하려고 사용했다면 정탐입니다
- **오탐** `R`: AES, SEED, ARIA, SHA-256 같은 표준 알고리즘입니다
- **조치** `G`: 검증된 표준 알고리즘을 사용하고, 업무 데이터나 개인정보에는 IT 보안인증사무국이 검증한 암호모듈(검증필 암호모듈)을 사용합니다. 가이드의 표(암호알고리즘 검증기준 Ver 2.0, 2012)는 다음을 제시합니다. 블록 암호는 ARIA(128/192/256비트 키)와 SEED(128)입니다. 해시는 SHA-224/256/384/512입니다. 메시지 인증은 HMAC, CMAC, GMAC입니다. 난수 생성기는 HASH_DRBG, HMAC_DRBG, CTR_DRBG입니다. 공개키 암호는 키 길이가 2048비트나 3072비트인 RSAES입니다. 전자서명과 키 설정은 RSA-PSS(2048비트나 3072비트 키), KCDSA, ECDSA, EC-KCDSA, DH, ECDH입니다
- **조치** `D`
  - 개발보안 가이드는 DES의 대체 알고리즘으로 3DES를 제시합니다. 이를 권장하지 않습니다. NIST가 2023년 이후 암호화에 TDEA를 허용하지 않았기 때문입니다(SP 800-131A Rev. 2). AES, ARIA, SEED를 사용합니다
  - 이 표는 2012년 자료입니다. 신규 시스템은 KISA의 최신 『암호 알고리즘 및 키 길이 이용 안내서』를 확인합니다(이 스킬에서는 검증하지 않았습니다)
  - 이 표는 기밀성 모드에 ECB를 포함합니다("ECD"로 적혀 있으며, 오기로 보입니다). 무작위 IV를 사용하는 인증 모드(GCM, CCM)를 우선 사용합니다

```java
Cipher.getInstance("DES");                    // Vulnerable
Cipher.getInstance("AES/GCM/NoPadding");      // Safe (the guide's example uses AES/CBC/PKCS5Padding)
```

- **관련**: CWE-327 · SR2-6

## 22. 암호화되지 않은 중요정보

중요 데이터를 평문으로 저장하거나 전송합니다.

- **탐색**: DB 컬럼, 파일, 로그, 쿠키에 기록하는 패스워드와 개인정보, 이를 전달하는 `Socket`/`http://` 연결, 설정 파일에 패스워드가 들어 있는 연결 문자열, HTTPS 사이트에서 `setSecure(true)`가 없는 쿠키
- **정탐** `R`
  - 저장: 요청이나 소켓에서 읽은 패스워드를 그대로 DB나 파일에 기록합니다. 설정 파일에 DB 패스워드를 평문으로 보관합니다
  - 전송: 패스워드를 평문 소켓에 씁니다. 보안 채널이 아니라 HTTP로 데이터를 보냅니다. URL이 중요한 값을 암호화하지 않고 전달합니다. 중요 데이터가 담긴 쿠키에 secure 속성이 없습니다
  - 중요 데이터를 담았던 임시 변수를 사용한 뒤에 지우지 않습니다(가이드는 진단할 때 이 부분을 확인하라고 요구합니다)
- **오탐** `R`: 저장하기 전에 데이터를 암호화하거나 해시하고, 암호화된 채널로만 전송합니다. 가이드는 별도의 오탐 예시를 제시하지 않습니다
- **조치** `G`: 개인정보, 금융 정보, 패스워드를 저장할 때와 전송할 때 암호화합니다(TLS/HTTPS). 쿠키에 secure 속성을 설정하고, 중요 데이터의 읽기와 쓰기를 권한이 있는 사용자로 제한합니다. 패스워드는 솔트를 적용한 해시로 저장합니다(보안약점 31)

```java
// Vulnerable: plaintext password stored
stmt.setString(2, request.getParameter("pwd"));

// Safe: salted hash (see weakness 31 for the recommended algorithm)
stmt.setString(2, passwordEncoder.encode(request.getParameter("pwd")));
```

- 나중에 복호화해야 하는 데이터(주민등록번호, 계좌번호)는 보안약점 21번과 24번의 알고리즘과 키 길이로 암호화해야 합니다. 이 항목은 그 알고리즘과 키 길이를 정하지 않습니다. 설계 기준 SR2-7은 한국 법령이 암호화를 요구하는 대상을 나열합니다
- **관련**: CWE-312, CWE-319 · SR2-7, SR2-8

## 23. 하드코드된 중요정보

패스워드나 암호화 키가 소스 코드에 적혀 있습니다. 코드와 함께 유출되며 변경하기도 어렵습니다.

- **탐색**: `DriverManager.getConnection`, `SecretKeySpec`, `NetworkCredential`, `setPassword`에 전달하는 문자열 상수나 바이트 배열 상수, `PASS`, `PASSWORD`, `KEY`, `SECRET`이라는 이름의 상수, 입력과 비교하는 리터럴 해시
- **정탐** `R`
  - 사용자, 관리자, 서버 접속 패스워드가 코드의 리터럴입니다
  - 코드에 리터럴로 저장한 **암호화된** 패스워드도 정탐입니다
  - 암호화 키가 리터럴입니다. 예를 들어 `SecretKeySpec`에 전달하는 `byte[] key = {'6','8','a','f', ...}`가 해당합니다
- **오탐** `R`: 알고리즘 이름을 가리키는 리터럴입니다. 예를 들어 `new SecretKeySpec(key, "DESede")`에서 `key`가 외부에서 옵니다
- **조치** `G`: 패스워드를 별도의 파일에 암호화해서 저장하고 사용할 때 복호화합니다. 키는 코드 밖에 보관합니다(암호화한 외부 파일, C에서는 환경 변수)

```java
private static final String PASS = "SCOTT";                       // Vulnerable
String pass = decrypt(props.getProperty("db.password.enc"));      // Safe: encrypted value outside the code
```

- **관련**: CWE-259, CWE-321 · SR2-3, SR2-5 · `egovframe` PMD 규칙 12 AvoidUsingHardCodedIP, 22 HardCodedCryptoKey

## 24. 충분하지 않은 키 길이 사용

검증된 알고리즘을 사용하지만 키가 짧아서 빠르게 찾아낼 수 있습니다.

- **탐색**: `KeyPairGenerator.initialize(n)`, `KeyGenerator.init(n)`, `RSA_generate_key(n, ...)`, 설정에 있는 키 크기
- **정탐** `R`: 진단가이드의 최소 기준보다 짧습니다. 대칭키(AES, ARIA, SEED)는 128비트, 해시 함수는 128비트, 공개키 알고리즘(RSA, DSA)은 2048비트, ECC는 256비트입니다. 예를 들어 1024비트나 512비트 RSA가 해당합니다
- **오탐** `R`: 이 최소 기준 이상입니다
- **조치** `G`: RSA는 2048비트 이상, 대칭 알고리즘은 128비트 이상을 사용합니다
- 가이드의 알고리즘 표(보안약점 21)는 위와 달리 최소 112비트의 보안 강도를 제시합니다. 이 스킬은 위의 더 엄격한 수치를 적용합니다. 2030년 이후에도 사용하는 시스템에는 개발보안 가이드 제3장의 NIST 표가 128비트 보안 강도(RSA 3072, ECC 256)를 요구합니다

```java
keyGen.initialize(1024);   // Vulnerable
keyGen.initialize(2048);   // Safe
```

- **관련**: CWE-326 · SR2-6

## 25. 적절하지 않은 난수값 사용

예측할 수 없어야 하는 곳에 예측 가능한 난수를 사용합니다.

- **탐색**: 세션 ID, 토큰, 키, 임시 패스워드, 인증 코드에 사용한 `Math.random()`, `new Random(...)`, `java.util.Random`, C `rand()`, `random()`
- **정탐** `R`
  - `Math.random()`(진단가이드는 모든 사용을 정탐으로 판단합니다)
  - 시드를 고정한 `java.util.Random`
  - 세션 ID나 그 밖의 보안 결정 값으로 사용하는 난수가 `SecureRandom`에서 나온 것이 아닙니다
- **오탐** `R`: 보안 결정에 `java.security.SecureRandom`을 사용합니다. 진단가이드는 직접 만든 난수 키를 날짜 요소로 보강한 값(날짜 범위로 조정한 난수)도 안전하다고 판단합니다
- **날짜 요소에 대한 `D`**: 시간은 예측할 수 있으므로, 시간을 섞는다고 해서 `Math.random()`이나 `java.util.Random`이 보안 값에 쓸 만해지지는 않습니다. 이 오탐 사례는 바탕이 되는 생성기가 `SecureRandom`이거나(가이드의 코드처럼) 그 값을 보안 결정에 사용하지 않을 때만 인정합니다
- **`java.util.Random`에 대한 `D`**: 진단가이드의 한 문장은 `java.util.Random`이 정탐이 아니라고 하지만, 같은 가이드와 개발보안 가이드는 보안 결정에 사용하기에 안전하지 않다고 하고, 그 문장 아래에 제시한 오탐 코드도 `SecureRandom`만 사용합니다. `java.util.Random`이 보안 값을 만들어 낼 때는 보고하고, 보안과 무관한 용도(표시 목록 섞기)에는 보고하지 않습니다
- **조치** `G`: 세션 ID, 키, 그 밖의 보안 값에는 `SecureRandom`을 사용합니다. C에서는 변하는 값(시간을 사용한 `srand`/`srandom`)으로 시드를 설정합니다. 보안 값에는 플랫폼의 암호학적 생성기를 사용합니다(`D`: 시간 시드는 예측할 수 있습니다)

```java
String weak = Long.toString(new Random().nextLong());                 // Vulnerable for a token
byte[] b = new byte[32]; new SecureRandom().nextBytes(b);             // Safe
String token = Base64.getUrlEncoder().withoutPadding().encodeToString(b);
```

- **관련**: CWE-330 · SR2-6

## 26. 취약한 비밀번호 허용

회원 가입이나 패스워드 변경에서 강력한 패스워드 규칙을 강제하지 않습니다.

- **탐색**: 회원 가입과 패스워드 변경 핸들러, 패스워드 정책 검증기
- **정탐** `R`: 패스워드를 생성하거나 변경할 때 null, 길이, 문자 종류를 검사하지 않거나 검사가 약합니다. 복잡도를 검사하지 않고 가입을 승인합니다
- **오탐** `R`: 로그인할 때 패스워드를 확인하기만 하는 코드(패스워드를 설정하지는 않습니다), 인증하려고 설정에서 패스워드를 읽는 코드
- **조치** `G`: SR2-3이 인용하는 KISA 규칙(『패스워드 선택 및 이용 안내서』)을 적용합니다. 문자 종류(대문자, 소문자, 숫자, 특수문자) 중 두 가지 이상을 조합해서 8자 이상이거나, 10자 이상이어야 합니다. 반복 패턴이나 키보드 배열 패턴, 개인정보, 사용자 ID, 사전 단어, 유사 문자 치환을 거부하고, 주기적인 변경을 요구합니다
- **조치** `D`: 가이드의 정규식 `((?=.*[a-zA-Z])(?=.*[0-9@#$%]). {9, })`는 불필요한 공백이 들어 있고 영문자와 숫자 한 개만 있어도 통과합니다. 이를 복사하지 않습니다

```java
static boolean acceptable(String pw, String userId) {
    if (pw == null || pw.contains(userId)) return false;
    long kinds = Stream.of("[a-z]", "[A-Z]", "[0-9]", "[^a-zA-Z0-9]")
                       .filter(r -> Pattern.compile(r).matcher(pw).find()).count();
    return (kinds >= 2 && pw.length() >= 8) || pw.length() >= 10;
}
```

- **관련**: CWE-521 · SR2-3

## 27. 부적절한 전자서명 확인

서명된 파일(예: JAR)을 서명이나 서명자를 검증하지 않고 사용합니다.

- **탐색**: 다운로드하거나 업로드한 JAR에 사용하는 `new JarFile(...)`, `JarInputStream`, `URLClassLoader`. 결과를 무시하는 `Signature.verify`
- **정탐** `R`: 검증 없이 `new JarFile(f)`를 사용합니다. `new JarFile(f, true)`를 사용하지만 `getCodeSigners()`로 서명자를 확인하지 않습니다
- **오탐** `R`: `new JarFile(f, true)`를 사용하고, 모든 엔트리를 읽고, `getCodeSigners()`가 존재하는지 확인합니다
- **조치** `G`: 항상 서명을 검증하고, 신뢰할 수 없는 출처가 서명한 파일은 사용하지 않습니다
- **조치** `D`: 가이드는 서명자가 존재하는지만 확인합니다. 서명자 인증서가 기대하는 배포자와 일치하는지도 비교합니다

```java
try (JarFile jar = new JarFile(file, true)) {
    for (JarEntry e : Collections.list(jar.entries())) {
        if (e.isDirectory() || e.getName().startsWith("META-INF/")) continue;   // manifest and signature files are unsigned
        try (InputStream in = jar.getInputStream(e)) { in.readAllBytes(); }   // reading triggers verification
        CodeSigner[] signers = e.getCodeSigners();
        if (signers == null || !trusted(signers)) throw new SecurityException(e.getName());
    }
}
```

- **관련**: CWE-347 · SR1-10

## 28. 부적절한 인증서 유효성 검증

인증서를 검사하지 않거나 불완전하게 검사해서, 프로그램이 악의적인 호스트에 접속하거나 그 호스트의 데이터를 수락합니다. (가이드의 요약 목록은 이름을 "부적절한 인증서 인증서 유효성 검증"으로 적고 있으며, 항목 제목에는 한 번만 나옵니다.)

- **탐색**: OpenSSL `SSL_get_verify_result`, `SSL_get_peer_certificate`, `SSL_set_verify`, Java `X509TrustManager`와 `HostnameVerifier` 구현, 직접 만든 trust manager를 사용하는 `SSLContext.init`, 모든 인증서를 신뢰하도록 설정한 HTTP 클라이언트
- **정탐** `R`
  - 검증 결과를 확인하지 않고 상대방의 인증서를 사용합니다
  - `X509_V_OK`가 아닌 결과를 수락합니다. 예를 들어 `X509_V_ERR_SELF_SIGNED_CERT_IN_CHAIN`이 해당합니다
  - 인증서는 검증하지만 호스트 이름(Common Name)은 검증하지 않습니다
- **정탐** `D`: `checkServerTrusted`가 비어 있는 Java trust manager, 항상 `true`를 반환하는 `HostnameVerifier`. 가이드에는 이에 대한 Java 예시가 없지만 같은 보안약점입니다
- **조치** `G`: 사용하기 전에 이름이 호스트와 일치하는지, 신뢰할 수 있는 CA가 서명했는지, 유효 기간 안에 있는지, 폐기되지 않았는지(CRL이나 OCSP), 안전한 알고리즘을 사용하는지 확인합니다

```c
SSL_set_verify(ssl, SSL_VERIFY_PEER, NULL);
SSL_set1_host(ssl, "www.example.go.kr");
X509 *cert = SSL_get_peer_certificate(ssl);
if (cert == NULL || SSL_get_verify_result(ssl) != X509_V_OK) { /* abort */ }
```

```java
toVerify.verify(caCert.getPublicKey());   // signed by the CA
toVerify.checkValidity();                 // within the validity period
```

- **관련**: CWE-295 · SR2-1, SR2-6

## 29. 사용자 하드디스크에 저장되는 쿠키를 통한 정보노출

수명이 긴 쿠키가 디스크에 기록되면 중요한 값을 탈취하기가 더 쉬워집니다.

- **탐색**: `Cookie.setMaxAge`, `ResponseCookie.maxAge`, remember-me 쿠키
- **정탐** `R`: 브라우저로 전송한 쿠키의 수명이 지나치게 깁니다(가이드의 예시: 1년, 약 360일, 10년). 진단가이드의 정탐 예시는 값이 `"YES"`뿐인 remember-me 쿠키이므로, 수명이 긴 것만으로도 정탐으로 판단합니다. 진단할 때는 쿠키가 ID, 역할, 세션 ID 같은 중요 데이터를 담고 있는지도 확인합니다
- **오탐** `R`: 수명이 그 기능에 필요한 최소 기간입니다(가이드의 예시: Java에서 1일, C#에서 10분)
- **조치** `G`: 세션 길이를 고려해서 만료 시간을 최소로 설정하고, 중요 데이터를 지속 쿠키에 넣지 않습니다. 가이드는 수치 한계를 제시하지 않습니다
- 쿠키 속성(`HttpOnly`, `Secure`)은 이 항목이 아니라 SR4-1과 보안약점 22에서 다룹니다

```java
cookie.setMaxAge(60 * 60 * 24 * 365);   // Vulnerable: one year on disk
cookie.setMaxAge(60 * 60 * 24);         // Safe in the guides' example
```

- **관련**: CWE-539 · SR2-7

## 30. 주석문 안에 포함된 시스템 주요정보

패스워드나 그 밖의 시스템 비밀 정보가 주석에 남아 있습니다.

- **탐색**: DB 접속과 관리자 로그인 코드 근처의 주석, `password`, `passwd`, `pwd`, `비밀번호`, `암호`, `root`, 계정 ID, 해시, 키가 들어 있는 주석
- **정탐** `R`: 주석에 실제 패스워드, 계정, 키 또는 암호화 전후의 값이 들어 있습니다
- **오탐** `R`: 주석에 "password"나 "비밀번호"라는 단어는 있지만 실제 비밀 정보는 없습니다
- **조치** `G`: ID, 패스워드, 그 밖의 보안 정보를 주석에 적지 않으며, 개발하는 동안 남긴 것은 삭제합니다

```java
// DB연결 root / a1q2w3r3f2!@     <- Vulnerable: delete the comment
```

- **관련**: CWE-615 · SR2-5

## 31. 솔트 없이 일방향 해쉬함수 사용

패스워드를 솔트 없이 해시하기 때문에, 미리 계산한 테이블(레인보우 테이블)로 복원됩니다.

- **탐색**: 솔트를 `update`하지 않고 `digest(password...)`를 호출하는 `MessageDigest.getInstance(...)`, 패스워드만으로 계산하는 C# `ComputeHash`, 로그인 코드에서 비교하는 해시
- **정탐** `R`: SHA-512 같은 강력한 해시를 사용하더라도 패스워드만으로 해시를 계산합니다
- **오탐** `R`: 안전한 해시 알고리즘을 사용하고, 다이제스트를 생성하기 전에 솔트를 추가합니다
- **조치** `G`: 패스워드를 솔트와 함께 해시합니다. SR2-3은 패스워드마다 고유한 무작위 솔트가 필요하며, 32바이트 이상이면 추측하기 어렵고, 해시는 서버에서 수행해야 한다고 덧붙입니다
- **조치** `D`: 솔트를 적용한 SHA-2는 이 보안약점을 통과하지만, 빠른 해시 하나만으로는 무차별 대입을 막기 어렵습니다. 솔트와 반복 연산을 대신 처리하는 패스워드 해시 함수(PBKDF2, bcrypt, Argon2)를 권장합니다. 개발보안 가이드의 SSO 부록도 bcrypt와 Argon2를 제시합니다

```java
md.update(password.getBytes(UTF_8));                          // Vulnerable: no salt
return md.digest();

PasswordEncoder encoder = new BCryptPasswordEncoder();        // Recommended (D)
String stored = encoder.encode(password);                     // salt generated and embedded
```

- **관련**: CWE-759 · SR2-6 (SR2-3 요구사항 3도 솔트를 적용한 패스워드 해시를 다루지만, 대응표에는 SR2-6만 나열되어 있습니다)

## 32. 무결성 검사 없는 코드 다운로드

소스 코드나 실행 파일을 무결성을 검사하지 않고 다운로드해서 실행하기 때문에, 호스트 침해, DNS 스푸핑, 전송 중 변조가 발생하면 공격자의 코드가 실행됩니다.

- **탐색**: `URLClassLoader`, `Class.forName(..., loader)`, `defineClass`, 다운로드해서 실행하는 스크립트나 바이너리, 플러그인과 업데이트 메커니즘
- **정탐** `R`: 체크섬을 비교하거나 서명을 검증하지 않고 코드를 로드합니다
- 가이드는 정탐 코드와 오탐 코드를 제시하지 않으며, 위의 진단 방법이 판단 기준입니다
- **조치** `G`: 로드하기 전에 체크섬이나 서명을 검증하고, 보호된 채널로 코드를 전송하며, 최소 권한으로 실행합니다
- **조치** `D`: 가이드의 Java 예시는 서명이 아니라 "개인키로 암호화"하고, C 예시는 다운로드 호출이 성공했는지만 확인합니다. 고정한 공개키로 서명을 검증하거나, 별도의 신뢰할 수 있는 채널로 얻은 해시와 비교합니다

```java
byte[] jar = Files.readAllBytes(downloaded);
Signature sig = Signature.getInstance("SHA256withRSA");
sig.initVerify(publisherKey);
sig.update(jar);
if (!sig.verify(signatureBytes)) throw new SecurityException("tampered");
// load only after verification
```

- **관련**: CWE-494 · SR1-10

## 33. 반복된 인증시도 제한 기능 부재

로그인 시도를 제한하지 않으면 사전 대입 공격과 무차별 대입 공격이 가능합니다.

- **탐색**: 로그인 핸들러, OTP와 인증 코드 검사, 패스워드 재설정 질문의 답변, 인증 반복문
- **정탐** `R`: 시도 횟수를 세어서 제한하는 코드 없이 인증 기능을 반복해서 호출할 수 있습니다
- 가이드는 오탐 예시를 제시하지 않습니다
- **조치** `G`: 시도 횟수를 적절한 수로 제한하고, 그 횟수를 넘으면 계정을 잠그거나 추가 인증을 요구합니다. 구현 예시는 5회를 사용하며, SR2-2는 3회에서 5회라고 설명하고 그 산출물 예시는 5회라고 설명합니다
- **조치** `G` (SR2-2): 실패 횟수, 잠금 상태, 마지막 성공 시각과 실패 시각을 계정별로 DB에 저장하고, 실패한 시도(ID, 시각, IP)를 로그로 남깁니다. 가이드의 Java 예시는 지역 반복문 안에서 횟수를 세므로 요청마다 초기화됩니다. 서버에서 요청 전체에 걸쳐 횟수를 셉니다

```java
if (account.getFailCount() >= MAX_ATTEMPTS) throw new LockedException("locked");
if (!encoder.matches(pw, account.getPasswordHash())) {
    accountRepository.increaseFailCount(account.getId());   // persisted, not a local counter
    throw new BadCredentialsException("invalid");
}
accountRepository.resetFailCount(account.getId());
```

- **관련**: CWE-307 · SR2-2
