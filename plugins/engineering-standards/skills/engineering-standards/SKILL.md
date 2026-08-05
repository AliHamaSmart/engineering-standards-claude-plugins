---
name: engineering-standards
description: Enforce professional engineering standards automatically whenever writing, modifying, refactoring, or reviewing code in ANY language, framework, or project. Auto-triggered: fires on ANY operation that produces or changes code — including but not limited to Write, Edit, MultiEdit, Bash code generation, and code review actions. This is an ALWAYS-ACTIVE skill, not a slash command skill. It activates on every code write or modification regardless of whether the user prompt mentions "standards", "architecture", "clean code", "review", or "PR". Also auto-activates on code review, code audit, quality rating, and PR review requests. If code is being written, modified, or reviewed in this session, this skill applies — no explicit invocation needed.
---

# Engineering Standards (Universal — Always Active)

**ALWAYS-ACTIVE SKILL** — These engineering standards are enforced on every code operation automatically. No slash command needed. Fires whenever Write, Edit, MultiEdit, or code generation occurs.

These standards apply to ALL code in ANY language or framework. They are constraints, not suggestions. If the project has its own conventions (a `CLAUDE.md`, style guide, or existing patterns in the codebase), project conventions win on specifics; these rules fill the gaps.

## Phase 0: Project Discovery (run once, at the start of every task)

Before applying any rules, **scan the project to understand what you are working with**. This makes standards adapt to the project instead of the project bending to standards.

```
1. LIST top-level files — what exists? (package.json? Cargo.toml? go.mod? requirements.txt? Gemfile? Makefile? Justfile? pyproject.toml? .env.example?)
2. LIST top-level directories — what structure exists? (src/?, lib/?, app/?, api/?, core/?, domain/?)
3. CHECK for existing patterns — any CLAUDE.md? CONTRIBUTING.md? tsconfig.json? .eslintrc? Makefile targets? CI config (.github/, .gitlab-ci.yml)?
4. INFER — what language? what framework? what testing setup? what CI? what style conventions?
5. INJECT — adapt ALL rules below based on findings. Use the project's existing test framework, linter, and style guide rather than inventing new ones.
```

**Output of discovery:** Briefly note what you found to the user (1-2 lines max). Then proceed with rules adapted to the project.

Examples of what discovery might reveal:
- `package.json` + `tsconfig.json` + `jest.config.*` → Node/TypeScript with Jest; enforce TypeScript strict mode, use `@jest/globals` patterns.
- `go.mod` + `golangci-lint.yaml` → Go project; use `golangci-lint` config as baseline, follow go idioms.
- `Cargo.toml` → Rust project; use `clippy` rules, follow `rustfmt` conventions.
- `requirements.txt` + `Makefile` (with `test` target) → Python; use whatever test runner the Makefile/test target invokes.
- `Gemfile` → Ruby; use whatever gem-based linting the project has.
- **No project files at all** → apply default universal rules below, and flag the lack of tooling as tech debt to propose.

Discovery is lightweight and stateless — re-run it at the start of every new task to account for project evolution.

## Rules (modular — read the relevant ones as needed)

| File | When to read |
|------|-------------|
| `rules/file-size.md` | Always — hard limits apply to every output |
| `rules/decomposition.md` | Always — before writing or reviewing business logic |
| `rules/anti-patching.md` | When modifying existing code |
| `rules/clean-code.md` | Always — naming, DRY, comments, types |
| `rules/security.md` | When writing data access, auth, or handling user input |

### Reading reference files (on-demand)

| File | When to read |
|------|-------------|
| `references/architecture-patterns.md` | Designing a new module/feature structure |
| `references/infrastructure-as-code.md` | Working on IaC (Terraform, Pulumi, CDK, Ansible, K8s, Helm) |
| `references/review-checklist.md` | Asked to review code or a PR |
| `references/quality-scorecard.md` | Asked to rate/score/audit code quality |

## Core principles (always active, summarized)

### Hard limits (never violate)

| Rule | Limit |
|------|------|
| File length | ≤ 550 lines. If output would exceed this, plan the module split BEFORE writing. |
| Function/method length | ≤ 40 lines. Extract helpers when longer. |
| Function parameters | ≤ 5. Group into an object/struct/record beyond that. |
| Nesting depth | ≤ 3 levels. Use early returns / guard clauses. |
| Duplication | Never copy-paste a block > 5 lines. Extract and reuse. |
| One responsibility | One file = one cohesive purpose. A "utils" dumping ground is a violation. |

Never produce a single monolithic file "to make it work first". Working-but-unmaintainable is a failed output.

### Architecture: separation of concerns

**Business logic must not depend on delivery mechanisms or infrastructure.**

Identify three zones:
1. **Core / domain** — business rules, entities, calculations. Pure: no HTTP, no SQL, no SDK imports, no framework types.
2. **Application / orchestration** — use cases that coordinate the core via abstractions.
3. **Edges** — everything touching the outside world: HTTP handlers, DB access, external APIs, file IO, UI.

FORBIDDEN in any project: business logic inside handlers; core importing framework/vendor; persistence models leaking across boundaries; circular dependencies.

### Data safety (universal)

- Every query/operation on multi-user data MUST scope by owning identity (user id, org id) as explicit parameter.
- Never hardcode secrets, keys, or credentials.
- All external input validated at the edge before reaching core logic.

### Testing

- Core/application logic must be testable without real DB, network, or filesystem.
- Every new use case gets at least one unit test. Bug fixes get a regression test.
- **Use the project's existing test framework** (discovered in Phase 0) — don't invent a new one.

## Output discipline

- Before writing a feature that spans multiple concerns, briefly state the planned file/module breakdown, then implement.
- Code, identifiers, and comments in English. Explanations to the user in the user's language.
