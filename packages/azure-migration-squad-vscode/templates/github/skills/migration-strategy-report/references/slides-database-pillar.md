# Database-Pillar Slide Specifications — Reference

Slide specs and field references that apply ONLY when the Database pillar is detected. Loaded by the `migration-strategy-report` skill conditionally.

---

## Database Input Fields

#### Database Fields (for DMA, Azure Migrate DB, MAP Toolkit data)
| Field | Description | Example |
|-------|-------------|--------|
| DB Instance Name | Server\instance or cluster name | SQLPROD-01\INST1, pgprod-cluster |
| DB Engine | Database platform and version | SQL Server 2019, PostgreSQL 14.2, Oracle 19c |
| DB Size (GB) | Total database size | 850 GB |
| DB Count on Instance | Number of databases on the instance | 12 |
| HA Configuration | Clustering/replication setup | Always On AG, Log Shipping, Oracle RAC |
| Stored Procedure Count | SP/function complexity indicator | 342 |
| Cross-DB Queries | Whether queries span databases | Yes — joins to FinanceDB |
| Linked Servers | External server links | 3 linked servers (Oracle, DB2) |
| CLR / Extended Features | Platform-specific features used | CLR assemblies, SSIS, SSRS, SSAS |
| Connection Count | Active/max connections | Avg 120, Max 500 |
| Backup Size / RPO | Backup volume and recovery objective | 200 GB / RPO 15 min |
| Apps Dependent on DB | Applications using this database | App1, App2, App3 |
| Target Azure Service | Recommended target (if pre-assessed) | Azure SQL MI, Azure SQL DB, PG Flex |
| Migration Method | Recommended approach | DMS online, Native backup/restore, Replication |
| Migration Readiness | Assessment result (if available) | Ready, Ready with warnings, Not ready |
| Regulatory / Compliance | Data classification | ePHI, PCI, SOX |
| Owner / DBA Team | Responsible team | DBA Team - East, Vendor DBA |

---

## Database Target Service Matrix

Factory-default engine → Azure target mappings (per Cloud Accelerate Factory Service Descriptions, May 2026). See also the full deterministic classification algorithm in `classification-algorithm.md`.

### Engine → Azure Target (Factory scope)

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
  - Sources: On-premises, Azure VM, AWS EC2, AWS RDS, GCP Compute Engine, Oracle Cloud, ODAA
  - Schema conversion supported via SSMA for Oracle, VS Code PostgreSQL extension (integrated with Azure OpenAI)
  - Data migration via SSMA, Ora2Pg, Striim (license provided by Microsoft for large workloads)
  - Estimated 8 weeks per wave
  - **EXCLUDED from Oracle Factory:** E-Business Suite, Enterprise Manager, JD Edwards, Middleware, PeopleSoft, Siebel, Cloud Applications
  - Customer must actively participate in schema conversion and testing

- **SAP ASE (Sybase) 11.9.2+** → Azure SQL DB/MI/VM (AI-assisted, via SSMA for Sybase)
  - Sources: On-premises, Azure VM (Linux/Windows), AWS EC2, GCP Compute Engine
  - Schema conversion via SSMA for Sybase (integrated with Azure OpenAI)
  - HA/DR configuration and setup included

- **Oracle Database@Azure [ODAA]** (May 2026 — new Factory track)
  - Migration of on-premises or any public cloud Oracle database estate to Oracle Database@Azure (Exadata, Exascale, Autonomous, Base DB)
  - Includes scope of infrastructure migration hosting applications connected to Oracle database estate
  - Sources: On-premises, AWS, GCP, Oracle Cloud
  - Customer and OCI must have collaborated in advance; contract and purchase must be completed
  - Explicitly EXCLUDED if customer has signed for OCI CES/LIFT or competing OCI services (requires alignment)

### Factory Analytics Tracks (May 2026 — DB/data workloads)
- **Fabric Lakehouse** migration (Medallion Architecture — new implementation, legacy warehouse migration, or new use case on existing deployment)
  - Valid sources: Azure SQL DB, Azure SQL MI, ADLS Gen2, SQL Server, Oracle (on-premises), Dedicated SQL Pool
