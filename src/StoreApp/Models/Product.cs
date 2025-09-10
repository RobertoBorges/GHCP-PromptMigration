using System.ComponentModel.DataAnnotations;

namespace StoreApp.Models
{
    public class Product
    {
        public int Id { get; set; }
        
        [Required]
        [StringLength(100)]
        public string Name { get; set; } = string.Empty;
        
        [Required]
        [Range(0.01, 10000)]
        [DataType(DataType.Currency)]
        public decimal Price { get; set; }
        
        [Required]
        [StringLength(500)]
        public string Description { get; set; } = string.Empty;
    }
}
