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
# Terminal tools are named differently per surface: VS Code uses runInTerminal /
# awaitTerminal, Copilot CLI uses bash / powershell / shell, and toolset-qualified
# forms appear as execute/<tool>. A name this list misses means the read-only
# guarantee silently does not hold on that surface.
case "$TOOL_NAME" in
  runInTerminal|runTerminalCommand|terminal|awaitTerminal|runCommands) ;;
  execute|execute/runInTerminal|execute/awaitTerminal|execute/runCommands) ;;
  bash|shell|powershell|pwsh|cmd) ;;
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
# Walk each 'aws ...' invocation token by token. Global flags must be skipped before the
# service/operation pair can be read: matching the first three bare words instead reads
# 'aws --profile prod' as service='--profile', operation='prod' and denies a legitimate
# read-only command.
VALUE_FLAGS=" --profile --region --output --endpoint-url --query --ca-bundle --color --cli-read-timeout --cli-connect-timeout --cli-binary-format "
ALLOWED_VERB='^(describe|list|get|lookup|search|select|batch-get|generate-credential-report|help)'

check_aws_invocation() {
  # shellcheck disable=SC2206
  local -a tok=($1)
  local n=${#tok[@]}
  local i=0
  while [ "$i" -lt "$n" ]; do
    if [ "$(echo "${tok[$i]}" | tr '[:upper:]' '[:lower:]')" != "aws" ]; then
      i=$((i+1)); continue
    fi

    local j=$((i+1))
    while [ "$j" -lt "$n" ]; do
      case "${tok[$j]}" in
        *=*) case "${tok[$j]}" in -*) j=$((j+1)); continue ;; esac ;;
        -*)
          if [ "${VALUE_FLAGS#* ${tok[$j]} }" != "$VALUE_FLAGS" ]; then
            j=$((j+2)); continue
          fi
          j=$((j+1)); continue
          ;;
      esac
      break
    done

    if [ $((j+1)) -lt "$n" ]; then
      local service="${tok[$j]}"
      local operation="${tok[$((j+1))]}"
      case "$operation" in -*) i=$((i+1)); continue ;; esac
      if [ "$service" = "s3" ] && [ "$operation" = "ls" ]; then i=$((i+1)); continue; fi
      if [[ ! "$operation" =~ $ALLOWED_VERB ]]; then
        deny "READ-ONLY VIOLATION: 'aws $service $operation' is not a read-only operation. This agent may only run describe-*, list-*, get-*, lookup-*, search-*, select-* and batch-get-* operations. If a mutating action is genuinely required, run it yourself outside this agent."
      fi
    fi
    i=$((i+1))
  done
}

check_aws_invocation "$CMD"

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
