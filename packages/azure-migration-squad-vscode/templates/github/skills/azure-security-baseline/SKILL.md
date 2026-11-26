---
name: azure-security-baseline
description: |
  Security router for Azure migration work. Use when assessing or generating identity, secrets, network, RBAC, compliance, or OWASP security guidance for any supported app stack. Applies to Phase 1-6 planning, code migration, infrastructure generation, deployment, CI/CD, and post-migration hardening. Enforces standing rules: prefer managed identities over keys, store secrets in Azure Key Vault with RBAC not access policies, never commit secrets, and never query or modify Azure resources without explicit user consent.
user-invocable: false
---

# Azure Security Baseline

## When to use

Use this router whenever migration work touches Azure security posture, app authentication, workload identity, secret handling, permissions, network exposure, compliance readiness, or security review. It is stack-agnostic and applies across the repository's universal migration scope.

Standing rules to carry into every referenced topic:

- Prefer managed identities over connection strings, account keys, client secrets, and passwords.
- Store secrets, certificates, and keys in Azure Key Vault with Azure RBAC, not legacy access policies, unless a documented service limitation forces an exception.
- Never commit secrets or live connection strings to the repository, reports, examples, logs, screenshots, or generated artifacts.
- Never query or modify Azure resources without explicit user consent.
- Use least privilege at the smallest practical scope; separate runtime, deployment, and human identities.
- Treat public exposure, open admin ports, broad wildcard rules, missing telemetry, and unsupported components as remediation findings.

## Signal to reference selection

| Signal in the task or evidence | Load this reference | Use it for |
|---|---|---|
| Defender for Cloud, Secure Score, Azure Policy, SOC 2, GDPR, PCI DSS, ISO 27001, continuous export, compliance evidence | [Microsoft Defender for Cloud and compliance readiness](./references/azure-defender-compliance.md) | Posture review, Defender plan selection, Secure Score prioritization, policy guardrails, compliance-readiness evidence, and alert routing. |
| Entra ID, app registrations, OAuth/OIDC, JWT validation, scopes, app roles, workforce or external identity, replacing Windows/Forms/custom auth | [Azure Entra ID integration](./references/azure-entra-id.md) | User sign-in, API protection, delegated scopes, app roles, redirect URIs, and separating user identity from workload identity. |
| Key Vault, certificates, keys, app settings references, container secret references, vault diagnostics, purge protection, rotation | [Azure Key Vault secrets and certificates](./references/azure-keyvault-secrets.md) | Moving secrets/certs/keys to Key Vault, enabling RBAC, using platform references, diagnostics, and rotation practices. |
| Network isolation, public ingress, private endpoints, service endpoints, WAF, NSGs, TLS, IP restrictions, VNet integration, egress | [Azure network security and perimeter controls](./references/azure-network-security.md) | Edge/app/data/management tier boundaries, private connectivity, WAF placement, TLS enforcement, and network hardening findings. |
| Managed identity, DefaultAzureCredential, Azure-to-Azure auth, replacing service principals, app access to Key Vault/Storage/SQL/Service Bus/App Configuration/ACR | [Managed identity](./references/managed-identity.md) | Choosing system-assigned vs user-assigned identity, removing stored credentials, assigning data-plane roles, and documenting local dev auth. |
| Azure RBAC, least privilege, role assignments, control plane vs data plane, operator access, custom roles, broad inherited permissions | [RBAC least privilege](./references/rbac-least-privilege.md) | Selecting exact roles, scopes, and identity separation for runtime, deployment, human operators, and support. |
| Secrets in code/config/pipelines/docs/logs, secret classes, CI/CD bootstrap, local dev secrets, rotation ownership, sample files | [Secret management](./references/secret-management.md) | Discovering, externalizing, eliminating, rotating, and documenting secrets without exposing values. |
| OWASP Top 10, security review, go/no-go, CodeQL, GHAS, secret scanning, dependency findings, SSRF, auth bypass, injection, logging gaps | [OWASP Top 10 review for Azure migrations](./references/owasp-top10-review.md) | Risk-ranked application and platform security review with Azure-specific evidence, severity, remediation, and validation. |

## How to use

1. Identify the security signal from the current phase, report, code, IaC, or user request.
2. Open only the matching reference files above, plus any cross-cutting reference needed for identities, secrets, or RBAC.
3. Apply the standing rules before generating code, IaC, reports, or recommendations.
4. For migration artifacts, record unresolved security assumptions, exceptions, owners, validation steps, and any user-consent requirement.
5. For production readiness, combine identity, Key Vault, network, RBAC, Defender/compliance, and OWASP references rather than treating one control as sufficient.
