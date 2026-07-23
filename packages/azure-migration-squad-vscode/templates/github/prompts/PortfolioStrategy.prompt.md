---
name: PortfolioStrategy
description: Generate an executive-ready Migration Strategy Report (HTML deck) for a customer portfolio — invokes the migration-strategy-report skill on the customer folder you specify.
argument-hint: "Specify the path to the customer folder containing CMDB, RVTools, DMA, or other artifacts (e.g., 'Generate a migration strategy report for Customers/Contoso')"
agent: Code Migration Modernization Agent
model: Claude Sonnet 4.7 (copilot)
---


<!-- BEGIN: action-log-contract (auto-managed by inject-action-log-contract.mjs) -->

## 📜 Action Log Contract

**After each meaningful action** in this prompt, append one single-line entry to the `## 📜 Action Log` section at the bottom of `reports/Report-Status.md`.

Canonical format:
```
- <ISO-8601-UTC> | actor=PortfolioStrategy | action=<verb-phrase> | files=<+created,~modified,-deleted> | tokens=~<bucket> | turn=<n> | notes="<free text>"
```

Rules:
- Use `actor=PortfolioStrategy` for actions taken by this prompt.
- Use `actor=User` for actions taken by the user (e.g., answering a decision).
- Log **only meaningful actions**: phase transitions, artifact production, decision events, gate passes/blocks, user inputs, rollback events. Do NOT log every internal grep or file read.
- Estimate `tokens` in buckets: `~0`, `~500`, `~2k`, `~8k`, `~30k`. The `turn` counter is exact; token estimate is best-effort. Point users to Copilot Dashboard for authoritative counts.
- If `reports/Report-Status.md` doesn't exist yet, create it from `.github/skills/migration-report-template.md` first — it already includes the `## 📜 Action Log` section.

Full spec: `.github/skills/action-log-format.md`.

<!-- END: action-log-contract -->
# Portfolio Migration Strategy Report

## What This Prompt Does

Invokes the `migration-strategy-report` skill to analyze a customer portfolio and produce a CIO-ready HTML migration deck. This is the **Portfolio Planning flow** — produces an executive plan that informs which apps to modernize via the per-app flow (`/Phase1-Plan`).

## When to Use

- A customer has shared CMDB / portfolio / inventory data and needs an executive migration plan
- A solution architect or CSA needs to scope a multi-app Azure engagement
- An RVTools, Azure Migrate, or DMA export needs to become a leadership-ready story
- Mixed artifacts (data + meeting notes + vendor proposals) need synthesis into one coherent deck

If you only need to modernize one application's code, use `/Phase0-Multi-repo-assessment` or `/Phase1-Plan` instead.

## Required Input

A **customer folder path** containing at least ONE artifact. Supported types include CMDB exports (CSV/XLSX/JSON), RVTools/vCenter/Azure Migrate exports, DMA output, meeting notes, architecture diagrams, vendor proposals, prior reports, or any structured/unstructured data.

The skill will:
1. Recursively scan the customer folder
2. Auto-detect workload pillars (Apps / DB / Infra)
3. Apply CAF-aligned deterministic classification (6 Rs + Factory/Partner/Unknown)
4. Generate a self-contained HTML deck named `{CustomerName}_Migration_Strategy_Report.html` saved into the same customer folder

## Workflow

### Step 1: Confirm Customer Folder
Ask the user: **"Which customer folder should I analyze?"** if not already provided.

**Customer data isolation is ABSOLUTE.** Once a customer folder is set:
- Read files ONLY from that exact folder path
- NEVER read from any other customer's folder — even for template/style reference
- If the customer name is ambiguous, ASK before proceeding

### Step 2: Invoke the migration-strategy-report Skill
The `migration-strategy-report` skill will own the workflow from here:
1. STEP -1: Artifact discovery (scan + classify every file)
2. STEP -0.5: Workload type auto-detection (Apps / DB / Infra)
3. STEP 0: Scope identification (Total Portfolio vs. In-Scope split)
4. STEP 1: Optional WorkIQ enrichment (if configured)
5. STEP 2: Apply deterministic classification (6 Rs + ownership)
6. STEP 3: Select slides driven by available evidence
7. STEP 4: Generate the HTML deck
8. STEP 5: Verify math, cite sources, attach disclaimers

### Step 3: Verify Output
After the skill completes, confirm:
- The HTML file was saved into the customer folder
- All classification sums match the in-scope total (math verification)
- Required disclaimers are present on the Execution Ownership slide
- No internal/meta language ("algorithm", "formula", "scenario") leaked into the output

### Step 4: Offer Follow-Up Actions
After the deck is generated, ask the user: **"Which application from the portfolio should I modernize first?"**

List the candidate applications from the deck, showing for each:
- Application name
- Current stack
- Target stack
- 6 Rs strategy
- Execution ownership (Factory / ISD-Partner / Unknown)

