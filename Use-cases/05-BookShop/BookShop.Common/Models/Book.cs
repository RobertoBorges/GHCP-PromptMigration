using System;
using System.Collections.Generic;
using System.Text;

namespace BookShop.Common.Models
{
    public class Book
    {
        public int BookId { get; set; }
        public string Title { get; set; }
        public string ISBN { get; set; }
        public string Description { get; set; }
        public decimal Price { get; set; }
        public int StockQuantity { get; set; }
        public DateTime PublicationDate { get; set; }
        public string ImageUrl { get; set; }
        public bool IsActive { get; set; }
        public DateTime CreatedDate { get; set; }
        public DateTime ModifiedDate { get; set; }
        
        // Foreign Keys
        public int AuthorId { get; set; }
        public int CategoryId { get; set; }
        
        // Navigation Properties
        public Author Author { get; set; }
        public Category Category { get; set; }
    }
}