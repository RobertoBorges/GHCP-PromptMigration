# WCF to REST API Migration

Use this skill when a .NET Framework solution exposes WCF services that must become Azure-friendly HTTP APIs.

## When to Use

Apply this skill when the source contains:

- `[ServiceContract]`, `[OperationContract]`, or `[DataContract]`
- `.svc` files, `ServiceHost`, or `system.serviceModel`
- `BasicHttpBinding`, `WSHttpBinding`, `WebHttpBinding`, or `NetTcpBinding`
- SOAP envelopes, generated proxies, or XML-serialized fault contracts

## Target State

Modernize toward:

- ASP.NET Core Web API or minimal APIs on .NET 8
- JSON over HTTPS by default
- OpenAPI/Swagger for discoverability
- `ProblemDetails` for errors
- Entra ID or managed identity-aware auth where required

## Contract Mapping

| WCF Concept | ASP.NET Core / REST Target |
|---|---|
| `[ServiceContract]` | Controller, route group, or minimal API module |
| `[OperationContract]` | `[HttpGet]`, `[HttpPost]`, `[HttpPut]`, `[HttpDelete]` |
| `[DataContract]` | DTO class or `record` |
| `[DataMember]` | Standard JSON property or serializer attribute only if needed |
| `FaultContract<T>` | `ProblemDetails` or typed HTTP error model |
| `.svc` endpoint | `/api/...` route |
| `ServiceHost` | ASP.NET Core host in `Program.cs` |
| `BasicHttpBinding` / `WSHttpBinding` | HTTPS JSON API |
| `NetTcpBinding` | Redesign to HTTP, gRPC, queue, or event-driven pattern |

## Endpoint Design Rules

- Design routes around resources and actions with business meaning.
- Preserve core business semantics even when URI structure changes.
- Do not mirror SOAP action names if a resource-oriented route is clearer.
- Flag duplex callbacks, sessionful contracts, and one-way messaging as redesign hotspots.

## ServiceContract to Controller Example

### Before - WCF contract and implementation

```csharp
[ServiceContract]
public interface ICustomerService
{
    [OperationContract]
    CustomerDto GetCustomer(int id);

    [OperationContract]
    void UpdateCustomer(CustomerDto customer);
}

public class CustomerService : ICustomerService
{
    public CustomerDto GetCustomer(int id)
    {
        return Repository.Load(id);
    }

    public void UpdateCustomer(CustomerDto customer)
    {
        Repository.Save(customer);
    }
}
```

### After - application service + controller

```csharp
public interface ICustomerApplicationService
{
    Task<CustomerDto?> GetAsync(int id, CancellationToken cancellationToken);
    Task UpdateAsync(CustomerDto customer, CancellationToken cancellationToken);
}

[ApiController]
[Route("api/customers")]
public sealed class CustomersController(ICustomerApplicationService service) : ControllerBase
{
    [HttpGet("{id:int}")]
    public async Task<IActionResult> Get(int id, CancellationToken cancellationToken)
    {
        var customer = await service.GetAsync(id, cancellationToken);
        return customer is null ? NotFound() : Ok(customer);
    }

    [HttpPut("{id:int}")]
    public async Task<IActionResult> Update(int id, [FromBody] CustomerDto customer, CancellationToken cancellationToken)
    {
        if (id != customer.Id) return BadRequest();
        await service.UpdateAsync(customer, cancellationToken);
        return NoContent();
    }
}
```

## OperationContract to HTTP Verb Mapping

| Legacy Operation Pattern | Recommended REST Mapping |
|---|---|
| `GetOrder(int id)` | `GET /api/orders/{id}` |
| `FindOrders(SearchRequest request)` | `GET /api/orders?status=...` or `POST /api/orders/search` for complex criteria |
| `CreateOrder(CreateOrderRequest request)` | `POST /api/orders` |
| `UpdateOrder(OrderDto order)` | `PUT /api/orders/{id}` |
| `DeleteOrder(int id)` | `DELETE /api/orders/{id}` |

## DataContract to DTO / Record Example

### Before - WCF `DataContract`

```csharp
[DataContract]
public class OrderDto
{
    [DataMember(Order = 1)]
    public int Id { get; set; }

    [DataMember(Order = 2)]
    public string CustomerName { get; set; }
}
```

### After - REST DTO

```csharp
public sealed record OrderDto(int Id, string CustomerName);
```

Use serializer attributes only when compatibility demands them.

## Faults and Error Handling

### Before - SOAP fault contract

```csharp
[FaultContract(typeof(ServiceFault))]
[OperationContract]
OrderDto GetOrder(int id);
```

### After - HTTP Problem Details

```csharp
builder.Services.AddProblemDetails();

app.UseExceptionHandler();
```

Recommended mappings:

- Validation issue -> `400 Bad Request`
- Missing resource -> `404 Not Found`
- Conflict -> `409 Conflict`
- Unauthorized -> `401 Unauthorized`
- Forbidden -> `403 Forbidden`
- Unexpected error -> `500 Internal Server Error`

## Binding Translation Guidance

| WCF Binding | Modern Direction |
|---|---|
| `BasicHttpBinding` | REST over HTTPS |
| `WSHttpBinding` | REST over HTTPS + Entra ID / policy-driven auth |
| `WebHttpBinding` | Usually direct Web API migration |
| `NetTcpBinding` | Consider gRPC, queues, or HTTP APIs |
| `NetMsmqBinding` | Azure Service Bus / event-driven redesign |

## Program.cs Baseline

```csharp
var builder = WebApplication.CreateBuilder(args);

builder.Services.AddControllers();
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();
builder.Services.AddProblemDetails();

var app = builder.Build();

app.UseExceptionHandler();
app.UseHttpsRedirection();
app.MapControllers();
app.UseSwagger();
app.UseSwaggerUI();

app.Run();
```

## Security and Compatibility Notes

- Publish an explicit contract-difference section in the migration report.
- Version routes when consumers cannot switch immediately.
- Generate OpenAPI and sample requests for downstream consumers.
- Do not promise wire-level SOAP compatibility unless a dedicated compatibility layer is actually built.

## Validation Commands

```bash
dotnet build
dotnet test
```

## Output Expectations for Prompts

When this skill is applied, the prompt should:

- Produce an operation-by-operation WCF-to-REST mapping table
- Generate controllers, DTOs, service abstractions, and `Program.cs` wiring
- Flag breaking contract changes explicitly
- Call out non-REST-friendly patterns such as callbacks, sessions, and MSMQ
