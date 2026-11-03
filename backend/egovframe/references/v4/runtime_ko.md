# eGovFrame 4.x 실행환경

eGovFrame 4.x의 클래스 이름, import, 설정을 다룹니다. 실행환경 `v4.3.0-Final`과 `egovframe-web-sample`의 `v4.3.0` 태그로 검증했습니다. 4.0부터 4.2까지는 아래 클래스를 모두 미검증으로 취급하고, 프로젝트의 의존성에서 직접 확인합니다.

## 플랫폼

| 항목 | 4.3.0의 값 |
|------|------------|
| Java | 1.8 |
| Spring Framework | 5.3.37 |
| 서블릿과 어노테이션 | `javax.servlet.*`, `javax.annotation.Resource` |
| 실행환경 그룹 ID | `org.egovframe.rte` |
| 실행환경 아티팩트 ID | 점 표기: `org.egovframe.rte.ptl.mvc`, `org.egovframe.rte.psl.dataaccess`, `org.egovframe.rte.fdl.idgnr`, `org.egovframe.rte.fdl.property` |
| 버전 프로퍼티 | `<org.egovframe.rte.version>4.3.0</org.egovframe.rte.version>` |

## 의존성

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

## 핵심 클래스

| 레이어 | 클래스 또는 어노테이션 | import |
|--------|------------------------|--------|
| 서비스 | `EgovAbstractServiceImpl` | `org.egovframe.rte.fdl.cmmn.EgovAbstractServiceImpl` |
| 서비스 | `EgovBizException` | `org.egovframe.rte.fdl.cmmn.exception.EgovBizException` |
| 데이터처리 (Mapper 인터페이스) | `@Mapper` | `org.egovframe.rte.psl.dataaccess.mapper.Mapper` |
| 데이터처리 (Mapper 스캔) | `MapperConfigurer` | `org.egovframe.rte.psl.dataaccess.mapper.MapperConfigurer` |
| 데이터처리 (MyBatis DAO) | `EgovAbstractMapper` | `org.egovframe.rte.psl.dataaccess.EgovAbstractMapper` |
| 데이터처리 (iBatis DAO, 레거시) | `EgovAbstractDAO` | `org.egovframe.rte.psl.dataaccess.EgovAbstractDAO` |
| 데이터처리 | `EgovMap` | `org.egovframe.rte.psl.dataaccess.util.EgovMap` |
| 화면처리 | `PaginationInfo` | `org.egovframe.rte.ptl.mvc.tags.ui.pagination.PaginationInfo` |
| 화면처리 | `@CommandMap` (Map 바인딩) | `org.egovframe.rte.ptl.mvc.bind.annotation.CommandMap` |
| 화면처리 (입력값 검증) | `DefaultBeanValidator` (Commons Validator, `org.egovframe.rte:spring-modules-validation:0.9`에서 제공) | `org.springmodules.validation.commons.DefaultBeanValidator` |
| 공통기반 | `EgovIdGnrService` | `org.egovframe.rte.fdl.idgnr.EgovIdGnrService` |
| 공통기반 | `EgovPropertyService` | `org.egovframe.rte.fdl.property.EgovPropertyService` |
| 공통기반 (암호화) | `EgovCryptoService`, `EgovARIACryptoService`, `EgovDigestService`, `EgovEnvCryptoService` | `org.egovframe.rte.fdl.cryptography.*` |
| 공통기반 (보안) | `EgovSecuredObjectService` | `org.egovframe.rte.fdl.security.securedobject.EgovSecuredObjectService` |

- `EgovAbstractServiceImpl`은 `javax.annotation.Resource`로 `messageSource`와 `leaveaTrace`를 주입받습니다.
- `EgovAbstractMapper`는 `javax.annotation.Resource`로 `sqlSession`을 주입받습니다. `selectByPk`와 `list`는 `@Deprecated`이므로 `selectOne`과 `selectList`를 사용합니다.
- `EgovTableIdGnrService`, `EgovSequenceIdGnrService`, `EgovUUIdGnrService`가 각각의 `...Impl` 클래스와 함께 있습니다. 5.x에서도 동작하도록 빈은 `...Impl` 클래스로 설정합니다.
- 보안, 암호화, 접근 제어는 eGovFrame XML 네임스페이스(`EgovSecurityNameHandler`, `EgovCryptoNameHandler`, `EgovAccessConfigNameHandler`)로 설정할 수 있습니다.

## 예시

4.3 웹 샘플 방식으로 작성한 Mapper 인터페이스와 ServiceImpl입니다.

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

4.3 웹 샘플 자체는 이름 없는 `@Mapper`와 Lombok `@RequiredArgsConstructor`를 사용한 생성자 주입을 씁니다. 두 방식 모두 올바르므로, 프로젝트의 방식을 따릅니다.

## 5.x로 전환할 때

4.x 프로젝트를 업그레이드할 때는 `../v5/runtime_ko.md`의 "4.x에서 바뀐 점" 절을 읽습니다. 업그레이드하려면 Java 17이 필요하고, eGovFrame 클래스뿐 아니라 애플리케이션 전체에서 `javax`를 `jakarta`로 바꿔야 합니다.
