# 예외, 로그, ID 생성, 프로퍼티

eGovFrame 실행환경이 제공하는 공통 서비스를 다룹니다. 따로 표시하지 않은 클래스 이름은 4.3과 5.0.2에 모두 있습니다. import와 삭제된 클래스는 버전 파일에서 확인합니다.

출처: `egovframe-runtime/business-logic-layer/exception-handling.md`, `foundation-layer-core/aop-guide.md`, `foundation-layer/logging.md`, `logging-slf4j.md`, `foundation-layer/id-generation.md`, `foundation-layer/property-service.md`, 실행환경 소스

## 예외

| # | 규칙 | 강도 | 검사 방법 |
|---|------|------|-----------|
| 1 | ServiceImpl에서 업무 오류는 `throw processException("메시지.키")`로 발생시킵니다. 이 메서드는 `messageSource`에서 메시지를 찾아 `EgovBizException`을 돌려줍니다 | G | ServiceImpl 클래스에서 `throw new ...Exception(`을 찾습니다 |
| 2 | 예외를 감쌀 때는 원인 예외를 넘깁니다: `processException("메시지.키", e)`. 메시지 인자가 필요하면 `String[]`을 받는 오버로드를 사용합니다 | G | catch한 예외를 버리지 않는지 확인합니다 |
| 3 | `EgovBizException`은 업무 오류용 검사 예외입니다(`BaseException`이 `Exception`을 상속합니다) | G | `processException`을 호출하는 메서드에 `throws Exception`이 선언되어 있는지 확인합니다 |
| 4 | 비검사 예외로 발생시키려면 감싸서 던집니다: `throw new BaseRuntimeException(processException("key"))` (5.0 샘플의 방식) | C | — |
| 5 | 메시지 키는 사용하는 모든 로캘의 `message-common*.properties` 파일에 있어야 합니다 | G | `processException`에서 사용하는 키를 하나씩 검색합니다 |
| 6 | 예외 후처리(로그 기록, 알림)는 AOP로 실행됩니다: after-throwing advice → `ExceptionTransfer.transfer()` → `ExceptionHandlerService` → 핸들러 | G | `context-aspect.xml`이나 Java 설정에서 `ExceptionTransfer`를 찾습니다 |
| 7 | 사용자 정의 핸들러는 `ExceptionHandler`를 구현합니다. 사용자 정의 매니저는 `AbstractExceptionHandleManager`를 상속하고 `ExceptionHandlerService`를 구현합니다 | G | — |
| 8 | 오류가 아닌 후처리에는 `leaveaTrace("메시지.키")`를 사용합니다. 이 메서드는 예외를 던지지 않습니다 | G | — |

`processException`의 반환형은 `EgovBizException`이 아니라 `Exception`입니다. 그래서 호출하는 쪽에서 `throw processException(...)`으로 작성해야 하고, 메서드에는 `throws Exception`을 선언해야 합니다.

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

실행환경 클래스는 다음과 같습니다.

| 클래스 | 역할 |
|--------|------|
| `org.egovframe.rte.fdl.cmmn.exception.EgovBizException` | 업무용 검사 예외 |
| `org.egovframe.rte.fdl.cmmn.exception.BaseRuntimeException` | 비검사 예외의 기반 클래스 |
| `org.egovframe.rte.fdl.cmmn.exception.FdlException` | 프레임워크(공통기반 레이어) 예외 |
| `org.egovframe.rte.fdl.cmmn.aspect.ExceptionTransfer` | AOP가 호출하며, 예외를 핸들러 매니저로 전달합니다 |
| `org.egovframe.rte.fdl.cmmn.exception.manager.DefaultExceptionHandleManager` | 기본 핸들러 매니저이며, 패턴으로 핸들러를 고릅니다 |
| `ExceptionHandler` 구현체 | 프로젝트에서 작성합니다. 가이드에 나오는 `EgovServiceExceptionHandler`는 실행환경의 테스트 소스에만 있고, 실행환경 JAR에는 들어 있지 않습니다 |

## 로그

