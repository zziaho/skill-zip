# skill-zip

**English** | [한국어](README_ko.md)

**스킬집 (skill + 集)**: a collection of agent skills, organized by topic.

## Layout

```
skill-zip/
└── <category>/
    └── <skill-name>/
        ├── SKILL.md
        ├── SKILL_ko.md
        └── references/
            ├── <file>.md
            └── <file>_ko.md
```

- Each skill directory name matches the `name` field in its `SKILL.md` frontmatter.
- Every document is maintained in two languages: the English original and a Korean version with `_ko` appended to the file name (e.g., `SKILL.md` / `SKILL_ko.md`). When you change one, update the other in the same commit.
- Korean files follow the [fluent-korean](https://github.com/snflkd/fluent-korean) writing guidelines.
- Agents load `SKILL.md` as the skill entry point; `SKILL_ko.md` is a Korean reference for human readers.

## Skills

| Category | Skill | Description |
|----------|-------|-------------|
| frontend | [accessibility](frontend/accessibility/SKILL.md) | KWCAG 2.2, MACAG 2025, WCAG 2.2 A/AA, WAI-ARIA 1.2 reference for building and reviewing UI |

## License

[MIT](LICENSE). Standard names and requirement numbers (KS X OT0003, KS X 3253, WCAG, WAI-ARIA) belong to their respective publishers; this repository contains only summarized reference material.
