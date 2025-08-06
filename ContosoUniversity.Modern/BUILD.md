# ContosoUniversity.Modern Build Instructions

This folder contains build scripts to compile, test, and publish the ContosoUniversity.Modern application.

## Prerequisites

- [.NET SDK 8.0](https://dotnet.microsoft.com/download/dotnet/8.0) or later
- PowerShell or Command Prompt (Windows)

## Building the Solution

### Using PowerShell (Windows, macOS, Linux)

```powershell
# Build with default settings (Release configuration)
./build.ps1

# Build with Debug configuration
./build.ps1 -Configuration Debug

# Build without running tests
./build.ps1 -NoTest

# Build and publish
./build.ps1 -Publish

# Build, publish to a specific folder
./build.ps1 -Publish -PublishFolder "./dist"

# Get detailed build output
./build.ps1 -Verbosity detailed
```

### Using Command Prompt (Windows)

```cmd
# Build with default settings (Release configuration)
build.bat

# Build with Debug configuration
build.bat --configuration Debug

# Build without running tests
build.bat --no-test

# Build and publish
build.bat --publish

# Build, publish to a specific folder
build.bat --publish --publish-folder dist

# Get detailed build output
build.bat --verbosity detailed
```

## Available Options

| Option | Description |
|--------|-------------|
| `--configuration`, `-c` | The build configuration (Debug or Release, default: Release) |
| `--no-build` | Skip the build step |
| `--no-test` | Skip the test step |
| `--publish` | Publish the application after building |
| `--publish-folder` | The folder to publish to (default: ./publish) |
| `--verbosity`, `-v` | The verbosity level (q[uiet], m[inimal], n[ormal], d[etailed], diag[nostic]) |

## Project Structure

- **ContosoUniversity.Data**: Data access layer with EF Core models and repositories
- **ContosoUniversity.Web**: ASP.NET Core MVC web application
- **ContosoUniversity.Tests**: Unit and integration tests

## Continuous Integration

These build scripts are designed to work with CI/CD pipelines. You can use them in GitHub Actions, Azure DevOps, or other CI systems.
