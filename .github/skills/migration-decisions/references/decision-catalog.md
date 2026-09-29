# Skill: Decision Catalog

> The canonical list of major architecture decisions the Code Migration Modernization Agent asks the user about. Used by Phase 1 to generate `reports/Decisions-Required.md`, and referenced by every Phase prompt for hard-gate enforcement.

**This catalog is closed. Adding or removing entries requires a PR review** — the catalog protects the user's autonomy, so changes need explicit approval.

For each decision: ID, name, required-by-phase, dependencies, options, and recommendation logic. Phase 1 expands this into `reports/Decisions-Required.md` using `decisions-required-template.md` as the format.

**Convention:** Option 1 is always **Stay-as-is** (or the lowest-disruption option) so the user has to actively reject the conservative path.

---

## D-01: Target framework / runtime version

- **Required for:** Phase 2 — Migrate Code
- **Depends on:** —
- **Locks downstream:** Phase 3 hosting choices (some frameworks excluded on certain hosts)

### Why ask
Framework version determines support lifecycle, breaking changes, library compatibility, and team skill requirements for the next 3+ years. Microsoft / Oracle / Python Foundation / Node Foundation have different LTS cadences. Picking wrong locks out cloud-native features OR forces a re-upgrade within 18 months.

### Options (stack-conditional — pick the matrix matching `Capability-Matrix.yaml#stack.primary`)

**Stack: .NET**

| # | Option | When to pick | Tradeoffs |
|---|--------|--------------|-----------|
| 1 | **Stay on current version** (Framework 4.x or .NET Core 3.x) | Rehost only; no code modernization | Locked out of cloud-native features; EOL risk |
| 2 | **.NET 8 LTS** | Want proven LTS, mature library ecosystem | Support ends Nov 2026; may need re-upgrade |
| 3 | **.NET 10 LTS** | Want newest LTS, longest runway (support Nov 2028) | Larger jump from Framework 4.x; some libraries lag |
| 4 | **.NET 9 STS** | Only if planned upgrade in 18 months | Short-term support; risky as final target |

**Stack: Java**

| # | Option | When to pick | Tradeoffs |
|---|--------|--------------|-----------|
| 1 | **Stay on Java 8 / 11** | Rehost only | Public OpenJDK 8 EOL approaching; library churn |
| 2 | **Java 17 LTS** | Conservative jump, broad library support | Will need follow-up to Java 21 |
| 3 | **Java 21 LTS** | Newest LTS, virtual threads, longest runway | Some legacy libraries may need updates |

**Stack: Python**

| # | Option | When to pick | Tradeoffs |
|---|--------|--------------|-----------|
| 1 | **Stay on Python 2.x / 3.8 / 3.9** | Rehost only | 2.x is EOL; 3.8 EOL Oct 2024; library risk |
| 2 | **Python 3.11** | Balanced choice, broad library support | Mid-lifecycle |
| 3 | **Python 3.12+** | Latest features, performance | Library compat varies |

**Stack: Node.js**

| # | Option | When to pick | Tradeoffs |
|---|--------|--------------|-----------|
| 1 | **Stay on Node 16 / 18** | Rehost only | Node 16 EOL; Node 18 EOL April 2025 |
| 2 | **Node 20 LTS** | Stable LTS, broad ecosystem | Mid-lifecycle |
| 3 | **Node 22 LTS** | Newest LTS, longest runway | Some libs lag a bit |

**Other stacks** (PHP, Ruby, Go, Perl, Rust, Oracle Forms, PowerBuilder, Delphi/VB6, Scala/Kotlin, C++ Windows): consult the matching `stack-<name>.md` skill for the recommended target.

### Recommendation logic
- If `source.primary_adapter == "on-premise"` AND `stack.framework_eol_within_year == true` → suggest Option 3 (newest LTS).
- If team has visible production deployments of a specific version in the repo (e.g., references in CI configs) → suggest that version.
- Otherwise → suggest newest LTS but explicitly note "I'm guessing — your team's familiarity should drive this."

