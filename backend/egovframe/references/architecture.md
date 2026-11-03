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
| 5 | Mapper interfaces carry the version's mapper annotation and are scanned by `MapperConfigurer`; DAO classes extend `EgovAbstractMapper` with `@Repository` | G | Confirm every Mapper interface has the annotation and its package is in `basePackage` |
| 6 | Transactions are applied by AOP on ServiceImpl methods with `rollback-for="Exception"` | G | Find the `tx:advice` or `@Transactional` setup and confirm it covers `*Impl` classes and checked exceptions |

The guide does not state which layer may call which. Treat a Controller that calls a Mapper directly as a `C` recommendation, not a violation.

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
| Spring XML config | `resources/egovframework/spring/` | `context-*.xml` (`context-common`, `context-datasource`, `context-mapper`, `context-transaction`, `context-idgen`, `context-properties`, `context-aspect`) | C |
| MVC config | `WEB-INF/config/egovframework/springmvc/` | `dispatcher-servlet.xml` | C |
| Messages | `resources/egovframework/message/` | `message-common*.properties` | C |

- Class names come from the table name in PascalCase; field names from columns in camelCase (generator spec).
- Spring Boot projects (`egovframe-boot-sample-java-config`) use Java config instead of the XML files. Keep the package layout.

## Naming of SQL IDs and URLs

| Item | Convention | Strength |
|------|------------|----------|
| Mapper namespace | Fully qualified name of the Mapper interface | G |
| SQL ID | Same as the Mapper method name | G |
| SQL IDs for CRUD | `insertXxx`, `updateXxx`, `deleteXxx`, `selectXxx`, `selectXxxList`, `selectXxxListTotCnt` | C |
| URLs | `/xxx/xxxList.do` (GET), `addXxxView.do`, `addXxx.do`, `updateXxxView.do`, `updateXxx.do`, `deleteXxx.do` (POST) | C |
| View names | `<module>/egovXxxList`, `<module>/egovXxxRegister` | C |

## Bean names and injection

| # | Rule | Strength | Check |
|---|------|----------|-------|
| 1 | Beans named `messageSource` and `leaveaTrace` must exist when any class extends `EgovAbstractServiceImpl` (it injects them by name) | R | Search the context config for both bean IDs |
| 2 | A bean named `sqlSession` (a `SqlSessionFactoryBean`) must exist when any DAO extends `EgovAbstractMapper` | R | Search for `id="sqlSession"` or an equivalent `@Bean` name |
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
