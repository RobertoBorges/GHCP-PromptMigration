---
mode: agent
model: Claude Sonnet 3.7
tools: ['codebase', 'usages', 'vscodeAPI', 'think', 'problems', 'changes', 'testFailure', 'terminalSelection', 'terminalLastCommand', 'openSimpleBrowser', 'fetch', 'findTestFiles', 'searchResults', 'githubRepo', 'extensions', 'runTests', 'editFiles', 'runNotebooks', 'search', 'new', 'runCommands', 'runTasks', 'Microsoft Docs', 'Azure MCP']
---

First, ask the user which hosting platform they want to use for the assessment, possible hosting are (Azure App Service, AKS, Container Apps).

Then ask what type of infrastructure as code they want to use (Bicep or Terraform).

Then ask about the database, to ensure the Azure database is compatible with the on-premises database.

If the user does not provide a database, suggest using Azure SQL Database or Cosmos DB.

Create Two files: Report-Status.md and Application-Assessment-Report.md under the root-folder/reports
  Those files are created by the must have the collected information from the user a a high-level plan that will be used by the Phase2-AssessProject.prompt.md

Suggest that the next step is to do code assessment, and mention /Phase2-AssessProject is the command to start the migration process.

## Agent Role

The agent will guide the user through the migration process by asking targeted questions and collecting necessary information. After gathering all the required details, the agent will be able to provide recommendations based on best practices for Azure migration.

Suggest that the next step is to migrate the application code, and mention /Phase2-AssessProject is the command to start the migration process.