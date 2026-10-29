# ARIA Widget Patterns (APG)

Implementation patterns from W3C ARIA Authoring Practices Guide. Each section shows the minimum ARIA + keyboard contract for the widget. Source: https://www.w3.org/WAI/ARIA/apg/patterns/

## Accordion

```
Container: no special role
Header: <button aria-expanded="true/false" aria-controls="panel-id">
Panel:  <div id="panel-id" role="region" aria-labelledby="header-id">
```
Keys: `Enter/Space` toggle panel. Optional: `Up/Down` move between headers, `Home/End` first/last.

## Alert

```
<div role="alert">Message text</div>
```
Announced immediately (assertive). Do not require user action to dismiss. For confirmable alerts, use `alertdialog`.

## Dialog (Modal)

```
<div role="dialog" aria-modal="true" aria-labelledby="title-id">
  <h2 id="title-id">Dialog Title</h2>
  ...
  <button>Close</button>
</div>
```
Keys: `Tab/Shift+Tab` cycle within dialog (trap focus). `Escape` closes. On open, focus first interactive element. On close, return focus to trigger.

## Disclosure

```
<button aria-expanded="false" aria-controls="content-id">Show more</button>
<div id="content-id" hidden>Expanded content</div>
```
Keys: `Enter/Space` toggle. Toggle `hidden` and `aria-expanded` together.

## Tabs

```
<div role="tablist" aria-label="Label">
  <button role="tab" aria-selected="true" aria-controls="panel-1" id="tab-1">Tab 1</button>
  <button role="tab" aria-selected="false" aria-controls="panel-2" id="tab-2" tabindex="-1">Tab 2</button>
</div>
<div role="tabpanel" id="panel-1" aria-labelledby="tab-1">...</div>
<div role="tabpanel" id="panel-2" aria-labelledby="tab-2" hidden>...</div>
```
Keys: `Left/Right` (horizontal) or `Up/Down` (vertical) switch tabs. `Home` first tab. `End` last tab. Only active tab has `tabindex="0"`, others `-1`.

## Menu & Menu Button

```
<button aria-haspopup="true" aria-expanded="false" aria-controls="menu-id">Menu</button>
<ul role="menu" id="menu-id">
  <li role="menuitem">Action 1</li>
  <li role="menuitem">Action 2</li>
  <li role="menuitemcheckbox" aria-checked="false">Toggle</li>
</ul>
```
Keys: `Enter/Space/Down` open menu. `Up/Down` navigate items. `Enter/Space` activate. `Escape` close, return focus to button. Type-ahead: typing characters moves to matching item.

## Combobox

```
<label for="cb">Choose</label>
<input id="cb" role="combobox" aria-expanded="false" aria-controls="listbox-id" aria-autocomplete="list">
<ul role="listbox" id="listbox-id">
  <li role="option" aria-selected="false">Option 1</li>
</ul>
```
Keys: `Down` opens/navigates list. `Up` navigates up. `Enter` selects. `Escape` closes. `aria-activedescendant` tracks highlighted option without moving DOM focus.

## Listbox

```
<div role="listbox" aria-label="Choose items" aria-multiselectable="false" tabindex="0">
  <div role="option" aria-selected="true">Item 1</div>
  <div role="option">Item 2</div>
</div>
```
Keys: `Up/Down` navigate. `Home/End` first/last. `Enter/Space` select. Multi-select: `Shift+Down/Up` extend selection. Type-ahead supported.

## Radio Group

```
<div role="radiogroup" aria-label="Color">
  <div role="radio" aria-checked="true" tabindex="0">Red</div>
  <div role="radio" aria-checked="false" tabindex="-1">Blue</div>
  <div role="radio" aria-checked="false" tabindex="-1">Green</div>
</div>
```
Keys: `Right/Down` next radio. `Left/Up` previous. Selection follows focus. Only checked radio has `tabindex="0"`.

## Checkbox

```
<div role="checkbox" aria-checked="false" tabindex="0">Label text</div>
```
Keys: `Space` toggles. Tri-state: cycles `false → true → mixed`. Prefer native `<input type="checkbox">`.

## Slider

```
<div role="slider" aria-label="Volume" aria-valuenow="50" aria-valuemin="0" aria-valuemax="100" tabindex="0"></div>
```
Keys: `Right/Up` increase. `Left/Down` decrease. `Home` min. `End` max. `Page Up/Down` larger steps.

