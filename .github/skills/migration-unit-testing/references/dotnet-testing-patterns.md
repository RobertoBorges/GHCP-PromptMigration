# .NET Testing Patterns

Load these examples only for a .NET target. Check package versions against the selected target framework and current package guidance before using them.

## .NET Testing Patterns (xUnit)

### Project Setup

```xml
<!-- Tests.csproj -->
<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <TargetFramework>net10.0</TargetFramework>
    <IsPackable>false</IsPackable>
    <Nullable>enable</Nullable>
  </PropertyGroup>

  <ItemGroup>
    <PackageReference Include="Microsoft.NET.Test.Sdk" Version="17.8.0" />
    <PackageReference Include="xunit" Version="2.6.2" />
    <PackageReference Include="xunit.runner.visualstudio" Version="2.5.4" />
    <PackageReference Include="Moq" Version="4.20.70" />
    <PackageReference Include="FluentAssertions" Version="6.12.0" />
    <PackageReference Include="Microsoft.AspNetCore.Mvc.Testing" Version="10.0.0" />
    <PackageReference Include="Microsoft.EntityFrameworkCore.InMemory" Version="10.0.0" />
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
