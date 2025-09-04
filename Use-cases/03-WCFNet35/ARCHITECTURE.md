# WCF Demo Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    WCF Demo Application                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────┐    ┌──────────────────┐    ┌──────────────┐│
│  │  WCFDemo.Client │    │   WCFDemo.Host   │    │WCFDemo.Service││
│  │  (Console App)  │    │  (Console App)   │    │   (Library)   ││
│  │                 │    │                  │    │               ││
│  │ ┌─────────────┐ │    │ ┌──────────────┐ │    │ ┌─────────────┐││
│  │ │ Program.cs  │ │    │ │ Program.cs   │ │    │ │ICustomer-   │││
│  │ │   - Demo    │ │    │ │  - Service   │ │    │ │Service.cs   │││
│  │ │   - Proxy   │ │    │ │    Host      │ │    │ │(Contract)   │││
│  │ │   - CRUD    │ │    │ │  - Error     │ │    │ │             │││
│  │ │    Ops      │ │    │ │    Handling  │ │    │ │Customer-    │││
│  │ └─────────────┘ │    │ └──────────────┘ │    │ │Service.cs   │││
│  │                 │    │                  │    │ │(Implement.) │││
│  │ ┌─────────────┐ │    │ ┌──────────────┐ │    │ │             │││
│  │ │ app.config  │ │    │ │ app.config   │ │    │ │Customer.cs  │││
│  │ │ - Endpoint  │ │    │ │ - Service    │ │    │ │(Data        │││
│  │ │   Config    │ │    │ │   Config     │ │    │ │ Contract)   │││
│  │ └─────────────┘ │    │ │ - Bindings   │ │    │ └─────────────┘││
│  └─────────────────┘    │ │ - Behaviors  │ │    └──────────────┘│
│                         │ └──────────────┘ │                    │
│                         └──────────────────┘                    │
└─────────────────────────────────────────────────────────────────┘

                     Communication Flow:
                            
    Client                    Network                   Host/Service
      │                         │                          │
      │ 1. Create Proxy         │                          │
      │──────────────────────── │ ──────────────────────── │
      │                         │                          │ 2. ServiceHost.Open()
      │ 3. Call Service Method  │                          │
      │──────────────────────── │ ──── HTTP/SOAP ────────▶ │ 4. Process Request
      │                         │                          │
      │ 6. Receive Response     │                          │ 5. Return Data
      │◀─────────────────────── │ ──── HTTP/SOAP ◀──────── │
      │                         │                          │
      │ 7. Close Proxy         │                          │
      │──────────────────────── │ ──────────────────────── │

Configuration Details:

┌─────────────────────────────────────────────────────────────────┐
│ Service Configuration (Host & Service)                         │
├─────────────────────────────────────────────────────────────────┤
│ • Base Address: http://localhost:8080/CustomerService          │
│ • Binding: BasicHttpBinding (SOAP over HTTP)                   │
│ • Contract: WCFDemo.Service.ICustomerService                   │
│ • Metadata: Enabled (MEX endpoint)                             │
│ • Behavior: ServiceMetadata + ServiceDebug                     │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ Service Operations (ICustomerService)                          │
├─────────────────────────────────────────────────────────────────┤
│ • GetAllCustomers() → List<Customer>                           │
│ • GetCustomerById(int) → Customer                              │
│ • GetCustomersByCountry(string) → List<Customer>               │
│ • AddCustomer(Customer) → int                                  │
│ • UpdateCustomer(Customer) → bool                              │
│ • DeleteCustomer(int) → bool                                   │
│ • GetCustomerCount() → int                                     │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ Fake Data (10 International Customers)                         │
├─────────────────────────────────────────────────────────────────┤
│ 1. John Doe (USA)        6. Anna Kowalski (Poland)            │
│ 2. Jane Smith (UK)       7. Luigi Rossi (Italy)               │
│ 3. Carlos Rodriguez (Spain) 8. Sarah Johnson (Canada)          │
│ 4. Marie Dubois (France) 9. Yuki Tanaka (Japan)               │
│ 5. Hans Mueller (Germany) 10. Pedro Silva (Brazil)             │
└─────────────────────────────────────────────────────────────────┘
```

## Key Learning Points:

1. **Service Contract**: `[ServiceContract]` and `[OperationContract]` attributes
2. **Data Contract**: `[DataContract]` and `[DataMember]` attributes  
3. **Service Hosting**: Self-hosting using ServiceHost class
4. **Client Proxy**: ChannelFactory pattern for service consumption
5. **Configuration**: XML-based endpoint and binding configuration
6. **Error Handling**: Proper proxy cleanup and exception management