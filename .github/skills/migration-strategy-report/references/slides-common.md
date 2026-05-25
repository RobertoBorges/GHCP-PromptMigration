# Common Slide Specifications — Reference

Slide specs that apply to ALL pillars (Applications / Databases / Infrastructure) or cross-cut multiple pillars. Always loaded by the `migration-strategy-report` skill.

## Slide 1: Title / Cover

- Organization name, "Application Portfolio Migration Strategy", "Enterprise Modernization Roadmap", date, confidentiality

## Slide 2: Portfolio Overview (KPI Cards)

This slide adapts its KPI cards and charts based on the detected workload pillars. Use the variant that matches the data:

**Variant A — Application Portfolio (when Apps pillar detected):**
- 4 KPI cards: **Total Portfolio**, **In-Scope for Migration**, Primary DB Dependent (among in-scope), Mission Critical (among in-scope)
- Clearly label which number is total vs. in-scope
- By Criticality: bar chart (levels 1–4) — for in-scope apps
- By Architecture: bar chart (Client/Server, Web, N-Tier, Platform, Desktop) — for in-scope apps

**Variant B — Infrastructure Estate (when Infra pillar detected WITHOUT Apps):**
- 4 KPI cards: **Total Servers/VMs**, **Powered-On (Active)**, **Physical vs Virtual split**, **Total Compute** (aggregate vCPU & RAM)
- By Environment: bar chart — Prod | Dev/Test | DR | Unknown
- By Hypervisor: donut chart — VMware ESXi | Hyper-V | KVM | Physical | Other
- By OS Family: bar chart — Windows Server (by version) | RHEL | Ubuntu | CentOS | SLES | Other
- *Note: Slide 4c (Infrastructure Discovery & Sizing) provides the deep-dive; this slide is the executive summary.*

**Variant C — Database Estate (when DB pillar detected WITHOUT Apps or Infra):**
- 4 KPI cards: **Total DB Instances**, **Total Databases**, **Total Data Volume (TB)**, **Migration-Ready %** (from DMA/assessment, or "Assessment Pending" if not yet run)
- By Engine: horizontal bar chart — SQL Server | PostgreSQL | MySQL | Oracle | DB2 | MongoDB | Other
- By Migration Readiness: bar chart — Ready | Ready with Warnings | Not Ready | Not Assessed
- By HA Configuration: bar chart — Always On AG | Log Shipping | Replication | Oracle RAC | No HA
- *Note: Slide 4e (Database Migration Strategy) provides the deep-dive; this slide is the executive summary.*

**Variant D — Mixed (when multiple pillars detected):**
- **6 KPI cards** in a 3×2 grid to give leadership the full estate picture at a glance:
  | Row | Card 1 | Card 2 |
  |-----|--------|--------|
  | **Apps** | Total Applications | In-Scope for Migration |
  | **Infra** | Total Servers/VMs | Powered-On (Active) |
  | **Databases** | Total DB Instances | Total Data Volume (TB) |
  - If only 2 pillars are detected, use a 2×2 grid (4 cards) picking the 2 most important KPIs per pillar
- **Scope Summary callout** below the KPI grid: "This engagement covers X applications, Y servers/VMs, and Z database instances across N datacenters"
- By Criticality: bar chart (from Apps data) — provides the risk lens leadership cares about
- **Cross-Pillar Linkage callout** (when data supports): "X% of in-scope apps depend on Y database instances running on Z servers" — connects the three pillars into a single migration story
- The conditional slides (4c, 4d, 4e) provide the Infra/DB deep-dives — this slide is the unified executive summary

## Slide 5b: Execution Ownership

- Donut chart: **Up to 4 segments** — Factory vs ISD / Partner vs No Migration Needed vs Unknown. The "No Migration Needed" segment appears only when SaaS or Already-in-Cloud apps exist in the portfolio.
- Detailed breakdown table: scope category | VM/app/DB count | Factory service name | migration method
- Detail columns: Factory (count) | ISD / Partner (count) | No Migration Needed (count, when applicable) | Unknown (count) — with criteria and risks
- **COTS Vendor labeling:** When apps are classified as ISD / Partner due to COTS/Vendor/Vendor-Managed Application Type, label the bucket as **"ISD / Partner / COTS Vendor"** in the detail table to distinguish vendor-managed apps from other ISD / Partner triggers.
- **OPTIONAL callout:** "Collaborate delivery model" note explaining that ~X Factory apps at complexity boundary will use Factory-executes + ISD / Partner-validates approach. This is informational — it does NOT create an additional segment or change any counts.
- **REQUIRED:** disclaimer note about classification source and bucket fluidity
- **REQUIRED:** cite the source document used for Factory eligibility (e.g., "Cloud Accelerate Factory — Service Descriptions, May 2026")
- **REQUIRED:** verification line showing math: "Factory + ISD / Partner + No Migration Needed + Unknown = Total In-Scope ✓"

