# Azure Infrastructure Diagram for Store App

```mermaid
graph TD
    subgraph "Azure Resource Group"
        ASP[App Service Plan] --> WA[Windows Web App]
        SA[Storage Account] --> FS[File Share]
        FS --> WA
        AI[Application Insights] --> WA
        
        subgraph "Optional VNet Integration"
            VNET[Virtual Network]
            SUBNET[App Service Subnet]
            NSG[Network Security Group]
            
            VNET --> SUBNET
            NSG --> SUBNET
            SUBNET --> WA
        end
    end
    
    CLIENT[Client Browser] --> WA
    
    subgraph "App Components"
        WA --> RAZOR[Razor Pages]
        WA --> EF[Entity Framework Core]
        EF --> SQLITE[SQLite Database]
        SQLITE --> FS
    end
    
    style WA fill:#4da6ff,stroke:#333,stroke-width:2px
    style SQLITE fill:#f9f,stroke:#333,stroke-width:2px
    style CLIENT fill:#bbf,stroke:#333,stroke-width:2px
```

## Architecture Overview

The diagram above illustrates the Azure infrastructure for hosting the Store App:

1. **Core Azure Resources**:
   - **Resource Group**: Contains all resources
   - **App Service Plan**: Provides the compute resources
   - **Windows Web App**: Hosts the ASP.NET Core application
   - **Storage Account**: Contains File Share for SQLite persistence
   - **Application Insights**: Provides monitoring and logging

2. **Optional VNet Integration**:
   - **Virtual Network**: Isolated network for the application
   - **App Service Subnet**: Dedicated subnet with delegation for App Service
   - **Network Security Group**: Controls traffic flow

3. **Application Components**:
   - **Razor Pages**: The web interface
   - **Entity Framework Core**: Data access layer
   - **SQLite Database**: Stored in Azure File Share for persistence

This architecture ensures:
- Reliable hosting on Azure App Service
- Data persistence through Azure Storage
- Application monitoring and diagnostics
- Optional network isolation for enhanced security
