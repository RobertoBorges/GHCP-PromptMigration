# Classification Algorithms — Reference

This reference is loaded by the `migration-strategy-report` skill whenever classification work occurs (which is almost always). Contains the deterministic 6 Rs strategy classification and execution ownership classification (Factory / Partner / Unknown) for Apps, Databases, and Infrastructure pillars.

## Why These Algorithms Are Deterministic

Given the same CMDB export with the same field values, these algorithms produce the same results every time. Rules are evaluated in strict priority order with no subjective judgment — the LLM applies CAF business-driver indicators and ownership conditions mechanically.

---

## CAF-Aligned 6 Rs Strategy Classification

**Framework Reference:** Microsoft Cloud Adoption Framework (CAF) — [Select your cloud migration strategies](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/plan/select-cloud-migration-strategy)

**CAF defines 8 migration strategies:**

| # | Strategy | CAF Business Driver | When to Apply |
|---|----------|--------------------|--------------|
| 1 | **Retire** | Need to decommission redundant or low-value workloads | Workload has limited business value; migration cost outweighs benefits |
| 2 | **Rehost** | Need minimal business disruption and no modernization in near future | Stable, Azure-compatible, low-risk; short-term cloud goals; reduce CapEx |
| 3 | **Replatform** | Need PaaS solutions and minimal code changes to offload maintenance | Simplify reliability/DR; reduce OS/licensing overhead; containerize app |
| 4 | **Refactor** | Need code changes to reduce technical debt or optimize for cloud | Decrease maintenance cost; use Azure SDKs; apply cloud design patterns |
| 5 | **Rearchitect** | Need architecture changes to unlock cloud-native capabilities | Modularization; service decomposition; varying scaling needs per component |
| 6 | **Replace** | Need SaaS/AI solution to simplify operations | Internal dev resources better used elsewhere; little need for customization |
| 7 | **Rebuild** | Need new cloud-native solution to meet requirements | Legacy too outdated; need modern frameworks; reduce operational cost |
| 8 | **Retain** | Need stability and no change | Stable, compliant; no near-term driver to move; low ROI from migration |

### 6 Rs vs 8 Rs Mode

- **Default (6 Rs):** Use 6 strategies — Rehost, Replatform, Refactor, Replace, Retire, Retain. Merge Rearchitect into Refactor (both involve code/architecture modernization). Merge Rebuild into Replace (both involve replacing the current workload with something new).
- **8 Rs mode:** Use all 8 strategies only when the customer explicitly requests it or when the portfolio has clear Rearchitect/Rebuild candidates that should be tracked separately.

All references below use 6 Rs labels. In 8 Rs mode, split Refactor → Refactor + Rearchitect, and Replace → Replace + Rebuild, using the CAF criteria in the table above.

### CAF Core Principle

Each workload's migration strategy is determined by its **business driver** — the gap between the workload's current state and the desired future state. Per CAF:
1. **Define business goals** — what the organization wants from cloud adoption (cost reduction, agility, innovation, resilience, AI adoption)
2. **Identify gaps** — what each workload must change to support those goals
3. **Determine the business driver** — the specific, actionable reason for change
4. **Map business driver → strategy** — use the table above

When explicit business-driver data is unavailable (common with raw CMDB exports), **infer the business driver from technical and operational indicators** in the CMDB using the rules below.

### Classification Rules (Priority Order — First Match Wins)

Every in-scope application is assigned to exactly ONE strategy. Rules are evaluated top-to-bottom; the FIRST matching rule wins.

**Scope:** This algorithm applies ONLY to in-scope applications (those with a Proposed Modernization Phase or Pilot Flag). Out-of-scope apps are NOT classified.

---

#### Step 1: RETIRE
**CAF Driver:** "Need to decommission redundant or low-value workloads"
**CAF Indicators:** Workload has limited current or future business value; migration or modernization cost outweighs business benefits.

