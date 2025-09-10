# Troubleshooting Git Fetch Error 128

This guide provides detailed steps to troubleshoot and resolve the "Git fetch failed with exit code: 128" error in Azure DevOps pipelines.

## Understanding Error 128

Error code 128 in Git usually indicates one of the following issues:
- Authentication problems
- Network connectivity issues
- SSL certificate validation problems
- Repository access permission issues
- Git configuration problems

## Last Resort Solution: Manual Git Checkout Script

We've implemented a robust last-resort solution that should fix even the most stubborn Git checkout issues:

1. **Dedicated PowerShell Script**:
   - Located at `/infrastructure/cicd/scripts/git-checkout.ps1`
   - Automatically used by the pipeline as its first step
   - Makes multiple attempts to clone the repository using different methods
   - Provides detailed diagnostics for each attempt

2. **How the Script Works**:
   - Configures optimal Git settings to avoid common issues
   - Tries multiple checkout methods in sequence:
     1. Standard Git clone
     2. Clone with OAuth token authentication
     3. Alternative Git protocol
     4. Manual initialization and fetch
   - Diagnoses network connectivity issues
   - Verifies successful checkout
   - Provides detailed logs for troubleshooting

3. **Pipeline Configuration**:
   - The pipeline has been updated to use this script
   - OAuth token access is provided to the script
   - No changes to your pipeline definition are needed

## Solution Implemented in Pipeline

We've updated the pipeline to include a robust Git cloning process that:

1. Configures Git with appropriate settings:
   - Enables long paths support
   - Disables SSL verification if needed

2. Provides detailed diagnostics:
   - Logs Git version information
   - Shows repository URL and source directory
   - Captures and displays detailed error messages

3. Implements fallback mechanisms:
   - Uses alternate authentication method with OAuth token
   - Cleans existing directory to avoid conflicts

4. Verifies success:
   - Lists repository contents after cloning
   - Checks out the correct branch

## Additional Troubleshooting Steps

If you still encounter Git fetch errors after these pipeline changes, try the following:

### 1. Check Pipeline Permissions

Ensure the pipeline has appropriate permissions:
- Navigate to Project Settings > Pipelines > Pipeline permissions
- Verify that the build service has "Read" access to the repository
- Enable the "Allow pipelines to access this repository" option

### 2. Enable OAuth Token Access

Update pipeline settings to use OAuth token for Git operations:
- Edit the pipeline
- Click on the "..." menu and select "Pipeline settings"
- Check the option "Allow scripts to access the OAuth token"

### 3. Check Repository Settings

Review repository settings in Azure DevOps:
- Go to Project Settings > Repositories > Your Repository
- Under "Security", verify that the build service account has "Read" permission
- If using Git LFS, ensure the build service has appropriate permissions

### 4. Network and Firewall Issues

If running self-hosted agents:
- Verify network connectivity to Azure DevOps (or your Git provider)
- Check if firewalls or proxy servers are blocking Git operations
- Ensure outbound HTTPS connections are allowed

### 5. SSL Certificate Issues

If SSL certificate validation is failing:
- Update the Git configuration in the build agent with:
  ```
  git config --global http.sslVerify false
  ```
- For a more secure approach, install the proper certificates in the agent's trust store

### 6. Git Authentication

For Microsoft-hosted agents:
- Use the built-in System.AccessToken
- Configure repository with appropriate permissions for the build service

For self-hosted agents:
- Configure Git credentials properly
- Consider using a Personal Access Token with appropriate scopes

## Advanced Diagnostics

To further diagnose Git issues, you can add these environment variables:
```
GIT_TRACE=1
GIT_CURL_VERBOSE=1
```

These will provide detailed information about Git operations and the underlying HTTP requests.
