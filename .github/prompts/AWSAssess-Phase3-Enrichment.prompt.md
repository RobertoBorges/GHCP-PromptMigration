---
name: Phase3-Enrichment
description: Enrich the inventory with tags, creation date, creator identity, ownership and cost attribution
argument-hint: "Optionally scope enrichment, e.g., 'Only attribute creators for EC2 and RDS' or 'Skip cost analysis'"
agent: AWS Account Assessment Agent
---

# Phase 3 — Metadata Enrichment

**Goal:** answer *who owns this, when was it created, who created it, and what does it cost* for every resource in the inventory.

**Prerequisite:** Phase 2 normalized inventory exists.

Load the **aws-metadata-enrichment** skill.

---

## Step 1: Tag Consolidation

For every resource, merge tags from all sources (Tagging API, native `describe` output, Config) into a single tag map.

Then compute tag hygiene metrics:

| Metric | Definition |
|--------|-----------|
| Tag coverage | % of taggable resources with ≥1 tag |
| Required-tag coverage | % with each key of the required tag set |
| Untagged resources | Absolute count and list |
| Tag key variants | Case/spelling variants of the same intent (`owner`, `Owner`, `OWNER`, `own er`) |
| Value cardinality | Distinct values per key — high cardinality on `Environment` signals inconsistency |

Ask the user for the **required tag set** if not already known. Default proposal:

`Environment`, `Owner`, `Application`, `CostCenter`, `ManagedBy`

---

## Step 2: Creation Date

Prefer the resource's native creation field. Never guess.

| Resource type | Field |
|---------------|-------|
| EC2 instance | `LaunchTime` |
| EBS volume | `CreateTime` |
| EBS snapshot | `StartTime` |
| AMI | `CreationDate` |
| Security group | *(none — use CloudTrail)* |
| VPC / subnet | *(none — use CloudTrail)* |
| S3 bucket | `CreationDate` from `list-buckets` |
| RDS instance | `InstanceCreateTime` |
| RDS/Aurora cluster | `ClusterCreateTime` |
| DynamoDB table | `CreationDateTime` |
| Lambda function | `LastModified` *(creation not exposed — use CloudTrail)* |
| ECS service | `createdAt` |
| ECS task definition | `registeredAt` |
| EKS cluster | `createdAt` |
| EKS node group | `createdAt` |
| ECR repository | `createdAt` |
| Elastic Beanstalk env | `DateCreated` |
| ELB / ALB / NLB | `CreatedTime` |
| IAM user / role / policy | `CreateDate` |
| KMS key | `CreationDate` |
| CloudFormation stack | `CreationTime` |
| CloudWatch log group | `creationTime` (epoch ms) |
| Secrets Manager secret | `CreatedDate` |
| ACM certificate | `CreatedAt` |
| Config-recorded resource | `resourceCreationTime` |

When no native field exists, mark `createdOn` as `null` and let CloudTrail fill it.

---

## Step 3: Creator Attribution ("who created it")

### 3.a — CloudTrail lookup (default, 90-day window)

```powershell
aws cloudtrail lookup-events `
  --lookup-attributes AttributeKey=ResourceName,AttributeValue=<resource-id> `
  --max-results 50 `
  --region <region> `
  --output json --no-cli-pager
```

Or search by the creating event name across a time window:

```powershell
aws cloudtrail lookup-events `
  --lookup-attributes AttributeKey=EventName,AttributeValue=RunInstances `
  --start-time 2026-05-21T00:00:00Z --end-time 2026-08-19T00:00:00Z `
  --region <region> `
  --output json --no-cli-pager
```

Extract from the matching event:
- `userIdentity.arn` → the principal
- `userIdentity.type` → `IAMUser` / `AssumedRole` / `Root` / `AWSService`
- `userIdentity.sessionContext.sessionIssuer.userName` → the underlying role for assumed sessions
- `userIdentity.principalId` → for SSO sessions, the part after `:` is usually the user identity
- `eventTime` → authoritative creation time
- `sourceIPAddress` and `userAgent` → distinguishes console vs CLI vs Terraform vs CloudFormation

**Interpret the user agent** — this is often more useful than the principal:

| `userAgent` contains | Means |
|----------------------|-------|
| `console.amazonaws.com` / `AWS Internal` | Created manually in the AWS Console |
| `aws-cli/` | Created from the CLI |
| `Terraform` / `HashiCorp` | Provisioned by Terraform |
| `cloudformation.amazonaws.com` | Provisioned by CloudFormation/CDK/SAM |
| `Boto3` / `aws-sdk-*` | Created by an application or script |
| `<service>.amazonaws.com` | Created by another AWS service on your behalf |

### 3.b — Beyond 90 days (Athena over the CloudTrail S3 bucket)

**⚠️ State the 90-day limit clearly to the user.** `lookup-events` only covers CloudTrail Event history for the last 90 days.

If Phase 0 detected a trail writing to S3, offer the Athena path. The agent may generate the query but must ask for consent because Athena scans are billed:

```sql
SELECT eventtime, eventname, useridentity.arn, useridentity.type,
       sourceipaddress, useragent, requestparameters, responseelements
FROM cloudtrail_logs
WHERE eventname IN ('RunInstances','CreateDBInstance','CreateDBCluster','CreateFunction20150331',
                    'CreateCluster','CreateService','CreateBucket','CreateVpc','CreateRepository')
  AND useridentity.type <> 'AWSService'
ORDER BY eventtime DESC;
```

