# AWS Resource Inventory

> **Generated:** `<YYYY-MM-DD HH:mm UTC>`
> **Accounts:** `<list>` · **Regions:** `<n>` · **Total resources:** `<n>`
> Flat export: [inventory.csv](inventory.csv)

Organized **Account → Region → Service**. Repeat the structure below per account.

---

# Account `<account-id>` — `<alias>`

## Summary

| Service | Count | Regions | Est. monthly cost | Untagged | Unknown owner |
|---------|-------|---------|-------------------|----------|---------------|
| | | | | | |
| **Total** | | | | | |

---

## Region `<region>`

### Compute — EC2

| Name | Instance ID | Type | State | AZ | VPC / Subnet | Private IP | Public IP | Launched | Created By | Via | Owner | Tags |
|------|-------------|------|-------|-----|--------------|-----------|-----------|----------|-----------|-----|-------|------|
| | | | | | | | | | | | | |

### Compute — EBS Volumes

| Volume ID | Size | Type | State | Attached To | Encrypted | KMS Key | Created | Owner | Tags |
|-----------|------|------|-------|-------------|-----------|---------|---------|-------|------|
| | | | | | | | | | |

### Compute — Auto Scaling Groups

| Name | Min/Desired/Max | Launch Template | Instance Types | Subnets / AZs | Target Groups | Created | Owner | Tags |
|------|-----------------|-----------------|----------------|---------------|---------------|---------|-------|------|
| | | | | | | | | |

### Compute — Elastic Beanstalk

| Application | Environment | Solution Stack | Retired? | Tier | Health | Instances | LB Type | Created | Created By | Owner | Tags |
|-------------|-------------|----------------|----------|------|--------|-----------|---------|---------|-----------|-------|------|
| | | | | | | | | | | | |

### Containers — ECS

| Cluster | Service | Launch Type | Desired/Running | Task Definition | CPU/Mem | Image | Subnets | Target Group | Created | Owner | Tags |
|---------|---------|-------------|-----------------|-----------------|---------|-------|---------|--------------|---------|-------|------|
| | | | | | | | | | | | |

### Containers — EKS

| Cluster | K8s Version | Supported? | Endpoint Access | Node Groups | Instance Types | Fargate Profiles | Add-ons | Created | Owner | Tags |
|---------|-------------|-----------|-----------------|-------------|----------------|------------------|---------|---------|-------|------|
| | | | | | | | | | | |

### Containers — ECR

| Repository | URI | Images | Latest Push | Scan on Push | Immutable | Encryption | Lifecycle | Critical CVEs | Created | Owner |
|-----------|-----|--------|-------------|--------------|-----------|------------|-----------|---------------|---------|-------|
| | | | | | | | | | | |

### Serverless — Lambda

| Function | Runtime | Deprecated? | Memory | Timeout | Package | VPC | Triggers | Last Modified | Created By | Owner | Tags |
|----------|---------|-------------|--------|---------|---------|-----|----------|---------------|-----------|-------|------|
| | | | | | | | | | | | |

### Serverless — Messaging

| Type | Name | Encryption | FIFO | DLQ | Subscribers / Sources | Created | Owner | Tags |
|------|------|------------|------|-----|----------------------|---------|-------|------|
| SQS | | | | | | | | |
| SNS | | | — | — | | | | |
| EventBridge | | — | — | — | | | | |

### Serverless — API

| Type | API | Stage | Endpoint | Authorizer | Integration Target | Created | Owner | Tags |
|------|-----|-------|----------|-----------|--------------------|---------|-------|------|
| | | | | | | | | |

### Databases — RDS / Aurora

| Identifier | Engine | Version | EOL? | Class | Multi-AZ | Public | Encrypted | Backup (days) | Del. Protection | Endpoint | Created | Created By | Owner | Tags |
|-----------|--------|---------|------|-------|----------|--------|-----------|---------------|-----------------|----------|---------|-----------|-------|------|
| | | | | | | | | | | | | | | |

