# Uninote Claude Code Plugins

Internal plugin marketplace for Claude Code.

## Install

```
/plugin marketplace add <org-or-user>/uninote-claude-plugins
/plugin install engineering-standards@uninote-plugins
```

For a private repo, make sure your git credentials (SSH or HTTPS) can clone it — Claude Code uses your git config.

After install, run `/plugin` or start a new session; the skill activates automatically whenever code is written, modified, or reviewed.

## Usage

- Write/modify code as usual — standards (layering, ≤400-line files, DRY, anti-patching) are applied automatically.
- `review this PR` → severity-based review (blocker / should-fix / nit).
- `audit this file with the quality scorecard` → 1–5 scores for maintainability, scalability, performance, security, DRY, readability + top 3 actions.

## Update (maintainers)

1. Edit files under `plugins/engineering-standards/skills/engineering-standards/`
2. Bump `version` in `plugins/engineering-standards/.claude-plugin/plugin.json` and in `.claude-plugin/marketplace.json`
3. Commit & push

Users refresh with:

```
/plugin marketplace update uninote-plugins
```

## Structure

```
.claude-plugin/marketplace.json          # catalog (repo root — required location)
plugins/engineering-standards/
├── .claude-plugin/plugin.json           # plugin manifest
└── skills/engineering-standards/
    ├── SKILL.md                         # core rules (always loaded when coding)
    └── references/
        ├── architecture-patterns.md     # layering per paradigm (BE/FE/CLI/pipeline)
        ├── infrastructure-as-code.md    # tool-agnostic IaC rules
        ├── review-checklist.md          # blocker/should-fix/nit checklist
        └── quality-scorecard.md         # 6-dimension rating rubric
```
