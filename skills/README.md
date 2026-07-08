# Skills Catalog

This `skills/` folder is the **REFERENCE catalog** for broader knowledge, training, and onboarding. It is **not** the prompt-authoritative skill layer.

## Two Skill Layers

- `.github/skills/` — **authoritative prompt-local skills** referenced directly by prompts via `#file:`
- `skills/` (this folder) — **reference-only catalog** for humans, onboarding, and broader background material

## Authoritative Rules

- Prompts use `.github/skills/` **exclusively**.
- If you add a new skill for prompt composition, put it in `.github/skills/`.
- If you add reference, training, or onboarding material, put it in `skills/`.
- If a root `skills/` document should become prompt-consumable later, **promote/copy it into `.github/skills/` first**, then point the prompt at the `.github/skills/` copy.

## Current Audit

- Prompt audit: **21** prompt files, **94** skill-reference lines, **0** references to root `skills/`
- Root reference catalog: **26** skill files + `README.md` + `INDEX.md`
- Prompt-local catalog: **23** files under `.github/skills/`

### Root skills with `.github/skills/` counterparts (17)

`asp-classic-to-dotnet.md`, `azure-app-service.md`, `azure-container-apps.md`, `azure-entra-id.md`, `bicep-modules.md`, `config-transformation.md`, `docker-containerize.md`, `dotnet-framework-to-dotnet8.md`, `ef-migration.md`, `java8-to-java21.md`, `managed-identity.md`, `migration-report-template.md`, `rbac-least-privilege.md`, `rollback-strategy.md`, `secret-management.md`, `wcf-to-rest-api.md`, `webforms-to-razor.md`

### Root-only reference skills (9)

`azd-configuration.md`, `azure-aks.md`, `azure-devops-pipelines.md`, `azure-key-vault.md`, `azure-monitor-appinsights.md`, `azure-sql-migration.md`, `cost-optimization.md`, `github-actions-cicd.md`, `terraform-azure.md`

### Root files that had identical `.github/skills/` counterparts and are now labeled `REFERENCE ONLY` (4)

`asp-classic-to-dotnet.md`, `azure-container-apps.md`, `docker-containerize.md`, `migration-report-template.md`

## How to use skills in prompts

- Keep the phase prompt focused on workflow and orchestration.
- Reference authoritative prompt skills with `#file:.github/skills/<skill-name>.md`.
- Compose multiple `.github/skills/` files for scenario-specific migrations instead of duplicating instructions.
- Keep skills acyclic; prompts can compose many skills, but skill files should not depend on each other recursively.
- Do **not** point prompts at `skills/` paths.

## Reference Catalog

> **Full content skills** are marked with **★**. This table describes reference material in `skills/`; the phase names are topical guidance, **not** direct prompt references to these root paths.

