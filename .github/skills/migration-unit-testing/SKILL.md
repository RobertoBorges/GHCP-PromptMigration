---
name: migration-unit-testing
description: |
  Unit testing patterns for validating migrated applications.
  **Use when:** Creating tests to verify migration correctness and prevent regressions.
  **Triggers on:** Test creation requests, validation phase, post-migration verification.
  **Covers:** xUnit/NUnit for .NET, JUnit 5 for Java, mocking strategies, test organization patterns.
user-invocable: false
---

# Migration Unit Testing Skill

Use this skill when creating unit tests to validate migrated applications work correctly after modernization.

## When to Use This Skill

- Creating tests to validate migration correctness
- Building test suites for migrated applications of any stack (`.NET`, `Java`, `Python`, `Node.js`, `PHP`, `Ruby`, `Go`, etc.). This skill ships worked examples for .NET and Java; adapt the same patterns to other stacks using their idiomatic test frameworks (pytest for Python, jest/vitest for Node, phpunit for PHP, rspec for Ruby, testing package for Go, etc.).
- Implementing equivalence testing (old vs new behavior)
- Setting up mocking for external dependencies
- Creating regression tests for business logic
- Establishing test coverage baselines

## Testing Strategy for Migrated Applications

### Priority Order

1. **Business Logic** - Critical calculations, validations, workflows
2. **Data Access** - Repository operations, query correctness
3. **API Endpoints** - Request/response contracts, status codes
4. **Authentication/Authorization** - Security flows
5. **Integrations** - External service interactions
6. **UI Components** - View models, presentation logic

### Coverage Goals

| Code Area | Minimum Coverage | Target Coverage |
|-----------|------------------|-----------------|
| Business logic | 80% | 90%+ |
| API controllers | 70% | 85% |
| Data access | 60% | 80% |
| Utilities/helpers | 70% | 90% |

## Language-Specific Test Patterns

Load only the reference for the selected target stack, and verify its package versions before use:

- [.NET and xUnit examples](./references/dotnet-testing-patterns.md)
- [Java and JUnit examples](./references/java-testing-patterns.md)

## Migration-Specific Test Scenarios

### API Equivalence Test

```csharp
/// <summary>
/// Compares responses from legacy and migrated APIs to ensure equivalence
/// </summary>
public class ApiEquivalenceTests
{
    private readonly HttpClient _legacyClient;
    private readonly HttpClient _modernClient;
    
    [Fact]
    public async Task GetUsers_ResponseMatchesLegacyApi()
    {
        // Get responses from both APIs
        var legacyResponse = await _legacyClient.GetAsync("/api/users");
        var modernResponse = await _modernClient.GetAsync("/api/users");
        
        // Parse responses
        var legacyUsers = await legacyResponse.Content.ReadFromJsonAsync<List<LegacyUserDto>>();
        var modernUsers = await modernResponse.Content.ReadFromJsonAsync<List<UserDto>>();
        
        // Compare (accounting for known differences)
        modernUsers.Should().HaveCount(legacyUsers!.Count);
        
        for (int i = 0; i < legacyUsers.Count; i++)
        {
            modernUsers![i].Id.Should().Be(legacyUsers[i].UserId);
            modernUsers[i].Name.Should().Be(legacyUsers[i].UserName);
            modernUsers[i].Email.Should().Be(legacyUsers[i].Email);
        }
    }
}
```

### Business Logic Validation Test

```csharp
/// <summary>
/// Tests that business calculations remain correct after migration
/// </summary>
public class BusinessLogicValidationTests
{
    [Theory]
    [InlineData(100, 0)]      // No discount under threshold
    [InlineData(150, 15)]     // 10% discount
    [InlineData(500, 75)]     // 15% discount for large orders
    [InlineData(1000, 200)]   // 20% discount for very large orders
    public void CalculateDiscount_MatchesLegacyBehavior(decimal orderTotal, decimal expectedDiscount)
    {
        // Arrange
        var calculator = new DiscountCalculator();
        
        // Act
        var actualDiscount = calculator.Calculate(orderTotal);
        
        // Assert - these values were captured from the legacy system
        actualDiscount.Should().Be(expectedDiscount);
    }
}
```

## Template Files

- [templates/dotnet/UnitTestExamples.cs](./templates/dotnet/UnitTestExamples.cs) - .NET unit test examples
- [templates/dotnet/IntegrationTestBase.cs](./templates/dotnet/IntegrationTestBase.cs) - .NET integration test base class
- [templates/java/TestExamples.java](./templates/java/TestExamples.java) - Java test examples

## Test Execution Commands

### .NET
```bash
# Run all tests
dotnet test

# Run with coverage
dotnet test --collect:"XPlat Code Coverage"

# Run specific test class
dotnet test --filter "FullyQualifiedName~UserServiceTests"
```

### Java
```bash
# Run all tests
mvn test

# Run with coverage
mvn test jacoco:report

# Run specific test class
mvn test -Dtest=UserServiceTest
```

## Migration Testing Checklist

- [ ] All critical business logic has test coverage
- [ ] API endpoints return correct status codes
- [ ] Data transformations preserve values
- [ ] Error handling produces expected results
- [ ] Authentication/authorization works correctly
- [ ] Database operations succeed
- [ ] External service mocks are in place
- [ ] Performance is within acceptable bounds
- [ ] Tests pass in CI/CD pipeline
