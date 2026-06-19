<%@ Page Language="C#" AutoEventWireup="true" CodeFile="About.aspx.cs" Inherits="About" MasterPageFile="~/Site.master" %>

<asp:Content ID="Content1" ContentPlaceHolderID="HeadContent" runat="server">
    <title>About BookShop - Your Destination for Books</title>
</asp:Content>

<asp:Content ID="Content2" ContentPlaceHolderID="MainContent" runat="server">
    <div class="container">
        <div class="about-section">
            <h1>About BookShop</h1>
            <div class="about-content">
                <p>Welcome to BookShop, your trusted source for quality books since 1998. We are committed to providing our customers with the best selection of books across various genres.</p>
                
                <h2>Our Mission</h2>
                <p>Our mission is to promote reading and make quality literature accessible to all. We believe that books have the power to educate, inspire, and transform lives.</p>
                
                <h2>Our History</h2>
                <p>Founded in 1998 as a small corner bookstore, BookShop has grown into a comprehensive online and physical retailer of books. What started with a small collection of classics has expanded to include thousands of titles across fiction, non-fiction, academic, and special interest categories.</p>
                
                <h2>Our Team</h2>
                <p>Our team consists of passionate book lovers who are dedicated to helping you find your next great read. From our knowledgeable staff to our efficient delivery team, everyone at BookShop is committed to providing you with an exceptional book buying experience.</p>
                
                <asp:Label ID="VersionLabel" runat="server" CssClass="version-info"></asp:Label>
                
                <div class="contact-info">
                    <h2>Contact Us</h2>
                    <p>Phone: (555) 123-4567</p>
                    <p>Email: info@bookshop.com</p>
                    <p>Address: 123 Book Street, Reading, RG1 2CD</p>
                </div>
            </div>
        </div>
    </div>
</asp:Content>
