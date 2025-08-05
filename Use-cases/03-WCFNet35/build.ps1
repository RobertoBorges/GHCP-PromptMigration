# WCF Demo Build Script - .NET Framework 3.5
Write-Host "===============================================" -ForegroundColor Yellow
Write-Host "WCF Demo Build Script - .NET Framework 3.5" -ForegroundColor Yellow
Write-Host "===============================================" -ForegroundColor Yellow
Write-Host

# Check for MSBuild
Write-Host "Checking for MSBuild..." -ForegroundColor Cyan
try {
    $msbuildVersion = & msbuild /version 2>$null
    Write-Host "MSBuild found." -ForegroundColor Green
} catch {
    Write-Host "ERROR: MSBuild not found. Please install .NET Framework 3.5 SDK or Visual Studio." -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "Building solution..." -ForegroundColor Cyan
Write-Host

# Build the solution
$buildResult = & msbuild WCFDemo.sln /p:Configuration=Debug /p:Platform="Any CPU" /verbosity:minimal
if ($LASTEXITCODE -ne 0) {
    Write-Host
    Write-Host "ERROR: Build failed. Please check the output above for errors." -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host
Write-Host "Build completed successfully!" -ForegroundColor Green
Write-Host

Write-Host "To run the demo:" -ForegroundColor Yellow
Write-Host "1. Start the service host: " -NoNewline -ForegroundColor White
Write-Host "WCFDemo.Host\bin\Debug\WCFDemo.Host.exe" -ForegroundColor Cyan
Write-Host "2. In another terminal, run the client: " -NoNewline -ForegroundColor White
Write-Host "WCFDemo.Client\bin\Debug\WCFDemo.Client.exe" -ForegroundColor Cyan
Write-Host

Write-Host "Service endpoints:" -ForegroundColor Yellow
Write-Host "- Service: " -NoNewline -ForegroundColor White
Write-Host "http://localhost:8080/CustomerService" -ForegroundColor Cyan
Write-Host "- Metadata: " -NoNewline -ForegroundColor White
Write-Host "http://localhost:8080/CustomerService/mex" -ForegroundColor Cyan
Write-Host

Read-Host "Press Enter to exit"