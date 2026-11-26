# Migration Handoff and Orchestration

Use this skill whenever the agent transitions work from one phase, skill, or sub-agent to another.

## Purpose

This skill turns isolated phase skills into a coordinated workflow by enforcing:

- explicit phase entry and exit criteria
- required artifacts before handoff
- automatic agent dispatch expectations
- status report updates at every milestone

## Phase Transition Checklist

Before moving to the next phase, verify:

1. the current phase deliverables exist
2. blockers and risks are recorded in `reports/Report-Status.md`
3. the next command is explicit
4. required reviewers or specialist agents have been engaged
5. rollback and recovery impact is understood for risky transitions

## Required Artifacts by Phase

| Phase | Required Artifacts |
|---|---|
| Phase 0 | `reports/codebase-summary.md`, per-repo reports, repo inventory |
| Phase 1 | `reports/Application-Assessment-Report.md`, updated `reports/Report-Status.md` |
| Phase 2 | migration report section, modernized project folder, build/test evidence |
| Phase 3 | `infra/` files, `azure.yaml`, validation output, identity/network notes |
| Phase 4 | deployment summary, environment endpoints, smoke-test evidence |
| Phase 5 | pipeline files, CI/CD report, approval and rollback steps |
| Phase 6 | ops report, runbooks, alerting/dashboard definitions |
| Rollback | rollback execution plan, validation report, communications, post-mortem |

## Quality Gate Definitions

A phase is ready to hand off only when:

- **Completeness**: required artifacts exist and are populated
- **Validation**: builds/tests/infra validation for that phase were executed or documented
- **Risk visibility**: open blockers and assumptions are recorded
- **Ownership**: lead and specialist agents for the next phase are identified
- **Next action clarity**: the next slash command is specified

### Per-phase exit gates

A phase only advances when its gate is true and the artifacts above are updated. `reports/Migration-Plan.md` cites these as the standard gates and adds app-specific gates on top.

| Phase | Gate (all must be true) |
|---|---|
| Phase 0 — Multi-Repo Assessment | Repository inventory complete; candidate apps prioritized; shared dependencies documented; each repo has a recommended migration path and next-step owner. |
| Phase 1 — Plan | Capability Matrix loaded; target Azure platform chosen; assessment report updated; risks recorded; success criteria explicit. |
| Phase 2 — Migrate Code | Core paths compile and validate for every stack in the matrix; breaking changes addressed or logged; config and auth changes documented; regression checks pass; database-impacting changes handed to the Database Specialist. |
| Database migration | Target engine decided; schema converted and validated; data copy and sync method tested; row-count and checksum validation planned; rollback path for data defined. |
| Phase 3 — Generate Infra | IaC generated and reviewed; parameters and secrets externalized; network, identity and hosting explicit; security baseline present; deployment instructions runnable. |
| Security hardening | Managed identities in place of keys; secrets in Key Vault with RBAC; network exposure reviewed; findings fixed or accepted with an owner. |
| Phase 4 — Deploy to Azure | Deployment succeeds in the target environment; smoke tests pass; app config verified in Azure; rollback path ready; status reflects deployed state. |
| Phase 5 — Setup CI/CD | Pipeline runs end to end; promotion gates defined; secrets handled securely; deployment repeatable; failure handling configured. |
| Phase 6 — Post-Migration Ops | Dashboards, alerts and runbooks exist; health signals connected; performance baseline captured; cost guardrails defined; operational ownership clear. |
| Rollback | Trigger conditions defined; rollback steps rehearsable; data integrity checks specified; communications plan exists; post-rollback validation documented. |

## Strategy → Phase Emphasis

Use `migration_strategy.recommendation` from the Capability Matrix to decide which phases get the most attention. For effort, prefer `complexity.effort_breakdown` (see [complexity-model.md](./complexity-model.md)); use this table only to shape scope or when the breakdown is missing.

| Strategy | Phases emphasized | Phases lightened |
|---|---|---|
| `rehost` | Phase 3 (infra), Phase 4 (deploy) | Phase 2 is mostly packaging |
| `replatform` | Phase 2 (config and runtime), Phase 3, Phase 4 | — |
| `refactor` | Phase 2 (heavy code work) | — |
| `rearchitect` | Phase 1 (redesign), Phase 2, Phase 3 (new IaC) | — |
| `rebuild` | All phases; treat as greenfield | Phase 0 usually skipped |
| `retain` | Phase 3 (integration only) | Phase 2, Phase 4 |
| `retire` | None; decommission plan only | All |

Workload-specific emphasis lives in each `workload-adapters/references/workload-*.md` file under "Phase Emphasis".

## Agent Dispatch Triggers

Trigger specialist agents when any of the following is true:

- infrastructure work begins -> Azure Specialist
- authentication or permissions change -> Security Auditor
- data access or schema migration changes -> Database Specialist
- scaling, latency, or sizing concerns appear -> Performance Engineer
- skill or agent behavior changes -> Evaluator
- a meaningful milestone is reached -> Scribe
- validation is required -> Tester

## Status Report Update Protocol

Always update `reports/Report-Status.md` with:

- current phase and timestamp
- completed artifacts
- validation status
- blockers, risks, and owner
- next recommended command
- dispatched agents and pending follow-up

### Example status snippet

```markdown
## Current Phase
- **In Progress:** Phase 3 - Generate Infrastructure
- **Last Updated:** 2026-05-28 16:20 UTC
- **Lead Agent:** Azure Specialist
- **Parallel Agents:** Security Auditor, Database Specialist

## Exit Criteria
- [x] Hosting target confirmed
- [x] Bicep modules generated
- [ ] Private endpoint validation completed

## Next Step
Run `/phase4-deploy-to-azure` after Phase 3 gates pass.
```

## Handoff Template

Use this structure at the end of a phase report or agent response:

```markdown
## Handoff Summary
- **Completed:** [what is done]
- **Artifacts:** [files created or updated]
- **Risks / Blockers:** [open issues]
- **Dispatched Agents:** [who was engaged]
- **Next Command:** [/phaseX-command]
- **Gate Status:** [pass / conditional / blocked]
```

## Output Expectations

When this skill is applied, the agent should:

- refuse to hand off without required artifacts or documented exceptions
- name the next phase command explicitly
- identify which specialist agents must join the next step
- update `reports/Report-Status.md` as the canonical orchestration ledger
