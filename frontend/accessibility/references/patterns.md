# Common Accessible Patterns

Reusable patterns for building accessible interfaces. Copy and adapt.

## Images

```
Informative:  <img src="chart.png" alt="Sales grew 40% in Q3 2025">
Decorative:   <img src="divider.png" alt="">
Complex:      <img src="org-chart.png" alt="Organization chart (details below)">
              <details><summary>Chart details</summary>...</details>
Icon button:  <button aria-label="Close dialog"><svg>...</svg></button>
```

## Forms

```html
<!-- Every input needs a visible, associated label -->
<label for="email">Email address</label>
<input id="email" type="email" autocomplete="email" required aria-describedby="email-err">
<span id="email-err" role="alert"></span>  <!-- keep in DOM empty; inject text on error so it is announced -->

<!-- Group related inputs -->
<fieldset>
  <legend>Shipping address</legend>
  ...
</fieldset>

<!-- Required field: don't use color alone -->
<label for="name">Name <span aria-hidden="true">*</span></label>
<input id="name" required>  <!-- native required is exposed to AT; aria-required is only for custom (non-native) inputs -->
```

## Navigation

```html
<!-- Skip link: first focusable element. KWCAG 6.4.1 requires it to be visible on screen -->
<a href="#main" class="skip-link">본문 바로가기</a>

<!-- Frames: every frame needs a concise, unique title (KWCAG 6.4.2) -->
<iframe src="map.html" title="오시는 길 지도"></iframe>

<!-- Landmarks: native elements already carry the roles; do not add redundant role attributes -->
<header>...</header>
<nav aria-label="Main">...</nav>
<main id="main">...</main>
<aside>...</aside>
<footer>...</footer>
```

## Tables

```html
<!-- Describe content/structure and separate header cells from data cells (KWCAG 5.3.1) -->
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

## Headings

```
Best practice (not a WCAG/KWCAG requirement): one h1 per page, no skipped levels.
Requirement: headings describe their sections (unified 2.4.1) and are marked up as headings (1.3.1).
Correct:   h1 > h2 > h3 > h2 > h3
Incorrect: h1 > h3 (skipped h2)
```

## Focus Management

```javascript
// Modal: trap focus inside, restore on close
dialog.showModal();  // makes the rest of the page inert and supports Esc to close
dialog.addEventListener('close', () => triggerButton.focus());

// Dynamic content: move focus to new content
newSection.setAttribute('tabindex', '-1');
newSection.focus();
```

## Status Messages

```html
<!-- Announced without focus change -->
<!-- role="status" is implicitly polite, role="alert" implicitly assertive -->
<div role="status">3 results found</div>
<div role="alert">Session expires in 2 minutes</div>

<!-- Loading state -->
<div role="status">Loading...</div>
```

## Color and Contrast

```
Text contrast:     minimum 4.5:1 (normal text), 3:1 (18pt+ or 14pt bold+)
                   KWCAG 5.4.3 also allows 3:1 for text that can be zoomed
UI contrast:       minimum 3:1 for borders, icons, focus indicators (WCAG only)
Never use color alone: add icon, pattern, underline, or text label
```

## Multimedia

```html
<!-- Video with captions -->
<video controls>
  <source src="video.mp4" type="video/mp4">
  <track kind="captions" src="captions.vtt" srclang="ko" label="Korean" default>
</video>

<!-- Audio with transcript -->
<audio controls src="podcast.mp3"></audio>
<details><summary>Transcript</summary>...</details>
```

## Mobile Touch Targets

```css
/* WCAG minimum 24x24 CSS px; KWCAG recommends 6.0mm diagonal; 44x44 is comfortable */
.button {
  min-width: 44px;
  min-height: 44px;
  padding: 10px;
}

/* Sufficient spacing between adjacent targets */
.icon-button + .icon-button {
  margin-left: 8px;
}
```

## Text Resizing

```css
/* Use relative units so text scales with user preferences */
body { font-size: 100%; line-height: 1.5; }  /* respects browser default */
h1   { font-size: 2rem; }       /* scales with root */
p    { font-size: 1rem; }

/* Support reflow: no fixed-width containers */
.container { max-width: 100%; }
```

## Language Declaration

```html
<!-- Page language -->
<html lang="ko">

<!-- Inline language change -->
<p>이 문서는 <span lang="en">Web Content Accessibility Guidelines</span>를 기반으로 합니다.</p>
```