Classify as **Retire** if ANY of:
- Application status/disposition contains "Decommission", "Sunset", "End of Life", "Retire", "Deprecated", or "Obsolete"
- Criticality = Low AND no active users or business process dependency documented AND Complexity = "Simple"
- Redundant application (duplicate functionality with another in-scope app that IS being migrated)
- Criticality = Low AND Architecture Type = "Desktop" AND Containerized ≠ "Yes" — desktop utility apps with no cloud path

**CAF Validation:** Confirm the workload is obsolete and has no critical dependencies that would affect other systems.

---

#### Step 2: RETAIN
**CAF Driver:** "Need stability and no change"
**CAF Indicators:** Workload is stable, compliant, and meets all business needs; no near-term driver to migrate; migration offers low ROI.

Classify as **Retain** if ANY of:
- Complexity = "Very Complex" AND Integration Count > 20 AND Criticality ≥ High — too interconnected and critical to move safely in near term
- Tech Stack contains legacy platforms explicitly out of scope for this tool (COBOL, RPG, PL/I, Natural on mainframe / IBM i / midrange) — these require a specialist-partner engagement (Micro Focus / Astadia / Kyndryl / LzLabs)
- Regulatory/compliance constraints explicitly block cloud migration (data sovereignty, air-gapped requirements, specific regulatory hold)
- Assigned to Phase 7–8 AND Complexity = "Very Complex" AND Architecture Type = "Platform" — intentionally deferred
- Database Platform = "DB2" or "Teradata" AND Complexity = "Very Complex" — deep platform lock-in with no near-term migration driver

**CAF Guidance:** Use Azure Arc to manage retained on-premises workloads from Azure. Consider Azure Local for on-premises modernization. Revisit in future migration waves when constraints change.

---

#### Step 3: REPLACE
**CAF Driver:** "Need SaaS/AI solution to simplify operations"
**CAF Indicators:** Internal development resources are better used elsewhere; little need for customization; SaaS alternative exists with comparable features.

Classify as **Replace** if ANY of:
- Architecture Type contains "COTS", "Vendor-Managed", "SaaS", or "Packaged"
- Application is a known commercial product category with mature SaaS alternatives (CRM, HR, ERP, collaboration, email, print management, fax)
- Tech Stack references commercial platforms: SAP, Salesforce, ServiceNow, Dynamics, PeopleSoft, Siebel, Oracle EBS
- Application Owner = external vendor (not internal IT) AND Complexity ≤ Medium — vendor-managed app where SaaS substitution is the natural path

*In 8 Rs mode:* Apps where the legacy system is too outdated and needs full cloud-native redevelopment (not just SaaS replacement) are classified as **Rebuild** instead.

**CAF Guidance:** Consider data migration complexity, user training needs, and process changes. Common scenarios: CRM systems, HR platforms, collaboration tools.

---

#### Step 4: REFACTOR
**CAF Driver:** "Need code changes to reduce technical debt or optimize code for cloud"
**CAF Indicators:** High maintenance costs; significant technical debt; Azure SDKs or services can improve performance/observability; team can apply cloud design patterns.

Classify as **Refactor** if ANY of:
- Integration Count > 20 AND Complexity = "Complex" AND Criticality ≥ High — high-value app benefiting from cloud-native optimization
- Containerized = "Yes" AND Integration Count > 10 — already containerized, extend to cloud-native patterns
- Architecture Type = "N-Tier" AND Complexity = "Complex" AND Integration Count > 10 — candidate for service decomposition
- Tech Stack = modern framework (.NET Core/.NET 5+, Spring Boot, Node.js, React, Angular) AND Complexity = "Complex" — modern stack with high technical debt benefits from cloud design patterns

*In 8 Rs mode:* Apps requiring full architecture redesign (modularization, microservices decomposition, mixed technology stacks, varying scaling needs per component) are classified as **Rearchitect** instead.

**CAF Guidance:** Refactor during migration when the team has the required skills and time. If not, defer modernization and classify as Replatform or Rehost.

---

