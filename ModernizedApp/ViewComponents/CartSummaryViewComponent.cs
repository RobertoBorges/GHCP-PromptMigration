using ASPStoreModernized.Services;
using Microsoft.AspNetCore.Mvc;

namespace ASPStoreModernized.ViewComponents
{
    public class CartSummaryViewComponent : ViewComponent
    {
        private readonly ICartService _cartService;

        public CartSummaryViewComponent(ICartService cartService)
        {
            _cartService = cartService;
        }

        public IViewComponentResult Invoke()
        {
            var count = _cartService.GetCartItemCount();
            return View(count);
        }
    }
}
