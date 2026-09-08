---
name: aws-resource-inventory
description: The complete read-only AWS CLI command catalog for inventorying every service domain — compute, containers, serverless, databases, storage, networking, identity, security, data, observability, DevOps and IaC — plus the broad-discovery strategies and the normalized inventory schema. Use during Phase 1 and Phase 2.
---

# AWS Resource Inventory Skill

The command catalog for the sweep. **Every command here is read-only.** If a command you need is not in this catalog, verify it uses a `describe-*`, `list-*`, `get-*`, `lookup-*`, `search-*`, `select-*` or `batch-get-*` verb before running it.

## Conventions used in every command
- Add `--output json --no-cli-pager` for deterministic, parseable output
- Add `--region <region>` explicitly; never rely on the ambient default during a sweep
- **Paginate to exhaustion**: follow `NextToken` / `nextToken` / `Marker` / `PaginationToken` / `--starting-token`
- Write raw output to `reports/raw/<account-id>/<region>/<service>.json`

---

## Part 1 — Broad Discovery (run first)

### 1.1 Resource Groups Tagging API — universal, returns tags

```powershell
aws resourcegroupstaggingapi get-resources --region <region> --resources-per-page 100 --output json --no-cli-pager
aws resourcegroupstaggingapi get-tag-keys --region <region> --output json --no-cli-pager
aws resourcegroupstaggingapi get-tag-values --key <key> --region <region> --output json --no-cli-pager
```

Covers most taggable resource types. **Does not cover** untaggable resources or resources whose service does not integrate with the Tagging API — that is why Part 2 exists.

### 1.2 AWS Config aggregator — fastest when available

```powershell
aws configservice describe-configuration-aggregators --output json --no-cli-pager

aws configservice select-aggregate-resource-config `
  --configuration-aggregator-name <name> `
  --expression "SELECT accountId, awsRegion, resourceType, resourceId, resourceName, tags, resourceCreationTime" `
  --limit 100 --output json --no-cli-pager

aws configservice select-aggregate-resource-config `
  --configuration-aggregator-name <name> `
  --expression "SELECT resourceType, COUNT(*) GROUP BY resourceType" `
  --output json --no-cli-pager
```

Single-account variant:

```powershell
aws configservice select-resource-config --expression "SELECT resourceId, resourceType, tags WHERE resourceType = 'AWS::EC2::Instance'" --region <region> --output json --no-cli-pager
aws configservice list-discovered-resources --resource-type AWS::EC2::Instance --region <region> --output json --no-cli-pager
```

### 1.3 Resource Explorer

```powershell
aws resource-explorer-2 list-indexes --output json --no-cli-pager
aws resource-explorer-2 search --query-string "*" --max-results 1000 --region <aggregator-region> --output json --no-cli-pager
aws resource-explorer-2 search --query-string "service:ec2" --max-results 1000 --region <aggregator-region> --output json --no-cli-pager
```

### 1.4 Service quotas actually in use (optional signal)

```powershell
aws service-quotas list-service-quotas --service-code ec2 --region <region> --output json --no-cli-pager
aws support describe-trusted-advisor-checks --language en --region us-east-1 --output json --no-cli-pager
```

Trusted Advisor requires Business/Enterprise Support — treat failure as "not available", not a gap.

---

## Part 2 — Deep Inventory By Domain

### Domain 1 — Networking

