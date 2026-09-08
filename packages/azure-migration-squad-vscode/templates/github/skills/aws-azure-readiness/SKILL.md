---
name: aws-azure-readiness
description: AWS to Azure service mapping summary, landing-zone requirement derivation, compatibility blockers and migration wave planning, used to produce the Azure readiness artifact and hand off to the AWS to Azure Migration Agent. Use during Phase 6 only.
---

# AWS → Azure Readiness Skill

Translates an assessed AWS estate into an Azure-shaped plan. **This skill plans; it does not migrate.**

> For deep, per-service migration guidance (SDK conversion, IaC conversion, code changes), use the
> `aws-service-mapping` and `aws-sdk-migration` skills in `AgenticMod/GHCP-AWS-To-Azure-Migration`.
> This skill deliberately stays at the estate/inventory level so it does not duplicate that agent.

## Complexity legend

| Rating | Meaning | Typical driver |
|--------|---------|----------------|
| 🟢 Low | Near drop-in; configuration re-creation | Direct equivalent exists |
| 🟡 Medium | API/behavioral differences, moderate rework | Partial feature parity |
| 🟠 High | Redesign of a component or data model | Significant feature gap |
| 🔴 Very High | Architectural rethink, no direct equivalent | Proprietary AWS capability |

---

## 1. Service Mapping Summary

### Compute

| AWS | Azure option(s) | Complexity | Selection criteria |
|-----|-----------------|-----------|--------------------|
| EC2 | Azure Virtual Machines · VM Scale Sets | 🟢 | VMSS for ASG-backed fleets; VM for pets |
| Auto Scaling Group | VM Scale Set | 🟢 | Launch template maps to VMSS model |
| Elastic Beanstalk | Azure App Service | 🟢 | Web tier; Worker tier maps to WebJobs or Container Apps Jobs |
| Lambda | Azure Functions · Container Apps | 🟡 | Functions for event-driven; Container Apps for custom runtimes or long-running |
| Batch | Azure Batch · Container Apps Jobs | 🟡 | Azure Batch for HPC; Jobs for containerized batch |
| App Runner | Azure Container Apps | 🟢 | Direct conceptual match |
| Lightsail | Azure VMs · App Service | 🟢 | Depends on the workload inside |

### Containers

| AWS | Azure option(s) | Complexity | Selection criteria |
|-----|-----------------|-----------|--------------------|
| ECS on Fargate | Azure Container Apps · AKS | 🟡 | Container Apps unless Kubernetes primitives are required |
| ECS on EC2 | AKS · Container Apps | 🟡 | AKS when node-level control matters |
| EKS | AKS | 🟡 | Manifests largely portable; IRSA becomes Workload Identity |
| ECR | Azure Container Registry | 🟢 | Re-tag and push; lifecycle policies re-created as ACR retention |
| Fargate Spot | Container Apps consumption · AKS spot node pools | 🟡 | |

### Serverless & Integration

| AWS | Azure option(s) | Complexity | Selection criteria |
|-----|-----------------|-----------|--------------------|
| SQS (standard) | Service Bus queue · Storage queue | 🟢 | Service Bus for enterprise features |
| SQS FIFO | Service Bus with sessions | 🟡 | Ordering semantics differ |
| SNS | Service Bus topic · Event Grid | 🟡 | Event Grid for event routing; Service Bus for pub/sub with subscriptions |
| EventBridge | Event Grid · Azure Logic Apps | 🟡 | Schema registry has no direct equivalent |
| Step Functions | Durable Functions · Logic Apps | 🟠 | Express workflows are the hardest case |
| API Gateway | Azure API Management · Functions HTTP · Container Apps ingress | 🟡 | APIM for full gateway features |
| AppSync | Azure API Management + a GraphQL backend | 🟠 | No managed GraphQL equivalent |
| Kinesis Data Streams | Event Hubs | 🟢 | Kafka-compatible endpoint available |
| Data Firehose | Event Hubs Capture · Stream Analytics · Data Factory | 🟡 | |
| MSK | Event Hubs (Kafka) · HDInsight Kafka · Confluent | 🟡 | |

