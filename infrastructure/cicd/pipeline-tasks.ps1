# Helper script for common CI/CD pipeline tasks

param (
    [Parameter(Mandatory=$true)]
    [ValidateSet("init-db", "run-tests", "version-update", "start-warmup")]
    [string]$Action,
    
    [Parameter(Mandatory=$false)]
    [string]$Environment = "dev",
    
    [Parameter(Mandatory=$false)]
    [string]$Version
)

$ErrorActionPreference = "Stop"

function Initialize-Database {
    param (
        [string]$Environment
    )
    
    Write-Host "Preparing database for $Environment environment..." -ForegroundColor Yellow
    
    # For SQLite, we may need to create initial schema or seed data
    $projectPath = "..\src\StoreApp"
    
    # Check if the database folder exists
    $dbFolder = Join-Path $projectPath "App_Data"
    if (-not (Test-Path $dbFolder)) {
        Write-Host "Creating App_Data folder..." -ForegroundColor Cyan
        New-Item -ItemType Directory -Path $dbFolder | Out-Null
    }
    
    # Check if the initial migration has been applied
    # This is a simplified approach - in a real scenario, you'd use EF Core commands
    Write-Host "Database preparation completed successfully!" -ForegroundColor Green
}

function Start-Tests {
    Write-Host "Running tests..." -ForegroundColor Yellow
    
    # Look for test projects
    $testProjects = Get-ChildItem -Path "..\src" -Filter "*.Tests.csproj" -Recurse
    
    if ($testProjects.Count -eq 0) {
        Write-Host "No test projects found. Skipping tests." -ForegroundColor Cyan
        return
    }
    
    $allTestsPassed = $true
    
    foreach ($testProject in $testProjects) {
        Write-Host "Running tests for: $($testProject.FullName)" -ForegroundColor Cyan
        dotnet test $testProject.FullName --no-restore --verbosity normal
        
        if ($LASTEXITCODE -ne 0) {
            $allTestsPassed = $false
            Write-Host "Tests failed for: $($testProject.FullName)" -ForegroundColor Red
        }
    }
    
    if ($allTestsPassed) {
        Write-Host "All tests passed successfully!" -ForegroundColor Green
    } else {
        Write-Host "Some tests failed. Please check the output above." -ForegroundColor Red
        exit 1
    }
}

function Update-Version {
    param (
        [string]$Version
    )
    
    if (-not $Version) {
        Write-Host "No version specified. Skipping version update." -ForegroundColor Yellow
        return
    }
    
    Write-Host "Updating version to $Version..." -ForegroundColor Yellow
    
    # Update version in project file
    $projectFile = "..\src\StoreApp\StoreApp.csproj"
    $xml = [xml](Get-Content $projectFile)
    $versionNode = $xml.SelectSingleNode("//Version")
    
    if ($versionNode) {
        $versionNode.InnerText = $Version
    } else {
        $propertyGroup = $xml.SelectSingleNode("//PropertyGroup")
        $versionElement = $xml.CreateElement("Version")
        $versionElement.InnerText = $Version
        $propertyGroup.AppendChild($versionElement) | Out-Null
    }
    
    $xml.Save($projectFile)
    
    Write-Host "Version updated successfully!" -ForegroundColor Green
}

function Start-AppWarmup {
    param (
        [string]$Environment
    )
    
    Write-Host "Performing application warmup for $Environment environment..." -ForegroundColor Yellow
    
    # Get the app service URL - this would come from Terraform outputs in a real scenario
    $appUrl = "https://storeapp-app-$Environment.azurewebsites.net"
    
    try {
        # Send requests to key pages to warm up the application
        $pages = @("/", "/products", "/about", "/contact")
        
        foreach ($page in $pages) {
            $url = "$appUrl$page"
            Write-Host "Warming up: $url" -ForegroundColor Cyan
            $response = Invoke-WebRequest -Uri $url -UseBasicParsing
            Write-Host "Status: $($response.StatusCode)" -ForegroundColor Cyan
        }
        
        Write-Host "Warmup completed successfully!" -ForegroundColor Green
    }
    catch {
        Write-Host "Error during warmup: $_" -ForegroundColor Red
        # Don't fail the pipeline on warmup issues
    }
}

# Main script execution
switch ($Action) {
    "init-db" {
        Initialize-Database -Environment $Environment
    }
    "run-tests" {
        Start-Tests
    }
    "version-update" {
        Update-Version -Version $Version
    }
    "start-warmup" {
        Start-AppWarmup -Environment $Environment
    }
    default {
        Write-Host "Unknown action: $Action" -ForegroundColor Red
        exit 1
    }
}
