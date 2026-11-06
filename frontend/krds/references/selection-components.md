# Selection Components (선택 컴포넌트)

KRDS components for choosing values: 라디오 버튼, 체크박스, 셀렉트, 토글 스위치, 태그. All were first registered on 2025-01-15 (Figma v1.0.0, HTML Component Kit v1.0.1); the tag delete button was resized on 2025-02-04 (HTML Component Kit v1.0.3).

The **Rules** tables use the strengths in `SKILL.md`.

## Which component to use

| Situation | Use | Source |
|-----------|-----|--------|
| Choose exactly one; options must be compared, or speed matters | Radio buttons | 라디오 버튼, 셀렉트 |
| Choose one of more than 7 options the user knows well | Select (or combo box) | 라디오 버튼 |
| Choose one of 7 to 20 options, or space is short, or mobile matters | Select | 셀렉트 |
| More than 20 options | Combo box that suggests matches, or several selects | 셀렉트 |
| On mobile platforms, one of several | Consider a select or combo box first | 라디오 버튼 |
| Choose one or more; the choice is part of a larger task confirmed later (apply, submit) | Checkboxes | 체크박스 |
| Two opposite boolean states that take effect immediately | Toggle switch | 토글 스위치 |
| The state needs a separate submit or apply step | Checkbox or radio buttons, not a toggle | 토글 스위치 |
| Options in a hierarchy | Checkbox list with an indeterminate parent | 토글 스위치, 체크박스 |
| Show or remove filter and sort options already set | Tags | 태그 |
| Only label or classify data, no interaction | Badge, not a tag | 태그 |

- `D`: radio buttons stop at "more than 7" and selects start at "7 or more", so exactly 7 fits both. Prefer radio buttons when the options must be compared, a select when space is short.

## 라디오 버튼 (radio button)

For choosing one value among options; choosing a new option clears the previous one.

- **Structure**: 1 group label (optional), 2 control, 3 option label

**Rules**

| Rule | Strength | KWCAG | Check |
|------|----------|-------|-------|
| Order options alphabetically (가나다순) by default. Ordering by popularity can be faster, but can reinforce bias; with no clear reason, 가나다순 is safest | `G` | — | |
| Stack radio buttons vertically; lay them out horizontally only with short labels | `G` | — | |
| Place each label to the right of its control | `R` | — | Labels on the right |
| With horizontal layout, leave clearly more space between buttons than between a control and its label | `R` | — | |
| Write clear, precise option labels | `R` | — | |
| When an accurate answer matters, do not preselect an option | `R` | — | No `checked` on load |
| Consider a 해당 없음, 잘 모름 or 선택 안 함 option, especially for optional questions (a chosen radio cannot be cleared) | `G` | — | |
| Give the control 3:1 contrast against the adjacent background | `R` | 5.4.3 (WCAG 1.4.11) | |
| Do not show the selected state by color alone | `R` | 5.4.1 색에 무관한 콘텐츠 인식 | |
| Make radio buttons operable with the keyboard. In custom styles, do not hide the native input with `display:none`, `visibility:hidden` or `opacity:0` | `R` | 6.1.1 키보드 사용 보장 | |
| Make focus clearly visible; size and place the hidden native input to match the visible control so the focus ring appears in the right place | `R` | 6.1.2 초점 이동과 표시 (KRDS: "초점 이동") | |
| Give each radio an accessible name (`<label>`, `title`, `aria-label`, `aria-labelledby`); prefer `<label>` so the label is clickable | `R` | 7.3.2 레이블 제공 (KRDS cites 6.1.1 here, likely a copying error) | |
| Let screen readers find the group label: `fieldset` and `legend` convey it (KRDS: "~전달할 수 있다") | `G` | — (WCAG 1.3.1, 3.3.2) | Every radio group is in a `fieldset` with a `legend` |
| `D`: treat the group label as required. WCAG 1.3.1 requires the relationship to be programmatic, and a group of "예/아니요" options means nothing without its question | `D` | — | |

**Keyboard**

| Key | Behavior |
|-----|----------|
| Tab, Shift + Tab | Reach the radio group |
| Arrow keys ↑/←, ↓/→ | Move to the previous or next radio and select it |
| Space | Select the focused radio |
| Click | Clicking the control or its label selects it |

**Markup**: required `.krds-check-area` (whole area) and `.krds-form-check` (each option); optional `.chk-column` (vertical), sizes `.medium`, `.large`. Extra description: `.krds-form-check-cnt > p.krds-form-check-p`. Chip style: `.krds-form-chip` with `label.krds-form-chip-outline` (not in the selector table).

```html
<fieldset class="form-group">
  <legend class="form-tit">발급 방법</legend>
  <div class="krds-check-area chk-column">
    <div class="krds-form-check"><input type="radio" name="issue" id="issue1" value="online"><label for="issue1">온라인 발급</label></div>
    <div class="krds-form-check"><input type="radio" name="issue" id="issue2" value="mail"><label for="issue2">등기우편</label></div>
  </div>
</fieldset>
```