### Data

| AWS | Azure option(s) | Complexity | Selection criteria |
|-----|-----------------|-----------|--------------------|
| RDS PostgreSQL | Azure Database for PostgreSQL Flexible Server | 🟢 | Verify extension parity |
| RDS MySQL / MariaDB | Azure Database for MySQL Flexible Server | 🟢 | |
| RDS SQL Server | Azure SQL Managed Instance · Azure SQL Database | 🟡 | MI when cross-DB queries, SQL Agent or CLR are used |
| RDS Oracle | Oracle on Azure VMs · Oracle Database@Azure | 🟠 | Licensing drives the choice |
| Aurora PostgreSQL/MySQL | Azure Database for PostgreSQL/MySQL Flexible Server | 🟡 | Aurora-specific features (Global DB, fast clone, Serverless v2) need redesign |
| DynamoDB | Cosmos DB (NoSQL or Table API) | 🟠 | Partition-key and consistency-model review required |
| ElastiCache Redis | Azure Managed Redis · Azure Cache for Redis | 🟢 | |
| MemoryDB | Azure Managed Redis with persistence | 🟡 | |
| DocumentDB | Cosmos DB (MongoDB API) · MongoDB Atlas | 🟡 | Verify API version support |
| Neptune | Cosmos DB (Gremlin API) | 🟠 | SPARQL has no equivalent |
| Redshift | Azure Synapse Analytics · Fabric Warehouse | 🟠 | |
| Timestream | Azure Data Explorer | 🟠 | |
| Athena | Azure Synapse serverless SQL · Azure Data Explorer | 🟡 | |
| Glue | Azure Data Factory · Synapse pipelines | 🟡 | |
| EMR | Azure HDInsight · Databricks · Synapse Spark | 🟡 | |

### Storage

| AWS | Azure option(s) | Complexity | Notes |
|-----|-----------------|-----------|-------|
| S3 Standard | Blob Storage Hot tier | 🟢 | |
| S3 Standard-IA | Blob Cool tier | 🟢 | |
| S3 Glacier Instant/Flexible | Blob Cold / Archive tier | 🟡 | Rehydration semantics differ |
| S3 static website | Static Website hosting · Azure Static Web Apps | 🟢 | |
| EBS | Azure Managed Disks | 🟢 | gp3 maps to Premium SSD v2 |
| EFS | Azure Files (NFS) · Azure NetApp Files | 🟡 | |
| FSx for Windows | Azure Files (SMB) | 🟢 | |
| FSx for Lustre | Azure Managed Lustre | 🟡 | |
| AWS Backup | Azure Backup | 🟡 | |

### Networking & Edge

| AWS | Azure option(s) | Complexity | Notes |
|-----|-----------------|-----------|-------|
| VPC | Virtual Network | 🟡 | Re-plan CIDRs against existing Azure space |
| Subnet | Subnet | 🟢 | Azure reserves 5 IPs per subnet vs AWS 5 |
| Security Group | Network Security Group · Application Security Group | 🟡 | SG-to-SG references map to ASGs |
| NACL | NSG at subnet scope | 🟡 | Azure has no separate stateless layer |
| ALB | Application Gateway · Front Door | 🟡 | |
| NLB | Azure Load Balancer | 🟢 | |
| Classic ELB | Application Gateway or Load Balancer | 🟡 | Must be re-platformed regardless |
| NAT Gateway | NAT Gateway | 🟢 | |
| Transit Gateway | Virtual WAN · hub-spoke peering | 🟡 | |
| VPC Peering | VNet peering | 🟢 | |
| PrivateLink / VPC endpoints | Private Link / Private Endpoints | 🟢 | |
| Direct Connect | ExpressRoute | 🟡 | |
| Site-to-Site VPN | VPN Gateway | 🟢 | |
| Route 53 | Azure DNS · Traffic Manager | 🟢 | Routing policies map to Traffic Manager methods |
| CloudFront | Azure Front Door · Azure CDN | 🟡 | |
| Global Accelerator | Front Door (anycast) | 🟡 | |
| WAF | Azure WAF on Front Door or App Gateway | 🟡 | Rule sets must be rewritten |
| Shield Advanced | DDoS Protection | 🟢 | |

