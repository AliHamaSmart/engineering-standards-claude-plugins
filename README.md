# Engineering Standards — Universal Claude Code Plugin

Engineering standards that work with **ANY** project — Node, Python, Go, Rust, Ruby, Java, mobile, CLI, IaC, data pipelines, or anything else. No configuration needed. Just install and use.

## Quick Start

```bash
# Option 1: Direct install (recommended for individual use)
cp -r plugins/engineering-standards ~/.claude/skills/engineering-standards
cp -r plugins/engineering-standards-ci ~/.claude/skills/engineering-standards-ci

# Option 2: Via marketplace (for distributed use)
/plugin marketplace add uninote-plugins
/plugin install engineering-standards

# After install, start a new Claude Code session
```

The skills auto-activate on every code write, modification, or review — no slash command needed.

## How it works

This plugin uses a **Project Discovery Protocol** — before applying any rules, the skill automatically scans your project to understand:

- What language / framework it uses
- What testing setup exists (Jest? pytest? Go test?)
- What linting / style tools are configured
- What directory conventions the project follows

Then it **adapts the rules to your project** instead of forcing your project to adapt to generic rules. Works with ANY project — no configuration, no setup, no `@org-name` needed.

### What it does automatically

- **ALWAYS-ACTIVE** — no slash command needed. Fires on every Write, Edit, MultiEdit, or code generation.
- Enforces architecture layering, file/function size limits, DRY, security, anti-patching rules.
- Adapts to your project's existing test framework, linter, and style guide.
- Flags tech debt explicitly when standards can't be followed immediately.
- **Generates CI configs** that enforce these same standards in your pipeline (GitHub Actions, pre-commit hooks, PR templates).

### When to ask for deeper review

- `review this PR` → severity-based review (blocker / should-fix / nit).
- `audit this file with the quality scorecard` → 1–5 scores for maintainability, scalability, performance, security, DRY, readability + top 3 actions.
- `generate ci for this project` → generates GitHub Actions workflow, pre-commit hooks, and PR template with engineering standards checks.

## Structure

```
plugins/engineering-standards/
├── .claude-plugin/plugin.json               # Plugin manifest
└── skills/
    ├── engineering-standards/               # Core engineering standards skill
    │   ├── SKILL.md                         # Orchestrator (~60 lines — discovery protocol + rule references)
    │   ├── rules/                           # Modular rule files
    │   │   ├── file-size.md                 # Hard limits (≤550 lines, ≤40 funcs, ≤3 nesting)
    │   │   ├── decomposition.md             # Business logic splitting, architecture layers
    │   │   ├── anti-patching.md             # Maintainability, no bolt-on patches
    │   │   ├── clean-code.md                # Naming, DRY, comments, types, immutability
    │   │   └── security.md                  # Data scoping, secrets, input validation, auth
    │   └── references/                      # Deep-dive references (read on demand)
    │       ├── architecture-patterns.md     # Layering per paradigm (BE/FE/CLI/pipeline)
    │       ├── infrastructure-as-code.md    # Tool-agnostic IaC rules
    │       ├── review-checklist.md          # Blocker/should-fix/nit checklist
    │       └── quality-scorecard.md         # 6-dimension rating rubric
    └── engineering-standards-ci/            # CI enforcement skill
        ├── SKILL.md                         # CI generation orchestrator
        └── templates/                       # Generated CI config templates
            ├── .github/workflows/ci.yml     # GitHub Actions workflow
            ├── .pre-commit-config.yaml      # Pre-commit hooks
            └── .github/pull_request_template.md  # PR template with standards checklist
```

## Capabilities

| Feature | Description |
|---------|-------------|
| **Project Discovery** | Auto-detects language, framework, testing setup, and adapts rules |
| **Always-Active** | No slash command needed — fires on every code operation |
| **Modular Rules** | File-size, decomposition, anti-patching, clean-code, security |
| **Architecture Review** | Layering, separation of concerns, dependency direction |
| **Code Review** | Blocker/should-fix/nit severity-based review |
| **Quality Scorecard** | 6-dimension rating (maintainability, scalability, performance, security, DRY, readability) |
| **CI Enforcement** | Generate GitHub Actions, pre-commit hooks, PR templates |
| **Universal** | Works with any project type — Node, Python, Go, Rust, Ruby, Java, mobile, IaC, CLI, data pipelines |

## For Maintainers

To release to marketplace:

1. Edit files under `plugins/engineering-standards/skills/`
2. Bump `version` in `plugins/engineering-standards/.claude-plugin/plugin.json` and in `.claude-plugin/marketplace.json`
3. Commit & push

Users refresh with:
```
/plugin marketplace update uninote-plugins
```

