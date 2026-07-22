# Infrastructure as Code — Universal Standards

These principles apply regardless of tool (Terraform, OpenTofu, CloudFormation, Pulumi, CDK, Ansible, Kubernetes manifests, Helm). Tools change; the rules below don't.

## Structure: modules over monoliths

The layering rule translated to IaC:

1. **Reusable modules/components** — the "core": parameterized definitions of one cohesive thing (a network, a database, a service). No environment-specific values inside.
2. **Composition/environments** — the "edges": `dev/`, `staging/`, `prod/` (or stacks/workspaces) that instantiate modules with concrete values.

FORBIDDEN:
- Environment values (account ids, instance sizes, domain names) hardcoded inside a reusable module — inject via variables/parameters.
- One giant file defining everything ("main.tf with 2000 lines" or a single mega-template) — same ≤400-line file rule applies; split by resource domain (network, compute, data, iam).
- Copy-pasting a module per environment with small edits — parameterize instead (the IaC version of `processDataV2`).

## Hard rules

- **No secrets in code, state, or variables files committed to git.** Secrets come from a secret manager or injected at deploy time. `.tfvars`/parameter files with credentials never enter version control.
- **Explicit naming/tagging convention**: every resource carries owner/environment/project identifiers so cost and ownership are traceable.
- **Least privilege**: IAM/roles/policies scoped to what the component needs — no wildcard `*` actions/resources without written justification in the code.
- **Pin versions**: providers, modules, images, charts pinned to versions or digests. "latest" in production IaC is a blocker.
- **Idempotency**: applying twice must not change anything the second time. Scripts that shell out imperatively inside IaC break this — isolate them.

## Change discipline (anti-patching for infra)

- Before adding a resource to an existing file, check cohesion: does it belong to this file's domain, or is the file becoming a dumping ground?
- Never fix drift by clicking in a console/UI — fix in code, then apply. Flag manual changes as debt.
- Destructive changes (rename that forces recreate, deletion of stateful resources like databases/storage) must be called out EXPLICITLY in the plan summary before applying, never buried.
- One change = one concern. Do not mix a networking refactor with an application deploy in the same changeset.

## Review checklist additions (for IaC diffs)

Blockers:
- [ ] Secret, key, or credential in code/vars
- [ ] Wildcard IAM permission without justification
- [ ] Unpinned provider/module/image version in production path
- [ ] Destructive change (recreate/delete of stateful resource) not explicitly flagged
- [ ] Public exposure (open security group/bucket/endpoint) without justification

Should-fix:
- [ ] Environment value hardcoded inside a reusable module
- [ ] Duplicated resource blocks that should be a parameterized module/loop
- [ ] Missing standard tags/labels (owner, environment, project)
- [ ] File exceeding size limit / mixing unrelated resource domains

## Testability

- Prefer tools' native validation in CI: format check, validate/lint (tflint, cfn-lint, kubeval, ansible-lint — whichever fits the stack), plan/diff review as a required gate.
- A plan/preview must be reviewed before apply in shared environments — never auto-apply to prod without a human or policy gate.
