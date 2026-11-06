# Input Components (입력 컴포넌트)

KRDS components for entering values: 텍스트 입력 필드, 텍스트 영역, 날짜 입력 필드, 달력, 파일 업로드. All were first registered on 2025-01-15 (Figma v1.0.0, HTML Component Kit v1.0.1).

The **Rules** tables use the strengths in `SKILL.md`. KRDS cites KWCAG 2.2 "텍스트 콘텐츠의 명도 대비" (5.4.3) for the 3:1 contrast of control borders and icons; KWCAG 2.2 has no separate non-text contrast item, so this skill keeps KRDS's citation and notes WCAG 1.4.11 Non-text Contrast.

## 텍스트 입력 필드 (text input)

For one line of short text: letters, digits and symbols.

- **Use for**: values expected on one line (name, phone number, birth date, numbers with a minimum and maximum); free answers that cannot be predicted, instead of radio buttons or a select
- **Do not use for**: multi-line text (use 텍스트 영역); values with fixed content or format (use radio buttons, checkboxes or a select)
- **Structure**: 1 label, 2 input field (distinguished from the background), 3 help text (optional; help or error message), 4 placeholder (optional; hint or example)

**Rules**

| Rule | Strength | KWCAG | Check |
|------|----------|-------|-------|
| Size the field to the expected text: full section width by default, fixed to the maximum length for predictable values (name, postal code, phone). Check that the value is not cut off on small screens | `R` | — | |
| Give every text input a label. Omit it only with a clear reason | `G` | — | |
| A placeholder must not be used as a substitute for a label or help. It disappears on input, and browsers render it below the minimum contrast | `R` | — | No format or instruction only in `placeholder` |
| Do not restrict copy and paste | `G` | — | |
| Enable autofill for values users enter often (personal data) | `G` | — | `autocomplete` set |
| Make the focus of every input visible, especially for custom fields | `R` | 6.1.2 초점 이동과 표시 | Tab to each field; focus is visible |
| Give the field border or fill 3:1 contrast against the adjacent background | `G` | 5.4.3 (WCAG 1.4.11) | |
| Give the field an accessible name with `<label>`, `title`, `aria-label` or `aria-labelledby`; prefer `<label>` so clicking it focuses the field | `R` | 7.3.2 레이블 제공 | |

**Keyboard**: Click on the label or field places the cursor. Tab and Shift + Tab reach every field except disabled ones.

**Markup**

| Part | Required | Optional |
|------|----------|----------|
| Input | `.krds-input` | State on `.form-conts`: `.is-error`, `.is-success` (`.is-information` also appears in the code); size `.small`, `.medium`, `.large` |

- Read-only and disabled use the `readonly` and `disabled` attributes.
- If a `<label>` cannot be linked, give a `title` (KRDS development note).
- Icon buttons inside the field (show password, clear) go in `.form-conts.btn-ico-wrap` with `button.krds-btn.medium.icon` and an `sr-only` name.

```html
<div class="form-group">
  <div class="form-tit"><label for="pw">비밀번호</label></div>
  <div class="form-conts btn-ico-wrap">
    <input type="password" id="pw" class="krds-input" autocomplete="new-password" aria-describedby="pw_hint">
    <button type="button" class="krds-btn medium icon" aria-pressed="false">
      <span class="sr-only">비밀번호 표시</span><i class="svg-icon ico-pw-visible" aria-hidden="true"></i>
    </button>
  </div>
  <p class="form-hint" id="pw_hint">영문자, 숫자, 특수문자를 조합해 8~12자로 입력하세요.</p>
</div>
```

- `D`: KRDS's password example gives the composition rule only as a placeholder, with no help text, which breaks its own placeholder rule. The corrected example moves it to linked help text.
- `D`: for the show-password button, either change its name ("표시"/"숨기기") or keep one name and toggle `aria-pressed`; do not do both.

## 텍스트 영역 (textarea)

For several lines of text.

- **Use for**: input expected on several lines
- **Do not use for**: answers to several questions at once; split the questions and use radio buttons or checkboxes where possible
- **Structure**: 1 label, 2 input area, 3 placeholder (optional), 4 character count (limit and characters entered)

**Rules**

