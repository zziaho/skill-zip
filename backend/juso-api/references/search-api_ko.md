# 도로명주소 검색 API

전국 도로명주소 데이터베이스를 검색어로 조회합니다. 호출하는 쪽이 검색어를 보내면 일치하는 주소 한 페이지를 XML이나 JSON으로 받습니다. 출처는 business.juso.go.kr의 API 페이지(2026-11-06 저장)와 가이드 PDF "[가이드]검색API_활용_방법"(27쪽, 2025-12)입니다. 둘이 다를 때는 표에 이 스킬이 어느 쪽을 따르는지 적었습니다.

`R`, `G`, `D`는 `SKILL_ko.md`에 정의되어 있습니다.

## 엔드포인트

| 용도 | URL | 방식 | 출력 |
|------|-----|------|------|
| 서버 간 호출 | `https://business.juso.go.kr/addrlink/addrLinkApi.do` | GET, POST | XML(기본값) 또는 JSON |
| 웹 페이지에서 직접 호출(JSONP) | `https://business.juso.go.kr/addrlink/addrLinkApiJsonp.do` | GET, POST | XML이나 JSON을 감싼 JSONP |

- 검색용 승인키로는 팝업 엔드포인트를 호출할 수 없고, 팝업용 승인키로는 이 엔드포인트를 호출할 수 없습니다(`R`. `SKILL_ko.md`의 승인키 참조).
- 행정망 안의 시스템은 다른 URL을 사용합니다. 가이드는 고객센터(1588-0061)에 문의하라고 안내합니다.
- 페이지에는 "Java 1.6 이상, TLS 1.2를 사용할 수 없는 환경에서는 `http://`를 사용"이라는 안내가 덧붙어 있습니다. `D`: `https://`만 사용합니다. HTTP로 호출하면 승인키와 사용자가 입력한 주소 검색어가 평문으로 전송됩니다(`secure-coding` SR2-8). 다운그레이드하지 말고 런타임을 고칩니다.

## 요청 변수

| 이름 | 타입 | 필수 | 기본값 | 설명 |
|------|------|------|--------|------|
| `confmKey` | String | Y | | 이 시스템에 발급된 승인키 |
| `currentPage` | Integer | Y | 1 | 페이지 번호, `n > 0` |
| `countPerPage` | Integer | Y | 10 | 페이지당 출력 건수, `0 < n <= 100` |
| `keyword` | String | Y | | 검색어(아래 규칙 참조) |
| `resultType` | String | N | `xml` | `xml` 또는 `json` |
| `hstryYn` | String | N | `N` | 변경된 주소 포함 여부. `Y`이면 이전 주소로도 현재 도로명주소를 찾습니다. 2020-12-08 추가 |
| `firstSort` | String | N | `none` | `none`은 정확도 순, `road`는 도로명에 검색어가 들어 있는 결과를 먼저, `location`은 지번주소에 대해 같은 방식으로 먼저 보여 줍니다. 2020-12-08 추가 |
| `addInfoYn` | String | N | `N` | `Y`이면 출력에 `hstryYn`, `relJibun`, `hemdNm`이 추가됩니다. 이 추가 필드는 나중에 바뀌거나 없어질 수 있다고 가이드가 경고합니다. 2020-12-08 추가 |

- `currentPage`와 `countPerPage`의 값 범위는 가이드 PDF와 샘플의 주석에서 가져왔습니다. 페이지의 표에는 없습니다.
- 검색어는 법정동 이름뿐 아니라 행정동 이름도 가능합니다.

**검색어 규칙**(`R`: 어기면 각각 오류 코드가 반환됩니다)

| 규칙 | 오류 |
|------|------|
| 비어 있지 않아야 합니다 | E0005 |
| 시도나 시군구 이름만 입력하면 안 됩니다 | E0006 |
| 두 글자 이상이어야 합니다 | E0008 |
| 숫자만 입력하면 안 되고, 문자와 숫자를 함께 입력해야 합니다 | E0009 |
| 한글 40자 또는 영문자와 숫자 80자 이하여야 합니다 | E0010 |
| 숫자가 10자를 넘게 이어지면 안 됩니다 | E0011 |
| 특수문자와 숫자만 입력하면 안 됩니다 | E0012 |
| SQL 예약어와 `%` `=` `>` `<` `[` `]`를 사용하면 안 됩니다 | E0013 |

