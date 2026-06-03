# Migration Portfolio — Ocean's Twelve — The Azure Heist

> Portfolio view of the seven supported migration targets in this repository.

## Current portfolio status

This repo is currently organized as a **7-target migration library** rather than a live program board with named human owners and delivery dates. Every target has a dedicated `Use-cases\` folder, a walkthrough in `docs\walkthroughs\`, and a cheat sheet in `docs\use-case-cheatsheets\`. `05-BookShop` remains the strongest **reference / benchmark** scenario and should be treated as the closest thing to an end-to-end exemplar.

### Status legend

- **🟢 Guided path ready** — the repo has a use-case folder plus walkthrough and cheat sheet coverage
- **📚 Reference exemplar** — completed or reference-heavy material intended to guide other migrations
- **🧭 Assessment first** — start with `QuickAssessment` or `InteractiveMigrationInterview` before committing to a phase path

## Portfolio summary

| Use-Case | Source → Target | Entry Prompt | Primary Agent Assignments | Current Repo Status | Key Docs |
|----------|------------------|--------------|---------------------------|---------------------|----------|
| `01-ASPClassicApp` | Classic ASP → App Service + Azure SQL | `QuickAssessment` | Architect, Azure Specialist, Coder, Database Specialist, Security Auditor, Tester | 🟢 Guided path ready | `Use-cases\01-ASPClassicApp`, `docs\walkthroughs\01-classic-asp-walkthrough.md`, `docs\use-case-cheatsheets\01-asp-classic.md` |
| `02-NetFramework30-ASPNET-WEB` | .NET Framework 3.0 → App Service + Azure SQL | `QuickAssessment` | Architect, Coder, Azure Specialist, Database Specialist, DevOps Engineer, Tester | 🟢 Guided path ready | `Use-cases\02-NetFramework30-ASPNET-WEB`, `docs\walkthroughs\02-dotnet30-webforms-walkthrough.md`, `docs\use-case-cheatsheets\02-dotnet30-webforms.md` |
| `03-WCFNet35` | WCF .NET 3.5 → Container Apps + REST API | `QuickAssessment` | Architect, Coder, Azure Specialist, Performance Engineer, Security Auditor, Tester | 🟢 Guided path ready | `Use-cases\03-WCFNet35`, `docs\walkthroughs\03-wcf-to-rest-walkthrough.md`, `docs\use-case-cheatsheets\03-wcf-net35.md` |
| `04-ContosoUniversityDiPS` | ASP.NET MVC → App Service + Azure SQL | `QuickAssessment` | Architect, Azure Specialist, Coder, Database Specialist, DevOps Engineer, Observability Engineer, Tester | 🟢 Guided path ready | `Use-cases\04-ContosoUniversityDiPS`, `docs\walkthroughs\04-contoso-university-walkthrough.md`, `docs\use-case-cheatsheets\04-contoso-university.md` |
| `05-BookShop` | .NET 3.5 WebForms → Container Apps + Azure SQL | `InteractiveMigrationInterview` or `GetStatus` | Database Specialist, Coder, Azure Specialist, DevOps Engineer, Cutover Commander, Performance Engineer, Tester | 📚 Reference exemplar | `Use-cases\05-BookShop`, `docs\walkthroughs\05-bookshop-reference-walkthrough.md`, `docs\use-case-cheatsheets\05-bookshop-reference.md` |
| `06-Java-API-BusReservation` | Java 8 API → Container Apps + PostgreSQL | `QuickAssessment` | Azure Specialist, Coder, Database Specialist, DevOps Engineer, Observability Engineer, Performance Engineer, Tester | 🟢 Guided path ready | `Use-cases\06-Java-API-BusReservation`, `docs\walkthroughs\06-java-api-walkthrough.md`, `docs\use-case-cheatsheets\06-java-api.md` |
| `07-PartsUnlimited-aspnet45` | ASP.NET 4.5 → App Service + Azure SQL | `QuickAssessment` | Architect, Coder, Azure Specialist, DevOps Engineer, Security Auditor, Observability Engineer, Tester | 🟢 Guided path ready | `Use-cases\07-PartsUnlimited-aspnet45`, `docs\walkthroughs\07-parts-unlimited-walkthrough.md`, `docs\use-case-cheatsheets\07-parts-unlimited.md` |

## How to use this portfolio

1. Start with `QuickAssessment` for most targets; use `InteractiveMigrationInterview` when the application is unfamiliar or messy.
2. Use `.squad\routing.md` to move from intake into the correct guided phase prompt.
3. Use `GetStatus` whenever blockers, owners, risks, or the next command need to be restated.
4. Treat BookShop as the benchmark/reference stream rather than the generic starting template for new work.

## Portfolio review checklist

- [ ] All 7 targets are still represented in `Use-cases\`
- [ ] Walkthrough and cheat sheet paths still match the current docs tree
- [ ] Agent assignments still match `.squad\routing.md`
- [ ] Entry prompts still reflect the current operator flow
- [ ] Any target-specific milestone or blocker is also reflected in the relevant use-case docs

