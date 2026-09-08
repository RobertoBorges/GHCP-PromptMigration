---
name: aws-iam-to-azure-rbac
description: Migrate AWS Identity and Access Management (IAM) to Azure Entra ID, Azure RBAC, and Managed Identities. Covers IAM users, groups, roles, policies, resource-based policies, cross-account trust, STS assume-role patterns, and the mapping from AWS policy JSON to Azure role assignments. Use during Phase 2 of AWS-to-Azure migration when identity model is in scope.
---

# AWS IAM → Azure Entra ID + RBAC + Managed Identity Migration Guide

This skill provides comprehensive guidance for migrating AWS Identity and Access Management (IAM) to Azure's identity and authorization platform: **Entra ID**, **Role-Based Access Control (RBAC)**, and **Managed Identities**.

---

## Conceptual Mapping

| AWS Concept | Azure Equivalent | Notes |
|---|---|---|
| IAM User | Entra ID User | Human identities managed in Entra ID tenant |
| IAM Group | Entra ID Group | Security groups for role assignment; supports dynamic membership |
| IAM Role (for services) | Managed Identity (System/User-Assigned) | Preferred for Azure services; no credentials to manage |
| IAM Role (cross-account / federation) | Entra ID App Registration + Service Principal | For service identities, external integrations, and CI/CD |
| IAM Policy (JSON) | Azure RBAC Role Assignment | Different structure; RBAC assigns built-in or custom roles at a scope |
| Resource-based Policy | RBAC scoped to resource | Azure RBAC can be assigned at resource, resource group, subscription, or management group scope |
| STS AssumeRole | Entra ID federated credentials / app-to-app auth | Workload identity federation eliminates shared secrets |
| Service Control Policies (SCPs) | Azure Policy | Organization-level governance and compliance enforcement |
| Permission Boundaries | Custom RBAC roles with limited scope | Define a ceiling for permissions via custom role definitions |
| AWS Account | Azure Subscription | Billing and governance boundary |
| AWS Organization | Azure Management Group | Hierarchical grouping of subscriptions |
| Cross-account access | Cross-subscription RBAC | Assign RBAC roles to identities across subscriptions within the same or different tenants |
| AWS SSO / Identity Center | Entra ID (with SSO and Conditional Access) | Centralized identity provider with MFA, conditional access policies |
| Cognito User Pools | Entra ID (B2C or External Identities) | User authentication for customer-facing applications |

---

## IAM Policy → RBAC Translation Patterns

AWS IAM policies are JSON documents that grant or deny actions on resources. Azure uses **RBAC role assignments** that bind a **principal** (user, group, service principal, or managed identity) to a **role definition** at a **scope**.

### Common Service-Level Translations

| AWS IAM Permission | Azure Built-in RBAC Role | Scope |
|---|---|---|
| `s3:GetObject`, `s3:PutObject` on a bucket | **Storage Blob Data Contributor** | Storage account or container |
| `s3:GetObject` (read-only) | **Storage Blob Data Reader** | Storage account or container |
| `sqs:SendMessage` | **Azure Service Bus Data Sender** | Service Bus namespace or queue |
| `sqs:ReceiveMessage`, `sqs:DeleteMessage` | **Azure Service Bus Data Receiver** | Service Bus namespace or queue |
| `dynamodb:GetItem`, `dynamodb:PutItem`, `dynamodb:Query` | **Cosmos DB Built-in Data Contributor** | Cosmos DB account or database |
| `dynamodb:GetItem`, `dynamodb:Query` (read-only) | **Cosmos DB Built-in Data Reader** | Cosmos DB account or database |
| `lambda:InvokeFunction` | **Website Contributor** or custom role | Function App |
| `secretsmanager:GetSecretValue` | **Key Vault Secrets User** | Key Vault or individual secret |
| `secretsmanager:CreateSecret`, `secretsmanager:PutSecretValue` | **Key Vault Secrets Officer** | Key Vault |
| `kms:Encrypt`, `kms:Decrypt` | **Key Vault Crypto User** | Key Vault or individual key |
| `ecr:GetDownloadUrlForLayer`, `ecr:BatchGetImage` | **AcrPull** | Azure Container Registry |
| `ecr:PutImage`, `ecr:InitiateLayerUpload` | **AcrPush** | Azure Container Registry |
| `logs:PutLogEvents`, `cloudwatch:PutMetricData` | **Monitoring Metrics Publisher** | Resource or resource group |
| `logs:GetLogEvents`, `cloudwatch:GetMetricData` | **Monitoring Reader** | Resource or resource group |
| `sns:Publish` | **Azure Service Bus Data Sender** (or Event Grid) | Service Bus topic or Event Grid domain |
| `sts:AssumeRole` | Federated credential or RBAC role assignment | Target subscription or resource |

