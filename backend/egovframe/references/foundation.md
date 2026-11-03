# Exceptions, Logging, ID Generation, Properties

Cross-cutting services of the eGovFrame runtime. Class names here exist in both 4.3 and 5.0.2 unless stated; take imports and removed classes from the version file.

Sources: `egovframe-runtime/business-logic-layer/exception-handling.md`, `foundation-layer-core/aop-guide.md`, `foundation-layer/logging.md`, `logging-slf4j.md`, `foundation-layer/id-generation.md`, `foundation-layer/property-service.md`, and the runtime source.

## Exceptions

| # | Rule | Strength | Check |
|---|------|----------|-------|
| 1 | In a ServiceImpl, raise business errors with `throw processException("message.key")`. It resolves the message from `messageSource` and returns an `EgovBizException` | G | Find `throw new ...Exception(` in ServiceImpl classes |
| 2 | Pass the cause when wrapping: `processException("message.key", e)`; message arguments use the `String[]` overloads | G | Confirm caught exceptions are not dropped |
| 3 | `EgovBizException` is a checked exception (`BaseException` extends `Exception`) for business errors | G | Methods that call `processException` declare `throws Exception` |
| 4 | To raise an unchecked error, wrap it: `throw new BaseRuntimeException(processException("key"))` (5.0 sample pattern) | C | — |
| 5 | Message keys exist in the `message-common*.properties` files for every locale used | G | Search each key used in `processException` |
| 6 | Post-processing (logging, alerts) runs through AOP: after-throwing advice → `ExceptionTransfer.transfer()` → `ExceptionHandlerService` → handlers | G | Find `ExceptionTransfer` in `context-aspect.xml` or Java config |
| 7 | A custom handler implements `ExceptionHandler`; a custom manager extends `AbstractExceptionHandleManager` and implements `ExceptionHandlerService` | G | — |
| 8 | Use `leaveaTrace("message.key")` for post-processing that is not an error; it does not throw | G | — |

`processException` returns `Exception`, not `EgovBizException`, so the caller writes `throw processException(...)` and the method must declare `throws Exception`.

```java
@Override
public SampleVO selectSample(SampleVO vo) throws Exception {
    SampleVO resultVO = sampleMapper.selectSample(vo);
    if (resultVO == null) {
        throw processException("info.nodata.msg");
    }
    return resultVO;
}
```

Runtime classes:

| Class | Role |
|-------|------|
| `org.egovframe.rte.fdl.cmmn.exception.EgovBizException` | Checked business exception |
| `org.egovframe.rte.fdl.cmmn.exception.BaseRuntimeException` | Unchecked base exception |
| `org.egovframe.rte.fdl.cmmn.exception.FdlException` | Framework (foundation layer) exception |
| `org.egovframe.rte.fdl.cmmn.aspect.ExceptionTransfer` | Called by AOP to pass exceptions to handler managers |
| `org.egovframe.rte.fdl.cmmn.exception.manager.DefaultExceptionHandleManager` | Default handler manager, matches handlers by pattern |
| `ExceptionHandler` implementations | Written by the project. The guide's `EgovServiceExceptionHandler` exists only in the runtime's test sources, not in the runtime JAR |

## Logging

| # | Rule | Strength | Check |
|---|------|----------|-------|
| 1 | Log through SLF4J; the implementation is Log4j 2 (since eGovFrame 3.0) | G | Find `java.util.logging`, `commons-logging` or direct Log4j API use in application code |
| 2 | Do not use `System.out.println()`. The guide gives the reasons: overwritten console files, code that differs between test and production, synchronized I/O that lowers throughput | R | PMD rule 34 SystemPrintln |
| 3 | Do not use `printStackTrace()`; log the exception | R | PMD rule 7 AvoidPrintStackTrace |
| 4 | Use `{}` placeholders instead of string concatenation | G | Find `log.debug("..." + x)` |
| 5 | Subclasses of `EgovAbstractServiceImpl` may use the inherited `egovLogger`, or declare their own SLF4J logger as the samples do | C | — |

## ID generation

`EgovIdGnrService` (`org.egovframe.rte.fdl.idgnr`) produces IDs as `int`, `short`, `byte`, `long`, `BigDecimal` or `String` (`getNextIntegerId()`, `getNextStringId()`, and so on).

| Implementation (`org.egovframe.rte.fdl.idgnr.impl`) | Source of IDs | Notes |
|------------------------------------------------------|---------------|-------|
| `EgovTableIdGnrServiceImpl` | A key table with `table_name` (CHAR/VARCHAR) and `next_id` (integer/DECIMAL) columns | Properties `dataSource`, `blockSize`, `table`, `tableName`; set `destroy-method="destroy"` |
| `EgovSequenceIdGnrServiceImpl` | A DB sequence | Not usable on MySQL, which has no sequences |
| `EgovUUIdGnrServiceImpl` | UUID | No DB access |

| # | Rule | Strength | Check |
|---|------|----------|-------|
| 1 | Generate primary keys with an ID generation service, not `MAX(ID) + 1` in SQL | G | Search mapper XML for `MAX(` used to build keys |
| 2 | For prefixed string IDs (e.g. `SAMPLE-00001`), use `EgovIdGnrStrategyImpl` with `prefix`, `cipers` (digits) and `fillChar` | G | — |
| 3 | The ID table row for each `tableName` must exist before first use | G | Check the DDL/seed scripts |
| 4 | The generator and samples name the PK service bean `egovIdGnrService` | C | — |

```xml
<bean name="egovIdGnrService" class="org.egovframe.rte.fdl.idgnr.impl.EgovTableIdGnrServiceImpl" destroy-method="destroy">
    <property name="dataSource" ref="dataSource"/>
    <property name="strategy" ref="mixPrefixSample"/>
    <property name="blockSize" value="10"/>
    <property name="table" value="IDS"/>
    <property name="tableName" value="SAMPLE"/>
</bean>

<bean name="mixPrefixSample" class="org.egovframe.rte.fdl.idgnr.impl.strategy.EgovIdGnrStrategyImpl">
    <property name="prefix" value="SAMPLE-"/>
    <property name="cipers" value="5"/>
    <property name="fillChar" value="0"/>
</bean>
```

## Properties and messages

| # | Rule | Strength | Check |
|---|------|----------|-------|
| 1 | Read configuration values through `EgovPropertyService` (`org.egovframe.rte.fdl.property`), implemented by `EgovPropertyServiceImpl` | G | Find hard-coded page sizes and limits in Controllers |
| 2 | `EgovPropertyServiceImpl` needs a `messageSource` bean whose basenames include `org/egovframe/rte/fdl/idgnr/messages/idgnr` and `org/egovframe/rte/fdl/property/messages/properties` | G | Check the `messageSource` basenames |
| 3 | Bean names vary: the guide uses `propertyService`, the samples use `propertiesService` | C | Follow the name already defined in the project |
| 4 | The message source is Spring's `ReloadableResourceBundleMessageSource`; the runtime has no separate message source class | G | — |