### Databases — DynamoDB

| Table | Items | Size | Billing Mode | RCU/WCU | GSIs | Streams | PITR | Encryption | Created | Owner | Tags |
|-------|-------|------|--------------|---------|------|---------|------|------------|---------|-------|------|
| | | | | | | | | | | | |

### Databases — Cache & Other

| Type | Identifier | Engine | Version | Nodes | Multi-AZ | Encrypted | Endpoint | Created | Owner | Tags |
|------|-----------|--------|---------|-------|----------|-----------|----------|---------|-------|------|
| | | | | | | | | | | |

### Storage — S3

| Bucket | Region | Size | Objects | Encryption | Versioning | Public Access | Lifecycle | Replication | Logging | Created | Owner | Tags |
|--------|--------|------|---------|------------|------------|---------------|-----------|-------------|---------|---------|-------|------|
| | | | | | | | | | | | | |

### Storage — File Systems

| Type | ID | Size | Performance | Encrypted | Mount Targets / Subnets | Backup | Created | Owner | Tags |
|------|----|------|-------------|-----------|-------------------------|--------|---------|-------|------|
| | | | | | | | | | |

### Networking — VPCs & Subnets

| VPC | CIDR | Default? | Subnets | AZs | IGW | NAT | Endpoints | Flow Logs | Created | Owner | Tags |
|-----|------|----------|---------|-----|-----|-----|-----------|-----------|---------|-------|------|
| | | | | | | | | | | | |

| Subnet | VPC | CIDR | AZ | Public? | Auto-assign Public IP | Available IPs | Resources | Tags |
|--------|-----|------|-----|---------|----------------------|---------------|-----------|------|
| | | | | | | | | |

### Networking — Load Balancers

| Name | Type | Scheme | DNS | Listeners | Target Groups | Healthy Targets | WAF | Created | Owner | Tags |
|------|------|--------|-----|-----------|---------------|-----------------|-----|---------|-------|------|
| | | | | | | | | | | |

### Networking — Security Groups

| Group ID | Name | VPC | Ingress Rules | `0.0.0.0/0`? | Attached To | Created By | Owner | Tags |
|----------|------|-----|---------------|--------------|-------------|-----------|-------|------|
| | | | | | | | | |

### Identity — IAM

| Type | Name | Created | Last Used | Attached Policies | MFA | Key Age | Cross-Account Trust | Notes |
|------|------|---------|-----------|-------------------|-----|---------|---------------------|-------|
| User | | | | | | | — | |
| Role | | | | | — | — | | |

### Security — Keys, Secrets & Certificates

| Type | Name / ARN | Rotation | Used By | Expiry | Created | Owner | Tags |
|------|-----------|----------|---------|--------|---------|-------|------|
| KMS key | | | | — | | | |
| Secret | | | | — | | | |
| ACM cert | | — | | | | | |

> Secret **values are never collected**. Only names, ARNs and rotation metadata appear here.

### Observability

| Type | Name | Retention | Stored Size | Subscriptions / Actions | Created | Owner | Tags |
|------|------|-----------|-------------|------------------------|---------|-------|------|
| Log group | | | | | | | |
| Alarm | | — | — | | | | |

### IaC — CloudFormation

| Stack | Status | Resources | Drift | Created | Created By | Owner | Tags |
|-------|--------|-----------|-------|---------|-----------|-------|------|
| | | | | | | | |

### Resources NOT Managed By IaC

| Resource | Type | Region | Created | Created By | Via | Owner | Est. Cost |
|----------|------|--------|---------|-----------|-----|-------|-----------|
| | | | | | | | |

---

## Region `<region>` — No Resources

No resources found. Region was scanned successfully.

---

## Coverage Gaps For This Account

| Region | Service | Operation | Reason |
|--------|---------|-----------|--------|
| | | | |