- **Fabric Warehouse** migration (from Synapse Dedicated SQL Pool, SQL Server Product Family, Power BI DataMart EOL)
- **Power BI Migration** (SSRS → Power BI, SSAS/AAS → Power BI, Power BI Premium P SKU → Fabric F SKU)
  - Complexity tiers: Simple (18 days), Medium (26 days), High (32 days)

### ISD / Partner scope (NOT Factory-eligible for DB migration)
- DB2 (any version)
- Teradata / Netezza (unless Synapse Dedicated SQL Pool → Fabric Warehouse)
- Informix
- Oracle < 12c R2 (unless targeting ODAA)
- Oracle E-Business Suite, Enterprise Manager, JD Edwards, Middleware, PeopleSoft, Siebel, Cloud Applications (unless targeting ODAA)
- SAP ASE (Sybase) < 11.9.2
- SQL Server < 2012
- PostgreSQL < 9.5
- MySQL < 5.6
- MariaDB < 10.2
- MongoDB < 3.6
- Cassandra < 3.11
- Any migration requiring SSIS package migration
- Migration target = Azure SQL Edge
- Migration target = Synapse Analytics (unless source is Synapse Dedicated SQL Pool → Fabric Warehouse)

### What Factory does NOT cover (ISD / Partner/Customer responsibility)
- Application dependency testing and validation (pre- and post-migration)
- Performing and configuring backups, monitoring, alerts (pre- and post-migration)
- Database performance testing and tuning
- Data archival solutions
- Source environment configuration changes
- Third-party tools setup and configuration
- DB server upgrade/patch management (in-place)
- Any migration path not explicitly listed above

---

## Slide 4b (DB Portion): EOS Impact & ESU Strategy — Databases

Slide 4b is a **dedicated slide** whenever EOS/EOL data is present. The following are the **DB-specific elements** within that slide.

### SQL Server EOS Dates (key reference)
- **SQL Server 2012:** Jul 2022 (ESU expired Jul 2025)
- **SQL Server 2014:** Jul 2024 (ESU via Azure Arc until Jul 2027)

### Three-Tier Action Cards — DB Relevance
- **Orange (ESU bridge available — act now):** SQL Server 2014 instances with active ESU window — deploy Arc ESU as bridge to cover migration timeline
- **Red (No mitigation / ESU expired):** SQL Server 2012 instances (ESU window closed Jul 2025) — must migrate immediately or accept unpatched CVE exposure

### SQL Server Discovery Gap Callout
Include this callout when SQL version data is missing from the inventory:

> **SQL Server Discovery Gap:** SQL Server version data was not present in the source inventory. SQL Server EOS instances cannot be identified without version-level data. Recommend running DMA or Azure Migrate database assessment to capture SQL Server versions across the estate before finalizing the EOS impact count.

### ESU via Azure Arc (Factory delivery)
- Azure Arc ESU enrollment can be completed in approximately 15 days
- Back-charge billing model applies (Arc ESU billed from EOS date, not enrollment date)
- SQL Server 2014 ESU window: active until Jul 2027

---

## Slide 4e: Database Migration Strategy

This is a **conditional slide** — include when database instance inventory data is detected (DMA output, Azure Migrate DB assessment, MAP Toolkit, or any DB inventory with engine/version/size fields). For pure app-centric reports with no DB-level data, the existing tech stack and obsolescence slides cover DB platforms at a summary level.

**Data sources that trigger this slide:**
- Data Migration Assistant (DMA) output (JSON/CSV)
- Azure Migrate database assessment
- MAP Toolkit database inventory
- Manual DB inventory spreadsheet with instance-level data
- CMDB with dedicated DB fields (engine, version, size, HA config)

**Content structure:**
- **4 KPI cards:** Total DB Instances, Total Databases, Total Data Volume (TB), Migration-Ready % (from DMA/assessment)
- **Database Engine Distribution:** Horizontal bar chart
  | Engine | Instance Count | DB Count | Total Size (TB) | Azure Target |
  |--------|---------------|----------|-----------------|-------------|
  | SQL Server (by version) | n | n | n TB | Azure SQL DB / MI / VM |
  | PostgreSQL | n | n | n TB | Azure DB for PostgreSQL Flex |
  | MySQL / MariaDB | n | n | n TB | Azure DB for MySQL Flex |
  | Oracle | n | n | n TB | ISD / Partner scope (OCI interconnect / Oracle on Azure VMs / refactor to PG) |
  | DB2 | n | n | n TB | ISD / Partner scope (refactor to PG/SQL) |
  | MongoDB | n | n | n TB | Cosmos DB for MongoDB / Azure managed |
  | Cassandra | n | n | n TB | Cosmos DB for Apache Cassandra |
  | Other (Teradata, Sybase, Informix) | n | n | n TB | Assessment needed |
