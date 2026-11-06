# 팝업 API

juso 서비스가 팝업 창에 자체 주소 검색 화면을 보여 주고, 선택한 주소를 호출하는 쪽 사이트의 페이지로 POST합니다. 출처는 business.juso.go.kr의 팝업 API, 모바일 팝업 API, 상세주소 팝업 API 페이지(2026-11-06 저장), 가이드 PDF "[가이드]팝업API_활용_방법"과 "[가이드]모바일팝업API_활용_방법"(각 27쪽, 2026-07), JSP, PHP, ASP 샘플 소스입니다. 좌표 팝업(`coordinate-api_ko.md`)과 영문 팝업(`english-api_ko.md`)도 같은 방식으로 동작합니다.

`R`, `G`, `D`는 `SKILL_ko.md`에 정의되어 있습니다.

## 엔드포인트

| 용도 | URL | 방식 | 출력 |
|------|-----|------|------|
| PC 팝업 | `https://business.juso.go.kr/addrlink/addrLinkUrl.do` | POST(GET도 허용) | `returnUrl`로 POST되는 폼 파라미터 |
| 모바일 팝업 | `https://business.juso.go.kr/addrlink/addrMobileLinkUrl.do` | POST(GET도 허용) | 같음 |

- 팝업은 **팝업** 유형으로 발급받은 키가 필요하고, 모바일 URL에는 **모바일 팝업** 유형의 키가 필요합니다. 검색용 승인키는 동작하지 않습니다(`R`).
- 모바일 팝업(2017-05 추가)은 변수와 흐름이 같고 URL과 창 크기만 다릅니다. 샘플은 URL 하나를 주석 처리하는 방식으로 둘을 전환하며, 자동으로 감지하지 않습니다.
- 행정망 안의 시스템은 고객센터(1588-0061)에 다른 URL을 문의합니다.

## 흐름

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

- 샘플은 두 번의 로드에 페이지 하나(`jusoPopup.jsp`, `.php`, `.asp`)를 쓰고 `inputYn`으로 둘을 구분합니다. 첫 로드에서는 `Y`가 아니고, juso가 결과를 POST할 때는 `Y`입니다. 표에는 `inputYn`이 문서화되어 있지 않으며, 이 해석은 샘플 코드에서 가져왔습니다.
- `returnUrl`은 returnUrl 페이지 자신의 주소입니다(샘플에서는 `location.href`). `D`: 키를 발급받은 URL이나 IP에 두어야 합니다. 자료는 키를 URL이나 IP별로 발급한다고만 밝힙니다.
- PC 창: `width=570,height=420, scrollbars=yes, resizable=yes`. 모바일: 크기를 지정하지 않습니다.

## 요청 변수

returnUrl 페이지가 자동으로 제출하는 폼이 보냅니다.

| 이름 | 필수 | 설명 |
|------|------|------|
| `confmKey` | Y | 팝업 유형의 승인키 |
| `returnUrl` | Y | 결과를 받을 URL. 없으면 "정상적인 경로로 접속하시기 바랍니다"가 표시됩니다 |
| `resultType` | N | 결과 목록에 표시할 내용, `1`부터 `4`(아래 참조). 샘플은 항상 `4`를 보냅니다 |
| `useDetailAddr` | N | `Y`: 동/층/호 선택을 제공합니다(상세주소 팝업). `N`이거나 없으면 사용자가 상세주소를 직접 입력합니다 |
| `encodingType` | N | 받는 시스템이 EUC-KR을 쓸 때만 `EUC-KR`을 지정합니다. 기본값은 UTF-8입니다. 페이지의 표에는 없고 샘플과 가이드에 있습니다 |

**`resultType`**: 2부터 4까지의 의미가 자료마다 다릅니다(`D`: 두 해석 모두 `4`가 가장 많이 보여 준다는 점은 같으므로, 목록을 더 짧게 하려는 경우가 아니면 `4`를 사용합니다).

| 값 | API 페이지 | 가이드 PDF와 내려받는 샘플 |
|----|-----------|---------------------------|
| 1 | 도로명 | 도로명 |
| 2 | 도로명+지번 | 도로명+지번+상세보기(관련지번, 관할주민센터) |
| 3 | 도로명+상세 건물명 | 도로명+상세보기(상세건물명) |
| 4 | 도로명+지번+상세 건물명 | 도로명+지번+상세보기(관련지번, 관할주민센터, 상세건물명) |

## 출력

juso가 이 파라미터들을 `returnUrl`로 POST하고, 샘플은 이를 opener 페이지의 `jusoCallBack`에 넘깁니다. 이름이 같은 필드는 `search-api_ko.md`와 같은 의미입니다. 팝업은 `roadFullAddr`와 `addrDetail`을 추가합니다.

**`jusoCallBack` 인자 순서**(위치 기반이며, 페이지의 출력 표 순서와 다릅니다):

