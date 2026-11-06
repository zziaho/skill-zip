---
name: juso-api
description: Reference for integrating the Korean road name address APIs (도로명주소 API) of business.juso.go.kr (주소기반산업지원서비스, 행정안전부): the road name address search API (addrLinkApi.do), popup and mobile popup APIs (addrLinkUrl.do, addrMobileLinkUrl.do, jusoCallBack), English address API, coordinate API (addrCoordApi.do, entX/entY in UTM-K) and detail address (동/층/호) API. Covers request and output variables corrected against the guides, error codes per API, approval key (승인키, confmKey) rules, keyword limits and IP blocking, paging limits, address composition (roadAddrPart1 + 상세주소 + roadAddrPart2), and fixes for the security problems in the official JSP/PHP/ASP samples (reflected XSS in jusoPopup, exposed keys, unencoded proxy parameters). Use this skill when adding an address search (주소 검색, 우편번호 찾기) to a Korean website or app, when the user mentions juso.go.kr, 도로명주소 API, 주소검색 API, 팝업 API, jusoPopup, jusoCallBack, confmKey, 승인키 or TESTJUSOGOKR, when an address API returns E0001 to E0015 or -999, when the popup result does not reach the page, or when reviewing code copied from the juso samples.
---

# 도로명주소 API (juso.go.kr address APIs)

Reference for calling the address APIs of the 주소기반산업지원서비스 (business.juso.go.kr), run for the Ministry of the Interior and Safety (행정안전부). Verified against the site's API pages as saved on 2026-11-06 and the downloadable guides and samples of the same day (guide PDFs created 2025-12 for the search types and 2026-07 for the popup types, by their PDF creation dates).

**Scope**: 9 APIs: road name address search, popup and mobile popup; English address search and popup; coordinate search and popup; detail address search and popup. The map APIs (지도제공 검색, 팝업) and the downloadable address databases and spatial data are not covered; say so instead of guessing.

The site's terms of use for this material were not checked. This skill summarizes and corrects it rather than copying it.

## How to use

1. Pick the API type with the table below. The type decides the key you apply for
2. Read the reference file for that API, and **always** the rules in this file (keys, blocking, security)
3. When **building**: start from the corrected examples in this skill, not from the official samples
4. When **reviewing** code copied from juso samples: check it against "Problems in the official samples" below and the tables in the reference files

## Conventions

| Strength | Meaning | How to report in a review |
|----------|---------|---------------------------|
| `R` | The sources state it as a rule, or breaking it returns an error code, gets the IP blocked or stops the service | Violation |
| `G` | The sources state it as advice | Recommendation |
| `D` | This skill's judgment: where the sources disagree, are silent, or where the official samples are insecure. The reason is given next to it | Recommendation, and say that it goes beyond the juso guides |

- **The sources contradict each other in many places**: the API pages, the guide PDFs and the downloadable samples differ on field names (`InbrMnnm` for `lnbrMnnm`), required flags, `resultType` meanings, endpoint URLs and error messages. The tables in this skill are corrected; each reference file says what was corrected and on what basis.
- Field names are case-sensitive. The lot-number fields begin with a lowercase L (`lnbr`).

## Quick Lookup

| Task | File to Load |
|------|-------------|
| Address search box with a result list on your own page; paging; keyword rules; building the stored address | `references/search-api.md` |
| "우편번호 찾기" button that opens juso's search window (PC or mobile); `jusoCallBack`; returnUrl page; `useDetailAddr` | `references/popup-api.md` |
| English addresses (`addrEngApi.do`, `addrEngUrl.do`) | `references/english-api.md` |
| X/Y coordinates of an address, UTM-K, converting to latitude and longitude | `references/coordinate-api.md` |
| Dong/floor/unit lists for a building (`addrDetailApi.do`) | `references/detail-address-api.md` |

## Choosing an API type

| Situation | Type | Why |
|-----------|------|-----|
| Most forms that need a postal address | **Popup** (mobile popup for mobile web) | juso provides the search UI, keyword handling, paging and the detail address step. Least code |
| The search must be part of your own screen (inline list, autocomplete, app UI) | **Search**, called from your server | Full control; you build the list, paging and detail address input |
| You also need coordinates | Coordinate popup, or search then coordinate search | `coordinate-api.md` |
| Apartment unit selection | Popup with `useDetailAddr=Y`, or detail address search | `detail-address-api.md` |

## Approval keys (승인키, `confmKey`)

| Rule | Strength |
|------|----------|
| Apply at business.juso.go.kr: 주소정보 자료제공 → 주소정보 API 연계, then 신청하기 on the API in the API 목록. Choose the API (도로명주소, 영문주소, 좌표제공, 상세주소) **and** the type (검색, 팝업, 모바일 팝업) | `R` |
| **One key per system, issued for a URL or IP.** A key works only from the URL or IP it was issued for. Each site or application needs its own key; sharing a key across sites can get the service stopped. For several domains (for example `sub.test.co.kr`, `new.test.co.kr`), attach the 활용시스템 리스트 form to get a key per URL or IP | `R` |
| **Popup keys and search keys are not interchangeable.** Using one for the other returns `E0001` (승인되지 않은 KEY) | `R` |
| Development keys are issued at once without identity verification and **expire** (`E0014`); the guides do not give the period. The regular application requires identity verification | `R` |
| Apply for the regular key before release, so the service does not stop when the development key expires | `D` |
| `TESTJUSOGOKR` is the test key used in the guides' samples | `G` |
| Check and edit applications under 마이페이지 → API 인증키 관리 | `G` |
| Keep search keys in server configuration, not in code or pages; call the search API from your server (`secure-coding` 23) | `D` |
| A popup key is necessarily visible in the page. Its protection is the registered URL or IP: register exact URLs, not broad ones | `D` |

