# Managed Identity

Use this skill when Azure-hosted workloads need to access Azure services without storing passwords, client secrets, or connection-string credentials.

## Use Cases

Apply this skill when the solution needs:

- workload identity for App Service, Container Apps, Functions, AKS, VMs, or automation
- secret-free access to Key Vault, Storage, Azure SQL, Service Bus, Event Hubs, or App Configuration
- replacement for service principals that currently depend on client secrets or certificates
- separation of runtime identity from deployment identity
- migration guidance that removes credentials instead of merely relocating them

## Core Rule

Prefer managed identity over stored credentials for Azure-to-Azure access.

Do not keep workload credentials in:

- source code or checked-in config files
- deployment manifests or container images
- pipeline variables when they only bootstrap Azure access
- wiki pages, runbooks, tickets, or screenshots

## Identity Selection

Choose the identity type intentionally.

| Scenario | Preferred Pattern | Why |
|---|---|---|
| One app owns one identity lifecycle | system-assigned managed identity | simplest setup and cleanup |
| Multiple apps/jobs need the same permissions | user-assigned managed identity | reusable principal and stable lifecycle |
| Identity must survive app redeploy or move across hosts | user-assigned managed identity | decoupled from compute resource |
| App also needs user sign-in | Entra app registration for users + managed identity for Azure resources | separates user auth from workload auth |
| Non-Azure host needs Azure access | service principal or workload identity federation | managed identity is only for Azure-hosted compute |

## Access Pattern Baseline

Managed identity is only half the design.

Also require:

- Azure RBAC at the smallest practical scope
- resource-specific data-plane roles where applicable
- network access that matches the target resource posture
- explicit local-development fallback behavior

## Common Target Services

| Target Service | Preferred Auth Pattern | Typical Role |
|---|---|---|
| Key Vault secrets | managed identity + RBAC | `Key Vault Secrets User` |
| Blob Storage | managed identity + RBAC | `Storage Blob Data Reader` or `Storage Blob Data Contributor` |
| Azure SQL | Entra auth with managed identity | contained user / database role mapping |
| Service Bus | managed identity + RBAC | `Azure Service Bus Data Sender` / `Receiver` |
| Event Hubs | managed identity + RBAC | `Azure Event Hubs Data Sender` / `Receiver` |
| Azure App Configuration | managed identity + RBAC | `App Configuration Data Reader` |
| Container Registry pull | managed identity + RBAC | `AcrPull` |

## .NET Pattern

Use `DefaultAzureCredential` unless a narrower credential chain is required.

```csharp
using Azure.Identity;
using Azure.Security.KeyVault.Secrets;

var credential = new DefaultAzureCredential();
var client = new SecretClient(new Uri(keyVaultUri), credential);
```

This pattern lets local development use signed-in developer credentials while Azure-hosted runtime uses the managed identity.

## Hosting Patterns

### App Service

```bicep
resource app 'Microsoft.Web/sites@2023-12-01' = {
  name: appName
  location: location
  identity: {
    type: 'SystemAssigned'
  }
  properties: {}
}
```

### Container Apps

```bicep
resource app 'Microsoft.App/containerApps@2024-03-01' = {
  name: appName
  location: location
  identity: {
    type: 'SystemAssigned'
  }
  properties: {}
}
```

### User-Assigned Identity Attachment

```powershell
az identity create --name id-contoso-prod --resource-group rg-contoso-prod --location eastus
az webapp identity assign --name app-contoso-prod --resource-group rg-contoso-prod --identities $identityId
az containerapp identity assign --name ca-contoso-prod --resource-group rg-contoso-prod --user-assigned $identityId
```

## Azure SQL Pattern

Prefer Microsoft Entra authentication over SQL usernames and passwords.

Migration guidance should:

1. enable managed identity on the app
2. create the database principal for that identity
3. grant only required database roles
4. remove SQL password usage from config and pipelines

Use SQL auth only as a temporary exception and document the removal plan.

## Local Development Pattern

Document how developers authenticate locally.

Preferred order:

1. signed-in developer credentials through Azure CLI / Visual Studio / VS Code
2. environment-specific dev identity with least privilege
3. temporary local secret only when a target service cannot yet use Entra auth

Do not require developers to copy production secrets into local config.

## RBAC Baseline

Pair each managed identity with an explicit minimum role.

| Need | Recommended Role | Notes |
|---|---|---|
| Read secret at runtime | `Key Vault Secrets User` | runtime usually reads only |
| Read blob content | `Storage Blob Data Reader` | avoid account keys |
| Write to queue/topic | service-specific data sender role | avoid generic contributor |
| Pull image from ACR | `AcrPull` | no push/admin for runtime |
| Read app config | `App Configuration Data Reader` | separate from config admin |

Avoid giving managed identities broad control-plane roles such as `Contributor` unless the workload truly provisions resources.

## Network and Platform Considerations

Managed identity does not bypass networking.

Still validate:

- private endpoints, firewalls, and VNet integration where required
- outbound routing from App Service or Container Apps to restricted resources
- tenant and subscription boundaries for the referenced resource
- startup behavior when token acquisition or downstream RBAC fails

## Migration Patterns

| Legacy Pattern | Better Target |
|---|---|
| connection string with account key | managed identity + RBAC |
| Key Vault client secret auth | managed identity |
| SQL username/password in `web.config` | Entra auth + managed identity |
| pipeline secret for runtime Azure SDK auth | managed identity at runtime |
| shared service principal across many unrelated apps | per-app system identity or scoped shared user-assigned identity |

## Anti-Patterns

Treat these as findings:

- creating a managed identity but continuing to use secrets anyway
- assigning `Contributor`, `Owner`, or subscription-wide roles to runtime identities
- sharing one user-assigned identity across unrelated apps without justification
- using managed identity for user sign-in scenarios it does not solve
- skipping local-development guidance so the app works only in Azure

## Validation Checklist

- every Azure-hosted workload has a documented identity choice
- stored credentials were removed where the target service supports managed identity or Entra auth
- each identity has the minimum required RBAC role at the correct scope
- local development fallback is documented and does not depend on production secrets
- networking constraints were checked for every downstream resource
- exceptions are documented with a removal plan

## Output Expectations for Prompts

When this skill is applied, the prompt should:

- recommend system-assigned or user-assigned identity explicitly and explain why
- name the exact Azure resources that should trust the identity
- specify the minimum RBAC roles instead of broad admin access
- remove or flag every secret-based Azure access path that can be eliminated
- document local-development and failure-handling expectations
