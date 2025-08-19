using System;
using System.Collections.Generic;
using System.Text;

namespace BookShop.Common.Models
{
    public class Order
    {
        public int OrderId { get; set; }
        public DateTime OrderDate { get; set; }
        public decimal TotalAmount { get; set; }
        public string Status { get; set; }
        public string ShippingAddress { get; set; }
        public string BillingAddress { get; set; }
        public DateTime? ShippedDate { get; set; }
        public string TrackingNumber { get; set; }
        public DateTime CreatedDate { get; set; }
        public DateTime ModifiedDate { get; set; }
        
        // Foreign Keys
        public int CustomerId { get; set; }
        public int? EmployeeId { get; set; }
        
        // Navigation Properties
        public Customer Customer { get; set; }
        public Employee Employee { get; set; }
        public List<OrderItem> OrderItems { get; set; }
        
        public Order()
        {
            OrderItems = new List<OrderItem>();
        }
    }
}