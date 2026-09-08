# AWS → Azure Service Mapping Template

> **Usage**: Copy this template and fill it in during **Phase 1 Assessment** to document which AWS services are used in the source application and which Azure equivalents have been selected.
>
> **Reference**: See [SKILL.md](../SKILL.md) for the full decision matrix with selection criteria.

---

## Application Information

| Field | Value |
|-------|-------|
| **Application Name** | _[Enter name]_ |
| **Assessment Date** | _[YYYY-MM-DD]_ |
| **Assessed By** | _[Name/Team]_ |
| **Source Environment** | AWS _[Region(s)]_ |
| **Target Environment** | Azure _[Region(s)]_ |

---

## Service Inventory

Instructions:
1. Check each category below for AWS services used in your application
2. For each service found, fill in the mapping row
3. Use the decision matrix in SKILL.md to select the appropriate Azure equivalent
4. Document the justification for your choice

---

### Compute Services

| AWS Service | In Use? | Azure Equivalent Selected | Complexity | Justification |
|-------------|---------|---------------------------|------------|---------------|
| EC2 | ☐ Yes ☐ No | _[e.g., Azure VMs / VMSS / App Service]_ | _[🟢🟡🟠🔴]_ | _[Why this option was selected]_ |
| Lambda | ☐ Yes ☐ No | _[e.g., Azure Functions (Consumption/Premium) / Container Apps]_ | _[🟢🟡🟠🔴]_ | _[Why this option was selected]_ |
| Elastic Beanstalk | ☐ Yes ☐ No | _[e.g., Azure App Service]_ | _[🟢🟡🟠🔴]_ | _[Why this option was selected]_ |
| ECS | ☐ Yes ☐ No | _[e.g., Azure Container Apps / ACI]_ | _[🟢🟡🟠🔴]_ | _[Why this option was selected]_ |
| EKS | ☐ Yes ☐ No | _[e.g., AKS]_ | _[🟢🟡🟠🔴]_ | _[Why this option was selected]_ |
| Fargate | ☐ Yes ☐ No | _[e.g., Container Apps / ACI]_ | _[🟢🟡🟠🔴]_ | _[Why this option was selected]_ |
| AWS Batch | ☐ Yes ☐ No | _[e.g., Azure Batch / Container Apps Jobs]_ | _[🟢🟡🟠🔴]_ | _[Why this option was selected]_ |

**Compute Notes**: _[Any additional context, e.g., instance types in use, auto-scaling policies, custom AMIs]_

---

### Storage Services

| AWS Service | In Use? | Azure Equivalent Selected | Complexity | Justification |
|-------------|---------|---------------------------|------------|---------------|
| S3 | ☐ Yes ☐ No | _[e.g., Azure Blob Storage (Hot/Cool/Archive) / ADLS Gen2]_ | _[🟢🟡🟠🔴]_ | _[Why this option was selected]_ |
| EBS | ☐ Yes ☐ No | _[e.g., Azure Managed Disks (Premium SSD / Standard)]_ | _[🟢🟡🟠🔴]_ | _[Why this option was selected]_ |
| EFS | ☐ Yes ☐ No | _[e.g., Azure Files / Azure NetApp Files]_ | _[🟢🟡🟠🔴]_ | _[Why this option was selected]_ |
| FSx | ☐ Yes ☐ No | _[e.g., Azure NetApp Files / Azure Managed Lustre]_ | _[🟢🟡🟠🔴]_ | _[Why this option was selected]_ |
| Glacier | ☐ Yes ☐ No | _[e.g., Azure Blob Archive tier]_ | _[🟢🟡🟠🔴]_ | _[Why this option was selected]_ |

**Storage Notes**: _[Data volumes, access patterns, lifecycle policies, cross-region replication needs]_

---

### Database Services

