# Setting Up Pipeline Triggers in Azure DevOps

This guide explains how to configure different types of triggers for your application deployment pipeline in Azure DevOps.

## Types of Pipeline Triggers

Azure DevOps supports several types of triggers:

1. **Branch-based triggers**: Automatically run when changes are pushed to specific branches
2. **Pull request validation**: Run when pull requests are created or updated
3. **Scheduled triggers**: Run on a predefined schedule
4. **Pipeline completion triggers**: Run after another pipeline completes
5. **Manual triggers**: Run only when explicitly triggered by a user

## Configuring Triggers in YAML Pipelines

### 1. Branch-Based Triggers

To automatically trigger your pipeline when changes are pushed to specific branches:

```yaml
trigger:
  branches:
    include:
      - main
      - pipeline-branch
      - feature/*
    exclude:
      - docs/*
```

To disable automatic triggers entirely:

```yaml
trigger: none
```

### 2. Pull Request Validation

To trigger the pipeline for pull requests:

```yaml
pr:
  branches:
    include:
      - main
      - pipeline-branch
  paths:
    include:
      - src/*
    exclude:
      - docs/*
      - README.md
```

To disable PR triggers:

```yaml
pr: none
```

### 3. Scheduled Triggers

To run the pipeline on a schedule:

```yaml
schedules:
- cron: '0 0 * * *'  # Run at midnight every day
  displayName: Daily midnight build
  branches:
    include:
      - main
  always: true  # Run even if there are no code changes
```

## Setting Up Triggers via Azure Portal

For triggers that cannot be configured in YAML, use the Azure DevOps portal:

1. Go to **Pipelines** > **Your Pipeline** > **Edit**
2. Click the **More actions** (three dots) menu > **Triggers**
3. Configure triggers in the visual editor

## Steps to Set Up Triggers for Our Application

### Option 1: Using the PowerShell Script

1. Open a PowerShell window
2. Navigate to the script directory:
   ```powershell
   cd C:\Users\v-pmamidi\source\repos\GHCP-PromptMigration\infrastructure\cicd
   ```
3. Run the configuration script with your Azure DevOps details:
   ```powershell
   .\Configure-Pipeline-Trigger.ps1 -AzureDevOpsOrg "YourOrg" -AzureDevOpsProject "YourProject"
   ```

### Option 2: Manual Configuration

#### Step 1: Update YAML File

1. Edit the `azure-devops-app-pipeline.yml` file
2. Add the appropriate trigger configuration at the top of the file
3. Commit and push your changes to the repository

#### Step 2: Create the Pipeline in Azure DevOps

1. Go to your Azure DevOps project
2. Navigate to **Pipelines** > **New Pipeline**
3. Select your repository
4. Choose **Existing Azure Pipelines YAML file**
5. Select the path: `/infrastructure/cicd/azure-devops-app-pipeline.yml`
6. Click **Continue**
7. Review the pipeline and click **Save**

#### Step 3: Configure Additional Triggers (if needed)

1. Go to the pipeline settings
2. Click **Edit** > **More actions** (three dots) > **Triggers**
3. Configure any additional triggers not specified in the YAML file

## Trigger Strategy for Our Application

For our migrated applications, we recommend the following trigger strategy:

1. **Development Branch**: Configure automatic triggers for the `pipeline-branch`
2. **Main Branch**: Use PR validation to ensure quality before merging
3. **Scheduled Builds**: Run nightly builds to verify deployment health
4. **Manual Deployment**: Require manual approval for production deployments

## Monitoring and Managing Triggers

To check the status of your pipeline triggers:

1. Go to **Pipelines** > **Your Pipeline**
2. Click **Edit** > **More actions** (three dots) > **Triggers**
3. Review the configured triggers

## Troubleshooting Trigger Issues

If your pipeline is not triggering as expected:

1. **Check YAML Configuration**: Ensure trigger syntax is correct
2. **Review Branch Filters**: Verify branch naming matches your repository
3. **Check Path Filters**: Ensure file path patterns are correct
4. **Service Hooks**: Verify webhook configurations are properly set up
5. **Build Policies**: Check repository policies that might block triggers

## Best Practices

1. **Limit Automatic Triggers**: Only trigger builds when necessary to conserve resources
2. **Use Path Filters**: Only trigger when relevant files change
3. **Schedule Non-Critical Builds**: Run resource-intensive builds during off-hours
4. **Implement Approval Gates**: Require approvals for production deployments
5. **Monitor Build History**: Regularly review what's triggering your pipelines
