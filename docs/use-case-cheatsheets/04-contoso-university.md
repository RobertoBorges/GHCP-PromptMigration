# 04-ContosoUniversityDiPS Cheat Sheet — The Campus

## What is this app?

A multi-project university solution already on ASP.NET Core 2.1, spanning a traditional web app, a REST API, a React SPA, shared libraries, data projects, and multiple test suites. It is the best training case for a complex-but-not-legacy-modernization: lots of moving parts, but no `System.Web` rewrite.

## Source stack

| Area | Current state |
|---|---|
| Web | ASP.NET Core 2.1 MVC / Razor |
| API | ASP.NET Core 2.1 REST API |
| SPA | React SPA project |
| Data | EF Core 2.1 with Sqlite and SqlServer options |
| Auth | Identity 2.0, JWT, OAuth hooks |
| Integrations | SendGrid, Twilio |
| Tests | Unit, integration, and UI test projects |

## Target stack

| Area | Recommended target |
|---|---|
| App runtime | .NET 8 |
| Hosting | Azure App Service |
| Data | Azure SQL |
| Auth | Entra ID + modern ASP.NET Core auth patterns |
| Ops | Application Insights, Key Vault, GitHub Actions |
| SPA strategy | Keep in same solution unless a hard split is justified |

## Top 5 risks

1. **Multi-project coordination risk** — API, Web, SPA, Data, and tests can drift if migrated independently.
2. **Auth sprawl risk** — Identity, JWT, OAuth, and token generation require careful consolidation.
3. **Dependency refresh risk** — ASP.NET Core 2.1-era packages and SPA tooling are outdated.
4. **Secret handling risk** — SendGrid and Twilio placeholders must move to secure secret storage.
5. **Database/provider risk** — Sqlite/SqlServer assumptions may behave differently in Azure SQL.

## Key migration patterns

- Modernize from ASP.NET Core 2.1 to .NET 8 without flattening the solution structure
- Preserve API/Web/SPA/Data/Test boundaries and document dependencies
- Consolidate auth flows and secret handling with Entra ID + Key Vault
- Revalidate EF Core provider behavior against Azure SQL
- Modernize build, test, and SPA packaging before CI/CD hardening

## Prompt sequence

1. `/run quick assessment`
2. `Assess #file:Use-cases/04-ContosoUniversityDiPS as one multi-project solution with API, Web, React SPA, Data, Common, and Tests. Target .NET 8 on Azure App Service with Azure SQL. Do not treat this as a multi-repo assessment.`
3. `/run Phase 1 plan and assess`
4. `Produce a dependency map across the projects. Highlight JWT, Identity, SendGrid, Twilio, EF Core provider choices, SPA build pipeline, and test-suite impact.`
5. `/run database migration review`
6. `/run Phase 2 code migration`
7. `/run security hardening review`
8. `/run Phase 3 infrastructure generation`
9. `/run Phase 4 deploy to Azure`
10. `/run Phase 5 CI/CD setup`
11. `/run Phase 6 post-migration ops`
12. `@agent show migration status`

## Agent dispatch order

| Phase | Ocean's Twelve dispatch |
|---|---|
| Phase 1 | Architect -> Azure Specialist -> Security Auditor -> Database Specialist |
| Phase 2 | Coder -> Tester -> Database Specialist -> Security Auditor |
| Phase 3 | Azure Specialist -> DevOps Engineer -> Observability Engineer |
| Phase 4 | Cutover Commander -> Azure Specialist -> Coder |
| Phase 5 | DevOps Engineer -> Tester -> Evaluator |
| Phase 6 | Observability Engineer -> Performance Engineer -> Security Auditor -> Scribe |

## Estimated effort

**2-3 weeks** for a strong modernization plan; **4-6 weeks** for full delivery if the SPA and test estate are included.

## Reference

- [BookShop reference cheat sheet](05-bookshop-reference.md)
- [BookShop modernization reference](../../Use-cases/05-BookShop/docs/Modernization-Prompts-Reference.md)

## Sample prompts

- `Assess #file:Use-cases/04-ContosoUniversityDiPS as a single multi-project modernization to .NET 8 on Azure App Service.`
- `Map project dependencies across API, Web, SPA, Data, Common, and Tests, and recommend the safest migration order.`
- `Show how JWT, Identity, SendGrid, Twilio, and secrets should be modernized for Azure.`
- `Design the target App Service and Azure SQL deployment topology without splitting the repo unless necessary.`
