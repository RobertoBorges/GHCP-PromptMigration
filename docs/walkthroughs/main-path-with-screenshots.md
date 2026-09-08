# Main-path migration walkthrough (with screenshot slots)

An end-to-end walkthrough of the default 7-step Azure migration flow, taking you from an unknown application to a working Azure deployment. Screenshots are placeholders — replace them by running the flow on a real workspace and capturing the marked moments.

> **How to fill in the screenshots:** Each `📷 SCREENSHOT` block calls out exactly what to capture. Take screenshots against a **real customer-anonymized workspace** and drop them into `docs/walkthroughs/main-path-images/` using the filenames indicated. Then remove the placeholder markers.

## Prerequisites

- VS Code 1.90+ with the [Azure Migration Agent extension](https://marketplace.visualstudio.com/) installed
- GitHub Copilot Chat installed and signed in
- A workspace open in VS Code with the app to migrate (any stack, any source)

## Step 1: Initialize the extension

Open Command Palette (`Ctrl+Shift+P`) and run `Azure Migration: Initialize in this workspace`.

The extension scaffolds:
- `.github/` — agent + prompts + skills
- `MIGRATION-START-HERE.md` — welcome doc (auto-opens on first run)
- `reports/` — where all output artifacts live

> 📷 **SCREENSHOT: `01-initialize-success.png`**
> Capture: the "Initialize" success notification + the auto-opened `MIGRATION-START-HERE.md` in the editor, sidebar rocket icon 🚀 visible on the left.

## Step 2: Assess the application (`/assess-any-application`)

Open Copilot Chat (`Ctrl+Alt+I`) and type:

```
/assess-any-application
```

Or use natural language: *"Assess this application for Azure migration."*

The agent walks you through:
- Confidence-labeled source classification (on-prem / AWS / GCP / K8s / GitHub / ZIP / other)
- Stack detection (.NET / Java / Python / Node.js / PHP / Ruby / Go / …)
- Workload pattern (web / API / batch / event-driven / serverless / …)
- Data + integrations inventory

Produces two files:
- `reports/Discovery-Dossier.md` — narrative
- `reports/Capability-Matrix.yaml` — structured contract that Phase 1-6 consume

> 📷 **SCREENSHOT: `02-assess-any-application-running.png`**
> Capture: Copilot Chat mid-way through the interview, showing the agent asking a confidence question about the source environment. Include the `.github/prompts/Assess-Any-Application.prompt.md` tree entry in the sidebar.

> 📷 **SCREENSHOT: `03-discovery-dossier-produced.png`**
> Capture: `reports/Discovery-Dossier.md` open in preview mode with the header + first classification table visible. Include the sidebar showing both `Discovery-Dossier.md` and `Capability-Matrix.yaml` under `reports/`.

## Step 3: Plan (`/Phase1-Plan`)

Next, generate the `reports/Decisions-Required.md` file — the 18 canonical architecture decisions the agent will refuse to guess on your behalf.

```
/Phase1-Plan
```

Produces:
- `reports/Decisions-Required.md` — 18 decisions with option matrices + tradeoffs
- `reports/Application-Assessment-Report.md` — per-app narrative
- `reports/Migration-Plan.md` — phased plan

> 📷 **SCREENSHOT: `04-decisions-required.png`**
> Capture: `reports/Decisions-Required.md` open in preview mode, scrolled to a representative decision (e.g., D-01 Target framework, D-06 Hosting platform). Include the "Decisions" node in the sidebar tree showing pending status count.

You'll now be asked to answer the 18 decisions before Phase 2 starts. **This is the Decision Hardstop Protocol** — the agent will not make major architecture choices for you.

> 📷 **SCREENSHOT: `05-decision-hardstop-gate.png`**
> Capture: Copilot Chat showing the agent presenting an options table with tradeoffs, waiting for your pick. Highlight the "Stay-as-is" option (option 1 in every block).

## Step 4: Migrate code (`/Phase2-MigrateCode`)

Once your decisions are `✅ DECIDED`, run:

```
/Phase2-MigrateCode
```

The agent applies the stack-appropriate skill (e.g., `stack-dotnet.md`, `stack-java.md`, `stack-python.md`) and makes minimum-viable-Azure-compatibility changes:

- Framework version upgrade
- File-system I/O → Azure Blob Storage / Files
- Local auth → Entra ID + Managed Identity
- Local config → App Configuration + Key Vault
- Local logging → Application Insights + OpenTelemetry

> 📷 **SCREENSHOT: `06-phase2-code-changes.png`**
> Capture: VS Code diff view showing before/after of one file (e.g., `Program.cs` with the DefaultAzureCredential wiring, or `application.yml` with Key Vault reference). Sidebar shows list of touched files.

## Step 5: Generate infrastructure (`/Phase3-GenerateInfra`)

```
/Phase3-GenerateInfra
```

Produces `infra/` folder with Bicep or Terraform (per your D-07 decision), using Azure Verified Modules. Wires:

- Managed identity → target resources
- Key Vault with RBAC (no access policies)
- Application Insights + Log Analytics
- Networking + Private Endpoints (per D-10 tenancy decision)

> 📷 **SCREENSHOT: `07-infra-generated.png`**
> Capture: The `infra/` folder in the sidebar expanded, with `main.bicep` open showing the top-level resource declarations and clear AVM module references.

## Step 6: Deploy (`/Phase4-DeployToAzure`)

```
/Phase4-DeployToAzure
```

Runs `azd provision && azd deploy` in a controlled sequence. Handles:

- Coexistence period (D-14 decision)
- DNS + TLS cutover
- Data seeding / migration invocation
- Post-deploy smoke tests

> 📷 **SCREENSHOT: `08-deploy-running.png`**
> Capture: VS Code integrated terminal running `azd deploy` with the Azure portal open in another window showing the newly-created resources.

## Step 7: CI/CD (`/Phase5-SetupCICD`)

```
/Phase5-SetupCICD
```

Produces:

- `.github/workflows/azure-deploy.yml` — automated deploy per the D-16 decision
- Environment protection rules
- OIDC federation to Entra ID (no long-lived secrets)
- Pull-request preview environments (optional)

> 📷 **SCREENSHOT: `09-cicd-workflow.png`**
> Capture: The generated GitHub Actions workflow file open in the editor, with the sidebar showing a completed run in the Actions panel.

## Step 8: Post-migration operations (`/Phase6-PostMigrationOps`)

```
/Phase6-PostMigrationOps
```

Wires ongoing operations:

- Availability / Reliability alerts
- Cost budget + anomaly alerts
- Security hardening pass (per D-11)
- Backup / DR verification (per D-13)

> 📷 **SCREENSHOT: `10-ops-dashboard.png`**
> Capture: Azure portal showing the Application Insights dashboard for the migrated app with live traffic + the cost budget alert in Cost Management.

## Congratulations — migration complete

At this point the `reports/Report-Status.md` Action Log shows the full trace of what was done, when, and (approximately) how many tokens each action consumed. Use it to:

- Recover a session that was interrupted
- Explain to stakeholders what work was performed
- Aggregate token costs across migrations for engagement accounting

> 📷 **SCREENSHOT: `11-action-log.png`**
> Capture: `reports/Report-Status.md` open in preview mode scrolled to the `## 📜 Action Log` section, showing a chronological trail from Assess through Phase 6.

## Where to go next

- **Multi-repo business solution?** Run `/Phase0-Multi-repo-assessment` at the very start, before `/assess-any-application`.
- **Whole portfolio?** Run `/PortfolioStrategy` for a CIO-ready deck across many apps.
- **AWS-sourced workload?** After Discovery, chain into `/AWSAssess-Phase0-SetupAndScope` for a read-only estate scan, then `/AWS2Azure-Phase1-Plan` for the migration.
- **Something the agent doesn't know how to migrate?** The `skill-creator` meta-skill offers to author a new skill on the fly — accept it and continue.

See [`MIGRATION-START-HERE.md`](../../MIGRATION-START-HERE.md) for the full add-ons matrix.
