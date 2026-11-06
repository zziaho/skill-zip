# Application and Login Service Patterns (신청, 로그인 서비스 패턴)

KRDS service patterns for forms: the application (신청) overview with its checklist, 신청서 작성, 확인/확정, and 로그인 정보 입력. All were first registered on 2025-01-15 (Figma v1.0.0, HTML Component Kit v1.0.1).

Service pattern rules carry a KRDS application level. This skill maps **필수 → `R`** and **권장, 우수 → `G`** (`SKILL.md`). KRDS: "the usability guidelines of service patterns are divided into three levels by importance and satisfaction from the user's point of view; core services must, at a minimum, meet the lowest level, 필수." KRDS does not define 권장 and 우수 further.

## 신청 개요 (application overview)

An application is a task in which the user fills in a form to tell an institution what they need. It covers every request by the user, not only the civil petitions (민원) named in law.

| Type | Meaning | Examples |
|------|---------|----------|
| 제출 (submit) | Fill in and submit a fixed form | Welfare benefits, moving-in report (전입신고), return report |
| 조회 (look up) | Check eligibility, document validity, results | Document authenticity, tax amount |
| 발급 (issue) | Issue certificates or numbers | Resident registration copy, customs clearance number, vehicle registration |
| 예약 (reserve) | Apply to use goods or services for a period | Books, seats, tickets |

**Flow**: 1 find the service (browse the list, select one or more, apply), 2 fill in the application (move between steps, enter data, autofill from verification or earlier input, help, form manuals, attach documents, several applications, temporary save), 3 confirm and submit (final check, confirm submission, cancel), 4 check the result (find the result screen, browse by date or status, check progress). The checklist adds three stages that are not in the flow: service information, notices and eligibility, and completion.

### Checklist

53 items: 필수 23, 권장 29, 우수 1. Report 필수 items as violations.

| Stage | Level | Guideline |
|-------|-------|-----------|
| Find the service | 권장 | Sort the service list in a way that suits the service |
| Find the service | 권장 | Cluster the list and give it metadata |
| Find the service | **필수** | Show the application status (open, closed) clearly |
| Find the service | 권장 | Show the application period in previews and summaries |
| Find the service | **필수** | Use the official service name as the title |
| Find the service | **필수** | Do not truncate titles with an ellipsis |
| Find the service | 권장 | Keep preview and summary text short |
| Find the service | 권장 | Offer an action button that starts the application without the detail screen |
| Find the service | 권장 | Give clear visual cues on buttons that go to external services or open new windows |
| Service information | 권장 | Use the service name as the title of the body |
| Service information | **필수** | Write details concisely and clearly |
| Service information | **필수** | Keep details accurate and up to date |
| Service information | **필수** | List every channel for applying and its restrictions |
| Service information | **필수** | Make it clear when online application is not possible |
| Service information | **필수** | List every form and document needed, with quick access to them |
| Service information | **필수** | Explain the application process and handling procedure |
| Service information | 권장 | Give the usual time for each stage |
| Service information | 권장 | Offer other helpful information |
| Service information | 권장 | Show basic information on one screen |
| Service information | **필수** | Show basic information in the first tab |
| Service information | 권장 | Let the user open extra information when needed |
| Service information | 권장 | Every link goes to the screen its label names |
| Service information | 권장 | Keep the user's browsing context after "back to list" or the browser's back action |
| Notices and eligibility | 권장 | Make notices and eligibility checks the first step of the application form |
| Notices and eligibility | **필수** | Tell the user clearly about situations that will force them to stop midway or at the last step |
| Notices and eligibility | 권장 | Show information by importance and hierarchy |
| Notices and eligibility | 권장 | Leave out information needed during later steps or after completion |
| Application form | **필수** | Do not split form sections within one step into tabs or accordions |
| Application form | 권장 | Put fields that affect earlier fields or steps into those earlier fields or steps |
| Application form | **필수** | Tell the user when a value changes earlier fields or steps |
| Application form | 권장 | Use the administrative information sharing system (행정정보 공동이용) to minimize attached documents |
| Application form | 권장 | Offer temporary save for multi-step or long applications |
| Application form | 권장 | Explain field labels |
| Application form | **필수** | Offer several ways to get help with the form |
| Application form | 권장 | Give help in context |
| Application form | **필수** | Make help accurate |
| Application form | **필수** | Distinguish the reset button clearly from other buttons |
| Confirm and submit | **필수** | Include a confirm step when the application cannot be cancelled, withdrawn or edited after submission |
| Confirm and submit | 권장 | Summarize the key information entered |
| Confirm and submit | **필수** | State clearly what cannot be cancelled or edited |
| Confirm and submit | **필수** | Offer both a confirm and a cancel button |
| Completion | **필수** | Every application has a completion step |
| Completion | 권장 | Summarize the key information entered |
| Completion | 권장 | Link to the screen where the result can be checked |
| Completion | 우수 | For services used repeatedly, offer a button to do the same task again |
| Completion | 권장 | Link to related services |
| Check the result | 권장 | Use an intuitive label for links to the result screen |
| Check the result | **필수** | Provide the application details |
| Check the result | **필수** | Provide the application history |
| Check the result | 권장 | Structure the history so it is easy to read |
| Check the result | 권장 | Offer sorting |
| Check the result | **필수** | Show the procedure and the current status |
| Check the result | 권장 | Offer bulk selection |

