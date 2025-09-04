<%@ Page Title="Manage Books" Language="C#" MasterPageFile="~/AdminMaster.master" AutoEventWireup="true"
    CodeFile="ManageBooks.aspx.cs" Inherits="Admin_ManageBooks" %>

<asp:Content ID="HeaderContent" runat="server" ContentPlaceHolderID="HeadContent">
</asp:Content>
<asp:Content ID="BodyContent" runat="server" ContentPlaceHolderID="MainContent">
    <h2>Manage Books</h2>
    
    <div class="quick-actions">
        <h3>Book Management</h3>
        <asp:Button ID="AddNewBookButton" runat="server" Text="Add New Book" CssClass="btn btn-success" 
            OnClick="AddNewBookButton_Click" />
        <asp:Button ID="RefreshButton" runat="server" Text="Refresh List" CssClass="btn" 
            OnClick="RefreshButton_Click" />
    </div>
    
    <asp:Label ID="MessageLabel" runat="server" CssClass="message" Visible="false" />
    
    <h3>Book Inventory</h3>
    <asp:GridView ID="BooksGridView" runat="server" CssClass="grid" AutoGenerateColumns="false"
        OnRowCommand="BooksGridView_RowCommand" OnRowDataBound="BooksGridView_RowDataBound">
        <Columns>
            <asp:BoundField DataField="BookId" HeaderText="ID" />
            <asp:BoundField DataField="Title" HeaderText="Title" />
            <asp:BoundField DataField="Author.FullName" HeaderText="Author" />
            <asp:BoundField DataField="Category.Name" HeaderText="Category" />
            <asp:BoundField DataField="ISBN" HeaderText="ISBN" />
            <asp:BoundField DataField="Price" HeaderText="Price" DataFormatString="${0:F2}" />
            <asp:BoundField DataField="StockQuantity" HeaderText="Stock" />
            <asp:TemplateField HeaderText="Status">
                <ItemTemplate>
                    <asp:Label ID="StatusLabel" runat="server" Text='<%# (bool)Eval("IsActive") ? "Active" : "Inactive" %>' />
                </ItemTemplate>
            </asp:TemplateField>
            <asp:TemplateField HeaderText="Actions">
                <ItemTemplate>
                    <asp:Button ID="EditButton" runat="server" Text="Edit" CssClass="btn btn-warning" 
                        CommandName="EditBook" CommandArgument='<%# Eval("BookId") %>' />
                    <asp:Button ID="DeleteButton" runat="server" Text="Delete" CssClass="btn btn-danger" 
                        CommandName="DeleteBook" CommandArgument='<%# Eval("BookId") %>' 
                        OnClientClick="return confirm('Are you sure you want to delete this book?');" />
                </ItemTemplate>
            </asp:TemplateField>
        </Columns>
        <EmptyDataTemplate>
            <div class="message">No books found in the inventory.</div>
        </EmptyDataTemplate>
    </asp:GridView>
    
    <div style="margin-top: 20px;">
        <h3>Quick Statistics</h3>
        <ul>
            <li>Total Books: <asp:Label ID="TotalBooksLabel" runat="server" /></li>
            <li>Active Books: <asp:Label ID="ActiveBooksLabel" runat="server" /></li>
            <li>Low Stock (< 10): <asp:Label ID="LowStockBooksLabel" runat="server" /></li>
            <li>Out of Stock: <asp:Label ID="OutOfStockBooksLabel" runat="server" /></li>
        </ul>
    </div>
</asp:Content>