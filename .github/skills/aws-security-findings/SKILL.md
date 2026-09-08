---
name: aws-security-findings
description: Finding catalog and severity model for an AWS account assessment — internet exposure, encryption gaps, IAM and credential hygiene, network risk, EOL runtimes and engines, backup and resilience gaps, orphaned resources, and how to consume GuardDuty, Security Hub, AWS Config, Inspector and Access Analyzer results. Use during Phase 4 and Phase 5.
---

# AWS Security & Governance Findings Skill

The finding catalog. Every finding must carry: **severity**, **affected resource ARNs**, **the API evidence used**, and **a concrete recommendation**.

## Severity model

| Severity | Criteria |
|----------|----------|
| 🔴 **Critical** | Direct, unauthenticated internet exposure of data or admin control; publicly assumable roles; root access keys |
| 🟠 **High** | Exposure requiring one additional condition; unencrypted sensitive data; broad privileged access; unsupported production engines |
| 🟡 **Medium** | Weak configuration, missing defense-in-depth, resilience gaps, EOL approaching |
| 🟢 **Low** | Hygiene, best-practice deviations, minor waste |
| ℹ️ **Informational** | Observations with no direct risk (e.g. resource created via console) |

**Rule:** never report a severity without the evidence that justifies it. Never infer exploitability that has not been observed.

---

## 1. Internet Exposure

| ID | Finding | Severity | Detection |
|----|---------|----------|-----------|
| EXP-01 | Publicly accessible RDS / Aurora / DocumentDB / Neptune / Redshift | 🔴 | `PubliclyAccessible: true` **and** an SG allowing the DB port from `0.0.0.0/0` |
| EXP-02 | Public S3 bucket | 🔴 | `get-public-access-block` disabled **or** `get-bucket-policy-status.IsPublic: true` **or** an ACL granting `AllUsers`/`AuthenticatedUsers` |
| EXP-03 | Security group allowing `0.0.0.0/0` on an administrative port | 🔴 | Ingress `0.0.0.0/0` or `::/0` on 22, 3389, 5985/5986, 5900 |
| EXP-04 | Security group allowing `0.0.0.0/0` on a database port | 🔴 | Ingress `0.0.0.0/0` on 3306, 5432, 1433, 1521, 27017, 6379, 11211, 9200, 9092, 5439 |
| EXP-05 | Security group allowing all ports from `0.0.0.0/0` | 🔴 | `IpProtocol: -1` with `CidrIp: 0.0.0.0/0` |
| EXP-06 | Public EKS API endpoint open to the world | 🟠 | `endpointPublicAccess: true` **and** `publicAccessCidrs` contains `0.0.0.0/0` |
| EXP-07 | Lambda function URL without auth | 🟠 | `get-function-url-config` → `AuthType: NONE` |
| EXP-08 | API Gateway route without an authorizer | 🟠 | No authorizer and `authorizationType: NONE` on non-public-by-design routes |
| EXP-09 | Public ECR repository or repository policy granting `*` | 🟠 | `ecr-public describe-repositories`; repository policy `Principal: "*"` |
| EXP-10 | Publicly shared EBS snapshot or AMI | 🔴 | `describe-snapshot-attribute --attribute createVolumePermission` → `Group: all`; `describe-image-attribute --attribute launchPermission` → `Group: all` |
| EXP-11 | Internet-facing load balancer fronting an unauthenticated backend | 🟡 | `Scheme: internet-facing` with no WAF association and no auth action on the listener |
| EXP-12 | Elastic IP attached to a non-hardened instance | 🟡 | EIP association + permissive SG |
| EXP-13 | OpenSearch / ElastiCache reachable from a public subnet | 🟠 | Domain/cluster in a public subnet with a permissive SG |
| EXP-14 | Dangling DNS record | 🟠 | Route 53 record target not present in the inventory (deleted ALB, released EIP, deleted bucket) — subdomain takeover risk |

---

## 2. Encryption

