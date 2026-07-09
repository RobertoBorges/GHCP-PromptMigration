# Hook: Stop - Append canonical Action Log entry for session end
# Emits: - <ISO-8601-UTC> | actor=hook | action=session-ended | tokens=~0 | turn=<final> | notes="session=<id>"
# Spec: .github/skills/action-log-format.md
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
    $timestampUtc = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mmZ")
    $sessionId = $hookInput.sessionId
    if (-not $sessionId) { $sessionId = "unknown" }
    # Trim long session ids to a stable prefix so log lines stay short.
    if ($sessionId.Length -gt 8) { $sessionId = $sessionId.Substring(0, 8) }

    # Best-effort turn counter: parse the last Action Log entry to find the last turn=<n>
    # and use turn=<final> which the agent may have advanced during the session.
    # Hooks can't know the true final turn — leave a "?" if unknown; the next
    # session-start hook will infer from the last log line.
    $finalTurn = "?"
    try {
        $content = Get-Content $statusPath -Raw -ErrorAction SilentlyContinue
        if ($content) {
            $matches = [regex]::Matches($content, '\|\s*turn=(\d+)')
            if ($matches.Count -gt 0) {
                $lastTurn = [int]$matches[$matches.Count - 1].Groups[1].Value
                $finalTurn = $lastTurn.ToString()
            }
        }
    } catch { }

    # Ensure the file has an Action Log section — append one if missing so subsequent
    # session-start hooks + prompts can find it deterministically.
    $hasSection = $false
    try {
        $lookup = Get-Content $statusPath -Raw -ErrorAction SilentlyContinue
        if ($lookup -and $lookup -match '(?m)^##\s+📜\s+Action Log') { $hasSection = $true }
    } catch { }

    if (-not $hasSection) {
        Add-Content -Path $statusPath -Value "`n## 📜 Action Log`n" -ErrorAction SilentlyContinue
    }

    $entry = "- $timestampUtc | actor=hook | action=session-ended | tokens=~0 | turn=$finalTurn | notes=`"session=$sessionId`""
    Add-Content -Path $statusPath -Value $entry -ErrorAction SilentlyContinue
}

Write-Output '{"continue":true}'
