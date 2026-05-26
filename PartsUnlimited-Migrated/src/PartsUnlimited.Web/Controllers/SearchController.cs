using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using PartsUnlimited.ProductSearch;

namespace PartsUnlimited.Controllers
{
    public class SearchController : Controller
    {
        private readonly IProductSearch search;

        public SearchController(IProductSearch search)
        {
            this.search = search;
        }

        [HttpGet]
        public async Task<IActionResult> Index(string q)
        {
            var result = await search.Search(q);
            return View(result);
        }
    }
}