#### Step 5: REPLATFORM
**CAF Driver:** "Need PaaS solutions and minimal code changes to offload maintenance and facilitate reliability"
**CAF Indicators:** Simplify reliability and disaster recovery; reduce OS and licensing overhead; containerize app; improve time-to-cloud with moderate investment.

Classify as **Replatform** if ANY of:
- Database Platform version is end-of-support or nearing EOS (SQL Server 2012/2014/2016, Oracle 11g, MySQL 5.x) — DB upgrade during migration = Replatform
- Tech Stack = legacy framework requiring upgrade (.NET Framework 2.0–4.8, Java 7/8, Python 2.x, Classic ASP) AND Complexity ≠ "Very Complex"
- OS = end-of-support (Windows Server 2008/2012/R2, CentOS 6–8, RHEL 4–6) AND the app will get an OS upgrade during migration
- Architecture Type = "N-Tier" AND Database Platform = SQL Server AND Complexity = "Medium" — candidate for Azure SQL MI + App Service
- Complexity = "Medium" AND Integration Count between 5–10 — moderate complexity benefits from managed PaaS service adoption

**CAF Guidance:** Choose workloads where PaaS options reduce operational overhead, improve reliability, or simplify disaster recovery. Minimal code refactoring might be necessary.

---

#### Step 6: REHOST (Default)
**CAF Driver:** "Need minimal business disruption and no modernization in near future"
**CAF Indicators:** Workload is stable and Azure-compatible; low-risk migration; short-term cloud adoption goals; no immediate need for modernization; reduce capital expense; free up datacenter space.

All remaining in-scope apps default to **Rehost:**
- Typically Simple/Medium complexity, standard tech stacks, <10 integrations, on supported platforms
- Like-for-like migration: on-premises VMs → Azure VMs, cloud IaaS → Azure IaaS
- Lowest risk, fastest path to cloud

**CAF Guidance:** Don't rehost problematic workloads — rehosting doesn't resolve existing performance, reliability, or architectural issues. Confirm the workload won't require modernization within two years; if it will, prefer Replatform or Refactor to avoid duplicate effort.

---

### Distribution Guidelines

Expected ranges based on typical enterprise portfolios (per CAF patterns). These are guidelines, NOT hard caps:

| Strategy | Expected Range | Rationale |
|----------|---------------|-----------|
| Retire | 5–15% | Low-value/obsolete apps found in most enterprise portfolios |
| Retain | 3–10% | Complex/locked-in workloads requiring deferral or Azure Arc management |
| Replace | 5–15% | COTS/vendor apps with mature SaaS alternatives |
| Refactor | 5–15% | High-value apps benefiting from cloud-native optimization |
| Replatform | 20–35% | Largest modernization opportunity — PaaS with minimal code changes |
| Rehost | 25–40% | Stable workloads suitable for lift-and-shift |

If the distribution falls significantly outside these ranges, review borderline cases:
- **Rehost > 40%:** Check if EOS DB/OS/framework apps were missed for Replatform
- **Replatform < 20%:** Pull EOS database/OS apps from Rehost into Replatform
- **Retire > 15%:** Verify each Retire app truly has no business value or dependencies
- **Replace < 5% but vendor apps exist:** Check for vendor-owned apps that landed in Rehost

### Verification (MANDATORY)
- Sum of all strategy counts MUST = In-Scope total
- If the sum doesn't match, recount. Do NOT adjust numbers to force a total.
- Show math: e.g., "Rehost (247) + Replatform (155) + Refactor (85) + Replace (106) + Retire (78) + Retain (35) = 706 ✓"

### Repeatability Guarantee
Given the same CMDB export with the same field values, this algorithm produces the same numbers every time. Rules are evaluated in strict CAF-aligned priority order (Retire → Retain → Replace → Refactor → Replatform → Rehost). The LLM applies CAF business-driver indicators mechanically — no subjective judgment.

### What Changes Between Runs (and what must NOT)
- **MUST be stable:** The strategy counts for a given CMDB snapshot. Same data = same numbers.
- **MAY change:** Narrative descriptions on each strategy card (wording can improve). Example apps cited. Callout text.
- **MUST NOT change:** The headline count on each card, the verification sum, the relative ordering.

