# Security Features (보안기능)

Weaknesses 18 to 33. They arise when authentication, access control, confidentiality, cryptography or privilege management is implemented wrongly. The guides number them 1 to 16 within the type; this file uses the overall numbers 18 to 33.

The item format is the same as in `input-validation.md`: **Find**, **Vulnerable** (정탐), **Not vulnerable** (오탐), **Fix**, **Related**.

Many items here cannot be judged by a static tool: the diagnostic guide says the diagnoser must decide what counts as sensitive information or a critical function. Before reviewing, list the project's sensitive data (passwords, resident registration numbers, passport and alien registration numbers, card and account numbers, authentication data) and critical functions (payment, transfer, changing personal data or passwords, granting roles, admin functions, modifying or deleting posts).

## 18. 적절한 인증 없는 중요기능 허용 (critical function without proper authentication)

Sensitive information can be read or changed without proper authentication.

- **Find**: handlers for the critical functions listed above; authentication checks done in JavaScript; Spring Security configuration that `permitAll()`s such URLs
- **Vulnerable** `R`
  - A critical function runs without re-authentication, for example a transfer that calls the send service directly
  - The check runs only on the client (`if (allowedIp == false) { alert(...); history.back(); }`) and can be bypassed
  - A modify request is processed without checking that the requested user is the logged-in user
- **Not vulnerable** `R`: the server checks authentication before the function runs and, for critical functions, re-authenticates
- **Fix** `G`: design so that client-side checks cannot be bypassed, re-authenticate on critical pages, and use verified frameworks or libraries for security functions
- **`D`**: the development guide's safe example skips the comparison when either ID is null and goes on to modify. Reject the request instead, as below

```java
String loginId = (String) session.getAttribute("userId");
if (loginId == null || !loginId.equals(member.getUserId())) {
    throw new AccessDeniedException("not the owner");      // compare before modifying
}
service.modifyMember(member);
```

- **Related**: CWE-306 · SR2-1

## 19. 부적절한 인가 (improper authorization)

Access control is not checked, or is checked incompletely, on every execution path, so information leaks through a path the attacker can reach.

- **Find**: handlers that read, create, change or delete data, without a role or ACL check (`@PreAuthorize`, `@Secured`, `hasRole` in the security configuration, or a manual check); anonymous LDAP binds (`Context.SECURITY_AUTHENTICATION` set to `"none"`); access control done in JavaScript
- **Vulnerable** `R`
  - A function that reads or changes data does not check that the caller holds the predefined permission, for example `if ("delete".equals(action)) boardDao.delete(id);`
  - Access control is done only on the client
  - An LDAP query runs with an anonymous bind and no separate access control
- **Not vulnerable** `R`: the function runs only after a permission check, for example `"delete".equals(action) && checkAccessControlList(user, action)`
- **Data-level checks** `G`: the diagnostic guide's design example for SR2-4 separates access control into screen, function and data levels. At the data level, even a user allowed to call a function must be checked for permission on the specific record. The development guide's appendix (Top 10) gives the case of requests served by ID alone exposing other users' data
- **Data-level checks as weakness 19** `D`: report a handler that loads a record by an ID from the request without checking the user's permission on it (IDOR) as weakness 19. The guides do not attach a weakness number to the data-level rule; the definition of 19 (incomplete access control on an execution path) covers it
- **Fix** `G`: assign functions by role to reduce the attack surface and manage ACLs per user. The guides name JAAS Authorization Framework and OWASP ESAPI Access Control; chapter 3 of the development guide names Spring Security (including its ACL module)

```java
@PreAuthorize("hasRole('BOARD_ADMIN') or @boardAuth.isOwner(#id, authentication)")
@PostMapping("/board/{id}/delete")
public String delete(@PathVariable long id) { boardService.delete(id); return "redirect:/board"; }
```

- **Related**: CWE-285 · SR2-4

## 20. 중요한 자원에 대한 잘못된 권한 설정 (incorrect permission on a critical resource)

Read or write permission on a security-relevant resource (configuration files, executables, libraries, uploaded files) is granted unintentionally.

- **Find**: `setReadable`, `setWritable`, `setExecutable` with `false` as the second argument; `Files.setPosixFilePermissions`; `umask(0)`, `chmod 777`, `Runtime.exec("umask 0")`; files created in shared directories
- **Vulnerable** `R`: a file the program creates is readable or writable by all users; configuration or document files have execute permission
- **Not vulnerable** `R`: execute and write permission are removed and read permission is limited to the owner, for example `setExecutable(false); setReadable(true); setWritable(false);`
- **Fix** `G`: let only the software administrator read and write configuration files, executables and libraries; give files the least permission (read for the owner only)

