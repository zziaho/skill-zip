# 도로명주소 검색 API (road name address search API)

Keyword search over the national road name address database. The caller sends a keyword and gets a page of matching addresses as XML or JSON. Sources: the API page of business.juso.go.kr (saved 2026-11-06) and the guide PDF "[가이드]검색API_활용_방법" (27 pages, 2025-12). Where they disagree, the table notes which one this skill follows.

`R`, `G` and `D` are defined in `SKILL.md`.

## Endpoints

| Use | URL | Method | Output |
|-----|-----|--------|--------|
| Server-to-server call | `https://business.juso.go.kr/addrlink/addrLinkApi.do` | GET, POST | XML (default) or JSON |
| Direct call from a web page (JSONP) | `https://business.juso.go.kr/addrlink/addrLinkApiJsonp.do` | GET, POST | JSONP wrapping XML or JSON |

- A search key cannot call the popup endpoints, and a popup key cannot call these (`R`, see `SKILL.md`, approval keys).
- Systems inside the government network (행정망) use a different URL; the guide says to ask the help center (1588-0061) for it.
- The page adds "Java 1.6 or later; environments that cannot use TLS 1.2 use `http://`". `D`: use `https://` only. A plain-HTTP call sends the approval key and the user's address keyword in clear text (`secure-coding` SR2-8). Fix the runtime instead of downgrading.

## Request variables

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `confmKey` | String | Y | | Approval key issued for this system |
| `currentPage` | Integer | Y | 1 | Page number, `n > 0` |
| `countPerPage` | Integer | Y | 10 | Rows per page, `0 < n <= 100` |
| `keyword` | String | Y | | Search keyword (rules below) |
| `resultType` | String | N | `xml` | `xml` or `json` |
| `hstryYn` | String | N | `N` | Include changed addresses: with `Y`, a former address still finds the current road name address. Added 2020-12-08 |
| `firstSort` | String | N | `none` | `none` accuracy order; `road` puts results whose road name contains the keyword first; `location` does the same for the lot-number (지번) address. Added 2020-12-08 |
| `addInfoYn` | String | N | `N` | With `Y`, the output adds `hstryYn`, `relJibun` and `hemdNm`. The guide warns that these extra fields may change or be removed later. Added 2020-12-08 |

- The value ranges of `currentPage` and `countPerPage` come from the guide PDF and the sample comments; the page table omits them.
- The keyword may be an administrative-dong (행정동) name as well as a legal-dong (법정동) name.

**Keyword rules** (`R`: each one returns an error code)

| Rule | Error |
|------|-------|
| Not empty | E0005 |
| Not only a province or city name (시도, 시군구) | E0006 |
| At least two characters | E0008 |
| Not digits only; letters and digits together | E0009 |
| At most 40 Korean characters or 80 Latin letters and digits | E0010 |
| No run of more than 10 digits | E0011 |
| Not special characters and digits only | E0012 |
| No SQL reserved words and none of `%` `=` `>` `<` `[` `]` | E0013 |

Keywords with SQL reserved words or special characters can also get the **caller's IP blocked** by the service's security equipment, not only an error code. See "Keyword filter" below and `SKILL.md`.

## Output

Results come in `results`, with one `common` block and a list of `juso` entries (a JSON array, repeated XML elements). In JSON every value is a string.

**common**

| Name | Description |
|------|-------------|
| `totalCount` | Total number of matches |
| `currentPage` | Page number |
| `countPerPage` | Rows per page |
| `errorCode` | `0` on success, otherwise a code from the table below |
| `errorMessage` | Message for the code |

**juso**

| Name | Required | Description |
|------|----------|-------------|
| `roadAddr` | Y | Full road name address, with the reference part |
| `roadAddrPart1` | Y | Road name address without the reference part |
| `roadAddrPart2` | N | Reference part, for example `(상암동)` |
| `jibunAddr` | Y | Lot-number (지번) address |
| `engAddr` | Y | Road name address in English |
| `zipNo` | Y | Postal code |
| `admCd` | Y | Administrative district code (10 digits) |
| `rnMgtSn` | Y | Road name code (12 digits) |
| `bdMgtSn` | Y | Building management number (건물관리번호) |
| `detBdNmList` | N | Detailed building names (for example apartment block names) |
| `bdNm` | N | Building name |
| `bdKdcd` | Y | Multi-unit housing: `1` yes, `0` no |
| `siNm` | Y | Province or metropolitan city |
| `sggNm` | Y | City, county or district |
| `emdNm` | Y | Eup, myeon or dong |
| `liNm` | N | Legal ri name |
| `rn` | Y | Road name |
| `udrtYn` | Y | Underground: `0` above ground, `1` underground |
| `buldMnnm` | Y | Building main number |
| `buldSlno` | Y | Building sub number, `0` if none |
| `mtYn` | Y | Mountain lot (산): `0` no, `1` yes |
| `lnbrMnnm` | Y | Lot main number (번지) |
| `lnbrSlno` | Y | Lot sub number (호), `0` if none |
| `emdNo` | Y | Eup/myeon/dong serial number |
| `hstryYn` | | With `addInfoYn=Y`: `0` current address, `1` found through a changed (former) address |
| `relJibun` | | With `addInfoYn=Y`: related lot numbers |
| `hemdNm` | | With `addInfoYn=Y`: the administrative dong office (관할주민센터). Reference only; it may differ from reality |

