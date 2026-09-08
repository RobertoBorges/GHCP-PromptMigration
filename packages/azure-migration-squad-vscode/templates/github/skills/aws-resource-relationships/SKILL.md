---
name: aws-resource-relationships
description: Edge-inference catalog for building the AWS dependency graph — how to derive relationships from ENIs, security groups, target groups, IAM trust policies, event sources, container images, environment variables and flow logs, plus internet-exposure path tracing and cross-account edge detection. Use during Phase 4.
---

# AWS Resource Relationships Skill

Turns a flat inventory into a graph. Every edge carries `source`, `target`, `edgeType`, `evidence` and `confidence`.

## Confidence model

| Level | Meaning | Rendering in Mermaid |
|-------|---------|----------------------|
| `HIGH` | Explicit identifier in the API response (ARN, resource ID, attachment) | Solid line `-->` |
| `MEDIUM` | Strong circumstantial evidence (matching endpoint, port-specific SG rule, shared tag) | Dotted line `-.->` with label |
| `LOW` | Naming convention only | Dotted line, listed in the table but usually omitted from diagrams |

**Never render a `LOW` edge as if it were fact.** State the evidence in the edge table.

---

## 1. Network Containment Edges (HIGH)

| Edge | Derived from |
|------|--------------|
| `resource → VPC` | `VpcId` on the resource, or `DBSubnetGroup.VpcId` (RDS), `resourcesVpcConfig.vpcId` (EKS), `awsvpcConfiguration.subnets` → subnet → VPC (ECS Fargate), `VpcConfig.VpcId` (Lambda) |
| `resource → subnet` | `SubnetId`, `Subnets[]`, `SubnetIds[]` |
| `subnet → AZ` | `AvailabilityZone` |
| `subnet → route table` | `ec2 describe-route-tables` → `Associations[].SubnetId`; the VPC's `Main` route table applies to unassociated subnets |
| `route table → IGW/NAT/TGW/peering/endpoint` | `Routes[].GatewayId` / `NatGatewayId` / `TransitGatewayId` / `VpcPeeringConnectionId` / `VpcEndpointId` |

**Public subnet classification:** a subnet is public when its effective route table has a `0.0.0.0/0` route to an `igw-*`. Everything else is private. This single derivation drives most of the exposure analysis.

---

## 2. Security Group Edges (HIGH — the backbone)

```powershell
aws ec2 describe-security-groups --region $R --output json --no-cli-pager
```

For each `IpPermissions` / `IpPermissionsEgress` entry:

| Rule source | Edge produced |
|-------------|---------------|
| `UserIdGroupPairs[].GroupId` | `sg-source → sg-target` labeled with protocol/port — **the strongest application-tier evidence available** |
| `UserIdGroupPairs[].UserId` different from the account | **Cross-account** security group reference — flag it |
| `IpRanges[].CidrIp == 0.0.0.0/0` | Internet exposure edge |
| `IpRanges[].CidrIp` matching another VPC's CIDR | Probable peering/TGW traffic path |
| `PrefixListIds[]` | Edge to an AWS service prefix list (S3/DynamoDB gateway endpoints) |

Then project SG-to-SG edges onto the resources attached to those groups (via `describe-network-interfaces` → `Groups[]` → `Attachment`), producing resource-to-resource edges.

**Port heuristics for labeling** (MEDIUM confidence when combined with an SG-to-SG rule):

| Port | Likely target |
|------|---------------|
| 3306 | MySQL / Aurora MySQL / MariaDB |
| 5432 | PostgreSQL / Aurora PostgreSQL |
| 1433 | SQL Server |
| 1521 | Oracle |
| 27017 | DocumentDB / MongoDB |
| 6379 | Redis / ElastiCache / MemoryDB |
| 11211 | Memcached |
| 9092 | Kafka / MSK |
| 5439 | Redshift |
| 8182 | Neptune |
| 443 / 80 | HTTP(S) service |

