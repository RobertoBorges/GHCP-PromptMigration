# Application Assessment Report

## ASP Classic Store Application

**Assessment Date:** September 3, 2025  
**Last Updated:** September 10, 2025

## Application Overview

The application is a simple e-commerce store built with ASP Classic technology. It features:

- Product catalog with product listings
- Product detail pages
- Basic shopping cart functionality
- Contact form with validation
- Static about page
- Session-based user state management

## Technology Stack

| Component | Current Technology | Notes |
|-----------|-------------------|-------|
| **Frontend** | HTML, CSS, ASP Classic | Basic responsive design |
| **Backend** | ASP Classic (VBScript) | Server-side scripting |
| **Database** | Simulated (hardcoded arrays) | References to Access database (.mdb) |
| **Authentication** | None implemented | Basic session management present |
| **Session State** | ASP Session object | Used for cart management |

## Detailed Component Analysis

### Pages and Components

| Component | Current Implementation | Migration Approach | Complexity |
|-----------|------------------------|-------------------|------------|
| **Layout (Header/Footer)** | ASP includes | Razor _Layout.cshtml | Low |
| **Homepage** | Simple HTML with includes | Razor Page (Index.cshtml) | Low |
| **Products Listing** | Hardcoded array, for loop | Entity Framework, Razor Page | Medium |
| **Product Detail** | QueryString param, Select Case | Route parameter, EF lookup | Medium |
| **Shopping Cart** | Session based, form submission | Session middleware, form handling | Medium |
| **Contact Form** | Form validation, error handling | Model validation, Tag Helpers | Medium |
| **About Page** | Static content with includes | Static Razor Page | Low |
| **CSS Styling** | External CSS file | Can be used as-is | Low |
| **Session Management** | global.asa, Session object | ASP.NET Core Session middleware | Medium |

### Database Structure

The application currently uses hardcoded arrays for demonstration purposes, but references a Microsoft Access database in `database.asp`. For migration, we'll need to create proper models and a SQLite database:

#### Product Model
```csharp
public class Product
{
    public int Id { get; set; }
    public string Name { get; set; }
    public decimal Price { get; set; }
    public string Description { get; set; }
}
```

#### Cart Item Model
```csharp
public class CartItem
{
    public int Id { get; set; }
    public int ProductId { get; set; }
    public Product Product { get; set; }
    public int Quantity { get; set; }
    public string SessionId { get; set; }
}
```

### Business Logic

| Feature | Current Implementation | ASP.NET Core Approach |
|---------|------------------------|----------------------|
| **Product Listing** | Hardcoded array iteration | ProductService + EF Core |
| **Product Details** | Select Case based on ID | ProductService.GetProduct(id) |
| **Add to Cart** | Session variable | CartService + Session middleware |
| **Form Validation** | Manual validation in VBScript | Model validation, Data Annotations |
| **Session Management** | global.asa for initialization | Program.cs session configuration |

## Migration Requirements

### Migration Goals and Requirements
* Migrate the ASP Classic application to a modern technology stack
* Maintain existing business logic and functionality
* Preserve the current user experience and design
* No changes to business logic or images

### Target Technology Stack
* **Frontend & Backend**: ASP.NET Core with Razor Pages
* **Database**: SQLite (lightweight, file-based database for simplicity)
* **Authentication**: None required (maintaining current functionality)
* **Hosting**: Azure App Service
* **Infrastructure as Code**: Terraform

### Infrastructure Preferences
* Azure App Service for application hosting
* SQLite database embedded with the application
* No authentication services required

## Infrastructure Design

### Azure Resources

The following Azure resources will be provisioned using Terraform:

| Resource | Purpose | Configuration |
|----------|---------|---------------|
| **Resource Group** | Logical container for all resources | Region: East US |
| **App Service Plan** | Compute resources for the web app | SKU: B1 (Basic tier) |
| **Windows Web App** | Hosts the ASP.NET Core application | .NET 8 runtime |
| **Application Insights** | Monitoring and diagnostics | Web application type |
| **Storage Account** | File storage for SQLite database | Standard LRS |
| **File Share** | Persistent storage for SQLite data | 5GB quota |
| **Optional VNet** | Network isolation (if required) | 10.0.0.0/16 address space |

### Security Considerations

