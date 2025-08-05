# WCF Demo Troubleshooting Guide

## Common Issues and Solutions

### Build Issues

#### 1. "MSBuild not found" or "Build tools not available"
**Problem**: MSBuild is not installed or not in PATH
**Solution**: 
- Install .NET Framework 3.5 SDK
- Install Visual Studio 2008 or later
- Add MSBuild to your system PATH

#### 2. "Target framework not found"
**Problem**: .NET Framework 3.5 is not installed
**Solution**:
- Install .NET Framework 3.5 from Microsoft website
- On Windows 10/11: Enable via Windows Features

#### 3. "System.ServiceModel reference not found"
**Problem**: WCF components not available
**Solution**:
- Ensure .NET Framework 3.5 is fully installed
- WCF is included with .NET Framework 3.0+

### Runtime Issues

#### 1. "Service failed to start" or "Address already in use"
**Problem**: Port 8080 is already in use
**Solution**:
- Close other applications using port 8080
- Or modify the port in both app.config files:
  ```xml
  <add baseAddress="http://localhost:8081/CustomerService" />
  ```

#### 2. "HTTP could not register URL" or "Access denied"
**Problem**: Insufficient permissions to bind to HTTP address
**Solution**:
- Run command prompt as Administrator
- Or use a different port (above 1024)
- Or use netsh to reserve the URL:
  ```cmd
  netsh http add urlacl url=http://+:8080/CustomerService user=Everyone
  ```

#### 3. "Could not connect to service" from client
**Problem**: Service is not running or wrong address
**Solution**:
- Ensure WCFDemo.Host.exe is running first
- Check the service shows "Service started successfully"
- Verify the address matches in both configurations
- Check Windows Firewall isn't blocking port 8080

#### 4. "Proxy communication exception"
**Problem**: Communication failure between client and service
**Solution**:
- Restart the service host
- Check network connectivity
- Ensure both apps use same binding configuration

### Configuration Issues

#### 1. "Endpoint not found" 
**Problem**: Endpoint configuration mismatch
**Solution**:
- Verify address, binding, and contract match in:
  - WCFDemo.Host/app.config (service endpoint)
  - WCFDemo.Client/app.config (client endpoint)

#### 2. "Contract mismatch"
**Problem**: Service contract doesn't match client expectations
**Solution**:
- Ensure both projects reference the same service library
- Rebuild the entire solution
- Verify ICustomerService interface is properly referenced

#### 3. "Metadata not available"
**Problem**: Cannot browse service metadata
**Solution**:
- Ensure serviceMetadata httpGetEnabled="true"
- Verify MEX endpoint is configured
- Check service is running and accessible

### Development Issues

#### 1. Visual Studio can't open project files
**Problem**: Project format not supported
**Solution**:
- These are Visual Studio 2008 format projects
- Use Visual Studio 2008 or later
- Or manually edit .csproj files for newer versions

#### 2. IntelliSense not working for WCF types
**Problem**: References not properly loaded
**Solution**:
- Clean and rebuild solution
- Ensure System.ServiceModel reference is present
- Restart Visual Studio

## Testing the Service

### 1. Verify Service is Running
Open browser and navigate to: `http://localhost:8080/CustomerService`
You should see the service description page.

### 2. Check Metadata Endpoint
Navigate to: `http://localhost:8080/CustomerService/mex`
This should return service metadata.

### 3. Manual Testing with WCF Test Client
If you have WCF Test Client installed:
```cmd
wcftestclient http://localhost:8080/CustomerService
```

### 4. Test with SOAP UI or Postman
You can test the service with any SOAP client using the WSDL:
`http://localhost:8080/CustomerService?wsdl`

## Performance Tips

1. **Service Hosting**: For production, use IIS hosting instead of self-hosting
2. **Data Storage**: Replace in-memory storage with database
3. **Security**: Add authentication and authorization
4. **Bindings**: Consider wsHttpBinding for more features
5. **Throttling**: Configure service throttling for high load

## Getting Help

If you continue to have issues:
1. Check the console output for detailed error messages
2. Enable WCF tracing for detailed diagnostics
3. Verify all prerequisites are installed
4. Ensure Windows Firewall allows the application
5. Try running both applications as Administrator

## Useful Commands

```cmd
# Check if port is in use
netstat -an | findstr :8080

# List all HTTP URL reservations
netsh http show urlacl

# Add URL reservation (run as admin)
netsh http add urlacl url=http://+:8080/ user=Everyone

# Delete URL reservation (run as admin)  
netsh http delete urlacl url=http://+:8080/
```