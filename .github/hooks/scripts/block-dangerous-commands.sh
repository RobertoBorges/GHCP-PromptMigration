#!/bin/bash
# Hook: PreToolUse - Block destructive terminal commands
# Requires: jq
INPUT=$(cat)
TOOL_NAME=$(echo "$INPUT" | jq -r '.tool_name // empty' 2>/dev/null)

if [ "$TOOL_NAME" != "runInTerminal" ] && [ "$TOOL_NAME" != "runTerminalCommand" ] && \
   [ "$TOOL_NAME" != "terminal" ]; then
    echo '{"continue":true}'
    exit 0
fi

COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // .tool_input.input // empty' 2>/dev/null)

if [ -z "$COMMAND" ]; then
    echo '{"continue":true}'
    exit 0
fi

if echo "$COMMAND" | grep -qiE \
    'rm\s+-rf\s+/|rmdir\s+/s\s+/q|az\s+group\s+delete|az\s+resource\s+delete|terraform\s+destroy|DROP\s+(TABLE|DATABASE|SCHEMA)|DELETE\s+FROM\s+\w+\s*;?\s*$|TRUNCATE\s+TABLE|git\s+push\s+.*--force|git\s+push\s+-f\s|azd\s+down\s+--force|kubectl\s+delete\s+(namespace|ns)\s'; then
    echo '{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"deny","permissionDecisionReason":"Destructive command blocked. This operation requires explicit user consent. Run manually if intended."}}'
    exit 0
fi

echo '{"continue":true}'
