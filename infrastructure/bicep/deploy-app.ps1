# Deploy the ASP.NET Core application to Azure App Service
param(
    [string]$resourceGroupName = "rg-netframeworkwebapp-dev",
    [string]$webAppName = "",
    [string]$projectPath = "./src/NetFrameworkWebApp"
)

# If web app name is not specified, try to get it from the resource group
if ([string]::IsNullOrEmpty($webAppName)) {
    Write-Host "Web app name not specified, retrieving from resource group..."
    $webApps = az webapp list --resource-group $resourceGroupName --query "[].name" -o json | ConvertFrom-Json
    
    if ($webApps.Count -eq 0) {
        Write-Error "No web apps found in resource group $resourceGroupName"
        exit 1
    } elseif ($webApps.Count -eq 1) {
        $webAppName = $webApps[0]
        Write-Host "Found web app: $webAppName"
    } else {
        Write-Host "Multiple web apps found in resource group ${resourceGroupName}:"
        for ($i = 0; $i -lt $webApps.Count; $i++) {
            Write-Host "[$i] $($webApps[$i])"
        }
        
        $selection = Read-Host "Enter the number of the web app to deploy to"
        $webAppName = $webApps[$selection]
        Write-Host "Selected web app: $webAppName"
    }
}

# Build and publish the application
Write-Host "Building and publishing the application..."
dotnet publish $projectPath -c Release -o ./publish

# Zip the published output
Write-Host "Creating deployment package..."
$publishFolder = "./publish"
$deployPackage = "./deploy.zip"

# Remove existing zip file if it exists
if (Test-Path $deployPackage) {
    Remove-Item $deployPackage -Force
}

# Create the zip file
Add-Type -AssemblyName System.IO.Compression.FileSystem
[System.IO.Compression.ZipFile]::CreateFromDirectory($publishFolder, $deployPackage)

# Deploy to Azure App Service
Write-Host "Deploying to Azure App Service: $webAppName"
az webapp deployment source config-zip --resource-group $resourceGroupName --name $webAppName --src $deployPackage

# Clean up
Write-Host "Cleaning up..."
Remove-Item $deployPackage -Force
Remove-Item -Recurse -Force $publishFolder

Write-Host "Deployment completed successfully!"
Write-Host "Your application is now running at: https://$webAppName.azurewebsites.net"
