# Design-Phase Security Criteria (설계단계 보안설계 기준)

The 20 design-phase criteria, defined in 별표3 of the notice and explained in chapter 3 of the development guide and PART3 of the diagnostic guide. They are checked against analysis and design deliverables, before implementation starts.

Strengths in this file: the numbered requirements under each criterion are `R`; the **Check** and **Test plan** items are `G` (what the guides show as evidence of the design); items marked `D` are this skill's judgment.

## How the design diagnosis works

- **When**: when design is complete and implementation is starting or being prepared.
- **What is reviewed**: analysis and design deliverables such as the requirements definition (요구사항정의서), architecture design (아키텍처설계서), program, class, component and use-case specifications, DB design (DB설계서), initial data design, requirements traceability matrix (요구사항추적표), unit test cases, and the project's development guide (개발가이드, 표준코딩정의서).
- **Two questions per requirement**: for every numbered requirement below, the diagnostic guide asks (1) is a security design for it present in the deliverables, and (2) is there a test plan to check it. Report a missing test plan as a gap as well (`D`: the guides ask both questions but do not say how to grade a missing test plan).
- **Identification first**: in the analysis phase the project classifies sensitive information and critical functions. Criteria SR2-1, SR2-4, SR2-7 and SR2-8 depend on that classification; ask for it first.
- **Evidence**: each finding needs an objective basis (this guide or a law), a practical improvement, and the deliverable that shows the gap.
- **Naming**: chapter 3 numbers the criteria 1.1 to 4.1; the appendix and the example deliverables use SR1-1 to SR4-1. They are the same (1.n = SR1-n). Use the SR form in reports.

A design plan (설계항목 적용계획서) lists, per criterion: type, requirement number, criterion name, countermeasure, how it is applied, and a remark (often "defined in the coding standard"). Apply criteria through a framework or common library where possible, and review that library's own security.

## The 20 criteria

| ID | Criterion | Implementation weaknesses it covers |
|----|-----------|-------------------------------------|
| SR1-1 | DBMS 조회 및 결과 검증 | 1 |
| SR1-2 | XML 조회 및 결과 검증 | 8, 9 |
| SR1-3 | 디렉토리 서비스 조회 및 결과 검증 | 10 |
| SR1-4 | 시스템 자원 접근 및 명령어 수행 입력값 검증 | 2, 3, 5, 12 |
| SR1-5 | 웹 서비스 요청 및 결과 검증 | 4 |
| SR1-6 | 웹 기반 중요 기능 수행 요청 유효성 검증 | 11 |
| SR1-7 | HTTP 프로토콜 유효성 검증 | 7, 13 |
| SR1-8 | 허용된 범위내 메모리 접근 | 16, 17 |
| SR1-9 | 보안기능 입력값 검증 | 14, 15, 39 |
| SR1-10 | 업로드·다운로드 파일 검증 | 6, 27, 32 |
| SR2-1 | 인증 대상 및 방식 | 12, 18, 28, 48 |
| SR2-2 | 인증 수행 제한 | 33 |
| SR2-3 | 비밀번호 관리 | 23, 26 |
| SR2-4 | 중요자원 접근통제 | 19, 20 |
| SR2-5 | 암호키 관리 | 23, 30 |
| SR2-6 | 암호연산 | 21, 24, 25, 28, 31 |
| SR2-7 | 중요정보 저장 | 22, 29 |
| SR2-8 | 중요정보 전송 | 22 |
| SR3-1 | 예외처리 | 36 |
| SR4-1 | 세션통제 | 44 |

Types: SR1 입력데이터 검증 및 표현 (10), SR2 보안기능 (8), SR3 에러처리 (1), SR4 세션통제 (1). Twelve implementation weaknesses map to no criterion (34, 35, 37, 38, 40 to 43, 45 to 47, 49); the guides say some weaknesses can be removed by following coding rules alone.

## SR1: Input data validation and representation

### SR1-1 DBMS 조회 및 결과 검증

1. The application connects to the DB with a least-privilege account
2. SQL is not built dynamically from external input
3. Where dynamic SQL is unavoidable, input is validated first

