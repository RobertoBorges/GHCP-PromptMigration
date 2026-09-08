#!/usr/bin/env bash
# Hook: PreToolUse - Enforce read-only AWS CLI usage
# Denies any AWS CLI invocation whose operation verb is not read-only.
set -uo pipefail

INPUT="$(cat)"

allow() { echo '{"continue":true}'; exit 0; }

deny() {
  local reason="$1"
  if command -v jq >/dev/null 2>&1; then
    jq -nc --arg r "$reason" \
      '{hookSpecificOutput:{hookEventName:"PreToolUse",permissionDecision:"deny",permissionDecisionReason:$r}}'
  else
    printf '{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"deny","permissionDecisionReason":"%s"}}\n' "$reason"
  fi
  exit 0
}

command -v jq >/dev/null 2>&1 || allow

TOOL_NAME="$(jq -r '.tool_name // empty' <<<"$INPUT" 2>/dev/null)" || allow
case "$TOOL_NAME" in
  runInTerminal|runTerminalCommand|terminal|awaitTerminal) ;;
  *) allow ;;
esac

CMD="$(jq -r '.tool_input.command // .tool_input.input // empty' <<<"$INPUT" 2>/dev/null)"
[[ -z "$CMD" ]] && allow

# --- 1. Generic destructive commands -------------------------------------------------
DESTRUCTIVE=(
  'rm[[:space:]]+-rf[[:space:]]+/'
  'terraform[[:space:]]+(destroy|apply)'
  'kubectl[[:space:]]+(delete|apply|patch|scale|drain)'
  'DROP[[:space:]]+(TABLE|DATABASE|SCHEMA)'
  'TRUNCATE[[:space:]]+TABLE'
  'git[[:space:]]+push[[:space:]]+.*(--force|-f)[[:space:]]'
)
for p in "${DESTRUCTIVE[@]}"; do
  grep -qiE "$p" <<<"$CMD" && \
    deny "Destructive command blocked. The AWS Account Assessment Agent is read-only. Run this manually if it is genuinely intended."
done

# --- 2. AWS CLI read-only enforcement ------------------------------------------------
ALLOWED_VERB='^(describe|list|get|lookup|search|select|batch-get|generate-credential-report|help)'

while read -r service operation; do
  [[ -z "${operation:-}" ]] && continue
  [[ "$operation" == -* ]] && continue
  [[ "$service" == "s3" && "$operation" == "ls" ]] && continue
  if [[ ! "$operation" =~ $ALLOWED_VERB ]]; then
    deny "READ-ONLY VIOLATION: 'aws $service $operation' is not a read-only operation. This agent may only run describe-*, list-*, get-*, lookup-*, search-*, select-* and batch-get-* operations. If a mutating action is genuinely required, run it yourself outside this agent."
  fi
done < <(grep -oiE '\baws[[:space:]]+[a-z0-9-]+[[:space:]]+[a-z0-9-]+' <<<"$CMD" | awk '{print $2, $3}')

# --- 3. Explicitly forbidden AWS operations even though the verb looks read-only ------
grep -qiE 'aws[[:space:]]+secretsmanager[[:space:]]+get-secret-value' <<<"$CMD" && \
  deny "BLOCKED: Reading secret values is forbidden. Inventory secrets by name/ARN only."

grep -qiE 'aws[[:space:]]+ssm[[:space:]]+get-parameters?(-by-path)?.*--with-decryption' <<<"$CMD" && \
  deny "BLOCKED: Reading decrypted SSM parameters is forbidden. Inventory parameter names/types only."

grep -qiE 'aws[[:space:]]+kms[[:space:]]+(decrypt|generate-data-key)' <<<"$CMD" && \
  deny "BLOCKED: Producing plaintext key material is forbidden."

grep -qiE 'aws[[:space:]]+configure[[:space:]]+set' <<<"$CMD" && \
  deny "BLOCKED: Modifying local AWS configuration is out of scope for this agent."

grep -qiE 'aws[[:space:]]+s3[[:space:]]+(rm|rb|mv|cp|sync)[[:space:]]' <<<"$CMD" && \
  deny "BLOCKED: S3 data operations are forbidden. Use s3api list/get metadata operations only."

grep -qiE 'aws[[:space:]]+cloudformation[[:space:]]+detect-stack-drift' <<<"$CMD" && \
  deny "BLOCKED: detect-stack-drift starts a job. Use describe-stack-drift-detection-status to read an existing result."

grep -qiE 'aws[[:space:]]+dynamodb[[:space:]]+(scan|query)[[:space:]]' <<<"$CMD" && \
  deny "BLOCKED: Reading table data is out of scope. Use describe-table for metadata."

allow
