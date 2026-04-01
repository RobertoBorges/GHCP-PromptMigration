# Hook: PreToolUse - Block hardcoded secrets in code changes
# Returns: permissionDecision "deny" if secrets detected
$ErrorActionPreference = "SilentlyContinue"

try {
    $inputText = [Console]::In.ReadToEnd()
    $hookInput = $inputText | ConvertFrom-Json
} catch {
    Write-Output '{"continue":true}'
    exit 0
}

$toolName = $hookInput.tool_name
if ($toolName -notin @("editFiles", "createFile", "edit", "create")) {
    Write-Output '{"continue":true}'
    exit 0
}

$content = $hookInput.tool_input | ConvertTo-Json -Depth 10 -Compress

$patterns = @(
    'Password\s*[:=]\s*["''][^"'']{8,}',
    'ConnectionString\s*[:=]\s*["'']Server=',
    '[Aa]pi[_-]?[Kk]ey\s*[:=]\s*["''][^"'']{8,}',
    'SharedAccessKey=[A-Za-z0-9+/=]{20,}',
    'AccountKey=[A-Za-z0-9+/=]{20,}',
    'sk-[A-Za-z0-9]{20,}',
    'DefaultEndpointsProtocol=https;AccountName=',
    'Server=.*Password=[^;]{8,}',
    'Data Source=.*Password=[^;]{8,}',
    'client[_-]?secret\s*[:=]\s*["''][^"'']{8,}'
)

foreach ($pattern in $patterns) {
    if ($content -match $pattern) {
        $result = @{
            hookSpecificOutput = @{
                hookEventName = "PreToolUse"
                permissionDecision = "deny"
                permissionDecisionReason = "Potential secret detected. Use Azure Key Vault or environment variables instead of hardcoding credentials."
            }
        }
        Write-Output ($result | ConvertTo-Json -Depth 5 -Compress)
        exit 0
    }
}

Write-Output '{"continue":true}'
