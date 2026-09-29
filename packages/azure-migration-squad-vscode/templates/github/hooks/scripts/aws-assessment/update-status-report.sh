#!/usr/bin/env bash
# Hook: Stop - Refresh the assessment status footer with what is actually on disk
set -uo pipefail

INPUT="$(cat)"
ok() { echo '{"continue":true}'; exit 0; }

command -v jq >/dev/null 2>&1 || ok

CWD="$(jq -r '.cwd // empty' <<<"$INPUT" 2>/dev/null)"
[[ -z "$CWD" ]] && CWD="$(pwd)"

REPORTS="$CWD/reports"
RAW="$REPORTS/raw"
STATUS="$REPORTS/Report-Status.md"

[[ -f "$STATUS" ]] || ok

ROWS=""
TOTAL_ITEMS=0
TOTAL_GAPS=0
ACCOUNT_COUNT=0

if [[ -d "$RAW" ]]; then
  while IFS= read -r dir; do
    acct="$(basename "$dir")"
    [[ "$acct" =~ ^[0-9]{12}$ ]] || continue
    ACCOUNT_COUNT=$((ACCOUNT_COUNT + 1))

    p1="--"; p2="--"; p3="--"; p4="--"
    [[ -f "$dir/_index.json" ]]              && p1="OK"
    [[ -f "$dir/_summary.json" ]]            && p2="OK"
    [[ -f "$dir/_inventory-enriched.json" ]] && p3="OK"
    [[ -f "$dir/_edges.json" ]]              && p4="OK"

    items="-"; last="-"
    if [[ -f "$dir/_summary.json" ]]; then
      n="$(jq -r '.totalItems // empty' "$dir/_summary.json" 2>/dev/null)"
      if [[ -n "$n" && "$n" != "null" ]]; then items="$n"; TOTAL_ITEMS=$((TOTAL_ITEMS + n)); fi
      f="$(jq -r '.finishedAt // empty' "$dir/_summary.json" 2>/dev/null)"
      [[ -n "$f" && "$f" != "null" ]] && last="${f%T*} ${f#*T}"
    fi

    if [[ -f "$dir/_errors.json" ]]; then
      g="$(jq -r '[.[] | select(.class=="coverage-gap")] | length' "$dir/_errors.json" 2>/dev/null || echo 0)"
      TOTAL_GAPS=$((TOTAL_GAPS + ${g:-0}))
    fi

    ROWS+="| $acct | $p1 | $p2 | $p3 | $p4 | $items | $last |"$'\n'
  done < <(find "$RAW" -maxdepth 1 -mindepth 1 -type d 2>/dev/null | sort)
fi

REGION_COUNT=0
if [[ -d "$RAW" ]]; then
  REGION_COUNT="$(find "$RAW" -mindepth 2 -maxdepth 2 -type d ! -name global 2>/dev/null \
    | xargs -r -n1 basename | sort -u | wc -l | tr -d ' ')"
fi

MARKER='<!-- AUTO-GENERATED: refreshed at session end from reports/raw/. Do not edit by hand. -->'
TMP="$(mktemp)"
awk -v m="$MARKER" 'index($0, m) {exit} {print}' "$STATUS" > "$TMP"

{
  echo ""
  echo "$MARKER"
  echo "## Collected Data (auto-refreshed)"
  echo ""
  echo "_Last refreshed: $(date -u '+%Y-%m-%d %H:%M') UTC_"
  echo ""
  if [[ -n "$ROWS" ]]; then
    echo "| Account | P1 | P2 | P3 | P4 | Items | Last scanned |"
    echo "|---------|----|----|----|----|-------|--------------|"
    printf '%s' "$ROWS"
    echo ""
    echo "- Accounts with data: **$ACCOUNT_COUNT**"
    echo "- Distinct regions with data: **$REGION_COUNT**"
    echo "- Total items collected: **$TOTAL_ITEMS**"
    echo "- Coverage gaps recorded: **$TOTAL_GAPS**"
  else
    echo "_No account folders found under \`reports/raw/\`._"
  fi
  echo ""
} >> "$TMP"

mv "$TMP" "$STATUS"
ok
