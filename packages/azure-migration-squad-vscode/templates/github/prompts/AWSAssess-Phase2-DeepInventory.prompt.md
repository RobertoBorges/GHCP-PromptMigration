---
name: Phase2-DeepInventory
description: Collect per-service detail for every discovered resource and normalize it into the inventory dataset
argument-hint: "Optionally scope the deep inventory, e.g., 'Only compute and databases' or 'Focus on containers'"
agent: AWS Account Assessment Agent
---

# Phase 2 — Deep Inventory

**Goal:** for every resource indexed in Phase 1, collect the service-specific attributes that the broad sweep cannot return — instance types, engine versions, encryption state, endpoints, scaling configuration, exposure and lifecycle status.

**Prerequisite:** `reports/raw/<account-id>/_index.json` exists for at least one account.

Load the **aws-resource-inventory** skill — it holds the full read-only CLI command catalog per service domain. Execute domain by domain and **delegate each domain to a subagent** so raw JSON stays out of the main context.

---

## Execution Order

Run domains in this order so later domains can reference earlier results:

1. Networking (VPCs, subnets, security groups) — everything else attaches to these
2. Compute
3. Containers
4. Serverless
5. Databases
6. Storage
7. Identity & Security
8. Data & Integration
9. Observability
10. DevOps & IaC
11. Other services

---

## Domain 1 — Networking

Collect: VPCs, subnets, route tables, internet gateways, NAT gateways, VPC endpoints, peering connections, Transit Gateways and attachments, VPN and Customer Gateways, Direct Connect, security groups, NACLs, flow logs, ENIs, Elastic IPs, load balancers (ALB/NLB/GWLB/Classic), target groups and target health, Route 53 hosted zones and records, CloudFront distributions, Global Accelerator, WAFv2 Web ACLs, Network Firewall.

**Must capture per VPC:** CIDR blocks, `IsDefault`, tenancy, DHCP options, subnet-to-AZ mapping, public vs private subnet classification (route to IGW = public).

**Must capture per security group:** every ingress/egress rule with source (CIDR or referenced SG) — the referenced-SG edges are the backbone of the Phase 4 dependency graph.

---

## Domain 2 — Compute

Collect: EC2 instances, EBS volumes, snapshots owned by the account, self-owned AMIs, key pairs, Elastic IPs, Auto Scaling Groups, Launch Templates and versions, Elastic Beanstalk applications/environments/configuration, Lightsail instances, Batch compute environments and job queues, App Runner services.

**Must capture per EC2 instance:** instance ID, name tag, instance type, state, AZ, VPC/subnet, private/public IP, `LaunchTime`, platform details, architecture, root device type, attached security groups, IAM instance profile, EBS volume IDs, monitoring state, tenancy, `SpotInstanceRequestId` if spot.

**Must capture per Elastic Beanstalk environment:** application name, environment name, solution stack (this reveals the runtime and its EOL status), tier (WebServer vs Worker), health, instance count, load balancer type, and the underlying EC2/ASG resources.

---

## Domain 3 — Containers

Collect: ECS clusters, services, running tasks, task definitions, capacity providers; EKS clusters, node groups, Fargate profiles, add-ons, OIDC provider, access entries; ECR repositories, images and scan findings.

**Must capture per ECS service:** cluster, launch type (`FARGATE` vs `EC2` vs capacity provider strategy), desired/running/pending count, task definition ARN and revision, CPU/memory, network mode, subnets and security groups, load balancer target group, service discovery, platform version, deployment configuration.

**Must capture per ECS task definition:** container images (registry + tag — this identifies ECR vs Docker Hub vs private registry), CPU/memory, environment variables **names only** (never dump values that may contain secrets), secrets references (ARNs), log configuration, execution and task role ARNs, port mappings, volumes.

**Must capture per EKS cluster:** Kubernetes version (flag if below the supported window), endpoint public/private access, VPC config, logging types enabled, encryption config, platform version, node group instance types and AMI type, Fargate profile selectors, installed add-ons and versions.