| Rule | Strength | KWCAG | Check |
|------|----------|-------|-------|
| Make the height proportional to the expected maximum text, so that a reasonable amount is visible without scrolling | `G` | — | |
| Give every textarea a label | `G` | — | |
| A placeholder must not be used as a substitute for a label or help | `R` | — | |
| Do not restrict copy and paste | `G` | — | |
| If length is limited, show the maximum and the remaining count after the label or the area, updated as the user types | `R` | — | Count changes on input |
| Give the area 3:1 contrast against the adjacent background | `G` | 5.4.3 (WCAG 1.4.11) | |
| Give the textarea an accessible name (`<label>`, `title`, `aria-label`, `aria-labelledby`) | `R` | 7.3.2 레이블 제공 | |

**Keyboard**: Tab and Shift + Tab reach the field; the arrow keys and the scroll wheel scroll content beyond the default height.

**Markup**: required `.textarea-wrap` (whole area) and `.krds-input` (the textarea); the count is `p.textarea-count` with `span.count-now` and `span.count-total`.

```html
<div class="form-group">
  <div class="form-tit"><label for="memo">문의 내용</label></div>
  <div class="form-conts"><div class="textarea-wrap">
    <textarea id="memo" class="krds-input" maxlength="100" aria-describedby="memo_count"></textarea>
    <p class="textarea-count" id="memo_count" aria-live="polite">
      <span class="count-now">0</span><span class="count-total">/100</span>
    </p>
  </div></div>
</div>
```

- `D`: KRDS's example has a static count, no `maxlength`, and no link between the count and the field. Update the count with script, link it with `aria-describedby`, and use `aria-live="polite"` (or announce only near the limit, to avoid announcing every keystroke).

## 날짜 입력 필드 (date input)

For entering or choosing a date or a period.

- **Structure**: 1 label, 2 input field, 3 calendar icon button (optional; shows or hides the calendar), 4 help text (optional), 5 placeholder (optional; date format hint)

**Types**

| Type | Use when | Examples |
|------|----------|----------|
| Several fields (year, month, day) | The date must match a document exactly. The least efficient method, because users move between fields. Year or day may be omitted | Card expiry, passport issue date, birth date |
| Single field | The user knows the date. More flexible. If users may not remember the date, a date picker **must** be added | First part of the resident registration number, birth date |
| Range (two single fields) | Start and end dates, also for approximate dates. If users may not remember the range, a date picker **must** be added | Date filters in search and list screens |
| With date picker | Dates far from today, when the weekday matters, or when nearby dates must be compared | Reservations, visit dates |

- **Do not use for**: relative dates ("within 5 days", "1 day later"); use a short text input or a select of the allowed options

**Rules**

| Rule | Strength | KWCAG | Check |
|------|----------|-------|-------|
| Give every date field a label and say which date to enter. For several fields, label year, month and day, with a description above | `R` | — | |
| State the date format in help text below the field; the placeholder may show `YYYY-MM-DD`, but the help text gives the digits and an example | `R` | — | Format is visible after typing starts |
| Match the field layout to the source document when asking for a date printed on it, and make it easy to paste | `G` | — | |
| Let the user enter an approximate date (month only, or a range) when the exact date is hard to remember | `R` | — | |
| Enable autofill for dates users enter often (birth date) | `G` | — | `autocomplete="bday"` |
| Let the user type the date with the keyboard even when a date picker exists; do not make the field disabled or read-only | `R` | 6.1.1 키보드 사용 보장 | Typing a date works without the picker |
| Label day, month and year fields precisely and link the labels programmatically | `R` | 7.3.2 레이블 제공 | |
| If a format is required, state it in help text | `R` | — (WCAG 3.3.2) | |

**Keyboard**: Click on the label or field places the cursor; Tab and Shift + Tab reach every field. The calendar has its own table (below).

**Markup**: required `.form-group`, `.form-tit`, `.calendar-input` (input area), `.form-btn-datepicker` (calendar button), `.form-hint`. The kit's script fills the field with the chosen date only if the input has the classes `datepicker cal`. Script `krds_calendar`: `init()`, `openDatePicker()`, `closeAllDatePickers()`, `toggleDateSelector()`.

```html
<div class="form-group">
  <div class="form-tit"><label for="visit">방문 희망일</label></div>
  <div class="form-conts calendar-conts">
    <div class="calendar-input">
      <input type="text" id="visit" class="krds-input datepicker cal" inputmode="numeric"
             placeholder="YYYY.MM.DD" aria-describedby="visit_hint">
      <button type="button" class="krds-btn medium icon form-btn-datepicker" aria-expanded="false">
        <span class="sr-only">달력 열기</span><i class="svg-icon ico-calendar"></i>
      </button>
    </div>
    <div class="krds-calendar-area"><!-- calendar --></div>
  </div>
  <p class="form-hint" id="visit_hint">숫자 8자리로 입력하세요. 예: 2026.11.06</p>
</div>
```

