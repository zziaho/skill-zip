# skill-zip

[English](README.md) | **한국어**

**스킬집 (skill + 集)**: 에이전트 스킬을 주제별로 모아 둔 저장소입니다.

## 구조

```
skill-zip/
└── <카테고리>/
    └── <스킬 이름>/
        ├── SKILL.md
        ├── SKILL_ko.md
        └── references/
            ├── <파일>.md
            └── <파일>_ko.md
```

- 스킬 폴더의 이름은 `SKILL.md` frontmatter에 있는 `name` 값과 같습니다.
- 모든 문서는 영어 원본과 한국어 번역본을 함께 유지합니다. 한국어 파일은 원본 파일명 뒤에 `_ko`를 붙여서 만듭니다(예: `SKILL.md` / `SKILL_ko.md`). 한쪽을 수정하면 같은 커밋에서 다른 쪽도 함께 수정합니다.
- 한국어 파일은 [fluent-korean](https://github.com/snflkd/fluent-korean) 작성 지침을 따릅니다.
- 에이전트는 `SKILL.md`를 스킬의 진입점으로 불러옵니다. `SKILL_ko.md`는 사람이 읽기 위한 한국어 참조 문서입니다.

## 스킬 목록

| 카테고리 | 스킬 | 설명 |
|----------|------|------|
| frontend | [accessibility](frontend/accessibility/SKILL_ko.md) | 사용자 인터페이스를 구현하고 검토할 때 참조하는 KWCAG 2.2, MACAG 2025, WCAG 2.2 A/AA, WAI-ARIA 1.2 자료 |

## 라이선스

[MIT](LICENSE) 라이선스를 따릅니다. 표준의 명칭과 요구사항 번호(KS X OT0003, KS X 3253, WCAG, WAI-ARIA)에 대한 권리는 각 발행 기관에 있으며, 이 저장소에는 그 내용을 요약한 참조 자료만 들어 있습니다.
