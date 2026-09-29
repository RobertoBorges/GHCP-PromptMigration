# Hook: PreToolUse - Enforce customer data isolation
# Purpose: when a customer context is active (env var COPILOT_CUSTOMER_CONTEXT set
#          to the customer folder path), block Read/edit tool calls targeting
#          files inside any OTHER customer folder under Customers/.
# Returns: permissionDecision "deny" if a cross-customer access is detected.
$ErrorActionPreference = "SilentlyContinue"

try {
    $inputText = [Console]::In.ReadToEnd()
    $hookInput = $inputText | ConvertFrom-Json
} catch {
    Write-Output '{"continue":true}'
    exit 0
}

$customerContext = $env:COPILOT_CUSTOMER_CONTEXT
if (-not $customerContext) {
    Write-Output '{"continue":true}'
    exit 0
}

$toolName = $hookInput.tool_name
$readOrEditTools = @("read", "edit", "editFiles", "create", "createFile", "search/codebase")
if ($toolName -notin $readOrEditTools) {
    Write-Output '{"continue":true}'
    exit 0
}

$targetPath = ""
if ($hookInput.tool_input.filePath) { $targetPath = $hookInput.tool_input.filePath }
elseif ($hookInput.tool_input.path) { $targetPath = $hookInput.tool_input.path }
elseif ($hookInput.tool_input.file_path) { $targetPath = $hookInput.tool_input.file_path }

if (-not $targetPath) {
    Write-Output '{"continue":true}'
    exit 0
}

$normalizedTarget = $targetPath -replace '\\', '/'
$normalizedContext = $customerContext -replace '\\', '/'

if ($normalizedTarget -notmatch '(?i)/?Customers/') {
    Write-Output '{"continue":true}'
    exit 0
}

# Extract the customer leaf (segment immediately after 'Customers') from both target and context.
# Path-segment equality (NOT substring) prevents false matches like context='Customers/HCA' allowing target='Customers/HCA Healthcare/...'.
$targetSegments = $normalizedTarget -split '/'
$contextSegments = $normalizedContext -split '/'

$targetCustomer = $null
for ($i = 0; $i -lt $targetSegments.Count - 1; $i++) {
    if ($targetSegments[$i] -ieq 'Customers') {
        $targetCustomer = $targetSegments[$i + 1]
        break
    }
}

$contextCustomer = $null
for ($i = 0; $i -lt $contextSegments.Count - 1; $i++) {
    if ($contextSegments[$i] -ieq 'Customers') {
        $contextCustomer = $contextSegments[$i + 1]
        break
    }
}

# Fallback: if context isn't a Customers/-rooted path, use its leaf as the customer ID
if (-not $contextCustomer) {
    $contextCustomer = Split-Path $normalizedContext -Leaf
}

if ($targetCustomer -and $contextCustomer -and ($targetCustomer -ieq $contextCustomer)) {
    Write-Output '{"continue":true}'
    exit 0
}

$contextLeaf = $contextCustomer
$result = @{
    hookSpecificOutput = @{
        hookEventName = "PreToolUse"
        permissionDecision = "deny"
        permissionDecisionReason = "Customer data isolation violation: active customer context is '$contextLeaf' but the requested file '$targetPath' is in a different customer folder. Each customer is a fully isolated engagement (NDA). Do NOT cross-reference customer folders for any reason."
    }
}
Write-Output ($result | ConvertTo-Json -Depth 5 -Compress)
