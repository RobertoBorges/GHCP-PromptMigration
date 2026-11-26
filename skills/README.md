# Skills Catalog

This `skills/` folder is the **REFERENCE catalog** for broader knowledge, training, and onboarding. It is **not** the prompt-authoritative skill layer.

## Two Content Layers

- `.github/skills/<name>/SKILL.md` — **discoverable Agent Skills** with YAML `name` and `description` metadata. Copilot and compatible hosts can load these when relevant.
- Flat `.github/skills/*.md` files — **prompt reference material**, such as adapters, schemas, checklists, and templates. They are included only when a prompt or chatmode explicitly references them; they are not individually auto-discovered Agent Skills.
- `skills/` (this folder) — **reference-only catalog** for humans, onboarding, and broader background material. It is not shipped with the VS Code extension.

## Authoritative Rules

- Prompts use `.github/skills/` **exclusively**.
- For reusable workflows that should activate by relevance, add a lowercase directory with a `SKILL.md` containing `name` and `description` frontmatter.
- For a schema, adapter, or template that a workflow should load explicitly, add a flat reference file under `.github/skills/` and use `#file:.github/skills/<name>.md`.
- Keep general reference, training, or onboarding material in this `skills/` folder.
- If a root `skills/` document should become prompt-consumable, promote/copy it into `.github/skills/` first and update every prompt/chatmode link to that copy. The extension syncs `.github/` content, not the root `skills/` folder.

## Current Audit

- Discoverable Agent Skills: **9** `SKILL.md` directories under `.github/skills/`.
- Explicit prompt references: **72** flat Markdown files under `.github/skills/`; their `#file:` targets must exist in the installed workspace.
- Root-only reference catalog: **4** documents remain unpromoted: `azure-devops-pipelines.md`, `azure-key-vault.md`, `azure-sql-migration.md`, and `github-actions-cicd.md`.
- The prompt and chatmode audit must report **zero** links to root `skills/` paths or nonexistent hook documentation.

### Root skills with `.github/skills/` counterparts (22)

`asp-classic-to-dotnet.md`, `azd-configuration.md`, `azure-aks.md`, `azure-app-service.md`, `azure-container-apps.md`, `azure-entra-id.md`, `azure-monitor-appinsights.md`, `bicep-modules.md`, `config-transformation.md`, `cost-optimization.md`, `docker-containerize.md`, `dotnet-framework-to-dotnet8.md`, `ef-migration.md`, `java8-to-java21.md`, `managed-identity.md`, `migration-report-template.md`, `rbac-least-privilege.md`, `rollback-strategy.md`, `secret-management.md`, `terraform-azure.md`, `wcf-to-rest-api.md`, `webforms-to-razor.md`

### Root-only reference skills (4)

`azure-devops-pipelines.md`, `azure-key-vault.md`, `azure-sql-migration.md`, `github-actions-cicd.md`

### Root files that had identical `.github/skills/` counterparts and are now labeled `REFERENCE ONLY` (4)

`asp-classic-to-dotnet.md`, `azure-container-apps.md`, `docker-containerize.md`, `migration-report-template.md`

## How to use skills and references in prompts

- Keep the phase prompt focused on workflow and orchestration.
- Use a directory-based Agent Skill for reusable, relevance-triggered workflows.
- Reference flat guides, schemas, and templates with `#file:.github/skills/<reference-name>.md`.
- Compose only the prompt references required for the selected scenario instead of attaching every adapter or duplicating instructions.
- Keep skills acyclic; prompts can compose many skills, but skill files should not depend on each other recursively.
- Do **not** point prompts at `skills/` paths.

## Reference Catalog

> **Full content skills** are marked with **★**. This table describes reference material in `skills/`; the phase names are topical guidance, **not** direct prompt references to these root paths.

