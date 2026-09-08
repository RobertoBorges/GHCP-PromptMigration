# Hook: Stop - Refresh the assessment status footer with what is actually on disk
# Keeps Report-Status.md honest between sessions without touching the analytical content.
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

if (-not (Test-Path $statusPath)) {
    Write-Output '{"continue":true}'
    exit 0
}

$accountDirs = @()
if (Test-Path $rawDir) {
    $accountDirs = @(Get-ChildItem $rawDir -Directory -ErrorAction SilentlyContinue |
        Where-Object { $_.Name -match '^\d{12}$' } | Sort-Object Name)
}

$rows = @()
$totalItems = 0
$totalGaps = 0

foreach ($d in $accountDirs) {
    $p1 = if (Test-Path (Join-Path $d.FullName "_index.json"))              { "OK" } else { "--" }
    $p2 = if (Test-Path (Join-Path $d.FullName "_summary.json"))            { "OK" } else { "--" }
    $p3 = if (Test-Path (Join-Path $d.FullName "_inventory-enriched.json")) { "OK" } else { "--" }
    $p4 = if (Test-Path (Join-Path $d.FullName "_edges.json"))              { "OK" } else { "--" }

    $items = "-"
    $lastScan = "-"
    $sumFile = Join-Path $d.FullName "_summary.json"
    if (Test-Path $sumFile) {
        try {
            $s = Get-Content $sumFile -Raw | ConvertFrom-Json
            if ($null -ne $s.totalItems) { $items = $s.totalItems; $totalItems += [int]$s.totalItems }
            if ($s.finishedAt) { $lastScan = ([datetime]$s.finishedAt).ToString("yyyy-MM-dd HH:mm") }
        } catch { }
    }
    if ($lastScan -eq "-") {
        $lastScan = (Get-Item $d.FullName).LastWriteTimeUtc.ToString("yyyy-MM-dd HH:mm")
    }

    $errFile = Join-Path $d.FullName "_errors.json"
    if (Test-Path $errFile) {
        try {
            $errs = Get-Content $errFile -Raw | ConvertFrom-Json
            $totalGaps += @($errs | Where-Object { $_.class -eq 'coverage-gap' }).Count
        } catch { }
    }

    $rows += "| $($d.Name) | $p1 | $p2 | $p3 | $p4 | $items | $lastScan UTC |"
}

$regionCount = 0
if (Test-Path $rawDir) {
    $regionCount = @(Get-ChildItem $rawDir -Directory -Recurse -Depth 1 -ErrorAction SilentlyContinue |
        Where-Object { $_.Parent.Name -match '^\d{12}$' -and $_.Name -ne 'global' } |
        Select-Object -ExpandProperty Name -Unique).Count
}

$block = @()
$block += ""
$block += "<!-- AUTO-GENERATED: refreshed at session end from reports/raw/. Do not edit by hand. -->"
$block += "## Collected Data (auto-refreshed)"
$block += ""
$block += "_Last refreshed: $((Get-Date).ToUniversalTime().ToString('yyyy-MM-dd HH:mm')) UTC_"
$block += ""
if ($rows.Count -gt 0) {
    $block += "| Account | P1 | P2 | P3 | P4 | Items | Last scanned |"
    $block += "|---------|----|----|----|----|-------|--------------|"
    $block += $rows
    $block += ""
    $block += "- Accounts with data: **$($accountDirs.Count)**"
    $block += "- Distinct regions with data: **$regionCount**"
    $block += "- Total items collected: **$totalItems**"
    $block += "- Coverage gaps recorded: **$totalGaps**"
}
else {
    $block += "_No account folders found under `reports/raw/`._"
}
$block += ""

$content = Get-Content $statusPath -Raw
$marker = "<!-- AUTO-GENERATED: refreshed at session end from reports/raw/. Do not edit by hand. -->"
$idx = $content.IndexOf($marker)
if ($idx -ge 0) {
    $content = $content.Substring(0, $idx).TrimEnd()
}
$content = $content.TrimEnd() + "`n" + ($block -join "`n")
Set-Content -Path $statusPath -Value $content -Encoding utf8NoBOM

Write-Output '{"continue":true}'
