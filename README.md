# skill-zip

**English** | [한국어](README_ko.md)

**스킬집 (skill + 集)**: practical agent skills for Korean developers.

Global skill collections rarely cover the standards and regulations that Korean projects must follow. skill-zip gathers them in one place so that coding agents such as Claude Code and Codex can apply Korean accessibility standards (KWCAG), public-sector frameworks, privacy law, and other Korea-specific requirements while they build and review software.

## Install

### Agent Skills CLI (Claude Code, Codex, Cursor, and other agents)

```bash
# Install every skill
npx --yes skills add zziaho/skill-zip --all -g

# Install a single skill
npx --yes skills add zziaho/skill-zip --skill accessibility -g

# List the available skills without installing
npx --yes skills add zziaho/skill-zip --list
```

Requires Node.js 18 or later and `npx`.

### Claude Code plugin

```
/plugin install skill-zip --marketplace zziaho/skill-zip
```

On Claude Code versions earlier than 2.1.275, add the marketplace first:

```
/plugin marketplace add zziaho/skill-zip
/plugin install skill-zip@skill-zip
```

## Skills

### Frontend

| What it does | Skill | Description |
|--------------|-------|-------------|
| Build and review accessible UI | [`accessibility`](frontend/accessibility/SKILL.md) | KWCAG 2.2 (all 33 items), MACAG 2025, WCAG 2.2 Level A/AA, and WAI-ARIA 1.2 reference with rules, test steps, ARIA widget patterns, and code snippets |

## Roadmap

The following topics are planned and not yet available:

- Korean public-sector development: eGovFrame (전자정부 표준프레임워크), web compatibility
- Compliance: Personal Information Protection Act (개인정보보호법), secure coding guide (시큐어 코딩 가이드)
- Frontend: Korean typography, Korean form patterns (address search, identity verification)

## Repository layout

```
skill-zip/
├── .claude-plugin/         # Claude Code marketplace and plugin manifests
├── scripts/                # Repository checks
└── <category>/
    └── <skill-name>/
        ├── SKILL.md        # Skill entry point loaded by agents
        ├── SKILL_ko.md     # Korean version for human readers
        └── references/
            ├── <file>.md
            └── <file>_ko.md
```

Every document is maintained in English and Korean (`<name>_ko.md`). Korean files follow the [fluent-korean](https://github.com/snflkd/fluent-korean) writing guidelines. See [CONTRIBUTING.md](CONTRIBUTING.md) before adding or changing a skill.

## License

[MIT](LICENSE). Standard names and requirement numbers (KS X OT0003, KS X 3253, WCAG, WAI-ARIA) belong to their respective publishers; this repository contains only summarized reference material.
