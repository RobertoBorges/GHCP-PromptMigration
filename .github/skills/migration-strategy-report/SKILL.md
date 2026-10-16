---
name: migration-strategy-report
description: |
  Generate an executive-ready Migration Strategy Report (HTML deck) from a customer portfolio — CMDB exports, RVTools/Azure Migrate inventories, DMA outputs, vendor proposals, architecture diagrams.
  **Use when:** producing a CIO-ready migration plan for a customer portfolio (apps, databases, infra, or any mix). Starts the Portfolio Planning flow for multi-app engagements.
  **Triggers:** "generate migration report", "analyze CMDB", "portfolio analysis", "migration strategy report for X", "RVTools export analysis", "Azure Migrate analysis", "portfolio assessment", "build a deck from these artifacts".
  **Covers:** workload detection, evidence-backed 6 Rs and ownership, per-pillar reconciliation, validation audits, financial provenance, dependency evidence, resumable HTML generation, optional bilingual reports and execution packages.
argument-hint: "Path to the customer folder (e.g., 'generate migration strategy report for Customers/Contoso')"
user-invocable: false
---

# Migration Strategy Report — Skill

Generate executive-ready Migration Strategy Reports (self-contained HTML decks) from any customer portfolio artifacts. Adapts to **Applications, Infrastructure, Databases, or any combination**. The slide selection is data-driven — evidence determines depth.

---

## 🔒 CRITICAL RULES (NO EXCEPTIONS)

These rules ALWAYS apply when this skill is active. They are absolute. Violating them is a serious engagement failure.

### 1. Excel Sheet Completeness
- When loading Excel files, **list ALL sheet names first** and load every sheet that contains data.
- Do NOT assume single-sheet workbooks — always check `sheetnames` programmatically before loading.
- Empty sheets (0 data rows) or legend/reference sheets can be skipped, but must be explicitly checked and documented in console output.
- Sheets with partial data (few non-null columns) should be examined and included if they contain any unique information not available in other sheets.

### 2. Customer Folder Convention (Per-Invocation)
- The skill does NOT hard-code a `Customers/` path. The user provides the folder path each invocation (e.g., `generate migration strategy report for /path/to/Customer/Contoso`).
- If the user does not specify a path, **ASK** before scanning anything.
- The customer folder must contain at least ONE meaningful artifact (CMDB CSV, RVTools XLSX, DMA JSON, meeting notes, etc.).

### 3. Determinism Guarantee
- All classification algorithms (6 Rs, Microsoft / Partner / Unknown) MUST produce identical results for identical inputs. See [references/classification-algorithm.md](references/classification-algorithm.md). No subjective judgment in counts.
- Verification is mandatory: classification counts MUST sum to the in-scope total. Show the math.

### 4. Evidence and Delivery Gates
- Always load [references/reporting-quality.md](references/reporting-quality.md). Complete preflight before analysis; append the real validation evidence to the run audit at every stage.
- Compute counts from classified source records and explicit joins, never plausible percentages or subtraction-derived residuals.
- Keep applications, database instances, databases, and VMs as separate units. Never add unlike units into a migration count.
- Recommendations are not architecture decisions. Keep unapproved targets provisional; user-owned decision gates still apply before execution.
- Do not declare success when required evidence or output validation failed. Report `READY`, `CONDITIONAL`, `BLOCKED`, or `FAILED` with the reason.

---

## When to Use This Skill

Use this skill when:
- A customer has shared CMDB/portfolio data and needs an executive migration plan.
- A solution architect or CSA needs to scope a multi-app Azure migration engagement.
- An RVTools, Azure Migrate, or DMA export needs to become a leadership-ready story.
- Mixed artifacts (data + meeting notes + vendor proposals) need synthesis into one coherent deck.
- A prior strategy report needs updating with new artifacts (incremental iteration).

