# Skill: Migration Strategy Decision Tree

> The strategic brain of the Discovery Engineer. Picks a migration strategy (Rehost / Replatform / Refactor / Rearchitect / Rebuild / Retire / Retain) based on a structured decision tree that weighs business priority, source constraints, code mutability, data gravity, integration complexity, target Azure options, cutover constraints, modernization depth, and team readiness.

> 6Rs are an **output field**, not the engine. Use this tree to derive the recommendation, then attach the 6Rs label.

## When to Use

- At the end of discovery, after source/stack/workload/data axes are classified
- Whenever the Capability Matrix's `migration_strategy.recommendation` needs to be set or revised
- During Architect approval if the recommendation looks weak

## Inputs (from Capability Matrix)

- `application.business_priority` (`speed | modernize | cost | risk`)
- `source.primary_adapter` + `source.evidence_confidence`
- `stack.primary_stack` + `stack.evidence_confidence`
- `workload.primary_pattern`
- `data.primary_datastore` + `data.data_gravity`
- `risk_flags` (e.g., `regulated-data`, `vendor-licensed-runtime`, `no-source-code-available`)

## Output

A structured strategy recommendation that includes:

```yaml
migration_strategy:
  recommendation: <rehost | replatform | refactor | rearchitect | rebuild | retire | retain>
  rationale: <multi-line: which branches were taken>
  decision_path:
    - <branch and choice>
    - ...
  alternatives_considered:
    - alternative: <X>
      rejected_because: <reason>
    - alternative: <Y>
      rejected_because: <reason>
  target_azure_candidates:
    - service: <Azure service>
      fit_score: <high | medium | low>
      fit_notes: <one-line>
    - ...
  required_specialists: [<applicable sub-agent names>]
```

## Decision Tree

Apply the branches in order. The first branch that fires wins (with the option for an upstream branch to enforce its outcome).

### Branch 1 — Retire / Retain (filter out apps that should not move at all)

- If business priority is `cost` AND the app is `low-business-value` (per user) AND there is a documented sunset plan → **Retire**.
- If the app is a regulatory-required SaaS-embedded system (Salesforce, ServiceNow, SAP) AND only integrations need to move to Azure → **Retain** (only the Azure integration glue is built).

Otherwise continue.

### Branch 2 — No source code available

If `risk_flags` contains `no-source-code-available`:

- If `workload.primary_pattern` is `packaged-app` AND vendor supports container image → **Rehost** (container-based, lift to Container Apps or AKS).
- If vendor offers Azure-supported runtime (e.g., SAP on Azure VMs, Oracle on AVS) → **Rehost** (managed VM landing zone).
- Else → **Rehost** (VM-based lift-and-shift).

This branch ends decisively. Code-touching strategies are off the table.

### Branch 3 — SaaS-embedded / unsupported source / unsupported runtime

If `risk_flags` contains `saas-embedded`, `unsupported-source`, or `unsupported-runtime`:

- → Open `source-unsupported-escalation`. Recommendation depends on escalation outcome. For **mainframe / midrange / IBM i** and other explicitly-unsupported source families (COBOL, RPG, Natural, PL/I on z/OS, z/VSE, or AS-400), this tool does not attempt code-level migration — escalate to a specialist partner (Micro Focus / Astadia / Kyndryl / LzLabs / TCS / NTT DATA). Default strategy field to **Retain** or **Rearchitect** pending partner engagement.
- Add Architect + Cost Engineer + Security Auditor as required specialists.

### Branch 4 — Business priority = `speed-to-cloud`

If `application.business_priority == "speed"`:

- If source is in a supported PaaS runtime (current .NET / current Java / current Node.js / current Python) AND data gravity is `small` or `medium` → **Replatform** (App Service or Container Apps; minimal code change; managed data service).
- If source is on an unsupported runtime (out-of-support framework version) → **Replatform with mandatory runtime upgrade** (still tagged Replatform, but Phase 2 effort goes up).
- If source is a binary/packaged app → **Rehost** (per Branch 2 logic).

Speed-first never chooses Rebuild or Rearchitect.

### Branch 5 — Business priority = `modernize first`

If `application.business_priority == "modernize"`:

- If the codebase is small (<50k LOC), stack is supported, and tests exist → **Refactor** (in-place modernization to current LTS runtime + Azure PaaS).
- If the codebase is large or has heavy legacy debt AND `workload.primary_pattern` is `webapp` or `api-service` AND code mutability is high → **Rearchitect** (decompose monolith, modern PaaS).
- If the codebase is unmaintainable (no tests, no docs, original team gone) AND business owners are willing to invest → **Rebuild** (greenfield with modern stack; old app keeps running until parity).

Modernization paths never default to Rehost.

### Branch 6 — Business priority = `cost first`

If `application.business_priority == "cost"`:

- If the app is low-traffic, event-driven, or batch → **Refactor to serverless** (Functions / Container Apps Jobs / Logic Apps). Big TCO win.
- If the app is steady-state web/API → **Replatform** (right-sized App Service or Container Apps with autoscale floor = 0 where possible).
- If the app is a candidate for retirement → loop back to Branch 1.

### Branch 7 — Business priority = `risk first`

If `application.business_priority == "risk"`:

- If there's a regulated-data flag → **Replatform** (preserve current behavior; modernize only network/identity/secrets layer; small attack surface for change).
- If the app is production-only (no test env) → **Replatform** with extra Cutover Commander rehearsal gate before Phase 4.
- If the app is mission-critical with tight RTO/RPO → **Replatform** with database-level replication (Azure DMS continuous sync) and traffic-shifting cutover.

