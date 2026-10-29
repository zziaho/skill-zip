# ARIA 위젯 패턴 (APG)

W3C ARIA Authoring Practices Guide에 실린 구현 패턴입니다. 각 절에서는 위젯마다 최소한으로 갖춰야 하는 ARIA 구성과 키보드 동작을 설명합니다. 출처는 https://www.w3.org/WAI/ARIA/apg/patterns/ 입니다.

## 아코디언 (Accordion)

```
컨테이너: 별도의 역할 없음
헤더: <button aria-expanded="true/false" aria-controls="panel-id">
패널: <div id="panel-id" role="region" aria-labelledby="header-id">
```
키: `Enter/Space`로 패널을 펼치거나 접습니다. 선택적으로 `Up/Down`으로 헤더 사이를 이동하고, `Home/End`로 첫 번째와 마지막 헤더로 이동합니다.

## 경고 (Alert)

```
<div role="alert">메시지 텍스트</div>
```
즉시(assertive) 읽힙니다. 사용자가 직접 닫아야 하는 방식으로 만들지 않습니다. 사용자의 확인이 필요한 경고라면 `alertdialog`를 사용합니다.

## 대화상자 (Dialog, 모달)

```
<div role="dialog" aria-modal="true" aria-labelledby="title-id">
  <h2 id="title-id">대화상자 제목</h2>
  ...
  <button>닫기</button>
</div>
```
키: `Tab/Shift+Tab`으로 대화상자 안에서만 초점이 순환합니다(초점 가두기). `Escape`로 닫습니다. 대화상자가 열리면 첫 번째 대화형 요소로 초점을 옮기고, 닫히면 대화상자를 연 요소로 초점을 되돌립니다.

## 펼침 영역 (Disclosure)

```
<button aria-expanded="false" aria-controls="content-id">더 보기</button>
<div id="content-id" hidden>펼쳐지는 내용</div>
```
키: `Enter/Space`로 펼치거나 접습니다. `hidden`과 `aria-expanded`는 항상 함께 바꿉니다.

## 탭 (Tabs)

```
<div role="tablist" aria-label="레이블">
  <button role="tab" aria-selected="true" aria-controls="panel-1" id="tab-1">탭 1</button>
  <button role="tab" aria-selected="false" aria-controls="panel-2" id="tab-2" tabindex="-1">탭 2</button>
</div>
<div role="tabpanel" id="panel-1" aria-labelledby="tab-1">...</div>
<div role="tabpanel" id="panel-2" aria-labelledby="tab-2" hidden>...</div>
```
키: 가로 탭은 `Left/Right`, 세로 탭은 `Up/Down`으로 탭을 전환합니다. `Home`은 첫 번째 탭, `End`는 마지막 탭으로 이동합니다. 활성화된 탭에만 `tabindex="0"`을 지정하고, 나머지 탭에는 `-1`을 지정합니다.

## 메뉴와 메뉴 버튼 (Menu & Menu Button)

```
<button aria-haspopup="true" aria-expanded="false" aria-controls="menu-id">메뉴</button>
<ul role="menu" id="menu-id">
  <li role="menuitem">동작 1</li>
  <li role="menuitem">동작 2</li>
  <li role="menuitemcheckbox" aria-checked="false">토글</li>
</ul>
```
키: `Enter/Space/Down`으로 메뉴를 엽니다. `Up/Down`으로 항목 사이를 이동하고, `Enter/Space`로 실행합니다. `Escape`로 메뉴를 닫고 초점을 버튼으로 되돌립니다. 문자를 입력하면 그 문자로 시작하는 항목으로 이동합니다(type-ahead).

## 콤보 상자 (Combobox)

```
<label for="cb">선택하세요</label>
<input id="cb" role="combobox" aria-expanded="false" aria-controls="listbox-id" aria-autocomplete="list">
<ul role="listbox" id="listbox-id">
  <li role="option" aria-selected="false">옵션 1</li>
</ul>
```
키: `Down`으로 목록을 열거나 아래로 이동합니다. `Up`으로 위로 이동합니다. `Enter`로 선택하고, `Escape`로 닫습니다. `aria-activedescendant`를 사용하면 DOM 초점을 옮기지 않고도 강조된 옵션을 보조기술에 알릴 수 있습니다.

