using System;
using System.Collections.Generic;
using System.Text;

namespace BookShop.Common.Models
{
    public class OrderItem
    {
        public int OrderItemId { get; set; }
        public int Quantity { get; set; }
        public decimal UnitPrice { get; set; }
        public decimal TotalPrice { get; set; }
        public DateTime CreatedDate { get; set; }
        
        // Foreign Keys
        public int OrderId { get; set; }
        public int BookId { get; set; }
        
        // Navigation Properties
        public Order Order { get; set; }
        public Book Book { get; set; }
    }
}