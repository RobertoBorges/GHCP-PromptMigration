# GitHub Copilot Customization for Azure Migration

This folder contains VS Code GitHub Copilot customization files for the **Code Migration Modernization Agent** - a guided workflow for migrating legacy .NET and Java applications to Azure.

## 📁 Folder Structure

```
.github/
├── agents/                              # Agent definitions
│   └── Code-Migration-Modernization.agent.md
├── prompts/                             # Phase-specific prompts
│   ├── Phase0-Multi-repo-assessment.prompt.md
│   ├── Phase1-PlanAndAssess.prompt.md
│   ├── Phase2-MigrateCode.prompt.md
│   ├── Phase3-GenerateInfra.prompt.md
│   ├── Phase4-DeployToAzure.prompt.md
│   ├── Phase5-SetupCICD.prompt.md
│   └── GetStatus.prompt.md
├── skills/                              # Reusable migration skills
│   ├── dotnet-modernization/           # .NET Framework → .NET 10+ patterns
│   ├── java-modernization/             # Java EE → Spring Boot 3.x patterns
│   ├── azure-infrastructure/           # Bicep/Terraform IaC templates
│   ├── azure-containerization/         # Docker and Container Apps patterns
│   ├── wcf-to-rest-migration/          # WCF → REST API conversion
│   ├── config-transformation/          # web.config → appsettings.json
│   └── migration-unit-testing/         # Unit testing for validation
└── README.md                            # This file
```

## 🚀 Quick Start

### Using the Agent

1. Open VS Code Command Palette (`Ctrl+Shift+P`)
2. Type `@Code Migration Modernization Agent` in Copilot Chat
3. Describe your migration scenario or use a handoff:
   - **Phase 1: Plan & Assess** - Analyze your application
   - **Phase 2: Migrate Code** - Modernize your codebase
   - **Phase 3: Generate Infrastructure** - Create IaC files
   - **Phase 4: Deploy to Azure** - Deploy with `azd`
   - **Phase 5: Setup CI/CD** - Configure pipelines

### Using Prompts Directly

Type `/` in Copilot Chat followed by the prompt name:
- `/phase1-planandassess`
- `/phase2-migratecode`
- `/phase3-generateinfra`
- `/phase4-deploytoazure`
- `/phase5-setupcicd`
- `/getstatus`

## 📚 Skills Reference

Skills are automatically loaded based on context. Each skill provides:
- **SKILL.md** - Patterns, mappings, and best practices
- **templates/** - Ready-to-use code templates

| Skill | Purpose |
|-------|---------|
| `business-logic-mapping` | **NEW** - Track and preserve business logic during migration |
| `dotnet-modernization` | .NET Framework → .NET 10+ LTS upgrade patterns |
| `java-modernization` | Java EE → Spring Boot 3.x with Java 21 |
| `azure-infrastructure` | Bicep/Terraform using Azure Verified Modules |
| `azure-containerization` | Multi-stage Dockerfiles, Container Apps |
| `wcf-to-rest-migration` | WCF service → REST API conversion |
| `config-transformation` | web.config → appsettings.json transformation |
| `migration-unit-testing` | xUnit/JUnit 5 patterns for validation |

## 🎯 Supported Migration Paths

### .NET Migrations
- .NET Framework 3.0-4.8 → .NET 10+ LTS
- ASP.NET Web Forms/MVC → ASP.NET Core MVC/Razor Pages
- WCF Services → ASP.NET Core Web APIs
- Entity Framework 6 → Entity Framework Core

### Java Migrations
- Java EE 6-8 → Spring Boot 3.x with Java 21
- EJB → Spring Beans
- JSP/Servlets → Spring MVC/REST
- JAAS → Spring Security with OAuth2

### Azure Hosting Targets
- Azure App Service (Web Apps)
- Azure Container Apps (Serverless Containers)
- Azure Kubernetes Service (Full Orchestration)

## 📊 Reports

The agent creates and maintains reports in the `reports/` folder:
- `Report-Status.md` - Migration progress tracking
- `Application-Assessment-Report.md` - Comprehensive assessment

## 🔒 Agent Guardrails

- Requires user consent before modifying Azure resources
- Prefers managed identities over connection strings
- Stores secrets in Azure Key Vault
- Uses PowerShell (pwsh) for commands
- Never stores secrets in repository

## 📖 Documentation

- [VS Code Agents Documentation](https://code.visualstudio.com/docs/copilot/copilot-customization)
- [Azure Developer CLI (azd)](https://learn.microsoft.com/azure/developer/azure-developer-cli/)
- [Azure Verified Modules](https://azure.github.io/Azure-Verified-Modules/)