## Spinbutton

```
<div role="spinbutton" aria-label="Quantity" aria-valuenow="1" aria-valuemin="0" aria-valuemax="99" tabindex="0"></div>
```
Keys: `Up` increment. `Down` decrement. `Home` min. `End` max. Editable: direct number typing.

## Switch

```
<button role="switch" aria-checked="false">Dark mode</button>
```
Keys: `Enter/Space` toggle on/off. Update `aria-checked`.

## Grid

```
<table role="grid" aria-label="Data">
  <tr><th role="columnheader">Name</th></tr>
  <tr><td role="gridcell" tabindex="-1">Alice</td></tr>
</table>
```
Keys: `Arrow keys` navigate cells. `Enter` activate cell. `Tab` moves out of grid. Only one cell has `tabindex="0"` (roving tabindex).

## Tree View

```
<ul role="tree" aria-label="Files">
  <li role="treeitem" aria-expanded="true">
    Folder
    <ul role="group">
      <li role="treeitem">File.txt</li>
    </ul>
  </li>
</ul>
```
Keys: `Right` expand/enter child. `Left` collapse/go to parent. `Up/Down` navigate items. `Enter` activate. `Home/End` first/last visible.

## Toolbar

```
<div role="toolbar" aria-label="Formatting" aria-orientation="horizontal">
  <button tabindex="0">Bold</button>
  <button tabindex="-1">Italic</button>
  <button tabindex="-1">Underline</button>
</div>
```
Keys: `Left/Right` navigate tools. `Tab` moves out of toolbar. Roving tabindex within.

## Breadcrumb

```
<nav aria-label="Breadcrumb">
  <ol>
    <li><a href="/">Home</a></li>
    <li><a href="/products">Products</a></li>
    <li><a href="/products/shoes" aria-current="page">Shoes</a></li>
  </ol>
</nav>
```
Mark current page with `aria-current="page"`. Separator is CSS-only (not in DOM or announced).

## Carousel

```
<div role="region" aria-roledescription="carousel" aria-label="Featured">
  <div role="group" aria-roledescription="slide" aria-label="1 of 5">...</div>
  <button aria-label="Previous slide">◀</button>
  <button aria-label="Next slide">▶</button>
</div>
```
Auto-rotation must have a pause/start button, placed first in Tab order within the carousel. Rotation stops while any carousel element has keyboard focus or pointer hover. Prev/next are standard buttons (`Enter`/`Space`).

## Feed

```
<div role="feed" aria-label="News">
  <article aria-posinset="1" aria-setsize="-1">
    <h2>Title</h2>
    <p>Content...</p>
  </article>
</div>
```
Keys: `Page Down` next article. `Page Up` previous. `aria-setsize="-1"` when total unknown (infinite scroll). Announce `aria-busy="true"` during loading.

## Meter

```
<div role="meter" aria-label="Disk usage" aria-valuenow="75" aria-valuemin="0" aria-valuemax="100">75%</div>
```
No keyboard interaction needed (display only). Prefer native `<meter>` element.

## Link

```
<a href="/page">Text</a>         <!-- preferred -->
<span role="link" tabindex="0">Text</span>  <!-- only if <a> impossible -->
```
Keys: `Enter` activates. Always prefer native `<a>`.

## Tooltip

```
<button aria-describedby="tip-1">Save</button>
<div role="tooltip" id="tip-1">Save your changes</div>
```
Show on focus and hover; focus stays on the trigger (the tooltip never receives focus). `Escape` dismisses it. A keyboard-triggered tooltip hides on blur. A hover-triggered tooltip stays open while the pointer is over the trigger **or the tooltip itself**, so do not hide it on mouse-out of the trigger alone (WCAG 1.4.13, unified 1.4.10). No time-based auto-hide. Not interactive; for focusable content use a non-modal dialog. Note: the APG tooltip pattern is still marked work in progress.

## Window Splitter

```
<div role="separator" aria-valuenow="50" aria-valuemin="0" aria-valuemax="100" aria-label="Resize" tabindex="0"></div>
```
Keys: `Left/Right` or `Up/Down` resize. `Home` min. `End` max. `Enter` toggle between current and most recent previous position.
