# eGovFrame 5.x 실행환경

eGovFrame 5.x의 클래스 이름, import, 설정을 다룹니다. 실행환경 `v5.0.2-Final`(2026-09-22), `egovframe-web-sample`의 `v5.0.0` 태그, `egovframe-boot-sample-java-config`로 검증했습니다. 5.0.0은 2026-05-18에, 5.0.1은 2026-09-03에 배포되었습니다.

## 플랫폼

| 항목 | 5.0.2의 값 |
|------|------------|
| Java | 17 |
| Spring Framework | 6.2.11 |
| 서블릿과 어노테이션 | `jakarta.servlet.*`, `jakarta.annotation.Resource`, `jakarta.validation.*` |
| 실행환경 그룹 ID | `org.egovframe.rte` |
| 실행환경 아티팩트 ID | 하이픈 표기: `egovframe-rte-ptl-mvc`, `egovframe-rte-psl-dataaccess`, `egovframe-rte-fdl-idgnr`, `egovframe-rte-fdl-property` |
| 부모 POM | `org.egovframe.boot:egovframe-boot-starter-parent`(Spring Boot), `org.egovframe.web:egovframe-web-config-parent`(XML로 설정하는 웹) |
| Maven 저장소 | `https://maven.egovframe.go.kr/maven/` |

## 의존성

부모 POM이 실행환경 버전을 관리하므로, 의존성에는 버전을 적지 않습니다.

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

위의 부모 POM 버전은 공식 샘플에서 사용하는 값입니다. 버전을 판별할 때는 프로젝트에 적힌 부모 POM 버전을 읽습니다.

## 핵심 클래스

| 레이어 | 클래스 또는 어노테이션 | import |
|--------|------------------------|--------|
| 서비스 | `EgovAbstractServiceImpl` | `org.egovframe.rte.fdl.cmmn.EgovAbstractServiceImpl` |
| 서비스 | `EgovBizException` | `org.egovframe.rte.fdl.cmmn.exception.EgovBizException` |
| 데이터처리 (Mapper 인터페이스) | `@EgovMapper` | `org.egovframe.rte.psl.dataaccess.mapper.EgovMapper` |
| 데이터처리 (Mapper 스캔) | `MapperConfigurer` | `org.egovframe.rte.psl.dataaccess.mapper.MapperConfigurer` |
| 데이터처리 (MyBatis DAO) | `EgovAbstractMapper` | `org.egovframe.rte.psl.dataaccess.EgovAbstractMapper` |
| 데이터처리 (iBatis DAO, 레거시) | `EgovAbstractDAO` | `org.egovframe.rte.psl.dataaccess.EgovAbstractDAO` |
| 데이터처리 | `EgovMap` | `org.egovframe.rte.psl.dataaccess.util.EgovMap` |
| 화면처리 | `PaginationInfo` | `org.egovframe.rte.ptl.mvc.tags.ui.pagination.PaginationInfo` |
| 화면처리 | `AbstractKrdsPaginationRenderer` (KRDS 스타일 페이지 이동) | `org.egovframe.rte.ptl.mvc.tags.ui.pagination.AbstractKrdsPaginationRenderer` |
| 화면처리 (입력값 검증) | Bean Validation `@Valid` + `BindingResult` | `jakarta.validation.Valid` |
| 공통기반 | `EgovIdGnrService` | `org.egovframe.rte.fdl.idgnr.EgovIdGnrService` |
| 공통기반 | `EgovPropertyService` | `org.egovframe.rte.fdl.property.EgovPropertyService` |
| 공통기반 (암호화) | `EgovCryptoService`, `EgovARIACryptoService`, `EgovDigestService`, `EgovEnvCryptoService` | `org.egovframe.rte.fdl.crypto.*` |
| 공통기반 (암호화 설정) | `EgovCryptoConfiguration` | `org.egovframe.rte.fdl.crypto.config.EgovCryptoConfiguration` |
| 공통기반 (보안 설정) | `EgovSecurityConfiguration` | `org.egovframe.rte.fdl.security.config.EgovSecurityConfiguration` |
| 공통기반 (보안) | `EgovSecuredObjectService` | `org.egovframe.rte.fdl.security.secureobject.EgovSecuredObjectService` |
| 공통기반 (접근 제어 설정) | `EgovAccessConfiguration` | `org.egovframe.rte.fdl.access.config.EgovAccessConfiguration` |