---

## Execution Ownership Classification

### Pillar Orchestration Rules

**Which algorithm(s) to run depends on what workload types are detected in the data:**

| Scenario | Detected Data | Algorithm(s) to Execute | Slide 5b Output |
|----------|---------------|------------------------|------------------|
| **1. Apps only** | CMDB/app portfolio (Application Name, Complexity, Tech Stack, etc.) — no VM inventory, no DB inventory | Run **APP Execution Ownership** algorithm only | Single ownership donut for apps |
| **2. DB only** | DB instance inventory (Engine, Version, Size, etc.) — no app portfolio, no VM data | Run **DATABASE Execution Ownership** algorithm only | Single ownership donut for DB instances |
| **3. Infra only** | VM/server inventory (Hostname, OS, vCPU, RAM, etc.) — no app portfolio, no DB inventory | Run **INFRASTRUCTURE Execution Ownership** algorithm only | Single ownership donut for VMs/servers |
| **4. Mixed (any combination)** | Two or more of the above data types present | Run **each detected pillar's algorithm independently**, then combine | Combined estate donut + per-pillar breakdown table |

**Key rules for mixed scenarios (Scenario 4):**
1. **Each pillar classified independently** — an app's ownership is determined ONLY by the APP algorithm; a DB instance ONLY by the DB algorithm; a VM ONLY by the INFRA algorithm. No cross-contamination.
2. **App-level DB Platform field ≠ separate DB pillar data** — If the app CMDB has a "Database Platform" column (e.g., "Oracle", "SQL Server"), that field is used within the APP algorithm to evaluate app-level ISD / Partner triggers. This is separate from a dedicated DB instance inventory. Both can coexist.
3. **No double-counting** — If a DB instance appears in BOTH an app-level "Database Platform" field AND a standalone DB inventory, classify it once under the DB pillar algorithm only. The app-level reference informs the app's classification but does not create a second DB workload entry.
4. **Combined totals** — The combined estate donut sums all three pillar totals: Total = (Apps in-scope) + (DB instances in-scope) + (VMs in-scope). Factory/ISD / Partner/Unknown are summed across pillars.
5. **Verification** — Each pillar MUST independently verify (F+P+U = pillar total), AND the combined estate MUST verify (sum of all pillar Factories + sum of all pillar Partners + sum of all pillar Unknowns = grand total).

**What if a field is ambiguous between pillars?**
- A CMDB row with Application Name + Database Platform + Host Server = **one app workload** (classify under APP algorithm; the DB Platform and Host Server fields are inputs to the app formula, not separate DB/Infra workloads)
- A standalone DB inventory row (no parent app) = **one DB workload** (classify under DB algorithm)
- A standalone VM inventory row (no parent app, no hosted DB instance) = **one Infra workload** (classify under INFRA algorithm)
- If RVTools shows a VM that hosts both an app AND a DB, it is ONE infra workload for the INFRA algorithm. The app and DB are classified separately under their own algorithms if their own inventory data exists.

---

### Application Pillar — Factory / ISD-Partner / Unknown / No Migration Needed

**CRITICAL:** This algorithm MUST produce identical results given the same input data. The LLM does NOT make judgment calls — it applies the rules below in strict priority order. There are exactly **4 output buckets**: Factory, ISD / Partner, No Migration Needed, Unknown. No other buckets (e.g., "Collaborate") may be invented.

**Step 0: Classify as NO MIGRATION NEEDED first (highest priority — before all other checks):**
An app is **No Migration Needed** if ANY of:
- Application Type = "SaaS" or "SaaS - NOT using On-Prem Components" or any pure SaaS indicator (already cloud-hosted, no on-prem execution)
- Application Type = "Already running in Cloud" or "Already in Cloud" (already migrated)
- These apps require zero migration execution — they are accounted for in the total portfolio but excluded from Factory/ISD / Partner/Unknown workload counts.

