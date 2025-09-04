<%@ Page Title="Administration Dashboard" Language="C#" MasterPageFile="~/AdminMaster.master" AutoEventWireup="true"
    CodeFile="Default.aspx.cs" Inherits="AdminDefault" %>

<asp:Content ID="HeaderContent" runat="server" ContentPlaceHolderID="HeadContent">
</asp:Content>
<asp:Content ID="BodyContent" runat="server" ContentPlaceHolderID="MainContent">
    <h2>BookShop Administration Dashboard</h2>
    
    <div class="quick-actions">
        <h3>Quick Actions</h3>
        <asp:Button ID="AddBookButton" runat="server" Text="Add New Book" CssClass="btn btn-success" 
            PostBackUrl="~/Admin/ManageBooks.aspx" />
        <asp:Button ID="ViewOrdersButton" runat="server" Text="View Recent Orders" CssClass="btn btn-warning" 
            PostBackUrl="~/Admin/ViewOrders.aspx" />
        <asp:Button ID="ManageUsersButton" runat="server" Text="Manage Employees" CssClass="btn" 
            PostBackUrl="~/Admin/ManageEmployees.aspx" />
    </div>
    
    <div class="dashboard-cards">
        <div class="dashboard-card">
            <h3>Books in Inventory</h3>
            <span class="stat-number">
                <asp:Label ID="TotalBooksLabel" runat="server" Text="--" />
            </span>
            <div class="stat-label">Total Books</div>
        </div>
        
        <div class="dashboard-card">
            <h3>Orders Today</h3>
            <span class="stat-number">
                <asp:Label ID="TodayOrdersLabel" runat="server" Text="--" />
            </span>
            <div class="stat-label">New Orders</div>
        </div>
        
        <div class="dashboard-card">
            <h3>Low Stock Items</h3>
            <span class="stat-number">
                <asp:Label ID="LowStockLabel" runat="server" Text="--" />
            </span>
            <div class="stat-label">Need Restocking</div>
        </div>
        
        <div class="dashboard-card">
            <h3>Active Employees</h3>
            <span class="stat-number">
                <asp:Label ID="EmployeeCountLabel" runat="server" Text="--" />
            </span>
            <div class="stat-label">Staff Members</div>
        </div>
    </div>
    
    <h3>Recent Activity</h3>
    <div class="message">
        <asp:Label ID="ActivityLabel" runat="server" Text="Loading recent activity..." />
    </div>
    
    <h3>System Information</h3>
    <table class="form-table">
        <tr>
            <td class="label">Server Time:</td>
            <td><asp:Label ID="ServerTimeLabel" runat="server" /></td>
        </tr>
        <tr>
            <td class="label">Current User:</td>
            <td><asp:Label ID="CurrentUserInfoLabel" runat="server" /></td>
        </tr>
        <tr>
            <td class="label">Database Status:</td>
            <td><asp:Label ID="DatabaseStatusLabel" runat="server" /></td>
        </tr>
        <tr>
            <td class="label">Application Version:</td>
            <td>BookShop v1.0 (.NET Framework 3.5)</td>
        </tr>
    </table>
    
    <div style="margin-top: 30px;">
        <h3>Administration Guidelines</h3>
        <ul>
            <li>All book inventory changes require manager approval</li>
            <li>Employee information must be updated within 24 hours of changes</li>
            <li>Daily reports should be generated before 6 PM</li>
            <li>System backup is performed automatically at midnight</li>
            <li>For technical support, contact IT at ext. 1234</li>
        </ul>
    </div>
</asp:Content>