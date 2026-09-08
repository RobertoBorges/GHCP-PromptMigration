---
name: aws-metadata-enrichment
description: Techniques for enriching an AWS inventory with tags, native creation timestamps, creator identity via CloudTrail (including the 90-day limit and the Athena path), ownership resolution with confidence levels, and Cost Explorer attribution by service, region, tag and account. Use during Phase 3.
---

# AWS Metadata Enrichment Skill

Answers *when was this created*, *who created it*, *who owns it*, and *what does it cost*.

---

## 1. Tag Consolidation

Tags arrive from three places and must be merged:

| Source | Command | Notes |
|--------|---------|-------|
| Tagging API | `resourcegroupstaggingapi get-resources` | Broadest coverage in one call |
| Native describe output | `Tags` / `TagList` / `tags` on the resource | Sometimes fresher; some services only expose tags here |
| Dedicated tag call | `list-tags-for-resource` (RDS, SNS, Firehose), `list-tags-of-resource` (DynamoDB), `list-queue-tags` (SQS), `describe-tags` (ELB Classic), `--include TAGS` (ECS) | Required for services that omit tags from describe output |

**Tag key shapes to normalize when analyzing (but never when reporting the raw value):**

```
Owner | owner | OWNER | Owner_Name | owner-name | Contact | contact | ContactEmail
Environment | env | ENV | Env | Stage | stage | environment
Application | app | App | Project | project | Service | service | Workload
CostCenter | cost-center | costcenter | CC | BillingCode | Budget
ManagedBy | managed-by | IaC | Terraform | Provisioner
```

### Metrics to compute

| Metric | Formula |
|--------|---------|
| Tag coverage | taggable resources with ≥1 tag ÷ taggable resources |
| Required-tag compliance | resources carrying **all** required keys ÷ taggable resources |
| Per-key coverage | resources with key *K* ÷ taggable resources |
| Key variant count | distinct case/spelling variants mapping to the same normalized key |
| Value cardinality | distinct values per key (high cardinality on `Environment` = inconsistency) |
| Untagged cost | sum of `estimatedMonthlyCost` where tags are empty |

Some resource types are **not taggable** (certain route table associations, some legacy resources). Exclude them from coverage denominators and say so, otherwise the percentage is misleading.

---

## 2. Creation Timestamp — Native Fields

Always prefer the native field. Do not derive a creation time from CloudTrail when the API already returns one.

| Resource | Field | Notes |
|----------|-------|-------|
| EC2 instance | `LaunchTime` | Resets on stop/start for some cases — treat as "current launch" |
| EBS volume | `CreateTime` | |
| EBS snapshot | `StartTime` | |
| AMI | `CreationDate` | |
| Elastic IP | — | CloudTrail only |
| Security group / VPC / subnet / route table | — | CloudTrail only |
| ASG | `CreatedTime` | |
| Launch template | `CreateTime` | |
| S3 bucket | `CreationDate` (from `list-buckets`) | |
| EFS | `CreationTime` | |
| FSx | `CreationTime` | |
| RDS instance | `InstanceCreateTime` | |
| RDS/Aurora cluster | `ClusterCreateTime` | |
| RDS snapshot | `SnapshotCreateTime` | |
| DynamoDB table | `CreationDateTime` | |
| ElastiCache cluster | `CacheClusterCreateTime` | |
| Redshift cluster | `ClusterCreateTime` | |
| OpenSearch domain | `Created` flag only | CloudTrail for the timestamp |
| Lambda function | `LastModified` only | **Creation not exposed** — CloudTrail required |
| ECS service | `createdAt` | |
| ECS task definition | `registeredAt` | |
| ECS task | `createdAt` | |
| EKS cluster / node group / Fargate profile | `createdAt` | |
| ECR repository | `createdAt` | |
| Elastic Beanstalk app / env | `DateCreated` | |
| ALB/NLB | `CreatedTime` | |
| Classic ELB | `CreatedTime` | |
| Target group | — | CloudTrail only |
| CloudFront distribution | `LastModifiedTime` only | CloudTrail for creation |
| Route 53 hosted zone | — | CloudTrail only |
| IAM user/role/group/policy | `CreateDate` | |
| Access key | `CreateDate` | |
| KMS key | `CreationDate` | |
| Secrets Manager secret | `CreatedDate` | |
| ACM certificate | `CreatedAt` | |
| SQS queue | `CreatedTimestamp` attribute | Epoch seconds |
| SNS topic | — | CloudTrail only |
| CloudWatch log group | `creationTime` | Epoch **milliseconds** |
| CloudFormation stack | `CreationTime` | |
| Step Functions state machine | `creationDate` | |
| API Gateway REST API | `createdDate` | |
| API Gateway v2 API | `CreatedDate` | |
| Config-recorded resource | `resourceCreationTime` | Works for many types at once |

