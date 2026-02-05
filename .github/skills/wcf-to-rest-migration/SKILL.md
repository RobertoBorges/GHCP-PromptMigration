---
name: wcf-to-rest-migration
description: |
  WCF to REST API migration patterns for .NET modernization.
  **Use when:** Converting WCF services to ASP.NET Core REST APIs.
  **Triggers on:** .svc files, ServiceContract attributes, OperationContract, DataContract, WCF bindings.
  **Covers:** ServiceContract to controllers, DataContract to DTOs, FaultContract to Problem Details, OpenAPI generation.
  **Important:** This is a rewrite, not a compatibility layer. Existing WCF clients will need updates.
---

# WCF to REST Migration Skill

Use this skill when migrating WCF (Windows Communication Foundation) services to ASP.NET Core REST APIs.

## When to Use This Skill

- Converting WCF ServiceContracts to REST controllers
- Transforming DataContracts to DTOs
- Migrating SOAP operations to HTTP methods
- Generating OpenAPI/Swagger documentation
- Handling WCF bindings and endpoints
- Converting WCF error handling to REST problem details

## WCF to REST Mapping Overview

| WCF Concept | REST Equivalent |
|-------------|-----------------|
| `ServiceContract` | `[ApiController]` class |
| `OperationContract` | Controller action method |
| `DataContract` | DTO class |
| `DataMember` | Public property |
| `FaultContract` | Problem Details (RFC 7807) |
| `MessageContract` | Request/Response DTOs |
| WSDL | OpenAPI/Swagger specification |
| Bindings | HTTP/HTTPS endpoints |

## HTTP Method Mapping

| WCF Operation Pattern | HTTP Method | Example |
|----------------------|-------------|---------|
| `GetXxx`, `FindXxx`, `SearchXxx` | GET | `GET /api/users/{id}` |
| `CreateXxx`, `AddXxx`, `InsertXxx` | POST | `POST /api/users` |
| `UpdateXxx`, `ModifyXxx`, `EditXxx` | PUT | `PUT /api/users/{id}` |
| `PatchXxx`, `PartialUpdateXxx` | PATCH | `PATCH /api/users/{id}` |
| `DeleteXxx`, `RemoveXxx` | DELETE | `DELETE /api/users/{id}` |

## ServiceContract to Controller Conversion

### WCF Service Contract

```csharp
// Legacy WCF
[ServiceContract(Namespace = "http://mycompany.com/services")]
public interface IUserService
{
    [OperationContract]
    User GetUser(int userId);
    
    [OperationContract]
    List<User> GetAllUsers();
    
    [OperationContract]
    int CreateUser(User user);
    
    [OperationContract]
    void UpdateUser(User user);
    
    [OperationContract]
    void DeleteUser(int userId);
    
    [OperationContract]
    List<User> SearchUsers(UserSearchCriteria criteria);
}
```

### ASP.NET Core REST Controller

```csharp
// Modern REST API
[ApiController]
[Route("api/[controller]")]
[Produces("application/json")]
public class UsersController : ControllerBase
{
    private readonly IUserService _userService;
    private readonly ILogger<UsersController> _logger;
    
    public UsersController(IUserService userService, ILogger<UsersController> logger)
    {
        _userService = userService;
        _logger = logger;
    }
    
    /// <summary>
    /// Gets a user by ID
    /// </summary>
    [HttpGet("{id:int}")]
    [ProducesResponseType(typeof(UserDto), StatusCodes.Status200OK)]
    [ProducesResponseType(StatusCodes.Status404NotFound)]
    public async Task<ActionResult<UserDto>> GetUser(int id)
    {
        var user = await _userService.GetByIdAsync(id);
        if (user == null)
            return NotFound();
        return Ok(user);
    }
    
    /// <summary>
    /// Gets all users
    /// </summary>
    [HttpGet]
    [ProducesResponseType(typeof(IEnumerable<UserDto>), StatusCodes.Status200OK)]
    public async Task<ActionResult<IEnumerable<UserDto>>> GetAllUsers()
    {
        var users = await _userService.GetAllAsync();
        return Ok(users);
    }
    
    /// <summary>
    /// Creates a new user
    /// </summary>
    [HttpPost]
    [ProducesResponseType(typeof(UserDto), StatusCodes.Status201Created)]
    [ProducesResponseType(StatusCodes.Status400BadRequest)]
    public async Task<ActionResult<UserDto>> CreateUser([FromBody] CreateUserDto dto)
    {
        var user = await _userService.CreateAsync(dto);
        return CreatedAtAction(nameof(GetUser), new { id = user.Id }, user);
    }
    
    /// <summary>
    /// Updates an existing user
    /// </summary>
    [HttpPut("{id:int}")]
    [ProducesResponseType(StatusCodes.Status204NoContent)]
    [ProducesResponseType(StatusCodes.Status404NotFound)]
    public async Task<IActionResult> UpdateUser(int id, [FromBody] UpdateUserDto dto)
    {
        var exists = await _userService.UpdateAsync(id, dto);
        if (!exists)
            return NotFound();
        return NoContent();
    }
    
    /// <summary>
    /// Deletes a user
    /// </summary>
    [HttpDelete("{id:int}")]
    [ProducesResponseType(StatusCodes.Status204NoContent)]
    [ProducesResponseType(StatusCodes.Status404NotFound)]
    public async Task<IActionResult> DeleteUser(int id)
    {
        var deleted = await _userService.DeleteAsync(id);
        if (!deleted)
            return NotFound();
        return NoContent();
    }
    
    /// <summary>
    /// Searches users with criteria
    /// </summary>
    [HttpGet("search")]
    [ProducesResponseType(typeof(IEnumerable<UserDto>), StatusCodes.Status200OK)]
    public async Task<ActionResult<IEnumerable<UserDto>>> SearchUsers(
        [FromQuery] UserSearchCriteriaDto criteria)
    {
        var users = await _userService.SearchAsync(criteria);
        return Ok(users);
    }
}
```

