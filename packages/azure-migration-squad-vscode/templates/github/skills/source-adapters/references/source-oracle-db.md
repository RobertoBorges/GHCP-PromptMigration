# Skill: Source Adapter — Oracle Database (Stub)

> **Stub adapter.** Provides recognition + escalation guidance. For deep migration, pair with a partner or extend this skill into a full adapter.

## Overview

Characterizes an Oracle Database backing the application — schemas, PL/SQL packages, RAC clusters, partitioning, links, security, on-prem vs cloud.

## When to Use

Oracle DB is the primary or secondary datastore; or the user runs Oracle Forms / Reports / APEX / Oracle EBS

## Inputs

- Oracle connection (read-only): SID/service name, host, port
- Or DBA-supplied AWR/ADDM reports, schema exports
- DB version + edition (SE / EE / XE), patch level
- License model (per-core / per-NUP / cloud-bring-your-own / ULA)

## Probes

- `SELECT * FROM v` → version + edition
- `SELECT * FROM dba_users` → schema inventory
- `SELECT owner, count(*) FROM dba_objects GROUP BY owner, object_type` → schema size
- `SELECT * FROM dba_db_links` → cross-DB dependencies
- `SELECT * FROM dba_directories` → file system mounts referenced by PL/SQL
- `SELECT * FROM dba_jobs / dba_scheduler_jobs` → in-DB schedulers
- `SELECT * FROM dba_segments WHERE bytes > 1e9 ORDER BY bytes DESC` → largest tables
- `SELECT * FROM dba_indexes` → index strategy
- `SELECT * FROM dba_constraints` → FK + check constraints
- `SELECT * FROM dba_triggers` → DB-side logic
- `SELECT * FROM dba_source WHERE type='PACKAGE BODY'` → PL/SQL business logic surface
- `SELECT * FROM dba_advanced_replication` / GoldenGate config → replication topology
- `SELECT * FROM v` → backup posture

## Target Azure Mapping (signals only — Architect decides)

| Oracle today | Azure candidate |
|--------------|-----------------|
| Oracle DB (SE/EE) — keep Oracle | **Oracle Database Service for Azure (ODSA)** — Oracle Cloud collocated in Azure |
| Oracle DB — keep Oracle on VMs | Azure VMs with Oracle BYOL or Marketplace |
| Oracle DB — migrate off Oracle | Azure SQL DB / MI (T-SQL refactor) |
| Oracle DB — migrate off Oracle | PostgreSQL Flexible Server (Ora2Pg + manual PL/SQL refactor) |
| Oracle XE | Azure SQL Free tier / PostgreSQL |
| Oracle EBS | Lift to Azure VMs (BYOL); or migrate to Oracle Fusion Cloud |
| Oracle APEX | Keep APEX on ODSA / VMs |

## Risks / Constraints

- **PL/SQL business logic.** Often dozens of packages — refactor decision (DB tier vs app tier) per package.
- **Database links** to other Oracle DBs — chain may need migration in sequence.
- **Oracle-specific features:** Partitioning, Advanced Compression, Advanced Security, Spatial, Text — each has license cost; replace or replicate in target.
- **License model** — Oracle on Azure is allowed but counted; Cost Engineer must review BYOL implications.
- **Data Guard / GoldenGate / Streams replication** — replication topology may include systems out of scope.
- **Character set differences** (AL32UTF8 vs WE8MSWIN1252) can break data on conversion.
- **NUMBER precision vs SQL Server NUMERIC / Postgres NUMERIC** — silent precision loss possible.

## Output Checklist

- [ ] Source environment identified
- [ ] Available access method captured
- [ ] Existing inventory or export captured
- [ ] Risks flagged for Architect + Cost Engineer review
- [ ] Escalation path decided (if applicable)
- [ ] Confidence label set on `source.evidence_confidence`