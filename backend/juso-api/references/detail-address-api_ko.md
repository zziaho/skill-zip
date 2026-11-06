# 상세주소 API (동, 층, 호)

건물 하나에 등록된 동, 층, 호 이름을 반환하므로 사용자가 직접 입력하지 않고 호를 선택할 수 있습니다. 출처는 상세주소 검색 API 페이지(2026-11-06 저장), 가이드 PDF "[가이드]상세주소검색API_활용_방법"(24쪽, 2025-12), 샘플입니다. 이 기능의 팝업 형태는 `popup-api_ko.md`의 `useDetailAddr=Y` 옵션입니다.

`R`, `G`, `D`는 `SKILL_ko.md`에 정의되어 있습니다.

## 엔드포인트

| 용도 | URL |
|------|-----|
| 서버 간 호출 | `https://business.juso.go.kr/addrlink/addrDetailApi.do` |
| JSONP | `https://business.juso.go.kr/addrlink/addrDetailApiJsonp.do` |

- 내려받는 샘플은 `www.juso.go.kr`을 호출하고, Java 컨트롤러는 **좌표** 엔드포인트 `addrCoordApi.do`를 호출합니다. 페이지와 가이드는 위의 URL을 사용하므로 샘플의 URL을 복사하지 않습니다(`D`).

## 요청 변수

| 이름 | 필수 | 기본값 | 설명 |
|------|------|--------|------|
| `confmKey` | Y | | 이 API로 발급받은 승인키 |
| `admCd` | Y | | 행정구역코드(10자리), 검색 결과에서 가져옵니다 |
| `rnMgtSn` | Y | | 도로명코드(12자리) |
| `udrtYn` | Y | | `0` 지상, `1` 지하 |
| `buldMnnm` | Y | | 건물 본번 |
| `buldSlno` | Y | | 건물 부번, 없으면 `0` |
| `searchType` | N | `dong` | `dong`: 동 목록, `floorho`: 층과 호 목록 |
| `dongNm` | N | | 층과 호를 조회할 동(`searchType=floorho`일 때) |
| `resultType` | N | `xml` | `xml` 또는 `json` |

- `admCd`, `rnMgtSn`, `udrtYn`, `buldMnnm`, `buldSlno`는 사용자가 선택한 주소의 도로명주소 검색, 영문 검색, 좌표 API 결과에서 가져옵니다.
- 사이트의 API 목록은 이 API를 신청할 수 있는 별도 항목으로 제공합니다. 어떤 유형의 키를 받는지는 밝히지 않습니다. 이 API의 오류 표에는 "(팝업API 승인키 사용불가)"라고 적혀 있고, 검색 페이지에는 "(검색API 승인키 사용불가)"라고 적혀 있습니다. `D`: 이 API용 키를 신청합니다.

## 2단계 흐름

```
1. searchType=dong            → list of dongNm      (fill the "동" select)
2. searchType=floorho&dongNm=… → list of floorNm, hoNm (fill the "층/호" select)
```

- 단계는 둘뿐이며, 층과 호는 2단계에서 함께 반환됩니다.
- 1단계에서 동이 하나도 반환되지 않으면 샘플은 "동 표기 없음" 옵션을 보여 줍니다. 동이 없는 건물의 층과 호를 조회하는 방법은 자료에 나와 있지 않습니다. `D`: `dongNm`을 비운 채로 2단계를 시도하고, 등록된 호가 없는 건물이 많으므로 항상 사용자가 상세주소를 직접 입력할 수 있게 합니다.
- 가이드의 샘플 응답은 어느 단계에 대한 응답인지 밝히지 않으며, `dongNm`, `floorNm`, `hoNm`이 함께 들어 있고 `totalCount`는 1인데 항목은 여러 개입니다. 둘 다 믿지 않습니다(`D`).
- 샘플 주석에 따르면 테스트 키 `TESTJUSOGOKR`은 이 API에서 고정된 테스트 값만 반환합니다(`G`). 실제 건물을 확인하려면 개발승인키를 사용합니다.

## 출력

| 구분 | 이름 | 설명 |
|------|------|------|
| common | `totalCount`, `errorCode`, `errorMessage` | 검색 API와 같습니다 |
| juso | `admCd`, `rnMgtSn`, `udrtYn`, `buldMnnm`, `buldSlno` | 건물 코드를 그대로 반환합니다 |
| juso | `bdMgtSn` | 건물관리번호(PDF의 표와 샘플 응답에 있고, 페이지의 표에는 없습니다) |
| juso | `dongNm` | 동 이름. 예: `가동`, `101동` |
| juso | `floorNm` | 층 이름 |
| juso | `hoNm` | 호 이름 |

선택한 값으로 `101동 1004호` 같은 상세주소를 조합하고, `search-api_ko.md`("저장하고 표시할 주소 조합")에서 설명한 대로 삽입합니다.

## 오류 코드

| 코드 | 의미 |
|------|------|
| `0` | 정상 |
| `-999` | 시스템에러 |
| `E0001` | 승인되지 않은 KEY |
| `E0002` | `admCd` 누락 |
| `E0003` | `rnMgtSn` 누락 |
| `E0004` | `udrtYn` 누락 |
| `E0005` | `buldMnnm` 누락 |
| `E0006` | `buldSlno` 누락 |

번호 체계는 좌표 검색과 같고(`E0007`은 없습니다), 도로명주소 검색과 다릅니다.

## 샘플

| 샘플 코드 | 문제 | 대신 사용할 방법(`D`) |
|-----------|------|----------------------|
| 컨트롤러가 `dongNm`만 인코딩하며, 파라미터가 없어도 `URLEncoder.encode`를 호출합니다 | 그대로 둔 값이 쿼리를 바꾸고, `dongNm`이 없는 요청은 예외가 발생합니다 | 모든 파라미터를 인코딩하고, `dongNm`이 비어 있으면 생략합니다 |
| 화면에 보이는 `<input>`에서 가져온 키와 `req.getParameter("confmKey")` | 공개된 키 | 서버 설정(`secure-coding` 23) |
| `"<option value='"+dongNm+"'>"+dongNm+"</option>"`와 `.html(htmlStr)` | 값이 HTML로 삽입됩니다 | `new Option(text, value)`나 `textContent` |
| JSON을 `text/xml`로 반환합니다 | 잘못된 타입입니다 | `application/json` |

```javascript
function fillSelect(select, values) {
  select.length = 0;
  values.forEach(function (v) { select.add(new Option(v, v)); });   // no HTML parsing
}
```

- 가이드의 차단 패턴 절은 검색어 필터링 안내를 반복하지만, 이 API에는 검색어가 없습니다.
