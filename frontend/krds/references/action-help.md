# Actions, Feedback and Help (버튼, 단계 표시기, 맥락적 도움말, 툴팁)

KRDS components used around forms. All were first registered on 2025-01-15 (Figma v1.0.0, HTML Component Kit v1.0.1); contextual help was changed on 2025-03-05 (HTML Component Kit v1.0.4: the layer closes only when the user clicks outside it).

The **Rules** tables use the strengths in `SKILL.md`.

## 버튼 (button)

Runs a function or changes a state. Styles reflect the importance of the action.

- **Structure**: 1 text label (every button has one; icon-only buttons hide it visually), 2 container (optional), 3 icon (optional)
- **Use for**: submitting forms, running dialogs, cancelling, general functions, changing state, help, stopping a running process, permanent deletion
- **Do not use for**: going to a completely different screen or service, or opening a new window or tab. Use a link

**Rules**

| Rule | Strength | KWCAG | Check |
|------|----------|-------|-------|
| Give all buttons in a group the same size; show hierarchy with style, not size | `G` | — | |
| Make the hierarchy follow the importance of the task: filled with the main color = emphasized (key action), outlined = default (medium), text = lowest (many functions) | `G` | — | |
| Use the top-level emphasized button only once per page | `G` | — | One most-emphasized button per page |
| In a vertical button group (panels, mobile), put the top-level button first | `R` | — | |
| Label buttons with verbs that predict the result, except common actions (완료, 닫기, 취소, 추가, 삭제) or where a verb makes the label too long or unclear | `R` | — | "신청하기", not "확인" for submitting an application |
| Use icons only on important actions, and only where needed; the icon **must** be closely related in meaning to the text label. Avoid icon-only buttons except well-known ones (settings, close, like). A button with an icon must be more emphasized than one without: if the most important action has no icon, lower actions **must not** have one | `R` | — | |
| Expect double presses (slow network, tremor): data-sending buttons **must** ignore the second interaction | `R` | — | Double click sends one request |
| Give every button an accessible name that explains its function | `R` | 6.4.3 적절한 링크 텍스트 (as cited by KRDS; WCAG 4.1.2) | |
| Do not give alternative text to an icon in a button that already has a text label | `R` | 5.1.1 적절한 대체 텍스트 제공 | Decorative icons are `aria-hidden` or empty |
| For icon-only buttons, the name describes the function, not the image | `R` | 6.4.3 적절한 링크 텍스트 (WCAG 2.4.6) | "검색", not "돋보기" |
| Make every button reachable and operable with the keyboard, except disabled ones | `R` | 6.1.1 키보드 사용 보장 | |
| Keep focus visible: keep the user agent's focus ring where possible; if restyled, it must not be hidden and needs 3:1 contrast | `R` | 6.1.2 초점 이동과 표시 | |
| Anything that works as a button must be announced as a button: use `<button>`, or `role="button"` when another element is unavoidable | `R` | — (WCAG 4.1.2) | No clickable `div` without a role |
| Make the target at least 17 × 17 px for mouse and 44 × 44 px for touch | `G` | 6.1.3 조작 가능 | |

**Keyboard**: Tab and Shift + Tab reach every button; Click, Enter and Space run it.

**Markup**

| Part | Required | Optional |
|------|----------|----------|
| Button | `.krds-btn` | Color `.primary`, `.secondary`, `.tertiary`; size `.xsmall`, `.small`, `.medium`, `.large`, `.xlarge`; text style `.text`; icon only `.icon`, with border and background `.icon.border` |

- KRDS does not say which class matches filled, outlined and text emphasis. `D`: confirm in the Figma library before mapping `.primary` to the single top-level button.
- KRDS gives no rule for the order of submit and cancel buttons; follow the input form pattern (`form-patterns.md`: submit at the right end).

```html
<div class="btn-wrap">
  <button type="button" class="krds-btn medium tertiary">임시 저장</button>
  <button type="button" class="krds-btn medium secondary">이전</button>
  <button type="submit" class="krds-btn medium primary">신청하기</button>
</div>
<button type="button" class="krds-btn medium icon"><span class="sr-only">검색</span><i class="svg-icon ico-sch" aria-hidden="true"></i></button>
```

- `D`: always set `type` on buttons. KRDS's help icon button has none, so inside a form it submits the form.

## 단계 표시기 (step indicator)

Shows the steps of a service and the current progress.

- **Structure**: 1 step number (small screens may show only "4단계 중 1단계"), 2 step label, 3 current step identifier, 4 completed step identifier, 5 connecting line

**Rules**

