# File Size & Function Limits

These are hard limits. Never violate them. If a request would produce output that exceeds these limits, plan the module split BEFORE writing any code.

## File length

- **≤ 550 lines per file.** This is the maximum.
- If your planned output would exceed 550 lines, stop and split BEFORE writing.
- Aim lower when possible: 200-300 lines is the sweet spot for maintainability.
- A "utils" or "helpers" file that grows past 100 lines is almost always a smell — extract by responsibility instead.

## Function / method length

- **≤ 40 lines per function or method.** This is the maximum.
- Extract helpers when a function exceeds 40 lines.
- Extract on the 2nd or 3rd logical step — don't wait until a function is 80 lines.

## Function parameters

- **≤ 5 parameters per function.**
- Beyond 5, group into an object / struct / record / data class.
- Named parameters / keyword arguments are preferred over positional.

## Nesting depth

- **≤ 3 levels of nesting.**
- Use early returns and guard clauses to flatten.
- Extract inner logic into named functions to reduce visual nesting.

## Single responsibility

- One file = one cohesive purpose.
- A file that does auth, data access, and UI logic is violating this rule.
- When a file has multiple responsibilities, split it before committing.

## When limits are already violated in existing code

- Do not rewrite the entire file in the same change.
- New code within or adjacent to the file follows the limits.
- Flag the existing violation as debt with a concrete follow-up suggestion.
