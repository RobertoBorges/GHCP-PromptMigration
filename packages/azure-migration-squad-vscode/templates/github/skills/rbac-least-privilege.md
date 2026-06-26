# RBAC Least Privilege

Use this skill when assigning Azure permissions for applications, pipelines, automation, operators, or support teams.

## Use Cases

Apply this skill when the solution needs:

- Azure RBAC design for managed identities, service principals, and human operators
- separation of deployment permissions from runtime permissions
- scoped access for Key Vault, Storage, App Configuration, messaging, monitoring, or databases
- migration away from broad inherited permissions or subscription-level roles
- review evidence that permissions are justified, narrow, and auditable

## Core Rule

Grant the minimum role, to the correct identity, at the smallest practical scope.

Default scope order:

resource -> resource group -> subscription

Do not use `Owner` or broad `Contributor` roles for convenience when a narrower data-plane or service role exists.

## Identity Separation

Separate responsibilities before choosing roles.

| Identity Type | Purpose | Typical Access Pattern |
|---|---|---|
| Runtime workload identity | app reads/writes only what it needs | narrow data-plane role |
| Deployment identity | provisions or updates Azure resources | scoped control-plane role |
| Human operator | support, diagnostics, approval | read or operator role with JIT where possible |
| Break-glass admin | emergency recovery only | tightly controlled, audited, rarely used |

Do not reuse one identity for runtime, deployment, and human operations.

## Role Selection Workflow

Choose roles in this order:

1. define the exact action the identity must perform
2. determine whether it needs control-plane or data-plane access
3. choose the smallest built-in role that satisfies only that action
4. scope the assignment to the specific resource when possible
5. document why broader scope or a custom role is required if no built-in role fits

## Scope Guidance

| Scope | When to Use | Risk Level |
|---|---|---|
| Resource | default for app runtime and single-service access | lowest |
| Resource group | shared lifecycle or several tightly related resources | moderate |
| Subscription | only for true platform operations or central automation | high |
| Management group | rare; enterprise governance scenarios only | very high |

If the assignment can be made at resource scope, do not place it at resource group or subscription scope.

## Common Role Mappings

| Need | Recommended Role | Notes |
|---|---|---|
| Read Key Vault secret values | `Key Vault Secrets User` | runtime should usually only read |
| Manage Key Vault secrets/certs | dedicated admin role, not runtime identity | separate admin from app runtime |
| Read blobs | `Storage Blob Data Reader` | avoid account keys |
| Write blobs | `Storage Blob Data Contributor` | not full storage account contributor |
| Read App Configuration | `App Configuration Data Reader` | runtime reads config only |
| Send Service Bus messages | `Azure Service Bus Data Sender` | sender only |
| Receive Service Bus messages | `Azure Service Bus Data Receiver` | receiver only |
| Send Event Hubs data | `Azure Event Hubs Data Sender` | sender only |
| Receive Event Hubs data | `Azure Event Hubs Data Receiver` | receiver only |
| Pull container images | `AcrPull` | runtime rarely needs push |
| Read monitoring data | `Monitoring Reader` | diagnostics and support |
| Deploy web app content/config | deployment-specific web role set | keep separate from runtime |

Prefer built-in roles before custom roles.

## Bicep Pattern

Use explicit role assignments tied to principal IDs.

```bicep
resource secretsUserRole 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(keyVault.id, managedIdentity.properties.principalId, 'KeyVaultSecretsUser')
  scope: keyVault
  properties: {
    principalId: managedIdentity.properties.principalId
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', '4633458b-17de-408a-b874-0445c86b69e6')
    principalType: 'ServicePrincipal'
  }
}
```

Assign at the target resource scope unless there is a documented reason to go broader.

## Review Questions

Before approving a role assignment, ask:

- what exact operation requires this role?
- is this a runtime, deployment, or human identity?
- can the scope be narrowed to a single resource?
- does a data-plane role exist instead of control-plane contributor rights?
- is there already inherited access that should be removed rather than relied on silently?

## Custom Roles

Use a custom role only when:

- no built-in role matches the exact permission set
- the permissions are stable and reusable
- the custom role definition is reviewed and versioned
- the blast radius is lower than using a broad built-in role

Do not create custom roles just to avoid understanding built-in roles.

## Anti-Patterns

Treat these as findings:

- `Owner` used for app runtime identities
- subscription-wide `Contributor` for a single app or pipeline stage
- human users sharing the same identity as application runtime
- broad inherited access left undocumented
- secret-read identities also receiving vault or subscription admin rights
- deployment identities retaining permanent prod admin access when JIT or narrower scope would work

## Validation Checklist

- every assignment has a named business or technical purpose
- runtime, deployment, and human identities are separated
- smallest viable built-in role was selected first
- scope is resource-level unless broader scope is justified
- broad inherited permissions were reviewed and documented
- exceptions and custom roles include rationale and owner

## Output Expectations for Prompts

When this skill is applied, the prompt should:

- name the identity that needs access and what it must do
- recommend exact Azure roles, not generic admin language
- specify the assignment scope explicitly
- separate runtime, deployment, and operator permissions
- flag every broad or inherited permission pattern as remediation work