## 신청서 작성 (application form)

Stage 2 of the application flow.

**Structure**: 1 title (purpose of the form), 2 description (optional; overall notes), 3 input form, 4 step indicator (for multi-step applications), 5 help panel (help, related links, contact information), 6 annotation icon (opens the help panel).

**Rules**

| Rule | Level | Strength | KWCAG | Check |
|------|-------|----------|-------|-------|
| Do not split sections within one step into tabs or accordions; users may not notice them and miss fields | 필수 | `R` | — | |
| If a later field resets or changes an earlier field's value or requirement, design the order so the influencing field comes first | 권장 | `G` | — | |
| If that order is impossible, tell the user with an inline message that an earlier field has changed | 필수 | `R` | — | |
| Tell the user which documents are handled through 행정정보 공동이용 and need not be attached | 권장 | `G` | — | |
| Offer temporary save; do not assume the form is finished in one session | 권장 | `G` | — | |
| Use plain words in labels; explain unavoidable terms with help components | 권장 | `G` | — | |
| Offer at least one way to get help, including contact information: phone, email, chatbot; help components (annotation, help panel, coach mark); FAQ; example filled-in forms | 필수 | `R` | — | |
| Put help on the field itself, not in a notice section at the top or below the form | 권장 | `G` | — | |
| Make help accurate: no typos, official names, links that go where their labels say | 필수 | `R` | — | |
| Separate the reset button visually and spatially from other buttons | 필수 | `R` | — | |
| Let screen readers identify the current step (`aria-current`, or "현재 단계" text) | — | `R` | 5.1.1 적절한 대체 텍스트 제공 (as cited by KRDS; WCAG 4.1.2) | |
| Give form sections `h2` to `h6` headings, so users can skip by section | — | `R` | 6.4.2 제목 제공 | |

- KRDS calls "several ways to get help" 필수 but its description says one or more ways "is desirable". `D`: treat contact information as the minimum.

## 확인/확정 (confirm and submit)

Stage 3 of the application flow: the last step before completion.

**Structure**: 1 title (summary of the requested action), 2 description (optional), 3 information to confirm, 4 actions (submit, or stop and return to the form).

**Types**: modal (little key information, no scrolling needed) or single screen (much information that needs structure). On a single screen in a multi-step application, a step indicator is recommended.

**Rules**

| Rule | Level | Strength | Check |
|------|-------|----------|-------|
| Include a confirm step when the application cannot be cancelled, withdrawn or edited after submission. Issue-type services that can be repeated may omit it | 필수 | `R` | |
| Summarize only the key information: contact details for the reply, items that cannot be changed (for example the romanized name of a passport application), items that affect the review (for example income) | 권장 | `G` | |
| State in the title, heading or description that the application cannot be cancelled or edited | 필수 | `R` | The text is present, not only implied |
| Offer both a confirm button and a cancel button that returns to the form | 필수 | `R` | |

