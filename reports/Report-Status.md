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
| Phase 3 — Generate Infra | ✅ Complete | `PartsUnlimited-Migrated/infra/` + `azure.yaml` |
| Phase 4 — Deploy to Azure | 🟡 Ready (azd env provisioned, awaiting `azd up`) | `reports/Deployment-Summary-Report.md` |
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

Run `azd up` from `PartsUnlimited-Migrated/` to provision and deploy. After successful deploy, run the SQL `CREATE USER ... FROM EXTERNAL PROVIDER` step from `reports/Deployment-Summary-Report.md` §10, then proceed to `/Phase5-SetupCICD`.

---

## Phase 4 Summary

- **Mode:** User-executed. Per safety policy, the agent did not invoke `azd up` directly (creates billable resources).
- **azd environment:** `partsunlimited-dev` created in `PartsUnlimited-Migrated/.azure/partsunlimited-dev/`.
- **Target region:** `westeurope`.
- **Target subscription:** Azure Migrate Demo Subscription (`6785ea1f-ac40-4244-a9ce-94b12fd832ca`).
- **Pre-set env values:** `AZURE_ENV_NAME`, `AZURE_LOCATION`, `AZURE_SUBSCRIPTION_ID`, `AZURE_PRINCIPAL_ID`, `AZURE_PRINCIPAL_NAME`, `SQL_ADMIN_LOGIN`.
- **Pre-flight:** azd 1.23.13 ✅, az 2.80.0 ✅, signed in as `roborges@microsoft.com` ✅, Phase 2 build ✅, Phase 3 bicep ✅.
- **Deployment runbook:** `reports/Deployment-Summary-Report.md` covers resource inventory, security review, monitoring, post-deploy verification, performance baseline template, cost estimate (~$25-35/month idle), troubleshooting playbook, and the required post-deploy step to grant the Managed Identity database access (`CREATE USER ... FROM EXTERNAL PROVIDER`).
- **Known gap to close after first deploy:** Bicep firewall rule `AllowAllWindowsAzureIps` is broad — migrate to private endpoints + VNet integration before production.

---

## Phase 3 Summary

- **IaC type:** Bicep (compiles clean — `az bicep build` 0 errors).
- **Target topology:** Azure Container Apps + Azure SQL Database (serverless GP_S_Gen5_2) + Azure Container Registry + Azure Key Vault + User-Assigned Managed Identity + Application Insights + Log Analytics.
- **Files generated:**
  - `PartsUnlimited-Migrated/azure.yaml` — azd service map (`web` → Container Apps, builds `./Dockerfile`).
  - `PartsUnlimited-Migrated/infra/main.bicep` — orchestration + outputs consumed by azd.
  - `PartsUnlimited-Migrated/infra/main.parameters.json` — azd-resolved parameters (`AZURE_ENV_NAME`, `AZURE_LOCATION`, `AZURE_PRINCIPAL_ID`).
  - `infra/modules/monitoring.bicep` — Log Analytics + Application Insights + Metrics Publisher RBAC.
  - `infra/modules/identity.bicep` — User-Assigned Managed Identity.
  - `infra/modules/registry.bicep` — ACR (Basic) + AcrPull RBAC for the identity.
  - `infra/modules/keyvault.bicep` — Key Vault (RBAC-only, soft-delete + purge protection) + Secrets User RBAC.
  - `infra/modules/sql.bicep` — Azure SQL Server with Entra ID admin + serverless DB (auto-pause 60 min, 0.5 vCore min).
  - `infra/modules/containerApp.bicep` — Container Apps Environment + Container App (port 8080, http scaling, liveness/readiness probes).
- **Security:**
  - User-Assigned Managed Identity used for ACR pull, Key Vault secret access, and SQL AAD authentication.
  - SQL connection string uses `Authentication=Active Directory Default` (no passwords in env).
  - Key Vault enforces RBAC (no access policies); soft-delete + purge protection on.
  - Container Apps ingress: external HTTPS-only (`allowInsecure: false`), TLS termination at edge.
  - ACR admin user disabled; anonymous pull disabled.
  - SQL minimum TLS 1.2.
- **Scaling:** HTTP-based KEDA scaler (50 concurrent requests/replica), 1–3 replicas; serverless SQL auto-pauses when idle.
- **Cost optimization:** Container Apps consumption plan, ACR Basic, SQL Serverless GP_S_Gen5_2 with 0.5 vCore min + 60 min auto-pause, Log Analytics PerGB2018 30-day retention.
- **Monitoring:** App Insights connection string injected as `ApplicationInsights__ConnectionString` env var; container `stderr/stdout` streamed to Log Analytics via Container Apps log destination; Metrics Publisher role granted to the app identity.
- **Outputs (consumed by azd):** `SERVICE_WEB_NAME`, `SERVICE_WEB_URI`, `AZURE_CONTAINER_REGISTRY_ENDPOINT`, `AZURE_SQL_SERVER_FQDN`, `AZURE_KEY_VAULT_ENDPOINT`, `AZURE_APPLICATION_INSIGHTS_CONNECTION_STRING`, `AZURE_CLIENT_ID`.
- **Validation:** `az bicep build --file main.bicep` succeeds with 0 errors (1 cosmetic length warning on ACR name — `uniqueString` produces 13 chars at runtime).
- **Open items / Phase 4 prerequisites:**
  - Deployer must have permission to assign roles in the resource group (RBAC contributor).
  - `AZURE_PRINCIPAL_ID` (and optionally `AZURE_PRINCIPAL_NAME`) must be set so the SQL Entra ID admin is configured.
  - After first deploy, the `web` service `azd-service-name` tag tells azd which Container App to update with the freshly built image — `containerImage` parameter defaults to a quickstart placeholder for initial provision.
  - Database schema is created on app startup via `db.Database.EnsureCreated()` for the migrated demo; production should switch to EF Core migrations + a deployment job.

---
**Session ended:** 2026-05-25 19:38:07 UTC | Session: unknown


---
**Session ended:** 2026-05-25 21:21:03 UTC | Session: unknown


---
**Session ended:** 2026-05-26 00:27:36 UTC | Session: unknown


---
**Session ended:** 2026-05-26 00:35:44 UTC | Session: unknown

