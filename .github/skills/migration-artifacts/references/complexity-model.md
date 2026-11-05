# Migration Complexity Model

> A repeatable, explainable way to rate how hard an application is to migrate to Azure and turn that rating into an effort range in weeks. Produced during `/assess-any-application` (Step 8.6). Consumed by `/build-migration-plan`, `/phase1-plan` and `/quick-assessment`.

**All numbers live in [`complexity-model.yaml`](./complexity-model.yaml).** This document explains the method and the rating rubric. If the two disagree, the YAML wins. Never hard-code weights, thresholds or weeks in a report or skill. Read them from the YAML and record its `model_version`.

## Overview

```
8 dimensions ── rate each 1–5 from evidence ──► delivery-model relief (AI-assisted: code-bound dimensions −1)
                                                   │
                                     adjusted ratings → weighted rating (1.0–5.0)
                                                   │
                         score = round((weighted − 1) / 4 × 100)   → 0–100
                                                   │
                         level from score thresholds (Low / Medium / High / Very High)
                                                   │
                         floor rules can raise the level (never lower it)
                                                   │
       effort weeks = level weeks × strategy factor
                                                   │
       breakdown: split the weeks across 9 work streams by share × stream rating
                  (low-confidence evidence widens only the streams it drives)
```

## Step 1 — Rate each dimension (1–5)

Rate from evidence already gathered in Discovery Steps 3–7. Every rating must cite evidence (file path, command output or user statement) and carry the `evidence_confidence` of the axis it came from. If there is no evidence, rate **3** and set confidence `low`. Do not guess low.

### 1. Code size (weight 0.20)

Use LOC (non-blank lines) **excluding** vendored, generated, third-party and minified code. Bands come from `dimensions.code_size.loc_bands`:

| Rating | LOC |
|---|---|
| 1 | < 10k |
| 2 | 10k – 50k |
| 3 | 50k – 200k |
| 4 | 200k – 1M |
| 5 | ≥ 1M |

For Oracle Forms, PowerBuilder or other binary-source 4GLs, LOC cannot be read directly. Rate from object counts instead: forms/windows/reports < 50 → 2, 50–200 → 3, 200–500 → 4, > 500 → 5. Set confidence `medium`.

### 2. Stack & runtime modernization gap (weight 0.15)

| Rating | Evidence |
|---|---|
| 1 | Already on a current LTS runtime and framework; Azure-native SDKs |
| 2 | One minor/major version behind (e.g., .NET 6→8, Java 17→21, Node 18→20); no breaking framework change |
| 3 | Major framework jump with known migration path (e.g., .NET Core 3.1→.NET 8, Spring Boot 2→3, Python 3.6→3.12); a few outdated libraries |
| 4 | Platform jump (.NET Framework→.NET 8/10, Java EE→Spring Boot, Python 2→3, PHP 5→8); legacy UI tech (WebForms, Silverlight, Flash, JSF, Struts 1); multiple unsupported or commercial off-the-shelf libraries without a modern version |
| 5 | Legacy 4GL / RAD stack (VB6, Delphi, PowerBuilder, Oracle Forms); no vendor support; rewrite needed |

### 3. Integrations (weight 0.15)

Count distinct external systems (inbound + outbound) from the integration map. Bands come from `dimensions.integrations.count_bands`:

| Rating | Integrations |
|---|---|
| 1 | 0 – 2 |
| 2 | 3 – 5 |
| 3 | 6 – 10 |
| 4 | 11 – 20 |
| 5 | > 20 |

Add `legacy_protocol_bump` (+1, capped at 5) if any integration uses SOAP/WCF, JMS, MSMQ, SMB/FTP file drops, COM/DCOM, or a mainframe/midrange link.

### 4. Data (weight 0.15)

| Rating | Evidence |
|---|---|
| 1 | No persistent data, or small data on a like-for-like Azure engine |
| 2 | Small–medium data, same engine family (e.g., SQL Server → Azure SQL), few stored procedures |
| 3 | Medium–large data, or a moderate amount of stored procedures/triggers (≈ 20–100), or a few cross-database queries |
| 4 | Large data, or engine change (e.g., Oracle → PostgreSQL), or > 100 stored procedures/packages, or replication / reporting consumers to keep in sync |
| 5 | Very large data with engine change and heavy in-database logic, or multiple datastores that must move together with near-zero downtime |

