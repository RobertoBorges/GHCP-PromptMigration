#!/bin/bash
# Hook: SessionStart - Load migration state + recent Action Log for recovery
# Returns: additionalContext with current migration status + last 5 Action Log entries
# Spec: .github/skills/action-log-format.md
# Requires: jq (returns {"continue":true} gracefully if missing)

INPUT=$(cat)

if command -v jq >/dev/null 2>&1; then
    CWD=$(echo "$INPUT" | jq -r '.cwd // empty' 2>/dev/null)
else
    CWD=""
fi
[ -z "$CWD" ] && CWD=$(pwd)

STATUS_FILE="$CWD/reports/Report-Status.md"
ASSESS_FILE="$CWD/reports/Application-Assessment-Report.md"
CAPABILITY_FILE="$CWD/reports/Capability-Matrix.yaml"

SUMMARY=""

append_summary() {
    if [ -z "$SUMMARY" ]; then
        SUMMARY="$1"
    else
        SUMMARY="$SUMMARY | $1"
    fi
}

if [ -f "$STATUS_FILE" ]; then
    # Phase, Target, Platform, IaC — quick greps
    PHASE=$(grep -iE 'Current\s*Phase\s*:\s*' "$STATUS_FILE" | head -n 1 | sed -E 's/.*Current\s*Phase\s*:\s*//i')
    [ -n "$PHASE" ] && append_summary "Phase: $PHASE"

    TARGET=$(grep -iE 'Target\s*Framework\s*:\s*' "$STATUS_FILE" | head -n 1 | sed -E 's/.*Target\s*Framework\s*:\s*//i')
    [ -n "$TARGET" ] && append_summary "Target: $TARGET"

    PLATFORM=$(grep -oE '(App Service|Container Apps|AKS|Functions|VMs)' "$STATUS_FILE" | head -n 1)
    [ -n "$PLATFORM" ] && append_summary "Platform: $PLATFORM"

    IAC=$(grep -oE '(Bicep|Terraform)' "$STATUS_FILE" | head -n 1)
    [ -n "$IAC" ] && append_summary "IaC: $IAC"

    # Parse Action Log — last 5 entries + highest turn counter
    if grep -qE '^-\s+[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}Z\s+\|\s+actor=' "$STATUS_FILE"; then
        RECENT=$(grep -E '^-\s+[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}Z\s+\|\s+actor=' "$STATUS_FILE" \
                    | tail -n 5 \
                    | sed -E 's/^-\s+//' \
                    | tr '\n' ';' \
                    | sed 's/;$//' \
                    | sed 's/;/ ; /g')
        append_summary "Recent actions (last 5): $RECENT"

        MAX_TURN=$(grep -oE 'turn=[0-9]+' "$STATUS_FILE" | sed 's/turn=//' | sort -n | tail -n 1)
        if [ -n "$MAX_TURN" ]; then
            NEXT_TURN=$((MAX_TURN + 1))
            append_summary "Prior session ended at turn=$MAX_TURN — next turn=$NEXT_TURN"
        fi
    fi
fi

[ -f "$ASSESS_FILE" ] && append_summary "Assessment report exists"
[ -f "$CAPABILITY_FILE" ] && append_summary "Capability Matrix exists"

# Portfolio strategy decks
DECK_COUNT=$(find "$CWD" -maxdepth 5 -name "*Migration_Strategy_Report*.html" 2>/dev/null | wc -l | tr -d ' ')
if [ "$DECK_COUNT" -gt 0 ]; then
    LATEST_DECK=$(find "$CWD" -maxdepth 5 -name "*Migration_Strategy_Report*.html" 2>/dev/null | head -n 1 | xargs basename 2>/dev/null)
    append_summary "Portfolio plan: $DECK_COUNT deck(s), latest='$LATEST_DECK' (use /PortfolioStrategy to iterate)"
fi

# Detect project stack — brief signal only
DETECTIONS=""
add_detection() {
    if [ -z "$DETECTIONS" ]; then DETECTIONS="$1"; else DETECTIONS="$DETECTIONS, $1"; fi
}
[ -n "$(find "$CWD" -maxdepth 4 -name '*.csproj' 2>/dev/null | head -n 1)" ] && add_detection ".NET"
[ -n "$(find "$CWD" -maxdepth 4 -name 'pom.xml' 2>/dev/null | head -n 1)" ] && add_detection "Java/Maven"
[ -n "$(find "$CWD" -maxdepth 4 -name 'build.gradle*' 2>/dev/null | head -n 1)" ] && add_detection "Java/Gradle"
[ -n "$(find "$CWD" -maxdepth 4 -name 'package.json' 2>/dev/null | head -n 1)" ] && add_detection "Node.js"
[ -n "$(find "$CWD" -maxdepth 4 -name 'requirements.txt' 2>/dev/null | head -n 1)" ] && add_detection "Python"
[ -n "$(find "$CWD" -maxdepth 4 -name 'pyproject.toml' 2>/dev/null | head -n 1)" ] && add_detection "Python/Poetry"
[ -n "$(find "$CWD" -maxdepth 4 -name 'composer.json' 2>/dev/null | head -n 1)" ] && add_detection "PHP"
[ -n "$(find "$CWD" -maxdepth 4 -name 'Gemfile' 2>/dev/null | head -n 1)" ] && add_detection "Ruby"
[ -n "$(find "$CWD" -maxdepth 4 -name 'go.mod' 2>/dev/null | head -n 1)" ] && add_detection "Go"
[ -n "$(find "$CWD" -maxdepth 4 -name 'Cargo.toml' 2>/dev/null | head -n 1)" ] && add_detection "Rust"
[ -n "$(find "$CWD" -maxdepth 4 -name 'web.config' 2>/dev/null | head -n 1)" ] && add_detection "web.config"
[ -n "$(find "$CWD" -maxdepth 4 -name '*.svc' 2>/dev/null | head -n 1)" ] && add_detection "WCF"
[ -n "$(find "$CWD" -maxdepth 4 -name 'Dockerfile' 2>/dev/null | head -n 1)" ] && add_detection "Docker"

[ -n "$DETECTIONS" ] && append_summary "Detected: $DETECTIONS"

if [ -n "$SUMMARY" ]; then
    if command -v jq >/dev/null 2>&1; then
        jq -n --arg ctx "Migration context: $SUMMARY" \
            '{hookSpecificOutput: {hookEventName: "SessionStart", additionalContext: $ctx}}'
    else
        printf '{"hookSpecificOutput":{"hookEventName":"SessionStart","additionalContext":"Migration context: %s"}}\n' "$SUMMARY"
    fi
else
    echo '{"continue":true}'
fi
