<#
.SYNOPSIS
    Bulk-clones every Git repository of an Azure DevOps project to a local folder.
    Idempotent (safe to re-run — skips repos already on disk) and local-only
    (never pushes / never modifies anything server-side).

.PARAMETER OrgUrl
    Azure DevOps organization URL, e.g. https://dev.azure.com/MyOrg

.PARAMETER Project
    Azure DevOps project name.

.PARAMETER DestinationPath
    Local folder to clone all repos into. Defaults to the current directory.

.EXAMPLE
    .\clone-all.ps1 -OrgUrl "https://dev.azure.com/MyOrg" -Project "MyProject" -DestinationPath "C:\Repos\MyProject"

.NOTES
    Requires: az cli, azure-devops extension, an authenticated az session
    (az login --use-device-code --allow-no-subscriptions is enough — no
    Azure subscription is needed to read Azure DevOps repos).
#>
param(
    [Parameter(Mandatory = $true)]
    [string]$OrgUrl,

    [Parameter(Mandatory = $true)]
    [string]$Project,

    [string]$DestinationPath = (Get-Location).Path
)

$ErrorActionPreference = 'Continue'

if (-not (Test-Path $DestinationPath)) {
    New-Item -ItemType Directory -Path $DestinationPath -Force | Out-Null
}
Set-Location $DestinationPath

# Long paths bite a lot of older/monorepo-style repos on Windows — enable once, globally.
git config --global core.longpaths true

az devops configure --defaults organization=$OrgUrl project=$Project | Out-Null

Write-Host "Listing repositories in '$Project'..." -ForegroundColor Cyan
az repos list -o json | ConvertFrom-Json | Select-Object name, defaultBranch |
    ConvertTo-Json | Out-File -Encoding utf8 (Join-Path $DestinationPath 'repos.json')

$repos = Get-Content (Join-Path $DestinationPath 'repos.json') -Raw | ConvertFrom-Json

# Azure DevOps' well-known first-party resource ID — public constant, not client-specific.
$adoResourceId = '499b84ac-1321-427f-aa17-267ca6975798'
$token = az account get-access-token --resource $adoResourceId --query accessToken -o tsv

$results = @()

# Windows reserved device names (with or without an extension).
$reservedNamePattern = '(?i)(^|/)(con|prn|aux|nul|com[1-9]|lpt[1-9])(\.[^/]*)?$'

function Repair-AndCheckout {
    param([string]$Branch)

    $badPaths = @()

    # 1) Reserved device names.
    $reserved = git ls-tree -r --name-only $Branch | Select-String -Pattern $reservedNamePattern
    if ($reserved) { $badPaths += $reserved.Line }

    # 2) Invalid/control characters — only attempted if Python is available.
    $pythonAvailable = $null -ne (Get-Command python -ErrorAction SilentlyContinue)
    if ($pythonAvailable) {
        git ls-tree -r -z --name-only $Branch | Out-File -Encoding utf8 all_paths.txt
        $badFromPython = python -c @"
data = open('all_paths.txt','rb').read()
parts = [p for p in data.split(b'\x00') if p]
bad = [p for p in parts if any(b < 32 for b in p) or any(c in p for c in b'<>:\"|?*')]
for b in bad:
    print(b.decode('utf-8', errors='replace'))
"@
        if ($badFromPython) { $badPaths += ($badFromPython -split "`n" | Where-Object { $_ }) }
    }

    if ($badPaths.Count -gt 0) {
        $badPaths = $badPaths | Select-Object -Unique
        $exclude = $badPaths | ForEach-Object { ":!$_" }
        git checkout $Branch -- . @exclude 2>&1 | Out-Null
        Remove-Item all_paths.txt, good_paths.txt -ErrorAction SilentlyContinue
        return $badPaths
    }

    # No known-bad paths detected — just retry a plain checkout (covers long-path / transient cases
    # now that core.longpaths is set).
    git checkout $Branch -- . 2>&1 | Out-Null
    return @()
}

foreach ($repo in $repos) {
    $name = $repo.name
    $branch = $repo.defaultBranch -replace '^refs/heads/', ''
    $dest = Join-Path $DestinationPath $name

    if (Test-Path $dest) {
        Write-Host "SKIP (already exists): $name" -ForegroundColor Yellow
        $results += [pscustomobject]@{ repo = $name; status = 'skipped'; excluded = @() }
        continue
    }

    $encodedRepo = [uri]::EscapeDataString($name)
    $cloneUrl = "https://x-access-token:$token@dev.azure.com/$([uri]::EscapeDataString($OrgUrl -replace '^https://dev.azure.com/', ''))/$([uri]::EscapeDataString($Project))/_git/$encodedRepo"

    Write-Host "Cloning $name (branch: $branch)..." -ForegroundColor Cyan
    if ($branch) {
        git clone --branch $branch --single-branch $cloneUrl $dest 2>&1 | Out-Null
    } else {
        git clone $cloneUrl $dest 2>&1 | Out-Null
    }

    if ($LASTEXITCODE -eq 0) {
        Write-Host "OK: $name" -ForegroundColor Green
        $results += [pscustomobject]@{ repo = $name; status = 'ok'; excluded = @() }
        continue
    }

    # Clone reported failure — could be a checkout-only failure (objects downloaded fine).
    if (Test-Path (Join-Path $dest '.git')) {
        Push-Location $dest
        $excluded = Repair-AndCheckout -Branch $branch
        $pending = (git status --short | Measure-Object -Line).Lines
        Pop-Location

        if ($excluded.Count -gt 0 -and $pending -le $excluded.Count) {
            Write-Host "OK-WITH-EXCLUSIONS: $name (skipped: $($excluded -join ', '))" -ForegroundColor Yellow
            $results += [pscustomobject]@{ repo = $name; status = 'ok-with-exclusions'; excluded = $excluded }
        } elseif ($pending -eq 0) {
            Write-Host "OK: $name (recovered)" -ForegroundColor Green
            $results += [pscustomobject]@{ repo = $name; status = 'ok'; excluded = @() }
        } else {
            Write-Host "FAIL: $name (needs manual attention)" -ForegroundColor Red
            $results += [pscustomobject]@{ repo = $name; status = 'fail'; excluded = @() }
        }
    } else {
        Write-Host "FAIL: $name" -ForegroundColor Red
        $results += [pscustomobject]@{ repo = $name; status = 'fail'; excluded = @() }
    }
}

$results | ConvertTo-Json -Depth 5 | Out-File -Encoding utf8 (Join-Path $DestinationPath 'clone-results.json')
$results | Group-Object status | Select-Object Name, Count | Format-Table -AutoSize

$failed = $results | Where-Object { $_.status -eq 'fail' }
if ($failed) {
    Write-Host "`nRepos needing manual attention:" -ForegroundColor Red
    $failed | ForEach-Object { Write-Host "  git clone https://$($OrgUrl -replace 'https://','')/_git/$($_.repo)" }
}