- `D`: KRDS's code uses `type="number"` with a `YYYY.MM.DD` placeholder; a number field cannot hold that text (the demo script switches the type). Use `type="text"` with `inputmode="numeric"`.
- `D`: the rule shows `YYYY-MM-DD` and the code `YYYY.MM.DD`. KRDS fixes neither; choose one separator for the whole site and state it in the help text.

## 달력 (calendar)

Shows date information and functions; also used as the date picker of 날짜 입력 필드.

- **Use for**: services offered on recurring dates; comparing several dates; checking or choosing dates near today
- **Do not use for**: information that is not updated regularly, or months with two or fewer events (KRDS names no alternative; `D`: a list)
- **Structure**: 1 year/month (optionally selectable), 2 previous/next buttons, 3 grid, 4 weekday headings, 5 dates (buttons), 6 today (with an identifier), 7 selected date (with an identifier), 8 unavailable dates (optional), 9 dates of the previous and next month, 10 events (optional)

**Rules**

| Rule | Strength | KWCAG | Check |
|------|----------|-------|-------|
| Represent date states (today, selected, inactive, unavailable) and legends (closed days, holidays) consistently wherever the calendar appears | `R` | — | |
| Distinguish states by more than text or background color: weight, underline, shape, extra identifiers; today and the selected date may carry text | `R` | — | |
| For complex events, provide a separate list or table, or switch to a week or day view | `R` | — | |
| Always provide weekday headings in the grid | `R` | — | `th` per weekday |
| Do not convey date meaning by color alone (underline, a border difference of 1 px or more, identifiers) | `R` | 5.4.1 색에 무관한 콘텐츠 인식 | |
| Give states and legends text for screen readers (일정 있음, 휴관일, 공휴일) | `R` | 5.1.1 적절한 대체 텍스트 제공 | Each marked date has an accessible description |
| Make every calendar function work with mouse, keyboard and touch | `R` | 6.1.1 키보드 사용 보장 | |
| Make the focus of every button and link in the calendar clearly visible | `R` | 6.1.2 초점 이동과 표시 | |

**Keyboard**

| Key | KRDS behavior |
|-----|---------------|
| Tab, Shift + Tab | Move through the calendar's controls in order |
| Click, Enter | Run the action button or follow the link |

- `D`: KRDS defines only Tab and Enter. In a grid of 28 to 31 buttons this is slow. Following the WAI-ARIA date picker dialog pattern, make the grid one Tab stop and move with the arrow keys, Home/End (week), PageUp/PageDown (month), and Esc to close and return focus to the calendar button.

**Markup**

| Part | Required | Optional |
|------|----------|----------|
| Whole area | `.calendar-conts` | |
| Calendar | `.krds-calendar-area` | Single date selection `.calendar-wrap.single` |
| Header (year, month, navigation) | `.calendar-head` | |
| Grid | `.calendar-body` | Selected `td.period.start.end`; unavailable `td.old`, `td.new`, `td.disabled`; event `td.day-event`; today `td.today`; holiday `td.day-off` |
| Footer | `.calendar-footer` | |

- The grid is `table.calendar-tbl` with a `caption` and weekday `th`; each date is `td > button.btn-set-date`. The footer holds 오늘, 취소, 확인. KRDS's script adds `aria-label` "N 오늘" and "N 일정있음", `aria-pressed` on selected dates, `aria-expanded` on the open button, and a focus trap while open; it returns focus to the open button on close.
- `D`: KRDS's structure says previous/next month dates "can be selected", but the selector table files `td.old`/`td.new` under unavailable dates and the demo disables them. Decide per service and make the state visible and announced.
- `D`: KRDS's script gives no text to holidays (`td.day-off`), against its own legend rule. Add it (for example `aria-label="25일 공휴일"`).

## 파일 업로드 (file upload)

For choosing and attaching one or more local files.

- **Structure**: 1 label or title (purpose of the upload), 2 description (optional), 3 help text (process, requirements, formats, sizes), 4 file selection button, 5 drop area, 6 counter (allowed and uploaded count), 7 file item (name, extension, size), 8 delete button, 9 status icon (spinner while uploading; success icon, which then turns into the delete button)