```powershell
# VPC core
aws ec2 describe-vpcs --region $R
aws ec2 describe-subnets --region $R
aws ec2 describe-route-tables --region $R
aws ec2 describe-internet-gateways --region $R
aws ec2 describe-egress-only-internet-gateways --region $R
aws ec2 describe-nat-gateways --region $R
aws ec2 describe-vpc-endpoints --region $R
aws ec2 describe-vpc-endpoint-services --region $R
aws ec2 describe-vpc-peering-connections --region $R
aws ec2 describe-dhcp-options --region $R
aws ec2 describe-network-acls --region $R
aws ec2 describe-security-groups --region $R
aws ec2 describe-network-interfaces --region $R
aws ec2 describe-addresses --region $R
aws ec2 describe-flow-logs --region $R
aws ec2 describe-prefix-lists --region $R
aws ec2 describe-managed-prefix-lists --region $R
aws ec2 describe-availability-zones --region $R

# Hybrid / transit
aws ec2 describe-transit-gateways --region $R
aws ec2 describe-transit-gateway-attachments --region $R
aws ec2 describe-transit-gateway-route-tables --region $R
aws ec2 describe-vpn-connections --region $R
aws ec2 describe-vpn-gateways --region $R
aws ec2 describe-customer-gateways --region $R
aws directconnect describe-connections --region $R
aws directconnect describe-virtual-interfaces --region $R
aws directconnect describe-direct-connect-gateways --region $R

# Load balancing
aws elbv2 describe-load-balancers --region $R
aws elbv2 describe-target-groups --region $R
aws elbv2 describe-listeners --load-balancer-arn <arn> --region $R
aws elbv2 describe-rules --listener-arn <arn> --region $R
aws elbv2 describe-target-health --target-group-arn <arn> --region $R
aws elb describe-load-balancers --region $R            # Classic ELB

# DNS / edge (global)
aws route53 list-hosted-zones
aws route53 list-resource-record-sets --hosted-zone-id <id>
aws route53 list-health-checks
aws route53resolver list-resolver-endpoints --region $R
aws route53resolver list-resolver-rules --region $R
aws route53domains list-domains --region us-east-1
aws cloudfront list-distributions
aws cloudfront list-origin-access-controls
aws globalaccelerator list-accelerators --region us-west-2

# Edge security
aws wafv2 list-web-acls --scope REGIONAL --region $R
aws wafv2 list-web-acls --scope CLOUDFRONT --region us-east-1
aws wafv2 list-ip-sets --scope REGIONAL --region $R
aws network-firewall list-firewalls --region $R
aws shield describe-subscription --region us-east-1
aws shield list-protections --region us-east-1
```

**Key attributes to keep:** VPC CIDRs and `IsDefault`; subnet AZ + public/private classification (a default route to an IGW = public); every security-group rule with its source (CIDR **or referenced group ID** — these become graph edges); load balancer `Scheme` (`internet-facing` vs `internal`); target group targets; flow-log enablement.

---

### Domain 2 — Compute

```powershell
aws ec2 describe-instances --region $R
aws ec2 describe-instance-status --include-all-instances --region $R
aws ec2 describe-instance-types --region $R                 # only for types actually in use
aws ec2 describe-volumes --region $R
aws ec2 describe-snapshots --owner-ids self --region $R
aws ec2 describe-images --owners self --region $R
aws ec2 describe-key-pairs --region $R
aws ec2 describe-placement-groups --region $R
aws ec2 describe-reserved-instances --region $R
aws ec2 describe-spot-instance-requests --region $R
aws ec2 describe-hosts --region $R
aws ec2 describe-capacity-reservations --region $R
aws ec2 describe-launch-templates --region $R
aws ec2 describe-launch-template-versions --launch-template-id <id> --region $R

aws autoscaling describe-auto-scaling-groups --region $R
aws autoscaling describe-auto-scaling-instances --region $R
aws autoscaling describe-policies --region $R
aws autoscaling describe-scheduled-actions --region $R
aws autoscaling describe-lifecycle-hooks --auto-scaling-group-name <name> --region $R

aws elasticbeanstalk describe-applications --region $R
aws elasticbeanstalk describe-application-versions --region $R
aws elasticbeanstalk describe-environments --region $R
aws elasticbeanstalk describe-environment-resources --environment-name <name> --region $R
aws elasticbeanstalk describe-configuration-settings --application-name <app> --environment-name <env> --region $R
aws elasticbeanstalk describe-environment-health --environment-name <name> --attribute-names All --region $R
aws elasticbeanstalk list-available-solution-stacks --region $R

aws lightsail get-instances --region $R
aws lightsail get-databases --region $R
aws lightsail get-load-balancers --region $R

aws batch describe-compute-environments --region $R
aws batch describe-job-queues --region $R
aws batch describe-job-definitions --status ACTIVE --region $R

aws apprunner list-services --region $R
aws apprunner describe-service --service-arn <arn> --region $R

aws outposts list-outposts --region $R
aws ssm describe-instance-information --region $R          # SSM-managed inventory incl. on-prem
```

