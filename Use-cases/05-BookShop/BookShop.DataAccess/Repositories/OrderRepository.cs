using System;
using System.Collections.Generic;
using System.Text;
using BookShop.Common.Models;
using BookShop.DataAccess.Base;

namespace BookShop.DataAccess.Repositories
{
    public class OrderRepository : BaseRepository
    {
        // Basic order repository for future expansion  
        public int InsertOrder(Order order)
        {
            string query = @"
                INSERT INTO Orders (OrderDate, TotalAmount, Status, ShippingAddress, BillingAddress, CustomerId, EmployeeId, CreatedDate, ModifiedDate)
                VALUES (@OrderDate, @TotalAmount, @Status, @ShippingAddress, @BillingAddress, @CustomerId, @EmployeeId, @CreatedDate, @ModifiedDate);
                SELECT SCOPE_IDENTITY();";

            var parameters = new[] {
                CreateParameter("@OrderDate", order.OrderDate),
                CreateParameter("@TotalAmount", order.TotalAmount),
                CreateParameter("@Status", order.Status),
                CreateParameter("@ShippingAddress", order.ShippingAddress),
                CreateParameter("@BillingAddress", order.BillingAddress),
                CreateParameter("@CustomerId", order.CustomerId),
                CreateParameter("@EmployeeId", order.EmployeeId),
                CreateParameter("@CreatedDate", DateTime.Now),
                CreateParameter("@ModifiedDate", DateTime.Now)
            };

            object result = ExecuteScalar(query, parameters);
            return Convert.ToInt32(result);
        }
    }
}