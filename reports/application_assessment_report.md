# Contoso University Application Assessment Report

**Date**: August 6, 2025  
**Project**: ContosoUniversityDiPS  
**Target Hosting Platform**: Azure App Service  
**Target Infrastructure as Code**: Terraform  

## Executive Summary

The Contoso University application is a .NET Core 2.1 based educational institution management system with multiple components including a web application, REST API, and a React-based SPA. This assessment evaluates the application's readiness for migration to Azure App Service using Terraform for infrastructure as code. The application was created to demonstrate ASP.NET Core concepts and needs to be modernized to current .NET versions and cloud-native practices.

## Application Overview

Contoso University is a sample application consisting of the following components:

1. **ContosoUniversity.Web** - Traditional web application using MVC and Razor Pages
2. **ContosoUniversity.Api** - REST API service with JWT authentication
3. **ContosoUniversity.Spa.React** - React-based single-page application
4. **ContosoUniversity.Data** - Data access layer with Entity Framework Core
5. **ContosoUniversity.Common** - Shared components and utilities

The application demonstrates various educational institution management features like managing departments, courses, students, and instructors.

## Current Technical Stack

| Component | Current Version | Compatibility |
|-----------|----------------|---------------|
| .NET SDK | 2.1.300 | End of life, needs upgrade |
| ASP.NET Core | 2.1 | End of life, needs upgrade |
| Entity Framework Core | 2.1 | End of life, needs upgrade |
| Identity | 2.1 | End of life, needs upgrade |
| Entity Framework Provider | SQL Server, SQLite | Compatible with upgrade path |
| Authentication | Cookie-based + JWT Bearer | Compatible with upgrade path |
| Front-end | Traditional MVC + Razor Pages + React SPA | Compatible with upgrade path |
| External Authentication | Google, Facebook | Requires reconfiguration for Entra ID |
| Database | MS SQL Server (LocalDB) | Compatible, needs connection string updates |
| Testing | xUnit, Moq | Compatible with upgrade path |

## Current Architecture

```
                    +-------------------+
                    | User/Browser      |
                    +-------------------+
                       /              \
                      /                \
        +-----------------+       +------------------+
        | Web Application |       | React SPA        |
        | (MVC/Razor)     |       |                  |
        +-----------------+       +------------------+
                |                           |
                |                           |
        +-----------------+       +------------------+
        | Common Layer    | <---> | REST API         |
        +-----------------+       +------------------+
                |                           |
                |                           |
        +-----------------+                 |
        | Data Layer      | <---------------+
        | (EF Core)       |
        +-----------------+
                |
                |
        +-----------------+
        | SQL Server      |
        | (LocalDB)       |
        +-----------------+
```

## Assessment Findings

### Framework Version

The application is built with .NET Core 2.1, which reached end of support on August 21, 2021. Migration to a supported .NET version (preferably .NET 8 LTS) is required.

### Project Structure

The application follows a modular approach with separate projects for different concerns:
- Presentation layers (Web, API, SPA)
- Data access layer
- Common utilities

This structure is compatible with modern .NET practices and can be maintained during migration.

### Authentication and Identity

- Uses ASP.NET Core Identity 2.1 for user management
- Implements JWT Bearer authentication for API access
- Uses cookie-based authentication for web application
- Supports two-factor authentication
- Has OAuth integrations with external providers (Google, Facebook)

This authentication setup needs to be updated to the latest Identity patterns and migrated to use Entra ID for authentication.

### Database Access

- Uses Entity Framework Core 2.1 with Repository and Unit of Work patterns
- Supports multiple database providers (SQL Server, SQLite)
- Uses code-first approach with migrations

The Entity Framework implementation requires updating to the latest version, but the overall patterns can be maintained.

### Dependencies and NuGet Packages

All NuGet packages are from the .NET Core 2.1 timeframe and need to be upgraded to compatible versions for the target .NET version.

### Cloud-Incompatible Components

1. **LocalDB usage**: The application currently uses LocalDB, which is not available in Azure. The connection strings need to be updated to use Azure SQL Database.
2. **File system access**: Any direct file system operations need to be reviewed and potentially migrated to Azure Storage.

### Testing Strategy

The application has a comprehensive testing suite:
- Unit tests using Moq and xUnit
- Integration tests using TestHost and InMemoryDatabase

The testing framework is compatible with newer .NET versions but will require updates.

## Migration Plan

### Target State

| Component | Current Version | Target Version |
|-----------|----------------|---------------|
| .NET SDK | 2.1.300 | .NET 8.0 (LTS) |
| ASP.NET Core | 2.1 | ASP.NET Core 8.0 |
| Entity Framework Core | 2.1 | Entity Framework Core 8.0 |
| Identity | 2.1 | ASP.NET Core Identity 8.0 + Entra ID |
| Authentication | Cookie + JWT | Cookie + JWT + Entra ID |
| Hosting | Local | Azure App Service |
| Database | LocalDB | Azure SQL Database |
| Infrastructure | Manual | Terraform |

