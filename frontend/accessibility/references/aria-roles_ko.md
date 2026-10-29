# WAI-ARIA 1.2 역할, 상태, 속성

올바른 ARIA 역할과 속성을 고를 때 참고하는 빠른 참조 자료입니다. 출처는 W3C WAI-ARIA 1.2입니다.

**기본 원칙**: ARIA보다 네이티브 HTML 요소를 우선합니다. `<div role="button">`보다 `<button>`이 언제나 더 좋습니다. 필요한 의미를 제공하는 네이티브 요소가 없을 때에만 ARIA를 사용합니다.

## 랜드마크 역할

페이지의 영역을 구분할 때 사용합니다. 스크린 리더는 랜드마크를 빠른 탐색 수단으로 제공합니다.

| 역할 | 대응하는 HTML | 용도 |
|------|---------------|------|
| `banner` | `<header>` (최상위) | 사이트 전체의 헤더, 로고, 검색 |
| `navigation` | `<nav>` | 주요 내비게이션 링크 |
| `main` | `<main>` | 페이지의 주요 콘텐츠 |
| `complementary` | `<aside>` | 주요 콘텐츠와 관련된 보조 콘텐츠 |
| `contentinfo` | `<footer>` (최상위) | 저작권 표시, 개인정보처리방침 링크 |
| `search` | `<search>` | 검색 기능 |
| `region` | `<section>` (이름이 있는 경우) | 의미 있는 구역이며, 접근 가능한 이름이 필요합니다 |
| `form` | `<form>` (이름이 있는 경우) | 폼 랜드마크이며, 접근 가능한 이름이 필요합니다 |

같은 종류의 랜드마크가 여러 개 있다면, 각각에 고유한 `aria-label`을 지정합니다.

## 위젯 역할

| 역할 | 필수 속성 | 주요 상태 | 비고 |
|------|-----------|-----------|------|
| `button` | — | `aria-pressed`, `aria-expanded` | 네이티브 `<button>`을 대신 사용합니다 |
| `checkbox` | `aria-checked` | `true/false/mixed` | 네이티브 `<input type="checkbox">`를 대신 사용합니다 |
| `radio` | `aria-checked` | `true/false` | 반드시 `radiogroup` 안에 있어야 합니다 |
| `switch` | `aria-checked` | `true/false` (켜짐/꺼짐) | 토글 컨트롤입니다 |
| `combobox` | `aria-expanded`, `aria-controls` | `aria-autocomplete` | 입력 필드와 팝업 목록의 조합입니다 |
| `listbox` | — | `aria-multiselectable` | 선택할 수 있는 옵션의 목록입니다 |
| `option` | `aria-selected` | 기본값 `false` | `listbox`나 `combobox` 팝업의 자식 요소입니다 |
| `slider` | `aria-valuenow` | `aria-valuemin` (기본값 0), `aria-valuemax` (기본값 100), `aria-orientation` (기본값 horizontal) | 범위 입력 컨트롤입니다 |
| `spinbutton` | — | `aria-valuenow` (기본값 0), `aria-valuemin`, `aria-valuemax` (기본값: 제한 없음) | 숫자를 한 단계씩 바꾸는 컨트롤입니다 |
| `textbox` | — | `aria-multiline`, `aria-readonly` | 네이티브 `<input>`이나 `<textarea>`를 대신 사용합니다 |
| `searchbox` | — | `aria-autocomplete` | 네이티브 `<input type="search">`를 대신 사용합니다 |
| `tab` | — | `aria-selected` | 반드시 `tablist` 안에 있어야 합니다 |
| `tablist` | — | `aria-orientation` | `tab` 요소를 포함합니다 |
| `menu` | — | `aria-orientation` | `menuitem` 요소를 포함합니다 |
| `menubar` | — | `aria-orientation` | 가로 방향의 메뉴 막대입니다 |
| `menuitem` | — | `aria-haspopup`, `aria-expanded` | `menu`나 `menubar`의 자식 요소입니다 |
| `menuitemcheckbox` | `aria-checked` | `true/false/mixed` | 체크할 수 있는 메뉴 항목입니다 |
| `menuitemradio` | `aria-checked` | `true/false` | 라디오 방식의 메뉴 항목입니다 |
| `grid` | — | `aria-multiselectable`, `aria-readonly` | 조작할 수 있는 데이터 그리드입니다 |
| `gridcell` | — | `aria-selected`, `aria-readonly` | `grid` 안의 셀입니다 |
| `tree` | — | `aria-multiselectable` | 계층 구조로 된 목록입니다 |
| `treeitem` | — | `aria-expanded`, `aria-selected` | `tree` 안의 항목입니다 |
| `treegrid` | — | — | 트리와 그리드를 결합한 형태입니다 |
| `meter` | `aria-valuenow` | `aria-valuemin` (기본값 0), `aria-valuemax` (기본값 100), `aria-valuetext` | 알려진 범위 안의 값(디스크 사용량, 배터리 등)을 나타냅니다. 표시 전용이며, 네이티브 `<meter>`를 우선합니다 |
| `progressbar` | — | `aria-valuenow` (진행률을 알 수 없으면 생략), `aria-valuemin` (기본값 0), `aria-valuemax` (기본값 100), `aria-valuetext` | 작업 진행률을 나타냅니다 |
| `scrollbar` | `aria-controls`, `aria-valuenow` | `aria-valuemin` (기본값 0), `aria-valuemax` (기본값 100), `aria-orientation` (기본값 vertical) | 스크롤 컨트롤입니다 |
| `separator` (초점을 받는 경우) | `aria-valuenow` | `aria-valuemin` (기본값 0), `aria-valuemax` (기본값 100), `aria-orientation` (기본값 horizontal) | 크기를 조절하는 분할선입니다. 초점을 받지 않는 separator에는 값이 필요하지 않습니다 |
| `dialog` | 접근 가능한 이름 | `aria-modal` | 모달 또는 비모달 창입니다 |
| `alertdialog` | 접근 가능한 이름 | `aria-modal` | 긴급한 내용을 알리는 모달 대화상자입니다 |
| `toolbar` | — | `aria-orientation` | 컨트롤을 묶은 그룹입니다 |
| `tooltip` | — | — | 포인터를 올리거나 초점을 받았을 때 나타나는 정보 팝업입니다 |

