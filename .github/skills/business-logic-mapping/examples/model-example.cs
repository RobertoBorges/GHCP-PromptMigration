// =============================================================================
// .NET Framework EF6 to .NET 8 EF Core Entity Conversion Example
// =============================================================================

// -----------------------------------------------------------------------------
// BEFORE: .NET Framework EF6 Entity (Models/Product.cs)
// -----------------------------------------------------------------------------
/*
using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace ProjectName.Models
{
    [Table("Products")]
    public class Product
    {
        [Key]
        public int Id { get; set; }

        [Required]
        [StringLength(255)]
        public string Name { get; set; }

        [Required]
        [StringLength(255)]
        public string Slug { get; set; }

        public string Description { get; set; }

        [Column(TypeName = "decimal(18,2)")]
        public decimal Price { get; set; }

        public int CategoryId { get; set; }

        public bool IsActive { get; set; }

        public string MetadataJson { get; set; }

        public DateTime CreatedAt { get; set; }
        public DateTime? UpdatedAt { get; set; }
        public DateTime? DeletedAt { get; set; }

        // Navigation Properties
        [ForeignKey("CategoryId")]
        public virtual Category Category { get; set; }

        public virtual ICollection<Review> Reviews { get; set; }

        public virtual ICollection<Tag> Tags { get; set; }

        public virtual ICollection<Image> Images { get; set; }

        // Constructor
        public Product()
        {
            Reviews = new HashSet<Review>();
            Tags = new HashSet<Tag>();
            Images = new HashSet<Image>();
            IsActive = true;
        }

        // Business Logic Methods
        public string GetFormattedPrice()
        {
            return string.Format("${0:N2}", Price);
        }

        public bool IsAvailable(int stockQuantity)
        {
            return IsActive && stockQuantity > 0;
        }

        public decimal ApplyDiscount(decimal percentage)
        {
            return Price * (1 - percentage / 100);
        }
    }
}

// EF6 DbContext
using System.Data.Entity;

namespace ProjectName.Data
{
    public class ApplicationDbContext : DbContext
    {
        public ApplicationDbContext() : base("DefaultConnection")
        {
            // Disable lazy loading
            Configuration.LazyLoadingEnabled = false;
        }

        public DbSet<Product> Products { get; set; }
        public DbSet<Category> Categories { get; set; }
        public DbSet<Review> Reviews { get; set; }
        public DbSet<Tag> Tags { get; set; }

        protected override void OnModelCreating(DbModelBuilder modelBuilder)
        {
            base.OnModelCreating(modelBuilder);

            // Many-to-many relationship
            modelBuilder.Entity<Product>()
                .HasMany(p => p.Tags)
                .WithMany(t => t.Products)
                .Map(m =>
                {
                    m.ToTable("ProductTags");
                    m.MapLeftKey("ProductId");
                    m.MapRightKey("TagId");
                });

            // Soft delete filter (manual implementation)
            // Note: EF6 doesn't have global query filters
        }

        public override int SaveChanges()
        {
            // Auto-set timestamps
            foreach (var entry in ChangeTracker.Entries<Product>())
            {
                if (entry.State == EntityState.Added)
                {
                    entry.Entity.CreatedAt = DateTime.Now;
                }
                else if (entry.State == EntityState.Modified)
                {
                    entry.Entity.UpdatedAt = DateTime.Now;
                }
            }

            return base.SaveChanges();
        }
    }
}
*/

// -----------------------------------------------------------------------------
// AFTER: .NET 8 EF Core Entity (Models/Entities/Product.cs)
// -----------------------------------------------------------------------------

using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace ProjectName.Models.Entities;

public class Product
{
    public int Id { get; set; }

    [Required]
    [MaxLength(255)]
    public string Name { get; set; } = string.Empty;

    [Required]
    [MaxLength(255)]
    public string Slug { get; set; } = string.Empty;

    public string? Description { get; set; }

    [Column(TypeName = "decimal(18,2)")]
    public decimal Price { get; set; }

    public int CategoryId { get; set; }

    public bool IsActive { get; set; } = true;

    public string? MetadataJson { get; set; }

    public DateTime CreatedAt { get; set; }
    public DateTime? UpdatedAt { get; set; }
    public DateTime? DeletedAt { get; set; } // Soft delete

    // Navigation Properties (same pattern, no virtual keyword needed)
    
    // Foreign key relationship
    public Category Category { get; set; } = null!;

    // One-to-many
    public ICollection<Review> Reviews { get; set; } = new List<Review>();

    // Many-to-many via join entity (EF Core pattern)
    public ICollection<ProductTag> ProductTags { get; set; } = new List<ProductTag>();

    // Polymorphic relationship
    public ICollection<Image> Images { get; set; } = new List<Image>();

    // Computed Property (replaces method for simple formatting)
    [NotMapped]
    public string FormattedPrice => $"${Price:N2}";

    // PRESERVED: Business Logic Methods (same implementation)
    public bool IsAvailable(int stockQuantity) => IsActive && stockQuantity > 0;

    public decimal ApplyDiscount(decimal percentage) => Price * (1 - percentage / 100);
}

