using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.UI;
using System.Web.UI.WebControls;

public partial class AdminMaster : System.Web.UI.MasterPage
{
    protected void Page_Load(object sender, EventArgs e)
    {
        if (!IsPostBack)
        {
            LoadUserInfo();
        }
    }

    private void LoadUserInfo()
    {
        try
        {
            if (HttpContext.Current.User.Identity.IsAuthenticated)
            {
                // Get Windows username
                string username = HttpContext.Current.User.Identity.Name;
                CurrentUserLabel.Text = username;

                // In a real application, you would use EmployeeService to check admin status
                // For demonstration, we'll simulate this
                bool isAdmin = IsCurrentUserAdmin(username);
                
                if (isAdmin)
                {
                    UserRoleLabel.Text = "(Administrator)";
                    UserRoleLabel.CssClass = "user-role admin";
                }
                else
                {
                    UserRoleLabel.Text = "(Employee)";
                    UserRoleLabel.CssClass = "user-role employee";
                    
                    // Hide admin-only menu items for non-admin users
                    HideAdminMenuItems();
                }
            }
            else
            {
                CurrentUserLabel.Text = "Not Authenticated";
                UserRoleLabel.Text = "";
                // Redirect to login or show error
                Response.Redirect("~/Login.aspx");
            }
        }
        catch (Exception ex)
        {
            CurrentUserLabel.Text = "Error loading user info";
            UserRoleLabel.Text = "";
            // Log the error
        }
    }

    private bool IsCurrentUserAdmin(string username)
    {
        // In a real application, this would use EmployeeService.IsEmployeeAdmin(username)
        // For demonstration, we'll check against some sample admin usernames
        string[] adminUsers = { 
            "BOOKSHOP\\jsmith", 
            "BOOKSHOP\\mjohnson",
            @"DOMAIN\Administrator",
            @"DOMAIN\BookShopAdmin"
        };
        
        return adminUsers.Contains(username, StringComparer.OrdinalIgnoreCase);
    }

    private void HideAdminMenuItems()
    {
        // Hide admin-only menu items for regular employees
        foreach (MenuItem item in NavigationMenu.Items)
        {
            if (item.Text == "Manage Employees" || item.Text == "Reports")
            {
                item.Enabled = false;
                item.Selectable = false;
            }
        }
    }
}