SQL 예약어나 특수문자가 들어 있는 검색어는 오류 코드가 반환될 뿐 아니라 서비스의 보안 장비가 **호출한 IP를 차단**할 수도 있습니다. 아래 "검색어 필터"와 `SKILL_ko.md`를 참조합니다.

## 출력

결과는 `results`에 담기며, `common` 블록 하나와 `juso` 항목 목록(JSON은 배열, XML은 반복 요소)으로 구성됩니다. JSON에서는 모든 값이 문자열입니다.

**common**

| 이름 | 설명 |
|------|------|
| `totalCount` | 일치하는 전체 건수 |
| `currentPage` | 페이지 번호 |
| `countPerPage` | 페이지당 출력 건수 |
| `errorCode` | 성공이면 `0`, 아니면 아래 표의 코드 |
| `errorMessage` | 코드에 대한 메시지 |

**juso**

| 이름 | 필수 | 설명 |
|------|------|------|
| `roadAddr` | Y | 참고항목을 포함한 전체 도로명주소 |
| `roadAddrPart1` | Y | 참고항목을 제외한 도로명주소 |
| `roadAddrPart2` | N | 참고항목. 예: `(상암동)` |
| `jibunAddr` | Y | 지번주소 |
| `engAddr` | Y | 영문 도로명주소 |
| `zipNo` | Y | 우편번호 |
| `admCd` | Y | 행정구역코드(10자리) |
| `rnMgtSn` | Y | 도로명코드(12자리) |
| `bdMgtSn` | Y | 건물관리번호 |
| `detBdNmList` | N | 상세 건물명(예: 아파트 동 이름) |
| `bdNm` | N | 건물명 |
| `bdKdcd` | Y | 공동주택 여부: `1` 예, `0` 아니요 |
| `siNm` | Y | 시도명 |
| `sggNm` | Y | 시군구명 |
| `emdNm` | Y | 읍면동명 |
| `liNm` | N | 법정리명 |
| `rn` | Y | 도로명 |
| `udrtYn` | Y | 지하 여부: `0` 지상, `1` 지하 |
| `buldMnnm` | Y | 건물 본번 |
| `buldSlno` | Y | 건물 부번, 없으면 `0` |
| `mtYn` | Y | 산 여부: `0` 아니요, `1` 예 |
| `lnbrMnnm` | Y | 지번 본번(번지) |
| `lnbrSlno` | Y | 지번 부번(호), 없으면 `0` |
| `emdNo` | Y | 읍면동 일련번호 |
| `hstryYn` | | `addInfoYn=Y`일 때: `0`은 현재 주소, `1`은 변경된(이전) 주소로 찾은 경우 |
| `relJibun` | | `addInfoYn=Y`일 때: 관련 지번 |
| `hemdNm` | | `addInfoYn=Y`일 때: 관할주민센터. 참고용이며 실제와 다를 수 있습니다 |

- **페이지의 출력 표에는 오류가 있습니다**(`D`: 서로 일치하는 가이드 PDF의 표, 샘플 응답, 샘플 소스 코드를 근거로 위 표에서 바로잡았습니다). `currentPage`가 `currentPerPage`로, `lnbrMnnm`이 `InbrMnnm`(대문자 I)으로 적혀 있고, `emdNo` 행이 없으며, `emdNo`의 설명이 `lnbrSlno`로 올라가 있습니다. 소문자 `l`로 시작하는 이름을 사용합니다. `lnbr`은 지번(lot number)의 줄임말입니다.
- `sggNm`, `liNm`, `relJibun`, `hemdNm`의 필수 여부가 페이지와 PDF에서 서로 다릅니다. `D`: `liNm`은 선택 항목으로 취급하고(샘플은 빈 값으로 반환합니다), 주소의 모든 부분이 비어 있을 수 있다고 보고 저장합니다.
- `D`: 코드 값은 숫자가 아니라 문자열로 저장합니다. `zipNo`와 `emdNo`는 앞자리가 0이고(`03923`, `03`), `bdMgtSn`(25자리)은 64비트 정수에 들어가지 않습니다.

## 오류 코드

