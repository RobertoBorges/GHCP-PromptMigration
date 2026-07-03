# Phase Gates

Use this hook to enforce quality gates between migration phases. A phase can hand off only when its required artifacts, validation evidence, and approvals are present or an explicit exception is documented in `reports/Report-Status.md`.

## Global Gate Rules

Every phase handoff must include:

- updated `reports/Report-Status.md`
- artifacts required by the current phase
- blockers, assumptions, and open risks
- named next command and recommended lead agent
- rollback impact noted for risky transitions
- named specialist reviews for the agents required by that phase

## Agent Reference

| Agent | Typical gate responsibility |
|-------|-----------------------------|
| Architect | scope, sequencing, and handoff approval |
| Coder | migration implementation readiness |
| Tester | validation evidence and user-facing quality checks |
| Azure Specialist | target platform, hosting, networking, and identity fit |
| DevOps Engineer | deployment and pipeline readiness |
| Observability Engineer | telemetry, alerts, runbooks, and operations readiness |
| Database Specialist | schema, data migration, validation, and cutover readiness |
| Performance Engineer | baseline, load, and scale review |
| Security Auditor | auth, secrets, RBAC, compliance, and exposure review |
| Cost Engineer | cost posture, savings estimates, and budget guardrails review |
| Evaluator | prompt, hook, and orchestration quality review |
| Cutover Commander | rollout, rollback, and production sign-off |
| Scribe | milestone and decision capture |
| Presentation Specialist | stakeholder-ready reporting, executive summaries, and visual deliverables |

## Phase 0 -> Phase 1

**Lead / required specialists:** Architect leads discovery with Azure Specialist and Security Auditor support; Scribe records milestone context when the portfolio assessment is handed off.

Checklist:

- [ ] `codebase-repos.md` processed and repository inventory created
- [ ] per-repo analysis files created in `reports/`
- [ ] `reports/codebase-summary.md` created or updated
- [ ] cross-repo dependencies and communication paths documented
- [ ] candidate migration order proposed
- [ ] lead Architect review completed for scope and sequencing
- [ ] Azure Specialist and Security Auditor findings captured for platform and risk assumptions

## Phase 1 -> Phase 2

**Lead / required specialists:** Architect confirms the plan with Azure Specialist, Security Auditor, and Database Specialist input; Presentation Specialist joins when the assessment must be delivered as a formal report or executive summary.

Checklist:

- [ ] `reports/Application-Assessment-Report.md` completed
- [ ] source runtime/framework and target Azure platform confirmed
- [ ] migration scope agreed (upgrade, remediation, or full modernization)
- [ ] top risks and blockers ranked
- [ ] target hosting, IaC, auth, and database choices recorded
- [ ] `reports/Report-Status.md` updated with next command `/phase2-migratecode`
- [ ] Architect handoff to Coder recorded
- [ ] Azure Specialist, Security Auditor, and Database Specialist assumptions recorded by name

## Phase 2 -> Phase 3

**Lead / required specialists:** Coder owns implementation readiness with Tester review, Database Specialist support for data-impacting changes, Performance Engineer input for scale-sensitive paths, and Security Auditor review when auth or secret handling changes.

Checklist:

- [ ] modernized project folder created
- [ ] code migration report section or equivalent notes updated
- [ ] solution/app builds successfully or blockers are explicitly documented
- [ ] critical auth, config, and data access changes implemented or flagged
- [ ] WCF/WebForms/Java migration exceptions documented
- [ ] Tester review requested for build/test evidence
- [ ] Database Specialist, Performance Engineer, and Security Auditor reviews captured when their areas are touched
- [ ] `reports/Report-Status.md` updated with next command `/phase3-generateinfra`

## Phase 3 -> Phase 4

**Lead / required specialists:** Azure Specialist leads infrastructure generation with DevOps Engineer, Security Auditor, Observability Engineer, Database Specialist, and Cost Engineer engaged when hosting SKUs, scaling guardrails, or cost controls are in scope.

Checklist:

- [ ] `infra/` files generated and structured by module
- [ ] `azure.yaml` created or updated
- [ ] identity, networking, monitoring, and database resources defined
- [ ] validation completed (`build`, `validate`, `what-if`, or equivalent)
- [ ] RBAC and private endpoint decisions documented
- [ ] Azure Specialist and Security Auditor review captured
- [ ] DevOps Engineer, Observability Engineer, Database Specialist, and Cost Engineer review captured when applicable
- [ ] `reports/Report-Status.md` updated with next command `/phase4-deploytoazure`

## Phase 4 -> Phase 5

**Lead / required specialists:** DevOps Engineer owns deployment readiness with Cutover Commander and Tester support; Azure Specialist and Observability Engineer are named when platform remediation or production telemetry validation is needed.

Checklist:

- [ ] deployment summary report created
- [ ] target environment endpoints, URLs, and identities recorded
- [ ] smoke tests and health checks executed
- [ ] monitoring and telemetry confirmed
- [ ] rollback path identified for deployed environment
- [ ] production blockers called out clearly
- [ ] DevOps Engineer, Cutover Commander, and Tester review recorded
- [ ] Azure Specialist and Observability Engineer review recorded when deployment remediation or telemetry validation was required
- [ ] `reports/Report-Status.md` updated with next command `/phase5-setupcicd`

## Phase 5 -> Phase 6

**Lead / required specialists:** DevOps Engineer leads CI/CD readiness with Tester and Security Auditor review; Azure Specialist and Cutover Commander are named when pipeline changes affect platform provisioning, release approvals, or go-live control.

Checklist:

- [ ] CI/CD workflow files created or updated
- [ ] build, test, security scan, and deploy stages defined
- [ ] environment approvals and secrets strategy documented
- [ ] rollback/redeploy steps included in pipeline design
- [ ] pipeline validation or dry-run evidence captured
- [ ] DevOps Engineer and Tester review recorded
- [ ] Security Auditor review recorded for secrets, approvals, and release controls
- [ ] Azure Specialist and Cutover Commander review recorded when platform or go-live controls changed
- [ ] `reports/Report-Status.md` updated with next command `/phase6-postmigrationops`

## Phase 6 -> Closeout

**Lead / required specialists:** Observability Engineer leads post-migration operations with Performance Engineer, Security Auditor, Cost Engineer, Cutover Commander, Scribe, and Presentation Specialist support; Azure Specialist or Architect can be named when stakeholder follow-up depends on platform or portfolio decisions.

Checklist:

- [ ] `reports/Post-Migration-Ops-Report.md` created or updated
- [ ] runbooks and alerting definitions completed
- [ ] health checks, dashboards, and SLO/SLA metrics reviewed
- [ ] security and cost follow-up items prioritized with Cost Engineer input
- [ ] ownership for ongoing operations captured
- [ ] stakeholder-ready reporting, executive summary, or visual deliverable prepared when requested with Presentation Specialist support
- [ ] final `/getstatus` summary ready
- [ ] Scribe milestone entry completed
- [ ] Observability Engineer, Performance Engineer, Security Auditor, Cost Engineer, and Cutover Commander sign-off recorded for operational readiness

## Any Phase -> Rollback

**Lead / required specialists:** Cutover Commander owns rollback planning with DevOps Engineer, Coder, Database Specialist, Security Auditor, and Observability Engineer engaged according to the failure mode.

Trigger rollback planning immediately when any of the following is true:

- [ ] release causes outage or critical health failure
- [ ] security control fails or data integrity is at risk
- [ ] deployment window is exceeded with no safe forward path
- [ ] cost or scale behavior threatens service continuity
- [ ] rollback is lower risk than fix-forward

Required rollback artifacts:

- [ ] `reports/Rollback-Execution-Plan.md`
- [ ] `reports/Rollback-Validation-Report.md`
- [ ] `reports/Rollback-Communications.md`
- [ ] `reports/Post-Mortem-Analysis.md`
- [ ] Cutover Commander, DevOps Engineer, and domain specialist approvals recorded for the selected rollback path

## Gate Outcomes

Use one of these results at every handoff:

- **Pass** - all required artifacts and validation complete
- **Conditional** - handoff allowed with named blockers, owner, and outstanding specialist approvals
- **Blocked** - next phase cannot begin safely