## 문서 구조 역할

| 역할 | 용도 |
|------|------|
| `article` | 독립적인 콘텐츠(블로그 글, 댓글, 게시판 글) |
| `heading` | 구역의 제목이며, `aria-level`이 필요합니다 |
| `list` | `listitem` 요소를 담는 컨테이너 |
| `listitem` | `list` 안의 항목 |
| `table` | 데이터 표이며, `row`와 `rowgroup`을 포함합니다 |
| `row` | `table`이나 `grid` 안의 행 |
| `rowgroup` | 행의 묶음(thead, tbody, tfoot에 해당) |
| `img` | 이미지 컨테이너이며, 자식 요소가 있는 복잡한 이미지에 사용합니다 |
| `figure` | 캡션을 붙일 수 있는 도해 콘텐츠 |
| `group` | 관련된 요소를 묶는 일반 컨테이너 |
| `feed` | 스크롤할 수 있는 `article` 목록(무한 스크롤) |
| `math` | 수식 |
| `note` | 괄호 안의 내용이나 보충 설명 |
| `term` | 정의되는 단어나 구 |
| `definition` | 바로 앞에 있는 `term`의 정의 |
| `none`/`presentation` | 요소를 접근성 트리에서 제거합니다(장식용 요소에만 사용합니다) |

## 라이브 영역 역할

| 역할 | 동작 | 사용 사례 |
|------|------|-----------|
| `alert` | 암묵적으로 `aria-live="assertive"`, `aria-atomic="true"`가 적용됩니다 | 오류 메시지, 긴급 경고 |
| `status` | 암묵적으로 `aria-live="polite"`, `aria-atomic="true"`가 적용됩니다 | 검색 결과 개수, 저장 완료 알림 |
| `log` | 암묵적으로 `aria-live="polite"`가 적용되며, 추가된 내용을 읽어 줍니다 | 채팅 메시지, 이벤트 기록 |
| `timer` | 암묵적으로 `aria-live="off"`가 적용됩니다 | 카운트다운, 경과 시간 |
| `marquee` | 암묵적으로 `aria-live="off"`가 적용됩니다 | 주식 시세, 뉴스 자막 |

암묵적인 값과 중복되는 `aria-live`는 추가하지 않습니다(예: `role="alert" aria-live="assertive"`).

## 상태와 속성 빠른 참조

### 이름 지정

