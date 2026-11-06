# Form Patterns (기본 패턴)

KRDS basic patterns for input forms: 입력 폼, 개인 식별 정보 입력, 오류, 동의, 첨부파일, 확인, 도움. All were first registered on 2025-01-15 (Figma v1.0.0, HTML Component Kit v1.0.1).

Each pattern has a **Rules** table. `R`, `G` and `D` are defined in `SKILL.md`. The KWCAG column gives the KWCAG 2.2 item KRDS cites, with its number; `—` means KRDS cites no KWCAG item.

## 입력 폼 (input form)

A content section where the user enters data to send to the server, made of one or more input controls.

**Structure**: 1 title (purpose of the form), 2 description (optional; notes for entering data), 3 content (the input components), 4 fieldset (optional; groups related components), 5 error message, 6 action buttons (submit or stop).

**Types**

| Type | Use when |
|------|----------|
| Single screen | The default. Reduce complexity with progressive disclosure |
| Modal | Very important data that is rarely entered or changed. Keep it to about 5 input components |
| Step-by-step | The data is complex or needs saving midway. Steps must be clear, the content of each step must have a logical, linear relationship, and progress must be shown with a separate component (step indicator). It is slow for expert users: first try clearer sections, headings and shorter content. Order questions from easy to hard, in small meaningful chunks |

**Rules**

| Rule | Strength | KWCAG | Check |
|------|----------|-------|-------|
| Align content vertically in one column. Use several columns only for much data in a wide container | `G` | — | No unrelated fields side by side |
| Put fields that form one piece of information on one row: family and given name, phone number, card number, postal code and address, start and end date | `G` | — | Row groups are semantically related |
| Give enough space between forms and between content blocks | `G` | — | |
| Place action buttons consistently, at the bottom right by default. With 3 or more actions, put the tertiary action at the bottom left | `G` | — | Same position on every form |
| The submit button **must** be the rightmost of the group, with the next buttons to its left. If the group is at the bottom left, reverse the order: the submit button is leftmost | `R` | — | |
| Consider disabling the submit or next button until all required fields are filled | `G` | — | |
| Disable the submit button after it is pressed, to prevent duplicate submission. If processing takes time, show a message and a spinner | `G` | — | Double click sends one request |
| Put labels and descriptions close to the field | `G` | — | |
| Show the unit of a value (개, 부 and so on) apart from the label | `G` | — | |
| Distinguish required and optional fields clearly. If most are required, mark only the optional ones; if most are optional, mark only the required ones | `R` | — | |
| Mark required or optional fields the same way across the same type of form and the whole site: the text 필수/선택 in the label, an asterisk on required fields, or a note at the top when every field is required | `R` | — | One method site-wide |
| Ask only for the minimum data needed; derive each field carefully | `R` | — | Every field has a purpose |
| Consider autofill for frequently entered data: member data when logged in, an option to reuse the previous input, and `autocomplete` for browser-stored data | `G` | — | |
| Do not automatically delete values the user entered or selected wrongly | `R` | — | Invalid input is still in the field after an error |
| Design for mobile first: touch screens and limited bandwidth | `R` | — | |
| Give every input field and the form an accessible name | `R` | 7.3.2 레이블 제공 | Every control has a label, `aria-label` or `aria-labelledby` |
| Give each form section a heading (`h2` to `h6`) | `R` | 6.4.2 제목 제공 | |
| Tell the user exactly which field has an error. After server-side validation, move focus to the field in error when the error dialog's OK button is pressed | `R` | 7.3.1 오류 정정 | |
| Let the user move focus freely; even with automatic focus advance, the user can go back to the previous field | `R` | 6.1.2 초점 이동과 표시 | |
| If required fields are marked with an image, give it alternative text | `R` | 5.1.1 적절한 대체 텍스트 제공 | |
| In a multi-step form, fill repeated data automatically or offer "use the previous input" | `R` | 7.3.4 반복 입력 정보 | |

**Validation**

The form must check that required fields are filled and that values match the required format, and give feedback for invalid input (`R`).

| Event | Behavior |
|-------|----------|
| Client-side validation | Recommended: check in the browser before sending, with inline messages on the fields in error |
| Server-side validation | **Must always be used as well**: client checks are easily bypassed and are not a security check. Show the results inline on the fields too |
| Keyup | Validate while typing for values that need live feedback (a duplicate user ID, a password with composition rules) |
| Focusout | Validate when the user leaves the field for values that cannot be judged until complete (dates) |
| Click or Enter on submit (server side) | Move focus to the **first** field in error |

- The rules require exact error identification and cite WCAG Status Messages, but give no markup. `D`: link each error message to its field with `aria-describedby`, set `aria-invalid="true"`, and for many errors add a summary at the top with links to the fields.

