using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using StoreApp.Models;
using StoreApp.Services;

namespace StoreApp.Pages.Products
{
    public class DetailsModel : PageModel
    {
        private readonly IProductService _productService;
        private readonly ICartService _cartService;

        public DetailsModel(IProductService productService, ICartService cartService)
        {
            _productService = productService;
            _cartService = cartService;
        }

        public Product Product { get; set; } = default!;

        [BindProperty]
        public int ProductId { get; set; }

        [BindProperty]
        public int Quantity { get; set; } = 1;

        public async Task<IActionResult> OnGetAsync(int id)
        {
            var product = await _productService.GetProductByIdAsync(id);
            
            if (product == null)
            {
                return RedirectToPage("./Index");
            }

            Product = product;
            ProductId = product.Id;
            
            return Page();
        }

        public async Task<IActionResult> OnPostAsync()
        {
            if (!ModelState.IsValid)
            {
                var product = await _productService.GetProductByIdAsync(ProductId);
                if (product == null)
                {
                    return RedirectToPage("./Index");
                }
                
                Product = product;
                return Page();
            }

            await _cartService.AddToCartAsync(ProductId, Quantity, HttpContext.Session.Id);
            
            return RedirectToPage("/Cart");
        }
    }
}
