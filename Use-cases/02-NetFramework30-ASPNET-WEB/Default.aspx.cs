using System;
using System.Collections.Generic;
using System.Web;
using System.Web.UI;
using System.Web.UI.WebControls;

namespace NetFramework30ASPNETWEB
{
    public partial class Default : System.Web.UI.Page
    {
        protected void Page_Load(object sender, EventArgs e)
        {
            // Set the current date and time on each page load
            string authInfo = "";
            
            // Add authentication details
            if (User != null && User.Identity != null)
            {
                authInfo = String.Format("User: {0} | Authenticated: {1} | Auth Type: {2}", 
                    User.Identity.Name, 
                    User.Identity.IsAuthenticated, 
                    User.Identity.AuthenticationType);
            }
            else
            {
                authInfo = "User identity not available";
            }
            
            DateTimeLabel.Text = "Current server time: " + DateTime.Now.ToString("f") + " | " + authInfo;
        }
    }
}
