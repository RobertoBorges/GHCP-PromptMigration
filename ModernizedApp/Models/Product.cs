using System.ComponentModel.DataAnnotations;
using Microsoft.EntityFrameworkCore;

namespace ASPStoreModernized.Models
{
    public class Product
    {
        public int Id { get; set; }

        [Required]
        [StringLength(100)]
        public string Name { get; set; } = string.Empty;

        [Required]
        [Range(0.01, 10000)]
        public decimal Price { get; set; }

        [StringLength(500)]
        public string Description { get; set; } = string.Empty;
        
        [StringLength(255)]
        public string ImageUrl { get; set; } = string.Empty;
        
        [StringLength(50)]
        public string Category { get; set; } = string.Empty;
        
        public bool InStock { get; set; } = true;
    }
}