### Example: AWS S3 Policy → Azure RBAC

**AWS IAM Policy (JSON):**

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:PutObject",
        "s3:DeleteObject"
      ],
      "Resource": "arn:aws:s3:::my-app-bucket/*"
    }
  ]
}
```

**Azure RBAC equivalent (Azure CLI):**

```bash
# Assign Storage Blob Data Contributor role to a managed identity at the container scope
az role assignment create \
  --assignee "<managed-identity-principal-id>" \
  --role "Storage Blob Data Contributor" \
  --scope "/subscriptions/<sub-id>/resourceGroups/<rg>/providers/Microsoft.Storage/storageAccounts/<account>/blobServices/default/containers/my-app-bucket"
```

### Example: AWS Secrets Manager Policy → Azure Key Vault RBAC

**AWS IAM Policy (JSON):**

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "secretsmanager:GetSecretValue",
      "Resource": "arn:aws:secretsmanager:us-east-1:123456789012:secret:my-app/*"
    }
  ]
}
```

**Azure RBAC equivalent (Azure CLI):**

```bash
# Assign Key Vault Secrets User role at the Key Vault scope
az role assignment create \
  --assignee "<managed-identity-principal-id>" \
  --role "Key Vault Secrets User" \
  --scope "/subscriptions/<sub-id>/resourceGroups/<rg>/providers/Microsoft.KeyVault/vaults/<vault-name>"
```

### Example: AWS SQS Policy → Azure Service Bus RBAC

**AWS IAM Policy (JSON):**

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "sqs:SendMessage",
        "sqs:ReceiveMessage",
        "sqs:DeleteMessage"
      ],
      "Resource": "arn:aws:sqs:us-east-1:123456789012:my-queue"
    }
  ]
}
```

**Azure RBAC equivalent (Azure CLI):**

```bash
# Sender role
az role assignment create \
  --assignee "<sender-identity-principal-id>" \
  --role "Azure Service Bus Data Sender" \
  --scope "/subscriptions/<sub-id>/resourceGroups/<rg>/providers/Microsoft.ServiceBus/namespaces/<namespace>/queues/my-queue"

# Receiver role
az role assignment create \
  --assignee "<receiver-identity-principal-id>" \
  --role "Azure Service Bus Data Receiver" \
  --scope "/subscriptions/<sub-id>/resourceGroups/<rg>/providers/Microsoft.ServiceBus/namespaces/<namespace>/queues/my-queue"
```

---

## Authentication Migration

### CLI and Developer Authentication

| AWS | Azure | Notes |
|---|---|---|
| `aws configure` (access key + secret) | `az login` (browser-based OAuth) | No long-lived credentials stored locally |
| `~/.aws/credentials` profiles | `az login` + `az account set` | Azure CLI manages token refresh automatically |
| `AWS_ACCESS_KEY_ID` / `AWS_SECRET_ACCESS_KEY` env vars | `AZURE_CLIENT_ID` / `AZURE_CLIENT_SECRET` / `AZURE_TENANT_ID` env vars | Only for service principal auth; prefer managed identity |
| `AWS_PROFILE` | `AZURE_SUBSCRIPTION_ID` | Select which subscription context to use |
| `aws sts get-caller-identity` | `az account show` | Verify current identity |

### SDK Credential Chain

**AWS SDK credential resolution order:**

1. Environment variables (`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`)
2. Shared credentials file (`~/.aws/credentials`)
3. IAM role for EC2/ECS/Lambda (instance metadata)

**Azure `DefaultAzureCredential` resolution order:**

1. Environment variables (`AZURE_CLIENT_ID`, `AZURE_CLIENT_SECRET`, `AZURE_TENANT_ID`)
2. Workload identity (Kubernetes)
3. Managed Identity (System-Assigned or User-Assigned)
4. Azure CLI (`az login`)
5. Azure PowerShell (`Connect-AzAccount`)
6. Azure Developer CLI (`azd auth login`)
7. Interactive browser

**Migration in code (.NET):**

```csharp
// BEFORE: AWS SDK
using Amazon;
using Amazon.S3;
var s3Client = new AmazonS3Client(RegionEndpoint.USEast1);
// Relies on AWS credential chain

