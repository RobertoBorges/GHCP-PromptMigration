# Team Guide for Human + Squad Collaboration

This guide shows how Robert Borges' team can split migration work across humans and GHCP squad agents when using the 5-phase migration workflow in this repository.

> **Important:** The current Fast Squad in `.squad/team.md` includes **Architect**, **Coder**, and **Tester**. This guide also references **Azure Specialist** and **Security Auditor** as functional specialist roles. If those agents are not added to the squad yet, use the fallback mapping in each section.

## 1. Team Roles & Assignment Guide

| Role | Owns | Phases | Squad Agent |
|------|------|--------|-------------|
| Migration Lead | Overall strategy, scope, sequencing, approvals | Phase 0-1 | Architect |
| App Developer | Code modernization and app validation | Phase 2 | Coder |
| Cloud Engineer | Azure landing zone, IaC, environment readiness | Phase 3-4 | Azure Specialist |
| DevOps Engineer | CI/CD, release flow, environment promotion | Phase 5 | Coder |
| Security Engineer | Security review, identity, secrets, RBAC | Cross-cutting | Security Auditor |
| QA Engineer | Test strategy, validation evidence, status reporting | Cross-cutting | Tester |

### Migration Lead
- **What they do**
  - Select the migration scope, target Azure platform, IaC preference, and delivery sequence.
  - Run Phase 0 for portfolio-level discovery when multiple repos or apps are involved.
  - Approve the Phase 1 assessment and decide whether the team proceeds, pauses, or narrows scope.
- **What prompts they use**
  - `/phase0-multirepoassessment`
  - `/phase1-planandassess`
  - `/getstatus`
- **Artifacts they produce**
  - `codebase-repos.md` for portfolio assessments
  - `reports/Application-Assessment-Report.md`
  - Initial `reports/Report-Status.md`
  - Scope, risk, and target-state decisions shared with the team
- **How they hand off**
  - Confirm Phase 1 decisions are explicit: hosting target, IaC tool, database strategy, security constraints, blockers, and next owner.
  - Assign the App Developer and Cloud Engineer using the approved report, not a verbal summary.
- **Sample prompts**
  - `Assess this app for Azure migration. Target Azure App Service, Bicep, and Azure SQL. Write the assessment and initialize reports/Report-Status.md.`
  - `Quick scan all repos in codebase-repos.md and recommend migration order, shared dependencies, and cross-app risks.`

### App Developer
- **What they do**
  - Modernize application code in Phase 2 using the approved assessment as the source of truth.
  - Preserve functional behavior, document breaking changes, and keep validation evidence with the migration.
  - Coordinate with QA and Security for risky refactors.
- **What prompts they use**
  - `/phase2-migratecode`
  - `/getstatus`
  - `@terminal` or debug chat mode when the build breaks
- **Artifacts they produce**
  - Modernized application in a new project folder
  - Updated `reports/Report-Status.md`
  - Build/test notes, migration notes, and deferred items
  - Container assets if the assessment requires them
- **How they hand off**
  - Provide a working build, a summary of changed architecture, config changes, and a list of runtime assumptions the Cloud Engineer must honor.
  - Flag anything that still requires manual remediation before deployment.
- **Sample prompts**
  - `Migrate Use-cases/02-NetFramework30-ASPNET-WEB from .NET Framework 3.0 to .NET 8 and preserve current behavior.`
  - `Convert this WCF service to an ASP.NET Core REST API and document breaking changes for the handoff.`

### Cloud Engineer
- **What they do**
  - Translate the migrated app into Azure infrastructure and deployment-ready configuration.
  - Generate `infra/` assets, parameter files, `azure.yaml`, and deployment assumptions.
  - Validate environment prerequisites before Phase 4 deployment.
- **What prompts they use**
  - `/phase3-generateinfra`
  - `/phase4-deploytoazure`
  - `/getstatus`
- **Artifacts they produce**
  - `infra/` directory with Bicep or Terraform
  - `azure.yaml`
  - Deployment scripts or instructions
  - Deployment summary report and endpoint inventory
- **How they hand off**
  - Share validated IaC, environment parameters, secret strategy, RBAC notes, and the exact deployment path that succeeded.
  - Hand production hardening gaps to Security and release automation needs to DevOps.
- **Sample prompts**
  - `Generate Bicep for the migrated app targeting Azure App Service with Azure SQL, Key Vault, and Application Insights.`
  - `Deploy the modernized app to Azure using azd and summarize the resources, endpoints, and validation results.`
- **Fallback if no Azure Specialist agent exists**
  - Use **Coder** plus Azure-focused prompts/skills and keep **Architect** involved for environment decisions.

### DevOps Engineer
- **What they do**
  - Turn the known-good manual deployment into a repeatable CI/CD workflow.
  - Add build, test, infra validation, deployment, smoke test, approval, and rollback stages.
  - Align secrets, branch protection, environments, and promotion flow with the team.
- **What prompts they use**
  - `/phase5-setupcicd`
  - `/getstatus`
