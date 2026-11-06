# 팝업 API (popup, mobile popup and detail address popup)

The juso service shows its own address search screen in a popup window and posts the chosen address back to a page on the caller's site. Sources: the API pages of business.juso.go.kr for 팝업 API, 모바일 팝업 API and 상세주소 팝업 API (saved 2026-11-06), the guide PDFs "[가이드]팝업API_활용_방법" and "[가이드]모바일팝업API_활용_방법" (27 pages each, 2026-07), and the JSP, PHP and ASP sample sources. The coordinate popup (`coordinate-api.md`) and the English popup (`english-api.md`) work the same way.

`R`, `G` and `D` are defined in `SKILL.md`.

## Endpoints

| Use | URL | Method | Output |
|-----|-----|--------|--------|
| PC popup | `https://business.juso.go.kr/addrlink/addrLinkUrl.do` | POST (GET accepted) | Form parameters posted to `returnUrl` |
| Mobile popup | `https://business.juso.go.kr/addrlink/addrMobileLinkUrl.do` | POST (GET accepted) | Same |

- The popup needs a key issued for the **popup** type, or the **mobile popup** type for the mobile URL. A search key does not work (`R`).
- The mobile popup (added 2017-05) has the same variables and flow; only the URL and the window size differ. The samples switch between the two by commenting out one URL; there is no automatic detection.
- Systems inside the government network (행정망) ask the help center (1588-0061) for a different URL.

## Flow

```
your form page ──window.open──▶ your returnUrl page (first load)
                                   │ auto-submits a form with confmKey, returnUrl, resultType
                                   ▼
                                juso search screen (user searches, picks, enters the detail address)
                                   │ POSTs the result to returnUrl, with inputYn=Y
                                   ▼
                                your returnUrl page (second load)
                                   │ opener.jusoCallBack(...); window.close()
                                   ▼
your form page fills its fields
```

- The samples use one page for both loads (`jusoPopup.jsp`, `.php`, `.asp`) and tell them apart with `inputYn`: not `Y` on the first load, `Y` when juso posts the result. The tables do not document `inputYn`; this reading comes from the sample code.
- `returnUrl` is the returnUrl page's own address (`location.href` in the samples). `D`: keep it on the URL or IP the key was issued for; the sources say only that keys are issued per URL or IP.
- PC window: `width=570,height=420, scrollbars=yes, resizable=yes`. Mobile: no size.

## Request variables

Sent by the returnUrl page's auto-submitted form.

| Name | Required | Description |
|------|----------|-------------|
| `confmKey` | Y | Approval key for the popup type |
| `returnUrl` | Y | URL that receives the result. Missing → "정상적인 경로로 접속하시기 바랍니다" |
| `resultType` | N | What the result list shows, `1` to `4` (see below). The samples always send `4` |
| `useDetailAddr` | N | `Y`: offer dong/floor/unit choices (detail address popup). `N` or absent: the user types the detail address |
| `encodingType` | N | `EUC-KR` only when the receiving system uses EUC-KR; the default is UTF-8. Not in the page's table; it appears in the samples and the guide |

**`resultType`**: the sources disagree on the meaning of 2 to 4 (`D`: both readings agree that `4` shows the most, so use `4` unless a smaller list is wanted).

| Value | The API page | The guide PDF and the downloadable samples |
|-------|--------------|--------------------------------------------|
| 1 | 도로명 | 도로명 |
| 2 | 도로명+지번 | 도로명+지번+상세보기(관련지번, 관할주민센터) |
| 3 | 도로명+상세 건물명 | 도로명+상세보기(상세건물명) |
| 4 | 도로명+지번+상세 건물명 | 도로명+지번+상세보기(관련지번, 관할주민센터, 상세건물명) |

## Output

juso posts these parameters to `returnUrl`, and the samples pass them on to `jusoCallBack` on the opener page. Fields with the same name mean the same as in `search-api.md`; the popup adds `roadFullAddr` and `addrDetail`.

