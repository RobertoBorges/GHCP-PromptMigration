# ASP Classic Store Demo Application

This is a simple ASP Classic e-commerce store demo application. It demonstrates how to create a dynamic web application using ASP Classic technology.

## Features

- Product catalog with sample products
- Product detail pages
- Basic shopping cart functionality
- Contact form with validation
- Responsive design

## Setup Instructions

### Prerequisites

- Windows with IIS (Internet Information Services) installed
- ASP Classic enabled in IIS

### Installation Steps

1. **Install IIS** (if not already installed):
   - Go to Control Panel > Programs > Turn Windows Features on or off
   - Check "Internet Information Services" and expand it
   - Make sure "World Wide Web Services" > "Application Development Features" > "ASP" is checked
   - Click OK and wait for installation to complete

2. **Enable ASP Classic in IIS**:
   - Open IIS Manager (type "IIS" in the Windows search bar)
   - Select your server in the left panel
   - Double-click on "ISAPI and CGI Restrictions"
   - Ensure that "Active Server Pages" is set to "Allowed"

3. **Create a Website in IIS**:
   - Open IIS Manager
   - Right-click on "Sites" in the left panel and select "Add Website"
   - Enter a site name (e.g., "ASPClassicStore")
   - Set the physical path to the root folder of this application (e.g., `C:\git\ASPClassicApp`)
   - Set a port number (e.g., 8080)
   - Click OK

4. **Set Permissions**:
   - Right-click on your application folder (e.g., `C:\git\ASPClassicApp`)
   - Select Properties > Security tab
   - Ensure that IUSR and IIS_IUSRS have Read & Execute permissions

5. **Test the Application**:
   - Open a web browser and navigate to `http://localhost:[port]/default.asp`
   - You should see the home page of the ASP Classic Store

## File Structure

- `default.asp`: Homepage
- `products.asp`: Product listing page
- `product-detail.asp`: Individual product details
- `about.asp`: About page
- `contact.asp`: Contact form
- `cart.asp`: Shopping cart functionality
- `database.asp`: Database connection functions (simulated)
- `global.asa`: Application and session settings
- `includes/`: Folder containing reusable page elements
  - `header.asp`: Common header
  - `footer.asp`: Common footer
- `css/`: Folder containing stylesheets
  - `styles.css`: Main stylesheet
- `db/`: Folder for database files (simulated in this demo)

## Notes on Database

This demo uses a simulated database with hardcoded product information. In a real application, you would:

1. Create an Access database (.mdb file) in the `db` folder
2. Implement proper database queries in `database.asp`
3. Replace the hardcoded arrays with actual database queries

## Troubleshooting

- **500 - Internal Server Error**: Check that ASP is enabled in IIS and that the application has proper permissions.
- **404 - File Not Found**: Ensure the file path is correct and the file exists.
- **Error in Include File**: Make sure all include paths are correct relative to the page they're included in.

## Additional Resources

- [Microsoft ASP Documentation](https://docs.microsoft.com/en-us/previous-versions/iis/6.0-sdk/ms524984(v=vs.90))
- [Classic ASP Debugging Guide](https://docs.microsoft.com/en-us/previous-versions/troubleshoot/iis/asp-troubleshooting-guide)
