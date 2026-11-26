# Skill Inventory Index

This index maps native Agent Skills, prompt reference material, and the human-facing reference catalog.

## Layer Contract

- `.github/skills/<name>/SKILL.md` = **discoverable Agent Skills**
- Flat `.github/skills/*.md` = **explicit prompt reference material** (schemas, adapters, templates, and playbooks)
- `skills/` = **reference-only catalog** for onboarding, examples, and broader knowledge
- Prompts and chatmodes should reference **only** `.github/skills/`; the extension does not ship root `skills/`

## Snapshot

- Root `skills/`: **26** skill files + `README.md` + `INDEX.md`
- `.github/skills/`: **72** flat reference files and **9** `SKILL.md` directories
- Shared skill names: **22**
- Root-only reference skills: **4**
- `.github/skills/`-only skills: **6**
- Prompt/chatmode audit: **0** root `skills/` paths or missing hook-document references

## Root skills with `.github/skills/` counterparts

| Root skill | Authoritative prompt path | Status |
|---|---|---|
| `asp-classic-to-dotnet.md` | `.github/skills/asp-classic-to-dotnet.md` | Had an identical body before labeling; root file now marked `REFERENCE ONLY` |
| `azd-configuration.md` | `.github/skills/azd-configuration.md` | Prompt copy promoted; root remains reference-only |
| `azure-aks.md` | `.github/skills/azure-aks.md` | Prompt copy promoted; root remains reference-only |
| `azure-app-service.md` | `.github/skills/azure-app-service.md` | Counterpart exists; `.github/skills/` remains authoritative |
| `azure-container-apps.md` | `.github/skills/azure-container-apps.md` | Had an identical body before labeling; root file now marked `REFERENCE ONLY` |
| `azure-entra-id.md` | `.github/skills/azure-entra-id.md` | Counterpart exists; `.github/skills/` remains authoritative |
| `azure-monitor-appinsights.md` | `.github/skills/azure-monitor-appinsights.md` | Prompt copy promoted; root remains reference-only |
| `bicep-modules.md` | `.github/skills/bicep-modules.md` | Counterpart exists; `.github/skills/` remains authoritative |
| `config-transformation.md` | `.github/skills/config-transformation.md` | Counterpart exists; `.github/skills/` remains authoritative |
| `cost-optimization.md` | `.github/skills/cost-optimization.md` | Prompt copy promoted; root remains reference-only |
| `docker-containerize.md` | `.github/skills/docker-containerize.md` | Had an identical body before labeling; root file now marked `REFERENCE ONLY` |
| `dotnet-framework-to-dotnet8.md` | `.github/skills/dotnet-framework-to-dotnet8.md` | Counterpart exists; `.github/skills/` remains authoritative |
| `ef-migration.md` | `.github/skills/ef-migration.md` | Counterpart exists; `.github/skills/` remains authoritative |
| `java8-to-java21.md` | `.github/skills/java8-to-java21.md` | Counterpart exists; `.github/skills/` remains authoritative |
| `managed-identity.md` | `.github/skills/managed-identity.md` | Counterpart exists; `.github/skills/` remains authoritative |
| `migration-report-template.md` | `.github/skills/migration-report-template.md` | Had an identical body before labeling; root file now marked `REFERENCE ONLY` |
| `rbac-least-privilege.md` | `.github/skills/rbac-least-privilege.md` | Counterpart exists; `.github/skills/` remains authoritative |
| `rollback-strategy.md` | `.github/skills/rollback-strategy.md` | Counterpart exists; `.github/skills/` remains authoritative |
| `secret-management.md` | `.github/skills/secret-management.md` | Counterpart exists; `.github/skills/` remains authoritative |
| `terraform-azure.md` | `.github/skills/terraform-azure.md` | Prompt copy promoted; root remains reference-only |
| `wcf-to-rest-api.md` | `.github/skills/wcf-to-rest-api.md` | Counterpart exists; `.github/skills/` remains authoritative |
| `webforms-to-razor.md` | `.github/skills/webforms-to-razor.md` | Counterpart exists; `.github/skills/` remains authoritative |

## Root-only reference skills

| Root skill | Status |
|---|---|
| `azure-devops-pipelines.md` | Reference catalog only |
| `azure-key-vault.md` | Reference catalog only |
| `azure-sql-migration.md` | Reference catalog only |
| `github-actions-cicd.md` | Reference catalog only |

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

- Root reference scan: search `.github/prompts/` and `.github/chatmodes/` for `#file:skills/`
- Prompt reference scan: verify all `#file:.github/skills/` paths exist and are included in extension templates

Interpretation: matches should resolve to `.github/skills/`; any direct prompt reference to root `skills/` is a regression.
