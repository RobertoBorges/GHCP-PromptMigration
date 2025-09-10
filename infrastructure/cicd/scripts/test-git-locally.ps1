# Local Git Repository Test Script
# Run this script to test Git connectivity from your local machine to diagnose Git fetch issues

param(
    [string]$RepoUrl = "https://dev.azure.com/learnadoz/ghcpnew/_git/ghcpnew",
    [string]$TestDir = "$env:TEMP\git-test-$(Get-Random)"
)

Write-Host "Testing Git repository access..."
Write-Host "Repository URL: $RepoUrl"
Write-Host "Test directory: $TestDir"
Write-Host "Git version: $(git --version)"

# Create test directory
Write-Host "Creating test directory..."
if (Test-Path $TestDir) {
    Remove-Item -Path $TestDir -Recurse -Force
}
New-Item -ItemType Directory -Path $TestDir -Force | Out-Null

# Try to clone the repository
Set-Location $TestDir
Write-Host "Attempting to clone repository..."
$output = git clone $RepoUrl . 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "Success! Git clone was successful."
    Write-Host "Repository contents:"
    Get-ChildItem -Force | Select-Object Name, Length, LastWriteTime
} else {
    Write-Host "Error: Git clone failed with exit code $LASTEXITCODE"
    Write-Host "Error output: $output"
    
    # Check network connectivity
    $uri = [System.Uri]$RepoUrl
    $hostname = $uri.Host
    Write-Host "Testing network connectivity to $hostname..."
    Test-NetConnection -ComputerName $hostname -Port 443
    
    # Try with SSL verification disabled
    Write-Host "Trying with SSL verification disabled..."
    git config --global http.sslVerify false
    $output = git clone $RepoUrl . 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Success with SSL verification disabled!"
    } else {
        Write-Host "Still failed with SSL verification disabled. Error: $output"
    }
}

Write-Host "Test complete. Cleaning up test directory..."
Set-Location $env:USERPROFILE
Remove-Item -Path $TestDir -Recurse -Force -ErrorAction SilentlyContinue