Do NOT use this skill for:
- Per-application code modernization → use the Modernize an App flow (`/phase1-plan` for single apps, `/phase0-multi-repo-assessment` for multi-repo business solutions).
- Data migration execution → refer to Azure Database Migration Service.
- Binary scanning → refer to stack-appropriate external assessment tools. Supplied source/configuration and dependency telemetry can be analyzed using [references/dependency-evidence.md](references/dependency-evidence.md); static findings are not proof of runtime connectivity.

---

## Workflow Overview

```
STEP -1  Preflight & Discovery    → validate path, snapshot inputs, manifest all files/sheets
STEP -0.5 Workload Detection      → auto-detect Apps / DB / Infra pillars
STEP 0   Scope Identification     → split Total Portfolio vs. In-Scope
STEP 1   Optional WorkIQ Query    → enrich with meeting context
STEP 2   Apply Classification     → computed record model, 6 Rs + ownership, confidence
STEP 3   Select Slides            → evidence-driven, per detected pillar
STEP 4   Generate Incrementally   → runnable skeleton, small batches, optional translations
STEP 5   Verify & Cite            → per-pillar reconciliation, citations, final audit verdict
OPTIONAL Execution Package       → validated JSON, PPTX and blocker/action workbook
```

---

## STEP -1: Artifact Discovery (MANDATORY FIRST STEP)

Before generating ANY report:

1. **Validate the path and snapshot inputs** before writing outputs. Follow the accessibility, workbook-manifest, exclusion, and conflicting-source gates in [reporting-quality.md](references/reporting-quality.md). Create the audit with preflight results; a failed preflight is `BLOCKED`, not a completed report.
2. **Classify each artifact** by type (data export, narrative, visual, assessment, vendor doc, etc.).
3. **Read and analyze** each relevant file to extract:
   - Quantitative data (counts, scores, percentages, sizes)
   - Qualitative insights (decisions, risks, constraints, stakeholder positions)
   - Temporal information (timelines, deadlines, phase assignments)
   - Organizational context (owners, teams, vendors, governance)
4. **Detect workload types** (see STEP -0.5).
5. **Identify data density** — which slides have strong evidence vs. which would be speculative.
6. **Determine the optimal slide set** — see [references/slides-common.md](references/slides-common.md) for the cross-pillar slide catalog.
7. **Detect dependency evidence** from schemas and supplied first-party source/configuration, not filenames alone. If present, load [dependency-evidence.md](references/dependency-evidence.md) and record external/source/hybrid coverage.
8. **Append discovery validation** to the audit: input and sheet manifests, detected pillars, source language, and every candidate slide's inclusion/exclusion reason.

### Supported Artifact Types
The skill works with **any** of these — none are required:
- CMDB / portfolio exports (CSV, Excel, JSON)
- Infrastructure exports (RVTools, Azure Migrate, vCenter, SCCM, Movere)
- Database assessments (DMA, MAP Toolkit, Azure Migrate DB, custom inventories)
- Network topology (Visio, firewall exports, IPAM, NSG exports)
- Storage inventory (SAN/NAS reports, disk utilization)
- Identity / AD exports (forest diagrams, ADFS config, GPO reports)
- Meeting notes / transcripts (.md, .docx, .txt, .pdf)
- Architecture documents (diagrams, .drawio, .pptx)
- Assessment reports (AppCAT, CAST, custom)
- Vendor proposals / SOWs (.pdf, .docx)
- Business cases / strategy docs (.pptx, .docx, .md)
- Prior reports / decks (.html, .pptx, .pdf)

Detailed field-level references per pillar:
- Applications → [references/slides-application-pillar.md](references/slides-application-pillar.md) (Application Input Fields section)
- Databases → [references/slides-database-pillar.md](references/slides-database-pillar.md) (Database Input Fields section)
- Infrastructure → [references/slides-infrastructure-pillar.md](references/slides-infrastructure-pillar.md) (Infrastructure + Network/Storage/Identity Input Fields sections)

---

