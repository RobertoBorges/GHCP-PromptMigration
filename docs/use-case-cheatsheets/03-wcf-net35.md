# 03-WCFNet35 Cheat Sheet — The Wire

## What is this app?

A WCF demonstration solution centered on service contracts, data contracts, SOAP-style bindings, and a client/host split. It is the cleanest lab for teaching the agent how to move from `.NET 3.5 + WCF + app.config` to ASP.NET Core REST APIs deployed on Azure Container Apps.

## Source stack

| Area | Current state |
|---|---|
| Service model | WCF `ServiceContract` / `OperationContract` |
| Framework | Legacy contract/client on .NET Framework 3.5 |
| Transport | `basicHttpBinding` SOAP over HTTP |
| Config | `app.config` / `system.serviceModel` |
| Client | Console client with generated/proxy-style calls |
| Data | In-memory demo data |

## Target stack

> ⚠ The rows below are **candidates, not defaults.** `/phase1-plan` presents each option with tradeoffs and records your answer in `reports/Decisions-Required.md`. The agent never picks a target framework, hosting platform, or database engine on your behalf.

| Area | Candidate target (your decision) |
|---|---|
| API | ASP.NET Core 8 Web API |
| Hosting | Azure Container Apps |
| Contracts | REST + OpenAPI/Swagger |
| Auth | Entra ID for API access, managed identity for Azure resources |
| Ops | Container registry, Application Insights, Log Analytics |

## Top 5 risks

1. **Contract break risk** — SOAP contracts and REST contracts are not one-to-one.
2. **Client compatibility risk** — WCF client consumers may need new HTTP client logic.
3. **Config-to-code risk** — `system.serviceModel` settings move out of XML and into code/config.
4. **Serialization risk** — Data contract behavior may differ once DTOs are redesigned.
5. **Operational model risk** — self-hosted console patterns do not map to Container Apps directly.

## Key migration patterns

- Convert WCF service contracts to REST endpoints with explicit verbs and status codes
- Replace SOAP envelopes and proxy patterns with DTOs, controllers, and OpenAPI
- Move `app.config` behavior to `appsettings.json`, DI, and ASP.NET Core host setup
- Containerize the API for Azure Container Apps
- Document breaking changes and client replacement strategy before cutover

## Command sequence

> Steps marked 🟢 are the 7-step main path. Steps marked 🔵 are optional add-ons. Free-text lines are follow-up requests you type in the same thread.

1. `/assess-any-application`
2. `Assess #file:Use-cases/03-WCFNet35 for WCF .NET 3.5 to ASP.NET Core REST migration on Azure Container Apps. Focus on ServiceContract, OperationContract, basicHttpBinding, app.config, and client compatibility.`
3. `/phase1-plan`
4. `Map each operation in WCFDemo.Service to REST endpoints, request/response DTOs, status codes, and breaking changes. Recommend API versioning and authentication approach.`
5. `/phase2-migrate-code`
6. `/security-hardening`
7. `/phase3-generate-infra`
8. `/phase4-deploy-to-azure`
9. `/phase5-setup-cicd`
10. `/phase6-post-migration-ops`
11. `/get-status`

## Agent dispatch order

| Phase | Ocean's Twelve dispatch |
|---|---|
| Phase 1 | Architect -> Azure Specialist -> Security Auditor -> Tester |
| Phase 2 | Coder -> Tester -> Security Auditor |
| Phase 3 | Azure Specialist -> DevOps Engineer -> Observability Engineer |
| Phase 4 | Cutover Commander -> Azure Specialist -> Coder |
| Phase 5 | DevOps Engineer -> Tester -> Evaluator |
| Phase 6 | Observability Engineer -> Performance Engineer -> Security Auditor -> Scribe |

## Estimated effort

**2-4 weeks** for contract redesign, API delivery, and Container Apps readiness.

## Reference

- [Full walkthrough for this app](../walkthroughs/03-wcf-to-rest-walkthrough.md)
- [Skill catalog](../architecture/SKILL-CATALOG.md) — all 36 skills and 9 custom agents
- [Skills map](../guides/skills-map.md) — which skills load at which step
- [BookShop reference cheat sheet](05-bookshop-reference.md)
- [BookShop reference walkthrough](../walkthroughs/05-bookshop-reference-walkthrough.md)

## Sample requests

- `Assess #file:Use-cases/03-WCFNet35 for WCF-to-REST conversion and list contract-breaking changes before Phase 2.`
- `Map every ServiceContract and OperationContract to REST endpoints, DTOs, and status codes.`
- `Design the Azure Container Apps target, including container registry, secrets, health probes, and monitoring.`
- `Create a client migration plan that replaces WCF proxies with HTTP/OpenAPI clients.`
