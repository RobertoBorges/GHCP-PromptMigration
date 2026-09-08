# Hook: SessionStart - Load assessment state so the agent resumes without re-discovery
# Returns a concise additionalContext block describing accounts scanned and next action.
$ErrorActionPreference = "SilentlyContinue"

try {
    $inputText = [Console]::In.ReadToEnd()
    $hookInput = $inputText | ConvertFrom-Json
} catch {
    Write-Output '{"continue":true}'
    exit 0
}

$cwd = $hookInput.cwd
if (-not $cwd) { $cwd = (Get-Location).Path }

$reportsDir = Join-Path $cwd "reports"
$rawDir     = Join-Path $reportsDir "raw"
$statusPath = Join-Path $reportsDir "Report-Status.md"
$scopePath  = Join-Path $rawDir "_scope.json"

$summary = New-Object System.Collections.Generic.List[string]

if (-not (Test-Path $reportsDir)) {
    $result = @{
        hookSpecificOutput = @{
            hookEventName     = "SessionStart"
            additionalContext = "AWS Assessment: no reports/ folder found. No assessment has started. Begin with /phase0-setupandscope."
        }
    }
    Write-Output ($result | ConvertTo-Json -Depth 5 -Compress)
    exit 0
}

# Scope and options
if (Test-Path $scopePath) {
    try {
        $scope = Get-Content $scopePath -Raw | ConvertFrom-Json
        $summary.Add("Mode: $($scope.accountModel)")
        if ($scope.regions) { $summary.Add("Regions in scope: $($scope.regions.Count)") }
        if ($scope.options) {
            $opts = @()
            if ($scope.options.costAnalysis)     { $opts += "cost" }
            if ($scope.options.securityFindings) { $opts += "findings" }
            if ($scope.options.maskAccountIds)   { $opts += "masked-ids" }
            if ($opts.Count -gt 0) { $summary.Add("Options: $($opts -join ', ')") }
        }
    } catch { }
}

# Account folders are the source of truth
$accountDirs = @()
if (Test-Path $rawDir) {
    $accountDirs = @(Get-ChildItem $rawDir -Directory -ErrorAction SilentlyContinue |
        Where-Object { $_.Name -match '^\d{12}$' })
}

if ($accountDirs.Count -gt 0) {
    $lines = @()
    $totalItems = 0
    foreach ($d in $accountDirs) {
        $phases = @()
        if (Test-Path (Join-Path $d.FullName "_index.json"))               { $phases += "P1" }
        if (Test-Path (Join-Path $d.FullName "_summary.json"))             { $phases += "P2" }
        if (Test-Path (Join-Path $d.FullName "_inventory-enriched.json"))  { $phases += "P3" }
        if (Test-Path (Join-Path $d.FullName "_edges.json"))               { $phases += "P4" }

        $items = ""
        $sumFile = Join-Path $d.FullName "_summary.json"
        if (Test-Path $sumFile) {
            try {
                $s = Get-Content $sumFile -Raw | ConvertFrom-Json
                if ($null -ne $s.totalItems) {
                    $items = " ($($s.totalItems) items)"
                    $totalItems += [int]$s.totalItems
                }
            } catch { }
        }

        $phaseText = if ($phases.Count -gt 0) { $phases -join "+" } else { "started" }
        $lines += "$($d.Name)[$phaseText]$items"
    }
    $summary.Add("Accounts scanned: $($accountDirs.Count) -> $($lines -join '; ')")
    if ($totalItems -gt 0) { $summary.Add("Total items collected: $totalItems") }
}
else {
    $summary.Add("No account data collected yet under reports/raw/.")
}

# Coverage gaps
$gapCount = 0
foreach ($d in $accountDirs) {
    $errFile = Join-Path $d.FullName "_errors.json"
    if (Test-Path $errFile) {
        try {
            $errs = Get-Content $errFile -Raw | ConvertFrom-Json
            $gapCount += @($errs | Where-Object { $_.class -eq 'coverage-gap' }).Count
        } catch { }
    }
}
if ($gapCount -gt 0) { $summary.Add("Coverage gaps recorded: $gapCount") }

# Status file next action
if (Test-Path $statusPath) {
    $statusContent = Get-Content $statusPath -Raw -ErrorAction SilentlyContinue
    if ($statusContent -match '(?ms)##\s*Next Action\s*(.+?)(\r?\n#|\z)') {
        $next = ($Matches[1] -replace '\s+', ' ').Trim()
        if ($next.Length -gt 240) { $next = $next.Substring(0, 240) + "..." }
        $summary.Add("Next action (from Report-Status.md): $next")
    }
}

# Which reports already exist
$existing = @()
foreach ($f in @(
        "AWS-Account-Assessment-Report.md", "AWS-Resource-Inventory.md",
        "AWS-Network-Topology.md", "AWS-Dependency-Map.md",
        "AWS-Security-Findings.md", "AWS-Tagging-Governance.md",
        "AWS-Cost-Analysis.md", "Azure-Migration-Readiness.md", "inventory.csv")) {
    if (Test-Path (Join-Path $reportsDir $f)) { $existing += $f }
}
if ($existing.Count -gt 0) { $summary.Add("Reports present: $($existing -join ', ')") }

$summary.Add("Reminder: this agent is READ-ONLY. Reports must be regenerated from ALL folders under reports/raw/ whenever a new account is added.")

$result = @{
    hookSpecificOutput = @{
        hookEventName     = "SessionStart"
        additionalContext = "AWS Assessment state -- " + ($summary -join " | ")
    }
}
Write-Output ($result | ConvertTo-Json -Depth 5 -Compress)
