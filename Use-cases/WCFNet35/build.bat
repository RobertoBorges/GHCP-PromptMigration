@echo off
echo ===============================================
echo WCF Demo Setup Script - .NET Framework 3.5
echo ===============================================
echo.

echo Checking for MSBuild...
msbuild /version >nul 2>&1
if errorlevel 1 (
    echo ERROR: MSBuild not found. Please install .NET Framework 3.5 SDK or Visual Studio.
    pause
    exit /b 1
)

echo MSBuild found. Building solution...
echo.

msbuild WCFDemo.sln /p:Configuration=Debug /p:Platform="Any CPU" /verbosity:minimal
if errorlevel 1 (
    echo.
    echo ERROR: Build failed. Please check the output above for errors.
    pause
    exit /b 1
)

echo.
echo Build completed successfully!
echo.
echo To run the demo:
echo 1. Start the service host: WCFDemo.Host\bin\Debug\WCFDemo.Host.exe
echo 2. In another terminal, run the client: WCFDemo.Client\bin\Debug\WCFDemo.Client.exe
echo.
echo The service will be available at: http://localhost:8080/CustomerService
echo Metadata endpoint: http://localhost:8080/CustomerService/mex
echo.
pause