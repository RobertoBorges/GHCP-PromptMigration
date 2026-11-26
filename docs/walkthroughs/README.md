# Walkthroughs — Reference Migration Guides

One agent. One command surface. Seven reference modernization paths.

These walkthroughs are worked examples. They are **not** the product — the product is a universal migration agent that handles .NET, Java, Python, Node.js, PHP, Ruby, Go, Perl, Rust, Scala/Kotlin, C++ (Windows), Delphi/VB6, PowerBuilder, and Oracle Forms, from on-premise, AWS, GCP, Oracle, VMware, Kubernetes, a container registry, a GitHub repo, or a plain ZIP. The seven apps below are just the ones that ship in this repository so you can follow along.

> Mainframe and midrange workloads (z/OS, IBM i / AS-400, COBOL, RPG, Natural, PL/I, CICS/IMS, VSAM) and SaaS-embedded code (Salesforce Apex, ServiceNow, Power Platform) are **out of scope**. Discovery routes them to a specialist-partner escalation playbook instead of attempting a code-level migration.

## The Main Path

Every walkthrough below is the same seven steps applied to a different app:

`/assess-any-application` → `/phase1-plan` → `/phase2-migrate-code` → `/phase3-generate-infra` → `/phase4-deploy-to-azure` → `/phase5-setup-cicd` → `/phase6-post-migration-ops`

Anything else — `/database-migration`, `/security-hardening`, `/cost-optimization`, `/portfolio-strategy`, `/phase-rollback`, `/get-status` — is an optional add-on you reach for when you need it.

## Why One Surface

- **One surface:** no agent switching required to get started.
- **Natural language:** say what you want to migrate and where it should land.
- **Automatic routing:** the agent reads your Capability Matrix and pulls in the right adapters and specialists behind the scenes.

## Shared Agent Flow

```mermaid
flowchart TD
    A[Pick your legacy app]
    A --> U1[1. Classic ASP]
    A --> U2[2. WebForms]
    A --> U3[3. WCF SOAP]
    A --> U4[4. Contoso University]
    A --> U5[5. SAP CAP Bookshop]
    A --> U6[6. Java Spring Boot]
    A --> U7[7. Parts Unlimited]
    U1 --> B[@agent migrate]
    U2 --> B
    U3 --> B
    U4 --> B
    U5 --> B
    U6 --> B
    U7 --> B
    B --> C{Agent pattern}
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

1. Run `/assess-any-application` first. Everything downstream reads the Capability Matrix it produces.
2. Answer the decisions in `reports/Decisions-Required.md`. Later steps hard-stop until they are `✅ DECIDED`.
3. Work the seven steps in order, or describe the outcome in natural language and let the agent route.
4. Add **"fan out"** when you want parallel execution across specialists.
5. Ask follow-up questions anytime — you do not need to restart the flow.
6. Open the matching walkthrough below when you want a concrete example to copy.

## Quick Start — Pick Your Use Case

> ⚠ The **Target** column shows what each worked example chose, not what the agent will choose for you. Target framework, hosting platform, and database engine are always your decisions, surfaced by `/phase1-plan` with tradeoffs.

| # | Walkthrough | Cheat sheet | Source → Target used in the example | Difficulty |
|---|---|---|---|---|
| 1 | [Classic ASP 🏺](01-classic-asp-walkthrough.md) | [01](../use-case-cheatsheets/01-asp-classic.md) | Classic ASP → .NET + App Service | ⭐⭐⭐⭐⭐ |
| 2 | [WebForms 🦴](02-dotnet30-webforms-walkthrough.md) | [02](../use-case-cheatsheets/02-dotnet30-webforms.md) | .NET 3.0 WebForms → .NET + App Service | ⭐⭐⭐⭐ |
| 3 | [WCF SOAP 🔌](03-wcf-to-rest-walkthrough.md) | [03](../use-case-cheatsheets/03-wcf-net35.md) | WCF .NET 3.5 → REST + Container Apps | ⭐⭐⭐⭐ |
| 4 | [Contoso University 🎓](04-contoso-university-walkthrough.md) | [04](../use-case-cheatsheets/04-contoso-university.md) | ASP.NET MVC multi-project → .NET + App Service | ⭐⭐⭐⭐⭐ |
| 5 | [SAP CAP Bookshop 📚](05-bookshop-reference-walkthrough.md) | [05](../use-case-cheatsheets/05-bookshop-reference.md) | SAP CAP Java → Container Apps + PostgreSQL | ⭐⭐⭐⭐ |
| 6 | [Java Spring Boot 👑](06-java-api-walkthrough.md) | [06](../use-case-cheatsheets/06-java-api.md) | Java Spring Boot → Container Apps + PostgreSQL | ⭐⭐⭐ |
| 7 | [Parts Unlimited 🏭](07-parts-unlimited-walkthrough.md) | [07](../use-case-cheatsheets/07-parts-unlimited.md) | ASP.NET MVC 5 + EF6 → .NET + App Service + SQL | ⭐⭐⭐⭐ |

## What These Guides Give You

- A realistic opening request to kick off each migration.
- A repeatable pattern across discovery, planning, implementation, deployment, CI/CD, and operations.
- A way to stay in one thread while still getting specialist depth when needed.

## Common Request Shape

Use the same formula every time: app context + target Azure outcome + any constraint you care about.
If you want speed, add **"fan out"**.
If you want clarity, keep asking follow-up questions in the same thread.

## See also

- [Skill catalog](../architecture/SKILL-CATALOG.md) — all 65 skills and 10 custom agents
- [Skills map](../guides/skills-map.md) — which skills load at which step
- [Handoff protocol](../guides/handoff-protocol.md) — what each step must produce before the next one starts
- [VS Code quickstart](../vscode-quickstart.md) — install and run in under two minutes
