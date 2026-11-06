# skill-zip

[한국어](README.md) | **English**

**스킬집 (skill + 集)**: practical agent skills for Korean developers.

Global skill collections rarely cover the standards and regulations that Korean projects must follow. skill-zip gathers them in one place so that coding agents such as Claude Code and Codex can apply Korean accessibility standards (KWCAG), public-sector frameworks, privacy law, and other Korea-specific requirements while they build and review software.

## Install

### Agent Skills CLI (Claude Code, Codex, Cursor, and other agents)

```bash
# Install every skill
npx --yes skills add zziaho/skill-zip --all -g

# Install a single skill
npx --yes skills add zziaho/skill-zip --skill accessibility -g
npx --yes skills add zziaho/skill-zip --skill krds -g
npx --yes skills add zziaho/skill-zip --skill egovframe -g
npx --yes skills add zziaho/skill-zip --skill juso-api -g
npx --yes skills add zziaho/skill-zip --skill secure-coding -g

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
| Build and review forms on Korean government websites with KRDS | [`krds`](frontend/krds/SKILL.md) | Reference for the input form area of KRDS (범정부 UI/UX 디자인시스템), with basic patterns, input, selection, button and help component rules mapped to KWCAG items, krds-* classes, and the application service checklist |

### Backend

| What it does | Skill | Description |
|--------------|-------|-------------|
| Build and review code on eGovFrame (전자정부 표준프레임워크) | [`egovframe`](backend/egovframe/SKILL.md) | eGovFrame 4.x and 5.x reference with version detection, layer and naming conventions, runtime base classes, the 44-rule PMD ruleset, and the official SQL writing rules split by DBMS |
| Integrate and review the Korean road name address APIs | [`juso-api`](backend/juso-api/SKILL.md) | Reference for the road name, English, coordinate and detail address APIs of business.juso.go.kr (주소기반산업지원서비스), with request and output tables corrected where the official sources disagree, error codes per API, approval key rules, how to avoid IP blocking, and fixes for the security problems in the official samples |

### Security

| What it does | Skill | Description |
|--------------|-------|-------------|
| Apply Korean public-sector secure coding (소프트웨어 개발보안) and diagnose security weaknesses | [`secure-coding`](security/secure-coding/SKILL.md) | Reference based on the Ministry of the Interior and Safety secure coding guide and weakness diagnosis guide (2021.11. revision), with true- and false-positive criteria for the 49 implementation-phase weaknesses, safe Java and C code, the 20 design-phase security criteria, and a script that lists candidate weaknesses |

## Repository layout

```
skill-zip/
├── .claude-plugin/         # Claude Code marketplace and plugin manifests
├── scripts/                # Repository checks
├── <category>/             # frontend, backend, security
│   └── <skill-name>/
│       ├── SKILL.md        # Skill entry point loaded by agents
│       ├── SKILL_ko.md     # Korean version for human readers
│       ├── references/     # Task-specific references (<file>.md, <file>_ko.md)
│       └── scripts/        # Check scripts used by the skill (optional)
├── README.md               # Korean (default)
└── README_en.md            # English
```

Every document is maintained in English and Korean (`<name>_ko.md`). The README is the exception: the Korean version is `README.md` and the English version is `README_en.md`. See [CONTRIBUTING.md](CONTRIBUTING.md) before adding or changing a skill.

## License

[MIT](LICENSE). Standard names and requirement numbers (KS X OT0003, KS X 3253, WCAG, WAI-ARIA) belong to their respective publishers; this repository contains only summarized reference material.