## STEP -0.5: Workload Type Detection (AUTO-DETECT)

Classify the portfolio into one or more pillars from column headers and file content. The report dynamically adapts.

| Pillar | Detected When | Report Title |
|---|---|---|
| **Applications** | Columns: Application Name, Business Capability, Criticality, Architecture Tier, Tech Stack | "Application Portfolio Migration Strategy" |
| **Infrastructure** | Columns: VM Name, vCPU, RAM, Disk, Cluster, Hypervisor, Powered On; OR file names containing "RVTools", "vInfo", "Azure Migrate" | "Infrastructure Migration Strategy" |
| **Databases** | Columns: DB Instance, DB Engine, DB Size, Stored Procedures, HA Config, Migration Readiness; OR DMA output files | "Database Migration Strategy" |
| **Mixed (2+)** | Multiple pillar signals detected | "Enterprise Migration Strategy" (or most-inclusive applicable title) |

Detection heuristics:
- RVTools tabs (vInfo, vCPU, vMemory, vDisk, vNetwork) → **Infrastructure** (always)
- DMA JSON/CSV output → **Databases** (always)
- A single dataset can trigger MULTIPLE pillars (e.g., CMDB with app + server + DB fields activates all three)

**Detection is automatic — never ask the user what type of data they have.**

### Pillar → Reference File Loading

Load reference files based on detected pillars:

| Detected | Load These References |
|---|---|
| **Always** | [classification-algorithm.md](references/classification-algorithm.md), [slides-common.md](references/slides-common.md), [reporting-quality.md](references/reporting-quality.md) |
| Applications | [slides-application-pillar.md](references/slides-application-pillar.md) |
| Databases | [slides-database-pillar.md](references/slides-database-pillar.md) |
| Infrastructure | [slides-infrastructure-pillar.md](references/slides-infrastructure-pillar.md) |
| Mixed | Load all relevant pillar files + run classification independently per pillar, then combine |
| **At generation time** | [style-guide.md](references/style-guide.md) |
| Dependency evidence or supplied customer source | [dependency-evidence.md](references/dependency-evidence.md) |
| Optional bilingual output or execution package | [delivery-options.md](references/delivery-options.md) |

---

## STEP 0: Scope Identification (WHEN PORTFOLIO DATA EXISTS)

If portfolio data is available, ALWAYS split:

### For Application Data
1. **Total Portfolio** = all unique apps in the CMDB dataset.
2. **In-Scope for Migration** = apps with an assigned Proposed Modernization Phase OR Pilot Flag = Yes.
3. **Out of Scope** = apps with no phase assigned AND no pilot flag (Retain as-is, not actively migrating).

### For Infrastructure Data
1. **Total Servers/VMs** = all unique VMs/servers in the inventory.
2. **Powered-On vs Powered-Off** = active vs inactive VMs (powered-off are retire candidates).
3. **In-Scope for Migration** = VMs with an assigned wave/phase OR in production environment.
4. **Physical vs Virtual split** = physical servers need P2V before cloud migration.
5. **Environment split** = Prod / Dev / Test / DR — different migration priorities.

### For Database Data
1. **Total DB Instances** = all unique database instances.
2. **Total Databases** = sum of databases across instances.
3. **Total Data Volume** = aggregate size (TB).
4. **In-Scope for Migration** = instances with assigned target service or migration phase.
5. **Shared vs Dedicated** = databases serving multiple apps vs single-app databases.

**Reporting rule:** Always report BOTH numbers prominently. The Microsoft/Partner/Unknown split and 6 Rs distribution apply ONLY to In-Scope.

**Never conflate total portfolio with in-scope. Always show both.**

State the execution unit beside every KPI: applications, VMs/servers, DB instances, or individual databases. A DB-hosting VM is a subset of the VM inventory, not an additional VM. Count a host as removed for a PaaS option only when every hosted workload is accounted for and the host-retirement decision is evidenced; otherwise its future is unresolved.