**EC2 projection helper**

```powershell
aws ec2 describe-instances --region $R --output json --no-cli-pager `
  --query "Reservations[].Instances[].{Id:InstanceId,Name:Tags[?Key=='Name']|[0].Value,Type:InstanceType,State:State.Name,AZ:Placement.AvailabilityZone,Vpc:VpcId,Subnet:SubnetId,PrivateIp:PrivateIpAddress,PublicIp:PublicIpAddress,Launched:LaunchTime,Platform:PlatformDetails,Arch:Architecture,Sgs:SecurityGroups[].GroupId,Profile:IamInstanceProfile.Arn,Tags:Tags}"
```

**Elastic Beanstalk note:** the `SolutionStackName` (e.g. `64bit Amazon Linux 2 v5.8.4 running Node.js 16`) is the single most important field — it identifies the platform version and whether it is retired. Cross-check against `list-available-solution-stacks`; a stack no longer listed is **retired** and must be flagged.

---

### Domain 3 — Containers

```powershell
# ECS
aws ecs list-clusters --region $R
aws ecs describe-clusters --clusters <arns> --include ATTACHMENTS SETTINGS STATISTICS TAGS --region $R
aws ecs list-services --cluster <cluster> --region $R
aws ecs describe-services --cluster <cluster> --services <arns> --include TAGS --region $R
aws ecs list-tasks --cluster <cluster> --region $R
aws ecs describe-tasks --cluster <cluster> --tasks <arns> --include TAGS --region $R
aws ecs list-task-definitions --status ACTIVE --region $R
aws ecs describe-task-definition --task-definition <family:rev> --include TAGS --region $R
aws ecs list-container-instances --cluster <cluster> --region $R
aws ecs describe-container-instances --cluster <cluster> --container-instances <arns> --region $R
aws ecs describe-capacity-providers --region $R
aws ecs list-task-definition-families --status ACTIVE --region $R

# EKS
aws eks list-clusters --region $R
aws eks describe-cluster --name <cluster> --region $R
aws eks list-nodegroups --cluster-name <cluster> --region $R
aws eks describe-nodegroup --cluster-name <cluster> --nodegroup-name <ng> --region $R
aws eks list-fargate-profiles --cluster-name <cluster> --region $R
aws eks describe-fargate-profile --cluster-name <cluster> --fargate-profile-name <fp> --region $R
aws eks list-addons --cluster-name <cluster> --region $R
aws eks describe-addon --cluster-name <cluster> --addon-name <addon> --region $R
aws eks list-access-entries --cluster-name <cluster> --region $R
aws eks list-identity-provider-configs --cluster-name <cluster> --region $R
aws eks describe-update --name <cluster> --update-id <id> --region $R

# ECR
aws ecr describe-repositories --region $R
aws ecr describe-images --repository-name <repo> --region $R
aws ecr get-lifecycle-policy --repository-name <repo> --region $R
aws ecr get-repository-policy --repository-name <repo> --region $R
aws ecr describe-image-scan-findings --repository-name <repo> --image-id imageTag=<tag> --region $R
aws ecr-public describe-repositories --region us-east-1
```

**Fargate detection:** an ECS service is Fargate when `launchType == "FARGATE"` **or** its `capacityProviderStrategy` references `FARGATE` / `FARGATE_SPOT`. Report Fargate and EC2 launch types separately — they migrate to different Azure targets.

**EKS version check:** compare `version` against the currently supported Kubernetes release window and flag anything in extended support or out of support.

**Container image provenance:** parse every `image` in the task definition / node group launch template. `<acct>.dkr.ecr.<region>.amazonaws.com/...` = ECR (internal); anything else = external registry, which becomes a supply-chain finding and a migration dependency.

---

### Domain 4 — Serverless

```powershell
aws lambda list-functions --region $R
aws lambda get-function-configuration --function-name <name> --region $R
aws lambda list-versions-by-function --function-name <name> --region $R
aws lambda list-aliases --function-name <name> --region $R
aws lambda list-layers --region $R
aws lambda list-event-source-mappings --region $R
aws lambda get-function-url-config --function-name <name> --region $R
aws lambda get-policy --function-name <name> --region $R
aws lambda get-function-concurrency --function-name <name> --region $R
aws lambda list-function-event-invoke-configs --function-name <name> --region $R