| ID | Finding | Severity | Detection |
|----|---------|----------|-----------|
| ENC-01 | Unencrypted RDS / Aurora | 🟠 | `StorageEncrypted: false` |
| ENC-02 | Unencrypted EBS volume | 🟠 | `Encrypted: false` |
| ENC-03 | Unencrypted EBS snapshot | 🟠 | `Encrypted: false` |
| ENC-04 | S3 bucket without default encryption | 🟡 | `get-bucket-encryption` throws `ServerSideEncryptionConfigurationNotFoundError` |
| ENC-05 | Unencrypted EFS / FSx | 🟠 | `Encrypted: false` |
| ENC-06 | Unencrypted DynamoDB (AWS-owned key only) | 🟢 | `SSEDescription` absent — encrypted by default but not with a CMK |
| ENC-07 | Unencrypted SQS / SNS | 🟡 | No `KmsMasterKeyId` |
| ENC-08 | Unencrypted CloudWatch log group | 🟢 | No `kmsKeyId` |
| ENC-09 | EKS secrets not encrypted with KMS | 🟠 | `encryptionConfig` empty |
| ENC-10 | KMS key rotation disabled | 🟡 | `get-key-rotation-status.KeyRotationEnabled: false` on a customer-managed key |
| ENC-11 | ELB listener without TLS or with an outdated policy | 🟠 | Listener `Protocol: HTTP` on an internet-facing LB, or an `SslPolicy` permitting TLS 1.0/1.1 |
| ENC-12 | S3 bucket policy not enforcing TLS | 🟡 | No `aws:SecureTransport: false` deny statement |

---

## 3. IAM & Credentials

| ID | Finding | Severity | Detection |
|----|---------|----------|-----------|
| IAM-01 | Root account access keys exist | 🔴 | Credential report → `access_key_1_active` for `<root_account>` |
| IAM-02 | Root account used recently | 🔴 | CloudTrail `userIdentity.type: Root`, or credential report `password_last_used` |
| IAM-03 | Root without MFA | 🔴 | `get-account-summary` → `AccountMFAEnabled: 0` |
| IAM-04 | IAM user with console access and no MFA | 🟠 | Credential report `password_enabled: true` + `mfa_active: false` |
| IAM-05 | Access key older than 90 days | 🟡 | `list-access-keys` → `CreateDate` |
| IAM-06 | Access key unused for 90+ days | 🟡 | `get-access-key-last-used` → `LastUsedDate` |
| IAM-07 | Policy granting `Action: "*"` on `Resource: "*"` | 🟠 | Inline or customer-managed policy documents |
| IAM-08 | Role assumable by `"AWS": "*"` | 🔴 | Trust policy `Principal.AWS: "*"` |
| IAM-09 | Cross-account trust to an account outside the organization | 🟠 | Trust policy principal account not in `organizations list-accounts` |
| IAM-10 | Cross-account role without `sts:ExternalId` | 🟡 | Third-party trust with no external-ID condition (confused-deputy risk) |
| IAM-11 | Unused IAM role (no activity in 90+ days) | 🟢 | `get-role` → `RoleLastUsed.LastUsedDate` |
| IAM-12 | Unused IAM user | 🟢 | Credential report shows no password or key usage |
| IAM-13 | Weak password policy or none | 🟡 | `get-account-password-policy` |
| IAM-14 | Inline policies used instead of managed policies | 🟢 | `list-role-policies` / `list-user-policies` non-empty |
| IAM-15 | Users with directly attached policies instead of group membership | 🟢 | `list-attached-user-policies` non-empty |
| IAM-16 | Wildcard `iam:PassRole` | 🟠 | Policy allowing `iam:PassRole` on `*` — privilege-escalation path |
| IAM-17 | Service accounts with console passwords | 🟡 | Credential report: programmatic user with `password_enabled: true` |

---

## 4. Network

| ID | Finding | Severity | Detection |
|----|---------|----------|-----------|
| NET-01 | VPC Flow Logs not enabled | 🟡 | No flow log for the VPC |
| NET-02 | Default VPC still in use | 🟢 | `IsDefault: true` with resources attached |
| NET-03 | Default security group allows traffic | 🟡 | Default SG with any ingress rule |
| NET-04 | Unrestricted egress (`0.0.0.0/0` on all ports) | 🟢 | Common but worth listing for data-exfiltration posture |
| NET-05 | Overly permissive NACL | 🟡 | Allow-all rules with a lower rule number than the denies |
| NET-06 | Cross-account VPC peering to an external account | 🟠 | Peering accepter/requester outside the organization |
| NET-07 | Transit Gateway shared with an external account | 🟠 | RAM share to a non-org account |
| NET-08 | No WAF on internet-facing ALB / CloudFront | 🟡 | No Web ACL association |
| NET-09 | Unused security groups | 🟢 | Not referenced by any ENI or other SG |
| NET-10 | Subnet auto-assigning public IPs | 🟡 | `MapPublicIpOnLaunch: true` on a subnet hosting workloads |
| NET-11 | NAT Gateway in a single AZ for a multi-AZ workload | 🟡 | Resilience gap |
| NET-12 | Expiring or expired ACM certificate | 🟠 | `NotAfter` within 30 days, or `Status: EXPIRED` while `InUseBy` is non-empty |

---

## 5. End-of-Life & Unsupported Versions

