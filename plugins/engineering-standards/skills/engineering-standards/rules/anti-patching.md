# Anti-Patching Rule (Maintainability)

When modifying existing code, never just bolt things on.

## The anti-patching workflow

1. **Check the file first.** Before adding to a file, check: is it already near or over 550 lines, or is the target function already complex? If yes, propose a small extraction / refactor as part of the change.
2. **Boy scout rule.** Leave touched code slightly better — but keep refactors scoped to what you touch. Do not rewrite unrelated code in the same change.
3. **Guard clauses over branches.** If a "quick fix" would add another special-case branch to an already-branchy function, extract a strategy / handler / lookup instead.
4. **No near-duplicates.** Never duplicate an existing function with a slight variation ("processDataV2") — parameterize or compose.
5. **Flag tech debt explicitly.** If the proper fix is out of scope, say so and describe the follow-up. Hidden debt is a violation.

## What counts as "patching"

| ✅ Good | ❌ Patching |
|---------|------------|
| Extract a new helper function | Add another `if/else` branch |
| Create a new file for a new concern | Stuff everything into the existing file |
| Parameterize a duplicated function | Copy-paste and rename ("v2", "v3", "New") |
| Refactor on the way you touch code | Leave a broken file "for another PR" |

## Patching detection signals

Watch for these smells in code you're about to write:
- A function that grows from 30 → 45 lines because of "just one more case"
- A file that gains a second or third responsibility
- A new function that is 90% identical to an existing one
- A `TODO` comment left inside the code with no follow-up

Flag any of these. Don't let them accumulate.