| # | 이름 | # | 이름 | # | 이름 |
|---|------|---|------|---|------|
| 1 | `roadFullAddr`(상세주소를 포함한 전체 주소) | 10 | `bdMgtSn` | 19 | `udrtYn` |
| 2 | `roadAddrPart1` | 11 | `detBdNmList` | 20 | `buldMnnm` |
| 3 | `addrDetail`(사용자가 입력한 상세주소) | 12 | `bdNm` | 21 | `buldSlno` |
| 4 | `roadAddrPart2` | 13 | `bdKdcd` | 22 | `mtYn` |
| 5 | `engAddr` | 14 | `siNm` | 23 | `lnbrMnnm` |
| 6 | `jibunAddr` | 15 | `sggNm` | 24 | `lnbrSlno` |
| 7 | `zipNo` | 16 | `emdNm` | 25 | `emdNo` |
| 8 | `admCd` | 17 | `liNm` | | |
| 9 | `rnMgtSn` | 18 | `rn` | | |

- 페이지의 출력 표는 `InbrMnnm`과 `InbrSlno`(대문자 I)로 적었고, 모바일 페이지는 `liNM`으로 적었습니다. 샘플과 가이드는 `lnbrMnnm`, `lnbrSlno`, `liNm`을 사용하므로 이를 사용합니다(`D`).
- 좌표 팝업은 `entX`와 `entY`를 26번째와 27번째 인자로 추가합니다.
- 가이드의 PHP 예시는 콜백을 인자 10개로 선언하지만, 내려받는 샘플은 25개를 사용합니다. 25개를 사용합니다.
- returnUrl 페이지를 직접 작성한다면 위치 기반 인자 25개 대신 객체를 넘기는 편이 더 안전합니다(`D`. 아래 예시).

## 오류 메시지

팝업은 juso 화면에 오류를 표시하며, 페이지는 코드 없이 메시지만 나열합니다. 검색 API의 메시지(`search-api_ko.md`)와 같고, 다음이 추가됩니다.

| 메시지 | 원인 |
|--------|------|
| 승인되지 않은 KEY 입니다(가이드: "승인키가 일치하지 않습니다") | 키가 잘못되었거나, 검색용 승인키를 팝업에 사용했습니다 |
| 정상적인 경로로 접속하시기 바랍니다 | `returnUrl`이 없습니다(페이지는 `reurnUrl`로 적었습니다) |

## 상세주소 팝업

- 팝업이나 모바일 팝업 유형으로 도로명주소 API 또는 좌표제공 API를 신청하고, 해당 API의 샘플을 사용하며, returnUrl 페이지의 폼에 hidden 필드를 하나 추가합니다(기능이 동작하려면 `R`).

```html
<input type="hidden" name="useDetailAddr" value="Y">
```

- 그러면 팝업이 동, 층, 호 선택을 제공합니다. 공동주택은 건축물대장에서, 다가구주택은 등록된 도로명주소 데이터에서 가져옵니다.
- 선택한 값이 출력에 어떤 형태로 나타나는지는 자료에 나와 있지 않습니다. `D`: `addrDetail`과 `roadFullAddr`에서 읽고, 등록된 호가 없는 건물도 있으므로 사용자가 수정할 수 있게 합니다.

## 샘플의 보안 문제

공식 returnUrl 페이지는 전달받은 값을 JavaScript 문자열 리터럴에 그대로 기록합니다.

```jsp
opener.jusoCallBack("<%=roadFullAddr%>","<%=roadAddrPart1%>","<%=addrDetail%>", ...);   // JSP
opener.jusoCallBack("<?=$ADDR[roadFullAddr]?>", ...);                                   // PHP
```

returnUrl 페이지는 어디에서 보내든 POST를 받으며, JSP 샘플은 쿼리 문자열도 읽는 `request.getParameter`로 값을 읽으므로 `jusoPopup.jsp?inputYn=Y&roadFullAddr=…` 같은 단순한 링크만으로 충분합니다. 첫 로드의 `var inputYn= "<%=inputYn%>";` 줄도 같은 방식으로 반사됩니다. `"`나 `</script>`가 들어간 값은 문자열을 끝내고 자체 출처에서 스크립트를 실행합니다. 이것이 반사형 XSS입니다(juso 자료는 이를 언급하지 않으므로 `D`이며, `secure-coding`의 보안약점 4에 해당합니다). `addrDetail`은 사용자가 직접 입력하는 자유 텍스트이므로 정상적으로 사용해도 페이지가 깨질 수 있습니다. ASP와 PHP 샘플은 POST 데이터만 읽습니다(`Request.Form`, `$_POST`).

