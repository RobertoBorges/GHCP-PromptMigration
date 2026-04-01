#!/bin/bash
# Hook: SessionStart - Load migration state to provide agent context
# Requires: jq
INPUT=$(cat)
CWD=$(echo "$INPUT" | jq -r '.cwd // empty' 2>/dev/null)
[ -z "$CWD" ] && CWD=$(pwd)

SUMMARY=""

STATUS_FILE="$CWD/reports/Report-Status.md"
if [ -f "$STATUS_FILE" ]; then
    PHASE=$(grep -i 'Current\s*Phase\s*:' "$STATUS_FILE" | head -1 | sed 's/.*:\s*//')
    TARGET=$(grep -i 'Target.*Framework\s*:' "$STATUS_FILE" | head -1 | sed 's/.*:\s*//')
    PLATFORM=$(grep -oiE '(App Service|Container Apps|AKS)' "$STATUS_FILE" | head -1)
    IAC=$(grep -oiE '(Bicep|Terraform)' "$STATUS_FILE" | head -1)

    [ -n "$PHASE" ] && SUMMARY="Phase: $PHASE"
    [ -n "$TARGET" ] && SUMMARY="${SUMMARY:+$SUMMARY | }Target: $TARGET"
    [ -n "$PLATFORM" ] && SUMMARY="${SUMMARY:+$SUMMARY | }Platform: $PLATFORM"
    [ -n "$IAC" ] && SUMMARY="${SUMMARY:+$SUMMARY | }IaC: $IAC"
fi

ASSESS_FILE="$CWD/reports/Application-Assessment-Report.md"
[ -f "$ASSESS_FILE" ] && SUMMARY="${SUMMARY:+$SUMMARY | }Assessment report exists"

# Detect project type
DETECTIONS=""
[ -n "$(find "$CWD" -maxdepth 5 -name '*.csproj' 2>/dev/null | head -1)" ] && DETECTIONS=".NET"
[ -n "$(find "$CWD" -maxdepth 5 -name 'pom.xml' 2>/dev/null | head -1)" ] && DETECTIONS="${DETECTIONS:+$DETECTIONS, }Java/Maven"
[ -n "$(find "$CWD" -maxdepth 5 -name 'web.config' 2>/dev/null | head -1)" ] && DETECTIONS="${DETECTIONS:+$DETECTIONS, }web.config"
[ -n "$(find "$CWD" -maxdepth 5 -name '*.svc' 2>/dev/null | head -1)" ] && DETECTIONS="${DETECTIONS:+$DETECTIONS, }WCF"
[ -n "$(find "$CWD" -maxdepth 5 -name 'Dockerfile' 2>/dev/null | head -1)" ] && DETECTIONS="${DETECTIONS:+$DETECTIONS, }Docker"

[ -n "$DETECTIONS" ] && SUMMARY="${SUMMARY:+$SUMMARY | }Detected: $DETECTIONS"

if [ -n "$SUMMARY" ]; then
    CONTEXT="Migration context: $SUMMARY"
    CONTEXT=$(echo "$CONTEXT" | sed 's/"/\\"/g')
    echo "{\"hookSpecificOutput\":{\"hookEventName\":\"SessionStart\",\"additionalContext\":\"$CONTEXT\"}}"
else
    echo '{"continue":true}'
fi
