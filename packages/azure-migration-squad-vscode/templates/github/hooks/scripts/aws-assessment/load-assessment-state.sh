#!/usr/bin/env bash
# Hook: SessionStart - Load assessment state so the agent resumes without re-discovery
set -uo pipefail

INPUT="$(cat)"

emit() {
  if command -v jq >/dev/null 2>&1; then
    jq -nc --arg c "$1" '{hookSpecificOutput:{hookEventName:"SessionStart",additionalContext:$c}}'
  else
    echo '{"continue":true}'
  fi
  exit 0
}

command -v jq >/dev/null 2>&1 || { echo '{"continue":true}'; exit 0; }

CWD="$(jq -r '.cwd // empty' <<<"$INPUT" 2>/dev/null)"
[[ -z "$CWD" ]] && CWD="$(pwd)"

REPORTS="$CWD/reports"
RAW="$REPORTS/raw"
STATUS="$REPORTS/Report-Status.md"
SCOPE="$RAW/_scope.json"

[[ -d "$REPORTS" ]] || emit "AWS Assessment: no reports/ folder found. No assessment has started. Begin with /phase0-setupandscope."

PARTS=()

if [[ -f "$SCOPE" ]]; then
  MODE="$(jq -r '.accountModel // empty' "$SCOPE" 2>/dev/null)"
  RCOUNT="$(jq -r '(.regions // []) | length' "$SCOPE" 2>/dev/null)"
  [[ -n "$MODE" ]] && PARTS+=("Mode: $MODE")
  [[ -n "$RCOUNT" && "$RCOUNT" != "0" ]] && PARTS+=("Regions in scope: $RCOUNT")
fi

ACCOUNTS=()
TOTAL=0
if [[ -d "$RAW" ]]; then
  while IFS= read -r dir; do
    acct="$(basename "$dir")"
    [[ "$acct" =~ ^[0-9]{12}$ ]] || continue
    phases=""
    [[ -f "$dir/_index.json" ]]              && phases="${phases}P1+"
    [[ -f "$dir/_summary.json" ]]            && phases="${phases}P2+"
    [[ -f "$dir/_inventory-enriched.json" ]] && phases="${phases}P3+"
    [[ -f "$dir/_edges.json" ]]              && phases="${phases}P4+"
    phases="${phases%+}"
    [[ -z "$phases" ]] && phases="started"

    items=""
    if [[ -f "$dir/_summary.json" ]]; then
      n="$(jq -r '.totalItems // empty' "$dir/_summary.json" 2>/dev/null)"
      if [[ -n "$n" && "$n" != "null" ]]; then
        items=" ($n items)"
        TOTAL=$((TOTAL + n))
      fi
    fi
    ACCOUNTS+=("${acct}[${phases}]${items}")
  done < <(find "$RAW" -maxdepth 1 -mindepth 1 -type d 2>/dev/null | sort)
fi

if [[ ${#ACCOUNTS[@]} -gt 0 ]]; then
  PARTS+=("Accounts scanned: ${#ACCOUNTS[@]} -> $(IFS='; '; echo "${ACCOUNTS[*]}")")
  [[ $TOTAL -gt 0 ]] && PARTS+=("Total items collected: $TOTAL")
else
  PARTS+=("No account data collected yet under reports/raw/.")
fi

GAPS=0
while IFS= read -r errfile; do
  n="$(jq -r '[.[] | select(.class=="coverage-gap")] | length' "$errfile" 2>/dev/null || echo 0)"
  GAPS=$((GAPS + ${n:-0}))
done < <(find "$RAW" -maxdepth 2 -name '_errors.json' 2>/dev/null)
[[ $GAPS -gt 0 ]] && PARTS+=("Coverage gaps recorded: $GAPS")

if [[ -f "$STATUS" ]]; then
  NEXT="$(awk '/^##[[:space:]]*Next Action/{flag=1;next} /^#/{flag=0} flag' "$STATUS" 2>/dev/null | tr '\n' ' ' | sed 's/  */ /g' | cut -c1-240)"
  [[ -n "${NEXT// }" ]] && PARTS+=("Next action (from Report-Status.md):${NEXT}")
fi

EXISTING=()
for f in AWS-Account-Assessment-Report.md AWS-Resource-Inventory.md AWS-Network-Topology.md \
         AWS-Dependency-Map.md AWS-Security-Findings.md AWS-Tagging-Governance.md \
         AWS-Cost-Analysis.md Azure-Migration-Readiness.md inventory.csv; do
  [[ -f "$REPORTS/$f" ]] && EXISTING+=("$f")
done
[[ ${#EXISTING[@]} -gt 0 ]] && PARTS+=("Reports present: $(IFS=', '; echo "${EXISTING[*]}")")

PARTS+=("Reminder: this agent is READ-ONLY. Reports must be regenerated from ALL folders under reports/raw/ whenever a new account is added.")

emit "AWS Assessment state -- $(IFS=' | '; echo "${PARTS[*]}")"
