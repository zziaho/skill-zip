# Architecture and Naming

Layer structure, package layout and naming for eGovFrame applications. Class names and imports differ by version; take them from `v4/runtime.md` or `v5/runtime.md`.

Sources: `egovframe-runtime/intro/overview.md`, the CRUD code generator spec (`egovframe-development/vscode-implementation-tool/vscode-code-generation-generate-crud-code.md`), `egovframe-runtime/foundation-layer-core/aop-guide.md`, and the official samples `egovframe-web-sample` (tags `v4.3.0`, `v5.0.0`) and `egovframe-boot-sample-java-config`.

## Runtime service groups

The runtime is organised into service groups. Use them to place code and to choose runtime modules.

| Group | Responsibility | Runtime module prefix |
|-------|----------------|-----------------------|
| Presentation (화면처리) | MVC, input validation, i18n, pagination tags | `ptl` |
| Business logic (업무처리) | Business logic, process control, exception handling | `fdl.cmmn` (service base class) |
| Persistence (데이터처리) | DB access, MyBatis/iBatis/JPA, declarative transactions | `psl` |
| Integration (연계통합) | Integration and web services | `itl` |
| Batch (배치처리) | Spring Batch based jobs | `bat` |
| Foundation (공통기반) | ID generation, property, logging, crypto, security, exceptions | `fdl` |

## Layer chain

| # | Rule | Strength | Check |
|---|------|----------|-------|
| 1 | Requests flow Controller → Service interface → ServiceImpl → Mapper (or DAO). The generator produces exactly this chain | C | For each Controller, confirm it calls a Service interface, not a Mapper or DAO |
| 2 | Exceptions raised in the DAO/Mapper are handled in the Service layer (`aop-guide.md`) | G | Confirm Controllers do not catch persistence exceptions to build business messages |
| 3 | ServiceImpl extends `EgovAbstractServiceImpl` and implements the Service interface | G | Check the `extends` clause of every `*ServiceImpl` |
| 4 | Business errors are raised through `processException("message.key")` from the ServiceImpl | G | Look for `new RuntimeException`/`new Exception` in ServiceImpl classes |
| 5 | Persistence uses one of the styles in "Persistence styles" below, consistently within the project | G | Identify the style first; apply only that style's checks |
| 6 | Transactions are applied by AOP on ServiceImpl methods with `rollback-for="Exception"` | G | Find the `tx:advice`, the Java config advisor or `@Transactional` and confirm it covers `*Impl` classes and checked exceptions |
| 7 | The transaction pointcut expression matches the package where the `*Impl` classes actually are | R | Compare the expression with real paths: `execution(* x..service.*Impl.*(..))` does not match `x.y.service.impl.FooServiceImpl`; `execution(* x..impl.*Impl.*(..))` does. A mismatch means no transaction at all |

The guide does not state which layer may call which. Treat a Controller that calls a Mapper directly as a `C` recommendation, not a violation.

Rule 7 is `R` because a pointcut that matches nothing silently disables every transaction.

## Persistence styles

eGovFrame projects use one of three styles. The official samples use the Mapper interface style; projects built on the common components (공통컴포넌트) and their templates use the DAO class style.

| Style | How to recognise it | Rules that apply | Strength |
|-------|---------------------|------------------|----------|
| Mapper interface | Interfaces annotated with the version's mapper annotation (`@Mapper` in 4.x, `@EgovMapper` in 5.x), scanned by `MapperConfigurer` | Namespace is the interface's fully qualified name; SQL ID equals the method name; the interface's package is in `basePackage` | G |
| DAO class | `@Repository("XxxDAO")` classes that extend `EgovAbstractMapper`, often through a project base class such as `EgovComAbstractDAO`, calling `selectList("XxxDAO.selectXxxList", vo)` | Namespace is the DAO name string (e.g. `XxxDAO`); statement IDs are written as `"<namespace>.<id>"`; every ID used in Java exists in the XML | G |
| JPA | `*Repository` interfaces extending Spring Data repositories | Outside this skill (see SKILL.md, "Scope") | — |

Checks for both MyBatis styles:

| # | Rule | Strength | Check |
|---|------|----------|-------|
| 1 | The SQL session's mapper location pattern matches existing files | R | Expand `mapperLocations` (XML or Java config), including any `${Globals.DbType}` or other suffix, and confirm at least one file matches. A pattern such as `*_mariadb.xml` with only `*_mysql.xml` files loads no SQL at all |
| 2 | Every statement ID referenced from Java exists in the loaded XML | R | For DAO classes, search each `"<namespace>.<id>"` string; for Mapper interfaces, each method name |
| 3 | Projects with one SQL file per DBMS keep the statement IDs identical across the DBMS files | G | Compare the ID lists of `Xxx_SQL_<dbms>.xml` files of the same module |

Do not report the DAO class style as a deviation from the Mapper interface style; both are supported by the runtime.

## Package and file layout