| AWS Service | In Use? | Azure Equivalent Selected | Complexity | Justification |
|-------------|---------|---------------------------|------------|---------------|
| DynamoDB | ☐ Yes ☐ No | _[e.g., Cosmos DB for NoSQL / Cosmos DB for Table]_ | _[🟢🟡🟠🔴]_ | _[Why this option was selected]_ |
| RDS (engine: ___) | ☐ Yes ☐ No | _[e.g., Azure SQL Database / PostgreSQL Flexible / MySQL Flexible]_ | _[🟢🟡🟠🔴]_ | _[Why this option was selected]_ |
| Aurora (engine: ___) | ☐ Yes ☐ No | _[e.g., Azure SQL Hyperscale / PostgreSQL Flexible / Cosmos DB for PostgreSQL]_ | _[🟢🟡🟠🔴]_ | _[Why this option was selected]_ |
| ElastiCache (engine: ___) | ☐ Yes ☐ No | _[e.g., Azure Cache for Redis / Azure Managed Redis]_ | _[🟢🟡🟠🔴]_ | _[Why this option was selected]_ |
| Redshift | ☐ Yes ☐ No | _[e.g., Azure Synapse Analytics / Microsoft Fabric]_ | _[🟢🟡🟠🔴]_ | _[Why this option was selected]_ |
| DocumentDB | ☐ Yes ☐ No | _[e.g., Cosmos DB for MongoDB (RU / vCore)]_ | _[🟢🟡🟠🔴]_ | _[Why this option was selected]_ |
| Neptune | ☐ Yes ☐ No | _[e.g., Cosmos DB for Apache Gremlin]_ | _[🟢🟡🟠🔴]_ | _[Why this option was selected]_ |
| MemoryDB | ☐ Yes ☐ No | _[e.g., Azure Managed Redis (Enterprise)]_ | _[🟢🟡🟠🔴]_ | _[Why this option was selected]_ |

**Database Notes**: _[Database sizes, RCU/WCU or instance types, replication topology, backup retention]_

---

### Messaging & Eventing Services

| AWS Service | In Use? | Azure Equivalent Selected | Complexity | Justification |
|-------------|---------|---------------------------|------------|---------------|
| SQS | ☐ Yes ☐ No | _[e.g., Azure Queue Storage / Service Bus Queues]_ | _[🟢🟡🟠🔴]_ | _[Why this option was selected]_ |
| SNS | ☐ Yes ☐ No | _[e.g., Service Bus Topics / Event Grid / Notification Hubs]_ | _[🟢🟡🟠🔴]_ | _[Why this option was selected]_ |
| EventBridge | ☐ Yes ☐ No | _[e.g., Azure Event Grid]_ | _[🟢🟡🟠🔴]_ | _[Why this option was selected]_ |
| Kinesis | ☐ Yes ☐ No | _[e.g., Azure Event Hubs / Event Hubs Capture]_ | _[🟢🟡🟠🔴]_ | _[Why this option was selected]_ |
| Amazon MQ | ☐ Yes ☐ No | _[e.g., Azure Service Bus / self-hosted RabbitMQ]_ | _[🟢🟡🟠🔴]_ | _[Why this option was selected]_ |
| MSK (Kafka) | ☐ Yes ☐ No | _[e.g., Event Hubs (Kafka endpoint) / HDInsight Kafka]_ | _[🟢🟡🟠🔴]_ | _[Why this option was selected]_ |

**Messaging Notes**: _[Message volumes, ordering requirements, consumer patterns, retention needs]_

---

### Networking Services

