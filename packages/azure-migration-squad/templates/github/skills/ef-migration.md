# EF and Data Access Migration

Use this skill when modernizing ADO.NET, EF6, LINQ to SQL, or legacy repository code for Azure-hosted applications.

## When to Use

Apply this skill when the source uses:

- `SqlConnection`, `SqlCommand`, `DataSet`, or `DataTable`
- Entity Framework 6 (`System.Data.Entity`)
- EDMX models or designer-generated contexts
- synchronous data access or connection strings tied to on-prem SQL Server

## Migration Goals

Default to these targets unless the assessment report says otherwise:

- EF Core 8 for mainstream relational workloads
- `Microsoft.Data.SqlClient` for raw SQL that must remain hand-written
- dependency-injected `DbContext`
- async query and save patterns
- Azure SQL or PostgreSQL connectivity that supports modern auth patterns

## ADO.NET to EF Core Example

### Before - raw ADO.NET

```csharp
public Customer Load(int id)
{
    using var connection = new SqlConnection(ConfigurationManager.ConnectionStrings["DefaultConnection"].ConnectionString);
    using var command = new SqlCommand("SELECT Id, Name FROM Customers WHERE Id = @id", connection);
    command.Parameters.AddWithValue("@id", id);
    connection.Open();

    using var reader = command.ExecuteReader();
    if (!reader.Read()) return null;

    return new Customer
    {
        Id = reader.GetInt32(0),
        Name = reader.GetString(1)
    };
}
```

### After - EF Core query service

```csharp
public sealed class CustomerRepository(AppDbContext dbContext)
{
    public Task<Customer?> LoadAsync(int id, CancellationToken cancellationToken) =>
        dbContext.Customers.SingleOrDefaultAsync(x => x.Id == id, cancellationToken);
}
```

## EF6 to EF Core Migration

| Legacy Pattern | EF Core Target |
|---|---|
| `System.Data.Entity` | `Microsoft.EntityFrameworkCore` |
| EDMX designer model | code-first entity classes + fluent configuration |
| `DbSet.Find()` in sync flows | `FindAsync()` / async LINQ |
| lazy loading by default | explicit `Include()` or proxies only when justified |
| `Database.Initialize(false)` | migrations + explicit startup checks |
| `DbFunctions` helpers | EF Core LINQ translation or `EF.Functions` |

### Before - EF6 context

```csharp
public class LegacyContext : DbContext
{
    public LegacyContext() : base("name=DefaultConnection") { }
    public DbSet<Order> Orders { get; set; }
}
```

### After - EF Core context

```csharp
public sealed class AppDbContext(DbContextOptions<AppDbContext> options) : DbContext(options)
{
    public DbSet<Order> Orders => Set<Order>();

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        modelBuilder.Entity<Order>(entity =>
        {
            entity.ToTable("Orders");
            entity.HasKey(x => x.Id);
            entity.Property(x => x.Number).HasMaxLength(64).IsRequired();
        });
    }
}
```

## DbContext Setup

### SQL Server

```csharp
builder.Services.AddDbContext<AppDbContext>(options =>
    options.UseSqlServer(builder.Configuration.GetConnectionString("DefaultConnection")));
```

### PostgreSQL

```csharp
builder.Services.AddDbContext<AppDbContext>(options =>
    options.UseNpgsql(builder.Configuration.GetConnectionString("DefaultConnection")));
```

## Managed Identity Connection Pattern

For Azure SQL, prefer a connection string that enables Entra auth when the hosting platform has a managed identity.

```json
{
  "ConnectionStrings": {
    "DefaultConnection": "Server=tcp:contoso-sql.database.windows.net,1433;Database=Store;Authentication=Active Directory Default;Encrypt=True;TrustServerCertificate=False;"
  }
}
```

Grant the app identity database access separately; the connection string alone is not enough.

## Migrations Commands

```bash
dotnet tool install --global dotnet-ef
dotnet ef migrations add InitialCreate --project src/Contoso.Data --startup-project src/Contoso.Web
dotnet ef database update --project src/Contoso.Data --startup-project src/Contoso.Web
```

Use migrations only when the application owns schema evolution. If DBAs control the schema, generate SQL scripts for review instead.

## Seeding Pattern

Use deterministic startup seeding only for small reference data.

```csharp
public static class SeedData
{
    public static async Task InitializeAsync(AppDbContext dbContext, CancellationToken cancellationToken)
    {
        if (await dbContext.Categories.AnyAsync(cancellationToken)) return;

        dbContext.Categories.AddRange(
            new Category { Name = "Books" },
            new Category { Name = "Games" });

        await dbContext.SaveChangesAsync(cancellationToken);
    }
}
```

Call seeding from a controlled startup or deployment step, not from random request paths.

## Modernization Checklist

- Convert sync I/O to async.
- Re-test transaction and concurrency behavior.
- Parameterize every raw SQL call.
- Separate entities from DTOs and API contracts.
- Document stored procedure, trigger, and SQL Agent dependencies that remain.

## Validation Checklist

- Queries return the same business results as before.
- Transactions and optimistic concurrency still work.
- Migration scripts are repeatable and environment-safe.
- Managed identity or secret handling is documented and validated.
- Seed data is idempotent.

## Output Expectations for Prompts

When this skill is applied, the prompt should:

- Identify whether ADO.NET, EF6, or hybrid access is in use
- Generate `DbContext`, DI registration, connection updates, and migration commands
- Flag stored procedures and advanced SQL features needing manual review
- Document whether schema ownership allows EF migrations or requires SQL-first change control