### Identity, Security & Ops

| AWS | Azure option(s) | Complexity | Notes |
|-----|-----------------|-----------|-------|
| IAM users | Entra ID users | 🟠 | Prefer eliminating long-lived credentials |
| IAM roles + policies | Azure RBAC + custom roles | 🟠 | Not a 1:1 policy translation |
| Instance profile / task role / Lambda role | Managed Identity | 🟡 | |
| EKS IRSA | AKS Workload Identity | 🟡 | |
| Cross-account role | Cross-tenant/subscription RBAC · Workload Identity Federation | 🟠 | |
| Cognito | Entra ID · Entra External ID | 🟠 | |
| KMS | Key Vault · Managed HSM | 🟡 | |
| Secrets Manager | Key Vault secrets | 🟢 | |
| SSM Parameter Store | App Configuration · Key Vault | 🟢 | |
| ACM | Key Vault certificates · App Service managed certs | 🟢 | |
| Organizations + SCPs | Management Groups + Azure Policy | 🟡 | |
| GuardDuty | Microsoft Defender for Cloud | 🟡 | |
| Security Hub | Defender for Cloud + Microsoft Sentinel | 🟡 | |
| AWS Config | Azure Policy + Resource Graph | 🟡 | |
| Inspector | Defender for Cloud vulnerability assessment | 🟡 | |
| CloudTrail | Azure Activity Log + Entra audit logs | 🟢 | |
| CloudWatch metrics/alarms | Azure Monitor metrics/alerts | 🟢 | |
| CloudWatch Logs | Log Analytics workspace | 🟡 | Query language changes to KQL |
| X-Ray | Application Insights | 🟡 | |
| CloudFormation / CDK | Bicep · Terraform | 🟠 | |
| CodePipeline / CodeBuild | GitHub Actions · Azure Pipelines | 🟡 | |
| CodeCommit | GitHub · Azure Repos | 🟢 | |
| CodeArtifact | Azure Artifacts · GitHub Packages | 🟢 | |
| SES | Azure Communication Services Email | 🟡 | |
| SageMaker | Azure Machine Learning | 🟠 | |
| Bedrock | Microsoft Foundry | 🟡 | |

---

## 2. No Direct Equivalent — Flag As Blockers

| AWS capability | Situation |
|----------------|-----------|
| Step Functions Express workflows | High-throughput short workflows; Durable Functions has different scaling and cost characteristics |
| Aurora Serverless v2 fine-grained ACU scaling | Azure Flexible Server scales differently |
| Aurora Global Database sub-second RPO | Azure cross-region replication has different RPO |
| DynamoDB Streams + single-table design | Cosmos DB change feed differs in ordering and retention |
| Athena federated query / Redshift Spectrum | Requires re-architecture on Synapse/Fabric |
| Kinesis Data Analytics (SQL) | Stream Analytics has a different dialect |
| Lambda@Edge / CloudFront Functions | Front Door Rules Engine is less programmable |
| Lambda Layers | No equivalent; use shared packages or container deployment |
| Macie / Detective | Partial coverage via Purview and Sentinel |
| Ground Station, Braket, Outposts-specific services | Evaluate case by case |
| Marketplace AMIs with AWS-only licensing | Vendor must support Azure |
| Graviton/ARM64 workloads | Azure Arm-based VM availability varies by region and size |

---

## 3. Landing Zone Requirement Derivation

Derive each requirement from actual inventory data — never from assumptions.