**Step 1: Classify as UNKNOWN (checked before Factory/ISD / Partner):**
An app is **Unknown** if ANY of:
- Complexity field is blank/null/missing
- 2+ of these fields are blank: {Complexity, Tech Stack, Integration Count, Application Owner, Architecture Type}
- No Proposed Modernization Phase AND no Pilot Flag (i.e., not in-scope — but if the app IS in-scope and just has bad data, still Unknown)

**Step 2: Classify as ISD / PARTNER (second priority — checked before Factory):**
An app is **ISD / Partner** if ANY ONE of these conditions is true:
- Complexity = "Very Complex" or "Complex"
- Architecture Type = "Vendor" or "COTS" or "Vendor-Managed" (any vendor-supplied indicator) — label these as **ISD / Partner / COTS Vendor** in the detail table
- Tech Stack contains languages/frameworks NOT supported by GHCP automated tooling (i.e., NOT in the Factory-supported list below)
- Database Platform contains "DB2" or "Teradata" or "Informix" (no Factory migration path exists for these engines)
- Database Platform contains "Oracle" AND (version < 12c Release 2 OR version is unknown/blank) — ISD / Partner unless version is confirmed ≥ 12c R2. Oracle 12c R2+ IS Factory-eligible via AI-assisted heterogeneous migration, but eligibility requires version proof.
- Database Platform contains "Oracle" AND workload is E-Business Suite, JD Edwards, PeopleSoft, Siebel, or Enterprise Manager (explicitly excluded from Factory Oracle scope regardless of version)
- Database Platform contains "Sybase"/"SAP ASE" AND (version < 11.9.2 OR version is unknown/blank) — ISD / Partner unless version is confirmed ≥ 11.9.2. SAP ASE 11.9.2+ IS Factory-eligible, but eligibility requires version proof.
- Regulatory field contains "ePHI" AND Criticality >= 4 (Mission Critical with health data = specialized handling)
- Application Owner/BU = vendor name (not internal IT)
- Tech Stack contains "Solaris" or "AIX" or "HP-UX" (legacy platforms requiring re-architecture; mainframe/COBOL/RPG platforms are out of scope for this tool and route to `source-unsupported-escalation`)

**GHCP Factory-Supported Languages & Frameworks (for tech stack evaluation):**
Apps using ANY of these are Factory-eligible from a language perspective:
- **.NET / C#** — ASP.NET, ASP.NET Core, WinForms, WPF, Blazor, .NET MAUI
- **VB.NET** — ASP.NET WebForms, WinForms
- **Java** — Spring Boot, Spring MVC, Jakarta EE, Quarkus, Micronaut, Servlet/JSP, Tomcat 8.5+, JBoss EAP 7.4+, WebSphere, WebLogic (migration FROM these app servers to Azure PaaS is Factory-eligible)
- **JavaScript / TypeScript** — Node.js, Express, Next.js, Angular, React, Vue.js, Svelte
- **Python** — Django, Flask, FastAPI (containerization supported; code/config changes are customer/partner responsibility)
- **PHP** — Laravel, Symfony, WordPress, Drupal
- **Go** — Gin, Echo, standard library (containerization supported; code/config changes are customer/partner responsibility)
- **Ruby** — Rails, Sinatra

**Factory-Supported Container Migration Sources (May 2026):**
On-premises containers, **AWS EKS**, **OpenShift**, **GCP GKE** → AKS, ARO, or Azure Container Apps. Includes migrating current-state architecture to targeted AKS/ACA architecture including network, storage, and policies.

Apps using languages/frameworks NOT in this list (e.g., Perl, Fortran, PowerBuilder, Delphi, Classic ASP/VBScript, Cold Fusion, Lotus Notes/Domino, Progress 4GL) trigger ISD / Partner classification — GHCP does not have automated migration tooling for these stacks.