| Skill | Description | Typical migration phases if promoted to `.github/skills/` |
|---|---|---|
| **★** `skills/dotnet-framework-to-dotnet8.md` | .NET Framework to .NET 8 migration patterns | `QuickAssessment`, `Phase1-Plan`, `Phase2-MigrateCode` |
| **★** `skills/wcf-to-rest-api.md` | WCF contracts and hosting mapped to ASP.NET Core REST APIs | `QuickAssessment`, `Phase1-Plan`, `Phase2-MigrateCode` |
| `skills/webforms-to-razor.md` | Web Forms and ASPX modernization guidance | `QuickAssessment`, `Phase1-Plan`, `Phase2-MigrateCode` |
| **★** `skills/java8-to-java21.md` | Java 8 to Java 21 and Spring Boot 3 modernization | `QuickAssessment`, `Phase1-Plan`, `Phase2-MigrateCode` |
| `skills/asp-classic-to-dotnet.md` | Classic ASP to .NET 8 modernization strategy | `QuickAssessment`, `Phase1-Plan`, `Phase2-MigrateCode` |
| **★** `skills/config-transformation.md` | `web.config` / `app.config` to `appsettings.json` patterns | `Phase1-Plan`, `Phase2-MigrateCode`, `Phase4-DeployToAzure` |
| `skills/ef-migration.md` | ADO.NET or EF6 to EF Core migration patterns | `Phase1-Plan`, `Phase2-MigrateCode`, `DatabaseMigration` |
| **★** `skills/azure-app-service.md` | App Service hosting and deployment patterns | `Phase1-Plan`, `Phase3-GenerateInfra`, `Phase4-DeployToAzure` |
| `skills/azure-container-apps.md` | Container Apps patterns for APIs and background workloads | `Phase1-Plan`, `Phase3-GenerateInfra`, `Phase4-DeployToAzure` |
| `skills/azure-aks.md` | AKS deployment and Helm chart guidance | `Phase1-Plan`, `Phase3-GenerateInfra`, `Phase4-DeployToAzure` |
| `skills/azure-sql-migration.md` | SQL Server to Azure SQL Database migration guidance | `Phase1-Plan`, `Phase3-GenerateInfra`, `DatabaseMigration` |
| **★** `skills/azure-entra-id.md` | Entra ID authentication and authorization setup | `Phase1-Plan`, `Phase2-MigrateCode`, `Phase3-GenerateInfra`, `SecurityHardening` |
| `skills/azure-key-vault.md` | Key Vault integration patterns | `Phase3-GenerateInfra`, `Phase4-DeployToAzure`, `Phase5-SetupCICD`, `SecurityHardening` |
| `skills/azure-monitor-appinsights.md` | Azure Monitor and Application Insights observability | `Phase3-GenerateInfra`, `Phase4-DeployToAzure`, `Phase6-PostMigrationOps` |
| **★** `skills/bicep-modules.md` | Bicep module structure and Azure Verified Modules usage | `Phase3-GenerateInfra`, `Phase4-DeployToAzure` |
| `skills/terraform-azure.md` | Terraform Azure provider and module patterns | `Phase3-GenerateInfra`, `Phase4-DeployToAzure` |
| `skills/azd-configuration.md` | `azure.yaml` and Azure Developer CLI setup guidance | `Phase3-GenerateInfra`, `Phase4-DeployToAzure`, `Phase5-SetupCICD` |
| `skills/github-actions-cicd.md` | GitHub Actions CI/CD workflow patterns | `Phase5-SetupCICD` |
| `skills/azure-devops-pipelines.md` | Azure DevOps pipeline patterns | `Phase5-SetupCICD` |
| `skills/docker-containerize.md` | Dockerfile, image hardening, and runtime patterns | `Phase2-MigrateCode`, `Phase3-GenerateInfra`, `Phase4-DeployToAzure` |
| `skills/managed-identity.md` | Managed identity usage patterns | `Phase3-GenerateInfra`, `Phase4-DeployToAzure`, `SecurityHardening` |
| `skills/rbac-least-privilege.md` | Least-privilege RBAC assignments | `Phase3-GenerateInfra`, `Phase4-DeployToAzure`, `SecurityHardening` |
| `skills/secret-management.md` | Secret handling, Key Vault, and pipeline secret guidance | `Phase2-MigrateCode`, `Phase3-GenerateInfra`, `Phase5-SetupCICD`, `SecurityHardening` |
| **★** `skills/migration-report-template.md` | Standard report format for assessment and migration phases | `Phase0-Multi-repo-assessment`, `Phase1-Plan`, `GetStatus`, `Phase6-PostMigrationOps` |
| `skills/rollback-strategy.md` | Rollback, cutover, and recovery planning patterns | `Phase4-DeployToAzure`, `Phase5-SetupCICD`, `Phase-Rollback` |
| `skills/cost-optimization.md` | Azure cost optimization patterns for target architecture | `CostOptimization`, `Phase3-GenerateInfra`, `Phase4-DeployToAzure`, `Phase6-PostMigrationOps` |

