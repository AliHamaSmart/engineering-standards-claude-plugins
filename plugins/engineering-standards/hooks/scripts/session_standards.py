#!/usr/bin/env python3
"""SessionStart injection: make "always active" actually always active.

Skill selection is a model decision, so it can be missed. This digest is
injected by the harness every session, which guarantees the limits are in
context before the first line of code. It is deliberately short — the full
rules stay in the skill, loaded on demand.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import hooklib  # noqa: E402

DIGEST = """Engineering standards are active for this session (engineering-standards plugin).

Hard limits: file <= 550 lines, function <= 40 lines, parameters <= 5, nesting <= 3 levels,
never copy-paste a block > 5 lines, one file = one cohesive purpose.

Layering: dependencies point inward. domain (pure: no HTTP/SQL/SDK/framework imports)
<- application (use cases via ports it defines) <- edges (routes, CLI, UI, DB, external APIs).
Business logic inside a handler or component is forbidden.

Data safety: every query on multi-user data is scoped by an explicit owner identity
(user/org/account id). Secrets come from env or a secret manager, never source. External
input is validated at the edge.

Before writing code: run Phase 0 project discovery. If the repo is empty, that is greenfield —
read references/greenfield-bootstrap.md and follow it; do not improvise a structure.

Write/Edit calls are hook-checked: an oversized whole-file write or a hardcoded credential is
blocked outright, and files crossing the size threshold are reported back.
Full rules: the engineering-standards skill (rules/ and references/)."""


def main():
    hooklib.add_context("SessionStart", DIGEST)


if __name__ == "__main__":
    try:
        main()
    except Exception:
        sys.exit(0)  # fail open
