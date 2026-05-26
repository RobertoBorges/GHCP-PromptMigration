using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using PartsUnlimited.Models;
using PartsUnlimited.Utils;
using PartsUnlimited.ViewModels;

namespace PartsUnlimited.Controllers
{
    public class ShoppingCartController : Controller
    {
        private readonly IPartsUnlimitedContext db;
        private readonly ITelemetryProvider telemetry;
        private readonly IShippingTaxCalculator shippingTaxCalculator;

        public ShoppingCartController(IPartsUnlimitedContext context, ITelemetryProvider telemetryProvider,
            IShippingTaxCalculator shippingTaxCalc)
        {
            db = context;
            telemetry = telemetryProvider;
            shippingTaxCalculator = shippingTaxCalc;
        }

        public IActionResult Index()
        {
            var cart = ShoppingCart.GetCart(db, HttpContext);
            var items = cart.GetCartItems();
            var itemsCount = items.Sum(x => x.Count);
            var costSummary = shippingTaxCalculator.CalculateCost(items, null);

            var viewModel = new ShoppingCartViewModel
            {
                CartItems = items,
                CartCount = itemsCount,
                OrderCostSummary = costSummary
            };

            telemetry.TrackTrace("Cart/Server/Index");
            return View(viewModel);
        }

        public async Task<IActionResult> AddToCart(int id)
        {
            var addedProduct = db.Products.Single(product => product.ProductId == id);
            var startTime = DateTime.Now;
            var cart = ShoppingCart.GetCart(db, HttpContext);
            cart.AddToCart(addedProduct);
            await db.SaveChangesAsync(CancellationToken.None);

            var measurements = new Dictionary<string, double>
            {
                { "ElapsedMilliseconds", DateTime.Now.Subtract(startTime).TotalMilliseconds }
            };
            telemetry.TrackEvent("Cart/Server/Add", null, measurements);

            return RedirectToAction("Index");
        }

        [HttpPost]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> RemoveFromCart([FromQuery] int id)
        {
            var startTime = DateTime.Now;
            var cart = ShoppingCart.GetCart(db, HttpContext);

            var cartItem = db.CartItems.Include(c => c.Product).Single(item => item.CartItemId == id);
            string productName = cartItem.Product.Title;

            int itemCount = cart.RemoveFromCart(id);
            await db.SaveChangesAsync(CancellationToken.None);

            string removed = (itemCount > 0) ? " 1 copy of " : string.Empty;

            var measurements = new Dictionary<string, double>
            {
                { "ElapsedMilliseconds", DateTime.Now.Subtract(startTime).TotalMilliseconds }
            };
            telemetry.TrackEvent("Cart/Server/Remove", null, measurements);

            var items = cart.GetCartItems();
            var itemsCount = items.Sum(x => x.Count);
            var subTotal = items.Sum(x => x.Count * x.Product.Price);
            var shipping = itemsCount * 5.00m;
            var tax = (subTotal + shipping) * 0.05m;
            var total = subTotal + shipping + tax;

            var results = new ShoppingCartRemoveViewModel
            {
                Message = removed + productName + " has been removed from your shopping cart.",
                CartSubTotal = subTotal.ToString("C"),
                CartShipping = shipping.ToString("C"),
                CartTax = tax.ToString("C"),
                CartTotal = total.ToString("C"),
                CartCount = itemsCount,
                ItemCount = itemCount,
                DeleteId = id
            };

            return Json(results);
        }
    }
}
