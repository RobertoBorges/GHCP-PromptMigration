# Use-Case Routing Overrides

Use this hook to apply workload-specific skill and agent overrides on top of the default phase routing.

## Use-case 01 - Classic ASP (`01-ASPClassicApp`)
- **Critical agents:** Architect, Coder, Azure Specialist, Database Specialist, Security Auditor, Tester
- **Extra skills:** `asp-classic-to-dotnet`, `config-transformation`, `migration-handoff`
- **Extra agents:** Database Specialist (ADODB / stored procedure migration), Security Auditor (legacy auth review)
- **Notes:** Expect COM, IIS assumptions, and classic session-state dependencies.

## Use-case 02 - .NET Framework 3.0 ASP.NET (`02-NetFramework30-ASPNET-WEB`)
- **Critical agents:** Architect, Coder, Azure Specialist, Database Specialist, DevOps Engineer, Tester
- **Extra skills:** `dotnet-framework-to-dotnet8`, `config-transformation`, `azure-app-service`
- **Extra agents:** Azure Specialist, Tester
- **Notes:** Watch for `System.Web`, old package formats, and web.config transforms.

## Use-case 03 - WCF .NET 3.5 (`03-WCFNet35`)
- **Critical agents:** Architect, Coder, Azure Specialist, Database Specialist, Security Auditor, Performance Engineer, Tester
- **Extra skills:** `wcf-to-rest-api`, `dotnet-framework-to-dotnet8`, `azure-entra-id`
- **Extra agents:** Security Auditor (binding security), Database Specialist (service/data contract coupling)
- **Notes:** Flag contract-breaking SOAP -> REST changes clearly.

## Use-case 04 - ContosoUniversityDiPS (`04-ContosoUniversityDiPS`)
- **Critical agents:** Architect, Coder, Azure Specialist, Database Specialist, DevOps Engineer, Observability Engineer, Tester
- **Extra skills:** `dotnet-framework-to-dotnet8`, `ef-migration`, `azure-app-service`
- **Extra agents:** Database Specialist, Tester
- **Notes:** Prioritize MVC-to-ASP.NET Core patterns and EF modernization.

## Use-case 05 - BookShop Web Forms (`05-BookShop`)
- **Critical agents:** Architect, Coder, Azure Specialist, Database Specialist, DevOps Engineer, Cutover Commander, Performance Engineer, Tester
- **Extra skills:** `webforms-to-razor`, `dotnet-framework-to-dotnet8`, `ef-migration`
- **Extra agents:** Tester (UI parity), Database Specialist
- **Notes:** Preserve routes and checkout flows while replacing ViewState/postbacks.

## Use-case 06 - Java API Bus Reservation (`06-Java-API-BusReservation`)
- **Critical agents:** Architect, Coder, Azure Specialist, Database Specialist, DevOps Engineer, Observability Engineer, Performance Engineer, Tester
- **Extra skills:** `java8-to-java21`, `azure-entra-id`, `config-transformation`
- **Extra agents:** Azure Specialist, Performance Engineer
- **Notes:** Watch for Spring Boot 2 -> 3 and `javax` -> `jakarta` breaking changes.

## Use-case 07 - PartsUnlimited ASP.NET 4.5 (`07-PartsUnlimited-aspnet45`)
- **Critical agents:** Architect, Coder, Azure Specialist, DevOps Engineer, Security Auditor, Observability Engineer, Performance Engineer, Tester
- **Extra skills:** `dotnet-framework-to-dotnet8`, `config-transformation`, `azure-app-service`, `azure-entra-id`
- **Extra agents:** Security Auditor, Performance Engineer
- **Notes:** E-commerce flows require auth, session, performance, and deployment-slot discipline.

## Cross-Cutting Support

- **Evaluator:** Required whenever use-case-specific prompt, hook, routing, or orchestration behavior changes.
- **Scribe:** Required for milestone logging, decision capture, and durable handoff context across all seven use-cases.
- **Presentation Specialist:** Optional cross-cutting support for stakeholder communication, readiness reports, executive summaries, deck creation, PPTX generation, slide updates, and visual reporting.

## Override Rules

- Apply these overrides in addition to `phase-gates.md` and `agent-dispatch.md`.
- If multiple use-cases are in scope, union the critical agents, extra skills, and extra agents.
- Record the selected overrides in `reports/Report-Status.md` before phase execution begins.
