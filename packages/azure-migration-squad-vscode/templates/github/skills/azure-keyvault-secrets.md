# Azure Key Vault Secrets and Certificates

Use this skill when migrating any application secret, certificate, key, or connection string to Azure-hosted workloads.

## Use Cases

Apply this skill when the solution needs:

- secret storage outside source control and deployment manifests
- certificate lifecycle management for HTTPS, mutual TLS, or signing
- workload identity access from App Service, Container Apps, Functions, or VMs
- replacement for appsettings, web.config, `.env`, or pipeline-stored secrets
- audit logging, rotation policy, and security review evidence

## Core Rule

Use Azure Key Vault for secrets, certificates, and cryptographic keys by default.

Do not keep production secrets in:

- source code
- `appsettings.json`, `web.config`, or checked-in `.env` files
- pipeline variables unless they only bootstrap Key Vault access
- wiki pages, runbooks, tickets, or logs

## Managed Identity Pattern

Prefer managed identity over client secrets.

| Scenario | Preferred Pattern | Why |
|---|---|---|
| Single App Service or Container App reads its own secrets | system-assigned managed identity | lowest operational overhead |
| Multiple apps need the same identity or same Key Vault access | user-assigned managed identity | reusable permissions and stable principal |
| Cross-subscription or pre-provisioned identity lifecycle is required | user-assigned managed identity | identity survives app redeploy |
| App needs user sign-in | Entra app registration + managed identity for downstream Azure access | separate user identity from workload identity |

## RBAC Roles

Prefer Azure RBAC on the vault over legacy access policies.

| Need | Recommended Role | Notes |
|---|---|---|
| Read secret values at runtime | `Key Vault Secrets User` | app runtime should usually only read |
| Use keys for encrypt/decrypt/sign/verify | `Key Vault Crypto User` | for app-level crypto operations |
| Manage certificate lifecycle | `Key Vault Certificates Officer` | not required for ordinary secret reads |
| Manage vault configuration | narrow admin role, not app identity | keep runtime and admin identities separate |

Do not give application identities broad roles such as `Key Vault Contributor` unless they truly manage the vault.

## Key Vault Baseline

For production, expect this minimum baseline:

- soft delete enabled
- purge protection enabled
- RBAC authorization enabled
- diagnostic settings enabled
- private endpoint for high-value workloads
- public network access restricted where feasible
- naming and tags aligned with environment ownership

## Bicep Pattern

```bicep
resource kv 'Microsoft.KeyVault/vaults@2023-07-01' = {
  name: 'kv-${appName}-${environmentName}'
  location: location
  properties: {
    tenantId: tenantId
    enableRbacAuthorization: true
    enablePurgeProtection: true
    enableSoftDelete: true
    sku: {
      family: 'A'
      name: 'standard'
    }
    publicNetworkAccess: 'Disabled'
  }
}
```

## App Service Key Vault References

Use platform references when the app only needs configuration injection.

```text
ConnectionStrings__Default=@Microsoft.KeyVault(SecretUri=https://kv-contoso-prod.vault.azure.net/secrets/sql-default/)
ApiKeys__Payments=@Microsoft.KeyVault(VaultName=kv-contoso-prod;SecretName=payments-api-key)
```

Use a versionless secret URI when normal rotation should roll forward automatically.

If App Service uses a user-assigned identity for Key Vault references, bind it explicitly:

```powershell
az webapp identity assign --name app-contoso-prod --resource-group rg-contoso-prod --identities $userAssignedIdentityId
az webapp update --name app-contoso-prod --resource-group rg-contoso-prod --set keyVaultReferenceIdentity=$userAssignedIdentityId
```

If the vault is network-restricted, enable outbound routing through VNet integration:

```powershell
az webapp config set --name app-contoso-prod --resource-group rg-contoso-prod --generic-configurations '{"vnetRouteAllEnabled": true}'
```

## Container Apps Key Vault References

Use Key Vault-backed secrets in Container Apps configuration rather than baking secrets into images.

```bicep
resource app 'Microsoft.App/containerApps@2024-03-01' = {
  name: 'ca-contoso-prod'
  location: location
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    configuration: {
      secrets: [
        {
          name: 'sql-connection'
          keyVaultUrl: 'https://kv-contoso-prod.vault.azure.net/secrets/sql-connection'
          identity: 'system'
        }
      ]
    }
  }
}
```

