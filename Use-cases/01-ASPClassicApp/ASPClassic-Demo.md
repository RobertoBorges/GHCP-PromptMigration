# ASP Classic Application Instructions

## Introduction to ASP Classic

ASP (Active Server Pages) Classic is a server-side scripting environment that can be used to create dynamic and interactive web applications. Developed by Microsoft, ASP Classic pages have a `.asp` extension and can contain a mixture of HTML, scripts, and ASP commands.

## How ASP Classic Works

1. **Server-Side Processing**:
   - When a browser requests an ASP file, the web server (typically IIS - Internet Information Services) processes the ASP file.
   - The server executes any script code contained within the file (usually VBScript or JScript).
   - The server then sends the resulting HTML to the client browser.

2. **ASP Tags**:
   - ASP code is enclosed within `<%` and `%>` tags.
   - For output expressions, you can use `<%= expression %>` as a shorthand for `<% Response.Write(expression) %>`.

3. **Session Management**:
   - ASP Classic maintains session state for each user.
   - Sessions are used to store user-specific data between page requests.

4. **Built-in Objects**:
   - Request: Access form data, query strings, cookies, etc.
   - Response: Send content to the client browser.
   - Session: Store session-specific variables.
   - Application: Store application-wide variables.
   - Server: Create server components and perform URL encoding/decoding.

## Project Structure

For a basic ASP Classic application, create the following files:

1. **global.asa**: Application and session-level events.
2. **default.asp**: The main landing page.
3. **database.asp**: Database connection and functions.
4. **products.asp**: Product listing page with fake data.
5. **product-detail.asp**: Individual product details.
6. **includes/header.asp**: Common header include file.
7. **includes/footer.asp**: Common footer include file.
8. **css/styles.css**: Stylesheet.

## Sample Code Examples

### Database Connection (database.asp)

```vbscript
<%
' Database connection function
Function GetConnection()
    Dim conn
    Set conn = Server.CreateObject("ADODB.Connection")
    conn.Open "Provider=Microsoft.Jet.OLEDB.4.0;Data Source=" & Server.MapPath("/db/fakestore.mdb")
    Set GetConnection = conn
End Function
%>
```

### Displaying Fake Products (products.asp)

```vbscript
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
```

### Product Detail Page (product-detail.asp)

```vbscript
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
```

### Header Include (includes/header.asp)

```vbscript
<!DOCTYPE html>
<html>
<head>
    <title>Classic ASP Store</title>
    <link rel="stylesheet" href="/css/styles.css">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body>
    <header>
        <div class="container">
            <h1 class="logo">Classic ASP Store</h1>
            <nav>
                <ul>
                    <li><a href="default.asp">Home</a></li>
                    <li><a href="products.asp">Products</a></li>
                    <li><a href="about.asp">About</a></li>
                    <li><a href="contact.asp">Contact</a></li>
                </ul>
            </nav>
        </div>
    </header>
    
    <div class="container content">
```

### Footer Include (includes/footer.asp)

```vbscript
    </div><!-- end .content -->
    
    <footer>
        <div class="container">
            <p>&copy; <%= Year(Date) %> Classic ASP Store. All rights reserved.</p>
        </div>
    </footer>
    
    <script>
        // Optional JavaScript can go here
    </script>
</body>
</html>
```

## Setting Up Your Environment

1. **Install IIS**:
   - Windows: Control Panel > Programs > Turn Windows Features on or off > Internet Information Services

2. **Enable ASP**:
   - In Windows Features, ensure ASP is checked under: Internet Information Services > World Wide Web Services > Application Development Features > ASP

3. **Create a Website**:
   - Open IIS Manager
   - Right-click "Sites" > Add Website
   - Enter a site name, physical path, and port

4. **Set Permissions**:
   - Ensure the IIS user has read/execute permissions on your website folder

## Testing Your ASP Classic Application

1. Start IIS if it's not already running.
2. Navigate to `http://localhost:[your-port]/default.asp` in a browser.
3. You should see your homepage and be able to navigate to the products listing.

## Debugging Tips

1. Enable detailed error messages in IIS.
2. Use `Response.Write` statements to output variable values.
3. Check the IIS logs for server-side errors.

## Common ASP Classic Functions

```vbscript
' String manipulation
strValue = "Hello World"
Response.Write(UCase(strValue)) ' Outputs: HELLO WORLD
Response.Write(LCase(strValue)) ' Outputs: hello world
Response.Write(Len(strValue)) ' Outputs: 11

' Date functions
Response.Write(Date()) ' Current date
Response.Write(Now()) ' Current date and time
Response.Write(Year(Date())) ' Current year

' Type conversion
intValue = CInt("123") ' Convert to integer
dblValue = CDbl("123.45") ' Convert to double

' Conditional logic
If condition Then
    ' Do something
ElseIf anotherCondition Then
    ' Do something else
Else
    ' Default action
End If

' Looping
For i = 1 To 10
    ' Do something 10 times
Next

Do While condition
    ' Do something while condition is true
Loop
```

Happy coding with ASP Classic!
