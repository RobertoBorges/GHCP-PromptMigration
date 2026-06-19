<%@ Page Language="C#" AutoEventWireup="true" CodeBehind="About.aspx.cs" Inherits="NetFramework30ASPNETWEB.About" %>

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">

<html xmlns="http://www.w3.org/1999/xhtml">
<head runat="server">
    <title>About - My ASP.NET Application</title>
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
                    <AnonymousTemplate>
                        [ <a href="Login.aspx" ID="HeadLoginStatus">Log In</a> ]
                    </AnonymousTemplate>
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
                        <asp:MenuItem NavigateUrl="~/About.aspx" Text="About" Selected="True"/>
                        <asp:MenuItem NavigateUrl="~/Secure.aspx" Text="Secure Page"/>
                    </Items>
                </asp:Menu>
            </div>
        </div>
        <div class="main">
            <div class="content">
                <h2>About</h2>
                <p>
                    This is a simple ASP.NET Framework 3.0 application.
                </p>
                <p>
                    This application was created as a demonstration of a basic ASP.NET website structure.
                </p>
                <h3>Technologies Used</h3>
                <ul>
                    <li>ASP.NET Framework 3.0</li>
                    <li>C# programming language</li>
                    <li>HTML and CSS for layout and styling</li>
                </ul>
            </div>
        </div>
        <div class="footer">
            <p>&copy; <%= DateTime.Now.Year %> - My ASP.NET Application</p>
        </div>
    </form>
</body>
</html>
