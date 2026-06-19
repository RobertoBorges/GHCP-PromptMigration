# Agent Dispatch Rules

Use this hook to decide which squad agents should be engaged automatically for each slash command or migration condition.

## Core Dispatch Rules

- One lead agent owns the prompt response.
- Parallel agents provide specialist review or supporting artifacts.
- Tester validates implementation-facing changes.
- Evaluator reviews prompt or orchestration changes.
- Scribe updates `JOURNAL.md` after meaningful milestones.
- Presentation Specialist supports deliverables, reports, executive summaries, decks, PPTX, slide updates, and visual reporting when stakeholder-ready output is requested.

## Slash Command Routing

### Trigger: `/phase0-multirepoassessment`
- **Lead:** Architect
- **Parallel:** Azure Specialist, Security Auditor
- **Post:** Scribe

### Trigger: `/phase1-planandassess`
- **Lead:** Architect
- **Parallel:** Azure Specialist, Security Auditor, Database Specialist
- **Conditional:** Presentation Specialist when the assessment must be packaged as a report, executive summary, or stakeholder-ready deliverable
- **Post:** Scribe

### Trigger: `/phase2-migratecode`
- **Lead:** Coder
- **Parallel:** Database Specialist, Performance Engineer
- **Conditional:** Security Auditor when auth, secrets, or permissions change
- **Conditional:** Presentation Specialist when code migration output must be turned into an executive summary, workshop readout, or visual deliverable
- **Post:** Tester, Scribe

### Trigger: `/phase3-generateinfra`
- **Lead:** Azure Specialist
- **Parallel:** DevOps Engineer, Security Auditor
- **Conditional:** Database Specialist or Observability Engineer when data topology or monitoring design is in scope
- **Conditional:** Presentation Specialist when architecture diagrams, infrastructure reports, or stakeholder-ready visuals are requested
- **Post:** Tester, Scribe

### Trigger: `/phase4-deploytoazure`
- **Lead:** DevOps Engineer
- **Parallel:** Cutover Commander, Tester
- **Conditional:** Azure Specialist when platform remediation is needed during deployment
- **Conditional:** Presentation Specialist when deployment outcomes must be summarized for stakeholders or captured in visual reporting
- **Post:** Scribe

### Trigger: `/phase5-setupcicd`
- **Lead:** DevOps Engineer
- **Parallel:** Tester, Security Auditor
- **Conditional:** Azure Specialist when pipeline work changes platform provisioning or identity flow
- **Conditional:** Presentation Specialist when pipeline readiness or release governance must be delivered as a report or executive summary
- **Post:** Scribe

### Trigger: `/phase6-postmigrationops`
- **Lead:** Observability Engineer
- **Parallel:** Performance Engineer, Presentation Specialist
- **Conditional:** Security Auditor or Cutover Commander when operational findings affect production sign-off
- **Post:** Scribe

### Trigger: `/quickassessment`
- **Lead:** Architect
- **Parallel:** Azure Specialist
- **Conditional:** Database Specialist for heavy data workloads
- **Conditional:** Presentation Specialist when the output is requested as a stakeholder brief, report, or executive summary
- **Post:** Scribe

### Trigger: `/databasemigration`
- **Lead:** Database Specialist
- **Parallel:** Coder, Security Auditor
- **Conditional:** Presentation Specialist when migration findings or cutover readiness must be communicated visually
- **Post:** Tester, Scribe

### Trigger: `/securityhardening`
- **Lead:** Security Auditor
- **Parallel:** Azure Specialist, Observability Engineer
- **Conditional:** Presentation Specialist when hardening findings, compliance updates, or executive risk summaries are requested
- **Post:** Scribe

### Trigger: `/costoptimization`
- **Lead:** Cost Engineer
- **Parallel:** Azure Specialist, Architect
- **Conditional:** DevOps Engineer when autoscale policies, schedules, or budget guardrails require automation changes
- **Conditional:** Observability Engineer when recommendations depend on telemetry gaps or alert coverage
- **Conditional:** Presentation Specialist when cost findings are delivered as a report, executive summary, or visual narrative
- **Post:** Scribe

### Trigger: `/phase-rollback`
- **Lead:** Cutover Commander
- **Parallel:** Coder, Database Specialist
- **Conditional:** Security Auditor or Observability Engineer when the incident includes security or production-health uncertainty
- **Conditional:** Presentation Specialist when rollback status, stakeholder communications, or incident reporting require slides or visual summaries
- **Post:** Scribe

### Trigger: `/getstatus`
- **Lead:** Tester
- **Parallel:** none by default
- **Conditional:** Architect when the status report implies reprioritization, resequencing, or portfolio-level scope changes
- **Conditional:** Scribe when the status report is stale or inconsistent
- **Conditional:** Presentation Specialist when status must be delivered as an executive summary, report, deck, or visual readout

## Conditional Dispatch Rules

Dispatch additional agents when these conditions are detected:

- **WCF/SOAP found** -> Coder + Security Auditor
- **Web Forms found** -> Coder + Tester
- **EF6 or complex SQL migration** -> Database Specialist
- **Entra ID / auth redesign** -> Security Auditor
- **App Service, networking, or RBAC work** -> Azure Specialist
- **Cost, budget, spending, expensive, right-size, reserved instance, or savings concerns** -> Cost Engineer
- **Performance regression or scale concerns** -> Performance Engineer
- **Monitoring gaps or prod readiness review** -> Observability Engineer
- **Prompt, chatmode, or hook changes** -> Evaluator
- **Meaningful milestone reached** -> Scribe
- **Deck creation, PPTX generation, slide updates, visual reporting, presentation request, deliverable packaging, report generation, or executive summary request appears** -> Presentation Specialist

## Dispatch Recording

Whenever agents are dispatched, update `reports/Report-Status.md` with:

- lead agent
- parallel agents
- why they were engaged
- outstanding reviews or approvals