## 목록 상자 (Listbox)

```
<div role="listbox" aria-label="항목 선택" aria-multiselectable="false" tabindex="0">
  <div role="option" aria-selected="true">항목 1</div>
  <div role="option">항목 2</div>
</div>
```
키: `Up/Down`으로 이동합니다. `Home/End`로 첫 번째와 마지막 항목으로 이동합니다. `Enter/Space`로 선택합니다. 여러 항목을 선택할 수 있다면 `Shift+Down/Up`으로 선택 범위를 넓힙니다. 문자 입력으로 항목을 찾는 기능(type-ahead)을 지원합니다.

## 라디오 그룹 (Radio Group)

```
<div role="radiogroup" aria-label="색상">
  <div role="radio" aria-checked="true" tabindex="0">빨강</div>
  <div role="radio" aria-checked="false" tabindex="-1">파랑</div>
  <div role="radio" aria-checked="false" tabindex="-1">초록</div>
</div>
```
키: `Right/Down`으로 다음 라디오 버튼, `Left/Up`으로 이전 라디오 버튼으로 이동합니다. 초점이 이동하면 선택도 함께 바뀝니다. 선택된 라디오 버튼에만 `tabindex="0"`을 지정합니다.

## 체크박스 (Checkbox)

```
<div role="checkbox" aria-checked="false" tabindex="0">레이블 텍스트</div>
```
키: `Space`로 체크 상태를 바꿉니다. 세 가지 상태를 가진 체크박스는 `false → true → mixed` 순서로 바뀝니다. 네이티브 `<input type="checkbox">`를 우선합니다.

## 슬라이더 (Slider)

```
<div role="slider" aria-label="음량" aria-valuenow="50" aria-valuemin="0" aria-valuemax="100" tabindex="0"></div>
```
키: `Right/Up`으로 값을 높이고, `Left/Down`으로 낮춥니다. `Home`은 최솟값, `End`는 최댓값으로 이동합니다. `Page Up/Down`으로 값을 크게 바꿉니다.

## 스핀 버튼 (Spinbutton)

```
<div role="spinbutton" aria-label="수량" aria-valuenow="1" aria-valuemin="0" aria-valuemax="99" tabindex="0"></div>
```
키: `Up`으로 값을 늘리고, `Down`으로 줄입니다. `Home`은 최솟값, `End`는 최댓값으로 이동합니다. 편집할 수 있는 스핀 버튼은 숫자를 직접 입력할 수 있습니다.

## 스위치 (Switch)

```
<button role="switch" aria-checked="false">다크 모드</button>
```
키: `Enter/Space`로 켜거나 끕니다. 상태가 바뀌면 `aria-checked`를 갱신합니다.

## 그리드 (Grid)

```
<table role="grid" aria-label="데이터">
  <tr><th role="columnheader">이름</th></tr>
  <tr><td role="gridcell" tabindex="-1">홍길동</td></tr>
</table>
```
키: 방향키로 셀 사이를 이동합니다. `Enter`로 셀을 실행합니다. `Tab`을 누르면 그리드 밖으로 이동합니다. 한 번에 하나의 셀에만 `tabindex="0"`을 지정합니다(로빙 tabindex).

## 트리 뷰 (Tree View)

```
<ul role="tree" aria-label="파일">
  <li role="treeitem" aria-expanded="true">
    폴더
    <ul role="group">
      <li role="treeitem">File.txt</li>
    </ul>
  </li>
</ul>
```
키: `Right`로 항목을 펼치거나 자식 항목으로 이동합니다. `Left`로 항목을 접거나 부모 항목으로 이동합니다. `Up/Down`으로 항목 사이를 이동하고, `Enter`로 실행합니다. `Home/End`로 화면에 보이는 첫 번째와 마지막 항목으로 이동합니다.

## 도구 모음 (Toolbar)

```
<div role="toolbar" aria-label="서식" aria-orientation="horizontal">
  <button tabindex="0">굵게</button>
  <button tabindex="-1">기울임</button>
  <button tabindex="-1">밑줄</button>
</div>
```
키: `Left/Right`로 도구 사이를 이동합니다. `Tab`을 누르면 도구 모음 밖으로 이동합니다. 도구 모음 안에서는 로빙 tabindex를 사용합니다.