aws stepfunctions list-state-machines --region $R
aws stepfunctions describe-state-machine --state-machine-arn <arn> --region $R
aws stepfunctions list-activities --region $R

aws events list-event-buses --region $R
aws events list-rules --region $R
aws events list-targets-by-rule --rule <name> --region $R
aws events list-connections --region $R
aws events list-api-destinations --region $R
aws scheduler list-schedules --region $R

aws sqs list-queues --region $R
aws sqs get-queue-attributes --queue-url <url> --attribute-names All --region $R
aws sqs list-queue-tags --queue-url <url> --region $R

aws sns list-topics --region $R
aws sns get-topic-attributes --topic-arn <arn> --region $R
aws sns list-subscriptions-by-topic --topic-arn <arn> --region $R
aws sns list-tags-for-resource --resource-arn <arn> --region $R

aws apigateway get-rest-apis --region $R
aws apigateway get-stages --rest-api-id <id> --region $R
aws apigateway get-resources --rest-api-id <id> --region $R
aws apigateway get-authorizers --rest-api-id <id> --region $R
aws apigateway get-domain-names --region $R
aws apigateway get-usage-plans --region $R
aws apigatewayv2 get-apis --region $R
aws apigatewayv2 get-stages --api-id <id> --region $R
aws apigatewayv2 get-routes --api-id <id> --region $R
aws apigatewayv2 get-integrations --api-id <id> --region $R
aws apigatewayv2 get-authorizers --api-id <id> --region $R

aws appsync list-graphql-apis --region $R
aws appsync list-data-sources --api-id <id> --region $R
```

**⚠️ Environment variables:** `get-function-configuration` returns `Environment.Variables` **with values**. Record **keys only**. Never write values into any report or raw file — teams routinely put credentials there, and capturing them would turn the assessment output into a secret store.

**Deprecated Lambda runtimes** are a standing finding: any `python3.7`/`3.8`, `nodejs12.x`/`14.x`/`16.x`, `dotnetcore*`, `dotnet6` (check current status), `ruby2.7`, `go1.x`, `java8` (non-Corretto) and anything AWS has announced as deprecated. Always verify against the current AWS Lambda runtime deprecation page rather than a hard-coded list.

---

### Domain 5 — Databases

```powershell
# RDS + Aurora
aws rds describe-db-instances --region $R
aws rds describe-db-clusters --region $R
aws rds describe-global-clusters --region $R
aws rds describe-db-snapshots --snapshot-type manual --region $R
aws rds describe-db-cluster-snapshots --snapshot-type manual --region $R
aws rds describe-db-subnet-groups --region $R
aws rds describe-db-parameter-groups --region $R
aws rds describe-db-cluster-parameter-groups --region $R
aws rds describe-option-groups --region $R
aws rds describe-db-proxies --region $R
aws rds describe-event-subscriptions --region $R
aws rds describe-reserved-db-instances --region $R
aws rds describe-db-engine-versions --engine <engine> --region $R
aws rds describe-pending-maintenance-actions --region $R
aws rds list-tags-for-resource --resource-name <arn> --region $R

# DynamoDB
aws dynamodb list-tables --region $R
aws dynamodb describe-table --table-name <name> --region $R
aws dynamodb describe-continuous-backups --table-name <name> --region $R
aws dynamodb describe-time-to-live --table-name <name> --region $R
aws dynamodb list-tags-of-resource --resource-arn <arn> --region $R
aws dynamodb list-backups --region $R
aws dynamodb list-global-tables --region $R
aws dynamodb describe-limits --region $R