| Rule | Strength | KWCAG | Check |
|------|----------|-------|-------|
| Keep step labels short and clear; extra text may go next to them, but the label itself **must** not be cut or wrap | `R` | — | |
| Lay out steps logically, left to right or top to bottom, with connecting lines, arrows or chevrons, consistently across the site | `R` | — | |
| Use 3 to 7 steps. Remove unnecessary steps; tasks without problems should be done in one step | `G` | — | |
| Make the current step clearly distinguishable from the others | `R` | — | |
| Choose the navigation model: sequential (the next step is disabled until the current one is done) or adaptive (steps can be skipped or visited in any order) | `G` | — | |
| Let users skip optional steps, placed after the required ones, with a clear label (건너뛰기, 다음에 입력하기). With no required steps left, skip to the final review | `R` | — | |
| Use an ordered list (`ol`, `li`) | `R` | 6.4.2 제목 제공 (as cited by KRDS; WCAG 1.3.1) | |
| Do not distinguish current and completed steps by color alone | `R` | 5.4.1 색에 무관한 콘텐츠 인식 | |
| Let screen readers identify the current step: if the label has no "현재" text, add `aria-current`; if `aria-current` cannot be used, add "현재 단계" as visible or `sr-only` text | `R` | 5.1.1 적절한 대체 텍스트 제공 (as cited by KRDS; WCAG 4.1.2) | |

**Markup**

| Part | Required | Optional |
|------|----------|----------|
| Whole area | `.krds-step-wrap` (on `ol`) | |
| Step | `> li` | Completed `.done`, current `.active` |
| Label | `.step-tit` | |

```html
<ol class="krds-step-wrap">
  <li class="done"><span><i class="step">1단계</i><span class="step-tit">신청인 정보<span class="sr-only">(완료)</span></span></span></li>
  <li class="active" aria-current="step"><span><i class="step">2단계</i><span class="step-tit">신청 내용</span></span></li>
  <li><span><i class="step">3단계</i><span class="step-tit">확인</span></span></li>
</ol>
```

- `D`: KRDS writes `aria-current="true"`; the ARIA value `step` is meant for this case and is announced as "current step". KRDS's example uses `sr-only` "현재단계" text instead, which its rule also allows. Completed steps have no text in KRDS; `D`: add "(완료)" so the state is not visual only.

## 맥락적 도움말 (contextual help)

A popover next to a component with its state or details, shown only when the user asks through an info or help icon button.

- **Structure**: 1 icon button (toggles the help; ⓘ for information, ? for help), 2 container, 3 title, 4 body (short; links allowed), 5 close button
- **Types**: information (ⓘ: extra or good-to-know information, such as why a control is disabled; the body is short but **must** give specific guidance about the element) and help (?: detailed help, with images, video or links, such as how to fill a field)
- **Do not use for**: labels of controls (tooltip); information needed to complete the task (inline help or help panel; it **must not** be hidden in a popover); short extra information (tooltip or inline help)

**Rules**

| Rule | Strength | KWCAG | Check |
|------|----------|-------|-------|
| Place the icon button next to the element it explains | `G` | — | |
| Keep the popover inside the screen | `R` | — | Check at every screen width |
| Do not let the popover cover important content (the button or the element it explains) | `G` | — | |
| Information the user must know **must not** be only in the help; summarize it in the body | `R` | — | |
| Do not open another contextual help or a modal from a contextual help | `R` | — | |
| Open links in the help in a new window | `G` | — | |
| Do not use contextual help and a help panel together in one task flow | `R` | — | |
| Give the icon 3:1 contrast against the adjacent background | `R` | 5.4.3 (WCAG 1.4.11) | |
| Give each icon button a name | `R` | 6.4.3 적절한 링크 텍스트 (as cited by KRDS) | |
| Make each icon button's name unique and include what it explains | `R` | 6.4.3 적절한 링크 텍스트 (WCAG 2.4.6) | "발급 방법 도움말", not "도움말" |
| Open the help only on user request, never on page load | `R` | 7.2.1 사용자 요구에 따른 실행 | |
| Put the popover content right after its icon button in the reading order | `R` | 5.3.2 콘텐츠의 선형구조 (KRDS: "콘텐츠의 선형화") | |
| Move focus logically: if the popover has links, focus moves into it when opened; avoid keyboard traps | `R` | 6.1.2 초점 이동과 표시 | |
| Consider an icon button target of 44 × 44 CSS px; buttons at the end of a sentence are exempt | `G` | 6.1.3 조작 가능 | |

**Keyboard**

| Key | Behavior |
|-----|----------|
| Click, Enter, Space on the icon button | Show the help; press again to hide it, focus stays on the button |
| Tab | Move through the links inside the open popover |
| Click outside, Esc | Hide the help and return focus to the icon button |

**Markup**: required `.krds-contextual-help`, `.tooltip-action` (control), `.tooltip-popover`; optional position `.top.left`, `.top.center`, `.top.right`, `.bottom.left`, `.bottom.center`, `.bottom.right` (the script adds `top left` by default). Script `krds_contextualHelp`: `init()`, `setupTooltips()`, `toggleTooltip()`.

