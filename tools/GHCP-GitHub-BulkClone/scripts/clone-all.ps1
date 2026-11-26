<#
.SYNOPSIS
    Bulk-clones every accessible Git repository owned by a GitHub user or organization.
    Idempotent (safe to re-run - skips repos already on disk) and local-only
    (never pushes or modifies anything server-side).

.PARAMETER Owner
    GitHub user or organization login, e.g. octocat or github.

.PARAMETER DestinationPath
    Local folder to clone all repos into. Defaults to the current directory.

.EXAMPLE
    .\clone-all.ps1 -Owner "octocat" -DestinationPath "C:\Repos\octocat"

.NOTES
    Requires: GitHub CLI (gh), Git for Windows, and an authenticated gh session.
#>
param(
    [Parameter(Mandatory = $true)]
    [ValidateNotNullOrEmpty()]
    [string]$Owner,

    [string]$DestinationPath = (Get-Location).Path
)

$ErrorActionPreference = 'Stop'

$Owner = $Owner.Trim()
if ([uri]::IsWellFormedUriString($Owner, [uriKind]::Absolute)) {
    $ownerUri = [uri]$Owner
    if ($ownerUri.Host -notin @('github.com', 'www.github.com')) {
        throw 'Owner URL must use github.com.'
    }
    $Owner = $ownerUri.AbsolutePath.Trim('/').Split('/')[0]
}
if ($Owner -notmatch '^[A-Za-z0-9](?:[A-Za-z0-9-]{0,37}[A-Za-z0-9])?$') {
    throw "'$Owner' is not a valid GitHub user or organization login."
}

if (-not (Get-Command gh -ErrorAction SilentlyContinue)) {
    throw 'GitHub CLI (gh) is required. Install it from https://cli.github.com/.'
}
if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    throw 'Git is required. Install Git for Windows from https://git-scm.com/.'
}

gh auth status 2>&1 | Out-Null
if ($LASTEXITCODE -ne 0) {
    throw 'GitHub CLI is not authenticated. Run: gh auth login --web --git-protocol https'
}

if (-not (Test-Path -LiteralPath $DestinationPath)) {
    New-Item -ItemType Directory -Path $DestinationPath -Force | Out-Null
}
$DestinationPath = (Resolve-Path -LiteralPath $DestinationPath).Path

Write-Host "Listing repositories owned by '$Owner'..." -ForegroundColor Cyan
$query = @'
query($endCursor: String, $owner: String!) {
    repositoryOwner(login: $owner) {
        repositories(first: 100, after: $endCursor, orderBy: {field: NAME, direction: ASC}) {
            nodes {
                name
                nameWithOwner
                url
                isArchived
                isFork
                defaultBranchRef { name }
            }
            pageInfo { hasNextPage endCursor }
        }
    }
}
'@
$pagesJson = gh api graphql --paginate --slurp -F "owner=$Owner" -f "query=$query"
if ($LASTEXITCODE -ne 0) {
    throw "Could not list repositories for '$Owner'. Check the owner and your GitHub access."
}

$pages = @($pagesJson | ConvertFrom-Json)
if ($pages.Count -eq 0 -or $null -eq $pages[0].data.repositoryOwner) {
        throw "GitHub user or organization '$Owner' was not found or is not visible to this account."
}
$repos = @($pages | ForEach-Object { $_.data.repositoryOwner.repositories.nodes })

$repos |
    Select-Object name, nameWithOwner, defaultBranchRef, url, isArchived, isFork |
    ConvertTo-Json -Depth 5 |
    Out-File -Encoding utf8 (Join-Path $DestinationPath 'repos.json')

$results = @()
$reservedNamePattern = '(?i)(^|/)(con|prn|aux|nul|com[1-9]|lpt[1-9])(\.[^/]*)?$'

