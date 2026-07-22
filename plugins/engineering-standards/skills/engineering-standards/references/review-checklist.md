# Code Review Checklist (Universal)

Group findings by severity:
- **Blocker** — must fix before merge
- **Should-fix** — fix in this PR unless justified
- **Nit** — optional improvement

## Blockers

- [ ] Layer violation: business logic in a handler/controller/component, or core importing framework/vendor/infrastructure
- [ ] Data scoping: query/operation on multi-user data without an explicit owning-identity filter (user/org/account id)
- [ ] Secrets, keys, or credentials hardcoded
- [ ] Injection risk: unparameterized queries, unsanitized input reaching interpreters/shells
- [ ] Unvalidated external input reaching core logic
- [ ] New file > 550 lines or function > 40 lines without split justification
- [ ] Circular dependency introduced

## Should-fix

- [ ] Duplicated block (> 5 lines) that should be extracted
- [ ] Weak typing where the language offers better (`any`, missing hints, stringly-typed data)
- [ ] Patch-on-patch smell: another special-case branch added to an already-branchy function
- [ ] Persistence model leaking across a layer boundary
- [ ] New behavior without a unit test; bug fix without a regression test
- [ ] Error swallowed (empty catch, bare except, ignored error return) or overly generic error where a specific one fits
- [ ] Function with > 5 parameters
- [ ] Copy of an existing function with slight variation instead of parameterizing

## Nits

- [ ] Vague names (`data`, `handle`, `process`, `temp`, `misc`)
- [ ] Commented-out code or unused imports left in
- [ ] "What" comments that should be renames
- [ ] Inconsistent naming/style with surrounding code

## Output format

```
## Review: <PR/file name>

### Blockers (N)
1. <file>:<line> — <finding>. Fix: <concrete suggestion>

### Should-fix (N)
...

### Nits (N)
...

### Overall
<1–3 sentences: architecturally sound? Maintainability trend? Tech-debt flags?>
```

Always propose the fix, not just the problem. If the diff is clean, say so — do not invent findings.