// AFTER: Azure SDK with DefaultAzureCredential
using Azure.Identity;
using Azure.Storage.Blobs;
var credential = new DefaultAzureCredential();
var blobClient = new BlobServiceClient(
    new Uri("https://<account>.blob.core.windows.net"),
    credential);
```

**Migration in code (Java):**

```java
// BEFORE: AWS SDK
import software.amazon.awssdk.services.s3.S3Client;
S3Client s3 = S3Client.builder()
    .region(Region.US_EAST_1)
    .build();
// Relies on AWS credential chain

// AFTER: Azure SDK with DefaultAzureCredential
import com.azure.identity.DefaultAzureCredentialBuilder;
import com.azure.storage.blob.BlobServiceClient;
import com.azure.storage.blob.BlobServiceClientBuilder;
DefaultAzureCredential credential = new DefaultAzureCredentialBuilder().build();
BlobServiceClient blobClient = new BlobServiceClientBuilder()
    .endpoint("https://<account>.blob.core.windows.net")
    .credential(credential)
    .buildClient();
```

### Service Identity Migration

| AWS Pattern | Azure Equivalent | When to Use |
|---|---|---|
| IAM Role for EC2 (instance profile) | System-Assigned Managed Identity for VM | VM needs access to Azure resources |
| IAM Role for ECS Task | System-Assigned Managed Identity for Container Apps | Container workload identity |
| IAM Role for Lambda | System-Assigned Managed Identity for Azure Functions | Serverless function identity |
| IAM Role for EKS Pod (IRSA) | Workload Identity for AKS Pod | Kubernetes pod-level identity |
| Cross-account IAM Role (AssumeRole) | Cross-subscription RBAC assignment | Service in Sub A accesses resources in Sub B |
| IAM Role for GitHub Actions (OIDC) | Entra ID federated credential for GitHub Actions | CI/CD pipeline identity |
| IAM User with access keys (service account) | User-Assigned Managed Identity or Service Principal | Shared identity across multiple services |

### Enabling Managed Identity (Azure CLI)

```bash
# System-Assigned MI for a Web App
az webapp identity assign --name <app-name> --resource-group <rg>

# System-Assigned MI for an Azure Function
az functionapp identity assign --name <func-name> --resource-group <rg>

# System-Assigned MI for Container Apps
az containerapp identity assign --name <app-name> --resource-group <rg> --system-assigned

# Create a User-Assigned MI (shared across services)
az identity create --name <identity-name> --resource-group <rg>

# Assign User-Assigned MI to a Web App
az webapp identity assign --name <app-name> --resource-group <rg> \
  --identities "/subscriptions/<sub-id>/resourceGroups/<rg>/providers/Microsoft.ManagedIdentity/userAssignedIdentities/<identity-name>"
```

### Cross-Account → Cross-Subscription Access

**AWS pattern (AssumeRole):**

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "sts:AssumeRole",
      "Resource": "arn:aws:iam::ACCOUNT-B:role/CrossAccountRole"
    }
  ]
}
```

**Azure equivalent (cross-subscription RBAC):**

```bash
# Grant a managed identity from Subscription A access to a resource in Subscription B
az role assignment create \
  --assignee "<managed-identity-principal-id-from-sub-A>" \
  --role "Storage Blob Data Reader" \
  --scope "/subscriptions/<sub-B-id>/resourceGroups/<rg>/providers/Microsoft.Storage/storageAccounts/<account>"
```

### Cognito → Entra ID

| AWS Cognito Feature | Azure Entra ID Equivalent |
|---|---|
| User Pool | Entra ID tenant (or Entra External ID for B2C) |
| Identity Pool | Entra ID token exchange / federated credentials |
| Hosted UI | Entra ID sign-in experience (customizable) |
| User Pool Groups | Entra ID Security Groups + App Roles |
| Custom attributes | Entra ID extension attributes or custom claims |
| Lambda triggers | Authentication events + custom extensions |
| Cognito SDK (`Auth.signIn()`) | MSAL library (`acquireTokenSilent()`) |

---

## Best Practices

### Identity and Credential Management

