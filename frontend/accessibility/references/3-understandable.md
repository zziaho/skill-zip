# 3. Understandable (이해의 용이성)

Content and UI operation must be understandable regardless of user ability.

`KWCAG` column: KS X OT0003:2022 item number. Every row with a number is **mandatory** for Korean web accessibility compliance, regardless of `Level`. `—` = no corresponding KWCAG item.

## 3.1 Readability (가독성)

| ID | Rule | Test | Scope | Level | KWCAG |
|----|------|------|-------|-------|-------|
| 3.1.1 | Declare the primary language of the page/app so assistive tech selects correct voice/braille module | Web: html element has valid lang attribute. Mobile: app language setting matches content language | WM | A | 7.1.1 |
| 3.1.2 | Mark passages in a different language from the page default | Web: span/div with lang attribute on foreign-language text. Mobile: language metadata on mixed-language sections | WM | AA | — |

## 3.2 Predictability (예측 가능성)

| ID | Rule | Test | Scope | Level | KWCAG |
|----|------|------|-------|-------|-------|
| 3.2.1 | No auto-execution of functions on focus. Receiving focus must not trigger: form submission, new window, menu item execution, or focus relocation. Exceptions: visual changes (highlight, border) and additional info shown without moving focus are OK | Tab to every control; no unintended actions fire on focus alone | WM | A | 7.2.1 |
| 3.2.2 | Selecting a value in a control (combo box, radio, checkbox) must not auto-submit or execute; require an accompanying submit button. Exceptions: visual-only changes are OK | Change dropdown/radio/checkbox values; verify no auto-submission or navigation | WM | A | 7.2.1 |
| 3.2.3 | New windows/popups must not open in situations users cannot predict. Layer popups are discouraged (they tend to break focus order and linear structure). When a window/popup/layer popup has focus, its close button or close action must actually close it | Check for unexpected popups; verify close works; verify focus management | WM | A | 7.2.1 |
| 3.2.4 | Repeated UI components appear in same position and use same appearance/name across pages | Check header, nav, footer across pages; same layout, labels, and order | WM | AA | — |
| 3.2.5 | Same-function components use identical visual design and naming | Find duplicate functions (e.g., search on multiple pages); verify same icon, label, behavior | WM | AA | — |
| 3.2.6 | If help is provided (contact details, contact methods like chat/board/SNS, FAQ/how-to, chatbot), at least one is reachable in the same relative order on each page | Navigate multiple pages; verify help links/buttons appear in consistent relative order | WM | A | 7.2.2 |

## 3.3 Input Assistance (입력 도움)

| ID | Rule | Test | Scope | Level | KWCAG |
|----|------|------|-------|-------|-------|
| 3.3.1 | On input error: tell users where the error occurred and why, in text. Moving focus to the error or giving an error summary first helps. Does not apply to system/platform errors | Submit form with missing/invalid fields; verify error message names the field and explains the issue | WM | A | 7.3.1 |
| 3.3.2 | Every input has a label that is programmatically associated so AT can recognize it. Label clearly describes the input purpose | Check every input has a label; verify association (for/id, aria-labelledby, or wrapping label element) | WM | A | 7.3.2 |
| 3.3.3 | For important submissions (legal, financial, data deletion, test submission): provide cancel, edit/review, or confirmation step before final submission | Test checkout/delete/submit flows; verify at least one safeguard (undo, review, confirm dialog) | WM | AA | — |
| 3.3.4 | Within a process, information already entered or provided must be auto-filled or selectable (e.g., "same as orderer address"). Exception: re-entry required for security (passwords) | Check multi-step forms; verify previously entered data carries forward or is selectable | WM | A | 7.3.4 |
| 3.3.5 | Authentication must not rely solely on cognitive function tests (passwords, touch patterns, memorizing strings, calculation, image object recognition). Provide at least one alternative: form markup that lets the browser save ID/password, OAuth third party, biometrics, or possession-based (phone, USB). The user's own name/email/phone are not cognitive tests | Test login flow; verify at least one non-cognitive auth method available | WM | AA | 7.3.3 |
| 3.3.6 | If an input error is automatically detected and correction suggestions are known, provide the suggestions, unless doing so would jeopardize security or the purpose of the content (e.g., a test) | Enter invalid formats (date, email, phone); error message tells how to fix it (e.g., "YYYY-MM-DD 형식으로 입력하세요") | WM | AA | — |
