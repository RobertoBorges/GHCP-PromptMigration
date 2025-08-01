---
mode: agent
---
Validate the migrated application code

# Rules for Code Validation
- Validate the modernized application code against best practices for the target framework (.NET or Java).
- For .NET applications, validate against:
  - Modern .NET coding standards and patterns
  - Azure-compatible practices for configuration, authentication, and data access
  - REST API design principles (if WCF was migrated to REST)
  - Dependency injection usage
  - Configuration management
  - Logging implementation
  - Cloud-native patterns
  - Containerization best practices (if applicable)

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
  - Framework compatibility with Azure
  - Authentication implementation (Entra ID integration)
  - Configuration management (environment variables, externalized config)
  - Database access code compatibility with Azure databases
  - Error handling and logging patterns
  - API design (if applicable)
  - Performance considerations
  - Security best practices

- Generate a validation report in the 'reports' folder, named 'code_validation_report.md'. This report should summarize the validation results, including:
  - Compliance with framework best practices
  - Identified issues or concerns
  - Recommendations for further improvements
  - Migration quality score (percentage of successful migration aspects)
  - List of items that pass validation
  - List of items that require attention

- If the validation fails for critical items, provide detailed error messages and suggestions for fixing the issues.
- If the validation passes or has only minor issues, indicate that the code is ready for deployment.
- Make the validation report human-readable and in markdown format, using headings, bullet points, and other formatting options to make it easy to read.
- Validation state must be one of: Success, Warning (with minor issues), Failed, or Could Not Validate.
- If the validate prompt is called before code migration has been performed, create a report stating that validation cannot be performed since migration has not started yet.
- If the user runs Validate again, ask if they want to overwrite the existing report. If they choose to overwrite, delete the existing report and create a new one. If they choose not to overwrite, ask if they want to create the report in a new file instead and act accordingly.
- Suggest that the next step is to validate the infrastructure files, and mention /phase5-validateinfra is the command to start the infrastructure validation process.
- At the end, update the status report file with the status of the code validation step.
