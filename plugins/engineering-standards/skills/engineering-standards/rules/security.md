# Security Rules (Universal)

These rules apply whenever code touches data access, authentication, user input, or external systems.

## Data scoping

- Any code touching multi-user or multi-tenant data MUST scope every query/operation by the owning identity (user id, org id, account id) as an explicit parameter — never inferred implicitly deep inside.
- If unsure whether data is scoped, ask the user; do not guess.

## Secrets and credentials

- Never hardcode secrets, keys, or credentials in source code.
- Configuration comes from environment variables, config files, or secret managers.
- `.env` files and credential files are NEVER committed to version control.
- If a project has no secret management, flag it as tech debt and propose a minimal setup.

## Input validation

- All external input is validated at the edge before reaching core logic.
- Validation rules live at the boundary; core logic assumes validated input.
- Use parameterized queries, prepared statements, or safe encoding for all data going to interpreters, shells, or databases.

## Authentication and authorization

- Never bypass auth checks in "convenience" paths.
- Authorization is per-operation, not per-route — check the specific permission, not just "is logged in".
- Principle of least privilege: give only what is needed, nothing more.

## Error handling (security angle)

- Do not leak internal stack traces, SQL queries, file paths, or implementation details in error responses.
- Use generic error messages for users; log detailed errors internally.
