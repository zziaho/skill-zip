# 영문주소 API

도로명주소와 지번주소를 영문으로 반환합니다. 검색어는 한글이나 영문 모두 가능합니다. 출처는 영문주소 검색 API와 영문주소 팝업 API 페이지(2026-11-06 저장), 가이드 PDF "[가이드]영문주소_검색API_활용_방법"(25쪽, 2025-12)과 "[가이드]영문주소_팝업API_활용_방법"(19쪽, 2026-07), 샘플입니다.

여기에 나열하지 않은 내용은 `search-api_ko.md`(검색)와 `popup-api_ko.md`(팝업)와 같습니다. `R`, `G`, `D`는 `SKILL_ko.md`에 정의되어 있습니다.

## 검색 API

| 용도 | URL |
|------|-----|
| 서버 간 호출 | `https://business.juso.go.kr/addrlink/addrEngApi.do` |
| JSONP | `https://business.juso.go.kr/addrlink/addrEngApiJsonp.do` |

**요청 변수**: `confmKey`, `currentPage`, `countPerPage`, `keyword`, `resultType`이며, 의미와 제한은 도로명주소 검색과 같습니다. `hstryYn`, `firstSort`, `addInfoYn`은 없습니다.

**출력**: `common`은 도로명주소 검색과 같습니다(페이지는 `currentPerPage`로 적었지만 필드는 `currentPage`입니다). 각 `juso` 항목에는 다음이 있습니다.

| 이름 | 설명 |
|------|------|
| `roadAddr` | 영문 도로명주소. 예: `6 Gangnam-daero 12-gil, Seocho-gu, Seoul` |
| `jibunAddr` | 영문 지번주소. 예: `326-1 Yangjae-dong, Seocho-gu, Seoul` |
| `zipNo` | 우편번호 |
| `admCd`, `rnMgtSn`, `udrtYn`, `buldMnnm`, `buldSlno` | 좌표 API와 상세주소 API에 사용하는 코드 |
| `bdKdcd` | 공동주택 여부: `1` 예, `0` 아니요 |
| `siNm`, `sggNm`, `emdNm`, `liNm`, `rn` | 영문 시도명, 시군구명, 읍면동명, 리명, 도로명 |
| `mtYn`, `lnbrMnnm`, `lnbrSlno` | 산 여부와 지번 번호 |
| `korAddr` | 한글 도로명주소 |

- `roadAddrPart1`, `roadAddrPart2`, `engAddr`, `bdMgtSn`, `bdNm`, `detBdNmList`는 없습니다. 건물관리번호나 한글 참고항목이 필요하면 도로명주소 검색도 함께 호출하거나, 이 API 대신 도로명주소 검색의 `engAddr` 필드를 사용합니다(`D`).
- 페이지는 `korAddr`가 Number라고 적었지만 문자열입니다(PDF의 표와 샘플 응답이 일치합니다). 샘플 JSON 응답에는 XML 응답과 달리 `rn`이 없습니다. `D`: 모든 필드를 방어적으로 읽습니다.

**오류 코드**: 도로명주소 검색과 코드와 조치가 같지만, `E0005`부터는 메시지가 영어입니다. 예를 들어 `E0005`는 "No search word has been entered.", `E0008`은 "Address entered too short.", `E0013`은 "Can not search SQL & special characters(%,=,>,<,[,]).", `E0015`는 "The search range has been exceeded."입니다. `E0001`은 여전히 한국어입니다. 메시지 문구가 아니라 코드로 대응시킵니다(`D`).

**상세주소를 포함한 영문 주소 작성**: API 페이지는 한글 검색 페이지의 한글 표시 규칙과 `roadAddrPart1` + 상세주소 + `roadAddrPart2` 공식을 그대로 반복하지만, 이 API에는 그런 필드가 없습니다. 영문 조합 규칙은 제시되지 않았습니다. `D`: `101-dong 1004-ho, 6 Gangnam-daero 12-gil, Seocho-gu, Seoul`처럼 상세주소를 반환된 주소 앞에 두고, 한글 주소와 마찬가지로 사용자의 상세주소는 별도 필드에 보관합니다. 검색 API는 여전히 상세주소를 반환하지 않으므로 호출하는 쪽이 입력란을 만들어야 합니다(`R`. `search-api_ko.md`와 같습니다).

## 팝업 API

| 용도 | URL |
|------|-----|
| PC 팝업 | `https://business.juso.go.kr/addrlink/addrEngUrl.do` |

- 영문 팝업에는 모바일 URL과 `useDetailAddr`가 문서화되어 있지 않습니다.
- 요청 변수: `confmKey`, `returnUrl`, `resultType`(`1`은 도로명, `2`는 도로명과 지번이며 샘플은 `2`를 보냅니다), EUC-KR 시스템을 위한 `encodingType=EUC-KR`입니다.
- 출력과 콜백: 값 20개입니다. 콜백 순서는 출력 표와 다르며, `addrDetail`이 세 번째에 옵니다.

```
jusoCallBack(roadFullAddr, roadAddr, addrDetail, jibunAddr, zipNo, admCd, rnMgtSn, bdKdcd,
             siNm, sggNm, emdNm, liNm, rn, udrtYn, buldMnnm, buldSlno, mtYn, lnbrMnnm, lnbrSlno, korAddr)
```

  `roadFullAddr`는 영문 전체 도로명주소이고, `roadAddr`는 영문 도로명주소이며, `korAddr`는 한글 도로명주소입니다.
- `returnUrl`이 없을 때 returnUrl 페이지가 보여 주는 메시지는 "Please connect us with a normal route."입니다.
- 가이드의 JSP, ASP, PHP returnUrl 예시는 일부 변수만 선언하지만("필요한 항목 추가 기술") 값 20개를 모두 전달하고, ASP와 PHP 입력 화면 예시는 로드할 때 콜백을 값 19개(`korAddr` 없음)로 호출합니다. 내려받는 샘플을 사용하되 아래와 같이 바로잡습니다.

**보안**: 영문 팝업 샘플에도 한글 팝업과 같은 반사형 XSS가 있습니다. `jusoPopup.jsp`가 `"<%=roadFullAddr%>"`와 나머지 값 19개를 스크립트에 기록하며, PHP와 ASP 버전도 마찬가지입니다. `popup-api_ko.md`의 안전한 returnUrl 페이지를 위의 필드 목록과 액션 URL `addrEngUrl.do`로 사용합니다. 그 문서의 배포 시 주의할 점(CSRF 필터, `SameSite` 쿠키, opener 확인)도 똑같이 적용됩니다.
