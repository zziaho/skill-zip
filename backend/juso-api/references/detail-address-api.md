# 상세주소 API (detail address: dong, floor and unit)

Returns the registered dong (building block), floor and unit (호) names of one building, so the user can choose a unit instead of typing it. Sources: the API page for 상세주소 검색 API (saved 2026-11-06), the guide PDF "[가이드]상세주소검색API_활용_방법" (24 pages, 2025-12) and the samples. The popup form of this feature is the `useDetailAddr=Y` option in `popup-api.md`.

`R`, `G` and `D` are defined in `SKILL.md`.

## Endpoints

| Use | URL |
|-----|-----|
| Server-to-server | `https://business.juso.go.kr/addrlink/addrDetailApi.do` |
| JSONP | `https://business.juso.go.kr/addrlink/addrDetailApiJsonp.do` |

- The downloadable samples call `www.juso.go.kr`, and their Java controllers call the **coordinate** endpoint `addrCoordApi.do`. The page and the guide use the URLs above; do not copy the sample URLs (`D`).

## Request variables

| Name | Required | Default | Description |
|------|----------|---------|-------------|
| `confmKey` | Y | | Approval key issued for this API |
| `admCd` | Y | | Administrative district code (10 digits), from a search result |
| `rnMgtSn` | Y | | Road name code (12 digits) |
| `udrtYn` | Y | | `0` above ground, `1` underground |
| `buldMnnm` | Y | | Building main number |
| `buldSlno` | Y | | Building sub number, `0` if none |
| `searchType` | N | `dong` | `dong`: list the dongs; `floorho`: list floors and units |
| `dongNm` | N | | The dong to list floors and units for (with `searchType=floorho`) |
| `resultType` | N | `xml` | `xml` or `json` |

- Take `admCd`, `rnMgtSn`, `udrtYn`, `buldMnnm` and `buldSlno` from the road name address search, English search or coordinate API result for the address the user picked.
- The API list on the site offers this API as its own entry to apply for. Which key types it accepts is not stated: its error table says "(팝업API 승인키 사용불가)", while the search pages say "(검색API 승인키 사용불가)". `D`: apply for a key for this API.

## Two-step flow

```
1. searchType=dong            → list of dongNm      (fill the "동" select)
2. searchType=floorho&dongNm=… → list of floorNm, hoNm (fill the "층/호" select)
```

- There are only two steps; floors and units come together in step 2.
- If step 1 returns no dongs, the sample shows the option "동 표기 없음". The sources do not say how to query floors and units for a building with no dong. `D`: try step 2 with `dongNm` empty, and always let the user type the detail address by hand, since many buildings have no registered units.
- The guide's sample response does not say which step it answers; it contains `dongNm`, `floorNm` and `hoNm` together and shows `totalCount` 1 with several entries. Do not rely on either (`D`).
- The sample comments say the test key `TESTJUSOGOKR` returns only fixed test values for this API (`G`). Use a development key to check real buildings.

## Output

| Group | Name | Description |
|-------|------|-------------|
| common | `totalCount`, `errorCode`, `errorMessage` | As in the search API |
| juso | `admCd`, `rnMgtSn`, `udrtYn`, `buldMnnm`, `buldSlno` | Echo of the building codes |
| juso | `bdMgtSn` | Building management number (in the PDF table and the sample response; missing from the page table) |
| juso | `dongNm` | Dong name, for example `가동`, `101동` |
| juso | `floorNm` | Floor name |
| juso | `hoNm` | Unit name |

Build the detail address from the chosen values, for example `101동 1004호`, and insert it as described in `search-api.md` ("Building the address to store and show").

## Error codes

| Code | Meaning |
|------|---------|
| `0` | 정상 |
| `-999` | 시스템에러 |
| `E0001` | 승인되지 않은 KEY |
| `E0002` | `admCd` missing |
| `E0003` | `rnMgtSn` missing |
| `E0004` | `udrtYn` missing |
| `E0005` | `buldMnnm` missing |
| `E0006` | `buldSlno` missing |

Same numbering as the coordinate search (without `E0007`), different from the road name address search.

## Samples

| Sample code | Problem | Use instead (`D`) |
|-------------|---------|-------------------|
| Controller encodes only `dongNm`, and calls `URLEncoder.encode` on it even when the parameter is absent | Raw values change the query; a request without `dongNm` throws | Encode every parameter; skip `dongNm` when empty |
| Key from a visible `<input>` and `req.getParameter("confmKey")` | Public key | Server configuration (`secure-coding` 23) |
| `"<option value='"+dongNm+"'>"+dongNm+"</option>"` and `.html(htmlStr)` | Values inserted as HTML | `new Option(text, value)` or `textContent` |
| JSON returned as `text/xml` | Wrong type | `application/json` |

```javascript
function fillSelect(select, values) {
  select.length = 0;
  values.forEach(function (v) { select.add(new Option(v, v)); });   // no HTML parsing
}
```

- The guide's block-pattern section repeats the keyword filtering advice, but this API has no keyword.
