using System;
using System.Threading;
using System.Threading.Tasks;
using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.ChangeTracking;

namespace PartsUnlimited.Models
{
    public interface IPartsUnlimitedContext : IDisposable
    {
        DbSet<CartItem> CartItems { get; }
        DbSet<Category> Categories { get; }
        DbSet<OrderDetail> OrderDetails { get; }
        DbSet<Order> Orders { get; }
        DbSet<Product> Products { get; }
        DbSet<ApplicationUser> Users { get; }
        DbSet<Raincheck> RainChecks { get; }
        DbSet<Store> Stores { get; }

        Task<int> SaveChangesAsync(CancellationToken requestAborted);
        EntityEntry Entry(object entity);
    }
}
