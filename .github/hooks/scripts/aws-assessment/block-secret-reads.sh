#!/usr/bin/env bash
# Hook: PreToolUse - Prevent credentials and secret material from being written to disk
# Scans file-edit payloads for AWS credentials, tokens and private keys.
set -uo pipefail

INPUT="$(cat)"

allow() { echo '{"continue":true}'; exit 0; }

deny() {
  local reason="$1"
  jq -nc --arg r "$reason" \
    '{hookSpecificOutput:{hookEventName:"PreToolUse",permissionDecision:"deny",permissionDecisionReason:$r}}'
  exit 0
}

command -v jq >/dev/null 2>&1 || allow

TOOL_NAME="$(jq -r '.tool_name // empty' <<<"$INPUT" 2>/dev/null)" || allow
case "$TOOL_NAME" in
  createFile|editFiles|applyPatch|insertEdit|replaceString|multiReplaceString) ;;
  *) allow ;;
esac

PAYLOAD="$(jq -r '[.tool_input.content, .tool_input.newString, .tool_input.code, .tool_input.text, .tool_input.patch] | map(select(. != null)) | join("\n")' <<<"$INPUT" 2>/dev/null)"
[[ -z "$PAYLOAD" ]] && allow

check() {
  local name="$1" pattern="$2"
  if grep -qEi "$pattern" <<<"$PAYLOAD"; then
    deny "Secret material detected in the content being written ($name). Assessment artifacts must never contain credentials, tokens or private keys. Record the resource identity (name/ARN) instead of its content."
  fi
}

check "AWS access key ID"       '\b(AKIA|ASIA|ABIA|ACCA)[0-9A-Z]{16}\b'
check "AWS secret access key"   '(aws_)?secret_?access_?key[[:space:]]*[:=][[:space:]]*"?[A-Za-z0-9/+=]{40}'
check "AWS session token"       '(aws_)?session_?token[[:space:]]*[:=][[:space:]]*"?[A-Za-z0-9/+=]{100,}'
check "Private key block"       '-----BEGIN (RSA |EC |OPENSSH |PGP )?PRIVATE KEY-----'
check "Generic password assign" '(password|passwd|pwd)[[:space:]]*[:=][[:space:]]*"[^"[:space:]]{8,}"'
check "DB connection string"    '(mongodb(\+srv)?|postgres(ql)?|mysql|redis|amqp)://[^:[:space:]]+:[^@[:space:]]+@'
check "Bearer token"            'authorization[[:space:]]*[:=][[:space:]]*"?bearer[[:space:]]+[A-Za-z0-9._-]{20,}'

allow
