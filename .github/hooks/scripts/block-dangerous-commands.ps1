# Hook: PreToolUse - Block destructive terminal commands
# Returns: permissionDecision "deny" if dangerous command detected
$ErrorActionPreference = "SilentlyContinue"

try {
    $inputText = [Console]::In.ReadToEnd()
    $hookInput = $inputText | ConvertFrom-Json
} catch {
    Write-Output '{"continue":true}'
    exit 0
}

$toolName = $hookInput.tool_name
if ($toolName -notin @("runInTerminal", "runTerminalCommand", "terminal")) {
    Write-Output '{"continue":true}'
    exit 0
}

$command = ""
if ($hookInput.tool_input.command) { $command = $hookInput.tool_input.command }
elseif ($hookInput.tool_input.input) { $command = $hookInput.tool_input.input }

if (-not $command) {
    Write-Output '{"continue":true}'
    exit 0
}

$dangerousPatterns = @(
    'rm\s+-rf\s+/',
    'rmdir\s+/s\s+/q\s+[A-Z]:\\',
    'Remove-Item\s+.*-Recurse.*-Force.*[/\\]$',
    'az\s+group\s+delete',
    'az\s+resource\s+delete',
    'terraform\s+destroy',
    'DROP\s+(TABLE|DATABASE|SCHEMA)',
    'DELETE\s+FROM\s+\w+\s*;?\s*$',
    'TRUNCATE\s+TABLE',
    'git\s+push\s+.*--force',
    'git\s+push\s+-f\s',
    'azd\s+down\s+--force',
    'kubectl\s+delete\s+(namespace|ns)\s'
)

foreach ($pattern in $dangerousPatterns) {
    if ($command -match $pattern) {
        $result = @{
            hookSpecificOutput = @{
                hookEventName = "PreToolUse"
                permissionDecision = "deny"
                permissionDecisionReason = "Destructive command blocked: This operation requires explicit user consent. Run manually if intended."
            }
        }
        Write-Output ($result | ConvertTo-Json -Depth 5 -Compress)
        exit 0
    }
}

Write-Output '{"continue":true}'
