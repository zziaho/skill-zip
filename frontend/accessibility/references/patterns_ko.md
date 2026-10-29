# 자주 쓰는 접근성 패턴

접근성을 갖춘 인터페이스를 만들 때 재사용할 수 있는 패턴입니다. 복사해서 상황에 맞게 수정하여 사용합니다.

## 이미지

```
정보 전달:    <img src="chart.png" alt="2025년 3분기 매출이 40% 증가함">
장식용:       <img src="divider.png" alt="">
복잡한 이미지: <img src="org-chart.png" alt="조직도(자세한 내용은 아래 참조)">
              <details><summary>조직도 상세 설명</summary>...</details>
아이콘 버튼:  <button aria-label="대화상자 닫기"><svg>...</svg></button>
```

## 폼

```html
<!-- 모든 입력 필드에는 눈에 보이고 프로그램으로 연결된 레이블이 필요함 -->
<label for="email">이메일 주소</label>
<input id="email" type="email" autocomplete="email" required aria-describedby="email-err">
<span id="email-err" role="alert"></span>  <!-- 빈 상태로 DOM에 두었다가, 오류가 발생하면 텍스트를 넣어야 읽힘 -->

<!-- 관련된 입력 필드는 묶어서 제공 -->
<fieldset>
  <legend>배송지 주소</legend>
  ...
</fieldset>

<!-- 필수 입력 필드: 색상만으로 표시하지 않음 -->
<label for="name">이름 <span aria-hidden="true">*</span></label>
<input id="name" required>  <!-- 네이티브 required는 보조기술에 전달됨. aria-required는 네이티브가 아닌 커스텀 입력 요소에만 사용 -->
```

## 내비게이션

```html
<!-- 건너뛰기 링크: 첫 번째로 초점을 받는 요소. KWCAG 6.4.1은 화면에 보이도록 요구함 -->
<a href="#main" class="skip-link">본문 바로가기</a>

<!-- 프레임: 모든 프레임에는 간결하고 고유한 title이 필요함 (KWCAG 6.4.2) -->
<iframe src="map.html" title="오시는 길 지도"></iframe>

<!-- 랜드마크: 네이티브 요소에 이미 역할이 있으므로 중복된 role 속성을 추가하지 않음 -->
<header>...</header>
<nav aria-label="주 메뉴">...</nav>
<main id="main">...</main>
<aside>...</aside>
<footer>...</footer>
```

## 표

```html
<!-- 내용과 구조를 설명하고, 제목 셀과 데이터 셀을 구분함 (KWCAG 5.3.1) -->
<table>
  <caption>2025년 분기별 매출: 분기, 매출액, 증감률</caption>
  <thead>
    <tr><th scope="col">분기</th><th scope="col">매출액</th><th scope="col">증감률</th></tr>
  </thead>
  <tbody>
    <tr><th scope="row">1분기</th><td>120억</td><td>+5%</td></tr>
  </tbody>
</table>
```

## 제목

```
권장 사항(WCAG·KWCAG 요구사항은 아님): 페이지마다 h1은 하나만 사용하고, 수준을 건너뛰지 않음
요구사항: 제목은 해당 구역을 설명해야 하고(통합 2.4.1), 제목 요소로 마크업해야 함(1.3.1)
올바른 예:   h1 > h2 > h3 > h2 > h3
잘못된 예:   h1 > h3 (h2를 건너뜀)
```

## 초점 관리

```javascript
// 모달: 초점을 안에 가두고, 닫으면 원래 위치로 되돌림
dialog.showModal();  // 페이지의 나머지 부분을 비활성화(inert)하고, Esc로 닫는 기능을 지원함
dialog.addEventListener('close', () => triggerButton.focus());

// 동적 콘텐츠: 새로 나타난 콘텐츠로 초점을 옮김
newSection.setAttribute('tabindex', '-1');
newSection.focus();
```

## 상태 메시지

```html
<!-- 초점을 옮기지 않고 읽어 줌 -->
<!-- role="status"는 암묵적으로 polite, role="alert"는 암묵적으로 assertive -->
<div role="status">검색 결과 3건</div>
<div role="alert">2분 후에 세션이 만료됩니다</div>

<!-- 로딩 상태 -->
<div role="status">불러오는 중...</div>
```

## 색상과 명도 대비

```
텍스트 명도 대비:  최소 4.5:1(일반 텍스트), 3:1(18pt 이상 또는 14pt 이상 굵은 글꼴)
                   KWCAG 5.4.3은 확대할 수 있는 텍스트에도 3:1을 허용함
UI 명도 대비:      테두리, 아이콘, 초점 표시는 최소 3:1 (WCAG에만 해당)
색상만으로 정보를 전달하지 않음: 아이콘, 패턴, 밑줄, 텍스트 레이블을 함께 사용
```

## 멀티미디어

```html
<!-- 자막이 있는 동영상 -->
<video controls>
  <source src="video.mp4" type="video/mp4">
  <track kind="captions" src="captions.vtt" srclang="ko" label="한국어" default>
</video>

<!-- 대본이 있는 오디오 -->
<audio controls src="podcast.mp3"></audio>
<details><summary>대본</summary>...</details>
```

## 모바일 터치 대상

```css
/* WCAG 최소 24x24 CSS px, KWCAG 권장 대각선 6.0mm, 44x44면 편하게 조작할 수 있음 */
.button {
  min-width: 44px;
  min-height: 44px;
  padding: 10px;
}

/* 인접한 대상 사이에 충분한 간격을 둠 */
.icon-button + .icon-button {
  margin-left: 8px;
}
```

## 텍스트 크기 조정

```css
/* 상대 단위를 사용해서 사용자 설정에 따라 텍스트 크기가 바뀌도록 함 */
body { font-size: 100%; line-height: 1.5; }  /* 브라우저 기본값을 따름 */
h1   { font-size: 2rem; }       /* 루트 크기에 비례함 */
p    { font-size: 1rem; }

/* 리플로우 지원: 너비가 고정된 컨테이너를 사용하지 않음 */
.container { max-width: 100%; }
```

## 언어 선언

```html
<!-- 페이지 언어 -->
<html lang="ko">

<!-- 문장 안에서 언어가 바뀌는 부분 -->
<p>이 문서는 <span lang="en">Web Content Accessibility Guidelines</span>를 기반으로 합니다.</p>
```
