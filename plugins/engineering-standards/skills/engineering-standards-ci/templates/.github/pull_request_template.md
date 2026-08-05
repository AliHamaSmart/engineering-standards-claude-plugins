# Engineering Standards Checklist

## Architecture
- [ ] Business logic is separated from infrastructure (core vs edges)
- [ ] No framework/vendor imports in business logic files
- [ ] No circular dependencies between modules
- [ ] New file/function structure follows project conventions

## Code Quality
- [ ] No file exceeds 550 lines
- [ ] No function exceeds 40 lines
- [ ] Nesting depth ≤ 3 levels (early returns / guard clauses used)
- [ ] No copy-paste blocks > 5 lines (extracted and reused)
- [ ] One file = one cohesive purpose (no "utils" dumping ground)

## Anti-Patching
- [ ] New code follows existing patterns (no bolt-on patches)
- [ ] No duplicated functions with slight variations
- [ ] No "TODO" comments left in final code
- [ ] Modified files improved slightly (boy scout rule)

## Security
- [ ] No hard-coded secrets, keys, or credentials
- [ ] External input validated at the edge
- [ ] Multi-user data scoped by owning identity (user/org id)
- [ ] Errors handled, not swallowed (no empty catches)

## Testing
- [ ] New functionality has unit tests
- [ ] Bug fixes have regression tests
- [ ] Core logic testable without real DB/network/filesystem

## Naming & Documentation
- [ ] Variables/functions named for intent, not implementation
- [ ] No cryptic abbreviations
- [ ] Comments explain WHY, not what
- [ ] No dead code (commented-out blocks, unused imports)

## What changed?
<!-- Describe the changes in this PR -->

## Why?
<!-- Explain the motivation for these changes -->

## How does this affect the architecture?
<!-- Did you add new layers? New dependencies? New abstractions? -->
