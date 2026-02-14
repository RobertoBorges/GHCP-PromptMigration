---
name: Phase 2 - Migrate Code
description: Upgrade legacy .NET or Java application code to modern framework versions
argument-hint: "Specify target framework if not already assessed, e.g., 'Migrate to .NET 8' or 'Upgrade to Spring Boot 3'"
agent: Code Migration Modernization Agent
---

Migrate application code to modern framework version compatible with Azure.

## Skills to Load

Load the appropriate skills based on application type:
- **business-logic-mapping** skill — **ALWAYS** use to track and preserve business logic during migration
- For .NET applications: Use **dotnet-modernization** skill for patterns and templates
- For Java applications: Use **java-modernization** skill for patterns and templates  
- For WCF services: Use **wcf-to-rest-migration** skill for service conversion
- For config files: Use **config-transformation** skill for settings migration

## Business Logic Preservation (Critical)

Before making any code changes:
1. **Create** `reports/Business-Logic-Mapping.md` to track all business logic
2. **Identify** all business logic in the legacy application (see business-logic-mapping skill)
3. **Document** each business logic item with source location
4. **Update** the mapping document as you migrate each item
5. **Verify** each migrated item produces the same results

Categories to track:
- Calculations (pricing, tax, discounts, etc.)
- Validations (business rules, constraints)
- Workflows (state machines, approval chains)
- Transformations (data conversions, aggregations)
- Integrations (external APIs, third-party services)
- Authorization (business-level permissions)
- Notifications (email triggers, alerts)
- Scheduling (batch jobs, timed operations)

## Media and Asset Preservation

Track and copy all media assets:
- Images, CSS, JavaScript, fonts
- User uploads and documents
- Email templates, report templates
- Localization/resource files

Update `reports/Business-Logic-Mapping.md` with asset migration status.

---

Ensure appropriate Azure extensions for the target framework are installed in VS Code.

Always start migration by creating a new folder under the root folder with an intuitive name for the modernized project. 

Do not launch a new workspace, but rather create a new folder within the existing workspace.

Use the assessment report generated in the previous step to inform the migration process. The assessment report can be found in the 'reports' folder.

Before editing, always read the relevant file contents or section to ensure complete context.

Use `semantic_search` tool to identify all code files that need migration.

Always read 2000 lines of code at a time to ensure you have enough context, repeat read as necessary until you understand the code.

If a patch is not applied correctly, attempt to reapply it.

Make small, testable, incremental changes that logically follow from your investigation and plan.

Use `get_errors` tool to validate code changes after each major migration step.

Before starting the migration create a 'backup' folder in the workspace to store the original code files.

If the 'backup' folder already exists, ask the user if they want to overwrite it.

Use the guidance from the assessment report (reports/Application-Assessment-Report.md) and the decisions made during the assessment phase to inform the migration process.

Copy media files from the original project directory to the new project directory at same relative paths.

Keep equivalent UI components to avoid breaking changes.

Confirm that all functionality is preserved after migration.

Containerize the application if specified in the assessment report.

Create a Script to build and run the application in a Docker container, if applicable.

Make sure you build the application as you create it, and fix them as you go.

Based on the assessed application type (.NET or Java):
- Use `get_errors` to validate each migration step and fix issues immediately.
- Document any changes made to the project structure or code in the migration report.
- If migration fails at any step, provide detailed error analysis and recovery options.

Suggest that the next step is to generate infrastructure files, and mention `/phase3-generateinfra` is the command to start the infra generation process.

At the end, update the status report file reports/Report-Status.md with the status of the migration step.

## For .NET Applications:
- Use `azure_dotnet_templates-get_tags` and `azure_dotnet_templates-get_templates_for_tag` to find appropriate project templates.
- Create a modern .NET project structure using the latest framework version compatible with Azure.
- Use `file_search` to locate all source files for migration.
- Use `semantic_search` to identify patterns that need modernization.
- Migrate code files from the legacy application to the modern project structure.
- Transform configuration:
  - Convert web.config or app.config to appsettings.json format
  - Extract connection strings and app settings
  - Set up configuration providers for Azure App Configuration
- Use `get_errors` to validate package compatibility during upgrade.
- Upgrade NuGet packages to compatible versions.
- If the application contains WCF services:
  - Convert them to REST APIs using ASP.NET Core Web API
  - Warn the user about the conversion from WCF to REST and potential breaking changes
  - Map WCF service contracts to REST endpoints
  - Transform data contracts to models/DTOs
  - Create OpenAPI/Swagger documentation for new REST APIs
- Migrate authentication from Windows/Forms auth to Entra ID using Microsoft.Identity.Web.
- Update database access code to use Azure-compatible providers.

## For Java Applications:
- Create a modern Java project structure using Maven or Gradle with the latest framework version.
- Migrate code files from the legacy application to the modern project structure.
- Transform configuration:
  - Convert XML configs to application.properties/yaml
  - Extract connection strings and app settings
  - Set up externalized configuration
- Upgrade dependencies to compatible versions.
- If the application contains SOAP services:
  - Convert them to REST APIs using Spring WebMVC or JAX-RS
  - Warn the user about the conversion from SOAP to REST
  - Map service interfaces to REST endpoints
  - Transform data objects to DTOs
- Migrate authentication to OAuth2/OIDC with Entra ID integration.
- Update database access code to be compatible with Azure databases.
- Set up proper logging with SLF4J and Azure-compatible appenders.

