---
name: Phase3-GenerateInfra
description: Generate Bicep or Terraform infrastructure as code for Azure deployment
argument-hint: "Specify IaC preference if not already set, e.g., 'Generate Bicep for App Service' or 'Create Terraform for AKS'"
agent: Code Migration Modernization Agent
---





<!-- BEGIN: capability-matrix-gate (auto-managed by inject-capability-matrix-gates.mjs) -->

## 🚦 MANDATORY OPENING CHECK — Capability Matrix Required

**Before doing ANY work for Phase 3 — Generate Infra, verify the Discovery contract:**

| Required artifact | Location | If missing |
|-------------------|----------|------------|
| Discovery Dossier | `reports/Discovery-Dossier.md` | **STOP** — run `/assess-any-application` first |
| Capability Matrix | `reports/Capability-Matrix.yaml` | **STOP** — run `/assess-any-application` first |
| Approved Migration Plan | `reports/Migration-Plan.md` | **STOP** — run `/build-migration-plan` |

### If ANY of those three artifacts is missing

Reply with exactly:

```
🚨 Phase 3 — Generate Infra cannot proceed without the Discovery contract.

Missing artifacts:
  - reports/Discovery-Dossier.md          [missing/present]
  - reports/Capability-Matrix.yaml         [missing/present]
  - reports/Migration-Plan.md              [missing/present]

Required steps before re-running this phase:
  1. Open Copilot Chat → /assess-any-application  (or in CLI: "assess this application")
  2. Then: /build-migration-plan                  (or in CLI: "build the migration plan")
  3. Then: /phase...

To override (skip Discovery and accept risk), log a waiver entry in
reports/Decision-Log.md with `Waiver: skip-discovery=<reason>` and re-invoke
this prompt with the `--accept-risk` natural-language flag in your request.
```

**Do NOT proceed past this gate unless:**
- All three artifacts exist, OR
- A waiver entry exists in `reports/Decision-Log.md` AND the user explicitly said "skip discovery" or similar

### When the gate passes

1. Read `reports/Capability-Matrix.yaml` and extract these fields you must honor:
   - `source.primary_adapter` → load the matching `source-*` skill
   - `stack.primary_stack` + `stack.secondary_stacks` → load matching `stack-*` skills
   - `workload.primary_pattern` → load matching `workload-*` skill
   - `migration_strategy.recommendation` → adjust phase emphasis based on the recommended strategy
   - `risk_flags` → load the matching risk skills (e.g., `risk-cross-region-data.md`)
   - `unresolved_questions` → if any remain unanswered, surface them BEFORE starting work
2. Read `reports/Migration-Plan.md` for approved sequencing and any app-specific extra gates.
3. Confirm Phase prerequisites are met.

<!-- END: capability-matrix-gate -->
<!-- BEGIN: decision-hardstop-gate (auto-managed by inject-decision-gates.mjs) -->

## 🛑 MANDATORY DECISION GATE — Major decisions required for Phase 3 — Generate Infra

The Code Migration Modernization Agent does **not** decide major architecture on your behalf.
Before Phase 3 — Generate Infra can do any work, every decision below must be **DECIDED** in
`reports/Decisions-Required.md` (or marked **🚫 N/A** if genuinely not applicable).

| Catalog ID | Decision | Required status |
|-----------|----------|-----------------|
| D-06 | Hosting platform | ✅ DECIDED (or 🚫 N/A) |
| D-07 | IaC tool | ✅ DECIDED (or 🚫 N/A) |
| D-08 | Region & data residency | ✅ DECIDED (or 🚫 N/A) |
| D-10 | Multi-tenancy approach _(only if app is multi-tenant)_ | ✅ DECIDED (or 🚫 N/A) |
| D-12 | Cost ceiling | ✅ DECIDED (or 🚫 N/A) |
| D-13 | DR — RPO / RTO targets | ✅ DECIDED (or 🚫 N/A) |
| D-18 | Container registry _(only if hosting is container-based)_ | ✅ DECIDED (or 🚫 N/A) |

### Check sequence (run this BEFORE anything else in this prompt)

1. Open `reports/Decisions-Required.md`.
2. For each row in the table above, locate its section and read **Status**.
3. Any decision still at `⏸ PENDING` → STOP. Do not proceed.
4. Apply the **Decision Hardstop protocol** from `.github/skills/decision-hardstop.md`:
   - Post the 🛑 DECISION REQUIRED block in chat with options + tradeoffs from `.github/skills/decision-catalog.md`.
   - Wait for the user's reply (or for the file to be updated).
   - Record the answer in `reports/Decision-Log.md`.
   - Update Status to `✅ DECIDED <ISO date>` in `reports/Decisions-Required.md`.
   - THEN re-run the check sequence.
5. If `reports/Decisions-Required.md` is missing → STOP and route the user to `/Phase1-PlanAndAssess`.

### Hard rules

- **Never assume.** Newer is not automatically better. "What most projects use" is not a decision.
- **Never silently pick.** If a value is missing, ask. Don't infer.
- **Never accept brief replies.** "Use SQL" is not enough — confirm engine, tier, region.
- **Never bypass with an expert flag.** This protocol applies on every project.

See [`.github/skills/decision-hardstop.md`](../skills/decision-hardstop.md) for the full protocol
and [`.github/skills/decision-catalog.md`](../skills/decision-catalog.md) for canonical option matrices.

<!-- END: decision-hardstop-gate -->

