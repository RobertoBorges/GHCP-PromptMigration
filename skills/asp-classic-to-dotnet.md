# Classic ASP to .NET 8

> **REFERENCE ONLY** — This root `skills/` copy is for reference and onboarding. Prompts must reference the authoritative prompt-local copy at `#file:.github/skills/asp-classic-to-dotnet.md`.

Use this skill when modernizing legacy Classic ASP (`.asp`) applications into .NET 8 web applications.

## When to use

Apply this skill when the source relies on VBScript/JScript pages, inline SQL, COM interop, include files, and IIS-era request processing.

## Recommended target

- Prefer **Razor Pages** or **ASP.NET Core MVC** for server-rendered experiences.
- Introduce APIs only where the new architecture benefits from separation.
- Use a **strangler pattern** when the legacy application is large and risky to replace in one pass.

## Migration priorities

1. Inventory pages, includes, and shared helper logic.
2. Extract business rules from inline scripts.
3. Replace COM dependencies with .NET libraries or external services.
4. Move data access into repositories/services with parameterized queries or EF Core.
5. Rebuild authentication, configuration, and error handling using ASP.NET Core primitives.

## Key transformations

| Classic ASP pattern | Modern target |
|---|---|
| inline VBScript | C# services, controllers, page models |
| `<!-- #include -->` | partials, services, shared layouts |
| `Request/Response` globals | `HttpContext`, model binding, typed results |
| ADODB access | EF Core or `Microsoft.Data.SqlClient` |
| Session-heavy flows | explicit session or distributed cache only where needed |

## Target snippet

```csharp
app.MapGet("/orders/{id:int}", async (int id, IOrderService service, CancellationToken ct) =>
{
    var order = await service.GetAsync(id, ct);
    return order is null ? Results.NotFound() : Results.Ok(order);
});
```

## Validation checklist

- Every legacy page maps to a modern route, page, or endpoint.
- COM, filesystem, and machine-local assumptions are documented or removed.
- SQL injection risks are eliminated during migration.
- Session and auth behavior are explicitly redesigned, not blindly copied.
