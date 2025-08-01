---
mode: agent
---
Set up comprehensive testing strategy for the migrated application

# Rules for Testing Setup
- Use `test_search` to locate existing test files and understand current testing patterns.
- Use `semantic_search` to identify code areas that need test coverage.
- Use `get_errors` to validate test compilation and execution.
- Create a comprehensive testing strategy that includes unit tests, integration tests, and end-to-end tests.
- Set up testing infrastructure compatible with the target Azure platform.

## Testing Strategy Implementation

### For .NET Applications:
- Set up modern testing frameworks (xUnit, NUnit, or MSTest)
- Create unit tests for business logic with high coverage
- Implement integration tests for:
  - Database operations with test databases
  - External API integrations
  - Authentication and authorization flows
  - Configuration management
- Set up API testing for REST endpoints using:
  - ASP.NET Core Test Host
  - WebApplicationFactory for integration testing
  - Postman/Newman collections for API testing
- Implement container testing if applicable
- Set up performance and load testing using:
  - Azure Load Testing service
  - NBomber or similar tools
- Configure test data management and cleanup

### For Java Applications:
- Set up modern testing frameworks (JUnit 5, TestNG)
- Create unit tests using Mockito for mocking
- Implement integration tests for:
  - Database operations with Testcontainers
  - External service integrations
  - Spring Boot application context testing
  - Security configurations
- Set up API testing for REST endpoints using:
  - Spring Boot Test
  - MockMvc for controller testing
  - RestTemplate/WebClient testing
- Implement container testing with Testcontainers
- Set up performance testing using JMeter or Gatling
- Configure test profiles and data management

## Test Environment Configuration

### Local Testing Setup:
- Configure test databases (in-memory, containerized, or dedicated test instances)
- Set up test configuration files separate from production
- Configure mock services for external dependencies
- Set up test data seeding and cleanup procedures
- Configure parallel test execution

### Azure Testing Integration:
- Set up Azure Test Plans integration if using Azure DevOps
- Configure Application Insights for test telemetry
- Set up test environments in Azure for integration testing
- Configure automated test execution in CI/CD pipelines
- Set up test result reporting and analysis

## Testing Best Practices Implementation:

### Test Coverage and Quality:
- Achieve minimum 80% code coverage for business logic
- Implement mutation testing to validate test quality
- Set up static code analysis for test code
- Configure test result reporting and metrics
- Implement test categorization (unit, integration, e2e)

### Security Testing:
- Implement security testing for authentication/authorization
- Set up vulnerability scanning in test pipelines
- Test for common security issues (OWASP Top 10)
- Validate secure configuration handling
- Test API security and input validation

### Performance Testing:
- Create load testing scenarios for expected traffic patterns
- Set up baseline performance metrics
- Configure performance regression testing
- Test auto-scaling behaviors
- Validate database performance under load

## Test Automation and CI/CD Integration:

### Test Pipeline Configuration:
- Set up automated test execution in build pipelines
- Configure test result publishing and analysis
- Set up test failure notifications
- Implement test retry mechanisms for flaky tests
- Configure parallel test execution for faster feedback

### Quality Gates:
- Set up quality gates based on test coverage
- Configure build failure on test failures
- Set up performance regression detection
- Implement security test validation gates
- Configure deployment approval based on test results

## Testing Documentation:

### Test Strategy Documentation:
- Document testing approach and methodologies
- Create test execution guides and procedures
- Document test data management strategies
- Create troubleshooting guides for test failures
- Document performance testing procedures and baselines

### Test Maintenance:
- Set up procedures for test maintenance and updates
- Document test environment setup and configuration
- Create guidelines for writing and maintaining tests
- Set up test code review processes
- Document testing tools and framework usage

## Deliverables:

- Generate a testing strategy report in the 'reports' folder, named 'testing_strategy_report.md', including:
  - Comprehensive testing approach and coverage strategy
  - Test frameworks and tools configuration
  - Test environment setup and management
  - Performance and security testing procedures
  - CI/CD integration and automation setup
  - Test maintenance and quality assurance procedures
  - Testing metrics and success criteria
  - Troubleshooting guides and best practices

- If testing setup fails at any step, provide detailed error analysis and alternative approaches.
- Make the testing report human-readable and in markdown format with clear sections and actionable guidance.
- Suggest that the next step is to set up CI/CD pipelines, and mention /phase8-setupcicd is the command to start the CI/CD setup process.
- At the end, update the status report file with the status of the testing setup step.
