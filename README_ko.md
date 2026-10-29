# skill-zip

[English](README.md) | **한국어**

**스킬집 (skill + 集)**: 한국 개발자를 위한 실무 에이전트 스킬 모음집입니다.

해외에서 만든 스킬 모음에는 한국 프로젝트가 지켜야 하는 표준과 법규가 거의 들어 있지 않습니다. skill-zip은 이런 내용을 한곳에 모아서, Claude Code나 Codex 같은 코딩 에이전트가 소프트웨어를 만들고 검토할 때 한국 접근성 표준(KWCAG), 공공 부문 프레임워크, 개인정보보호법 같은 한국 고유의 요구사항을 적용할 수 있게 합니다.

## 설치

### Agent Skills CLI (Claude Code, Codex, Cursor 등 여러 에이전트)

```bash
# 전체 스킬 설치
npx --yes skills add zziaho/skill-zip --all -g

# 특정 스킬만 설치
npx --yes skills add zziaho/skill-zip --skill accessibility -g

# 설치하지 않고 사용할 수 있는 스킬 목록만 확인
npx --yes skills add zziaho/skill-zip --list
```

Node.js 18 이상과 `npx`가 필요합니다.

### Claude Code 플러그인

```
/plugin install skill-zip --marketplace zziaho/skill-zip
```

Claude Code 2.1.275보다 이전 버전을 사용한다면, 마켓플레이스를 먼저 추가해야 합니다.

```
/plugin marketplace add zziaho/skill-zip
/plugin install skill-zip@skill-zip
```

## 스킬 목록

### 프론트엔드

| 할 수 있는 일 | 스킬 | 설명 |
|---------------|------|------|
| 접근성을 갖춘 사용자 인터페이스 구현과 검토 | [`accessibility`](frontend/accessibility/SKILL_ko.md) | KWCAG 2.2(33개 항목 전체), MACAG 2025, WCAG 2.2 Level A/AA, WAI-ARIA 1.2를 다루는 참조 자료입니다. 규칙, 검사 방법, ARIA 위젯 패턴, 코드 예제를 제공합니다 |

## 로드맵

아래 주제는 추가할 예정이며, 아직 제공하지 않습니다.

- 공공 부문 개발: 전자정부 표준프레임워크, 웹 호환성
- 법규 준수: 개인정보보호법, 시큐어 코딩 가이드
- 프론트엔드: 한글 타이포그래피, 한국형 입력 폼 패턴(주소 검색, 본인 인증)

## 저장소 구조

```
skill-zip/
├── .claude-plugin/         # Claude Code 마켓플레이스·플러그인 매니페스트
├── scripts/                # 저장소 검사 스크립트
└── <카테고리>/
    └── <스킬 이름>/
        ├── SKILL.md        # 에이전트가 불러오는 스킬 진입점
        ├── SKILL_ko.md     # 사람이 읽기 위한 한국어 문서
        └── references/
            ├── <파일>.md
            └── <파일>_ko.md
```

모든 문서는 영어 원본과 한국어 번역본(`<이름>_ko.md`)을 함께 유지합니다. 한국어 파일은 [fluent-korean](https://github.com/snflkd/fluent-korean) 작성 지침을 따릅니다. 스킬을 추가하거나 수정하기 전에 [CONTRIBUTING_ko.md](CONTRIBUTING_ko.md)를 확인해 주세요.

## 라이선스

[MIT](LICENSE) 라이선스를 따릅니다. 표준의 명칭과 요구사항 번호(KS X OT0003, KS X 3253, WCAG, WAI-ARIA)에 대한 권리는 각 발행 기관에 있으며, 이 저장소에는 그 내용을 요약한 참조 자료만 들어 있습니다.
