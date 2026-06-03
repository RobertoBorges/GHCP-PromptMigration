# RBAC Least Privilege

Use this skill when assigning Azure permissions for applications, pipelines, and operators.

## Rules

- Scope roles as low as possible: resource > resource group > subscription.
- Avoid `Owner` unless absolutely required.
- Prefer built-in roles before custom roles.
- Separate deployment permissions from runtime permissions.

## Common role mappings

| Need | Recommended role |
|---|---|
| Read secrets from Key Vault | `Key Vault Secrets User` |
| Deploy to App Service | `Website Contributor` or deployment-specific role set |
| Pull from ACR in AKS/Container Apps | `AcrPull` |
| Read monitoring data | `Monitoring Reader` |

## Validation checklist

- Every role assignment has a named purpose.
- Human and workload identities are separated.
- Broad inherited permissions are not relied on silently.
