# Hook: SessionStart - Load migration state + recent Action Log for recovery
# Returns: additionalContext with current migration status + last 5 Action Log entries
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
$assessPath = Join-Path $cwd "reports" "Application-Assessment-Report.md"
$capabilityPath = Join-Path $cwd "reports" "Capability-Matrix.yaml"

$summary = @()

# ── Extract key info from status report (phase, target, platform, IaC) ─────
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

    if ($statusContent -match '(?i)(App Service|Container Apps|AKS|Functions|VMs)') {
        $summary += "Platform: $($Matches[1])"
    }

    if ($statusContent -match '(?i)(Bicep|Terraform)') {
        $summary += "IaC: $($Matches[1])"
    }

    # ── Parse the Action Log for recovery: last 5 entries + turn totals ────
    $logLines = [regex]::Matches(
        $statusContent,
        '(?m)^-\s+\d{4}-\d{2}-\d{2}T\d{2}:\d{2}Z\s+\|\s+actor=\S+\s+\|\s+action=\S+.*$'
    )
    if ($logLines.Count -gt 0) {
        $recent = @()
        $start = [Math]::Max(0, $logLines.Count - 5)
        for ($i = $start; $i -lt $logLines.Count; $i++) {
            $line = $logLines[$i].Value -replace '^-\s+', ''
            $recent += $line
        }
        $summary += "Recent actions (last 5): " + ($recent -join " ; ")

        # Extract highest turn counter seen — that's where the next session picks up.
        $turnMatches = [regex]::Matches($statusContent, '\|\s*turn=(\d+)')
        if ($turnMatches.Count -gt 0) {
            $maxTurn = 0
            foreach ($m in $turnMatches) {
                $t = [int]$m.Groups[1].Value
                if ($t -gt $maxTurn) { $maxTurn = $t }
            }
            $summary += "Prior session ended at turn=$maxTurn — next turn=$($maxTurn + 1)"
        }
    }
}

if (Test-Path $assessPath) {
    $summary += "Assessment report exists"
}

if (Test-Path $capabilityPath) {
    $summary += "Capability Matrix exists"
}

# Detect portfolio Migration Strategy Report deck(s) (HTML)
try {
    $strategyDecks = Get-ChildItem $cwd -Recurse -Filter "*Migration_Strategy_Report*.html" -Depth 5 -ErrorAction SilentlyContinue
    if ($strategyDecks -and $strategyDecks.Count -gt 0) {
        $deckCount = $strategyDecks.Count
        $latestDeck = $strategyDecks | Sort-Object LastWriteTime -Descending | Select-Object -First 1
        $deckName = $latestDeck.Name
        $summary += "Portfolio plan: $deckCount deck(s), latest='$deckName' (use /PortfolioStrategy to regenerate or iterate)"
    }
} catch { }

# Detect project stack from workspace — brief signal only.
$detections = @()
if (Get-ChildItem $cwd -Recurse -Filter "*.csproj" -Depth 4 -ErrorAction SilentlyContinue | Select-Object -First 1) { $detections += ".NET" }
if (Get-ChildItem $cwd -Recurse -Filter "pom.xml" -Depth 4 -ErrorAction SilentlyContinue | Select-Object -First 1) { $detections += "Java/Maven" }
if (Get-ChildItem $cwd -Recurse -Filter "build.gradle*" -Depth 4 -ErrorAction SilentlyContinue | Select-Object -First 1) { $detections += "Java/Gradle" }
if (Get-ChildItem $cwd -Recurse -Filter "package.json" -Depth 4 -ErrorAction SilentlyContinue | Select-Object -First 1) { $detections += "Node.js" }
if (Get-ChildItem $cwd -Recurse -Filter "requirements.txt" -Depth 4 -ErrorAction SilentlyContinue | Select-Object -First 1) { $detections += "Python" }
if (Get-ChildItem $cwd -Recurse -Filter "pyproject.toml" -Depth 4 -ErrorAction SilentlyContinue | Select-Object -First 1) { $detections += "Python/Poetry" }
if (Get-ChildItem $cwd -Recurse -Filter "composer.json" -Depth 4 -ErrorAction SilentlyContinue | Select-Object -First 1) { $detections += "PHP" }
if (Get-ChildItem $cwd -Recurse -Filter "Gemfile" -Depth 4 -ErrorAction SilentlyContinue | Select-Object -First 1) { $detections += "Ruby" }
if (Get-ChildItem $cwd -Recurse -Filter "go.mod" -Depth 4 -ErrorAction SilentlyContinue | Select-Object -First 1) { $detections += "Go" }
if (Get-ChildItem $cwd -Recurse -Filter "Cargo.toml" -Depth 4 -ErrorAction SilentlyContinue | Select-Object -First 1) { $detections += "Rust" }
if (Get-ChildItem $cwd -Recurse -Filter "web.config" -Depth 4 -ErrorAction SilentlyContinue | Select-Object -First 1) { $detections += "web.config" }
if (Get-ChildItem $cwd -Recurse -Filter "*.svc" -Depth 4 -ErrorAction SilentlyContinue | Select-Object -First 1) { $detections += "WCF" }
if (Get-ChildItem $cwd -Recurse -Filter "Dockerfile" -Depth 4 -ErrorAction SilentlyContinue | Select-Object -First 1) { $detections += "Docker" }

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