# In-memory
aws elasticache describe-cache-clusters --show-cache-node-info --region $R
aws elasticache describe-replication-groups --region $R
aws elasticache describe-serverless-caches --region $R
aws elasticache describe-cache-subnet-groups --region $R
aws elasticache describe-cache-parameter-groups --region $R
aws memorydb describe-clusters --region $R

# Purpose-built
aws docdb describe-db-clusters --region $R
aws docdb describe-db-instances --region $R
aws neptune describe-db-clusters --region $R
aws redshift describe-clusters --region $R
aws redshift-serverless list-workgroups --region $R
aws redshift-serverless list-namespaces --region $R
aws timestream-write list-databases --region $R
aws timestream-write list-tables --database-name <db> --region $R
aws keyspaces list-keyspaces --region $R
aws keyspaces list-tables --keyspace-name <ks> --region $R
aws qldb list-ledgers --region $R
```

**Aurora vs RDS:** `Engine` beginning with `aurora` (`aurora-mysql`, `aurora-postgresql`) is Aurora. Aurora resources appear in both `describe-db-clusters` (the cluster) and `describe-db-instances` (writer/reader instances) — report the cluster as the primary entity and the instances as its members, and do not double-count.

**DocumentDB and Neptune** also surface in `rds describe-db-clusters` with engines `docdb` and `neptune`. Classify by engine, and use their dedicated namespaces for the detail.

**Always capture:** `EngineVersion` (for EOL analysis), `PubliclyAccessible`, `StorageEncrypted` + `KmsKeyId`, `MultiAZ`, `BackupRetentionPeriod`, `DeletionProtection`, `Endpoint.Address`, `DBSubnetGroup.VpcId`, `VpcSecurityGroups`, `InstanceCreateTime`/`ClusterCreateTime`, `IAMDatabaseAuthenticationEnabled`, `ServerlessV2ScalingConfiguration`.

---

### Domain 6 — Storage

```powershell
# S3 (bucket list is global; everything else is per bucket)
aws s3api list-buckets
aws s3api get-bucket-location --bucket <b>
aws s3api get-bucket-encryption --bucket <b>
aws s3api get-bucket-versioning --bucket <b>
aws s3api get-public-access-block --bucket <b>
aws s3api get-bucket-policy-status --bucket <b>
aws s3api get-bucket-policy --bucket <b>
aws s3api get-bucket-acl --bucket <b>
aws s3api get-bucket-tagging --bucket <b>
aws s3api get-bucket-lifecycle-configuration --bucket <b>
aws s3api get-bucket-replication --bucket <b>
aws s3api get-bucket-logging --bucket <b>
aws s3api get-bucket-website --bucket <b>
aws s3api get-object-lock-configuration --bucket <b>
aws s3api get-bucket-notification-configuration --bucket <b>
aws s3control get-public-access-block --account-id <acct>

# File systems
aws efs describe-file-systems --region $R
aws efs describe-mount-targets --file-system-id <id> --region $R
aws efs describe-access-points --region $R
aws fsx describe-file-systems --region $R
aws fsx describe-volumes --region $R
aws storagegateway list-gateways --region $R
aws storagegateway list-file-shares --region $R

# Backup
aws backup list-backup-plans --region $R
aws backup list-backup-vaults --region $R
aws backup list-protected-resources --region $R
aws backup list-backup-jobs --region $R
```

Many `get-bucket-*` calls throw when the configuration is absent (`NoSuchBucketPolicy`, `ServerSideEncryptionConfigurationNotFoundError`, `NoSuchLifecycleConfiguration`, `ReplicationConfigurationNotFoundError`). **Treat these as "not configured", not as errors** — and note that "not configured" is often itself the finding.

**Bucket size and object count** come from CloudWatch, never from listing objects:

```powershell
aws cloudwatch get-metric-statistics --namespace AWS/S3 --metric-name BucketSizeBytes `
  --dimensions Name=BucketName,Value=<b> Name=StorageType,Value=StandardStorage `
  --start-time <T-2d> --end-time <now> --period 86400 --statistics Average --region <bucket-region>

