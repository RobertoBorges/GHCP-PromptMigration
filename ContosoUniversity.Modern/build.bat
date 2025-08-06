@echo off
setlocal enabledelayedexpansion

echo ===== ContosoUniversity.Modern Build Script =====
echo.

set CONFIGURATION=Release
set VERBOSITY=minimal
set NOBUILD=0
set NOTEST=0
set PUBLISH=0
set PUBLISHFOLDER=publish

REM Parse command line arguments
:parse_args
if "%~1"=="" goto :done_parsing
if /i "%~1"=="--configuration" (
    set CONFIGURATION=%~2
    shift
    shift
    goto :parse_args
)
if /i "%~1"=="-c" (
    set CONFIGURATION=%~2
    shift
    shift
    goto :parse_args
)
if /i "%~1"=="--verbosity" (
    set VERBOSITY=%~2
    shift
    shift
    goto :parse_args
)
if /i "%~1"=="-v" (
    set VERBOSITY=%~2
    shift
    shift
    goto :parse_args
)
if /i "%~1"=="--no-build" (
    set NOBUILD=1
    shift
    goto :parse_args
)
if /i "%~1"=="--no-test" (
    set NOTEST=1
    shift
    goto :parse_args
)
if /i "%~1"=="--publish" (
    set PUBLISH=1
    shift
    goto :parse_args
)
if /i "%~1"=="--publish-folder" (
    set PUBLISHFOLDER=%~2
    shift
    shift
    goto :parse_args
)
shift
goto :parse_args
:done_parsing

echo Configuration: %CONFIGURATION%
echo.

REM Restore NuGet packages
echo ^> Restoring NuGet packages...
dotnet restore
if %ERRORLEVEL% neq 0 (
    echo Package restore failed with exit code %ERRORLEVEL%
    exit /b %ERRORLEVEL%
)
echo Package restore completed successfully.
echo.

REM Build solution
if %NOBUILD% equ 0 (
    echo ^> Building solution...
    dotnet build --configuration %CONFIGURATION% --verbosity %VERBOSITY% --no-restore
    if %ERRORLEVEL% neq 0 (
        echo Build failed with exit code %ERRORLEVEL%
        exit /b %ERRORLEVEL%
    )
    echo Build completed successfully.
    echo.
)

REM Run tests
if %NOTEST% equ 0 (
    echo ^> Running tests...
    dotnet test --configuration %CONFIGURATION% --verbosity %VERBOSITY% --no-build
    if %ERRORLEVEL% neq 0 (
        echo Tests failed with exit code %ERRORLEVEL%
        exit /b %ERRORLEVEL%
    )
    echo Tests completed successfully.
    echo.
)

REM Publish application
if %PUBLISH% equ 1 (
    echo ^> Publishing application to .\%PUBLISHFOLDER%...
    dotnet publish ContosoUniversity.Web\ContosoUniversity.Web.csproj --configuration %CONFIGURATION% --output .\%PUBLISHFOLDER% --verbosity %VERBOSITY% --no-build
    if %ERRORLEVEL% neq 0 (
        echo Publishing failed with exit code %ERRORLEVEL%
        exit /b %ERRORLEVEL%
    )
    echo Publishing completed successfully.
    echo.
)

echo ===== Build Process Completed Successfully =====
exit /b 0
