# eGovFrame 4.x Runtime

Class names, imports and configuration for eGovFrame 4.x. Verified against runtime `v4.3.0-Final` and `egovframe-web-sample` tag `v4.3.0`. For 4.0 to 4.2, treat every class below as unverified and confirm it in the project's dependencies.

## Platform

| Item | Value in 4.3.0 |
|------|----------------|
| Java | 1.8 |
| Spring Framework | 5.3.37 |
| Servlet and annotations | `javax.servlet.*`, `javax.annotation.Resource` |
| Runtime group ID | `org.egovframe.rte` |
| Runtime artifact IDs | Dotted: `org.egovframe.rte.ptl.mvc`, `org.egovframe.rte.psl.dataaccess`, `org.egovframe.rte.fdl.idgnr`, `org.egovframe.rte.fdl.property` |
| Version property | `<org.egovframe.rte.version>4.3.0</org.egovframe.rte.version>` |

## Dependencies

```xml
<properties>
    <org.egovframe.rte.version>4.3.0</org.egovframe.rte.version>
</properties>

<dependency>
    <groupId>org.egovframe.rte</groupId>
    <artifactId>org.egovframe.rte.ptl.mvc</artifactId>
    <version>${org.egovframe.rte.version}</version>
</dependency>
<dependency>
    <groupId>org.egovframe.rte</groupId>
    <artifactId>org.egovframe.rte.psl.dataaccess</artifactId>
    <version>${org.egovframe.rte.version}</version>
</dependency>
```

## Core classes

| Layer | Class or annotation | Import |
|-------|---------------------|--------|
| Service | `EgovAbstractServiceImpl` | `org.egovframe.rte.fdl.cmmn.EgovAbstractServiceImpl` |
| Service | `EgovBizException` | `org.egovframe.rte.fdl.cmmn.exception.EgovBizException` |
| Persistence (Mapper interface) | `@Mapper` | `org.egovframe.rte.psl.dataaccess.mapper.Mapper` |
| Persistence (Mapper scanning) | `MapperConfigurer` | `org.egovframe.rte.psl.dataaccess.mapper.MapperConfigurer` |
| Persistence (MyBatis DAO) | `EgovAbstractMapper` | `org.egovframe.rte.psl.dataaccess.EgovAbstractMapper` |
| Persistence (iBatis DAO, legacy) | `EgovAbstractDAO` | `org.egovframe.rte.psl.dataaccess.EgovAbstractDAO` |
| Persistence | `EgovMap` | `org.egovframe.rte.psl.dataaccess.util.EgovMap` |
| Presentation | `PaginationInfo` | `org.egovframe.rte.ptl.mvc.tags.ui.pagination.PaginationInfo` |
| Presentation | `@CommandMap` (map binding) | `org.egovframe.rte.ptl.mvc.bind.annotation.CommandMap` |
| Presentation (validation) | `DefaultBeanValidator` (Commons Validator, from `org.egovframe.rte:spring-modules-validation:0.9`) | `org.springmodules.validation.commons.DefaultBeanValidator` |
| Foundation | `EgovIdGnrService` | `org.egovframe.rte.fdl.idgnr.EgovIdGnrService` |
| Foundation | `EgovPropertyService` | `org.egovframe.rte.fdl.property.EgovPropertyService` |
| Foundation (crypto) | `EgovCryptoService`, `EgovARIACryptoService`, `EgovDigestService`, `EgovEnvCryptoService` | `org.egovframe.rte.fdl.cryptography.*` |
| Foundation (security) | `EgovSecuredObjectService` | `org.egovframe.rte.fdl.security.securedobject.EgovSecuredObjectService` |

- `EgovAbstractServiceImpl` injects `messageSource` and `leaveaTrace` with `javax.annotation.Resource`.
- `EgovAbstractMapper` injects `sqlSession` with `javax.annotation.Resource`. `selectByPk` and `list` are `@Deprecated`; use `selectOne` and `selectList`.
- `EgovTableIdGnrService`, `EgovSequenceIdGnrService` and `EgovUUIdGnrService` exist alongside their `...Impl` classes. Configure beans with the `...Impl` classes so the code also works on 5.x.
- Security, crypto and access control can be configured with eGovFrame XML namespaces (`EgovSecurityNameHandler`, `EgovCryptoNameHandler`, `EgovAccessConfigNameHandler`).

## Example

Mapper interface and ServiceImpl in the 4.3 web sample style:

```java
import org.egovframe.rte.psl.dataaccess.mapper.Mapper;

@Mapper("sampleMapper")
public interface SampleMapper {
    void insertSample(SampleVO vo) throws Exception;
    SampleVO selectSample(SampleVO vo) throws Exception;
    List<?> selectSampleList(SampleDefaultVO searchVO) throws Exception;
    int selectSampleListTotCnt(SampleDefaultVO searchVO);
}
```

```java
import javax.annotation.Resource;

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
    public SampleVO selectSample(SampleVO vo) throws Exception {
        SampleVO resultVO = sampleMapper.selectSample(vo);
        if (resultVO == null) {
            throw processException("info.nodata.msg");
        }
        return resultVO;
    }
}
```

The 4.3 web sample itself uses an unnamed `@Mapper` with Lombok `@RequiredArgsConstructor` constructor injection. Both styles are valid; follow the project.

## Moving to 5.x

When a 4.x project is upgraded, read `../v5/runtime.md`, section "Changes from 4.x". Upgrading requires Java 17 and the `javax` → `jakarta` change across the whole application, not only eGovFrame classes.
