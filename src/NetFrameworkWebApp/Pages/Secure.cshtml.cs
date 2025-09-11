using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using System.Security.Claims;

namespace NetFrameworkWebApp.Pages
{
    // No [AllowAnonymous] means this page requires authentication
    public class SecureModel : PageModel
    {
        public string UserName { get; private set; } = string.Empty;
        public string AuthType { get; private set; } = string.Empty;
        public string IsAuthenticated { get; private set; } = string.Empty;
        public string AuthTime { get; private set; } = string.Empty;
        
        // Simulated secure data
        public string AccountId { get; private set; } = "ACC-12345";
        public string LastLogin { get; private set; } = DateTime.Now.AddDays(-1).ToString("g");
        public string SecurityLevel { get; private set; } = "Standard";

        public void OnGet()
        {
            if (User.Identity != null)
            {
                UserName = User.Identity.Name ?? "Unknown";
                AuthType = User.Identity.AuthenticationType ?? "Unknown";
                IsAuthenticated = User.Identity.IsAuthenticated.ToString();
                
                // Try to get auth time from claims
                var authTimeClaim = User.Claims.FirstOrDefault(c => c.Type == "auth_time");
                
                if (authTimeClaim != null && long.TryParse(authTimeClaim.Value, out long authTimeStamp))
                {
                    // Convert Unix timestamp to DateTime
                    var dateTime = DateTimeOffset.FromUnixTimeSeconds(authTimeStamp).DateTime;
                    AuthTime = dateTime.ToString("g");
                }
                else
                {
                    AuthTime = "Not available";
                }
            }
        }
    }
}