Always verify against current AWS documentation rather than a hard-coded list — deprecation dates move.

| ID | Finding | Severity | Detection |
|----|---------|----------|-----------|
| EOL-01 | RDS engine version out of standard support | 🟠 | Compare `EngineVersion` with `describe-db-engine-versions`; check for RDS Extended Support charges |
| EOL-02 | Deprecated Lambda runtime | 🟠 | `Runtime` matching an AWS-announced deprecated runtime |
| EOL-03 | EKS cluster in extended support or unsupported | 🟠 | `version` below the supported window |
| EOL-04 | Retired Elastic Beanstalk solution stack | 🟠 | `SolutionStackName` no longer in `list-available-solution-stacks` |
| EOL-05 | Unsupported OS on EC2 | 🟠 | AMI/platform indicating an out-of-support OS (Windows Server 2012 R2, Amazon Linux 1, CentOS 7, Ubuntu below LTS support) |
| EOL-06 | Previous-generation instance family | 🟢 | `t1`, `m1`, `m2`, `m3`, `c1`, `c3`, `cc2`, `cr1`, `hs1`, `i2`, `r3`, `g2` |
| EOL-07 | Previous-generation EBS volume type | 🟢 | `standard` (magnetic), `gp2` where `gp3` is cheaper and faster |
| EOL-08 | Classic Load Balancer in use | 🟡 | Any `elb describe-load-balancers` result |
| EOL-09 | EC2-Classic or ClassicLink artifacts | 🟡 | Retired platform |
| EOL-10 | Outdated ElastiCache / OpenSearch engine version | 🟡 | Engine version below the supported window |
| EOL-11 | Container image with known critical CVEs | 🟠 | `ecr describe-image-scan-findings` → CRITICAL/HIGH counts |
| EOL-12 | Container base image not scanned | 🟡 | `imageScanningConfiguration.scanOnPush: false` |

---

## 6. Resilience & Backup

| ID | Finding | Severity | Detection |
|----|---------|----------|-----------|
| RES-01 | Production RDS without Multi-AZ | 🟠 | `MultiAZ: false` on a resource tagged `Environment=prod` |
| RES-02 | RDS backup retention of 0–1 days | 🟠 | `BackupRetentionPeriod` |
| RES-03 | RDS deletion protection disabled | 🟡 | `DeletionProtection: false` |
| RES-04 | DynamoDB without point-in-time recovery | 🟡 | `describe-continuous-backups` → `PointInTimeRecoveryStatus: DISABLED` |
| RES-05 | S3 bucket without versioning | 🟡 | `get-bucket-versioning` not `Enabled` |
| RES-06 | Single-AZ workload in production | 🟠 | All instances/tasks of an application in one AZ |
| RES-07 | ASG spanning a single subnet/AZ | 🟡 | One `VPCZoneIdentifier` entry |
| RES-08 | No AWS Backup plan protecting a resource type in use | 🟡 | `list-protected-resources` vs inventory |
| RES-09 | EBS volume with no recent snapshot | 🟢 | Newest snapshot older than 30 days |
| RES-10 | Aurora cluster with a single instance | 🟡 | No reader instance |
| RES-11 | ECS service with `desiredCount: 1` in production | 🟡 | Single task, no redundancy |

---

## 7. Logging & Monitoring

| ID | Finding | Severity | Detection |
|----|---------|----------|-----------|
| LOG-01 | CloudTrail not enabled, or not multi-region | 🔴 | `describe-trails` empty, or `IsMultiRegionTrail: false` |
| LOG-02 | CloudTrail log file validation disabled | 🟡 | `LogFileValidationEnabled: false` |
| LOG-03 | CloudTrail trail not logging | 🟠 | `get-trail-status` → `IsLogging: false` |
| LOG-04 | AWS Config not recording | 🟡 | No configuration recorder, or recorder stopped |
| LOG-05 | GuardDuty not enabled in a region with resources | 🟠 | `list-detectors` empty where resources exist |
| LOG-06 | Security Hub not enabled | 🟡 | `describe-hub` fails |
| LOG-07 | S3 server access logging disabled on a sensitive bucket | 🟢 | `get-bucket-logging` empty |
| LOG-08 | ALB access logs disabled | 🟢 | Attribute `access_logs.s3.enabled: false` |
| LOG-09 | Log group with no retention policy | 🟢 | `retentionInDays: null` — cost and compliance issue |
| LOG-10 | No CloudWatch alarms on critical resources | 🟢 | Production RDS/EC2/ECS with zero alarms |

---

## 8. Governance & Cost

