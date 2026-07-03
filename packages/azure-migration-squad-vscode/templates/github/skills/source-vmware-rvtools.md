# Skill: Source Adapter — VMware Estate (RVTools Export) (Stub)

> **Stub adapter.** Provides recognition + escalation guidance. For deep migration, pair with a partner or extend this skill into a full adapter.

## Overview

Characterizes a VMware estate from an RVTools export when individual application discovery is not yet possible. Feeds portfolio-level migration planning before per-app discovery.

## When to Use

Customer provides an RVTools XLSX; bulk assessment of an entire vCenter; portfolio sequencing across many apps

## Inputs

- RVTools export (`.xlsx`) — typically `vInfo`, `vCPU`, `vMemory`, `vDisk`, `vNetwork`, `vSnapshot`, `vCD`, `vHost`, `vCluster`, `vRP`, `vTools`, `vSC_VMK` sheets
- Optional: business owner / tier mapping CSV

## Probes

- Parse `vInfo` → VM count, power state, OS, vCenter / cluster / datacenter
- Parse `vCPU` + `vMemory` → sizing profile (right-sizing baseline)
- Parse `vDisk` → disk count + sizes → storage profile
- Parse `vNetwork` → port group / VLAN inventory
- Parse `vSnapshot` → orphan snapshot risk
- Parse `vTools` → VMware Tools status (uninstall risk)
- Group VMs by tags / annotations → application clustering

## Target Azure Mapping (signals only — Architect decides)

| VMware shape | Azure candidate |
|--------------|-----------------|
| Standard Linux/Windows VMs | Azure VMs (after right-sizing) |
| Whole VMware estate (lift) | **Azure VMware Solution (AVS)** — same vSphere tooling |
| Per-VM migration | **Azure Migrate** for assessment + Server Migration |
| App-aware migration | Per-app discovery via `/assess-any-application` after sizing |

## Risks / Constraints

- **Sizing only — no business context.** RVTools tells you what's there, not what depends on what. Application-level discovery is still required for each app.
- **License entitlements** for OS, SQL Server, etc. — Hybrid Use Benefit applies; Cost Engineer must review.
- **Network topology** is in vCenter, not RVTools — get vDS / NSX dump separately.
- **VM-level metrics** (CPU / memory utilization) are NOT in RVTools — pair with vROps / Aria Operations for right-sizing baseline.
- **Datacenter-to-Azure-region** mapping requires latency / compliance review.

## Output Checklist

- [ ] Source environment identified
- [ ] Available access method captured
- [ ] Existing inventory or export captured
- [ ] Risks flagged for Architect + Cost Engineer review
- [ ] Escalation path decided (if applicable)
- [ ] Confidence label set on `source.evidence_confidence`