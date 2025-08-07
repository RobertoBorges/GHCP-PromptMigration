using Microsoft.AspNetCore.Mvc.Rendering;
using System.Collections.Generic;

namespace ContosoUniversity.Web.ViewModels
{
    public class SendCodeViewModel
    {
        public string SelectedProvider { get; set; } = string.Empty;

        public ICollection<SelectListItem> Providers { get; set; } = new List<SelectListItem>();

        public string ReturnUrl { get; set; } = string.Empty;

        public bool RememberMe { get; set; }
    }
}
