# Engineering Standards — Universal Claude Code Plugin

Engineering standards that work with **ANY** project — Node, Python, Go, Rust, Ruby, Java, mobile, CLI, IaC, data pipelines, or anything else. No configuration needed. Just install and use.

## What is this?

A Claude Code plugin that **automatically enforces engineering best practices** on every code operation. No slash command required — it activates the moment you write, modify, or review code.

## What standards are enforced?

### Hard Limits (never violate)

| Rule | Limit |
|------|------|
| File length | ≤ 550 lines |
| Function/method length | ≤ 40 lines |
| Function parameters | ≤ 5 (group into object/struct/record beyond that) |
| Nesting depth | ≤ 3 levels (use early returns / guard clauses) |
| Duplication | Never copy-paste a block > 5 lines |
| One responsibility | One file = one cohesive purpose |

### Architecture

- Business logic **must not** depend on delivery mechanisms or infrastructure
- Three zones: **Core/Domain** (pure), **Application/Orchestration** (use cases), **Edges** (HTTP, DB, external APIs)
- FORBIDDEN: business logic in handlers, core importing framework/vendor, persistence models leaking across boundaries, circular dependencies

### Data Safety

- Every query/operation on multi-user data **MUST** scope by owning identity (user id, org id)
- Never hardcode secrets, keys, or credentials
- All external input validated at the edge before reaching core logic

### Testing

- Core/application logic must be testable without real DB, network, or filesystem
- Every new use case gets at least one unit test
- Bug fixes get a regression test
- Use the **project's existing test framework** (auto-detected)

### Anti-Patching

- Do not just bolt on — extract helpers or refactor when needed
- Flag tech debt explicitly when standards can't be followed immediately
- No "processDataV2" duplicates — parameterize or compose

## How it works

1. **Project Discovery (Phase 0)** — Scans your project to detect language, framework, testing setup, linting tools
2. **Adapts rules** — Uses your existing tools (Jest, pytest, golangci-lint, etc.) instead of inventing new ones
3. **Applies standards** — Enforces architecture layering, size limits, DRY, security, anti-patching

## How to install

```bash
# Option 1: Direct install (recommended for individual use)
cp -r plugins/engineering-standards ~/.claude/skills/engineering-standards
cp -r plugins/engineering-standards-ci ~/.claude/skills/engineering-standards-ci

# Option 2: Via marketplace
/plugin marketplace add engineering-standards
/plugin install engineering-standards
```

After install, **start a new Claude Code session**. The skills auto-activate on every code write, modification, or review.

## How to use

### Automatic enforcement

Just write code normally. The plugin activates automatically:

```bash
# This will enforce all standards
"Create a function to validate user email"
"Refactor this auth module"
"Write a test for the payment service"
```

### Code review mode

```bash
# severity-based review (blocker / should-fix / nit)
"review this PR"

# 6-dimension quality scorecard (1-5 scores with evidence)
"audit this file with the quality scorecard"
```

### Generate CI configs

```bash
# Auto-generates GitHub Actions workflow, pre-commit hooks, and PR template
"generate ci for this project"
```

## What it does automatically

- **ALWAYS-ACTIVE** — no slash command needed. Fires on every Write, Edit, MultiEdit, or code generation.
- **Auto-detects** project type (Node, Python, Go, Rust, Ruby, Java, mobile, CLI, IaC, data pipelines)
- **Adapts** to your existing test framework, linter, and style guide
- **Flags tech debt** explicitly when standards can't be followed immediately
- **Generates CI configs** that enforce the same standards in your pipeline (GitHub Actions, pre-commit hooks, PR templates)

## Example outputs

### Project Discovery output

```
Discovered project: Node/TypeScript with Jest
- package.json found
- jest.config.ts found
- Using Jest for testing
- Using ESLint for linting
```

### Code review output

```
## Review: auth-module.ts

### Blockers (1)
1. auth-module.ts:45 — Business logic in handler. Move to core layer. Fix: extract to `domain/auth-service.ts`

### Should-fix (2)
1. auth-module.ts:78 — Swallowed error. Add try/catch with specific error. Fix: log and return user-friendly message
2. auth-module.ts:112 — Hard-coded secret. Use env variable. Fix: `process.env.JWT_SECRET`

### Nits (1)
1. auth-module.ts:33 — Vague name `handleStuff`. Rename to `validateUserInput`
```

### Quality scorecard output

```
## Quality Scorecard: payment-service

| Dimension       | Score | Key evidence |
|-----------------|-------|--------------|
| Maintainability | 4/5   | Good layer separation, but file is 480 lines |
| Scalability     | 5/5   | Stateless, pagination, parallelizable |
| Performance     | 3/5   | N+1 query on line 89 |
| Security        | 5/5   | Parameterized queries, input validated |
| DRY             | 4/5   | Minor duplication on lines 120-135 |
| Readability     | 4/5   | Good naming, some long functions |

**Overall: 4.2/5** — Solid code with minor performance concern

### Top 3 actions to raise the score
1. Refactor N+1 query on line 89 to batch query
2. Extract helper function on lines 120-135 to reduce duplication
3. Split file into domain/application/edge layers
```

## Structure

```
plugins/engineering-standards/
├── .claude-plugin/plugin.json               # Plugin manifest
└── skills/
    ├── engineering-standards/               # Core engineering standards skill
    │   ├── SKILL.md                         # Orchestrator (~96 lines — discovery protocol + rule references)
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

## Supported project types

| Files found | Project type | Linters/testers |
|-------------|--------------|-----------------|
| `package.json` + `tsconfig.json` | Node/TypeScript | ESLint, Prettier, Jest/Vitest |
| `go.mod` | Go | golangci-lint, gofmt |
| `Cargo.toml` | Rust | clippy, rustfmt, cargo test |
| `requirements.txt` + `pyproject.toml` | Python | ruff, pytest |
| `Gemfile` | Ruby | rubocop, rspec |
| `.csproj` or `.sln` | C# | dotnet format, dotnet test |
| `pom.xml` or `build.gradle` | Java/Kotlin | checkstyle, Spotless, JUnit |

## Requirements

- Claude Code v1.0+
- Git repository (for CI template generation)
- No additional dependencies — works with any project

## Troubleshooting

**Plugin not activating?**
- Make sure you started a new session after install
- Check `~/.claude/skills/engineering-standards/SKILL.md` exists
- Run `/plugin list` to verify it's installed

**Rules not adapting to my project?**
- The plugin scans top-level files on each task — make sure your project files are in the repo root
- Some project types (mobile, CLI) may not have standard detection files — the plugin will fall back to default rules

**CI template not generating?**
- Make sure you're in a Git repository
- Run `generate ci for this project` in the repo root

## For Maintainers

To release to marketplace:

1. Edit files under `plugins/engineering-standards/skills/`
2. Bump `version` in `plugins/engineering-standards/.claude-plugin/plugin.json` and in `.claude-plugin/marketplace.json`
3. Commit & push

Users refresh with:
```
/plugin marketplace update engineering-standards
```

