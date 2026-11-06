---
name: krds
description: KRDS (범정부 UI/UX 디자인시스템, Korea Design System) reference for building and reviewing Korean government web forms. Covers the KRDS form patterns (입력 폼, 개인 식별 정보 입력, 오류, 동의, 첨부파일, 확인, 도움), the input, selection, button and help components with their usability and accessibility rules, keyboard behavior and krds-* CSS classes, and the application (신청) and login service patterns with the 필수/권장/우수 checklist. Use this skill when building or reviewing forms for a Korean public-sector or government website (정부 누리집, 공공 웹사이트), when the user mentions KRDS, 범정부 디자인시스템, 디지털 정부 디자인 시스템, krds-* classes (krds-input, krds-btn, krds-form-check) or the HTML Component Kit, when designing sign-up, application (신청서), consent (약관 동의), login, file upload or date input screens for a Korean service, or when the user asks how KRDS says to handle labels, placeholders, errors, required fields or personal information fields.
---

# KRDS (범정부 UI/UX 디자인시스템)

Reference for building and reviewing web forms with KRDS, the Korean government's UI/UX design system published by the Ministry of the Interior and Safety (행정안전부) at www.krds.go.kr. Verified against the KRDS site as saved on 2026-11-06: Figma library v1.0.0 and HTML Component Kit v1.0.1 (pages first registered 2025-01-15; tag v1.0.3 and contextual help v1.0.4 updates included).

**Current scope: input forms.** This skill covers the form-related basic patterns, components and service patterns listed in the Quick Lookup table. Navigation, layout, identity (header, footer), design tokens and other KRDS areas are not yet included; say so instead of guessing.

KRDS material is provided under 공공누리 제1유형 (KOGL Type 1): commercial use and modification are allowed, and the source must be credited. Credit text suggested by KRDS: 본 저작물은 행정안전부에서 2024년 작성하여 공공누리 제1유형으로 개방한 '범정부 UI/UX 디자인시스템(KRDS)'을 이용하였으며, 해당 저작물은 'KRDS 디자인시스템 홈페이지(www.krds.go.kr)'에서 무료로 다운받으실 수 있습니다.

**Whether KRDS is mandatory for a given public website is unverified in this skill.** Ask the client for the project's requirements instead of stating an obligation.

## How to use

1. Decide the form type first (see `references/form-patterns.md`, "입력 폼"): single screen, modal, or step-by-step
2. Look up the task in the Quick Lookup table and read **only** the files it names
3. When **building**: follow the rules of the pattern, then of each component on the screen. Use the KRDS classes from the **Markup** part of each component and the corrected examples in this skill
4. When **reviewing**: go through the **Rules** table of each pattern and component on the screen, then the checklist in `references/application-flow.md` for application services

## Conventions

| Strength | Meaning | How to report in a review |
|----------|---------|---------------------------|
| `R` | KRDS states it as a requirement ("~해야 한다", "~안 된다", "~하지 않는다", "반드시"), it is a 필수 item of a service pattern checklist, or it is an accessibility rule tied to a KWCAG 2.2 item (unless KRDS words it as 권장 or 고려한다: then it is `G`) | Violation |
| `G` | KRDS states it as the normal way ("~한다", "권장", "~하는 것이 좋다"), or it is a 권장/우수 checklist item | Recommendation |
| `D` | This skill's judgment where KRDS is silent, inconsistent, or where its own example code breaks its own rules. The reason is given next to it | Recommendation, and say that it goes beyond KRDS |

- Report with the KRDS page name and the rule, for example "KRDS 텍스트 입력 필드: 플레이스홀더가 레이블이나 도움말의 대체 수단으로 사용되어서는 안 된다".
- KRDS accessibility rules cite KWCAG 2.2 items by name only. This skill adds the item number (for example 레이블 제공 = 7.3.2). If the `accessibility` skill is installed, its `references/cross-reference.md` maps them further to WCAG.
- **KRDS example code often breaks KRDS's own rules or skips what they recommend**: help text not linked with `aria-describedby`, groups without `fieldset`/`legend`, `autocomplete` missing where a rule requires it, `role="tooltip"` on popovers with buttons. Follow the rules, not the example markup. The examples in this skill are corrected.

