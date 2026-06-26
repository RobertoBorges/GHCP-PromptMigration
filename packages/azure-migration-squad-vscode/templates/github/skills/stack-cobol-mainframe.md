# Skill: Stack Adapter — COBOL / Mainframe

> Stack adapter for COBOL applications running on mainframe (z/OS, IBM i / AS400) or distributed (Micro Focus, GnuCOBOL, OpenCobolIDE) targeting Azure migration.

> **High-risk path.** This adapter almost always pairs with `source-mainframe` and triggers the `Architect` + `Cost Engineer` + `Database Specialist` for escalation.

## When to Use

- `stack.primary_stack: cobol-mainframe` in the Capability Matrix
- File evidence: `*.cbl`, `*.cob`, `*.cpy` (copybooks), `*.jcl`, BMS maps, IMS DBDs / PSBs
- User describes batch jobs, CICS transactions, COBOL programs, JCL jobs

## Sub-Stack Detection

| Sub-stack | Detection signal | Typical migration target |
|-----------|------------------|--------------------------|
| **z/OS COBOL with CICS** | `EXEC CICS` statements; BMS maps; PCT/PPT/FCT references | Replatform to Java/.NET on AKS via Micro Focus/Astadia, OR rewrite |
| **z/OS COBOL batch (JCL only)** | `*.jcl` files; SORT, IDCAMS utility calls; DD statements | Container Apps Jobs + Java/.NET; OR Azure Batch |
| **z/OS COBOL with IMS DB** | DBD / PSB files; `DLI` calls | Refactor IMS to Db2 LUW → Azure SQL / PostgreSQL |
| **z/OS COBOL with Db2** | `EXEC SQL` blocks; DCLGEN copybooks | Refactor to Azure SQL / PostgreSQL (schema-equivalent) |
| **z/OS COBOL with VSAM** | `SELECT ... ASSIGN TO ...` with `ORGANIZATION IS INDEXED|SEQUENTIAL|RELATIVE`; KSDS/ESDS/RRDS | Migrate to Azure SQL / Blob (depends on access pattern) |
| **IBM i (AS/400) RPG + COBOL** | `*.rpgle`, `*.sqlrpgle`; DDS files; SAVF | Often rewrite to .NET/Java; or keep on Power VS / Skytap on Azure |
| **Micro Focus COBOL** | Visual COBOL solution files (`*.app`); `*.idy` | Replatform to AKS using Micro Focus Enterprise Server on Azure |
| **GnuCOBOL / OpenCOBOL** | `cobc` build; Linux runtime | Container Apps with OpenCOBOL runtime |

## Probes

### Source inventory

1. Count `*.cbl` / `*.cob` files
2. Count `*.cpy` (copybooks) — shared data definitions
3. Count `*.jcl` files
4. Count BMS maps (`*.bms`, `*.bmsout`)
5. Count IMS DBDs / PSBs
6. Identify SQL precompiler usage (Db2 `EXEC SQL`)

### Program characterization (per main program)

- Program ID: `IDENTIFICATION DIVISION. PROGRAM-ID. <name>.`
- Storage: `WORKING-STORAGE`, `LINKAGE`
- Files: `FILE-CONTROL` `SELECT` entries → VSAM / sequential / Db2 references
- I/O: `READ` / `WRITE` / `OPEN` / `CLOSE`
- DB: `EXEC SQL ... END-EXEC` blocks → Db2 statements
- CICS: `EXEC CICS ... END-EXEC` blocks → BMS RECEIVE/SEND, READ/WRITE TS/TD queues
- IMS: `CALL "CBLTDLI" USING ...` → DLI calls
- Subroutine calls: `CALL "OTHER-PGM" USING ...` → program graph

### JCL inventory

For each `*.jcl`:

- Job statements (`//JOBNAME JOB ...`)
- Step PROC / EXEC PGM=
- DD statements (input/output datasets)
- COND codes
- IDCAMS / SORT / FTP utility steps
- SYSIN parameter blocks

Captures the **operational topology** — what runs at what time with what data.

### Data access

- VSAM: KSDS (keyed), ESDS (entry-sequenced), RRDS (relative)
- Sequential files (QSAM / BSAM)
- PDS / PDSE members
- Db2 tables (DCLGEN copybooks reveal schemas)
- IMS hierarchical (DBD reveals structure)
- GDG datasets (generation data groups)