**Epoch conversion:**

```powershell
[DateTimeOffset]::FromUnixTimeMilliseconds($ms).UtcDateTime.ToString("o")   # log groups
[DateTimeOffset]::FromUnixTimeSeconds($s).UtcDateTime.ToString("o")         # SQS
```

---

## 3. Creator Attribution via CloudTrail

### 3.1 The hard limit

`cloudtrail lookup-events` reads **CloudTrail Event history**, which retains **90 days**. Anything created before that window cannot be attributed this way. **State this explicitly in every report** — an unattributed 3-year-old resource is a data limitation, not a finding of poor governance.

### 3.2 Efficient bulk strategy (preferred)

Do not run one lookup per resource. Instead, pull creation events once per region and join.

```powershell
$creationEvents = @(
  'RunInstances','CreateVolume','CreateSnapshot','CreateImage','AllocateAddress',
  'CreateSecurityGroup','CreateVpc','CreateSubnet','CreateRouteTable','CreateNatGateway',
  'CreateLoadBalancer','CreateTargetGroup','CreateAutoScalingGroup','CreateLaunchTemplate',
  'CreateDBInstance','CreateDBCluster','CreateDBSnapshot','CreateTable','CreateCacheCluster',
  'CreateReplicationGroup','CreateCluster','CreateService','RegisterTaskDefinition',
  'CreateNodegroup','CreateRepository','CreateFunction20150331','CreateBucket',
  'CreateQueue','CreateTopic','CreateStack','CreateKey','CreateSecret',
  'CreateRole','CreateUser','CreateAccessKey','CreateHostedZone','CreateDistribution',
  'CreateApplication','CreateEnvironment','CreateFileSystem','CreateLogGroup'
)

foreach ($e in $creationEvents) {
  aws cloudtrail lookup-events `
    --lookup-attributes AttributeKey=EventName,AttributeValue=$e `
    --start-time (Get-Date).AddDays(-90).ToString("yyyy-MM-ddTHH:mm:ssZ") `
    --end-time   (Get-Date).ToString("yyyy-MM-ddTHH:mm:ssZ") `
    --region $R --output json --no-cli-pager
}
```

Then join each event to the inventory using the resource ID found in `CloudTrailEvent` → `responseElements` or `requestParameters`.

### 3.3 Per-resource lookup (fallback for high-value resources)

```powershell
aws cloudtrail lookup-events `
  --lookup-attributes AttributeKey=ResourceName,AttributeValue=<resource-id> `
  --max-results 50 --region $R --output json --no-cli-pager
```

`ResourceName` matching works for many but not all resource types. `AttributeKey=ResourceType` (e.g. `AWS::EC2::Instance`) is a useful complement.

### 3.4 Parsing the event

`CloudTrailEvent` is a **JSON string** inside the response — parse it, then extract:

| Field | Meaning |
|-------|---------|
| `eventTime` | Authoritative creation time |
| `userIdentity.type` | `IAMUser`, `AssumedRole`, `Root`, `AWSService`, `AWSAccount`, `FederatedUser` |
| `userIdentity.arn` | Full principal ARN |
| `userIdentity.userName` | For IAM users |
| `userIdentity.sessionContext.sessionIssuer.userName` | The **role** behind an assumed session — usually what you want |
| `userIdentity.principalId` | For SSO: `AROA...:<user-identity>`; take the part after `:` |
| `userIdentity.invokedBy` | Set when an AWS service made the call |
| `sourceIPAddress` | Origin (also `AWS Internal` for service-initiated calls) |
| `userAgent` | **How** it was created |
| `requestParameters` / `responseElements` | The resource ID to join on |
| `errorCode` | Skip failed events |

### 3.5 `userAgent` → `createdVia` mapping

| `userAgent` contains | `createdVia` |
|----------------------|--------------|
| `console.amazonaws.com`, `AWS Internal`, `signin.amazonaws.com` | `console` |
| `aws-cli/` | `cli` |
| `Terraform`, `HashiCorp`, `APN/1.0 HashiCorp` | `terraform` |
| `cloudformation.amazonaws.com` | `cloudformation` |
| `Pulumi` | `pulumi` |
| `aws-cdk` | `cdk` (usually surfaces as CloudFormation) |
| `Boto3`, `aws-sdk-go`, `aws-sdk-java`, `aws-sdk-js`, `Botocore` | `sdk` |
| `<service>.amazonaws.com` (e.g. `autoscaling.amazonaws.com`) | `service` |
| `serverless`, `sam-cli` | `sdk` |

