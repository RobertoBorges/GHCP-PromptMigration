# Optional Languages and Execution Package

These options extend the default HTML deck. Enable only when requested or agreed with the user. They use the same classified record model and do not change ownership, scope, or architecture decisions.

## Language and Locale

Detect candidate source languages from headers and narrative text, not technical names alone. Confirm the report language if ambiguous. Offer source-language plus English output when useful; do not require two versions automatically.

Generate both versions from one `Report_Data.json` with shared IDs and summaries. Translate titles, labels, callouts, status text, recommendations, and methodology. Preserve source identifiers, app/host names, products, source quotations, and citation locators. Translate narrative meaning, not identifiers.

Use a locale-aware formatter for every displayed number/date/currency (for example `Intl.NumberFormat` with an explicit BCP-47 locale in the generator). Do not use English comma formatting globally or search/replace separators in rendered HTML. Decimal precision, nonbreaking spaces, percentages, and currency symbols must be handled consistently.

Use a language suffix such as `_pt-BR.html` and `_en-US.html`. Validate that every version has the same slide IDs, source references, scoped counts, ownership totals, and financial inputs. Distinguish translated labels from original source values in the audit.

## Delivery Package Contract

The bundled renderer produces a **four-slide execution summary**, an XLSX workbook, and traceability JSON. It is not an export of every HTML slide and does not replace the full report or audit. No external corporate PowerPoint template is required.

Extend the model in [reporting-quality.md](reporting-quality.md) with:

```json
{
  "waves": [
    {
      "id": "W1",
      "name": "Pilot - pending approval",
      "record_refs": [{"pillar": "applications", "id": "APP-01"}]
    }
  ],
  "questions": [
    {"id": "Q1", "text": "Approve proposed hosting target?", "owner": "Application owner", "evidence": ["D1: APP-01"]}
  ],
  "blockers": [
    {"id": "B1", "text": "Compatibility assessment not run", "owner": "Technical SME", "evidence": ["D1: APP-01"]}
  ]
}
```

References in waves must identify existing, in-scope records that require migration. A record can occur in at most one wave; unassigned migrating records appear explicitly in the workbook as `Unassigned`, making the package conditional. Each question/blocker has a unique ID, text, owner, and evidence. Do not put a record in a wave to conceal an unresolved decision.

Use self-contained delivery wording: no "see Scenario B/slide 5b" or assumptions that the delivery team received the HTML deck. Keep open questions to necessary execution decisions; do not ask for fields already established by evidence. Store details/evidence in the workbook rather than dropping blockers from a top-five summary.

## Run the Bundled Tools

Python 3.8+ is required. The model validator uses only the standard library. Office rendering additionally needs `python-pptx` and `openpyxl`; if missing, explain the dependency error and install only with the user's environment approval.

```powershell
python .github/skills/migration-strategy-report/scripts/report_data.py "<customer>\_work\<run-id>\Report_Data.json"
python .github/skills/migration-strategy-report/scripts/delivery_package.py "<customer>\_work\<run-id>\Report_Data.json" --output "<customer>\DeliveryPackage\<run-id>"
```

The output directory must not exist, preventing silent overwrites. A dependency/model failure creates no package. Rendering/verification failures exit nonzero and leave `Validation.json` marked FAILED where the output directory could be created. Never distribute that folder as validated.

Outputs:
- `Execution_Summary.pptx`: title, Microsoft scope, Partner/Unknown scope, top-five waves and blockers. Scope counts stay separated by pillar.
- `Execution_Workbook.xlsx`: Open Questions, Delivery Blockers, Scope and Waves, Validation Steps. Full record IDs, ownership, targets, confidence, evidence, wave assignments and all blockers remain available.
- `Traceability.json`: the input model and computed summary.
- `Validation.json`: one result per actual integrity/count/content check and READY/CONDITIONAL/FAILED package outcome.

The renderer validates OOXML ZIP integrity, reopens the PPTX and workbook, checks slide count/titles, required worksheets/row counts, and JSON round-trip consistency. Copy individual results into the run audit, then inspect slide/workbook layout visually. Package integrity does not prove source truth, HTML consistency, translation quality, or business approval; perform those checks separately.

Set the **run** verdict to the most restrictive applicable result, not just the package's structural outcome. Outstanding questions, blockers, Unknown ownership, Low confidence, or unassigned migrating records make the package CONDITIONAL. Do not use READY to override a failed report check or pending architecture decision.

## References

- [python-pptx quickstart](https://python-pptx.readthedocs.io/en/latest/user/quickstart.html) (reviewed 2026-10-16).
- [openpyxl tutorial](https://openpyxl.readthedocs.io/en/stable/tutorial.html) (reviewed 2026-10-16).
