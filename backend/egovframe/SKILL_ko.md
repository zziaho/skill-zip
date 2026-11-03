---
name: egovframe
description: 전자정부 표준프레임워크(eGovFrame)의 표준 구조에 맞게 코드를 작성하고 검토하기 위한 참조 스킬입니다. 버전 판별(4.x와 5.x), 레이어 구조와 이름 규칙, 실행환경 기반 클래스(EgovAbstractServiceImpl, EgovAbstractMapper, @EgovMapper), PMD 코드 점검 규칙 44개, 공식 SQL 작성 규칙, 예외 처리·로그·ID 생성·프로퍼티 서비스를 다룹니다. org.egovframe.rte(또는 egovframework.*) 패키지에 의존하는 Java 프로젝트에서 작업할 때, 사용자가 eGovFrame, 전자정부 표준프레임워크, 표준프레임워크, 공공 SI용 Spring 프로젝트를 언급할 때, Controller·Service·ServiceImpl·Mapper·VO나 MyBatis SQL 매퍼 XML을 추가할 때, 이런 코드나 SQL이 표준을 따르는지 검토할 때, 사용자가 자신의 프로젝트가 어떤 eGovFrame 버전인지 물을 때 항상 이 스킬을 사용합니다.
---

# 전자정부 표준프레임워크 (eGovFrame)

행정안전부와 NIA가 공공 부문 정보시스템을 위해 배포하는 Spring 기반 개발 프레임워크인 eGovFrame으로 코드를 작성하고 검토할 때 참조하는 자료입니다. 실행환경 `v4.3.0-Final`과 `v5.0.2-Final`(2026-09-22 배포), 공식 가이드 문서(`eGovFramework/egovframe-docs`, 커밋 `94ce018`, 2026-10-22)와 대조하여 검증했습니다.

## 사용 방법

1. **가장 먼저 버전을 판별합니다**(아래 참조). 버전을 추측하지 않습니다.
2. 판별한 버전에 맞는 파일을 읽습니다: `references/v4/runtime_ko.md` 또는 `references/v5/runtime_ko.md`
3. 조회표에서 작업에 해당하는 항목을 찾고, 그 공통 파일**만** 읽습니다.
4. **구현**할 때는 규칙을 따르고, 정확한 클래스 이름과 import는 버전 파일에서 가져옵니다.
5. **검토**할 때는 **검사 방법** 열을 사용하고, 발견한 사항을 강도별로 보고합니다(표기 규칙 참조).

## 버전 판별

다른 단계보다 먼저 실행하고, 사용자가 프로젝트의 버전을 물을 때에도 실행합니다. 추측하지 말고 근거(파일과 행 번호)와 함께 답합니다.

| 근거 | 4.x | 5.x |
|------|-----|-----|
| 실행환경 아티팩트 ID (`pom.xml`, `build.gradle`) | 점 표기: `org.egovframe.rte.ptl.mvc`, `org.egovframe.rte.psl.dataaccess` | 하이픈 표기: `egovframe-rte-ptl-mvc`, `egovframe-rte-psl-dataaccess` |
| 버전 선언 | `<org.egovframe.rte.version>4.x.x</org.egovframe.rte.version>` 프로퍼티 | 버전이 `5.x.x`인 부모 POM `org.egovframe.boot:egovframe-boot-starter-parent` 또는 `org.egovframe.web:egovframe-web-config-parent`, 혹은 같은 이름의 프로퍼티 |
| Java / Spring | Java 1.8, Spring 5.3.x | Java 17, Spring 6.2.x |
| 소스의 import | `javax.annotation.Resource`, `javax.servlet.*` | `jakarta.annotation.Resource`, `jakarta.servlet.*` |
| Mapper 어노테이션 | `org.egovframe.rte.psl.dataaccess.mapper.Mapper` | `org.egovframe.rte.psl.dataaccess.mapper.EgovMapper` |

