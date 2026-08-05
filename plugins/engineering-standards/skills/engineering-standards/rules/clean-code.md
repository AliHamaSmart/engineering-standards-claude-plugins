# Clean Code Rules

Universal rules for readability, intent, and correctness. These apply to every line of output.

## DRY — but not premature

- Extract on the 2nd–3rd real duplication, not speculatively.
- Premature abstraction adds indirection without payoff.
- When in doubt, duplicate once, refactor the second time.

## Naming describes intent

- `syncCalendarEvents`, not `processData` / `handleStuff` / `doWork`.
- No cryptic abbreviations except universal ones: `id`, `db`, `url`, `i` in a tiny loop.
- Variable names should answer "what is this?" without context.
- Function names should answer "what does this do?" when read in isolation.

## No dead code

- No commented-out blocks.
- No unused imports.
- No unreachable branches in final output.
- If something is commented out for "future reference", move it to git history, not the file.

## Errors are handled, not swallowed

- No bare / empty catch.
- Raise meaningful, specific errors in core logic.
- Translate to transport-appropriate errors (HTTP status, exit code, UI message) only at the edge.
- A swallowed error is one of the most common silent bugs — never tolerate it.

## Types

- Use the strongest typing the language offers (type hints, strict mode, no `any`-equivalents).
- Prefer explicit types over inference when inference would lose information.
- Generic types are fine; avoid `any`/`object`/`interface{}` unless there's a good reason.

## Immutability by default

- Where the language supports it cheaply, prefer immutable data.
- Mutate only with reason.
- Pure functions where possible.

## Comments explain WHY, not what

- If code needs a "what" comment, rename or restructure instead.
- Comments should explain the intent, the trade-off, or the reason for a non-obvious decision.
- Dead comments (out of sync with code) are worse than no comments — delete stale ones.

## English identifiers

- Code, identifiers, and comments in English.
- Explanations to the user in the user's language.
