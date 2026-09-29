# IAM Migration Checklist

> **Application:** `<application-name>`
> **Migration Date:** `<YYYY-MM-DD>`
> **Owner:** `<team-or-individual>`
> **AWS Account(s):** `<account-id(s)>`
> **Azure Subscription(s):** `<subscription-id(s)>`

---

## 1. IAM Roles Inventory & Mapping

List all AWS IAM roles used by the application and map each to the appropriate Azure identity type.

| # | AWS IAM Role | Purpose | Azure Identity Type | Azure Identity Name | Status |
|---|---|---|---|---|---|
| 1 | | | ☐ System-Assigned MI ☐ User-Assigned MI ☐ Service Principal | | ☐ Mapped ☐ Created ☐ Verified |
| 2 | | | ☐ System-Assigned MI ☐ User-Assigned MI ☐ Service Principal | | ☐ Mapped ☐ Created ☐ Verified |
| 3 | | | ☐ System-Assigned MI ☐ User-Assigned MI ☐ Service Principal | | ☐ Mapped ☐ Created ☐ Verified |
| 4 | | | ☐ System-Assigned MI ☐ User-Assigned MI ☐ Service Principal | | ☐ Mapped ☐ Created ☐ Verified |
| 5 | | | ☐ System-Assigned MI ☐ User-Assigned MI ☐ Service Principal | | ☐ Mapped ☐ Created ☐ Verified |

---

## 2. IAM Policies → Azure RBAC Role Mapping

List all AWS IAM policies (inline and managed) and map each permission set to Azure RBAC roles.

| # | AWS IAM Policy | AWS Actions | Azure RBAC Role | Azure Scope | Status |
|---|---|---|---|---|---|
| 1 | | | | | ☐ Mapped ☐ Assigned ☐ Verified |
| 2 | | | | | ☐ Mapped ☐ Assigned ☐ Verified |
| 3 | | | | | ☐ Mapped ☐ Assigned ☐ Verified |
| 4 | | | | | ☐ Mapped ☐ Assigned ☐ Verified |
| 5 | | | | | ☐ Mapped ☐ Assigned ☐ Verified |

**Quick reference — common mappings:**

| AWS Actions | Azure RBAC Role |
|---|---|
| `s3:GetObject`, `s3:PutObject` | Storage Blob Data Contributor |
| `s3:GetObject` (read-only) | Storage Blob Data Reader |
| `sqs:SendMessage` | Azure Service Bus Data Sender |
| `sqs:ReceiveMessage` | Azure Service Bus Data Receiver |
| `dynamodb:*` | Cosmos DB Built-in Data Contributor |
| `secretsmanager:GetSecretValue` | Key Vault Secrets User |
| `kms:Encrypt`, `kms:Decrypt` | Key Vault Crypto User |
| `ecr:GetDownloadUrlForLayer` | AcrPull |
| `ecr:PutImage` | AcrPush |
| `logs:PutLogEvents` | Monitoring Metrics Publisher |

---

## 3. Authentication Mechanism Migration

Track the migration of each authentication mechanism from AWS to Azure.

### 3.1 Application Authentication

- [ ] **SDK credential provider migrated** — AWS SDK credential chain → `DefaultAzureCredential`
- [ ] **Environment variables updated** — `AWS_ACCESS_KEY_ID` / `AWS_SECRET_ACCESS_KEY` → Managed Identity (no env vars needed) or `AZURE_CLIENT_ID` / `AZURE_TENANT_ID`
- [ ] **Hardcoded credentials removed** — searched codebase for AWS access keys and removed all instances
- [ ] **Configuration files updated** — removed `~/.aws/credentials` references; app config points to Azure endpoints
- [ ] **Local development auth configured** — developers can use `az login` + `DefaultAzureCredential` for local testing

### 3.2 CI/CD Pipeline Authentication

- [ ] **Pipeline identity migrated** — AWS IAM user/role for CI/CD → Entra ID workload identity federation
- [ ] **OIDC federation configured** — GitHub Actions / ADO configured with federated credentials (no secrets)
- [ ] **Pipeline secrets updated** — `AWS_ACCESS_KEY_ID` / `AWS_SECRET_ACCESS_KEY` secrets removed from CI/CD
- [ ] **Azure secrets configured** — `AZURE_CLIENT_ID`, `AZURE_TENANT_ID`, `AZURE_SUBSCRIPTION_ID` set in CI/CD

