# Migration Handoff and Orchestration

Use this skill whenever a prompt transitions work from one phase, prompt, or sub-agent to another.

## Purpose

This skill turns isolated phase prompts into a coordinated workflow by enforcing:

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

## Agent Dispatch Triggers

Trigger specialist agents when any of the following is true:

- infrastructure work begins -> Azure Specialist
- authentication or permissions change -> Security Auditor
- data access or schema migration changes -> Database Specialist
- scaling, latency, or sizing concerns appear -> Performance Engineer
- prompt behavior changes -> Evaluator
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
Run `/phase4-deploytoazure` after Phase 3 gates pass.
```

## Handoff Template

Use this structure at the end of a phase report or prompt response:

```markdown
## Handoff Summary
- **Completed:** [what is done]
- **Artifacts:** [files created or updated]
- **Risks / Blockers:** [open issues]
- **Dispatched Agents:** [who was engaged]
- **Next Command:** [/phaseX-command]
- **Gate Status:** [pass / conditional / blocked]
```

## Output Expectations for Prompts

When this skill is applied, the prompt should:

- refuse to hand off without required artifacts or documented exceptions
- name the next phase command explicitly
- identify which specialist agents must join the next step
- update `reports/Report-Status.md` as the canonical orchestration ledger
