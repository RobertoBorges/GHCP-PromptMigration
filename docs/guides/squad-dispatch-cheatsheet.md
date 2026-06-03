# Squad Dispatch Cheat Sheet

Use this as the quick reference card for Robert's team when deciding which squad agent should lead a task.

> **Current squad:** Architect, Coder, Tester
>
> **Recommended specialist aliases:**
> - **Azure Specialist** = Cloud Engineer workflow owner; if not available, use Coder with Azure-focused prompts/skills.
> - **Security Auditor** = Security workflow owner; if not available, use a dedicated security review agent/tool plus human review.

## 📋 ASSESSMENT
- `Assess [app] for Azure migration` → **Architect**
- `Quick scan of [repo] for migration complexity` → **Architect**
- `Assess multiple repos listed in codebase-repos.md and recommend migration order` → **Architect**

## 🔧 MIGRATION
- `Migrate [app] from .NET Framework to .NET 8` → **Coder**
- `Convert WCF service to REST API` → **Coder**
- `Upgrade Java 8 to Java 21` → **Coder**
- `Preserve existing behavior while modernizing config and dependencies` → **Coder**

## ☁️ INFRASTRUCTURE
- `Generate Bicep for [app] targeting App Service` → **Azure Specialist**
- `Create Terraform for AKS deployment` → **Azure Specialist**
- `Set up Azure SQL with managed identity` → **Azure Specialist**
- `Prepare azure.yaml and environment parameters for azd` → **Azure Specialist**

## 🚀 DEPLOYMENT
- `Deploy [app] to Azure using azd` → **Azure Specialist**
- `Validate Azure deployment and summarize endpoints, logs, and health` → **Azure Specialist**
- `Set up GitHub Actions CI/CD` → **Coder**
- `Create staged deployment with approvals and rollback guidance` → **Coder**

## 🔒 SECURITY
- `Review [app] migration for security issues` → **Security Auditor**
- `Validate Entra ID and RBAC config` → **Security Auditor**
- `Check for hardcoded secrets` → **Security Auditor**
- `Review Key Vault, managed identity, and network exposure` → **Security Auditor**

## 📊 STATUS
- `What's the migration status?` → **Tester/DevRel**
- `Generate a status dashboard` → **Tester/DevRel**
- `Update docs for Phase 3 completion` → **Tester/DevRel**
- `Summarize blockers and recommend the next phase owner` → **Tester/DevRel**

## 🐛 DEBUG
- `Build is failing after migration` → **Coder**
- `Deployment failed with error X` → **Azure Specialist**
- `Tests are failing after code migration` → **Tester**
- `The status report and artifacts disagree` → **Tester/DevRel**

## Recommended Command Sequence
1. `/phase0-multirepoassessment` for portfolio discovery
2. `/phase1-planandassess` for app-level decisions
3. `/phase2-migratecode` for modernization
4. `/phase3-generateinfra` for Azure IaC
5. `/phase4-deploytoazure` for environment validation
6. `/phase5-setupcicd` for repeatable delivery
7. `/getstatus` after every phase boundary

## Fast Routing Rules
- **Need scope, sequencing, or go/no-go?** Use **Architect**.
- **Need code changed or pipelines built?** Use **Coder**.
- **Need status, docs, or release readiness?** Use **Tester/DevRel**.
- **Need Azure resources or deployment help?** Use **Azure Specialist**.
- **Need security sign-off?** Use **Security Auditor**.

## Fallback Mapping When Only the Fast Squad Exists
| Needed function | Use this now |
|-----------------|--------------|
| Azure Specialist | Coder + Azure prompts/skills + Architect review |
| Security Auditor | Tester + security review tooling + human security approval |
| QA Engineer | Tester |
| DevOps Engineer | Coder |