- `D`: KRDS's example uses `div.fieldset` with no `legend`, and puts two groups under the same `name`, which merges them into one radio group. Use a real `fieldset`/`legend` and one `name` per group.

## 체크박스 (checkbox)

For choosing one or more values; each option is independent of the others.

- **Structure**: 1 group label (optional), 2 control, 3 option label
- **Types**: independent options (checked, unchecked); "select all" with sub-options (checked, unchecked, indeterminate: the parent is indeterminate when only some children are checked)
- **Use for**: filters, terms, conditions. **Do not use for**: a single choice (radio buttons); settings that apply immediately (toggle switch)

**Rules**

| Rule | Strength | KWCAG | Check |
|------|----------|-------|-------|
| Order options 가나다순 by default (same reasoning as radio buttons) | `G` | — | |
| Stack checkboxes vertically; lay them out horizontally only with short labels | `G` | — | |
| Place each label to the right of its control | `R` | — | |
| Write clear, precise option labels | `R` | — | |
| With "select all", show the indeterminate state clearly | `G` | — | Parent is not shown as checked when some children are unchecked |
| Give the checkbox and icon 3:1 contrast against the adjacent background | `R` | 5.4.3 (WCAG 1.4.11) | |
| Do not show the checked state by color alone | `R` | 5.4.1 색에 무관한 콘텐츠 인식 | |
| Keep checkboxes keyboard operable (no `display:none`, `visibility:hidden`, `opacity:0` on the native input) | `R` | 6.1.1 키보드 사용 보장 | |
| Make focus clearly visible, aligned with the visible control | `R` | 6.1.2 초점 이동과 표시 (KRDS: "초점 이동") | |
| Give each checkbox an accessible name; prefer `<label>` | `R` | 7.3.2 레이블 제공 | |
| Use `fieldset` and `legend` for a group (KRDS: "~전달할 수 있다"; `D`: treat as required, as for radio buttons) | `G` | — (WCAG 1.3.1, 3.3.2) | |

**Keyboard**: Tab and Shift + Tab reach every checkbox; Space toggles the focused one. Click on the control or label toggles it; the label **must** extend the click area, because the control is small.

**Markup**: same classes as radio buttons (`.krds-check-area`, `.krds-form-check`, `.chk-column`, `.medium`, `.large`).

- `D`: KRDS gives no markup for the indeterminate state. For a native checkbox set `input.indeterminate = true` in script; for a custom one use `aria-checked="mixed"`.

## 셀렉트 (select)

Shows options in a popup and lets the user choose one.

- **Structure**: 1 label, 2 container, 3 expand/collapse icon, 4 highlight (selected or focused option), 5 options
- **Use for**: 7 to 20 options; choosing a value in a form; short space or mobile (native control)
- **Do not use for**: comparing options (radio buttons); several values (checkboxes, multi-select dropdown); more than 20 options (combo box or split selects)

**Rules**

| Rule | Strength | KWCAG | Check |
|------|----------|-------|-------|
| Keep option text short; if it exceeds the width, a tooltip **must** show the full text | `R` | — | |
| Give every select a label. Omit it only with a clear reason | `G` | — | |
| Changing the value must not submit the form; submit only with a separate button | `R` | — (`D`: also KWCAG 7.2.1 사용자 요구에 따른 실행) | No `onchange="form.submit()"` |
| Give the select an accessible name (`<label>`, `title`, `aria-label`, `aria-labelledby`) | `R` | 7.3.2 레이블 제공 | |
| Give the expand icon 3:1 contrast against the adjacent background | `R` | 5.4.3 (WCAG 1.4.11) | |

**Keyboard**

| Key | Behavior |
|-----|----------|
| Click, Enter, Space on the container | Expand or collapse the list |
| Click outside | Collapse the list |
| Esc | Collapse the list and move focus to the container |
| Tab, Shift + Tab | Reach every select |
| Arrow keys ↑/←, ↓/→ | With the list collapsed, change to the previous or next option |
| Enter on an option | Select it and collapse the list |

- KRDS's select is the native `<select>`, which provides this behavior. Rebuild it only if the custom version reproduces every key above.

**Markup**: required `.krds-form-select`; optional `.completed` (value chosen), `.is-error`, sizes `.small`, `.medium`, `.large`. A sorting variant uses `.krds-form-select-sort` with only `title="선택"`; `D`: give it a visible or `sr-only` label ("정렬 기준"), since "선택" does not say what is chosen.

```html
<div class="form-group">
  <div class="form-tit"><label for="region">시도</label></div>
  <div class="form-conts">
    <select id="region" class="krds-form-select" aria-describedby="region_hint">
      <option value="">시도를 선택하세요</option>
      <option value="11">서울특별시</option>
    </select>
  </div>
  <p class="form-hint" id="region_hint">주민등록상 주소지를 선택하세요.</p>
</div>
```

## 토글 스위치 (toggle switch)

Switches between two mutually exclusive states.

