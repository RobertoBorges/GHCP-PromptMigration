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
    'rm[[:space:]]+-rf[[:space:]]+/|rmdir[[:space:]]+/s[[:space:]]+/q|az[[:space:]]+group[[:space:]]+delete|az[[:space:]]+resource[[:space:]]+delete|terraform[[:space:]]+destroy|DROP[[:space:]]+(TABLE|DATABASE|SCHEMA)|DELETE[[:space:]]+FROM[[:space:]]+[[:alnum:]_]+[[:space:]]*;?[[:space:]]*$|TRUNCATE[[:space:]]+TABLE|git[[:space:]]+push[[:space:]]+.*--force|git[[:space:]]+push[[:space:]]+-f[[:space:]]|azd[[:space:]]+down[[:space:]]+--force|kubectl[[:space:]]+delete[[:space:]]+(namespace|ns)[[:space:]]'; then
    echo '{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"deny","permissionDecisionReason":"Destructive command blocked. This operation requires explicit user consent. Run manually if intended."}}'
    exit 0
fi

echo '{"continue":true}'