### 5. Architecture, state & jobs (weight 0.10)

| Rating | Evidence |
|---|---|
| 1 | Single stateless deployable |
| 2 | 2–3 deployables, externalized state |
| 3 | Monolith with in-process session state or local file writes, or a handful of scheduled/batch jobs |
| 4 | Many deployables (4–10) or tight coupling, shared file shares, machine-local caches, many cron/Windows scheduled tasks |
| 5 | > 10 deployables, distributed transactions, hard-coded topology, or a desktop client/server split that needs redesign |

### 6. Azure compatibility blockers (weight 0.10)

Use the blocker list from `quick-triage` Step 3: Windows-only APIs, GAC/COM registration, registry access, machine-local state, unsupported drivers/native libraries, hard-coded IPs/hostnames, no clear entry point, incompatible datastore.

| Rating | Blockers found |
|---|---|
| 1 | None |
| 2 | 1 minor (config-only fix) |
| 3 | 2–3, or 1 needing code change |
| 4 | 4+, or 1 needing a design change |
| 5 | A blocker that forces rehost to VM or a rebuild |

### 7. Identity, security & compliance (weight 0.10)

| Rating | Evidence |
|---|---|
| 1 | Already uses Entra ID / OIDC; no regulated data |
| 2 | Standard OAuth/SAML; secrets externalized |
| 3 | Windows/AD integrated auth or forms auth with own user store; some hard-coded secrets |
| 4 | Custom auth + regulated data (PII/PCI/HIPAA/GDPR) or data-residency constraints |
| 5 | Multiple identity providers, regulated data, strict audit/sovereignty requirements |

### 8. Delivery readiness & cutover (weight 0.05)

| Rating | Evidence |
|---|---|
| 1 | Good automated tests, CI/CD, IaC, docs; flexible cutover window |
| 2 | Tests + CI exist; IaC or docs missing |
| 3 | Few tests, manual build or deploy; one environment missing |
| 4 | No tests, no CI/CD, tight cutover window, or HA/DR / multi-region requirement |
| 5 | No tests, no build reproducibility, near-zero downtime required, HA/DR across regions |

## Step 2 — Apply the delivery model

The delivery model says who does the hands-on work. Read it from `delivery_model` in the YAML. The default is **`ai-assisted`**: a coding agent (for example GitHub Copilot agent mode with Claude Sonnet 5.5) performs the code conversion and engineers review, test and decide. Use `traditional` only when the user says the team will not use an AI coding agent.

| Dimension type | Dimensions | AI-assisted adjustment |
|---|---|---|
| Code-bound | code size, stack gap, architecture, Azure blockers | Rating − `rating_relief` (default 1), never below 1. Ratings of `no_relief_at_rating` (5) stay: rewrites and redesigns are still human-led. |
| Human-bound | integrations, data, identity & compliance, delivery & cutover | No change. They depend on other teams, data volume, approvals and downtime windows. |

Keep both values: `rating` (what the evidence says) and `adjusted_rating` (after relief). Scoring uses `adjusted_rating`. Record the agent and model actually used in `tooling`.

Also compute the **traditional comparison**: score, level and effort with no relief. Reports show it as a one-line "without AI assistance" reference so stakeholders see the difference.

## Step 3 — Score and level

1. `weighted = Σ (weight × adjusted_rating)`, a value from 1.0 to 5.0.
2. `score = round((weighted − 1) / 4 × 100)`, a value from 0 to 100.
3. Pick the highest `levels[].name` whose `min_score ≤ score`. Defaults: Low < 30, Medium 30–54, High 55–74, Very High ≥ 75.
4. Apply every rule in `floor_rules`. If a rule fires and its `min_level` is higher, raise the level. Record each fired rule `id`.
5. If any `no_estimate_when` condition holds, set `level: not-estimated` and point to `source-unsupported-escalation`.

## Step 4 — Effort in weeks

