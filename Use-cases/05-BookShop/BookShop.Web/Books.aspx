<%@ Page Title="Browse Books" Language="C#" MasterPageFile="~/Site.master" AutoEventWireup="true"
    CodeFile="Books.aspx.cs" Inherits="Books" %>

<asp:Content ID="HeaderContent" runat="server" ContentPlaceHolderID="HeadContent">
</asp:Content>
<asp:Content ID="BodyContent" runat="server" ContentPlaceHolderID="MainContent">
    <h2>Browse Our Book Collection</h2>
    
    <div style="margin-bottom: 20px;">
        <label for="CategoryDropDown"><strong>Filter by Category:</strong></label>
        <asp:DropDownList ID="CategoryDropDown" runat="server" AutoPostBack="true" 
            OnSelectedIndexChanged="CategoryDropDown_SelectedIndexChanged">
            <asp:ListItem Value="0" Text="All Categories" Selected="True" />
        </asp:DropDownList>
    </div>
    
    <asp:Label ID="MessageLabel" runat="server" CssClass="message" Visible="false" />
    
    <div class="book-list">
        <asp:Repeater ID="BooksRepeater" runat="server">
            <ItemTemplate>
                <div class="book-item">
                    <img src='<%# ResolveUrl(Eval("ImageUrl").ToString()) %>' alt='<%# Eval("Title") %>' onerror="this.src='images/books/no-image.jpg';" />
                    <h3><%# Eval("Title") %></h3>
                    <div class="author">by <%# Eval("Author.FullName") %></div>
                    <div class="category"><%# Eval("Category.Name") %></div>
                    <div class="price">$<%# String.Format("{0:F2}", Eval("Price")) %></div>
                    <div style="margin-top: 10px;">
                        Stock: <%# Eval("StockQuantity") %> available
                    </div>
                    <asp:Button ID="ViewDetailsButton" runat="server" Text="View Details" CssClass="btn" 
                        PostBackUrl='<%# "~/BookDetails.aspx?id=" + Eval("BookId") %>' />
                </div>
            </ItemTemplate>
        </asp:Repeater>
    </div>
    
    <div style="clear: both; text-align: center; margin-top: 20px;">
        <asp:Label ID="NoResultsLabel" runat="server" Text="No books found matching your criteria." 
            Visible="false" CssClass="message" />
    </div>
</asp:Content>