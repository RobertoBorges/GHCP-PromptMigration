---
mode: agent
---
Migrate application code to modern framework version compatible with Azure.

# Rules for Code Migration and Modernization
- Ensure appropriate Azure extensions for the target framework are installed in VS Code.
- Always start migration by creating a new folder with an intuitive name for the modernized project. Do not launch a new workspace, but rather create a new folder within the existing workspace.
- Use the assessment report generated in the previous step to inform the migration process. The assessment report can be found in the 'reports' folder.
- Based on the assessed application type (.NET or Java):
- Before starting the migration create a 'backup' folder in the workspace to store the original code files.
- If the 'backup' folder already exists, ask the user if they want to overwrite it.

## For .NET Applications:
- Create a modern .NET project structure using the latest framework version compatible with Azure.
- Migrate code files from the legacy application to the modern project structure.
- Transform configuration:
  - Convert web.config or app.config to appsettings.json format
  - Extract connection strings and app settings
  - Set up configuration providers
- Upgrade NuGet packages to compatible versions.
- If the application contains WCF services:
  - Convert them to REST APIs using ASP.NET Core Web API
  - Warn the user about the conversion from WCF to REST
  - Map WCF service contracts to REST endpoints
  - Transform data contracts to models/DTOs
- Implement modern dependency injection pattern.
- Migrate authentication from Windows/Forms auth to Entra ID.
- Update database access code to be compatible with Azure databases.
- Set up proper logging with ILogger and Application Insights support.
- Implement middleware for cross-cutting concerns.
- Containerize the application if specified in the assessment report.

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
- Implement modern dependency injection with Spring or CDI.
- Migrate authentication to OAuth2/OIDC with Entra ID integration.
- Update database access code to be compatible with Azure databases.
- Set up proper logging with SLF4J and Azure-compatible appenders.
- Implement filters/interceptors for cross-cutting concerns.
- Containerize the application if specified in the assessment report.

## General Rules:
- Create a migration report in the 'reports' folder, named 'code_migration_report.md'. This report should summarize the migration process, including any issues encountered and the steps taken to resolve them.
- Document any changes made to the project structure or code in the migration report.
- Make the migration report human-readable and in markdown format. Use headings, bullet points, and other formatting options as appropriate.
- Suggest that the next step is to generate infrastructure files, and mention /phase3-generateinfra is the command to start the infra generation process.
- At the end, update the status report file with the status of the migration step.
