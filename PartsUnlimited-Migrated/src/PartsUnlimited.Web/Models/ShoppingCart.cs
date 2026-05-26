using System;
using System.Collections.Generic;
using System.Linq;
using Microsoft.AspNetCore.Http;
using Microsoft.EntityFrameworkCore;

namespace PartsUnlimited.Models
{
    public partial class ShoppingCart
    {
        private readonly IPartsUnlimitedContext _db;
        string ShoppingCartId { get; set; }

        public ShoppingCart(IPartsUnlimitedContext db)
        {
            _db = db;
        }

        public static ShoppingCart GetCart(IPartsUnlimitedContext db, HttpContext context)
        {
            var cart = new ShoppingCart(db);
            cart.ShoppingCartId = cart.GetCartId(context);
            return cart;
        }

        public void AddToCart(Product product)
        {
            var cartItem = _db.CartItems.SingleOrDefault(
                c => c.CartId == ShoppingCartId
                && c.ProductId == product.ProductId);

            if (cartItem == null)
            {
                cartItem = new CartItem
                {
                    ProductId = product.ProductId,
                    CartId = ShoppingCartId,
                    Count = 1,
                    DateCreated = DateTime.Now
                };
                _db.CartItems.Add(cartItem);
            }
            else
            {
                cartItem.Count++;
            }
        }

        public int RemoveFromCart(int id)
        {
            var cartItem = _db.CartItems.Single(
                cart => cart.CartId == ShoppingCartId
                && cart.CartItemId == id);

            int itemCount = 0;

            if (cartItem != null)
            {
                if (cartItem.Count > 1)
                {
                    cartItem.Count--;
                    itemCount = cartItem.Count;
                }
                else
                {
                    _db.CartItems.Remove(cartItem);
                }
            }

            return itemCount;
        }

        public void EmptyCart()
        {
            var cartItems = _db.CartItems.Where(cart => cart.CartId == ShoppingCartId).ToList();
            foreach (var item in cartItems)
                _db.CartItems.Remove(item);
        }

        public List<CartItem> GetCartItems()
        {
            return _db.CartItems.Where(cart => cart.CartId == ShoppingCartId).Include(c => c.Product).ToList();
        }

        public int GetCount()
        {
            int sum = _db.CartItems
                .Where(c => c.CartId == ShoppingCartId)
                .Sum(c => (int?)c.Count) ?? 0;
            return sum;
        }

        public decimal GetTotal()
        {
            decimal total = 0;
            foreach (var item in _db.CartItems.Include(c => c.Product).Where(c => c.CartId == ShoppingCartId))
            {
                total += item.Count * item.Product.Price;
            }
            return total;
        }

        public int CreateOrder(Order order)
        {
            decimal orderTotal = 0;

            var cartItems = GetCartItems();

            foreach (var item in cartItems)
            {
                var product = _db.Products.Single(a => a.ProductId == item.ProductId);

                var orderDetail = new OrderDetail
                {
                    ProductId = item.ProductId,
                    OrderId = order.OrderId,
                    UnitPrice = product.Price,
                    Count = item.Count,
                };

                orderTotal += (item.Count * product.Price);
                _db.OrderDetails.Add(orderDetail);
            }

            order.Total = orderTotal;
            EmptyCart();
            return order.OrderId;
        }

        public string GetCartId(HttpContext context)
        {
            string cartId = context.Request.Cookies["Session"];
            if (string.IsNullOrEmpty(cartId))
            {
                cartId = Guid.NewGuid().ToString();
                context.Response.Cookies.Append("Session", cartId, new CookieOptions
                {
                    Expires = DateTimeOffset.UtcNow.AddDays(30),
                    HttpOnly = true,
                    IsEssential = true
                });
            }
            return cartId;
        }
    }
}