- **The page's output table has errors** (`D`: corrected above from the guide PDF table, its sample responses and the sample source code, which agree with each other): `currentPerPage` for `currentPage`, `InbrMnnm` (capital I) for `lnbrMnnm`, the `emdNo` row missing, and the description of `emdNo` moved up to `lnbrSlno`. Use the lowercase `l` names; `lnbr` is short for lot number.
- The page and the PDF disagree on whether `sggNm`, `liNm`, `relJibun` and `hemdNm` are required. `D`: treat `liNm` as optional (the samples return it empty) and all address parts as possibly empty when you store them.
- `D`: store code values as strings, not numbers: `zipNo` and `emdNo` have leading zeros (`03923`, `03`), and `bdMgtSn` (25 digits) does not fit in a 64-bit integer.

## Error codes

| Code | Message (summary) | Action |
|------|-------------------|--------|
| `0` | 정상 | |
| `-999` | 시스템에러 | Contact the help center |
| `E0001` | 승인되지 않은 KEY | Wrong key, or a popup key used for search (or the reverse) |
| `E0005` | 검색어가 입력되지 않았습니다 | Enter a keyword |
| `E0006` | 주소를 상세히 입력해 주시기 바랍니다 | A province name alone cannot be searched |
| `E0008` | 검색어는 두글자 이상 입력되어야 합니다 | One character cannot be searched |
| `E0009` | 검색어는 문자와 숫자 같이 입력되어야 합니다 | Digits alone cannot be searched |
| `E0010` | 검색어가 너무 깁니다 | 40 Korean or 80 Latin/digit characters at most |
| `E0011` | 검색어에 너무 긴 숫자가 포함되어 있습니다 | 10 digits at most |
| `E0012` | 특수문자+숫자만으로는 검색이 불가능 합니다 | |
| `E0013` | SQL 예약어 또는 특수문자( %,=,>,<,[,] )는 검색이 불가능 합니다 | Remove them and search again |
| `E0014` | 개발승인키 기간이 만료되어 서비스를 이용하실 수 없습니다 | Issue a new development key |
| `E0015` | 검색 범위를 초과하였습니다 | More than 9,000 results cannot be paged through |

- The guide PDF also lists `E0002` (승인되지 않은 사이트: the calling URL or IP does not match the key) and `E0003` (정상적인 경로로 접속하시기 바랍니다), and says "한글자 이상" for `E0008`. The page (saved 2026-11-06; the PDF was created 2025-12) says "두글자 이상", and its action column agrees. `D`: follow the page, and handle `E0002` and `E0003` as well in case the server still returns them.
- The page's action for `E0001` reads "(검색API 승인키 사용불가)", the same words as on the popup page. Read it as "keys of the other API type are not accepted".
- Check `errorCode` before reading `juso`. A `0` with `totalCount` 0 is a normal empty result; the guide says that a search that should match but returns 0 is usually a keyword encoding problem.
- **The codes `E0002` to `E0007` mean different things in the coordinate and detail address APIs.** Do not share one error-code map across APIs (`D`).

## Calling patterns

| Pattern | Flow | Use when |
|---------|------|----------|
| Server proxy (가이드 "일반적인 API 이용방법") | Browser → your server → juso → your server → browser | `D`: the default. The key stays on the server, the server can validate and limit calls, and the response can be checked before it reaches the page |
| JSONP from the page (가이드 "웹 페이지에서 직접 API 이용방법") | Browser → juso (JSONP) | Only for static pages with no server side. The key and the keyword travel in the page's URL, and the page trusts a third-party script response |

**What the official samples get wrong** (`D`, check for these when reviewing code copied from them)

