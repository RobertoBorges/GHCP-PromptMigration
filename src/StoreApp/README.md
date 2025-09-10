# Store Application

## Overview
This is a modernized ASP.NET Core application migrated from an ASP Classic codebase. The application provides a simple e-commerce storefront with product listings, details, and shopping cart functionality.

## Technology Stack
- ASP.NET Core 8.0
- Razor Pages
- Entity Framework Core
- SQLite Database
- Bootstrap 5

## Features
- Product catalog browsing
- Product details view
- Shopping cart functionality
- Contact form with validation
- Responsive design

## Getting Started

### Prerequisites
- .NET 8.0 SDK or later
- Visual Studio 2022 or Visual Studio Code

### Local Development
1. Clone the repository
2. Navigate to the StoreApp directory
3. Run `dotnet restore` to restore dependencies
4. Run `dotnet run` to start the application
5. Open a web browser and navigate to `https://localhost:5001`

### Database
The application uses SQLite for data storage. The database is automatically created and seeded with sample data on first run.

## Deployment
The application can be deployed to Azure App Service using the provided deployment scripts:

1. Use the Terraform configuration in the `infrastructure/terraform` folder to provision Azure resources
2. Run the deployment script: `.\infrastructure\terraform\deploy.ps1`

Alternatively, use the Azure DevOps pipeline configured in `infrastructure/cicd/deployment-pipeline.yml`.

## Project Structure
- `Data/` - Database context and migrations
- `Models/` - Entity models
- `Pages/` - Razor Pages
- `Services/` - Business logic
- `ViewComponents/` - Reusable UI components
- `wwwroot/` - Static files (CSS, JS, images)

## CI/CD Pipeline
A complete CI/CD pipeline is configured in Azure DevOps, with the following stages:
- Build and test
- Infrastructure validation
- Deployment to development environment
- Deployment to production environment (with approval)
