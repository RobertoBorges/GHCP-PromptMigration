#!/bin/bash
# Hook: PostToolUse - Provide validation reminders after code edits
# Requires: jq
INPUT=$(cat)
TOOL_NAME=$(echo "$INPUT" | jq -r '.tool_name // empty' 2>/dev/null)

if [ "$TOOL_NAME" != "editFiles" ] && [ "$TOOL_NAME" != "createFile" ] && \
   [ "$TOOL_NAME" != "edit" ] && [ "$TOOL_NAME" != "create" ]; then
    echo '{"continue":true}'
    exit 0
fi

CONTENT=$(echo "$INPUT" | jq -c '.tool_input // empty' 2>/dev/null)
CONTEXT=""

if echo "$CONTENT" | grep -q '\.bicep'; then
    CONTEXT="Bicep file modified. Validate: az bicep build --file <path>"
elif echo "$CONTENT" | grep -q '\.tf"'; then
    CONTEXT="Terraform file modified. Validate: terraform validate"
elif echo "$CONTENT" | grep -q '\.csproj'; then
    CONTEXT="Project file modified. Validate: dotnet restore && dotnet build"
elif echo "$CONTENT" | grep -q 'Dockerfile'; then
    CONTEXT="Dockerfile modified. Check: specific base image tag, HEALTHCHECK, non-root USER"
fi

if [ -n "$CONTEXT" ]; then
    CONTEXT=$(echo "$CONTEXT" | sed 's/"/\\"/g')
    echo "{\"hookSpecificOutput\":{\"hookEventName\":\"PostToolUse\",\"additionalContext\":\"$CONTEXT\"}}"
else
    echo '{"continue":true}'
fi
