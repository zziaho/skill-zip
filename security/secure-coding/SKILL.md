---
name: secure-coding
description: Korean public-sector secure coding (소프트웨어 개발보안, 시큐어코딩) reference based on the Ministry of the Interior and Safety guides. Covers the 49 implementation-phase security weaknesses (구현단계 보안약점 제거 기준) with the diagnostic guide's true-positive and false-positive criteria, safe code in Java (Spring, JSP, MyBatis, iBatis, Hibernate) and C, and the 20 design-phase security criteria (설계단계 보안설계 기준, SR1-1 to SR4-1). Use this skill when writing or reviewing code for a Korean public-sector or government project (공공 SI, 정보화사업, 감리 대상), when the user mentions 시큐어코딩, 개발보안, 보안약점, 보안약점 진단, 행정안전부 개발보안 가이드, 49개 항목, or SR1-1 style IDs, when preparing for or responding to a security weakness diagnosis (진단원, 감리, 정탐/오탐), when reviewing design documents (요구사항정의서, 아키텍처설계서) for security criteria, or when the user asks which security weakness a piece of code falls under.
---

# Secure Coding (소프트웨어 개발보안)

Reference for building and reviewing software under the Korean government's software development security regime. It is based on two guides published by the Ministry of the Interior and Safety (행정안전부) and KISA:

| Guide | Edition | Used for |
|-------|---------|----------|
| 소프트웨어 개발보안 가이드 (전자정부 SW 개발·운영자를 위한 소프트웨어 개발보안 가이드) | Revision 5, 2021.11. (file dated 2021-12-29) | Definitions, countermeasures, code examples, design criteria |
| 소프트웨어 보안약점 진단가이드 | Revision 4, 2021.11. | Diagnosis method, true-positive (정탐) and false-positive (오탐) code |

Both guides cite 「행정기관 및 공공기관 정보시스템 구축·운영 지침」 as 행정안전부고시 제2021-3호. The current version is **행정안전부고시 제2025-1호** (partially revised and effective 2025-01-02; confirmed on law.go.kr on 2026-11-06). Its articles on software development security still match the guides: 제50조 (principle, mandatory projects, scope), 제52조 (diagnosis criteria), 제53조 (diagnosis in audits, diagnosis tools), 제54조 and 별표 4 (diagnosers). 별표 3 (소프트웨어 보안약점 기준) lists the same 20 design criteria and 49 weaknesses that this skill covers. Cite the current notice number to clients, and check law.go.kr for later revisions.

Source attribution required by both guides: 행정안전부·한국인터넷진흥원의 『전자정부 SW 개발·운영자를 위한 소프트웨어 개발보안 가이드』 and 행정안전부·한국인터넷진흥원의 『소프트웨어 보안약점 진단가이드』. This skill summarizes and restructures them; it does not reproduce them.

## How to use

1. Decide whether the task is **design** (requirements, architecture and screen design documents) or **implementation** (source code)
2. Look up the task in the Quick Lookup table and read **only** the files it names
3. When **building**: follow the safe pattern of every item that applies to the code you write
4. When **reviewing**: find candidates with the **Find** line of each item, then judge each one with the **Vulnerable** and **Not vulnerable** lines. Report only the candidates that are vulnerable

## Scope of the regime

| Item | Rule in the guides |
|------|--------------------|
| Mandatory for | Projects under 「전자정부법 시행령」 제71조제1항, which the guides describe as information system projects subject to audit (정보시스템 감리대상 사업). Other projects may apply it (지침 제50조) |
| New development | All design-phase deliverables and all source code |
| Maintenance | The design deliverables and source code changed by the maintenance, in full (the guides do not say whether this means changed files or changed lines) |
| Excluded | Commercial off-the-shelf software (상용 소프트웨어) |
| Criteria | 20 design-phase security criteria and 49 implementation-phase weakness removal criteria |
| Diagnosis | Audit firms diagnose whether the weaknesses in 별표 3 were removed, and may assign certified diagnosers (진단원) first (지침 제53조). A diagnosis tool, if used, must be certified by the National Security Research Institute, confirmed by KISA, or hold an NIS security function confirmation (보안기능 확인서), and must cover 별표 3. The diagnostic guide adds manual diagnosis to reduce misses (미탐). The first report lists file, line, weakness name, cause and fix; a second diagnosis confirms removal |

Neither the notice nor the guides give a project size or an agency list for the mandate; they refer to 「전자정부법 시행령」 제71조제1항. Do not state a threshold.

## Conventions

Every rule in the reference files carries a strength:

| Strength | Meaning | How to report in a review |
|----------|---------|---------------------------|
| `R` | The weakness or design criterion itself, and the guides' judgment of what is vulnerable | Finding (weakness to remove) |
| `G` | A countermeasure method the guides show (a library, a code pattern, a configuration) | Recommendation; another fix that removes the weakness is equally acceptable |
| `D` | This skill's judgment where the guides are silent, inconsistent, outdated or wrong. The reason is given next to it | Recommendation, and say that it goes beyond the guides |

- **Name findings with the official number and Korean name**, for example "보안약점 1 SQL 삽입" or "설계 기준 SR1-1 DBMS 조회 및 결과 검증". Diagnosers and auditors use these names.
- The guides' own true-positive and false-positive examples are the strongest evidence in a dispute with a diagnoser. Cite them as "진단가이드 정탐 예" or "진단가이드 오탐 예".
- Code in the guides contains many typos (for example `||` where `&&` is meant, `stmcpy` for `strncpy`). The examples in this skill are corrected. Never copy guide code without reading it.
- The guides' examples are Java (including Spring, JSP, MyBatis, iBatis, Hibernate), C and C#. This skill keeps Java and C. For other languages, apply the definition and the judgment rules, not the code.

