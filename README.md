# skill-zip

**스킬집 (skill + 集)**: a collection of agent skills, organized by topic.

에이전트 스킬을 주제별로 모아 둔 저장소입니다.

## Layout

```
skill-zip/
└── <category>/
    └── <skill-name>/
        ├── SKILL.md
        └── references/
```

Each skill directory name matches the `name` field in its `SKILL.md` frontmatter.

스킬 폴더 이름은 `SKILL.md` frontmatter의 `name` 값과 같습니다.

## Skills

| Category | Skill | Description |
|----------|-------|-------------|
| frontend | [accessibility](frontend/accessibility/SKILL.md) | KWCAG 2.2, MACAG 2025, WCAG 2.2 A/AA, WAI-ARIA 1.2 reference for building and reviewing UI |

## License

[MIT](LICENSE). Standard names and requirement numbers (KS X OT0003, KS X 3253, WCAG, WAI-ARIA) belong to their respective publishers; this repository contains only summarized reference material.