**Must capture per ECR repository:** URI, image tag mutability, scan-on-push, encryption, lifecycle policy presence, image count, most recent push date, and the highest-severity scan finding.

---

## Domain 4 — Serverless

Collect: Lambda functions, versions, aliases, layers, event source mappings, function URLs, reserved/provisioned concurrency; Step Functions state machines; EventBridge buses, rules and targets; SQS queues; SNS topics and subscriptions; API Gateway REST APIs (v1) and HTTP/WebSocket APIs (v2), stages, authorizers, integrations; AppSync GraphQL APIs.

**Must capture per Lambda function:** name, runtime (**flag deprecated runtimes**), handler, memory, timeout, architecture, package type (Zip vs Image), code size, last modified, VPC config, environment variable **names only**, layers, dead-letter config, tracing config, execution role, and every event source mapping (SQS/Kinesis/DynamoDB Streams/MSK).

**Must capture per SQS queue:** URL, ARN, visibility timeout, message retention, FIFO vs standard, encryption (SSE-SQS vs SSE-KMS), redrive policy and DLQ target, approximate message counts.

**Must capture per SNS topic:** ARN, subscription count and protocols, encryption, and the delivery targets (these become dependency edges).

---

## Domain 5 — Databases

Collect: RDS instances, RDS/Aurora clusters, global clusters, snapshots, parameter groups, subnet groups, event subscriptions; DynamoDB tables, GSIs, streams, backups, TTL, capacity mode; ElastiCache clusters, replication groups, serverless caches; MemoryDB clusters; DocumentDB clusters; Neptune clusters; Redshift clusters and Redshift Serverless workgroups; Timestream databases; Keyspaces; QLDB ledgers.

**Must capture per RDS/Aurora:** identifier, engine and **engine version** (flag EOL/extended-support versions), instance class, allocated/max storage and storage type, Multi-AZ, `PubliclyAccessible`, encryption at rest and KMS key, backup retention and window, deletion protection, endpoint and port, VPC/subnet group, security groups, parameter group, performance insights, `InstanceCreateTime` / `ClusterCreateTime`, IAM auth enabled, Serverless v2 min/max ACU.

Distinguish **Aurora** (`Engine` starts with `aurora`) from standard RDS engines and report writer/reader topology per cluster.

**Must capture per DynamoDB table:** name, item count, size, billing mode (provisioned vs on-demand), provisioned RCU/WCU, GSIs and LSIs, streams and stream view type, TTL, point-in-time recovery, encryption type, global table replicas, `CreationDateTime`.

---

## Domain 6 — Storage

Collect: S3 buckets with region, encryption, versioning, public access block, bucket policy status, lifecycle rules, replication, logging, object lock, and size/object count from CloudWatch; EFS file systems and mount targets; FSx file systems; Storage Gateway gateways; AWS Backup plans, vaults and protected resources.

**S3 size** comes from CloudWatch, not from listing objects:

```powershell
aws cloudwatch get-metric-statistics `
  --namespace AWS/S3 --metric-name BucketSizeBytes `
  --dimensions Name=BucketName,Value=<bucket> Name=StorageType,Value=StandardStorage `
  --start-time (Get-Date).AddDays(-2).ToString("yyyy-MM-ddTHH:mm:ssZ") `
  --end-time (Get-Date).ToString("yyyy-MM-ddTHH:mm:ssZ") `
  --period 86400 --statistics Average `
  --output json --no-cli-pager
```

⚠️ Never run `aws s3 ls --recursive` on large buckets — it is slow, expensive in LIST requests, and unnecessary.

---

## Domain 7 — Identity & Security

Collect: IAM users, roles, groups, customer-managed policies, inline policies, access keys and their last-used dates, MFA devices, the credential report, account password policy, SAML/OIDC providers; Organizations accounts, OUs and SCPs; KMS keys and aliases and rotation status; Secrets Manager secret **names/ARNs/rotation config only**; SSM Parameter Store parameter **names/types only**; ACM certificates and expiry; Cognito user pools and identity pools; GuardDuty detectors and findings; Security Hub enabled standards and findings; AWS Config recorders, rules and compliance; Inspector coverage and findings; IAM Access Analyzer findings; Macie session.

