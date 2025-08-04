using ASPStoreModernized.Models;

namespace ASPStoreModernized.Data
{
    public static class DbInitializer
    {
        public static void Initialize(StoreDbContext context)
        {
            // Create the database if it doesn't exist
            context.Database.EnsureCreated();

            // Check if there are already products
            if (context.Products.Any())
            {
                return; // Database has been seeded
            }

            // Seed products
            var products = new Product[]
            {
                new Product
                {
                    Name = "Classic T-Shirt",
                    Description = "A comfortable and stylish t-shirt for everyday wear.",
                    Price = 19.99m,
                    ImageUrl = "/images/products/tshirt.jpg",
                    Category = "Apparel",
                    InStock = true
                },
                new Product
                {
                    Name = "Retro Denim Jeans",
                    Description = "High-quality denim jeans with a classic fit and style.",
                    Price = 49.99m,
                    ImageUrl = "/images/products/jeans.jpg",
                    Category = "Apparel",
                    InStock = true
                },
                new Product
                {
                    Name = "Vintage Watch",
                    Description = "Elegant timepiece with a leather strap and classic design.",
                    Price = 129.99m,
                    ImageUrl = "/images/products/watch.jpg",
                    Category = "Accessories",
                    InStock = true
                },
                new Product
                {
                    Name = "Leather Wallet",
                    Description = "Handcrafted leather wallet with multiple card slots and compartments.",
                    Price = 39.99m,
                    ImageUrl = "/images/products/wallet.jpg",
                    Category = "Accessories",
                    InStock = true
                },
                new Product
                {
                    Name = "Wireless Headphones",
                    Description = "Premium wireless headphones with noise cancellation and long battery life.",
                    Price = 199.99m,
                    ImageUrl = "/images/products/headphones.jpg",
                    Category = "Electronics",
                    InStock = true
                },
                new Product
                {
                    Name = "Smartphone Case",
                    Description = "Durable protective case for your smartphone with a sleek design.",
                    Price = 24.99m,
                    ImageUrl = "/images/products/phone-case.jpg",
                    Category = "Electronics",
                    InStock = true
                }
            };

            context.Products.AddRange(products);
            context.SaveChanges();
        }
    }
}