## 개인 식별 정보 입력 (personal identification data)

Any information that identifies a person or confirms basic data of a person or organization. KRDS covers four fields: name, birth date, gender, phone number.

**Rules**

| Rule | Strength | KWCAG | Check |
|------|----------|-------|-------|
| Check again that the data is needed for the service | `R` | — | Each field has a stated purpose |
| Explain clearly what the data will be used for | `R` | — | |
| Allow copy and paste in every personal identification field | `R` | — | No `onpaste="return false"` |
| Do not set default values. Placeholders must be easy to tell from real input | `R` | — | |
| **Name**: accept and display every character the user can type, including symbols and spaces. If a task such as identity verification restricts the format, explain the restriction and offer an alternative | `R` | — | |
| **Name**: allow enough characters for every name, and size the field to the maximum. Do not require 3 or more characters for Korean names | `R` | — | Two-character names pass |
| **Name**: use a single text field; use several name fields only with care, since not every name has a family/given form. (The input form pattern lists family and given name as fields that may share a row; `D`: follow this more specific rule) | `R` | — | |
| **Name**: check that users who changed their name can enter it; if there is a restriction, explain the solution next to the field | `R` | — | |
| **Romanized name (foreigners)**: make the field at least 320 to 360 px wide, or 100% in a single-column form; long names must scroll or show in full | `G` | — | |
| **Romanized name**: accept spaces inside the name; do not reject or strip them in client or server validation. Example help: "여권에 표기된 이름 전체를 입력하세요. 공백과 '-'를 포함할 수 있습니다." | `R` | — | |
| **Romanized name**: do not normalize upper and lower case; store and show it as typed | `R` | — | |
| **Birth date**: do not use a date picker | `R` | — | |
| **Birth date**: do not use a select for year or day; use the date input component (several fields or a single field) | `R` | — | |
| **Birth date**: state the input format exactly (see `input-components.md`, 날짜 입력 필드) | `G` | — | |
| **Gender**: do not preselect a gender | `R` | — | No `checked` on load |
| **Gender**: offer a "선택 안 함" option, or make the field optional when identity verification does not need it | `G` | — | |
| **Phone**: ask for the type of number the purpose needs; restricting to one type (mobile only) is acceptable only for verification or messaging | `G` | — | |
| **Phone**: label clearly (휴대 전화번호, 지역 번호; just 전화번호 if the type does not matter) | `G` | — | |
| **Phone**: accept spaces, hyphens and other formats. If a format is required, explain it in help text; automatic formatting is allowed | `R` | — | `010 1234 5678` and `010-1234-5678` both pass |
| **Phone**: use a combo box of country names and codes for the country code | `G` | — | |
| **Phone**: with several numbers, label each one (휴대 전화번호, 사무실 전화번호) and let the user mark the main one | `R` | — | |
| Set the `autocomplete` attribute so that user agents know the purpose of each field | `R` | — (KRDS cites WCAG 1.3.5 Identify Input Purpose only) | Every personal data field has a valid `autocomplete` token |

**Fields KRDS does not cover** (`D`)

KRDS gives no rules for resident registration numbers, addresses or email, and no `autocomplete` values. This skill adds the following; mark them as beyond KRDS in a review.

| Field | `autocomplete` | Other attributes | Notes |
|-------|----------------|------------------|-------|
| Name | `name` | | One field, per KRDS |
| Birth date (single field) | `bday` | `inputmode="numeric"` | Several fields: `bday-year`, `bday-month`, `bday-day` |
| Mobile or phone number | `tel` (`tel-national` without country code) | `type="tel"` | `type="tel"` brings up the phone keypad |
| Email | `email` | `type="email"` | |
| Postal code | `postal-code` | `inputmode="numeric"`, read-only if filled by an address search | |
| Address | `address-line1` (road address), `address-line2` (detail) | | Search address with a button that opens the road address search; keep the detail address as a separate text field |
| Resident registration number | `off` | Back part `type="password"` or masked | Collect it only where laws and regulations specifically require or allow it, offer another way to sign up (for example identity verification), and encrypt it when stored (개인정보 보호법 제24조의2, unverified in this skill: check the current text on law.go.kr; `secure-coding` SR2-7) |
| User ID, password | `username`, `current-password` or `new-password` | | See `application-flow.md`, 로그인 정보 입력 |