---

## STEP 1: WorkIQ Enrichment (OPTIONAL, IF CONFIGURED)

If WorkIQ is configured and the customer has meeting history, query BEFORE generating:

1. *"What meeting notes exist for [CUSTOMER] related to migration or modernization?"*
2. *"What decisions or blockers were discussed for [CUSTOMER] applications?"*
3. *"What vendor timelines or commitments were shared for [CUSTOMER]?"*
4. *"What stakeholder concerns or priorities were raised for [CUSTOMER]?"*
5. *"What discovery findings or workshop outcomes exist for [CUSTOMER]?"*

| Finding Type | Incorporate Into |
|---|---|
| Decisions made in meetings | Next Steps slide (mark as "Decided"), Phase assignments |
| Blockers discussed | Risk cards (with meeting date as evidence) |
| Vendor timelines shared | Phased Roadmap, Execution Ownership |
| Stakeholder concerns | Risk cards, Success Factors |
| Technical constraints mentioned | Obsolescence Assessment, Modernization Tracks |
| Scope changes or exclusions | Scope Identification, Portfolio Overview KPIs |
| Budget/resource constraints | Risks, Recommended Next Steps |

**Citation rule:** When using WorkIQ-sourced information, cite it: *"Per [CUSTOMER] migration workshop (DATE)..."* or *"As discussed in stakeholder review (DATE)..."*.

---

## STEP 2: Apply Classification

All classification logic lives in [references/classification-algorithm.md](references/classification-algorithm.md). It is deterministic, priority-ordered, and CAF-aligned.

- **6 Rs (Strategy)**: Retire → Retain → Replace → Refactor → Replatform → Rehost
- **Execution Ownership (per pillar)**: Microsoft / Partner / Unknown / (Apps only) No Migration Needed
- **Mixed portfolios**: Run each pillar independently and show separate reconciled totals. Do not combine unlike units into a donut or migration grand total.

**Source document:** the references use Migration Service Descriptions, May 2026 as their baseline. Verify the applicable service-description version and scope before confirming commercial eligibility. Record title, version/date, section, and any override in the audit; absent proof means provisional/Unknown, not confirmed Microsoft scope. Never silently rewrite packaged rules from a customer attachment.

Create `_work/Report_Data.json` using the contract in [reporting-quality.md](references/reporting-quality.md), then run the bundled `scripts/report_data.py` validator. Use its computed per-pillar summary in every output. Preserve classified IDs, source row references, rule, rationale, confidence, and unresolved joins; the validator checks the model, not the truth of the source assessment.

---

## STEP 3: Select Slides (Evidence-Driven)

| Slide | Include If | Skip If |
|---|---|---|
| Title | Always | Never |
| Portfolio Overview (KPIs) | Always — adapts to pillars | Never |
| Tech Stack Landscape | Apps pillar + technology data with counts | Apps pillar missing |
| Obsolescence Assessment | Version/EOL data available | No version info |
| EOS Impact & ESU Strategy | EOS OS/DB/middleware data | No EOS info |
| Infrastructure Discovery & Sizing | Infra pillar + VM data with CPU/RAM/disk | No infra data |
| Network & Landing Zone | Network/identity data | No network data |
| Database Migration Strategy | DB pillar + DB inventory with engine/version/size | No DB data |
| 6 Rs Strategy | Apps pillar + ≥10 classifiable apps | Infra-only / DB-only (use 5b + 4e instead) |
| Execution Ownership (Microsoft/Partner) | Any pillar with ownership signals | No ownership clarity AND no VM inventory |
| Phased Roadmap | Phase assignments or timeline data | No temporal data |
| Dependency Mapping | Integration data OR architecture maps OR middleware refs OR cross-pillar links | No dependency signals |
| Move Group Recommendations | Integration data + ≥2 of: shared-DB, capability, criticality, phase, infra | Flat app list with no relationship data |
| Business Capability Grouping | Business function mapping exists | Pure infra view |
| Phase 1 Pilot Detail | Pilot candidates identified | No pilot decisions |
| Modernization Tracks | Tech stack diversity warrants it | Single-tech portfolio |
| Risks & Dependencies | Always | Never |
| Next Steps | Always | Never |
| Appendix Statistics | Quantitative data exists | Pure qualitative report |

