using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.EntityFrameworkCore;
using PartsUnlimited.Models;
using PartsUnlimited.ViewModels;

namespace PartsUnlimited.Utils
{
    public class OrdersQuery : IOrdersQuery
    {
        private readonly IPartsUnlimitedContext db;

        public OrdersQuery(IPartsUnlimitedContext context)
        {
            db = context;
        }

        public async Task<OrdersModel> IndexHelperAsync(string username, DateTime? start, DateTime? end, string invalidOrderSearch, bool isAdminSearch)
        {
            var queryStart = (start ?? DateTime.Now).Date;
            var queryEnd = (end ?? DateTime.Now).Date.AddDays(1).AddSeconds(-1);

            var results = await GetOrderQuery(username, queryStart, queryEnd).ToListAsync();

            await FillOrderDetails(results);

            return new OrdersModel(results, username, queryStart, queryEnd, invalidOrderSearch, isAdminSearch);
        }

        private IQueryable<Order> GetOrderQuery(string username, DateTime start, DateTime end)
        {
            if (string.IsNullOrEmpty(username))
            {
                return db.Orders
                    .Where(o => o.OrderDate < end && o.OrderDate >= start)
                    .OrderBy(o => o.OrderDate);
            }
            return db.Orders
                .Where(o => o.OrderDate < end && o.OrderDate >= start && o.Username == username)
                .OrderBy(o => o.OrderDate);
        }

        public async Task<Order> FindOrderAsync(int id)
        {
            var order = await db.Orders.FirstOrDefaultAsync(o => o.OrderId == id);
            if (order != null)
            {
                await FillOrderDetails(new[] { order });
            }
            return order;
        }

        private async Task FillOrderDetails(IEnumerable<Order> orders)
        {
            foreach (var order in orders)
            {
                if (order == null) continue;
                order.OrderDetails = await db.OrderDetails.Where(o => o.OrderId == order.OrderId).ToListAsync();

                foreach (var details in order.OrderDetails)
                {
                    details.Product = await db.Products.FirstOrDefaultAsync(o => o.ProductId == details.ProductId);
                }
            }
        }
    }
}