- **Structure**: 1 switch (track and handle), 2 label (what the state applies to), 3 state icon, 4 help text (optional)
- **Use for**: two opposite boolean states; turning a feature on or off (notifications); changes that take effect immediately
- **Do not use for**: hierarchical options (indeterminate checkbox list); labels that cannot describe both states (two radio buttons); no default state (do not use a toggle); states that are not opposites or not boolean (radio buttons); several exclusive options (radio buttons); changes that need a submit or apply step (checkbox or radio buttons)

**Rules**

| Rule | Strength | KWCAG | Check |
|------|----------|-------|-------|
| Write the label as a noun where possible; if unclear, use a verb or add help so the effect of on and off is obvious | `R` | — | |
| Keep the label the same in both states; the state is shown by the handle position and icon. State text, if any, goes next to the switch | `R` | — | Label text does not change on toggle |
| Keep the label close to the switch; in wide containers, put it right next to the switch | `G` | — | |
| Use one layout for all switches on a screen: if one shows state text or icons, all do | `R` | — | |
| Give the track, handle and state icon 3:1 contrast against the adjacent background | `R` | 5.4.3 (WCAG 1.4.11) | |
| Keep the switch keyboard operable (no `display:none`, `visibility:hidden`, `opacity:0` on the native input) | `R` | 6.1.1 키보드 사용 보장 | |
| Make focus clearly visible, aligned with the visible switch | `R` | 6.1.2 초점 이동과 표시 | |
| Give the switch an accessible name (`<label>`, `aria-label`, `aria-labelledby`); prefer `<label>` | `R` | 7.3.2 레이블 제공 | |
| Link the help text with `aria-describedby` | `G` | — (WCAG 1.3.1) | |

**Keyboard**: Tab and Shift + Tab reach every switch; Space toggles it. Click on the switch or label toggles it; the label **must** extend the click area.

**Markup**: required `.krds-form-toggle-switch`; optional sizes `.medium`, `.large`. The visible switch is `span.switch-toggle > i` inside the label.

```html
<div class="krds-form-toggle-switch">
  <input type="checkbox" id="noti" role="switch" aria-describedby="noti_hint">
  <label for="noti"><span class="switch-toggle"><i></i></span>알림 수신</label>
</div>
<p class="form-hint" id="noti_hint">신청 처리 결과를 문자로 받습니다.</p>
```

- `D`: KRDS's example is a plain checkbox. Add `role="switch"` so screen readers announce "on/off" instead of "checked"; KRDS does not mention it.

## 태그 (tag)

Classifies content with keywords, or shows that a category or attribute is selected in a list.

- **Structure**: 1 label, 2 container, 3 delete icon, 4 bulk action button, 5 "more" button
- **Types**: plain label (non-interactive, on data items); leading check icon and label (interactive filter or sort option; reverts to a plain label when cleared); label and delete icon (removes a filter or sort option already set)
- **Use for**: showing and removing filter and sort options. **Do not use for**: labeling without interaction (badge)

**Rules**

| Rule | Strength | KWCAG | Check |
|------|----------|-------|-------|
| Keep labels accurate and short: two words or fewer, no line break | `R` | — | |
| Place tags next to the item they belong to, so it is clear which item each tag describes | `R` | — | |
| Do not mix interactive and non-interactive tags in one group | `R` | — | |
| Do not use too many tags; start small and add based on user feedback | `R` | — | |
| Do not use too many colors; one color is best, and added colors must be meaningful and equally emphasized | `R` | — | |
| Show focus on interactive tags with an outline of 3:1 contrast | `R` | 6.1.2 초점 이동과 표시 (KRDS: "초점 이동") | |
| Give interactive tags their function or state: `aria-pressed="true/false"` for filter toggles, `aria-label="[태그 레이블] 옵션 삭제"` for delete buttons, `aria-label="[태그 레이블] 필터 옵션 추가"` for tags that add a filter | `R` | — (WCAG 4.1.2) | |
| Do not convey meaning by tag color | `R` | 5.4.1 색에 무관한 콘텐츠 인식 | |
| Give tag labels and icons 3:1 contrast against the adjacent background | `R` | 5.4.3 (KRDS cites 5.4.1 here; WCAG 1.4.3, 1.4.11) | |

**Keyboard**

| Action | Behavior |
|--------|----------|
| Tab into a tag group | Focus the first tag; only one tag in the group has keyboard focus at a time |
| Click, or Space/Enter (on keyup), on a filter tag | Add the condition; focus moves to the bar that shows applied filters |
| Click, or Space/Enter, on a toggle tag | Toggle its selected state; focus stays |
| Click, or Space/Enter, on a delete button | Remove the tag; focus moves to the previous tag, or to the tag list container if none remain |

**Markup**: required `.krds-tag-wrap` (group) and `.krds-btn-tag` (tag); optional sizes `.large`, `.medium`, `.small`, link style `.link` (an `<a>`).

```html
<div class="krds-tag-wrap medium">
  <span class="krds-btn-tag">서울특별시
    <button type="button" class="btn-delete" aria-label="서울특별시 옵션 삭제"></button>
  </span>
</div>
```

- `D`: KRDS's example names every delete button "삭제" (`sr-only`), against its own `aria-label` rule, and has no `aria-pressed` example.