**Key Principle:** 8 outstanding evidence-backed slides > 12 padded slides. Leadership values precision over volume.

**Synthesis approach:**
- When multiple artifacts overlap, cross-reference and reconcile.
- When artifacts conflict, establish precedence from verified content/version dates or an explicit user choice. If authority is unresolved, record the blocker and ask; do not silently pick a file by its filename or filesystem modification time.
- When data is thin for a slide, either skip it OR explicitly flag gaps as findings (gaps ARE findings).

---

## STEP 4: Generate the HTML Deck

Output format and styling rules are in [references/style-guide.md](references/style-guide.md).

### Output File Naming
- Default: `{CustomerName}_Migration_Strategy_Report.html`
- Save into the customer folder (same place the inputs live)
- For iterations, append timestamp: `{CustomerName}_Migration_Strategy_Report_{YYYYMMDD}.html`

### Checkpoint-First Generation
1. Write a runnable generator into the customer folder's `_work/` directory. Load the bundled scaffold CSS, emit the cover with an **INCOMPLETE** indicator, and run it immediately.
2. Add at most three slides per batch, rerun after each batch, and report the slide count and on-disk path. Keep classification in `Report_Data.json`, not duplicated constants in slide code.
3. Checkpoint the completed slide IDs, input snapshot, language options, and outstanding checks in the audit. Resume from that state after interruption; do not start over or treat a partial deck as delivered.
4. Complete the required slides and checks before removing the incomplete indicator. Always put Data Sources and Data Quality last.

### Optional Delivery Modes
Use [delivery-options.md](references/delivery-options.md) for bilingual/localized output and the execution package. Default is one HTML deck in the agreed report language. Do not silently add mandatory translations or Office dependencies.

### CRITICAL: Never Use PowerShell to Write the HTML
PowerShell heredocs (`@"..."@`) treat `$` as variable references and silently strip all dollar signs (e.g., `$702K/mo` becomes `/mo`). This corrupts cost figures.

**Safe methods:**
- Use the `create` or `editFiles` tool (default and recommended)
- If you must script it, use Python: `open(path, 'w', encoding='utf-8')`

If dollar signs are accidentally stripped, [`scripts/export_to_pdf.py`](scripts/export_to_pdf.py) auto-detects and repairs the damage on its next run (see `validate_and_fix_dollars()`).

### Optional: Export to PDF
After generating the HTML, optionally produce a PDF:
```bash
pip install playwright
playwright install chromium
python .github/skills/migration-strategy-report/scripts/export_to_pdf.py "<path-to>/<CustomerName>_Migration_Strategy_Report.html"
```

---

## STEP 5: Verify & Cite

Before declaring the report complete:

### Mandatory Math Checks
- 6 Rs sum: `Retire + Retain + Replace + Refactor + Replatform + Rehost = In-Scope total`
- App ownership sum: `Microsoft + Partner + No Migration Needed + Unknown = In-Scope total` (per pillar)
- DB ownership sum: `Microsoft + Partner + Unknown = DB In-Scope total`
- Infra ownership sum: `Microsoft + Partner + Unknown = Infra In-Scope total`
- Mixed portfolios: each pillar reconciles independently; show no combined migration grand total
- **If the math doesn't add up, recount. Do NOT adjust numbers to force a total.**

