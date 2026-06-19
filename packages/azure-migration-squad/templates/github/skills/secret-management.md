# Secret Management

Use this skill when handling secrets, certificates, connection strings, signing keys, or sensitive configuration across application code, infrastructure, and CI/CD.

## Use Cases

Apply this skill when the solution needs:

- migration of secrets out of source control, config files, deployment manifests, or pipelines
- clear separation between development secrets, build-time bootstrap secrets, and production runtime secrets
- Key Vault integration for App Service, Container Apps, Functions, AKS, or VMs
- rotation planning for passwords, API keys, certificates, and connection strings
- validation that documentation, logs, templates, and reports do not expose secret values

## Core Rule

Do not store production secrets in code, checked-in config, or long-lived pipeline variables.

Prefer this order:

1. remove the secret entirely through managed identity or Entra auth when possible
2. store the secret in Azure Key Vault when it must still exist
3. use local developer secret stores for non-production development values

## Secret Classes

| Secret Type | Preferred Target | Notes |
|---|---|---|
| App runtime secret | Azure Key Vault | inject by reference or SDK |
| Database credential that cannot yet be removed | Azure Key Vault | document rotation and removal plan |
| TLS certificate | Key Vault certificate or platform-managed cert | central lifecycle preferred |
| Pipeline credential | OIDC / federated identity first | use secret store only when federation is unavailable |
| Local development secret | user secrets / local `.env` outside source control | never production value |

## Default Storage Pattern

| Environment | Recommended Store | Guidance |
|---|---|---|
| Production | Azure Key Vault | RBAC, diagnostics, rotation ownership |
| Non-production shared env | Azure Key Vault | keep parity with prod where practical |
| CI/CD bootstrap | federated identity or pipeline secret store | only for deployment bootstrap |
| Local development | developer secret store | keep outside git and sample files |

## Migration Pattern

Move secret handling in this order:

1. discover every secret source in code, config, scripts, containers, and pipelines
2. classify whether each secret can be removed, externalized, or temporarily retained
3. replace plaintext config with logical setting names and Key Vault references
4. switch Azure-to-Azure auth to managed identity wherever supported
5. define rotation owner, cadence, and validation steps
6. remove old secret copies from runtime settings, scripts, and docs

## Placement Guide

| Legacy Pattern | Better Target |
|---|---|
| connection string in `appsettings.json` or `web.config` | Key Vault secret reference |
| storage account key in code | managed identity + RBAC |
| API key in pipeline variable copied into app settings | Key Vault secret plus runtime reference |
| checked-in `.env` with real values | `.env.example` + local secret store |
| certificate copied manually to each host | Key Vault certificate or managed platform cert |

## CI/CD Baseline

Pipelines should bootstrap access, not become the long-term secret store.

Preferred model:

- use OIDC or workload identity federation for Azure login
- let deployment tools reference Key Vault or assign managed identity
- keep only the minimum bootstrap values in pipeline secret storage when federation is impossible
- never echo secret values to logs, artifacts, or approval notes

## Documentation and Template Rules

Safe documentation includes:

- secret names
- expected source system
- owner
- rotation cadence
- reference pattern examples without real values

Unsafe documentation includes:

- copied secret values
- full production connection strings
- private keys or certificates in markdown, scripts, or screenshots
- sample files that silently contain live credentials

## Rotation Patterns

Choose the right rotation model explicitly.

| Secret Type | Preferred Rotation Pattern | Notes |
|---|---|---|
| Database password | staged rotation with validation window | keep rollback plan |
| External API key | dual-key or overlapping-validity rotation | avoid hard cutover |
| Certificate | renew before expiry and validate installation target | track issuer and SANs |
| Storage/service credential | replace with managed identity | removal is best rotation |

Operational rules:

- define owner and review cadence
- alert before expiry, not after failure
- test secret refresh behavior before relying on seamless rotation
- remove superseded secret copies after cutover

## Logging and Exposure Controls

Never allow secrets in:

- application logs
- console output
- CI/CD logs
- crash dumps or support bundles when avoidable
- generated reports committed to git

Mask sensitive values and sanitize diagnostics before storing or sharing them.

## Anti-Patterns

Treat these as findings:

- committing secrets or certificates to git, even in sample files
- storing secrets in ARM/Bicep/Terraform parameters committed with live values
- copying Key Vault secrets into app settings when direct references would work
- keeping the same secret in code, pipeline, Key Vault, and docs at once
- using production secrets for local development
- rotating secrets without validation, ownership, or rollback planning

## Validation Checklist

- repository files and templates contain no live secret values
- every production secret is removed or externalized to Key Vault
- Azure-to-Azure access uses managed identity where supported
- pipeline auth uses federation or minimal bootstrap secrets only
- docs and sample files reference secret names, not values
- rotation owner, cadence, and validation steps are documented
- logging and diagnostics paths were reviewed for secret leakage

## Output Expectations for Prompts

When this skill is applied, the prompt should:

- identify every secret source that must be removed, externalized, or eliminated
- recommend Key Vault, managed identity, or local secret-store patterns explicitly
- separate runtime secret handling from CI/CD bootstrap handling
- document rotation, expiry, and ownership expectations
- flag any secret-in-code, secret-in-config, or secret-in-pipeline pattern as remediation work