### 3.3 User Authentication

- [ ] **Identity provider migrated** — Cognito User Pool → Entra ID (or Entra External ID for B2C)
- [ ] **Authentication SDK updated** — Cognito SDK / Amplify Auth → MSAL library
- [ ] **Token validation updated** — JWT validation points to Entra ID endpoints
- [ ] **User migration planned** — existing Cognito users migrated or re-registered in Entra ID
- [ ] **MFA configuration migrated** — Cognito MFA → Entra ID MFA / Conditional Access

---

## 4. Cross-Account Access → Cross-Subscription RBAC

List all cross-account access patterns and map to Azure cross-subscription RBAC.

| # | Source AWS Account | Target AWS Account | AssumeRole ARN | Azure Source Identity | Azure Target Scope | Azure RBAC Role | Status |
|---|---|---|---|---|---|---|---|
| 1 | | | | | | | ☐ Mapped ☐ Assigned ☐ Verified |
| 2 | | | | | | | ☐ Mapped ☐ Assigned ☐ Verified |
| 3 | | | | | | | ☐ Mapped ☐ Assigned ☐ Verified |

---

## 5. Service Identity Migration (IAM Roles for Services → Managed Identities)

Track the migration of each AWS service IAM role to an Azure Managed Identity.

| # | AWS Service | AWS IAM Role | Azure Service | Managed Identity Type | MI Created | RBAC Assigned | Tested |
|---|---|---|---|---|---|---|---|
| 1 | EC2 | | VM / App Service | ☐ System ☐ User | ☐ | ☐ | ☐ |
| 2 | ECS / Fargate | | Container Apps | ☐ System ☐ User | ☐ | ☐ | ☐ |
| 3 | Lambda | | Azure Functions | ☐ System ☐ User | ☐ | ☐ | ☐ |
| 4 | EKS (IRSA) | | AKS (Workload Identity) | ☐ Workload Identity | ☐ | ☐ | ☐ |
| 5 | | | | ☐ System ☐ User | ☐ | ☐ | ☐ |

---

## 6. Governance & Policy Migration

Track migration of organizational governance controls from AWS to Azure.

- [ ] **Service Control Policies (SCPs) → Azure Policy** — organization-level restrictions mapped and applied
- [ ] **Permission Boundaries → Custom RBAC roles** — IAM permission boundaries translated to custom role definitions with constrained action sets
- [ ] **Tag policies → Azure Policy tag enforcement** — required tags enforced via Azure Policy
- [ ] **AWS Config Rules → Azure Policy compliance** — compliance rules translated to Azure Policy definitions
- [ ] **CloudTrail → Azure Activity Log + Entra ID Audit Logs** — audit logging configured and verified
- [ ] **IAM Access Analyzer → Entra ID Access Reviews** — periodic access reviews scheduled

---

## 7. Credential Cleanup Verification

Confirm all AWS credentials have been removed from the migrated application.

- [ ] Searched codebase for `AWS_ACCESS_KEY_ID` — no results
- [ ] Searched codebase for `AWS_SECRET_ACCESS_KEY` — no results
- [ ] Searched codebase for `AKIA` prefix (AWS access key pattern) — no results
- [ ] Searched codebase for `aws_access_key` — no results
- [ ] Searched codebase for `aws_secret_key` — no results
- [ ] Searched CI/CD secrets for residual AWS credentials — removed
- [ ] Searched environment variable configs for AWS references — removed
- [ ] Verified no `~/.aws/credentials` file references remain
- [ ] Confirmed application starts and authenticates using Azure identity only

---

## 8. Validation & Sign-Off

| Validation Step | Date | Verified By | Notes |
|---|---|---|---|
| All IAM roles mapped to Azure identities | | | |
| All IAM policies mapped to RBAC roles | | | |
| Managed Identities created and RBAC assigned | | | |
| Application authenticates via DefaultAzureCredential | | | |
| Cross-subscription access working | | | |
| CI/CD pipeline uses federated credentials | | | |
| AWS credentials fully removed | | | |
| Governance policies applied (Azure Policy) | | | |
| Access reviews / PIM configured | | | |
| **Final sign-off** | | | |