`createdVia = console` is one of the most actionable governance findings — it identifies infrastructure that exists outside any code repository.

### 3.6 Beyond 90 days — Athena over the CloudTrail S3 bucket

Only if Phase 0 found a trail with an S3 destination. **Athena scans are billed** — obtain consent and always partition-prune.

```sql
-- Creation events for the last 24 months, excluding service-initiated calls
SELECT
  eventtime,
  eventname,
  useridentity.type          AS principal_type,
  useridentity.arn           AS principal_arn,
  useridentity.sessioncontext.sessionissuer.username AS role_name,
  sourceipaddress,
  useragent,
  requestparameters,
  responseelements
FROM cloudtrail_logs
WHERE eventname LIKE 'Create%' OR eventname IN ('RunInstances','AllocateAddress')
  AND useridentity.type <> 'AWSService'
  AND errorcode IS NULL
  AND year   BETWEEN '2024' AND '2026'
ORDER BY eventtime DESC;
```

Check whether a Glue table already exists before proposing to create one — **creating a table is a mutating operation and is out of scope for this agent.** If no table exists, hand the SQL to the user with instructions and let them decide.

### 3.7 Alternative sources when CloudTrail is unavailable

| Source | What it gives |
|--------|---------------|
| CloudFormation `describe-stack-events` | The principal that created stack resources, for the full stack history |
| `iam get-role` → `RoleLastUsed` | Whether a role is still active and from which region |
| `iam get-access-key-last-used` | Key activity and the service used |
| Config `get-resource-config-history` | Configuration change history where Config is recording |
| Resource tags | `Owner`, `CreatedBy`, `created-by`, `Creator`, `Contact` |

---

## 4. Ownership Resolution

Apply in order and record the confidence:

| Order | Rule | Confidence |
|-------|------|-----------|
| 1 | CloudTrail principal resolved to a human/SSO identity | `HIGH` |
| 2 | `Owner` / `CreatedBy` / `Contact` tag present | `MEDIUM` |
| 3 | Member of a CloudFormation stack carrying an owner tag | `MEDIUM` |
| 4 | `Team` / `CostCenter` tag present (team-level, not individual) | `MEDIUM` |
| 5 | Naming prefix matching a known team convention | `LOW` |
| 6 | Nothing found | `UNKNOWN` |

When CloudTrail names a **role** rather than a person (CI/CD pipelines, automation), record the role as the owner and mark `createdVia` accordingly — "owned by the deployment pipeline" is a valid and useful answer.

**Never invent an owner.** `UNKNOWN` with a cost figure attached is the finding that drives action.

### Ownership output

| Owner | Type | Resources | Accounts | Est. monthly cost | Untagged | Console-created |
|-------|------|-----------|----------|-------------------|----------|-----------------|
| platform-team | team | 214 | 2 | $4,120 | 6 | 12 |
| ci-deploy-role | automation | 96 | 1 | $1,880 | 0 | 0 |
| *UNKNOWN* | — | 87 | 3 | $1,940 | 87 | ? |

---

## 5. Cost Attribution

### ⚠️ Consent first
Cost Explorer bills **per API request** (~$0.01). Tell the user the planned request count before calling, and batch the queries.

### Core queries

```powershell
# By service
aws ce get-cost-and-usage --time-period Start=<YYYY-MM-DD>,End=<YYYY-MM-DD> `
  --granularity MONTHLY --metrics UnblendedCost `
  --group-by Type=DIMENSION,Key=SERVICE --region us-east-1 --output json --no-cli-pager

# By region
aws ce get-cost-and-usage --time-period Start=<...>,End=<...> `
  --granularity MONTHLY --metrics UnblendedCost `
  --group-by Type=DIMENSION,Key=REGION --region us-east-1 --output json --no-cli-pager

# By linked account (Organizations management account only)
aws ce get-cost-and-usage --time-period Start=<...>,End=<...> `
  --granularity MONTHLY --metrics UnblendedCost `
  --group-by Type=DIMENSION,Key=LINKED_ACCOUNT --region us-east-1 --output json --no-cli-pager

# By tag (requires the key to be an activated cost allocation tag)
aws ce get-cost-and-usage --time-period Start=<...>,End=<...> `
  --granularity MONTHLY --metrics UnblendedCost `
  --group-by Type=TAG,Key=Owner --region us-east-1 --output json --no-cli-pager

# By usage type within a service (finds the specific driver)
aws ce get-cost-and-usage --time-period Start=<...>,End=<...> `
  --granularity MONTHLY --metrics UnblendedCost `
  --filter '{"Dimensions":{"Key":"SERVICE","Values":["Amazon Elastic Compute Cloud - Compute"]}}' `
  --group-by Type=DIMENSION,Key=USAGE_TYPE --region us-east-1 --output json --no-cli-pager

