using Microsoft.AspNetCore.Identity.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore;

namespace PartsUnlimited.Models
{
    public class PartsUnlimitedContext : IdentityDbContext<ApplicationUser>, IPartsUnlimitedContext
    {
        public PartsUnlimitedContext(DbContextOptions<PartsUnlimitedContext> options) : base(options)
        {
        }

        public DbSet<Product> Products { get; set; }
        public DbSet<Order> Orders { get; set; }
        public DbSet<Category> Categories { get; set; }
        public DbSet<CartItem> CartItems { get; set; }
        public DbSet<OrderDetail> OrderDetails { get; set; }
        public DbSet<Raincheck> RainChecks { get; set; }
        public DbSet<Store> Stores { get; set; }

        DbSet<ApplicationUser> IPartsUnlimitedContext.Users => base.Users;

        protected override void OnModelCreating(ModelBuilder builder)
        {
            base.OnModelCreating(builder);
            builder.Entity<Product>().HasKey(a => a.ProductId);
            builder.Entity<Order>().HasKey(o => o.OrderId);
            builder.Entity<Category>().HasKey(g => g.CategoryId);
            builder.Entity<CartItem>().HasKey(c => c.CartItemId);
            builder.Entity<OrderDetail>().HasKey(o => o.OrderDetailId);
            builder.Entity<Raincheck>().HasKey(o => o.RaincheckId);
            builder.Entity<Store>().HasKey(o => o.StoreId);

            // Decimal precision for SQL Server
            builder.Entity<Product>().Property(p => p.Price).HasPrecision(18, 2);
            builder.Entity<Product>().Property(p => p.SalePrice).HasPrecision(18, 2);
            builder.Entity<Order>().Property(o => o.Total).HasPrecision(18, 2);
            builder.Entity<OrderDetail>().Property(o => o.UnitPrice).HasPrecision(18, 2);
        }
    }
}