* TLS 1.2 minimum version enforced
* HTTPS required
* System-assigned managed identity
* Optional VNet integration for enhanced security
* Storage account network rules
* Application logging and monitoring

### Scalability

* App Service Plan allows vertical scaling (changing SKU)
* Multiple deployment slots can be added for zero-downtime deployments
* SQLite is not designed for high scalability scenarios, but sufficient for this application's needs

### Monitoring

* Application Insights for:
  * Performance monitoring
  * Error tracking
  * User behavior analysis
  * Availability testing
  * Log collection

### Deployment Process

1. Provision Azure resources using Terraform
2. Build and publish the ASP.NET Core application
3. Deploy to Azure App Service using ZIP deployment
4. Configure database connection
5. Verify application functionality

## Identified Migration Challenges

1. **Session State Migration**
   - ASP Classic uses built-in Session object
   - ASP.NET Core requires explicit session configuration
   - Solution: Implement Session middleware and CartService

2. **Form Handling and Validation**
   - ASP Classic uses manual validation with VBScript
   - ASP.NET Core uses model binding and validation
   - Solution: Create proper models with validation attributes

3. **Database Implementation**
   - ASP Classic uses hardcoded arrays (simulating Access DB)
   - ASP.NET Core uses Entity Framework Core
   - Solution: Create models, DbContext, and migration scripts

4. **Routing and Navigation**
   - ASP Classic uses direct file references (.asp)
   - ASP.NET Core uses routing middleware
   - Solution: Configure proper route mappings in Program.cs

5. **Shared UI Components**
   - ASP Classic uses #include directive
   - ASP.NET Core uses _Layout and Partial Views
   - Solution: Create appropriate Razor layout and partial views

## Migration Approach

The ASP Classic application will require a complete rewrite to ASP.NET Core due to the significant differences between ASP Classic and modern web frameworks. Based on user requirements, we'll follow this approach:

### Migration Path: ASP.NET Core Web Application

* **Framework**: ASP.NET Core with Razor Pages
* **Database**: SQLite (lightweight, file-based database)
* **Hosting**: Azure App Service
* **Infrastructure as Code**: Terraform

### Architectural Diagram

![Architecture Diagram](./images/architecture-diagram.md)

### Migration Components Mapping

| Current ASP Classic | ASP.NET Core Equivalent |
|---------------------|-------------------------|
| `.asp` pages | Razor Pages (`.cshtml`) |
| VBScript code | C# code-behind |
| `global.asa` | `Program.cs` and `Startup.cs` |
| Session state | ASP.NET Core session middleware |
| Includes (header/footer) | Razor _Layout and Partial Views |
| Hardcoded arrays | Entity models with SQLite |
| CSS (unchanged) | CSS (unchanged) |

### Project Structure

```
/
├── StoreApp/                      # Main project folder
│   ├── Program.cs                 # App configuration and services
│   ├── appsettings.json           # Configuration
│   ├── StoreApp.csproj            # Project file
│   ├── Data/                      # Data access
│   │   ├── ApplicationDbContext.cs
│   │   ├── Migrations/            # EF Core migrations
│   │   └── SeedData.cs            # Initial data seeding
│   ├── Models/                    # Data models
│   │   ├── Product.cs
│   │   └── CartItem.cs
│   ├── Pages/                     # Razor Pages
│   │   ├── _ViewStart.cshtml
│   │   ├── _ViewImports.cshtml
│   │   ├── Index.cshtml           # Home page
│   │   ├── Products/
│   │   │   ├── Index.cshtml       # Product listing
│   │   │   └── Details.cshtml     # Product details
│   │   ├── Cart.cshtml            # Shopping cart
│   │   ├── Contact.cshtml         # Contact form
│   │   └── About.cshtml           # About page
│   ├── Services/                  # Business logic
│   │   ├── ProductService.cs
│   │   └── CartService.cs
│   ├── wwwroot/                   # Static files
│   │   ├── css/
│   │   │   └── styles.css         # Original CSS
│   │   ├── js/
│   │   └── images/
│   └── Shared/                    # Shared components
│       ├── _Layout.cshtml         # Main layout
│       └── _ValidationScriptsPartial.cshtml
└── StoreApp.Tests/                # Unit tests
```

