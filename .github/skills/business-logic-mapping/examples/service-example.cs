// =============================================================================
// .NET Framework to .NET 8 Service Conversion Example
// =============================================================================

// -----------------------------------------------------------------------------
// BEFORE: .NET Framework Service (Services/ProductService.cs)
// -----------------------------------------------------------------------------
/*
using System;
using System.Collections.Generic;
using System.Linq;
using System.Web.Caching;
using System.Runtime.Caching;
using ProjectName.Data;
using ProjectName.Models;

namespace ProjectName.Services
{
    public class ProductService
    {
        private readonly ProductRepository _productRepository;
        private static MemoryCache _cache = MemoryCache.Default;

        public ProductService()
        {
            _productRepository = new ProductRepository();
        }

        public List<Product> GetAllProducts()
        {
            var cacheKey = "products.all";
            
            if (_cache.Contains(cacheKey))
            {
                return (List<Product>)_cache.Get(cacheKey);
            }
            
            System.Diagnostics.Debug.WriteLine("Fetching all products from database");
            var products = _productRepository.GetAll().ToList();
            
            _cache.Add(cacheKey, products, DateTimeOffset.Now.AddHours(1));
            return products;
        }

        public Product GetProductById(int id)
        {
            var cacheKey = $"products.{id}";
            
            if (_cache.Contains(cacheKey))
            {
                return (Product)_cache.Get(cacheKey);
            }
            
            var product = _productRepository.GetById(id);
            if (product != null)
            {
                _cache.Add(cacheKey, product, DateTimeOffset.Now.AddHours(1));
            }
            return product;
        }

        public Product CreateProduct(ProductViewModel model)
        {
            var product = new Product
            {
                Name = model.Name,
                Price = model.Price,
                Description = model.Description,
                CreatedAt = DateTime.Now
            };

            _productRepository.Add(product);
            _productRepository.SaveChanges();
            
            _cache.Remove("products.all");
            System.Diagnostics.Debug.WriteLine($"Product created: {product.Id}");
            
            return product;
        }

        public void UpdateProduct(int id, ProductViewModel model)
        {
            var product = _productRepository.GetById(id);
            if (product == null)
                throw new Exception("Product not found");

            product.Name = model.Name;
            product.Price = model.Price;
            product.Description = model.Description;
            product.UpdatedAt = DateTime.Now;

            _productRepository.SaveChanges();
            
            _cache.Remove("products.all");
            _cache.Remove($"products.{id}");
            System.Diagnostics.Debug.WriteLine($"Product updated: {id}");
        }

        public void DeleteProduct(int id)
        {
            var product = _productRepository.GetById(id);
            if (product == null)
                throw new Exception("Product not found");

            _productRepository.Delete(product);
            _productRepository.SaveChanges();
            
            _cache.Remove("products.all");
            _cache.Remove($"products.{id}");
            System.Diagnostics.Debug.WriteLine($"Product deleted: {id}");
        }

        public List<Product> SearchProducts(string query, int? categoryId, decimal? minPrice, decimal? maxPrice)
        {
            var products = _productRepository.GetAll()
                .Where(p => p.Name.Contains(query));

            if (categoryId.HasValue)
                products = products.Where(p => p.CategoryId == categoryId.Value);

            if (minPrice.HasValue)
                products = products.Where(p => p.Price >= minPrice.Value);

            if (maxPrice.HasValue)
                products = products.Where(p => p.Price <= maxPrice.Value);

            return products.ToList();
        }
    }
}
*/

// -----------------------------------------------------------------------------
// AFTER: .NET 8 Service Interface (Services/Interfaces/IProductService.cs)
// -----------------------------------------------------------------------------

using ProjectName.Models.DTOs;
using ProjectName.Models.Entities;

namespace ProjectName.Services.Interfaces;

public interface IProductService
{
    Task<IEnumerable<Product>> GetAllProductsAsync();
    Task<Product?> GetProductByIdAsync(int id);
    Task<Product> CreateProductAsync(CreateProductDto dto);
    Task<Product> UpdateProductAsync(int id, UpdateProductDto dto);
    Task DeleteProductAsync(int id);
    Task<IEnumerable<Product>> SearchProductsAsync(string query, ProductSearchFilters? filters = null);
}

// -----------------------------------------------------------------------------
// AFTER: .NET 8 Service Implementation (Services/ProductService.cs)
// -----------------------------------------------------------------------------

using Microsoft.Extensions.Caching.Memory;
using Microsoft.EntityFrameworkCore;
using ProjectName.Data;
using ProjectName.Models.DTOs;
using ProjectName.Models.Entities;
using ProjectName.Services.Interfaces;

namespace ProjectName.Services;

public class ProductService : IProductService
{
    private readonly ApplicationDbContext _context;
    private readonly IMemoryCache _cache;
    private readonly ILogger<ProductService> _logger;
    
    private const string AllProductsCacheKey = "products.all";
    private static readonly TimeSpan CacheDuration = TimeSpan.FromHours(1);

