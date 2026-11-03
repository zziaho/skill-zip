# eGovFrame 5.x Runtime

Class names, imports and configuration for eGovFrame 5.x. Verified against runtime `v5.0.2-Final` (2026-09-22), `egovframe-web-sample` tag `v5.0.0` and `egovframe-boot-sample-java-config`. 5.0.0 was released on 2026-05-18 and 5.0.1 on 2026-09-03. For 5.0.0 and 5.0.1 the full class list was not compared; the 5.0.0 web sample uses the same core classes (`@EgovMapper`, `EgovAbstractServiceImpl`, `jakarta.*`), so treat other classes as unverified on those versions.

## Platform

| Item | Value in 5.0.2 |
|------|----------------|
| Java | 17 |
| Spring Framework | 6.2.11 |
| Servlet and annotations | `jakarta.servlet.*`, `jakarta.annotation.Resource`, `jakarta.validation.*` |
| Runtime group ID | `org.egovframe.rte` |
| Runtime artifact IDs | Hyphenated: `egovframe-rte-ptl-mvc`, `egovframe-rte-psl-dataaccess`, `egovframe-rte-fdl-idgnr`, `egovframe-rte-fdl-property` |
| Parent POMs | `org.egovframe.boot:egovframe-boot-starter-parent` (Spring Boot), `org.egovframe.web:egovframe-web-config-parent` (XML-configured web) |
| Maven repository | `https://maven.egovframe.go.kr/maven/` |

## Dependencies

The parent POM manages runtime versions, so the dependencies need no version.

```xml
<parent>
    <groupId>org.egovframe.boot</groupId>
    <artifactId>egovframe-boot-starter-parent</artifactId>
    <version>5.0.1</version>
</parent>

<dependency>
    <groupId>org.egovframe.rte</groupId>
    <artifactId>egovframe-rte-ptl-mvc</artifactId>
</dependency>
<dependency>
    <groupId>org.egovframe.rte</groupId>
    <artifactId>egovframe-rte-psl-dataaccess</artifactId>
</dependency>
```

The parent version above is the one used by the official samples. Read the project's own parent version for version detection.

## Core classes

| Layer | Class or annotation | Import |
|-------|---------------------|--------|
| Service | `EgovAbstractServiceImpl` | `org.egovframe.rte.fdl.cmmn.EgovAbstractServiceImpl` |
| Service | `EgovBizException` | `org.egovframe.rte.fdl.cmmn.exception.EgovBizException` |
| Persistence (Mapper interface) | `@EgovMapper` | `org.egovframe.rte.psl.dataaccess.mapper.EgovMapper` |
| Persistence (Mapper scanning) | `MapperConfigurer` | `org.egovframe.rte.psl.dataaccess.mapper.MapperConfigurer` |
| Persistence (MyBatis DAO) | `EgovAbstractMapper` | `org.egovframe.rte.psl.dataaccess.EgovAbstractMapper` |
| Persistence (iBatis DAO, legacy) | `EgovAbstractDAO` | `org.egovframe.rte.psl.dataaccess.EgovAbstractDAO` |
| Persistence | `EgovMap` | `org.egovframe.rte.psl.dataaccess.util.EgovMap` |
| Presentation | `PaginationInfo` | `org.egovframe.rte.ptl.mvc.tags.ui.pagination.PaginationInfo` |
| Presentation | `AbstractKrdsPaginationRenderer` (KRDS-styled pagination) | `org.egovframe.rte.ptl.mvc.tags.ui.pagination.AbstractKrdsPaginationRenderer` |
| Presentation (validation) | Bean Validation `@Valid` + `BindingResult` | `jakarta.validation.Valid` |
| Foundation | `EgovIdGnrService` | `org.egovframe.rte.fdl.idgnr.EgovIdGnrService` |
| Foundation | `EgovPropertyService` | `org.egovframe.rte.fdl.property.EgovPropertyService` |
| Foundation (crypto) | `EgovCryptoService`, `EgovARIACryptoService`, `EgovDigestService`, `EgovEnvCryptoService` | `org.egovframe.rte.fdl.crypto.*` |
| Foundation (crypto config) | `EgovCryptoConfiguration` | `org.egovframe.rte.fdl.crypto.config.EgovCryptoConfiguration` |
| Foundation (security config) | `EgovSecurityConfiguration` | `org.egovframe.rte.fdl.security.config.EgovSecurityConfiguration` |
| Foundation (security) | `EgovSecuredObjectService` | `org.egovframe.rte.fdl.security.secureobject.EgovSecuredObjectService` |
| Foundation (access config) | `EgovAccessConfiguration` | `org.egovframe.rte.fdl.access.config.EgovAccessConfiguration` |

