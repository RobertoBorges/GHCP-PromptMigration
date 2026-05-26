using System;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.Filters;
using Microsoft.Extensions.Caching.Memory;
using PartsUnlimited.Models;

namespace PartsUnlimited.Utils
{
    public class LayoutDataFilter : IAsyncActionFilter
    {
        private readonly IPartsUnlimitedContext _dataContext;
        private readonly IMemoryCache _cache;

        public LayoutDataFilter(IPartsUnlimitedContext dataContext, IMemoryCache cache)
        {
            _dataContext = dataContext;
            _cache = cache;
        }

        public async Task OnActionExecutionAsync(ActionExecutingContext context, ActionExecutionDelegate next)
        {
            try
            {
                if (context.Controller is Controller controller)
                {
                    var cart = ShoppingCart.GetCart(_dataContext, context.HttpContext);
                    var items = cart.GetCartItems();
                    var summary = items.Select(a => a.Product?.Title).Where(t => t != null).OrderBy(x => x).ToList();
                    var cartCount = items.Sum(i => i.Count);

                    if (!_cache.TryGetValue<Product>("latestProduct", out var latestProduct))
                    {
                        latestProduct = _dataContext.Products.OrderByDescending(a => a.Created).FirstOrDefault();
                        if (latestProduct != null)
                        {
                            _cache.Set("latestProduct", latestProduct, TimeSpan.FromMinutes(10));
                        }
                    }

                    controller.ViewBag.Categories = _dataContext.Categories.ToList();
                    controller.ViewBag.CartSummary = summary;
                    controller.ViewBag.CartCount = cartCount;
                    controller.ViewBag.Product = latestProduct;
                }
            }
            catch
            {
                // Layout data is best-effort; never break the request.
            }

            await next();
        }
    }
}
