# GitHub Copilot Migration & Modernization for Azure

This repository showcases how GitHub Copilot using custom prompts and chat mode can be leveraged to migrate solutions from various languages and frameworks to Azure. The current focus is on .NET and Java applications, demonstrating end-to-end migration journeys.

## Overview

The GitHub Copilot Migration & Modernization for Azure project provides a structured approach to:

1. Assess legacy applications for cloud readiness
2. Migrate code to modern frameworks
3. Generate Azure infrastructure as code
4. Validate code and infrastructure
5. Deploy applications to Azure
6. Set up CI/CD pipelines for automated deployment

Through a guided, AI-assisted workflow, developers can efficiently transform legacy applications into modern, cloud-native solutions running on Azure.

## Repository Structure

- **`.github/`**: Contains custom prompts and chat modes that enable GitHub Copilot to assist with migration
  - **`chatmodes/`**: Defines specialized chat experiences for migration scenarios
  - **`prompts/`**: Structured prompts for each phase of the migration process

- **`Use-cases/`**: Example applications representing different migration scenarios
  - **`01-ASPClassicApp/`**: Classic ASP application with e-commerce functionality
  - **`02-NetFramework30-ASPNET-WEB/`**: .NET Framework 3.0 ASP.NET Web Application
  - **`03-WCFNet35/`**: WCF services using .NET Framework 3.5
  - **`04-ContosoUniversityDiPS/`**: Sample university application with multiple components

## Migration & Modernization Process

The repository implements a structured 7-phase approach to application migration:

### Phase 1: Assessment

Generate a comprehensive report assessing the current application structure, dependencies, and architecture.

### Phase 2: Code Migration

Upgrade application code to the latest framework versions compatible with Azure.

### Phase 3: Infrastructure Generation

Create infrastructure as code (IaC) files (Bicep or Terraform) for deploying to Azure.

### Phase 4: Code Validation

Validate the migrated application code against modern standards and best practices.

### Phase 5: Infrastructure Validation

Validate the infrastructure files for Azure deployment readiness.

### Phase 6: Deployment to Azure

Deploy the validated application to Azure services.

### Phase 7: CI/CD Pipeline Setup

Configure automated deployment pipelines for continuous integration and delivery.

## Key Features

- **Comprehensive Assessment**: Analyze existing .NET Framework or Java applications for cloud readiness
- **Automated Code Migration**: Transform legacy code to modern versions compatible with Azure
- **Infrastructure as Code**: Generate Bicep or Terraform files for Azure resources
- **Multi-Platform Support**: Target different Azure hosting options (App Service, AKS, Container Apps)
- **Authentication Modernization**: Convert on-premises authentication to Azure Entra ID
- **Service Migration**: Transform WCF services to modern REST APIs and SOAP services to RESTful endpoints
- **Configuration Transformation**: Convert legacy configuration files to modern formats
- **CI/CD Integration**: Set up GitHub Actions or Azure DevOps pipelines for automated deployment
- **Validation & Best Practices**: Ensure migrated applications follow Azure best practices

## Getting Started

1. Clone this repository
2. Install [GitHub Copilot](https://copilot.github.com/) in your Visual Studio Code
3. Open one of the use case projects in VS Code
4. Start a chat with GitHub Copilot using the `/phase1-assessproject under the folder #file:02-NetFramework30-ASPNET-WEB` command
5. Follow the guided prompts to complete each phase of the migration process

## Target Azure Hosting Platforms

The migration process supports multiple Azure hosting options:

- **Azure App Service**: For web applications and APIs
- **Azure Kubernetes Service (AKS)**: For containerized applications
- **Azure Container Apps**: For microservices and containerized applications

## Authentication & Authorization

The repository includes support for migrating from various authentication systems to Azure Entra ID, ensuring secure access to modernized applications.

## Use Cases

This repository contains example applications that can be used to test prompts and understand how GitHub Copilot works in the context of migration and modernization:

- **ASP Classic Apps**: Migration path for legacy ASP applications
- **.NET Framework Web Apps**: Upgrading to modern .NET versions
- **WCF Services**: Converting to RESTful APIs
- **Java Applications**: Modernizing for Azure compatibility

## Contributing

Contributions to improve the prompts, chat modes, or add new use cases are welcome. Please feel free to submit pull requests or open issues to discuss potential improvements.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
