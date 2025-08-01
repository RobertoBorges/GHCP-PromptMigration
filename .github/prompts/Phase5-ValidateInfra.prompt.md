---
mode: agent
---
Validate infrastructure as code files

# Rules for Validating Infrastructure as Code Files
- Use `azure_development-summarize_topic` to get guidance on validating IaC files.
- Use `azure_check_predeploy` to perform comprehensive infrastructure validation.
- Use `azure_check_region` to validate regional availability of all specified Azure resources.
- Use `azure_check_quota` to ensure sufficient quota for all resources in the target subscription.
- Use `get_errors` to identify syntax and configuration errors in IaC files.
- Validate the infrastructure files in the 'infra' folder against Azure best practices.
- Check that the infrastructure matches the target hosting platform selected during assessment (App Service, AKS, or Container Apps).
- Validate that the IaC files follow these requirements:
- Use `azure_check_predeploy` to perform comprehensive infrastructure validation.
- Use `azure_check_region` to validate regional availability of all specified Azure resources.
- Use `azure_check_quota` to ensure sufficient quota for deployment.
- Validate Azure.yaml file configuration for AZD compatibility.
- Check for infrastructure testing scripts and validation procedures.
- Validate cost estimation and budget considerations.
- Check compliance with organizational policies and governance requirements.
- Generate an infrastructure validation report in the 'reports' folder, named 'infra_validation_report.md', summarizing:
  - Compliance with Azure best practices and Well-Architected Framework
  - Resource configuration correctness with specific recommendations
  - Security considerations and compliance status
  - Scalability configurations and performance expectations
  - Monitoring and logging setup with alerting configurations
  - Cost optimization recommendations and budget estimates
  - Regional availability and quota validation results
  - Any issues found with detailed remediation steps
  - Infrastructure quality score with breakdown by category
  - Deployment readiness assessment

- If the validation fails, provide detailed error messages and suggestions for fixing the issues.
- If the validation passes or has only minor issues, indicate that the infrastructure is ready for deployment.
- Make the validation report human-readable and in markdown format, using headings, bullet points, and other formatting options to make it easy to read.
- Validation state must be one of: Success, Warning (with minor issues), Failed, or Could Not Validate.
- If the validate prompt is called before infrastructure generation has been performed, create a report stating that validation cannot be performed.
- If the user runs Validate again, ask if they want to overwrite the existing report. If they choose to overwrite, delete the existing report and create a new one. If they choose not to overwrite, ask if they want to create the report in a new file instead.
- Suggest that next step is to deploy the application to Azure, and mention /phase6-deploytoazure is the command to start the deployment process.
- At the end, update the status report file with the status of the infrastructure validation step.


## For Bicep Infrastructure:
- Proper modularization with separate files for different resource types
- Use of Azure Verified Modules (AVM) where appropriate
- Proper parameters and variables usage with secure parameter handling
- Correct resource dependencies and deployment ordering
- Secure configuration settings (no hardcoded secrets, proper Key Vault integration)
- Appropriate use of managed identities with proper RBAC assignments
- Proper RBAC setup with least privilege principle
- Monitoring and logging configuration with Application Insights and diagnostic settings
- Networking security configurations (private endpoints, NSGs, firewalls)
- Proper tagging and naming conventions following Azure naming standards
- Cost optimization configurations (appropriate SKUs, auto-scaling settings)
- Disaster recovery and backup configurations
- Compliance with Azure security benchmarks

## For Terraform Infrastructure:
- Proper modularization with separate files for different resource types
- Use of Terraform modules where appropriate
- Proper variables and outputs definitions
- Correct resource dependencies
- Secure configuration settings
- Appropriate use of managed identities
- Proper RBAC setup with least privilege
- Monitoring and logging configuration with Application Insights
- Networking security configurations (if applicable)
- Proper tagging and naming conventions
