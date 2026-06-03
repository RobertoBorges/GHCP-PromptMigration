# 06-Java-API-BusReservation Cheat Sheet — The Express

## What is this app?

A Java 8 Spring Boot API for bus reservation workflows, backed by Spring Web, Spring Data JPA, Maven, and an in-memory H2 database. For Ocean's Twelve, it is the best cross-stack lab: the migration is not about .NET, but about moving Java 8-era Spring services into a modern Azure container platform with a production database.

## Source stack

| Area | Current state |
|---|---|
| Runtime | Java 8 |
| Framework | Spring Boot 2.3 |
| API | REST controllers in `RestApi.java` |
| Data | Spring Data JPA + H2 |
| Build | Maven |
| Auth | No mature auth layer visible in sample |

## Target stack

| Area | Recommended target |
|---|---|
| Runtime | Java 21 |
| Framework | Spring Boot 3 |
| Hosting | Azure Container Apps |
| Data | Azure Database for PostgreSQL |
| Security | Key Vault / managed identity pattern for secrets |
| Ops | Application Insights / Azure Monitor, GitHub Actions |

## Top 5 risks

1. **Java 8 -> 21 compatibility risk** — JDK behavior and dependencies change materially.
2. **Spring Boot 2 -> 3 risk** — `javax` namespaces and framework expectations move to `jakarta`.
3. **H2 -> PostgreSQL risk** — in-memory test assumptions differ from production PostgreSQL behavior.
4. **Container readiness risk** — the app needs a clean Docker/runtime story before deployment.
5. **Security baseline risk** — the sample lacks a production-ready auth and secret strategy.

## Key migration patterns

- Upgrade Java and Spring Boot together, not independently
- Replace H2 assumptions with PostgreSQL-compatible schema, queries, and migrations
- Containerize the API and externalize configuration
- Introduce production-grade secret handling and monitoring
- Validate actuator, health probes, and startup behavior for Container Apps

## Prompt sequence

1. `@squad run quick assessment`
2. `Assess #file:Use-cases/06-Java-API-BusReservation for Java 8 + Spring Boot 2.3 modernization to Java 21 + Spring Boot 3 on Azure Container Apps with PostgreSQL. Highlight H2, javax->jakarta, Docker, and Maven risks.`
3. `@squad run Phase 1 plan and assess`
4. `Review pom.xml, application.properties, and RestApi.java. Produce an endpoint inventory, dependency upgrade plan, and target architecture using Container Apps and PostgreSQL.`
5. `@squad run database migration review`
6. `@squad run Phase 2 code migration`
7. `@squad run security hardening review`
8. `@squad run Phase 3 infrastructure generation`
9. `@squad run Phase 4 deploy to Azure`
10. `@squad run Phase 5 CI/CD setup`
11. `@squad run Phase 6 post-migration ops`
12. `@squad show migration status`

## Agent dispatch order

| Phase | Ocean's Twelve dispatch |
|---|---|
| Phase 1 | Architect -> Azure Specialist -> Database Specialist -> Security Auditor |
| Phase 2 | Coder -> Database Specialist -> Tester |
| Phase 3 | Azure Specialist -> DevOps Engineer -> Observability Engineer |
| Phase 4 | Cutover Commander -> Azure Specialist -> Coder |
| Phase 5 | DevOps Engineer -> Tester -> Evaluator |
| Phase 6 | Observability Engineer -> Performance Engineer -> Security Auditor -> Scribe |

## Estimated effort

**2-4 weeks** for runtime modernization, containerization, and PostgreSQL landing.

## Reference

- [BookShop reference cheat sheet](05-bookshop-reference.md)
- [BookShop modernization reference](../../Use-cases/05-BookShop/docs/Modernization-Prompts-Reference.md)

## Sample prompts

- `Assess #file:Use-cases/06-Java-API-BusReservation for Java 21 + Spring Boot 3 migration and rank the biggest blockers.`
- `Create an H2-to-PostgreSQL migration plan for this API and show what breaks first.`
- `Design the Azure Container Apps target, Docker strategy, secrets flow, and monitoring baseline for this Java service.`
- `List every javax->jakarta change likely to affect this codebase before Phase 2 starts.`
