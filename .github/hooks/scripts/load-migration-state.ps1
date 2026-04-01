# Hook: SessionStart - Load migration state to provide agent context
# Returns: concise additionalContext with current migration status
$ErrorActionPreference = "SilentlyContinue"

try {
    $inputText = [Console]::In.ReadToEnd()
    $hookInput = $inputText | ConvertFrom-Json
} catch {
    Write-Output '{"continue":true}'
    exit 0
}

$cwd = $hookInput.cwd
if (-not $cwd) { $cwd = Get-Location }

$statusPath = Join-Path $cwd "reports" "Report-Status.md"
$assessPath = Join-Path $cwd "reports" "Application-Assessment-Report.md"

$summary = @()

# Extract key info from status report
if (Test-Path $statusPath) {
    $statusContent = Get-Content $statusPath -Raw -ErrorAction SilentlyContinue

    if ($statusContent -match '(?i)Current\s*Phase\s*:\s*(.+)') {
        $summary += "Phase: $($Matches[1].Trim())"
    } elseif ($statusContent -match '\[x\].*Phase\s*(\d)') {
        $summary += "Completed: Phase $($Matches[1])"
    }

    if ($statusContent -match '(?i)Target\s*Framework\s*:\s*(.+)') {
        $summary += "Target: $($Matches[1].Trim())"
    }

    if ($statusContent -match '(?i)(App Service|Container Apps|AKS)') {
        $summary += "Platform: $($Matches[1])"
    }

    if ($statusContent -match '(?i)(Bicep|Terraform)') {
        $summary += "IaC: $($Matches[1])"
    }
}

if (Test-Path $assessPath) {
    $summary += "Assessment report exists"
}

# Detect project type from workspace
$detections = @()
if (Get-ChildItem $cwd -Recurse -Filter "*.csproj" -Depth 4 -ErrorAction SilentlyContinue | Select-Object -First 1) {
    $detections += ".NET"
}
if (Get-ChildItem $cwd -Recurse -Filter "pom.xml" -Depth 4 -ErrorAction SilentlyContinue | Select-Object -First 1) {
    $detections += "Java/Maven"
}
if (Get-ChildItem $cwd -Recurse -Filter "web.config" -Depth 4 -ErrorAction SilentlyContinue | Select-Object -First 1) {
    $detections += "web.config"
}
if (Get-ChildItem $cwd -Recurse -Filter "*.svc" -Depth 4 -ErrorAction SilentlyContinue | Select-Object -First 1) {
    $detections += "WCF"
}
if (Get-ChildItem $cwd -Recurse -Filter "Dockerfile" -Depth 4 -ErrorAction SilentlyContinue | Select-Object -First 1) {
    $detections += "Docker"
}

if ($detections.Count -gt 0) {
    $summary += "Detected: $($detections -join ', ')"
}

if ($summary.Count -gt 0) {
    $contextStr = "Migration context: " + ($summary -join " | ")
    $result = @{
        hookSpecificOutput = @{
            hookEventName = "SessionStart"
            additionalContext = $contextStr
        }
    }
    Write-Output ($result | ConvertTo-Json -Depth 5 -Compress)
} else {
    Write-Output '{"continue":true}'
}