**Types**: single upload (one file, or unrelated files with one component each in separate sections) and multiple upload (related files, such as an album); by method, a file picker button, or drag and drop.

- **Do not use for**: multiple uploads in a modal (the file list grows vertically)

**Rules**

| Rule | Strength | KWCAG | Check |
|------|----------|-------|-------|
| Use file upload only when needed; do not ask for unnecessary files | `R` | — | |
| Label it so the user knows its purpose and exactly which file to submit | `G` | — | |
| State limits on file type, size and count in help text | `G` | — | |
| Restrict formats as little as possible, and allow every extension of a format (`.jpg`, `.jpeg`, `.jpe`) | `R` | — | |
| Restrict size as little as possible; if a limit is needed, set it so common files fit | `R` | — | |
| Consider automatic compression for image files with a size limit | `G` | — | |
| Keep the file selection button (or drop area) enabled after upload, so files can be added or changed. Use the disabled state only to block input itself | `G` | — | |
| Give the selection button a lower emphasis than the submit button | `G` | — | Not `.primary` next to a primary submit |
| Do not upload or store files before the user submits the form | `R` | — | No request on file selection |
| Give a specific error for each case: no file, wrong format, too large, empty, upload failed, too many files; others (password-protected, virus) if detected | `G` | — | |
| Do not wrap uploaded file names to two lines; truncate with an ellipsis | `R` | — | Full name available (for example `title`) |
| Give the upload an appropriate label that explains the purpose | `R` | 7.3.2 레이블 제공 | |
| Group each file item with its delete button (`p` for one file, `ul`/`li` for many) and link the delete button to the file name with `aria-describedby` | `R` | 5.3.2 콘텐츠의 선형구조 (KRDS: "콘텐츠의 선형화") | |
| Make keyboard focus on the selection button clearly visible | `R` | 6.1.2 초점 이동과 표시 | |
| Drag and drop must always come with a file picker that works with a single click and Enter | `R` | 6.1.1 키보드 사용 보장, 6.5.1 단일 포인터 입력 지원 (KRDS: "누르기 동작 지원") | |
| Hide the native `input type="file"` with a visually-hidden style that screen readers can still reach | `R` | — (WCAG 4.1.2) | Not `hidden`, `display:none` |

**Keyboard**

| Action | Keys |
|--------|------|
| Navigate | Tab reaches the selection button or drop area and each delete button; arrow keys move in the open file picker |
| Select files | Click, Space or Enter on the file and the picker's open button; dropping files in the drop area starts the upload |
| Delete | Click, Space or Enter on the delete button |

**Markup**: required `.krds-file-upload` (whole area), `.file-upload` (upload area), `.file-list` (uploaded files). Items are `ul.upload-list > li > .file-info` with `.file-name` and `.btn-wrap`; errors are `li.is-error` with `p.file-hint-invalid`.

```html
<div class="krds-file-upload">
  <div class="file-head"><h3 class="tit" id="up_tit">증빙서류 첨부</h3>
    <p id="up_hint">hwp, pdf, jpg 파일을 3개까지 첨부할 수 있습니다. 파일 크기는 20MB 미만이어야 합니다.</p></div>
  <div class="file-upload">
    <input type="file" id="up_file" class="sr-only" multiple aria-describedby="up_tit up_hint">
    <label for="up_file" class="krds-btn medium secondary">파일 선택</label>
  </div>
  <div class="file-list">
    <ul class="upload-list">
      <li class="is-error"><div class="file-info">
        <span class="file-name" id="f1">통장사본.pdf [pdf, 25MB]</span>
        <div class="btn-wrap"><button type="button" class="krds-btn medium text" aria-describedby="f1 f1_err">삭제</button></div>
      </div><p class="file-hint-invalid" id="f1_err">20MB 미만의 파일만 등록할 수 있습니다.</p></li>
    </ul>
  </div>
</div>
```

- `D`: KRDS's example uses the `hidden` attribute on the file input (removed from the accessibility tree, against its own rule), has no `aria-describedby` on delete buttons, and nests a `<button>` inside the `<label>`. The corrected example uses a visually hidden input with a label styled as a button. Keyboard focus then lands on the hidden input, so draw the focus ring on the label with `#up_file:focus-visible + label`; otherwise the "focus visible" rule fails.
- The client-side checks above are usability rules. Server-side checks of extension, size and storage location are required separately: see `secure-coding`, weakness 6 (위험한 형식 파일 업로드).
