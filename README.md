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
2. **Branches** — existing project → adapt to it; **empty repo → greenfield bootstrap** (see below)
3. **Adapts rules** — Uses your existing tools (Jest, pytest, golangci-lint, etc.) instead of inventing new ones
4. **Applies standards** — Enforces architecture layering, size limits, DRY, security, anti-patching

### Starting from scratch (empty repo)

Discovery has nothing to infer from an empty repo, so it switches to a bootstrap sequence instead
of falling back to defaults:

1. **Asks** the three decisions that can't be defaulted — project shape, language/runtime, deploy
   target — each with a recommendation and the reason behind it (say "you pick" to take the defaults)
2. **Tooling before features** — manifest + pinned runtime → `.gitignore` + `.env.example` →
   linter/formatter → test runner with one passing smoke test
3. **One real vertical slice**, not empty layer folders — a single thin feature crossing
   edge → use case → pure domain → adapter, so the pattern is demonstrated for every later feature
4. **CI** — handed to the `engineering-standards-ci` skill, which now has real commands to wrap
5. **`CLAUDE.md`** — writes the chosen stack, layers, commands, and limits to disk, so the next
   session finds conventions and runs on the normal path

Infrastructure stays deferred until earned: no Dockerfile, DI container, migration framework,
cache abstraction, or auth system until something actually needs it.

## How to install

Two commands, from inside Claude Code:

```
/plugin marketplace add AliHamaSmart/engineering-standards-claude-plugins
/plugin install engineering-standards
```

Then **start a new session** — hooks and skills load at session start. That is the whole setup:
no config file to write, no per-project step, no dependencies to install. It applies to every
project you open, and adapts to each one at the start of every task.

### Verify it took

```bash
claude plugin details engineering-standards
#   Skills (2)  engineering-standards, engineering-standards-ci
#   Hooks (3)   SessionStart, PreToolUse, PostToolUse
#   Always-on:  ~391 tok   added to every session

claude plugin list      # Status should read: ✔ enabled
```

If `plugin list` shows anything other than `✔ enabled`, read the error there — `plugin validate`
does not catch every load failure, so `list` is the authoritative check.

### What you'll notice afterwards

| When | What happens |
|------|--------------|
| Every session starts | A short standards digest enters context — limits, layering, data safety |
| You ask for code | Phase 0 scans the project first and reports what it found in a line or two, then writes code adapted to your existing test runner and linter |
| A write would exceed 550 lines | **Blocked** before it reaches disk, with the reason. Claude plans a module split instead of retrying |
| A write carries a credential | **Blocked.** Claude rewrites it to read from the environment |
| A file passes 450 / 550 lines | Reported back so the split happens now, not three edits later |
| The repo is empty | Greenfield: you get stack questions with recommendations before any code is written |

Nothing is blocked silently — every block states what tripped and what to do instead.

### Requirements

Claude Code v1.0+, and `python3` on PATH used only by the hooks. Stdlib only, nothing to
`pip install`. Present by default on Ubuntu, Debian, Fedora, and macOS with Xcode CLT. Without it
the skills still work; the hooks report a non-blocking error and enforce nothing.

No other dependencies, and no project setup — it works against any language or framework. A git
repo is needed only for the CI-template generation.

### Update, disable, uninstall

```bash
claude plugin update engineering-standards      # pull the latest published version
claude plugin disable engineering-standards     # keep it installed, stop it loading
claude plugin enable engineering-standards
claude plugin uninstall engineering-standards   # remove entirely
```

Updates are not automatic — run `update` to pick up new rules or hook fixes. Restart the session
after any of these; plugins load at session start.

### Scope

Installing as above enables it for **your user**, in every project you open. To scope it to one
repo instead, put this in that repo's `.claude/settings.json` and skip the user-level install:

```json
{
  "extraKnownMarketplaces": {
    "engineering-standards": {
      "source": { "source": "github", "repo": "AliHamaSmart/engineering-standards-claude-plugins" }
    }
  },
  "enabledPlugins": { "engineering-standards@engineering-standards": true }
}
```

Committing that file gives every teammate the plugin when they open the repo, with no setup on
their side. A marketplace name can only have one source, so do not declare it both ways.

<details>
<summary>Other install routes</summary>

```bash
# From the CLI instead of the slash command
claude plugin marketplace add AliHamaSmart/engineering-standards-claude-plugins
claude plugin install engineering-standards@engineering-standards

# From a local checkout, for working on the plugin itself.
# Note the `./` — a bare `.` is rejected as an invalid source format.
claude plugin marketplace add ./

# Skills only, no hook enforcement — the size and secret checks become
# advice rather than enforcement.
cp -r plugins/engineering-standards/skills/engineering-standards    ~/.claude/skills/
cp -r plugins/engineering-standards/skills/engineering-standards-ci ~/.claude/skills/
```

</details>

## Enforcement layers

The standards are enforced at three levels, weakest to strongest:

| Layer | Mechanism | Strength |
|-------|-----------|----------|
| Skills | `SKILL.md` + `rules/` loaded into context | Guidance — depends on the model applying it |
| Hooks | `hooks/hooks.json` run by the harness | **Deterministic** — runs whether or not the model cooperates |
| CI | Workflow + pre-commit generated by the CI skill | Deterministic, and applies to human commits too |

The bundled workflow detects the project type once and gates **steps**, not jobs — a job-level `if`
cannot read the `matrix` context, so the common matrix-per-language shape skips every leg and
reports success having run nothing. Lint and test failures are never swallowed with `|| true`;
dependency audits are the one advisory check, and they say so.