**🚫 Absolute rule:** never call `get-secret-value`, `get-parameter --with-decryption`, or `kms decrypt`. Inventory the existence and metadata of secrets, never their content.

**Must capture per IAM role:** name, ARN, trust policy principals (**this reveals cross-account trust**), attached managed policies, inline policy names, `CreateDate`, `RoleLastUsed`, max session duration, permissions boundary.

---

## Domain 8 — Data & Integration

Collect: Kinesis Data Streams, Data Firehose delivery streams, MSK clusters, Glue databases/crawlers/jobs/connections, Athena workgroups and data catalogs, EMR clusters, QuickSight dashboards, Data Pipeline pipelines.

---

## Domain 9 — Observability

Collect: CloudWatch log groups (**with retention and stored bytes — untagged, never-expiring log groups are a common hidden cost**), alarms, dashboards, composite alarms; X-Ray sampling rules and service graph; CloudTrail trails, status, multi-region and organization flags, and their S3/CloudWatch destinations.

---

## Domain 10 — DevOps & IaC

Collect: CodeCommit repositories, CodeBuild projects, CodePipeline pipelines and stages, CodeDeploy applications and deployment groups, CodeArtifact domains and repositories; CloudFormation stacks, stack resources, stack sets, outputs, and drift status.

**CloudFormation is high-value:** stacks tell you which resources are managed as code and which were created manually. Every resource *not* owned by a stack is a candidate for the "manually created / undocumented" finding.

---

## Domain 11 — Other Services

Collect: SES/SESv2 identities and sending status, Amplify apps, Amazon MQ brokers, Transfer Family servers, WorkSpaces, SageMaker notebooks/endpoints/domains, Bedrock custom models and provisioned throughput, Service Catalog portfolios.

---

## Step: Normalize The Inventory

Write per-service raw JSON to `reports/raw/<account-id>/<region>/<service>.json`, then produce the normalized inventory record for every resource:

```json
{
  "arn": "arn:aws:rds:sa-east-1:123456789012:db:orders-prod",
  "accountId": "123456789012",
  "region": "sa-east-1",
  "service": "rds",
  "resourceType": "AWS::RDS::DBInstance",
  "resourceId": "orders-prod",
  "resourceName": "orders-prod",
  "state": "available",
  "createdOn": "2023-04-11T18:22:04Z",
  "createdBy": null,
  "owner": null,
  "tags": { "Environment": "prod", "Application": "orders" },
  "attributes": {
    "engine": "aurora-postgresql",
    "engineVersion": "13.9",
    "instanceClass": "db.r6g.xlarge",
    "multiAz": true,
    "publiclyAccessible": false,
    "storageEncrypted": true,
    "backupRetentionPeriod": 7
  },
  "relationships": {
    "vpcId": "vpc-0a1b2c",
    "subnetIds": ["subnet-1", "subnet-2"],
    "securityGroupIds": ["sg-0aa11"],
    "kmsKeyId": "arn:aws:kms:..."
  },
  "managedBy": "CloudFormation:orders-db-stack",
  "sourceOperation": "rds:DescribeDBInstances"
}
```

`createdBy` and `owner` stay `null` here — Phase 3 fills them.

---

## Exit Criteria

- [ ] All 11 domains executed for every scanned account and region
- [ ] Per-service raw JSON written under `reports/raw/<account-id>/<region>/`
- [ ] Normalized inventory records produced for every indexed resource
- [ ] Resources present in the Phase 1 index but not resolvable in Phase 2 recorded as coverage gaps
- [ ] EOL/deprecated versions flagged (RDS engines, Lambda runtimes, EKS versions, Beanstalk solution stacks)
- [ ] `Report-Status.md` updated

**Next step:** proceed to `/AWSAssess-phase3-enrichment`
