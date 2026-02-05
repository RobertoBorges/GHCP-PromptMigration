// =============================================================================
// .NET Framework to .NET 8 Controller Conversion Example
// =============================================================================

// -----------------------------------------------------------------------------
// BEFORE: .NET Framework MVC Controller (Controllers/ProductController.cs)
// -----------------------------------------------------------------------------
/*
using System.Web.Mvc;
using ProjectName.Services;
using ProjectName.Models;

namespace ProjectName.Controllers
{
    public class ProductController : Controller
    {
        private readonly ProductService _productService;

        public ProductController()
        {
            _productService = new ProductService(); // Manual instantiation
        }

        public ActionResult Index()
        {
            var products = _productService.GetAllProducts();
            return View(products);
        }

        public ActionResult Details(int id)
        {
            var product = _productService.GetProductById(id);
            
            if (product == null)
            {
                return HttpNotFound();
            }
            
            return View(product);
        }

        [HttpPost]
        [ValidateAntiForgeryToken]
        public ActionResult Create(ProductViewModel model)
        {
            if (!ModelState.IsValid)
            {
                return View(model);
            }

            var product = _productService.CreateProduct(model);
            
            TempData["Success"] = "Product created successfully.";
            return RedirectToAction("Details", new { id = product.Id });
        }

        [HttpPost]
        [ValidateAntiForgeryToken]
        public ActionResult Edit(int id, ProductViewModel model)
        {
            if (!ModelState.IsValid)
            {
                return View(model);
            }

            _productService.UpdateProduct(id, model);
            
            TempData["Success"] = "Product updated successfully.";
            return RedirectToAction("Details", new { id });
        }

        [HttpPost]
        [ValidateAntiForgeryToken]
        public ActionResult Delete(int id)
        {
            _productService.DeleteProduct(id);
            
            TempData["Success"] = "Product deleted successfully.";
            return RedirectToAction("Index");
        }
    }
}
*/

// -----------------------------------------------------------------------------
// AFTER: .NET 8 Controller (Controllers/ProductController.cs)
// -----------------------------------------------------------------------------

using Microsoft.AspNetCore.Mvc;
using ProjectName.Models.DTOs;
using ProjectName.Services.Interfaces;

namespace ProjectName.Controllers;

public class ProductController : Controller
{
    private readonly IProductService _productService;
    private readonly ILogger<ProductController> _logger;

    // Constructor injection (replaces manual instantiation)
    public ProductController(
        IProductService productService,
        ILogger<ProductController> logger)
    {
        _productService = productService;
        _logger = logger;
    }

    // GET: /products
    public async Task<IActionResult> Index()
    {
        var products = await _productService.GetAllProductsAsync();
        return View(products);
    }

    // GET: /products/{id}
    public async Task<IActionResult> Details(int id)
    {
        var product = await _productService.GetProductByIdAsync(id);
        
        if (product is null)
        {
            return NotFound(); // Replaces HttpNotFound()
        }
        
        return View(product);
    }

    // POST: /products
    [HttpPost]
    [ValidateAntiForgeryToken]
    public async Task<IActionResult> Create([FromForm] CreateProductDto dto)
    {
        if (!ModelState.IsValid)
        {
            return View(dto);
        }

        var product = await _productService.CreateProductAsync(dto);
        
        TempData["Success"] = "Product created successfully.";
        return RedirectToAction(nameof(Details), new { id = product.Id });
    }

    // POST: /products/{id}/edit
    [HttpPost]
    [ValidateAntiForgeryToken]
    public async Task<IActionResult> Edit(int id, [FromForm] UpdateProductDto dto)
    {
        if (!ModelState.IsValid)
        {
            return View(dto);
        }

        await _productService.UpdateProductAsync(id, dto);
        
        TempData["Success"] = "Product updated successfully.";
        return RedirectToAction(nameof(Details), new { id });
    }

    // POST: /products/{id}/delete
    [HttpPost]
    [ValidateAntiForgeryToken]
    public async Task<IActionResult> Delete(int id)
    {
        await _productService.DeleteProductAsync(id);
        
        TempData["Success"] = "Product deleted successfully.";
        return RedirectToAction(nameof(Index));
    }
}

// -----------------------------------------------------------------------------
// DTO for Create (Models/DTOs/CreateProductDto.cs)
// -----------------------------------------------------------------------------

namespace ProjectName.Models.DTOs;

public class CreateProductDto
{
    [Required]
    [MaxLength(255)]
    public string Name { get; set; } = string.Empty;

    [Required]
    [Range(0, double.MaxValue)]
    public decimal Price { get; set; }

    public string? Description { get; set; }
}

// -----------------------------------------------------------------------------
// KEY CONVERSION NOTES:
// -----------------------------------------------------------------------------
// 1. System.Web.Mvc → Microsoft.AspNetCore.Mvc
// 2. Manual service instantiation → Constructor injection with interfaces
// 3. Add ILogger for logging
// 4. All methods become async with Task<IActionResult>
// 5. ActionResult → IActionResult
// 6. HttpNotFound() → NotFound()
// 7. Use nameof() for action names in redirects
// 8. Add [FromForm] for form data binding (explicit)
// 9. Use DTOs instead of ViewModels for input
// 10. Nullable reference types enabled (string?)
