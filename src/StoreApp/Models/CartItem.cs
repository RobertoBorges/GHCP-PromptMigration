using System.ComponentModel.DataAnnotations;

namespace StoreApp.Models
{
    public class CartItem
    {
        public int Id { get; set; }
        
        [Required]
        public int ProductId { get; set; }
        
        public Product? Product { get; set; }
        
        [Required]
        [Range(1, 100)]
        public int Quantity { get; set; } = 1;
        
        public string SessionId { get; set; } = string.Empty;
    }
}
