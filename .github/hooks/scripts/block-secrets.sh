#!/bin/bash
# Hook: PreToolUse - Block hardcoded secrets in code changes
# Requires: jq
INPUT=$(cat)
TOOL_NAME=$(echo "$INPUT" | jq -r '.tool_name // empty' 2>/dev/null)

if [ "$TOOL_NAME" != "editFiles" ] && [ "$TOOL_NAME" != "createFile" ] && \
   [ "$TOOL_NAME" != "edit" ] && [ "$TOOL_NAME" != "create" ]; then
    echo '{"continue":true}'
    exit 0
fi

CONTENT=$(echo "$INPUT" | jq -c '.tool_input // empty' 2>/dev/null)

if echo "$CONTENT" | grep -qiE \
    'Password[[:space:]]*[:=][[:space:]]*["'"'"'][^"'"'"'[:space:]]{8,}|ConnectionString[[:space:]]*[:=][[:space:]]*["'"'"']Server=|[Aa]pi[_-]?[Kk]ey[[:space:]]*[:=][[:space:]]*["'"'"'][^"'"'"'[:space:]]{8,}|SharedAccessKey=[A-Za-z0-9+/=]{20,}|AccountKey=[A-Za-z0-9+/=]{20,}|sk-[A-Za-z0-9]{20,}|DefaultEndpointsProtocol=https;AccountName=|Server=.*Password=[^;]{8,}|Data Source=.*Password=[^;]{8,}|client[_-]?secret[[:space:]]*[:=][[:space:]]*["'"'"'][^"'"'"'[:space:]]{8,}'; then
    echo '{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"deny","permissionDecisionReason":"Potential secret detected. Use Azure Key Vault or environment variables instead of hardcoding credentials."}}'
    exit 0
fi

echo '{"continue":true}'