### Scheduling

- z/OS: TWS / Control-M / OPC / IBM Workload Scheduler → captures cron-like topology
- IBM i: Job schedulers
- Distributed Micro Focus: cron / systemd / Windows Task Scheduler

### Security

- RACF (z/OS), Top Secret, ACF2 → identity sources for the batch / online users
- IBM i: object-level + program adoption

### Integration

- MQ Series → external messaging
- SOAP / REST adapters (sometimes via Connect:Direct, FTP, NDM)
- File-based interfaces (drop directories on USS for z/OS)

## Phase 2 Effort Mapping

Mainframe migrations are **always L or XL** in Phase 2 effort. The choice is between:

| Approach | Effort | Risk | When |
|----------|--------|------|------|
| **Replatform via emulator (Micro Focus / Astadia / TmaxSoft / Heirloom)** | L | Medium | Source COBOL preserved; runs on AKS; faster time-to-Azure |
| **Refactor to Java (transformer tools)** | XL | High | Want to escape COBOL skill dependency; multi-quarter project |
| **Rewrite (greenfield)** | XL | High | Business logic well-understood, willing to rebuild |
| **Retire / consolidate** | n/a | n/a | When app is duplicative |

## Identity Modernization

| Today | Target |
|-------|--------|
| RACF / Top Secret / ACF2 | Federation to Entra ID; or Entra ID + custom mapping layer |
| 3270 terminal sessions | Web UI rewrite (in Phase 2); Entra ID OIDC at the edge |
| IBM i object-level | Entra ID + Azure AD app role mapping |

## Data Migration

| Source | Target candidate |
|--------|------------------|
| Db2 z/OS | Azure SQL DB / MI (after schema review) or PostgreSQL Flexible Server |
| Db2 LUW | Azure SQL DB / MI or PostgreSQL |
| IMS hierarchical | Refactor to relational (Azure SQL / PostgreSQL); document the transformation |
| VSAM KSDS | Azure SQL (table per file) or Cosmos DB (key-value) |
| VSAM sequential | Blob Storage (cold/hot tier per use) |
| GDG datasets | Blob Storage with naming convention + lifecycle policy |
| QSAM datasets | Blob Storage |

Use **Azure DMS** when possible; for IMS / VSAM, expect custom ETL.

## Target Azure Mapping

| Approach | Compute | Notes |
|----------|---------|-------|
| Micro Focus Enterprise Server | AKS | Vendor-validated; preserves COBOL |
| Astadia FastTrack | AKS or VMs | Transforms COBOL to Java + AKS deployment |
| Heirloom Computing | AKS | Java conversion approach |
| TmaxSoft OpenFrame | AKS or VMs | Emulator approach |
| Greenfield Java rewrite | AKS or Container Apps | Standard cloud-native; long timeline |
| Greenfield .NET rewrite | AKS or Container Apps | Same as above with .NET stack |

## Anti-Patterns

- Don't recommend "lift-and-shift to Azure VMs running z/OS" — z/OS does not run on Azure compute.
- Don't promise "we'll move IMS to Cosmos DB in Phase 2." IMS-to-relational is its own multi-month workstream.
- Don't ignore JCL — it carries scheduling and data lineage. Treat each JCL as a job spec.
- Don't ignore copybooks. They define shared record structures across programs — a single copybook can affect dozens of programs.
- Don't try to dispatch the Coder before the Architect. This is one of the few migrations where Architect runs Phase 2 design before any code change.
- Don't migrate GDG datasets to fixed-name blobs. Preserve the generation pattern via naming + lifecycle rules.

## Output Checklist

- [ ] Sub-stack identified (one of the 8 above)
- [ ] COBOL program count + LOC captured
- [ ] Copybook count captured
- [ ] JCL inventory captured (job names + schedule)
- [ ] CICS / IMS / Db2 / VSAM usage characterized
- [ ] Subroutine call graph approximated
- [ ] Scheduler captured (TWS / Control-M / OPC / etc.)
- [ ] Security model captured (RACF / Top Secret / ACF2)
- [ ] Integration points captured (MQ, file-based, web services)
- [ ] Data migration strategy outlined per source
- [ ] Vendor / emulator approach options captured
- [ ] Phase 2 effort label assigned (always L or XL)
- [ ] Target Azure compute approach noted
- [ ] Architect + Cost Engineer + Database Specialist all flagged as required
