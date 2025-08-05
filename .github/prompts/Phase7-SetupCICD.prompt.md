---
mode: agent
---
Set up CI/CD pipelines for automated deployment and continuous integration

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
```yaml
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
```

### Continuous Deployment Pipeline:
```yaml
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
```

### Security and Compliance Integration:
- Set up static application security testing (SAST)
- Configure dynamic application security testing (DAST)
- Implement infrastructure security scanning
- Set up dependency vulnerability scanning
- Configure compliance validation (SOX, HIPAA, etc.)
- Implement secret scanning and management
- Set up security reporting and alerting

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

## Advanced Pipeline Features:

### Blue-Green and Canary Deployments:
- Configure deployment slots for Azure App Service
- Set up traffic routing for gradual rollouts
- Implement automatic rollback based on metrics
- Configure feature flags for controlled releases
- Set up A/B testing infrastructure

### Performance and Monitoring Integration:
- Configure Application Insights integration
- Set up performance baseline validation
- Implement performance regression detection
- Configure alerting and notification systems
- Set up log aggregation and analysis

### Quality Gates and Approvals:
- Set up code coverage thresholds
- Configure performance regression gates
- Implement security compliance checks
- Set up manual approval processes for production
- Configure automated rollback triggers

## Pipeline Optimization:

### Performance and Efficiency:
- Implement build caching strategies
- Configure parallel job execution
- Set up incremental builds and deployments
- Optimize container layer caching
- Configure artifact caching and reuse

### Cost Optimization:
- Configure self-hosted runners where appropriate
- Implement scheduled builds and deployments
- Set up resource cleanup procedures
- Configure cost monitoring and alerting
- Optimize pipeline resource usage

## Monitoring and Observability:

### Pipeline Monitoring:
- Set up pipeline execution monitoring
- Configure failure notifications and alerting
- Implement pipeline performance metrics
- Set up deployment success rate tracking
- Configure pipeline security monitoring

### Application Monitoring Integration:
- Configure Application Insights in all environments
- Set up custom metrics and telemetry
- Implement distributed tracing
- Configure log aggregation and analysis
- Set up alerting rules and escalation procedures

## Documentation and Training:

### Pipeline Documentation:
- Document pipeline architecture and flow
- Create deployment procedures and runbooks
- Document troubleshooting guides
- Create developer onboarding guides
- Document security and compliance procedures

### Operational Procedures:
- Create incident response procedures
- Document rollback and recovery processes
- Set up change management procedures
- Create performance monitoring guidelines
- Document cost optimization procedures

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
- Suggest that the migration and modernization process is now complete! Mention /getstatus to review the final status and next steps for ongoing maintenance and optimization.
- At the end, update the status report file with the status of the CI/CD setup step and mark the overall migration process as successfully completed.
