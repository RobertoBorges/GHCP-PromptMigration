# Dependency Evidence and Delivery Responsibility

Load when supplied artifacts contain connectivity/dependency fields or usable first-party source/configuration. This is evidence collection for planning, not binary scanning, runtime execution, or permission to modify code.

## Detect and Choose the Mode

Inspect CSV/workbook schemas for source/destination hosts, ports, protocols, app IDs, connection targets, replication, clustering, or linked-server fields. Inspect supplied application roots for project/build manifests, source and configuration. Never treat this skill's own report generator, the migration tooling repository, or generated output as customer source.

| Available evidence | Mode |
|---|---|
| Connectivity exports, embedded dependency sheets, diagrams only | External |
| Supplied first-party source/configuration only | Source |
| Both | Hybrid |

Keep each source's scope, timestamp, environment, and coverage. Analyze with available search/parsing tools directly; there is no required `@dependency-analysis` agent. Load the existing stack/source adapters when relevant. If inputs are inaccessible, record a blocker or approved exclusion; do not claim full coverage.

## Source Audit

Inventory every supplied root/project/file before scanning. Classify each file as eligible, excluded, failed, or truncated, with a specific reason. Typical exclusions are binaries, generated files, dependency trees, build outputs, and vendored third-party source. Do not execute untrusted customer code or read secret values to prove a dependency.

Scan full eligible files, not samples. Follow project references and inspect configuration and call/use sites for APIs, SDKs, queues/topics/brokers, COM+/native components, databases/storage, identity, file transfers, shared folders, scheduled jobs, and environment-resolved endpoints. Keep unresolved configuration targets as candidates; do not invent hostnames.

Emit `_work/<run-id>/Code_Audit_Manifest.csv`:
`Root, Project, Relative_File, Status, Reason, Lines_Scanned`.

Report roots/projects/files/lines, eligible/scanned counts, exclusions, failures/truncations, and eligible-file coverage percentage. "Complete source coverage" requires every eligible file fully scanned and zero failures/truncations; it does not prove runtime completeness.

Emit one row **per occurrence** in `Code_Dependency_Evidence.csv`:
`Finding_ID, Project, Relative_File, Start_Line, End_Line, Symbol_or_Config_Key, Dependency_Type, Target, Confidence, Evidence_Status, Redacted_Summary`.

Use exact 1-based lines. For non-line-addressable artifacts, use N/A plus a section/key locator and reason. Preserve all occurrences when rolling up a dependency; link every evidence row to its finding. Redact credentials, tokens, personal data, and sensitive payloads from snippets and outputs.

## Evidence Strength and Reconciliation

- **Confirmed:** explicit static reference/configuration with a resolvable target; not proof of a successful live call.
- **Inferred:** evidence supports a relationship but target/usage needs confirmation.
- **Candidate:** ambiguous reference, unresolved target, or insufficient context.
- Hybrid reconciliation: **Corroborated**, **Runtime only**, **Code only**, or **Conflict**. Compare direction, environment, observation window, and normalized IDs before matching. Missing telemetry is not proof a static dependency is unused.

Use stable finding IDs and an explicit app-to-host/DB join. An integration count alone does not identify its endpoints or justify a topology. Do not form definitive move groups from unknown edges; label provisional sequencing and request discovery.

## Agent and SME Disposition

Assign every Confirmed/Inferred finding exactly one disposition:

| Disposition | SME type | Required evidence |
|---|---|---|
| Agent can handle | None | Bounded technical change and executable acceptance checks |
| Agent + Technical SME | Technical | Exact platform/network/identity/vendor input needed |
| Agent + Functional SME | Functional | Business behavior or process validation needed |
| Functional SME required | Functional | Unknown business meaning, redesign, or acceptance decisions the agent cannot own |

Candidates use `Needs validation`, not a promised implementation. Record agent action, exact SME question/input, accountable owner, rationale, validation/acceptance evidence, and whether business behavior must change. Technical difficulty alone does not imply functional redesign. An agent-capable change is not automatically Microsoft-funded or in commercial scope.

Summarize counts by disposition and technical/functional responsibility on the dependency slide. Bundle occurrence-level evidence separately and link it from the audit; do not crowd the executive deck with source code.
