<!--#include file="includes/header.asp"-->
<!--#include file="database.asp"-->

<%
' Get the product ID from the URL
productId = Request.QueryString("id")
If productId = "" Then
    Response.Redirect "products.asp"
End If

' In a real app, you would fetch product data from a database
' For this example, we'll use fake data again
Dim productName, productPrice, productDesc

Select Case CInt(productId)
    Case 1
        productName = "Classic Desk Lamp"
        productPrice = 49.99
        productDesc = "A stylish desk lamp for your home office. Features adjustable brightness and color temperature settings. The lamp includes a USB charging port and touch controls."
    Case 2
        productName = "Ergonomic Office Chair"
        productPrice = 199.99
        productDesc = "Comfortable chair with lumbar support. Fully adjustable height, armrests, and recline settings. Breathable mesh back keeps you cool during long work sessions."
    Case 3
        productName = "Wireless Keyboard"
        productPrice = 79.99
        productDesc = "Compact keyboard with quiet keys. Connects via Bluetooth to up to 3 devices simultaneously. Includes backlit keys and a rechargeable battery that lasts up to 2 weeks."
    Case 4
        productName = "LED Monitor"
        productPrice = 249.99
        productDesc = "24-inch full HD display. Features ultra-thin bezels, 144Hz refresh rate, and AMD FreeSync technology. Includes HDMI, DisplayPort, and USB-C connections."
    Case 5
        productName = "Bluetooth Speaker"
        productPrice = 89.99
        productDesc = "Portable speaker with rich bass. Waterproof design makes it perfect for outdoor use. Provides up to 12 hours of playback on a single charge and includes a built-in microphone for calls."
    Case Else
        Response.Redirect "products.asp"
End Select
%>

<div class="product-detail">
    <h1><%= productName %></h1>
    <div class="product-meta">
        <span class="price">$<%= FormatNumber(productPrice, 2) %></span>
        <span class="product-id">Product ID: <%= productId %></span>
    </div>
    
    <div class="product-description">
        <h2>Description</h2>
        <p><%= productDesc %></p>
    </div>
    
    <form method="post" action="cart.asp">
        <input type="hidden" name="productId" value="<%= productId %>">
        <label for="quantity">Quantity:</label>
        <input type="number" name="quantity" id="quantity" value="1" min="1" max="10">
        <button type="submit" class="button">Add to Cart</button>
    </form>
    
    <a href="products.asp" class="back-link"><- Back to Products</a>
</div>

<!--#include file="includes/footer.asp"-->