Once the user picks an app, write `reports/portfolio-handoff.json` per the schema defined in [## Handoff File: portfolio-handoff.json](#handoff-file-portfolio-handoffjson) below, then confirm:

> ✅ Handoff file written. Click **🚀 Modernize a single application** to start on `[App-Name]`.

Also offer:
- **Export to PDF:** `python .github/skills/migration-strategy-report/scripts/export_to_pdf.py "<path-to-html>"`
- **Iterate:** Re-run with additional artifacts or refined scope

## Prerequisites (Local Setup)

- Customer artifacts placed in a folder (any structure; recursive scan handles it)
- Optional: `Cloud Accelerate Factory - Service Descriptions.PDF` placed at workspace root (gitignored — provides verification reference for Factory/Partner classification). The skill's classification algorithm is already aligned with this document, so the PDF is optional but recommended.
- Optional: Python + Playwright installed if PDF export is needed (`pip install playwright && playwright install chromium`)

## Critical Reminders

- 💲 **Never use PowerShell to write the HTML** — it strips dollar signs from cost figures. Use the `create` or `editFiles` tool, or Python with `open()`.
- 📊 **The math must add up.** Classification counts MUST sum to the in-scope total. If they don't, recount — do NOT adjust numbers.
- 📝 **8 outstanding evidence-backed slides > 12 padded slides.** Skip slides where evidence is thin; flag gaps as findings.

## Handoff File: portfolio-handoff.json

When the user picks an application to start modernizing (Step 4), this skill writes a structured handoff file to `reports/portfolio-handoff.json` that the per-app modernization flow (`/Phase1-Plan`) reads automatically to pre-populate setup questions.

### Schema

| Field | Type | Description | Allowed values |
|---|---|---|---|
| `schema_version` | string | Schema version (currently "1.0") | "1.0" |
| `source_deck` | string | Relative path to the source HTML deck | e.g., `Customers/Contoso/Contoso_Migration_Strategy_Report.html` |
| `generated_at` | string (ISO-8601) | UTC timestamp when handoff was written | e.g., `2026-05-25T14:00:00Z` |
| `customer` | string | Customer name | free-form |
| `app.name` | string | Application name as it appears in the deck | free-form |
| `app.code_path` | string | Relative path to the application's code/repo | e.g., `Customers/Contoso/repos/order-processing` |
| `app.factory_or_partner` | string | Execution ownership classification | `Factory` \| `ISD-Partner` \| `Unknown` |
| `app.six_r_strategy` | string | CAF 6 Rs strategy | `Rehost` \| `Replatform` \| `Refactor` \| `Replace` \| `Retire` \| `Retain` |
| `app.target_platform` | string | Azure hosting platform | `App Service` \| `Container Apps` \| `AKS` |
| `app.iac_preference` | string | Infrastructure-as-Code tool | `Bicep` \| `Terraform` |
| `app.database_strategy` | string | Target Azure database service | e.g., `Azure SQL Database`, `Cosmos DB`, `Azure Database for PostgreSQL` |
| `app.current_stack` | string | Current framework/version | e.g., `.NET Framework 4.8`, `Java 8 + Spring 4.x`, `Python 2.7 + Django 1.11`, `Node.js 12 + Express 4`, `PHP 5.6 + Laravel 5`, `Ruby 2.6 + Rails 5`, `Delphi 7`, `Oracle Forms 11g` |
| `app.target_stack` | string | Target framework/version | e.g., `.NET 10 LTS`, `Spring Boot 3.x + Java 21`, `Python 3.12 + Django 5`, `Node.js 20 LTS + Express 5`, `PHP 8.3 + Laravel 11`, `Ruby 3.3 + Rails 7`, or `unchanged (rehost only)` |
| `app.criticality` | string | Business criticality from deck | `Low` \| `Medium` \| `High` \| `Critical` |
| `app.notes` | string | Free-form context to carry forward | optional |

### Example
```json
{
  "schema_version": "1.0",
  "source_deck": "Customers/Contoso/Contoso_Migration_Strategy_Report.html",
  "generated_at": "2026-05-25T14:00:00Z",
  "customer": "Contoso",
  "app": {
    "name": "OrderProcessing",
    "code_path": "Customers/Contoso/repos/order-processing",
    "factory_or_partner": "Factory",
    "six_r_strategy": "Replatform",
    "target_platform": "Container Apps",
    "iac_preference": "Bicep",
    "database_strategy": "Azure SQL Database",
    "current_stack": ".NET Framework 4.8",
    "target_stack": ".NET 10 LTS",
    "criticality": "High",
    "notes": "Pilot candidate per portfolio plan; integration with Salesforce."
  }
}
```

## Output

A self-contained HTML deck saved to the customer folder, ready for executive review. The deck includes:
- Title + Portfolio Overview (KPI cards)
- Pillar-specific slides (tech stack, EOS, infra discovery, network, DB strategy — only those with data)
- 6 Rs Strategy distribution (if apps pillar)
- Execution Ownership (Factory / ISD-Partner / Unknown)
- Phased Roadmap + Dependency Mapping + Move Groups
- Risks & Dependencies + Recommended Next Steps + Appendix Statistics

See [.github/skills/migration-strategy-report/SKILL.md](../skills/migration-strategy-report/SKILL.md) for full skill workflow.

## Next Steps

When the Portfolio Strategy Report is complete:

1. ✅ Update `reports/Report-Status.md` to mark **Portfolio Strategy** as complete.
2. 📊 The skill writes `reports/portfolio-handoff.json` capturing the pilot application's planned target stack, hosting platform, database strategy, and IaC choice.
3. ▶️ Output the following Next Steps block to the user:

   > **Next Steps**
   >
   > For a **multi-repo deep assessment** of the portfolio, run **`/Phase0-Multi-repo-assessment`**.
   >
   > For a **single-app modernization** starting with the pilot, run **`/Phase1-Plan`** — it automatically reads `portfolio-handoff.json` to pre-fill setup choices.
   >
   > Or click **🚀 Modernize a single application** / **🗂️ Run multi-repo assessment** if the handoff buttons are visible in your UI.