aws cloudwatch get-metric-statistics --namespace AWS/S3 --metric-name NumberOfObjects `
  --dimensions Name=BucketName,Value=<b> Name=StorageType,Value=AllStorageTypes `
  --start-time <T-2d> --end-time <now> --period 86400 --statistics Average --region <bucket-region>
```

---

### Domain 7 — Identity & Security

```powershell
# IAM (global)
aws iam list-users
aws iam list-roles
aws iam list-groups
aws iam list-policies --scope Local
aws iam list-instance-profiles
aws iam get-account-summary
aws iam get-account-password-policy
aws iam list-account-aliases
aws iam list-saml-providers
aws iam list-open-id-connect-providers
aws iam list-attached-role-policies --role-name <role>
aws iam list-role-policies --role-name <role>
aws iam get-role --role-name <role>
aws iam list-access-keys --user-name <user>
aws iam get-access-key-last-used --access-key-id <id>
aws iam list-mfa-devices --user-name <user>
aws iam list-virtual-mfa-devices
aws iam get-account-authorization-details          # one call, full IAM graph
aws iam generate-credential-report
aws iam get-credential-report                       # metadata only, no secrets

# IAM Identity Center
aws sso-admin list-instances --region $R
aws sso-admin list-permission-sets --instance-arn <arn> --region $R
aws identitystore list-users --identity-store-id <id> --region $R

# Encryption & secrets metadata
aws kms list-keys --region $R
aws kms describe-key --key-id <id> --region $R
aws kms list-aliases --region $R
aws kms get-key-rotation-status --key-id <id> --region $R
aws kms list-grants --key-id <id> --region $R
aws kms get-key-policy --key-id <id> --policy-name default --region $R

aws secretsmanager list-secrets --region $R          # names/ARNs/rotation only
aws secretsmanager describe-secret --secret-id <arn> --region $R
aws ssm describe-parameters --region $R              # names/types only

aws acm list-certificates --region $R
aws acm describe-certificate --certificate-arn <arn> --region $R
aws acm-pca list-certificate-authorities --region $R

# User identity services
aws cognito-idp list-user-pools --max-results 60 --region $R
aws cognito-idp describe-user-pool --user-pool-id <id> --region $R
aws cognito-idp list-user-pool-clients --user-pool-id <id> --region $R
aws cognito-identity list-identity-pools --max-results 60 --region $R

# Security services
aws guardduty list-detectors --region $R
aws guardduty get-detector --detector-id <id> --region $R
aws guardduty list-findings --detector-id <id> --region $R
aws guardduty get-findings --detector-id <id> --finding-ids <ids> --region $R
aws securityhub describe-hub --region $R
aws securityhub get-enabled-standards --region $R
aws securityhub get-findings --region $R
aws configservice describe-configuration-recorders --region $R
aws configservice describe-config-rules --region $R
aws configservice describe-compliance-by-config-rule --region $R
aws inspector2 batch-get-account-status --region $R
aws inspector2 list-coverage --region $R
aws inspector2 list-findings --region $R
aws accessanalyzer list-analyzers --region $R
aws accessanalyzer list-findings --analyzer-arn <arn> --region $R
aws macie2 get-macie-session --region $R
aws detective list-graphs --region $R
aws ram list-resources --resource-owner SELF --region $R
aws ram list-resources --resource-owner OTHER-ACCOUNTS --region $R
```

### 🚫 Hard prohibitions in this domain

| Never run | Why |
|-----------|-----|
| `aws secretsmanager get-secret-value` | Returns the secret itself |
| `aws ssm get-parameter --with-decryption` | Returns decrypted `SecureString` values |
| `aws ssm get-parameters-by-path --with-decryption` | Same, in bulk |
| `aws kms decrypt` / `generate-data-key` | Produces plaintext key material |
| `aws iam create-*` / `update-*` / `attach-*` | Mutating |

`get-credential-report` returns **metadata only** (MFA status, key age, last-used dates) and is safe. Summarize it in the findings report — do not paste the raw CSV.

---

### Domain 8 — Data & Integration

```powershell
aws kinesis list-streams --region $R
aws kinesis describe-stream-summary --stream-name <n> --region $R
aws firehose list-delivery-streams --region $R
aws firehose describe-delivery-stream --delivery-stream-name <n> --region $R
aws kafka list-clusters-v2 --region $R
aws kafka describe-cluster-v2 --cluster-arn <arn> --region $R

