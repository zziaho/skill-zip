---
name: accessibility
description: 한국 접근성 표준(WCAG 2.1을 기반으로 하는 KWCAG 2.2와 MACAG 2025)과 WCAG 2.2 Level A/AA, WAI-ARIA를 다루는 참조 스킬입니다. 폼, 버튼, 이미지, 내비게이션, 모달, 미디어 플레이어, 인증 절차처럼 사용자가 직접 조작하는 인터페이스 컴포넌트를 만들거나 수정하거나 검토할 때 항상 이 스킬을 사용합니다. 페이지나 화면이 접근성 기준을 준수하는지 진단할 때, 명도 대비를 확인할 때, 초점 순서를 검증할 때, ARIA 사용 방식을 검토할 때에도 사용합니다. HTML, CSS, React, Vue, Angular, SwiftUI, Jetpack Compose, Flutter 등 사용자 인터페이스를 만드는 모든 프론트엔드 작업에서 이 스킬이 호출됩니다.
---

# 한국 접근성 표준 + WAI-ARIA

이 스킬은 KS X OT0003:2022(KWCAG 2.2, 웹), KS X 3253:2025(모바일), WAI-ARIA 1.2의 역할·상태·속성, ARIA Authoring Practices Guide(APG)의 위젯 패턴을 다룹니다. 통합 요구사항 64개(KWCAG 2.2의 요구사항 33개와 WCAG 2.2 Level A/AA를 모두 포함)와 ARIA 참조 자료 전체를 제공합니다.

## 사용 방법

1. 아래 조회표에서 지금 진행하는 작업에 해당하는 항목을 찾습니다.
2. 관련된 참조 파일**만** 읽습니다. 모든 파일을 한꺼번에 불러오지 않습니다.
3. **구현**할 때는 각 요구사항 표의 **규칙** 열을 따릅니다.
4. **검토**할 때는 **검사 방법** 열로 준수 여부를 확인합니다.
5. 코드 예제가 필요하면 `references/patterns_ko.md`를 읽습니다.

## 표기 규칙

참조 파일에서는 다음과 같은 표기를 사용합니다.

- **범위**: `W`는 웹 전용, `M`은 모바일 전용, `WM`은 웹과 모바일 모두에 적용된다는 뜻입니다.
- **수준**: WCAG 적합성 수준(`A` / `AA` / `AAA`)이며, 참고용으로만 표기합니다. `AAA` 항목은 WCAG AA를 목표로 하는 경우에도 선택 사항입니다.
- **KWCAG**: KS X OT0003:2022의 요구사항 번호입니다. KWCAG에는 **A/AA 수준이 없으며, 33개 요구사항이 모두 필수**입니다. 한국 웹 접근성을 준수해야 한다면, 수준이 `AA`로 표기되어 있더라도 KWCAG 번호가 있는 모든 행을 필수로 취급합니다. `—`는 대응하는 KWCAG 요구사항이 없다는 뜻입니다(WCAG에서는 여전히 권장됩니다).
- KWCAG와 WCAG의 기준이 서로 다른 경우에는 규칙 열에 두 기준을 함께 적었습니다(예: 대상 크기, 명도 대비 예외, 건너뛰기 링크의 표시 여부).
- **통합 ID는 이 참조 자료 안에서만 사용하는 번호이며, WCAG 성공 기준 번호가 아닙니다.** 통합 ID는 형태가 같은 WCAG 번호와 다른 기준을 가리키는 경우가 많습니다(예: 통합 1.4.1은 WCAG 1.4.2 Audio Control이고, 통합 1.4.4는 WCAG 1.4.11 Non-text Contrast입니다). 보고서에는 통합 ID만 단독으로 적지 않습니다.

## 조회표

| 작업 | 읽을 파일 |
|------|-----------|
| 이미지, 아이콘, 대체 텍스트, CAPTCHA | `references/1-perceivable_ko.md` |
| 동영상, 오디오, 자막, 대본 | `references/1-perceivable_ko.md` |
| 색상, 명도 대비, 텍스트 크기, 간격 | `references/1-perceivable_ko.md` |
| 툴팁, 팝오버, 마우스를 올리거나 초점을 받을 때 나타나는 콘텐츠 | `references/1-perceivable_ko.md` |
| 의미 구조, 표, 읽기 순서, 화면 방향 | `references/1-perceivable_ko.md` |
| 모양, 위치, 색상, 소리에 의존하는 지시사항 | `references/1-perceivable_ko.md` |
| 키보드·터치 접근, 초점 순서, 초점 표시 | `references/2-operable_ko.md` |
| 터치 대상 크기, 건너뛰기 링크 | `references/2-operable_ko.md` |
| 시간 제한, 애니메이션, 자동 재생 제어 | `references/2-operable_ko.md` |
| 깜빡임과 번쩍임으로 인한 발작 예방 | `references/2-operable_ko.md` |
| 제목, 페이지·프레임 제목, 링크 텍스트, 탐색 방법 | `references/2-operable_ko.md` |
| 전자출판물(쪽 단위 문서)의 쪽 번호 | `references/2-operable_ko.md` |
| 제스처, 포인터 입력, 드래그 대체 수단 | `references/2-operable_ko.md` |
| 동작 기반 작동, 레이블과 네임 | `references/2-operable_ko.md` |
| 언어 선언 | `references/3-understandable_ko.md` |
| 예측 가능한 동작, 팝업, 일관된 사용자 인터페이스 | `references/3-understandable_ko.md` |
| 폼, 레이블, 오류 메시지, 오류 예방 | `references/3-understandable_ko.md` |
| 인증, 반복 입력 | `references/3-understandable_ko.md` |
| HTML 유효성, ARIA 역할, 이름·역할·값 | `references/4-robust_ko.md` |
| 상태 메시지, 보조기술 호환성 | `references/4-robust_ko.md` |
| ARIA 역할, 상태, 속성 참조 | `references/aria-roles_ko.md` |
| 위젯 패턴(탭, 대화상자, 메뉴 등) | `references/aria-patterns_ko.md` |
| 코드 패턴과 예제 | `references/patterns_ko.md` |
| 원래의 KS·WCAG 표준 번호와 대응, KWCAG 33개 항목 전체 목록 | `references/cross-reference_ko.md` |