Paths follow the generator spec and the samples. The root package in the samples is `egovframework.<app>.<module>`.

| Element | Location | Name | Strength |
|---------|----------|------|----------|
| VO | `<module>/service/` | `XxxVO`, search/paging parent `XxxDefaultVO` | C |
| Service interface | `<module>/service/` | `XxxService` (samples: `EgovXxxService`) | C |
| ServiceImpl | `<module>/service/impl/` | `XxxServiceImpl` | C |
| Mapper interface | `<module>/service/impl/` | `XxxMapper` | C |
| Controller | `<module>/web/` | `XxxController` | C |
| SQL mapper XML | `resources/egovframework/sqlmap/<app>/mappers/` | `Xxx_SQL.xml` | C |
| SQL mapper XML, one file per DBMS (common components) | `resources/egovframework/mapper/<app>/<module>/` | `Xxx_SQL_<dbms>.xml` (e.g. `_mysql`, `_oracle`, `_postgresql`), selected by `Globals.DbType` | C |
| DAO class (DAO class style) | `<module>/service/impl/` | `XxxDAO` | C |
| Spring XML config | `resources/egovframework/spring/` | `context-*.xml` (`context-common`, `context-datasource`, `context-mapper`, `context-transaction`, `context-idgen`, `context-properties`, `context-aspect`) | C |
| MVC config | `WEB-INF/config/egovframework/springmvc/` | `dispatcher-servlet.xml` | C |
| Messages | `resources/egovframework/message/` | `message-common*.properties` | C |

- Class names come from the table name in PascalCase; field names from columns in camelCase (generator spec).
- Spring Boot projects (`egovframe-boot-sample-java-config`) use Java config instead of the XML files. Keep the package layout.

## Naming of SQL IDs and URLs

| Item | Convention | Strength |
|------|------------|----------|
| Mapper namespace | Mapper interface style: fully qualified name of the interface. DAO class style: the DAO name string | G |
| SQL ID | Mapper interface style: same as the method name. DAO class style: referenced from Java as `"<namespace>.<id>"` | G |
| SQL IDs for CRUD | `insertXxx`, `updateXxx`, `deleteXxx`, `selectXxx`, `selectXxxList`, `selectXxxListTotCnt` | C |
| URLs | `/xxx/xxxList.do` (GET), `addXxxView.do`, `addXxx.do`, `updateXxxView.do`, `updateXxx.do`, `deleteXxx.do` (POST) | C |
| View names | `<module>/egovXxxList`, `<module>/egovXxxRegister` | C |

## Bean names and injection

| # | Rule | Strength | Check |
|---|------|----------|-------|
| 1 | Beans named `messageSource` and `leaveaTrace` must exist when any class extends `EgovAbstractServiceImpl` (it injects them by name) | R | Search the context config for both bean IDs |
| 2 | A bean named `sqlSession` (a `SqlSessionFactoryBean`) must exist when any DAO extends `EgovAbstractMapper` directly. A base class that overrides `setSqlSessionFactory` injects its own name instead (the common components' `EgovComAbstractDAO` uses `egov.sqlSession`) | R | For each DAO, find which `setSqlSessionFactory` applies and search for that bean name, including aliases such as `@Bean(name = {"sqlSession", "egov.sqlSession"})` |
| 3 | Name services and mappers explicitly, e.g. `@Service("sampleService")`, `@EgovMapper("sampleMapper")`, and inject with `@Resource(name = ...)` | C | Follow the project's existing style |
| 4 | Constructor injection with `final` fields is also used by the official samples (4.3 web sample, Boot sample) | C | Do not flag constructor injection as a deviation |

Rules 1 and 2 are marked `R` because the runtime source injects these names with `@Resource(name = ...)`; the application fails to start without them.

## Component scanning and transactions

The XML-based samples split scanning between two contexts. Keep this split when adding configuration.

| Context | Scans | Strength |
|---------|-------|----------|
| Root (`context-common.xml`) | All components except `@Controller` | C |
| Dispatcher (`dispatcher-servlet.xml`) | Only `@Controller`; excludes `@Service` and `@Repository` | C |

Transaction setup used by both web sample versions:

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

- `rollback-for="Exception"` matters: eGovFrame services throw checked exceptions (`EgovBizException` extends `Exception`), which Spring does not roll back by default.
- When a project uses `@Transactional` instead, check that it sets `rollbackFor = Exception.class`.
- Boot projects define the same advice in Java config (in the common components, `EgovConfigAppTransaction`), typically as an `AspectJExpressionPointcut` with a `RuleBasedTransactionAttribute` that has a `RollbackRuleAttribute` for `Exception`. Check the expression string with layer chain rule 7.
- The samples and common components use `DataSourceTransactionManager` for MyBatis/iBatis. When a project uses `JpaTransactionManager` instead (JPA and MyBatis together), do not report it as a violation: Spring's `JpaTransactionManager` also manages JDBC access on the same `DataSource`. Confirm only that the advice references the manager that exists.
