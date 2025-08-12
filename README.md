# GitHub Copilot Migration & Modernization for Azure

This repository showcases how GitHub Copilot using custom prompts and chat mode can be leveraged to migrate solutions from various languages and frameworks to Azure. The current focus is on .NET and Java applications, demonstrating end-to-end migration journeys. The project now includes enhanced modernization tracking, status reporting, and a more structured approach to the migration process.

## Overview

The GitHub Copilot Migration & Modernization for Azure project provides a structured approach to:

1. Assess legacy applications for cloud readiness
2. Migrate code to modern frameworks
3. Generate Azure infrastructure as code
4. Validate code and infrastructure

5. Deploy applications to Azure
6. Set up CI/CD pipelines for automated deployment

Through a guided, AI-assisted workflow, developers can efficiently transform legacy applications into modern, cloud-native solutions running on Azure.

## Avoiding Hallucinations

To reduce hallucinations during the migration, the guided prompts use two files in the repository's `reports/` folder:

- `modernization_status.md` — overall migration status dashboard
- `Application-Assessment-Report.md` — application assessment summary

You can update these files at any phase to fit your requirements.

During each phase, read the summary carefully to understand what will be delivered by the model and what inputs are needed.

Pro tip: during the rewrite migration process, some unnecessary files may be created (Class1.cs); clean them up before your final check-in.

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


The repository implements a structured 6-phase approach to application migration:

### Phase 1: Plan Migration

Plan your migration by asking key questions about your migration project requirements, hosting preferences, and database needs to create a tailored migration strategy.

### Phase 2: Assessment

Generate a comprehensive report assessing the current application structure, dependencies, and architecture with detailed risk analysis and effort estimation.

### Phase 3: Code Migration

Upgrade application code to the latest framework versions compatible with Azure, with automated transformations and incremental validation.

### Phase 4: Infrastructure Generation

Create infrastructure as code (IaC) files (Bicep or Terraform) for deploying to Azure, incorporating best practices and security configurations.

### Phase 5: Deployment to Azure

Deploy the validated application to Azure services with comprehensive deployment monitoring and validation.

### Phase 6: CI/CD Pipeline Setup

Configure automated deployment pipelines for continuous integration and delivery, with environment-specific configurations and security gates.

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
- **Status Tracking**: Comprehensive modernization status reporting with progress tracking and quality metrics
- **Structured Migration Planning**: Guided approach to planning migration with targeted questions and requirements gathering
- **Risk Assessment & Mitigation**: Identification and mitigation strategies for potential migration issues
- **Deployment Monitoring**: Real-time validation and monitoring during application deployment
- **Incremental Validation**: Step-by-step validation throughout the migration process

## Migration Status Tracking

The project now includes comprehensive migration status tracking through the `/getstatus` command:

- **Progress Monitoring**: Track overall migration progress with completion percentages and phase status
- **Quality Metrics**: View quality scores for each completed phase
- **Timeline Tracking**: Timestamps for completed phases to monitor project timeline
- **Risk Management**: Identification and tracking of potential issues with severity levels
- **Next Steps Guidance**: Clear recommendations for the next steps in the migration process
- **Resource Links**: Quick access to relevant documentation and resources
- **Executive Summary**: At-a-glance view of key migration metrics and status

Status reports are stored in the `reports/modernization_status.md` file, providing a central location for tracking migration progress across all phases.

## Getting Started

1. Clone this repository
2. Install [GitHub Copilot](https://copilot.github.com/) in your Visual Studio Code
3. Open one of the use case projects in VS Code
4. Start a chat with GitHub Copilot using the `/phase1-planmigration under the folder #file:02-NetFramework30-ASPNET-WEB` command to begin the migration planning
5. Use `/getstatus` at any time to check the current migration status
6. Follow the guided prompts to complete each phase of the migration process

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

## Improved Prompt Structure

The custom prompts have been significantly enhanced with:

### Enhanced Structured Workflow

- **Planning Phase**: Added a dedicated planning phase to gather requirements before starting the assessment
- **Status Command**: New `/getstatus` command to check migration progress at any time
- **Report Generation**: Automatic creation of assessment, validation, and status reports
- **Incremental Validation**: Step-by-step validation checks throughout the migration process
- **Context Preservation**: Better context retention between phases of the migration

### Technical Improvements

- **Enhanced Azure Integration**: Better support for Azure resource validation and deployment
- **Comprehensive Validation**: More thorough code and infrastructure validation checks
- **Database Migration**: Improved guidance for database migration scenarios
- **Security Focus**: Enhanced security validation and configuration for Azure resources
- **Cost Optimization**: Added recommendations for optimizing cost in Azure deployments

### Documentation and Reporting

- **Detailed Reports**: More comprehensive reports with actionable recommendations
- **Visual Progress**: Visual progress tracking with completion percentages
- **Risk Management**: Enhanced risk identification and mitigation guidance
- **Architecture Diagrams**: Support for generating before/after architecture diagrams
- **Performance Metrics**: Added performance baseline recommendations and validation

## Contributing

Contributions to improve the prompts, chat modes, or add new use cases are welcome. Please feel free to submit pull requests or open issues to discuss potential improvements.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