---

## D-02: UI architecture

- **Required for:** Phase 2 — Migrate Code
- **Depends on:** D-01 (some UI options require modern frameworks)
- **Locks downstream:** Frontend hosting choice (SWA vs in-process)

### Why ask
UI rewrites are months of work and re-train the team on a new mental model. Keeping the existing UI is often the right call for migrations focused on infra modernization.

### Options (when workload includes a UI)

| # | Option | When to pick | Tradeoffs |
|---|--------|--------------|-----------|
| 1 | **Keep existing UI** (MVC / WebForms / JSP / etc.) | Migration is infra-focused; UI works | No frontend modernization; locked to server-rendered |
| 2 | **Razor Pages / server-rendered (.NET)** | Light modernization; team knows Razor | Still server-rendered; limited interactivity |
| 3 | **Blazor Server / WebAssembly** | Want C#-everywhere; SPA experience | Newer ecosystem; some lib gaps |
| 4 | **React** | Mature SPA, biggest hiring pool | Steep ramp from MVC; rewrite cost |
| 5 | **Angular** | Enterprise patterns, opinionated | Heavier than React; steeper learning curve |
| 6 | **Vue** | Lighter SPA, good DX | Smaller ecosystem than React |
| 7 | **Static + API (SWA)** | Pure JAMstack | Requires full UI rewrite |
| 8 | **No UI** | Workload is API/batch/service-only | N/A |

### Recommendation logic
- If `workload.primary == "api-service"` OR `workload.primary == "batch-job"` → suggest Option 8 (no UI).
- If migration strategy is `rehost` or `replatform` → suggest Option 1 (keep existing UI).
- If migration strategy is `rearchitect` or `rebuild` → present 3-7 with no single recommendation; user picks based on team skills.

---

## D-03: Backend / API style

- **Required for:** Phase 2 — Migrate Code (only when rearchitect / rebuild)
- **Depends on:** D-01, D-02

### Why ask
Affects client codegen, observability, gateway choice, and team's mental model. Hard to change later.

### Options

| # | Option | When to pick | Tradeoffs |
|---|--------|--------------|-----------|
| 1 | **Keep existing API surface** | Don't rewrite; preserves clients | Carries forward old patterns |
| 2 | **REST + OpenAPI** | Industry default; broadest tooling | Versioning, breaking-change discipline |
| 3 | **GraphQL** | Front-end-driven; many client types | Server complexity; caching harder |
| 4 | **gRPC** | Service-to-service; low latency; strict contracts | Browser limited (gRPC-Web required); harder debugging |
| 5 | **Minimal API (.NET)** | Lightweight, modern .NET | Less ceremony; some patterns missing |

---

## D-04: Database engine

- **Required for:** Phase 2, Phase 3, DatabaseMigration
- **Depends on:** —
- **Locks downstream:** D-05 (migration tool)

### Why ask
Sticks for 5+ years. Affects ops cost, hiring, query rewrites, transaction semantics, and tooling. By far the most consequential decision.

### Options

| # | Option | When to pick | Tradeoffs |
|---|--------|--------------|-----------|
| 1 | **Stay on current DBMS** (rehost on Azure VM / on-prem) | Pure lift; minimize change | No PaaS benefits; ops burden remains |
| 2 | **Azure SQL Database** | Coming from SQL Server | Closest fidelity; some T-SQL features differ |
| 3 | **Azure SQL Managed Instance** | Coming from SQL Server with cross-DB or SQL Agent | Higher cost; full SQL Server compat |
| 4 | **Azure Database for PostgreSQL — Flexible Server** | Open-source preference; cross-platform | Schema/queries need rewrite from SQL Server |
| 5 | **Azure Database for MySQL — Flexible Server** | Coming from MySQL | Same engine; mostly drop-in |
| 6 | **Azure Cosmos DB — NoSQL API** | Document patterns; planet-scale | Major rewrite from relational; consistency models |
| 7 | **Azure Cosmos DB — PostgreSQL API (Citus)** | Distributed PostgreSQL | Newer offering; ecosystem still maturing |
| 8 | **Azure Database for MariaDB** | Coming from MariaDB | EOL announced — only for short-term lift |
| 9 | **MongoDB Atlas on Azure** | Coming from MongoDB; want first-party Mongo | Marketplace billing; cross-org governance |
| 10 | **Multi-engine** | Different services use different stores | Operational complexity multiplies |