### Detailed Migration Strategy

1. **Project Setup**
   - Create ASP.NET Core Razor Pages project
   - Configure SQLite with Entity Framework Core
   - Set up session middleware
   - Configure static file middleware for CSS

2. **Data Layer Implementation**
   - Create Product and CartItem models
   - Implement DbContext
   - Create database migration scripts
   - Seed initial product data

3. **Business Logic Services**
   - Implement ProductService for product management
   - Create CartService for shopping cart functionality
   - Add form handling and validation services

4. **UI Implementation**
   - Create _Layout.cshtml (based on header.asp/footer.asp)
   - Implement Razor Pages for each ASP page
   - Port CSS styles to wwwroot/css
   - Implement form validation

5. **Session Management**
   - Configure session middleware
   - Implement cart functionality using session
   - Create helper extensions for session

## CI/CD Pipeline Implementation

### Pipeline Components

The CI/CD pipeline has been set up with dual support for both GitHub Actions and Azure DevOps:

| Component | Implementation | Purpose |
|-----------|----------------|---------|
| **Source Control** | Git (GitHub / Azure DevOps) | Version control and collaboration |
| **Build Automation** | GitHub Actions / Azure DevOps | Compile, test, and package application |
| **Infrastructure as Code** | Terraform | Provision and configure Azure resources |
| **Artifact Storage** | GitHub Packages / Azure Artifacts | Store build outputs |
| **Deployment Automation** | GitHub Actions / Azure DevOps | Deploy to target environments |
| **Environment Management** | Environment definitions with approvals | Control deployment flow |
| **Monitoring** | Application Insights | Track application performance |
| **Authentication** | Service Principal | Secure access to Azure resources |
| **State Management** | Azure Storage | Store Terraform state files |

### Pipeline Workflow

The CI/CD pipeline follows this workflow:

1. **Build & Test**
   - Restore NuGet packages
   - Build ASP.NET Core application
   - Run automated tests
   - Create deployment package

2. **Validate Infrastructure**
   - Initialize Terraform
   - Validate Terraform configuration
   - Check Terraform formatting

3. **Deploy Infrastructure**
   - Plan Terraform changes
   - Apply infrastructure changes
   - Export resource information

4. **Deploy Application**
   - Deploy application package to App Service
   - Perform post-deployment verification
   - Execute application warmup

### Azure DevOps Implementation

The Azure DevOps pipeline has been configured with:

1. **Multi-Stage Pipeline**
   - YAML-based pipeline definition in `infrastructure/cicd/deployment-pipeline.yml`
   - Three main stages: Build, Validate Infrastructure, and Deploy
   - Environment-specific deployment configurations

2. **Variable Groups**
   - **AzureServicePrincipal**: Stores Service Principal credentials for Azure authentication
   - **TerraformConfig**: Contains Terraform state storage configuration

3. **Service Connection**
   - Azure Resource Manager connection for secure Azure resource access
   - Named `azure-service-connection` for consistent reference in pipeline

4. **Security Features**
   - No hardcoded credentials in pipeline definition
   - Secrets stored as secure variables in variable groups
   - Service Principal with least privilege access
   - Branch protection policies

5. **Deployment Configuration**
   - Deployment to Dev environment on main branch changes
   - Manual triggers for Test and Production environments
   - Environment-specific variable substitution

### Environment Strategy

The pipeline supports multiple environments with progressive deployment:

| Environment | Purpose | Deployment Trigger | Approval Requirements |
|-------------|---------|-------------------|----------------------|
| **Dev** | Development and testing | Automatic on merge to main | None |
| **Test** | QA and integration testing | Manual | Single approver |
| **Prod** | Production deployment | Manual | Multiple approvers |

### Security Measures

The CI/CD pipeline implements these security measures:

- Service principal with least privilege access
- Secrets stored in GitHub Secrets / Azure KeyVault / Azure DevOps variable groups
- Environment-specific variable scoping
- Approval gates for production deployments
- Infrastructure validation before deployment
- Clean branch strategy to avoid security scanning issues
- No hardcoded credentials in source code or pipeline definitions
- Azure DevOps security scanning for secrets in code

### Rollback Strategy

In case of deployment failures, the pipeline supports:

