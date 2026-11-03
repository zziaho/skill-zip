# 아키텍처와 이름 규칙

eGovFrame 애플리케이션의 레이어 구조, 패키지 구성, 이름 규칙을 다룹니다. 클래스 이름과 import는 버전마다 다르므로 `v4/runtime_ko.md` 또는 `v5/runtime_ko.md`에서 가져옵니다.

출처: `egovframe-runtime/intro/overview.md`, CRUD 코드 생성기 명세(`egovframe-development/vscode-implementation-tool/vscode-code-generation-generate-crud-code.md`), `egovframe-runtime/foundation-layer-core/aop-guide.md`, 공식 샘플 `egovframe-web-sample`(태그 `v4.3.0`, `v5.0.0`)과 `egovframe-boot-sample-java-config`

## 실행환경 서비스 그룹

실행환경은 여러 서비스 그룹으로 구성되어 있습니다. 코드를 어디에 둘지, 어떤 실행환경 모듈을 쓸지 정할 때 이 구분을 사용합니다.

| 그룹 | 담당하는 일 | 실행환경 모듈 접두어 |
|------|-------------|----------------------|
| 화면처리 (Presentation) | MVC, 입력값 검증, 다국어 처리, 페이지 이동 태그 | `ptl` |
| 업무처리 (Business Logic) | 업무 로직, 프로세스 제어, 예외 처리 | `fdl.cmmn` (서비스 기반 클래스) |
| 데이터처리 (Persistence) | DB 접근, MyBatis·iBatis·JPA, 선언적 트랜잭션 | `psl` |
| 연계통합 (Integration) | 시스템 연계와 웹 서비스 | `itl` |
| 배치처리 (Batch) | Spring Batch 기반 작업 | `bat` |
| 공통기반 (Foundation) | ID 생성, 프로퍼티, 로그, 암호화, 보안, 예외 | `fdl` |

## 레이어 흐름

| # | 규칙 | 강도 | 검사 방법 |
|---|------|------|-----------|
| 1 | 요청은 Controller → Service 인터페이스 → ServiceImpl → Mapper(또는 DAO) 순서로 흐릅니다. 코드 생성기도 정확히 이 흐름으로 코드를 만듭니다 | C | Controller마다 Mapper나 DAO가 아니라 Service 인터페이스를 호출하는지 확인합니다 |
| 2 | DAO·Mapper에서 발생한 예외는 Service 레이어에서 처리합니다(`aop-guide.md`) | G | Controller가 데이터 접근 예외를 잡아서 업무 메시지를 만들지 않는지 확인합니다 |
| 3 | ServiceImpl은 `EgovAbstractServiceImpl`을 상속하고 Service 인터페이스를 구현합니다 | G | 모든 `*ServiceImpl` 클래스의 `extends` 절을 확인합니다 |
| 4 | 업무 오류는 ServiceImpl에서 `processException("메시지.키")`로 발생시킵니다 | G | ServiceImpl 클래스에서 `new RuntimeException`, `new Exception`을 찾습니다 |
| 5 | 데이터 접근에는 아래 "저장 방식" 절의 방식 중 하나를 프로젝트 안에서 일관되게 사용합니다 | G | 먼저 저장 방식을 파악하고, 그 방식에 해당하는 검사만 적용합니다 |
| 6 | 트랜잭션은 AOP로 ServiceImpl 메서드에 적용하며, `rollback-for="Exception"`을 지정합니다 | G | `tx:advice`, Java 설정의 advisor, `@Transactional` 중 프로젝트가 쓰는 설정을 찾아서 `*Impl` 클래스와 검사 예외(checked exception)까지 포함하는지 확인합니다 |
| 7 | 트랜잭션 포인트컷 표현식이 `*Impl` 클래스가 실제로 있는 패키지와 일치해야 합니다 | R | 표현식을 실제 경로와 비교합니다. `execution(* x..service.*Impl.*(..))`는 `x.y.service.impl.FooServiceImpl`과 일치하지 않고, `execution(* x..impl.*Impl.*(..))`는 일치합니다. 일치하지 않으면 트랜잭션이 전혀 적용되지 않습니다 |

어느 레이어가 어느 레이어를 호출할 수 있는지는 가이드에 명시되어 있지 않습니다. 따라서 Controller가 Mapper를 직접 호출하는 코드는 위반이 아니라 `C` 권장 사항으로 보고합니다.

7번 규칙을 `R`로 표시한 이유는, 아무 클래스와도 일치하지 않는 포인트컷이 경고 없이 모든 트랜잭션을 꺼 버리기 때문입니다.

## 저장 방식

eGovFrame 프로젝트는 다음 세 가지 방식 중 하나를 사용합니다. 공식 샘플은 Mapper 인터페이스 방식을 쓰고, 공통컴포넌트와 그 템플릿을 기반으로 만든 프로젝트는 DAO 클래스 방식을 씁니다.

