# 1. Perceivable (인식의 용이성)

All content must be presentable in ways users can perceive through sight, hearing, or touch.

`KWCAG` column: KS X OT0003:2022 item number. Every row with a number is **mandatory** for Korean web accessibility compliance, regardless of `Level`. `—` = no corresponding KWCAG item.

## 1.1 Text Alternatives (대체 텍스트)

| ID | Rule | Test | Scope | Level | KWCAG |
|----|------|------|-------|-------|-------|
| 1.1.1 | Provide concise text alternatives for all non-text content that conveys meaning, including meaningful background images. Image links/buttons describe their function; complex content (charts) gets a sufficient description. Decorative content gets an empty alternative | Every img/icon has descriptive alt; meaningful CSS background images expose their meaning to AT; decorative items use alt="" | WM | A | 5.1.1 |
| 1.1.2 | CAPTCHA must provide alternatives for different sensory abilities | CAPTCHA offers audio alternative or other non-visual method | WM | A | 5.1.1 |

## 1.2 Multimedia Alternatives (멀티미디어 대체수단)

| ID | Rule | Test | Scope | Level | KWCAG |
|----|------|------|-------|-------|-------|
| 1.2.1 | Provide captions, a transcript, or sign language equivalent to the speech in multimedia (at least one). Synchronized closed captions are preferred | Every video with speech has accurate captions, transcript, or sign language | WM | A | 5.2.1 |
| 1.2.2 | Video-only content needs a description (text, audio, or script); audio-only content needs captions, transcript, or sign language | Video-only content has text/audio description; audio-only content has a transcript | WM | A | 5.2.1 |
| 1.2.3 | Provide sign language interpretation for pre-recorded multimedia | Sign language video accompanies multimedia content | WM | AAA | — (KWCAG 5.2.1 accepts sign language as one option) |
| 1.2.4 | Live multimedia must have real-time captions | Live streams provide real-time captioning | WM | AA | 5.2.1 |
| 1.2.5 | Provide audio description for all pre-recorded video content in synchronized media, unless the media is a clearly labeled alternative for text | Videos whose visual information is not conveyed by the soundtrack have an audio-described version or description track | WM | AA | — |

## 1.3 Adaptable Content (적응성)

| ID | Rule | Test | Scope | Level | KWCAG |
|----|------|------|-------|-------|-------|
| 1.3.1 | Use semantic markup so structure is programmatically determined | Headings use heading elements; lists use list elements; tables have headers | W | A | — (partly 5.3.1, 6.4.2) |
| 1.3.2 | Provide content in a logical linear order; reading order must stay logical even when CSS changes the visual layout | Disable CSS/remove styles; content order still logical | WM | A | 5.3.2 |
| 1.3.3 | Data tables provide information about their content/structure (e.g., caption, summary) and distinguish header cells from data cells | Every data table has a caption or equivalent description and th elements; complex tables use scope/headers attributes | W | A | 5.3.1 |
| 1.3.4 | Do not restrict display orientation (portrait/landscape) unless essential | App works in both orientations; no forced lock unless essential (e.g., piano app) | M | AA | — |
| 1.3.5 | Identify input purpose for user data fields (name, email, phone, address) | Autocomplete attributes present on personal data fields | WM | AA | — |
| 1.3.6 | Instructions must not rely solely on shape, size, position, direction, color, or sound. Refer to elements by their actual name/alt text, or supplement sensory cues with another sense (e.g., beep + visible text) | Find instructions like "press the round button" or "see the right"; the target is identifiable without that sensory cue; audio feedback has a visual equivalent | W | A | 5.3.3 |

## 1.4 Distinguishable (명료성)

| ID | Rule | Test | Scope | Level | KWCAG |
|----|------|------|-------|-------|-------|
| 1.4.1 | Do not auto-play sound. Sounds under 3 seconds are allowed. Sound playing 3+ seconds must stop within 3 seconds or stop with a designated key (e.g., Esc), and must offer controls (stop, pause, volume). Preferably provide media paused and play only on user request | No sound plays on load beyond 3s; if it does, a key stops it and controls exist | WM | A | 5.4.2 |
| 1.4.2 | Do not convey information by color alone; use shape, pattern, or text too | Remove color (grayscale/high-contrast mode): all info still distinguishable | WM | A | 5.4.1 |
| 1.4.3 | Text (and images of text) contrast at least 4.5:1 against background. 3:1 allowed for 18pt+ or 14pt+ bold text, and (KWCAG) for text that can be zoomed. Exceptions: logos, decorative content, content whose contrast increases on focus | Measure contrast with tool; all text meets threshold | WM | AA | 5.4.3 |
| 1.4.4 | UI component and graphical object contrast at least 3:1 against adjacent colors | Buttons, icons, form borders meet 3:1 against background | WM | AA | — |
| 1.4.5 | Adjacent content must be visually distinguishable (borders, separator lines, patterns, background contrast, line/letter spacing, etc.) | Neighboring content blocks and controls have visible boundaries or sufficient spacing | WM | A | 5.4.4 |
| 1.4.6 | Support text resize up to 200% without loss of content or function | Zoom to 200%; no content clipped, overlapping, or hidden | WM | AA | — |
| 1.4.7 | Do not use images of text; use real text (except logos, signatures, diagrams) | No meaningful text rendered as image; text is selectable/scalable | WM | AA | — |
| 1.4.8 | Content reflows at 320px width (mobile) / 400% zoom without horizontal scroll | At 320px viewport or 400% zoom, no 2D scrolling needed (except maps, diagrams, video) | WM | AA | — |
| 1.4.9 | Text spacing adjustable without content/function loss: line-height 1.5x, paragraph spacing 2x, letter-spacing 0.12x, word-spacing 0.16x of font size | Apply specified spacing values; no content clipped or overlapping | WM | AA | — |
| 1.4.10 | Content that appears on pointer hover or keyboard focus (tooltips, custom popovers) must be: **dismissible** without moving hover/focus (e.g., Esc), unless it reports an input error or does not obscure other content; **hoverable**, so the pointer can move onto it without it disappearing; **persistent** until hover/focus is removed, the user dismisses it, or it is no longer valid. Exception: user-agent-controlled content such as the native `title` tooltip | Hover/focus each trigger; press Esc to dismiss; move the pointer onto the popup and confirm it stays; confirm it does not time out | WM | AA | — |