---

## 3. ENI Edges (HIGH — the universal resolver)

`aws ec2 describe-network-interfaces` is the most under-used inventory call. Every ENI has:
- `Attachment.InstanceId` → EC2 instance
- `InterfaceType` → `interface`, `nat_gateway`, `vpc_endpoint`, `lambda`, `network_load_balancer`, `gateway_load_balancer_endpoint`, `transit_gateway`, `efa`, `branch`
- `Description` → often names the owning resource explicitly:
  - `ELB app/<lb-name>/<id>` → ALB
  - `ELB net/<lb-name>/<id>` → NLB
  - `AWS Lambda VPC ENI-<function>-<id>` → Lambda in a VPC
  - `RDSNetworkInterface` → RDS
  - `EFS mount target <fsmt-id>` → EFS
  - `VPC Endpoint Interface <vpce-id>` → interface endpoint
  - `arn:aws:ecs:<region>:<acct>:attachment/<id>` → ECS Fargate task
- `RequesterId` / `RequesterManaged` → the AWS service that owns it

ENIs resolve "what is actually in this subnet" for services that never appear in a subnet listing.

---

## 4. Load Balancing Edges (HIGH)

```
ALB/NLB → Listener → (Rule) → TargetGroup → Targets
```

```powershell
aws elbv2 describe-load-balancers --region $R
aws elbv2 describe-listeners --load-balancer-arn <arn> --region $R
aws elbv2 describe-rules --listener-arn <arn> --region $R
aws elbv2 describe-target-groups --load-balancer-arn <arn> --region $R
aws elbv2 describe-target-health --target-group-arn <arn> --region $R
```

Target types: `instance` (EC2 instance ID), `ip` (Fargate task ENI IP or on-prem IP), `lambda` (function ARN), `alb` (NLB fronting an ALB).

Also derive:
- `ASG → target group` from `autoscaling describe-auto-scaling-groups` → `TargetGroupARNs`
- `ECS service → target group` from `describe-services` → `loadBalancers[].targetGroupArn`
- `EKS Ingress → ALB` via the AWS Load Balancer Controller (LB has `elbv2.k8s.aws/cluster` tag)

Target groups with **zero healthy targets** and load balancers with **zero targets** are orphan findings.

---

## 5. Container Edges (HIGH)

| Edge | Source |
|------|--------|
| `ECS service → task definition` | `describe-services` → `taskDefinition` |
| `task definition → container image` | `containerDefinitions[].image` |
| `container image → ECR repository` | Image URI matching `<acct>.dkr.ecr.<region>.amazonaws.com/<repo>:<tag>` |
| `task definition → IAM roles` | `taskRoleArn`, `executionRoleArn` |
| `task definition → log group` | `logConfiguration.options["awslogs-group"]` |
| `task definition → secrets` | `secrets[].valueFrom` → Secrets Manager ARN or SSM parameter ARN |
| `ECS service → subnets/SGs` | `networkConfiguration.awsvpcConfiguration` |
| `ECS service → service discovery` | `serviceRegistries[].registryArn` → Cloud Map |
| `ECS cluster → capacity provider` | `capacityProviders[]` → ASG for EC2 launch type |
| `EKS cluster → node group → launch template → AMI` | `describe-nodegroup` → `launchTemplate` / `amiType` |
| `EKS cluster → OIDC provider → IAM role (IRSA)` | `describe-cluster` → `identity.oidc.issuer`, then IAM roles whose trust policy names that issuer |
| `EKS Fargate profile → subnets + namespace selectors` | `describe-fargate-profile` |

**IRSA is a high-value edge**: it links Kubernetes service accounts to IAM roles and therefore to the AWS resources those roles can reach. Search IAM role trust policies for `oidc-provider/oidc.eks.<region>.amazonaws.com/id/<cluster-id>`.

---

## 6. Event-Driven Edges (HIGH)