## Rules for every API

| Rule | Strength |
|------|----------|
| Use `https://business.juso.go.kr/addrlink/…`. The search pages allow `http://` for runtimes without TLS 1.2; do not: the key and the user's address travel in clear text (`secure-coding` SR2-8). Government-network (행정망) systems ask the help center (1588-0061) for their URL | `D` |
| **Keywords with SQL reserved words or `<` `>` `=` `%` can get the calling IP blocked** by the service's security equipment, besides returning `E0013`. Clean keywords before calling and show the user a message (`search-api.md`, "Keyword filter") | `R` |
| Check keywords on the server too, and reject them with a message instead of silently editing the input | `D` |
| **Exclude the address APIs from penetration tests (모의 해킹).** The guides warn repeatedly that the tester's IP can be blocked | `R` |
| Exclude them from automated vulnerability scans as well | `D` |
| The coordinate API returns `E0007` for too many calls in a short time; the search API cannot page past 9,000 results (`E0015`) | `R` |
| Do not call any of the APIs in bulk loops; call when an address is entered and store the result | `D` |
| Check `errorCode` before using results; `0` is success. Error codes **differ by API** (`E0005` is "no keyword" in the search API and "`buldMnnm` missing" in the coordinate and detail APIs); map them per API | `D` |
| Store code fields as strings: `zipNo` and `emdNo` have leading zeros, and `bdMgtSn` (25 digits) does not fit in a 64-bit integer | `D` |
| Treat address values coming back from the user's browser (popup callbacks, form fields) as user input: validate and escape them like any other | `D` |

## Problems in the official samples

The JSP, PHP, ASP and Java samples on the site are what most projects copy. They have these problems (`D`; details and fixes in the reference files):

| Problem | Where | Fix | `secure-coding` |
|---------|-------|-----|-----------------|
| Posted values written unescaped into a JavaScript string: `opener.jusoCallBack("<%=roadFullAddr%>", …)` (reflected XSS on the returnUrl page) | Every popup sample: `jusoPopup.jsp`, `.php`, `.asp` | Escape for HTML and read from the DOM, or JSON-encode (`popup-api.md`) | 4 |
| API results joined into HTML and inserted with `.html(...)` | Search, coordinate and detail samples | `textContent`, `.text()`, `new Option()` | 4 |
| The key taken from the browser (`req.getParameter("confmKey")`) or kept in a visible input | Search, coordinate and detail proxy samples | Server configuration | 23 |
| Only the keyword URL-encoded; other parameters concatenated raw; `admCd =` typo; detail sample calls the coordinate URL | Proxy controllers | Encode and validate every parameter | |
| No timeouts; stream not closed on error | Proxy controllers | Timeouts and try-with-resources | 40 |
| Keyword filter removes `OR` inside words (`KOREA` → `KEA`) and misses `[` `]` | `checkSearchedWord` | Whole-word match, reject instead of rewrite | |
| `document.domain`, IE trusted-site and compatibility-view tips | Popup samples and guides | Obsolete; see `popup-api.md` deployment pitfalls | |

## When building

1. Choose the API type and apply for a key for each system URL or IP (development key first)
2. Popup: put the returnUrl page on the same origin as the form, exempt it from CSRF and login filters, and write it with output escaping (`popup-api.md`)
3. Search: add a server endpoint that holds the key, validates the keyword and page, encodes every parameter, sets timeouts and rate limits, and returns JSON (`search-api.md`)
4. Store `roadAddrPart1`, the detail address, `roadAddrPart2`, `zipNo` and `bdMgtSn` separately; build the display string from them
5. Before release: switch to the regular key, and tell the security testers to exclude the juso endpoints

## When reviewing

1. Find the returnUrl page and any `<%= %>`, `<?= ?>` or string concatenation of request values inside `<script>`
2. Find where `confmKey` comes from and whether the search API is called from the browser
3. Check the proxy controller: encoding, validation, timeouts, content type, rate limiting
4. Check the field names against the corrected tables (`lnbrMnnm`, not `InbrMnnm`) and the error handling against the right API's code table
5. Check that keywords are filtered before the call, without breaking English road names

## Related skills

- `secure-coding`: weaknesses 4 (XSS), 23 (hard-coded sensitive information), 40 (resource release), design criteria SR1-5 (web service request and result validation) and SR2-8 (sensitive data in transit)
- `krds`: the address rows in `references/form-patterns.md` (개인 식별 정보 입력): a button that opens the address search, a read-only postal code filled by it, and a separate detail address field. That table is marked there as beyond KRDS (`D`)
- `egovframe`: when the proxy is built on 전자정부 표준프레임워크 and the key is kept in `globals.properties`, encrypt it with the crypto service and keep it out of the repository, as its `references/code-inspection.md` says. `D`: put the upstream call in a service class, not in the controller
