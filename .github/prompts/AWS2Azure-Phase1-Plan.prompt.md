---
name: AWS2Azure-Phase1-Plan
description: Inventory AWS services, perform Azure compatibility assessment, and generate a migration plan
argument-hint: "Specify the folder path to your AWS application, e.g., 'Assess the app in my-aws-lambda-project'"
agent: AWS to Azure Migration Agent
---

# AWS-to-Azure Migration Planning & Assessment Prompt

## Migration Scope

This guided migration helps you:
- ✅ Migrate AWS workloads to Azure with verified compatibility
- ✅ Map AWS services to Azure equivalents with trade-off analysis
- ✅ Convert infrastructure from CloudFormation/CDK to Bicep/Terraform
- ✅ Set up CI/CD pipelines for Azure deployment

This migration does **NOT** include:
- ❌ **Data Migration** — Use Azure Migrate, DMS, AzCopy, or Azure Data Factory
- ❌ **AWS Account Decommissioning** — Refer to AWS documentation
- ❌ **Full Re-architecture** — Focus is equivalent migration, not redesign

---

## Phase 1: Planning - Gather Requirements

### Step 1: Collect User Preferences (REQUIRED)

#### 1.1 Migration Scope
Ask: **"Which migration scope do you want?"**
- [ ] AWS service migration only (SDK + service integrations)
- [ ] Full workload migration (code + infra + CI/CD)
- [ ] Infrastructure conversion only (CloudFormation/CDK → Bicep/Terraform)

#### 1.2 Azure Hosting Platform
Ask: **"Which Azure hosting platform do you want to target?"**
| Platform | Best For | AWS Equivalent |
|----------|----------|---------------|
| **Azure App Service** | Web apps, APIs | Elastic Beanstalk, EC2 web apps |
| **Azure Container Apps** | Microservices, serverless containers | ECS/Fargate |
| **Azure Kubernetes Service (AKS)** | Full Kubernetes orchestration | EKS |
| **Azure Functions** | Serverless event-driven | Lambda |

#### 1.3 Infrastructure as Code
Ask: **"Which IaC tool do you prefer?"**
- **Bicep** — Azure-native, simpler syntax
- **Terraform** — Multi-cloud, HCL syntax

#### 1.4 Database Strategy
Ask: **"What database does your application currently use?"**
| Current AWS DB | Recommended Azure DB |
|---------------|---------------------|
| DynamoDB | Cosmos DB (NoSQL API or Table API) |
| RDS PostgreSQL | Azure Database for PostgreSQL |
| RDS MySQL | Azure Database for MySQL |
| RDS SQL Server | Azure SQL Database |
| Aurora | Azure SQL / Azure DB for PostgreSQL |
| ElastiCache Redis | Azure Cache for Redis |
| DocumentDB | Cosmos DB (MongoDB API) |
| Redshift | Azure Synapse Analytics |

### Step 2: Validate Requirements
**⚠️ DO NOT PROCEED UNTIL USER CONFIRMS** all four choices.

Once confirmed, create the reports folder and initialize status tracking:
- Create `reports/Report-Status.md` with planning phase details
- Create `reports/Application-Assessment-Report.md` placeholder

---

## Phase 2: Assessment - Analyze Application

### Step 3: AWS Service Inventory
Scan the codebase for AWS service usage:

#### For dependency files
Search for AWS SDK packages:
| Language | File | AWS SDK Pattern |
|----------|------|----------------|
| .NET | *.csproj | `AWSSDK.*` |
| Java | pom.xml / build.gradle | `software.amazon.awssdk`, `com.amazonaws` |
| Python | requirements.txt / pyproject.toml | `boto3`, `botocore` |
| Node.js | package.json | `@aws-sdk/*`, `aws-sdk` |
| Go | go.mod | `github.com/aws/aws-sdk-go-v2` |
| Rust | Cargo.toml | `aws-sdk-*`, `aws-config` |