| AWS Service | In Use? | Azure Equivalent Selected | Complexity | Justification |
|-------------|---------|---------------------------|------------|---------------|
| VPC | ☐ Yes ☐ No | _[e.g., Azure VNet]_ | _[🟢🟡🟠🔴]_ | _[Why this option was selected]_ |
| Route 53 | ☐ Yes ☐ No | _[e.g., Azure DNS / Traffic Manager / Front Door]_ | _[🟢🟡🟠🔴]_ | _[Why this option was selected]_ |
| CloudFront | ☐ Yes ☐ No | _[e.g., Azure Front Door / Azure CDN]_ | _[🟢🟡🟠🔴]_ | _[Why this option was selected]_ |
| API Gateway | ☐ Yes ☐ No | _[e.g., Azure API Management]_ | _[🟢🟡🟠🔴]_ | _[Why this option was selected]_ |
| ALB / NLB | ☐ Yes ☐ No | _[e.g., Application Gateway / Azure Load Balancer / Front Door]_ | _[🟢🟡🟠🔴]_ | _[Why this option was selected]_ |
| Direct Connect | ☐ Yes ☐ No | _[e.g., Azure ExpressRoute / VPN Gateway]_ | _[🟢🟡🟠🔴]_ | _[Why this option was selected]_ |
| Transit Gateway | ☐ Yes ☐ No | _[e.g., Azure Virtual WAN / hub-spoke VNet peering]_ | _[🟢🟡🟠🔴]_ | _[Why this option was selected]_ |
| PrivateLink | ☐ Yes ☐ No | _[e.g., Azure Private Link / Private Endpoints]_ | _[🟢🟡🟠🔴]_ | _[Why this option was selected]_ |

**Networking Notes**: _[CIDR ranges, peering topology, DNS zones, firewall rules, hybrid connectivity]_

---

### Identity & Security Services

| AWS Service | In Use? | Azure Equivalent Selected | Complexity | Justification |
|-------------|---------|---------------------------|------------|---------------|
| IAM | ☐ Yes ☐ No | _[e.g., Entra ID / Azure RBAC / Managed Identities]_ | _[🟢🟡🟠🔴]_ | _[Why this option was selected]_ |
| Cognito | ☐ Yes ☐ No | _[e.g., Microsoft Entra External ID / Azure AD B2C]_ | _[🟢🟡🟠🔴]_ | _[Why this option was selected]_ |
| Secrets Manager | ☐ Yes ☐ No | _[e.g., Azure Key Vault]_ | _[🟢🟡🟠🔴]_ | _[Why this option was selected]_ |
| Parameter Store | ☐ Yes ☐ No | _[e.g., Azure App Configuration / Key Vault]_ | _[🟢🟡🟠🔴]_ | _[Why this option was selected]_ |
| KMS | ☐ Yes ☐ No | _[e.g., Azure Key Vault (Keys) / Managed HSM]_ | _[🟢🟡🟠🔴]_ | _[Why this option was selected]_ |
| WAF | ☐ Yes ☐ No | _[e.g., Azure WAF on Front Door / Application Gateway]_ | _[🟢🟡🟠🔴]_ | _[Why this option was selected]_ |
| GuardDuty | ☐ Yes ☐ No | _[e.g., Microsoft Defender for Cloud]_ | _[🟢🟡🟠🔴]_ | _[Why this option was selected]_ |
| Security Hub | ☐ Yes ☐ No | _[e.g., Defender for Cloud / Microsoft Sentinel]_ | _[🟢🟡🟠🔴]_ | _[Why this option was selected]_ |
| Shield | ☐ Yes ☐ No | _[e.g., Azure DDoS Protection]_ | _[🟢🟡🟠🔴]_ | _[Why this option was selected]_ |

**Security Notes**: _[IAM policies count, user pool sizes, encryption requirements, compliance standards]_

---

### Observability Services

| AWS Service | In Use? | Azure Equivalent Selected | Complexity | Justification |
|-------------|---------|---------------------------|------------|---------------|
| CloudWatch | ☐ Yes ☐ No | _[e.g., Azure Monitor / Application Insights / Log Analytics]_ | _[🟢🟡🟠🔴]_ | _[Why this option was selected]_ |
| X-Ray | ☐ Yes ☐ No | _[e.g., Application Insights (Distributed Tracing)]_ | _[🟢🟡🟠🔴]_ | _[Why this option was selected]_ |
| CloudTrail | ☐ Yes ☐ No | _[e.g., Azure Activity Log / Entra Audit Logs]_ | _[🟢🟡🟠🔴]_ | _[Why this option was selected]_ |

