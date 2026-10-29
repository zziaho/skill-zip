# WAI-ARIA 1.2 Roles, States & Properties

Quick reference for choosing correct ARIA roles and attributes. Source: W3C WAI-ARIA 1.2.

**Rule of thumb**: Prefer native HTML elements over ARIA. A `<button>` is always better than `<div role="button">`. Use ARIA only when no native element provides the semantics you need.

## Landmark Roles

Use these to define page regions. Screen readers expose them for quick navigation.

| Role | HTML Equivalent | Purpose |
|------|----------------|---------|
| `banner` | `<header>` (top-level) | Site-wide header, logo, search |
| `navigation` | `<nav>` | Major navigation links |
| `main` | `<main>` | Primary page content |
| `complementary` | `<aside>` | Supporting content related to main |
| `contentinfo` | `<footer>` (top-level) | Copyright, privacy links |
| `search` | `<search>` | Search functionality |
| `region` | `<section>` (with name) | Perceivable section; requires accessible name |
| `form` | `<form>` (with name) | Form landmark; requires accessible name |

If multiple landmarks of same type exist, give each a unique `aria-label`.

## Widget Roles

| Role | Required Attrs | Key States | Notes |
|------|---------------|------------|-------|
| `button` | — | `aria-pressed`, `aria-expanded` | Use native `<button>` instead |
| `checkbox` | `aria-checked` | `true/false/mixed` | Use native `<input type="checkbox">` instead |
| `radio` | `aria-checked` | `true/false` | Must be inside `radiogroup` |
| `switch` | `aria-checked` | `true/false` (on/off) | Toggle control |
| `combobox` | `aria-expanded`, `aria-controls` | `aria-autocomplete` | Input + popup list |
| `listbox` | — | `aria-multiselectable` | List of selectable options |
| `option` | `aria-selected` | default `false` | Child of `listbox` or `combobox` popup |
| `slider` | `aria-valuenow` | `aria-valuemin` (default 0), `aria-valuemax` (default 100), `aria-orientation` (default horizontal) | Range input |
| `spinbutton` | — | `aria-valuenow` (default 0), `aria-valuemin`, `aria-valuemax` (default: no limit) | Numeric stepper |
| `textbox` | — | `aria-multiline`, `aria-readonly` | Use native `<input>`/`<textarea>` instead |
| `searchbox` | — | `aria-autocomplete` | Use native `<input type="search">` instead |
| `tab` | — | `aria-selected` | Must be inside `tablist` |
| `tablist` | — | `aria-orientation` | Contains `tab` elements |
| `menu` | — | `aria-orientation` | Contains `menuitem` elements |
| `menubar` | — | `aria-orientation` | Horizontal menu strip |
| `menuitem` | — | `aria-haspopup`, `aria-expanded` | Child of `menu`/`menubar` |
| `menuitemcheckbox` | `aria-checked` | `true/false/mixed` | Checkable menu item |
| `menuitemradio` | `aria-checked` | `true/false` | Radio menu item |
| `grid` | — | `aria-multiselectable`, `aria-readonly` | Interactive data grid |
| `gridcell` | — | `aria-selected`, `aria-readonly` | Cell in `grid` |
| `tree` | — | `aria-multiselectable` | Hierarchical list |
| `treeitem` | — | `aria-expanded`, `aria-selected` | Item in `tree` |
| `treegrid` | — | — | Tree + grid hybrid |
| `meter` | `aria-valuenow` | `aria-valuemin` (default 0), `aria-valuemax` (default 100), `aria-valuetext` | Scalar value within a known range (disk usage, battery). Display only; prefer native `<meter>` |
| `progressbar` | — | `aria-valuenow` (omit when indeterminate), `aria-valuemin` (default 0), `aria-valuemax` (default 100), `aria-valuetext` | Task progress |
| `scrollbar` | `aria-controls`, `aria-valuenow` | `aria-valuemin` (default 0), `aria-valuemax` (default 100), `aria-orientation` (default vertical) | Scroll control |
| `separator` (focusable) | `aria-valuenow` | `aria-valuemin` (default 0), `aria-valuemax` (default 100), `aria-orientation` (default horizontal) | Resizable splitter; non-focusable separator needs no value |
| `dialog` | accessible name | `aria-modal` | Modal/non-modal window |
| `alertdialog` | accessible name | `aria-modal` | Urgent modal dialog |
| `toolbar` | — | `aria-orientation` | Group of controls |
| `tooltip` | — | — | Popup info on hover/focus |

## Document Structure Roles