function Repair-AndCheckout {
    param([Parameter(Mandatory = $true)][string]$Branch)

    $badPaths = @()

    $reserved = git ls-tree -r --name-only $Branch | Select-String -Pattern $reservedNamePattern
    if ($reserved) {
        $badPaths += $reserved.Line
    }

    # Use -c so Git quotes unusual names consistently; Python parses NUL-delimited bytes safely.
    $pythonAvailable = $null -ne (Get-Command python -ErrorAction SilentlyContinue)
    if ($pythonAvailable) {
        $pathListFile = Join-Path $env:TEMP "github-bulk-clone-$PID-paths.bin"
        $badPathFile = Join-Path $env:TEMP "github-bulk-clone-$PID-bad.txt"
        try {
            $gitProcess = Start-Process -FilePath (Get-Command git).Source -ArgumentList @(
                '-c', 'core.quotepath=false', 'ls-tree', '-r', '-z', '--name-only', $Branch
            ) -RedirectStandardOutput $pathListFile -NoNewWindow -Wait -PassThru
            if ($gitProcess.ExitCode -ne 0) {
                throw "Could not inspect paths on branch '$Branch'."
            }
            python -c @"
import pathlib
data = pathlib.Path(r'$pathListFile').read_bytes()
parts = [part for part in data.split(b'\x00') if part]
bad = [part for part in parts if any(byte < 32 for byte in part) or any(char in part for char in b'<>:"|?*')]
pathlib.Path(r'$badPathFile').write_text('\n'.join(part.decode('utf-8', errors='replace') for part in bad), encoding='utf-8')
"@
            if (Test-Path -LiteralPath $badPathFile) {
                $badPaths += @(Get-Content -LiteralPath $badPathFile | Where-Object { $_ })
            }
        } finally {
            Remove-Item -LiteralPath $pathListFile, $badPathFile -ErrorAction SilentlyContinue
        }
    }

    $badPaths = @($badPaths | Select-Object -Unique)
    if ($badPaths.Count -gt 0) {
        $exclude = @($badPaths | ForEach-Object { ":!$_" })
        git checkout $Branch -- . @exclude 2>&1 | Out-Null
        return $badPaths
    }

    git checkout $Branch -- . 2>&1 | Out-Null
    return @()
}

foreach ($repo in $repos) {
    $name = $repo.name
    $branch = $repo.defaultBranchRef.name
    $destination = Join-Path $DestinationPath $name

    if (Test-Path -LiteralPath $destination) {
        git -C $destination rev-parse --verify HEAD 2>&1 | Out-Null
        if ($LASTEXITCODE -eq 0) {
            $pending = @(git -C $destination status --short).Count
            $note = if ($pending -gt 0) { 'existing checkout has local changes or missing files' } else { $null }
            Write-Host "SKIP (already exists): $name$(if ($note) { " - $note" })" -ForegroundColor Yellow
            $results += [pscustomobject]@{ repo = $repo.nameWithOwner; status = 'skipped'; excluded = @(); note = $note }
        } else {
            Write-Host "FAIL: $name (existing directory is not a complete Git checkout)" -ForegroundColor Red
            $results += [pscustomobject]@{
                repo = $repo.nameWithOwner
                status = 'fail'
                excluded = @()
                note = 'existing directory is not a complete Git checkout; left untouched'
            }
        }
        continue
    }

    Write-Host "Cloning $($repo.nameWithOwner) (branch: $branch)..." -ForegroundColor Cyan

    if ($branch) {
        gh repo clone $repo.nameWithOwner $destination -- --branch $branch --single-branch -c core.longpaths=true 2>&1 | Out-Null
    } else {
        gh repo clone $repo.nameWithOwner $destination -- -c core.longpaths=true 2>&1 | Out-Null
    }

    if ($LASTEXITCODE -eq 0) {
        Write-Host "OK: $name" -ForegroundColor Green
        $results += [pscustomobject]@{ repo = $repo.nameWithOwner; status = 'ok'; excluded = @() }
        continue
    }

    # A failed clone may still have downloaded every object and failed only during checkout.
    if ((Test-Path -LiteralPath (Join-Path $destination '.git')) -and $branch) {
        Push-Location $destination
        try {
            git config core.longpaths true
            $excluded = @(Repair-AndCheckout -Branch $branch)
            $pending = @(git status --short).Count
        } finally {
            Pop-Location
        }

        if ($excluded.Count -gt 0 -and $pending -le $excluded.Count) {
            Write-Host "OK-WITH-EXCLUSIONS: $name (skipped: $($excluded -join ', '))" -ForegroundColor Yellow
            $results += [pscustomobject]@{ repo = $repo.nameWithOwner; status = 'ok-with-exclusions'; excluded = $excluded }
        } elseif ($pending -eq 0) {
            Write-Host "OK: $name (recovered)" -ForegroundColor Green
            $results += [pscustomobject]@{ repo = $repo.nameWithOwner; status = 'ok'; excluded = @() }
        } else {
            Write-Host "FAIL: $name (needs manual attention)" -ForegroundColor Red
            $results += [pscustomobject]@{ repo = $repo.nameWithOwner; status = 'fail'; excluded = @() }
        }
    } else {
        Write-Host "FAIL: $name" -ForegroundColor Red
        $results += [pscustomobject]@{ repo = $repo.nameWithOwner; status = 'fail'; excluded = @() }
    }
}

$results |
    ConvertTo-Json -Depth 5 |
    Out-File -Encoding utf8 (Join-Path $DestinationPath 'clone-results.json')

$results | Group-Object status | Select-Object Name, Count | Format-Table -AutoSize

$failed = @($results | Where-Object { $_.status -eq 'fail' })
if ($failed.Count -gt 0) {
    Write-Host "`nRepositories needing manual attention:" -ForegroundColor Red
    $failed | ForEach-Object { Write-Host "  git clone https://github.com/$($_.repo).git" }
}