### Evidence and Output Checks
- Re-run `scripts/report_data.py`; compare every repeated KPI to the same computed summary.
- Verify each ownership row has evidence, confidence, rationale, and a rule reference. Keep COTS vendors distinguishable inside Partner.
- Every cost/savings figure needs a source, calculation, assumptions, currency, pricing date/region/term; use `TBD - financial model pending` when inputs are absent.
- Verify source-file/sheet coverage, dependency limitations, all applicable slides, last-slide data quality, offline HTML, locale formatting, and interrupted-run status using [reporting-quality.md](references/reporting-quality.md).
- Append actual validation results and the final verdict to the audit. Log meaningful stage transitions and artifact production to `reports/Report-Status.md` using the [Action Log contract](../migration-artifacts/references/action-log-format.md).

### Required Disclaimers (ALWAYS include)
1. **Execution Ownership slide:** *"This classification is based on currently available CMDB data. Workloads may move between buckets (Microsoft, Partner, or Unknown) as further discovery and assessment activities provide additional clarity."*
2. **Assessment Tooling Gap:** State which compatibility tools were actually run, their scope and date, and which readiness claims remain inferred. Do not infer that a language has no tooling or add an unexplained fixed effort buffer.

### Citation
Cite the governing scope document concisely on the ownership slide and cite quantitative claims where they appear. Keep version comparisons, row-level calculations, and detailed execution traces in the audit. The report is a deliverable, not a changelog.

---

## Infrastructure Migration Options (Always Present When Infra Detected)

When the data is primarily infrastructure-focused, always evaluate and present these three paths:

| Option | When to Recommend | Key Value |
|---|---|---|
| **Azure IaaS VMs (Lift & Shift)** | Evidence supports like-for-like migration and the customer chooses it | Granular control, Azure-native monitoring, path to PaaS modernization |
| **Azure VMware Solution (AVS)** | VMware estates; large VM counts; operational continuity priority | vMotion-native migration, minimal change, fastest time-to-cloud |
| **Azure Arc (Hybrid Management)** | VMs that CANNOT move (regulatory, latency, data sovereignty, vendor lock-in); phased migrations where some stay on-prem | Unified management plane, Azure Policy from on-prem, bridge to full migration |

### Always Include Azure Arc as an Option When ANY Apply
- Regulatory/compliance constraints prevent leaving on-premises
- Data sovereignty requirements mandate geographic residency that Azure regions don't satisfy
- Latency-sensitive workloads (<1ms requirements)
- Vendor-locked applications requiring vendor cooperation
- Phased migration where some VMs stay on-prem for 6–18 months
- Edge/branch locations that will persist after data center exit
- Workloads with hardware dependencies (HSMs, specialized I/O, physical security)

Present Azure Arc as **"Option: Hybrid Management"** alongside primary options — a governance bridge, NOT a competing alternative.

---

## Iteration Pattern

