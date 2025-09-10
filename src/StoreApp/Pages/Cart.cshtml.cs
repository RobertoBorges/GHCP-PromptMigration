using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using StoreApp.Models;
using StoreApp.Services;

namespace StoreApp.Pages
{
    public class CartModel : PageModel
    {
        private readonly ICartService _cartService;

        public CartModel(ICartService cartService)
        {
            _cartService = cartService;
        }

        public List<CartItem> CartItems { get; set; } = new List<CartItem>();
        
        public decimal CartTotal => CartItems.Sum(item => item.Product?.Price * item.Quantity ?? 0);

        public async Task OnGetAsync()
        {
            CartItems = await _cartService.GetCartItemsAsync(HttpContext.Session.Id);
        }

        public async Task<IActionResult> OnPostClearAsync()
        {
            await _cartService.ClearCartAsync(HttpContext.Session.Id);
            return RedirectToPage();
        }
    }
}