## 이동 경로 (Breadcrumb)

```
<nav aria-label="이동 경로">
  <ol>
    <li><a href="/">홈</a></li>
    <li><a href="/products">상품</a></li>
    <li><a href="/products/shoes" aria-current="page">신발</a></li>
  </ol>
</nav>
```
현재 페이지에는 `aria-current="page"`를 지정합니다. 구분 기호는 CSS로만 표시하며, DOM에 넣지 않으므로 보조기술이 읽지 않습니다.

## 캐러셀 (Carousel)

```
<div role="region" aria-roledescription="carousel" aria-label="추천 콘텐츠">
  <div role="group" aria-roledescription="slide" aria-label="1/5">...</div>
  <button aria-label="이전 슬라이드">◀</button>
  <button aria-label="다음 슬라이드">▶</button>
</div>
```
자동으로 넘어가는 캐러셀에는 일시정지·재생 버튼이 있어야 하며, 이 버튼은 캐러셀 안에서 Tab 순서상 가장 먼저 와야 합니다. 캐러셀 안의 요소가 키보드 초점을 받았거나 포인터가 올라가 있는 동안에는 자동 전환을 멈춥니다. 이전·다음 버튼은 일반 버튼처럼 `Enter`/`Space`로 동작합니다.

## 피드 (Feed)

```
<div role="feed" aria-label="뉴스">
  <article aria-posinset="1" aria-setsize="-1">
    <h2>제목</h2>
    <p>내용...</p>
  </article>
</div>
```
키: `Page Down`으로 다음 글, `Page Up`으로 이전 글로 이동합니다. 전체 개수를 알 수 없는 경우(무한 스크롤)에는 `aria-setsize="-1"`을 지정합니다. 콘텐츠를 불러오는 동안에는 `aria-busy="true"`를 지정합니다.

## 미터 (Meter)

```
<div role="meter" aria-label="디스크 사용량" aria-valuenow="75" aria-valuemin="0" aria-valuemax="100">75%</div>
```
표시 전용이므로 키보드 조작이 필요하지 않습니다. 네이티브 `<meter>` 요소를 우선합니다.

## 링크 (Link)

```
<a href="/page">텍스트</a>         <!-- 권장 -->
<span role="link" tabindex="0">텍스트</span>  <!-- <a>를 쓸 수 없을 때만 사용 -->
```
키: `Enter`로 실행합니다. 언제나 네이티브 `<a>`를 우선합니다.

## 툴팁 (Tooltip)

```
<button aria-describedby="tip-1">저장</button>
<div role="tooltip" id="tip-1">변경 사항을 저장합니다</div>
```
초점을 받거나 포인터가 올라가면 툴팁을 표시합니다. 이때 초점은 트리거 요소에 그대로 남아 있으며, 툴팁 자체는 초점을 받지 않습니다. `Escape`로 툴팁을 닫습니다. 키보드로 나타난 툴팁은 초점이 벗어나면 숨깁니다. 포인터로 나타난 툴팁은 포인터가 트리거 **또는 툴팁 위에** 있는 동안 계속 표시해야 하므로, 포인터가 트리거에서 벗어났다는 이유만으로 숨기면 안 됩니다(WCAG 1.4.13, 통합 1.4.10). 시간이 지나면 자동으로 숨기는 동작도 넣지 않습니다. 툴팁에는 대화형 요소를 넣지 않으며, 초점을 받아야 하는 콘텐츠라면 비모달 대화상자를 사용합니다. 참고로 APG의 툴팁 패턴은 아직 작성 중(work in progress)인 상태입니다.

## 창 분할선 (Window Splitter)

```
<div role="separator" aria-valuenow="50" aria-valuemin="0" aria-valuemax="100" aria-label="크기 조절" tabindex="0"></div>
```
키: `Left/Right` 또는 `Up/Down`으로 크기를 조절합니다. `Home`은 최솟값, `End`는 최댓값으로 이동합니다. `Enter`를 누르면 현재 위치와 직전 위치 사이를 전환합니다.