CLI pattern:

```powershell
az containerapp secret set --name ca-contoso-prod --resource-group rg-contoso-prod --secrets sql-connection=keyvaultref:https://kv-contoso-prod.vault.azure.net/secrets/sql-connection,identityref:system
```

## Connection String Migration Pattern

Move connection details in this order:

1. remove secrets from `appsettings.json`, `web.config`, Helm values, or `.env`
2. keep only logical configuration keys in the app
3. store the secret value in Key Vault
4. inject it through Key Vault references or SDK retrieval
5. prefer Entra auth or managed identity to eliminate the secret entirely when the target service supports it

| Legacy Pattern | Better Target |
|---|---|
| checked-in `appsettings.Production.json` connection string | Key Vault secret reference |
| pipeline variable holding database password | Key Vault secret + managed identity bootstrap |
| static storage account key | managed identity + RBAC |
| TLS cert uploaded manually to each app | Key Vault certificate with centralized lifecycle |

## Rotation Patterns

Choose a rotation model explicitly.

| Secret Type | Preferred Rotation Pattern | Notes |
|---|---|---|
| database password that cannot yet be removed | rotate in Key Vault, update downstream service, validate app refresh | keep emergency rollback plan |
| API key for external SaaS | dual-key or overlapping-validity rotation | avoid one-shot cutovers |
| certificates | auto-renew where integrated, otherwise staged rollover | track issuer and expiry |
| storage or service credentials | replace with managed identity where possible | best rotation is removal |

Operational rules:

- document owner, cadence, and validation steps
- alert before expiry, not after outage
- use versioned secrets when pinning is required for controlled release windows
- use versionless references when automatic pickup of current version is desired
- test how the platform refreshes references before relying on zero-downtime rotation

## Certificate Management

Use Key Vault certificates when the workload needs central issuance, renewal tracking, or export control.

- prefer App Service managed certificates for the simplest public web scenarios
- use Key Vault certificates when multiple services share the cert or compliance requires centralized control
- document issuer, SAN coverage, renewal owner, and installation target
- rotate certificates before expiration windows become operational incidents

## Access Policies vs RBAC

| Model | Recommendation |
|---|---|
| Key Vault access policies | legacy-only; avoid for new migration work |
| Azure RBAC for data plane | preferred default |
| Mixed access policies and RBAC | avoid unless required by a legacy constraint |

Use access policies only when a specific service limitation forces them and record that exception in the migration report.

## Diagnostics and Audit Logging

Enable diagnostic settings for every production vault.

```powershell
az monitor diagnostic-settings create --name kv-to-law --resource $(az keyvault show --name kv-contoso-prod --query id -o tsv) --workspace $lawId --logs '[{"category":"AuditEvent","enabled":true}]'
```

Capture at minimum:

- `AuditEvent` logs to Log Analytics, Event Hub, or Storage
- alerting on unauthorized access attempts and secret expiry
- ownership for reviewing vault access changes
- evidence of rotation and certificate renewal events

## Anti-Patterns

Treat these as security findings:

- secrets in code, config files, ARM parameters, or Terraform variables committed to git
- secrets echoed to console output, build logs, or test artifacts
- app runtime identities with admin-level vault permissions
- pipeline secrets copied into app settings when a Key Vault reference would work
- using Key Vault as a generic database for non-secret application data

## Validation Checklist

- managed identity is enabled for every Azure-hosted runtime that reads secrets
- vault authorization uses RBAC unless a documented exception exists
- runtime identity has only the required data-plane role
- app settings and container secrets reference Key Vault rather than storing plaintext
- diagnostic settings and audit log retention are configured
- secret rotation and certificate renewal ownership are documented

## Output Expectations for Prompts

When this skill is applied, the prompt should:

- externalize every credential, certificate, and key to Key Vault or remove it through managed identity
- specify whether system-assigned or user-assigned identity is required and why
- recommend exact RBAC roles instead of generic admin access
- document rotation, certificate renewal, and audit logging expectations
- flag every secret-in-config or secret-in-pipeline pattern as remediation work
