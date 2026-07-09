---
name: Phase4-DeployToAzure
description: Deploy the validated project to Azure using Azure Developer CLI
argument-hint: "Specify environment if needed, e.g., 'Deploy to dev environment' or 'Deploy to production'"
agent: Code Migration Modernization Agent
model: Claude Sonnet 4.7 (copilot)
---

<!-- BEGIN: capability-matrix-gate (auto-managed by inject-capability-matrix-gates.mjs) -->

## 🚦 MANDATORY OPENING CHECK — Capability Matrix Required

**Before doing ANY work for Phase 4 — Deploy to Azure, verify the Discovery contract:**

| Required artifact | Location | If missing |
|-------------------|----------|------------|
| Discovery Dossier | `reports/Discovery-Dossier.md` | **STOP** — run `/assess-any-application` first |
| Capability Matrix | `reports/Capability-Matrix.yaml` | **STOP** — run `/assess-any-application` first |
| Approved Migration Plan | `reports/Migration-Plan.md` | **STOP** — run `/Phase1-Plan` (or the `/build-migration-plan` add-on) |

### If ANY of those three artifacts is missing

Reply with exactly:

```
🚨 Phase 4 — Deploy to Azure cannot proceed without the Discovery contract.

Missing artifacts:
  - reports/Discovery-Dossier.md          [missing/present]
  - reports/Capability-Matrix.yaml         [missing/present]
  - reports/Migration-Plan.md              [missing/present]

Required steps before re-running this phase:
  1. Open Copilot Chat → /assess-any-application  (or in CLI: "assess this application")
  2. Then: /Phase1-Plan                            (produces the Migration Plan, or use /build-migration-plan add-on)
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

<!-- BEGIN: action-log-contract (auto-managed by inject-action-log-contract.mjs) -->

## 📜 Action Log Contract

**After each meaningful action** in this prompt, append one single-line entry to the `## 📜 Action Log` section at the bottom of `reports/Report-Status.md`.

Canonical format:
```
- <ISO-8601-UTC> | actor=Phase4-DeployToAzure | action=<verb-phrase> | files=<+created,~modified,-deleted> | tokens=~<bucket> | turn=<n> | notes="<free text>"
```

Rules:
- Use `actor=Phase4-DeployToAzure` for actions taken by this prompt.
- Use `actor=User` for actions taken by the user (e.g., answering a decision).
- Log **only meaningful actions**: phase transitions, artifact production, decision events, gate passes/blocks, user inputs, rollback events. Do NOT log every internal grep or file read.
- Estimate `tokens` in buckets: `~0`, `~500`, `~2k`, `~8k`, `~30k`. The `turn` counter is exact; token estimate is best-effort. Point users to Copilot Dashboard for authoritative counts.
- If `reports/Report-Status.md` doesn't exist yet, create it from `.github/skills/migration-report-template.md` first — it already includes the `## 📜 Action Log` section.

Full spec: `.github/skills/action-log-format.md`.

<!-- END: action-log-contract -->


<!-- BEGIN: decision-hardstop-gate (auto-managed by inject-decision-gates.mjs) -->

## 🛑 MANDATORY DECISION GATE — Major decisions required for Phase 4 — Deploy to Azure

The Code Migration Modernization Agent does **not** decide major architecture on your behalf.
Before Phase 4 — Deploy to Azure can do any work, every decision below must be **DECIDED** in
`reports/Decisions-Required.md` (or marked **🚫 N/A** if genuinely not applicable).

| Catalog ID | Decision | Required status |
|-----------|----------|-----------------|
| D-08 | Region & data residency (confirm) | ✅ DECIDED (or 🚫 N/A) |
| D-14 | Cutover strategy | ✅ DECIDED (or 🚫 N/A) |
| D-15 | Acceptable downtime | ✅ DECIDED (or 🚫 N/A) |

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
5. If `reports/Decisions-Required.md` is missing → STOP and route the user to `/Phase1-Plan`.

### Hard rules

- **Never assume.** Newer is not automatically better. "What most projects use" is not a decision.
- **Never silently pick.** If a value is missing, ask. Don't infer.
- **Never accept brief replies.** "Use SQL" is not enough — confirm engine, tier, region.
- **Never bypass with an expert flag.** This protocol applies on every project.

See [`.github/skills/decision-hardstop.md`](../skills/decision-hardstop.md) for the full protocol
and [`.github/skills/decision-catalog.md`](../skills/decision-catalog.md) for canonical option matrices.

<!-- END: decision-hardstop-gate -->

Deploy application to Azure, using Azure Developer CLI (azd) for streamlined deployment. 

## Preconditions

