using Microsoft.AspNetCore.Mvc;
using ASPStoreModernized.Models;
using ASPStoreModernized.Services;
using ASPStoreModernized.Data;
using Microsoft.EntityFrameworkCore;

namespace ASPStoreModernized.Controllers
{
    public class CartController : Controller
    {
        private readonly StoreDbContext _context;
        private readonly SessionCartService _cartService;

        public CartController(StoreDbContext context, SessionCartService cartService)
        {
            _context = context;
            _cartService = cartService;
        }

        public IActionResult Index()
        {
            var cart = _cartService.GetCart();
            return View(cart);
        }

        [HttpPost]
        public async Task<IActionResult> AddToCart(int productId, int quantity = 1)
        {
            var product = await _context.Products.FindAsync(productId);
            
            if (product == null)
            {
                return NotFound();
            }

            _cartService.AddToCart(product, quantity);
            
            // If this is an AJAX request, return a partial view or JSON
            if (Request.Headers["X-Requested-With"] == "XMLHttpRequest")
            {
                return Json(new { success = true, message = "Product added to cart", cartCount = _cartService.GetCartItemCount() });
            }
            
            return RedirectToAction(nameof(Index));
        }

        [HttpPost]
        public IActionResult RemoveFromCart(int productId)
        {
            _cartService.RemoveFromCart(productId);
            
            if (Request.Headers["X-Requested-With"] == "XMLHttpRequest")
            {
                return Json(new { success = true, message = "Product removed from cart", cartCount = _cartService.GetCartItemCount() });
            }
            
            return RedirectToAction(nameof(Index));
        }

        [HttpPost]
        public IActionResult UpdateQuantity(int productId, int quantity)
        {
            _cartService.UpdateQuantity(productId, quantity);
            
            if (Request.Headers["X-Requested-With"] == "XMLHttpRequest")
            {
                var cart = _cartService.GetCart();
                var item = cart.Items.FirstOrDefault(i => i.ProductId == productId);
                
                return Json(new { 
                    success = true, 
                    message = "Quantity updated", 
                    cartCount = _cartService.GetCartItemCount(),
                    itemTotal = item?.Total ?? 0,
                    cartTotal = cart.TotalPrice
                });
            }
            
            return RedirectToAction(nameof(Index));
        }

        [HttpPost]
        public IActionResult ClearCart()
        {
            _cartService.ClearCart();
            
            if (Request.Headers["X-Requested-With"] == "XMLHttpRequest")
            {
                return Json(new { success = true, message = "Cart cleared", cartCount = 0 });
            }
            
            return RedirectToAction(nameof(Index));
        }
    }
}