| Edge | Source |
|------|--------|
| `SQS/Kinesis/DynamoDB Stream/MSK → Lambda` | `lambda list-event-source-mappings` → `EventSourceArn` + `FunctionArn` |
| `S3 → Lambda/SQS/SNS` | `s3api get-bucket-notification-configuration` |
| `EventBridge rule → target` | `events list-targets-by-rule` → `Targets[].Arn` |
| `SNS topic → subscriber` | `sns list-subscriptions-by-topic` → `Endpoint` (SQS ARN, Lambda ARN, HTTPS URL, email) |
| `SQS → DLQ` | `get-queue-attributes` → `RedrivePolicy.deadLetterTargetArn` |
| `Lambda → DLQ` | `DeadLetterConfig.TargetArn` |
| `Step Functions state → resource` | State machine `definition` JSON → `Resource` fields (Lambda ARNs, `arn:aws:states:::<service>:<action>` integrations) |
| `API Gateway → integration` | `apigateway get-integration` / `apigatewayv2 get-integrations` → `uri` (Lambda ARN, HTTP endpoint, VPC Link) |
| `AppSync → data source` | `appsync list-data-sources` → `dynamodbConfig` / `lambdaConfig` / `relationalDatabaseConfig` |
| `CloudWatch alarm → SNS` | `describe-alarms` → `AlarmActions[]` |
| `Log group → subscription target` | `logs describe-subscription-filters` → `destinationArn` (Firehose, Lambda, cross-account) |

---

## 7. IAM Edges (HIGH — and the cross-account detector)

| Edge | Source |
|------|--------|
| `principal → role` | Role `AssumeRolePolicyDocument.Statement[].Principal` |
| `role → managed policies` | `list-attached-role-policies` |
| `role → services it can reach` | Policy document `Resource` ARNs (parse for concrete ARNs; note wildcards as a finding) |
| `EC2 instance → role` | `IamInstanceProfile` → instance profile → role |
| `Lambda → role` | `get-function-configuration` → `Role` |
| `ECS task → role` | `taskRoleArn` / `executionRoleArn` |
| `EKS service account → role` | OIDC trust condition (IRSA) |
| `CodeBuild/CodePipeline → role` | `serviceRole` / `roleArn` |

Run `aws iam get-account-authorization-details` once — it returns users, groups, roles, policies and their attachments in a single response, which is far cheaper than iterating.

**Cross-account trust detection:** any role trust policy whose `Principal.AWS` names an account ID other than the current one is a cross-account edge. Classify:

| Principal account | Classification |
|-------------------|----------------|
| In the organization's account list | Internal cross-account — normal, document it |
| Not in the organization | **EXTERNAL** — raise a finding, capture whether `sts:ExternalId` is enforced |
| A known AWS service account ID | Third-party integration (Datadog, Snyk, CloudHealth, etc.) — identify and document |
| `"AWS": "*"` | 🔴 Critical — publicly assumable role |

---

## 8. Encryption & Secrets Edges (HIGH)

| Edge | Source |
|------|--------|
| `resource → KMS key` | `KmsKeyId` / `KMSKeyArn` / `encryptionConfig` on EBS, RDS, S3, DynamoDB, EFS, SQS, SNS, Secrets Manager, ECR, EKS |
| `KMS key → external account` | Key policy statements and `kms list-grants` naming other accounts |
| `resource → secret` | ECS `secrets[].valueFrom`, Lambda env var **name** referencing a secret ARN, RDS `MasterUserSecret.SecretArn` |
| `secret → rotation Lambda` | `secretsmanager describe-secret` → `RotationLambdaARN` |

A KMS key used by resources in another account is a cross-account data dependency and must appear in the topology map.

---

## 9. Storage & Data Edges (HIGH)