| Derived from the assessment | Azure requirement to define |
|-----------------------------|-----------------------------|
| Account count + OU structure | Management group hierarchy and subscription topology |
| Regions actually in use | Target Azure regions and paired-region strategy |
| Every VPC/subnet CIDR | Non-overlapping VNet address plan — **list every conflict with existing Azure space explicitly** |
| Peering / TGW / VPN / Direct Connect inventory | Hub-spoke vs Virtual WAN; ExpressRoute vs VPN Gateway |
| Internet-facing endpoint list | Front Door / App Gateway / WAF placement |
| Route 53 zones and record count | Azure DNS zones, Private DNS zones, delegation plan |
| IAM users/roles + cross-account trust | Entra ID tenant, groups, RBAC model, Workload Identity Federation |
| Secrets Manager + Parameter Store counts | Key Vault topology (per-app vs per-environment) |
| KMS CMK usage | Customer-managed key strategy |
| Log group count, retention, volume | Log Analytics workspace design and retention policy |
| Alarm count and targets | Azure Monitor alert rules and action groups |
| Tag coverage + SCPs + Config rules | Azure Policy initiatives, tag policies, deny/audit effects |
| GuardDuty/Security Hub/Inspector findings | Defender for Cloud plan selection |
| Backup plans and retention | Azure Backup vault and policy design |
| Estimated monthly cost by service | Azure Pricing Calculator inputs and reservation strategy |

---

## 4. Compatibility Blockers Checklist

```
[ ] Workloads on EOL runtimes/engines that must be upgraded first
[ ] Services with no Azure equivalent (list from section 2)
[ ] Instance families/architectures without a clean Azure counterpart
[ ] Single-AZ production workloads needing an AZ design in Azure
[ ] Data volumes making lift-and-shift impractical in the window
[ ] Cross-account/cross-region data flows requiring redesign
[ ] Licensing constraints (SQL Server, Windows, Oracle, Marketplace AMIs)
[ ] Hard-coded AWS endpoints, ARNs and region names in configuration
[ ] Workloads with unknown owner — cannot be validated post-migration
[ ] Resources not managed as code — no reproducible definition to convert
[ ] Compliance/data-residency constraints on target regions
```

---

## 5. Wave Planning Rules

1. Build waves from the Phase 4 dependency graph, not from an org chart
2. **A resource may never be in an earlier wave than anything it depends on** — validate mechanically against `_edges.json`
3. Shared services (identity, DNS, logging, secrets, container registry) go in Wave 0
4. Stateless workloads before stateful ones
5. Non-production before production for the same application
6. EOL workloads that need modernization go last, or get a dedicated modernization track
7. Anything with `owner: UNKNOWN` is blocked until ownership is established — it cannot be validated after cutover

| Wave | Contents | Entry criteria | Exit criteria |
|------|----------|----------------|---------------|
| 0 | Landing zone, identity, networking, shared services | Landing zone approved | Connectivity and identity validated |
| 1 | Stateless, low-dependency, non-production | Wave 0 complete | Parity tests pass |
| 2 | Customer-facing stateless production | Wave 1 stable | Traffic cutover plan approved |
| 3 | Stateful services and databases | Data migration window agreed | Data validated, rollback tested |
| 4 | EOL / modernization-required workloads | Modernization complete | Parity tests pass |

---

## 6. Artifact & Handoff

Write `reports/Azure-Migration-Readiness.md` with:
1. Scope and the source assessment it derives from (timestamp + accounts)
2. Service mapping table with **real counts from the inventory**
3. Landing-zone requirements with the derived values filled in
4. Blockers with severity and owner
5. Wave plan, mechanically validated against the dependency graph
6. Data migration inventory: engine, size, RPO/RTO need, recommended tooling (execution out of scope)
7. Cost comparison inputs for the Azure Pricing Calculator
8. Open decisions requiring customer input

Then hand off:

> Continue with the **AWS to Azure Migration Agent** (`AgenticMod/GHCP-AWS-To-Azure-Migration`), starting at `/phase1-planandassess`.
> This assessment covered the **live AWS estate**; that agent covers **application code, SDKs, IaC and CI/CD**. Both inputs are required for a complete migration plan.