### Target Architecture

```
                      +------------------------+
                      | Azure App Service      |
                      | (Web Application)      |
                      +------------------------+
                                  |
                      +------------------------+
                      | Azure App Service      |
                      | (API)                  |
                      +------------------------+
                                  |
           +------------------+   |   +------------------+
           | Azure Entra ID   |<--+-->| Application      |
           | (Authentication) |   |   | Insights         |
           +------------------+   |   +------------------+
                                  |
                      +------------------------+
                      | Azure SQL Database     |
                      +------------------------+
                                  |
                      +------------------------+
                      | Azure Key Vault        |
                      | (Secrets Management)   |
                      +------------------------+
```

### Required Code Changes

#### Framework Upgrade

1. Update the global.json to target .NET 8.0
2. Update all project files (.csproj) to target .NET 8.0
3. Update NuGet package references to versions compatible with .NET 8.0
4. Address breaking changes between .NET Core 2.1 and .NET 8.0

#### Authentication Migration

1. Update Identity implementation to ASP.NET Core Identity 8.0
2. Integrate Microsoft.Identity.Web for Entra ID authentication
3. Update JWT bearer configuration to work with Entra ID
4. Migrate OAuth providers from Google/Facebook to Entra ID B2C (if social logins are still required)

#### Configuration Transformation

1. Review and update appsettings.json files to include Azure-specific configurations
2. Move sensitive configuration to Azure Key Vault
3. Implement the Azure App Configuration pattern for centralizing configuration

#### Database Migration

1. Update Entity Framework Core to version 8.0
2. Update connection strings to use Azure SQL Database
3. Create new migrations for the latest EF Core version
4. Implement connection resilience with retry patterns

#### Testing Updates

1. Update testing frameworks to latest versions
2. Adapt integration tests to work with the new EF Core version
3. Add tests for Azure-specific functionality

### Containerization Strategy

While Azure App Service supports direct deployment, containerization provides additional benefits:

1. Create Dockerfiles for Web and API components
2. Implement multi-stage builds for optimized container images
3. Configure container orchestration for local development
4. Use Azure App Service's container deployment capabilities

### Infrastructure as Code (Terraform)

1. Create a Terraform module structure for the application components
2. Define resources:
   - Azure App Service Plans
   - Azure App Services for Web and API
   - Azure SQL Database
   - Azure Key Vault
   - Application Insights
   - Entra ID applications
3. Configure CI/CD for infrastructure deployment

## Risk Assessment and Mitigation Strategies

| Risk | Impact | Likelihood | Mitigation Strategy |
|------|--------|------------|---------------------|
| Breaking changes in API contracts | High | Medium | Create comprehensive API tests, implement versioning |
| Authentication migration failures | High | Medium | Implement dual-authentication during transition period |
| Database migration issues | Medium | Low | Extensive testing of migrations, backup strategy |
| Performance degradation | Medium | Low | Performance testing, monitoring with Application Insights |
| Deployment failures | Medium | Low | Implement blue-green deployment, automated rollback |
| Security vulnerabilities in updated packages | High | Low | Security scanning, keep dependencies updated |

## Estimated Effort and Timeline

| Phase | Tasks | Estimated Effort | Timeline |
|-------|-------|------------------|----------|
| **Planning and Setup** | Project setup, environment configuration | 2-3 days | Week 1 |
| **Framework Migration** | Update to .NET 8, fix breaking changes | 4-6 days | Weeks 1-2 |
| **Authentication Migration** | Update Identity, integrate Entra ID | 3-4 days | Week 2 |
| **Database Migration** | Update EF Core, connection strings | 2-3 days | Week 3 |
| **Infrastructure as Code** | Create Terraform templates | 3-5 days | Week 3 |
| **Testing and Validation** | Run tests, fix issues | 3-4 days | Week 4 |
| **Deployment and Verification** | Deploy to Azure, verify functionality | 2-3 days | Week 4 |
| **Documentation and Knowledge Transfer** | Update docs, train team | 1-2 days | Week 4 |
| **Total** | | **20-30 days** | **4 weeks** |

## Recommendations

1. **Incremental Migration**: Perform the migration in stages, starting with framework updates, then authentication changes, and finally cloud deployment.
2. **Automated Testing**: Enhance the existing test suite to ensure thorough coverage during migration.
3. **Feature Flags**: Implement feature flags to enable gradual rollout of new functionality.
4. **Monitoring**: Set up comprehensive monitoring with Application Insights from the beginning of the migration.
5. **Security Enhancements**: Take the opportunity to implement additional security measures during the migration.

## Next Steps

1. Create a detailed migration plan with specific tasks and assignments
2. Set up development and staging environments in Azure
3. Begin the code modernization phase with /phase2-migratecode
4. Create the Terraform templates for infrastructure
5. Implement CI/CD pipelines for automated deployment

This assessment serves as a baseline for the migration effort. Adjustments to the plan may be necessary as the migration progresses.