#### For code files
Scan for AWS service patterns:
| AWS Service | Code Patterns to Search |
|-------------|------------------------|
| S3 | `s3.putObject`, `s3.getObject`, `S3Client`, `boto3.client('s3')` |
| SQS | `sqs.sendMessage`, `sqs.receiveMessage`, `SQSClient` |
| SNS | `sns.publish`, `SNSClient`, `boto3.client('sns')` |
| DynamoDB | `dynamodb.putItem`, `dynamodb.getItem`, `DynamoDBClient` |
| Lambda | `lambda.invoke`, `LambdaClient` |
| Secrets Manager | `secretsmanager.getSecretValue` |
| STS | `sts.assumeRole`, `STSClient` |
| CloudWatch | `cloudwatch.putMetricData` |
| SES | `ses.sendEmail`, `SESClient` |
| EventBridge | `events.putEvents`, `EventBridgeClient` |
| Step Functions | `sfn.startExecution`, `SFNClient` |
| Kinesis | `kinesis.putRecord`, `KinesisClient` |

#### For infrastructure files
Detect:
- **CloudFormation:** `template.yaml`, `template.json`, `*.cfn.yaml`
- **CDK:** `cdk.json`, `lib/*.ts` (CDK constructs)
- **SAM:** `template.yaml` with `AWS::Serverless::*`
- **Terraform:** `*.tf` with `aws` provider

#### For CI/CD files
Detect:
- **CodePipeline:** `buildspec.yml`, `pipeline.json`
- **CodeBuild:** `buildspec.yml`
- **GitHub Actions** with AWS references

### Step 4: Azure Compatibility Assessment (MANDATORY GATE)
Load the **azure-compatibility-assessment** skill and perform a full compatibility check:
1. Runtime/framework version support on target Azure platform
2. OS/architecture compatibility
3. Container image compatibility (if applicable)
4. Database feature parity analysis
5. AWS-proprietary feature dependency scan
6. Third-party library Azure support
7. Networking assumptions
8. Authentication mechanism compatibility

Produce a compatibility score and remediation list.

### Step 5: AWS → Azure Service Mapping
Load the **aws-service-mapping** skill and for each AWS service found:
1. Present Azure equivalent options (often >1)
2. Discuss trade-offs and feature gaps
3. Get user confirmation on each mapping decision
4. Document in service mapping table

### Step 6: Risk Assessment
| Risk Level | Criteria | Action |
|------------|----------|--------|
| 🔴 **Critical** | No Azure equivalent, data model redesign needed | Must address before migration |
| 🟠 **High** | Significant code changes, feature gap | Plan mitigation strategy |
| 🟡 **Medium** | Configuration changes, SDK swaps | Include in migration tasks |
| 🟢 **Low** | Direct equivalent available | Straightforward migration |

### Step 7: Generate Assessment Report
Create `reports/Application-Assessment-Report.md` with:
- **Executive Summary**
- **Migration Configuration** (target platform, IaC, database)
- **AWS Service Inventory** (complete list of AWS services found)
- **Azure Compatibility Assessment** (score + remediation list)
- **AWS → Azure Service Mapping** (all decisions with justification)
- **Current AWS Architecture** (Mermaid diagram)
- **Target Azure Architecture** (Mermaid diagram)
- **Risk Assessment** table
- **Migration Plan** with phases
- **Cost-Driver Analysis** (directional estimates — refer to [Azure Pricing Calculator](https://azure.microsoft.com/pricing/calculator/) for accuracy)
- **Data Migration Needs** (out of scope but documented with tool recommendations)
- **Remediation Prerequisites** (from compatibility assessment)
- **Next Steps:** Proceed to `/AWS2Azure-phase2-migratecode`

---

## Rules & Constraints
- Read **2000 lines at a time** for sufficient context
- Use `semantic_search` for cross-file AWS service discovery
- **DO NOT MODIFY CODE** — assessment only
- Always update `reports/Report-Status.md`
- Make reports human-readable with Mermaid diagrams, tables, and checklists

---

## Output Checklist
Before completing, ensure:
- [ ] User requirements fully captured and confirmed
- [ ] AWS service inventory complete
- [ ] Azure compatibility assessment performed (with score)
- [ ] All AWS → Azure service mappings decided with user
- [ ] Current AWS architecture diagram created
- [ ] Target Azure architecture diagram created
- [ ] Risk assessment completed
- [ ] Remediation list created (feeds into Phase 2)
- [ ] `Report-Status.md` updated
- [ ] Next steps clearly communicated: `/AWS2Azure-phase2-migratecode`
