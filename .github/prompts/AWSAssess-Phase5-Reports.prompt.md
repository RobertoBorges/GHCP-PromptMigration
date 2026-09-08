---
name: Phase5-Reports
description: Consolidate every artifact into the final assessment, inventory, topology, findings, governance and cost reports
argument-hint: "Optionally target a report, e.g., 'Regenerate only the findings report' or 'Aggregate all scanned accounts'"
agent: AWS Account Assessment Agent
---

# Phase 5 — Report Generation

**Goal:** turn the collected data into the deliverable set. This phase is **re-runnable** — every time a new account is scanned, run it again to re-aggregate.

**Prerequisite:** at least one account has completed Phases 1–4.

Load the **aws-inventory-reporting** skill (templates + Mermaid patterns) and the **aws-security-findings** skill (finding catalog + severity model).

---

## Step 0: Re-Aggregation Rule (READ FIRST)

**Always rebuild every report from every account folder present under `reports/raw/`.**

```
reports/raw/
├── 111111111111/
│   ├── _index.json
│   ├── _inventory-enriched.json
│   ├── _edges.json
│   └── <region>/<service>.json
├── 222222222222/
└── 333333333333/
```

Never edit a report in place to "append" an account — regenerate it. This guarantees consistent totals when the user logs in to accounts one at a time across multiple sessions.

If an account folder is missing Phases 2–4 output, include it in the reports as **partially assessed** and list what is missing.

---

## Report 1 — `reports/AWS-Account-Assessment-Report.md`

The executive deliverable. Structure:

1. **Assessment Metadata** — timestamp, accounts scanned, accounts pending, regions in scope, tooling versions, who ran it
2. **Executive Summary** — 5–10 bullets a non-technical stakeholder can act on
3. **Estate Profile**
   - Total resources by account, by region, by service
   - Compute footprint (EC2 count and vCPU/memory totals, container task count, Lambda function count)
   - Data footprint (database count and engines, total storage across S3/EBS/EFS/RDS)
   - Network footprint (VPC count, public vs private subnets, internet-facing endpoints)
4. **Workload Inventory** — one row per identified application with its resources, owner, environment and estimated cost
5. **Architecture Overview** — the account hierarchy and region heatmap diagrams
6. **Key Findings** — top 10 by severity and business impact, each with resource ARN evidence
7. **Cost Summary** — top services, top regions, top owners, unattributed spend
8. **Governance Summary** — tag coverage, IaC coverage, ownership coverage
9. **Modernization Signals** — EOL engines/runtimes, legacy instance families, unmanaged resources, single-AZ production workloads
10. **Coverage Gaps & Limitations** — what could not be scanned and why, plus the CloudTrail 90-day attribution caveat
11. **Recommendations** — prioritized, each mapped to the findings that justify it
12. **Next Steps** — including the optional `/AWSAssess-phase6-azurereadiness` handoff

---

## Report 2 — `reports/AWS-Resource-Inventory.md`

The complete inventory, organized **Account → Region → Service**.

Every table must include these columns:

| Resource | Type | ID/ARN | State | Tags | Created On | Created By | Created Via | Owner | Est. Cost |
|----------|------|--------|-------|------|-----------|-----------|-------------|-------|-----------|

Add service-specific columns per section. Examples:

**EC2**

| Name | Instance ID | Type | State | AZ | VPC/Subnet | Private IP | Public IP | Launched | Created By | Owner | Tags |
|------|-------------|------|-------|-----|-----------|-----------|-----------|----------|-----------|-------|------|

**RDS / Aurora**

| Identifier | Engine | Version | EOL? | Class | Multi-AZ | Public | Encrypted | Backup (days) | Created On | Created By | Owner | Tags |
|-----------|--------|---------|------|-------|----------|--------|-----------|---------------|-----------|-----------|-------|------|

**ECS / Fargate**

| Cluster | Service | Launch Type | Desired/Running | Task Def | CPU/Mem | Image | Subnets | Target Group | Created On | Owner | Tags |
|---------|---------|-------------|-----------------|----------|---------|-------|---------|--------------|-----------|-------|------|

**EKS**

| Cluster | K8s Version | Supported? | Endpoint Access | Node Groups | Instance Types | Fargate Profiles | Add-ons | Created On | Owner | Tags |
|---------|-------------|-----------|-----------------|-------------|----------------|------------------|---------|-----------|-------|------|

**ECR**

| Repository | URI | Images | Latest Push | Scan on Push | Immutable Tags | Encryption | Lifecycle Policy | Critical Findings | Created On | Owner |
|-----------|-----|--------|-------------|--------------|----------------|------------|------------------|-------------------|-----------|-------|

**Elastic Beanstalk**

| Application | Environment | Solution Stack | EOL? | Tier | Health | Instances | LB Type | Created On | Created By | Owner |
|-------------|-------------|----------------|------|------|--------|-----------|---------|-----------|-----------|-------|

**Lambda**

| Function | Runtime | Deprecated? | Memory | Timeout | Package | VPC | Triggers | Last Modified | Created By | Owner |
|----------|---------|-------------|--------|---------|---------|-----|----------|---------------|-----------|-------|

