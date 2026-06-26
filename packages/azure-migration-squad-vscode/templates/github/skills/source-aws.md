# Skill: Source Adapter — Amazon Web Services (AWS)

> Characterizes an application currently running on AWS (EC2, ECS, EKS, Lambda, Elastic Beanstalk, Fargate, RDS, S3, DynamoDB, etc.) targeting an Azure migration.

## When to Use

- User says "it runs on AWS"
- Inventory tools or accounts surface AWS resources backing the application
- Application source / state / data lives in AWS

## Inputs

- AWS account ID and region(s)
- Access: AWS profile name, IAM role assumption details, or read-only export (e.g., AWS Config snapshot, Application Discovery Service report)
- Optional: existing IaC (CloudFormation, CDK, Terraform with `aws` provider)

## Probes (use read-only AWS CLI calls; never modify)

### Compute

1. **EC2 instances backing the app**
   - `aws ec2 describe-instances --filters Name=tag:Application,Values=<name>` (or supply IDs)
   - Capture: instance type, AMI, OS, attached IAM role, security groups, VPC, subnet, tags
   - SSM into instance if accessible → run `source-on-premise` Linux/Windows probes for what's installed

2. **ECS / Fargate services**
   - `aws ecs list-clusters` → `describe-clusters`
   - `aws ecs list-services --cluster <X>` → `describe-services`
   - For each service: task definition (image URI, env vars, port mappings, IAM task role, secrets references)
   - `aws ecr describe-images --repository-name <X>` → image details

3. **EKS clusters**
   - `aws eks describe-cluster --name <X>` → version, VPC, addons
   - `kubectl get pods,services,ingresses --all-namespaces` (handoff to `source-kubernetes-cluster`)
   - `kubectl get nodes` → node group composition

4. **Lambda**
   - `aws lambda list-functions` → name, runtime, memory, timeout
   - `aws lambda get-function --function-name <X>` → trigger config, env vars, layers
   - `aws lambda list-event-source-mappings` → SQS/Kinesis/DynamoDB triggers
   - Pattern → typically `workload-event-driven` or `workload-serverless`

5. **Elastic Beanstalk**
   - `aws elasticbeanstalk describe-applications` + `describe-environments`
   - Capture platform (Java SE / Tomcat / .NET / Node / Python / Ruby / Go / PHP / Docker)
   - Beanstalk → App Service or Container Apps is the natural Azure target

6. **Batch / Step Functions**
   - `aws batch describe-job-queues`, `describe-compute-environments`, `describe-job-definitions`
   - `aws stepfunctions list-state-machines`
   - Pattern → `workload-batch-job` or `workload-event-driven`

### Data

7. **RDS / Aurora**
   - `aws rds describe-db-instances` → engine (MySQL / Postgres / SQL Server / Oracle / MariaDB), version, storage size, multi-AZ, encryption
   - `aws rds describe-db-clusters` → Aurora clusters
   - Capture `engine_version` and `allocated_storage_gb` for `data_gravity` calculation

8. **DynamoDB**
   - `aws dynamodb list-tables` → `describe-table` per table
   - Capture: provisioned vs on-demand, item count estimate, GSI/LSI count, streams enabled
   - Pattern → maps to Cosmos DB

9. **ElastiCache (Redis / Memcached)**
   - `aws elasticache describe-cache-clusters`
   - Azure target: Azure Cache for Redis

10. **S3**
    - `aws s3api list-buckets` → buckets owned by the account
    - For relevant buckets: `aws s3api list-objects-v2 --bucket <X> --max-keys 1` + `--no-paginate` for object count estimates
    - `aws s3api get-bucket-policy`, `get-bucket-lifecycle-configuration`, `get-bucket-versioning`
    - Azure target: Blob Storage (often Data Lake Gen2 for analytics)

11. **OpenSearch / Elasticsearch / DocumentDB / Neptune**
    - `aws opensearch list-domains`, `aws docdb describe-db-clusters`, `aws neptune describe-db-clusters`
    - Azure targets: Azure AI Search, Cosmos DB Mongo API, Cosmos DB Gremlin

### Messaging & Events

12. **SQS, SNS, EventBridge, MSK, Kinesis**
    - `aws sqs list-queues`, `aws sns list-topics`, `aws events list-rules`, `aws kafka list-clusters`, `aws kinesis list-streams`
    - Capture topology of producers ↔ consumers
    - Azure targets: Service Bus, Event Grid, Event Hubs (Kafka API for MSK)

### Networking

13. **VPC, Subnets, Security Groups, ALB/NLB, API Gateway**
    - `aws ec2 describe-vpcs`, `describe-subnets`, `describe-security-groups`
    - `aws elbv2 describe-load-balancers`, `describe-target-groups`
    - `aws apigateway get-rest-apis`, `aws apigatewayv2 get-apis`
    - Captures the request-path topology → influences Azure equivalents (VNet, App Gateway / Front Door, APIM)

### Identity & Secrets

14. **IAM roles + policies tied to the workload**
    - `aws iam list-roles | grep <app-prefix>`
    - `aws iam get-role-policy`, `list-attached-role-policies`
    - Capture least-privilege baseline to translate to Azure managed identities + RBAC

15. **Secrets**
    - `aws secretsmanager list-secrets`
    - `aws ssm describe-parameters --parameter-filters Key=Type,Values=SecureString`
    - Captures secrets-rotation surface → Azure Key Vault target

### Observability

16. **CloudWatch metrics / logs / alarms**
    - `aws cloudwatch describe-alarms`
    - `aws logs describe-log-groups`
    - X-Ray traces if enabled
    - Captures current observability shape → Azure Monitor / App Insights / Log Analytics equivalents

