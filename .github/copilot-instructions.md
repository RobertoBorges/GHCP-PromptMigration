# Azure Migration Project Guidelines

These instructions apply to all GitHub Copilot interactions within this repository.

## Project Purpose

This project supports **two complementary Azure migration flows**:

1. **Portfolio Planning Flow** (pre-engagement): Generate executive-ready Migration Strategy Reports from CMDB / RVTools / DMA / mixed customer artifacts. Produces a CIO-level HTML deck with CAF-aligned 6 Rs classification and Factory / ISD-Partner / Unknown execution ownership. Invoke with `/PortfolioStrategy` or use the `migration-strategy-report` skill.

2. **Per-Application Modernization Flow** (Phase 1–5, optionally preceded by Phase 0 multi-repo scan): Guided modernization of ONE legacy .NET or Java app at a time. Focus is on **version upgrades and code modernization** (not lift-and-shift) for Azure hosting compatibility. Invoke with `/Phase0-Multi-repo-assessment` through `/Phase5-SetupCICD`.

The portfolio flow runs before per-app execution — it determines which apps to migrate, in what order, and by whom. The per-app flow then executes against the plan one application at a time.

## Choosing Your Starting Point

```
Do you have a customer portfolio (CMDB / RVTools / DMA / 10+ apps)?
  YES → 📊 Plan a customer portfolio migration  (/PortfolioStrategy)
  NO ↓
Do you have multiple repos that form ONE business solution?
  YES → 🔗 Assess a multi-repo business solution  (/Phase0-Multi-repo-assessment)
  NO ↓
Modernizing ONE application's code?
  YES → 🚀 Modernize a single application  (/Phase1-PlanAndAssess)  ← most common
```

After picking a starting point, subsequent steps (⚙️ Migrate Code → 🏗️ Generate Infrastructure → ☁️ Deploy → 🔄 Set up CI/CD) flow naturally. The Portfolio Planning flow writes `reports/portfolio-handoff.json` so per-app modernization (Phase 1) auto-inherits classification and platform decisions.

## Migration Scope

### What This Project Does ✅
- **Portfolio assessment** of customer estates (apps + databases + infrastructure)
- **Deterministic classification** (6 Rs strategy + Factory/Partner/Unknown ownership) aligned with Cloud Accelerate Factory service descriptions
- Upgrades .NET Framework applications to .NET 10 LTS
- Upgrades Java EE/legacy Java to Spring Boot 3.x with Java 21
- Converts WCF services to REST APIs
- Transforms legacy configuration (web.config → appsettings.json)
- Generates Infrastructure as Code (Bicep/Terraform)
- Sets up CI/CD pipelines for Azure deployment
- Modernizes authentication to Entra ID

### What This Project Does NOT Do ❌
- **Data Migration**: Refer users to Azure Database Migration Service (DMS) or Data Migration Assistant (DMA)
- **Binary/Dependency Scanning**: Refer users to .NET Upgrade Assistant or similar external tools
- **Lift-and-Shift**: This is NOT containerizing legacy code as-is; it requires code upgrades

## Always Apply These Rules

### Security
- Prefer managed identities over connection strings and keys
- Store secrets in Azure Key Vault with RBAC (no access policies)
- Do not query or modify Azure resources without explicit user consent
- Never store secrets in the repository

### Customer Data Isolation (Portfolio Flow ONLY)
When working on a customer portfolio under a `Customers/` folder:
- Read ONLY from the active customer's folder — NEVER cross-reference other customer folders, not even for template/style examples
- The `customer-data-isolation` PreToolUse hook enforces this programmatically when `COPILOT_CUSTOMER_CONTEXT` is set
- Each customer is a fully isolated engagement (treat as separate NDAs)
- If a customer name is ambiguous, ASK before scanning

### Commands and Tools
- Use PowerShell (pwsh) for all shell commands
- Use Azure Developer CLI (azd) for deployments
- Use Azure Verified Modules (AVM) for Bicep templates

### Documentation
- Track migration progress in `reports/Report-Status.md`
- Generate assessment reports in `reports/Application-Assessment-Report.md`
- Use Mermaid diagrams for architecture visualization
- Format reports with clear headings, tables, and checklists

### Code Changes
- Read 2000 lines of code at a time for sufficient context
- Make small, testable, incremental changes
- Validate changes with `get_errors` after each major step
- Do not modify code unless the change can be confidently verified

## Target Platforms

| Platform | Best For |
|----------|----------|
| Azure App Service | Web apps, APIs, quick deployment, PaaS simplicity |
| Azure Container Apps | Microservices, event-driven apps, serverless containers |
| Azure Kubernetes Service (AKS) | Complex orchestration, multi-container workloads |

## Framework Version Targets

| Source | Target |
|--------|--------|
| .NET Framework 2.x | .NET 10 LTS |
| .NET Core 2.1/3.1 | .NET 10 LTS |
| Java 8/11 | Java 21 LTS |
| Java EE 7/8 | Spring Boot 3.x |
| Spring 4.x/5.x | Spring Boot 3.x |
