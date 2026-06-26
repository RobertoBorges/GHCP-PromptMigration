#!/bin/bash
# Hook: Stop - Append session end timestamp to Report-Status.md
# Requires: jq
INPUT=$(cat)
CWD=$(echo "$INPUT" | jq -r '.cwd // empty' 2>/dev/null)
[ -z "$CWD" ] && CWD=$(pwd)

STATUS_FILE="$CWD/reports/Report-Status.md"

if [ -f "$STATUS_FILE" ]; then
    TIMESTAMP=$(date -u +"%Y-%m-%d %H:%M:%S UTC")
    SESSION_ID=$(echo "$INPUT" | jq -r '.sessionId // "unknown"' 2>/dev/null)

    echo "" >> "$STATUS_FILE"
    echo "---" >> "$STATUS_FILE"
    echo "**Session ended:** $TIMESTAMP | Session: $SESSION_ID" >> "$STATUS_FILE"
fi

echo '{"continue":true}'
