# Manual Git Checkout Script for Azure DevOps Pipelines
# This script handles Git checkout issues that commonly result in "Git fetch failed with exit code: 128"

param(
    [string]$RepoUrl = $env:BUILD_REPOSITORY_URI,
    [string]$BranchName = $env:BUILD_SOURCEBRANCH,
    [string]$SourcesDirectory = $env:BUILD_SOURCESDIRECTORY,
    [string]$AccessToken = $env:SYSTEM_ACCESSTOKEN
)

# Show diagnostic information
Write-Host "Starting manual Git checkout process..."
Write-Host "Repository URL: $RepoUrl"
Write-Host "Branch: $BranchName"
Write-Host "Sources Directory: $SourcesDirectory"
Write-Host "Access token available: $($null -ne $AccessToken -and $AccessToken -ne '')"
Write-Host "Current directory: $(Get-Location)"
Write-Host "Git version: $(git --version)"

# Set Git global config
Write-Host "Configuring Git..."
git config --global core.longpaths true
git config --global http.sslVerify false
git config --global http.postBuffer 1048576000
git config --global core.compression 0
git config --global credential.helper store

# Extract the actual branch name from the full reference
if ($BranchName -match "refs/heads/(.+)") {
    $BranchName = $Matches[1]
}
Write-Host "Parsed branch name: $BranchName"

# Clean up existing directory if needed
if (Test-Path $SourcesDirectory -PathType Container) {
    Write-Host "Cleaning up existing directory..."
    Get-ChildItem -Path $SourcesDirectory -Force -Recurse | Remove-Item -Force -Recurse -ErrorAction SilentlyContinue
}
else {
    New-Item -ItemType Directory -Path $SourcesDirectory -Force | Out-Null
}

# Set working directory
Set-Location $SourcesDirectory
Write-Host "Working directory set to: $(Get-Location)"

# Try checkout with multiple approaches
$checkoutSuccess = $false

# Attempt 1: Standard clone
try {
    Write-Host "Attempt 1: Standard Git clone..."
    $env:GIT_TERMINAL_PROMPT = 0
    $output = git clone $RepoUrl . 2>&1
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Standard clone successful"
        $checkoutSuccess = $true
    }
    else {
        Write-Host "Standard clone failed with exit code $LASTEXITCODE"
        Write-Host "Error output: $output"
    }
}
catch {
    Write-Host "Exception during standard clone: $_"
}

# Attempt 2: Clone with access token
if (-not $checkoutSuccess -and $AccessToken) {
    try {
        Write-Host "Attempt 2: Git clone with access token..."
        $secureRepoUrl = $RepoUrl -replace "https://", "https://oauth2:$AccessToken@"
        $output = git clone $secureRepoUrl . 2>&1
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "Clone with access token successful"
            $checkoutSuccess = $true
        }
        else {
            Write-Host "Clone with access token failed with exit code $LASTEXITCODE"
            Write-Host "Error output: $output"
        }
    }
    catch {
        Write-Host "Exception during clone with access token: $_"
    }
}

# Attempt 3: Clone with git protocol and then fix origin
if (-not $checkoutSuccess) {
    try {
        Write-Host "Attempt 3: Trying alternative protocol..."
        
        # Try with git protocol if it's an Azure DevOps repo
        $altRepoUrl = $RepoUrl -replace "https://", "git://"
        $output = git clone $altRepoUrl . 2>&1
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "Alternative protocol clone successful"
            $checkoutSuccess = $true
        }
        else {
            Write-Host "Alternative protocol clone failed with exit code $LASTEXITCODE"
            Write-Host "Error output: $output"
        }
    }
    catch {
        Write-Host "Exception during alternative protocol clone: $_"
    }
}

# Attempt 4: Create empty repo and pull
if (-not $checkoutSuccess) {
    try {
        Write-Host "Attempt 4: Creating empty repo and setting remote..."
        
        git init
        
        if ($AccessToken) {
            $secureRepoUrl = $RepoUrl -replace "https://", "https://oauth2:$AccessToken@"
            git remote add origin $secureRepoUrl
        }
        else {
            git remote add origin $RepoUrl
        }
        
        # Try to fetch
        $output = git fetch origin 2>&1
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "Fetch successful"
            git checkout -f -t origin/$BranchName
            
            if ($LASTEXITCODE -eq 0) {
                Write-Host "Checkout after manual fetch successful"
                $checkoutSuccess = $true
            }
        }
        else {
            Write-Host "Fetch failed with exit code $LASTEXITCODE"
            Write-Host "Error output: $output"
        }
    }
    catch {
        Write-Host "Exception during manual fetch/checkout: $_"
    }
}

# Verify checkout
if ($checkoutSuccess) {
    Write-Host "Repository checkout successful"
    Write-Host "Contents of repository:"
    Get-ChildItem -Force | Select-Object Name, Length, LastWriteTime
    
    # Checkout specific branch if needed
    if ((git branch --show-current) -ne $BranchName) {
        Write-Host "Checking out branch: $BranchName"
        git checkout $BranchName -f
    }
    
    # Show current branch and last commit
    Write-Host "Current branch: $(git branch --show-current)"
    Write-Host "Last commit: $(git log -1 --oneline)"
    
    exit 0  # Success
}
else {
    Write-Host "##vso[task.logissue type=error]Failed to checkout repository after multiple attempts"
    Write-Host "Environment variables:"
    Get-ChildItem env: | Where-Object { $_.Name -match "BUILD|SYSTEM" } | Format-Table -AutoSize
    
    # Check network connectivity
    Write-Host "Testing network connectivity..."
    $uri = [System.Uri]$RepoUrl
    $hostname = $uri.Host
    Test-NetConnection -ComputerName $hostname -Port 443
    
    exit 1  # Failure
}