### What the hooks do

| Hook | Event | Behavior |
|------|-------|----------|
| `session_standards.py` | `SessionStart` | Injects a compact digest of the limits, layering, and data-safety rules — so the standards are in context even if the skill is never selected |
| `pre_write_guard.py` | `PreToolUse` on `Write`/`Edit`/`MultiEdit` | **Blocks** a whole-file write over 550 lines, and **blocks** content carrying a hardcoded credential (AWS key, private key block, GitHub/Slack/Google/OpenAI-style token, or a credential assigned a literal) |
| `post_write_check.py` | `PostToolUse` on `Write`/`Edit`/`MultiEdit` | Re-counts the file on disk and reports back when it crosses 450 (advisory) or 550 (must split now) — this is what catches edits accumulating over several calls |

Design notes:

- **Only checks that are reliable are enforced.** Function length and nesting depth need a real
  parser per language, so they stay with the linter that the CI skill configures
  (`max-lines-per-function`, `max-depth`, `max-params`) rather than a guessy regex.
- **Size limits apply to source only.** Docs, data, lock files, snapshots, migrations, generated
  and vendored output are exempt — a hook that cries wolf gets ignored.
- **Placeholders are not secrets.** Lines referencing `process.env`, `os.environ`, `${...}`, a
  secret manager, or an obvious dummy value pass through, as do `.env.example` and fixture files.
- **Every hook fails open.** A malformed payload, unreadable file, or unexpected error exits 0
  and lets the session continue. A broken guard would be worse than no guard.

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
.github/workflows/ci.yml                      # This repo's own CI: hook tests + manifest validation
tests/test_hooks.py                          # Contract tests for the hooks (stdlib only)
plugins/engineering-standards/
├── .claude-plugin/plugin.json               # Plugin manifest (points at hooks/hooks.json)
├── hooks/
│   ├── hooks.json                           # SessionStart + Pre/PostToolUse registrations
│   └── scripts/
│       ├── hooklib.py                       # Shared helpers, limits, path exemptions
│       ├── pre_write_guard.py               # Blocks oversized writes + hardcoded secrets
│       ├── post_write_check.py              # Re-counts the file on disk after a write
│       └── session_standards.py             # Injects the standards digest each session
└── skills/
    ├── engineering-standards/               # Core engineering standards skill
    │   ├── SKILL.md                         # Orchestrator — discovery protocol + rule references
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

## Troubleshooting

**Plugin not activating?**
- Start a new session — plugins load at session start, not mid-session
- `claude plugin list` must show `✔ enabled`. Any other status prints the reason
- `claude plugin update engineering-standards` if you installed before a fix you are expecting

**Rules not adapting to my project?**
- The plugin scans top-level files on each task — make sure your project files are in the repo root
- Some project types (mobile, CLI) may not have standard detection files — the plugin will fall back to default rules

**Hooks not firing?**
- `/hooks` lists what the harness has registered — the three entries should appear there
- Hooks load from a plugin install, not from a copy into `~/.claude/skills/`
- Verify `python3 --version` works in the same shell Claude Code runs in
- Drive the installed copy directly — this is the fastest way to see what a hook actually decides:

  ```bash
  HOOKS=$(find "${CLAUDE_CONFIG_DIR:-$HOME/.claude}/plugins" -path '*engineering-standards/hooks/scripts' -type d | head -1)
  echo '{"tool_input":{"file_path":"/x/a.py","content":"API_KEY = \"aB3dE5fG7hJ9kL1mN3pQ\""}}' \
    | python3 "$HOOKS/pre_write_guard.py"
  # prints a deny decision; silence means the hook allowed it
  ```

**A hook blocked something legitimate?**

Do not edit the installed copy — `claude plugin update` overwrites it. Open an issue or a PR
against this repo so the fix reaches everyone:

- Oversized generated or data files → the path exemption list `_UNCHECKED_PATH` in `hooks/scripts/hooklib.py`
- A false-positive secret → `PLACEHOLDER` or `SECRET_EXEMPT` in `hooks/scripts/pre_write_guard.py`

Every such report should come with the exact line that tripped, so it can become a test case.

**Need it off for one session?** `claude plugin disable engineering-standards`, restart. That is
better than working around a block, which defeats the check the hook exists to run.

**CI template not generating?**
- Make sure you're in a Git repository
- Run `generate ci for this project` in the repo root

## Contributing

```bash
python3 tests/test_hooks.py                          # 31 contract tests, no dependencies
claude plugin validate plugins/engineering-standards # manifest schema
claude plugin validate .                             # marketplace schema
```

The hooks are tested through their real interface — a JSON payload on stdin, a decision on stdout —
covering blocks, allows, path exemptions, secret false-positives, prefixed credential names, and fail-open behavior. CI also
checks that the hook scripts obey the plugin's own limits and that the manifest versions agree.

## License

MIT — see [LICENSE](LICENSE). Copyright holder is "Uninote Engineering", matching the `author`
already declared in both manifests; change both together if that is not the right entity.

## For Maintainers

To release to marketplace:

1. Edit files under `plugins/engineering-standards/skills/` (guidance) or `plugins/engineering-standards/hooks/` (enforcement)
2. Bump `version` in `plugins/engineering-standards/.claude-plugin/plugin.json` and in `.claude-plugin/marketplace.json`
3. Commit & push

Users refresh with:
```
/plugin marketplace update engineering-standards
```