```java
file.setReadable(true, false);   // Vulnerable: every user
// Safe: set the full permission set; setReadable(true) alone only adds the owner's bit
Files.setPosixFilePermissions(file.toPath(), PosixFilePermissions.fromString("rw-------"));
```

```c
umask(0);     /* Vulnerable: files readable and writable by everyone */
umask(077);   /* Safe: no permission for group and others */
```

- **Related**: CWE-732 · SR2-4

## 21. 취약한 암호화 알고리즘 사용 (weak cryptographic algorithm)

Weak or non-standard algorithms are used, or encoding is mistaken for encryption.

- **Find**: `Cipher.getInstance`, `MessageDigest.getInstance`, `Mac.getInstance`, `KeyGenerator` with `DES`, `RC2`, `RC4`, `RC5`, `RC6`, `MD4`, `MD5`, `SHA1`; Base64 used to "protect" a password; home-made cipher code; OpenSSL `EVP_des_*`
- **Vulnerable** `R`
  - One of the weak algorithms the guides list: RC2, RC4, RC5, RC6, MD4, MD5, SHA1, DES
  - A self-implemented algorithm (unless a cryptography expert vouches for it)
  - A password stored Base64-encoded in a configuration file. Base64 alone is not a weak algorithm; it is vulnerable when the developer used it to protect data
- **Not vulnerable** `R`: standard algorithms such as AES, SEED, ARIA, SHA-256
- **Fix** `G`: use verified standard algorithms, and for business or personal data use a cryptographic module validated by the IT security certification office (검증필 암호모듈). The guides' table (from 암호알고리즘 검증기준 Ver 2.0, 2012) lists: block ciphers ARIA (128/192/256-bit keys) and SEED (128); hashes SHA-224/256/384/512; HMAC, CMAC, GMAC; HASH_DRBG, HMAC_DRBG, CTR_DRBG; RSAES and RSA-PSS with 2048 or 3072-bit keys; KCDSA, ECDSA, EC-KCDSA, DH, ECDH
- **Fix** `D`
  - The development guide lists 3DES as a replacement for DES. Do not recommend it: NIST disallowed TDEA for encryption after 2023 (SP 800-131A Rev. 2). Use AES, ARIA or SEED
  - The table dates from 2012. For new systems, check the current KISA 『암호 알고리즘 및 키 길이 이용 안내서』 (unverified in this skill)
  - The table lists ECB among confidentiality modes (as "ECD", likely a typo). Prefer an authenticated mode (GCM, CCM) with a random IV

```java
Cipher.getInstance("DES");                    // Vulnerable
Cipher.getInstance("AES/GCM/NoPadding");      // Safe (the guide's example uses AES/CBC/PKCS5Padding)
```

- **Related**: CWE-327 · SR2-6

## 22. 암호화되지 않은 중요정보 (sensitive information not encrypted)

Sensitive data is stored or transmitted in plaintext.

- **Find**: passwords and personal data written to DB columns, files, logs or cookies; `Socket`/`http://` connections that carry them; connection strings with passwords in configuration files; cookies without `setSecure(true)` on HTTPS sites
- **Vulnerable** `R`
  - Storage: a password read from a request or socket is written to a DB or file as it is; a configuration file holds a DB password in plaintext
  - Transmission: a password is written to a plain socket; data is sent over HTTP instead of a secure channel; a URL carries sensitive values unencrypted; a cookie with sensitive data is not marked secure
  - Temporary variables that held sensitive data are not cleared after use (the guide asks to check this as part of the diagnosis)
- **Not vulnerable** `R`: data is encrypted or hashed before storage, and sent only over an encrypted channel. The guides give no separate false-positive example
- **Fix** `G`: encrypt personal data, financial data and passwords in storage and in transit (TLS/HTTPS); set the secure attribute on cookies; restrict reading and writing of sensitive data to authorized users. Passwords are stored as salted hashes (weakness 31)

```java
// Vulnerable: plaintext password stored
stmt.setString(2, request.getParameter("pwd"));

// Safe: salted hash (see weakness 31 for the recommended algorithm)
stmt.setString(2, passwordEncoder.encode(request.getParameter("pwd")));
```

- Data that must be decrypted later (resident registration numbers, account numbers) needs encryption with the algorithms and key lengths of weaknesses 21 and 24; this item does not choose them. Design criterion SR2-7 lists what Korean laws require to be encrypted
- **Related**: CWE-312, CWE-319 · SR2-7, SR2-8

