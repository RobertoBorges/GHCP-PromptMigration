---
name: Phase6-AzureReadiness
description: Translate the AWS inventory into an Azure landing-zone readiness view and hand off to the AWS to Azure Migration Agent
argument-hint: "Optionally scope, e.g., 'Readiness for the orders application only' or 'Only compute and databases'"
agent: AWS Account Assessment Agent
---

# Phase 6 — Azure Readiness (Optional)

**Goal:** convert the assessed AWS estate into an Azure-shaped view — target services, landing-zone requirements, migration complexity and wave sequencing — so the migration agent can take over with real data instead of assumptions.

**Prerequisite:** Phase 5 reports generated.

**This phase does not migrate anything.** It produces a plan artifact and a handoff.

Load the **aws-azure-readiness** skill.

---

## Step 1: Confirm Intent

Ask the user:
- Is Azure migration actually in scope, or is this assessment for governance/cost only?
- Which accounts/applications are candidates?
- Is there a target Azure tenant/subscription model already defined?

If Azure migration is not in scope, stop here and say so — do not generate speculative migration content.

---

## Step 2: Service Mapping

For every AWS service found in the inventory, produce the Azure target with complexity rating. Do not invent mappings — use the mapping table in the **aws-azure-readiness** skill, and where more than one Azure option exists, present the options with the selection criteria rather than picking silently.

| AWS Resource | Count | Azure Target Option(s) | Complexity | Notes |
|--------------|-------|------------------------|-----------|-------|
| EC2 instances | 88 | Azure VMs / VM Scale Sets / App Service | 🟢 Low | 14 use legacy instance families |
| Elastic Beanstalk envs | 6 | Azure App Service | 🟢 Low | 2 on EOL solution stacks |
| ECS services (Fargate) | 24 | Azure Container Apps / AKS | 🟡 Medium | Task defs map to Container Apps revisions |
| EKS clusters | 3 | AKS | 🟡 Medium | 1 cluster below the supported K8s window |
| ECR repositories | 41 | Azure Container Registry | 🟢 Low | Image re-tag and push required |
| Lambda functions | 61 | Azure Functions / Container Apps | 🟡 Medium | 7 on deprecated runtimes |
| Aurora PostgreSQL | 4 | Azure Database for PostgreSQL Flexible Server | 🟡 Medium | Verify extension parity |
| RDS SQL Server | 2 | Azure SQL Managed Instance / Azure SQL DB | 🟡 Medium | Check cross-DB query usage |
| DynamoDB tables | 12 | Cosmos DB (NoSQL or Table API) | 🟠 High | Data model review required |
| S3 buckets | 44 | Azure Blob Storage | 🟢 Low | Map storage classes to access tiers |
| SQS queues | 18 | Azure Service Bus queues | 🟢 Low | FIFO maps to Service Bus sessions |
| SNS topics | 9 | Service Bus topics / Event Grid | 🟡 Medium | Choose per pub/sub pattern |
| VPCs | 5 | Azure VNets | 🟡 Medium | Re-plan CIDRs against existing Azure address space |
| IAM roles | 214 | Entra ID + Azure RBAC + Managed Identity | 🟠 High | Not a 1:1 policy translation |

---

## Step 3: Landing Zone Requirements

Derive concrete Azure landing-zone requirements from the assessed estate:

| Dimension | Derived from the assessment | Azure requirement |
|-----------|----------------------------|-------------------|
| Subscription model | Account count and OU structure | Management group + subscription topology |
| Regions | AWS regions in use and data residency | Azure region pairs |
| Address space | Every VPC/subnet CIDR found | Non-overlapping VNet plan (list conflicts explicitly) |
| Connectivity | VPN / Direct Connect / peering / TGW inventory | VPN Gateway / ExpressRoute / hub-spoke or Virtual WAN |
| DNS | Route 53 zones and record counts | Azure DNS / Private DNS zones |
| Identity | IAM users, roles, SSO, Cognito, cross-account trust | Entra ID tenant, groups, RBAC, workload identity federation |
| Secrets | Secrets Manager + Parameter Store entry counts | Key Vault design |
| Encryption | KMS key usage and CMK vs AWS-managed split | Customer-managed keys plan |
| Observability | Log groups, retention, alarm count | Log Analytics workspaces, Azure Monitor, App Insights |
| Governance | Tag coverage, SCPs, Config rules | Azure Policy, tag policies, initiatives |
| Compliance | GuardDuty/Security Hub/Config findings | Defender for Cloud plan |

---

## Step 4: Compatibility Blockers

List anything that will block or complicate migration, sourced from the actual inventory:

- AWS-proprietary services with no direct Azure equivalent (e.g. Step Functions Express workflows, Kinesis Data Analytics, Athena federated queries, Redshift Spectrum, Ground Station)
- Workloads on EOL runtimes/engines that must be upgraded before or during migration
- Instance families/architectures with no direct Azure equivalent (Graviton/ARM workloads → Azure Arm-based VMs where available)
- Single-AZ production workloads that need an availability-zone design in Azure
- Data volumes that make lift-and-shift impractical within the migration window
- Cross-account/cross-region data flows that must be redesigned
- Licensing constraints (SQL Server, Windows Server, Oracle, third-party AMIs from Marketplace)
- Hard-coded AWS endpoints, ARNs and region names in workload configuration

---

## Step 5: Wave Plan

Sequence applications into migration waves using dependency data from Phase 4:

| Wave | Applications | Rationale | Dependencies | Risk |
|------|-------------|-----------|--------------|------|
| 1 | Stateless internal APIs, dev/test | No downstream consumers, low blast radius | None | 🟢 |
| 2 | Customer-facing web tier | Depends on Wave 1 shared services | Wave 1 | 🟡 |
| 3 | Databases and stateful services | Requires data migration window | Waves 1–2 | 🟠 |
| 4 | Legacy/EOL workloads | Requires modernization first | Wave 3 | 🔴 |

**Rule:** a resource cannot be in an earlier wave than anything it depends on. Validate the wave plan against the Phase 4 edge list.

---

## Step 6: Write The Artifact

Create `reports/Azure-Migration-Readiness.md` containing:
1. Scope and source assessment reference
2. Service mapping table with counts and complexity
3. Landing-zone requirements
4. Compatibility blockers with severity
5. Wave plan with dependency validation
6. Data migration inventory (volumes, engines, recommended tooling — execution out of scope)
7. Cost comparison inputs (what to price in the Azure Pricing Calculator)
8. Open decisions requiring the customer's input

---

## Step 7: Handoff

Present the handoff explicitly:

> The Azure readiness view is written to `reports/Azure-Migration-Readiness.md`.
> To continue with the actual migration, switch to the **AWS to Azure Migration Agent** (`AgenticMod/GHCP-AWS-To-Azure-Migration`) and start with `/phase1-planandassess`. It will consume this readiness artifact plus your application repositories to plan code, IaC and CI/CD migration.

Note the boundary clearly: this assessment agent reads the **live AWS estate**; the migration agent works on **repositories and code**. Both are needed for a complete picture.

---

## Exit Criteria

- [ ] Azure migration confirmed to be in scope
- [ ] Every AWS service in the inventory mapped, with options where more than one exists
- [ ] Landing-zone requirements derived from real inventory data
- [ ] Blockers listed with severity
- [ ] Wave plan validated against the dependency graph
- [ ] `reports/Azure-Migration-Readiness.md` written
- [ ] Handoff to the migration agent stated