- KRDS gives no accessibility rules for this page. For the modal type, apply the dialog rules in `form-patterns.md` (확인).

## 로그인 정보 입력 (login)

The account information step of the login pattern.

**Structure**: 1 labels, 2 account fields, 3 "save login" checkbox (ID, password, or both), 4 find ID and reset password links, 5 help (about entering account data or login methods).

**Rules**

| Rule | Level | Strength | KWCAG | Check |
|------|-------|----------|-------|-------|
| Give the ID format in advance (for example, when the ID is an email address), in the label or help text, not in a placeholder | 필수 | `R` | — | |
| Offer an option to show the password; hide it by default | 필수 | `R` | — | |
| Do not restrict copy and paste | 필수 | `R` | — | Pasting into the password field works |
| Offer to save the recent or preferred login method; optionally say what is saved (ID, password) and for how long | 우수 | `G` | — | |
| Put find-ID and reset-password links around the form | 필수 | `R` | — | |
| Make error messages clear and short, saying what went wrong and how to fix it | 필수 | `R` | — | |
| Move focus in a logical order: not to the login button before the password, and not to "save" options after the login button | — | `R` | 6.1.2 초점 이동과 표시, 5.3.2 콘텐츠의 선형구조 (KRDS: "콘텐츠의 선형 구조") | |
| Set the `autocomplete` attribute on the fields | — | `R` | — (KRDS cites WCAG 1.3.5) | |
| Validate as much as possible before submission: on focus loss, input errors such as invalid characters and empty fields **must** be checked | — | `R` | — | |
| On a server-side error, reload the screen, clear the password field, return the user to the user name field, and show inline messages with a clear fix | — | `R` | — | |
| In mobile apps with biometric login, offer automatic login (on the login screen or right after login); the default follows the institution's security policy | — | `G` | — | |

```html
<form method="post" action="/login">
  <div class="form-group">
    <div class="form-tit"><label for="login_id">아이디(이메일)</label></div>
    <div class="form-conts"><input type="email" id="login_id" class="krds-input" autocomplete="username"></div>
  </div>
  <div class="form-group">
    <div class="form-tit"><label for="login_pw">비밀번호</label></div>
    <div class="form-conts btn-ico-wrap">
      <input type="password" id="login_pw" class="krds-input" autocomplete="current-password">
      <button type="button" class="krds-btn medium icon" aria-pressed="false"><span class="sr-only">비밀번호 표시</span></button>
    </div>
  </div>
  <div class="krds-form-check"><input type="checkbox" id="save_id"><label for="save_id">아이디 저장</label></div>
  <button type="submit" class="krds-btn large primary">로그인</button>
  <a href="/find-id">아이디 찾기</a> <a href="/reset-pw">비밀번호 재설정</a>
</form>
```

**Password autofill and secure-coding** (`D`)

KRDS asks for `autocomplete` on login fields and forbids blocking paste. The Ministry's 2021 development security guide (`secure-coding`, design criterion SR2-7) asks for `autocomplete="off"` on forms that take credentials. This skill follows KRDS:

- KWCAG 2.2 7.3.3 접근 가능한 인증 requires that authentication not depend on memorizing or transcribing; password managers and paste are the usual way to meet it.
- Most current browsers ignore `autocomplete="off"` on login fields anyway, so it does not achieve what SR2-7 intends.
- Use `autocomplete="username"`, `"current-password"` (login) or `"new-password"` (sign-up, change). If a diagnoser cites SR2-7, explain the choice with KWCAG 7.3.3 and KRDS, and record it in the project's security design.

**Security rules KRDS does not cover** (`D`)

| Topic | Use |
|-------|-----|
| Error message content | Say that the ID or password is incorrect, without saying which, so that IDs cannot be enumerated. This still meets KRDS's "clear and specific" rule if it says how to recover (find ID, reset password) |
| Attempt limits, account lock, CAPTCHA | `secure-coding` weakness 33 and design criterion SR2-2 |
| Password rules | `secure-coding` weakness 26 and design criterion SR2-3 |
| "Save login" cookies | Keep lifetimes short and store no credentials in them: `secure-coding` weakness 29 |
