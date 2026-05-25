#!/bin/bash
# Hook: PreToolUse - Enforce customer data isolation
# Purpose: when a customer context is active (env var COPILOT_CUSTOMER_CONTEXT set
#          to the customer folder path), block Read/edit tool calls targeting
#          files inside any OTHER customer folder under Customers/.
# Returns: permissionDecision "deny" if a cross-customer access is detected.
# Requires: jq

INPUT=$(cat)

if [ -z "$COPILOT_CUSTOMER_CONTEXT" ]; then
    echo '{"continue":true}'
    exit 0
fi

TOOL_NAME=$(echo "$INPUT" | jq -r '.tool_name // empty' 2>/dev/null)
case "$TOOL_NAME" in
    read|edit|editFiles|create|createFile|search/codebase) ;;
    *) echo '{"continue":true}'; exit 0 ;;
esac

TARGET_PATH=$(echo "$INPUT" | jq -r '.tool_input.filePath // .tool_input.path // .tool_input.file_path // empty' 2>/dev/null)
if [ -z "$TARGET_PATH" ]; then
    echo '{"continue":true}'
    exit 0
fi

NORM_TARGET=$(echo "$TARGET_PATH" | tr '\\' '/')
NORM_CTX=$(echo "$COPILOT_CUSTOMER_CONTEXT" | tr '\\' '/')

# Only enforce when target path is inside a Customers/ subtree
if ! echo "$NORM_TARGET" | grep -qiE '/?Customers/'; then
    echo '{"continue":true}'
    exit 0
fi

# Extract the customer leaf (segment immediately after 'Customers') from both target and context.
# Path-segment equality (NOT substring) prevents false matches like context='Customers/HCA' allowing target='Customers/HCA Healthcare/...'.
extract_customer_segment() {
    local path="$1"
    local -a segments
    IFS='/' read -ra segments <<< "$path"
    local n=${#segments[@]}
    local i
    for ((i=0; i<n-1; i++)); do
        if [ "$(echo "${segments[$i]}" | tr '[:upper:]' '[:lower:]')" = "customers" ]; then
            printf '%s' "${segments[$i+1]}"
            return
        fi
    done
}

TARGET_CUSTOMER=$(extract_customer_segment "$NORM_TARGET")
CTX_CUSTOMER=$(extract_customer_segment "$NORM_CTX")
if [ -z "$CTX_CUSTOMER" ]; then
    CTX_CUSTOMER=$(basename "$NORM_CTX")
fi

# Exact (case-insensitive) match required — substring match would falsely allow e.g. 'HCA' vs 'HCA Healthcare'
if [ -n "$TARGET_CUSTOMER" ] && [ -n "$CTX_CUSTOMER" ]; then
    if [ "$(echo "$TARGET_CUSTOMER" | tr '[:upper:]' '[:lower:]')" = "$(echo "$CTX_CUSTOMER" | tr '[:upper:]' '[:lower:]')" ]; then
        echo '{"continue":true}'
        exit 0
    fi
fi

CTX_LEAF="$CTX_CUSTOMER"
REASON="Customer data isolation violation: active customer context is '$CTX_LEAF' but the requested file '$TARGET_PATH' is in a different customer folder. Each customer is a fully isolated engagement (NDA). Do NOT cross-reference customer folders for any reason."
# Escape quotes for JSON
REASON_ESC=$(echo "$REASON" | sed 's/"/\\"/g')
echo "{\"hookSpecificOutput\":{\"hookEventName\":\"PreToolUse\",\"permissionDecision\":\"deny\",\"permissionDecisionReason\":\"$REASON_ESC\"}}"
