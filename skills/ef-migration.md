# EF / Data Access Migration

Use this skill when migrating ADO.NET, raw SQL, LINQ to SQL, or Entity Framework 6 code to EF Core.

## When to use

Apply this skill when the source uses `SqlConnection`, `SqlCommand`, `DbContext` from EF6, EDMX models, or repository patterns tightly bound to legacy providers.

## Target patterns

- Prefer **EF Core 8** for mainstream relational workloads.
- Use **`Microsoft.Data.SqlClient`** for low-level SQL access that must remain hand-written.
- Keep entities, migrations, and query services separated from web concerns.

## Migration approach

1. Inventory contexts, repositories, stored procedure usage, and transaction boundaries.
2. Decide **database-first**, **code-first**, or **hybrid** based on schema ownership.
3. Replace EF6 APIs with EF Core equivalents.
4. Convert sync I/O to async.
5. Re-test query semantics, tracking behavior, and cascade delete expectations.

## Common changes

| Legacy pattern | EF Core target |
|---|---|
| `System.Data.SqlClient` | `Microsoft.Data.SqlClient` |
| EF6 `DbFunctions` | EF Core-supported LINQ or SQL translation |
| EDMX designer | code-first model classes and fluent config |
| lazy loading assumptions | explicit includes or EF Core proxies if justified |

## Example registration

```csharp
builder.Services.AddDbContext<AppDbContext>(options =>
    options.UseSqlServer(builder.Configuration.GetConnectionString("DefaultConnection")));
```

## Validation checklist

- Queries produce the same business result set.
- Transactions and concurrency control still work.
- Migrations are generated only if the repo owns schema evolution.
- Stored procedures and raw SQL are parameterized and tested.