```html
<div class="krds-contextual-help bottom left">
  <div class="tooltip-action">
    <button type="button" class="krds-btn medium icon tooltip-btn" aria-expanded="false" aria-controls="help_issue">
      <span class="sr-only">발급 방법 도움말</span><i class="svg-icon ico-tooltip" aria-hidden="true"></i>
    </button>
    <div class="tooltip-popover" id="help_issue">
      <h4 class="tooltip-title">발급 방법</h4>
      <div class="tooltip-contents"><p>온라인 발급은 직접 출력하거나 전자지갑으로 받을 수 있습니다.</p>
        <a href="/guide/issue" class="krds-btn xsmall link basic" target="_blank">자세히 보기<span class="sr-only">(새 창)</span></a></div>
      <button type="button" class="krds-btn xsmall icon tooltip-close"><span class="sr-only">발급 방법 도움말 닫기</span></button>
    </div>
  </div>
</div>
```

- `D`: KRDS's script sets `role="tooltip"` on this popover, but a tooltip may not contain interactive elements (KRDS's own tooltip page says so). Treat it as a disclosure: `aria-expanded` and `aria-controls` on the button, no `tooltip` role. When using the kit, also remove the line in `setupTooltips()` that adds the role, or the markup fix is undone.
- `D`: KRDS's Esc and close-button handlers close the popover without returning focus to the icon button, against its own keyboard table. Return focus in both cases.

## 툴팁 (tooltip)

A short extra description of an element, shown when the pointer is over, or focus is on, the element or a separate trigger button.

- **Structure**: 1 trigger button, 2 container, 3 icon (optional; status icon), 4 body
- **Types**: info or question icon tooltip (extra information next to a component or label); icon button tooltip (for icon buttons without a text label)
- **Use for**: labels of icon-only controls; short extra information that is not essential (meaning of a word)
- **Do not use for**: content with interactive elements (contextual help); more than about 150 characters (contextual help, help panel, or a help page)

**Rules**

| Rule | Strength | KWCAG | Check |
|------|----------|-------|-------|
| Prefer the tooltip component over the HTML `title` attribute (fixed font and position; may not be read by screen readers) | `G` | — | |
| Keep the popover inside the screen | `R` | — | |
| Do not let the popover cover important content | `G` | — | |
| Icon-only menu and function buttons **must** have a tooltip | `R` | — | |
| Use tooltips only for extra information; essential information **must not** be only in a tooltip | `R` | — | |
| Do not use a tooltip and a `title` attribute on the same element | `R` | — | Screen readers would read it twice |
| Do not mix icon tooltips with contextual help or a help panel on one screen (same-looking triggers, different behavior) | `R` | — | |
| On touch screens tooltips do not appear on hover: choose icons whose meaning is clear | `R` | — | |
| If there is a separate trigger button, toggle the popover with a click on it when a touch interface is detected | `G` | — | |
| Give each trigger button a name | `R` | 6.4.3 적절한 링크 텍스트 (as cited by KRDS) | |
| Make each trigger button's name unique and include what it explains | `R` | 6.4.3 적절한 링크 텍스트 (WCAG 2.4.6) | |
| Link the trigger button and the tooltip with `aria-labelledby`, so screen readers announce the content on focus | `G` | — (WCAG 1.3.1) | |
| Put the popover right after its trigger in the reading order | `R` | 5.3.2 콘텐츠의 선형구조 (KRDS: "콘텐츠의 선형화") | |

**Keyboard and pointer**

| Event | Behavior |
|-------|----------|
| Mouseover, Focus on the trigger; Click on touch screens | Show the tooltip |
| Mouseleave (from the trigger or the popover), Blur; on touch, a click outside | Hide the tooltip |
| Esc | Hide it and keep focus on the trigger; it stays hidden until focus leaves and returns |

**Markup**: required `.krds-tooltip` (trigger) and `.krds-tooltip-popover`; optional `.tooltip-vertical` (above or below), `.tooltip-box` (box style). The script `krds_tooltip` builds the popover from `data-tooltip`, inserts it after the button with `aria-hidden="true"`, and sets `aria-labelledby` on the button.

```html
<button type="button" class="krds-btn icon krds-tooltip" data-tooltip="입력한 검색 조건을 모두 지웁니다">
  <span class="sr-only">검색 조건 초기화</span><i class="svg-icon ico-reset" aria-hidden="true"></i>
</button>
<!-- The kit names the button "button text + data-tooltip" through aria-labelledby: do not repeat the same text in both -->
```

- `D`: KRDS's script registers only `mouseover`, `mouseout` (on the button only), `focus` and `focusout`. Touch click, staying open while the pointer is over the popover (WCAG 1.4.13), and Esc keeping it hidden are not implemented. Add them when using the kit.
- `D`: when the trigger already has a text label and the tooltip adds information, `aria-describedby` keeps the button's own name; `aria-labelledby` (KRDS) replaces it. KRDS's script copies the button text into the popover to compensate; keep that if you follow KRDS.