| Sample code | Problem | Use instead |
|-------------|---------|-------------|
| The controller takes `confmKey` from the request (`req.getParameter("confmKey")`); the page holds it in a hidden `<input>` | The key is public and any caller can supply any key | Keep the key in server configuration (`secure-coding` 23) |
| Only `keyword` is URL-encoded; `currentPage`, `countPerPage`, `resultType` and the key are concatenated raw | A value with `&` or `#` changes the upstream query | Encode every parameter, and validate `currentPage`, `countPerPage` as integers in range and `resultType` against `xml`/`json` |
| The keyword filter exists only in the page's JavaScript | Calls straight to the controller skip it | Validate on the server |
| `url.openStream()` without timeouts; `br.close()` not in `finally` | A slow upstream ties up request threads; streams leak on errors | Set connect and read timeouts; use try-with-resources (`secure-coding` 40) |
| Results are joined into an HTML string and inserted with `$("#list").html(...)` | Building names and other values are inserted as HTML (`secure-coding` 4) | Set text with `textContent` or `.text()`, or escape |
| A JSON response is returned with `Content-Type: text/xml` | Wrong type | `application/json;charset=UTF-8` |
| jQuery 1.8.3 | Old library with known issues | Use the project's current library |

**Server proxy (Java, Spring MVC)**

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

- Add the project's usual protections to the proxy endpoint: rate limiting per session or IP, and CSRF protection if it uses POST. Repeated calls can get **your server's** IP blocked, not the attacker's (`D`).
- Parsing the response and returning only the needed fields keeps unexpected upstream content out of the page.

## Keyword filter

The guide asks callers to remove SQL reserved words (`or`, `select`, `insert`, `delete`, `update`, `create`, `drop`, `exec`, `union`, `fetch`, `declare`, `truncate`) and the characters `<` `>` `=` `%` before calling, with a message to the user, because the service's security equipment treats them as SQL injection and **may block the calling IP** (`R`). Its block examples are patterns such as `' or '1'='1`, `' and 'f'='f`, `%27+and+` and `UNION+SELECT`.

- This filter protects the **service and your IP**, not your system. It is not an input validation control for your own queries (`D`).
- The sample `checkSearchedWord` removes each reserved word as a substring, case-insensitively: it turns `KOREA` into `KEA` and `ORANGE` into `ANGE`, and English road names break. It also misses `[` and `]`, which `E0013` rejects. `D`: reject rather than silently rewrite, match reserved words as whole words, and include the brackets. The sample's own comment says it removes reserved words "앞뒤공백포함" (with the spaces around them), so whole-word matching is what it meant:

```javascript
const BLOCKED_CHARS = /[%=<>\[\]]/;
const BLOCKED_WORDS = /\b(or|select|insert|delete|update|create|drop|exec|union|fetch|declare|truncate)\b/i;

function isAllowedKeyword(k) {
  return k.trim().length >= 2 && !BLOCKED_CHARS.test(k) && !BLOCKED_WORDS.test(k);
}
```

Apply the same check on the server, with the length limits of `E0010`:

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

Show the user a message such as "주소 검색어에 특수문자(%, =, <, >, [, ])나 SQL 예약어는 사용할 수 없습니다" instead of changing the input.

## Paging

- At most 9,000 results can be paged through: page 900 at 10 rows (`E0015`, `R`). Ask the user to narrow the keyword instead of paging further.
- `countPerPage` is at most 100.
- The page's paging sample uses the rows-per-page value as the number of page links and moves back by a fixed 5 (`prePage = firstPage-5`). `D`: use a separate page-block size and move back by that size.

## Building the address to store and show

The page gives the display order: 시/도 + 시/군/구 + 읍/면 + 도로명 + 건물번호(본번-부번) + 상세주소(동/층/호) + (참고항목). The reference part holds the legal dong and the apartment complex name; for 읍/면 addresses it holds only the complex name.

| Case | Example |
|------|---------|
| 읍/면, multi-unit housing | 경기도 가평군 가평읍 가화로 164, 201동 102호(휴먼시아) |
| 읍/면, other building | 강원도 평창군 대화면 가평로 19-1 |
| 동, multi-unit housing | 경기도 고양시 덕양구 화중로 164, 512동 1004호(화정동, 은빛마을5단지아파트) |
| 동, other building | 서울특별시 구로구 중앙로 5, 3층(고척동) |

- The search API returns no detail address. **The caller must build the detail address input itself** (`R`, the page says 필수). For apartment unit lists, see `detail-address-api.md`.
- With a detail address: `roadAddrPart1` + `", "` + detail address + `roadAddrPart2`.
- Without one: `roadAddr`, or `roadAddrPart1` + `roadAddrPart2`.
- `D`: store `roadAddrPart1`, the detail address, `roadAddrPart2`, `zipNo` and `bdMgtSn` in separate columns, and build the display string when showing it. `bdMgtSn` identifies the building if the address text changes later.

## Testing

- The test key `TESTJUSOGOKR` works in the guide's sample URLs. Use your own development key for development; development keys expire (`E0014`).
- **Exclude the address APIs from penetration tests** (`R`). The guide repeats that calling them during a 모의 해킹 test can get the IP blocked. `D`: exclude them from automated vulnerability scans too, and point scanners at your proxy endpoint with the upstream call stubbed out.