| 샘플 코드 | 문제 | 대신 사용할 방법(`D`) |
|-----------|------|----------------------|
| 스크립트 안의 `"<%=value%>"` | XSS | 값을 HTML 이스케이프(`<c:out>`, `htmlspecialchars`, `Server.HTMLEncode`)로 HTML에 기록하고 DOM에서 읽거나, `<`를 이스케이프하는 JSON 인코더로 직렬화합니다 |
| 페이지의 `var confmKey = "…"` | 누구나 키를 볼 수 있습니다 | 팝업에서는 피할 수 없습니다. juso가 브라우저에서 키를 받기 때문입니다. 키에 등록한 URL이나 IP를 정확하게 유지하고, 시스템마다 별도의 키를 사용합니다 |
| 검사 없이 `opener.jusoCallBack(...)` 호출 | opener가 없어지면 예외가 발생합니다 | `window.opener`가 있고 닫히지 않았는지 확인합니다 |
| opener가 값을 폼에 복사합니다 | 팝업을 거치든 거치지 않든 사용자가 임의의 값을 보낼 수 있습니다 | 제출된 주소를 다른 입력과 똑같이 서버에서 검증합니다: 길이, `zipNo`는 숫자 5자리, 코드 필드는 숫자 |
| PHP `<?` 블록과 `<?=$ADDR[roadFullAddr]?>` | `short_open_tag`가 꺼져 있으면 `<?` 블록이 실행되지 않고, 따옴표 없는 배열 키는 PHP 8에서 치명적 오류입니다 | hidden input의 `value` 속성에(아래 JSP처럼) `<?php echo htmlspecialchars($_POST['roadFullAddr'] ?? '', ENT_QUOTES, 'UTF-8'); ?>`를 사용합니다. 스크립트 문자열 안에는 쓰지 않습니다 |

**안전한 returnUrl 페이지(JSP)**

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

- `jusoPopupKey`는 서버 설정에서 가져와 설정하는 요청 속성이므로, 키가 소스 트리에 들어가지 않습니다(`secure-coding` 23). 그래도 키는 브라우저에 전달됩니다.
- 호출하는 페이지의 `jusoCallBack(data)`는 `data.roadAddrPart1` 등을 읽고, `.value`나 `textContent`로 설정하며, `innerHTML`은 절대 사용하지 않습니다.

## 배포 시 주의할 점(`D`)

returnUrl 페이지는 **business.juso.go.kr에서 보내는 교차 사이트 POST**를 받습니다.

| 설정 | 영향 | 수정 방법 |
|------|------|-----------|
| CSRF 필터(Spring Security 등) | juso의 POST에는 토큰이 없으므로 거부됩니다(403) | returnUrl 경로만 제외합니다. 이 페이지는 상태를 바꾸지 않으므로 제외해도 안전합니다 |
| returnUrl 경로의 로그인이나 세션 검사 | `SameSite=Lax`(Chromium의 기본값)인 세션 쿠키는 교차 사이트 POST에 전송되지 않으므로 페이지가 로그인으로 리다이렉트됩니다 | returnUrl 페이지를 공개합니다. 이 페이지는 값을 opener에 전달하기만 합니다 |
| returnUrl 페이지가 세션을 만드는 경우(JSP 기본값) | 교차 사이트 POST에는 세션 쿠키가 없으므로 서버가 새 세션 쿠키를 발급하고, 이 쿠키가 사용자의 기존 쿠키를 대체해 로그아웃시킬 수 있습니다 | 페이지에 `session="false"`를 지정하거나(위 참조) 핸들러에서 세션에 접근하지 않습니다 |
| 파라미터를 고쳐 쓰는 XSS 필터(Lucy XSS Filter 등) | 괄호나 쉼표가 들어간 주소가 변형되어 돌아옵니다 | 경로를 제외하고, 대신 출력할 때 이스케이프합니다(위 참조) |
| 호출하는 페이지의 `Cross-Origin-Opener-Policy: same-origin` | juso를 방문한 뒤 팝업이 `window.opener`를 잃습니다 | 호출하는 페이지에서는 `same-origin-allow-popups`를 사용하거나 설정하지 않습니다 |
| `document.domain = "…"`(샘플에서 "opener 오류가 발생하면"이라는 설명과 함께 주석 처리되어 있음) | 최신 브라우저는 무시하거나 차단합니다 | 사용하지 않습니다. 호출하는 페이지와 returnUrl 페이지를 같은 출처에 둡니다 |
| EUC-KR 사이트 | 한글이 깨집니다 | 폼에 `encodingType=EUC-KR`을 추가하고, 파라미터를 EUC-KR로 읽습니다. PHP와 ASP에는 EUC-KR 샘플 파일과 `_utf8` 샘플 파일이 따로 있습니다 |

- 가이드의 다른 안내(사이트를 신뢰할 수 있는 사이트에 추가, IE 11 호환성 보기)는 Internet Explorer용이므로 더 이상 적용되지 않습니다.
- **팝업 API는 모의 해킹에서 제외합니다**(`R`): 샘플 주석과 가이드가 IP가 차단될 수 있다고 경고합니다.

## 팝업 화면 스타일

juso 팝업 화면은 스타일을 바꿀 수 있습니다. 키를 신청할 때 CSS 파일을 등록합니다. 서비스는 배경 이미지와 색, 로고(PC에서 149×14 px), 검색창, 결과 행, 글자색, 페이지 버튼을 위한 템플릿(PC용 `addrlinkSample.css`, 모바일용 `addrlinkMobileSample.css`)을 제공합니다. 이 CSS는 juso의 화면에 적용되며 자체 페이지에는 적용되지 않습니다. 이미지 URL은 `https://`를 사용합니다. 템플릿에는 `http://` 자리 표시자가 들어 있습니다.
