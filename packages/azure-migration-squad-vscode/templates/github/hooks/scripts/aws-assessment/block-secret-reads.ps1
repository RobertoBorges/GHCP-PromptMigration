# Hook: PreToolUse - Prevent credentials and secret material from being written to disk
# Scans file-edit payloads for AWS credentials, tokens and private keys.
$ErrorActionPreference = "SilentlyContinue"

try {
    $inputText = [Console]::In.ReadToEnd()
    $hookInput = $inputText | ConvertFrom-Json
} catch {
    Write-Output '{"continue":true}'
    exit 0
}

$toolName = $hookInput.tool_name
if ($toolName -notin @("createFile", "editFiles", "applyPatch", "insertEdit", "replaceString", "multiReplaceString")) {
    Write-Output '{"continue":true}'
    exit 0
}

$payload = ""
foreach ($prop in @("content", "newString", "code", "text", "patch")) {
    if ($hookInput.tool_input.$prop) { $payload += ($hookInput.tool_input.$prop | Out-String) }
}
if (-not $payload) {
    Write-Output '{"continue":true}'
    exit 0
}

$secretPatterns = @(
    @{ n = 'AWS access key ID';       p = '\b(AKIA|ASIA|ABIA|ACCA)[0-9A-Z]{16}\b' },
    @{ n = 'AWS secret access key';   p = '(?i)(aws_)?secret_?access_?key\s*[:=]\s*["\x27]?[A-Za-z0-9/+=]{40}' },
    @{ n = 'AWS session token';       p = '(?i)(aws_)?session_?token\s*[:=]\s*["\x27]?[A-Za-z0-9/+=]{100,}' },
    @{ n = 'Private key block';       p = '-----BEGIN (RSA |EC |OPENSSH |PGP )?PRIVATE KEY-----' },
    @{ n = 'Generic password assign'; p = '(?i)\b(password|passwd|pwd)\s*[:=]\s*["\x27][^"\x27\s]{8,}["\x27]' },
    @{ n = 'DB connection string';    p = '(?i)(mongodb(\+srv)?|postgres(ql)?|mysql|redis|amqp)://[^:\s]+:[^@\s]+@' },
    @{ n = 'Bearer token';            p = '(?i)authorization\s*[:=]\s*["\x27]?bearer\s+[A-Za-z0-9._\-]{20,}' }
)

foreach ($s in $secretPatterns) {
    if ($payload -match $s.p) {
        $result = @{
            hookSpecificOutput = @{
                hookEventName            = "PreToolUse"
                permissionDecision       = "deny"
                permissionDecisionReason = "Secret material detected in the content being written ($($s.n)). Assessment artifacts must never contain credentials, tokens or private keys. Record the resource identity (name/ARN) instead of its content."
            }
        }
        Write-Output ($result | ConvertTo-Json -Depth 5 -Compress)
        exit 0
    }
}

Write-Output '{"continue":true}'