## 23. 하드코드된 중요정보 (hard-coded sensitive information)

Passwords or cryptographic keys are written in the source code. They leak with the code and are hard to change.

- **Find**: string or byte-array constants passed to `DriverManager.getConnection`, `SecretKeySpec`, `NetworkCredential`, `setPassword`; constants named `PASS`, `PASSWORD`, `KEY`, `SECRET`; literal hashes compared with input
- **Vulnerable** `R`
  - A user, admin or server connection password is a literal in the code
  - An **encrypted** password stored as a literal in the code is also vulnerable
  - A cryptographic key is a literal, for example `byte[] key = {'6','8','a','f', ...}` passed to `SecretKeySpec`
- **Not vulnerable** `R`: a literal that names an algorithm, for example `new SecretKeySpec(key, "DESede")`, where `key` comes from outside
- **Fix** `G`: store passwords encrypted in a separate file and decrypt them at use; keep keys outside the code (an encrypted external file, environment variables in C)

```java
private static final String PASS = "SCOTT";                       // Vulnerable
String pass = decrypt(props.getProperty("db.password.enc"));      // Safe: encrypted value outside the code
```

- **Related**: CWE-259, CWE-321 · SR2-3, SR2-5 · `egovframe` PMD rules 12 AvoidUsingHardCodedIP, 22 HardCodedCryptoKey

## 24. 충분하지 않은 키 길이 사용 (insufficient key length)

A verified algorithm is used with a key short enough to be found quickly.

- **Find**: `KeyPairGenerator.initialize(n)`, `KeyGenerator.init(n)`, `RSA_generate_key(n, ...)`, key sizes in configuration
- **Vulnerable** `R`: shorter than the diagnostic guide's minimums: symmetric keys (AES, ARIA, SEED) 128 bits, hash functions 128 bits, public-key algorithms (RSA, DSA) 2048 bits, ECC 256 bits. For example RSA with 1024 or 512 bits
- **Not vulnerable** `R`: at or above those minimums
- **Fix** `G`: RSA with at least 2048 bits, symmetric algorithms with at least 128 bits
- The guides' algorithm table (weakness 21) gives a 112-bit minimum security level instead; this skill applies the stricter numbers above. For systems used past 2030, the NIST table in chapter 3 of the development guide asks for 128-bit security (RSA 3072, ECC 256)

```java
keyGen.initialize(1024);   // Vulnerable
keyGen.initialize(2048);   // Safe
```

- **Related**: CWE-326 · SR2-6

## 25. 적절하지 않은 난수값 사용 (insufficiently random values)

A predictable random number is used where unpredictability matters.

- **Find**: `Math.random()`, `new Random(...)`, `java.util.Random` used for session IDs, tokens, keys, temporary passwords, verification codes; C `rand()`, `random()`
- **Vulnerable** `R`
  - `Math.random()` (the diagnostic guide judges every use vulnerable)
  - `java.util.Random` with a fixed seed
  - A random value used as a session ID or other security decision value that is not from `SecureRandom`
