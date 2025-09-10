using Microsoft.AspNetCore.Mvc;
using StoreApp.Services;

namespace StoreApp.ViewComponents
{
    public class CartSummaryViewComponent : ViewComponent
    {
        private readonly ICartService _cartService;

        public CartSummaryViewComponent(ICartService cartService)
        {
            _cartService = cartService;
        }

        public async Task<IViewComponentResult> InvokeAsync()
        {
            var sessionId = HttpContext.Session.Id;
            var cartItemCount = await _cartService.GetCartItemCountAsync(sessionId);
            return View(cartItemCount);
        }
    }
}