1. Take `weeks.min` / `weeks.max` of the final level. The same table applies to both delivery models; AI changes the ratings, not the table.
2. Multiply by `strategy_factors[migration_strategy.recommendation]`. Keep the unrounded values for Step 5.
3. Always show `baseline_team`, the delivery model and the `effort_scope` includes/excludes next to the number. A week figure without its assumptions is misleading.

## Step 5 — Effort breakdown (where the weeks go)

Split the Step 4 effort across `work_streams`. Each stream maps to a main-path phase so `/phase1-plan` can reuse it.

1. **Stream rating** = mean of its `drivers`' adjusted ratings (`overall` = the weighted rating).
2. **Slice** = `share × stream rating / 3`. Normalise: `percent = slice / Σ slices`. A stream with harder drivers gets a bigger share; easy ones shrink.
3. **Stream min / max** = unrounded total min / max × percent.
4. **Low confidence:** for each stream with at least one driver at `evidence_confidence: low`, multiply that stream's max by `low_confidence.stream_max_multiplier` (2.0). Mark the estimate `provisional` and name the widened streams. Only the uncertain part of the plan grows.
5. **Totals:** `min = floor(Σ stream min)` (at least 1 unless the strategy factor is 0), `max = ceil(Σ stream max)`.
6. Present stream effort in **team-days** (weeks × 5) so small streams stay readable. Round the minimum **down** and the maximum **up** to the nearest 0.5 day (the minimum is never below 0.5), the same direction as the week totals. When both ends round to the same value, show it once (for example `0.5` rather than `0.5–0.5`). Rounded stream values may not add up exactly to the rounded totals.

For `retire` / `retain` (factor 0), skip the breakdown.

## Measuring lines of code

Prefer a real counter if one is installed. Otherwise use the fallback commands. Always state which method was used.

| Tool | Command |
|---|---|
| `scc` | `scc --exclude-dir node_modules,bin,obj,dist,build,out,target,vendor,packages,.git,.venv,venv,__pycache__,coverage --no-cocomo .` |
| `cloc` | `cloc --exclude-dir=node_modules,bin,obj,dist,build,out,target,vendor,packages,.git,.venv,venv,__pycache__,coverage --not-match-f='\.(min|designer|generated|g)\.' .` |

PowerShell fallback (non-blank lines of common source extensions):

```powershell
# Run from the application root. Exclusions match only paths below the root.
$root = (Get-Location).Path
$skip = '[\\/](node_modules|bin|obj|dist|build|out|target|vendor|packages|\.git|\.venv|venv|__pycache__|coverage|bower_components)[\\/]'
$ext  = '.cs','.vb','.fs','.java','.kt','.scala','.groovy','.py','.js','.jsx','.ts','.tsx','.vue','.php','.rb','.go','.rs','.pl','.pm','.c','.cc','.cpp','.h','.hpp','.sql','.cshtml','.razor','.aspx','.ascx','.master','.jsp','.erb','.pas','.frm','.bas','.cls','.xaml'
Get-ChildItem -Recurse -File -ErrorAction SilentlyContinue |
  Where-Object { $ext -contains $_.Extension.ToLower() -and $_.FullName.Substring($root.Length) -notmatch $skip -and $_.Name -notmatch '\.(min|designer|generated|g)\.' } |
  Group-Object { $_.Extension.ToLower() } |
  ForEach-Object { [pscustomobject]@{ Ext = $_.Name; Files = $_.Count; Loc = ($_.Group | ForEach-Object { @(Get-Content -LiteralPath $_.FullName -ErrorAction SilentlyContinue | Where-Object { $_.Trim() }).Count } | Measure-Object -Sum).Sum } } |
  Sort-Object Loc -Descending
```

Bash fallback:

```bash
find . -type d \( -name node_modules -o -name bin -o -name obj -o -name dist -o -name build -o -name out -o -name target \
  -o -name vendor -o -name packages -o -name .git -o -name .venv -o -name venv -o -name __pycache__ -o -name coverage \) -prune -o \
  -type f -regextype posix-extended \
  -regex '.*\.(cs|vb|fs|java|kt|scala|groovy|py|js|jsx|ts|tsx|vue|php|rb|go|rs|pl|pm|c|cc|cpp|h|hpp|sql|cshtml|razor|aspx|ascx|master|jsp|erb|pas|frm|bas|cls|xaml)$' \
  ! -regex '.*\.(min|designer|generated|g)\..*' -print0 | xargs -0 cat 2>/dev/null | grep -cv '^[[:space:]]*$'
```

