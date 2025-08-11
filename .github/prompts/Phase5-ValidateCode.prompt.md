---
mode: agent
model: Claude Sonnet 3.7
tools: ['codebase', 'usages', 'vscodeAPI', 'think', 'problems', 'changes', 'testFailure', 'terminalSelection', 'terminalLastCommand', 'openSimpleBrowser', 'fetch', 'findTestFiles', 'searchResults', 'githubRepo', 'extensions', 'runTests', 'editFiles', 'runNotebooks', 'search', 'new', 'runCommands', 'runTasks']
---
Validate the migrated application code

# Rules for Code Validation
- Use `get_errors` tool to identify compilation and lint errors in the migrated code.
- Use `semantic_search` to find code patterns that may need additional modernization.
- Use `test_search` to locate and validate existing tests or create new test files.
- Validate the modernized application code against best practices for the target framework (.NET or Java).
- Run automated code analysis tools and security scanners if available.
- For .NET applications, validate against:
  - Modern .NET coding standards and patterns (async/await, nullable reference types, etc.)
  - Azure-compatible practices for configuration, authentication, and data access
  - REST API design principles (if WCF was migrated to REST)
  - Dependency injection usage and service lifetime management
  - Configuration management and secret handling
  - Logging implementation with structured logging
  - Cloud-native patterns (health checks, graceful shutdown, etc.)
  - Containerization best practices (if applicable)
  - Performance optimization (connection pooling, caching, etc.)
  - Security best practices (HTTPS, authentication, authorization)

- For Java applications, validate against:
  - Modern Java coding standards and patterns
  - Spring Boot or Jakarta EE best practices
  - Azure-compatible practices for configuration, authentication, and data access
  - REST API design principles (if SOAP was migrated to REST)
  - Dependency injection usage
  - Configuration management
  - Logging implementation
  - Cloud-native patterns
  - Containerization best practices (if applicable)

- Check the following aspects for both .NET and Java applications:
  - Framework compatibility with Azure services
  - Authentication implementation (Entra ID integration)
  - Configuration management (environment variables, externalized config, Key Vault integration)
  - Database access code compatibility with Azure databases
  - Error handling and logging patterns with proper correlation IDs
  - API design and documentation (OpenAPI/Swagger)
  - Performance considerations (async patterns, connection pooling)
  - Security best practices (input validation, output encoding, CSRF protection)
  - Testing coverage and quality (unit tests, integration tests)
  - Dependency management and vulnerability scanning
  - Container health checks and monitoring endpoints
  - Compliance with Azure Well-Architected Framework principles

- Generate a validation report in the 'reports' folder, named 'code_validation_report.md'. This report should summarize the validation results, including:
  - Compliance with framework best practices
  - Identified issues or concerns with severity levels (Critical, High, Medium, Low)
  - Recommendations for further improvements with actionable steps
  - Migration quality score (percentage of successful migration aspects)
  - List of items that pass validation
  - List of items that require attention with remediation steps
  - Performance analysis and optimization opportunities
  - Security assessment results
  - Testing coverage analysis
  - Code quality metrics
  - Azure compatibility assessment

- If the validation fails for critical items, provide detailed error messages and step-by-step resolution guidance.
- If validation identifies security vulnerabilities, prioritize them and provide immediate remediation steps.
- If the validation passes or has only minor issues, indicate that the code is ready for deployment.
- Include automated test execution results if tests are available.
- Provide specific recommendations for load testing and performance optimization.
- Make the validation report human-readable and in markdown format, using headings, bullet points, and color coding for severity levels.
- Validation state must be one of: Success, Warning (with minor issues), Failed, or Could Not Validate.
- If the validate prompt is called before code migration has been performed, create a report stating that validation cannot be performed since migration has not started yet.
- If the user runs Validate again, ask if they want to overwrite the existing report. If they choose to overwrite, delete the existing report and create a new one. If they choose not to overwrite, ask if they want to create the report in a new file instead and act accordingly.
- Suggest that the next step is to validate the infrastructure files, and mention /phase6-validateinfra is the command to start the infrastructure validation process.
- At the end, update the status report file Reports/Report-Status.md with the status of the assessment step.
