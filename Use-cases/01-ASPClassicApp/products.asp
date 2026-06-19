<!--#include file="includes/header.asp"-->
<!--#include file="database.asp"-->

<h1>Product Catalog</h1>

<div class="product-grid">
<%
' Since we're using fake data, we'll create it directly in the page
' In a real app, you'd query this from a database
Dim products(4, 3) ' 5 products with 4 attributes each (ID, Name, Price, Description)

' Initialize with fake data
products(0, 0) = 1
products(0, 1) = "Classic Desk Lamp"
products(0, 2) = 49.99
products(0, 3) = "A stylish desk lamp for your home office."

products(1, 0) = 2
products(1, 1) = "Ergonomic Office Chair"
products(1, 2) = 199.99
products(1, 3) = "Comfortable chair with lumbar support."

products(2, 0) = 3
products(2, 1) = "Wireless Keyboard"
products(2, 2) = 79.99
products(2, 3) = "Compact keyboard with quiet keys."

products(3, 0) = 4
products(3, 1) = "LED Monitor"
products(3, 2) = 249.99
products(3, 3) = "24-inch full HD display."

products(4, 0) = 5
products(4, 1) = "Bluetooth Speaker"
products(4, 2) = 89.99
products(4, 3) = "Portable speaker with rich bass."

' Display each product
For i = 0 To 4
%>
    <div class="product-item">
        <h3><%= products(i, 1) %></h3>
        <p class="price">$<%= FormatNumber(products(i, 2), 2) %></p>
        <p><%= products(i, 3) %></p>
        <a href="product-detail.asp?id=<%= products(i, 0) %>" class="button">View Details</a>
    </div>
<%
Next
%>
</div>

<!--#include file="includes/footer.asp"-->
