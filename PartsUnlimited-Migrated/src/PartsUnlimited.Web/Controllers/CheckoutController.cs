using System;
using System.Linq;
using System.Threading;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Identity;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using PartsUnlimited.Models;

namespace PartsUnlimited.Controllers
{
    [Authorize]
    public class CheckoutController : Controller
    {
        private readonly IPartsUnlimitedContext db;
        private readonly UserManager<ApplicationUser> _userManager;

        public CheckoutController(IPartsUnlimitedContext context, UserManager<ApplicationUser> userManager)
        {
            db = context;
            _userManager = userManager;
        }

        const string PromoCode = "FREE";

        public async Task<IActionResult> AddressAndPayment()
        {
            var id = _userManager.GetUserId(User);
            var user = await db.Users.FirstOrDefaultAsync(o => o.Id == id);

            var order = new Order
            {
                Name = user?.Name,
                Email = user?.Email,
                Username = user?.UserName
            };

            return View(order);
        }

        [HttpPost]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> AddressAndPayment(Order order)
        {
            var formCollection = Request.Form;

            try
            {
                if (string.Equals(formCollection["PromoCode"].ToString(), PromoCode, StringComparison.OrdinalIgnoreCase) == false)
                {
                    return View(order);
                }

                order.Username = User.Identity!.Name;
                order.OrderDate = DateTime.Now;

                db.Orders.Add(order);

                var cart = ShoppingCart.GetCart(db, HttpContext);
                cart.CreateOrder(order);

                await db.SaveChangesAsync(CancellationToken.None);

                return RedirectToAction("Complete", new { id = order.OrderId });
            }
            catch
            {
                return View(order);
            }
        }

        public IActionResult Complete(int id)
        {
            var username = User.Identity!.Name;

            var order = db.Orders.FirstOrDefault(o => o.OrderId == id && o.Username == username);

            if (order != null)
            {
                return View(order);
            }
            return View("Error");
        }
    }
}
