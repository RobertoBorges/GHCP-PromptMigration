---
name: migration-unit-testing
description: |
  Unit testing patterns for validating migrated applications.
  **Use when:** Creating tests to verify migration correctness and prevent regressions.
  **Triggers on:** Test creation requests, validation phase, post-migration verification.
  **Covers:** xUnit/NUnit for .NET, JUnit 5 for Java, mocking strategies, test organization patterns.
---

# Migration Unit Testing Skill

Use this skill when creating unit tests to validate migrated applications work correctly after modernization.

## When to Use This Skill

- Creating tests to validate migration correctness
- Building test suites for migrated .NET or Java applications
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

## .NET Testing Patterns (xUnit)

### Project Setup

```xml
<!-- Tests.csproj -->
<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <TargetFramework>net8.0</TargetFramework>
    <IsPackable>false</IsPackable>
    <Nullable>enable</Nullable>
  </PropertyGroup>

  <ItemGroup>
    <PackageReference Include="Microsoft.NET.Test.Sdk" Version="17.8.0" />
    <PackageReference Include="xunit" Version="2.6.2" />
    <PackageReference Include="xunit.runner.visualstudio" Version="2.5.4" />
    <PackageReference Include="Moq" Version="4.20.70" />
    <PackageReference Include="FluentAssertions" Version="6.12.0" />
    <PackageReference Include="Microsoft.AspNetCore.Mvc.Testing" Version="8.0.0" />
    <PackageReference Include="Microsoft.EntityFrameworkCore.InMemory" Version="8.0.0" />
  </ItemGroup>
</Project>
```

### Test Naming Convention

```
MethodName_Scenario_ExpectedBehavior
```

Examples:
- `GetUser_WithValidId_ReturnsUser`
- `CreateOrder_WithInvalidItems_ThrowsValidationException`
- `CalculateDiscount_WhenTotalExceeds100_Returns10Percent`

### Service Layer Test

```csharp
public class UserServiceTests
{
    private readonly Mock<IUserRepository> _repositoryMock;
    private readonly Mock<ILogger<UserService>> _loggerMock;
    private readonly UserService _sut; // System Under Test
    
    public UserServiceTests()
    {
        _repositoryMock = new Mock<IUserRepository>();
        _loggerMock = new Mock<ILogger<UserService>>();
        _sut = new UserService(_repositoryMock.Object, _loggerMock.Object);
    }
    
    [Fact]
    public async Task GetByIdAsync_WithExistingUser_ReturnsUser()
    {
        // Arrange
        var expectedUser = new User { Id = 1, Name = "John Doe", Email = "john@example.com" };
        _repositoryMock
            .Setup(r => r.GetByIdAsync(1))
            .ReturnsAsync(expectedUser);
        
        // Act
        var result = await _sut.GetByIdAsync(1);
        
        // Assert
        result.Should().NotBeNull();
        result.Should().BeEquivalentTo(expectedUser);
    }
    
    [Fact]
    public async Task GetByIdAsync_WithNonExistingUser_ReturnsNull()
    {
        // Arrange
        _repositoryMock
            .Setup(r => r.GetByIdAsync(It.IsAny<int>()))
            .ReturnsAsync((User?)null);
        
        // Act
        var result = await _sut.GetByIdAsync(999);
        
        // Assert
        result.Should().BeNull();
    }
    
    [Theory]
    [InlineData("")]
    [InlineData(" ")]
    [InlineData(null)]
    public async Task CreateAsync_WithInvalidName_ThrowsArgumentException(string? invalidName)
    {
        // Arrange
        var dto = new CreateUserDto(invalidName!, "test@example.com");
        
        // Act
        var act = () => _sut.CreateAsync(dto);
        
        // Assert
        await act.Should().ThrowAsync<ArgumentException>()
            .WithMessage("*name*");
    }
}
```

### Controller Integration Test

```csharp
public class UsersControllerTests : IClassFixture<WebApplicationFactory<Program>>
{
    private readonly HttpClient _client;
    private readonly WebApplicationFactory<Program> _factory;
    
    public UsersControllerTests(WebApplicationFactory<Program> factory)
    {
        _factory = factory.WithWebHostBuilder(builder =>
        {
            builder.ConfigureServices(services =>
            {
                // Replace real DB with in-memory
                var descriptor = services.SingleOrDefault(
                    d => d.ServiceType == typeof(DbContextOptions<AppDbContext>));
                if (descriptor != null)
                    services.Remove(descriptor);
                
                services.AddDbContext<AppDbContext>(options =>
                    options.UseInMemoryDatabase("TestDb"));
            });
        });
        _client = _factory.CreateClient();
    }
    
    [Fact]
    public async Task GetUsers_ReturnsSuccessAndCorrectContentType()
    {
        // Act
        var response = await _client.GetAsync("/api/users");
        
        // Assert
        response.EnsureSuccessStatusCode();
        response.Content.Headers.ContentType?.MediaType.Should().Be("application/json");
    }
    
    [Fact]
    public async Task GetUser_WithInvalidId_ReturnsNotFound()
    {
        // Act
        var response = await _client.GetAsync("/api/users/99999");
        
        // Assert
        response.StatusCode.Should().Be(HttpStatusCode.NotFound);
    }
    
    [Fact]
    public async Task CreateUser_WithValidData_ReturnsCreatedWithLocation()
    {
        // Arrange
        var newUser = new { Name = "Jane Doe", Email = "jane@example.com" };
        var content = new StringContent(
            JsonSerializer.Serialize(newUser),
            Encoding.UTF8,
            "application/json");
        
        // Act
        var response = await _client.PostAsync("/api/users", content);
        
        // Assert
        response.StatusCode.Should().Be(HttpStatusCode.Created);
        response.Headers.Location.Should().NotBeNull();
    }
}
```