- **SQL Server Target Selection Matrix (when SQL Server data exists):**
  | Decision Factor | Azure SQL DB | Azure SQL MI | SQL Server on Azure VM |
  |----------------|-------------|-------------|----------------------|
  | Cross-DB queries / Linked servers | ❌ | ✅ | ✅ |
  | CLR assemblies | ❌ | ✅ (limited) | ✅ |
  | SSIS / SSRS / SSAS | ❌ | ❌ (use ADF/PBI/AAS) | ✅ |
  | SQL Agent jobs | ❌ (use Elastic Jobs) | ✅ | ✅ |
  | Always On AG | ❌ (use geo-replication) | ✅ | ✅ |
  | DB size > 16 TB | ❌ (Hyperscale) | ✅ (up to 16 TB) | ✅ |
  | Max compatibility | Low | High | Full |
  | Mgmt overhead | None (PaaS) | Low (PaaS) | High (IaaS) |
  - Map each instance to recommended target based on feature usage
- **Migration Method per Instance:**
  | Instance | Engine | Size | Target | Method | Estimated Downtime |
  |----------|--------|------|--------|--------|-------------------|
  - DMS Online (near-zero downtime) vs DMS Offline vs Native backup/restore vs Replication vs Export/Import
  - Flag instances requiring offline window and estimated duration
- **Schema Complexity & Blockers (when DMA/assessment data exists):**
  - Count of instances with migration blockers (breaking changes)
  - Count of instances with warnings (behavioral changes)
  - Top blocker categories: unsupported features, deprecated syntax, CLR dependencies, cross-DB references
  - Remediation effort estimate per blocker category
- **Data Gravity Analysis:**
  - **Shared databases:** DBs serving 3+ applications — these drive move group sequencing
  - **Data warehouse / reporting DBs:** Large analytical stores that many apps query — consider replication strategy
  - **Cross-database dependencies:** Instances with linked servers or cross-DB queries — must co-migrate or refactor
  - Visual: table showing DB instance → dependent apps → shared-DB flag → migration constraint
- **HA/DR Mapping:**
  | Current HA Config | Instance Count | Azure Equivalent | Migration Complexity |
  |------------------|---------------|-----------------|---------------------|
  | Always On AG | n | SQL MI AG / VM AG | Medium |
  | Log Shipping | n | SQL MI auto-backup / VM log shipping | Low |
  | Replication | n | Azure SQL geo-replication | Medium |
  | Oracle RAC | n | ISD / Partner scope — Oracle on Azure VMs or refactor | High |
  | No HA | n | Add Azure HA (auto-failover groups, zone redundancy) | Low |
- **Performance Tier Recommendations (when utilization data exists):**
  - DTU vs vCore model recommendation per instance
  - Elastic Pool candidates (multiple small DBs from same app family)
  - Read replica needs for reporting workloads
  - Estimated monthly cost range per target service

**Key Principle:** This slide answers: *"How many databases do we have, where are they going in Azure, what's the migration method for each, and what blockers need remediation before we move?"*

---

## Slide 2 (Variant C): Portfolio Overview — Database Estate Only

Use this slide variant when the **DB pillar is detected WITHOUT Apps or Infra**.

- **4 KPI cards:** Total DB Instances, Total Databases, Total Data Volume (TB), Migration-Ready % (from DMA/assessment, or "Assessment Pending" if not yet run)
- **By Engine:** horizontal bar chart — SQL Server | PostgreSQL | MySQL | Oracle | DB2 | MongoDB | Other
- **By Migration Readiness:** bar chart — Ready | Ready with Warnings | Not Ready | Not Assessed
- **By HA Configuration:** bar chart — Always On AG | Log Shipping | Replication | Oracle RAC | No HA
- *Note: Slide 4e (Database Migration Strategy) provides the deep-dive; this slide is the executive summary.*