## 사용자 인터페이스를 구현할 때

사용자가 직접 보거나 조작하는 컴포넌트를 작성하거나 수정하기 전에 다음 절차를 따릅니다.

1. 위 조회표에서 작업을 찾고, 관련된 참조 파일을 읽습니다.
2. 목표로 하는 적합성 수준에 해당하는 `WM` 요구사항과 플랫폼별(`W` 또는 `M`) 요구사항을 모두 적용합니다. 한국 웹 접근성을 준수해야 한다면 KWCAG 번호가 있는 모든 행을 포함합니다.
3. 탭, 메뉴, 대화상자, 트리 같은 커스텀 위젯을 만든다면, `references/aria-patterns_ko.md`를 읽고 올바른 ARIA 구성과 키보드 동작을 확인합니다.
4. 역할과 속성을 선택할 때에는 `references/aria-roles_ko.md`를 읽습니다.
5. 바로 가져다 쓸 수 있는 코드 예제는 `references/patterns_ko.md`에서 확인합니다.
6. **ARIA보다 네이티브 HTML을 우선합니다.** `<div role="button">`보다 `<button>`이 언제나 더 좋습니다. 필요한 의미를 제공하는 네이티브 요소가 없을 때에만 ARIA를 사용합니다.

## 사용자 인터페이스를 검토할 때

검토 대상인 컴포넌트나 페이지마다 다음 절차를 따릅니다.

1. 4대 원칙 파일을 모두 읽습니다. 각 파일은 1,000~2,000토큰 정도로 작습니다.
2. 모든 요구사항의 **검사 방법** 열을 차례대로 확인합니다.
3. 위반 사항은 통합 ID만 단독으로 적지 말고, `references/cross-reference_ko.md`에서 찾은 KWCAG 번호나 WCAG SC 번호로 표기합니다(예: "KWCAG 5.4.3 / WCAG 1.4.3 위반: 명도 대비가 3.2:1이며, 4.5:1 이상이어야 함"). 통합 ID는 내부 참조용으로 필요할 때만 괄호 안에 덧붙입니다.
4. 준수 보고서에 KWCAG 항목명이나 WCAG SC 번호를 인용할 때에는 `references/cross-reference_ko.md`를 사용합니다. 이 파일에 있는 MACAG(모바일) 번호는 검증되지 않았으므로, 인용하기 전에 KS X 3253:2025 원문과 대조해야 합니다.

## 기억해야 할 핵심 수치

- 텍스트 명도 대비: 최소 **4.5:1**입니다(18pt 이상 또는 14pt 이상 굵은 글꼴은 3:1이며, KWCAG는 확대할 수 있는 텍스트에도 3:1을 허용합니다).
- 사용자 인터페이스 구성요소의 명도 대비: 최소 **3:1**입니다(WCAG에만 해당합니다).
- 대상 크기: 최소 **24x24 CSS px**입니다(WCAG). KWCAG는 대각선 길이 **6.0mm** 이상과 내부 여백 **1px** 이상을 권장합니다.
- 자동 재생되는 소리: **3초 미만**일 때만 허용됩니다. 그보다 긴 소리는 3초 안에 멈추거나, Esc 같은 키로 멈출 수 있어야 합니다.
- 텍스트 확대: 내용이 손실되지 않고 **200%**까지 확대할 수 있어야 합니다(WCAG에만 해당합니다).
- 번쩍임: 초당 **3~50회** 번쩍이는 콘텐츠는 절대 사용하지 않습니다. 번쩍이는 영역은 10인치 이상 화면의 **10%** 이하여야 합니다.
- 시간 연장 경고: 시간이 만료되기 최소 **20초** 전에 알려야 합니다.
- 텍스트 간격: 줄 간격 **1.5배**, 문단 간격 **2배**, 자간 **0.12배**, 단어 간격 **0.16배**입니다(WCAG에만 해당합니다).