Generate Infrastructure as Code Files for Azure Deployment

## Preconditions

Before generating infrastructure, verify Phase 2 (Code Modernization) is complete:

1. Check `reports/Report-Status.md` shows **Phase 2: Code Modernization** as ✅ complete.
2. Confirm a migrated project folder exists (e.g., `<OriginalName>-Migrated/`) with successfully building code.
3. Confirm `reports/Business-Logic-Mapping.md` exists.
4. If preconditions are not met, **STOP** and ask the user to run `/Phase2-MigrateCode` first.

Load the **azure-infrastructure** skill for Bicep/Terraform templates and Azure Verified Modules patterns.
Load the **azure-containerization** skill if containerization was selected in the assessment.

Use `azure_development-summarize_topic` tool to get high-level instructions to follow.

Use `azure_recommend_service_config` to automatically detect services and dependencies from the migrated application.

Use `azure_check_region` to validate that required Azure services are available in the target region.

Use `azure_check_quota` to ensure sufficient quota for deployment.

Create an 'infra' directory in the modernized project folder if it doesn't already exist.

Create an azure.yaml file in the root of the modernized project for Azure Developer CLI (azd) support.

Use `azure_check_predeploy` to validate the generated infrastructure files.

Use managed identities for authentication instead of connection strings and keys.

Set up proper RBAC with least privilege principles.

Configure appropriate scaling settings based on the application requirements.

Set up proper networking and security configurations including private endpoints where applicable.

Configure cost optimization settings (auto-scaling, reserved instances where appropriate).

Set up monitoring, alerting, and log aggregation.

Include infrastructure testing and validation scripts.

If infrastructure generation fails, provide detailed error analysis and alternative approaches.

Make the infrastructure section in the migration report human-readable and in markdown format, using headings, bullet points, and other formatting options as appropriate.

Suggest that the next step is to deploy to Azure, and mention `/Phase4-DeployToAzure` is the command to start the deployment process.

At the end, update the status report file reports/Report-Status.md with the status of the infrastructure generation step, including:
  - Infrastructure components created
  - Security configurations implemented  
  - Monitoring and logging setup
  - Any issues encountered during generation

## Next Steps

When infrastructure generation is complete:

1. ✅ Update `reports/Report-Status.md` to mark **Phase 3: Infrastructure Generation** as complete.
2. ▶️ Output the following Next Steps block to the user:

   > **Next Steps**
   >
   > Run **`/Phase4-DeployToAzure`** to deploy to Azure.
   >
   > Or click **☁️ Deploy to Azure** if the handoff button is visible in your UI.

Set up proper monitoring with Application Insights and Log Analytics.

Configure Entra ID integration for authentication with proper RBAC.

Set up database resources if applicable (Azure SQL, Cosmos DB, etc.) with private endpoints.

Include proper tagging and naming conventions using resource tokens.

Implement security best practices: managed identities, private endpoints, network restrictions.

Configure RBAC assignments for service-to-service authentication using managed identities.

Based on the chosen Azure hosting platform in the assessment report (App Service, AKS, or Container Apps), generate the appropriate infrastructure files:

## For Bicep Infrastructure:
- Use Azure Verified Modules (AVM) where available for best practices, https://github.com/Azure/bicep-registry-modules.
- Use `azure_bicep_schemas-get_bicep_resource_schema` tool for each resource type to ensure correct schema usage.
- Create the following structure in the 'infra' folder:
  - main.bicep - Main deployment file with proper targeting scope
  - main.parameters.json - Parameters for the deployment
  - modules/ - Folder for modular Bicep files
    - appService.bicep or containerApp.bicep or aks.bicep (depending on chosen platform)
    - monitoring.bicep - Application Insights and Log Analytics resources
    - database.bicep (if applicable) - Database resources with proper networking
    - identityAndSecurity.bicep - Managed Identity and RBAC setup
    - networking.bicep (if applicable) - VNet, NSG, private endpoints
    - keyvault.bicep - Azure Key Vault for secrets management
    - Key Vault must be configured with RBAC only (do not use access policies)
- Configure the infrastructure for the selected hosting platform:
  - For App Service: Set up App Service Plan, App Service, deployment slots, and related resources
  - For AKS: Set up AKS cluster, node pools, Azure Container Registry, and related resources
  - For Container Apps: Set up Container Apps Environment, Container Registry, and Container Apps

## For Terraform Infrastructure:
- Use `mcp_azure_mcp_azureterraformbestpractices` to retrieve current Terraform best practices for Azure.
- Create the following structure in the 'infra' folder:
  - main.tf - Main deployment file
  - variables.tf - Variable definitions
  - outputs.tf - Output definitions
  - providers.tf - Provider configuration
  - modules/ - Folder for modular Terraform files
    - app_service/ or container_app/ or aks/ (depending on chosen platform)
    - monitoring/ - Application Insights and Log Analytics resources
    - database/ (if applicable) - Database resources
    - identity/ - Managed Identity and RBAC setup
    - networking/ (if applicable) - VNet, NSG, etc.
- Configure the infrastructure for the selected hosting platform.
- Set up proper monitoring with Application Insights and Log Analytics.
- Configure Entra ID integration for authentication.
- Set up database resources if applicable (Azure SQL, Cosmos DB, etc.).
- Include proper tagging and naming conventions.
- Prefer Managed Identity and OIDC federated credentials; avoid storing secrets in state or code.
