---
mode: agent
model: Claude Sonnet 3.7
tools: ['codebase', 'usages', 'vscodeAPI', 'think', 'problems', 'changes', 'testFailure', 'terminalSelection', 'terminalLastCommand', 'openSimpleBrowser', 'fetch', 'findTestFiles', 'searchResults', 'githubRepo', 'extensions', 'runTests', 'editFiles', 'runNotebooks', 'search', 'new', 'runCommands', 'runTasks', 'Microsoft Docs', 'Azure MCP']
---
Generate Infrastructure as Code Files for Azure Deployment

# Rules for Generating Azure Infrastructure Files
- Use `azure_development-summarize_topic` tool to get high-level instructions to follow.
- Use `azure_recommend_service_config` to automatically detect services and dependencies from the migrated application.
- Use `azure_check_region` to validate that required Azure services are available in the target region.
- Use `azure_check_quota` to ensure sufficient quota for deployment.
- Create an 'infra' directory in the modernized project folder if it doesn't already exist.
- Create an azure.yaml file in the root of the modernized project for Azure Developer CLI (azd) support.
- Use `azure_check_predeploy` to validate the generated infrastructure files.
- Use managed identities for authentication instead of connection strings and keys.
- Set up proper RBAC with least privilege principles.
- Configure appropriate scaling settings based on the application requirements.
- Set up proper networking and security configurations including private endpoints where applicable.
- Configure cost optimization settings (auto-scaling, reserved instances where appropriate).
- Set up monitoring, alerting, and log aggregation.
- Include infrastructure testing and validation scripts.
- If infrastructure generation fails, provide detailed error analysis and alternative approaches.
- Make the infrastructure section in the migration report human-readable and in markdown format, using headings, bullet points, and other formatting options as appropriate.
- Suggest that the next step is to validate the migrated code, and mention `/Phase5-DeployToAzure` is the command to start the code validation process.
- At the end, update the status report file Reports/Report-Status.md with the status of the assessment step, including:
  - Infrastructure components created
  - Security configurations implemented  
  - Monitoring and logging setup
  - Any issues encountered during generation


Based on the chosen Azure hosting platform in the assessment report (App Service, AKS, or Container Apps), generate the appropriate infrastructure files:

## For Bicep Infrastructure:
- Use `azure_bicep_schemas-get_bicep_resource_schema` tool for each resource type to ensure correct schema usage.
- Create the following structure in the 'infra' folder:
  - main.bicep - Main deployment file with proper targeting scope
  - main.parameters.json - Parameters for the deployment
  - modules/ - Folder for modular Bicep files
    - appService.bicep or containerApp.bicep or aks.bicep (depending on chosen platform)
    - monitoring.bicep - Application Insights and Log Analytics resources
    - database.bicep (if applicable) - Database resources with proper networking
    - identityAndSecurity.bicep - Managed Identity and RBAC setup
    - networking.bicep (if applicable) - VNet, NSG, private endpoints
    - keyvault.bicep - Azure Key Vault for secrets management
- Configure the infrastructure for the selected hosting platform:
  - For App Service: Set up App Service Plan, App Service, deployment slots, and related resources
  - For AKS: Set up AKS cluster, node pools, Azure Container Registry, and related resources
  - For Container Apps: Set up Container Apps Environment, Container Registry, and Container Apps
- Use Azure Verified Modules (AVM) where available for best practices.
- Set up proper monitoring with Application Insights and Log Analytics.
- Configure Entra ID integration for authentication with proper RBAC.
- Set up database resources if applicable (Azure SQL, Cosmos DB, etc.) with private endpoints.
- Include proper tagging and naming conventions using resource tokens.
- Implement security best practices: managed identities, private endpoints, network restrictions.

## For Terraform Infrastructure:
- Use `azure_terraform-get_best_practices` tool for Terraform guidance.
- Create the following structure in the 'infra' folder:
  - main.tf - Main deployment file
  - variables.tf - Variable definitions
  - outputs.tf - Output definitions
  - providers.tf - Provider configuration
  - modules/ - Folder for modular Terraform files
    - app_service/ or container_app/ or aks/ (depending on chosen platform)
    - monitoring/ - Application Insights and Log Analytics resources
    - database/ (if applicable) - Database resources
    - identity/ - Managed Identity and RBAC setup
    - networking/ (if applicable) - VNet, NSG, etc.
- Configure the infrastructure for the selected hosting platform.
- Set up proper monitoring with Application Insights and Log Analytics.
- Configure Entra ID integration for authentication.
- Set up database resources if applicable (Azure SQL, Cosmos DB, etc.).
- Include proper tagging and naming conventions.