- `EgovAbstractServiceImpl`은 `jakarta.annotation.Resource`로 `messageSource`와 `leaveaTrace`를 주입받습니다. `egovLogger`는 하위 클래스의 이름을 로거 이름으로 사용합니다.
- `EgovAbstractMapper`는 `jakarta.annotation.Resource`로 `sqlSession`을 주입받습니다. `selectByPk`와 `list`는 `@Deprecated`이므로 `selectOne`과 `selectList`를 사용합니다.

## 예시

5.0 웹 샘플 방식으로 작성한 Mapper 인터페이스, ServiceImpl, Controller입니다.

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

Boot 샘플은 이름 없는 `@Service`와 `@EgovMapper`, 생성자 주입을 사용합니다. 두 방식 모두 올바르므로, 프로젝트의 방식을 따릅니다.

## 4.x에서 바뀐 점

`v4.3.0-Final`과 `v5.0.2-Final`의 클래스 목록을 비교하여 검증했습니다.

| 4.x | 5.x | 조치 |
|-----|-----|------|
| Java 1.8, Spring 5.3 | Java 17, Spring 6.2 | JDK와 Spring에 의존하는 모든 라이브러리를 업그레이드합니다 |
| `javax.servlet`, `javax.annotation`, `javax.validation`, `javax.persistence` | `jakarta.*` | JSP 태그 라이브러리와 필터를 포함하여 애플리케이션 전체의 import를 바꿉니다 |
| 점 표기 아티팩트 ID (`org.egovframe.rte.ptl.mvc`) | 하이픈 표기 아티팩트 ID (`egovframe-rte-ptl-mvc`)와 부모 POM | 의존성 부분을 다시 작성합니다 |
| `@Mapper` (`...dataaccess.mapper.Mapper`) | `@EgovMapper` (`...dataaccess.mapper.EgovMapper`) | 모든 Mapper 인터페이스의 어노테이션과 import를 바꿉니다 |
| `org.egovframe.rte.fdl.cryptography.*` | `org.egovframe.rte.fdl.crypto.*` | import를 바꿉니다. 클래스 이름은 그대로입니다 |
| `org.egovframe.rte.fdl.security.securedobject.*` | `org.egovframe.rte.fdl.security.secureobject.*` | import를 바꿉니다 |
| 보안, 암호화, 접근 제어의 XML 네임스페이스 설정 (`EgovSecurityNameHandler`, `EgovCryptoNameHandler`, `EgovAccessConfigNameHandler`) | Java 설정 (`EgovSecurityConfiguration`, `EgovCryptoConfiguration`, `EgovAccessConfiguration`) | XML 설정에 있는 eGovFrame 네임스페이스 요소를 설정 클래스로 바꿉니다 |
| `@CommandMap`, `CommandMapArgumentResolver`, `AnnotationCommandMapArgumentResolver`, `EgovRequestMappingHandlerAdapter` | 삭제됨 | `@ModelAttribute`로 VO에 바인딩하거나, `@RequestParam Map<String, String>`으로 `Map`에 바인딩합니다 |
| `SimpleUrlAnnotationHandlerMapping` | 삭제됨 | 표준 Spring MVC 요청 매핑을 사용합니다 |
| `RteFieldChecks`, `spring-modules-validation` (`DefaultBeanValidator`) | 삭제됨 | Bean Validation(`@Valid`, `jakarta.validation` 제약 조건)을 사용합니다 |
| `EgovTableIdGnrService`, `EgovSequenceIdGnrService`, `EgovUUIdGnrService` | 삭제됨. `...Impl` 클래스는 남아 있습니다 | 빈 정의가 `...Impl` 클래스를 가리키도록 바꿉니다 |
| `fdl.xml` 팩토리 (`EgovConcreteDOMFactory`, `EgovConcreteSAXFactory`, `abstractXMLFactoryService`) | 삭제됨. 5.x에는 `EgovAbstractXMLFactoryService`, `EgovDOMValidatorService`, `EgovSAXValidatorService`가 있습니다 | 5.x의 `fdl.xml` 클래스로 옮깁니다 |

가이드 문서 `presentation-layer/web-servlet-AnnotationCommandMapArgumentResolver.md`는 아직 `@CommandMap`을 설명하고 있습니다. 5.x에서는 이 기능을 사용하지 않습니다.