**`jusoCallBack` argument order** (positional; it differs from the order of the page's output table):

| # | Name | # | Name | # | Name |
|---|------|---|------|---|------|
| 1 | `roadFullAddr` (full address with detail address) | 10 | `bdMgtSn` | 19 | `udrtYn` |
| 2 | `roadAddrPart1` | 11 | `detBdNmList` | 20 | `buldMnnm` |
| 3 | `addrDetail` (detail address the user entered) | 12 | `bdNm` | 21 | `buldSlno` |
| 4 | `roadAddrPart2` | 13 | `bdKdcd` | 22 | `mtYn` |
| 5 | `engAddr` | 14 | `siNm` | 23 | `lnbrMnnm` |
| 6 | `jibunAddr` | 15 | `sggNm` | 24 | `lnbrSlno` |
| 7 | `zipNo` | 16 | `emdNm` | 25 | `emdNo` |
| 8 | `admCd` | 17 | `liNm` | | |
| 9 | `rnMgtSn` | 18 | `rn` | | |

- The page's output table writes `InbrMnnm` and `InbrSlno` (capital I), and the mobile page writes `liNM`. The samples and the guide use `lnbrMnnm`, `lnbrSlno` and `liNm`; use those (`D`).
- The coordinate popup adds `entX` and `entY` as arguments 26 and 27.
- The guide's PHP example declares the callback with 10 arguments; the downloadable samples use 25. Use 25.
- Passing an object instead of 25 positional arguments is safer when you write your own returnUrl page (`D`, example below).

## Error messages

The popup shows errors on the juso screen; the page lists messages without codes. They are the search API's messages (`search-api.md`), plus:

| Message | Cause |
|---------|-------|
| 승인되지 않은 KEY 입니다 (guide: "승인키가 일치하지 않습니다") | Wrong key, or a search key used for the popup |
| 정상적인 경로로 접속하시기 바랍니다 | `returnUrl` missing (the page writes it `reurnUrl`) |

## Detail address popup (상세주소 팝업)

- Apply for the 도로명주소 or 좌표제공 API with the popup or mobile popup type, use that API's samples, and add one hidden field to the returnUrl page's form (`R` for the feature to work):

```html
<input type="hidden" name="useDetailAddr" value="Y">
```

- The popup then offers dong, floor and unit choices: from the building register (건축물대장) for multi-unit housing, and from the registered road name address data for multi-household houses (다가구).
- The sources do not say how the choice appears in the output. `D`: read it from `addrDetail` and `roadFullAddr`, and let the user edit it, since not every building has registered units.

## The samples' security problems

The official returnUrl pages write the posted values straight into JavaScript string literals:

```jsp
opener.jusoCallBack("<%=roadFullAddr%>","<%=roadAddrPart1%>","<%=addrDetail%>", ...);   // JSP
opener.jusoCallBack("<?=$ADDR[roadFullAddr]?>", ...);                                   // PHP
```

The returnUrl page accepts a POST from anywhere, and the JSP sample reads values with `request.getParameter`, which also reads the query string: a plain link such as `jusoPopup.jsp?inputYn=Y&roadFullAddr=…` is enough. The first-load line `var inputYn= "<%=inputYn%>";` is reflected the same way. A value containing `"` or `</script>` ends the string and runs script on your origin: reflected XSS (`D` by the juso sources, which do not mention it; weakness 4 under `secure-coding`). `addrDetail` is free text typed by the user, so even normal use can break the page. The ASP and PHP samples read only POST data (`Request.Form`, `$_POST`).

| Sample code | Problem | Use instead (`D`) |
|-------------|---------|-------------------|
| `"<%=value%>"` in a script | XSS | Write values into HTML with HTML escaping (`<c:out>`, `htmlspecialchars`, `Server.HTMLEncode`) and read them from the DOM, or serialize them with a JSON encoder that escapes `<` |
| `var confmKey = "…"` in the page | The key is visible to anyone | Unavoidable for the popup: juso receives it from the browser. Keep the key's registered URL or IP exact, and use a separate key per system |
| `opener.jusoCallBack(...)` with no checks | Throws if the opener is gone | Check `window.opener` and that it is not closed |
| The opener copies values into the form | The user can send any value, with or without the popup | Validate the submitted address on the server like any other input: lengths, `zipNo` as 5 digits, code fields as digits |
| PHP `<?` blocks and `<?=$ADDR[roadFullAddr]?>` | `<?` blocks do not run when `short_open_tag` is off; unquoted array keys are a fatal error in PHP 8 | In a hidden input's `value` attribute (as in the JSP below): `<?php echo htmlspecialchars($_POST['roadFullAddr'] ?? '', ENT_QUOTES, 'UTF-8'); ?>`. Not inside a script string |

**Safe returnUrl page (JSP)**

```jsp
<%@ page contentType="text/html; charset=UTF-8" pageEncoding="UTF-8" session="false" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<% request.setCharacterEncoding("UTF-8"); %>
<!DOCTYPE html>
<html lang="ko">
<head><meta charset="UTF-8"><title>주소 검색</title></head>
<body>
<c:choose>
  <c:when test="${param.inputYn ne 'Y'}">
    <form id="jusoForm" method="post" action="https://business.juso.go.kr/addrlink/addrLinkUrl.do">
      <input type="hidden" name="confmKey" value="<c:out value='${jusoPopupKey}'/>">
      <input type="hidden" name="returnUrl" value="">
      <input type="hidden" name="resultType" value="4">
    </form>
    <script>
      var f = document.getElementById('jusoForm');
      f.returnUrl.value = location.href.split('?')[0];
      f.submit();
    </script>
  </c:when>
  <c:otherwise>
    <form id="result">
      <c:forEach var="n" items="roadFullAddr,roadAddrPart1,addrDetail,roadAddrPart2,engAddr,jibunAddr,zipNo,admCd,rnMgtSn,bdMgtSn,detBdNmList,bdNm,bdKdcd,siNm,sggNm,emdNm,liNm,rn,udrtYn,buldMnnm,buldSlno,mtYn,lnbrMnnm,lnbrSlno,emdNo">
        <input type="hidden" name="${n}" value="<c:out value='${param[n]}'/>">
      </c:forEach>
    </form>
    <script>
      var data = {};
      Array.prototype.forEach.call(document.getElementById('result').elements, function (el) {
        data[el.name] = el.value;
      });
      if (window.opener && !window.opener.closed && typeof window.opener.jusoCallBack === 'function') {
        window.opener.jusoCallBack(data);   // one object instead of 25 positional arguments
      }
      window.close();
    </script>
  </c:otherwise>
</c:choose>
</body>
</html>
```

- `jusoPopupKey` is a request attribute set from server configuration, so the key is not in the source tree (`secure-coding` 23). It still reaches the browser.
- The calling page's `jusoCallBack(data)` reads `data.roadAddrPart1` and so on, and sets them with `.value` or `textContent`, never `innerHTML`.

## Deployment pitfalls (`D`)

The returnUrl page receives a **cross-site POST from business.juso.go.kr**:

| Setting | Effect | Fix |
|---------|--------|-----|
| CSRF filter (Spring Security and similar) | juso's POST has no token and is rejected (403) | Exempt the returnUrl path only. The page changes no state, so the exemption is safe |
| Login or session check on the returnUrl path | Session cookies with `SameSite=Lax` (Chromium's default) are not sent on a cross-site POST, so the page redirects to login | Make the returnUrl page public; it only relays values to the opener |
| The returnUrl page creates a session (JSP default) | The cross-site POST arrives without the session cookie, so the server issues a new session cookie that can replace the user's and log them out | `session="false"` on the page (as above), or no session access in the handler |
| XSS filter that rewrites parameters (Lucy XSS Filter and similar) | Addresses with parentheses or commas come back altered | Exempt the path and escape on output instead (above) |
| `Cross-Origin-Opener-Policy: same-origin` on the calling page | The popup loses `window.opener` after visiting juso | Use `same-origin-allow-popups` on the calling page or do not set it there |
| `document.domain = "…"` (commented out in the samples, "if opener errors occur") | Modern browsers ignore or block it | Do not use it; keep the calling page and the returnUrl page on the same origin |
| EUC-KR site | Korean text is garbled | Add `encodingType=EUC-KR` to the form, and read parameters as EUC-KR. PHP and ASP have separate EUC-KR and `_utf8` sample files |

- The guide's other tips (add the site to trusted sites, IE 11 compatibility view) are for Internet Explorer and no longer apply.
- **Exclude the popup API from penetration tests** (`R`): the sample comments and the guide warn that the IP may be blocked.

## Popup screen style

The juso popup screen can be skinned: register a CSS file when applying for the key. The service provides templates (`addrlinkSample.css` for PC, `addrlinkMobileSample.css` for mobile) for the background image and color, the logo (149×14 px on PC), the search box, result rows, text colors and page buttons. The CSS applies to juso's screen, not to your pages. Use `https://` image URLs; the templates show `http://` placeholders.
