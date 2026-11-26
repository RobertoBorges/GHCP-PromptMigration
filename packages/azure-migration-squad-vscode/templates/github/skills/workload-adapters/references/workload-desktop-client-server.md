# Skill: Workload Pattern — Desktop Client-Server (Stub)

> **Stub pattern.** Provides classification + Azure target tendencies. For complex engagements, deepen this skill with engagement-specific guidance.

## Overview

Workload pattern for thick-client desktop applications (Windows Forms, WPF, MFC, Delphi, PowerBuilder, Java Swing/SWT) that talk to a backend (DB direct, application server, or REST API).

## Defining Characteristics

- **Client:** installed Windows / macOS / Linux desktop application
- **Communication:** typically DB connection (chat-heavy) or per-action server calls
- **State:** thick client holds session state; user-installable updates
- **Deployment:** MSI / installer / Click-Once / vendor package
- **Concurrency:** per-user installation; client-side caching

## Target Azure Mapping (signals — Architect decides)

| Today | Azure |
|-------|-------|
| Thick client + direct DB | **Rewrite as web app** (preferred) — App Service / Container Apps for the new web UI + Azure SQL / PostgreSQL for the DB |
| Thick client + REST API backend | Keep client (interim) — migrate backend to Azure; or rewrite client as web in parallel |
| Click-Once deployed | App Service + Azure AD authentication; rewrite as web SPA |
| MFC / Delphi / PowerBuilder | Rewrite required (no PaaS for native Windows UI) |
| Java Swing / SWT | Rewrite to web (Spring Boot + modern frontend) |
| Citrix / RDS-published desktop | **Azure Virtual Desktop** (lift the published-app pattern) |

## Risks / Migration Constraints

- **Chat-heavy DB pattern** does not survive WAN to Azure. Latency between desktop and Azure SQL will kill the UX. The migration often requires an API layer between them.
- **Local data caches** (SQLite, ISAM) must move to durable Azure storage with sync.
- **Installer / patch distribution** changes — web is patch-free; AVD is patch-light.
- **Authentication** — Windows auth + local AD → Entra ID OIDC (web) or Entra ID-joined VMs (AVD).
- **Reporting modules** (Crystal Reports, ActiveReports embedded) require modernization separately.
- Default recommendation: **rebuild** as web; AVD only if the desktop pattern is non-negotiable.

## Output Checklist

- [ ] Workload sub-pattern identified
- [ ] Source environment characterized
- [ ] Critical SLA / TPS / latency captured
- [ ] State + consistency model captured
- [ ] Vendor / license model captured (if applicable)
- [ ] Migration approach: `rehost` / `replatform` / `refactor` / `rebuild` / `retire` / `retain` selected
- [ ] Required specialists flagged (commonly Architect + Database Specialist + Cost Engineer)
- [ ] Target Azure compute + data tier identified