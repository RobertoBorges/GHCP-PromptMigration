using System.ComponentModel.DataAnnotations;

namespace ASPStoreModernized.Models
{
    public class ContactForm
    {
        [Required(ErrorMessage = "Please enter your name")]
        [StringLength(100)]
        [Display(Name = "Your Name")]
        public string Name { get; set; } = string.Empty;

        [Required(ErrorMessage = "Please enter your email address")]
        [EmailAddress(ErrorMessage = "Please enter a valid email address")]
        [Display(Name = "Email Address")]
        public string Email { get; set; } = string.Empty;

        [Required(ErrorMessage = "Please enter a message")]
        [StringLength(1000)]
        [Display(Name = "Message")]
        public string Message { get; set; } = string.Empty;
    }
}