## Prompt reference examples

> Use `#file:.github/skills/...` in prompts. If a skill only exists in this root catalog, promote it into `.github/skills/` before wiring a prompt to it.

### Example 1: Phase1 referencing `.github/skills/migration-report-template.md`

```md
## Shared skills
Use the following reusable skill before generating reports:
- `#file:.github/skills/migration-report-template.md`
```

### Example 2: Phase2 referencing `.github/skills/wcf-to-rest-api.md` and `.github/skills/config-transformation.md`

```md
## Shared skills
Apply these reusable skills when the source application needs them:
- `#file:.github/skills/wcf-to-rest-api.md`
- `#file:.github/skills/config-transformation.md`
```

### Example 3: Phase3 referencing `.github/skills/bicep-modules.md` and `.github/skills/azure-app-service.md`

```md
## Shared skills
Use these reusable skills while generating infrastructure:
- `#file:.github/skills/bicep-modules.md`
- If the assessed hosting target is Azure App Service, also apply `#file:.github/skills/azure-app-service.md`
```

## Skill composition patterns

### Scenario A: .NET WebForms -> App Service

Compose these skills in order:

1. `#file:.github/skills/dotnet-framework-to-dotnet8.md`
2. `#file:.github/skills/config-transformation.md`
3. `#file:.github/skills/ef-migration.md`
4. `#file:.github/skills/azure-app-service.md`
5. `#file:.github/skills/azure-entra-id.md`
6. Promote `skills/azure-key-vault.md` before using it in a prompt
7. Promote `skills/azure-monitor-appinsights.md` before using it in a prompt
8. `#file:.github/skills/bicep-modules.md`
9. Promote `skills/azd-configuration.md` before using it in a prompt
10. Promote `skills/github-actions-cicd.md` before using it in a prompt

Use this composition when modernizing ASP.NET Web Forms or MVC on .NET Framework into an App Service-hosted .NET 8 web app with Bicep-based deployment.

### Scenario B: Java API -> Container Apps

Compose these skills in order:

1. `#file:.github/skills/java8-to-java21.md`
2. `#file:.github/skills/azure-container-apps.md`
3. `#file:.github/skills/azure-entra-id.md`
4. Promote `skills/azure-key-vault.md` before using it in a prompt
5. Promote `skills/azure-monitor-appinsights.md` before using it in a prompt
6. Promote `skills/terraform-azure.md` before using it in a prompt
7. Promote `skills/azd-configuration.md` before using it in a prompt
8. Promote `skills/github-actions-cicd.md` before using it in a prompt
9. `#file:.github/skills/docker-containerize.md`

Use this composition for stateless Java APIs that will be containerized, deployed to Container Apps, and managed through Terraform.

### Scenario C: WCF -> AKS

Compose these skills in order:

1. `#file:.github/skills/wcf-to-rest-api.md`
2. `#file:.github/skills/config-transformation.md`
3. `#file:.github/skills/ef-migration.md`
4. Promote `skills/azure-aks.md` before using it in a prompt
5. `#file:.github/skills/azure-entra-id.md`
6. Promote `skills/azure-key-vault.md` before using it in a prompt
7. Promote `skills/azure-monitor-appinsights.md` before using it in a prompt
8. `#file:.github/skills/bicep-modules.md`
9. Promote `skills/azd-configuration.md` before using it in a prompt
10. Promote `skills/github-actions-cicd.md` before using it in a prompt
11. `#file:.github/skills/docker-containerize.md`

Use this composition when a WCF estate is split into containerized ASP.NET Core services deployed to AKS with Bicep-managed infrastructure.

## Authoring conventions

- Keep each skill narrowly focused and reusable.
- Prefer concrete checklists, mappings, snippets, and validation commands.
- Use conditional language only when a choice genuinely depends on workload characteristics.
- Point prompts to multiple `.github/skills/` files rather than re-describing the same migration pattern.