- **Artifacts they produce**
  - `.github/workflows/` or `azure-pipelines.yml`
  - `reports/cicd_setup_report.md`
  - Environment/secret checklist and promotion gates
- **How they hand off**
  - Provide pipeline ownership, required secrets, environment names, deployment approvals, and rollback responsibilities.
  - Hand the release verification checklist to QA and Security.
- **Sample prompts**
  - `Set up GitHub Actions CI/CD for this Azure app with build, test, infrastructure validation, staged deployment, and rollback guidance.`
  - `Create CI/CD for App Service deployment with separate dev, test, and prod environments and approval gates.`

### Security Engineer
- **What they do**
  - Review the migration for secrets, identity, auth flows, RBAC, network exposure, and insecure defaults.
  - Stay engaged during all phases instead of waiting until the end.
  - Approve or block production progression when security gates are not met.
- **What prompts they use**
  - Security hardening prompts
  - Security review requests against migrated code, IaC, and pipelines
  - `/getstatus` for open risks
- **Artifacts they produce**
  - Security findings list
  - Required remediations and approval notes
  - Identity/RBAC review summary
- **How they hand off**
  - Update the status report with open risks, accepted risks, and remediation owners.
  - Sign off before Phase 4 production deployment and Phase 5 production automation.
- **Sample prompts**
  - `Review this migration for security issues, hardcoded secrets, weak RBAC, and missing Key Vault or managed identity usage.`
  - `Validate Entra ID, managed identity, and RBAC configuration for this Azure deployment.`
- **Fallback if no Security Auditor agent exists**
  - Use **Tester** for documentation of issues plus a dedicated security review tool/agent or a human security reviewer.

### QA Engineer
- **What they do**
  - Define validation checkpoints across every phase.
  - Confirm status reports, test evidence, smoke tests, and release notes stay accurate.
  - Own the final migration readiness signal for the team.
- **What prompts they use**
  - `/getstatus`
  - Testing and validation prompts
  - Debug prompts when builds or tests fail after migration
- **Artifacts they produce**
  - Test checklist and validation evidence
  - Updated `reports/Report-Status.md`
  - Release-readiness notes and documentation updates
- **How they hand off**
  - Convert raw build/deploy output into a short go/no-go summary with blockers, evidence, and next steps.
  - Confirm the next role has all required artifacts before the handoff is considered complete.
- **Sample prompts**
  - `What's the migration status for this app, what is blocked, and what is the next recommended step?`
  - `Generate a test and validation checklist for the migrated app before Azure deployment.`

## 2. Parallel Work Patterns

### Pattern A: Assembly Line
```text
Day 1: Lead → Phase 1 assessment
Day 2: Developer → Phase 2 migration
Day 3: Cloud Eng → Phase 3 infra
Day 4: Cloud Eng → Phase 4 deploy
Day 5: DevOps → Phase 5 CI/CD
```
- **When to use it**
  - Small team, one use-case, low ambiguity, tight timeline.
  - Best for starter migrations and disciplined phase-by-phase execution.
- **Team size needed**
  - 2-4 people.
- **Communication points**
  - Daily check-in at the phase boundary.
  - `/getstatus` update at the end of each day.
  - Go/no-go review before Phase 3 and before Phase 5.
- **Handoff artifacts**
  - Phase 1: assessment report + status file
  - Phase 2: migrated code + build evidence
  - Phase 3: IaC + `azure.yaml` + environment assumptions
  - Phase 4: deployment summary + endpoints + smoke test results
- **Squad dispatch sequence**
  1. Architect for Phase 1.
  2. Coder for Phase 2.
  3. Azure Specialist for Phase 3-4.
  4. Coder for Phase 5 pipeline automation.
  5. Tester after every phase to update status and readiness.

### Pattern B: Parallel Phases
```text
Lead: Phase 1
├── Developer A: Migrate frontend (Phase 2a)
├── Developer B: Migrate backend (Phase 2b)
├── Cloud Eng: Prepare infra (Phase 3) ← starts after Phase 1
└── Security: Review throughout
```
- **When to use it**
  - One large app with clear seams between UI, APIs, services, or data layers.
  - Best when Phase 1 has already identified the target architecture and integration boundaries.
- **Team size needed**
  - 4-7 people.
- **Communication points**
  - Phase 1 architecture review to split work.
  - Integration sync between developers and Cloud Engineer at least twice per week.
  - Security review checkpoint during design, pre-deploy, and pre-CI/CD.
- **Handoff artifacts**
  - Shared Phase 1 assessment with workstream splits
  - Component-level migration notes for frontend and backend
  - Shared configuration contract: APIs, secrets, environment variables, ports, identity model
  - Consolidated integration checklist before Phase 4
- **Squad dispatch sequence**
  1. Architect runs Phase 1 and defines component boundaries.
  2. Coder agents execute frontend/backend migration work in parallel.
  3. Azure Specialist starts Phase 3 as soon as target-state decisions are stable.
  4. Security Auditor reviews code and IaC continuously.
  5. Tester consolidates status, integration evidence, and release readiness.