| # | 규칙 | 강도 | 검사 방법 |
|---|------|------|-----------|
| 1 | 로그는 SLF4J로 기록하며, 구현체는 Log4j 2입니다(eGovFrame 3.0부터) | G | 애플리케이션 코드에서 `java.util.logging`, `commons-logging`, Log4j API를 직접 사용하는 곳을 찾습니다 |
| 2 | `System.out.println()`을 사용하지 않습니다. 가이드가 밝힌 이유는 콘솔 파일이 덮어쓰일 수 있고, 테스트 코드와 운영 코드가 달라지며, 동기화된 I/O 때문에 처리량이 떨어진다는 것입니다 | R | PMD 규칙 34 SystemPrintln |
| 3 | `printStackTrace()`를 사용하지 말고, 예외를 로그로 기록합니다 | R | PMD 규칙 7 AvoidPrintStackTrace |
| 4 | 문자열 연결 대신 `{}` 자리 표시자를 사용합니다 | G | `log.debug("..." + x)` 형태를 찾습니다 |
| 5 | `EgovAbstractServiceImpl`의 하위 클래스는 상속받은 `egovLogger`를 사용해도 되고, 샘플처럼 SLF4J 로거를 직접 선언해도 됩니다 | C | — |

## ID 생성

`EgovIdGnrService`(`org.egovframe.rte.fdl.idgnr`)는 ID를 `int`, `short`, `byte`, `long`, `BigDecimal`, `String` 형으로 만들어 줍니다(`getNextIntegerId()`, `getNextStringId()` 등).

| 구현체 (`org.egovframe.rte.fdl.idgnr.impl`) | ID를 얻는 곳 | 참고 |
|---------------------------------------------|--------------|------|
| `EgovTableIdGnrServiceImpl` | `table_name`(CHAR·VARCHAR)과 `next_id`(integer·DECIMAL) 칼럼을 가진 키 테이블 | 프로퍼티는 `dataSource`, `blockSize`, `table`, `tableName`입니다. `destroy-method="destroy"`를 지정합니다 |
| `EgovSequenceIdGnrServiceImpl` | DB 시퀀스 | MySQL에는 시퀀스가 없으므로 사용할 수 없습니다 |
| `EgovUUIdGnrServiceImpl` | UUID | DB에 접근하지 않습니다 |

| # | 규칙 | 강도 | 검사 방법 |
|---|------|------|-----------|
| 1 | 기본 키는 SQL의 `MAX(ID) + 1`이 아니라 ID 생성 서비스로 만듭니다 | G | 매퍼 XML에서 키를 만들려고 `MAX(`를 사용하는 곳을 찾습니다 |
| 2 | 접두어가 붙은 문자열 ID(예: `SAMPLE-00001`)는 `EgovIdGnrStrategyImpl`에 `prefix`, `cipers`(자릿수), `fillChar`를 지정해서 만듭니다 | G | — |
| 3 | `tableName`마다 ID 테이블에 해당하는 행이 처음 사용하기 전에 있어야 합니다 | G | DDL과 초기 데이터 스크립트를 확인합니다 |
| 4 | 코드 생성기와 샘플은 기본 키 생성 서비스의 빈 이름을 `egovIdGnrService`로 씁니다 | C | — |

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

## 프로퍼티와 메시지

| # | 규칙 | 강도 | 검사 방법 |
|---|------|------|-----------|
| 1 | 설정값은 `EgovPropertyService`(`org.egovframe.rte.fdl.property`)로 읽습니다. 구현체는 `EgovPropertyServiceImpl`입니다 | G | Controller에 하드코딩된 페이지 크기나 제한값을 찾습니다 |
| 2 | `EgovPropertyServiceImpl`을 사용하려면 basename에 `org/egovframe/rte/fdl/idgnr/messages/idgnr`와 `org/egovframe/rte/fdl/property/messages/properties`가 들어 있는 `messageSource` 빈이 필요합니다 | G | `messageSource`의 basename을 확인합니다 |
| 3 | 빈 이름은 문서마다 다릅니다. 가이드는 `propertyService`, 샘플은 `propertiesService`를 사용합니다 | C | 프로젝트에 이미 정의된 이름을 따릅니다 |
| 4 | 메시지 소스는 Spring의 `ReloadableResourceBundleMessageSource`를 사용합니다. 실행환경에는 별도의 메시지 소스 클래스가 없습니다 | G | — |
