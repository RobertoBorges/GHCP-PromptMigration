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

| Area | Recommended target |
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

## Prompt sequence

1. `/run quick assessment`
2. `Assess #file:Use-cases/03-WCFNet35 for WCF .NET 3.5 to ASP.NET Core REST migration on Azure Container Apps. Focus on ServiceContract, OperationContract, basicHttpBinding, app.config, and client compatibility.`
3. `/run Phase 1 plan and assess`
4. `Map each operation in WCFDemo.Service to REST endpoints, request/response DTOs, status codes, and breaking changes. Recommend API versioning and authentication approach.`
5. `/run Phase 2 code migration`
6. `/run security hardening review`
7. `/run Phase 3 infrastructure generation`
8. `/run Phase 4 deploy to Azure`
9. `/run Phase 5 CI/CD setup`
10. `/run Phase 6 post-migration ops`
11. `@agent show migration status`

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

- [BookShop reference cheat sheet](05-bookshop-reference.md)
- [BookShop modernization reference](../../Use-cases/05-BookShop/docs/Modernization-Prompts-Reference.md)

## Sample prompts

- `Assess #file:Use-cases/03-WCFNet35 for WCF-to-REST conversion and list contract-breaking changes before Phase 2.`
- `Map every ServiceContract and OperationContract to REST endpoints, DTOs, and status codes.`
- `Design the Azure Container Apps target, including container registry, secrets, health probes, and monitoring.`
- `Create a client migration plan that replaces WCF proxies with HTTP/OpenAPI clients.`
