using System.Text.Json;
using ASPStoreModernized.Data;
using ASPStoreModernized.Models;

namespace ASPStoreModernized.Services
{
    public class SessionCartService : ICartService
    {
        private readonly IHttpContextAccessor _httpContextAccessor;
        private readonly StoreDbContext _dbContext;
        private const string CartSessionKey = "ShoppingCart";

        public SessionCartService(IHttpContextAccessor httpContextAccessor, StoreDbContext dbContext)
        {
            _httpContextAccessor = httpContextAccessor;
            _dbContext = dbContext;
        }

        public ShoppingCart GetCart()
        {
            var session = _httpContextAccessor.HttpContext?.Session;
            string? cartJson = session?.GetString(CartSessionKey);
            
            if (string.IsNullOrEmpty(cartJson))
            {
                return new ShoppingCart();
            }
            
            try
            {
                return JsonSerializer.Deserialize<ShoppingCart>(cartJson) ?? new ShoppingCart();
            }
            catch
            {
                // If deserialization fails, return a new cart
                return new ShoppingCart();
            }
        }

        public void SaveCart(ShoppingCart cart)
        {
            var session = _httpContextAccessor.HttpContext?.Session;
            string cartJson = JsonSerializer.Serialize(cart);
            session?.SetString(CartSessionKey, cartJson);
        }

        public void AddToCart(Product product, int quantity = 1)
        {
            var cart = GetCart();
            cart.AddItem(product, quantity);
            SaveCart(cart);
        }

        public void RemoveFromCart(int productId)
        {
            var cart = GetCart();
            cart.RemoveItem(productId);
            SaveCart(cart);
        }

        public void UpdateCartQuantity(int productId, int quantity)
        {
            var cart = GetCart();
            cart.UpdateQuantity(productId, quantity);
            SaveCart(cart);
        }

        public void ClearCart()
        {
            var cart = GetCart();
            cart.Clear();
            SaveCart(cart);
        }

        public int GetCartItemCount()
        {
            return GetCart().TotalItems;
        }
    }
}
