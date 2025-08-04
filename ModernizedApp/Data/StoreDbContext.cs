using Microsoft.EntityFrameworkCore;
using ASPStoreModernized.Models;

namespace ASPStoreModernized.Data
{
    public class StoreDbContext : DbContext
    {
        public StoreDbContext(DbContextOptions<StoreDbContext> options)
            : base(options)
        {
        }

        public DbSet<Product> Products { get; set; } = null!;

        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {
            base.OnModelCreating(modelBuilder);

            // Seed product data
            modelBuilder.Entity<Product>().HasData(
                new Product
                {
                    Id = 1,
                    Name = "Classic Desk Lamp",
                    Price = 49.99M,
                    Description = "A stylish desk lamp for your home office. Features adjustable brightness and color temperature settings. The lamp includes a USB charging port and touch controls."
                },
                new Product
                {
                    Id = 2,
                    Name = "Ergonomic Office Chair",
                    Price = 199.99M,
                    Description = "Comfortable chair with lumbar support. Fully adjustable height, armrests, and recline settings. Breathable mesh back keeps you cool during long work sessions."
                },
                new Product
                {
                    Id = 3,
                    Name = "Wireless Keyboard",
                    Price = 79.99M,
                    Description = "Compact keyboard with quiet keys. Connects via Bluetooth to up to 3 devices simultaneously. Includes backlit keys and a rechargeable battery that lasts up to 2 weeks."
                },
                new Product
                {
                    Id = 4,
                    Name = "LED Monitor",
                    Price = 249.99M,
                    Description = "24-inch full HD display. Features ultra-thin bezels, 144Hz refresh rate, and AMD FreeSync technology. Includes HDMI, DisplayPort, and USB-C connections."
                },
                new Product
                {
                    Id = 5,
                    Name = "Bluetooth Speaker",
                    Price = 89.99M,
                    Description = "Portable speaker with rich bass. Waterproof design makes it perfect for outdoor use. Provides up to 12 hours of playback on a single charge and includes a built-in microphone for calls."
                }
            );
        }
    }
}