- `EgovAbstractServiceImpl` injects `messageSource` and `leaveaTrace` with `jakarta.annotation.Resource`. Its `egovLogger` uses the subclass as the logger name.
- `EgovAbstractMapper` injects `sqlSession` with `jakarta.annotation.Resource`. `selectByPk` and `list` are `@Deprecated`; use `selectOne` and `selectList`.

## Example

Mapper interface, ServiceImpl and Controller in the 5.0 web sample style:

```java
import org.egovframe.rte.psl.dataaccess.mapper.EgovMapper;

@EgovMapper("sampleMapper")
public interface SampleMapper {
    void insertSample(SampleVO vo) throws Exception;
    SampleVO selectSample(SampleVO vo) throws Exception;
    List<?> selectSampleList(SampleVO vo) throws Exception;
    int selectSampleListTotCnt(SampleVO vo);
}
```

```java
import jakarta.annotation.Resource;

import org.egovframe.rte.fdl.cmmn.EgovAbstractServiceImpl;
import org.egovframe.rte.fdl.idgnr.EgovIdGnrService;
import org.springframework.stereotype.Service;

@Service("sampleService")
public class EgovSampleServiceImpl extends EgovAbstractServiceImpl implements EgovSampleService {

    @Resource(name = "sampleMapper")
    private SampleMapper sampleMapper;

    @Resource(name = "egovIdGnrService")
    private EgovIdGnrService egovIdGnrService;

    @Override
    public void insertSample(SampleVO vo) throws Exception {
        vo.setId(egovIdGnrService.getNextStringId());
        sampleMapper.insertSample(vo);
    }
}
```

```java
@PostMapping("/addSample.do")
public String addSample(@Valid @ModelAttribute("sampleVO") SampleVO sampleVO,
        BindingResult bindingResult, Model model, SessionStatus status) throws Exception {
    if (bindingResult.hasErrors()) {
        model.addAttribute("sampleVO", sampleVO);
        return "sample/egovSampleRegister";
    }
    sampleService.insertSample(sampleVO);
    status.setComplete();
    return "redirect:/egovSampleList.do";
}
```

The Boot sample uses unnamed `@Service` and `@EgovMapper` with constructor injection. Both styles are valid; follow the project.

## Changes from 4.x

Verified by comparing the class lists of `v4.3.0-Final` and `v5.0.2-Final`.

| 4.x | 5.x | Action |
|-----|-----|--------|
| Java 1.8, Spring 5.3 | Java 17, Spring 6.2 | Upgrade the JDK and every Spring-dependent library |
| `javax.servlet`, `javax.annotation`, `javax.validation`, `javax.persistence` | `jakarta.*` | Replace imports across the application, including JSP tag libraries and filters |
| Dotted artifact IDs (`org.egovframe.rte.ptl.mvc`) | Hyphenated artifact IDs (`egovframe-rte-ptl-mvc`) and parent POMs | Rewrite the dependency section |
| `@Mapper` (`...dataaccess.mapper.Mapper`) | `@EgovMapper` (`...dataaccess.mapper.EgovMapper`) | Replace the annotation and import on every Mapper interface |
| `org.egovframe.rte.fdl.cryptography.*` | `org.egovframe.rte.fdl.crypto.*` | Change imports; the class names are unchanged |
| `org.egovframe.rte.fdl.security.securedobject.*` | `org.egovframe.rte.fdl.security.secureobject.*` | Change imports |
| XML namespace configuration for security, crypto and access (`EgovSecurityNameHandler`, `EgovCryptoNameHandler`, `EgovAccessConfigNameHandler`) | Java configuration (`EgovSecurityConfiguration`, `EgovCryptoConfiguration`, `EgovAccessConfiguration`) | Replace the eGovFrame namespace elements in the XML configuration with the configuration classes |
| `@CommandMap`, `CommandMapArgumentResolver`, `AnnotationCommandMapArgumentResolver`, `EgovRequestMappingHandlerAdapter` | Removed | Bind to a VO with `@ModelAttribute` or to a `Map` with `@RequestParam Map<String, String>` |
| `SimpleUrlAnnotationHandlerMapping` | Removed | Use standard Spring MVC request mapping |
| `RteFieldChecks`, `spring-modules-validation` (`DefaultBeanValidator`) | Removed | Use Bean Validation (`@Valid`, `jakarta.validation` constraints) |
| `EgovTableIdGnrService`, `EgovSequenceIdGnrService`, `EgovUUIdGnrService` | Removed; the `...Impl` classes remain | Point bean definitions at the `...Impl` classes |
| `fdl.xml` factories (`EgovConcreteDOMFactory`, `EgovConcreteSAXFactory`, `abstractXMLFactoryService`) | Removed; `EgovAbstractXMLFactoryService`, `EgovDOMValidatorService` and `EgovSAXValidatorService` exist in 5.x | Move to the 5.x `fdl.xml` classes |

The guide page `presentation-layer/web-servlet-AnnotationCommandMapArgumentResolver.md` still documents `@CommandMap`. Do not use it on 5.x.