**Observability Notes**: _[Custom metrics, log retention requirements, dashboards to recreate, alarm count]_

---

### CI/CD Services

| AWS Service | In Use? | Azure Equivalent Selected | Complexity | Justification |
|-------------|---------|---------------------------|------------|---------------|
| CodePipeline | ☐ Yes ☐ No | _[e.g., GitHub Actions / Azure DevOps Pipelines]_ | _[🟢🟡🟠🔴]_ | _[Why this option was selected]_ |
| CodeBuild | ☐ Yes ☐ No | _[e.g., GitHub Actions runners / Azure DevOps agents]_ | _[🟢🟡🟠🔴]_ | _[Why this option was selected]_ |
| CodeDeploy | ☐ Yes ☐ No | _[e.g., GitHub Actions / Azure Deployment Center]_ | _[🟢🟡🟠🔴]_ | _[Why this option was selected]_ |
| CodeCommit | ☐ Yes ☐ No | _[e.g., GitHub / Azure Repos]_ | _[🟢🟡🟠🔴]_ | _[Why this option was selected]_ |
| CodeArtifact | ☐ Yes ☐ No | _[e.g., GitHub Packages / Azure Artifacts]_ | _[🟢🟡🟠🔴]_ | _[Why this option was selected]_ |

**CI/CD Notes**: _[Pipeline count, build frequencies, deployment targets, artifact types]_

---

### Serverless & Integration Services

| AWS Service | In Use? | Azure Equivalent Selected | Complexity | Justification |
|-------------|---------|---------------------------|------------|---------------|
| Step Functions | ☐ Yes ☐ No | _[e.g., Azure Durable Functions / Logic Apps]_ | _[🟢🟡🟠🔴]_ | _[Why this option was selected]_ |
| AppSync | ☐ Yes ☐ No | _[e.g., Azure API Management (GraphQL) / self-hosted]_ | _[🟢🟡🟠🔴]_ | _[Why this option was selected]_ |
| Amplify | ☐ Yes ☐ No | _[e.g., Azure Static Web Apps / azd]_ | _[🟢🟡🟠🔴]_ | _[Why this option was selected]_ |
| SES | ☐ Yes ☐ No | _[e.g., Azure Communication Services Email / SendGrid]_ | _[🟢🟡🟠🔴]_ | _[Why this option was selected]_ |
| Pinpoint | ☐ Yes ☐ No | _[e.g., Azure Communication Services / Notification Hubs]_ | _[🟢🟡🟠🔴]_ | _[Why this option was selected]_ |

**Integration Notes**: _[Workflow complexity, connector usage, notification channels]_

---

### Analytics & Data Services

| AWS Service | In Use? | Azure Equivalent Selected | Complexity | Justification |
|-------------|---------|---------------------------|------------|---------------|
| Glue | ☐ Yes ☐ No | _[e.g., Azure Data Factory / Synapse Pipelines / Purview]_ | _[🟢🟡🟠🔴]_ | _[Why this option was selected]_ |
| Athena | ☐ Yes ☐ No | _[e.g., Synapse Serverless SQL Pool]_ | _[🟢🟡🟠🔴]_ | _[Why this option was selected]_ |
| EMR | ☐ Yes ☐ No | _[e.g., HDInsight / Synapse Spark / Databricks]_ | _[🟢🟡🟠🔴]_ | _[Why this option was selected]_ |
| Lake Formation | ☐ Yes ☐ No | _[e.g., Microsoft Purview / ADLS Gen2]_ | _[🟢🟡🟠🔴]_ | _[Why this option was selected]_ |
| Kinesis Analytics | ☐ Yes ☐ No | _[e.g., Azure Stream Analytics / Databricks Streaming]_ | _[🟢🟡🟠🔴]_ | _[Why this option was selected]_ |

**Analytics Notes**: _[Data volumes, processing frequencies, query patterns, data lake structure]_

---

### AI/ML Services

