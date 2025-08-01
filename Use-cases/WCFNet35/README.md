# WCF Demo for .NET Framework 3.5

This repository contains a comprehensive demonstration of Windows Communication Foundation (WCF) technology using .NET Framework 3.5. The demo includes a complete WCF service implementation with fake customer data, a service host, and a client application.

## Project Structure

```
WCFDemo.sln                 # Visual Studio Solution file
├── WCFDemo.Service/        # WCF Service Library
│   ├── Customer.cs         # Data contract
│   ├── ICustomerService.cs # Service contract interface
│   ├── CustomerService.cs  # Service implementation
│   ├── app.config          # Service configuration
│   └── WCFDemo.Service.csproj
├── WCFDemo.Host/           # Console Host Application
│   ├── Program.cs          # Service hosting logic
│   ├── app.config          # Host configuration
│   └── WCFDemo.Host.csproj
└── WCFDemo.Client/         # Console Client Application
    ├── Program.cs          # Client consumption demo
    ├── app.config          # Client configuration
    └── WCFDemo.Client.csproj
```

## Features Demonstrated

### WCF Core Concepts
- **Service Contracts**: Interface defining service operations
- **Data Contracts**: Serializable data structures
- **Service Implementation**: Business logic implementation
- **Service Hosting**: Self-hosting in console application
- **Client Consumption**: Consuming services via proxy

### Service Operations
- `GetAllCustomers()` - Retrieve all active customers
- `GetCustomerById(int id)` - Get customer by ID
- `GetCustomersByCountry(string country)` - Filter customers by country
- `AddCustomer(Customer customer)` - Add new customer
- `UpdateCustomer(Customer customer)` - Update existing customer
- `DeleteCustomer(int id)` - Soft delete customer
- `GetCustomerCount()` - Get total customer count

### Sample Data
The service includes 10 fake customers from different countries:
- John Doe (USA), Jane Smith (UK), Carlos Rodriguez (Spain)
- Marie Dubois (France), Hans Mueller (Germany), Anna Kowalski (Poland)
- Luigi Rossi (Italy), Sarah Johnson (Canada), Yuki Tanaka (Japan)
- Pedro Silva (Brazil)

## How to Run the Demo

### Prerequisites
- Windows OS with .NET Framework 3.5 installed
- Visual Studio 2008 or later (or MSBuild tools)

### Step 1: Build the Solution
```bash
# Open Visual Studio and build the solution, or use MSBuild:
msbuild WCFDemo.sln /p:Configuration=Debug
```

### Step 2: Start the Service Host
```bash
# Run the host application (keeps the service running)
cd WCFDemo.Host\bin\Debug
WCFDemo.Host.exe
```
The service will start on `http://localhost:8080/CustomerService`

### Step 3: Run the Client Demo
```bash
# In a new terminal, run the client application
cd WCFDemo.Client\bin\Debug
WCFDemo.Client.exe
```

## WCF Configuration

### Service Configuration (Host)
- **Base Address**: `http://localhost:8080/CustomerService`
- **Binding**: BasicHttpBinding (SOAP over HTTP)
- **Metadata Exchange**: Enabled for service discovery
- **Debug Mode**: Exception details included in faults

### Client Configuration
- **Endpoint**: Connects to the service via BasicHttpBinding
- **Proxy**: Created using ChannelFactory pattern

## Learning Objectives

This demo helps understand:

1. **Service Contract Design**: How to define WCF service interfaces
2. **Data Contract Usage**: Serializing complex objects over WCF
3. **Service Implementation**: Business logic in WCF services
4. **Configuration Management**: XML-based WCF configuration
5. **Service Hosting**: Self-hosting services in applications
6. **Client Development**: Consuming WCF services programmatically
7. **Error Handling**: Proper cleanup and exception management
8. **CRUD Operations**: Complete Create, Read, Update, Delete functionality

## Technology Stack

- **.NET Framework 3.5**: Target framework version
- **WCF (Windows Communication Foundation)**: Service framework
- **BasicHttpBinding**: SOAP over HTTP communication
- **Console Applications**: Simple hosting and client demos

## Notes

- This demo uses in-memory data storage (fake data)
- Service supports soft deletion (marks records as inactive)
- All customer operations are demonstrated in the client
- Proper WCF proxy lifecycle management is implemented
- Service metadata is enabled for development/testing

The demo provides a solid foundation for understanding WCF architecture and can be extended with additional features like security, transactions, or different bindings.
