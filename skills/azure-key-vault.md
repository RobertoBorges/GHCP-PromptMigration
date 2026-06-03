# Azure Key Vault

Use this skill when applications or pipelines must retrieve secrets, certificates, or keys from Azure without embedding them in source control.

## Core rules

- Prefer **RBAC-only** Key Vault configuration.
- Prefer **managed identity** for Azure-hosted workloads.
- Store secrets by purpose and environment, using predictable names.
- Keep certificates and signing keys separate from generic application secrets.

## Integration pattern

1. Enable system- or user-assigned managed identity.
2. Grant `Key Vault Secrets User` or a narrower role at the vault scope.
3. Add Key Vault as a configuration source or fetch secrets through the SDK.
4. Keep local development on environment variables or developer credentials.

## .NET example

```csharp
using Azure.Identity;

builder.Configuration.AddAzureKeyVault(
    new Uri(builder.Configuration["KeyVaultUri"]!),
    new DefaultAzureCredential());
```

## Validation checklist

- No secret values are committed.
- App identity has only the roles it needs.
- Rotation strategy exists for secrets and certificates.
- Failure behavior is logged and diagnosable.