| AWS Service | In Use? | Azure Equivalent Selected | Complexity | Justification |
|-------------|---------|---------------------------|------------|---------------|
| SageMaker | ☐ Yes ☐ No | _[e.g., Azure Machine Learning]_ | _[🟢🟡🟠🔴]_ | _[Why this option was selected]_ |
| Bedrock | ☐ Yes ☐ No | _[e.g., Azure AI Foundry / Azure OpenAI Service]_ | _[🟢🟡🟠🔴]_ | _[Why this option was selected]_ |
| Comprehend | ☐ Yes ☐ No | _[e.g., Azure AI Language]_ | _[🟢🟡🟠🔴]_ | _[Why this option was selected]_ |
| Rekognition | ☐ Yes ☐ No | _[e.g., Azure AI Vision / Azure AI Face]_ | _[🟢🟡🟠🔴]_ | _[Why this option was selected]_ |
| Textract | ☐ Yes ☐ No | _[e.g., Azure AI Document Intelligence]_ | _[🟢🟡🟠🔴]_ | _[Why this option was selected]_ |
| Polly | ☐ Yes ☐ No | _[e.g., Azure AI Speech (TTS)]_ | _[🟢🟡🟠🔴]_ | _[Why this option was selected]_ |
| Lex | ☐ Yes ☐ No | _[e.g., Azure AI Bot Service / CLU]_ | _[🟢🟡🟠🔴]_ | _[Why this option was selected]_ |
| Translate | ☐ Yes ☐ No | _[e.g., Azure AI Translator]_ | _[🟢🟡🟠🔴]_ | _[Why this option was selected]_ |

**AI/ML Notes**: _[Models in use, training vs inference, custom models, API call volumes]_

---

### Container & Registry Services

| AWS Service | In Use? | Azure Equivalent Selected | Complexity | Justification |
|-------------|---------|---------------------------|------------|---------------|
| ECR | ☐ Yes ☐ No | _[e.g., Azure Container Registry (ACR)]_ | _[🟢🟡🟠🔴]_ | _[Why this option was selected]_ |
| App Runner | ☐ Yes ☐ No | _[e.g., Azure Container Apps / App Service (containers)]_ | _[🟢🟡🟠🔴]_ | _[Why this option was selected]_ |

**Container Notes**: _[Image count, registry size, deployment frequency, base images used]_

---

## Migration Complexity Summary

| Complexity | Service Count | Services |
|------------|---------------|----------|
| 🟢 Low | _[count]_ | _[list services]_ |
| 🟡 Medium | _[count]_ | _[list services]_ |
| 🟠 High | _[count]_ | _[list services]_ |
| 🔴 Very High | _[count]_ | _[list services]_ |

**Overall Assessment**: _[Estimated total migration complexity based on the combination of services]_

---

## Architecture Decisions

### Decision 1: _[Title, e.g., "Compute Platform Selection"]_

- **Context**: _[What AWS services are being used and how]_
- **Options Considered**: _[Azure options evaluated]_
- **Decision**: _[Selected Azure service(s)]_
- **Rationale**: _[Why this choice was made]_
- **Trade-offs**: _[What is gained and lost with this decision]_

### Decision 2: _[Title]_

- **Context**: _[...]_
- **Options Considered**: _[...]_
- **Decision**: _[...]_
- **Rationale**: _[...]_
- **Trade-offs**: _[...]_

_[Add more decisions as needed]_

---

## Risks and Mitigations

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| _[e.g., Feature gap in messaging service]_ | _[High/Med/Low]_ | _[High/Med/Low]_ | _[Mitigation strategy]_ |
| _[e.g., Data migration downtime]_ | _[High/Med/Low]_ | _[High/Med/Low]_ | _[Mitigation strategy]_ |

---

## Next Steps

- [ ] Review service mappings with application team
- [ ] Validate Azure service availability in target region(s)
- [ ] Estimate Azure costs using [Azure Pricing Calculator](https://azure.microsoft.com/pricing/calculator/)
- [ ] Create proof-of-concept for highest-complexity mappings (🟠/🔴)
- [ ] Proceed to Phase 2: Code Migration
