# Hook: PostToolUse - Provide validation reminders after code edits
# Returns: short additionalContext reminder based on file type
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
$context = $null

if ($content -match '\.bicep') {
    $context = "Bicep file modified. Validate: az bicep build --file <path>"
} elseif ($content -match '\.tf"') {
    $context = "Terraform file modified. Validate: terraform validate"
} elseif ($content -match '\.csproj') {
    $context = "Project file modified. Validate: dotnet restore && dotnet build"
} elseif ($content -match 'Dockerfile') {
    $context = "Dockerfile modified. Check: specific base image tag, HEALTHCHECK, non-root USER"
}

if ($context) {
    $result = @{
        hookSpecificOutput = @{
            hookEventName = "PostToolUse"
            additionalContext = $context
        }
    }
    Write-Output ($result | ConvertTo-Json -Depth 5 -Compress)
} else {
    Write-Output '{"continue":true}'
}
