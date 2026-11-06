# 영문주소 API (English address search and popup)

Returns road name and lot-number addresses in English. The keyword may be Korean or English. Sources: the API pages for 영문주소 검색 API and 영문주소 팝업 API (saved 2026-11-06), the guide PDFs "[가이드]영문주소_검색API_활용_방법" (25 pages, 2025-12) and "[가이드]영문주소_팝업API_활용_방법" (19 pages, 2026-07), and the samples.

Everything not listed here works as in `search-api.md` (search) and `popup-api.md` (popup). `R`, `G` and `D` are defined in `SKILL.md`.

## Search API

| Use | URL |
|-----|-----|
| Server-to-server | `https://business.juso.go.kr/addrlink/addrEngApi.do` |
| JSONP | `https://business.juso.go.kr/addrlink/addrEngApiJsonp.do` |

**Request variables**: `confmKey`, `currentPage`, `countPerPage`, `keyword`, `resultType`, with the same meaning and limits as the road name address search. There is no `hstryYn`, `firstSort` or `addInfoYn`.

**Output**: `common` is the same as the road name address search (the page writes `currentPerPage`; the field is `currentPage`). Each `juso` entry has:

| Name | Description |
|------|-------------|
| `roadAddr` | Road name address in English, for example `6 Gangnam-daero 12-gil, Seocho-gu, Seoul` |
| `jibunAddr` | Lot-number address in English, for example `326-1 Yangjae-dong, Seocho-gu, Seoul` |
| `zipNo` | Postal code |
| `admCd`, `rnMgtSn`, `udrtYn`, `buldMnnm`, `buldSlno` | Codes for the coordinate and detail address APIs |
| `bdKdcd` | Multi-unit housing: `1` yes, `0` no |
| `siNm`, `sggNm`, `emdNm`, `liNm`, `rn` | Province, city/district, eup/myeon/dong, ri and road name in English |
| `mtYn`, `lnbrMnnm`, `lnbrSlno` | Mountain lot flag and lot numbers |
| `korAddr` | Road name address in Korean |

- There is no `roadAddrPart1`, `roadAddrPart2`, `engAddr`, `bdMgtSn`, `bdNm` or `detBdNmList`. If you need the building management number or the Korean reference part, call the road name address search as well, or use its `engAddr` field instead of this API (`D`).
- The page says `korAddr` is a Number; it is a string (the PDF table and the sample response agree). The sample JSON response has no `rn` although the XML one does. `D`: read every field defensively.

**Error codes**: the same codes and actions as the road name address search, but the messages from `E0005` on are English, for example `E0005` "No search word has been entered.", `E0008` "Address entered too short.", `E0013` "Can not search SQL & special characters(%,=,>,<,[,]).", `E0015` "The search range has been exceeded.". `E0001` is still in Korean. Map codes, not message text (`D`).

**Writing the English address with a detail address**: the API page repeats the Korean display rules and the `roadAddrPart1` + detail + `roadAddrPart2` formula from the Korean search page, but this API has no such fields; no English composition rule is given. `D`: put the detail address before the returned address, as in `101-dong 1004-ho, 6 Gangnam-daero 12-gil, Seocho-gu, Seoul`, and keep the user's detail address in its own field as for Korean addresses. The search API still returns no detail address; the caller must build that input (`R`, as in `search-api.md`).

## Popup API

| Use | URL |
|-----|-----|
| PC popup | `https://business.juso.go.kr/addrlink/addrEngUrl.do` |

- No mobile URL and no `useDetailAddr` are documented for the English popup.
- Request variables: `confmKey`, `returnUrl`, `resultType` (`1` road name, `2` road name and lot number; the samples send `2`), and `encodingType=EUC-KR` for EUC-KR systems.
- Output and callback: 20 values. The callback order differs from the output table: `addrDetail` comes third.

```
jusoCallBack(roadFullAddr, roadAddr, addrDetail, jibunAddr, zipNo, admCd, rnMgtSn, bdKdcd,
             siNm, sggNm, emdNm, liNm, rn, udrtYn, buldMnnm, buldSlno, mtYn, lnbrMnnm, lnbrSlno, korAddr)
```

  `roadFullAddr` is the full English road name address; `roadAddr` is the English road name address; `korAddr` is the Korean one.
- The returnUrl-page message for a missing `returnUrl` is "Please connect us with a normal route.".
- The guide's JSP, ASP and PHP returnUrl examples declare only some of the variables ("필요한 항목 추가 기술") but pass all 20, and its ASP and PHP input-page examples call the callback with 19 values (no `korAddr`) on load. Use the downloadable samples, corrected as below.

**Security**: the English popup samples have the same reflected XSS as the Korean ones: `jusoPopup.jsp` writes `"<%=roadFullAddr%>"` and the other 19 values into a script, and the PHP and ASP versions do the same. Use the safe returnUrl page from `popup-api.md` with the field list above, and the action URL `addrEngUrl.do`. The deployment pitfalls there (CSRF filter, `SameSite` cookies, opener checks) apply as well.