- 정확한 버전은 프로퍼티나 부모 POM의 버전에서 읽습니다. 아티팩트 이름과 import로는 주 버전만 확인할 수 있습니다.
- 사용자가 버전을 알려 주더라도 빌드 파일을 확인합니다. 두 정보가 다르면 어느 한쪽을 조용히 따르지 말고, 차이를 사용자에게 알립니다.
- 패키지가 `org.egovframe.rte.*`가 아니라 `egovframework.rte.*`이면 3.x 이하 버전입니다. **이 스킬은 3.x를 다루지 않습니다**(미검증: 패키지 이름은 4.0에서 바뀐 것으로 알려져 있습니다). 이 사실을 사용자에게 알리고, 공통 파일만 적용합니다.
- `references/v4/runtime_ko.md`는 4.3.0으로만 검증했습니다. 4.0부터 4.2까지는 클래스가 존재하는지 검증하지 않았으므로, 프로젝트의 의존성에서 직접 확인합니다.

## 표기 규칙

참조 파일의 모든 규칙에는 강도가 표시되어 있습니다.

| 강도 | 의미 | 검토할 때 보고하는 방식 |
|------|------|--------------------------|
| `R` | 규칙: 공식 가이드가 요구사항으로 명시했거나("허용하지 않음", "사용하지 않음"), 표준 PMD 규칙에 들어 있거나, 지키지 않으면 실행환경이 동작하지 않습니다 | 위반 |
| `G` | 가이드: 공식 가이드가 프레임워크를 사용하는 방법으로 보여 주지만, 의무로 정하지는 않았습니다 | 권장 사항 |
| `C` | 관행: 공식 코드 생성기가 만들어 내거나 공식 샘플에서만 사용하는 방식입니다 | 권장 사항. 다만 프로젝트가 이미 다른 방식을 일관되게 따르고 있다면 보고하지 않습니다 |

- **공식 적용 점검 기준은 없습니다.** "프레임워크를 적용했다"고 말하기 위한 요건을 정의한 eGovFrame 문서는 없습니다. `G`나 `C` 항목을 의무 사항처럼 설명하지 않습니다.
- 프로젝트에 자체 개발 표준(개발 표준 정의서)이 있다면 그 표준이 `G`와 `C` 항목보다 우선합니다. 공공 부문 프로젝트를 검토할 때는 개발 표준 정의서가 있는지 사용자에게 묻습니다.
- 보고서에는 공식 번호를 적습니다(예: "SQL 규칙 10", "성능 원칙 14", "PMD 규칙 34 SystemPrintln").

## 조회표

| 작업 | 읽을 파일 |
|------|-----------|
| 이 프로젝트는 몇 버전인가? 클래스 이름, import, 필수 빈 이름 | `references/v4/runtime_ko.md` 또는 `references/v5/runtime_ko.md` |
| 기능 추가: Controller, Service, ServiceImpl, Mapper, VO, SQL 파일 | `references/architecture_ko.md` + 버전 파일 |
| 패키지 구성, 파일 위치, URL과 SQL ID 이름 | `references/architecture_ko.md` |
| 트랜잭션, 컴포넌트 스캔, AOP 포인트컷 | `references/architecture_ko.md` |
| SQL, MyBatis 매퍼 XML 작성과 검토 | `references/sql-rules_ko.md` |
| Java 코드 품질 검토, PMD 지적 사항, 보안 약점 | `references/code-inspection_ko.md` |
| 예외, `processException`, 로그 | `references/foundation_ko.md` |
| ID 생성, 프로퍼티 서비스, 메시지 소스 | `references/foundation_ko.md` + 버전 파일 |
| 4.x 코드를 5.x로 전환 | `references/v5/runtime_ko.md`("4.x에서 바뀐 점" 절) |

## 구현할 때

1. 버전을 판별하고 해당 버전의 runtime 파일을 읽습니다.
2. `references/architecture_ko.md`를 읽습니다. 레이어 흐름과 이름은 기존 프로젝트의 방식을 먼저 따르고, 프로젝트에 정해진 방식이 없을 때만 `C` 관행을 따릅니다.
3. SQL을 작성하기 전에 `references/sql-rules_ko.md`를 읽고 DBMS를 확인합니다.
4. Java 코드는 `references/code-inspection_ko.md`의 PMD 규칙을 통과하도록 작성합니다.

## 검토할 때

1. 버전과 DBMS를 확인합니다.
2. 관련된 파일마다 **검사 방법** 열을 사용하여 코드를 검사합니다.
3. 발견한 사항은 `R` 위반을 먼저 적고, 그다음에 `G`와 `C` 권장 사항을 적습니다.
4. 사항마다 파일과 행 번호, 규칙 번호와 강도, 그리고 버전 파일의 클래스 이름을 사용한 구체적인 수정 방법을 제시합니다.
