# Greenfield Bootstrap — Starting From an Empty Repo

Phase 0 discovery infers rules from what already exists. In an empty repo there is nothing to infer,
so this file replaces inference with a decision + bootstrap sequence.

**Read this when Phase 0 detects greenfield. Skip it entirely for any project that already has code.**

## Detection (all three must be true)

1. No manifest: no `package.json`, `go.mod`, `Cargo.toml`, `pyproject.toml`, `requirements.txt`, `Gemfile`, `pom.xml`, `build.gradle`, `*.csproj`.
2. No source files outside config — only things like `.git/`, `README.md`, `LICENSE`, `.gitignore`.
3. No `CLAUDE.md` or `CONTRIBUTING.md` declaring conventions.

If ANY is false, this is a brownfield project: follow normal Phase 0 inference instead.

## Inverted rules in greenfield

Two rules from the main skill flip here. This is intentional — do not apply them as written:

| Normal rule | In greenfield |
|-------------|---------------|
| "No tooling → flag the lack of tooling as tech debt to propose" | Missing tooling is **step 1 of the work**, not debt. Build it, don't flag it. |
| "Never introduce layers speculatively" | The **minimum skeleton below is not speculative** — it is the demonstrated pattern every later feature copies. Anti-speculation still fully applies to *infrastructure* (see Deferred-until-earned). |

## Step 0 — Ask, with recommendations

Three decisions cannot be defaulted safely: guessing wrong wastes every step that follows.
**Ask them in ONE message, and skip any the user's prompt already answered**
("build a FastAPI REST API" answers shape + language — do not ask again).

The user may not know the trade-offs. So every question carries a recommendation in this shape:

> **Recommended: X** — <one line why>. Trades away: <what you give up>.

If the user says "you pick" / "whatever's best", proceed with the recommended defaults and
record them in `CLAUDE.md` at step 7.

### Q1 — What shape is this project?

Backend service · CLI tool · Frontend app · Library/SDK · Data pipeline

The shape determines the skeleton, so it has no universal default — infer it from the user's
description and confirm in one line rather than presenting a menu.

### Q2 — Language + runtime?

| Shape | Recommend | Why | Trades away |
|-------|-----------|-----|-------------|
| Backend service | **TypeScript + Node (Fastify)** | Schema validation and types at the edge satisfy the input-validation rule with one tool; largest hiring pool | Raw throughput vs Go; needs a build step |
| Backend service (data/ML-adjacent) | **Python 3.12 + FastAPI** | Pydantic makes edge validation declarative; native access to the data/ML ecosystem | Slower runtime; packaging is fussier |
| CLI tool | **Go** | Single static binary — nothing to install on the target machine | More verbose; no REPL loop |
| CLI tool (glue/scripting) | **Python + Typer** | Fastest to write and change | Target machine needs a Python runtime |
| Frontend app | **TypeScript + React + Vite** | Fastest dev loop; TS is required by the strong-typing rule | Heavier than plain HTML for a tiny UI |
| Library / SDK | **The consumers' language** | A library's stack is dictated by who imports it, never by preference | — |
| Data pipeline | **Python + polars/pandas** | Unmatched ecosystem for transforms | Single-node until an orchestrator is added later |

Always pin the runtime version (`.nvmrc`, `.python-version`, `mise.toml`, `go.mod` toolchain).

### Q3 — Where will this run?

| Answer | What it changes |
|--------|-----------------|
| **Not decided yet** ← recommend this if the user is unsure | Skip all deploy config. A Dockerfile written before a real target is usually wrong. Trades away: nothing recoverable — add it the day the target is known |
| Container (Docker/K8s/ECS) | Config strictly from env; add `Dockerfile` + `.dockerignore` at step 6 |
| Serverless | Handler stays a thin edge adapter; core must not import the vendor SDK |
| Binary / on-prem | Static build target; config from file + env |

## Steps 1-7 — Tooling before features

Strict order. Each step exists to give a later step or a later session something to find.

| # | Deliverable | Why here |
|---|-------------|----------|
| 1 | Manifest + pinned runtime version file | Everything below needs a deterministic runtime |
| 2 | `.gitignore` + `.env.example` | Created *before* any file that could leak a secret. Gives the "never hardcode secrets" rule a destination |
| 3 | Linter + formatter config | The first line of code is written conforming, instead of retrofitted later |
| 4 | Test runner + **one smoke test that passes** | Makes "use the project's existing test framework" answerable in session 2. Do not skip the passing run |
| 5 | Layer folders + **one real vertical slice** | See below — this is the step that matters most |
| 6 | CI — hand off to the `engineering-standards-ci` skill | Only now does that skill have a manifest and a test command to detect |
| 7 | `README.md` + **`CLAUDE.md`** | See below — this is what ends the greenfield state |

