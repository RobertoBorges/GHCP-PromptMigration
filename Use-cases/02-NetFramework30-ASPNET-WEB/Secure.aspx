<%@ Page Language="C#" AutoEventWireup="true" CodeBehind="Secure.aspx.cs" Inherits="NetFramework30ASPNETWEB.Secure" %>

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">

<html xmlns="http://www.w3.org/1999/xhtml">
<head runat="server">
    <title>Secure Page - My ASP.NET Application</title>
    <link href="Styles/Site.css" rel="stylesheet" type="text/css" />
</head>
<body>
    <form id="form1" runat="server">
        <div class="header">
            <div class="title">
                <h1>Welcome to My ASP.NET Application</h1>
            </div>
            <div class="loginDisplay">
                <asp:LoginView ID="HeadLoginView" runat="server" EnableViewState="false">
                    <LoggedInTemplate>
                        Welcome <span class="bold"><asp:LoginName ID="HeadLoginName" runat="server" /></span>!
                        [ <asp:LoginStatus ID="HeadLoginStatus" runat="server" LogoutAction="Redirect" LogoutText="Log Out" LogoutPageUrl="~/"/> ]
                    </LoggedInTemplate>
                </asp:LoginView>
            </div>
            <div class="clear"></div>
            <div class="navigationMenu">
                <asp:Menu ID="NavigationMenu" runat="server" CssClass="menu" EnableViewState="false" IncludeStyleBlock="false" Orientation="Horizontal">
                    <Items>
                        <asp:MenuItem NavigateUrl="~/Default.aspx" Text="Home"/>
                        <asp:MenuItem NavigateUrl="~/About.aspx" Text="About"/>
                        <asp:MenuItem NavigateUrl="~/Secure.aspx" Text="Secure Page" Selected="True"/>
                    </Items>
                </asp:Menu>
            </div>
        </div>
        <div class="main">
            <div class="content">
                <h2>Secure Page</h2>
                <p>
                    This is a secure page that can only be accessed by authenticated users who are members of specific Windows groups.
                </p>
                <h3>Your Authentication Information</h3>
                <div class="userInfo">
                    <p>
                        <strong>User Name:</strong> <asp:Label ID="UserNameLabel" runat="server"></asp:Label>
                    </p>
                    <p>
                        <strong>Authentication Type:</strong> <asp:Label ID="AuthTypeLabel" runat="server"></asp:Label>
                    </p>
                    <p>
                        <strong>Is Authenticated:</strong> <asp:Label ID="IsAuthenticatedLabel" runat="server"></asp:Label>
                    </p>
                    <p>
                        <strong>Groups:</strong> <asp:BulletedList ID="GroupsList" runat="server"></asp:BulletedList>
                    </p>
                    <p>
                        <strong>Authorization Status:</strong> <asp:Label ID="AuthorizationStatusLabel" runat="server" Font-Bold="true"></asp:Label>
                    </p>
                </div>
                <h3>Secret Content</h3>
                <asp:Panel ID="SecretPanel" runat="server" Visible="false">
                    <p>
                        This is confidential information that only authorized users can see.
                    </p>
                    <p>
                        You are seeing this because you are a member of an authorized Windows group.
                    </p>
                </asp:Panel>
                <asp:Panel ID="UnauthorizedPanel" runat="server" Visible="false">
                    <p class="error">
                        You are authenticated but not authorized to view the secret content.
                    </p>
                    <p>
                        You must be a member of one of the authorized Windows groups to see the secret content.
                    </p>
                </asp:Panel>
            </div>
        </div>
        <div class="footer">
            <p>&copy; <%= DateTime.Now.Year %> - My ASP.NET Application</p>
        </div>
    </form>
</body>
</html>
