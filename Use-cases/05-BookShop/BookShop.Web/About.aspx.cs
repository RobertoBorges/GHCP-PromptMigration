using System;
using System.Collections.Generic;
using System.Web;
using System.Web.UI;
using System.Web.UI.WebControls;
using System.Reflection;

public partial class About : System.Web.UI.Page
{
    protected void Page_Load(object sender, EventArgs e)
    {
        if (!IsPostBack)
        {
            SetVersionInfo();
        }
    }

    private void SetVersionInfo()
    {
        try
        {
            // Get the current application version
            string version = Assembly.GetExecutingAssembly().GetName().Version.ToString();
            
            // Get .NET Framework version
            string frameworkVersion = Environment.Version.ToString();
            
            // Display version information
            VersionLabel.Text = string.Format("Application Version: {0}<br/>Running on .NET Framework: {1}", version, frameworkVersion);
        }
        catch (Exception ex)
        {
            // Log error but don't display to user
            System.Diagnostics.Trace.WriteLine("Error getting version info: " + ex.Message);
            VersionLabel.Text = "Application Version: 1.0"; // Fallback version
        }
    }
}
