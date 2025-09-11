// SeedData.cs - Initial product data
using Microsoft.EntityFrameworkCore;
using StoreApp.Data;
using StoreApp.Models;

namespace StoreApp.Data
{
    public static class SeedData
    {
        public static void Initialize(IServiceProvider serviceProvider)
        {
            using var context = new ApplicationDbContext(
                serviceProvider.GetRequiredService<DbContextOptions<ApplicationDbContext>>());

            // Look for existing products
            if (context.Products.Any())
            {
                return; // DB has been seeded
            }

            context.Products.AddRange(
                new Product
                {
                    Name = "Classic Desk Lamp",
                    Price = 49.99M,
                    Description = "A stylish desk lamp for your home office. Features adjustable brightness and color temperature settings. The lamp includes a USB charging port and touch controls."
                },
                new Product
                {
                    Name = "Ergonomic Office Chair",
                    Price = 199.99M,
                    Description = "Comfortable chair with lumbar support. Fully adjustable height, armrests, and recline settings. Breathable mesh back keeps you cool during long work sessions."
                },
                new Product
                {
                    Name = "Wireless Keyboard",
                    Price = 79.99M,
                    Description = "Compact keyboard with quiet keys. Connects via Bluetooth to up to 3 devices simultaneously. Includes backlit keys and a rechargeable battery that lasts up to 2 weeks."
                },
                new Product
                {
                    Name = "LED Monitor",
                    Price = 249.99M,
                    Description = "24-inch full HD display. Features ultra-thin bezels, 144Hz refresh rate, and AMD FreeSync technology. Includes HDMI, DisplayPort, and USB-C connections."
                },
                new Product
                {
                    Name = "Bluetooth Speaker",
                    Price = 89.99M,
                    Description = "Portable speaker with rich bass. Waterproof design makes it perfect for outdoor use. Provides up to 12 hours of playback on a single charge and includes a built-in microphone for calls."
                }
            );

            context.SaveChanges();
        }
    }
}
