# Migration Status — PartsUnlimited (ASP.NET 4.5 → .NET 10 on Azure Container Apps)

**Application:** PartsUnlimited
**Source location:** `Use-cases/07-PartsUnlimited-aspnet45`
**Last updated:** 2025

---

## Confirmed Configuration (Phase 1)

| Setting | Value |
|---|---|
| Modernization scope | Version upgrade (.NET Framework 4.5.1 → .NET 10 LTS) + Code remediation for cloud readiness |
| Target hosting platform | **Azure Container Apps** |
| Infrastructure as Code | **Bicep** |
| Database target | SQL Server → **Azure SQL Database** |
| Migration type (per assessment) | **Rewrite** (System.Web stack — not a binary-compatible upgrade) |

---

## Phase Progress

| Phase | Status | Output |
|---|---|---|
| Phase 1 — Plan & Assess | ✅ Complete | `reports/Application-Assessment-Report.md` |
| Phase 2 — Migrate Code | ✅ Complete | `PartsUnlimited-Migrated/` + `reports/Business-Logic-Mapping.md` |
| Phase 3 — Generate Infra | ⏳ Not started | — |
| Phase 4 — Deploy to Azure | ⏳ Not started | — |
| Phase 5 — Setup CI/CD | ⏳ Not started | — |

---

## Phase 2 Summary

- **Build status:** `dotnet build` — **0 errors, 0 warnings** against .NET 10 SDK.
- **Target framework:** `net10.0` (ASP.NET Core MVC + Razor Pages).
- **Project layout:** `PartsUnlimited-Migrated/src/PartsUnlimited.Web/` with `Program.cs` (top-level statements), 15 Models, 6 ViewModels, 2 ProductSearch, 2 Recommendations, 10 Utils, 7 MVC + 2 API controllers, 13 shared partials + 11 view files, full `wwwroot/` (Content, Scripts, Images, fonts copied verbatim).
- **Containerization:** Multi-stage `Dockerfile` (sdk:10.0 → aspnet:10.0), non-root user, port 8080, `HEALTHCHECK`, `.dockerignore`.
- **Key NuGet upgrades:** EF Core 10.0.0 (SqlServer), Identity.EntityFrameworkCore + Identity.UI 10.0.8, ApplicationInsights.AspNetCore 2.23.0, Newtonsoft.Json 13.0.3.
- **Authentication:** ASP.NET Identity v2 + OWIN → ASP.NET Core Identity with default Razor Pages UI. Social logins deferred.
- **Persistence:** EF6 Code First → EF Core 10; added `HasPrecision(18,2)` on all decimal columns (required by SQL Server provider). LocalDB for dev; Azure SQL target per Phase 1.
- **Telemetry:** Web.config AI snippet → `IConfiguration["ApplicationInsights:ConnectionString"]` + server-side `Microsoft.ApplicationInsights.AspNetCore`.
- **Cookies/sessions:** `HttpCookie` → `Response.Cookies.Append` with `IsEssential=true`, `HttpOnly=true`, 30-day expiry on cart cookie.
- **Deferred (documented in Business-Logic-Mapping.md §5, §6.4):** Admin area, AzureML recommendation engine (replaced with `NaiveRecommendationEngine`), SignalR `AnnouncementHub`, social authentication providers.
- **Removed dead code:** `HomeController.Recomendations` 1000-iteration busy loop (no view, no side effects).
- **Bugs fixed:** Null-guarded `postalCode.StartsWith("98")` in `DefaultShippingTaxCalculator.CalculateTax`.
- **Anomalies preserved verbatim (flagged for product owner review):** `StringContainsProductSearch.Depluralize` -s branch drops first char (was throwing in source); inconsistent tax rate (6% vs 5%) between calculator and `RemoveFromCart` summary. See `reports/Business-Logic-Mapping.md` §8.

---

## Next Action

Run `/Phase3-GenerateInfra` to generate Azure infrastructure as code (Bicep) for Azure Container Apps + Azure SQL Database.

---
**Session ended:** 2026-05-25 19:38:07 UTC | Session: unknown


---
**Session ended:** 2026-05-25 21:21:03 UTC | Session: unknown

