using ASPStoreModernized.Models;

namespace ASPStoreModernized.Services
{
    public interface ICartService
    {
        ShoppingCart GetCart();
        void SaveCart(ShoppingCart cart);
        void AddToCart(Product product, int quantity = 1);
        void RemoveFromCart(int productId);
        void UpdateCartQuantity(int productId, int quantity);
        void ClearCart();
        int GetCartItemCount();
    }
}