Risk-first rarely chooses Rebuild or Rearchitect.

### Branch 8 — Workload pattern guardrails

After choosing from Branches 4–7, apply workload-pattern overrides:

| Pattern | Override |
|---------|---------|
| `data-pipeline` | Strongly prefer **Replatform to Data Factory / Synapse / Databricks** even if `speed-to-cloud`. ETL apps don't survive a pure rehost. |
| `event-driven` | Strongly prefer **Refactor to Functions** over Container Apps when triggers map cleanly. |
| `desktop-client-server` | Force **Rebuild** path (web/PaaS replacement) unless explicit Rehost approval. |
| `packaged-app` | Force **Rehost** unless vendor offers PaaS SKU. |

### Branch 9 — Data gravity overrides

| Data gravity | Effect |
|--------------|-------|
| `none` or `small` (<1 GB) | No override |
| `medium` (1–100 GB) | Database Specialist required; no override |
| `large` (100 GB – 1 TB) | Cutover Commander required; if speed-to-cloud, consider phased data migration (DMS continuous) |
| `very-large` (>1 TB) | Strongly prefer **Replatform-with-DMS** strategy. Forbid Rebuild unless 6-month+ timeline. |

### Branch 10 — Target Azure candidates

Based on the chosen strategy + workload + data, produce an ordered list of Azure candidates.

#### For Rehost
1. Azure VM + managed disks + Azure Backup
2. Azure VMware Solution (AVS) if VMware-native
3. Container Apps if vendor offers a container image

#### For Replatform
1. **Webapp/API:** App Service (first), Container Apps (when containerization is desired), AKS (when orchestration complexity demands it)
2. **Batch:** Container Apps Jobs (first), Azure Batch (HPC-scale), Container Instances (one-shot)
3. **Event-driven:** Functions (first), Container Apps (KEDA-driven), Service Bus + Functions chain
4. **Data:** Azure SQL (from SQL Server), Azure PostgreSQL Flexible (from PG / Oracle small), Azure Database for MySQL (from MySQL), Cosmos DB (from Mongo / DynamoDB)

#### For Refactor / Rearchitect
1. Compute as for Replatform
2. Add Entra ID workload identity + Key Vault
3. Add Application Insights + Log Analytics
4. Add API Management when many APIs converge

#### For Rebuild
1. Greenfield Container Apps + serverless data services
2. Static Web Apps + Functions when frontend separates from backend
3. Modern PaaS choice independent of legacy

#### For Retire / Retain
1. No target. Document sunset plan or integration glue only.

### Branch 11 — Alternatives consideration

For each recommendation, generate **at least two alternatives** and explicit reasons for rejection. The Architect uses these to challenge the recommendation.

Pattern:

```
Recommendation: Refactor
Alternatives considered:
  - Rehost: rejected because business priority is "modernize first" — pure lift defers but doesn't pay down debt.
  - Rebuild: rejected because existing tests give us regression coverage; greenfield loses that asset.
```

### Branch 12 — Required specialists

Always include Architect + Azure Specialist + Tester + Scribe. Add specialists per matrix signals:

| Signal | Add |
|--------|-----|
| Any code change | Coder |
| Data gravity ≥ medium | Database Specialist |
| `regulated-data` | Security Auditor |
| `vendor-licensed-runtime` | Cost Engineer |
| `production-only-system` or `tight-cutover-window` | Cutover Commander |
| Performance-sensitive | Performance Engineer |
| Observability-from-day-one expected | Observability Engineer |
| Many integrations | Architect (extra) |
| Pipelines/CI-CD new | DevOps Engineer |

## Decision Path Documentation

Every recommendation must record the path taken. Example:

```yaml
decision_path:
  - "Branch 1 (Retire/Retain): not triggered — app is active, owner wants Azure"
  - "Branch 2 (No source): not triggered — full source in GitHub repo"
  - "Branch 3 (SaaS/unsupported-source/unsupported-runtime): not triggered"
  - "Branch 4 (speed-first): not triggered — priority is 'modernize'"
  - "Branch 5 (modernize-first): TRIGGERED — small codebase + tests + supported stack → Refactor"
  - "Branch 8 (workload override): workload=api-service, no override"
  - "Branch 9 (data gravity): medium → Database Specialist required, no strategy override"
  - "Branch 10 (target): primary candidate = Container Apps; secondary = App Service"
  - "Branch 12 (specialists): Coder + Database Specialist + Tester + Scribe + Azure Specialist"
```

## Anti-Patterns

- Do **not** default to Refactor for every "modernize" engagement. Apply the size/tests/debt filter.
- Do **not** recommend Rebuild for very-large data gravity unless a multi-quarter timeline is explicit.
- Do **not** recommend Rehost without checking Branch 2 conditions — Rehost is fine when source is unavailable, suspect when it isn't.
- Do **not** skip alternatives. Discovery without alternatives is opinion, not analysis.
- Do **not** name a specific Azure SKU or region — only **service candidates**. The Architect picks SKUs.

## Quality Bar

- [ ] Recommendation set (6Rs label)
- [ ] Decision path recorded (every branch evaluated, even when not triggered)
- [ ] At least 2 alternatives considered + rejection reasons
- [ ] Target Azure candidates ordered with fit notes
- [ ] Required specialists listed and traced to matrix signals
- [ ] No SKU-level or region-level decisions (those belong to Architect)