### 3.c — Fallback chain

Apply in order and record the confidence level:

| Order | Source | Confidence |
|-------|--------|-----------|
| 1 | CloudTrail event found | `HIGH` |
| 2 | `Owner` / `CreatedBy` / `Contact` tag | `MEDIUM` |
| 3 | CloudFormation stack owner / IaC-managed | `MEDIUM` |
| 4 | Naming convention match (e.g. `team-x-*`) | `LOW` |
| 5 | Nothing found | `UNKNOWN` |

**Never invent an owner.** `UNKNOWN` is a valid and useful finding.

### 3.d — Scope control

Attributing every resource individually is expensive. Default strategy:
1. Bulk-pull CloudTrail write events for the last 90 days once per region, filtered to creation event names
2. Join those events against the inventory by resource ID/ARN found in `requestParameters`/`responseElements`
3. Only do per-resource `lookup-events` for high-value resources still unattributed (EC2, RDS, EKS, S3, IAM roles)

---

## Step 4: Ownership Resolution

Produce a single `owner` field per resource by combining:
- `Owner` / `Team` / `CostCenter` tags
- CloudTrail principal (mapped to a human where the ARN is an IAM user or SSO identity)
- CloudFormation stack → stack tags → stack owner
- IAM role trust relationships (a role assumed only by one pipeline identifies that pipeline as the owner)

Output an **ownership coverage table**:

| Owner | Resources | Accounts | Est. monthly cost | Untagged resources |
|-------|-----------|----------|-------------------|--------------------|
| platform-team | 214 | 2 | $4,120 | 6 |
| *UNKNOWN* | 87 | 3 | $1,940 | 87 |

---

## Step 5: Cost Attribution

**⚠️ Warn the user first:** Cost Explorer API requests are billed (~$0.01 per request). Confirm before proceeding.

### By service

```powershell
aws ce get-cost-and-usage `
  --time-period Start=2026-05-01,End=2026-08-01 `
  --granularity MONTHLY --metrics UnblendedCost `
  --group-by Type=DIMENSION,Key=SERVICE `
  --region us-east-1 --output json --no-cli-pager
```

### By region

```powershell
aws ce get-cost-and-usage `
  --time-period Start=2026-05-01,End=2026-08-01 `
  --granularity MONTHLY --metrics UnblendedCost `
  --group-by Type=DIMENSION,Key=REGION `
  --region us-east-1 --output json --no-cli-pager
```

### By tag (requires the tag key to be activated as a cost allocation tag)

```powershell
aws ce get-cost-and-usage `
  --time-period Start=2026-05-01,End=2026-08-01 `
  --granularity MONTHLY --metrics UnblendedCost `
  --group-by Type=TAG,Key=Owner `
  --region us-east-1 --output json --no-cli-pager
```

### By linked account (Organizations management account only)

```powershell
aws ce get-cost-and-usage `
  --time-period Start=2026-05-01,End=2026-08-01 `
  --granularity MONTHLY --metrics UnblendedCost `
  --group-by Type=DIMENSION,Key=LINKED_ACCOUNT `
  --region us-east-1 --output json --no-cli-pager
```

### Optimization signals

```powershell
aws ce get-rightsizing-recommendation --service AmazonEC2 --region us-east-1 --output json --no-cli-pager
aws compute-optimizer get-ec2-instance-recommendations --output json --no-cli-pager
aws ce get-reservation-utilization --time-period Start=2026-05-01,End=2026-08-01 --region us-east-1 --output json --no-cli-pager
aws ce get-savings-plans-utilization --time-period Start=2026-05-01,End=2026-08-01 --region us-east-1 --output json --no-cli-pager
```

Correlate the top cost drivers back to the inventory so the report can show **expensive resources with no owner** — usually the highest-value finding in the whole assessment.

Always state that figures are **directional** and point to the AWS Cost Explorer console for authoritative numbers.

---

## Step 6: Write The Enriched Dataset

Update every inventory record with `createdOn`, `createdBy`, `createdVia`, `attributionConfidence`, `owner` and `estimatedMonthlyCost`, then write:

- `reports/raw/<account-id>/_inventory-enriched.json`
- `reports/inventory.csv` (flat, all accounts, re-generated from every account folder present)

CSV columns:

```
AccountId,AccountAlias,Region,Service,ResourceType,ResourceId,ResourceName,State,
CreatedOn,CreatedBy,CreatedVia,AttributionConfidence,Owner,Environment,Application,
CostCenter,ManagedBy,EstimatedMonthlyCost,PubliclyAccessible,Encrypted,Arn,AllTags
```

---

## Exit Criteria

- [ ] Tags consolidated and hygiene metrics computed
- [ ] `createdOn` populated from native fields wherever available
- [ ] Creator attribution attempted, with the 90-day limitation stated explicitly
- [ ] Attribution confidence recorded per resource
- [ ] Ownership resolved or explicitly marked `UNKNOWN`
- [ ] Cost attributed by service, region, tag and account (if enabled)
- [ ] `reports/inventory.csv` regenerated across all scanned accounts
- [ ] `Report-Status.md` updated

**Next step:** proceed to `/AWSAssess-phase4-relationships`
