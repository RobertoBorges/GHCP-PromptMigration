---
name: azure-compatibility-assessment
description: Comprehensive Azure compatibility checking for any workload migrating from AWS. Mandatory gate before Phase 2 code migration — verifies target Azure service parity, identifies unsupported features, flags data-residency + compliance constraints, and produces the remediation checklist consumed by later phases. Includes AWS-service-by-AWS-service checklists (Lambda, RDS, DynamoDB, S3, SQS/SNS, ECS/EKS, more).
---

# Azure Compatibility Assessment Skill

Comprehensive Azure compatibility checking for any workload migrating from AWS.

## When to Use
- **Always** before starting Phase 2 (Code Migration) — this is a mandatory gate
- When assessing whether an AWS workload can run on Azure
- When identifying remediation steps needed before migration

## Compatibility Assessment Checklist

### 1. Runtime & Framework Compatibility

Check if the application's language and framework version is supported on the target Azure platform.

#### Azure App Service Runtime Support
| Language | Supported Versions | Notes |
|----------|-------------------|-------|
| .NET | 6.0, 8.0, 9.0, 10.0 | LTS versions recommended |
| Java | 8, 11, 17, 21 | OpenJDK distributions |
| Python | 3.9, 3.10, 3.11, 3.12 | Check for native extensions |
| Node.js | 18 LTS, 20 LTS, 22 | Even-numbered LTS versions |
| Go | Any (via container) | Use Container Apps or AKS |
| Rust | Any (via container) | Use Container Apps or AKS |
| PHP | 8.1, 8.2, 8.3 | |
| Ruby | 3.1, 3.2 | Linux only |

#### Azure Container Apps / AKS
- Any language/framework that runs in a Linux or Windows container
- Check base image compatibility with Azure Container Registry
- Verify no ECR-specific or AWS-specific base image dependencies

#### Azure Functions Runtime Support
| Language | Supported Versions | Notes |
|----------|-------------------|-------|
| .NET | 6.0, 8.0 (isolated), 10.0 | In-process deprecated |
| Java | 8, 11, 17, 21 | |
| Python | 3.9, 3.10, 3.11, 3.12 | |
| Node.js | 18, 20, 22 | |
| PowerShell | 7.2, 7.4 | |
| Go / Rust | Custom handlers | Limited SDK support |

**Action:** If the runtime version is not supported, add "Upgrade runtime to [version]" to the remediation list.

### 2. OS & Architecture Compatibility

| Check | Details |
|-------|---------|
| Operating System | Linux or Windows? App Service supports both. Container Apps = Linux only. |
| Architecture | x86_64 (amd64) is standard. ARM64 support varies by service. |
| Native Dependencies | Check for OS-specific native binaries, system calls, or shared libraries |
| File System Assumptions | Local file storage is ephemeral on most Azure PaaS — use Blob Storage |
| Environment Variables | Verify no AWS-specific env vars are required at OS level |

**Action:** If the workload requires Windows and targets Container Apps, recommend App Service or AKS with Windows node pools.

### 3. Container Image Compatibility

| Check | Details |
|-------|---------|
| Base Image Source | ECR-hosted base images must be moved to ACR or use public registry |
| Image Size | Azure Container Apps has a 100GB uncompressed limit |
| Health Checks | Verify health check endpoints exist or can be added |
| Port Configuration | Container Apps uses EXPOSE and ingress config |
| Multi-stage Builds | Recommended for all container migrations |
| Secrets in Image | Scan for hardcoded AWS credentials in image layers |

**Action:** If using ECR base images, add "Push base images to ACR" to remediation list.

### 4. Database Feature Parity

