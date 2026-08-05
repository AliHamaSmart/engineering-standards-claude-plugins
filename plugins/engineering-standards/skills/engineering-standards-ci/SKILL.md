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

## Customization

If the project already has CI config, ADD to it rather than replacing. Preserve existing jobs and steps.
