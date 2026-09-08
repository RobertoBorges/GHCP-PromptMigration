---
name: Phase3-GenerateInfra
description: Convert CloudFormation/CDK to Bicep or Terraform and generate Azure infrastructure as code
argument-hint: "Specify IaC preference if not set, e.g., 'Convert CloudFormation to Bicep' or 'Generate Terraform for Container Apps'"
agent: AWS to Azure Migration Agent
---

Convert AWS Infrastructure as Code to Azure and Generate Azure Infrastructure Files

Load the **azure-infrastructure** skill for Bicep/Terraform templates and Azure Verified Modules patterns.
Load the **azure-containerization** skill if containerization was selected in the assessment.
Load the **aws-networking-migration** skill for VPC-to-VNet conversion patterns.
Load the **aws-observability-migration** skill for CloudWatch-to-Azure Monitor conversion patterns.

## CloudFormation/CDK → Bicep/Terraform Conversion

### Detect Existing AWS Infrastructure as Code
- Scan for CloudFormation templates: `template.yaml`, `template.json`, `*.cfn.yaml`, `*.cfn.json`, `cloudformation/` directories
- Scan for CDK projects: `cdk.json`, `lib/*.ts`, `lib/*.py`, `cdk.out/`
- Scan for existing Terraform with AWS provider: `*.tf` files referencing `aws_*` resources
- Scan for SAM templates: `template.yaml` with `AWS::Serverless::*` resources

### AWS-to-Azure Resource Mapping
Map each detected AWS resource to its Azure equivalent:

| AWS Resource | Azure Resource |
|-------------|---------------|
| EC2 / ECS / Fargate | App Service / Container Apps / AKS |
| ALB / NLB | Application Gateway / Azure Load Balancer / Front Door |
| RDS (MySQL/PostgreSQL/SQL Server) | Azure Database for MySQL/PostgreSQL / Azure SQL |
| DynamoDB | Cosmos DB |
| S3 | Azure Blob Storage |
| SQS | Azure Service Bus / Azure Queue Storage |
| SNS | Azure Event Grid / Azure Service Bus Topics |
| Lambda | Azure Functions |
| API Gateway | Azure API Management |
| CloudFront | Azure Front Door / Azure CDN |
| Route 53 | Azure DNS |
| IAM Roles/Policies | Managed Identities / Azure RBAC |
| Secrets Manager / SSM Parameter Store | Azure Key Vault |
| CloudWatch | Application Insights / Azure Monitor / Log Analytics |
| VPC / Subnets / Security Groups | VNet / Subnets / NSGs |
| NAT Gateway | Azure NAT Gateway |
| ElastiCache | Azure Cache for Redis |
| Cognito | Entra ID |
| CodePipeline/CodeBuild | GitHub Actions / Azure DevOps |
| ECR | Azure Container Registry |

### CloudFormation → Bicep Conversion Rules
- Convert CloudFormation `Parameters` → Bicep `param` declarations
- Convert CloudFormation `Outputs` → Bicep `output` declarations
- Convert CloudFormation `Mappings` → Bicep variables or parameter files
- Convert CloudFormation `Conditions` → Bicep conditional expressions
- Convert CloudFormation `!Ref` / `!GetAtt` → Bicep resource references
- Convert CloudFormation `!Sub` → Bicep string interpolation
- Convert nested stacks → Bicep modules
- Convert CloudFormation intrinsic functions → Bicep built-in functions

### CloudFormation → Terraform Conversion Rules
- Convert AWS provider resources (`aws_*`) to Azure provider resources (`azurerm_*`)
- Convert `aws_iam_role` → `azurerm_user_assigned_identity` + `azurerm_role_assignment`
- Convert `aws_vpc` → `azurerm_virtual_network`
- Convert `aws_security_group` → `azurerm_network_security_group`
- Migrate state management from S3 backend to Azure Storage backend

## Azure Infrastructure Generation

Use `azure_development-summarize_topic` tool to get high-level instructions to follow.

Use `azure_recommend_service_config` to automatically detect services and dependencies from the migrated application.

Use `azure_check_region` to validate that required Azure services are available in the target region.

Use `azure_check_quota` to ensure sufficient quota for deployment.

Create an `infra/` directory in the project folder if it doesn't already exist.

Create an `azure.yaml` file in the root of the project for Azure Developer CLI (azd) support.

Use managed identities for authentication instead of connection strings and keys.

Set up proper RBAC with least privilege principles — map AWS IAM policies to Azure RBAC roles.

Configure appropriate scaling settings based on the application requirements and AWS auto-scaling configuration.

### Networking (based on VPC analysis)
- Convert VPC CIDR blocks → VNet address spaces
- Convert AWS subnets → Azure subnets
- Convert Security Groups → NSGs with equivalent rules
- Convert NAT Gateway → Azure NAT Gateway
- Set up Private Endpoints for PaaS services (replacing VPC Endpoints)
- Convert AWS PrivateLink → Azure Private Link

