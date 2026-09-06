---
name: engineering-standards-ci
description: Generate CI/CD configurations that enforce engineering standards automatically in your project's pipeline. Use when setting up or updating CI for a project, or when asked to generate GitHub Actions, pre-commit hooks, or PR templates. Detects project type from package.json, Cargo.toml, go.mod, etc. and generates appropriate linter/config templates.
---

# Engineering Standards CI Enforcement

Generate CI/CD configurations that automatically enforce engineering standards in your project's pipeline. This skill detects your project type and generates appropriate linter, formatter, and test configurations.

## What this skill does

- Detects project type from top-level files (`package.json`, `Cargo.toml`, `go.mod`, `requirements.txt`, etc.)
- Generates CI workflow files (GitHub Actions, GitLab CI, etc.)
- Generates pre-commit hooks configuration
- Generates PR templates with engineering standards checklist
- Adapts configurations to your existing tooling (uses your linter, not invents new ones)

## When to use

- Setting up CI for a new project
- Updating existing CI to enforce engineering standards
- Adding PR templates with standards checks
- Generating pre-commit hooks for local standards enforcement

## Output

Generate files in the project root or `.github/` directory as appropriate:
- `.github/workflows/ci.yml` — GitHub Actions workflow
- `.pre-commit-config.yaml` — pre-commit hooks
- `.github/pull_request_template.md` — PR template

## Discovery

Before generating configs, scan the project:
1. List top-level files to detect language/framework
2. Check for existing CI config (`.github/`, `.gitlab-ci.yml`, `Jenkinsfile`)
3. Check for existing linting/testing setup
4. Use existing tools when possible (don't reinvent)
5. If the scan finds NO manifest and NO tooling, see "Greenfield" below — there is nothing to detect yet

## Greenfield (no manifest, no tooling)

"Use existing tools, don't reinvent" has no answer in an empty repo, so do not stall on it:

- If invoked as **step 6 of `references/greenfield-bootstrap.md`** (from the `engineering-standards`
  skill), the manifest, linter, and test command already exist as of steps 1-4 — detect them
  normally and generate CI around those exact commands.
- If invoked **directly on an empty repo**, do not generate CI first. CI that lints and tests
  nothing is noise. Say so, and point the user at the bootstrap sequence — CI is meaningful only
  once there is a test command to run.

Never invent a linter or test runner that the project does not have installed: a workflow calling
a missing binary is a red CI badge, not enforcement.

## Templates

### GitHub Actions (`.github/workflows/ci.yml`)

Generate workflows that:
- Run on PR and push to main
- Install dependencies
- Run linter(s)
- Run formatter check
- Run tests
- Run security scans (if applicable)

### Pre-commit hooks (`.pre-commit-config.yaml`)

Generate hooks that:
- Run on every commit
- Check file sizes
- Run linters
- Run formatters
- Check for secrets (`.git-secrets` or `detect-secrets`)

### PR template (`.github/pull_request_template.md`)

Generate PR template with:
- Engineering standards checklist (from `references/review-checklist.md`)
- Architecture checklist (from `references/architecture-patterns.md`)
- Security checklist (from `rules/security.md`)

## Project detection

| Files found | Project type | Linters to generate |
|-------------|--------------|---------------------|
| `package.json` + `tsconfig.json` | Node/TypeScript | eslint, prettier, jest/vitest |
| `go.mod` | Go | golangci-lint, gofmt |
| `Cargo.toml` | Rust | clippy, rustfmt, cargo test |
| `requirements.txt` + `pyproject.toml` | Python | ruff, pytest |
| `Gemfile` | Ruby | rubocop, rspec |
| `.csproj` or `.sln` | C# | dotnet format, dotnet test |
| `pom.xml` or `build.gradle` | Java/Kotlin | checkstyle, Spotless, JUnit |

## Rules to enforce

Apply these engineering standards in CI:
- File size ≤ 550 lines
- Function size ≤ 40 lines
- Nesting depth ≤ 3 levels
- No hard-coded secrets
- All external input validated at edges
- Business logic separated from infrastructure
- Tests required for new functionality

## Workflow pitfalls (do not regenerate these)

The bundled template was rewritten to avoid three failure modes that produce a green badge over
a pipeline that enforced nothing. Any workflow you generate must avoid them too:

1. **`matrix` is not available in a job-level `if`.** Only `github`, `needs`, `vars` and `inputs`
   are. A job gated on `needs.detect.outputs.type == matrix.type` compares against null, so every
   leg skips silently. Detect once in a step, then gate **steps** on `steps.<id>.outputs`.
2. **Never `|| true` on a lint or test command.** It swallows the signal — the same error-swallowing
   the clean-code rule forbids. If a check is genuinely advisory (dependency audits, say), mark it
   `continue-on-error: true` so the result stays visible, and say in a comment why.
3. **A hard-limit violation is `::error::`, not `::warning::`.** A warning that also exits non-zero
   just teaches people to distrust the annotations.

Also required in every generated workflow: a least-privilege `permissions:` block (`contents: read`
unless a step needs more) and a `concurrency:` group so superseded runs are cancelled.

## Customization

If the project already has CI config, ADD to it rather than replacing. Preserve existing jobs and steps.

Where the linter supports the limits natively, configure them there (`max-lines: 550`,
`max-lines-per-function: 40`, `max-depth: 3`, `max-params: 5`) instead of adding a bespoke
line-counting script — one enforcement path, and it runs locally too.