### Recommendation logic
- If `Capability-Matrix.yaml#data.primary_engine == "sql-server"` → suggest Option 2 (Azure SQL Database) and call out Option 3 only if cross-DB queries are detected.
- If `data.primary_engine == "oracle"` → present Options 4 (PG with schema migration) and 6 (Cosmos for doc-pattern subsets); note that Option 1 (Oracle on VM/AVS) is the only zero-change path.
- If `data.primary_engine == "mongodb"` → present Options 6 (Cosmos Mongo API), 9 (MongoDB Atlas), and 1.

---

## D-05: Database migration tool

- **Required for:** DatabaseMigration
- **Depends on:** D-04

### Options
| # | Option | When to pick | Tradeoffs |
|---|--------|--------------|-----------|
| 1 | **Azure DMS** (Database Migration Service) | SQL Server, MySQL, PostgreSQL, Oracle → Azure PaaS | Lift-friendly; not all engines |
| 2 | **DMA** (Data Migration Assistant) | Pre-migration schema/feature assessment | Assessment + small data sets |
| 3 | **Manual scripts** + bcp/pg_dump/mysqldump | Small datasets; max control | Manual checkpointing; cutover risk |
| 4 | **Cosmos DB Data Migration tool** | Anything → Cosmos | Cosmos-specific |
| 5 | **Database compare/sync tools** (Red Gate, dbt, Flyway) | Incremental sync with CDC | Vendor / OSS license + ops |
| 6 | **Azure Migrate: Database** (unified portal) | Want a guided portal experience | Wraps DMS; same constraints |

---

## D-06: Hosting platform

- **Required for:** Phase 3 — Generate Infra
- **Depends on:** D-01 (some frameworks have host constraints)
- **Locks downstream:** D-07 (IaC tool — every host has best-fit IaC modules)

### Options

| # | Option | When to pick | Tradeoffs |
|---|--------|--------------|-----------|
| 1 | **Azure VMs** | Pure lift; legacy OS/runtime; specific kernel needs | Highest ops burden; cheapest path |
| 2 | **Azure VMware Solution (AVS)** | Existing vSphere estate; minimize change | Premium pricing; only for vmware shops |
| 3 | **Azure App Service** | Web apps + APIs; PaaS simplicity | Some runtime version limits; container support partial |
| 4 | **Azure Container Apps** | Microservices, event-driven, batch | Serverless containers; some networking gaps |
| 5 | **Azure Kubernetes Service (AKS)** | Complex orchestration; existing K8s | Steepest learning; full power |
| 6 | **Azure Functions** | Event-driven, low traffic, glue code | Cold starts; not for long-running |
| 7 | **Azure Spring Apps** | Spring Boot with managed runtime | Java/Spring-specific |
| 8 | **Azure Static Web Apps** | JAMstack + serverless API | UI-focused; backend constraints |

### Recommendation logic
- If `migration.strategy == "rehost"` → Option 1 (VMs).
- If `workload.primary == "webapp"` AND framework is supported → Option 3 (App Service).
- If `workload.primary == "api-service"` AND containerized → Option 4 (Container Apps).
- If existing Kubernetes → Option 5 (AKS).

---

## D-07: IaC tool

- **Required for:** Phase 3 — Generate Infra
- **Depends on:** D-06