Before deploying to Azure, verify Phase 3 (Infrastructure Generation) is complete:

1. Check `reports/Report-Status.md` shows **Phase 3: Infrastructure Generation** as ✅ complete.
2. Confirm the `infra/` folder contains Bicep or Terraform files validated by `azure_check_predeploy`.
3. Confirm `azure.yaml` exists at the root of the modernized project.
4. If preconditions are not met, **STOP** and ask the user to run `/Phase3-GenerateInfra` first.

# Rules for deployment using user's desktop

- Use files generated by the previous steps in the 'reports' folder as references for deployment.
- Guide the user using the 'runCommands' to deploy using Azure Developer CLI (azd).
At the end, generate a comprehensive deployment summary report at `reports/Deployment-Summary-Report.md`, including:
- Deployment timeline and status
- Resource configurations and endpoints
- Security and monitoring setup
- Performance baseline measurements
- Operational procedures and troubleshooting guides
- Cost analysis and optimization recommendations
- Next steps for ongoing maintenance and optimization

- Suggest that the next step is to set up CI/CD pipelines, and mention `/Phase5-SetupCICD` is the command to start the CI/CD setup process.
- At the end, update the status report file reports/Report-Status.md with the status of the deployment step.

## Next Steps

When deployment is complete:

1. ✅ Update `reports/Report-Status.md` to mark **Phase 4: Deployment to Azure** as complete.
2. ▶️ Output the following Next Steps block to the user:

   > **Next Steps**
   >
   > Run **`/Phase5-SetupCICD`** to configure CI/CD pipelines.
   >
   > Or click **🔄 Set up CI/CD pipelines** if the handoff button is visible in your UI.

## Pre-Deployment Checklist

Before deploying, ensure:
- You have the latest Azure CLI and Azure Developer CLI installed
- You are logged in to Azure (`az login`)
- You have selected the correct subscription (`az account set --subscription <subscription-id>`)
- Your infrastructure files in the `infra/` folder are correctly set up and validated
- Your application code is ready for deployment
- If containerization is required, ensure Docker is installed and running

## Deployment Process Based on Target Platform

### For Azure App Service Deployments:
- Configure deployment settings in azure.yaml
- Set up application settings and connection strings
- Configure continuous deployment if needed
- Set up custom domains and SSL certificates if applicable
- Configure scaling rules
- Set up monitoring with Application Insights

### For Azure Kubernetes Service (AKS) Deployments:
- Ensure container images are built and pushed to a container registry
- Configure Kubernetes manifests or Helm charts
- Set up ingress controllers if needed
- Configure horizontal pod autoscalers
- Set up monitoring with Azure Monitor for Containers
- Configure network policies and security settings

### For Azure Container Apps Deployments:
- Ensure container images are built and pushed to a container registry
- Configure container app settings in the infrastructure files
- Set up scaling rules and triggers
- Configure ingress settings if needed
- Set up monitoring with Application Insights
- Configure environment variables and secrets

## Deployment Steps

1. **Environment Setup**
   ```bash
   # Initialize azd environment
   azd init

   # or use an existing environment
   azd env select <environment-name>
   ```

2. **Deploy the Application**
   ```bash
   # Deploy with azd
   azd up
   
   # Or provision infrastructure separately
   azd provision
   
   # Then deploy code
   azd deploy
   ```

3. **Verify Deployment**
   Use `azure_get_azd_app_logs` to check application logs and health status:
   - Verify all resources were created successfully in Azure portal
   - Check application logs for any errors or warnings
   - Test application functionality including authentication flows
   - Verify monitoring is working properly with Application Insights
   - Check that authentication with Entra ID is working correctly
   - Validate database connections and data access
   - Test API endpoints and verify proper responses
   - Check scaling and performance under load
   - Verify security configurations are properly applied

## Post-Deployment Tasks

- Use `azure_applens-diagnose_resource` to perform health checks on deployed resources
- Configure any additional settings in the Azure portal
- Set up CI/CD pipelines using `azure_config_deploymentpipeline` for future deployments
- Configure monitoring alerts and notification channels
- Set up backup and disaster recovery policies
- Validate security configurations and run security scans
- Perform load testing to validate performance
- Document the deployment process and configuration
- Create runbooks for operational procedures
- Set up cost monitoring and optimization alerts

## Error Handling and Troubleshooting

- If deployment fails, use `azure_activity_log-list` to investigate issues
- Use `azure_applens-diagnose_resource` to get insights into resource problems
- Check `azure_get_azd_app_logs` for application-specific errors
- Validate that all prerequisites are met (quotas, permissions, etc.)
- Verify that infrastructure files pass all validation checks
- Check for regional service outages or capacity issues