aws glue get-databases --region $R
aws glue get-tables --database-name <db> --region $R
aws glue get-crawlers --region $R
aws glue get-jobs --region $R
aws glue get-connections --region $R
aws glue get-triggers --region $R

aws athena list-work-groups --region $R
aws athena list-data-catalogs --region $R
aws emr list-clusters --cluster-states RUNNING WAITING STARTING BOOTSTRAPPING --region $R
aws emr describe-cluster --cluster-id <id> --region $R
aws emr-serverless list-applications --region $R
aws datapipeline list-pipelines --region $R
aws quicksight list-dashboards --aws-account-id <acct> --region $R
aws quicksight list-data-sources --aws-account-id <acct> --region $R
aws lakeformation list-resources --region $R
```

---

### Domain 9 — Observability

```powershell
aws logs describe-log-groups --region $R
aws logs describe-subscription-filters --log-group-name <n> --region $R
aws logs describe-metric-filters --region $R
aws logs describe-export-tasks --region $R

aws cloudwatch describe-alarms --region $R
aws cloudwatch describe-alarms-for-metric --namespace <ns> --metric-name <m> --region $R
aws cloudwatch list-dashboards --region $R
aws cloudwatch list-metrics --region $R
aws cloudwatch describe-anomaly-detectors --region $R
aws synthetics describe-canaries --region $R
aws application-insights list-applications --region $R

aws xray get-sampling-rules --region $R
aws xray get-service-graph --start-time <t> --end-time <t> --region $R

aws cloudtrail describe-trails --region $R
aws cloudtrail get-trail-status --name <trail> --region $R
aws cloudtrail list-trails --region $R
aws cloudtrail get-event-selectors --trail-name <trail> --region $R
aws cloudtrail list-channels --region $R
```

**Log groups are a cost hotspot.** Capture `retentionInDays` (`null` = never expires) and `storedBytes`. Never-expiring log groups with large `storedBytes` are almost always the cheapest savings in the whole assessment.

---

### Domain 10 — DevOps & IaC

```powershell
aws cloudformation describe-stacks --region $R
aws cloudformation list-stacks --stack-status-filter CREATE_COMPLETE UPDATE_COMPLETE UPDATE_ROLLBACK_COMPLETE --region $R
aws cloudformation list-stack-resources --stack-name <n> --region $R
aws cloudformation describe-stack-events --stack-name <n> --region $R
aws cloudformation list-stack-sets --region $R
aws cloudformation describe-stack-drift-detection-status --stack-drift-detection-id <id> --region $R
aws cloudformation get-template --stack-name <n> --region $R
aws cloudformation list-exports --region $R