| Edge | Source |
|------|--------|
| `S3 → replica bucket` | `get-bucket-replication` → `Rules[].Destination.Bucket` (often cross-account/region) |
| `S3 → CloudFront` | CloudFront `Origins[].DomainName` matching a bucket regional domain, plus OAC/OAI |
| `S3 → log destination` | `get-bucket-logging` → `TargetBucket` |
| `EFS → mount target → subnet` | `efs describe-mount-targets` |
| `RDS → read replica` | `describe-db-instances` → `ReadReplicaDBInstanceIdentifiers` / `ReadReplicaSourceDBInstanceIdentifier` (cross-region replicas produce cross-region edges) |
| `Aurora global cluster → regional clusters` | `describe-global-clusters` → `GlobalClusterMembers[]` |
| `DynamoDB global table → replicas` | `describe-table` → `Replicas[]` |
| `Backup plan → protected resources` | `backup list-protected-resources` |
| `Firehose → destination` | `describe-delivery-stream` → S3/Redshift/OpenSearch/HTTP destination |
| `Glue job → connections → data stores` | `get-jobs` + `get-connections` |

---

## 10. DNS & Edge Edges (HIGH)

| Edge | Source |
|------|--------|
| `Route 53 record → target` | `list-resource-record-sets` → alias target (ALB DNS, CloudFront domain, S3 website endpoint) or A/CNAME value |
| `CloudFront → origin` | `list-distributions` → `Origins[].DomainName` |
| `ACM certificate → resource` | `describe-certificate` → `InUseBy[]` |
| `WAF Web ACL → resource` | `wafv2 list-resources-for-web-acl --web-acl-arn <arn>` |

**Dangling DNS detection:** a Route 53 record whose target does not exist in the inventory (deleted ALB, released EIP, deleted S3 bucket) is a subdomain-takeover risk — raise it as a High finding.

---

## 11. Configuration-Derived Edges (MEDIUM)

Use **names only** — never read environment-variable values.

| Pattern | Inference |
|---------|-----------|
| Env var name matching `*_DB_HOST`, `*_DATABASE_URL`, `DB_ENDPOINT` | The workload connects to a database; correlate with an RDS endpoint reachable from its SG |
| Env var name matching `*_QUEUE_URL`, `SQS_*` | Connects to SQS |
| Env var name matching `*_BUCKET`, `S3_*` | Connects to S3 |
| Env var name matching `*_TABLE`, `DYNAMO*` | Connects to DynamoDB |
| Env var name matching `REDIS_*`, `CACHE_*` | Connects to ElastiCache/MemoryDB |
| Parameter Store path prefix `/app/orders/*` | Groups resources under the `orders` application |

When the SG graph independently supports the same edge, promote it to `MEDIUM-HIGH` and say so in the evidence field.

---

## 12. Flow-Log Edges (HIGH, when available)

If VPC Flow Logs are enabled and land in CloudWatch Logs or S3, actual traffic can be observed:

```powershell
aws ec2 describe-flow-logs --region $R --output json --no-cli-pager

aws logs start-query `
  --log-group-name <flow-log-group> `
  --start-time <epoch> --end-time <epoch> `
  --query-string "fields srcAddr, dstAddr, dstPort, protocol | filter action = 'ACCEPT' | stats sum(bytes) as total by srcAddr, dstAddr, dstPort | sort total desc | limit 200" `
  --region $R --output json --no-cli-pager

aws logs get-query-results --query-id <id> --region $R --output json --no-cli-pager
```

⚠️ `start-query` creates a query job and is billed by data scanned. Ask the user for consent, scope the time window tightly (1–24h), and state the cost implication. This is the only way to prove which of the *possible* SG edges are *actual* traffic — extremely valuable for migration wave planning.

Resolve the IPs back to resources via `describe-network-interfaces` → `PrivateIpAddress`.

---

## 13. Internet Exposure Path Tracing

Produce one row per path:

| # | Entry point | Path | Terminal resource | Auth | Severity |
|---|-------------|------|-------------------|------|----------|
| 1 | `0.0.0.0/0:443` | Route 53 → CloudFront → ALB(internet-facing) → TG → ECS Fargate | `orders-api` | Cognito | 🟢 |
| 2 | `0.0.0.0/0:5432` | SG `sg-legacy` → RDS `legacy-orders` (`PubliclyAccessible=true`) | `legacy-orders` | password | 🔴 |

Detection rules:
1. EC2 with a public IP **and** a public subnet **and** an SG allowing `0.0.0.0/0`
2. `elbv2` / `elb` with `Scheme: internet-facing`
3. RDS/DocumentDB/Neptune/Redshift with `PubliclyAccessible: true`
4. S3 with `get-public-access-block` disabled or `get-bucket-policy-status.IsPublic: true`
5. API Gateway with no authorizer, or a Lambda function URL with `AuthType: NONE`
6. EKS with `endpointPublicAccess: true` and `publicAccessCidrs` containing `0.0.0.0/0`
7. ElastiCache/MemoryDB/OpenSearch reachable from a public subnet
8. Any Elastic IP association
9. Global Accelerator endpoints
10. ECR public repositories, and ECR repository policies granting `*`

---

## 14. Cross-Account & Cross-Region Edge Checklist

```
[ ] VPC peering where accepter/requester accounts differ
[ ] Transit Gateway attachments owned by other accounts (and RAM shares)
[ ] IAM role trust policies naming external accounts
[ ] S3 bucket policies granting external principals
[ ] KMS key policies and grants naming external accounts
[ ] ECR repository policies granting cross-account pull
[ ] SNS/SQS resource policies granting external accounts
[ ] Route 53 private hosted zones associated with VPCs in other accounts
[ ] RDS cross-region read replicas and Aurora global clusters
[ ] DynamoDB global table replicas
[ ] S3 cross-region replication rules
[ ] CloudWatch Logs cross-account subscription destinations
[ ] AWS RAM shares (both directions)
[ ] CloudFormation StackSets targeting other accounts
[ ] Lambda resource policies granting external invoke
```

---

## 15. Application Grouping Precedence

1. `Application` / `Project` / `Service` / `app` tag value
2. CloudFormation stack membership
3. Connected component in the `HIGH`-confidence edge subgraph
4. Naming prefix (`orders-*`) — `LOW` confidence, mark as inferred
5. Otherwise → `Unclassified`

Report the `Unclassified` count and cost; a large `Unclassified` bucket is a governance finding in its own right.

---

## 16. Orphan Detection

Resources with **zero inbound and zero outbound HIGH-confidence edges** are decommissioning candidates. Cross-check with:

| Resource | Orphan signal |
|----------|---------------|
| EBS volume | `State: available` (unattached) |
| Elastic IP | No `AssociationId` |
| Security group | Not referenced by any ENI or other SG |
| Target group | No registered targets |
| Load balancer | No listeners or no healthy targets |
| ASG | `DesiredCapacity: 0` and no scheduled actions |
| NAT Gateway | No private subnet routes pointing at it |
| Snapshot / AMI | Older than 1 year and not referenced by a launch template |
| ECR repository | No images, or last push older than 1 year |
| Lambda | No triggers and no invocations in the CloudWatch `Invocations` metric |
| CloudWatch log group | `storedBytes: 0` or no ingestion in the last 90 days |
| RDS snapshot | Manual snapshot older than the retention policy |
| Cognito user pool | Zero users |

---

## 17. Edge Output Format

`reports/raw/<account-id>/_edges.json`:

```json
[
  {
    "source": "arn:aws:elasticloadbalancing:sa-east-1:111111111111:loadbalancer/app/orders-alb/abc",
    "target": "arn:aws:ecs:sa-east-1:111111111111:service/prod/orders-api",
    "edgeType": "load-balances",
    "evidence": "listener 443 -> target group tg-orders -> ECS service registered target",
    "confidence": "HIGH",
    "crossAccount": false,
    "crossRegion": false,
    "application": "orders"
  }
]
```