### Identity and Security
- Convert IAM Roles → Managed Identities with RBAC assignments
- Convert Secrets Manager / SSM Parameter Store → Key Vault secrets
- Key Vault must be configured with RBAC only (do not use access policies)
- Configure Entra ID integration for authentication

### Monitoring (based on CloudWatch analysis)
- Convert CloudWatch Metrics → Application Insights metrics
- Convert CloudWatch Alarms → Azure Monitor alerts
- Convert CloudWatch Logs → Log Analytics workspace
- Convert CloudWatch Dashboards → Azure Monitor workbooks
- Set up Application Insights for APM

Configure cost optimization settings (auto-scaling, reserved instances where appropriate).

Include infrastructure testing and validation scripts.

Use `azure_check_predeploy` to validate the generated infrastructure files.

If infrastructure generation fails, provide detailed error analysis and alternative approaches.

Based on the chosen Azure hosting platform in the assessment report (App Service, AKS, Container Apps, or Functions), generate the appropriate infrastructure files:

## For Bicep Infrastructure:
- Use Azure Verified Modules (AVM) where available for best practices, https://github.com/Azure/bicep-registry-modules.
- Use `azure_bicep_schemas-get_bicep_resource_schema` tool for each resource type to ensure correct schema usage.
- Create the following structure in the `infra/` folder:
  - `main.bicep` - Main deployment file with proper targeting scope
  - `main.parameters.json` - Parameters for the deployment (mapped from CloudFormation parameters)
  - `modules/` - Folder for modular Bicep files
    - `appService.bicep` or `containerApp.bicep` or `aks.bicep` or `functions.bicep` (depending on chosen platform)
    - `monitoring.bicep` - Application Insights and Log Analytics resources (replacing CloudWatch)
    - `database.bicep` (if applicable) - Database resources with proper networking (replacing RDS/DynamoDB)
    - `identityAndSecurity.bicep` - Managed Identity and RBAC setup (replacing IAM)
    - `networking.bicep` - VNet, NSG, private endpoints (replacing VPC)
    - `keyvault.bicep` - Azure Key Vault for secrets management (replacing Secrets Manager/SSM)
    - `storage.bicep` (if applicable) - Azure Storage (replacing S3)
- Configure the infrastructure for the selected hosting platform:
  - For App Service: Set up App Service Plan, App Service, deployment slots, and related resources
  - For AKS: Set up AKS cluster, node pools, Azure Container Registry, and related resources
  - For Container Apps: Set up Container Apps Environment, Container Registry, and Container Apps
  - For Functions: Set up Function App, App Service Plan (consumption or premium), and related resources

## For Terraform Infrastructure:
- Use `mcp_azure_mcp_azureterraformbestpractices` to retrieve current Terraform best practices for Azure.
- If migrating from AWS Terraform, convert `aws_*` resources to `azurerm_*` resources and update provider configuration.
- Create the following structure in the `infra/` folder:
  - `main.tf` - Main deployment file
  - `variables.tf` - Variable definitions (mapped from CloudFormation parameters or AWS Terraform variables)
  - `outputs.tf` - Output definitions
  - `providers.tf` - Provider configuration (azurerm instead of aws)
  - `backend.tf` - Azure Storage backend for state (replacing S3 backend)
  - `modules/` - Folder for modular Terraform files
    - `app_service/` or `container_app/` or `aks/` or `functions/` (depending on chosen platform)
    - `monitoring/` - Application Insights and Log Analytics resources
    - `database/` (if applicable) - Database resources
    - `identity/` - Managed Identity and RBAC setup
    - `networking/` - VNet, NSG, private endpoints
    - `keyvault/` - Key Vault for secrets management
    - `storage/` (if applicable) - Azure Storage
- Configure the infrastructure for the selected hosting platform.
- Set up proper monitoring with Application Insights and Log Analytics.
- Configure Entra ID integration for authentication.
- Include proper tagging and naming conventions.
- Prefer Managed Identity and OIDC federated credentials; avoid storing secrets in state or code.

## Deliverables

Make the infrastructure section in the migration report human-readable and in markdown format, using headings, bullet points, and other formatting options as appropriate.

Include a resource mapping table showing each AWS resource and its Azure equivalent in the generated infrastructure.

Suggest that the next step is to deploy to Azure, and mention `/AWS2Azure-phase4-deploytoazure` is the command to start the migration cutover and deployment process.

At the end, update the status report file `reports/Report-Status.md` with the status of the infrastructure generation step, including:
  - AWS resources detected and mapped
  - Azure infrastructure components created
  - CloudFormation/CDK conversion status
  - Security configurations implemented (IAM → RBAC mapping)
  - Networking conversion status (VPC → VNet)
  - Monitoring and logging setup (CloudWatch → Azure Monitor)
  - Any issues encountered during generation
