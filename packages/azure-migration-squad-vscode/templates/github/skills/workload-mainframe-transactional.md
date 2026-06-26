# Skill: Workload Pattern — Mainframe Transactional (CICS / IMS / Tuxedo) (Stub)

> **Stub pattern.** Provides classification + Azure target tendencies. For complex engagements, deepen this skill with engagement-specific guidance.

## Overview

Workload pattern for high-volume transactional workloads on mainframe (CICS regions, IMS message regions, Tuxedo) — online transaction processing with strict TPS, latency, and ACID requirements.

## Defining Characteristics

- **Volume:** thousands to millions TPS
- **Latency:** sub-100ms typically
- **Consistency:** strict ACID, often two-phase commit
- **State:** terminal session (3270 / 5250) + transactional DB
- **Failure tolerance:** rollback at transaction boundary

## Target Azure Mapping (signals — Architect decides)

| Today | Azure |
|-------|-------|
| CICS region | **Replatform via Micro Focus / Astadia / Heirloom** on AKS |
| CICS + Db2 z/OS | AKS + Db2 LUW on Azure VMs (or refactor to Azure SQL with major effort) |
| IMS Message Region | Refactor to event-driven / API-driven (Functions / Container Apps) |
| Tuxedo | Tuxedo on Azure VMs (Oracle license) or refactor to Spring Boot |
| 3270 terminals | Web UI rewrite (Phase 2 separate workstream) |

## Risks / Migration Constraints

- **No direct Azure equivalent for CICS / IMS / Tuxedo runtime.** Partner tooling required.
- **TPS preservation under partner runtime** — must be validated with Performance Engineer.
- **Two-phase commit across systems** — XA transactions across Azure services need design.
- **Data consistency during migration** — continuous replication (CDC) is typically required.
- **Skills risk** — both source mainframe expertise and partner-tooling expertise are scarce.
- **Always pairs with `stack-cobol-mainframe` + `source-mainframe`.**
- Default: **escalate** via `source-unsupported-escalation` for plan; this workload pattern signals that escalation will be required.

## Output Checklist

- [ ] Workload sub-pattern identified
- [ ] Source environment characterized
- [ ] Critical SLA / TPS / latency captured
- [ ] State + consistency model captured
- [ ] Vendor / license model captured (if applicable)
- [ ] Migration approach: `rehost` / `replatform` / `refactor` / `rebuild` / `retire` / `retain` selected
- [ ] Required specialists flagged (commonly Architect + Database Specialist + Cost Engineer)
- [ ] Target Azure compute + data tier identified