// CartService.cs - Service for shopping cart functionality
using Microsoft.EntityFrameworkCore;
using StoreApp.Data;
using StoreApp.Models;

namespace StoreApp.Services
{
    public interface ICartService
    {
        Task<int> AddToCartAsync(int productId, int quantity, string sessionId);
        Task<List<CartItem>> GetCartItemsAsync(string sessionId);
        Task<int> GetCartItemCountAsync(string sessionId);
        Task ClearCartAsync(string sessionId);
    }

    public class CartService : ICartService
    {
        private readonly ApplicationDbContext _context;
        private readonly IProductService _productService;

        public CartService(ApplicationDbContext context, IProductService productService)
        {
            _context = context;
            _productService = productService;
        }

        public async Task<int> AddToCartAsync(int productId, int quantity, string sessionId)
        {
            // Check if product exists
            var product = await _productService.GetProductByIdAsync(productId);
            if (product == null)
            {
                throw new ArgumentException("Product not found", nameof(productId));
            }

            // Check if item already in cart
            var cartItem = await _context.CartItems
                .FirstOrDefaultAsync(c => c.ProductId == productId && c.SessionId == sessionId);

            if (cartItem != null)
            {
                // Update quantity if already in cart
                cartItem.Quantity += quantity;
            }
            else
            {
                // Add new item to cart
                cartItem = new CartItem
                {
                    ProductId = productId,
                    Quantity = quantity,
                    SessionId = sessionId
                };
                _context.CartItems.Add(cartItem);
            }

            await _context.SaveChangesAsync();
            return await GetCartItemCountAsync(sessionId);
        }

        public async Task<List<CartItem>> GetCartItemsAsync(string sessionId)
        {
            return await _context.CartItems
                .Where(c => c.SessionId == sessionId)
                .Include(c => c.Product)
                .ToListAsync();
        }

        public async Task<int> GetCartItemCountAsync(string sessionId)
        {
            return await _context.CartItems
                .Where(c => c.SessionId == sessionId)
                .SumAsync(c => c.Quantity);
        }

        public async Task ClearCartAsync(string sessionId)
        {
            var cartItems = await _context.CartItems
                .Where(c => c.SessionId == sessionId)
                .ToListAsync();

            _context.CartItems.RemoveRange(cartItems);
            await _context.SaveChangesAsync();
        }
    }
}
