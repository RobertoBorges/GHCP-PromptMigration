# Onboarding Guide

Use this guide when a new team member joins Robert Borges' migration team.

## 1. Install prerequisites
Install the same baseline tools used by this repo:
- Git
- Visual Studio Code
- GitHub Copilot license and current VS Code extensions
- Azure MCP Server extension
- GitHub Copilot for Azure extension
- Azure CLI (`az`)
- Azure Developer CLI (`azd`)
- Language-specific SDKs needed for the use-case you will touch
  - .NET SDKs / Visual Studio workloads for .NET apps
  - Java 21 + Maven/Gradle for Java apps
  - Docker Desktop if you will build containers or run local deployment flows

## 2. Clone the repo
```bash
git clone https://github.com/v-dguncet_microsoft/GHCP-PromptMigration.git
cd GHCP-PromptMigration
```
Then open the repository in VS Code.

## 3. Understand the squad roles
Read these files first:
- `AGENTS.md`
- `CLAUDE.md`
- `.squad/team.md`
- `.squad/routing.md`
- `.squad/decisions.md`

Then review `docs/onboarding/team-guide.md`, `docs/onboarding/training-program.md`, and `docs/guides/squad-dispatch-cheatsheet.md`.

## 4. Pick your role
Choose the role you are primarily supporting:
- **Migration Lead** → scope, assessment, sequencing
- **App Developer** → code modernization
- **Cloud Engineer** → Azure IaC and deployment
- **DevOps Engineer** → CI/CD and release automation
- **Security Engineer** → security review and sign-off
- **QA Engineer** → validation, status, and readiness

If you are new to the repo, start as **QA Engineer** or **App Developer** on a small use-case.

## 5. Read the relevant prompt files
Use these prompt files as your operating manual:
- `Phase0-Multi-repo-assessment.prompt.md`
- `Phase1-PlanAndAssess.prompt.md`
- `Phase2-MigrateCode.prompt.md`
- `Phase3-GenerateInfra.prompt.md`
- `Phase4-DeployToAzure.prompt.md`
- `Phase5-SetupCICD.prompt.md`
- `GetStatus.prompt.md`

### Quick mapping
- Need to assess? → `/phase1-planandassess`
- Need to modernize code? → `/phase2-migratecode`
- Need Azure IaC? → `/phase3-generateinfra`
- Need deployment validation? → `/phase4-deploytoazure`
- Need automation? → `/phase5-setupcicd`
- Need a checkpoint? → `/getstatus`

## 6. Try a starter migration
Start with **Use-case 02**: `Use-cases/02-NetFramework30-ASPNET-WEB`

Why this starter:
- small scope
- easy to understand legacy WebForms structure
- good practice for the full assessment → migration → infra → deployment chain

### Suggested first exercise
1. Open `Use-cases/02-NetFramework30-ASPNET-WEB`
2. Run a planning session with:
   - `Plan and assess Use-cases/02-NetFramework30-ASPNET-WEB for Azure migration. Target App Service, Bicep, and Azure SQL.`
3. Review the generated reports.
4. Run `/getstatus`.
5. If the assessment looks sound, continue with a limited Phase 2 modernization task.

## 7. Learn the handoff process
Before you work on a later phase, read `docs/guides/handoff-protocol.md`.

Key rule: **do not start from chat memory alone.** Start from:
- `reports/Application-Assessment-Report.md`
- `reports/Report-Status.md`
- committed code or infrastructure artifacts
- explicit blockers and next-owner notes

## 8. Learn squad dispatch patterns
Use `docs/onboarding/team-guide.md` for the full patterns and `docs/guides/squad-dispatch-cheatsheet.md` for fast routing.

Remember the common patterns:
- **Assembly Line** for a small team and one app
- **Parallel Phases** for one large app with multiple workstreams
- **Multi-App Portfolio** for several apps moving together

## First-Day Checklist
- [ ] Repo cloned and opened in VS Code
- [ ] Copilot and Azure extensions installed
- [ ] Squad files read
- [ ] Starter role chosen
- [ ] Prompt files reviewed
- [ ] Use-case 02 assessment completed or observed
- [ ] `docs/guides/handoff-protocol.md` read
- [ ] `docs/guides/squad-dispatch-cheatsheet.md` bookmarked

## What good looks like
By the end of onboarding, a new teammate should be able to:
- explain the 5 migration phases
- route work to the right squad agent
- read and update `reports/Report-Status.md`
- hand off work using artifacts instead of chat summaries
- use BookShop (`Use-cases/05-BookShop`) as the quality benchmark

## Recommended next step after onboarding
Open `docs/onboarding/training-program.md`, then review `Use-cases/05-BookShop` and compare its reports, docs, code, and infra with the smaller starter app. That contrast teaches the full maturity model of this repo very quickly.