#### DynamoDB → Cosmos DB
| DynamoDB Feature | Cosmos DB Equivalent | Parity | Notes |
|-----------------|---------------------|--------|-------|
| Partition Key / Sort Key | Partition Key / id | ✅ Full | Different naming |
| Global Secondary Index | Composite indexes | ✅ Full | |
| DynamoDB Streams | Change Feed | ✅ Full | |
| TTL | TTL | ✅ Full | |
| DAX (Caching) | Integrated cache | ⚠️ Partial | Different API |
| PartiQL | SQL API | ✅ Full | Cosmos SQL is richer |
| Transactions | Transactional batch | ⚠️ Partial | Same partition key only |
| On-Demand Capacity | Serverless tier | ✅ Full | |
| Reserved Capacity | Reserved throughput | ✅ Full | |

**Key concern:** DynamoDB data model may need adaptation for Cosmos DB partitioning strategy.

#### RDS → Azure SQL / Azure Database for PostgreSQL/MySQL
| Feature | Azure Equivalent | Parity | Notes |
|---------|-----------------|--------|-------|
| Multi-AZ | Zone redundancy | ✅ Full | |
| Read Replicas | Read replicas | ✅ Full | |
| RDS Proxy | Connection pooling | ⚠️ Partial | Use PgBouncer or Azure SQL connection pooling |
| Aurora Serverless v2 | Azure SQL Serverless | ⚠️ Partial | Different scaling behavior |
| Aurora Global Database | Geo-replication | ✅ Full | |
| Performance Insights | Query Performance Insight | ✅ Full | |
| IAM DB Auth | Entra ID auth | ✅ Full | |

#### ElastiCache → Azure Cache for Redis
| Feature | Azure Equivalent | Parity |
|---------|-----------------|--------|
| Redis Cluster | Azure Cache Premium/Enterprise | ✅ Full |
| Redis Sentinel | Built-in HA | ✅ Full |
| Data tiering | Enterprise Flash | ✅ Full |
| Global Datastore | Active geo-replication | ✅ Full |

### 5. AWS-Proprietary Feature Dependencies

Scan the codebase for AWS-specific features that require special handling:

| AWS Feature | Azure Equivalent | Migration Complexity |
|-------------|-----------------|---------------------|
| Lambda Layers | Functions custom handlers / container | 🟡 Medium |
| Lambda@Edge | Azure Front Door Rules Engine / Functions | 🟡 Medium |
| SQS FIFO Queues | Service Bus Sessions | 🟢 Low |
| SQS Dead Letter Queues | Service Bus Dead Letter Queue | 🟢 Low |
| SNS Filter Policies | Service Bus Topic Filters | 🟢 Low |
| Step Functions | Durable Functions / Logic Apps | 🟠 High |
| AppSync (GraphQL) | API Management + custom backend | 🟠 High |
| Amplify | Azure Static Web Apps | 🟡 Medium |
| Cognito User Pools | Entra ID External Identities | 🟠 High |
| Cognito Identity Pools | Entra ID + Managed Identity | 🟡 Medium |
| X-Ray Segments/Subsegments | App Insights dependencies | 🟢 Low |
| CloudWatch Embedded Metrics | App Insights custom metrics | 🟢 Low |
| S3 Event Notifications | Blob Storage events + Event Grid | 🟢 Low |
| S3 Select | Blob query (limited) | 🟠 High |
| DynamoDB Streams + Lambda | Cosmos DB Change Feed + Functions | 🟡 Medium |
| EventBridge Rules | Event Grid subscriptions | 🟡 Medium |
| EventBridge Pipes | Event Grid + Functions | 🟡 Medium |
| Kinesis Data Streams | Event Hubs | 🟡 Medium |
| Kinesis Firehose | Event Hubs Capture / Stream Analytics | 🟡 Medium |

### 6. Third-Party Library Azure Support

Check all dependencies for Azure compatibility:

**For each dependency file, scan for:**
- Libraries that wrap AWS services (aws-amplify, serverless-framework aws plugins, etc.)
- Libraries with hardcoded AWS assumptions
- Libraries that require AWS-specific runtime features

