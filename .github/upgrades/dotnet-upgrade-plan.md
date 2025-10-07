# .NET 8.0 Upgrade Plan

## Execution Steps

Execute steps below sequentially one by one in the order they are listed.

1. Validate that a .NET 8.0 SDK required for this upgrade is installed on the machine and if not, help to get it installed.
2. Ensure that the SDK version specified in global.json files is compatible with the .NET 8.0 upgrade.
3. Upgrade WCFDemo.Service\WCFDemo.Service.csproj
4. Upgrade WCFDemo.Host\WCFDemo.Host.csproj
5. Upgrade WCFDemo.Client\WCFDemo.Client.csproj

## Settings

This section contains settings and data used by execution steps.

### Project upgrade details

This section contains details about each project upgrade and modifications that need to be done in the project.

#### WCFDemo.Service\WCFDemo.Service.csproj modifications

Project properties changes:
  - Project file needs to be converted to SDK-style
  - Target framework should be changed from `.NETFramework,Version=v3.5` to `net8.0`

Feature upgrades:
  - **Migrate .NET Framework WCF services to CoreWCF**: This project contains WCF service components that need to be migrated to CoreWCF for .NET 8.0 compatibility. CoreWCF is the modern implementation of WCF for .NET Core and .NET 5+.

#### WCFDemo.Host\WCFDemo.Host.csproj modifications

Project properties changes:
  - Project file needs to be converted to SDK-style
  - Target framework should be changed from `.NETFramework,Version=v3.5` to `net8.0`

#### WCFDemo.Client\WCFDemo.Client.csproj modifications

Project properties changes:
  - Project file needs to be converted to SDK-style
  - Target framework should be changed from `.NETFramework,Version=v3.5` to `net8.0`