**Rendering by scenario (how Slide 5b adapts to the detected workload type):**

| Scenario | What to show on Slide 5b |
|----------|-------------------------|
| **Apps only** | Single donut — APP ownership (Factory/ISD / Partner/No Migration Needed/Unknown). Verification: counts sum to total in-scope apps. |
| **DB only** | Single donut — DB ownership (Factory/ISD / Partner/Unknown). Verification: counts sum to total DB instances. |
| **Infra only** | Single donut — INFRA ownership (Factory/ISD / Partner/Unknown). Verification: counts sum to total VMs/servers. |
| **Mixed (2+ pillars)** | **Combined estate donut** showing TOTAL Factory/ISD / Partner/No Migration Needed/Unknown across ALL detected pillars, PLUS a **per-pillar breakdown table** showing each pillar's split independently. Verification: each pillar sums correctly AND combined total = sum of all pillar totals. |

For mixed scenarios, the per-pillar breakdown table format:
| Pillar | Total In-Scope | Factory | ISD / Partner | No Migration Needed | Unknown | Verification |
|--------|---------------|---------|---------|---------|---------|-------------|
| Applications | N | n | n | n | n | n+n+n+n = N ✓ |
| Databases | N | n | n | 0 | n | n+n+0+n = N ✓ |
| Infrastructure | N | n | n | 0 | n | n+n+0+n = N ✓ |
| **Combined Estate** | **N** | **n** | **n** | **n** | **n+n+n = N ✓** |

## Slide 6: Phased Migration Roadmap

- Bar chart: app count per phase (height proportional)
- Summary table: phase, count, focus, complexity, characteristics

## Slide 6b: Dependency Mapping

This is a **conditional slide** — include ONLY when dependency or integration data is present in the portfolio (CMDB integration count field, architecture diagrams, dependency maps, middleware/ESB documentation, meeting notes referencing integration patterns, OR cross-pillar data linking applications to databases and infrastructure). **Do NOT include if no dependency evidence exists.**

This slide provides a **unified full-estate dependency view** — mapping dependencies across all pillar combinations: app-to-app, app-to-database, app-to-infrastructure, app-to-external, infra-to-infra, and DB-to-DB. It is the single source of truth for "what depends on what" across all workload pillars.

**Data sources that trigger this slide:**
- CMDB field: Integration Count > 0 for multiple apps
- Architecture diagrams showing system interconnections
- Dependency maps (application-to-application, application-to-database, application-to-infrastructure, application-to-external)
- Middleware/ESB documentation (BizTalk, MuleSoft, Cloverleaf, TIBCO, IBM MQ, Kafka, etc.)
- Meeting notes referencing integration patterns, APIs, or data flows
- Cross-pillar linkage data (which apps use which DB instances, which apps run on which servers/VMs)
- Cross-cloud service dependencies (for cloud-to-cloud migrations: which services call which other services)
- Infrastructure dependency data (VM clustering, shared storage, load balancer → backend pool, DNS dependencies, network topology)
- Database dependency data (linked servers, replication chains, cross-database queries, ETL pipelines between instances, Always On AG, log shipping)

**Content structure:**
- **KPI cards (top):** Total Dependency Points (sum across portfolio — integrations + DB dependencies + infra dependencies), High-Fan-Out Apps (apps with 10+ dependencies), Dependency Hubs/Middleware Platforms count, External/Third-Party Dependencies count
- **Dependency Topology Map:** Visual representation (table or grouped layout) showing:
  - **Hub applications** — apps that many others depend on (highest inbound connection count)
  - **High-fan-out applications** — apps that connect to many downstream systems (highest outbound count)
  - **Middleware/ESB layer** — platforms routing traffic between workloads (BizTalk, MuleSoft, Cloverleaf, etc.) with app counts flowing through each
  - **External dependencies** — connections to vendor systems, SaaS platforms, partner APIs, regulatory feeds