# Which cost allocation tags are actually active
aws ce list-cost-allocation-tags --status Active --region us-east-1 --output json --no-cli-pager
```

### Optimization signals

```powershell
aws ce get-rightsizing-recommendation --service AmazonEC2 --region us-east-1 --output json --no-cli-pager
aws ce get-reservation-utilization --time-period Start=<...>,End=<...> --region us-east-1 --output json --no-cli-pager
aws ce get-reservation-purchase-recommendation --service AmazonEC2 --region us-east-1 --output json --no-cli-pager
aws ce get-savings-plans-utilization --time-period Start=<...>,End=<...> --region us-east-1 --output json --no-cli-pager
aws ce get-anomalies --date-interval StartDate=<...>,EndDate=<...> --region us-east-1 --output json --no-cli-pager
aws compute-optimizer get-ec2-instance-recommendations --output json --no-cli-pager
aws compute-optimizer get-ebs-volume-recommendations --output json --no-cli-pager
aws compute-optimizer get-lambda-function-recommendations --output json --no-cli-pager
aws compute-optimizer get-auto-scaling-group-recommendations --output json --no-cli-pager
```

### Attributing cost to individual resources

Cost Explorer groups by dimension, not by ARN, so per-resource cost is an **allocation, not a measurement**:

1. `RESOURCE_ID` grouping is available only when Cost Explorer resource-level data is enabled (extra charge)
2. Otherwise, distribute a service's regional cost across that service's resources in that region, weighted by size (instance type, allocated storage, provisioned capacity)
3. Always label these figures as **estimated** and state the allocation method

### Waste candidates to price explicitly

| Waste | Detection | Typical cost |
|-------|-----------|--------------|
| Unattached EBS volumes | `State: available` | Full volume price |
| Unassociated Elastic IPs | No `AssociationId` | Hourly idle charge |
| Stopped EC2 with attached EBS | `State: stopped` + volumes | EBS only, but often forgotten |
| Idle load balancers | Zero healthy targets | Full LB hourly + LCU |
| Unused NAT Gateways | No routes pointing at them | Hourly + data processing |
| Never-expiring log groups | `retentionInDays: null` + large `storedBytes` | Storage per GB-month |
| Old manual snapshots | `StartTime` older than 1 year | Storage per GB-month |
| Empty ASGs | `DesiredCapacity: 0` | Usually zero, but signals abandonment |
| Provisioned DynamoDB with low utilization | Provisioned mode + low consumed metrics | Provisioned capacity |
| Over-provisioned RDS | Compute Optimizer / low CPU metrics | Instance hours |
| Orphaned ECR images | No lifecycle policy + large repo size | Storage per GB-month |

---

## 6. Enriched Record Additions

Phase 3 adds these fields to every inventory record:

```json
{
  "createdOn": "2023-04-11T18:22:04Z",
  "createdOnSource": "rds:InstanceCreateTime",
  "createdBy": "arn:aws:sts::111111111111:assumed-role/AWSReservedSSO_Admin_x/hbarbosa",
  "createdByDisplay": "hbarbosa",
  "createdVia": "console",
  "attributionConfidence": "HIGH",
  "attributionSource": "cloudtrail:CreateDBInstance@2023-04-11T18:22:04Z",
  "owner": "platform-team",
  "ownerSource": "tag:Owner",
  "ownerConfidence": "MEDIUM",
  "estimatedMonthlyCost": 412.60,
  "costAllocationMethod": "service-region-weighted-by-instance-class",
  "tagCompliance": { "Environment": true, "Owner": true, "Application": true, "CostCenter": false }
}
```

---

## 7. Enrichment Quality Checklist

```
[ ] Tags merged from all three sources
[ ] Non-taggable resource types excluded from coverage denominators
[ ] createdOn populated from native fields where they exist
[ ] createdOnSource recorded so the figure is auditable
[ ] CloudTrail bulk pull done once per region, not per resource
[ ] 90-day limitation stated in the report
[ ] createdVia derived from userAgent
[ ] Ownership resolved with an explicit confidence level
[ ] UNKNOWN owners counted and costed
[ ] Cost Explorer consent obtained before any ce: call
[ ] Cost figures labeled as directional with the allocation method stated
[ ] Waste candidates identified and priced
```
