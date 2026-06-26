---
name: Phase5-SetupCICD
description: Configure GitHub Actions or Azure DevOps pipelines for automated deployment
argument-hint: "Specify CI/CD platform, e.g., 'Setup GitHub Actions' or 'Configure Azure DevOps pipelines'"
agent: Code Migration Modernization Agent
model: Claude Sonnet 4.6 (copilot)
---





<!-- BEGIN: capability-matrix-gate (auto-managed by inject-capability-matrix-gates.mjs) -->

## 🚦 MANDATORY OPENING CHECK — Capability Matrix Required

**Before doing ANY work for Phase 5 — Setup CI/CD, verify the Discovery contract:**

| Required artifact | Location | If missing |
|-------------------|----------|------------|
| Discovery Dossier | `reports/Discovery-Dossier.md` | **STOP** — run `/assess-any-application` first |
| Capability Matrix | `reports/Capability-Matrix.yaml` | **STOP** — run `/assess-any-application` first |
| Approved Migration Plan | `reports/Migration-Plan.md` | **STOP** — run `/build-migration-plan` |

### If ANY of those three artifacts is missing

Reply with exactly:

```
🚨 Phase 5 — Setup CI/CD cannot proceed without the Discovery contract.

Missing artifacts:
  - reports/Discovery-Dossier.md          [missing/present]
  - reports/Capability-Matrix.yaml         [missing/present]
  - reports/Migration-Plan.md              [missing/present]

Required steps before re-running this phase:
  1. Open Copilot Chat → /assess-any-application  (or in CLI: "assess this application")
  2. Then: /build-migration-plan                  (or in CLI: "build the migration plan")
  3. Then: /phase...

To override (skip Discovery and accept risk), log a waiver entry in
reports/Decision-Log.md with `Waiver: skip-discovery=<reason>` and re-invoke
this prompt with the `--accept-risk` natural-language flag in your request.
```

**Do NOT proceed past this gate unless:**
- All three artifacts exist, OR
- A waiver entry exists in `reports/Decision-Log.md` AND the user explicitly said "skip discovery" or similar

### When the gate passes

1. Read `reports/Capability-Matrix.yaml` and extract these fields you must honor:
   - `source.primary_adapter` → load the matching `source-*` skill
   - `stack.primary_stack` + `stack.secondary_stacks` → load matching `stack-*` skills
   - `workload.primary_pattern` → load matching `workload-*` skill
   - `migration_strategy.recommendation` → adjust phase emphasis based on the recommended strategy
   - `risk_flags` → load the matching risk skills (e.g., `risk-cross-region-data.md`)
   - `unresolved_questions` → if any remain unanswered, surface them BEFORE starting work
2. Read `reports/Migration-Plan.md` for approved sequencing and any app-specific extra gates.
3. Confirm Phase prerequisites are met.

<!-- END: capability-matrix-gate -->
Set up CI/CD pipelines for automated deployment and continuous integration

## Preconditions

Before configuring CI/CD, verify Phase 4 (Deployment to Azure) is complete:

1. Check `reports/Report-Status.md` shows **Phase 4: Deployment to Azure** as ✅ complete.
2. Confirm `reports/Deployment-Summary-Report.md` exists with the deployment outcome.
3. If preconditions are not met, **STOP** and ask the user to run `/Phase4-DeployToAzure` first.

# Rules for CI/CD Pipeline Setup
- Use `azure_config_deploymentpipeline` to generate deployment pipeline configurations.
- Use `file_search` to locate existing pipeline files and understand current CI/CD setup.
- Use `semantic_search` to identify deployment requirements from the application structure.
- Set up comprehensive CI/CD pipelines that support the target Azure platform and hosting approach.
- Create pipeline configurations that follow Azure DevOps and GitHub Actions best practices.

## CI/CD Strategy Implementation

### Pipeline Platform Selection:
- Determine whether to use GitHub Actions, Azure DevOps, or both
- Consider existing organizational preferences and integrations
- Evaluate security and compliance requirements
- Set up service connections and authentication

### For GitHub Actions:
- Create `.github/workflows/` directory structure
- Set up workflow files for:
  - Continuous Integration (CI) pipeline
  - Continuous Deployment (CD) pipeline
  - Infrastructure deployment pipeline
  - Security scanning pipeline
- Configure GitHub secrets for Azure authentication
- Set up environment protection rules
- Configure branch protection policies

### For Azure DevOps:
- Create Azure DevOps project and repository connections
- Set up build pipelines (azure-pipelines.yml)
- Configure release pipelines for deployment
- Set up service connections to Azure
- Configure variable groups and secure variables
- Set up approval processes and gates

## Pipeline Configuration Details

### Continuous Integration Pipeline:
# Include the following stages:
- Source code checkout and caching
- Dependency installation and caching
- Code quality analysis (SonarQube, ESLint, etc.)
- Security scanning (Snyk, OWASP dependency check)
- Unit test execution with coverage reporting
- Integration test execution
- Application build and packaging
- Container image build and security scanning (if applicable)
- Artifact publishing to registry
- Infrastructure validation (Bicep/Terraform linting)

### Continuous Deployment Pipeline:
# Include the following stages:
- Environment-specific configuration
- Infrastructure deployment (using azd or direct ARM/Bicep)
- Application deployment to staging environment
- Smoke tests and health checks
- Integration tests against staging
- Security tests and compliance validation
- Performance tests and baseline validation
- Production deployment with approval gates
- Post-deployment validation and monitoring
- Rollback procedures in case of failures

## Environment Management:

### Multi-Environment Setup:
- Configure development, staging, and production environments
- Set up environment-specific configurations and secrets
- Implement environment promotion strategies
- Configure environment isolation and security
- Set up monitoring and logging for each environment

### Infrastructure as Code Integration:
- Integrate Bicep/Terraform deployment in pipelines
- Set up infrastructure validation and testing
- Configure infrastructure drift detection
- Implement infrastructure rollback procedures
- Set up infrastructure security scanning

## Deliverables:

- Generate a CI/CD setup report in the 'reports' folder, named 'cicd_setup_report.md', including:
  - Pipeline architecture and configuration details
  - Environment setup and management procedures
  - Security and compliance integration
  - Quality gates and approval processes
  - Monitoring and observability setup
  - Performance optimization configurations
  - Operational procedures and troubleshooting guides
  - Cost optimization strategies
  - Training and documentation resources

- Create actual pipeline configuration files in the appropriate directories:
  - `.github/workflows/` for GitHub Actions
  - `azure-pipelines.yml` for Azure DevOps
  - Environment-specific configuration files
  - Security scanning configurations

- If CI/CD setup fails at any step, provide detailed error analysis and alternative approaches.
- Make the CI/CD report human-readable and in markdown format with clear sections and actionable guidance.
- Suggest that the migration and modernization process is now complete! Mention `/GetStatus` to review the final status and next steps for ongoing maintenance and optimization.
- At the end, update the status report file reports/Report-Status.md with the status of the CI/CD step and mark the overall migration process as successfully completed.

## Next Steps

When CI/CD setup is complete:

1. ✅ Update `reports/Report-Status.md` to mark **Phase 5: CI/CD Setup** as complete and the overall migration as successfully completed.
2. 🎉 Output the following completion block to the user:

   > **🎉 Migration Complete!**
   >
   > The migration and modernization process is now complete.
   >
   > 📋 Run **`/GetStatus`** to review the final status and recommended ongoing maintenance.