aws codecommit list-repositories --region $R
aws codebuild list-projects --region $R
aws codebuild batch-get-projects --names <names> --region $R
aws codepipeline list-pipelines --region $R
aws codepipeline get-pipeline --name <n> --region $R
aws codedeploy list-applications --region $R
aws codedeploy list-deployment-groups --application-name <app> --region $R
aws codeartifact list-domains --region $R
aws codeartifact list-repositories --region $R
aws codestar-connections list-connections --region $R
aws servicecatalog list-portfolios --region $R
aws ssm describe-patch-baselines --region $R
aws ssm list-documents --filters Key=Owner,Values=Self --region $R
```

⚠️ `describe-stack-drift-detection-status` only **reads** an existing detection result. Do **not** call `detect-stack-drift` — it is a mutating-class operation that starts a job.

**IaC coverage metric:** union all `list-stack-resources` physical resource IDs, then diff against the full inventory. Everything not in that union was created outside CloudFormation. Cross-check for Terraform by looking for an S3 state bucket, a DynamoDB lock table (`terraform-*`, `*-tfstate-lock`), or `ManagedBy: Terraform` tags.

---

### Domain 11 — Other Services

```powershell
aws ses list-identities --region $R
aws sesv2 list-email-identities --region $R
aws sesv2 get-account --region $R
aws sesv2 list-configuration-sets --region $R
aws amplify list-apps --region $R
aws mq list-brokers --region $R
aws transfer list-servers --region $R
aws workspaces describe-workspaces --region $R
aws workspaces describe-workspace-directories --region $R
aws sagemaker list-notebook-instances --region $R
aws sagemaker list-endpoints --region $R
aws sagemaker list-domains --region $R
aws sagemaker list-training-jobs --region $R
aws bedrock list-custom-models --region $R
aws bedrock list-provisioned-model-throughputs --region $R
aws connect list-instances --region $R
aws iot list-things --region $R
aws greengrassv2 list-core-devices --region $R
aws devicefarm list-projects --region us-west-2
aws pinpoint get-apps --region $R
aws mediaconvert list-queues --region $R
aws elastictranscoder list-pipelines --region $R
aws opensearch list-domain-names --region $R
aws opensearch describe-domain --domain-name <n> --region $R
aws es list-domain-names --region $R
```

Not every account uses these. Run them opportunistically and record "service not in use" rather than treating an empty result as a gap.

---

## Part 3 — Normalized Inventory Schema

Every resource, regardless of service, becomes one record:

```json
{
  "arn": "string (canonical identity)",
  "accountId": "string",
  "accountAlias": "string|null",
  "region": "string|'global'",
  "service": "string (ec2, rds, ecs, ...)",
  "resourceType": "string (AWS::EC2::Instance)",
  "resourceId": "string",
  "resourceName": "string|null",
  "state": "string|null",
  "createdOn": "ISO-8601|null",
  "createdBy": "string|null",
  "createdVia": "console|cli|terraform|cloudformation|sdk|service|null",
  "attributionConfidence": "HIGH|MEDIUM|LOW|UNKNOWN",
  "owner": "string|null",
  "tags": { "key": "value" },
  "attributes": { "service-specific fields" },
  "relationships": {
    "vpcId": "string|null",
    "subnetIds": [],
    "securityGroupIds": [],
    "iamRoleArns": [],
    "kmsKeyIds": [],
    "targetGroupArns": [],
    "imageUris": []
  },
  "managedBy": "CloudFormation:<stack>|Terraform|manual|null",
  "estimatedMonthlyCost": 0.0,
  "publiclyAccessible": true,
  "encrypted": true,
  "sourceOperation": "rds:DescribeDBInstances",
  "scanTimestamp": "ISO-8601"
}
```

### Rules
- `arn` is the join key everywhere. When a service does not return an ARN, construct the canonical form: `arn:<partition>:<service>:<region>:<account>:<type>/<id>`.
- `region` is `"global"` for IAM, Route 53, CloudFront and Organizations.
- Missing data is `null`, never an empty string and never a guess.
- `attributes` keeps the service-specific detail; the top level stays uniform so the CSV export and cross-service analysis work.
- **Never** place environment-variable values, secret values or connection strings in `attributes`.

---

## Part 4 — Sweep Checklist Per Region

```
[ ] Networking     [ ] Compute        [ ] Containers   [ ] Serverless
[ ] Databases      [ ] Storage        [ ] Identity     [ ] Data/Integration
[ ] Observability  [ ] DevOps/IaC     [ ] Other
[ ] Pagination exhausted for every call
[ ] Errors classified (gap vs not-in-use vs not-available)
[ ] Raw JSON written to reports/raw/<account>/<region>/
[ ] Region marked complete in Report-Status.md
```