## Quick Lookup

| Task | File to Load |
|------|-------------|
| SQL, OS command, code, LDAP, XML/XPath, XXE injection; XSS; path traversal; file upload; open redirect; CSRF; SSRF; HTTP response splitting; integer overflow; trusting client input for security decisions; buffer overflow; format string (weaknesses 1 to 17) | `references/input-validation.md` |
| Authentication, authorization, file permissions, cryptography, keys, random numbers, passwords, signatures, certificates, cookies, comments, hashing, code download, login attempt limits (weaknesses 18 to 33) | `references/security-features.md` |
| Race conditions, recursion, error messages, empty or broad catch blocks, null dereference, resource release, use after free, uninitialized variables, deserialization (weaknesses 34 to 43) | `references/time-error-code.md` |
| Shared state in singletons and servlets, debug code, returning or storing private arrays, DNS-based trust, dangerous APIs (weaknesses 44 to 49) | `references/encapsulation-api.md` |
| Review requirements, architecture or screen design documents; write a design-phase security plan (SR1-1 to SR4-1) | `references/design-phase.md` |
| Which weakness does this code fall under? | Search the **Find** lines of the four implementation files for the API or pattern |

The 49 weaknesses:

| Type | Numbers |
|------|---------|
| 입력데이터 검증 및 표현 (input data validation and representation) | 1 to 17 |
| 보안기능 (security features) | 18 to 33 |
| 시간 및 상태 (time and state) | 34, 35 |
| 에러처리 (error handling) | 36 to 38 |
| 코드오류 (code errors) | 39 to 43 |
| 캡슐화 (encapsulation) | 44 to 47 |
| API 오용 (API misuse) | 48, 49 |

## When building

1. Identify the external inputs (request parameters, headers, cookies, files, environment variables, properties edited outside the code, socket data, DB values that users wrote) and where each one is used
2. Read the reference file for each place an input reaches (query, command, path, response, redirect, security decision) and follow its safe pattern
3. For authentication, sessions, cryptography and sensitive data, read `references/security-features.md` before writing the code, and use the framework's security features (for example Spring Security) instead of hand-written checks
4. For C code, also read the items with C examples: weaknesses 3, 5, 14, 16 and 17 (`references/input-validation.md`), 20 and 28 (`references/security-features.md`), 34, 35 and 39 to 42 (`references/time-error-code.md`), and 49 (`references/encapsulation-api.md`)

## When reviewing

1. List candidates: run `scripts/find_candidates.py` (see below), then search the **Find** lines for what the script does not cover. A diagnosis tool report, if the user has one, is also a candidate list
2. Judge each candidate against **Vulnerable** and **Not vulnerable**, following the data flow from the external input to the use. Report only true positives
3. For a tool finding that matches a **Not vulnerable** case, say that it is a false positive and cite the case
4. For each finding give the file and line, the weakness number and Korean name, the strength, the cause, and a fix. Group `R` findings first, then `G` and `D` recommendations

## Candidate search script

`scripts/find_candidates.py` (in this skill's folder) lists candidate lines for the weaknesses that a pattern can find. It is read-only and needs only Python 3. It scans Java, JSP, MyBatis and iBatis mapper XML, Spring Security XML, C and C++, and `.properties`/`.yml` files, and skips build output and test folders.

```bash
python <skill-folder>/scripts/find_candidates.py src/main --summary   # counts per weakness
python <skill-folder>/scripts/find_candidates.py src/main --only 1,23,36
```

- Output lines are `path:line: [보안약점 N 이름] message`; the exit code is 1 when candidates exist. `--include-tests` also scans test folders.
- Every line is a **candidate**. Judge it with the item's **Vulnerable** and **Not vulnerable** lines before reporting it; many candidates are false positives by design (for example `<%= %>` printing a number).
- Searched: weaknesses 1 to 15, 17, 19 to 25, 27 to 32, 34, 36 to 39 and 43 to 49. Weakness 16 is covered through the banned functions of 49. Weakness 39 is searched only for a null check placed after the dereference.
- Not searched, because they need data flow or business context: 18, 26, 33, 35, 40, 41 and 42, and most cases of 39. Review them by reading the code; for Java, a PMD report (the `egovframe` skill's ruleset) covers 39 and 40.
- On a large project, run `--summary` first, then go through one weakness at a time with `--only`. JSP scriptlet output (weakness 4) usually produces the most candidates.

## Out of scope

The 49 criteria and 20 design criteria do not cover the following. Say so instead of attaching a weakness number:

- Vulnerable dependencies and SBOM. The development guide mentions Log4j and SBOM only in an appendix of reference material (제5장 제6절 참고자료, "Top 10"), outside the criteria; the revision history does not record when it was added
- Cloud, container and infrastructure configuration
- Design of API authentication schemes (JWT, OAuth, OpenID Connect). Weaknesses 15, 18, 19, 25 and 28 still apply to how the code uses them (trusting unverified tokens, missing checks, weak random values, skipped certificate validation)
- Business logic flaws that no weakness definition covers

Object-level authorization (checking that the user may access the requested record, IDOR) is **in scope**. The diagnostic guide's design example for SR2-4 requires data-level access control: even a user allowed to delete must be checked for permission on the record being deleted. Report missing checks as weakness 19 부적절한 인가 (`D`: the guides do not attach a weakness number to data-level checks; 19 is defined as access control not checked, or checked incompletely, on every execution path).

## Related skill

If the `egovframe` skill is installed, its PMD rules and SQL rules overlap with several weaknesses. Items that have a matching rule list it under **Related**.
