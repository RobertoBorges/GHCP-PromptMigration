# Hook: Stop - Append session end timestamp to Report-Status.md
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

if (Test-Path $statusPath) {
    $timestamp = (Get-Date).ToUniversalTime().ToString("yyyy-MM-dd HH:mm:ss") + " UTC"
    $sessionId = $hookInput.sessionId
    if (-not $sessionId) { $sessionId = "unknown" }

    $entry = "`n---`n**Session ended:** $timestamp | Session: $sessionId`n"
    Add-Content -Path $statusPath -Value $entry -ErrorAction SilentlyContinue
}

Write-Output '{"continue":true}'