### Pattern C: Multi-App Portfolio
```text
Lead: Phase 0 multi-repo assessment
├── Team A: Use-case 02 (all phases)
├── Team B: Use-case 03 (all phases)
├── Team C: Use-case 06 (all phases)
└── Lead: Consolidate, cross-app decisions
```
- **When to use it**
  - Portfolio modernization across several apps or repos.
  - Best when teams need a common target platform, security baseline, or release calendar.
- **Team size needed**
  - 5-12 people across multiple streams.
- **Communication points**
  - Phase 0 portfolio review to decide migration order.
  - Weekly architecture and dependency review across app teams.
  - Shared security and platform standards review.
  - Portfolio dashboard refresh using `PORTFOLIO.md`.
- **Handoff artifacts**
  - `codebase-repos.md`
  - Portfolio assessment summary
  - Per-app `reports/Report-Status.md`
  - Shared decisions for platform, networking, identity, and release approach
- **Squad dispatch sequence**
  1. Architect runs `/phase0-multirepoassessment` and sets the app order.
  2. Each app team follows the standard Phase 1-5 sequence with its own status report.
  3. Tester/DevRel consolidates portfolio status into `PORTFOLIO.md`.
  4. Architect resolves cross-app trade-offs and publishes shared standards.

## 3. Sample End-to-End Session: Use-case 02 (.NET Framework 3.0)

This walkthrough shows one practical team session for `Use-cases/02-NetFramework30-ASPNET-WEB`.

### Step 1: Migration Lead kicks off assessment
- **Human prompt**
  - `Plan and assess Use-cases/02-NetFramework30-ASPNET-WEB for Azure migration. Target Azure App Service, Bicep, and Azure SQL. Initialize the reports folder and write the assessment.`
- **Squad agent**
  - Architect
- **Expected outputs**
  - `reports/Application-Assessment-Report.md`
  - `reports/Report-Status.md`
  - Clear recommendation for Phase 2 and Phase 3 owners
- **Handoff point**
  - Lead shares the report plus a one-line decision: `Proceed with Phase 2 using .NET 8 and App Service.`

### Step 2: App Developer modernizes the application
- **Human prompt**
  - `Migrate Use-cases/02-NetFramework30-ASPNET-WEB from .NET Framework 3.0 to .NET 8. Preserve current pages and behavior, create the modernized app in a new folder, and update Report-Status.md.`
- **Squad agent**
  - Coder
- **Expected outputs**
  - New modernized project folder
  - Buildable .NET 8 app
  - Migration notes and updated status report
- **Parallel work**
  - QA drafts validation checklist.
  - Security reviews auth/config assumptions.
- **Handoff point**
  - Developer delivers build evidence, changed config model, and runtime assumptions.

### Step 3: Cloud Engineer prepares infrastructure
- **Human prompt**
  - `Generate Bicep infrastructure for the migrated Use-case 02 app targeting Azure App Service with Application Insights, Key Vault, and Azure SQL. Create azure.yaml and environment parameters.`
- **Squad agent**
  - Azure Specialist
- **Expected outputs**
  - `infra/`
  - `azure.yaml`
  - Parameter files and deployment notes
- **Handoff point**
  - Cloud Engineer shares deploy prerequisites, secret model, and environment names.

### Step 4: Cloud Engineer performs initial deployment
- **Human prompt**
  - `Deploy the migrated Use-case 02 app to Azure using azd and summarize resources, endpoints, validation results, and any remaining issues in the reports folder.`
- **Squad agent**
  - Azure Specialist
- **Expected outputs**
  - Deployment summary report
  - Azure resource inventory
  - App endpoint and smoke test results
- **Handoff point**
  - QA verifies smoke tests. Security verifies identity, secrets, and RBAC.

### Step 5: DevOps Engineer automates the path
- **Human prompt**
  - `Set up GitHub Actions CI/CD for the migrated Use-case 02 app with build, test, infrastructure validation, staged Azure deployment, and rollback guidance.`
- **Squad agent**
  - Coder
- **Expected outputs**
  - `.github/workflows/...`
  - `reports/cicd_setup_report.md`
  - Required secrets and approvals checklist
- **Handoff point**
  - QA runs the release-readiness checklist and closes the migration when pipeline output matches the known-good manual deployment.

### Final artifact set for Use-case 02
- `reports/Application-Assessment-Report.md`
- `reports/Report-Status.md`
- Modernized .NET 8 project folder
- `infra/` + `azure.yaml`
- Deployment summary report
- CI/CD workflow files
- QA validation checklist and security sign-off notes

## Recommended Team Cadence
- Update `reports/Report-Status.md` after every phase.
- Use `PORTFOLIO.md` for cross-app visibility.
- Make handoffs artifact-based, not chat-based.
- Treat BookShop (`Use-cases/05-BookShop`) as the reference implementation for what “good” looks like: rich status reporting, prompt references, code, infra, and deployment guidance.
