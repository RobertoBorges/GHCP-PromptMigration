---
name: migration-artifacts
description: |
  Router for canonical migration output artifacts and handoffs. Use when creating, updating, validating, or consuming reports/Discovery-Dossier.md, reports/Capability-Matrix.yaml, reports/Migration-Plan.md, reports/Application-Assessment-Report.md, reports/Report-Status.md, decisions logs, phase handoffs, or migration strategy reports. Emphasizes append-only traceability: every meaningful action must append an Action Log entry to reports/Report-Status.md so a future session can recover context.
user-invocable: false
---

# Migration Artifacts

## When to use

Use this router when a migration skill produces, updates, validates, or hands off named artifacts. It covers the documents and machine-readable files that connect the universal Assess + Phase 1-6 flow across stacks and source environments.

Project boundary: artifacts must stay stack-agnostic across supported application families. For mainframe/midrange evidence such as z/OS, IBM i, COBOL, RPG, Natural, PL/I, CICS, IMS, or VSAM, document unsupported-source escalation rather than implying code-level migration.

Canonical files covered here:

- `reports/Discovery-Dossier.md`
- `reports/Capability-Matrix.yaml`
- `reports/Migration-Plan.md`
- `reports/Application-Assessment-Report.md`
- `reports/Report-Status.md`
- supporting logs, reports, and handoff sections used by phases

The Action Log in `reports/Report-Status.md` is the migration's trace memory. Append an entry after every meaningful action: phase start/complete/block, artifact creation/update, user decision, gate event, Azure change, rollback, or other recoverable milestone.

## Signal to reference selection

| Signal in the task or evidence | Load this reference | Use it for |
|---|---|---|
| Appending to `reports/Report-Status.md`, recording phase events, artifacts, gates, user decisions, Azure changes, rollback, recovery history, or session trace | [Action Log format](./references/action-log-format.md) | Canonical single-line Action Log entry format, vocabulary, required fields, turn/tokens guidance, and recovery semantics. |
| Creating, validating, or consuming `reports/Capability-Matrix.yaml`; routing stack/source/workload/data/integration skills; carrying evidence confidence | [Capability Matrix](./references/capability-matrix.md) | Machine-readable discovery contract, schema, field conventions, consumer contract, update discipline, and quality gate. |
| Creating or validating `reports/Discovery-Dossier.md`; writing human-readable discovery findings, evidence, risks, strategy, candidates, and unresolved questions | [Discovery Dossier template](./references/discovery-dossier-template.md) | Fourteen-section discovery narrative paired with the Capability Matrix and evidence-confidence requirements. |
| Creating or updating `reports/Migration-Plan.md`; finalizing execution sequencing, target architecture, per-phase work, gates, rollback shape, and assumptions | [Migration Plan template](./references/migration-plan-template.md) | Architect-led plan structure for one application and the dispatch contract consumed by phases. |
| Creating or updating `reports/Report-Status.md`, `reports/Application-Assessment-Report.md`, or phase-specific Markdown reports | [Migration Report template](./references/migration-report-template.md) | Standard report set, assessment report layout, status report skeleton, report writing checklist, and next-step conventions. |
| Transitioning between skills, phases, or agents; validating phase deliverables; writing handoff summaries; identifying next command or specialist follow-up | [Migration Handoff and Orchestration](./references/migration-handoff.md) | Phase transition checklist, required artifacts by phase, quality gates, dispatch triggers, status update protocol, and handoff template. |

## How to use

1. Identify which artifact the phase must create, update, or consume.
2. Load the matching reference and preserve its required structure instead of inventing a new report shape.
3. Keep factual findings, assumptions, decisions, risks, and recommendations clearly separated.
4. Use the Capability Matrix as the machine-readable contract and the Discovery Dossier as its human-readable companion.
5. Keep `reports/Report-Status.md` current and append Action Log entries after every meaningful action; do not overwrite trace history.
6. At handoff, name completed artifacts, validation evidence, risks/blockers, dispatched specialists, gate status, and the next command.