Rules:
- Exclude test code from **rating** but report it separately (it signals delivery readiness).
- Exclude database migration scripts that are auto-generated (e.g., EF `Migrations/*.Designer.cs`).
- For `describe-only` sources, ask the user for an order-of-magnitude figure and set confidence `low`.

## Worked example

A .NET Framework 4.7.2 WebForms line-of-business app, replatform strategy, AI-assisted delivery:

| Dimension | Evidence | Rating | Adjusted (AI) | Weight | Weighted |
|---|---|---|---|---|---|
| Code size | `scc`: 320k LOC | 4 | 3 | 0.20 | 0.60 |
| Stack gap | `*.csproj` TargetFrameworkVersion v4.7.2, WebForms | 4 | 3 | 0.15 | 0.45 |
| Integrations | 8 systems, 2 SOAP | 3 + 1 = 4 | 4 | 0.15 | 0.60 |
| Data | SQL Server 2016, 150 GB, 60 stored procs → Azure SQL MI | 3 | 3 | 0.15 | 0.45 |
| Architecture | Monolith, InProc session, 4 scheduled tasks | 3 | 2 | 0.10 | 0.20 |
| Azure blockers | Registry reads, local file share | 3 | 2 | 0.10 | 0.20 |
| Identity | Windows integrated auth, no regulated data | 3 | 3 | 0.10 | 0.30 |
| Delivery | No tests, manual deploy | 4 | 4 | 0.05 | 0.20 |
| **Total** | | | | | **3.00** |

- Score = round((3.00 − 1) / 4 × 100) = **50**, which is **Medium**. No floor rule fires.
- Effort = 3–5 weeks × 0.8 (replatform) = **2–4 weeks** for 2 engineers + 1 part-time architect, AI-assisted.
- Without AI assistance (no relief): weighted 3.55, score 64, **High**, 6–10 × 0.8 = **4–8 weeks**.

Breakdown (unrounded total 2.4–4.0 weeks):

| Work stream | Drivers (adjusted) | Stream rating | Share | Team-days |
|---|---|---|---|---|
| Assessment, decisions & detailed plan | overall 3.00 | 3.00 | 7.7 % | 0.5–2 |
| Code & configuration migration | 3, 3 | 3.00 | 29.0 % | 3–6 |
| State, jobs & Azure-blocker remediation | 2, 2 | 2.00 | 6.5 % | 0.5–1.5 |
| Integration rework & connectivity | 4 | 4.00 | 10.3 % | 1–2.5 |
| Identity, secrets & compliance controls | 3 | 3.00 | 6.8 % | 0.5–1.5 |
| Data migration & validation | 3 | 3.00 | 9.7 % | 1–2 |
| Infrastructure as code & CI/CD | 2, 4 | 3.00 | 9.7 % | 1–2 |
| Testing & validation | 3, 4 | 3.50 | 11.3 % | 1–2.5 |
| Deployment, cutover & hypercare | 4 | 4.00 | 9.0 % | 1–2 |

If the data rating had been `low` confidence, only the data stream's max doubles (2 → 4 team-days): total **2–5 weeks (provisional)**.

## Output shape

Write the result into `reports/Capability-Matrix.yaml` under `complexity:` (schema in [capability-matrix.md](./capability-matrix.md)). Then render it in the Discovery Dossier §10 (lines of code also in §1 and §4) and in the HTML report's complexity and effort-breakdown sections.

## Calibration

After each migration completes, append an entry to `calibration_log` in `complexity-model.yaml`, including its `delivery_model`. When there are 5 or more entries, compare `actual_weeks` to the estimate range:
- Actuals consistently above `max` → raise level weeks or the weight of the dimension that drove the overrun.
- Actuals consistently below `min` → lower level weeks.
- AI-assisted actuals far below the estimate → raise `rating_relief`; far above → lower it.
- Track actual time per work stream when you can and tune `work_streams[].share`.
- Bump `model_version` after any change.