| 코드 | 메시지(요약) | 조치 |
|------|--------------|------|
| `0` | 정상 | |
| `-999` | 시스템에러 | 고객센터에 문의합니다 |
| `E0001` | 승인되지 않은 KEY | 키가 잘못되었거나, 팝업용 키를 검색에 사용했습니다(또는 그 반대) |
| `E0005` | 검색어가 입력되지 않았습니다 | 검색어를 입력합니다 |
| `E0006` | 주소를 상세히 입력해 주시기 바랍니다 | 시도명만으로는 검색할 수 없습니다 |
| `E0008` | 검색어는 두글자 이상 입력되어야 합니다 | 한 글자로는 검색할 수 없습니다 |
| `E0009` | 검색어는 문자와 숫자 같이 입력되어야 합니다 | 숫자만으로는 검색할 수 없습니다 |
| `E0010` | 검색어가 너무 깁니다 | 한글 40자 또는 영문자와 숫자 80자 이하 |
| `E0011` | 검색어에 너무 긴 숫자가 포함되어 있습니다 | 숫자는 10자 이하 |
| `E0012` | 특수문자+숫자만으로는 검색이 불가능 합니다 | |
| `E0013` | SQL 예약어 또는 특수문자( %,=,>,<,[,] )는 검색이 불가능 합니다 | 제거하고 다시 검색합니다 |
| `E0014` | 개발승인키 기간이 만료되어 서비스를 이용하실 수 없습니다 | 개발승인키를 새로 발급받습니다 |
| `E0015` | 검색 범위를 초과하였습니다 | 9,000건을 넘겨 페이지를 넘길 수 없습니다 |

- 가이드 PDF에는 `E0002`(승인되지 않은 사이트: 호출한 URL이나 IP가 키와 일치하지 않음)와 `E0003`(정상적인 경로로 접속하시기 바랍니다)도 있으며, `E0008`을 "한글자 이상"이라고 적었습니다. 페이지(2026-11-06 저장, PDF는 2025-12 작성)는 "두글자 이상"이라고 적었으며 조치 칸도 이와 일치합니다. `D`: 페이지를 따르되, 서버가 아직 `E0002`와 `E0003`을 반환할 수 있으므로 이 두 코드도 처리합니다.
- `E0001`의 조치 칸에 페이지는 "(검색API 승인키 사용불가)"라고 적었으며, 이는 팝업 페이지와 같은 문구입니다. "다른 API 유형의 키는 승인되지 않는다"는 뜻으로 읽습니다.
- `juso`를 읽기 전에 `errorCode`를 확인합니다. `totalCount`가 0이고 `errorCode`가 `0`이면 정상적인 빈 결과입니다. 일치해야 하는 검색인데 0건이 나오면 대개 검색어 인코딩 문제라고 가이드는 설명합니다.
- **`E0002`부터 `E0007`까지의 코드는 좌표 API와 상세주소 API에서 의미가 다릅니다.** API마다 오류 코드 맵을 따로 둡니다(`D`).

## 호출 방식

| 방식 | 흐름 | 사용하는 경우 |
|------|------|---------------|
| 서버 프록시(가이드 "일반적인 API 이용방법") | 브라우저 → 자체 서버 → juso → 자체 서버 → 브라우저 | `D`: 기본 방식입니다. 키가 서버에 남고, 서버가 호출을 검증하고 제한할 수 있으며, 응답이 페이지에 도달하기 전에 확인할 수 있습니다 |
| 페이지에서 JSONP(가이드 "웹 페이지에서 직접 API 이용방법") | 브라우저 → juso(JSONP) | 서버 측이 없는 정적 페이지에서만 사용합니다. 키와 검색어가 페이지의 URL에 실리고, 페이지가 제3자 스크립트 응답을 신뢰하게 됩니다 |

**공식 샘플이 잘못된 부분**(`D`. 샘플에서 복사한 코드를 검토할 때 확인합니다)

