using Microsoft.AspNetCore.Mvc;
using ASPStoreModernized.Models;
using ASPStoreModernized.Data;
using Microsoft.EntityFrameworkCore;

namespace ASPStoreModernized.Controllers
{
    public class ProductsController : Controller
    {
        private readonly StoreDbContext _context;

        public ProductsController(StoreDbContext context)
        {
            _context = context;
        }

        // GET: Products
        public async Task<IActionResult> Index()
        {
            var products = await _context.Products.ToListAsync();
            return View(products);
        }

        // GET: Products/Details/5
        public async Task<IActionResult> Details(int? id)
        {
            if (id == null)
            {
                return NotFound();
            }

            var product = await _context.Products
                .FirstOrDefaultAsync(m => m.Id == id);
            
            if (product == null)
            {
                return NotFound();
            }

            return View(product);
        }
    }
}