Recommended tooling for steps 3-4:

| Language | Lint/format | Test | Why |
|----------|-------------|------|-----|
| TypeScript | **Biome** | **Vitest** | One tool, one config, no eslint+prettier conflict; Vitest is ESM-native with a Jest-compatible API |
| Python | **ruff** (lint + format) | **pytest** | ruff replaces flake8 + isort + black in one binary |
| Go | **golangci-lint** + `gofmt` | stdlib `testing` (+ `testify` for assertions) | Ecosystem standard; nothing to argue about |
| Rust | `clippy` + `rustfmt` | `cargo test` | Built in |

Configure the file/function limits in the linter itself where supported
(`max-lines: 550`, `max-lines-per-function: 40`, `max-depth: 3`, `max-params: 5`)
so the limits are machine-enforced, not just prompt-enforced.

## Step 5 in detail — Vertical slice, never empty folders

Creating empty `domain/`, `application/`, `infrastructure/` folders IS speculative, and it
teaches the next session nothing. Instead build **the thinnest feature that crosses all three
zones** — a health endpoint, a `version` command, one list screen.

```
Backend example — GET /health
  edges/http/health_route.*      thin: parse → call use case → map response
  application/get_health.*       orchestrates, depends on the interface below
  domain/health.*                pure: no HTTP, no SQL, no SDK import
  domain/ports/clock.*           interface DEFINED BY the core
  infrastructure/system_clock.*  implements the port
  main.*                         composition root: wires the concrete into the port
```

This produces one real dependency inversion, so the pattern is **demonstrated, not documented**.
Features 2 through 50 copy it.

Guardrails at this step — the single highest-risk moment in a greenfield project, because there
is no existing code to imitate:

- Do **not** put the slice in one file "to get it working" — that is the exact failure this file exists to prevent.
- Every folder created must contain real code. No placeholders, no `index.ts` re-export stubs with nothing behind them.
- Hard limits apply from line one: file ≤ 550, function ≤ 40, params ≤ 5, nesting ≤ 3.
- The slice must be covered by the step-4 test runner and pass.

## Step 7 in detail — `CLAUDE.md` closes the loop

Write the decisions just made to disk. **This is what converts the repo to brownfield**, so the
next session's Phase 0 finds real conventions and never re-enters greenfield.

```markdown
# <Project> — Conventions

## Stack
<language + runtime version> · <framework> · <deploy target or "not decided">

## Layers (dependencies point inward)
- `domain/` — pure business rules. No HTTP, SQL, SDK, or framework imports.
- `application/` — use cases, coordinating domain via ports it defines.
- `infrastructure/` — port implementations: DB, external APIs, clock, storage.
- `edges/` — HTTP routes / CLI commands / UI. Thin: parse → call → map.
- `main.*` — composition root. Wiring lives only here.

## Commands
- Install: `<cmd>`
- Test: `<cmd>`
- Lint: `<cmd>`
- Run: `<cmd>`

## Limits
File ≤ 550 lines · function ≤ 40 · params ≤ 5 · nesting ≤ 3 · no copy-paste > 5 lines.

## Decisions made at bootstrap
- <choice> — <one-line reason>, so a future change knows what it is overturning.
```

Record the *reason* for each choice, not just the choice. A future session needs to know whether
a decision was deliberate or arbitrary before changing it.

## Deferred-until-earned

Anti-speculation applies in full to infrastructure. Do NOT create these at bootstrap — add each
one the day something actually needs it:

| Deferred | Earned when |
|----------|-------------|
| Dockerfile / compose | A real deploy target exists, or a second service needs local orchestration |
| DI container / framework | Manual wiring in the composition root becomes genuinely unwieldy (not before ~10 services) |
| Migration framework | A real schema exists and has changed once |
| Cache / queue / message-bus abstraction | A measured need, never an anticipated one |
| Monorepo tooling | There is an actual second package |
| Auth system | There is a real user, and a real thing to protect |
| API versioning (`/v1`) | There is an external consumer who can break |

Adding these early is the greenfield version of patch-on-patch: structure with no payoff, which
every later change must then work around.

## Done criteria

Bootstrap is complete when all of these hold:

- [ ] `<install>` then `<test>` succeeds from a clean clone
- [ ] `<lint>` passes with zero warnings
- [ ] The vertical slice runs and returns a real response
- [ ] No file exceeds 550 lines; no function exceeds 40
- [ ] No secret in any tracked file; `.env.example` documents every variable read
- [ ] Every folder created contains real code
- [ ] `CLAUDE.md` exists and its commands are copy-pasteable and verified
- [ ] CI runs lint + test on PR

Then report to the user in 3-5 lines: stack chosen, layers created, commands, what was
deliberately deferred. Following tasks proceed on the normal brownfield path.
