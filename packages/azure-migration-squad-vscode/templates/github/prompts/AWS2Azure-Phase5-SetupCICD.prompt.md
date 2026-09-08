---
name: Phase5-SetupCICD
description: Migrate CI/CD from AWS CodePipeline/CodeBuild to GitHub Actions or Azure DevOps
argument-hint: "Specify CI/CD platform, e.g., 'Migrate to GitHub Actions' or 'Set up Azure DevOps pipelines'"
agent: AWS to Azure Migration Agent
---

Migrate CI/CD Pipelines from AWS to GitHub Actions or Azure DevOps

# Rules for CI/CD Pipeline Migration
- Use `azure_config_deploymentpipeline` to generate deployment pipeline configurations.
- Use `file_search` to locate existing pipeline files and understand current CI/CD setup.
- Use `semantic_search` to identify deployment requirements from the application structure.
- Set up comprehensive CI/CD pipelines that support the target Azure platform and hosting approach.
- Create pipeline configurations that follow Azure DevOps and GitHub Actions best practices.

## 1. Detect Current AWS CI/CD

Scan the repository and project for existing AWS CI/CD configurations:
- **CodePipeline**: Look for pipeline definitions in CloudFormation templates (`AWS::CodePipeline::Pipeline`), CDK constructs, or JSON/YAML pipeline definitions
- **CodeBuild**: Scan for `buildspec.yml` or `buildspec.yaml` files (build specifications)
- **CodeDeploy**: Scan for `appspec.yml` or `appspec.yaml` files (deployment specifications)
- **CodeCommit**: Check for CodeCommit repository references in pipeline definitions or git remotes
- **CodeArtifact**: Check for CodeArtifact repository references in build configurations or package manager settings (`.npmrc`, `pip.conf`, `settings.xml`)
- **ECR**: Detect container image push/pull references to ECR registries
- **Existing GitHub Actions**: Check `.github/workflows/` for any workflows already in use
- **Other CI/CD**: Check for Jenkins (`Jenkinsfile`), CircleCI (`.circleci/`), Travis CI (`.travis.yml`), or other CI/CD already in use

## 2. Migration Mapping

Map AWS CI/CD components to their Azure/GitHub equivalents:

| AWS CI/CD Component | Azure/GitHub Equivalent |
|---------------------|------------------------|
| CodePipeline | GitHub Actions workflows / Azure DevOps Pipelines |
| CodeBuild `buildspec.yml` | GitHub Actions steps / Azure Pipelines tasks |
| CodeDeploy `appspec.yml` | `azd deploy` / Azure deployment strategies |
| CodeCommit | GitHub repository (already using if here) |
| CodeArtifact | GitHub Packages / Azure Artifacts |
| ECR image push/pull | ACR image push/pull |
| CodePipeline approvals | GitHub Environment protection rules / Azure DevOps approval gates |
| CodeBuild environment variables | GitHub Actions secrets/variables / Azure DevOps variable groups |
| CodePipeline artifacts (S3) | GitHub Actions artifacts / Azure DevOps artifacts |
| CodeStar Notifications | GitHub Actions notifications / Azure DevOps notifications |

## 3. For GitHub Actions

### Azure Authentication (OIDC — NO secrets)
- Set up OIDC federated credentials between GitHub and Azure (no client secrets)
- Use `azure/login@v2` action with OIDC
- Configure `AZURE_CLIENT_ID`, `AZURE_TENANT_ID`, `AZURE_SUBSCRIPTION_ID` as GitHub repository variables
- Do NOT store Azure credentials as GitHub secrets — use federated identity

### Pipeline Structure
Create `.github/workflows/` directory structure with the following workflows:

#### CI Workflow (`ci.yml`):
- Source code checkout and caching
- Dependency installation and caching
- Code quality analysis (SonarQube, ESLint, etc.)
- Security scanning (Snyk, OWASP dependency check, Trivy for containers)
- Unit test execution with coverage reporting
- Integration test execution
- Application build and packaging
- Container image build and push to ACR (if applicable)
- Artifact publishing
- Bicep/Terraform validation and linting (`az bicep build` or `terraform validate`)

#### CD Workflow (`cd.yml`):
- Azure login via OIDC federated credentials
- `azd provision` — deploy/update infrastructure
- `azd deploy` — deploy application
- Smoke tests and health checks
- Post-deployment validation

#### Infrastructure Workflow (`infra.yml`):
- Bicep/Terraform plan on pull requests (review infrastructure changes)
- Bicep/Terraform apply on merge to main
- Infrastructure drift detection (scheduled)

#### Security Scanning Workflow (`security.yml`):
- Dependency vulnerability scanning
- Container image scanning (Trivy/Snyk)
- Infrastructure security scanning (Checkov, tfsec)
- Secret scanning

### Migrate buildspec.yml → GitHub Actions Steps
- Convert `phases.install.commands` → setup/install steps
- Convert `phases.pre_build.commands` → pre-build steps
- Convert `phases.build.commands` → build steps
- Convert `phases.post_build.commands` → post-build steps
- Convert `artifacts` section → `actions/upload-artifact`
- Convert environment variables → GitHub Actions env/secrets

### Environment Protection Rules
- Set up environment protection rules for staging and production
- Require approvals for production deployments
- Configure branch protection policies

## 4. For Azure DevOps

### Azure Service Connections
- Create Azure Resource Manager service connections (use workload identity federation, not service principal secrets)
- Configure service connection permissions

### Pipeline Structure
- Create `azure-pipelines.yml` for the main pipeline
- Set up build pipelines with stages equivalent to CodeBuild `buildspec.yml`
- Configure release pipelines for deployment using `azd`
- Container build and push to ACR
- Bicep/Terraform validation and deployment

### Variable Groups and Security
- Configure variable groups for environment-specific settings
- Use Azure Key Vault-linked variable groups for secrets
- Set up approval processes and gates for production

## 5. Quality Gates and Environment Management

### Quality Gates (keep from existing CI/CD or add):
- Code coverage thresholds
- Security scan pass/fail criteria
- Performance test baselines
- Approval gates for production

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

## Deliverables

- Generate a CI/CD setup report at `reports/cicd_setup_report.md`, including:
  - AWS CI/CD components detected and migrated
  - Migration mapping (what was converted and how)
  - Pipeline architecture and configuration details
  - Azure authentication setup (OIDC federated credentials)
  - Environment setup and management procedures
  - Security and compliance integration
  - Quality gates and approval processes
  - Monitoring and observability setup
  - Operational procedures and troubleshooting guides

- Create actual pipeline configuration files in the appropriate directories:
  - `.github/workflows/` for GitHub Actions
  - `azure-pipelines.yml` for Azure DevOps
  - Environment-specific configuration files
  - Security scanning configurations

- If CI/CD migration fails at any step, provide detailed error analysis and alternative approaches.
- Make the CI/CD report human-readable and in markdown format with clear sections and actionable guidance.

The AWS-to-Azure migration process is now complete! Mention `/AWS2Azure-getstatus` to review the final migration status and next steps for ongoing maintenance and optimization.

At the end, update the status report file `reports/Report-Status.md` with the status of the CI/CD migration step and mark the overall AWS-to-Azure migration process as successfully completed.
