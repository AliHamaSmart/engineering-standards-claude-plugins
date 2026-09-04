# Business Logic Decomposition

Before writing or reviewing code, classify the logic and decompose when necessary. This is universal — it applies regardless of language or framework.

## Classify logic by I/O and imports

Scan imports and I/O patterns to classify:

- **Business logic (must be pure):** only stdlib / language-internal imports, no HTTP/DB/file/framework, deterministic input → output, no side effects.
- **Non-business (infrastructure / edges):** imports HTTP client, DB driver, file system, framework, or vendor SDK.

## Split criteria — MUST decompose when any apply

- Function handles > 3 distinct responsibilities (validate + transform + persist).
- Function has > 2 major conditional branches in sequence.
- Function exceeds 40 lines OR nesting > 3 levels.
- Logic references transport/framework types (request, response, ORM entity) outside edges.

## Architecture: separation of concerns

Business logic must not depend on delivery mechanisms or infrastructure. Identify three zones:

1. **Core / domain** — business rules, entities, calculations. Pure: no HTTP, no SQL, no SDK imports, no framework types. Depends on abstractions (interfaces / protocols / traits) it defines itself.
2. **Application / orchestration** — use cases that coordinate the core via those abstractions. Still free of transport and vendor details.
3. **Edges** — everything that touches the outside world: HTTP handlers, DB access, external API clients, file IO, UI rendering. Edges depend inward; the core NEVER depends on edges.

FORBIDDEN:
- Business logic inside an HTTP handler, controller, UI component, or CLI entry point (these must be thin: parse → call → map).
- Core/domain code importing a framework, ORM, HTTP client, or vendor SDK.
- Persistence models leaking across layer boundaries into responses/views — map to dedicated types.
- Circular dependencies between modules.

If the project already violates this, do not spread the violation — new code follows the rule and flag the debt.

## Naming inference (follow the project, don't guess)

1. Scan directory structure and existing naming — if you see `core/`, `domain/`, `usecases/`, `handlers/`, `api/`, `features/`, follow those.
2. Check `CLAUDE.md`, `tsconfig`, `package.json`, `pyproject.toml`, or project-style guides for layer conventions.
3. Infer layers from import direction: files importing only stdlib are candidates for core; files importing `express`, `prisma`, `axios` are edges.
4. If no structure exists, propose a minimal split and implement the split — don't dump everything in one place. If the repo is entirely empty, this is greenfield: follow `references/greenfield-bootstrap.md` instead of inventing a split ad hoc.

## Data safety (universal)

- Any code touching multi-user or multi-tenant data MUST scope every query/operation by the owning identity (user id, org id, account id) as an explicit parameter — never inferred implicitly deep inside.
- Never hardcode secrets, keys, or credentials. Configuration comes from environment / config layers.
- All external input is validated at the edge before reaching core logic.
