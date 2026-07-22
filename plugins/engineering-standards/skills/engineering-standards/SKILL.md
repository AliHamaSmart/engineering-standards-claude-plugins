---
name: engineering-standards
description: Enforce professional engineering standards whenever writing, modifying, refactoring, or reviewing code in ANY language, framework, or project. Use this skill EVERY time code is produced or changed — new features, bug fixes, refactors, scripts, boilerplate, code review, or PR review — even if the user does not mention "standards", "architecture", or "clean code". Covers architecture layering, file/function size limits, DRY, naming, error handling, testing, and anti-patching rules. If code is being written in this session, this skill applies.
---

# Engineering Standards (Universal)

These standards apply to ALL code in ANY language or framework. They are constraints, not suggestions. If a user request conflicts with these rules, follow the rules and explain the deviation — do not silently violate them. If the project has its own conventions (a CLAUDE.md, style guide, or existing patterns in the codebase), project conventions win on specifics; these rules fill the gaps.

## Hard limits (never violate)

| Rule | Limit |
|------|-------|
| File length | ≤ 550 lines. If output would exceed this, plan the module split BEFORE writing. |
| Function/method length | ≤ 40 lines. Extract helpers when longer. |
| Function parameters | ≤ 5. Group into an object/struct/record beyond that. |
| Nesting depth | ≤ 3 levels. Use early returns / guard clauses. |
| Duplication | Never copy-paste a block > 5 lines. Extract and reuse. |
| One responsibility | One file = one cohesive purpose. A "utils" dumping ground is a violation. |

Never produce a single monolithic file "to make it work first". Working-but-unmaintainable is a failed output.

## Business logic decomposition (objectively detect)

Before writing or reviewing code, scan **imports and I/O patterns** to classify logic:

- **Business logic (must be pure):** only stdlib imports, no HTTP/DB/file/framework, deterministic input→output, no side effects.
- **Non-business (infrastructure/edges):** imports HTTP client, DB driver, file system, framework, or vendor SDK.

**Split criteria — MUST decompose when any apply:**
- Function handles > 3 distinct responsibilities (validate + transform + persist).
- Function has > 2 major conditional branches in sequence.
- Function exceeds 40 lines OR nesting > 3 levels.
- Logic references transport/framework types (request, response, ORM entity) outside edges.

**Naming inference (follow the project, don't guess):**
1. Scan directory structure and existing naming — if you see `core/`, `domain/`, `usecases/`, `handlers/`, `api/`, `features/`, follow those.
2. Check `CLAUDE.md`, `tsconfig`, `package.json`, `pyproject.toml`, or project-style guides for layer conventions.
3. Infer layers from import direction: files importing only stdlib are candidates for core; files importing `express`, `prisma`, `axios` are edges.
4. If no structure exists, propose a minimal split and implement the split — don't dump everything in one place.

## Architecture: separation of concerns

Regardless of the specific style the project uses (hexagonal, clean architecture, MVC, feature-sliced), enforce the universal dependency rule:

**Business logic must not depend on delivery mechanisms or infrastructure.**

Concretely, identify three zones in any codebase:

1. **Core / domain** — business rules, entities, calculations. Pure: no HTTP, no SQL, no SDK imports, no framework types. Depends on abstractions (interfaces/protocols/traits) it defines itself.
2. **Application / orchestration** — use cases that coordinate the core via those abstractions. Still free of transport and vendor details.
3. **Edges** — everything that touches the outside world: HTTP handlers/controllers, DB access, external API clients, file IO, UI rendering. Edges depend inward; the core NEVER depends on edges.

FORBIDDEN in any project:
- Business logic inside an HTTP handler, controller, UI component, or CLI entry point (these must be thin: parse → call → map)
- Core/domain code importing a framework, ORM, HTTP client, or vendor SDK
- Persistence models (ORM entities, DB rows) leaking across layer boundaries into responses/views — map to dedicated types
- Circular dependencies between modules

If the project already violates this, do not spread the violation — new code follows the rule, and flag the debt.

Read `references/architecture-patterns.md` when designing a new module/feature structure or when unsure how to apply layering in a specific paradigm (backend service, frontend app, CLI, data pipeline).

When working on infrastructure code (Terraform/OpenTofu, CloudFormation, Pulumi, CDK, Ansible, Kubernetes manifests, Helm, or any IaC tool), read `references/infrastructure-as-code.md` — it contains tool-agnostic rules for module structure, secrets, least privilege, version pinning, and destructive-change discipline.

## Data safety (universal)

- Any code touching multi-user or multi-tenant data MUST scope every query/operation by the owning identity (user id, org id, account id) as an explicit parameter — never inferred implicitly deep inside. If unsure whether data is scoped, ask; do not guess.
- Never hardcode secrets, keys, or credentials. Configuration comes from environment/config layers.
- All external input is validated at the edge before reaching core logic.

## Anti-patching rule (maintainability)

When modifying existing code:

1. **Do not just bolt on.** Before adding to a file, check: is it already near/over 550 lines, or is the target function already complex? If yes, propose a small extraction/refactor as part of the change.
2. **Boy scout rule**: leave touched code slightly better — but keep refactors scoped to what you touch; do not rewrite unrelated code in the same change.
3. If a "quick fix" would add another special-case branch to an already-branchy function, extract a strategy/handler/lookup instead.
4. Never duplicate an existing function with a slight variation ("processDataV2") — parameterize or compose.
5. Flag tech debt explicitly: if the proper fix is out of scope, say so and describe the follow-up. Hidden debt is a violation.

## Clean code rules

- **DRY, not premature**: extract on the 2nd–3rd real duplication, not speculatively.
- **Naming describes intent**: `syncCalendarEvents`, not `processData` / `handleStuff` / `doWork`. No cryptic abbreviations except universal ones (id, db, url, i in a tiny loop).
- **No dead code**: no commented-out blocks, unused imports, or unreachable branches in final output.
- **Errors are handled, not swallowed**: no bare/empty catch. Raise meaningful, specific errors in core logic; translate to transport-appropriate errors (HTTP status, exit code, UI message) only at the edge.
- **Types**: use the strongest typing the language offers (type hints, strict mode, no `any`-equivalents).
- **Immutability by default** where the language supports it cheaply; mutate only with reason.
- **Comments explain WHY, not what.** If code needs a "what" comment, rename or restructure instead.

## Testing

- Core/application logic must be testable without a real DB, network, or filesystem — that is the payoff of depending on abstractions.
- Every new use case / significant behavior gets at least one unit test. Bug fixes get a regression test reproducing the bug.
- If the project has no test infrastructure, note it and propose the minimal setup rather than skipping silently.

## Code review mode

When asked to review code or a PR, use `references/review-checklist.md` and report findings grouped by severity (blocker / should-fix / nit), citing file:line with a concrete fix for each. Always check: layer violations, data scoping, size limits, patch-on-patch smell, swallowed errors.

When asked to rate, score, or audit code quality — or when a review covers a substantial change and a summary would help — additionally apply `references/quality-scorecard.md`: score Maintainability, Scalability, Performance, Security, DRY, and Readability on 1–5 anchors with evidence, plus the top 3 actions to improve.

## Output discipline

- Before writing a feature that spans multiple concerns, briefly state the planned file/module breakdown, then implement.
- Code, identifiers, and comments in English. Explanations to the user in the user's language.