// -----------------------------------------------------------------------------
// Join Entity for Many-to-Many (Models/Entities/ProductTag.cs)
// EF Core requires explicit join entity for many-to-many with payload
// -----------------------------------------------------------------------------

namespace ProjectName.Models.Entities;

public class ProductTag
{
    public int ProductId { get; set; }
    public Product Product { get; set; } = null!;

    public int TagId { get; set; }
    public Tag Tag { get; set; } = null!;
    
    // Can add additional properties (e.g., CreatedAt, SortOrder)
}

// -----------------------------------------------------------------------------
// EF Core DbContext (Data/ApplicationDbContext.cs)
// -----------------------------------------------------------------------------

using Microsoft.EntityFrameworkCore;
using ProjectName.Models.Entities;

namespace ProjectName.Data;

public class ApplicationDbContext : DbContext
{
    public ApplicationDbContext(DbContextOptions<ApplicationDbContext> options)
        : base(options) // Connection via DI, not hardcoded
    {
    }

    public DbSet<Product> Products => Set<Product>();
    public DbSet<Category> Categories => Set<Category>();
    public DbSet<Review> Reviews => Set<Review>();
    public DbSet<Tag> Tags => Set<Tag>();
    public DbSet<ProductTag> ProductTags => Set<ProductTag>();

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        base.OnModelCreating(modelBuilder);

        // Product configuration
        modelBuilder.Entity<Product>(entity =>
        {
            entity.HasKey(e => e.Id);
            
            entity.HasIndex(e => e.Slug).IsUnique();
            
            // Global query filter for soft delete (EF Core feature!)
            entity.HasQueryFilter(e => e.DeletedAt == null);

            // One-to-many relationship
            entity.HasOne(e => e.Category)
                .WithMany(c => c.Products)
                .HasForeignKey(e => e.CategoryId)
                .OnDelete(DeleteBehavior.Restrict);

            // One-to-many
            entity.HasMany(e => e.Reviews)
                .WithOne(r => r.Product)
                .HasForeignKey(r => r.ProductId);
        });

        // Many-to-many via join entity
        modelBuilder.Entity<ProductTag>(entity =>
        {
            entity.HasKey(pt => new { pt.ProductId, pt.TagId });

            entity.HasOne(pt => pt.Product)
                .WithMany(p => p.ProductTags)
                .HasForeignKey(pt => pt.ProductId);

            entity.HasOne(pt => pt.Tag)
                .WithMany(t => t.ProductTags)
                .HasForeignKey(pt => pt.TagId);
        });
    }

    // Override SaveChangesAsync for timestamps (async version)
    public override Task<int> SaveChangesAsync(CancellationToken cancellationToken = default)
    {
        var entries = ChangeTracker.Entries<Product>();

        foreach (var entry in entries)
        {
            if (entry.State == EntityState.Added)
            {
                entry.Entity.CreatedAt = DateTime.UtcNow; // Use UTC
            }
            else if (entry.State == EntityState.Modified)
            {
                entry.Entity.UpdatedAt = DateTime.UtcNow;
            }
        }

        return base.SaveChangesAsync(cancellationToken);
    }
}

// -----------------------------------------------------------------------------
// Query Extensions for Reusable Filters (Extensions/ProductQueryExtensions.cs)
// Replaces repository methods with composable LINQ extensions
// -----------------------------------------------------------------------------

namespace ProjectName.Extensions;

public static class ProductQueryExtensions
{
    public static IQueryable<Product> Active(this IQueryable<Product> query)
    {
        return query.Where(p => p.IsActive);
    }

    public static IQueryable<Product> InCategory(this IQueryable<Product> query, int categoryId)
    {
        return query.Where(p => p.CategoryId == categoryId);
    }

    public static IQueryable<Product> PriceRange(this IQueryable<Product> query, decimal min, decimal max)
    {
        return query.Where(p => p.Price >= min && p.Price <= max);
    }
    
    public static IQueryable<Product> IncludeSoftDeleted(this IQueryable<Product> query)
    {
        return query.IgnoreQueryFilters();
    }
}

// Usage:
// var products = await _context.Products
//     .Active()
//     .InCategory(5)
//     .PriceRange(10, 100)
//     .ToListAsync();

// -----------------------------------------------------------------------------
// KEY CONVERSION NOTES:
// -----------------------------------------------------------------------------
// 1. DbContext constructor: connection string → DbContextOptions via DI
// 2. virtual keyword not required for navigation properties
// 3. Many-to-many: implicit join table → explicit join entity (ProductTag)
// 4. Soft delete: manual filtering → HasQueryFilter (automatic!)
// 5. StringLength → MaxLength attribute
// 6. Collections: HashSet → List (or keep HashSet)
// 7. Nullable reference types: string → string? for optional
// 8. DateTime.Now → DateTime.UtcNow for cloud compatibility
// 9. SaveChanges → SaveChangesAsync (always async)
// 10. DbModelBuilder → ModelBuilder (Fluent API similar but different)
// 11. LazyLoadingEnabled = false → Default in EF Core (explicit Include)
// 12. Simple getters can use [NotMapped] computed properties
