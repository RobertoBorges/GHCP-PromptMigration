# Migration Strategy Report Skill

This skill generates **executive-ready Migration Strategy Reports** (self-contained HTML decks) from any customer portfolio artifacts — CMDB exports, RVTools dumps, Azure Migrate assessments, DMA outputs, meeting notes, vendor proposals, architecture diagrams, or any mix.

The skill is invoked by:
- The `/PortfolioStrategy` slash command (see [.github/prompts/PortfolioStrategy.prompt.md](../../prompts/PortfolioStrategy.prompt.md))
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
/PortfolioStrategy Generate a migration strategy report for Customers/Contoso

# 3. Output saved to the customer folder:
Customers/Contoso/Contoso_Migration_Strategy_Report.html

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
│   ├── classification-algorithm.md           # 6 Rs + Factory/Partner/Unknown rules (always loaded)
│   ├── slides-common.md                      # Cross-pillar slides (1, 2, 5b, 6, 6b, 6c, 10, 11, 12) (always loaded)
│   ├── slides-application-pillar.md          # Apps slides (3, 4, 5, 7, 8, 9) — loads if apps detected
│   ├── slides-database-pillar.md             # DB slides (4b DB portion, 4e) + target matrix — loads if DB detected
│   ├── slides-infrastructure-pillar.md       # Infra slides (4b infra, 4c, 4d) — loads if infra detected
│   └── style-guide.md                        # HTML/CSS/branding rules (loads at generation time)
└── scripts/
    └── export_to_pdf.py                      # HTML → PDF via Playwright/Chromium (auto-repairs missing $ signs)
```

## Prerequisites

| Requirement | Why |
|---|---|
| At least one artifact in the customer folder | Skill needs SOMETHING to analyze (data, narrative, visual, anything) |
| Customer/organization name | Used in titles, output filenames, classification context; can be inferred from folder name |
| (Optional) `Cloud Accelerate Factory - Service Descriptions.PDF` at workspace root | Verification reference for Factory/Partner classification. Gitignored. The skill's algorithm is already aligned with this document, so the PDF is optional but recommended. |
| (Optional) Python 3.8+ + Playwright | Only needed if exporting to PDF |
| (Optional) WorkIQ configuration | Enriches reports with meeting context, decisions, blockers, vendor commitments |

## How the Skill Works

1. **Artifact Discovery** — recursively scans the customer folder, classifies every file by type
2. **Workload Detection** — auto-detects which pillars are present: Applications, Databases, Infrastructure, or any combination
3. **Scope Identification** — splits Total Portfolio vs. In-Scope (the In-Scope number drives all classification math)
4. **WorkIQ Enrichment** (if configured) — pulls meeting context to enrich risks, decisions, vendor timelines
5. **Classification** — applies deterministic, priority-ordered algorithms:
   - 6 Rs Strategy (Retire → Retain → Replace → Refactor → Replatform → Rehost)
   - Execution Ownership per pillar (Factory / ISD-Partner / Unknown; Apps also has "No Migration Needed")
6. **Slide Selection** — evidence-driven; skips slides without strong data support
7. **HTML Generation** — produces a self-contained HTML deck with inline CSS, KPI cards, charts, callouts
8. **Verification** — math checks (sums equal in-scope total), disclaimers attached, single source citation

## Output Quality Rules (Executive Presentation)

Generated reports follow strict executive rules:
- **No internal/meta language** — no "algorithm", "formula", "scenario", "step-by-step trace" in the output
- **No zero-count items** — platforms/categories with 0 occurrences are omitted
- **Executive tone** — "Classification Note" not "Disclaimer", "Factory Scope Opportunity" not "Impact Analysis"
- **Deterministic** — same inputs produce identical classification numbers every time
- **Single source citation** — *"Cloud Accelerate Factory — Service Descriptions, May 2026"* (no version-diff explanation)

## Critical Rules

💲 **Never use PowerShell to write the HTML** — PowerShell heredocs (`@"..."@`) strip dollar signs from cost figures (`$702K/mo` becomes `/mo`). Use the `create` / `editFiles` tool or Python `open(path, 'w', encoding='utf-8')`. If `$` signs are accidentally stripped, `scripts/export_to_pdf.py` auto-detects and repairs them on its next run.

📊 **Math must add up** — classification counts MUST sum to the in-scope total. If they don't, recount — do NOT adjust numbers.

📝 **8 outstanding evidence-backed slides > 12 padded slides** — leadership values precision over volume

## Pillar Reference Loading

The skill is designed for progressive loading. Reference files are organized so only the pillars actually present in the data get loaded:

| Detected Pillar | Reference Files Loaded |
|---|---|
| Always | `classification-algorithm.md`, `slides-common.md`, `style-guide.md` (at gen time) |
| Applications | + `slides-application-pillar.md` |
| Databases | + `slides-database-pillar.md` |
| Infrastructure | + `slides-infrastructure-pillar.md` |

This keeps the active context window lean even though the full skill has substantial domain content.

## Related

- Skill definition → [SKILL.md](SKILL.md)
- Slash command → [.github/prompts/PortfolioStrategy.prompt.md](../../prompts/PortfolioStrategy.prompt.md)
- Enforcement hook → [.github/hooks/customer-data-isolation.json](../../hooks/customer-data-isolation.json)
- Context injection hook → [.github/hooks/scripts/load-migration-state.ps1](../../hooks/scripts/load-migration-state.ps1)
- Per-app modernization → [.github/prompts/Phase1-Plan.prompt.md](../../prompts/Phase1-Plan.prompt.md)