## Quick Lookup

| Task | File to Load |
|------|-------------|
| Form layout, required/optional marking, action buttons, validation timing | `references/form-patterns.md` (입력 폼) |
| Name, birth date, gender, phone number fields; resident registration number, address, email (`D`) | `references/form-patterns.md` (개인 식별 정보 입력) |
| Error messages, consent (약관 동의), confirmation dialogs, downloadable attachments, help text | `references/form-patterns.md` |
| Text input, textarea, date input, calendar (date picker), file upload | `references/input-components.md` |
| Radio buttons, checkboxes, select, toggle switch, tags; which one to use | `references/selection-components.md` |
| Buttons, step indicator, contextual help, tooltip | `references/action-help.md` |
| Application (신청) service flow and its 53-item checklist, application form, confirm/submit step | `references/application-flow.md` |
| Login form (ID, password, show password, save login, errors) | `references/application-flow.md` (로그인 정보 입력) |

## Common field markup

KRDS builds every field from the same blocks:

| Block | Class | Notes |
|-------|-------|-------|
| Field group | `.form-group` | One label, one control, optional help |
| Label area | `.form-tit` | Holds `<label for>`; for a group, use `<legend>` instead (`D`) |
| Control area | `.form-conts` | Add `.is-error`, `.is-success` or `.is-information` for states |
| Help text | `p.form-hint` | Link it with `aria-describedby` (`D`: KRDS examples do not) |
| Messages | `p.form-hint-invalid`, `.form-hint-success`, `.form-hint-information` | Error text goes in `form-hint-invalid` |

Corrected field (`D`: KRDS's example has no `aria-describedby`, `aria-invalid` or `autocomplete`):

```html
<div class="form-group">
  <div class="form-tit"><label for="user_name">이름</label></div>
  <div class="form-conts is-error">
    <input type="text" id="user_name" class="krds-input" autocomplete="name"
           aria-describedby="user_name_hint user_name_error" aria-invalid="true">
  </div>
  <p class="form-hint" id="user_name_hint">개명한 경우 회원 정보에서 이름을 변경한 후 신청할 수 있습니다.</p>
  <p class="form-hint-invalid" id="user_name_error">이름을 입력해 주세요.</p>
</div>
```

## When building

1. Choose the form type and lay out sections with headings (`h2` to `h6`), one column by default
2. For each field, pick the component with the "Use for / Do not use for" lines of the component files
3. Give every control a visible `<label>` (or `<legend>` for groups), help text linked with `aria-describedby`, and `autocomplete` on personal data fields
4. Mark required or optional fields in one consistent way, validate on the client and always on the server, and keep the user's input after an error
5. Put the submit button at the right end of the action group, and disable it while the request is in flight

## When reviewing

1. Identify the form type and every pattern and component on the screen
2. Check each against its **Rules** table, including the KWCAG items. Then check keyboard behavior with the **Keyboard** tables
3. For application services, also go through the checklist in `references/application-flow.md`; report 필수 items first
4. Group findings: `R` violations first, then `G` and `D` recommendations. For each, give the element, the KRDS page and rule, and a fix

## Related skills

- `accessibility`: KWCAG 2.2 and WCAG detail for every accessibility rule cited here
- `secure-coding`: weakness 6 (file upload), 15 (hidden fields and client values), 29 (persistent cookies, "save login"), 33 (login attempt limits), and design criterion SR2-7 (sensitive data storage). Where KRDS and secure-coding seem to conflict (password autocomplete), see `references/application-flow.md`, "로그인 정보 입력"
