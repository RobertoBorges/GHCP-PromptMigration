using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;

namespace NetFrameworkWebApp.Pages
{
    [AllowAnonymous]
    public class IndexModel : PageModel
    {
        public string DateTimeInfo { get; private set; } = string.Empty;

        public void OnGet()
        {
            string authInfo = "";
            
            // Add authentication details
            if (User != null && User.Identity != null)
            {
                authInfo = $"User: {User.Identity.Name} | Authenticated: {User.Identity.IsAuthenticated} | Auth Type: {User.Identity.AuthenticationType}";
            }
            else
            {
                authInfo = "User identity not available";
            }
            
            DateTimeInfo = $"Current server time: {DateTime.Now.ToString("f")} | {authInfo}";
        }
    }
}