| 방식 | 알아보는 방법 | 적용하는 규칙 | 강도 |
|------|---------------|---------------|------|
| Mapper 인터페이스 | 버전에 맞는 Mapper 어노테이션(4.x는 `@Mapper`, 5.x는 `@EgovMapper`)이 붙어 있고 `MapperConfigurer`로 스캔하는 인터페이스 | 네임스페이스는 인터페이스의 전체 이름이고, SQL ID는 메서드 이름과 같습니다. 인터페이스의 패키지가 `basePackage`에 포함되어야 합니다 | G |
| DAO 클래스 | `EgovAbstractMapper`를 상속하는 `@Repository("XxxDAO")` 클래스입니다. `EgovComAbstractDAO` 같은 프로젝트 기반 클래스를 거쳐 상속하는 경우가 많고, `selectList("XxxDAO.selectXxxList", vo)`처럼 호출합니다 | 네임스페이스는 DAO 이름 문자열(예: `XxxDAO`)이고, 구문 ID는 `"<네임스페이스>.<ID>"`로 적습니다. Java에서 사용하는 ID는 모두 XML에 있어야 합니다 | G |
| JPA | Spring Data 저장소를 상속하는 `*Repository` 인터페이스 | 이 스킬의 범위 밖입니다(SKILL_ko.md의 "적용 범위" 참조) | — |

두 MyBatis 방식에 공통으로 적용하는 검사는 다음과 같습니다.

| # | 규칙 | 강도 | 검사 방법 |
|---|------|------|-----------|
| 1 | SQL 세션의 매퍼 위치 패턴과 일치하는 파일이 실제로 있어야 합니다 | R | XML이나 Java 설정의 `mapperLocations`를 `${Globals.DbType}` 같은 접미어까지 펼쳐서, 일치하는 파일이 하나 이상 있는지 확인합니다. 예를 들어 패턴이 `*_mariadb.xml`인데 `*_mysql.xml` 파일만 있으면 SQL이 하나도 로드되지 않습니다 |
| 2 | Java에서 참조하는 구문 ID는 모두 로드되는 XML에 있어야 합니다 | R | DAO 클래스는 `"<네임스페이스>.<ID>"` 문자열을, Mapper 인터페이스는 메서드 이름을 하나씩 검색합니다 |
| 3 | DBMS마다 SQL 파일을 따로 두는 프로젝트에서는 DBMS별 파일의 구문 ID가 같아야 합니다 | G | 같은 모듈에 있는 `Xxx_SQL_<dbms>.xml` 파일들의 ID 목록을 비교합니다 |

DAO 클래스 방식을 Mapper 인터페이스 방식에서 벗어난 것으로 보고하지 않습니다. 실행환경은 두 방식을 모두 지원합니다.

## 패키지와 파일 구성

경로는 코드 생성기 명세와 샘플을 따릅니다. 샘플에서 사용하는 최상위 패키지는 `egovframework.<앱>.<모듈>`입니다.

| 요소 | 위치 | 이름 | 강도 |
|------|------|------|------|
| VO | `<모듈>/service/` | `XxxVO`, 검색·페이징용 부모 클래스 `XxxDefaultVO` | C |
| Service 인터페이스 | `<모듈>/service/` | `XxxService` (샘플: `EgovXxxService`) | C |
| ServiceImpl | `<모듈>/service/impl/` | `XxxServiceImpl` | C |
| Mapper 인터페이스 | `<모듈>/service/impl/` | `XxxMapper` | C |
| Controller | `<모듈>/web/` | `XxxController` | C |
| SQL 매퍼 XML | `resources/egovframework/sqlmap/<앱>/mappers/` | `Xxx_SQL.xml` | C |
| DBMS마다 따로 두는 SQL 매퍼 XML (공통컴포넌트) | `resources/egovframework/mapper/<앱>/<모듈>/` | `Xxx_SQL_<dbms>.xml` (예: `_mysql`, `_oracle`, `_postgresql`). `Globals.DbType`에 따라 선택됩니다 | C |
| DAO 클래스 (DAO 클래스 방식) | `<모듈>/service/impl/` | `XxxDAO` | C |
| Spring XML 설정 | `resources/egovframework/spring/` | `context-*.xml` (`context-common`, `context-datasource`, `context-mapper`, `context-transaction`, `context-idgen`, `context-properties`, `context-aspect`) | C |
| MVC 설정 | `WEB-INF/config/egovframework/springmvc/` | `dispatcher-servlet.xml` | C |
| 메시지 | `resources/egovframework/message/` | `message-common*.properties` | C |

- 클래스 이름은 테이블 이름을 PascalCase로, 필드 이름은 칼럼 이름을 camelCase로 바꿔서 만듭니다(코드 생성기 명세).
- Spring Boot 프로젝트(`egovframe-boot-sample-java-config`)는 XML 파일 대신 Java 설정을 사용합니다. 패키지 구성은 그대로 유지합니다.

## SQL ID와 URL 이름