| Role | Purpose |
|------|---------|
| `article` | Self-contained content (blog post, comment, forum post) |
| `heading` | Section heading; requires `aria-level` |
| `list` | Container for `listitem` elements |
| `listitem` | Item in a `list` |
| `table` | Data table; contains `row` and `rowgroup` |
| `row` | Row in `table`/`grid` |
| `rowgroup` | Group of rows (thead, tbody, tfoot equivalent) |
| `img` | Image container; use for complex images with child elements |
| `figure` | Illustrative content with optional caption |
| `group` | Generic container for related elements |
| `feed` | Scrollable list of `article` elements (infinite scroll) |
| `math` | Mathematical expression |
| `note` | Parenthetical or supplementary content |
| `term` | Word or phrase being defined |
| `definition` | Definition of preceding `term` |
| `none`/`presentation` | Remove element from accessibility tree (decorative only) |

## Live Region Roles

| Role | Behavior | Use Case |
|------|----------|----------|
| `alert` | Implicit `aria-live="assertive"`, `aria-atomic="true"` | Error messages, urgent warnings |
| `status` | Implicit `aria-live="polite"`, `aria-atomic="true"` | Search results count, save confirmation |
| `log` | Implicit `aria-live="polite"` (additions announced) | Chat messages, event log |
| `timer` | Implicit `aria-live="off"` | Countdown, elapsed time |
| `marquee` | Implicit `aria-live="off"` | Stock ticker, news crawl |

Do not add `aria-live` that duplicates the implicit value (e.g., `role="alert" aria-live="assertive"`).

## States & Properties Quick Reference

### Naming

| Attribute | Type | Use |
|-----------|------|-----|
| `aria-label` | property | Accessible name from string |
| `aria-labelledby` | property | Accessible name from element ID(s) |
| `aria-describedby` | property | Supplementary description from element ID(s) |
| `aria-description` | property | Supplementary description from string. **Not in ARIA 1.2** (ARIA 1.3 draft); prefer `aria-describedby` |
| `aria-roledescription` | property | Human-readable role name (e.g., "carousel", "slide"); use sparingly |

### State Indicators

| Attribute | Values | Use |
|-----------|--------|-----|
| `aria-checked` | `true/false/mixed` | Checkbox, radio, switch state |
| `aria-selected` | `true/false` | Tab, option, gridcell selection |
| `aria-expanded` | `true/false` | Disclosure, menu, combobox open state |
| `aria-pressed` | `true/false/mixed` | Toggle button state |
| `aria-disabled` | `true/false` | Non-operable but perceivable |
| `aria-hidden` | `true/false` | Remove from accessibility tree |
| `aria-invalid` | `true/false/grammar/spelling` | Form validation state |
| `aria-busy` | `true/false` | Region being updated |
| `aria-current` | `page/step/location/date/time/true` | Current item in set |

### Relationships

| Attribute | Use |
|-----------|-----|
| `aria-controls` | Element this one controls |
| `aria-owns` | Parent-child outside DOM order |
| `aria-activedescendant` | Active child in composite widget |
| `aria-errormessage` | Element containing error message |
| `aria-details` | Element with extended description |
| `aria-flowto` | Next in alternative reading order |

### Values

| Attribute | Use |
|-----------|-----|
| `aria-valuenow` | Current numeric value |
| `aria-valuemin` | Minimum value |
| `aria-valuemax` | Maximum value |
| `aria-valuetext` | Human-readable value text |
| `aria-placeholder` | Input hint text |

### Live Regions

| Attribute | Values | Use |
|-----------|--------|-----|
| `aria-live` | `off/polite/assertive` | Announce updates |
| `aria-atomic` | `true/false` | Announce entire region vs. changes only |
| `aria-relevant` | `additions/removals/text/all` | Which changes to announce |

### Set/Position

| Attribute | Use |
|-----------|-----|
| `aria-posinset` | Item position in set (1-based) |
| `aria-setsize` | Total items in set |
| `aria-level` | Heading level in hierarchy |
| `aria-colindex` | Column position (1-based) |
| `aria-rowindex` | Row position (1-based) |
| `aria-colspan` | Columns spanned |
| `aria-rowspan` | Rows spanned |
| `aria-colcount` | Total columns in grid |
| `aria-rowcount` | Total rows in grid |

### Widget Properties

| Attribute | Use |
|-----------|-----|
| `aria-autocomplete` | `none/inline/list/both` — completion behavior |
| `aria-haspopup` | `false/true/menu/listbox/tree/grid/dialog` — popup type |
| `aria-modal` | `true/false` — blocks outside interaction |
| `aria-multiline` | `true/false` — multi-line textbox |
| `aria-multiselectable` | `true/false` — multiple selection |
| `aria-orientation` | `horizontal/vertical` — layout direction |
| `aria-readonly` | `true/false` — not editable |
| `aria-required` | `true/false` — must complete |
| `aria-sort` | `none/ascending/descending/other` — column sort |
