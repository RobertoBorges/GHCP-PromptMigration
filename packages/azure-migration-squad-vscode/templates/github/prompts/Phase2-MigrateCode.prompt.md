---
name: Phase2-MigrateCode
description: Upgrade legacy .NET or Java application code to modern framework versions
argument-hint: "Specify target framework if not already assessed, e.g., 'Migrate to .NET 10' or 'Upgrade to Spring Boot 3'"
agent: Code Migration Modernization Agent
---





<!-- BEGIN: capability-matrix-gate (auto-managed by inject-capability-matrix-gates.mjs) -->

## 🚦 MANDATORY OPENING CHECK — Capability Matrix Required

**Before doing ANY work for Phase 2 — Migrate Code, verify the Discovery contract:**

| Required artifact | Location | If missing |
|-------------------|----------|------------|
| Discovery Dossier | `reports/Discovery-Dossier.md` | **STOP** — run `/assess-any-application` first |
| Capability Matrix | `reports/Capability-Matrix.yaml` | **STOP** — run `/assess-any-application` first |
| Approved Migration Plan | `reports/Migration-Plan.md` | **STOP** — run `/build-migration-plan` |

### If ANY of those three artifacts is missing

Reply with exactly:

```
🚨 Phase 2 — Migrate Code cannot proceed without the Discovery contract.

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

## 🛑 MANDATORY DECISION GATE — Major decisions required for Phase 2 — Migrate Code

The Code Migration Modernization Agent does **not** decide major architecture on your behalf.
Before Phase 2 — Migrate Code can do any work, every decision below must be **DECIDED** in
`reports/Decisions-Required.md` (or marked **🚫 N/A** if genuinely not applicable).

| Catalog ID | Decision | Required status |
|-----------|----------|-----------------|
| D-01 | Target framework / runtime version | ✅ DECIDED (or 🚫 N/A) |
| D-02 | UI architecture | ✅ DECIDED (or 🚫 N/A) |
| D-03 | Backend / API style _(only when migration.strategy is rearchitect or rebuild)_ | ✅ DECIDED (or 🚫 N/A) |
| D-04 | Database engine | ✅ DECIDED (or 🚫 N/A) |
| D-09 | Authentication | ✅ DECIDED (or 🚫 N/A) |

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

Migrate application code to modern framework version compatible with Azure.

## Preconditions

Before starting code migration, verify Phase 1 (Planning & Assessment) is complete:

1. Check `reports/Report-Status.md` shows **Phase 1: Planning & Assessment** as ✅ complete.
2. Confirm `reports/Application-Assessment-Report.md` exists with target framework, hosting platform, and IaC choices recorded.
3. If either is missing, **STOP** and ask the user to run `/Phase1-PlanAndAssess` first.

You review code through multiple perspectives simultaneously. Run each perspective as a parallel subagent so findings are independent and unbiased.

After all subagents complete, synthesize findings into a prioritized summary at `reports/Business-Logic-Mapping.md`. 

## Skills to Load

Load the appropriate skills based on application type:
- **business-logic-mapping** skill — **ALWAYS** use to track and preserve business logic during migration
- For .NET applications: Use **dotnet-modernization** skill for patterns and templates
- For Java applications: Use **java-modernization** skill for patterns and templates  
- For WCF services: Use **wcf-to-rest-migration** skill for service conversion
- For config files: Use **config-transformation** skill for settings migration

## Business Logic Preservation (Critical)

Before making any code changes:
1. **Create** `reports/Business-Logic-Mapping.md` to track all business logic
2. **Identify** all business logic in the legacy application (see business-logic-mapping skill)
3. **Document** each business logic item with source location
4. **Update** the mapping document as you migrate each item
5. **Verify** each migrated item produces the same results

Categories to track:
- Calculations (pricing, tax, discounts, etc.)
- Validations (business rules, constraints)
- Workflows (state machines, approval chains)
- Transformations (data conversions, aggregations)
- Integrations (external APIs, third-party services)
- Authorization (business-level permissions)
- Notifications (email triggers, alerts)
- Scheduling (batch jobs, timed operations)

## Media and Asset Preservation

Track and copy all media assets:
- Images, CSS, JavaScript, fonts
- User uploads and documents
- Email templates, report templates
- Localization/resource files

Update `reports/Business-Logic-Mapping.md` with asset migration status.

Ensure appropriate Azure extensions for the target framework are installed in VS Code.

Always start migration by creating a new folder under the root folder with an intuitive name for the modernized project. 

Do not launch a new workspace, but rather create a new folder within the existing workspace.

Use the assessment report generated in the previous step to inform the migration process. The assessment report can be found in the 'reports' folder.

Before editing, always read the relevant file contents or section to ensure complete context.

Use `semantic_search` tool to identify all code files that need migration.

Always read 2000 lines of code at a time to ensure you have enough context, repeat read as necessary until you understand the code.

If a patch is not applied correctly, attempt to reapply it.

Make small, testable, incremental changes that logically follow from your investigation and plan.

Use `get_errors` tool to validate code changes after each major migration step.

Before starting the migration create a '[OLD-SYSTEM-NAME-Migrated]' folder in the workspace to store the new code files.

If the '[OLD-SYSTEM-NAME-Migrated]' folder already exists, ask the user if they want to overwrite it.

Use the guidance from the assessment report (reports/Application-Assessment-Report.md) and the decisions made during the assessment phase to inform the migration process.

Copy media files from the original project directory to the new project directory at same relative paths.

Keep equivalent UI components to avoid breaking changes.

Confirm that all functionality is preserved after migration.

Containerize the application if specified in the assessment report.

Create a Script to build and run the application in a Docker container, if applicable.

Make sure you build the application as you create it, and fix them as you go.

Based on the assessed application type (.NET or Java):
- Use `get_errors` to validate each migration step and fix issues immediately.
- Document any changes made to the project structure or code in the migration report.
- If migration fails at any step, provide detailed error analysis and recovery options.

Suggest that the next step is to generate infrastructure files, and mention `/Phase3-GenerateInfra` is the command to start the infra generation process.

At the end, update the status report file reports/Report-Status.md with the status of the migration step.

## Next Steps

When code migration is complete:

1. ✅ Update `reports/Report-Status.md` to mark **Phase 2: Code Modernization** as complete.
2. ▶️ Output the following Next Steps block to the user:

   > **Next Steps**
   >
   > Run **`/Phase3-GenerateInfra`** to generate Azure infrastructure as code.
   >
   > Or click **🏗️ Generate Azure infrastructure (Bicep/Terraform)** if the handoff button is visible in your UI.

## For .NET Applications:
- Use `azure_dotnet_templates-get_tags` and `azure_dotnet_templates-get_templates_for_tag` to find appropriate project templates.
- Create a modern .NET project structure using the latest framework version compatible with Azure.
- Use `file_search` to locate all source files for migration.
- Use `semantic_search` to identify patterns that need modernization.
- Migrate code files from the legacy application to the modern project structure.
- Transform configuration:
  - Convert web.config or app.config to appsettings.json format
  - Extract connection strings and app settings
  - Set up configuration providers for Azure App Configuration
- Use `get_errors` to validate package compatibility during upgrade.
- Upgrade NuGet packages to compatible versions.
- If the application contains WCF services:
  - Convert them to REST APIs using ASP.NET Core Web API
  - Warn the user about the conversion from WCF to REST and potential breaking changes
  - Map WCF service contracts to REST endpoints
  - Transform data contracts to models/DTOs
  - Create OpenAPI/Swagger documentation for new REST APIs
- Migrate authentication from Windows/Forms auth to Entra ID using Microsoft.Identity.Web.
- Update database access code to use Azure-compatible providers.

## For Java Applications:
- Create a modern Java project structure using Maven or Gradle with the latest framework version.
- Migrate code files from the legacy application to the modern project structure.
- Transform configuration:
  - Convert XML configs to application.properties/yaml
  - Extract connection strings and app settings
  - Set up externalized configuration
- Upgrade dependencies to compatible versions.
- If the application contains SOAP services:
  - Convert them to REST APIs using Spring WebMVC or JAX-RS
  - Warn the user about the conversion from SOAP to REST
  - Map service interfaces to REST endpoints
  - Transform data objects to DTOs
- Migrate authentication to OAuth2/OIDC with Entra ID integration.
- Update database access code to be compatible with Azure databases.
- Set up proper logging with SLF4J and Azure-compatible appenders.

