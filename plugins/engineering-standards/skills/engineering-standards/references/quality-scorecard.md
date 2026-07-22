# Quality Scorecard — Dimensional Rating Rubric

When asked to rate, score, audit, or assess code quality (or when a review would benefit from an at-a-glance summary), score each dimension 1–5 using the anchors below. Scores must be justified with concrete evidence (file:line), never vibes. A dimension with no relevant code in the diff is marked N/A, not 5.

## Scale anchors

**5 — Exemplary**: could be used as a reference example for the team.
**4 — Solid**: minor improvements possible, nothing structural.
**3 — Acceptable**: works, but has should-fix issues that will cost time later.
**2 — Weak**: structural problems; changes here will be slow and risky.
**1 — Failing**: blocker-level issues; do not merge.

## Dimensions

### Maintainability
- 5: Clear layer separation; files/functions within limits; changes would be localized; intent obvious without archaeology.
- 3: Mostly organized but some fat files/functions or mixed responsibilities; a new dev needs guidance.
- 1: God files, patch-on-patch branches, logic scattered across layers; any change risks regressions.

### Scalability
Judge *architectural* scalability (can it grow?) and *runtime* scalability (can it handle load?) as relevant:
- 5: Stateless where it should be; no unbounded growth (memory, connections, result sets); pagination/batching on collections; work parallelizable or queueable if volume grows; no design that requires rewrite at 10x.
- 3: Fine at current scale, but has known ceilings (e.g., loads full table into memory, N+1 pattern, single synchronous path for heavy work).
- 1: Guaranteed to fall over with growth: unbounded queries, per-request global locks, hardcoded single-instance assumptions.

### Performance
- 5: Appropriate algorithms/data structures; no obvious wasted work; IO batched; hot paths lean; no premature micro-optimization that hurts clarity.
- 3: Correct but wasteful in places (repeated computation, chatty IO, sequential awaits that could batch) — acceptable unless on a hot path.
- 1: Pathological patterns: O(n²) on unbounded data, queries in loops, loading everything to filter in memory.

### Security
- 5: Input validated at the edge; parameterized queries; least-privilege access; secrets from config/secret manager; multi-user data scoped by owner identity; errors don't leak internals.
- 3: Core paths safe, but gaps: weak validation on secondary inputs, over-broad permissions, verbose error leakage.
- 1: Injection vector, hardcoded secret, missing tenant/owner scoping, or unauthenticated sensitive operation.
(Any single blocker-level security finding caps this dimension at 1 regardless of everything else.)

### DRY & Abstraction
- 5: No meaningful duplication; abstractions extracted at the right time (2nd–3rd occurrence), well-named, not speculative.
- 3: Some copy-paste blocks or near-duplicate functions; or the opposite sin — premature abstraction adding indirection without payoff.
- 1: Systematic duplication (parallel implementations drifting apart) or abstraction soup nobody can follow.

### Readability
- 5: Intent-revealing names; consistent style; small focused units; comments explain why; a reviewer understands flow in one pass.
- 3: Understandable with effort; some vague names, long functions, or missing types.
- 1: Cryptic names, deep nesting, dead code, no types; requires the author to explain it.

## Output format

```
## Quality Scorecard: <scope>

| Dimension       | Score | Key evidence |
|-----------------|-------|--------------|
| Maintainability | x/5   | <file:line — one-phrase reason> |
| Scalability     | x/5   | ... |
| Performance     | x/5   | ... |
| Security        | x/5   | ... |
| DRY             | x/5   | ... |
| Readability     | x/5   | ... |

**Overall: x.x/5** — <1–2 sentence verdict>

### Top 3 actions to raise the score
1. <highest-leverage fix>
2. ...
3. ...
```

Rules:
- Overall = average of scored dimensions (excluding N/A), but any dimension at 1 means the verdict must say "not mergeable" regardless of average.
- Always include "Top 3 actions" — a score without a path to improve it is useless.
- Keep evidence honest: if the code is good, score it high; do not manufacture findings to seem thorough.
