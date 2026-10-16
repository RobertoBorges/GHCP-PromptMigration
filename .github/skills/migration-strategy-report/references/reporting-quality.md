# Reporting Quality, Evidence Model, and Validation

Always load with the report skill. These controls supplement, rather than replace, the pillar references. Keep public labels Microsoft / Partner / Unknown and the existing COTS Vendor annotation.

## Stage Gates and Audit

Use a unique UTC run ID such as `20261016T153000Z`. Store the audit alongside the final HTML as `Validation_Audit_<run-id>.md`; intermediate generators, manifests, and normalized data belong in the customer's `_work/<run-id>/` directory. The main skill's `_work/Report_Data.json` is shorthand for this run-specific working path. Do not overwrite a prior run.

Create the audit when preflight starts so failures are recoverable. Append each stage's **actual** result before advancing; do not pre-fill PASS entries. Record stage, check ID, PASS/FAIL/N/A, method/command, evidence path, observed result, and remediation. N/A requires a reason.

| Stage | Evidence required to advance |
|---|---|
| Preflight | Valid path, fixed input snapshot, accessibility and workbook manifests; excluded files approved explicitly |
| Discovery | Pillars, units, languages, source authority, coverage gaps, included/excluded slide decisions |
| Classification | Classified record model, computed joins, reconciliation, rules/version, confidence, dependency coverage |
| Compose | Runnable generator, on-disk partial output, completed slide IDs, languages and optional outputs |
| Assurance | Model validation, cross-slide checks, HTML/Office checks, data-quality assessment, final verdict |

Final verdicts:
- `READY`: all applicable required checks pass and no material unresolved qualification remains.
- `CONDITIONAL`: the required output checks pass, but disclosed evidence gaps or unapproved recommendations limit execution readiness.
- `BLOCKED`: an unresolved input, source-authority, or required-decision gate prevents the requested work.
- `FAILED`: generation, validation, or required output integrity failed.

Do not call a BLOCKED/FAILED run complete. A conditional report can be delivered with its limitations, but does not authorize deployment. Report-only generation does not require approving every target option; execution still uses the repository decision gates.

## Preflight: Before Creating Analytical Outputs

1. Resolve the user-supplied folder; verify it exists, is a directory, and is readable. An invalid path stops the run before creating outputs.
2. Take a read-only recursive snapshot of existing input paths with relative path, size, content hash, and artifact type. Never follow symlinks/reparse points outside the supplied roots. Treat material changes during analysis as a new snapshot/run.
3. Distinguish raw inputs, governing references, and historical outputs. Exclude generated HTML/PDF/Office decks, `_work`, report output directories, and prior audits from raw analytics; a prior report may be read explicitly as historical context, not silently recounted.
4. For every input, attempt an appropriate parser. Record inaccessible, corrupt, password-protected, unsupported, or empty files with the exact path and error. Do not bypass protection or policy restrictions. Ask whether to repair or exclude inaccessible inputs; record explicit exclusions and their analytical impact.
5. For each workbook, list **every sheet**, headers, data-row count, and inclusion/exclusion reason. Read all relevant rows, not previews. Distinguish data rows from headers, blank rows, subtotals, and legends. Document skipped empty/reference sheets. Evaluate formula cells with both formula and cached-value views; missing/stale cached values are a gap, not zero.
6. Establish authoritative versions using embedded dates, source-system IDs, verified identical content, or user confirmation. When conflicting sources have no defensible precedence, pause the affected classification and ask. Filesystem modification times alone are insufficient.

Input manifest columns: `Source_ID, Relative_Path, SHA256, Artifact_Type, Access_Status, Inclusion, Exclusion_Approval, Limitation`.
Workbook manifest columns: `Source_ID, Sheet, Header_Row, Data_Rows, Included_Rows, Pillar, Disposition, Reason`.

## Computed Classification and Explicit Joins

Run a script over the full source rows. Normalize whitespace/case in join keys without destroying the original identifier. Use stable source-system IDs where available; composite keys must be documented. Detect duplicate IDs and one-to-many/many-to-many joins before counting. Do not count a joined application once per host.

Emit one classification row per unique `(pillar, id)`. Preserve source file, sheet/section, row/cell or source-system ID, evaluated rule, rationale, confidence, scope, and proposed target. Record unmatched/ambiguous joins explicitly. Never infer a relationship from co-occurrence in the same workbook.

Keep customer-declared migration intent (including free-text notes) separate from validated readiness. Read all relevant intent columns, regardless of header name. A proposed target is not an approved architecture decision.

Count each category directly from records, not as `Total - known categories`. Missing evidence remains Unknown. Validate:
- IDs unique within each pillar; exactly one ownership classification per row.
- Each pillar's ownership counts sum to that pillar's in-scope count.
- Strategy counts sum to in-scope applications; include Retain/Retire if those are the assigned recommendations.
- Out-of-scope and already-cloud/SaaS records remain visible in the portfolio context; only the explicitly scoped population enters the scope ownership denominator.
- Repeated KPIs come from one summary, with filters and denominators shown.