- Automatic failure detection
- Manual rollback to previous version
- Terraform state rollback capabilities
- Blue-green deployment support (for zero-downtime updates)

### Pipeline Execution Guide

To run the CI/CD pipeline in Azure DevOps, follow these steps:

1. **Prerequisites**
   - Azure subscription with appropriate permissions
   - Service Principal with Contributor access to the subscription
   - Azure Storage Account for Terraform state storage
   - Azure DevOps project with appropriate permissions

2. **Configure Variable Groups**
   - Navigate to **Library > Variable Groups** in Azure DevOps
   - Configure the **AzureServicePrincipal** variable group:
     - `ARM_CLIENT_ID`: Service Principal Client ID
     - `ARM_CLIENT_SECRET`: Service Principal Secret (mark as secret)
     - `ARM_SUBSCRIPTION_ID`: Azure Subscription ID
     - `ARM_TENANT_ID`: Azure Tenant ID
   - Configure the **TerraformConfig** variable group:
     - `TF_STATE_RESOURCE_GROUP_NAME`: Resource group for Terraform state
     - `TF_STATE_STORAGE_ACCOUNT_NAME`: Storage account for Terraform state
     - `TF_STATE_CONTAINER_NAME`: Container for Terraform state
     - `TF_STATE_KEY`: Key for Terraform state file (e.g., "storeapp.tfstate")

3. **Create Service Connection**
   - Go to **Project Settings > Service connections**
   - Create a new **Azure Resource Manager** connection
   - Name it `azure-service-connection`
   - Grant access permission to all pipelines

4. **Run the Pipeline**
   - Navigate to **Pipelines** in Azure DevOps
   - Select the **Deployment Pipeline**
   - Click **Run pipeline**
   - Select the **pipeline-branch** branch
   - Click **Run**

5. **Monitor Deployment**
   - Track progress through each pipeline stage
   - Verify infrastructure creation in Azure Portal
   - Validate application deployment and functionality
   - Review Application Insights for monitoring data

6. **Troubleshooting**
   - Check pipeline logs for error messages
   - Verify Service Principal permissions
   - Ensure Terraform state storage is accessible
   - Check for resource conflicts or quota limits

Detailed documentation for the pipeline setup can be found in `infrastructure/cicd/azure-devops-pipeline-setup.md`.

## Next Steps

1. **Phase 3: Code Modernization** ✅
   - Set up ASP.NET Core project structure
   - Create data models and SQLite database
   - Implement Razor Pages for each ASP page
   - Port business logic to C# services

2. **Phase 4: Infrastructure Generation** ✅
   - Create Terraform configuration for Azure resources
   - Set up App Service Plan and App Service
   - Configure Application Insights for monitoring
   - Set up storage for SQLite database

3. **Phase 5: Deployment to Azure** ✅
   - Create deployment script (deploy.ps1)
   - Set up Terraform state management
   - Configure Azure authentication
   - Test deployment to Dev environment

4. **Phase 6: CI/CD Setup** ✅
   - Configure CI/CD pipeline in Azure DevOps
   - Set up Service Principal for authentication
   - Create variable groups for secrets management
   - Configure deployment stages and environments
   - Create documentation for pipeline setup and maintenance

2. **Phase 4: Infrastructure Generation** ✅
   - Create Terraform scripts for Azure resources
   - Configure Azure App Service settings
   - Set up monitoring and logging

3. **Phase 5: Deployment to Azure** ✅
   - Deploy application to Azure App Service
   - Validate functionality in cloud environment
   - Perform testing and optimization

4. **Phase 6: CI/CD Setup** ✅
   - Configure CI/CD pipeline
   - Implement automated testing
   - Set up deployment automation

## Timeline Estimate

| Phase | Estimated Duration | Dependencies | Status |
|-------|-------------------|--------------|--------|
| Assessment | 1 week | None | ✅ Completed |
| Code Modernization | 2-3 weeks | Assessment | ✅ Completed |
| Infrastructure Generation | 1 week | None (can be parallel with Code Modernization) | ✅ Completed |
| Deployment | 1 week | Code Modernization and Infrastructure | ✅ Completed |
| CI/CD Setup | 1 week | Deployment | ✅ Completed |

**Total Estimated Time**: 5-6 weeks
**Actual Completion Time**: On schedule