| 샘플 코드 | 문제 | 대신 사용할 방법 |
|-----------|------|------------------|
| 컨트롤러가 요청에서 `confmKey`를 받고(`req.getParameter("confmKey")`), 페이지가 키를 hidden `<input>`에 둡니다 | 키가 공개되고, 호출하는 누구나 임의의 키를 보낼 수 있습니다 | 키를 서버 설정에 보관합니다(`secure-coding` 23) |
| `keyword`만 URL 인코딩하고 `currentPage`, `countPerPage`, `resultType`, 키는 그대로 이어 붙입니다 | `&`나 `#`이 들어간 값이 상위 쿼리를 바꿉니다 | 모든 파라미터를 인코딩하고, `currentPage`와 `countPerPage`는 범위 안의 정수인지, `resultType`은 `xml`/`json`인지 검증합니다 |
| 검색어 필터가 페이지의 JavaScript에만 있습니다 | 컨트롤러를 바로 호출하면 필터를 거치지 않습니다 | 서버에서 검증합니다 |
| 타임아웃 없이 `url.openStream()`을 호출하고, `br.close()`가 `finally`에 없습니다 | 느린 상위 서버가 요청 스레드를 붙잡고, 오류가 나면 스트림이 누수됩니다 | 연결 타임아웃과 읽기 타임아웃을 설정하고 try-with-resources를 사용합니다(`secure-coding` 40) |
| 결과를 HTML 문자열로 이어 붙여 `$("#list").html(...)`로 삽입합니다 | 건물명 등의 값이 HTML로 삽입됩니다(`secure-coding` 4) | `textContent`나 `.text()`로 텍스트를 지정하거나 이스케이프합니다 |
| JSON 응답을 `Content-Type: text/xml`로 반환합니다 | 잘못된 타입입니다 | `application/json;charset=UTF-8` |
| jQuery 1.8.3 | 알려진 문제가 있는 오래된 라이브러리입니다 | 프로젝트의 최신 라이브러리를 사용합니다 |

**서버 프록시(Java, Spring MVC)**

```java
@Value("${juso.search.key}") private String jusoKey;   // never from the request
private static final int ROWS = 10;                       // countPerPage, 1 to 100

@GetMapping(value = "/api/address", produces = "application/json;charset=UTF-8")
public ResponseEntity<String> search(@RequestParam String keyword,
                                     @RequestParam(defaultValue = "1") int page) throws IOException {
    String kw = keyword.trim();
    if (!KeywordFilter.isAllowed(kw)) {
        return ResponseEntity.badRequest().body("{\"error\":\"invalid keyword\"}");
    }
    if (page < 1 || page > 9000 / ROWS) {                     // E0015: at most 9,000 results
        return ResponseEntity.badRequest().body("{\"error\":\"invalid page\"}");
    }
    String query = "confmKey=" + enc(jusoKey) + "&currentPage=" + page
            + "&countPerPage=" + ROWS + "&resultType=json&keyword=" + enc(kw);
    HttpURLConnection con = (HttpURLConnection)
            new URL("https://business.juso.go.kr/addrlink/addrLinkApi.do?" + query).openConnection();
    con.setConnectTimeout(3000);
    con.setReadTimeout(5000);
    try (InputStream in = con.getInputStream()) {
        String body = new String(in.readAllBytes(), StandardCharsets.UTF_8);  // Java 9+
        return ResponseEntity.ok(body);   // or parse it and return only the fields the page needs
    }
}

private static String enc(String s) throws UnsupportedEncodingException {
    return URLEncoder.encode(s, "UTF-8");
}
```

- 프록시 엔드포인트에 프로젝트에서 쓰는 보호 장치를 추가합니다. 세션이나 IP별 호출 제한과, POST를 쓴다면 CSRF 방어입니다. 호출이 반복되면 공격자가 아니라 **자체 서버**의 IP가 차단될 수 있습니다(`D`).
- 응답을 파싱해서 필요한 필드만 반환하면 상위 서버가 보낸 예상하지 못한 내용이 페이지에 들어가지 않습니다.

## 검색어 필터

가이드는 호출하기 전에 SQL 예약어(`or`, `select`, `insert`, `delete`, `update`, `create`, `drop`, `exec`, `union`, `fetch`, `declare`, `truncate`)와 `<` `>` `=` `%` 문자를 제거하고 사용자에게 메시지를 보여 주라고 요구합니다. 서비스의 보안 장비가 이를 SQL 삽입으로 간주해 **호출한 IP를 차단할 수 있기** 때문입니다(`R`). 가이드가 드는 차단 예시는 `' or '1'='1`, `' and 'f'='f`, `%27+and+`, `UNION+SELECT` 같은 패턴입니다.

- 이 필터가 보호하는 대상은 자체 시스템이 아니라 **서비스와 자체 IP**입니다. 자체 쿼리를 위한 입력값 검증 수단이 아닙니다(`D`).
- 샘플의 `checkSearchedWord`는 예약어를 부분 문자열로 보고 대소문자 구분 없이 각각 제거합니다. `KOREA`가 `KEA`가 되고 `ORANGE`가 `ANGE`가 되어 영문 도로명이 깨집니다. `E0013`이 거부하는 `[`와 `]`도 놓칩니다. `D`: 조용히 고쳐 쓰지 말고 거부하며, 예약어는 단어 전체로 비교하고, 대괄호를 포함합니다. 샘플의 주석도 예약어를 "앞뒤공백포함"(앞뒤 공백을 포함해서) 제거한다고 적었으므로, 단어 전체 비교가 샘플이 의도한 방식입니다.

