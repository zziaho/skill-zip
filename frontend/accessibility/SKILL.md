---
name: accessibility
description: Korean accessibility standards reference (KWCAG 2.2, which is based on WCAG 2.1, + MACAG 2025) with WCAG 2.2 Level A+AA and WAI-ARIA. Use this skill whenever building, modifying, or reviewing any UI component — forms, buttons, images, navigation, modals, media players, authentication flows, or any user-facing interface. Also use when auditing a page or screen for accessibility compliance, checking contrast ratios, verifying focus order, or reviewing ARIA usage. Triggers on any frontend/UI work including HTML, CSS, React, Vue, Angular, SwiftUI, Jetpack Compose, Flutter, or any framework that produces user-facing interfaces.
---

# Korean Accessibility Standards + WAI-ARIA

Reference covering KS X OT0003:2022 (KWCAG 2.2, web), KS X 3253:2025 (mobile), WAI-ARIA 1.2 roles/states/properties, and ARIA Authoring Practices Guide widget patterns. 64 unified requirements (covering all 33 KWCAG 2.2 requirements and WCAG 2.2 Level A/AA) + full ARIA reference.

## How to use

1. Identify what you're working on from the lookup table below
2. Read **only** the relevant reference file(s) — don't load everything
3. When **building**: follow the **Rule** column in each requirement table
4. When **reviewing**: use the **Test** column to verify compliance
5. For code snippets, read `references/patterns.md`

## Conventions

In the reference files:
- **Scope**: `W` = web only, `M` = mobile only, `WM` = both
- **Level**: WCAG conformance level (`A` / `AA` / `AAA`), for reference only. `AAA` items are optional even under WCAG AA
- **KWCAG**: KS X OT0003:2022 requirement number. KWCAG has **no A/AA levels: all 33 requirements are mandatory**. For Korean web accessibility compliance, treat every row with a KWCAG number as required, even if its Level is `AA`. `—` = no KWCAG requirement (still recommended by WCAG)
- Where KWCAG and WCAG differ, the Rule column states both (e.g., target size, contrast exceptions, skip link visibility)
- **Unified IDs are internal to this reference and are NOT WCAG success criterion numbers.** They often point to a different criterion than the same-looking WCAG number (e.g., unified 1.4.1 = WCAG 1.4.2 Audio Control; unified 1.4.4 = WCAG 1.4.11 Non-text Contrast). Never cite a unified ID alone in a report

## Quick Lookup

| Task | File to Load |
|------|-------------|
| Images, icons, alt text, CAPTCHA | `references/1-perceivable.md` |
| Video, audio, captions, transcripts | `references/1-perceivable.md` |
| Color, contrast, text sizing, spacing | `references/1-perceivable.md` |
| Tooltips, popovers, content shown on hover/focus | `references/1-perceivable.md` |
| Semantic structure, tables, reading order, orientation | `references/1-perceivable.md` |
| Instructions relying on shape/position/color/sound | `references/1-perceivable.md` |
| Keyboard/touch access, focus order, focus visible | `references/2-operable.md` |
| Touch target size, skip navigation | `references/2-operable.md` |
| Time limits, animation, auto-play control | `references/2-operable.md` |
| Flashing/seizure prevention | `references/2-operable.md` |
| Headings, page/frame titles, link text, navigation methods | `references/2-operable.md` |
| E-publication page numbers (paginated documents) | `references/2-operable.md` |
| Gestures, pointer input, drag alternatives | `references/2-operable.md` |
| Motion actuation, label-in-name | `references/2-operable.md` |
| Language declaration | `references/3-understandable.md` |
| Predictable behavior, popups, consistent UI | `references/3-understandable.md` |
| Forms, labels, error messages, error prevention | `references/3-understandable.md` |
| Authentication, repeated input | `references/3-understandable.md` |
| HTML validity, ARIA roles, name/role/value | `references/4-robust.md` |
| Status messages, AT compatibility | `references/4-robust.md` |
| ARIA roles, states, properties reference | `references/aria-roles.md` |
| Widget patterns (tabs, dialogs, menus, etc.) | `references/aria-patterns.md` |
| Code patterns and examples | `references/patterns.md` |
| Map to original KS/WCAG standard IDs, list of all 33 KWCAG items | `references/cross-reference.md` |

## When building UI

Before writing or modifying any user-facing component:

1. Look up the task above and read the relevant reference file
2. Apply every `WM` and platform-specific (`W` or `M`) requirement at your conformance level. For Korean web compliance, include every row with a KWCAG number
3. For custom widgets (tabs, menus, dialogs, trees, etc.), read `references/aria-patterns.md` for the correct ARIA + keyboard contract
4. For choosing roles and attributes, read `references/aria-roles.md`
5. Check `references/patterns.md` for copy-paste code snippets
6. **Prefer native HTML over ARIA** — a `<button>` is always better than `<div role="button">`. Use ARIA only when no native element provides the semantics you need

## When reviewing UI

For each component or page under review:

1. Read all 4 principle files (they're small — ~1,000-2,000 tokens each)
2. Walk through every requirement's **Test** column
3. Flag failures with the KWCAG number and/or WCAG SC number from `references/cross-reference.md`, not the unified ID alone (e.g., "Fails KWCAG 5.4.3 / WCAG 1.4.3: contrast ratio is 3.2:1, needs 4.5:1"). Add the unified ID in parentheses only as an internal pointer if useful
4. Use `references/cross-reference.md` to cite KWCAG item names or WCAG SC numbers in compliance reports. MACAG (mobile) numbers there are unverified; confirm against KS X 3253:2025 before citing

## Key numbers to remember

- Text contrast: **4.5:1** minimum (3:1 for 18pt+ or 14pt+ bold; KWCAG also allows 3:1 for zoomable text)
- UI component contrast: **3:1** minimum (WCAG only)
- Target size: **24x24 CSS px** minimum (WCAG); KWCAG recommends **6.0mm diagonal** + **1px** inner padding
- Auto-play sound: allowed only under **3 seconds**; longer sound must stop within 3s or via a key (e.g., Esc)
- Text resize: support up to **200%** without loss (WCAG only)
- Flashing: never **3-50 Hz**; flashing area ≤ **10%** of a 10-inch+ screen
- Time extension warning: at least **20 seconds** before expiry
- Text spacing: line-height **1.5x**, paragraph **2x**, letter **0.12x**, word **0.16x** (WCAG only)
