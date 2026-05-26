using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using PartsUnlimited.Models;

namespace PartsUnlimited.Api
{
    [ApiController]
    [Route("api/products")]
    public class ProductsController : ControllerBase
    {
        private readonly IPartsUnlimitedContext _context;

        public ProductsController(IPartsUnlimitedContext context)
        {
            _context = context;
        }

        [HttpGet]
        public IEnumerable<Product> Get(bool sale = false)
        {
            if (!sale)
            {
                return _context.Products.ToList();
            }
            return _context.Products.Where(p => p.Price != p.SalePrice).ToList();
        }

        [HttpGet("{id}")]
        public async Task<IActionResult> Get(int id)
        {
            var product = await _context.Products.FirstOrDefaultAsync(p => p.ProductId == id);
            if (product == null)
            {
                return NotFound();
            }
            return Ok(product);
        }
    }
}
