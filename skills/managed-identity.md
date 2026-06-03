# Managed Identity

Use this skill when Azure-hosted workloads need secure access to Azure resources without stored credentials.

## Defaults

- Prefer **system-assigned managed identity** for single-resource ownership.
- Use **user-assigned managed identity** only when identity reuse is intentional.
- Pair identity with least-privilege RBAC.

## Application pattern

```csharp
using Azure.Identity;
using Azure.Security.KeyVault.Secrets;

var client = new SecretClient(new Uri(keyVaultUri), new DefaultAzureCredential());
```

## Typical targets

- Key Vault
- Azure SQL with Entra auth where supported
- Storage accounts
- Service Bus / Event Hubs

## Validation checklist

- No connection secret exists where managed identity can replace it.
- The assigned role is minimal and scoped correctly.
- Local development fallback is documented.
