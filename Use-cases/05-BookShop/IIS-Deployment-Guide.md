# IIS Deployment Scripts for BookShop Application

## Customer Website Deployment (BookShop.Web)

### PowerShell Script to Create Customer Site
```powershell
# Run as Administrator
Import-Module WebAdministration

# Create Application Pool
New-WebAppPool -Name "BookShopWebPool" -Force
Set-ItemProperty -Path "IIS:\AppPools\BookShopWebPool" -Name "managedRuntimeVersion" -Value "v2.0"
Set-ItemProperty -Path "IIS:\AppPools\BookShopWebPool" -Name "managedPipelineMode" -Value "Integrated"

# Create Website
$sitePath = "C:\inetpub\wwwroot\BookShop.Web"
New-Website -Name "BookShop Customer Portal" -Port 80 -PhysicalPath $sitePath -ApplicationPool "BookShopWebPool"

Write-Host "Customer website created successfully at http://localhost"
```

## Admin Website Deployment (BookShop.Admin)

### PowerShell Script to Create Admin Site
```powershell
# Run as Administrator
Import-Module WebAdministration

# Create Application Pool
New-WebAppPool -Name "BookShopAdminPool" -Force
Set-ItemProperty -Path "IIS:\AppPools\BookShopAdminPool" -Name "managedRuntimeVersion" -Value "v2.0"
Set-ItemProperty -Path "IIS:\AppPools\BookShopAdminPool" -Name "managedPipelineMode" -Value "Integrated"

# Create Website
$adminSitePath = "C:\inetpub\wwwroot\BookShop.Admin"
New-Website -Name "BookShop Administration" -Port 8080 -PhysicalPath $adminSitePath -ApplicationPool "BookShopAdminPool"

# Configure Windows Authentication
Set-WebConfiguration -Filter "system.webServer/security/authentication/windowsAuthentication" -Value @{enabled="true"} -PSPath "IIS:" -Location "BookShop Administration"
Set-WebConfiguration -Filter "system.webServer/security/authentication/anonymousAuthentication" -Value @{enabled="false"} -PSPath "IIS:" -Location "BookShop Administration"

Write-Host "Admin website created successfully at http://localhost:8080"
```

## Manual IIS Configuration Steps

### For Customer Site (BookShop.Web):
1. Open IIS Manager
2. Right-click "Sites" → "Add Website"
3. Site name: "BookShop Customer Portal"
4. Physical path: [Path to BookShop.Web folder]
5. Port: 80
6. Application pool: Create new "BookShopWebPool" with .NET Framework v2.0

### For Admin Site (BookShop.Admin):
1. Open IIS Manager
2. Right-click "Sites" → "Add Website"
3. Site name: "BookShop Administration"
4. Physical path: [Path to BookShop.Admin folder]
5. Port: 8080
6. Application pool: Create new "BookShopAdminPool" with .NET Framework v2.0
7. Select the site → Authentication → Enable Windows Authentication, Disable Anonymous Authentication

## File Permissions

### Customer Site:
- IIS_IUSRS: Read & Execute
- Application Pool Identity: Read & Execute

### Admin Site:
- IIS_IUSRS: Read & Execute
- Application Pool Identity: Read & Execute
- Domain Users (who need access): Read & Execute
- BookShop Admins group: Full Control

## Troubleshooting

### Common Issues:
1. **"Handler not found" error**: Ensure .NET Framework 3.5 is installed and registered with IIS
2. **Database connection issues**: Check connection strings and SQL Server permissions
3. **Windows Authentication not working**: Verify IIS Authentication settings and domain configuration
4. **Access denied**: Check file permissions and application pool identity

### Required Windows Features:
- IIS with ASP.NET support
- Windows Authentication
- .NET Framework 3.5 SP1

### Verification Steps:
1. Browse to http://localhost (Customer site)
2. Browse to http://localhost:8080 (Admin site - should prompt for Windows credentials)
3. Check Event Viewer for any errors
4. Test database connectivity from both sites