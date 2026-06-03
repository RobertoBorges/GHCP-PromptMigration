# Skill: Source Adapter — Mainframe (z/OS, IBM i, Unisys) (Stub)

> **Stub adapter.** Provides recognition + escalation guidance. For deep migration, pair with a partner or extend this skill into a full adapter.

## Overview

Characterizes a mainframe environment hosting workloads targeted for Azure migration. Always pairs with `stack-cobol-mainframe` and Architect escalation.

## When to Use

Customer mentions z/OS, OS/390, MVS, IBM i, AS/400, Unisys ClearPath, Bull, or any 3270/5250 environment

## Inputs

- LPAR inventory + MIPS allocation
- Workload mix (batch / online / DB)
- Source code access (SCLM / Endevor / ChangeMan / Git on z/OS)
- Database engines (Db2, IMS, Adabas, VSAM, IDMS)
- Scheduler exports (TWS / Control-M / Zeke)
- Network connections (TN3270 endpoints, MQ, FTP / NDM, Web Services)

## Probes

- LPAR list + CPU/memory allocations
- Job class / workload manager classifications
- Db2 subsystem list + database catalog
- IMS region list + DBD/PSB inventory (handoff to `stack-cobol-mainframe`)
- CICS region list + transaction inventory
- VSAM file inventory + sizes
- JCL inventory + scheduled job count
- Source repository (SCLM / Endevor / ChangeMan / Git) state
- Identity (RACF / Top Secret / ACF2) user + group counts
- MQ queue manager inventory
- Network: TN3270 ports, FTP / NDM connections, Web Services exposures

## Target Azure Mapping (signals only — Architect decides)

| Mainframe today | Azure approach |
|-----------------|---------------|
| z/OS CICS / batch | Replatform via Micro Focus / Astadia / Heirloom on AKS |
| z/OS Db2 | Replatform to Db2 LUW on Azure VMs, or refactor to Azure SQL / PostgreSQL |
| z/OS IMS | Refactor to relational (Azure SQL / PostgreSQL) — major effort |
| IBM i (AS/400) RPG / COBOL | Power VS on Azure (lift) or rewrite to Java/.NET |
| Unisys ClearPath | Vendor-specific replatform (limited options) |
| 3270 terminal sessions | Web UI rewrite + Entra ID auth |

## Risks / Constraints

- **No direct Azure equivalent.** All mainframe migrations require partner tooling (Micro Focus, Astadia, Heirloom, TmaxSoft, Modern Systems, etc.) or rewrite.
- **License entanglement** — IBM IPLA, Adabas, third-party tools each carry separate commercial paths.
- **Skills risk** — COBOL / RPG / Natural / PL/I expertise is scarce; modernization timelines are long.
- **Data conversion** — EBCDIC ↔ ASCII; packed decimal ↔ NUMERIC; VSAM / IMS ↔ relational.
- **Operational handoff** — scheduling, monitoring, security models all change.
- **Phased migration is the norm** — full cutover is rare; expect coexistence with continuous data sync for many quarters.

## Output Checklist

- [ ] Source environment identified
- [ ] Available access method captured
- [ ] Existing inventory or export captured
- [ ] Risks flagged for Architect + Cost Engineer review
- [ ] Escalation path decided (if applicable)
- [ ] Confidence label set on `source.evidence_confidence`