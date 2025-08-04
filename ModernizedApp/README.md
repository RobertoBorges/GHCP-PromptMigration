# ASP.NET Core Modernized Store

This project is a modernized version of a legacy ASP Classic web application migrated to ASP.NET Core 8.0.

## Project Overview

The application is a simple e-commerce store with product catalog, shopping cart, and contact features. It has been completely rewritten from ASP Classic to ASP.NET Core 8.0 MVC.

## Features

- Product catalog with categories
- Product details
- Shopping cart functionality using session state
- Contact form
- About page
- Responsive design using Bootstrap 5
- Modern UI with Bootstrap Icons

## Technologies Used

- ASP.NET Core 8.0 MVC
- Entity Framework Core 8.0
- C#
- Bootstrap 5
- Bootstrap Icons
- Microsoft SQL Server (LocalDB for development)
- Azure App Service (for production)
- Redis Cache (for production session state)
- Azure Entra ID (for authentication)
- Application Insights (for monitoring)

## Project Structure

```plaintext
ModernizedApp/
├── Controllers/        # MVC Controllers
├── Data/               # Database context and initialization
├── Models/             # Data models
├── Services/           # Business logic and services
├── ViewComponents/     # Reusable UI components
├── Views/              # Razor views
│   ├── Cart/           # Cart-related views
│   ├── Home/           # Home, About, Contact views
│   ├── Products/       # Product catalog views
│   └── Shared/         # Layout and shared views
├── wwwroot/            # Static content
│   ├── css/            # CSS stylesheets
│   ├── images/         # Images and product photos
│   ├── js/             # JavaScript files
│   └── lib/            # Client-side libraries
└── Program.cs          # Application startup configuration
```

## Configuration

The application uses appsettings.json for configuration:

- Database connection string (SQL Server)
- Redis Cache connection string (for distributed session)
- Application Insights integration
- Azure Entra ID authentication settings

## Getting Started

### Prerequisites

- .NET 8.0 SDK
- Visual Studio 2022 or Visual Studio Code
- SQL Server LocalDB (for development)

### Running Locally

1. Clone this repository
2. Restore NuGet packages
3. Update the database connection string in appsettings.json if needed
4. Run the application

### Development Commands

```powershell
# Restore dependencies
dotnet restore

# Build the project
dotnet build

# Run the application
dotnet run

# Watch for file changes during development
dotnet watch run
```

## Deployment

The application is configured for deployment to Azure App Service. Infrastructure as Code (Bicep) templates will be provided in the next phase of the project.

## Next Steps

1. Generate infrastructure templates (Bicep) for Azure deployment
2. Deploy to Azure App Service
3. Configure Redis Cache for distributed session state
4. Set up Azure Entra ID for authentication
5. Configure Application Insights for monitoring

## Migration Status

See [MigrationStatus.md](MigrationStatus.md) for detailed progress tracking of the migration project.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
