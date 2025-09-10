using System.ComponentModel.DataAnnotations;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;

namespace StoreApp.Pages
{
    public class ContactModel : PageModel
    {
        private readonly ILogger<ContactModel> _logger;

        public ContactModel(ILogger<ContactModel> logger)
        {
            _logger = logger;
        }

        [BindProperty]
        public ContactForm Contact { get; set; } = new();

        public bool MessageSent { get; private set; }

        public void OnGet()
        {
        }

        public IActionResult OnPost()
        {
            if (!ModelState.IsValid)
            {
                return Page();
            }

            // In a real application, you would save this to a database or send an email
            // For this demo, we'll just log the message and display a success message
            _logger.LogInformation("Contact form submitted: {Name}, {Email}, {Message}", 
                Contact.Name, Contact.Email, Contact.Message);

            MessageSent = true;
            
            // Clear the form
            ModelState.Clear();
            Contact = new ContactForm();

            return Page();
        }
    }

    public class ContactForm
    {
        [Required]
        [StringLength(100)]
        public string Name { get; set; } = string.Empty;

        [Required]
        [EmailAddress]
        [StringLength(100)]
        public string Email { get; set; } = string.Empty;

        [Required]
        [StringLength(1000)]
        public string Message { get; set; } = string.Empty;
    }
}
