<%@ Page Title="Home Page" Language="C#" MasterPageFile="~/Site.master" AutoEventWireup="true"
    CodeFile="Default.aspx.cs" Inherits="_Default" %>

<asp:Content ID="HeaderContent" runat="server" ContentPlaceHolderID="HeadContent">
</asp:Content>
<asp:Content ID="BodyContent" runat="server" ContentPlaceHolderID="MainContent">
    <h2>
        Welcome to BookShop Online Store
    </h2>
    <p>
        Welcome to our online bookstore! We offer a wide selection of books from various genres and authors.
        Browse our collection and find your next great read.
    </p>
    
    <h3>Featured Books</h3>
    <div class="book-list">
        <asp:Repeater ID="FeaturedBooksRepeater" runat="server">
            <ItemTemplate>
                <div class="book-item">
                    <img src='<%# ResolveUrl(Eval("ImageUrl").ToString()) %>' alt='<%# Eval("Title") %>' onerror="this.src='images/books/no-image.jpg';" />
                    <h3><%# Eval("Title") %></h3>
                    <div class="author">by <%# Eval("Author.FullName") %></div>
                    <div class="category"><%# Eval("Category.Name") %></div>
                    <div class="price">$<%# String.Format("{0:F2}", Eval("Price")) %></div>
                    <asp:Button ID="ViewDetailsButton" runat="server" Text="View Details" CssClass="btn" 
                        PostBackUrl='<%# "~/BookDetails.aspx?id=" + Eval("BookId") %>' />
                </div>
            </ItemTemplate>
        </asp:Repeater>
    </div>
    
    <div style="clear: both; margin-top: 20px;">
        <p>
            <asp:HyperLink ID="ViewAllBooksLink" runat="server" NavigateUrl="~/Books.aspx" Text="View All Books" />
        </p>
    </div>
    
    <h3>About Our Store</h3>
    <p>
        BookShop Library has been serving book lovers since 2008. We specialize in both classic and contemporary 
        literature, offering books across all genres. Our knowledgeable staff is always ready to help you find 
        exactly what you're looking for.
    </p>
    
    <p>
        <strong>Store Hours:</strong><br />
        Monday - Friday: 9:00 AM - 8:00 PM<br />
        Saturday: 9:00 AM - 6:00 PM<br />
        Sunday: 12:00 PM - 5:00 PM
    </p>
    
    <p>
        <strong>Contact Information:</strong><br />
        Phone: (555) 123-BOOK<br />
        Email: info@bookshop.com<br />
        Address: 123 Library Lane, Springfield, IL 62701
    </p>
</asp:Content>