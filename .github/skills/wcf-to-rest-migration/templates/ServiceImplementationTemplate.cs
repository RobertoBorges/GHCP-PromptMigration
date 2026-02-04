// =============================================================================
// Service Implementation Template
// =============================================================================
// Replaces WCF Service class with modern .NET service pattern
// =============================================================================

using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Caching.Memory;

namespace MyApp.Api.Services;

/// <summary>
/// Product service implementation
/// 
/// WCF Migration Notes:
/// - Remove [ServiceBehavior] attributes
/// - Use constructor injection (not ServiceLocator)
/// - Use async/await patterns
/// - Use ILogger instead of custom logging
/// - Use EF Core instead of direct ADO.NET
/// </summary>
public class ProductService : IProductService
{
    private readonly ApplicationDbContext _context;
    private readonly IMemoryCache _cache;
    private readonly ILogger<ProductService> _logger;

    // WCF used parameterless constructors with ServiceLocator
    // .NET Core uses constructor injection
    public ProductService(
        ApplicationDbContext context,
        IMemoryCache cache,
        ILogger<ProductService> logger)
    {
        _context = context;
        _cache = cache;
        _logger = logger;
    }

    /// <summary>
    /// Get product by ID with caching
    /// </summary>
    public async Task<ProductDto?> GetByIdAsync(int id)
    {
        var cacheKey = $"product_{id}";

        // Try cache first
        if (_cache.TryGetValue(cacheKey, out ProductDto? cached))
        {
            _logger.LogDebug("Cache hit for product {ProductId}", id);
            return cached;
        }

        // Query database
        var product = await _context.Products
            .AsNoTracking()
            .Where(p => p.Id == id)
            .Select(p => new ProductDto
            {
                Id = p.Id,
                Name = p.Name,
                Description = p.Description,
                Price = p.Price,
                Category = p.Category,
                IsActive = p.IsActive,
                CreatedAt = p.CreatedAt,
                UpdatedAt = p.UpdatedAt
            })
            .FirstOrDefaultAsync();

        if (product is not null)
        {
            // Cache for 5 minutes
            _cache.Set(cacheKey, product, TimeSpan.FromMinutes(5));
        }

        return product;
    }

    /// <summary>
    /// Get all products with filtering and pagination
    /// </summary>
    public async Task<IEnumerable<ProductDto>> GetAllAsync(
        string? category, 
        int page, 
        int pageSize)
    {
        var query = _context.Products
            .AsNoTracking()
            .Where(p => p.IsActive);

        // Apply category filter
        if (!string.IsNullOrWhiteSpace(category))
        {
            query = query.Where(p => p.Category == category);
        }

        // Apply pagination
        var products = await query
            .OrderBy(p => p.Name)
            .Skip((page - 1) * pageSize)
            .Take(pageSize)
            .Select(p => new ProductDto
            {
                Id = p.Id,
                Name = p.Name,
                Description = p.Description,
                Price = p.Price,
                Category = p.Category,
                IsActive = p.IsActive,
                CreatedAt = p.CreatedAt,
                UpdatedAt = p.UpdatedAt
            })
            .ToListAsync();

        return products;
    }

    /// <summary>
    /// Create a new product
    /// </summary>
    public async Task<ProductDto> CreateAsync(CreateProductRequest request)
    {
        var product = new Product
        {
            Name = request.Name,
            Description = request.Description,
            Price = request.Price,
            Category = request.Category,
            IsActive = true,
            CreatedAt = DateTime.UtcNow
        };

        _context.Products.Add(product);
        await _context.SaveChangesAsync();

        _logger.LogInformation("Created product {ProductId}: {ProductName}", 
            product.Id, product.Name);

        return new ProductDto
        {
            Id = product.Id,
            Name = product.Name,
            Description = product.Description,
            Price = product.Price,
            Category = product.Category,
            IsActive = product.IsActive,
            CreatedAt = product.CreatedAt
        };
    }

    /// <summary>
    /// Update an existing product
    /// </summary>
    public async Task<ProductDto?> UpdateAsync(UpdateProductRequest request)
    {
        var product = await _context.Products.FindAsync(request.Id);

        if (product is null)
        {
            return null;
        }

        // Update properties
        product.Name = request.Name;
        product.Description = request.Description;
        product.Price = request.Price;
        product.Category = request.Category;
        product.IsActive = request.IsActive;
        product.UpdatedAt = DateTime.UtcNow;

        await _context.SaveChangesAsync();

        // Invalidate cache
        _cache.Remove($"product_{product.Id}");

        _logger.LogInformation("Updated product {ProductId}", product.Id);

        return new ProductDto
        {
            Id = product.Id,
            Name = product.Name,
            Description = product.Description,
            Price = product.Price,
            Category = product.Category,
            IsActive = product.IsActive,
            CreatedAt = product.CreatedAt,
            UpdatedAt = product.UpdatedAt
        };
    }

    /// <summary>
    /// Delete a product (soft delete)
    /// </summary>
    public async Task<bool> DeleteAsync(int id)
    {
        var product = await _context.Products.FindAsync(id);

        if (product is null)
        {
            return false;
        }

        // Soft delete
        product.IsActive = false;
        product.UpdatedAt = DateTime.UtcNow;

        await _context.SaveChangesAsync();

        // Invalidate cache
        _cache.Remove($"product_{id}");

        _logger.LogInformation("Deleted product {ProductId}", id);

        return true;
    }
}

// =============================================================================
// Entity class (used by EF Core)
// =============================================================================

public class Product
{
    public int Id { get; set; }
    public string Name { get; set; } = string.Empty;
    public string? Description { get; set; }
    public decimal Price { get; set; }
    public string Category { get; set; } = string.Empty;
    public bool IsActive { get; set; }
    public DateTime CreatedAt { get; set; }
    public DateTime? UpdatedAt { get; set; }
}

// =============================================================================
// DbContext
// =============================================================================

public class ApplicationDbContext : DbContext
{
    public ApplicationDbContext(DbContextOptions<ApplicationDbContext> options)
        : base(options)
    {
    }

    public DbSet<Product> Products => Set<Product>();

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        modelBuilder.Entity<Product>(entity =>
        {
            entity.HasKey(e => e.Id);
            entity.Property(e => e.Name).HasMaxLength(200).IsRequired();
            entity.Property(e => e.Description).HasMaxLength(2000);
            entity.Property(e => e.Price).HasPrecision(18, 2);
            entity.Property(e => e.Category).HasMaxLength(100).IsRequired();
            entity.HasIndex(e => e.Category);
            entity.HasIndex(e => e.IsActive);
        });
    }
}
