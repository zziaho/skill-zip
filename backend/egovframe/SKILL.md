---
name: egovframe
description: Korean eGovFrame (전자정부 표준프레임워크) reference for writing and reviewing code that follows its standard structure. Covers version detection (4.x vs 5.x), layer architecture and naming conventions, runtime base classes (EgovAbstractServiceImpl, EgovAbstractMapper, @EgovMapper), the 44-rule PMD code inspection ruleset, the official SQL writing rules, and exception handling, logging, ID generation and property services. Use this skill whenever working in a Java project that depends on org.egovframe.rte (or egovframework.*) packages, when the user mentions eGovFrame, 전자정부 표준프레임워크, 표준프레임워크 or a Korean public-sector (공공 SI) Spring project, when adding a Controller/Service/ServiceImpl/Mapper/VO or MyBatis SQL mapper XML, when reviewing such code or SQL for conformance, or when the user asks which eGovFrame version their project uses.
---

# eGovFrame (전자정부 표준프레임워크)

Reference for building and reviewing code on eGovFrame, the Spring-based development framework published by the Ministry of the Interior and Safety and NIA for Korean public-sector systems. Verified against runtime `v4.3.0-Final` and `v5.0.2-Final` (released 2026-09-22) and the official guide docs (`eGovFramework/egovframe-docs`, commit `94ce018`, 2026-10-22).

## How to use

1. **Detect the version first** (see below). Never assume one
2. Read the version file that matches: `references/v4/runtime.md` or `references/v5/runtime.md`
3. Look up the task in the Quick Lookup table and read **only** those common files
4. When **building**: follow the rules, then the version file for exact class names and imports
5. When **reviewing**: use the **Check** column, and report findings by strength (see Conventions)

## Version detection

Run this before any other step, and whenever the user asks which version the project uses. Answer with the evidence (file and line), not a guess.

| Evidence | 4.x | 5.x |
|----------|-----|-----|
| Runtime artifact IDs (`pom.xml`, `build.gradle`) | Dotted: `org.egovframe.rte.ptl.mvc`, `org.egovframe.rte.psl.dataaccess` | Hyphenated: `egovframe-rte-ptl-mvc`, `egovframe-rte-psl-dataaccess` |
| Version declaration | Property `<org.egovframe.rte.version>4.x.x</org.egovframe.rte.version>` | Parent `org.egovframe.boot:egovframe-boot-starter-parent` or `org.egovframe.web:egovframe-web-config-parent` with version `5.x.x`, or the same property |
| Java / Spring | Java 1.8, Spring 5.3.x | Java 17, Spring 6.2.x |
| Imports in source | `javax.annotation.Resource`, `javax.servlet.*` | `jakarta.annotation.Resource`, `jakarta.servlet.*` |
| Mapper annotation | `org.egovframe.rte.psl.dataaccess.mapper.Mapper` | `org.egovframe.rte.psl.dataaccess.mapper.EgovMapper` |

- Read the exact version from the property or parent version. Artifact naming and imports only confirm the major version.
- If the user states a version, still check the build file. Report any mismatch instead of silently following either one.
- Packages under `egovframework.rte.*` (instead of `org.egovframe.rte.*`) indicate 3.x or earlier. **This skill does not cover 3.x** (unverified: the package rename happened in 4.0). Say so and apply only the common files.
- `references/v4/runtime.md` is verified against 4.3.0 only. For 4.0 to 4.2, treat class availability as unverified and confirm it in the project's dependencies.

## Conventions

Every rule in the reference files carries a strength:

| Strength | Meaning | How to report in a review |
|----------|---------|---------------------------|
| `R` | Rule: the official guide states it as a requirement ("허용하지 않음", "사용하지 않음"), it is in the standard PMD ruleset, or the runtime fails without it | Violation |
| `G` | Guide: the official guide shows it as the way to use the framework, but does not mandate it | Recommendation |
| `C` | Convention: produced by the official code generator or used in the official samples only | Recommendation, and only if the project does not already follow a different consistent convention |

- **There is no official conformance checklist.** No eGovFrame document defines what "applying the framework" requires. Never describe a `G` or `C` item as mandatory.
- A project's own development standard (개발 표준 정의서), if present, overrides `G` and `C` items. Ask for it when reviewing a public-sector project.
- Cite official numbering in reports (e.g., "SQL rule 10", "performance principle 14", "PMD rule 34 SystemPrintln").

## Quick Lookup

| Task | File to Load |
|------|-------------|
| Which version is this project? Class names, imports, required bean names | `references/v4/runtime.md` or `references/v5/runtime.md` |
| Add a feature: Controller, Service, ServiceImpl, Mapper, VO, SQL file | `references/architecture.md` + version file |
| Package layout, file locations, URL and SQL ID naming | `references/architecture.md` |
| Transactions, component scanning, AOP pointcuts | `references/architecture.md` |
| Write or review SQL, MyBatis mapper XML | `references/sql-rules.md` |
| Java code quality review, PMD findings, security weaknesses | `references/code-inspection.md` |
| Exceptions, `processException`, logging | `references/foundation.md` |
| ID generation, property service, message source | `references/foundation.md` + version file |
| Migrating 4.x code to 5.x | `references/v5/runtime.md` (section "Changes from 4.x") |

## When building

1. Detect the version and read its runtime file
2. Read `references/architecture.md` and follow the layer chain and naming of the existing project first; fall back to the `C` conventions only when the project has none
3. For any SQL, read `references/sql-rules.md` and detect the DBMS before writing
4. Write Java code that passes the PMD ruleset in `references/code-inspection.md`

## When reviewing

1. Detect the version and the DBMS
2. Check the code against each relevant file, using the **Check** column
3. Group findings: `R` violations first, then `G` and `C` recommendations
4. For each finding give the file and line, the rule number and strength, and a concrete fix that uses the class names from the version file