    // Constructor injection (replaces manual instantiation)
    public ProductService(
        ApplicationDbContext context,
        IMemoryCache cache,
        ILogger<ProductService> logger)
    {
        _context = context;
        _cache = cache;
        _logger = logger;
    }

    public async Task<IEnumerable<Product>> GetAllProductsAsync()
    {
        // IMemoryCache replaces MemoryCache.Default
        return await _cache.GetOrCreateAsync(AllProductsCacheKey, async entry =>
        {
            entry.AbsoluteExpirationRelativeToNow = CacheDuration;
            
            // ILogger replaces System.Diagnostics.Debug.WriteLine
            _logger.LogInformation("Fetching all products from database");
            return await _context.Products.ToListAsync();
        }) ?? Enumerable.Empty<Product>();
    }

    public async Task<Product?> GetProductByIdAsync(int id)
    {
        var cacheKey = $"products.{id}";
        
        return await _cache.GetOrCreateAsync(cacheKey, async entry =>
        {
            entry.AbsoluteExpirationRelativeToNow = CacheDuration;
            return await _context.Products.FindAsync(id);
        });
    }

    public async Task<Product> CreateProductAsync(CreateProductDto dto)
    {
        var product = new Product
        {
            Name = dto.Name,
            Price = dto.Price,
            Description = dto.Description,
            CreatedAt = DateTime.UtcNow // Use UTC
        };

        _context.Products.Add(product);
        await _context.SaveChangesAsync();
        
        _cache.Remove(AllProductsCacheKey);
        
        // Structured logging with template
        _logger.LogInformation("Product created: {ProductId}", product.Id);
        
        return product;
    }

    public async Task<Product> UpdateProductAsync(int id, UpdateProductDto dto)
    {
        var product = await _context.Products.FindAsync(id)
            ?? throw new NotFoundException($"Product {id} not found");

        product.Name = dto.Name;
        product.Price = dto.Price;
        product.Description = dto.Description;
        product.UpdatedAt = DateTime.UtcNow;

        await _context.SaveChangesAsync();
        
        _cache.Remove(AllProductsCacheKey);
        _cache.Remove($"products.{id}");
        _logger.LogInformation("Product updated: {ProductId}", id);
        
        return product;
    }

    public async Task DeleteProductAsync(int id)
    {
        var product = await _context.Products.FindAsync(id)
            ?? throw new NotFoundException($"Product {id} not found");

        _context.Products.Remove(product);
        await _context.SaveChangesAsync();
        
        _cache.Remove(AllProductsCacheKey);
        _cache.Remove($"products.{id}");
        _logger.LogInformation("Product deleted: {ProductId}", id);
    }

    public async Task<IEnumerable<Product>> SearchProductsAsync(
        string query, 
        ProductSearchFilters? filters = null)
    {
        var queryable = _context.Products.AsQueryable();

        // Name search
        queryable = queryable.Where(p => p.Name.Contains(query));

        // Apply filters (same logic, async execution)
        if (filters?.CategoryId.HasValue == true)
        {
            queryable = queryable.Where(p => p.CategoryId == filters.CategoryId);
        }

        if (filters?.MinPrice.HasValue == true)
        {
            queryable = queryable.Where(p => p.Price >= filters.MinPrice);
        }

        if (filters?.MaxPrice.HasValue == true)
        {
            queryable = queryable.Where(p => p.Price <= filters.MaxPrice);
        }

        return await queryable.ToListAsync();
    }
}

// -----------------------------------------------------------------------------
// Search Filters DTO (Models/DTOs/ProductSearchFilters.cs)
// -----------------------------------------------------------------------------

namespace ProjectName.Models.DTOs;

public class ProductSearchFilters
{
    public int? CategoryId { get; set; }
    public decimal? MinPrice { get; set; }
    public decimal? MaxPrice { get; set; }
}

// -----------------------------------------------------------------------------
// Custom Exception (Exceptions/NotFoundException.cs)
// -----------------------------------------------------------------------------

namespace ProjectName.Exceptions;

public class NotFoundException : Exception
{
    public NotFoundException(string message) : base(message) { }
}

// -----------------------------------------------------------------------------
// Register in DI (Program.cs)
// -----------------------------------------------------------------------------
/*
builder.Services.AddMemoryCache();
builder.Services.AddScoped<IProductService, ProductService>();
*/

// -----------------------------------------------------------------------------
// KEY CONVERSION NOTES:
// -----------------------------------------------------------------------------
// 1. Create interface (IProductService) for dependency injection
// 2. MemoryCache.Default → IMemoryCache via DI
// 3. System.Diagnostics.Debug.WriteLine → ILogger with structured logging
// 4. All methods become async with Task<T>
// 5. DateTime.Now → DateTime.UtcNow for cloud compatibility
// 6. Repository pattern can use DbContext directly
// 7. throw new Exception() → Custom exception types
// 8. Register service in DI container in Program.cs
// 9. Use GetOrCreateAsync for cache-aside pattern
// 10. Always use async EF methods: FindAsync, ToListAsync, SaveChangesAsync