## DataContract to DTO Conversion

### WCF DataContract

```csharp
// Legacy WCF
[DataContract(Namespace = "http://mycompany.com/data")]
public class User
{
    [DataMember(Name = "UserId", Order = 1)]
    public int Id { get; set; }
    
    [DataMember(Name = "UserName", Order = 2, IsRequired = true)]
    public string Name { get; set; }
    
    [DataMember(Order = 3)]
    public string Email { get; set; }
    
    [DataMember(Order = 4)]
    public DateTime? CreatedDate { get; set; }
}
```

### Modern DTO

```csharp
// Modern DTO with validation
public record UserDto(
    int Id,
    string Name,
    string Email,
    DateTime? CreatedDate
);

public record CreateUserDto(
    [Required] [StringLength(100)] string Name,
    [Required] [EmailAddress] string Email
);

public record UpdateUserDto(
    [Required] [StringLength(100)] string Name,
    [EmailAddress] string Email
);
```

## FaultContract to Problem Details

### WCF Fault Handling

```csharp
// Legacy WCF
[DataContract]
public class ServiceFault
{
    [DataMember]
    public string ErrorCode { get; set; }
    
    [DataMember]
    public string Message { get; set; }
}

[ServiceContract]
public interface IUserService
{
    [OperationContract]
    [FaultContract(typeof(ServiceFault))]
    User GetUser(int userId);
}

// Throwing fault
throw new FaultException<ServiceFault>(
    new ServiceFault { ErrorCode = "USER_NOT_FOUND", Message = "User not found" });
```

### REST Problem Details (RFC 7807)

```csharp
// Modern exception handling
public class UserNotFoundException : Exception
{
    public int UserId { get; }
    public UserNotFoundException(int userId) : base($"User {userId} not found")
    {
        UserId = userId;
    }
}

// Global exception handler
public class GlobalExceptionHandler : IExceptionHandler
{
    public async ValueTask<bool> TryHandleAsync(
        HttpContext context,
        Exception exception,
        CancellationToken cancellationToken)
    {
        var problemDetails = exception switch
        {
            UserNotFoundException ex => new ProblemDetails
            {
                Status = StatusCodes.Status404NotFound,
                Title = "User Not Found",
                Detail = ex.Message,
                Type = "https://api.mycompany.com/errors/user-not-found",
                Extensions = { ["userId"] = ex.UserId }
            },
            ValidationException ex => new ProblemDetails
            {
                Status = StatusCodes.Status400BadRequest,
                Title = "Validation Error",
                Detail = ex.Message
            },
            _ => new ProblemDetails
            {
                Status = StatusCodes.Status500InternalServerError,
                Title = "Internal Server Error"
            }
        };
        
        context.Response.StatusCode = problemDetails.Status ?? 500;
        await context.Response.WriteAsJsonAsync(problemDetails, cancellationToken);
        return true;
    }
}

// Register in Program.cs
builder.Services.AddExceptionHandler<GlobalExceptionHandler>();
builder.Services.AddProblemDetails();
```

## OpenAPI/Swagger Setup

```csharp
// Program.cs
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen(options =>
{
    options.SwaggerDoc("v1", new OpenApiInfo
    {
        Title = "User Service API",
        Version = "v1",
        Description = "Migrated from WCF UserService"
    });
    
    // Include XML comments
    var xmlFile = $"{Assembly.GetExecutingAssembly().GetName().Name}.xml";
    options.IncludeXmlComments(Path.Combine(AppContext.BaseDirectory, xmlFile));
});

// Middleware
app.UseSwagger();
app.UseSwaggerUI();
```

## Common Migration Challenges

| WCF Feature | REST Solution |
|-------------|---------------|
| Duplex communication | SignalR or WebSockets |
| Reliable messaging | Azure Service Bus |
| Transactions | Saga pattern or outbox pattern |
| Session state | Stateless + external cache (Redis) |
| MTOM attachments | Multipart/form-data uploads |
| WS-Security | OAuth 2.0 / JWT Bearer |

## Template Files

- [SampleController.cs](./templates/SampleController.cs) - REST controller template
- [SampleDtos.cs](./templates/SampleDtos.cs) - DTO examples with validation
- [GlobalExceptionHandler.cs](./templates/GlobalExceptionHandler.cs) - Exception to Problem Details

## Migration Checklist

- [ ] Identify all ServiceContracts and OperationContracts
- [ ] Map operations to HTTP methods
- [ ] Convert DataContracts to DTOs
- [ ] Add validation attributes to DTOs
- [ ] Implement global exception handling
- [ ] Generate OpenAPI documentation
- [ ] Update client code to use HttpClient
- [ ] Test all endpoints with Swagger UI
- [ ] Update authentication to JWT/OAuth
- [ ] Remove WCF dependencies from project
