using Microsoft.AspNetCore.Mvc.RazorPages;
using StoreApp.Models;
using StoreApp.Services;

namespace StoreApp.Pages.Products
{
    public class ProductsModel : PageModel
    {
        private readonly IProductService _productService;

        public ProductsModel(IProductService productService)
        {
            _productService = productService;
        }

        public IList<Product> Products { get; set; } = default!;

        public async Task OnGetAsync()
        {
            Products = await _productService.GetAllProductsAsync();
        }
    }
}
