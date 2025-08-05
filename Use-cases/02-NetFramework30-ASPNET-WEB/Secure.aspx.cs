using System;
using System.Collections.Generic;
using System.Security.Principal;
using System.Web;
using System.Web.UI;
using System.Web.UI.WebControls;
using System.Configuration;

namespace NetFramework30ASPNETWEB
{
    public partial class Secure : System.Web.UI.Page
    {
        // Define the authorized groups here
        // You can move these to web.config for easier management
        private static readonly string[] AuthorizedGroups = new string[] {
            @"BUILTIN\Administrators",
            @"DOMAIN\SecureAppUsers",
            @"NT AUTHORITY\Authenticated Users"  // Just to sample some access, in a real scenario we have a defined group
        };

        protected void Page_Load(object sender, EventArgs e)
        {
            // Check if the user is authenticated
            if (!User.Identity.IsAuthenticated)
            {
                // This shouldn't happen if web.config is configured correctly,
                // but just in case redirect to the home page
                Response.Redirect("~/Default.aspx");
                return;
            }

            // Display user information
            UserNameLabel.Text = User.Identity.Name;
            AuthTypeLabel.Text = User.Identity.AuthenticationType;
            IsAuthenticatedLabel.Text = User.Identity.IsAuthenticated.ToString();

            // Get the Windows identity
            WindowsIdentity windowsIdentity = User.Identity as WindowsIdentity;
            
            if (windowsIdentity != null)
            {
                // Get the Windows principal
                WindowsPrincipal windowsPrincipal = new WindowsPrincipal(windowsIdentity);
                
                // Display group memberships
                PopulateGroupsList(windowsIdentity);
                
                // Check if user is in any of the authorized groups
                bool isAuthorized = CheckAuthorization(windowsPrincipal);
                
                // Show appropriate content based on authorization
                SecretPanel.Visible = isAuthorized;
                UnauthorizedPanel.Visible = !isAuthorized;
                
                // Display authorization status
                AuthorizationStatusLabel.Text = isAuthorized ? "Authorized" : "Not Authorized";
                AuthorizationStatusLabel.ForeColor = isAuthorized ? System.Drawing.Color.Green : System.Drawing.Color.Red;
            }
            else
            {
                // This shouldn't happen with Windows authentication, but just in case
                AuthorizationStatusLabel.Text = "Not a Windows Identity";
                AuthorizationStatusLabel.ForeColor = System.Drawing.Color.Red;
                UnauthorizedPanel.Visible = true;
            }
        }

        private void PopulateGroupsList(WindowsIdentity windowsIdentity)
        {
            GroupsList.Items.Clear();

            try
            {
                IdentityReferenceCollection groups = windowsIdentity.Groups;
                if (groups != null)
                {
                    foreach (IdentityReference group in groups)
                    {
                        try
                        {
                            // Translate the SID to account name
                            NTAccount ntAccount = group.Translate(typeof(NTAccount)) as NTAccount;
                            if (ntAccount != null)
                            {
                                GroupsList.Items.Add(ntAccount.Value);
                            }
                        }
                        catch
                        {
                            // If we can't translate a SID, just show the SID
                            GroupsList.Items.Add(group.Value);
                        }
                    }
                }
            }
            catch (Exception ex)
            {
                GroupsList.Items.Add("Error retrieving groups: " + ex.Message);
            }
        }

        private bool CheckAuthorization(WindowsPrincipal windowsPrincipal)
        {
            // Check if the user is in any of the authorized groups
            foreach (string group in AuthorizedGroups)
            {
                if (windowsPrincipal.IsInRole(group))
                {
                    return true;
                }
            }

            // Not in any authorized group
            return false;
        }
    }
}