**S3**

| Bucket | Region | Size | Objects | Encryption | Versioning | Public Access | Lifecycle | Replication | Created On | Owner |
|--------|--------|------|---------|------------|------------|---------------|-----------|-------------|-----------|-------|

Add a **summary counts table** at the top of each account section so the reader gets the shape of the estate before the detail.

Also emit `reports/inventory.csv` with every resource flattened across all accounts.

---

## Report 3 — `reports/AWS-Network-Topology.md`

- VPC inventory table (CIDR, default?, subnets, AZs, IGW, NAT, endpoints, flow logs enabled)
- Subnet table with public/private classification
- Route table summary
- Peering / Transit Gateway / VPN / Direct Connect connectivity table
- Load balancer table with scheme, listeners, target groups and healthy target counts
- Route 53 zones and record counts, with records pointing at resources not found in the inventory flagged as **dangling DNS**
- **Internet exposure path table** — every path from `0.0.0.0/0` to a resource
- Per-VPC Mermaid topology diagrams

---

## Report 4 — `reports/AWS-Dependency-Map.md`

- Account hierarchy diagram
- Region heatmap diagram
- Per-application dependency diagrams
- Data-flow diagram
- Cross-account trust diagram with external accounts highlighted
- Full edge table: `Source | Target | Edge Type | Evidence | Confidence | Cross-Account | Cross-Region`
- **Orphan section**: resources with zero inbound and zero outbound edges — strong candidates for decommissioning

---

## Report 5 — `reports/AWS-Security-Findings.md`

Use the finding catalog and severity model from the **aws-security-findings** skill.

Summary table first:

| Severity | Count |
|----------|-------|
| 🔴 Critical | 4 |
| 🟠 High | 17 |
| 🟡 Medium | 42 |
| 🟢 Low | 88 |
| ℹ️ Informational | 130 |

Then one section per finding type:

```
### 🔴 CRITICAL — Publicly accessible RDS instance

**Finding:** RDS instances are reachable from the internet.
**Why it matters:** Direct database exposure bypasses application-layer controls.
**Affected resources:**

| Account | Region | Resource ARN | Detail |
|---------|--------|--------------|--------|
| 111111111111 | sa-east-1 | arn:aws:rds:...:db:legacy-orders | PubliclyAccessible=true, SG allows 5432 from 0.0.0.0/0 |

**Evidence:** rds:DescribeDBInstances + ec2:DescribeSecurityGroups
**Recommendation:** Set PubliclyAccessible=false, move to private subnets, restrict SG to the application security group.
```

Include findings sourced from GuardDuty, Security Hub, AWS Config and Inspector where those services are enabled, clearly attributed to their source, and note where they are **not** enabled as a finding in itself.

---

## Report 6 — `reports/AWS-Tagging-Governance.md`

- Tag coverage overall and per account/region/service
- Required-tag compliance matrix
- Tag key variant analysis (case/spelling inconsistencies)
- Untagged resource list with estimated cost — sorted by cost descending
- Ownership coverage table, with `UNKNOWN` owners listed explicitly
- **IaC coverage**: resources managed by CloudFormation vs created manually, with the manual list
- Naming convention analysis

---

## Report 7 — `reports/AWS-Cost-Analysis.md`

- Monthly trend for the analyzed window
- Cost by service (top 20 + other)
- Cost by region
- Cost by linked account (if Organizations)
- Cost by owner/cost-center tag, plus the **unattributed** bucket
- Top 25 most expensive individual resources, joined to owner and tags
- Waste candidates: unattached EBS volumes and EIPs, idle load balancers, stopped instances still incurring EBS cost, never-expiring CloudWatch log groups, old snapshots, empty ASGs, unused NAT Gateways
- Rightsizing and commitment (RI/Savings Plan) recommendations
- Disclaimer that figures are directional

---

## Report 8 — `reports/Report-Status.md`

Regenerate with:
- Phase completion checklist
- Per-account status table: `Account | Alias | Phase 1 | Phase 2 | Phase 3 | Phase 4 | Resources | Last Scanned`
- Pending accounts and the exact next command for the user
- Coverage gap table
- Assessment options in effect

---

## Step: Validate Before Delivering

- [ ] Every Mermaid block renders (no `->` inside labels, no duplicated nodes across subgraphs, no invalid edge-label syntax)
- [ ] Totals reconcile: inventory count == index count − coverage gaps
- [ ] No secret values, access keys, session tokens or private keys appear anywhere in `reports/`
- [ ] Account IDs masked if the user requested masking
- [ ] Every finding carries a resource ARN as evidence
- [ ] Every report states its generation timestamp and the account set it covers

---

## Exit Criteria

- [ ] All eight reports generated from **all** account folders present
- [ ] `reports/inventory.csv` regenerated
- [ ] Report set presented to the user with a short summary of the headline numbers
- [ ] Pending accounts and next steps clearly stated

**Next step:** scan another account with `/AWSAssess-phase1-resourcediscovery`, or proceed to `/AWSAssess-phase6-azurereadiness`
