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
        private readonly ICartService _cartService;

        public CartController(StoreDbContext context, ICartService cartService)
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
            try
            {
                var product = await _context.Products.FindAsync(productId);
                
                if (product == null)
                {
                    if (Request.Headers["X-Requested-With"] == "XMLHttpRequest")
                    {
                        return Json(new { success = false, message = "Product not found" });
                    }
                    return NotFound();
                }

                _cartService.AddToCart(product, quantity);
                
                // If this is an AJAX request, return JSON
                if (Request.Headers["X-Requested-With"] == "XMLHttpRequest")
                {
                    return Json(new { success = true, message = "Product added to cart", cartCount = _cartService.GetCartItemCount() });
                }
                
                return RedirectToAction(nameof(Index));
            }
            catch (Exception ex)
            {
                // Log the exception
                Console.WriteLine($"Error in AddToCart: {ex.Message}");
                
                if (Request.Headers["X-Requested-With"] == "XMLHttpRequest")
                {
                    return Json(new { success = false, message = "Error adding product to cart" });
                }
                
                TempData["ErrorMessage"] = "An error occurred while adding the product to the cart.";
                return RedirectToAction("Index", "Products");
            }
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
            _cartService.UpdateCartQuantity(productId, quantity);
            
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
