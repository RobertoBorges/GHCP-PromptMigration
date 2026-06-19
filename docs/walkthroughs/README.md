# Walkthroughs — CLI-First Migration Guides

One squad. One command surface. Seven legacy modernization paths.
These walkthroughs are written for a CLI-first flow: stay in Copilot CLI, describe the outcome in natural language, and let the squad route the work.

## Why CLI-First

- **One surface:** no chatmode switching required to get started.
- **Natural language:** say what you want to migrate and where it should land.
- **Automatic routing:** the squad pulls in the right specialists behind the scenes.

## Shared Squad Flow

```mermaid
flowchart TD
    A[Pick your legacy app]
    A --> U1[1. The Antique]
    A --> U2[2. The Fossil]
    A --> U3[3. The Wire]
    A --> U4[4. The Campus]
    A --> U5[5. The Bestseller]
    A --> U6[6. The Duke]
    A --> U7[7. The Factory]
    U1 --> B[@squad migrate]
    U2 --> B
    U3 --> B
    U4 --> B
    U5 --> B
    U6 --> B
    U7 --> B
    B --> C{Squad pattern}
    C --> D[Architect]
    C --> E[Coder]
    C --> F[Azure Specialist]
    C --> G[DevOps]
    C --> H[Monitor]
    D --> Z[Running on Azure]
    E --> Z
    F --> Z
    G --> Z
    H --> Z
```

## How to Use These Guides

1. Type `@squad` plus a natural-language migration request.
2. The squad figures out routing, phase order, and which specialists to involve.
3. Add **"fan out"** when you want parallel execution across the squad.
4. Ask follow-up questions anytime — you do not need to restart the flow.
5. Open the matching walkthrough below when you want a concrete example to copy.

## Quick Start — Pick Your Use Case

| # | Walkthrough | Source → Target | Difficulty | One-shot CLI prompt |
|---|---|---|---|---|
| 1 | [The Antique 🏺](01-classic-asp-walkthrough.md) | Classic ASP → .NET 8 + App Service | ⭐⭐⭐⭐⭐ | `@squad migrate this Classic ASP app to .NET 8 on App Service; assess rewrite risk, plan the landing zone, and fan out.` |
| 2 | [The Fossil 🦴](02-dotnet30-webforms-walkthrough.md) | .NET 3.0 WebForms → .NET 8 + App Service | ⭐⭐⭐⭐ | `@squad migrate this .NET 3.0 WebForms app to .NET 8 on App Service; map upgrade blockers and fan out.` |
| 3 | [The Wire 🔌](03-wcf-to-rest-walkthrough.md) | WCF .NET 3.5 → REST + Container Apps | ⭐⭐⭐⭐ | `@squad migrate this WCF .NET 3.5 service to a REST API on Azure Container Apps; convert contracts, plan hosting, and fan out.` |
| 4 | [The Campus 🎓](04-contoso-university-walkthrough.md) | ASP.NET MVC multi-proj → .NET 8 + App Service | ⭐⭐⭐⭐⭐ | `@squad migrate this multi-project ASP.NET MVC solution to .NET 8 on App Service; assess app boundaries, data, and fan out.` |
| 5 | [The Bestseller 📚](05-bookshop-reference-walkthrough.md) | SAP CAP Java → Container Apps + PostgreSQL | ⭐⭐⭐⭐ | `@squad migrate this SAP CAP Java app to Azure Container Apps with PostgreSQL; map services, data, and fan out.` |
| 6 | [The Duke 👑](06-java-api-walkthrough.md) | Java Spring Boot → Container Apps + PostgreSQL | ⭐⭐⭐ | `@squad migrate this Spring Boot API to Azure Container Apps with PostgreSQL; assess dependencies, target architecture, and fan out.` |
| 7 | [The Factory 🏭](07-parts-unlimited-walkthrough.md) | ASP.NET MVC 5 + EF6 → .NET 8 + App Service + SQL | ⭐⭐⭐⭐ | `@squad migrate this ASP.NET MVC 5 + EF6 app to .NET 8 on App Service with SQL; plan code, data, and fan out.` |

## What These Guides Give You

- A realistic one-shot prompt to kick off each migration.
- A repeatable squad pattern across assessment, implementation, deployment, and monitoring.
- A simple way to stay in the CLI while still getting specialist depth when needed.

## Common Prompt Shape

Use the same formula every time: `@squad` + app context + target Azure outcome + any constraint you care about.
If you want speed, add **"fan out"**.
If you want clarity, keep asking follow-up questions in the same thread.
