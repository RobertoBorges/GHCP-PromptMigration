# Migration Strategy Report Skill

This skill generates **executive-ready Migration Strategy Reports** (self-contained HTML decks) from any customer portfolio artifacts — CMDB exports, RVTools dumps, Azure Migrate assessments, DMA outputs, meeting notes, vendor proposals, architecture diagrams, or any mix.

The skill is invoked by:
- The `/portfolio-strategy` slash command (see [.github/skills/portfolio-strategy/SKILL.md](../../skills/portfolio-strategy/SKILL.md))
- Trigger phrases like *"generate migration report"*, *"analyze CMDB"*, *"migration strategy report for [CUSTOMER]"*
- The `Code Migration Modernization Agent` handoff for portfolio planning

## Quick Start

```
# 1. Place customer artifacts in a folder (anywhere — typically Customers/<CustomerName>/)
Customers/Contoso/
├── cmdb_export.xlsx
├── rvtools_export.xlsx
├── dma_assessment.json
├── meeting_notes.md
└── architecture_diagram.png

# 2. In VS Code Chat:
/portfolio-strategy Generate a migration strategy report for Customers/Contoso

# 3. Outputs saved to the customer folder:
Customers/Contoso/Contoso_Migration_Strategy_Report.html
Customers/Contoso/Validation_Audit_<run-id>.md

# 4. (Optional) Export to PDF:
pip install playwright; playwright install chromium
python .github/skills/migration-strategy-report/scripts/export_to_pdf.py "Customers/Contoso/Contoso_Migration_Strategy_Report.html"
```

## Folder Structure

```
.github/skills/migration-strategy-report/
├── SKILL.md                                  # Skill definition (frontmatter + critical rules + workflow)
├── README.md                                 # This file (human-facing)
├── references/                               # Pillar-based reference files (progressive loading)
│   ├── classification-algorithm.md           # 6 Rs + Microsoft/Partner/Unknown rules (always loaded)
│   ├── slides-common.md                      # Cross-pillar slides (1, 2, 5b, 6, 6b, 6c, 10, 11, 12) (always loaded)
│   ├── slides-application-pillar.md          # Apps slides (3, 4, 5, 7, 8, 9) — loads if apps detected
│   ├── slides-database-pillar.md             # DB slides (4b DB portion, 4e) + target matrix — loads if DB detected
│   ├── slides-infrastructure-pillar.md       # Infra slides (4b infra, 4c, 4d) — loads if infra detected
│   ├── reporting-quality.md                 # Preflight, stage gates, evidence contract, financial safeguards
│   ├── dependency-evidence.md               # Source/runtime evidence, coverage and SME disposition
│   ├── delivery-options.md                  # Optional locales, execution summary and action workbook
│   └── style-guide.md                        # HTML/CSS/branding rules (loads at generation time)
└── scripts/
    ├── export_to_pdf.py                      # HTML → PDF via Playwright/Chromium
    ├── report_data.py                        # Standard-library model validator and per-pillar summaries
    ├── delivery_package.py                   # Optional PPTX/XLSX/JSON renderer with saved-file checks
    └── requirements-delivery.txt             # Optional Office rendering dependencies
```

## Prerequisites

| Requirement | Why |
|---|---|
| At least one artifact in the customer folder | Skill needs SOMETHING to analyze (data, narrative, visual, anything) |
| Customer/organization name | Used in titles, output filenames, classification context; can be inferred from folder name |
| (Optional) `Migration Service Descriptions.PDF` at workspace root | Verification reference for Microsoft/Partner classification. Gitignored. The skill's algorithm is already aligned with this document, so the PDF is optional but recommended. |
| (Optional) Python 3.8+ + Playwright | Only needed if exporting to PDF |
| (Optional) WorkIQ configuration | Enriches reports with meeting context, decisions, blockers, vendor commitments |

## How the Skill Works

1. **Artifact Discovery** — recursively scans the customer folder, classifies every file by type
2. **Workload Detection** — auto-detects which pillars are present: Applications, Databases, Infrastructure, or any combination
3. **Scope Identification** — splits Total Portfolio vs. In-Scope (the In-Scope number drives all classification math)
4. **WorkIQ Enrichment** (if configured) — pulls meeting context to enrich risks, decisions, vendor timelines
5. **Classification** — applies deterministic, priority-ordered algorithms:
   - 6 Rs Strategy (Retire → Retain → Replace → Refactor → Replatform → Rehost)
   - Execution Ownership per pillar (Microsoft / Partner / Unknown; Apps also has "No Migration Needed")
