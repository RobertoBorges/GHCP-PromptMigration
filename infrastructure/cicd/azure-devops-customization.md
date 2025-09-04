# Azure DevOps Pipeline Customization Guide

## Changing Environment Names

If you want to change the environment names in the pipeline:

1. In the YAML file, update the environment names in these sections:

```yaml
- stage: Deploy_YourEnvironment  # Change 'Deploy_Dev' to your desired name
  displayName: 'Deploy to Your Environment'  # Update display name
  variables:
    environment: 'yourenvironment'  # Update environment variable
  jobs:
  - deployment: DeployInfrastructure
    environment: 'YourEnvironment'  # Update environment reference
```

2. Create corresponding environments in Azure DevOps:
   - Go to Pipelines > Environments
   - Create environments with the same names

## Adding Approval Gates

To add approval requirements:

1. Go to the environment in Azure DevOps (Pipelines > Environments)
2. Select the environment (e.g., Test or Prod)
3. Click on "Approvals and checks"
4. Click "Add check" > "Approvals"
5. Add the required approvers
6. Set minimum number of approvals required
7. Click "Create"

## Adding Variables

If you need to add custom variables:

1. Edit the pipeline YAML and add variables at the top:
```yaml
variables:
  - name: yourVariable
    value: yourValue
  - group: YourVariableGroup
```

2. Create variable groups in Azure DevOps:
   - Go to Pipelines > Library
   - Create variable groups with your variables

## Changing Terraform Backend

If you need to use a different Terraform backend:

1. Update the Terraform backend service connection:
```yaml
- task: TerraformTaskV4@4
  displayName: 'Terraform Init'
  inputs:
    provider: 'azurerm'
    command: 'init'
    workingDirectory: '$(System.ArtifactsDirectory)/terraform'
    backendServiceArm: 'Your Service Connection Name'
    backendAzureRmResourceGroupName: '$(TF_BACKEND_RG)'
    backendAzureRmStorageAccountName: '$(TF_BACKEND_STORAGE)'
    backendAzureRmContainerName: '$(TF_BACKEND_CONTAINER)'
    backendAzureRmKey: 'your-state-file.tfstate'
```

## Adding Post-Deployment Tests

To add tests after deployment:

```yaml
- task: PowerShell@2
  displayName: 'Run Post-Deployment Tests'
  inputs:
    targetType: 'inline'
    script: |
      $baseUrl = "https://your-app-url"
      $endpoints = @("/", "/api/health", "/api/status")
      
      foreach ($endpoint in $endpoints) {
        $url = "$baseUrl$endpoint"
        Write-Host "Testing endpoint: $url"
        try {
          $response = Invoke-WebRequest -Uri $url -UseBasicParsing
          Write-Host "Status code: $($response.StatusCode)"
          if ($response.StatusCode -ne 200) {
            Write-Error "Endpoint $url returned $($response.StatusCode)"
            exit 1
          }
        } catch {
          Write-Error "Error testing endpoint $url: $_"
          exit 1
        }
      }
```

## Setting Up Notifications

Configure notifications for pipeline runs:

1. Go to Project Settings > Notifications
2. Click "New subscription"
3. Select "Build completed"
4. Configure your notification settings
5. Click "Finish"
