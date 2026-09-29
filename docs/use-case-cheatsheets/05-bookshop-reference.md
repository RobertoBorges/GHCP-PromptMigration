# 05-BookShop Cheat Sheet — The Bestseller (Reference Implementation)

## What is this app?

BookShop is the repo's completed modernization reference: a formerly legacy web commerce app now expressed as a .NET 8 solution with Azure-ready infrastructure, testing, deployment guidance, and operational runbooks. Ocean's Twelve should treat it as the gold standard for what “good” looks like after migration.

## Source stack

| Area | Legacy origin |
|---|---|
| UI | ASP.NET WebForms / legacy admin UI |
| Framework | .NET Framework 3.5 / 4.x-era patterns |
| Data | SQL Server-style data access |
| Deployment | Manual / IIS-era deployment |
| Notes | Preserved under `Legacy-Archive/` |

## Target stack

> ⚠ The rows below are **candidates, not defaults.** `/phase1-plan` presents each option with tradeoffs and records your answer in `reports/Decisions-Required.md`. The agent never picks a target framework, hosting platform, or database engine on your behalf.

| Area | Implemented reference target |
|---|---|
| Runtime | .NET 8 |
| UI | ASP.NET Core web app |
| Data | Azure SQL + `Microsoft.Data.SqlClient` |
| Hosting | Azure App Service |
| IaC | Bicep + parameter files |
| CI/CD | GitHub Actions |
| Ops | Application Insights, Key Vault, deployment guides, rollback/runbook material |

## Top 5 risks

1. **Reference drift risk** — teams may copy patterns from stale notes instead of the implemented assets.
2. **Overfitting risk** — not every use-case needs every BookShop pattern.
3. **Assumption risk** — teams may assume BookShop's target is Container Apps when the repo implementation shows App Service.
4. **Selective reuse risk** — infra, docs, and reporting patterns can be missed if only code is studied.
5. **False equivalence risk** — WCF and Java migrations need different target patterns than BookShop.

## Key migration patterns to learn from

- How to structure a .NET 8 solution after modernization
- How to preserve legacy code under `Legacy-Archive/`
- How to produce Bicep templates, parameter files, and deployment guides
- How to pair migration work with tests, runbooks, and status artifacts
- How to package a migration so the next team member can operate it

## Command sequence

> Steps marked 🟢 are the 7-step main path. Steps marked 🔵 are optional add-ons. Free-text lines are follow-up requests you type in the same thread.

1. `/get-status`
2. `Use #file:Use-cases/05-BookShop as the reference implementation for .NET 8, ASP.NET Core, Azure App Service, Azure SQL, Bicep, GitHub Actions, Key Vault, and Application Insights. Extract reusable patterns for use-cases 01, 02, and 07.`
3. `/phase6-post-migration-ops`
4. `/security-hardening`
5. `/cost-optimization`
6. `/phase-rollback`
7. `/get-status`

## Agent dispatch order

| Phase | Ocean's Twelve dispatch |
|---|---|
| Reference review | Architect -> Tester -> Scribe -> Azure Specialist |
| Code pattern validation | Coder -> Tester -> Evaluator |
| Infra pattern validation | Azure Specialist -> DevOps Engineer -> Observability Engineer |
| Cutover/runbook review | Cutover Commander -> Security Auditor -> Tester |
| Operations review | Observability Engineer -> Performance Engineer -> Scribe |

## Estimated effort

**0.5-1 day** to extract patterns for planning; **2-3 days** to adapt the reference structure into another migration.

## Reference

- [Full walkthrough for this app](../walkthroughs/05-bookshop-reference-walkthrough.md)
- [Skills map](../guides/skills-map.md) — which skills load at which step
- [BookShop IIS deployment guide](../../Use-cases/05-BookShop/IIS-Deployment-Guide.md)
- [Skill catalog](../architecture/SKILL-CATALOG.md)

## Sample requests

- `Use #file:Use-cases/05-BookShop as the target-state benchmark for a .NET 8 + App Service + Azure SQL migration.`
- `Compare my current use-case against BookShop and list the missing reference patterns in code, infra, CI/CD, and operations.`
- `Extract the reporting, infra, and operational conventions from BookShop that should be standardized across the portfolio.`
- `Show which BookShop patterns should not be copied directly into the WCF and Java use-cases.`