```javascript
const BLOCKED_CHARS = /[%=<>\[\]]/;
const BLOCKED_WORDS = /\b(or|select|insert|delete|update|create|drop|exec|union|fetch|declare|truncate)\b/i;

function isAllowedKeyword(k) {
  return k.trim().length >= 2 && !BLOCKED_CHARS.test(k) && !BLOCKED_WORDS.test(k);
}
```

서버에도 `E0010`의 길이 제한을 포함해 같은 검사를 적용합니다.

```java
public final class KeywordFilter {
    private static final Pattern CHARS = Pattern.compile("[%=<>\\[\\]]");
    private static final Pattern WORDS = Pattern.compile(
        "\\b(or|select|insert|delete|update|create|drop|exec|union|fetch|declare|truncate)\\b",
        Pattern.CASE_INSENSITIVE);

    public static boolean isAllowed(String k) {
        return k.length() >= 2 && k.length() <= 80
            && !CHARS.matcher(k).find() && !WORDS.matcher(k).find();
    }
}
```

입력을 바꾸지 말고 "주소 검색어에 특수문자(%, =, <, >, [, ])나 SQL 예약어는 사용할 수 없습니다" 같은 메시지를 사용자에게 보여 줍니다.

## 페이지 나누기

- 페이지를 넘길 수 있는 결과는 최대 9,000건이며, 페이지당 10건이면 900페이지입니다(`E0015`, `R`). 더 넘기지 말고 사용자에게 검색어를 좁히도록 안내합니다.
- `countPerPage`는 최대 100입니다.
- 페이지의 페이지 나누기 샘플은 페이지당 출력 건수를 페이지 링크 개수로 쓰고, 이전 블록으로는 고정값 5만큼 이동합니다(`prePage = firstPage-5`). `D`: 페이지 블록 크기를 따로 두고 그 크기만큼 이동합니다.

## 저장하고 표시할 주소 조합

페이지가 제시하는 표시 순서는 시/도 + 시/군/구 + 읍/면 + 도로명 + 건물번호(본번-부번) + 상세주소(동/층/호) + (참고항목)입니다. 참고항목에는 법정동과 아파트 단지명이 들어가며, 읍/면 주소에는 단지명만 들어갑니다.

| 경우 | 예시 |
|------|------|
| 읍/면, 공동주택 | 경기도 가평군 가평읍 가화로 164, 201동 102호(휴먼시아) |
| 읍/면, 그 밖의 건물 | 강원도 평창군 대화면 가평로 19-1 |
| 동, 공동주택 | 경기도 고양시 덕양구 화중로 164, 512동 1004호(화정동, 은빛마을5단지아파트) |
| 동, 그 밖의 건물 | 서울특별시 구로구 중앙로 5, 3층(고척동) |

- 검색 API는 상세주소를 반환하지 않습니다. **호출하는 쪽이 상세주소 입력란을 직접 만들어야 합니다**(`R`. 페이지가 필수라고 적었습니다). 아파트 호 목록은 `detail-address-api_ko.md`를 참조합니다.
- 상세주소가 있으면 `roadAddrPart1` + `", "` + 상세주소 + `roadAddrPart2`로 조합합니다.
- 상세주소가 없으면 `roadAddr`을 쓰거나 `roadAddrPart1` + `roadAddrPart2`로 조합합니다.
- `D`: `roadAddrPart1`, 상세주소, `roadAddrPart2`, `zipNo`, `bdMgtSn`을 각각 별도의 컬럼에 저장하고, 표시할 때 표시용 문자열을 조합합니다. 나중에 주소 문자열이 바뀌어도 `bdMgtSn`으로 건물을 식별할 수 있습니다.

## 테스트

- 테스트 키 `TESTJUSOGOKR`은 가이드의 샘플 URL에서 동작합니다. 개발할 때는 직접 발급받은 개발승인키를 사용하며, 개발승인키는 만료됩니다(`E0014`).
- **주소 API는 모의 해킹에서 제외합니다**(`R`). 모의 해킹 중에 호출하면 IP가 차단될 수 있다고 가이드가 반복해서 설명합니다. `D`: 자동 취약점 스캔에서도 제외하고, 스캐너는 상위 호출을 스텁으로 대체한 자체 프록시 엔드포인트로 향하게 합니다.
