---
mode: agent
---
Generate Infrastructure as Code Files for Azure Deployment

# Rules for Generating Azure Infrastructure Files
- Use `azure_development-get_deployment_best_practices` tool to get high-level instructions to follow.
- Create an 'infra' directory in the modernized project folder if it doesn't already exist.
- Based on the chosen Azure hosting platform in the assessment report (App Service, AKS, or Container Apps), generate the appropriate infrastructure files:

## For Bicep Infrastructure:
- Use `azure_bicep_schemas-get_bicep_resource_schema` tool to help create Bicep files.
- Create the following structure in the 'infra' folder:
  - main.bicep - Main deployment file
  - main.parameters.json - Parameters for the deployment
  - modules/ - Folder for modular Bicep files
    - appService.bicep or containerApp.bicep or aks.bicep (depending on chosen platform)
    - monitoring.bicep - Application Insights and Log Analytics resources
    - database.bicep (if applicable) - Database resources
    - identityAndSecurity.bicep - Managed Identity and RBAC setup
    - networking.bicep (if applicable) - VNet, NSG, etc.
- Configure the infrastructure for the selected hosting platform:
  - For App Service: Set up App Service Plan, App Service, and related resources
  - For AKS: Set up AKS cluster, node pools, and related resources
  - For Container Apps: Set up Container Apps Environment, Container Registry, and Container Apps
- Set up proper monitoring with Application Insights and Log Analytics.
- Configure Entra ID integration for authentication.
- Set up database resources if applicable (Azure SQL, Cosmos DB, etc.).
- Include proper tagging and naming conventions.

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

## General Requirements:
- Create an azure.yaml file in the root of the modernized project for Azure Developer CLI (azd) support.
- Use managed identities for authentication instead of connection strings and keys.
- Set up proper RBAC with least privilege principles.
- Configure appropriate scaling settings based on the application requirements.
- Set up proper networking and security configurations.
- Update the migration report in the 'reports' folder with information about the generated infrastructure.
- If you make changes to the infrastructure files, ensure these changes are documented in the migration report.
- Make the infrastructure section in the migration report human-readable and in markdown format, using headings, bullet points, and other formatting options as appropriate.
- Suggest that the next step is to validate the migrated code, and mention /phase4-validatecode is the command to start the code validation process.
- At the end, update the status report file with the status of the infrastructure generation step.