| Reference guide | Description | Typical migration workflows |
|---|---|---|
| **★** `skills/dotnet-framework-to-dotnet8.md` | .NET Framework to .NET 8 migration patterns | `QuickAssessment`, `Phase1-PlanAndAssess`, `Phase2-MigrateCode` |
| **★** `skills/wcf-to-rest-api.md` | WCF contracts and hosting mapped to ASP.NET Core REST APIs | `QuickAssessment`, `Phase1-PlanAndAssess`, `Phase2-MigrateCode` |
| `skills/webforms-to-razor.md` | Web Forms and ASPX modernization guidance | `QuickAssessment`, `Phase1-PlanAndAssess`, `Phase2-MigrateCode` |
| **★** `skills/java8-to-java21.md` | Java 8 to Java 21 and Spring Boot 3 modernization | `QuickAssessment`, `Phase1-PlanAndAssess`, `Phase2-MigrateCode` |
| `skills/asp-classic-to-dotnet.md` | Classic ASP to .NET 8 modernization strategy | `QuickAssessment`, `Phase1-PlanAndAssess`, `Phase2-MigrateCode` |
| **★** `skills/config-transformation.md` | `web.config` / `app.config` to `appsettings.json` patterns | `Phase1-PlanAndAssess`, `Phase2-MigrateCode`, `Phase4-DeployToAzure` |
| `skills/ef-migration.md` | ADO.NET or EF6 to EF Core migration patterns | `Phase1-PlanAndAssess`, `Phase2-MigrateCode`, `DatabaseMigration` |
| **★** `skills/azure-app-service.md` | App Service hosting and deployment patterns | `Phase1-PlanAndAssess`, `Phase3-GenerateInfra`, `Phase4-DeployToAzure` |
| `skills/azure-container-apps.md` | Container Apps patterns for APIs and background workloads | `Phase1-PlanAndAssess`, `Phase3-GenerateInfra`, `Phase4-DeployToAzure` |
| `skills/azure-aks.md` | AKS deployment and Helm chart guidance; prompt copy: `.github/skills/azure-aks.md` | `Phase1-PlanAndAssess`, `Phase3-GenerateInfra`, `Phase4-DeployToAzure` |
| `skills/azure-sql-migration.md` | SQL Server to Azure SQL Database migration guidance | `Phase1-PlanAndAssess`, `Phase3-GenerateInfra`, `DatabaseMigration` |
| **★** `skills/azure-entra-id.md` | Entra ID authentication and authorization setup | `Phase1-PlanAndAssess`, `Phase2-MigrateCode`, `Phase3-GenerateInfra`, `SecurityHardening` |
| `skills/azure-key-vault.md` | Key Vault integration patterns | `Phase3-GenerateInfra`, `Phase4-DeployToAzure`, `Phase5-SetupCICD`, `SecurityHardening` |
| `skills/azure-monitor-appinsights.md` | Azure Monitor and Application Insights observability; prompt copy: `.github/skills/azure-monitor-appinsights.md` | `Phase3-GenerateInfra`, `Phase4-DeployToAzure`, `Phase6-PostMigrationOps` |
| **★** `skills/bicep-modules.md` | Bicep module structure and Azure Verified Modules usage | `Phase3-GenerateInfra`, `Phase4-DeployToAzure` |
| `skills/terraform-azure.md` | Terraform Azure provider and module patterns; prompt copy: `.github/skills/terraform-azure.md` | `Phase3-GenerateInfra`, `Phase4-DeployToAzure` |
| `skills/azd-configuration.md` | `azure.yaml` and Azure Developer CLI setup guidance; prompt copy: `.github/skills/azd-configuration.md` | `Phase3-GenerateInfra`, `Phase4-DeployToAzure`, `Phase5-SetupCICD` |
| `skills/github-actions-cicd.md` | GitHub Actions CI/CD workflow patterns | `Phase5-SetupCICD` |
| `skills/azure-devops-pipelines.md` | Azure DevOps pipeline patterns | `Phase5-SetupCICD` |
| `skills/docker-containerize.md` | Dockerfile, image hardening, and runtime patterns | `Phase2-MigrateCode`, `Phase3-GenerateInfra`, `Phase4-DeployToAzure` |
| `skills/managed-identity.md` | Managed identity usage patterns | `Phase3-GenerateInfra`, `Phase4-DeployToAzure`, `SecurityHardening` |
| `skills/rbac-least-privilege.md` | Least-privilege RBAC assignments | `Phase3-GenerateInfra`, `Phase4-DeployToAzure`, `SecurityHardening` |
| `skills/secret-management.md` | Secret handling, Key Vault, and pipeline secret guidance | `Phase2-MigrateCode`, `Phase3-GenerateInfra`, `Phase5-SetupCICD`, `SecurityHardening` |
| **★** `skills/migration-report-template.md` | Standard report format for assessment and migration phases | `Phase0-Multi-repo-assessment`, `Phase1-PlanAndAssess`, `GetStatus`, `Phase6-PostMigrationOps` |
| `skills/rollback-strategy.md` | Rollback, cutover, and recovery planning patterns | `Phase4-DeployToAzure`, `Phase5-SetupCICD`, `Phase-Rollback` |
| `skills/cost-optimization.md` | Azure cost optimization patterns for target architecture; prompt copy: `.github/skills/cost-optimization.md` | `CostOptimization`, `Phase3-GenerateInfra`, `Phase4-DeployToAzure`, `Phase6-PostMigrationOps` |

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
7. `#file:.github/skills/azure-monitor-appinsights.md`
8. `#file:.github/skills/bicep-modules.md`
9. `#file:.github/skills/azd-configuration.md`
10. Promote `skills/github-actions-cicd.md` before using it in a prompt

Use this composition when modernizing ASP.NET Web Forms or MVC on .NET Framework into an App Service-hosted .NET 8 web app with Bicep-based deployment.

### Scenario B: Java API -> Container Apps

Compose these skills in order:

1. `#file:.github/skills/java8-to-java21.md`
2. `#file:.github/skills/azure-container-apps.md`
3. `#file:.github/skills/azure-entra-id.md`
4. Promote `skills/azure-key-vault.md` before using it in a prompt
5. `#file:.github/skills/azure-monitor-appinsights.md`
6. `#file:.github/skills/terraform-azure.md`
7. `#file:.github/skills/azd-configuration.md`
8. Promote `skills/github-actions-cicd.md` before using it in a prompt
9. `#file:.github/skills/docker-containerize.md`

Use this composition for stateless Java APIs that will be containerized, deployed to Container Apps, and managed through Terraform.

### Scenario C: WCF -> AKS

Compose these skills in order:

1. `#file:.github/skills/wcf-to-rest-api.md`
2. `#file:.github/skills/config-transformation.md`
3. `#file:.github/skills/ef-migration.md`
4. `#file:.github/skills/azure-aks.md`
5. `#file:.github/skills/azure-entra-id.md`
6. Promote `skills/azure-key-vault.md` before using it in a prompt
7. `#file:.github/skills/azure-monitor-appinsights.md`
8. `#file:.github/skills/bicep-modules.md`
9. `#file:.github/skills/azd-configuration.md`
10. Promote `skills/github-actions-cicd.md` before using it in a prompt
11. `#file:.github/skills/docker-containerize.md`

Use this composition when a WCF estate is split into containerized ASP.NET Core services deployed to AKS with Bicep-managed infrastructure.

## Authoring conventions

- Keep each skill narrowly focused and reusable.
- Prefer concrete checklists, mappings, snippets, and validation commands.
- Use conditional language only when a choice genuinely depends on workload characteristics.
- Point prompts to multiple `.github/skills/` files rather than re-describing the same migration pattern.
