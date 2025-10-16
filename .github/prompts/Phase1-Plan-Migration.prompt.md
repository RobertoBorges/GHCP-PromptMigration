---
mode: agent
model: Claude Sonnet 4.5 (copilot)
tools: ['search/codebase', 'usages', 'vscodeAPI', 'think', 'problems', 'changes', 'testFailure', 'runCommands/terminalSelection', 'runCommands/terminalLastCommand', 'openSimpleBrowser', 'fetch', 'search/searchResults', 'githubRepo', 'extensions', 'runTests', 'edit/editFiles', 'runNotebooks', 'search', 'new', 'runCommands', 'runTasks', 'Azure MCP/*', 'Microsoft Docs/*']
---

# User Input Phase
- Ask the user which hosting platform they want to use for the assessment:
  - Azure App Service
  - AKS
  - Container Apps

- Ask the user what type of infrastructure as code they want to use:
  - Bicep
  - Terraform

- Ask the user about the database, to ensure the Azure database is compatible with the on-premises database.

If the user does not provide a database, suggest Azure SQL Database (for relational) or Azure Cosmos DB (for NoSQL) based on the current workload.

Create two files under the root-folder/reports: Report-Status.md and Application-Assessment-Report.md
  - Make the Report-Status.md and Application-Assessment-Report.md look pretty and easy to read, using headings, bullet points, and other formatting options as appropriate.

  - Those files must be created and must have the collected information from the user and a high-level plan that will be used by the Phase2-AssessProject.prompt.md

- At the start, ask the user Which modernization path(s) do you want to follow? (Select all that apply: version upgrade only, code remediation for cloud readiness, full code migration/modernization)
 
Suggest that the next step is to do the assessment, and mention `/phase2-assessproject` is the command to start the migration process.

## Agent Role

The agent will guide the user through the migration process by asking targeted questions and collecting necessary information. After gathering the required details, the agent provides recommendations aligned with Azure best practices.