### Options
| # | Option | When to pick | Tradeoffs |
|---|--------|--------------|-----------|
| 1 | **Bicep** | Azure-only; want Microsoft-native | Multi-cloud impossible; some ecosystem gaps |
| 2 | **Terraform** | Multi-cloud or existing TF team | OSS license history; state management |
| 3 | **ARM templates** | Legacy compatibility | Verbose JSON; superseded by Bicep |
| 4 | **Pulumi** | Want IaC in TypeScript/C#/Python | Smaller community; vendor lock-in lite |
| 5 | **Azure Verified Modules (AVM) via Bicep** | Want Microsoft-supported modules | Subset of Bicep; same trade-offs |
| 6 | **azd templates** | Want one-command provision + deploy | Convention-heavy; some flexibility loss |

### Recommendation logic
- If `team.existing_iac_tool` evidence in repo → suggest that.
- If team is Azure-only → suggest Bicep / AVM.
- If multi-cloud OR existing Terraform on other clouds → suggest Terraform.

---

## D-08: Region & data residency

- **Required for:** Phase 3, Phase 4
- **Depends on:** D-11 (compliance scope)

### Why ask
Data residency is a hard legal constraint. Region selection drives cost, latency, and disaster recovery options.

### Required fields
- **Primary region:** (free-text Azure region, e.g., `eastus2`, `westeurope`, `brazilsouth`)
- **Paired DR region:** (default per Microsoft's region pair list)
- **Data residency constraints:** (e.g., "must stay in EU", "must stay in Brazil", "no preference")

### Notes
- Microsoft maintains region pairs — if you pick primary, the paired region is suggested but can be overridden.
- Some services (Cosmos DB, SQL geo-replication) have region restrictions.

---

## D-09: Authentication

- **Required for:** Phase 2 — Migrate Code, Phase 3 — Generate Infra

### Options
| # | Option | When to pick | Tradeoffs |
|---|--------|--------------|-----------|
| 1 | **Stay on existing IdP** (LDAP, AD, custom) | Migration without auth modernization | Locked to current auth limitations |
| 2 | **Microsoft Entra ID** (workforce / employees) | B2E (business-to-employee) apps | Tenant + roles + RBAC |
| 3 | **Microsoft Entra External ID** (formerly B2C) | B2C apps; consumer auth | User flows + IdP federation |
| 4 | **Federated to external IdP** (Okta, Auth0, Ping) | Already-standardized SSO | License costs; integration |
| 5 | **No auth required** | Internal service, network-isolated | Operational risk if exposed |

---

## D-10: Multi-tenancy approach

- **Required for:** Phase 3 — Generate Infra (only if multi-tenant)

### Options
| # | Option | When to pick | Tradeoffs |
|---|--------|--------------|-----------|
| 1 | **Single-tenant** (no tenancy) | Internal app | N/A |
| 2 | **Pooled (shared DB + tenant column)** | Many small tenants | Noisy-neighbor risk; harder per-tenant scaling |
| 3 | **Silo per tenant (DB per tenant)** | Few large tenants; compliance | High ops cost per tenant |
| 4 | **Hybrid (silo for large, pool for small)** | Tiered SaaS | Operational complexity |

---

## D-11: Compliance scope

- **Required for:** Phase 1 (constrains every later phase)

### Required fields (multi-select)
- [ ] None
- [ ] HIPAA
- [ ] PCI-DSS
- [ ] SOC 2 Type II
- [ ] GDPR (or equivalent — LGPD, CCPA)
- [ ] FedRAMP (High / Moderate / Low)
- [ ] ITAR / Export-controlled
- [ ] Industry-specific (e.g., FINRA, FERPA)
- [ ] Other: _____

Affects: Region choice, encryption requirements, audit logging, retention, identity, secret rotation cadence.

---

## D-12: Cost ceiling

- **Required for:** Phase 3, Phase 4

### Required fields
- **Max monthly Azure spend (USD):** _____
- **Tolerance for overage:** (Hard cap / Soft cap / No cap)
- **Reserved capacity / Savings Plans tolerance:** (Yes / No / Need approval)

Drives SKU tier selection. Without this, the agent cannot validate that the proposed architecture fits budget.

---

## D-13: DR — RPO / RTO targets

- **Required for:** Phase 3, Phase 4

### Required fields
- **RPO (Recovery Point Objective):** Maximum acceptable data loss (e.g., 0 / 15 min / 1 hr / 24 hr)
- **RTO (Recovery Time Objective):** Maximum acceptable downtime during failover (e.g., 0 / 15 min / 1 hr / 24 hr)
- **DR strategy:** Active-active / Active-passive / Pilot light / Backup-only

Drives: geo-replication, backup frequency, secondary region SKUs, Front Door / Traffic Manager.

---

## D-14: Cutover strategy

- **Required for:** Phase 4 — Deploy to Azure

### Options
| # | Option | When to pick | Tradeoffs |
|---|--------|--------------|-----------|
| 1 | **Big-bang** (cutover weekend) | Small app, defined maintenance window | All-or-nothing risk |
| 2 | **Phased by feature** | Decomposed monolith | Long parallel-run period |
| 3 | **Blue-green** | Need instant rollback | 2x infra cost during cutover |
| 4 | **Canary** | High-traffic public app | Routing complexity; observability rigor |
| 5 | **Strangler fig** (gradual replacement) | Multi-year modernization | Most complex; longest timeline |

---

## D-15: Acceptable downtime

- **Required for:** Phase 4

### Required field
- **Max acceptable downtime for cutover:** (Zero / Seconds / Minutes / Hours / Maintenance window of X)

Constrains D-14 (cutover strategy) and D-04 (database migration approach — DMS online vs offline).

---

## D-16: CI/CD platform

- **Required for:** Phase 5 — Setup CI/CD

### Options
| # | Option | When to pick | Tradeoffs |
|---|--------|--------------|-----------|
| 1 | **Keep existing CI/CD** (Jenkins, TeamCity, etc.) | Pure lift; team trained | No modernization; ops burden continues |
| 2 | **GitHub Actions** | Code in GitHub; want native integration | Cost on private repos with high usage |
| 3 | **Azure DevOps Pipelines** | Enterprise Azure governance | Two-system world if also using GitHub |
| 4 | **GitLab CI** | Code in GitLab | Same as GitHub case |

---

## D-17: Observability stack

- **Required for:** Phase 6 — Post-Migration Ops

### Options
| # | Option | When to pick | Tradeoffs |
|---|--------|--------------|-----------|
| 1 | **Keep existing** (Splunk, Datadog, etc.) | Already standardized | Cost; potential dual-pane |
| 2 | **Azure Monitor + Application Insights** | Want Microsoft-native end-to-end | Less customization than Datadog |
| 3 | **Azure + Grafana managed** | Want dashboards-as-code | Grafana operator load |
| 4 | **Datadog / New Relic / Dynatrace** | Already a customer; multi-cloud | License costs |
| 5 | **Split** (App Insights + Datadog) | Migration period only | Long-term complexity |

---

## D-18: Container registry (if D-06 is container-based)

- **Required for:** Phase 3 (only if hosting is Container Apps / AKS / Functions Premium with custom containers)

### Options
| # | Option | When to pick | Tradeoffs |
|---|--------|--------------|-----------|
| 1 | **Azure Container Registry (ACR)** | Azure-native; private network integration | Cost tier choice (Basic / Standard / Premium) |
| 2 | **Docker Hub** | Already publishing there | Public-only or paid for private |
| 3 | **GitHub Container Registry (GHCR)** | Code in GitHub; want unified | Less Azure-native networking |
| 4 | **Multi-registry** | Mirror across providers | Sync ops; auth complexity |

---

## Recommendation discipline (reminder)

Every recommendation in this catalog is a **default guess**, not a "best choice." the agent surfaces evidence from the Capability Matrix but explicitly defers to the user. See [`decision-hardstop.md`](./decision-hardstop.md) for the binding behavior.