Never sum apps + DB instances + VMs as a migration total. DB-role servers are a subset of the server inventory. App-tier PaaS and data-tier PaaS remain distinct metrics. Do not assume PaaS removes a VM without an explicit host mapping and all other hosted workloads accounted for. Missing mappings mean an unresolved footprint, not zero VMs.

## Machine-Readable Record Model

Write UTF-8 JSON using this contract (`schema_version` is `"1.0"`):

```json
{
  "schema_version": "1.0",
  "customer": "Contoso",
  "language": "en-US",
  "records": [
    {
      "pillar": "applications",
      "id": "APP-01",
      "name": "Orders",
      "in_scope": true,
      "ownership": "Unknown",
      "strategy": "Replatform",
      "migration_required": true,
      "confidence": "Low",
      "rule": "APP-UNKNOWN",
      "rationale": "Proposed managed hosting; eligibility assessment pending.",
      "evidence": ["D1: Portfolio.xlsx / Apps / row 2 / APP-01"]
    }
  ],
  "waves": [],
  "questions": [],
  "blockers": []
}
```

`pillar`: `applications`, `databases` (DB **instances**), or `infrastructure` (VMs/servers).
`ownership`: `Microsoft`, `Partner`, `Unknown`, or applications-only `No Migration Needed`.
`strategy`: required for in-scope applications; one of the six Rs, or Rearchitect/Rebuild when eight-R mode is explicitly enabled with `"strategy_mode": "8R"` (otherwise `"6R"`).
`confidence`: `High`, `Medium`, or `Low`. `in_scope` and `migration_required` are JSON booleans. No Migration Needed and Retain/Retire do not represent migration execution.
`evidence`: nonempty array of precise, redacted source references. `rule` and `rationale` are nonempty strings. Keep service-policy version/section in the evidence when asserting commercial scope.
Optional `target` is a proposed destination, not proof of user approval. Optional `host_ids` lists exact infrastructure IDs where mappings are known; it never creates additional server records.

Run (PowerShell, from the workspace root):

```powershell
python .github/skills/migration-strategy-report/scripts/report_data.py "<customer>\_work\<run-id>\Report_Data.json"
```

The command emits computed, separate per-pillar summaries as JSON and exits nonzero with explicit validation errors. Use these summaries in the report, audit, and optional package. It validates record contracts and counts, **not** the accuracy/completeness of the original source classification, policy interpretation, or visual layout. Those require the source/slide checks above.

## Ownership Presentation

Every ownership breakdown includes count, confidence, decision rationale, source and classification criteria. Keep vendor-managed apps distinguishable as Partner (COTS Vendor), not a fifth ownership category. Separate ownership from technical compatibility and funding eligibility.

When evidenced PaaS candidates or modernization intent exist, present a like-for-like option and a modernization option using the same scoped inventory. Keep stay-as-is visible as option 1 when seeking an architecture choice. Include per-pillar deltas, prerequisites/approval status, and pre/post VM footprint (or unresolved mapping gap). If no evidenced modernization path exists, use a single migration option; never manufacture identical comparisons.

## Financial Evidence

Each cost, savings percentage, or financial comparison needs a nearby concise derivation:
`Result = calculation; source file/sheet/cells or dated pricing export; assumptions`.
State currency, region, price date, PAYG/reservation/savings-plan term, license/benefit assumptions, and what the baseline includes. Do not mix monthly/annual periods or currencies without an explicit conversion source/date.

Without the required inputs, write `TBD - financial model pending`, list the missing baseline/pricing inputs in Data Quality, and assign a next action. Do not substitute industry averages, arbitrary savings percentages, or generic effort buffers. Put detailed calculations in the audit while leaving the report's claims independently understandable.

## Data Quality and Assurance Checklist

Always end with Data Sources and a Data Quality table: dimension, Complete/Partial/Missing/N/A, source/coverage, impact, and next action. Evaluate inventory (apps, VMs, DB instances), exact versions, business criticality/owners, scope/intent, CPU/RAM utilization, storage IOPS separately, network/identity, app/DB compatibility assessments, integration/HA mapping, financial baseline, Azure pricing, target decisions, and supplied source-code coverage. N/A needs a reason; assessment not run is Missing, not validated readiness.

Before delivery:
1. Reconcile file/sheet manifests to all included/excluded inputs and document partial coverage.
2. Validate the record model and all per-pillar ownership/strategy totals. Verify duplicate handling and unmatched joins.
3. Check each repeated KPI against the computed summary with identical units, filters, and denominator.
4. Verify every applicable slide, ownership confidence/rationale, financial derivation, inline source citation, and final data-quality table.
5. Inspect offline HTML in a browser and print/PDF layout where requested: slide order, overflow, readability, dollar signs, incomplete marker removed only after passing.
6. For translations, confirm identical IDs/counts and locale-aware formatting. For Office delivery, reopen every saved artifact and record the actual checks.
7. Append failures/remediations, exact output paths, and final verdict to the audit. Do not replace a detailed audit with a single "generated successfully" entry.

## References

- [Microsoft CAF migration strategy guidance](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/plan/select-cloud-migration-strategy) (reviewed 2026-10-16). Strategies are recommendations to validate with stakeholders, not automatic approval.
- [Action Log format](../../migration-artifacts/references/action-log-format.md).
