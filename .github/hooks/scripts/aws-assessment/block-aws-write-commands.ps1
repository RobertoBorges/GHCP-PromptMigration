# Hook: PreToolUse - Enforce read-only AWS CLI usage
# Denies any AWS CLI invocation whose operation verb is not read-only.
$ErrorActionPreference = "SilentlyContinue"

try {
    $inputText = [Console]::In.ReadToEnd()
    $hookInput = $inputText | ConvertFrom-Json
} catch {
    Write-Output '{"continue":true}'
    exit 0
}

$toolName = $hookInput.tool_name
# Terminal tools are named differently per surface: VS Code uses runInTerminal /
# awaitTerminal, Copilot CLI uses bash / powershell / shell, and toolset-qualified
# forms appear as execute/<tool>. A name this list misses means the read-only
# guarantee silently does not hold on that surface.
$terminalTools = @(
    "runInTerminal", "runTerminalCommand", "terminal", "awaitTerminal", "runCommands",
    "execute", "execute/runInTerminal", "execute/awaitTerminal", "execute/runCommands",
    "bash", "shell", "powershell", "pwsh", "cmd"
)
if ($toolName -notin $terminalTools) {
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

function Deny([string]$reason) {
    $result = @{
        hookSpecificOutput = @{
            hookEventName            = "PreToolUse"
            permissionDecision       = "deny"
            permissionDecisionReason = $reason
        }
    }
    Write-Output ($result | ConvertTo-Json -Depth 5 -Compress)
    exit 0
}

# --- 1. Generic destructive commands -------------------------------------------------
$destructivePatterns = @(
    'rm\s+-rf\s+/',
    'rmdir\s+/s\s+/q\s+[A-Z]:\\',
    'Remove-Item\s+.*-Recurse.*-Force.*[/\\]$',
    'terraform\s+(destroy|apply)',
    'kubectl\s+(delete|apply|patch|scale|drain)',
    'DROP\s+(TABLE|DATABASE|SCHEMA)',
    'TRUNCATE\s+TABLE',
    'git\s+push\s+.*(--force|-f)\s'
)
foreach ($p in $destructivePatterns) {
    if ($command -match $p) {
        Deny "Destructive command blocked. The AWS Account Assessment Agent is read-only. Run this manually if it is genuinely intended."
    }
}

# --- 2. AWS CLI read-only enforcement ------------------------------------------------
# Walk each 'aws ...' invocation token by token. Global flags must be skipped before the
# service/operation pair can be read: a naive regex mistakes '--instance-ids' for the
# operation, sees it start with '-', treats it as a flag and lets the real verb through.
$valueFlags = @('--profile','--region','--output','--endpoint-url','--query','--ca-bundle',
                '--color','--cli-read-timeout','--cli-connect-timeout','--cli-binary-format')

function Get-AwsServiceOperation([string[]]$tokens, [int]$start) {
    $i = $start
    while ($i -lt $tokens.Count) {
        $t = $tokens[$i]
        if ($t -notmatch '^-') { break }
        if ($t -match '=') { $i++; continue }          # --profile=prod
        if ($valueFlags -contains $t.ToLower()) { $i += 2; continue }
        $i++                                            # boolean flag such as --no-cli-pager
    }
    if ($i + 1 -ge $tokens.Count) { return $null }
    return @{ Service = $tokens[$i]; Operation = $tokens[$i + 1] }
}

$allowedVerb = '^(describe|list|get|lookup|search|select|batch-get|generate-credential-report|help)'
$commandTokens = $command -split '\s+' | Where-Object { $_ -ne '' }

for ($idx = 0; $idx -lt $commandTokens.Count; $idx++) {
    if ($commandTokens[$idx].ToLower() -ne 'aws') { continue }

    $pair = Get-AwsServiceOperation -tokens $commandTokens -start ($idx + 1)
    if (-not $pair) { continue }

    $first     = $pair.Service
    $operation = $pair.Operation

    if ($operation -match '^-') { continue }                        # nothing left but flags
    if ($operation -match $allowedVerb) { continue }                # allowed read-only verb
    if ($first -eq 's3' -and $operation -in @('ls')) { continue }

    Deny "READ-ONLY VIOLATION: 'aws $first $operation' is not a read-only operation. This agent may only run describe-*, list-*, get-*, lookup-*, search-*, select-* and batch-get-* operations. If a mutating action is genuinely required, run it yourself outside this agent."
}

# --- 3. Explicitly forbidden AWS operations even though the verb looks read-only ------
$forbidden = @(
    @{ p = 'aws\s+secretsmanager\s+get-secret-value';                       r = 'Reading secret values is forbidden. Inventory secrets by name/ARN only.' },
    @{ p = 'aws\s+ssm\s+get-parameter[s]?(-by-path)?[^\r\n]*--with-decryption'; r = 'Reading decrypted SSM parameters is forbidden. Inventory parameter names/types only.' },
    @{ p = 'aws\s+kms\s+(decrypt|generate-data-key)';                       r = 'Producing plaintext key material is forbidden.' },
    @{ p = 'aws\s+configure\s+set';                                         r = 'Modifying local AWS configuration is out of scope for this agent.' },
    @{ p = 'aws\s+s3\s+(rm|rb|mv|cp|sync)\s';                               r = 'S3 data operations are forbidden. Use s3api list/get metadata operations only.' },
    @{ p = 'aws\s+cloudformation\s+detect-stack-drift';                     r = 'detect-stack-drift starts a job. Use describe-stack-drift-detection-status to read an existing result.' },
    @{ p = 'aws\s+dynamodb\s+(scan|query)\s';                               r = 'Reading table data is out of scope. Use describe-table for metadata.' }
)
foreach ($f in $forbidden) {
    if ($command -match "(?i)$($f.p)") { Deny "BLOCKED: $($f.r)" }
}

Write-Output '{"continue":true}'
