# 좌표제공 API (coordinate search and popup)

Returns the X and Y coordinates of a building. The search type takes a building's codes, not a keyword; the popup type returns the address and its coordinates together. Sources: the API pages for 좌표제공 검색 API and 좌표제공 팝업 API (saved 2026-11-06), the guide PDFs "[가이드]좌표검색API_활용_방법" (23 pages, 2025-12) and "[가이드]좌표팝업API_활용_방법" (21 pages, 2026-07), and the samples.

`R`, `G` and `D` are defined in `SKILL.md`.

## Coordinate system

The popup guide states: "X,Y 좌표는 GRS80 UTM-K 기준입니다. 위도, 경도 등 변경이 필요하시면 별도의 변환작업을 하셔야 합니다." That sentence is the only statement about the coordinate system in the sources.

- `D`: UTM-K on GRS80 is EPSG:5179 (general knowledge, not stated by the sources). The sample values (`entX` 945959.04, `entY` 1953851.73 for a building in Mapo-gu, Seoul) fit it. Treat the search API's coordinates as the same system; its guide does not say.
- To show the point on a web map, convert to WGS84 (EPSG:4326) with a projection library, for example `proj4js` in the browser or `proj4j`/GeoTools on a Java server, using the EPSG:5179 definition. Map providers that accept UTM-K directly need no conversion.
- The sources do not say which point of the building the coordinates mark (centroid or entrance). Do not present them as an entrance location (`D`).

## Search API

| Use | URL |
|-----|-----|
| Server-to-server | `https://business.juso.go.kr/addrlink/addrCoordApi.do` |
| JSONP | `https://business.juso.go.kr/addrlink/addrCoordApiJsonp.do` |

**Request variables**: copy these from a road name address search result (or the English search, or the address database). The names are the same.

| Name | Required | Description |
|------|----------|-------------|
| `confmKey` | Y | Approval key for the coordinate API (search type) |
| `admCd` | Y | Administrative district code, 10 digits |
| `rnMgtSn` | Y | Road name code, 12 digits |
| `udrtYn` | Y | `0` above ground, `1` underground |
| `buldMnnm` | Y | Building main number |
| `buldSlno` | Y | Building sub number. The page marks it optional, but the PDF marks it required and `E0006` is returned when it is missing; send `0` when there is none (`D`) |
| `resultType` | N | `xml` (default) or `json` |

There is no `keyword`, `currentPage` or `countPerPage`. One request returns one building.

**Output**

| Group | Name | Description |
|-------|------|-------------|
| common | `totalCount`, `errorCode`, `errorMessage` | As in the road name address search |
| juso | `admCd`, `rnMgtSn`, `bdMgtSn`, `udrtYn`, `buldMnnm`, `buldSlno` | The building's codes |
| juso | `entX` | X coordinate (UTM-K, see above) |
| juso | `entY` | Y coordinate |
| juso | `bdNm` | Building name (optional) |

- The coordinates are decimal strings. The sources do not say what comes back for a building without coordinates; handle an empty value (`D`).

**Error codes**: the numbers mean something different from the road name address search.

| Code | Meaning |
|------|---------|
| `0` | 정상 |
| `-999` | 시스템에러 |
| `E0001` | 승인되지 않은 KEY (wrong key or key type) |
| `E0002` | `admCd` missing |
| `E0003` | `rnMgtSn` missing |
| `E0004` | `udrtYn` missing |
| `E0005` | `buldMnnm` missing |
| `E0006` | `buldSlno` missing |
| `E0007` | Too many requests in a short time (짧은 시간동안 다량의 주소검색 요청). The action is "비정상적인 연속된 호출을 삼가하세요" |

- `E0007` means the service is limiting your calls. `D`: do not batch-geocode a whole table through this API in a loop. Call it when an address is saved, cache the result with the address, and back off on `E0007`. For bulk work, use the address and spatial data the service provides for download.
- The coordinate search page shows the keyword filter and paging examples copied from the road name address search page. This API has neither a keyword nor paging, so they do not apply.

**Samples**: the controller samples build the query with `"...addrCoordApi.do?admCd ="+admCd+...` (note the space before `=`), encode nothing although they import `URLEncoder`, and take the key from the request. Use the server proxy pattern in `search-api.md`, with the five codes validated as digits (`admCd` 10, `rnMgtSn` 12, `udrtYn` 0 or 1) before they are sent.

## Popup API

| Use | URL |
|-----|-----|
| PC popup | `https://business.juso.go.kr/addrlink/addrCoordUrl.do` |

- The flow, request variables (`confmKey`, `returnUrl`, `resultType`, `useDetailAddr`, `encodingType`) and error messages are those of the road name address popup (`popup-api.md`).
- The output adds `entX` and `entY`: the callback receives 27 values, the 25 of the road name address popup followed by `entX`, `entY`.
- The guide PDF's code examples submit to `addrLinkUrl.do` and handle only 10 values. The API page, the PDF's own table and the downloadable samples use `addrCoordUrl.do` and 27 values; follow them (`D`).
- The coordinate popup samples have the same reflected XSS as the other popups. Use the safe returnUrl page from `popup-api.md`, add `entX` and `entY` to the field list, and submit to `addrCoordUrl.do`.

## Choosing search or popup

| Need | Use |
|------|-----|
| The user picks an address in a form and you also want its coordinates | Coordinate popup: one step |
| You already use the search API, or have stored addresses with their codes | Coordinate search with the stored `admCd`, `rnMgtSn`, `udrtYn`, `buldMnnm`, `buldSlno` |
| A map on the page | The map APIs are not covered by this skill |
