# 2. Operable (운용의 용이성)

All UI components and navigation must be operable by all users regardless of input method.

`KWCAG` column: KS X OT0003:2022 item number. Every row with a number is **mandatory** for Korean web accessibility compliance, regardless of `Level`. `—` = no corresponding KWCAG item.

## 2.1 Input Device Accessibility (입력장치 접근성)

| ID | Rule | Test | Scope | Level | KWCAG |
|----|------|------|-------|-------|-------|
| 2.1.1 | All functionality accessible via keyboard alone (number of keystrokes does not matter). Exception: content where pointer path is essential (brush, simulation, maps, VR) or motion sensors; the rest of the UI must still be keyboard operable | Tab through every interactive element; activate with Enter/Space | W | A | 6.1.1 |
| 2.1.2 | Focus moves in a logical, predictable order (e.g., ID → password → login button). No keyboard traps; focus must always be able to move forward and back | Tab/Shift+Tab through page; order follows reading order; focus never gets stuck | WM | A | 6.1.2 |
| 2.1.3 | Focused element has a visible focus indicator with no time limit. Pointer focus and keyboard focus may look different | Tab through page; every focused element shows visible outline/border/highlight that does not disappear | WM | AA | 6.1.2 |
| 2.1.4 | When a component receives keyboard focus, it must not be entirely hidden by author-created content (sticky headers/footers, cookie banners, chat widgets, non-modal popups) | Tab through the page with sticky/overlay content present; every focused element remains at least partly visible | WM | AA | — |
| 2.1.5 | Controls must be large enough to select individually. WCAG: target at least 24x24 CSS px, except when: undersized targets are spaced so a 24px-diameter circle centered on each does not intersect another target or circle; an equivalent control on the same page meets the size; the target is inline in a sentence or constrained by line-height; size is set by the user agent and not modified by the author; a particular presentation is essential or legally required. KWCAG: diagonal length 6.0mm+ recommended, with 1px+ inner padding inside the border that does not respond to pointer input | Measure interactive elements against both thresholds | WM | AA | 6.1.3 |
| 2.1.6 | Controls without visible borders must have sufficient center-to-center spacing | Measure spacing between adjacent controls; adequate for finger operation | M | AA | — |
| 2.1.7 | Single-character keyboard shortcuts must satisfy at least one: can be turned off, can be remapped to include a modifier key (Ctrl, Alt, Shift, etc.), or active only when the relevant component has focus | Find single-key shortcuts; verify one of the three options | WM | A | 6.1.4 |
| 2.1.8 | Provide a skip link to the main content at the very beginning of the page. If there are several skip links, the one to main content comes first. KWCAG requires the skip link to be visually displayed on screen | First Tab stop is "Skip to content"; it is visible; activating it moves focus to main content | W | A | 6.4.1 |

## 2.2 Sufficient Time (충분한 시간 제공)

| ID | Rule | Test | Scope | Level | KWCAG |
|----|------|------|-------|-------|-------|
| 2.2.1 | Avoid time limits. If needed, let users turn off or extend the limit before it expires, and notify them at least 20 seconds in advance. Exceptions: real-time events (online auctions, real-time games; still announce the limit and its end), sessions 20h+ | Find timed features; verify disable/extend mechanism; warning appears 20s+ before expiry | WM | A | 6.2.1 |
| 2.2.2 | Auto-moving/scrolling/updating content must have pause/stop and previous/next controls | Find auto-scrolling banners, carousels; verify pause/stop/forward/back controls exist | WM | A | 6.2.2 |

## 2.3 Seizure Prevention (광과민성 발작 예방)

| ID | Rule | Test | Scope | Level | KWCAG |
|----|------|------|-------|-------|-------|
| 2.3.1 | Do not provide content that blinks or flashes 3-50 times per second. Flashing content must cover no more than 10% of a 10-inch+ screen; blinking content must be stoppable. Limiting flashing to under 3 seconds is recommended | Check animations/videos for flash rate, area, and duration | WM | A | 6.3.1 |

## 2.4 Navigation (쉬운 내비게이션)

| ID | Rule | Test | Scope | Level | KWCAG |
|----|------|------|-------|-------|-------|
| 2.4.1 | Content blocks get appropriate headings that describe their content. Blocks without body content must not get headings. Do not repeat unnecessary special symbols in headings | Every content section has a heading; heading text matches content; no empty headings | WM | A | 6.4.2 |
| 2.4.2 | Link text (alone or with surrounding context) describes link purpose/destination; avoid "click here". Put the link on the text that describes the destination; place "바로가기"/"GO" links right after the describing text; combine adjacent text + image links into one link (image alt then empty) | Read each link text; purpose is clear; "더보기" links are identifiable from context (e.g., "공지사항 더보기") | WM | A | 6.4.3 |
| 2.4.3 | Provide multiple navigation methods (e.g., menu + search + sitemap). Exception: content that is a step in a process | At least 2 ways to reach any page (e.g., nav menu + search, or nav + sitemap) | WM | AA | — |
| 2.4.4 | Every page has a concise, unique title; popup windows and frames also get titles (even an empty frame, e.g., "빈 프레임"). Do not repeat unnecessary special symbols in titles | Check title element of pages and popups and title attribute of every frame/iframe | WM | A | 6.4.2 |
| 2.4.5 | E-publication (paginated document) web pages provide page reference locators (e.g., page numbers) and a way to navigate to each page. Locators stay consistent regardless of zoom/reflow or platform | Open paginated document content; page numbers exist, page navigation works, locators persist after zoom | W | — | 6.4.4 |

## 2.5 Input Modalities (입력 방식)

| ID | Rule | Test | Scope | Level | KWCAG |
|----|------|------|-------|-------|-------|
| 2.5.1 | Multi-point gestures (pinch, rotate, two-finger tap) and path-based gestures (swipe, drag and drop, draw) must have single-pointer alternative. Exceptions: essential gestures (signature, simultaneous piano keys), gestures provided by OS/user agent/AT | Find multi-touch/swipe/drag features; verify single-tap alternative exists for each | WM | A | 6.5.1 |
| 2.5.2 | Functions triggered by single pointer: no activation on down-event alone; or complete on up-event with ability to abort/undo; or down-event action reversible on up-event. Exception: essential (piano key, shooting game) | Click/tap controls; verify action fires on release, not press; test aborting by dragging away | WM | A | 6.5.2 |
| 2.5.3 | Visible label text of UI components must be included in the accessible name. Ideally identical; if not, put the visible text at the start of the name | Compare visible button/link text to accessible name (aria-label, name property); visible text is included, preferably first | WM | A | 6.5.3 |
| 2.5.4 | Motion-activated functions (shake to undo, gesture photo) must also be operable via UI controls and must be disableable. Exceptions: accessibility interfaces (eye tracking), essential motion (pedometer) | Find motion-triggered features; verify UI control alternative exists; verify disable option | WM | A | 6.5.4 |
