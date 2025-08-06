#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Build script for ContosoUniversity.Modern solution
.DESCRIPTION
    This script builds all projects in the ContosoUniversity.Modern solution,
    runs tests, and can optionally publish the application
.PARAMETER Configuration
    The build configuration (Debug or Release)
.PARAMETER NoBuild
    Skip the build step
.PARAMETER NoTest
    Skip the test step
.PARAMETER Publish
    Publish the application after building
.PARAMETER PublishFolder
    The folder to publish to (default: ./publish)
.PARAMETER Verbosity
    The verbosity level for the build (q[uiet], m[inimal], n[ormal], d[etailed], diag[nostic])
#>

param (
    [string]$Configuration = "Release",
    [switch]$NoBuild,
    [switch]$NoTest,
    [switch]$Publish,
    [string]$PublishFolder = "./publish",
    [string]$Verbosity = "minimal"
)

$ErrorActionPreference = "Stop"
$SolutionPath = Join-Path $PSScriptRoot "ContosoUniversity.sln"

Write-Host "===== ContosoUniversity.Modern Build Script =====" -ForegroundColor Cyan
Write-Host "Solution: $SolutionPath" -ForegroundColor Cyan
Write-Host "Configuration: $Configuration" -ForegroundColor Cyan
Write-Host "=================================================" -ForegroundColor Cyan

# Restore NuGet packages
Write-Host "`n> Restoring NuGet packages..." -ForegroundColor Yellow
dotnet restore $SolutionPath
if ($LASTEXITCODE -ne 0) {
    Write-Host "Package restore failed with exit code $LASTEXITCODE" -ForegroundColor Red
    exit $LASTEXITCODE
}
Write-Host "Package restore completed successfully" -ForegroundColor Green

# Build solution
if (-not $NoBuild) {
    Write-Host "`n> Building solution..." -ForegroundColor Yellow
    dotnet build $SolutionPath --configuration $Configuration --verbosity $Verbosity --no-restore
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Build failed with exit code $LASTEXITCODE" -ForegroundColor Red
        exit $LASTEXITCODE
    }
    Write-Host "Build completed successfully" -ForegroundColor Green
}

# Run tests
if (-not $NoTest) {
    Write-Host "`n> Running tests..." -ForegroundColor Yellow
    dotnet test $SolutionPath --configuration $Configuration --verbosity $Verbosity --no-build
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Tests failed with exit code $LASTEXITCODE" -ForegroundColor Red
        exit $LASTEXITCODE
    }
    Write-Host "Tests completed successfully" -ForegroundColor Green
}

# Publish application
if ($Publish) {
    $WebProjectPath = Join-Path $PSScriptRoot "ContosoUniversity.Web/ContosoUniversity.Web.csproj"
    $PublishPath = Join-Path $PSScriptRoot $PublishFolder
    
    Write-Host "`n> Publishing application to $PublishPath..." -ForegroundColor Yellow
    dotnet publish $WebProjectPath --configuration $Configuration --output $PublishPath --verbosity $Verbosity --no-build
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Publishing failed with exit code $LASTEXITCODE" -ForegroundColor Red
        exit $LASTEXITCODE
    }
    Write-Host "Publishing completed successfully" -ForegroundColor Green
}

Write-Host "`n===== Build Process Completed Successfully =====" -ForegroundColor Cyan