- **Check**: one DB account per application with only the read, write, update and delete rights it needs (initial data design; on an existing dev server, the actual grants); an ORM or static-query environment in the architecture design; coding rules in the development guide (`#{}` in MyBatis/iBatis, `PreparedStatement`); for dynamic queries, a filter applied to every DB access, or a coding rule if applied per call
- **Test plan**: special characters (`' " = & | ! ( ) { } $ % @`), keywords (`UNION`, `SELECT`, `IF`, `END`), functions (`DATABASE()`, `CONCAT()`, `COUNT()`); requests outside the account's rights

### SR1-2 XML 조회 및 결과 검증

1. Parameters of XML queries (XPath, XQuery) are filtered or bound by type to a prepared query

- **Check**: a filter or safe library in the program, component or class design; a coding rule. The guides list `" [ ] / = @` as characters to filter
- **Gap**: chapter 3 has no design countermeasure for XXE (weakness 8) beyond an incident example. Add a rule that XML parsers disable DTDs and external entities (`D`)

### SR1-3 디렉토리 서비스 조회 및 결과 검증

1. When LDAP is used for authentication, input used in the request is filtered against LDAP injection

- **Check**: a filter for search-filter input (`= + < > # ; \`) or a safe library; a coding rule

### SR1-4 시스템 자원 접근 및 명령어 수행 입력값 검증

1. When input identifies a system resource (IP, port, process, memory, file), unauthorized resources cannot be used
2. When the server must run shell commands, input cannot make it run malicious commands

- **Check**: resources allowed for each function are listed (in properties or XML, so changes need little code change); where listing is impossible, a rule removes `..`, `/`, `\` and limits access to a fixed path; resource access is logged (time, user ID, IP, input, including denied access). Shell execution is avoided; if needed, commands and arguments come from an allowlist and input is only an index into it; executed commands are logged
- **Test plan**: path characters `.. / \`; command separators `| & ;`

### SR1-5 웹 서비스 요청 및 결과 검증

1. Input used in a dynamic response page passes an XSS filter
2. DB results used in a dynamic response page are HTML-encoded or XSS-filtered

- **Check**: a filter, interceptor or common validator for input; HTML encoding in the view layer for output, also for DB values; allowlist-based filter rules; if a servlet filter is used, its URL mapping covers every target. Libraries named: LUCY XSS Filter, OWASP ESAPI (Java)
- **Test plan**: filter-bypass inputs such as `<IMG SRC="javascript:alert('XSS');">`

### SR1-6 웹 기반 중요 기능 수행 요청 유효성 검증

1. Every request can be judged to be a valid request of the real user

- **Check**: CSRF tokens (per session, sent in a hidden field, compared on processing; checked automatically by an interceptor in Spring or Struts) or CAPTCHA on every data-changing request; re-authentication for critical functions. Spring Security provides CSRF protection from 3.2
- **Test plan**: automated script requests are blocked

### SR1-7 HTTP 프로토콜 유효성 검증

1. Input used in cookies or headers is filtered against response splitting
2. Input used as a redirect or forward URL only selects from an allowed list

- **Check**: functions that set headers (`setHeader`, `addCookie`, `sendRedirect`) are identified and CR/LF are removed; allowed domains and addresses are defined (in code or XML/properties) with a validating module
- **Test plan**: values with CR/LF; arbitrary URLs

### SR1-8 허용된 범위내 메모리 접근

1. Where the program manages memory (C, C++), reads and writes beyond buffer bounds are prevented
2. Vulnerable APIs that can overflow buffers are banned

- **Check**: non-executable stack, ASLR and StackGuard on the platform; a rule to check lengths when copying arrays; a list of banned functions and their replacements in the development guide (see weakness 49)
- **Test plan**: sufficiently long strings

### SR1-9 보안기능 입력값 검증

1. Information that decides roles and permissions is managed on the server (chapter 3 adds: identity information from the client is verified before use)
2. External input (cookies, environment variables, parameters) used as arguments of security functions is validated and used in a limited way
3. Important state or authentication and authorization data is not sent in cookies; if unavoidable, it is encrypted

- **Check**: roles (user, admin, super admin) and their permissions defined and stored in DB or session; permission checks use server data; for each input used in security functions, its kind, source, reason and validation (null checks, range checks for integer overflow); a list of cookies (name, value, meaning, lifetime) and the reason for any sensitive cookie, with encryption, integrity checks (HMAC) and secure-channel-only attributes. With external authentication services, verify the result through the back channel
- **Test plan**: tampered parameters and cookies try to bypass permission checks

### SR1-10 업로드·다운로드 파일 검증

1. Uploaded files are limited in type, size, number and execute permission
2. Stored uploads cannot be identified from outside
3. Requested download file names are validated
4. Downloaded source code or executables are checked for integrity

- **Check**: size limits in the framework (the guide's example: Spring `CommonsMultipartResolver` `maxUploadSize` 20 MB, `maxInMemorySize` 1 MB); type checks by MIME type and extension in a common module applied to every upload, with the same policy on client and server; upload paths that cannot run files; storage outside URL-reachable directories with downloads through a controller; random stored names mapped to original names in a DB table; download names cleaned of `.. / \`, checked against the DB and the user's permission, and scanned for malware; checksums or hashes provided and verified for downloaded code
- **Test plan**: disallowed types, sizes and counts; executing a stored file; `../` and `..\` in names; requesting other files by changing parameters; tampered files

## SR2: Security features

### SR2-1 인증 대상 및 방식

1. Critical functions and resources are used only after authentication
2. A safe authentication method prevents bypass and privilege escalation
3. Two-factor authentication is considered for critical functions

- **Check**: critical functions and resources classified in the requirements; authentication applied centrally (a framework component or a function-to-authentication mapping) so none is missed; authentication data stored and checked on the server, encrypted; attempt limits and error handling; failed authentication logged (time, IP, ID); additional authentication for personal data changes, password reset, permission management and admin functions, with its use and failures logged
- **OTP**: time-, event- or challenge-based; time-limited (30 to 60 seconds in finance); 6 or more digits or characters
- **Two factors**: two of knowledge (password, PIN), possession (token, smart card) and inherence (fingerprint, iris); or multi-device (SMS, ARS), certificates or biometric signatures
- **Test plan**: access to critical functions without authentication

### SR2-2 인증 수행 제한

1. Login attempts are limited and a restriction applies beyond the limit
2. Failed attempts are logged so they can be traced

- **Check**: the limit (chapter 3 and the diagnostic guide say 3 to 5 attempts; the example deliverables in both guides say 5, and the diagnostic guide's example adds a 24-hour lock beyond 5 failures); failure counts stored persistently (DB or file) per user ID and session; account lock or additional information beyond the limit; CAPTCHA; the user table holds failure count, lock status, last success and failure and logout times; logs hold user ID, failure count, time, IP and account status
- **Test plan**: repeated failures trigger the restriction and are recorded persistently

### SR2-3 비밀번호 관리

1. Password rules follow KISA 『패스워드 선택 및 이용 안내서』 (the appendix cites 『암호이용안내서』 instead)
2. Passwords sent over the network are encrypted or sent over an encrypted channel
3. Passwords are stored with a salted safe hash, computed on the server
4. Password change and reset follow safe rules
5. Password management rules are defined and applied

- **Rules**: at least two character classes and 8 or more characters, or 10 or more characters; no repeated or keyboard patterns, personal information, user ID, dictionary words, famous names, look-alike substitutions, default passwords
- **Transmission**: TLS or VPN on public networks, only the latest TLS versions (for example TLS 1.2 and 1.3) with algorithm suites from KISA 『암호 알고리즘 및 키 길이 이용 안내서』
- **Storage**: one-way hash with a unique salt per password, 32 bytes or more; the diagnostic guide lists SHA-224/256/384/512. Chapter 3 stores the salt with the digest in the DB; the diagnostic guide says to store it where the encryption keys are stored. `D`: treat either as acceptable and follow the project's key management design
- **Change and reset**: confirm the current password when changing; reset only after identity verification (mobile phone, i-PIN, certificate, card) and through the e-mail registered at sign-up; limit failed question-and-answer attempts; issue a temporary password and force a change at first login; never reuse previous passwords
- **Management**: change every 3 (or 6) months with expiry tracked in the user table; store and show the last successful login
- **Test plan**: rule enforcement; packet sniffing; cracking tools on stored values; bypassing identity verification or reaching the reset page directly

### SR2-4 중요자원 접근통제

1. Access control policies for critical resources
2. Access control policies for critical functions
3. Access control policies for admin pages

- **Check**: access control at three levels (the diagnostic guide's design example): screen (no buttons or links for functions the user may not use), function (the server checks the permission for each request, even a URL typed directly) and data (the server checks the permission on the specific record); common modules applied through a filter or interceptor; admin functions separated physically or logically; critical resources (files, processes, memory, DB, information) and subjects identified; least privilege and separation of privileges; RBAC for roles and ACLs for resources (Spring Security, including its ACL module, which checks permission on domain objects before and after method calls); if applied by a framework, it covers every request; critical functions separated into anonymous, user, privileged and admin areas, with parameter tampering checks and privilege raised as late as possible and dropped right after; admin pages on a hard-to-guess URL and a separate port, blocked from external networks, limited to defined IPs, over encrypted channels, with extra authentication and access logs
- **Test plan**: operations beyond assigned rights; admin access from outside; sniffing admin traffic

### SR2-5 암호키 관리

1. Keys for DB encryption are managed as KISA 『암호이용안내서』 defines (chapter 3 cites 『암호 키 관리 안내서』, 2014, instead)
2. Keys that encrypt sensitive values in configuration files (XML, properties) are themselves encrypted and stored in a separate directory

- **Check**: DB keys stored physically apart from the DB; explicit generation, distribution, use and destruction policies; passwords and keys not kept in memory, or zeroed after use; backups on generation and change; FIPS 140-2 level chosen for the organization; key recovery procedure; validity periods per key type (the guide's NIST figures: symmetric keys up to 2 years for the sender, public encryption keys and private decryption keys up to 2 years, signing keys 1 to 3 years); configuration secrets encrypted with a master key kept elsewhere
- **Test plan**: whether configuration secrets are encrypted and where the key is kept

### SR2-6 암호연산

1. Symmetric and asymmetric encryption use algorithms and key lengths from KISA 『암호이용 안내서』
2. One-way encryption uses a safe hash with a salt
3. Random numbers come from a safe generator

- **Check**: symmetric SEED, ARIA, AES; asymmetric RSA, KCDSA, ECC; keys of 128 bits (symmetric) and 2048 bits (asymmetric) or more (diagnostic guide). Chapter 3's NIST table asks for 112-bit security until 2030 and 128 bits after (RSA 3072, ECC 256), and its recommended lists include SHA-3 and LSH as well as SHA-2; hashes chosen by purpose (MAC, key derivation, random generation, signing); random numbers from a FIPS 140-2 validated module with seeds of 256 bits or more
- **`D`**: the diagnostic guide's coding rule example names `java.util.Random` as a safe API. Treat only `java.security.SecureRandom` as safe (see weakness 25)
- **Test plan**: attempts to decrypt or crack encrypted data

### SR2-7 중요정보 저장

1. Sensitive or personal information is stored encrypted
2. Unneeded sensitive information does not remain in memory

- **What to encrypt** (the diagnostic guide's list): under 개인정보보호법, unique identifiers (resident registration, driver's licence, passport and alien registration numbers), biometric data and passwords; under 정보통신망법, resident registration, credit card and account numbers; under 위치정보법, location data; system secrets such as DB and integration accounts and key settings
- **Check**: a safe area for sensitive data that it does not leave; encryption with SR2-6 algorithms and keys; no sensitive data in cookies or HTML5 local storage (encrypt if unavoidable); important logic and comments only in server-side code; memory zeroed after use in personal and financial data functions; caching disabled for sensitive pages; `autocomplete="off"` on credential forms
- The example deliverables also file "no comments that expose sensitive information" and "do not expose stored file names and paths" under SR2-7

### SR2-8 중요정보 전송

1. Sensitive information such as credentials is encrypted in transit
2. Sensitive information in cookies is encrypted in transit

- **Check**: the data to protect (same list as SR2-7); TLS or VPN between endpoints, or encryption with safe algorithms where no secure channel exists; no unnecessary data in hidden fields, Ajax variables, cookies and headers; sensitive cookies avoided, or made session cookies and encrypted. (The diagnostic guide writes "TLSv2"; `D`: read it as TLS 1.2 or later, as SR2-3 does)
- **Test plan**: packet sniffing

## SR3: Error handling

### SR3-1 예외처리

1. Explicit exceptions are handled in exception blocks
2. Runtime exceptions are prevented by checking input ranges
3. Detailed error information is not shown to users

- **Check**: handling per exception type in the development guide (never expose system information, always handle exceptions, separate handling per case); exception logging policy (time, reason, sensitive data in logs encrypted); range checks for inputs that can raise exceptions; a default error page set in the server (`web.xml` `error-page` for `java.lang.Throwable`, 404, 500) or a redirect rule; an error code book whose messages contain no sensitive information
- Weaknesses 37 and 38 are not mapped to this criterion (`D`: requirements 1 and 2 cover them in substance; review them together)

## SR4: Session control

### SR4-1 세션통제

1. Data is not shared between sessions
2. Sessions are managed safely
3. Session IDs are managed safely

- **Check**
  - No readable and writable member or class variables in classes that run as threads (servlets, controllers, singleton services, JSP declarations)
  - Logout available on every page and removing the session completely (`session.invalidate()`); sessions removed when the user disconnects
  - Timeouts: 2 to 5 minutes for critical functions, 15 to 30 minutes for low-risk applications; idle sessions removed by the server
  - If duplicate login is not allowed, the earlier session ends or the new one is refused
  - Session ID created by the server, at least 128 bits, from a safe random generator; sent only in cookies with `HttpOnly`, never by URL rewriting
  - A new session ID after login (against session fixation), periodically for long connections, and after a password change (with re-authentication)
- Chapter 3 says "change the session ID at (re)login"; the appendix and the diagnostic guide say "do not reuse the previous session ID". Both mean the same check
- **Test plan**: changing shared data from several sessions; reading the session ID from JavaScript; session ID renewal after login and over time

## Example deliverables

The development guide's appendix applies the criteria to screens of the eGovFrame common components. Use it as a checklist of which criteria a screen of each kind needs:

| Screen | Criteria applied |
|--------|------------------|
| Data input (sign-up) | SR1-1, SR1-5, SR1-6, SR1-10, SR2-3, SR2-7, SR2-8, SR3-1, SR4-1 |
| Data lookup (find ID or password) | SR1-1, SR1-5, SR2-3, SR2-4, SR2-7, SR2-8, SR3-1, SR4-1 |
| Data modify and delete (posts) | SR1-1, SR1-5, SR1-6, SR1-9, SR2-1, SR2-4, SR2-7, SR3-1, SR4-1 |
| File upload (post with attachments) | SR1-1, SR1-5, SR1-6, SR1-9, SR1-10, SR2-1, SR2-4, SR2-7, SR3-1, SR4-1 |
| File download | SR1-1, SR1-4, SR1-5, SR1-10, SR2-1, SR2-4, SR2-7, SR3-1, SR4-1 |
| Web editor | SR1-1, SR1-5, SR1-6, SR1-9, SR1-10, SR2-1, SR2-4, SR2-7, SR3-1, SR4-1 |
| Admin page | SR1-1, SR1-5, SR2-1, SR2-4, SR2-7, SR3-1, SR4-1 |

SR1-1, SR1-5, SR2-7, SR3-1 and SR4-1 appear on every screen. The chapter 3 login use case adds SR2-2 (attempt limits) and SR2-8 (encrypted channel).
