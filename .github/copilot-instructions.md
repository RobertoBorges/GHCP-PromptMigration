# Azure Migration Project Guidelines

These instructions apply to all GitHub Copilot interactions within this repository.

## Project Purpose

This project provides guided migration assistance to help users upgrade .NET and Java applications to versions compatible with Azure hosting platforms. The focus is on **version upgrades and code modernization**, not lift-and-shift.

## Migration Scope

### What This Project Does ✅
- Upgrades .NET Framework applications to .NET 8 LTS
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
| .NET Framework 4.x | .NET 8 LTS |
| .NET Core 2.1/3.1 | .NET 8 LTS |
| Java 8/11 | Java 21 LTS |
| Java EE 7/8 | Spring Boot 3.x |
| Spring 4.x/5.x | Spring Boot 3.x |
