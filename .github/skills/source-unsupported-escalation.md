# Skill: Source Adapter — Unsupported / Needs Specialist Expansion (Stub)

> **Stub adapter.** Provides recognition + escalation guidance. For deep migration, pair with a partner or extend this skill into a full adapter.

## Overview

Catch-all path for applications the standard adapter library cannot characterize at sufficient confidence. Defines the escalation playbook so the Discovery Engineer doesn't silently mis-classify.

## When to Use

- Source environment is SaaS-embedded (Salesforce Apex, ServiceNow, SharePoint customizations, Power Platform, Dynamics 365 plugins, SAP ABAP extensions, Workday Studio, Lotus Notes / Domino)
- Source environment is a **mainframe or midrange** (IBM z/OS, z/VSE, z/VM, IBM i / AS-400 / iSeries, CICS, IMS, VSAM data stores, JCL-driven batch, Unisys ClearPath, Bull GCOS)
- Application is written in **COBOL, PL/I, RPG, Assembler, or Natural** on any of the platforms above
- Source environment is a niche legacy (Tuxedo, Progress OpenEdge, IBM Informix-4GL, Sybase ASE, Adabas/Natural, CA-IDMS)
- Source code is in a proprietary archive format we cannot inspect
- User cannot provide any structured artifact or access

## Inputs

- What we know (free-form description from user)
- Vendor / platform name
- Whether vendor offers a documented Azure migration path
- Whether a specialist partner is engaged

## Probes

- Check vendor documentation for Azure migration guides
- Identify partner specialists with mainstream relationship (Microsoft Migration Factory, ISD partners, ISV-specific consultancies, mainframe modernization partners such as Micro Focus / Astadia / TCS / Kyndryl / LzLabs / NTT DATA)
- Capture what the customer has tried already
- Capture the business pressure / timeline driving the escalation

## Target Azure Mapping (signals only — Architect decides)

There is **no direct Azure mapping**. The output of this adapter is a **manual playbook**, not a mechanical target. The Architect's job is to:

1. Decide whether to bring in a specialist partner (**required** for mainframe/midrange workloads — this tool does not attempt code-level COBOL/RPG/Natural migration)
2. Decide whether to `retire` or `retain` the application
3. Decide whether to `rebuild` on a different stack the agent can support
4. Document the escalation path in `reports/Decision-Log.md`

## Risks / Constraints

- **High risk of mis-classification** if Discovery Engineer doesn't escalate and instead picks a "close-enough" adapter.
- **Vendor lock-in** — many SaaS-embedded platforms have no real exit; migration may mean rewrite on Azure-native.
- **Specialist availability** — niche stacks and mainframe workloads may have limited consultancies. Add lead time.
- **Mainframe workloads** typically involve tightly-coupled data (VSAM, DB2, IDMS), batch schedulers, and 40+ years of business logic. Migration is a multi-quarter to multi-year program — do not scope with the same effort model as a webapp migration.
- **Cost of escalation path** is typically higher than standard migration; flag Cost Engineer.

## Output Checklist

- [ ] Source environment identified
- [ ] Available access method captured
- [ ] Existing inventory or export captured
- [ ] Risks flagged for Architect + Cost Engineer review
- [ ] Escalation path decided (if applicable)
- [ ] Confidence label set on `source.evidence_confidence`