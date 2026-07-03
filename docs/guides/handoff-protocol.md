# Handoff Protocol

Use this protocol whenever a migration moves from one phase owner to the next. The goal is simple: every handoff is backed by artifacts, status, and explicit quality gates.

## Core Rules
1. **No handoff without artifacts.** `It is almost done` is not a handoff.
2. **`reports/Report-Status.md` is the handoff document.** Every phase updates it before asking the next role to start.
3. **Block early.** If a quality gate fails, stop and record the blocker in the status report.
4. **Hand off facts, not assumptions.** Identify what was verified, what is inferred, and what is still unknown.
5. **Name the next owner.** Every handoff must assign a human owner and expected agent.

## Required Artifacts by Phase Transition

| Transition | Required artifacts before next phase starts | Primary owner | Quality gate that blocks progress |
|------------|---------------------------------------------|---------------|-----------------------------------|
| Phase 0 → Phase 1 | `codebase-repos.md`, multi-repo summary, recommended migration order, shared risks | Migration Lead / Architect | Repo scope unresolved, dependencies unclear, or app order not agreed |
| Phase 1 → Phase 2 | `reports/Application-Assessment-Report.md`, initialized `reports/Report-Status.md`, approved target platform/IaC/database choices | Migration Lead / Architect | Scope not approved, target architecture unclear, blockers unowned |
| Phase 2 → Phase 3 | Modernized codebase, build evidence, config mapping, migration notes, updated `Report-Status.md` | App Developer / Coder | App does not build, core paths unverified, breaking changes undocumented |
| Phase 3 → Phase 4 | `infra/`, `azure.yaml`, parameter files, secrets/RBAC approach, deploy prerequisites, updated `Report-Status.md` | Cloud Engineer / Azure Specialist | IaC not reviewable, environment assumptions missing, secret strategy undefined |
| Phase 4 → Phase 5 | Deployment summary report, endpoint list, smoke test results, runtime issues list, updated `Report-Status.md` | Cloud Engineer / Azure Specialist | Manual deployment path failed, endpoints unhealthy, rollback path unknown |
| Phase 5 → Closeout | Pipeline files, `reports/cicd_setup_report.md`, required secrets, approvals, release ownership, updated `Report-Status.md` | DevOps Engineer / Coder | Pipeline cannot reproduce build/deploy, approvals unclear, smoke tests missing |

## Standard Handoff Checklist

Copy this checklist into the active use-case notes or paste it into the handoff issue/PR description.

```md
## Phase Handoff Checklist
- [ ] Current phase owner updated `reports/Report-Status.md`
- [ ] Required artifacts are committed or linked
- [ ] Build/test/deploy evidence is attached
- [ ] Open risks and blockers are listed with owners
- [ ] Next phase owner is named
- [ ] Recommended next command/prompt is included
- [ ] Security implications are called out
- [ ] Rollback or recovery path is documented if applicable
```

## How to Use `reports/Report-Status.md` as the Handoff Document

Every update to `reports/Report-Status.md` should include these sections:

```md
# Report Status - <App Name>

**Current Phase:** <Phase name>
**Status:** <Not started | In progress | Blocked | Complete>
**Owner:** <Human role>
**Agent:** <Architect | Coder | Tester | Azure Specialist | Security Auditor>
**Updated:** <YYYY-MM-DD HH:MM>

## Summary
- What was completed
- What was verified
- What remains open

## Completed Actions
- [x] Item
- [x] Item

## Handoff Artifacts
- `path/to/file-or-folder`
- `path/to/file-or-folder`

## Quality Gates
- [x] Gate passed
- [ ] Gate pending
- [ ] Gate failed: explain blocker

## Risks / Blockers
- Severity, issue, owner, target date

## Next Step
- **Next owner:** <role>
- **Next Agent:** <agent>
- **Recommended prompt/command:** `<exact prompt or slash command>`
```

### Minimum status update standard
- Keep it short enough to scan in one minute.
- Include links or relative paths to the actual artifacts.
- State the next command explicitly, for example `/phase2-migratecode` or `/phase3-generateinfra`.
- Record blockers even when they are uncomfortable; hidden blockers cause rework.

## Quality Gates by Phase

### Phase 0: Portfolio Discovery
- App list is complete enough to sequence work.
- Shared dependencies and integration points are documented.
- Migration order is agreed.

### Phase 1: Planning & Assessment
- Hosting platform, IaC tool, and database target are explicit.
- Assessment report exists and is reviewable.
- Risks, blockers, and effort estimate are documented.
- Team agrees to proceed, pause, or reduce scope.

### Phase 2: Code Migration
- Modernized app builds successfully.
- Functional parity assumptions are documented.
- Config/secrets model is mapped from legacy to modern form.
- Deferred remediation items are listed.

### Phase 3: Infrastructure Generation
- IaC is parameterized and human-readable.
- Identity, secrets, and RBAC approach are documented.
- Monitoring/logging resources are defined.
- Deployment prerequisites are written down.

### Phase 4: Deployment
- At least one manual deployment path succeeds.
- App health, endpoint checks, and basic smoke tests pass.
- Runtime issues and rollback notes are captured.
- The team knows what is still manual.

### Phase 5: CI/CD
- Pipeline repeats the known-good build and deployment path.
- Required secrets, environments, and approval gates are documented.
- Smoke tests and failure ownership are included.
- Rollback or recovery procedure is part of the release path.

## What Blocks Progress
- Missing or stale `Report-Status.md`
- No clear next owner
- No evidence for a claimed build/deploy success
- Security-critical gaps with no remediation plan
- Manual deployment not working but pipeline work starting anyway
- Phase work started from verbal handoff instead of committed artifacts

## BookShop as the Reference Standard
Use `Use-cases/05-BookShop/reports/Report-Status.md` as the model for a strong handoff document:
- short summary at the top
- completed actions list
- clear key findings
- explicit next action

If your status file is weaker than the BookShop example, improve it before handing off.