| 항목 | 관행 | 강도 |
|------|------|------|
| Mapper 네임스페이스 | Mapper 인터페이스 방식: 인터페이스의 전체 패키지 경로를 포함한 이름. DAO 클래스 방식: DAO 이름 문자열 | G |
| SQL ID | Mapper 인터페이스 방식: 메서드 이름과 같게 합니다. DAO 클래스 방식: Java에서 `"<네임스페이스>.<ID>"`로 참조합니다 | G |
| CRUD용 SQL ID | `insertXxx`, `updateXxx`, `deleteXxx`, `selectXxx`, `selectXxxList`, `selectXxxListTotCnt` | C |
| URL | `/xxx/xxxList.do` (GET), `addXxxView.do`, `addXxx.do`, `updateXxxView.do`, `updateXxx.do`, `deleteXxx.do` (POST) | C |
| 뷰 이름 | `<모듈>/egovXxxList`, `<모듈>/egovXxxRegister` | C |

## 빈 이름과 의존성 주입

| # | 규칙 | 강도 | 검사 방법 |
|---|------|------|-----------|
| 1 | `EgovAbstractServiceImpl`을 상속하는 클래스가 하나라도 있으면 `messageSource`와 `leaveaTrace`라는 이름의 빈이 있어야 합니다(이름으로 주입받기 때문입니다) | R | 컨텍스트 설정에서 두 빈 ID를 찾습니다 |
| 2 | `EgovAbstractMapper`를 직접 상속하는 DAO가 하나라도 있으면 `sqlSession`이라는 이름의 빈(`SqlSessionFactoryBean`)이 있어야 합니다. `setSqlSessionFactory`를 재정의한 기반 클래스는 자신이 지정한 이름의 빈을 주입받습니다(공통컴포넌트의 `EgovComAbstractDAO`는 `egov.sqlSession`을 사용합니다) | R | DAO마다 어느 `setSqlSessionFactory`가 적용되는지 확인하고, 그 빈 이름을 찾습니다. `@Bean(name = {"sqlSession", "egov.sqlSession"})` 같은 별칭도 포함합니다 |
| 3 | 서비스와 Mapper에는 `@Service("sampleService")`, `@EgovMapper("sampleMapper")`처럼 이름을 명시하고, `@Resource(name = ...)`로 주입합니다 | C | 프로젝트의 기존 방식을 따릅니다 |
| 4 | `final` 필드를 사용하는 생성자 주입도 공식 샘플(4.3 웹 샘플, Boot 샘플)에서 사용합니다 | C | 생성자 주입을 표준에서 벗어난 방식으로 지적하지 않습니다 |

1번과 2번 규칙을 `R`로 표시한 이유는, 실행환경 소스가 이 이름들을 `@Resource(name = ...)`로 주입하기 때문입니다. 이 빈이 없으면 애플리케이션이 시작되지 않습니다.

## 컴포넌트 스캔과 트랜잭션

XML 기반 샘플은 두 컨텍스트에서 스캔 대상을 나눕니다. 설정을 추가할 때도 이 구분을 유지합니다.

| 컨텍스트 | 스캔 대상 | 강도 |
|----------|-----------|------|
| 루트 (`context-common.xml`) | `@Controller`를 제외한 모든 컴포넌트 | C |
| 디스패처 (`dispatcher-servlet.xml`) | `@Controller`만 포함하고, `@Service`와 `@Repository`는 제외 | C |

두 버전의 웹 샘플이 공통으로 사용하는 트랜잭션 설정은 다음과 같습니다.

```xml
<tx:advice id="txAdvice" transaction-manager="txManager">
    <tx:attributes>
        <tx:method name="*" rollback-for="Exception"/>
    </tx:attributes>
</tx:advice>

<aop:config>
    <aop:pointcut id="requiredTx" expression="execution(* egovframework.example.sample..impl.*Impl.*(..))"/>
    <aop:advisor advice-ref="txAdvice" pointcut-ref="requiredTx"/>
</aop:config>
```

- `rollback-for="Exception"`은 꼭 필요합니다. eGovFrame 서비스는 검사 예외(`EgovBizException`은 `Exception`을 상속합니다)를 던지는데, Spring은 기본 설정에서 검사 예외가 발생해도 롤백하지 않기 때문입니다.
- 프로젝트가 `@Transactional`을 사용한다면 `rollbackFor = Exception.class`가 지정되어 있는지 확인합니다.
- Boot 프로젝트는 같은 advice를 Java 설정(공통컴포넌트에서는 `EgovConfigAppTransaction`)으로 정의합니다. 보통 `AspectJExpressionPointcut`과, `Exception`에 대한 `RollbackRuleAttribute`를 가진 `RuleBasedTransactionAttribute`를 사용합니다. 표현식 문자열은 레이어 흐름의 7번 규칙으로 확인합니다.
- 샘플과 공통컴포넌트는 MyBatis·iBatis에 `DataSourceTransactionManager`를 사용합니다. JPA와 MyBatis를 함께 쓰는 프로젝트가 `JpaTransactionManager`를 사용하더라도 위반으로 보고하지 않습니다. Spring의 `JpaTransactionManager`는 같은 `DataSource`에서 이루어지는 JDBC 접근도 관리하기 때문입니다. advice가 실제로 존재하는 트랜잭션 매니저를 참조하는지만 확인합니다.
