<!--#include file="includes/header.asp"-->

<%
' Process the add to cart form submission
If Request.ServerVariables("REQUEST_METHOD") = "POST" Then
    Dim productId, quantity
    
    productId = Request.Form("productId")
    quantity = CInt(Request.Form("quantity"))
    
    ' In a real app, you would store the cart in Session or database
    ' For this demo, we'll just show a confirmation message
    
    ' Update cart count in session
    If IsNumeric(Session("CartItems")) Then
        Session("CartItems") = Session("CartItems") + quantity
    Else
        Session("CartItems") = quantity
    End If
End If

' Define product data (just like in product-detail.asp)
Dim products(4, 3)
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

' Find product information
Dim productName, productPrice, productDesc
Dim i

For i = 0 To UBound(products, 1)
    If CStr(products(i, 0)) = productId Then
        productName = products(i, 1)
        productPrice = products(i, 2)
        productDesc = products(i, 3)
        Exit For
    End If
Next
%>

<h1>Shopping Cart</h1>

<% If Request.ServerVariables("REQUEST_METHOD") = "POST" Then %>
    <div class="success-message">
        <p><strong><%= quantity %> x <%= productName %></strong> added to your cart!</p>
    </div>
    
    <div class="cart-summary">
        <h2>Cart Summary</h2>
        <p>Items in cart: <%= Session("CartItems") %></p>
        <p>Last item added: <%= productName %></p>
        <p>Quantity: <%= quantity %></p>
        <p>Price per item: $<%= FormatNumber(productPrice, 2) %></p>
        <p>Subtotal for this item: $<%= FormatNumber(productPrice * quantity, 2) %></p>
    </div>
    
    <div class="cart-actions">
        <a href="products.asp" class="button">Continue Shopping</a>
        <a href="#" class="button checkout-button">Proceed to Checkout</a>
    </div>
<% Else %>
    <p>Your cart is currently empty.</p>
    <a href="products.asp" class="button">Start Shopping</a>
<% End If %>

<style>
    .success-message {
        background-color: #d4edda;
        color: #155724;
        padding: 15px;
        margin-bottom: 20px;
        border-radius: 4px;
    }
    
    .cart-summary {
        background: #f9f9f9;
        padding: 20px;
        margin-bottom: 20px;
        border-radius: 4px;
    }
    
    .cart-summary h2 {
        margin-bottom: 15px;
        border-bottom: 1px solid #eee;
        padding-bottom: 10px;
    }
    
    .cart-summary p {
        margin-bottom: 10px;
    }
    
    .cart-actions {
        display: flex;
        gap: 15px;
        margin-top: 30px;
    }
    
    .checkout-button {
        background: #28a745;
    }
    
    .checkout-button:hover {
        background: #218838;
    }
</style>

<script>
    // Add a click handler for the checkout button
    document.addEventListener('DOMContentLoaded', function() {
        var checkoutBtn = document.querySelector('.checkout-button');
        if (checkoutBtn) {
            checkoutBtn.addEventListener('click', function(e) {
                e.preventDefault();
                alert('This is a demo application. Checkout functionality is not implemented.');
            });
        }
    });
</script>

<!--#include file="includes/footer.asp"-->