- **Not vulnerable** `R`: `java.security.SecureRandom` for security decisions. The diagnostic guide also judges a value safe when a self-made random key is reinforced with date elements (a random number scaled into a date range)
- **`D` on date elements**: times are predictable, so mixing them in does not make `Math.random()` or `java.util.Random` acceptable for security values. Accept that false-positive case only when the underlying generator is `SecureRandom` (as in the guide's code) or the value is not used for a security decision
- **`D` on `java.util.Random`**: one sentence of the diagnostic guide says `java.util.Random` is not vulnerable, but the same guide and the development guide say it is unsafe for security decisions, and the false-positive code shown under that sentence uses only `SecureRandom`. Report `java.util.Random` when it produces a security value; do not report it for non-security uses (shuffling a display list)
- **Fix** `G`: use `SecureRandom` for session IDs, keys and other security values. In C, seed with a changing value (`srand`/`srandom` with time); for security values use the platform's cryptographic generator (`D`: a time seed is predictable)

```java
String weak = Long.toString(new Random().nextLong());                 // Vulnerable for a token
byte[] b = new byte[32]; new SecureRandom().nextBytes(b);             // Safe
String token = Base64.getUrlEncoder().withoutPadding().encodeToString(b);
```

- **Related**: CWE-330 · SR2-6

## 26. 취약한 비밀번호 허용 (weak password allowed)

Registration or password change does not enforce strong password rules.

- **Find**: sign-up and password-change handlers; password policy validators
- **Vulnerable** `R`: no check of null, length or character classes when a password is created or changed, or the check is weak; registration approved without a complexity check
- **Not vulnerable** `R`: code that only verifies a password at login (it does not set one); code that reads a password from configuration to authenticate
- **Fix** `G`: enforce the KISA rule cited in SR2-3 (『패스워드 선택 및 이용 안내서』): at least two character classes (upper case, lower case, digits, special characters) and 8 or more characters, or 10 or more characters; reject repeated or keyboard patterns, personal information, the user ID, dictionary words and look-alike substitutions; require periodic change
- **Fix** `D`: the guides' regular expression `((?=.*[a-zA-Z])(?=.*[0-9@#$%]). {9, })` has stray spaces and accepts letters plus a single digit. Do not copy it

```java
static boolean acceptable(String pw, String userId) {
    if (pw == null || pw.contains(userId)) return false;
    long kinds = Stream.of("[a-z]", "[A-Z]", "[0-9]", "[^a-zA-Z0-9]")
                       .filter(r -> Pattern.compile(r).matcher(pw).find()).count();
    return (kinds >= 2 && pw.length() >= 8) || pw.length() >= 10;
}
```

- **Related**: CWE-521 · SR2-3

## 27. 부적절한 전자서명 확인 (improper verification of a digital signature)

A signed file (for example a JAR) is used without verifying its signature or signer.

- **Find**: `new JarFile(...)`, `JarInputStream`, `URLClassLoader` on downloaded or uploaded JARs; `Signature.verify` results ignored
- **Vulnerable** `R`: `new JarFile(f)` without verification; `new JarFile(f, true)` but the signer is never checked with `getCodeSigners()`
- **Not vulnerable** `R`: `new JarFile(f, true)`, every entry read, and `getCodeSigners()` checked to be present
- **Fix** `G`: always verify signatures, and do not use files signed by untrusted sources
- **Fix** `D`: the guides only check that signers exist. Also compare the signer certificate with the expected publisher

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

- **Related**: CWE-347 · SR1-10

## 28. 부적절한 인증서 유효성 검증 (improper certificate validation)

A certificate is not checked, or not checked fully, so the program connects to a malicious host or accepts data from it. (The guides' summary list spells the name "부적절한 인증서 인증서 유효성 검증"; the item heading has it once.)

- **Find**: OpenSSL `SSL_get_verify_result`, `SSL_get_peer_certificate`, `SSL_set_verify`; Java `X509TrustManager` and `HostnameVerifier` implementations, `SSLContext.init` with custom trust managers, HTTP clients configured to trust all certificates
- **Vulnerable** `R`
  - The peer certificate is used without checking the verification result
  - A result other than `X509_V_OK` is accepted, for example `X509_V_ERR_SELF_SIGNED_CERT_IN_CHAIN`
  - The certificate is verified but the host name (Common Name) is not
- **Vulnerable** `D`: a Java trust manager with an empty `checkServerTrusted`, or a `HostnameVerifier` that always returns `true`. The guides have no Java example of this, but it is the same weakness
- **Fix** `G`: before use, check that the name matches the host, that a trusted CA signed it, that it is within its validity period, that it is not revoked (CRL or OCSP), and that it uses a secure algorithm

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

- **Related**: CWE-295 · SR2-1, SR2-6

## 29. 사용자 하드디스크에 저장되는 쿠키를 통한 정보노출 (information exposure through persistent cookies)

Cookies with a long lifetime are written to disk, where sensitive values are easier to steal.

- **Find**: `Cookie.setMaxAge`, `ResponseCookie.maxAge`, remember-me cookies
- **Vulnerable** `R`: a cookie sent to the browser has an excessive lifetime (the guides' examples: 1 year, about 360 days, 10 years). The diagnostic guide's true-positive example is a remember-me cookie whose value is only `"YES"`, so a long lifetime alone is judged vulnerable. The diagnosis also checks whether the cookie holds sensitive data such as an ID, role or session ID
- **Not vulnerable** `R`: the lifetime is the minimum the function needs (the guides' examples: 1 day in Java, 10 minutes in C#)
- **Fix** `G`: set expiry to the minimum considering session length, and keep sensitive data out of persistent cookies. The guides give no numeric limit
- Cookie attributes (`HttpOnly`, `Secure`) are covered by SR4-1 and weakness 22, not here

```java
cookie.setMaxAge(60 * 60 * 24 * 365);   // Vulnerable: one year on disk
cookie.setMaxAge(60 * 60 * 24);         // Safe in the guides' example
```

- **Related**: CWE-539 · SR2-7

## 30. 주석문 안에 포함된 시스템 주요정보 (system information in comments)

Passwords or other system secrets are left in comments.

- **Find**: comments near DB connection and admin login code; comments containing `password`, `passwd`, `pwd`, `비밀번호`, `암호`, `root`, account IDs, hashes or keys
- **Vulnerable** `R`: a comment holds a real password, account, key or the value before and after encryption
- **Not vulnerable** `R`: the comment contains the word "password" or "비밀번호" but no actual secret
- **Fix** `G`: never write IDs, passwords or other security information in comments; delete any left during development

```java
// DB연결 root / a1q2w3r3f2!@     <- Vulnerable: delete the comment
```

- **Related**: CWE-615 · SR2-5

## 31. 솔트 없이 일방향 해쉬함수 사용 (one-way hash without a salt)

Passwords are hashed without a salt, so precomputed (rainbow) tables recover them.

- **Find**: `MessageDigest.getInstance(...)` followed by `digest(password...)` with no salt `update`; C# `ComputeHash` on the password alone; hashes compared in login code
- **Vulnerable** `R`: the hash is computed from the password alone, even with a strong hash such as SHA-512
- **Not vulnerable** `R`: a safe hash algorithm with a salt added before the digest is produced
- **Fix** `G`: hash the password together with a salt. SR2-3 adds that each password needs its own random salt, that 32 bytes or more makes guessing hard, and that the hash runs on the server
- **Fix** `D`: SHA-2 with a salt passes this weakness, but a single fast hash is easy to brute-force. Recommend a password hashing function (PBKDF2, bcrypt, Argon2), which salts and iterates for you; the development guide's own appendix on SSO names bcrypt and Argon2

```java
md.update(password.getBytes(UTF_8));                          // Vulnerable: no salt
return md.digest();

PasswordEncoder encoder = new BCryptPasswordEncoder();        // Recommended (D)
String stored = encoder.encode(password);                     // salt generated and embedded
```

- **Related**: CWE-759 · SR2-6 (SR2-3 requirement 3 also covers salted password hashes, though the mapping table lists only SR2-6)

## 32. 무결성 검사 없는 코드 다운로드 (download of code without integrity check)

Source code or executables are downloaded and run without checking their integrity, so a compromised host, DNS spoofing or tampering in transit runs the attacker's code.

- **Find**: `URLClassLoader`, `Class.forName(..., loader)`, `defineClass`, downloaded scripts or binaries that are executed, plugin and update mechanisms
- **Vulnerable** `R`: code is loaded without comparing a checksum or verifying a signature first
- The guides give no true-positive or false-positive code; the diagnosis method above is the rule
- **Fix** `G`: verify a checksum or signature before loading, transfer code over a protected channel, and run it with the least privilege
- **Fix** `D`: the guides' Java example "encrypts with the private key" instead of signing, and its C example only checks that the download call succeeded. Verify a signature with a pinned public key, or compare a hash obtained over a separate trusted channel

```java
byte[] jar = Files.readAllBytes(downloaded);
Signature sig = Signature.getInstance("SHA256withRSA");
sig.initVerify(publisherKey);
sig.update(jar);
if (!sig.verify(signatureBytes)) throw new SecurityException("tampered");
// load only after verification
```

- **Related**: CWE-494 · SR1-10

## 33. 반복된 인증시도 제한 기능 부재 (no limit on repeated authentication attempts)

Unlimited login attempts allow dictionary and brute-force attacks.

- **Find**: login handlers, OTP and verification-code checks, password-reset answers, authentication loops
- **Vulnerable** `R`: the authentication function can be called repeatedly with no code that counts and limits attempts
- The guides give no false-positive example
- **Fix** `G`: limit attempts to an appropriate number and, beyond it, lock the account or require additional authentication. The implementation examples use 5 attempts; SR2-2 says 3 to 5, and its example deliverables say 5
- **Fix** `G` (SR2-2): store the failure count, lock status and last success and failure times per account in the DB, and log failed attempts (ID, time, IP). The guides' Java example counts inside a local loop, which resets on every request; count on the server across requests

```java
if (account.getFailCount() >= MAX_ATTEMPTS) throw new LockedException("locked");
if (!encoder.matches(pw, account.getPasswordHash())) {
    accountRepository.increaseFailCount(account.getId());   // persisted, not a local counter
    throw new BadCredentialsException("invalid");
}
accountRepository.resetFailCount(account.getId());
```

- **Related**: CWE-307 · SR2-2