6. **Slide Selection** — evidence-driven; skips slides without strong data support
7. **HTML Generation** — produces a self-contained HTML deck with inline CSS, KPI cards, charts, callouts
8. **Verification** — separate per-pillar reconciliation, inline citations, financial provenance, output checks and a persistent audit with READY/CONDITIONAL/BLOCKED/FAILED verdict

Preflight inventories all inputs and workbook sheets before analysis. Unreadable files need repair or explicit exclusion; conflicting source authority is a blocker. Counts are computed from classified records and explicit joins, not estimates. A runnable partial deck is saved early and regenerated in small batches; it remains marked incomplete until required checks pass.

## Optional Execution Package

Use the same classified `Report_Data.json` for the report and execution package:

```powershell
python .github/skills/migration-strategy-report/scripts/report_data.py "<customer>\_work\<run-id>\Report_Data.json"
# Install optional dependencies only when enabling Office output:
python -m pip install -r .github/skills/migration-strategy-report/scripts/requirements-delivery.txt
python .github/skills/migration-strategy-report/scripts/delivery_package.py "<customer>\_work\<run-id>\Report_Data.json" --output "<customer>\DeliveryPackage\<run-id>"
```

The package includes a four-slide execution summary, an XLSX workbook containing open questions/blockers/full scoped inventory, and JSON traceability/validation results. Saved Office artifacts are reopened and checked. Output directories must be new; unresolved scope, questions, blockers, or unassigned migrations remain CONDITIONAL. No corporate presentation template is needed.

The record contract and limitations are in [reporting-quality.md](references/reporting-quality.md); optional bilingual generation and locale formatting are in [delivery-options.md](references/delivery-options.md). The validator checks the normalized model, not source truth or HTML layout. Source-code analysis records coverage, occurrence-level evidence, and technical/functional SME needs without claiming static references prove runtime traffic.

## Output Quality Rules (Executive Presentation)

Generated reports follow strict executive rules:
- **No implementation chatter** — keep detailed execution traces in the audit; show concise financial calculations and understandable migration options in the deck
- **No zero-count items** — platforms/categories with 0 occurrences are omitted
- **Executive tone** — "Classification Note" not "Disclaimer", "Microsoft Scope Opportunity" not "Impact Analysis"
- **Deterministic** — same inputs produce identical classification numbers every time
- **Inline evidence** — governing scope reference on ownership slides and source/derivation beside quantitative claims
- **Distinct units** — no applications + DB instances + VMs migration grand total
- **Honest qualifications** — technical compatibility is not commercial scope or architecture approval; missing financial inputs stay TBD

## Critical Rules

💲 **Never use PowerShell to write the HTML** — PowerShell heredocs (`@"..."@`) strip dollar signs from cost figures (`$702K/mo` becomes `/mo`). Use the `create` / `editFiles` tool or Python `open(path, 'w', encoding='utf-8')`. If `$` signs are accidentally stripped, `scripts/export_to_pdf.py` auto-detects and repairs them on its next run.

📊 **Math must add up** — classification counts MUST sum to the in-scope total. If they don't, recount — do NOT adjust numbers.

📝 **8 outstanding evidence-backed slides > 12 padded slides** — leadership values precision over volume

## Pillar Reference Loading

The skill is designed for progressive loading. Reference files are organized so only the pillars actually present in the data get loaded:

| Detected Pillar | Reference Files Loaded |
|---|---|
| Always | `references/classification-algorithm.md`, `references/slides-common.md`, `references/reporting-quality.md`, `references/style-guide.md` (at generation time) |
| Applications | + `migration-strategy-report/references/slides-application-pillar.md` |
| Databases | + `migration-strategy-report/references/slides-database-pillar.md` |
| Infrastructure | + `migration-strategy-report/references/slides-infrastructure-pillar.md` |
| Source/runtime dependency evidence | + `references/dependency-evidence.md` |
| Optional languages or execution package | + `references/delivery-options.md` |

This keeps the active context window lean even though the full skill has substantial domain content.

## Related

- Skill definition → [SKILL.md](SKILL.md)
- Slash command → [.github/skills/portfolio-strategy/SKILL.md](../../skills/portfolio-strategy/SKILL.md)
- Context injection hook → [.github/hooks/scripts/load-migration-state.ps1](../../hooks/scripts/load-migration-state.ps1)
- Per-app modernization → [.github/skills/phase1-plan/SKILL.md](../../skills/phase1-plan/SKILL.md)
