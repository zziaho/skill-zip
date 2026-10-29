# Contributing

**English** | [한국어](CONTRIBUTING_ko.md)

Thank you for contributing to skill-zip. This guide explains how to add or change a skill.

## Scope

skill-zip collects practical skills for Korean developers. A new skill should cover a standard, regulation, or practice that is specific to Korean software projects, or that global skill collections do not cover well.

## Adding a skill

1. Create `<category>/<skill-name>/`. Use an existing category (`frontend`, ...) when one fits; add a new category only when none does.
2. Write `SKILL.md` with YAML frontmatter:
   - `name`: must match the directory name.
   - `description`: what the skill covers and when an agent should use it. Agents decide whether to load the skill from this text, so list concrete triggers.
3. Keep `SKILL.md` short and move detailed material into `references/`. Tell the agent which reference file to read for which task, so it does not load everything at once.
4. Write the Korean version of every document (see [Bilingual documents](#bilingual-documents)).
5. Register the skill:
   - Add its path to `skills` in `.claude-plugin/plugin.json`.
   - Add a row to the category table in both `README.md` and `README_ko.md`.
6. Run the checks (see [Checks](#checks)).

## Content rules

- Cite the exact name and version of every standard or law (e.g., KS X OT0003:2022). Mark anything you could not verify against the original text as unverified.
- Summarize and restructure source material in your own words. Do not paste long passages of standards or other copyrighted text.
- Prefer rules an agent can act on and steps it can check, over general explanations.

## Bilingual documents

- Every Markdown document has an English original and a Korean version named `<name>_ko.md` in the same directory (e.g., `SKILL.md` and `SKILL_ko.md`). `LICENSE` and non-document files are excluded.
- When you change one file of a pair, update the other in the same commit.
- Keep the structure of each pair identical: the same headings, table rows, and code blocks.
- Inside Korean files, link to other Korean files (`*_ko.md`).
- Write Korean text according to the [fluent-korean](https://github.com/snflkd/fluent-korean) guidelines.
- Keep standard numbers, ARIA attributes, code identifiers, and other technical names in their original form.

## Checks

```bash
python scripts/check_docs.py
```

The script checks that:

- every document has its `_ko` pair, and the pair has the same number of headings, table rows, and code fences;
- every skill directory is listed in `.claude-plugin/plugin.json`, and every listed path contains a `SKILL.md` whose `name` matches the directory name.

The same checks run in CI on every push and pull request.

## Commit messages

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <subject in English>

<body in English>

<body in Korean>
```

- `type`: `feat`, `fix`, `docs`, `chore`, `ci`, `refactor`, and so on.
- `scope`: the category of the skill you changed (e.g., `frontend`), when it applies.
- Write the subject line in English. Write the body in English first, then in Korean.

## License

By contributing, you agree that your contributions are licensed under the [MIT License](LICENSE).
