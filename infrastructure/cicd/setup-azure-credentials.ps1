# This script helps create a service principal for GitHub Actions to use with Azure
# It outputs the credentials in the format expected by GitHub Actions secrets

param (
    [Parameter(Mandatory=$true)]
    [string]$SubscriptionId,
    
    [Parameter(Mandatory=$false)]
    [string]$ServicePrincipalName = "github-actions-storeapp-sp",
    
    [Parameter(Mandatory=$false)]
    [string]$RoleDefinitionName = "Contributor"
)

# Login to Azure (uncomment if not already logged in)
# Connect-AzAccount

# Set the subscription context
Write-Host "Setting subscription context to: $SubscriptionId" -ForegroundColor Yellow
Select-AzSubscription -SubscriptionId $SubscriptionId

# Create the service principal with Contributor role
Write-Host "Creating service principal: $ServicePrincipalName" -ForegroundColor Yellow
$sp = New-AzADServicePrincipal -DisplayName $ServicePrincipalName -Role $RoleDefinitionName -Scope "/subscriptions/$SubscriptionId"

# Create a password credential for the service principal
$password = New-AzADSpCredential -ObjectId $sp.Id -StartDate (Get-Date) -EndDate (Get-Date).AddYears(1)

# Build the credential JSON
$credentials = @{
    clientId = $sp.AppId
    clientSecret = $password.SecretText
    subscriptionId = $SubscriptionId
    tenantId = (Get-AzContext).Tenant.Id
}

# Convert to JSON
$credentialsJson = $credentials | ConvertTo-Json

# Output the result
Write-Host "Service Principal created successfully!" -ForegroundColor Green
Write-Host "Add the following JSON as a GitHub secret named 'AZURE_CREDENTIALS':" -ForegroundColor Cyan
Write-Host $credentialsJson

# Optionally save to a file (commented out for security)
# $credentialsJson | Out-File -FilePath "azure-credentials.json"
# Write-Host "Credentials also saved to azure-credentials.json" -ForegroundColor Yellow
