#!/bin/bash
# Hook: Stop - Append canonical Action Log entry for session end
# Emits: - <ISO-8601-UTC> | actor=hook | action=session-ended | tokens=~0 | turn=<final> | notes="session=<id>"
# Spec: .github/skills/action-log-format.md
# Requires: jq (falls back gracefully if missing)

INPUT=$(cat)

if command -v jq >/dev/null 2>&1; then
    CWD=$(echo "$INPUT" | jq -r '.cwd // empty' 2>/dev/null)
    SESSION_ID=$(echo "$INPUT" | jq -r '.sessionId // "unknown"' 2>/dev/null)
else
    CWD=""
    SESSION_ID="unknown"
fi

[ -z "$CWD" ] && CWD=$(pwd)
STATUS_FILE="$CWD/reports/Report-Status.md"

if [ -f "$STATUS_FILE" ]; then
    TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%MZ")

    # Trim long session ids to a stable prefix so log lines stay short.
    SESSION_SHORT="${SESSION_ID:0:8}"
    [ -z "$SESSION_SHORT" ] && SESSION_SHORT="unknown"

    # Best-effort turn counter: parse the last turn=<n> from the file.
    FINAL_TURN=$(grep -oE 'turn=[0-9]+' "$STATUS_FILE" | tail -n 1 | sed 's/turn=//')
    [ -z "$FINAL_TURN" ] && FINAL_TURN="?"

    # Ensure the Action Log section exists.
    if ! grep -qE '^##\s+📜\s+Action Log' "$STATUS_FILE"; then
        printf '\n## 📜 Action Log\n\n' >> "$STATUS_FILE"
    fi

    printf -- '- %s | actor=hook | action=session-ended | tokens=~0 | turn=%s | notes="session=%s"\n' \
        "$TIMESTAMP" "$FINAL_TURN" "$SESSION_SHORT" >> "$STATUS_FILE"
fi

echo '{"continue":true}'