### Existing IaC

17. **CloudFormation**
    - `aws cloudformation list-stacks --stack-status-filter CREATE_COMPLETE UPDATE_COMPLETE`
    - For stacks relevant to the app: `describe-stack-resources` → resource inventory
    - This is the authoritative shape of what's deployed today

## Output Evidence

```yaml
source:
  primary_adapter: source-aws
  access_method: <aws-profile-name | role-arn | aws-config-snapshot>
  evidence_confidence: <high if live API access; medium if exports only>
  evidence_paths:
    - <account-id, region(s)>
    - <CFN stack names>
    - <key ARNs>
  notes: |
    - Compute today: <EC2 + ECS + Lambda mix>
    - Data today: <RDS engine + version; S3 buckets count; DynamoDB tables>
    - Messaging today: <SQS topology>
    - IaC today: <CloudFormation | CDK | Terraform | none>
    - Observability today: <CloudWatch | X-Ray>
    - IAM principals tied to workload: <count>
```

## Migration Constraints / Risks

- **AWS-specific services with no direct Azure equivalent.** Examples: Cognito (→ Entra ID + B2C, but mapping is non-trivial), API Gateway HTTP/REST API (→ APIM, structure differs), Step Functions (→ Logic Apps or Durable Functions, semantics differ), AWS WAF rules (manual translation), Route 53 health-routed records (→ Traffic Manager / Front Door).
- **Region/data-residency.** Tag every AWS region in scope; Azure region pairing has to honor compliance.
- **VPC topology lift.** Lift VPC + subnets one-for-one to Azure VNets + subnets only if mandatory; usually re-architecting network is cheaper.
- **IAM policies are not RBAC.** Translate IAM JSON to Azure built-in roles + custom roles + RBAC scope. Do not auto-port.
- **CloudFront, Route 53.** Edge / DNS migration is its own workstream — coordinate with Cutover Commander.
- **Egress costs out of AWS.** Large data migrations (S3 → Blob, RDS → Azure SQL) can incur material egress charges; flag for Cost Engineer.
- **Reserved instances / Savings Plans.** If the customer has RI/SP coverage in AWS, retiring carries financial implications — flag for Cost Engineer.

## Workload Pattern Inference

| AWS shape | Workload pattern |
|-----------|------------------|
| Lambda + SQS/Kinesis/SNS triggers | `event-driven` or `serverless` |
| ECS/Fargate task with ALB | `webapp` or `api-service` |
| EKS multi-service | `webapp` + `api-service` (likely) |
| Batch jobs | `batch-job` |
| Step Functions | `event-driven` orchestration |
| EC2 with Tomcat / IIS / nginx | `webapp` or `api-service` |
| Glue / EMR / Kinesis Analytics | `data-pipeline` |

## Target Azure Mapping (signals only — Architect decides)

| AWS today | Azure candidate |
|-----------|-----------------|
| EC2 (Linux, web app) | App Service Linux / Container Apps / AKS |
| EC2 (Windows, IIS) | App Service Windows / Container Apps with Windows |
| ECS / Fargate | Container Apps (first), AKS (when complex) |
| EKS | AKS |
| Lambda | Azure Functions (first), Container Apps (when long-running) |
| Elastic Beanstalk | App Service (matches platforms) |
| RDS PostgreSQL | Azure PostgreSQL Flexible Server |
| RDS MySQL | Azure Database for MySQL Flexible Server |
| RDS SQL Server | Azure SQL MI or Azure SQL DB |
| RDS Oracle | Azure VMs running Oracle, OR refactor to Azure SQL/Postgres |
| DynamoDB | Cosmos DB (NoSQL API) |
| S3 | Blob Storage (or Data Lake Gen2 for analytics) |
| SQS | Service Bus Queue |
| SNS | Event Grid or Service Bus Topic |
| EventBridge | Event Grid |
| Kinesis Data Streams | Event Hubs |
| MSK | Event Hubs (Kafka API) or HDInsight Kafka |
| ElastiCache Redis | Azure Cache for Redis |
| API Gateway | APIM |
| ALB / NLB | App Gateway / Load Balancer |
| Route 53 | Azure DNS + Traffic Manager / Front Door |
| CloudWatch | Azure Monitor + App Insights + Log Analytics |
| IAM | Entra ID + managed identities + RBAC |
| Secrets Manager / SSM Parameter Store | Key Vault |

## Anti-Patterns

- Don't generate the Azure design from AWS in this adapter — only surface the candidates. The Architect picks.
- Don't try to recreate IAM 1:1 in Azure. Re-derive from the workload's actual access needs.
- Don't ignore Lambda → Azure Functions cold-start parity. Surface as a `Phase 6` validation item.
- Don't migrate S3 buckets blindly. Check object count, total size, lifecycle policies first; very-large buckets may need AzCopy + multi-stage cutover.

## Output Checklist

- [ ] AWS account(s) + region(s) captured
- [ ] Compute services inventoried (EC2 / ECS / EKS / Lambda / Beanstalk / Batch)
- [ ] Data services inventoried (RDS / DynamoDB / S3 / ElastiCache / OpenSearch)
- [ ] Messaging services inventoried (SQS / SNS / EventBridge / MSK / Kinesis)
- [ ] Network topology captured (VPC / subnets / SGs / LBs / APIGW)
- [ ] IAM principals + secrets surface captured
- [ ] Observability shape captured
- [ ] Existing IaC (CFN / CDK / TF) identified
- [ ] Egress / RI flagged for Cost Engineer
- [ ] AWS-specific services with weak Azure equivalents flagged
