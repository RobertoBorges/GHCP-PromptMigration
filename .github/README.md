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
│   ├── PortfolioStrategy.prompt.md      # Portfolio Planning flow entry point
│   └── GetStatus.prompt.md
├── skills/                              # Reusable migration skills
│   ├── dotnet-modernization/           # .NET Framework → .NET 10+ patterns
│   ├── java-modernization/             # Java EE → Spring Boot 3.x patterns
│   ├── azure-infrastructure/           # Bicep/Terraform IaC templates
│   ├── azure-containerization/         # Docker and Container Apps patterns
│   ├── wcf-to-rest-migration/          # WCF → REST API conversion
│   ├── config-transformation/          # web.config → appsettings.json
│   ├── migration-unit-testing/         # Unit testing for validation
│   └── migration-strategy-report/      # Portfolio strategy HTML deck generator
├── hooks/                               # Agent lifecycle hooks
│   ├── security.json                   # PreToolUse: block secrets & dangerous commands
│   ├── validation.json                 # PostToolUse: auto-validate after edits
│   ├── session-lifecycle.json          # SessionStart + Stop hooks
│   ├── customer-data-isolation.json    # PreToolUse: enforce customer NDA isolation
│   └── scripts/                        # Hook scripts (PowerShell + Bash)
│       ├── block-secrets.ps1/.sh       # Detect hardcoded credentials
│       ├── block-dangerous-commands.ps1/.sh  # Block destructive operations
│       ├── auto-validate.ps1/.sh       # Validation reminders after edits
│       ├── load-migration-state.ps1/.sh     # Inject migration + portfolio context
│       ├── update-status-report.ps1/.sh     # Append session timestamps
│       └── customer-data-isolation.ps1/.sh  # Block cross-customer reads
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
- `/PortfolioStrategy` — Portfolio Planning flow entry point — generates executive Migration Strategy Report from customer portfolio artifacts and writes handoff file for per-app execution
- `/Phase0-Multi-repo-assessment`
- `/Phase1-PlanAndAssess`
- `/Phase2-MigrateCode`
- `/Phase3-GenerateInfra`
- `/Phase4-DeployToAzure`
- `/Phase5-SetupCICD`
- `/GetStatus`

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
| `migration-strategy-report` | **NEW** - Portfolio-level Migration Strategy Report generator (HTML executive deck from CMDB/RVTools/DMA artifacts; CAF-aligned 6 Rs + Factory/Partner/Unknown classification) |

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

## 🪝 Agent Hooks

Hooks enforce guardrails deterministically at the OS level, running shell scripts at key lifecycle points. Located in `.github/hooks/`.

| Hook | Event | What It Does | Context Cost |
|------|-------|-------------|-------------|
| **Block Secrets** | `PreToolUse` | Denies code edits containing hardcoded passwords, API keys, connection strings, or SAS tokens | Zero |
| **Block Dangerous Commands** | `PreToolUse` | Denies destructive terminal commands (`rm -rf /`, `terraform destroy`, `az group delete`, `git push --force`, etc.) | Zero |
| **Customer Data Isolation** | `PreToolUse` | Blocks cross-customer Read/edit access when `COPILOT_CUSTOMER_CONTEXT` is set (enforces NDA isolation for the Migration Strategy Report skill) | Zero |
| **Auto-Validate** | `PostToolUse` | Provides validation reminders after edits to `.bicep`, `.tf`, `.csproj`, or `Dockerfile` files | ~80 chars |
| **Load Migration State** | `SessionStart` | Reads `reports/Report-Status.md` and detects project type (`.csproj`, `pom.xml`, `web.config`, `.svc`) AND any Migration Strategy Report decks to inject concise context | ~200 chars |
| **Update Status Report** | `Stop` | Appends a session-end timestamp to `reports/Report-Status.md` for audit trail | Zero |

**Prerequisites:** Bash scripts require [`jq`](https://jqlang.github.io/jq/) for JSON parsing. PowerShell scripts use built-in `ConvertFrom-Json`.

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
