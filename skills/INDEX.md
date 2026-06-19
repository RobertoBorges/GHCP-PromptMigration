# Skill Inventory Index

This index maps the two skill layers and removes ambiguity about which folder prompts should use.

## Layer Contract

- `.github/skills/` = **authoritative prompt-local skills**
- `skills/` = **reference-only catalog** for onboarding, examples, and broader knowledge
- Prompts under `.github/prompts/` should reference **only** `.github/skills/`

## Snapshot

- Root `skills/`: **26** skill files + `README.md` + `INDEX.md`
- `.github/skills/`: **23** skill files
- Shared skill names: **17**
- Root-only reference skills: **9**
- `.github/skills/`-only skills: **6**
- Prompt audit: **0** root `skills/` references found under `.github/prompts/`

## Root skills with `.github/skills/` counterparts

| Root skill | Authoritative prompt path | Status |
|---|---|---|
| `asp-classic-to-dotnet.md` | `.github/skills/asp-classic-to-dotnet.md` | Had an identical body before labeling; root file now marked `REFERENCE ONLY` |
| `azure-app-service.md` | `.github/skills/azure-app-service.md` | Counterpart exists; `.github/skills/` remains authoritative |
| `azure-container-apps.md` | `.github/skills/azure-container-apps.md` | Had an identical body before labeling; root file now marked `REFERENCE ONLY` |
| `azure-entra-id.md` | `.github/skills/azure-entra-id.md` | Counterpart exists; `.github/skills/` remains authoritative |
| `bicep-modules.md` | `.github/skills/bicep-modules.md` | Counterpart exists; `.github/skills/` remains authoritative |
| `config-transformation.md` | `.github/skills/config-transformation.md` | Counterpart exists; `.github/skills/` remains authoritative |
| `docker-containerize.md` | `.github/skills/docker-containerize.md` | Had an identical body before labeling; root file now marked `REFERENCE ONLY` |
| `dotnet-framework-to-dotnet8.md` | `.github/skills/dotnet-framework-to-dotnet8.md` | Counterpart exists; `.github/skills/` remains authoritative |
| `ef-migration.md` | `.github/skills/ef-migration.md` | Counterpart exists; `.github/skills/` remains authoritative |
| `java8-to-java21.md` | `.github/skills/java8-to-java21.md` | Counterpart exists; `.github/skills/` remains authoritative |
| `managed-identity.md` | `.github/skills/managed-identity.md` | Counterpart exists; `.github/skills/` remains authoritative |
| `migration-report-template.md` | `.github/skills/migration-report-template.md` | Had an identical body before labeling; root file now marked `REFERENCE ONLY` |
| `rbac-least-privilege.md` | `.github/skills/rbac-least-privilege.md` | Counterpart exists; `.github/skills/` remains authoritative |
| `rollback-strategy.md` | `.github/skills/rollback-strategy.md` | Counterpart exists; `.github/skills/` remains authoritative |
| `secret-management.md` | `.github/skills/secret-management.md` | Counterpart exists; `.github/skills/` remains authoritative |
| `wcf-to-rest-api.md` | `.github/skills/wcf-to-rest-api.md` | Counterpart exists; `.github/skills/` remains authoritative |
| `webforms-to-razor.md` | `.github/skills/webforms-to-razor.md` | Counterpart exists; `.github/skills/` remains authoritative |

## Root-only reference skills

| Root skill | Status |
|---|---|
| `azd-configuration.md` | Reference catalog only |
| `azure-aks.md` | Reference catalog only |
| `azure-devops-pipelines.md` | Reference catalog only |
| `azure-key-vault.md` | Reference catalog only |
| `azure-monitor-appinsights.md` | Reference catalog only |
| `azure-sql-migration.md` | Reference catalog only |
| `cost-optimization.md` | Reference catalog only |
| `github-actions-cicd.md` | Reference catalog only |
| `terraform-azure.md` | Reference catalog only |

## `.github/skills/`-only skills

| Prompt-local skill | Status |
|---|---|
| `azure-defender-compliance.md` | Prompt-local only |
| `azure-keyvault-secrets.md` | Prompt-local only |
| `azure-network-security.md` | Prompt-local only |
| `migration-handoff.md` | Prompt-local only |
| `owasp-top10-review.md` | Prompt-local only |
| `pptx-generation.md` | Prompt-local only |

## Verification Commands

- Root reference scan: `grep -r "skills/" .github/prompts/`
- Authoritative prompt scan: `grep -r "\.github/skills/" .github/prompts/`

Interpretation: matches should resolve to `.github/skills/`; any direct prompt reference to root `skills/` is a regression.