**Step 3: Everything else is FACTORY (lowest priority — the default for in-scope apps with sufficient data):**
An app is **Factory** if:
- It was NOT classified as Unknown (has sufficient data)
- It was NOT classified as ISD / Partner (none of the ISD / Partner conditions triggered)
- This means: Simple/Medium complexity + internally developed + GHCP-supported language + no exotic DB + no critical compliance burden

**Tie-breaking rules:**
- If an app matches BOTH Unknown and ISD / Partner criteria, classify as **Unknown** (data quality must be fixed first)
- If an app matches ISD / Partner on ONE condition but seems borderline, it is still **ISD / Partner** — the algorithm is intentionally aggressive on ISD / Partner to avoid under-scoping complexity
- The threshold boundaries (>10 integrations, complexity labels, vendor indicators) come from the SOURCE DATA as-is — do NOT re-interpret or soften them

**What "Collaborate" IS (execution model annotation, NOT a classification bucket):**
- Collaborate is a **delivery model note** on the roadmap: "Factory executes with GHCP tooling, ISD / Partner validates and certifies"
- It applies to SOME Factory-classified apps at the complexity boundary (e.g., medium complexity with 6-10 integrations)
- It does NOT change the count. If 339 apps are Factory, they stay 339. A note may say "~X of these will use Collaborate delivery model"
- Never show Collaborate as a separate donut segment, legend item, or appendix row with its own count

**Verification step (MANDATORY before generating the slide):**
- Factory + ISD / Partner + No Migration Needed + Unknown MUST = In-Scope total (e.g., 706)
- If the sum doesn't match, recount. Do NOT adjust numbers to force a total.
- Show your math: "132 + 366 + 227 + 128 = 853 ✓" (or whatever the actual counts are)

**Repeatability guarantee:** Given the same CMDB export with the same field values, this algorithm produces the same 3 numbers every time. If a re-run produces different numbers, the algorithm was not followed.

**Report presentation rules (customer/LT-ready output):**
- **Never mention zero-count platforms** — if no apps use Sybase, Teradata, Informix, etc., do NOT list them with "0 apps". Only mention platforms that actually appear in the data.
- **No internal/meta language** — never use phrases like "New Formula", "Updated Algorithm", "Step-by-Step formula trace", "Pillar Scenario", or "Impact Analysis (New Formula)" in the report. The report is the final deliverable, not a changelog.
- **No algorithm documentation in the report** — the step-by-step classification logic lives in SKILL.md. The report shows the RESULT (counts, criteria summary, verification) but not the internal execution trace.
- **Executive tone** — use "Classification Note" not "Disclaimer"; use "Factory Scope Opportunity" not "Impact Analysis"; use "Recommendation" not "Action". Write for a CIO audience.
- **Cite the source document** once (e.g., "Cloud Accelerate Factory — Service Descriptions, May 2026") without explaining what changed between versions.

---

### Database Pillar — Factory / ISD-Partner / Unknown

Classification rules (when DATABASE data available — DMA, MAP, Azure Migrate DB):

**CRITICAL:** This algorithm MUST produce identical results given the same input data. There are exactly **3 output buckets**: Factory, ISD / Partner, Unknown. Apply rules in strict priority order.

**Step 1: Classify as UNKNOWN first (highest priority):**
A DB instance is **Unknown** if ANY of:
- DB engine/version field is blank/null/missing
- No size data AND no owner AND no migration readiness assessment
- Cannot determine engine type from available fields

