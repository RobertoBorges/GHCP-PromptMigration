using System;
using System.Linq;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Caching.Memory;
using Microsoft.Extensions.Configuration;
using PartsUnlimited.Models;
using PartsUnlimited.ViewModels;

namespace PartsUnlimited.Controllers
{
    public class StoreController : Controller
    {
        private readonly IPartsUnlimitedContext db;
        private readonly IMemoryCache _cache;
        private readonly IConfiguration _configuration;

        public StoreController(IPartsUnlimitedContext context, IMemoryCache cache, IConfiguration configuration)
        {
            db = context;
            _cache = cache;
            _configuration = configuration;
        }

        public IActionResult Index()
        {
            var genres = db.Categories.ToList();
            return View(genres);
        }

        public IActionResult Browse(int categoryId)
        {
            var genreModel = db.Categories.Include(g => g.Products).Single(g => g.CategoryId == categoryId);
            return View(genreModel);
        }

        public IActionResult Details(int id)
        {
            var productCacheKey = string.Format("product_{0}", id);
            if (!_cache.TryGetValue<Product>(productCacheKey, out var product))
            {
                product = db.Products.Single(a => a.ProductId == id);
                _cache.Set(productCacheKey, product, new MemoryCacheEntryOptions
                {
                    SlidingExpiration = TimeSpan.FromMinutes(10)
                });
            }

            var viewModel = new ProductViewModel
            {
                Product = product,
                ShowRecommendations = _configuration.GetValue<bool>("AppSettings:ShowRecommendations")
            };

            return View(viewModel);
        }
    }
}