1. **Always prefer Managed Identity over service principals with secrets.** Managed Identities eliminate credential management entirely — no secrets to rotate, no risk of credential leakage.

2. **Use System-Assigned MI for single-service scenarios.** The identity lifecycle is tied to the resource — when the resource is deleted, the identity is automatically cleaned up.

3. **Use User-Assigned MI for shared identity across services.** When multiple services need the same permissions, create one User-Assigned MI and assign it to all of them. This reduces the number of role assignments to maintain.

4. **Remove ALL AWS credentials from code during migration.** Search for and remove:
   - Hardcoded access keys and secret keys
   - `AWS_ACCESS_KEY_ID` / `AWS_SECRET_ACCESS_KEY` in environment configs
   - `~/.aws/credentials` references in deployment scripts
   - AWS SDK credential provider configurations

5. **Use `DefaultAzureCredential` in application code.** It automatically works with Managed Identity in Azure and falls back to CLI credentials for local development — no code changes needed between environments.

### RBAC and Authorization

6. **Assign RBAC roles at the narrowest scope possible.** Prefer container-level over storage-account-level, prefer resource-group-level over subscription-level. This follows the principle of least privilege.

   ```
   Scope hierarchy (narrowest → broadest):
   Resource → Resource Group → Subscription → Management Group
   ```

7. **Use built-in roles before creating custom roles.** Azure provides 300+ built-in roles. Only create custom roles when no built-in role matches your requirements.

8. **Assign roles to groups, not individual users.** This mirrors the AWS best practice of attaching policies to groups. It simplifies management and auditing.

9. **Use Azure Policy for governance (equivalent to SCPs).** Apply policies at the management group or subscription level to enforce compliance across all resources.

   ```bash
   # Example: Deny creation of resources without required tags
   az policy assignment create \
     --name "require-cost-center-tag" \
     --policy "/providers/Microsoft.Authorization/policyDefinitions/<policy-id>" \
     --scope "/subscriptions/<sub-id>"
   ```

### Advanced Access Control

10. **Use Entra ID Conditional Access for context-aware security.** This goes beyond AWS IAM conditions by evaluating device compliance, location, risk level, and MFA status.

11. **Use Entra ID Privileged Identity Management (PIM) for just-in-time access.** PIM provides time-bound, approval-based role activation — equivalent to AWS IAM Access Analyzer + temporary credentials but more integrated.

12. **Audit role assignments regularly.** Use Azure Resource Graph to query all role assignments across subscriptions:

    ```bash
    az graph query -q "authorizationresources
      | where type == 'microsoft.authorization/roleassignments'
      | project principalId, roleDefinitionId, scope"
    ```

### Migration Sequencing

13. **Migrate identity before migrating workloads.** Ensure Entra ID users, groups, and managed identities are in place before migrating applications.

14. **Test with `DefaultAzureCredential` locally before deploying.** Run `az login` and verify your application can authenticate to Azure resources using CLI credentials before relying on Managed Identity in production.

15. **Use federated credentials for CI/CD pipelines.** Configure GitHub Actions (or other CI/CD) with Entra ID workload identity federation — no secrets stored in CI/CD:

    ```yaml
    # GitHub Actions example
    - uses: azure/login@v2
      with:
        client-id: ${{ secrets.AZURE_CLIENT_ID }}
        tenant-id: ${{ secrets.AZURE_TENANT_ID }}
        subscription-id: ${{ secrets.AZURE_SUBSCRIPTION_ID }}
    ```

---

## Common Pitfalls

| Pitfall | Resolution |
|---|---|
| Using access keys instead of Managed Identity | Always use MI for Azure-hosted services; use `DefaultAzureCredential` in code |
| Assigning Owner/Contributor at subscription scope | Use the most specific built-in role at the narrowest scope |
| Creating Key Vault access policies instead of RBAC | Always use Key Vault RBAC authorization model, not access policies |
| Not removing AWS credentials after migration | Audit code and config for residual `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, and credential files |
| Mapping AWS IAM policies 1:1 to custom RBAC roles | Use Azure built-in roles; they often combine what AWS splits across multiple policies |
| Ignoring Entra ID Conditional Access | Implement conditional access policies for MFA, device compliance, and location-based controls |
| Hardcoding tenant/subscription IDs in application code | Use environment variables or app configuration; `DefaultAzureCredential` handles this automatically |