| 속성 | 유형 | 용도 |
|------|------|------|
| `aria-label` | property | 문자열로 접근 가능한 이름을 지정합니다 |
| `aria-labelledby` | property | 다른 요소의 ID로 접근 가능한 이름을 지정합니다 |
| `aria-describedby` | property | 다른 요소의 ID로 보충 설명을 지정합니다 |
| `aria-description` | property | 문자열로 보충 설명을 지정합니다. **ARIA 1.2에는 없는 속성**(ARIA 1.3 초안)이므로 `aria-describedby`를 우선합니다 |
| `aria-roledescription` | property | 사람이 읽을 수 있는 역할 이름을 지정합니다(예: "carousel", "slide"). 꼭 필요할 때만 사용합니다 |

### 상태 표시

| 속성 | 값 | 용도 |
|------|----|------|
| `aria-checked` | `true/false/mixed` | 체크박스, 라디오 버튼, 스위치의 상태 |
| `aria-selected` | `true/false` | 탭, 옵션, 그리드 셀의 선택 상태 |
| `aria-expanded` | `true/false` | 펼침 영역, 메뉴, 콤보 상자의 열림 상태 |
| `aria-pressed` | `true/false/mixed` | 토글 버튼의 상태 |
| `aria-disabled` | `true/false` | 조작할 수는 없지만 인식할 수는 있는 상태 |
| `aria-hidden` | `true/false` | 접근성 트리에서 제거 |
| `aria-invalid` | `true/false/grammar/spelling` | 폼 유효성 검사 상태 |
| `aria-busy` | `true/false` | 영역이 갱신되는 중인 상태 |
| `aria-current` | `page/step/location/date/time/true` | 집합 안에서 현재 항목 |

### 관계

| 속성 | 용도 |
|------|------|
| `aria-controls` | 이 요소가 제어하는 요소 |
| `aria-owns` | DOM 순서와 다른 부모·자식 관계 |
| `aria-activedescendant` | 복합 위젯 안에서 활성화된 자식 요소 |
| `aria-errormessage` | 오류 메시지를 담고 있는 요소 |
| `aria-details` | 자세한 설명을 담고 있는 요소 |
| `aria-flowto` | 다른 읽기 순서에서 다음에 오는 요소 |

### 값

| 속성 | 용도 |
|------|------|
| `aria-valuenow` | 현재 숫자 값 |
| `aria-valuemin` | 최솟값 |
| `aria-valuemax` | 최댓값 |
| `aria-valuetext` | 사람이 읽을 수 있는 값 텍스트 |
| `aria-placeholder` | 입력 힌트 텍스트 |

### 라이브 영역

| 속성 | 값 | 용도 |
|------|----|------|
| `aria-live` | `off/polite/assertive` | 갱신된 내용을 읽어 줍니다 |
| `aria-atomic` | `true/false` | 영역 전체를 읽을지, 바뀐 부분만 읽을지 정합니다 |
| `aria-relevant` | `additions/removals/text/all` | 어떤 변화를 읽어 줄지 정합니다 |

### 집합과 위치

| 속성 | 용도 |
|------|------|
| `aria-posinset` | 집합 안에서 항목의 위치(1부터 시작) |
| `aria-setsize` | 집합 안의 전체 항목 수 |
| `aria-level` | 계층 구조 안에서의 제목 수준 |
| `aria-colindex` | 열의 위치(1부터 시작) |
| `aria-rowindex` | 행의 위치(1부터 시작) |
| `aria-colspan` | 차지하는 열의 수 |
| `aria-rowspan` | 차지하는 행의 수 |
| `aria-colcount` | 그리드의 전체 열 수 |
| `aria-rowcount` | 그리드의 전체 행 수 |

### 위젯 속성

| 속성 | 용도 |
|------|------|
| `aria-autocomplete` | `none/inline/list/both`: 자동 완성 방식 |
| `aria-haspopup` | `false/true/menu/listbox/tree/grid/dialog`: 팝업의 종류 |
| `aria-modal` | `true/false`: 바깥 영역과의 상호작용을 막는지 여부 |
| `aria-multiline` | `true/false`: 여러 줄 입력 필드인지 여부 |
| `aria-multiselectable` | `true/false`: 여러 항목을 선택할 수 있는지 여부 |
| `aria-orientation` | `horizontal/vertical`: 배치 방향 |
| `aria-readonly` | `true/false`: 편집할 수 없는지 여부 |
| `aria-required` | `true/false`: 반드시 입력해야 하는지 여부 |
| `aria-sort` | `none/ascending/descending/other`: 열의 정렬 방식 |