```html
<div class="form-group">
  <div class="form-tit"><label for="phone">휴대 전화번호</label></div>
  <div class="form-conts">
    <input type="tel" id="phone" class="krds-input medium" autocomplete="tel-national" aria-describedby="phone_hint">
  </div>
  <p class="form-hint" id="phone_hint">숫자만 입력하거나 하이픈(-)을 넣어 입력할 수 있습니다.</p>
</div>

<fieldset class="form-group">
  <legend class="form-tit">성별</legend>
  <div class="krds-check-area">
    <div class="krds-form-check"><input type="radio" name="gender" id="g1" value="M"><label for="g1">남성</label></div>
    <div class="krds-form-check"><input type="radio" name="gender" id="g2" value="F"><label for="g2">여성</label></div>
    <div class="krds-form-check"><input type="radio" name="gender" id="g3" value="N"><label for="g3">선택 안 함</label></div>
  </div>
</fieldset>
```

- `D`: KRDS's gender example uses a `div.form-tit` with no `fieldset`/`legend`, which KRDS's radio button page recommends (`selection-components.md`). Its name example has no `autocomplete`, which breaks the rule above.

## 오류 (error)

Shown when the system cannot complete what the user asked. Unlike a warning, it reports a problem that has already happened, and it **must** lead the user to complete the original action. It is shown inline at the point of error or in a modal.

**Rules**

| Rule | Strength | KWCAG | Check |
|------|----------|-------|-------|
| Make errors quick to notice by size, color and position | `R` | — | |
| Explain clearly what went wrong and where | `R` | — | The message names the field and the problem |
| Give a way to fix the error, especially when the content is complex | `G` | — | |
| Use a polite tone that reassures the user | `R` | — | |
| Move focus automatically to the element in error; after an error modal closes, move focus to the field in error | `R` | 7.3.1 오류 정정 | |
| Keep the user's input after showing the error | `R` | 7.3.1 오류 정정 | |

