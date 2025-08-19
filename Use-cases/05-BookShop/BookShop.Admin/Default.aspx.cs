using System;
using System.Collections.Generic;
using System.Web;
using System.Web.UI;
using System.Web.UI.WebControls;

public partial class AdminDefault : System.Web.UI.Page
{
    protected void Page_Load(object sender, EventArgs e)
    {
        if (!IsPostBack)
        {
            LoadDashboardData();
            LoadSystemInfo();
        }
    }

    private void LoadDashboardData()
    {
        try
        {
            // In a real application, these would come from the business services
            // For demonstration, we'll use sample data
            
            TotalBooksLabel.Text = "127";
            TodayOrdersLabel.Text = "8";
            LowStockLabel.Text = "3";
            EmployeeCountLabel.Text = "6";
            
            ActivityLabel.Text = "Recent activity: 3 new orders processed, 1 book added to inventory, 2 customer inquiries handled.";
        }
        catch (Exception ex)
        {
            ActivityLabel.Text = "Error loading dashboard data: " + ex.Message;
            ActivityLabel.CssClass = "message error";
        }
    }

    private void LoadSystemInfo()
    {
        try
        {
            ServerTimeLabel.Text = DateTime.Now.ToString("yyyy-MM-dd HH:mm:ss");
            
            if (HttpContext.Current.User.Identity.IsAuthenticated)
            {
                CurrentUserInfoLabel.Text = HttpContext.Current.User.Identity.Name + " (Windows Authentication)";
            }
            else
            {
                CurrentUserInfoLabel.Text = "Not authenticated";
            }
            
            // Test database connection
            try
            {
                // In a real application, you would test the actual database connection here
                DatabaseStatusLabel.Text = "Connected (SQL Server 2008)";
                DatabaseStatusLabel.CssClass = "success";
            }
            catch
            {
                DatabaseStatusLabel.Text = "Connection Error";
                DatabaseStatusLabel.CssClass = "error";
            }
        }
        catch (Exception ex)
        {
            DatabaseStatusLabel.Text = "Error: " + ex.Message;
            DatabaseStatusLabel.CssClass = "error";
        }
    }
}