**Common libraries to flag:**
| Library | Issue | Recommendation |
|---------|-------|----------------|
| `serverless-framework` (AWS plugin) | AWS-specific | Use Azure Functions Core Tools or Terraform |
| `aws-amplify` | AWS-specific | Replace with Azure Static Web Apps + MSAL |
| `localstack` (testing) | AWS-specific | Use Azurite + local emulators |
| `moto` (Python AWS mocks) | AWS-specific | Replace with Azure SDK test utilities |
| `aws-cdk` constructs | AWS-specific | Convert to Bicep modules |

### 7. Networking Assumptions

| Check | Details |
|-------|---------|
| VPC Endpoints | Map to Azure Private Endpoints |
| Security Group rules | Map to NSG rules |
| NACLs | Map to NSG rules (Azure combines SG + NACL) |
| Elastic IPs | Map to Azure Public IP (static) |
| NAT Gateway | Map to Azure NAT Gateway |
| VPC Peering | Map to VNet Peering |
| Transit Gateway | Map to Azure Virtual WAN or VNet peering |
| PrivateLink | Map to Azure Private Link |
| Route 53 private zones | Map to Azure Private DNS Zones |

### 8. Authentication & Authorization

| AWS Mechanism | Azure Equivalent | Migration Path |
|---------------|-----------------|----------------|
| IAM Roles for EC2 | Managed Identity for VMs | Straightforward |
| IAM Roles for ECS/EKS | Managed Identity for Container Apps/AKS | Straightforward |
| IAM Roles for Lambda | Managed Identity for Functions | Straightforward |
| STS AssumeRole | Entra ID app registrations | Requires redesign |
| Cognito User Pools | Entra ID External Identities | Requires redesign |
| Cognito + ALB auth | Entra ID + App Gateway | Requires redesign |
| IAM policies (JSON) | Azure RBAC role assignments | Not direct translation |
| Resource-based policies | Azure RBAC + resource scope | Different model |
| Service Control Policies | Azure Policy | Different model |

## Compatibility Scoring

### Score Calculation
For each category, assign a score:
- ✅ **Compatible** (0 points): No changes needed
- 🟡 **Minor Changes** (1 point): Configuration or small code changes
- 🟠 **Moderate Changes** (2 points): Significant code changes or service replacement
- 🔴 **Major Redesign** (3 points): Architecture changes or feature gap

### Overall Score Interpretation
| Total Score | Rating | Recommendation |
|-------------|--------|----------------|
| 0-5 | 🟢 High Compatibility | Proceed with migration |
| 6-12 | 🟡 Moderate Compatibility | Proceed with planned remediation |
| 13-20 | 🟠 Low Compatibility | Significant remediation needed — review scope |
| 21+ | 🔴 Major Concerns | Consider phased approach or partial redesign |

## Output Template

The compatibility assessment should produce:

```markdown
## Azure Compatibility Assessment

### Compatibility Score: [X] / [MAX] — [🟢/🟡/🟠/🔴 Rating]

### Summary
[Brief overview of compatibility findings]

### Category Scores
| Category | Score | Status | Key Findings |
|----------|-------|--------|-------------|
| Runtime/Framework | X/3 | ✅/🟡/🟠/🔴 | [Details] |
| OS/Architecture | X/3 | ✅/🟡/🟠/🔴 | [Details] |
| Container Image | X/3 | ✅/🟡/🟠/🔴 | [Details] |
| Database | X/3 | ✅/🟡/🟠/🔴 | [Details] |
| AWS-Proprietary Features | X/3 | ✅/🟡/🟠/🔴 | [Details] |
| Third-Party Libraries | X/3 | ✅/🟡/🟠/🔴 | [Details] |
| Networking | X/3 | ✅/🟡/🟠/🔴 | [Details] |
| Authentication | X/3 | ✅/🟡/🟠/🔴 | [Details] |

### Remediation List (Priority Order)
1. [🔴 Critical] [Description] — Must fix before migration
2. [🟠 High] [Description] — Address during Phase 2
3. [🟡 Medium] [Description] — Address during migration
4. [🟢 Low] [Description] — Nice-to-have improvement

### Blockers
[Any items that would prevent migration entirely]

### Recommendations
[Strategic recommendations based on findings]
```
