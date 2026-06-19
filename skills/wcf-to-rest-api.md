# WCF to REST API

Use this skill when a .NET Framework application exposes WCF services that must be modernized into ASP.NET Core Web APIs.

## When to use

Apply this skill when the source contains:

- `[ServiceContract]`, `[OperationContract]`, or `[DataContract]`
- `.svc` files or `ServiceHost`
- `system.serviceModel` in `web.config` or `app.config`
- `BasicHttpBinding`, `WSHttpBinding`, `NetTcpBinding`, or SOAP endpoints

## Modernization goal

Migrate business operations, contracts, and serialization models into:

- ASP.NET Core controllers or minimal APIs
- JSON over HTTP/HTTPS by default
- OpenAPI/Swagger for discoverability
- Problem Details for errors
- Entra ID protected APIs where authentication is required

## Important constraints

- REST migration is usually a contract change, not a drop-in protocol swap.
- Preserve business semantics first; do not mirror SOAP action names unless they remain useful as resource operations.
- If a service depends on duplex callbacks, sessions, or MSMQ-style delivery, flag it as a redesign hotspot.

## Mapping guide

| WCF concept | REST / ASP.NET Core target |
|---|---|
| `[ServiceContract]` | Controller class or route group |
| `[OperationContract]` | HTTP verb + route |
| `[DataContract]` / `[DataMember]` | POCO/record DTO using `System.Text.Json` |
| `FaultException<T>` | `ProblemDetails` / typed error response |
| `.svc` endpoint | `MapControllers()` or `MapGroup()` |
| `ServiceHost` | ASP.NET Core host in `Program.cs` |
| `BasicHttpBinding` / `WSHttpBinding` | HTTPS JSON API |
| `NetTcpBinding` | Usually redesign to HTTP/gRPC/queue-based interaction |

## Migration workflow

1. Inventory all WCF contracts, operations, data contracts, and bindings.
2. Group operations into resource-oriented controllers.
3. Convert request/response types into DTOs.
4. Move business logic out of WCF service classes into application services.
5. Implement ASP.NET Core endpoints that call those services.
6. Add validation, Problem Details, auth, logging, and OpenAPI.
7. Create a compatibility note describing contract differences.

## Contract conversion example

### Legacy WCF contract

```csharp
[ServiceContract]
public interface IOrderService
{
    [OperationContract]
    [FaultContract(typeof(ServiceFault))]
    OrderDto GetOrder(int id);

    [OperationContract]
    void CreateOrder(CreateOrderRequest request);
}
```

### Application service

```csharp
public interface IOrderApplicationService
{
    Task<OrderDto?> GetAsync(int id, CancellationToken cancellationToken);
    Task<int> CreateAsync(CreateOrderRequest request, CancellationToken cancellationToken);
}
```

### ASP.NET Core controller target

```csharp
[ApiController]
[Route("api/orders")]
public sealed class OrdersController(IOrderApplicationService service) : ControllerBase
{
    [HttpGet("{id:int}")]
    [ProducesResponseType<OrderDto>(StatusCodes.Status200OK)]
    [ProducesResponseType(StatusCodes.Status404NotFound)]
    public async Task<IActionResult> Get(int id, CancellationToken cancellationToken)
    {
        var order = await service.GetAsync(id, cancellationToken);
        return order is null ? NotFound() : Ok(order);
    }

    [HttpPost]
    [ProducesResponseType(StatusCodes.Status201Created)]
    [ProducesResponseType<ProblemDetails>(StatusCodes.Status400BadRequest)]
    public async Task<IActionResult> Create([FromBody] CreateOrderRequest request, CancellationToken cancellationToken)
    {
        var id = await service.CreateAsync(request, cancellationToken);
        return CreatedAtAction(nameof(Get), new { id }, null);
    }
}
```

## Error handling pattern

Replace WCF fault contracts with consistent HTTP responses.

```csharp
builder.Services.AddProblemDetails();

app.UseExceptionHandler();
```

Recommended HTTP mappings:

- Validation failure -> `400 Bad Request`
- Missing resource -> `404 Not Found`
- Concurrency conflict -> `409 Conflict`
- Authorization failure -> `401` or `403`
- Unexpected server error -> `500` with correlation ID logged

## Serialization guidance

- Prefer `System.Text.Json` unless a converter is required.
- Flatten XML-specific contract concerns where possible.
- Keep DTOs separate from EF entities or domain models.
- If clients need backward compatibility, version routes or publish a transition guide.

## Security and Azure guidance

- Secure APIs with Entra ID and `Microsoft.Identity.Web`.
- Publish OpenAPI for downstream consumers.
- Use App Service or Container Apps unless AKS is justified by orchestration requirements.
- Add health endpoints, structured logging, and request correlation.

## Validation checklist

```bash
dotnet build
dotnet test
```

Confirm that:

- Every WCF operation has a mapped REST endpoint or a documented redesign exception.
- Existing business rules were moved out of service host classes.
- Error handling is consistent and uses HTTP semantics.
- Authentication, authorization, and OpenAPI generation work.

## Output expectations for the migration prompt

- Provide an operation-by-operation mapping table.
- Call out every breaking contract change.
- Generate the controller, DTO, service abstraction, and startup wiring.
- Recommend gRPC or messaging only when REST is a poor fit.
