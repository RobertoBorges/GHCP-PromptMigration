# Handoff Protocol

Use this protocol whenever a migration moves from one phase owner to the next. The goal is simple: every handoff is backed by artifacts, status, and explicit quality gates.

The canonical machine-readable contract lives in `.github/skills/migration-artifacts/references/migration-handoff.md`. This page is the human version.

## Core Rules
1. **No handoff without artifacts.** `It is almost done` is not a handoff.
2. **`reports/Report-Status.md` is the handoff document.** Every phase updates it — including its `## 📜 Action Log` — before asking the next role to start.
3. **Block early.** If a quality gate fails, stop and record the blocker in the status report.
4. **Hand off facts, not assumptions.** Identify what was verified, what is inferred, and what is still unknown. Discovery carries this as `evidence_confidence: high | medium | low`.
5. **Name the next owner.** Every handoff must assign a human owner and expected agent.
6. **Never hand off past a pending decision.** If `reports/Decisions-Required.md` still shows `⏸ PENDING` for anything the next phase depends on, the handoff is blocked. Architecture decisions belong to the user, not the agent.

## Required Artifacts by Phase Transition

| Transition | Required artifacts before next phase starts | Primary owner | Quality gate that blocks progress |
|------------|---------------------------------------------|---------------|-----------------------------------|
| Discovery → Phase 1 | `reports/Discovery-Dossier.md`, `reports/Capability-Matrix.yaml` with confidence labels on source/stack/workload/data/integrations | Discovery Engineer | No Capability Matrix, or a `low` confidence field that Phase 1 depends on |
| Phase 0 → Phase 1 *(multi-repo only)* | `codebase-repos.md`, cross-repo summary, recommended migration order, shared risks | Migration Lead / Architect | Repo scope unresolved, dependencies unclear, or app order not agreed |
| Phase 1 → Phase 2 | `reports/Migration-Plan.md`, `reports/Application-Assessment-Report.md`, `reports/Decisions-Required.md` with every Phase 2 item `✅ DECIDED` or `🚫 N/A`, initialized `reports/Report-Status.md` | Migration Lead / Architect | Scope not approved, target architecture unclear, any required decision still pending |
| Phase 2 → Phase 3 | Modernized codebase, build evidence, config mapping, `reports/Business-Logic-Mapping.md`, updated `Report-Status.md` | App Developer / Coder | App does not build, core paths unverified, breaking changes undocumented, business logic unmapped |
| Phase 3 → Phase 4 | `infra/`, `azure.yaml`, parameter files, secrets/RBAC approach, deploy prerequisites, updated `Report-Status.md` | Cloud Engineer / Azure Specialist | IaC not reviewable, environment assumptions missing, secret strategy undefined |
| Phase 4 → Phase 5 | `reports/Deployment-Summary-Report.md`, endpoint list, smoke test results, runtime issues list, updated `Report-Status.md` | Cloud Engineer / Azure Specialist | Manual deployment path failed, endpoints unhealthy, rollback path unknown |
| Phase 5 → Phase 6 | Pipeline files, `reports/cicd_setup_report.md`, required secrets, approvals, release ownership, updated `Report-Status.md` | DevOps Engineer / Coder | Pipeline cannot reproduce build/deploy, approvals unclear, smoke tests missing |
| Phase 6 → Closeout | `reports/Post-Migration-Ops-Report.md`, `reports/Operational-Runbook.md`, alert ownership, cost baseline, updated `Report-Status.md` | Observability Engineer | No runbook, no alert owner, no performance or cost baseline to compare against |

## Standard Handoff Checklist

Copy this checklist into the active use-case notes or paste it into the handoff issue/PR description.

```md
## Phase Handoff Checklist
- [ ] Current phase owner updated `reports/Report-Status.md` (including the `## 📜 Action Log`)
- [ ] Required artifacts are committed or linked
- [ ] Build/test/deploy evidence is attached
- [ ] Every decision this handoff depends on is `✅ DECIDED` or `🚫 N/A` in `reports/Decisions-Required.md`
- [ ] Open risks and blockers are listed with owners
- [ ] Next phase owner is named
- [ ] Recommended next command is included
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
**Agent:** <Discovery Engineer | Architect | Coder | Tester | Azure Specialist | DevOps Engineer | Observability Engineer | Security Auditor>
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
- **Recommended command:** `<exact slash command>`

## 📜 Action Log
- <ISO-8601-UTC> | actor=<skill-or-User> | action=<verb-phrase> | files=<+created,~modified,-deleted> | tokens=~<bucket> | turn=<n> | notes="<free text>"
```

### Minimum status update standard
- Keep it short enough to scan in one minute.
- Include links or relative paths to the actual artifacts.
- State the next command explicitly, for example `/phase2-migrate-code` or `/phase3-generate-infra`.
- Record blockers even when they are uncomfortable; hidden blockers cause rework.

## Quality Gates by Phase

### Discovery: Universal Intake
- Source environment, stack, workload, data, and integrations are classified with evidence.
- Every classification carries `evidence_confidence`.
- Any value with no matching adapter triggered `/skill-creator` rather than a guess.
- Mainframe, midrange, or SaaS-embedded findings were routed to the escalation playbook, not force-fitted.

### Phase 0: Portfolio Discovery *(multi-repo only)*
- App list is complete enough to sequence work.
- Shared dependencies and integration points are documented.
- Migration order is agreed.

### Phase 1: Planning & Assessment
- `reports/Decisions-Required.md` exists and lists every decision later phases depend on.
- Hosting platform, IaC tool, database target, and **framework version** are presented as options with tradeoffs — never silently chosen.
- Assessment report exists and is reviewable.
- Risks, blockers, and effort estimate are documented.
- Team agrees to proceed, pause, or reduce scope.

### Phase 2: Code Migration
- Every Phase 2 decision is `✅ DECIDED` or `🚫 N/A` before the first edit.
- Modernized app builds successfully.
- Functional parity assumptions are documented in `reports/Business-Logic-Mapping.md`.
- Config/secrets model is mapped from legacy to modern form.
- Deferred remediation items are listed.

### Phase 3: Infrastructure Generation
- IaC is parameterized and human-readable.
- Identity, secrets, and RBAC approach are documented — managed identity preferred over connection strings.
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

### Phase 6: Post-Migration Operations
- Runbook exists and names an owner per alert.
- Performance and cost baselines are recorded for comparison.
- Observability covers the paths the business actually depends on.

## What Blocks Progress
- Missing or stale `Report-Status.md`
- A required decision still `⏸ PENDING`
- No clear next owner
- No evidence for a claimed build/deploy success
- Security-critical gaps with no remediation plan
- Manual deployment not working but pipeline work starting anyway
- Phase work started from verbal handoff instead of committed artifacts

## The Status Report Template
Start every `reports/Report-Status.md` from `.github/skills/migration-artifacts/references/migration-report-template.md`. It already contains the `## 📜 Action Log` section, and the log format is specified in `.github/skills/migration-artifacts/references/action-log-format.md`.

A strong status file has:
- a short summary at the top
- a completed actions list
- clear key findings
- an explicit next action and next owner

The Action Log is the migration's **trace memory**. It is what lets a new session pick up where a lost one left off — so append an entry after every meaningful action, not just at phase boundaries.

## See also

- [Skills map](./skills-map.md)
- [Skill catalog](../architecture/SKILL-CATALOG.md)
- [Architecture](../architecture/ARCHITECTURE.md)
