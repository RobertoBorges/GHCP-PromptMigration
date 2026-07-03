# WCF to REST Migration Quick Reference

## Attribute Mapping

| WCF Attribute | REST Equivalent |
|--------------|-----------------|
| `[ServiceContract]` | `[ApiController]` |
| `[OperationContract]` | `[HttpGet]`, `[HttpPost]`, `[HttpPut]`, `[HttpDelete]` |
| `[DataContract]` | `record` or `class` with validation attributes |
| `[DataMember]` | Property (auto-included in JSON) |
| `[FaultContract]` | `ProblemDetails` return type |
| `[ServiceBehavior]` | Middleware + DI configuration |
| `[WebGet]` | `[HttpGet]` |
| `[WebInvoke]` | `[HttpPost]`, `[HttpPut]`, `[HttpDelete]` |

## HTTP Method Selection

| WCF Pattern | HTTP Method | Route Example |
|-------------|-------------|---------------|
| `GetItem(id)` | GET | `/api/items/{id}` |
| `GetItems()` | GET | `/api/items` |
| `CreateItem(item)` | POST | `/api/items` |
| `UpdateItem(item)` | PUT | `/api/items/{id}` |
| `DeleteItem(id)` | DELETE | `/api/items/{id}` |
| `SearchItems(criteria)` | GET | `/api/items?field=value` |
| `ProcessAction(id, action)` | POST | `/api/items/{id}/actions/{action}` |

## Response Patterns

### Success Responses

```csharp
// GET single item
return Ok(item);                           // 200 OK

// GET collection
return Ok(items);                          // 200 OK

// POST create
return CreatedAtAction(nameof(Get), 
    new { id = item.Id }, item);           // 201 Created

// PUT update
return Ok(item);                           // 200 OK
// or
return NoContent();                        // 204 No Content

// DELETE
return NoContent();                        // 204 No Content
```

### Error Responses

```csharp
// Not found
return NotFound(new ProblemDetails { ... }); // 404

// Bad request
return BadRequest(new ProblemDetails { ... }); // 400

// Validation error
return ValidationProblem(ModelState);      // 400

// Unauthorized
return Unauthorized();                     // 401

// Forbidden
return Forbid();                           // 403

// Conflict
return Conflict(new ProblemDetails { ... }); // 409
```

## Service Registration (Program.cs)

```csharp
// Replace WCF ServiceHost configuration

var builder = WebApplication.CreateBuilder(args);

// Add services (replaces WCF service instantiation)
builder.Services.AddScoped<IProductService, ProductService>();
builder.Services.AddScoped<IOrderService, OrderService>();

// Add exception handling (replaces FaultContract)
builder.Services.AddGlobalExceptionHandler();

// Add controllers
builder.Services.AddControllers();

// Add OpenAPI (replaces WSDL)
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();

var app = builder.Build();

// Configure pipeline
app.UseGlobalExceptionHandler();
app.UseSwagger();
app.UseSwaggerUI();
app.UseHttpsRedirection();
app.UseAuthorization();
app.MapControllers();

app.Run();
```

## Common Migration Tasks

### 1. Convert DataContract to DTO

**WCF:**
```csharp
[DataContract]
public class Product
{
    [DataMember]
    public int Id { get; set; }
    
    [DataMember(IsRequired = true)]
    public string Name { get; set; }
}
```

**REST:**
```csharp
public record ProductDto
{
    public int Id { get; init; }
    
    [Required]
    [StringLength(200)]
    public string Name { get; init; } = string.Empty;
}
```

### 2. Convert FaultContract to ProblemDetails

**WCF:**
```csharp
[FaultContract(typeof(ServiceFault))]
Product GetProduct(int id);

// Throwing fault
throw new FaultException<ServiceFault>(
    new ServiceFault { Message = "Not found" });
```

**REST:**
```csharp
[ProducesResponseType(typeof(ProblemDetails), 404)]
public async Task<ActionResult<ProductDto>> GetById(int id)
{
    // Throw custom exception (handled by middleware)
    throw new NotFoundException("Product", id.ToString());
}
```

### 3. Replace ServiceLocator with DI

**WCF:**
```csharp
public class ProductService : IProductService
{
    public Product GetProduct(int id)
    {
        var repository = ServiceLocator.Get<IProductRepository>();
        return repository.Get(id);
    }
}
```

**REST:**
```csharp
public class ProductService : IProductService
{
    private readonly IProductRepository _repository;
    
    public ProductService(IProductRepository repository)
    {
        _repository = repository;
    }
    
    public async Task<ProductDto?> GetByIdAsync(int id)
    {
        return await _repository.GetByIdAsync(id);
    }
}
```

## Files in This Template

| File | Purpose |
|------|---------|
| `ControllerTemplate.cs` | REST controller replacing WCF service contract |
| `ServiceImplementationTemplate.cs` | Service layer with DI and EF Core |
| `ExceptionMiddleware.cs` | Global error handling replacing FaultContract |
| `WcfMigrationGuide.md` | This quick reference guide |
