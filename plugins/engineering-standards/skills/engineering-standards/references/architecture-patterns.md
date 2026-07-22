# Architecture Patterns — Applying Layering Anywhere

The universal rule: **dependencies point inward, toward business logic.** How that looks per context:

## Backend service (any language/framework)

```
<root>/
├── api|handlers|controllers/   # EDGE: transport. Thin: parse → call use case → map response
├── application|usecases/       # Orchestration via abstractions
├── domain|core/                # Entities, business rules, interface definitions. Pure.
└── infrastructure|adapters/    # EDGE: DB repositories, external API clients, queues, storage
```

- The core defines interfaces (repository, gateway, clock, id-generator); infrastructure implements them.
- Wiring/dependency injection happens at the composition root (main/startup), not inside layers.
- Works identically in Python/FastAPI, Node/Express, Go, Java/Spring, C#/.NET, Rust — only file naming conventions differ.

## Frontend app (React/Vue/Svelte/mobile)

```
src/
├── features/<feature>/
│   ├── components|views/    # EDGE: rendering only, no business logic in markup
│   ├── hooks|composables|
│   │   viewmodels/          # Logic and state
│   ├── api.*                # EDGE: typed calls to backend, single place per feature
│   └── types.*
└── shared/                  # Reusable UI, base API client, utilities
```

- Component/view files ≤ 200 lines; extract sub-components and logic units.
- Server data flows through a data-fetching layer; do not mirror it into ad-hoc local state.
- User-facing strings go through the i18n layer if the project has one.

## CLI tool / script

Even a script follows the rule in miniature:
- `main`/entry parses args and wires things — no logic.
- Logic lives in pure functions/modules that take inputs and return outputs (testable without running the CLI).
- IO (file reads, network) isolated in small adapter functions passed in or called at the edge.

## Data pipeline / batch job

- Extract, transform, load as separate composable steps.
- Transforms are pure functions on data structures — no connection handles inside transform logic.
- Sources/sinks are adapters conforming to small interfaces so transforms are testable with in-memory data.

## Choosing granularity

- Small project (< ~15 files): folders may collapse (e.g., `core/` + `adapters/` only), but the import direction rule still holds.
- Growing project: split when a file crosses the 400-line limit or a folder loses cohesion — not before.
- Never introduce layers speculatively ("we might need CQRS") — add structure when a rule (size, purity, duplication) forces it.

## Enforcement hooks (recommend per ecosystem)

Suggest adding to CI when relevant:
- Python: `import-linter` (layer contracts), `ruff` (max-lines, complexity)
- JS/TS: `eslint` (`max-lines`, `max-depth`, `import/no-cycle`, boundary plugins like `eslint-plugin-boundaries`)
- Go: `depguard`, `gocyclo`
- Java/Kotlin: ArchUnit
- C#: NetArchTest
- Any: SonarQube for duplication/complexity

## Red flags to catch in any codebase

1. SQL/HTTP client call inside business logic → extract behind an interface.
2. Framework/vendor import in core → invert the dependency.
3. Persistence model returned to the presentation layer → map to a dedicated type.
4. God module/class accumulating unrelated methods → split by responsibility.
5. Two layers importing each other → cycle; redesign the boundary.