When a user asks to update an existing report:
1. Read the existing `{CustomerName}_Migration_Strategy_Report.html` from the customer folder.
2. Identify what's new (new artifacts, updated counts, new decisions).
3. Re-run only the affected slides (preserve deterministic counts if input data didn't change).
4. Save as `{CustomerName}_Migration_Strategy_Report_{YYYYMMDD}.html` and keep the prior version.
5. Use a unique run timestamp when an output name already exists. Compare the new input manifest to the prior run; exclude prior generated outputs from raw input analytics, retaining them only as explicitly marked historical context.

---

## Quick Reference: Trigger Phrases

- "generate migration report"
- "analyze CMDB"
- "create portfolio analysis"
- "migration strategy report for [CUSTOMER]"
- "analyze application portfolio"
- "create migration deck"
- "analyze what's in this folder"
- "build a deck from these artifacts"
- "create LT-ready report from available data"
- "analyze project folder and generate report"
- "analyze infrastructure for migration"
- "database migration strategy"
- "analyze RVTools export"
- "server migration report"
- "infra migration deck"
- "analyze Azure Migrate data"
- "database portfolio assessment"

---

---

## Step 6: Write Portfolio Handoff File (for per-app execution bridge)

After the deck is delivered AND verified, ask the user:

> **Which application from this portfolio should be modernized first?**

List the candidate applications with their key attributes from the deck:
- Name
- Current stack → Target stack
- 6 Rs strategy
- Microsoft / Partner / Unknown ownership
- Criticality

Once the user picks an application, write `reports/portfolio-handoff.json` with the full schema (defined in [.github/skills/portfolio-strategy/SKILL.md](../portfolio-strategy/SKILL.md#handoff-file-portfolio-handoffjson)).

**Schema summary** (must match the canonical spec in the `/portfolio-strategy` skill):
- `schema_version`: "1.0"
- `source_deck`: path to the HTML deck
- `generated_at`: ISO-8601 UTC timestamp
- `customer`: customer name
- `app.name`, `app.code_path`, `app.execution_ownership`, `app.six_r_strategy`, `app.target_platform`, `app.iac_preference`, `app.database_strategy`, `app.current_stack`, `app.target_stack`, `app.criticality`, `app.notes`

**How to write the file:**
Use Python (NOT PowerShell — PS strips dollar signs):
```python
import json, datetime
handoff = {
    "schema_version": "1.0",
    "source_deck": "Customers/Contoso/Contoso_Migration_Strategy_Report.html",
    "generated_at": datetime.datetime.utcnow().isoformat() + "Z",
    "customer": "Contoso",
    "app": {
        "name": "OrderProcessing",
        "code_path": "Customers/Contoso/repos/order-processing",
        "execution_ownership": "Microsoft",
        "six_r_strategy": "Replatform",
        "target_platform": "Container Apps",
        "iac_preference": "Bicep",
        "database_strategy": "Azure SQL Database",
        "current_stack": ".NET Framework 4.8",
        "target_stack": ".NET 10 LTS",
        "criticality": "High",
        "notes": "Pilot candidate per portfolio plan."
    }
}
with open("reports/portfolio-handoff.json", "w") as f:
    json.dump(handoff, f, indent=2)
```

Or use the `create`/`editFiles` tool.

After writing, surface a clickable next-step:
> ✅ Handoff written to `reports/portfolio-handoff.json`. Click **🚀 Modernize a single application** to start on `<App.Name>`.

If the user wants to pick MULTIPLE apps for a multi-app modernization wave, write one handoff file per app, e.g., `reports/portfolio-handoff-<AppName>.json`, and inform the user that `/phase1-plan` reads `reports/portfolio-handoff.json` by default (so they'll need to rename or copy when switching apps).

## Reference material

- Classification rules → [references/classification-algorithm.md](references/classification-algorithm.md)
- Cross-pillar slides → [references/slides-common.md](references/slides-common.md)
- Application slides → [references/slides-application-pillar.md](references/slides-application-pillar.md)
- Database slides → [references/slides-database-pillar.md](references/slides-database-pillar.md)
- Infrastructure slides → [references/slides-infrastructure-pillar.md](references/slides-infrastructure-pillar.md)
- HTML/CSS/output rules → [references/style-guide.md](references/style-guide.md)
- Validation, evidence model and audit → [references/reporting-quality.md](references/reporting-quality.md)
- Source/runtime dependency evidence → [references/dependency-evidence.md](references/dependency-evidence.md)
- Language and optional execution package → [references/delivery-options.md](references/delivery-options.md)
- PowerPoint generation → [references/pptx-generation.md](references/pptx-generation.md) — Uses the bundled package renderer; no external corporate template is required.
- Scripts → [scripts/export_to_pdf.py](scripts/export_to_pdf.py)

## HTML report scaffold

The executive deck is generated from this scaffold. Read the README before editing any generated HTML.

| Use when | File |
|---|---|
| Building or regenerating the executive HTML deck | [`README.md`](./templates/html-report-scaffold/README.md) |
| Adjusting deck styling (edit the scaffold, never the generated output) | [`style.css`](./templates/html-report-scaffold/assets/style.css) |