### Database Test with In-Memory Provider

```csharp
public class UserRepositoryTests : IDisposable
{
    private readonly AppDbContext _context;
    private readonly UserRepository _sut;
    
    public UserRepositoryTests()
    {
        var options = new DbContextOptionsBuilder<AppDbContext>()
            .UseInMemoryDatabase(Guid.NewGuid().ToString())
            .Options;
        _context = new AppDbContext(options);
        _sut = new UserRepository(_context);
    }
    
    [Fact]
    public async Task AddAsync_AddsUserToDatabase()
    {
        // Arrange
        var user = new User { Name = "Test User", Email = "test@example.com" };
        
        // Act
        await _sut.AddAsync(user);
        await _context.SaveChangesAsync();
        
        // Assert
        var savedUser = await _context.Users.FirstOrDefaultAsync(u => u.Email == "test@example.com");
        savedUser.Should().NotBeNull();
        savedUser!.Name.Should().Be("Test User");
    }
    
    public void Dispose() => _context.Dispose();
}
```

## Java Testing Patterns (JUnit 5)

### Project Setup (pom.xml)

```xml
<dependencies>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-test</artifactId>
        <scope>test</scope>
    </dependency>
    <dependency>
        <groupId>org.mockito</groupId>
        <artifactId>mockito-junit-jupiter</artifactId>
        <scope>test</scope>
    </dependency>
    <dependency>
        <groupId>org.assertj</groupId>
        <artifactId>assertj-core</artifactId>
        <scope>test</scope>
    </dependency>
    <dependency>
        <groupId>com.h2database</groupId>
        <artifactId>h2</artifactId>
        <scope>test</scope>
    </dependency>
</dependencies>
```

### Service Layer Test

```java
@ExtendWith(MockitoExtension.class)
class UserServiceTest {
    
    @Mock
    private UserRepository userRepository;
    
    @InjectMocks
    private UserService userService;
    
    @Test
    @DisplayName("Should return user when valid ID provided")
    void findById_WithValidId_ReturnsUser() {
        // Given
        User expectedUser = new User(1L, "John Doe", "john@example.com");
        when(userRepository.findById(1L)).thenReturn(Optional.of(expectedUser));
        
        // When
        Optional<User> result = userService.findById(1L);
        
        // Then
        assertThat(result)
            .isPresent()
            .hasValueSatisfying(user -> {
                assertThat(user.getName()).isEqualTo("John Doe");
                assertThat(user.getEmail()).isEqualTo("john@example.com");
            });
    }
    
    @Test
    @DisplayName("Should return empty when user not found")
    void findById_WithNonExistingId_ReturnsEmpty() {
        // Given
        when(userRepository.findById(anyLong())).thenReturn(Optional.empty());
        
        // When
        Optional<User> result = userService.findById(999L);
        
        // Then
        assertThat(result).isEmpty();
    }
    
    @ParameterizedTest
    @NullAndEmptySource
    @ValueSource(strings = {" ", "   "})
    @DisplayName("Should throw exception for invalid name")
    void create_WithInvalidName_ThrowsException(String invalidName) {
        // Given
        CreateUserDto dto = new CreateUserDto(invalidName, "test@example.com");
        
        // When/Then
        assertThatThrownBy(() -> userService.create(dto))
            .isInstanceOf(IllegalArgumentException.class)
            .hasMessageContaining("name");
    }
}
```

### Controller Integration Test

```java
@SpringBootTest
@AutoConfigureMockMvc
class UserControllerIntegrationTest {
    
    @Autowired
    private MockMvc mockMvc;
    
    @Autowired
    private ObjectMapper objectMapper;
    
    @Test
    @DisplayName("GET /api/users should return OK")
    void getUsers_ReturnsOk() throws Exception {
        mockMvc.perform(get("/api/users"))
            .andExpect(status().isOk())
            .andExpect(content().contentType(MediaType.APPLICATION_JSON));
    }
    
    @Test
    @DisplayName("GET /api/users/{id} with invalid ID should return 404")
    void getUser_WithInvalidId_ReturnsNotFound() throws Exception {
        mockMvc.perform(get("/api/users/99999"))
            .andExpect(status().isNotFound());
    }
    
    @Test
    @DisplayName("POST /api/users with valid data should return 201")
    void createUser_WithValidData_ReturnsCreated() throws Exception {
        CreateUserDto dto = new CreateUserDto("Jane Doe", "jane@example.com");
        
        mockMvc.perform(post("/api/users")
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(dto)))
            .andExpect(status().isCreated())
            .andExpect(header().exists("Location"));
    }
}
```

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

- [templates/dotnet/TestBase.cs](./templates/dotnet/TestBase.cs) - .NET test base class
- [templates/dotnet/SampleServiceTests.cs](./templates/dotnet/SampleServiceTests.cs) - Service test examples
- [templates/dotnet/SampleControllerTests.cs](./templates/dotnet/SampleControllerTests.cs) - Controller test examples
- [templates/java/TestBase.java](./templates/java/TestBase.java) - Java test base class
- [templates/java/SampleServiceTest.java](./templates/java/SampleServiceTest.java) - Service test examples

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