**Step 2: Classify as ISD / PARTNER (second priority) — if ANY ONE condition is true:**
A DB instance is **ISD / Partner** if:
- Engine = DB2 (any version) — no Factory migration path exists
- Engine = Teradata or Netezza — requires Synapse/Fabric specialized migration (note: Fabric Warehouse migration IS now a Factory Analytics track for Synapse Dedicated SQL Pool sources)
- Engine = Informix — no automated Azure migration path
- Engine = Oracle AND version < 12c Release 2 (below Factory minimum) AND migration target is NOT Oracle Database@Azure [ODAA] (ODAA has its own Factory track regardless of Oracle version)
- Engine = Oracle AND workload is E-Business Suite, Enterprise Manager, JD Edwards, Middleware, PeopleSoft, Siebel, or Cloud Applications (explicitly excluded from Factory heterogeneous migration — but MAY be Factory-eligible for ODAA lift-and-shift if OCI contract is in place)
- Engine = SAP ASE (Sybase) AND version < 11.9.2 (below Factory minimum)
- Engine = SQL Server AND version < 2012 (below Factory minimum: SQL Server 2012+)
- Engine = PostgreSQL AND version < 9.5 (below Factory minimum)
- Engine = MySQL AND version < 5.6 (below Factory minimum)
- Engine = MariaDB AND version < 10.2 (below Factory minimum)
- Engine = MongoDB AND version < 3.6 (below Factory minimum)
- Engine = Cassandra AND version < 3.11 (below Factory minimum)
- Migration requires SSIS package migration (explicitly out of Factory scope)
- Migration target is Azure SQL Edge (out of Factory scope for DB migration track)
- Migration target is Synapse Analytics — ISD / Partner UNLESS source is Synapse Dedicated SQL Pool migrating to Fabric Warehouse (which IS Factory Analytics scope)
- Any migration path NOT listed in Factory scope documentation

**Step 3: Everything else is FACTORY (default for DB instances with sufficient data):**
A DB instance is **Factory** if it was NOT classified as Unknown or ISD / Partner. This includes:
- **SQL Server 2012+** → Azure SQL DB / Azure SQL MI / SQL Server on Azure VM (via Azure Migrate / DMS)
  - Sources: On-premises, AWS EC2, AWS RDS, GCP Cloud SQL, GCP Compute Engine
  - HA/DR configuration and setup included for Azure SQL DB and Azure SQL MI
- **PostgreSQL 9.5+** → Azure Database for PostgreSQL Flexible Server (via DMS)
  - Sources: On-premises, Azure VM (Win/Linux), AWS EC2, AWS RDS, AWS Aurora, GCP Cloud SQL, GCP Compute Engine
  - Includes EDB and Persona PostgreSQL (excluding EDB/Persona-specific features)
  - HA/DR configuration and setup included
- **MySQL 5.6+** → Azure Database for MySQL Flexible Server (via DMS)
  - Sources: On-premises, Azure VM (Win/Linux), AWS EC2, AWS RDS, AWS Aurora, GCP Cloud SQL, GCP Compute Engine
  - Includes Persona MySQL (excluding Persona features)
  - HA/DR configuration and setup included
- **MariaDB 10.2+** → Azure Database for MySQL Flexible Server (via DMS)
  - Sources: On-premises, Azure VM (Win/Linux), AWS EC2, AWS RDS, GCP Compute Engine
  - HA/DR configuration and setup included
- **MongoDB 3.6+** → Azure Cosmos DB for MongoDB (vCore) (via Spark Utility / Azure Data Studio)
  - Sources: On-premises (Linux/Windows VM), AWS, GCP, AWS DocumentDB, MongoDB Atlas
  - Online (Spark/Azure Data Studio) and Offline (Native Tools/Spark) supported
  - HA/DR configuration and setup included
- **MongoDB (Atlas migration)** → MongoDB Atlas on Azure (via mongosync / Live Migrate)
  - Sources: MongoDB Community/Enterprise Advanced on-premises, Atlas on GCP/AWS
  - Minimum versions: 6.0.17+ for online, 4.2+ for legacy online, 4.2+ for offline
  - HA/DR configuration and setup included
- **Cassandra 3.11+** → Azure Managed Instance for Apache Cassandra (via dual-write proxy / Spark)
  - Sources: On-premises (Linux/Windows VM), AWS, GCP, Azure
  - Online (hybrid cluster/dual-write proxy) and Offline (Apache Spark) supported
  - HA/DR configuration and setup included
- **Oracle 12c R2+** → Azure SQL DB/MI/VM OR Azure Database for PostgreSQL Flexible Server (AI-assisted, via SSMA/Ora2Pg/Striim)
