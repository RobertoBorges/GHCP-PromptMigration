# Skill: Workload Pattern — Packaged / Vendor Application (Stub)

> **Stub pattern.** Provides classification + Azure target tendencies. For complex engagements, deepen this skill with engagement-specific guidance.

## Overview

Workload pattern for commercial off-the-shelf (COTS) software: SAP, Oracle EBS, Dynamics 365, Salesforce, vendor-installable binaries with limited customization. Customer does not own the source.

## Defining Characteristics

- **Source code:** not customer-owned
- **Customization surface:** vendor-provided extension points (plugins, scripts, config)
- **Deployment:** vendor installer / image / managed service
- **Support model:** vendor-licensed; vendor controls upgrade path

## Target Azure Mapping (signals — Architect decides)

| Today | Azure |
|-------|-------|
| SAP on-prem | **Azure for SAP** (vendor-validated VMs) or RISE with SAP on Azure |
| Oracle EBS | Azure VMs (BYOL) or Oracle Fusion Cloud |
| Dynamics 365 / GP / NAV / AX | Migrate to Dynamics 365 Online (recommended) |
| Vendor binary installable | Azure VM (lift) or Container Apps (if vendor offers container image) |
| Salesforce / ServiceNow | **Retain** (stay on SaaS); only Azure integration glue is in scope |
| SharePoint Server on-prem | Migrate to **SharePoint Online** (M365) |
| Exchange Server | Migrate to **Exchange Online** (M365) |
| Lotus Notes / Domino | Migrate mail to Exchange Online; rewrite apps to Power Platform or web |

## Risks / Migration Constraints

- **No source means no code-level migration option.** Rehost or vendor-managed migration only.
- **Vendor licensing** must be reviewed by Cost Engineer; many products allow Azure BYOL.
- **Vendor support** for Azure — confirm before commit (some products are not supported on Azure).
- **Customizations** (plugins / config / scripts) are the real migration scope — inventory them carefully.
- **Integration glue** between the packaged app and other systems usually needs work.
- **Data residency** — packaged apps may require specific Azure regions.
- Default: route to `source-unsupported-escalation` if the vendor has no documented Azure path.

## Output Checklist

- [ ] Workload sub-pattern identified
- [ ] Source environment characterized
- [ ] Critical SLA / TPS / latency captured
- [ ] State + consistency model captured
- [ ] Vendor / license model captured (if applicable)
- [ ] Migration approach: `rehost` / `replatform` / `refactor` / `rebuild` / `retire` / `retain` selected
- [ ] Required specialists flagged (commonly Architect + Database Specialist + Cost Engineer)
- [ ] Target Azure compute + data tier identified