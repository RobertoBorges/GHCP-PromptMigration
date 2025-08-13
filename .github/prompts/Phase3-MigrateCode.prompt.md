---
mode: agent
model: Claude Sonnet 3.7
tools: ['codebase', 'usages', 'vscodeAPI', 'think', 'problems', 'changes', 'testFailure', 'terminalSelection', 'terminalLastCommand', 'openSimpleBrowser', 'fetch', 'findTestFiles', 'searchResults', 'githubRepo', 'extensions', 'runTests', 'editFiles', 'runNotebooks', 'search', 'new', 'runCommands', 'runTasks', 'Microsoft Docs', 'Azure MCP']
---
Migrate application code to modern framework version compatible with Azure.

# Rules for Code Migration and Modernization
- Ensure appropriate Azure extensions for the target framework are installed in VS Code.
- Always start migration by creating a new folder with an intuitive name for the modernized project. Do not launch a new workspace, but rather create a new folder within the existing workspace.
- Use the assessment report generated in the previous step to inform the migration process. The assessment report can be found in the 'reports' folder.
- Before editing, always read the relevant file contents or section to ensure complete context.
- Use `semantic_search` to identify all code files that need migration.
- Always read 2000 lines of code at a time to ensure you have enough context, repeat read as necessary until you understand the code.
- If a patch is not applied correctly, attempt to reapply it.
- Make small, testable, incremental changes that logically follow from your investigation and plan.
- Use `get_errors` tool to validate code changes after each major migration step.
- Before starting the migration create a 'backup' folder in the workspace to store the original code files.
- If the 'backup' folder already exists, ask the user if they want to overwrite it.
- Use the guidance provided in #file:Code-Migration-Modernization.chatmode.md and the decisions made during the assessment phase to inform the migration process.
- Containerize the application if specified in the assessment report.
- Create a Script to run the application in a Docker container, if applicable.
- Create a Script to build and run the application on windows or Linux.
- Based on the assessed application type (.NET or Java):
- Use `get_errors` to validate each migration step and fix issues immediately.
- Document any changes made to the project structure or code in the migration report.
- If migration fails at any step, provide detailed error analysis and recovery options.
- Suggest that the next step is to generate infrastructure files, and mention `/phase4-generateinfra` is the command to start the infra generation process.
- At the end, update the status report file Reports/Report-Status.md with the status of the assessment step.


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