- **Cross-Pillar Dependency View (when mixed-pillar data exists):**
  - **App → Database:** Which applications depend on which DB instances (shared vs. dedicated). Drives data migration sequencing.
  - **App → Infrastructure:** Which applications run on which servers/VMs (when server-to-app mapping exists). Drives VM migration wave planning.
  - **App → External/Cloud Services:** Which applications depend on source-cloud-specific services that must be migrated or replaced (for cross-cloud scenarios)
  - **Infra → Infra:** VM clustering dependencies (failover clusters, shared storage arrays, load balancer → backend pool bindings), network dependencies between servers (DNS, NFS mounts, NIC teaming), hypervisor-level affinity/anti-affinity rules. Drives infrastructure wave sequencing — shared storage must move before dependent VMs.
  - **DB → DB:** Linked servers (cross-instance queries), replication chains (Always On AG, transactional replication, log shipping, merge replication), cross-database queries within an instance, ETL/SSIS pipelines between DB instances, database mirroring. Drives database migration ordering — publisher must move before subscriber, or replication must be re-established post-migration.
  - Format: Entity | Depends On | Dependency Type | Migration Constraint | Impact if Broken
- **Cross-Workload Dependency Table:** Top 15–20 most-connected apps showing:
  - Application Name | Integration Count | Dependent DBs | Host Infrastructure | Key Connected Systems | Migration Impact (High/Med/Low)
  - Sort by total dependency count descending
- **Migration Sequencing Implications callout:**
  - Which apps MUST migrate together (tight coupling — shared DBs, real-time integrations)
  - Which dependencies create phase-gate constraints (App B can't move until App A's DB is migrated)
  - Which middleware platforms need parallel migration tracks
  - Which infrastructure must move first to unblock application waves
  - Which DB instances must migrate together due to replication chains or linked server dependencies
  - Which VM clusters must move as a unit due to shared storage or failover group membership
- **Dependency Risk Summary:**
  - Count of apps sharing databases (data-level coupling)
  - Count of real-time vs. batch integrations (real-time = higher migration risk)
  - Count of apps with cross-pillar dependencies spanning 3+ layers (app + DB + infra = complex)
  - Count of undocumented/tribal-knowledge dependencies (if data quality flags exist)
  - Count of cross-cloud service dependencies that require dual-run during transition (for cloud migrations)
  - Count of DB instances in replication chains (must migrate in coordinated sequence)
  - Count of VMs in shared-storage clusters (must migrate as unit or re-architect storage first)

**Key Principle:** This slide answers the leadership question: *"What depends on what across our entire estate, and what breaks if we move one piece without the others?"* — it provides the unified dependency view that drives migration wave sequencing, move group formation, and risk assessment across all workload pillars.

## Slide 6c: Move Group Recommendations

This is a **conditional slide** — include when enough relationship data exists to cluster applications into co-migration groups. Requires integration data PLUS at least two of: shared-database information, business capability mapping, criticality ratings, phase assignments, or infrastructure/server data. **Do NOT include if only a flat app list exists with no relationship signals.**

A **Move Group** is a cluster of applications that should migrate together in the same wave because decoupling them would cause outages, data inconsistency, or broken business processes. This slide translates the raw dependency data from the Dependency Mapping slide (6b) into actionable migration execution units.

**Data sources used to form Move Groups (priority order):**
1. **Integration coupling** — apps sharing 5+ integrations with each other form a natural group
2. **Shared databases** — apps reading/writing the same DB instance MUST move together or have a replication strategy
3. **Business process chains** — apps in the same end-to-end workflow (e.g., Order → Billing → Collections) should co-migrate
4. **Common infrastructure** — apps on the same server cluster, same middleware bus, or same vendor platform
5. **Criticality alignment** — avoid mixing Mission Critical and Low-criticality apps in one group (different testing/rollback requirements)
6. **Vendor cohesion** — vendor-managed apps from the same vendor often share licenses, support windows, and upgrade paths

**Move Group Formation Algorithm (for agent):**
1. Start with the highest-integration apps (>20 connections) — each becomes a group anchor
2. Pull in all directly-connected apps that share databases or tight real-time integrations
3. Merge overlapping groups (if App A and App B are both anchors but share 3+ common dependencies, merge into one group)
4. Assign remaining apps to groups by business capability affinity, then by shared infrastructure
5. Apps with <5 integrations and no shared databases can be standalone ("independent movers")
6. Cap group size at 15-25 apps for execution manageability — split larger clusters into sub-groups with a defined migration sequence

**Content structure:**