| ID | Finding | Severity | Detection |
|----|---------|----------|-----------|
| GOV-01 | Resources without any tag | 🟡 | Empty tag map |
| GOV-02 | Resources missing required tags | 🟡 | Required tag set not fully present |
| GOV-03 | Resources with unknown owner | 🟡 | `owner: UNKNOWN` — report the associated cost |
| GOV-04 | Resources created via console (not IaC) | ℹ️ | `createdVia: console` |
| GOV-05 | Resources not managed by CloudFormation/Terraform | 🟢 | Not in any stack's resource list and no `ManagedBy` tag |
| GOV-06 | Orphaned resources | 🟢 | Zero HIGH-confidence graph edges (see the relationships skill) |
| GOV-07 | Unattached EBS volumes | 🟢 | `State: available` — direct waste |
| GOV-08 | Unassociated Elastic IPs | 🟢 | No `AssociationId` — hourly charge for nothing |
| GOV-09 | Idle load balancers | 🟢 | Zero healthy targets |
| GOV-10 | Suspended organization accounts still holding resources | 🟡 | `Status: SUSPENDED` with resources present |
| GOV-11 | Resources in unexpected regions | 🟡 | Regions outside the declared operating footprint — shadow-IT signal |
| GOV-12 | Over-provisioned resources | 🟢 | Compute Optimizer / Cost Explorer rightsizing recommendations |
| GOV-13 | Snapshots older than one year | 🟢 | Accumulated storage cost |
| GOV-14 | ECR repositories without a lifecycle policy | 🟢 | Unbounded image storage growth |
| GOV-15 | No SCPs applied in an Organizations environment | 🟢 | Only `FullAWSAccess` attached |

---

## 9. Consuming Native Security Services

**Prefer AWS's own findings over re-deriving them.** Where these services are enabled, ingest and attribute them; where they are not enabled, that absence is itself a finding (LOG-05/LOG-06).

```powershell
aws guardduty list-detectors --region $R
aws guardduty list-findings --detector-id <id> --finding-criteria '{"Criterion":{"severity":{"Gte":4}}}' --region $R
aws guardduty get-findings --detector-id <id> --finding-ids <ids> --region $R

aws securityhub get-findings --filters '{"RecordState":[{"Value":"ACTIVE","Comparison":"EQUALS"}],"SeverityLabel":[{"Value":"CRITICAL","Comparison":"EQUALS"},{"Value":"HIGH","Comparison":"EQUALS"}]}' --region $R
aws securityhub get-enabled-standards --region $R

aws configservice describe-compliance-by-config-rule --region $R
aws configservice get-compliance-details-by-config-rule --config-rule-name <rule> --region $R

aws inspector2 list-findings --filter-criteria '{"severity":[{"comparison":"EQUALS","value":"CRITICAL"}]}' --region $R
aws inspector2 list-coverage --region $R

aws accessanalyzer list-analyzers --region $R
aws accessanalyzer list-findings --analyzer-arn <arn> --region $R
```

Always attribute the finding to its source (`Source: GuardDuty`, `Source: Security Hub / CIS 1.4`, `Source: assessment-derived`) so the reader knows what is AWS's judgment and what is this assessment's.

---

## 10. Finding Output Format

```json
{
  "findingId": "EXP-01",
  "title": "Publicly accessible RDS instance",
  "severity": "CRITICAL",
  "source": "assessment-derived",
  "description": "RDS instance is reachable from the internet.",
  "impact": "Direct database exposure bypasses application-layer authentication and rate limiting.",
  "affectedResources": [
    {
      "accountId": "111111111111",
      "region": "sa-east-1",
      "arn": "arn:aws:rds:sa-east-1:111111111111:db:legacy-orders",
      "detail": "PubliclyAccessible=true; sg-0abc allows 0.0.0.0/0 on 5432",
      "owner": "UNKNOWN",
      "tags": {}
    }
  ],
  "evidence": ["rds:DescribeDBInstances", "ec2:DescribeSecurityGroups"],
  "recommendation": "Set PubliclyAccessible=false, relocate to private subnets, and restrict the security group to the application security group.",
  "references": ["https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_VPC.WorkingWithRDSInstanceinaVPC.html"]
}
```

---

## 11. Reporting Discipline

- **No speculation.** Report what the API returned. If exploitability is unknown, say so.
- **No severity inflation.** A permissive egress rule is not the same as an open admin port.
- **Always include the ARN.** A finding without a resource identifier is not actionable.
- **Group by finding, list resources inside.** Do not produce one section per resource.
- **Note what was not checked** — coverage gaps materially change the meaning of "no findings".
- **Never include secret values, keys or tokens in a finding**, even as evidence. Reference the resource, not its content.