**Markup**: inline errors use `.form-conts.is-error` and `p.form-hint-invalid` (see `SKILL.md`, "Common field markup"). KRDS does not say when to use a modal instead of inline messages. `D`: prefer inline messages on the fields; use a modal only for errors that are not tied to a field (for example a failed submission). An error modal needs `role="dialog"`, `aria-modal="true"`, a title linked with `aria-labelledby`, and one button that names the action (KRDS's example uses "아니요/예", which does not fit an error).

## 동의 (consent)

Lets the user read terms and conditions and confirm consent or acknowledgement. Terms are long and use difficult words, so they **must** be structured.

**Structure**: 1 "agree to all" option (a checkbox that toggles every item, b description of all items and of the optional ones); 2 list (a container, b item title, c body with the terms, d consent options as radio buttons or a checkbox).

**Rules**

| Rule | Strength | KWCAG | Check |
|------|----------|-------|-------|
| Offer a "동의하지 않음" option | `G` | — | Each item has agree and disagree |
| Make agree and disagree easy to tell apart | `G` | — | |
| Separate required and optional items: put 필수 or 선택 in each title, and group required items at the top | `R` | — | |
| Let the user scroll the terms with the keyboard | `R` | 6.1.1 키보드 사용 보장 | A scrolling terms box is focusable (`tabindex="0"`) |
| Structure the terms with headings and paragraphs | `R` | 6.4.2 제목 제공 | |
| Place the radio labels to the right of the control, and link each radio to its item title with `aria-describedby` | `R` | 7.3.2 레이블 제공 | Each option's description names its item |

**Keyboard and behavior**

| Action | Behavior |
|--------|----------|
| Tab, Shift + Tab | Move to the next or previous element with a visible focus ring |
| "Agree to all", Click or Space | Selecting it sets every item to 동의함; clearing it sets every item to 동의 안 함. Focus stays on the checkbox |
| Any item set to 동의 안 함 | "Agree to all" must stay cleared |
| Individual items | Follow the radio button and checkbox rules |

```html
<fieldset class="agree-item">
  <legend><h4 class="agree-tit" id="agree1_tit">[필수] 개인정보 수집 및 이용</h4></legend>
  <button type="button" class="krds-btn small secondary" aria-describedby="agree1_tit">약관 읽기</button>
  <div class="krds-check-area">
    <div class="krds-form-check"><input type="radio" name="agree1" id="agree1_n" aria-describedby="agree1_tit"><label for="agree1_n">동의하지 않음</label></div>
    <div class="krds-form-check"><input type="radio" name="agree1" id="agree1_y" aria-describedby="agree1_tit"><label for="agree1_y">동의함</label></div>
  </div>
</fieldset>
```

- `D`: KRDS's example has no `aria-describedby` on the options, no `fieldset`/`legend`, four identical "약관읽기" buttons, and an optional item with a single "확인함" checkbox instead of agree/disagree. The corrected example follows the rules.
- `D`: KRDS does not say what happens when a required item is not agreed. Block the next step and show an inline error on that item (see 오류).

## 첨부파일 (attachments)

Downloadable files attached to posts or body text. This is the download pattern; uploads are in `input-components.md` (파일 업로드).

**Structure**: 1 file name, 2 file information (type, size, page count), 3 download link, 4 preview link (opens in a new tab), 5 container, 6 icon (optional).

**Types**: inline link (in body text), list link (separate container with download and preview links; for documents with details), icon link (in structured lists and tables).

**Rules**

| Rule | Strength | KWCAG | Check |
|------|----------|-------|-------|
| Tell the user in advance that the link downloads a file (the word 다운로드 nearby or in the link), so that the action is predictable | `R` | — | |
| Show file type and size as `[유형, 크기]` to the right of the name, with KB, MB or GB | `G` | — | `[hwp, 328KB]` |
| Inline attachment text has the same size as the surrounding text | `R` | — | |
| Give the attachment icon alternative text with the exact file name | `R` | 5.1.1 적절한 대체 텍스트 제공, 6.4.3 적절한 링크 텍스트 | |
| Provide the attached document itself in a format screen readers can read (text, with alternative text for images) | `R` | — | |

```html
<li>
  <p class="tit" id="file1">사회보장급여 신청(변경)서 [hwp, 328KB]</p>
  <div class="btn-wrap">
    <a href="/files/1.hwp" class="krds-btn medium text" download aria-describedby="file1">다운로드</a>
    <a href="/files/1/view" class="krds-btn medium text" target="_blank" aria-describedby="file1">바로보기<span class="sr-only">(새 창)</span></a>
  </div>
</li>
```

- `D`: KRDS's example uses `<button>` for download and preview, with the name "다운로드" alone, so several files have identical buttons. Downloads and previews are navigation: use links, and include or link the file name.

## 확인 (confirmation)

Used when an action leads to a result that is hard to undo, or when the user must be aware of its effects. Types: when submitting a form, and when an important context on the screen changes.

**Rules**

| Rule | Strength | KWCAG | Check |
|------|----------|-------|-------|
| Ask for confirmation only for serious or hard-to-undo actions; frequent confirmations make users ignore the important ones | `R` | — | |
| Explain the situation clearly and briefly: what happens and why it matters | `R` | — | |
| Offer both a confirm and a cancel button | `R` | — | |
| Make button labels describe the action, so the user knows what happens without reading the body ("신청 취소", not "확인") | `G` | — | |

- KRDS gives no accessibility rules for this pattern, and its example is a terms modal with "취소/확인" buttons. `D`: a confirmation modal needs `role="dialog"` (or `alertdialog`), `aria-modal="true"`, focus moved into the dialog on open and back to the triggering control on close, and labels that name the action.

## 도움 (help)

Help about how the UI works, how to use it, or the task flow, combined from several components.

**Types**

| Type | Components | Use for |
|------|------------|---------|
| Fixed help (always visible) | Guide area (section heading and description), label, inline text, placeholder | Information everyone must see; frequent users and familiar screens |
| On-request help | Tooltip, contextual help, help panel, coach mark, follow-along panel | Preventing problems; new users, complex services, new features |
| Responsive help | FAQ, help menu (separate screens) | Users who already have a problem |

**Rules**

| Rule | Strength | KWCAG | Check |
|------|----------|-------|-------|
| Match help to the task: fixed help for simple or familiar screens, on-request help for complex or new ones | `G` | — | |
| Write help clearly and briefly, from the user's point of view, at the right moment | `R` | — | |
| Do not write help that applies only to some environments | `R` | — | |
| Make on-request help content also available as responsive help (FAQ, help menu) | `R` | — | |
| Use the same words for the same page titles and button names across every service | `R` | — | |
| Open links to related screens or resources in a new tab | `R` | — | |
| **Guide area**: use it for information needed to understand the whole page (whether it can be cancelled or changed, e-signature or identity verification steps, required documents); place it at the top of the body; use only one per screen. Extra content goes in a disclosure that is collapsed and holds nothing essential | `R` | — | |
| **Placeholder**: do not use it as a substitute for a label or help. It may show a date or number format or the number of digits, and the same text must also appear as inline text | `R` | — | Every placeholder text is repeated in visible help |
| **Inline text**: put information needed to complete the task next to the element | `G` | — | |
| **Tooltip**: for short extra information (one or two words, one sentence), and for labels of icon-only controls | `G` | — | |
| **Contextual help**: for the state or details of a component | `G` | — | |
| **Help panel**: for long help or complex tasks (results of the task, why fields are needed, how to decide, how to enter, definitions) | `G` | — | |
| **Coach mark, follow-along panel**: for rarely used tasks with many steps | `G` | — | |

- KRDS's help example puts `role="tooltip"` on a contextual help popover with a link and a close button; see `action-help.md` for the corrected markup.