- **KPI cards (top):** Total Move Groups identified, Largest Group size, Independent Movers (apps safe to migrate solo), Cross-Group Dependencies (links between groups that create sequencing constraints)

- **Move Group Summary Table:**
  | Group ID | Group Name | App Count | Anchor App(s) | Primary Domain | Binding Factor | Recommended Phase | Migration Risk |
  |----------|-----------|-----------|---------------|----------------|----------------|-------------------|----------------|
  - **Group Name:** descriptive label based on the binding factor (e.g., "Revenue Cycle SQL Cluster", "Clinical Integration Hub", "Facilities Vendor Suite")
  - **Anchor App(s):** the 1-2 highest-integration apps that define the group
  - **Binding Factor:** what ties the group together (shared DB, integration bus, vendor platform, business process)
  - **Recommended Phase:** which migration phase this group best fits (align with Slide 6 roadmap)
  - **Migration Risk:** High (tight coupling + mission critical), Medium (moderate coupling), Low (loose coupling + simple)
  - Sort by Migration Risk descending, then App Count descending
  - Show top 10-15 groups; summarize remaining as "N additional small groups (2-4 apps each)"

- **Move Group Dependency Map (visual or table):**
  Show which groups have cross-dependencies (Group A must complete before Group B can start). This drives wave sequencing beyond individual app dependencies.
  - Format: table with Group ID | Depends On | Dependency Type (data, integration, infrastructure) | Sequencing Impact (hard blocker vs. soft preference)

- **Independent Movers section:**
  - Count of apps with <5 integrations, no shared databases, and simple/medium complexity
  - These are "wave fillers" — can be added to any phase to balance workload without dependency risk
  - Callout: "N apps identified as independent movers — can be scheduled flexibly to balance wave capacity"

- **Move Group Sizing & Wave Alignment callout:**
  - Map each group to a migration phase from Slide 6
  - Flag groups that are too large for a single wave (>25 apps) and suggest sub-group splits
  - Flag cross-phase dependencies (Group X in Phase 2 depends on Group Y in Phase 4 — sequencing conflict)
  - Recommend wave capacity: "Target 30-50 apps per wave; each wave should contain 2-4 complete move groups plus independent movers as backfill"

- **Key Risks & Recommendations callout:**
  - Groups with Mission Critical anchors need extended testing windows
  - Groups spanning multiple vendors require coordinated change windows
  - Groups with shared databases need data migration strategy decided upfront (lift-and-shift DB first, or replicate?)
  - Undiscovered dependencies (from the 39.9% with no integration data) may merge or split groups during execution — build 20% buffer in wave capacity

**Key Principle:** This slide answers the leadership question: *"Which apps move together, in what order, and why?"* — it converts raw dependency analysis into a concrete migration execution plan that program managers can schedule against.

## Slide 10: Key Risks & Dependencies

- 6 risk cards (High/Red + Medium/Yellow mix)
- Each risk MUST be data-backed (cite counts, percentages, or specific technologies from the CMDB)
- Always evaluate these risk dimensions against the data (include if evidence exists):
  1. **Regulatory & Compliance** — SOX, HIPAA/ePHI, PCI, audit trail requirements; count regulated apps
  2. **Integration Layer Complexity** — middleware/ESB backbone (Cloverleaf, BizTalk, MuleSoft, etc.); apps with 20+ integrations
  3. **Vendor/Third-Party Dependency** — vendor-owned apps requiring vendor cooperation for migration timelines
  4. **Data Gravity & Platform Lock-in** — large databases (Teradata, DB2, EDW, Oracle RAC) that many apps depend on
  5. **EOL/Security Exposure** — obsolete OS/DB/middleware creating active CVE or compliance risk
  6. **Skill & Organizational Readiness** — cloud-native skill gaps, undefined ownership, change management gaps
  7. **Migration Complexity** — apps with extreme server counts, mixed DB dependencies, or legacy tech stacks
  8. **Data Quality / Discovery Gaps** — missing CMDB fields, unknown classifications, BU ownership gaps
- Pick the top 6 most impactful for THIS customer (3 High, 3 Medium). Not all 8 will apply every time.
- 3 Critical Success Factors (actionable, tied to the identified risks)

## Slide 11: Recommended Next Steps

- Action table: 6–8 actions with Owner, Timeline, Expected Outcome
- Decision Required banner

## Slide 12: Appendix — Portfolio Summary Statistics

- Three columns: by phase, by complexity + containerization, by regulatory + server footprint
