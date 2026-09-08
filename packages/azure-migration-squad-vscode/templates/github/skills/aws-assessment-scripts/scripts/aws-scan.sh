#!/usr/bin/env bash
# Read-only AWS multi-region resource sweep for account assessment.
#
# Collects inventory data from the currently authenticated AWS account across all
# enabled regions and writes normalized JSON to reports/raw/<account-id>/<region>/.
#
# Every operation is read-only. The script refuses to execute any AWS CLI verb that
# is not in the allow-list, so it cannot create, modify or delete anything.
#
# Requires: bash 4+, aws cli v2, jq

set -uo pipefail

PHASE="all"
OUTPUT_ROOT="./reports/raw"
REGIONS=""
AWS_PROFILE_ARG=""
CONCURRENCY=5
FORCE=0
DRY_RUN=0

usage() {
  cat <<'EOF'
Usage: aws-scan.sh [options]

  --phase <discovery|inventory|all>   Default: all
  --output-root <path>                Default: ./reports/raw
  --regions "<r1 r2 ...>"             Default: auto-detect enabled regions
  --profile <name>                    AWS named profile
  --concurrency <n>                   Regions in parallel (default 5)
  --force                             Re-collect files that already exist
  --dry-run                           Print the plan, collect nothing
  -h, --help                          Show this help
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --phase)        PHASE="$2"; shift 2 ;;
    --output-root)  OUTPUT_ROOT="$2"; shift 2 ;;
    --regions)      REGIONS="$2"; shift 2 ;;
    --profile)      AWS_PROFILE_ARG="--profile $2"; shift 2 ;;
    --concurrency)  CONCURRENCY="$2"; shift 2 ;;
    --force)        FORCE=1; shift ;;
    --dry-run)      DRY_RUN=1; shift ;;
    -h|--help)      usage; exit 0 ;;
    *) echo "Unknown option: $1" >&2; usage; exit 1 ;;
  esac
done

command -v aws >/dev/null 2>&1 || { echo "aws CLI not found" >&2; exit 1; }
command -v jq  >/dev/null 2>&1 || { echo "jq not found" >&2; exit 1; }

export AWS_RETRY_MODE=adaptive
export AWS_MAX_ATTEMPTS=10

ALLOWED_VERBS='^(describe|list|get|lookup|search|select|batch-get|generate-credential-report)'

# ---------------------------------------------------------------------------
# Operation catalog: "<file>|<service>|<cli args...>"
# ---------------------------------------------------------------------------
GLOBAL_OPS=(
  "sts-caller-identity|sts|sts get-caller-identity"
  "iam-users|iam|iam list-users"
  "iam-roles|iam|iam list-roles"
  "iam-groups|iam|iam list-groups"
  "iam-policies-local|iam|iam list-policies --scope Local"
  "iam-account-summary|iam|iam get-account-summary"
  "iam-account-aliases|iam|iam list-account-aliases"
  "iam-saml-providers|iam|iam list-saml-providers"
  "iam-oidc-providers|iam|iam list-open-id-connect-providers"
  "iam-authorization-details|iam|iam get-account-authorization-details"
  "s3-buckets|s3|s3api list-buckets"
  "route53-hosted-zones|route53|route53 list-hosted-zones"
  "route53-health-checks|route53|route53 list-health-checks"
  "cloudfront-distributions|cloudfront|cloudfront list-distributions"
  "organizations-describe|organizations|organizations describe-organization"
  "organizations-accounts|organizations|organizations list-accounts"
  "organizations-roots|organizations|organizations list-roots"
)

DISCOVERY_OPS=(
  "tagging-resources|tagging|resourcegroupstaggingapi get-resources"
  "config-recorders|config|configservice describe-configuration-recorders"
  "config-aggregators|config|configservice describe-configuration-aggregators"
)

INVENTORY_OPS=(
  # networking
  "ec2-vpcs|ec2|ec2 describe-vpcs"
  "ec2-subnets|ec2|ec2 describe-subnets"
  "ec2-route-tables|ec2|ec2 describe-route-tables"
  "ec2-internet-gateways|ec2|ec2 describe-internet-gateways"
  "ec2-nat-gateways|ec2|ec2 describe-nat-gateways"
  "ec2-vpc-endpoints|ec2|ec2 describe-vpc-endpoints"
  "ec2-vpc-peering|ec2|ec2 describe-vpc-peering-connections"
  "ec2-security-groups|ec2|ec2 describe-security-groups"
  "ec2-network-acls|ec2|ec2 describe-network-acls"
  "ec2-network-interfaces|ec2|ec2 describe-network-interfaces"
  "ec2-addresses|ec2|ec2 describe-addresses"
  "ec2-flow-logs|ec2|ec2 describe-flow-logs"
  "ec2-transit-gateways|ec2|ec2 describe-transit-gateways"
  "ec2-tgw-attachments|ec2|ec2 describe-transit-gateway-attachments"
  "ec2-vpn-connections|ec2|ec2 describe-vpn-connections"
  "directconnect-connections|directconnect|directconnect describe-connections"
  "elbv2-load-balancers|elbv2|elbv2 describe-load-balancers"
  "elbv2-target-groups|elbv2|elbv2 describe-target-groups"
  "elb-load-balancers|elb|elb describe-load-balancers"
  "wafv2-web-acls-regional|wafv2|wafv2 list-web-acls --scope REGIONAL"
  # compute
  "ec2-instances|ec2|ec2 describe-instances"
  "ec2-volumes|ec2|ec2 describe-volumes"
  "ec2-snapshots|ec2|ec2 describe-snapshots --owner-ids self"
  "ec2-images|ec2|ec2 describe-images --owners self"
  "ec2-key-pairs|ec2|ec2 describe-key-pairs"
  "ec2-launch-templates|ec2|ec2 describe-launch-templates"
  "ec2-reserved-instances|ec2|ec2 describe-reserved-instances"
  "autoscaling-groups|autoscaling|autoscaling describe-auto-scaling-groups"
  "beanstalk-applications|elasticbeanstalk|elasticbeanstalk describe-applications"
  "beanstalk-environments|elasticbeanstalk|elasticbeanstalk describe-environments"
  "batch-compute-environments|batch|batch describe-compute-environments"
  "apprunner-services|apprunner|apprunner list-services"
  "lightsail-instances|lightsail|lightsail get-instances"
  "ssm-instance-information|ssm|ssm describe-instance-information"
  # containers
  "ecs-clusters|ecs|ecs list-clusters"
  "ecs-task-definitions|ecs|ecs list-task-definitions --status ACTIVE"
  "eks-clusters|eks|eks list-clusters"
  "ecr-repositories|ecr|ecr describe-repositories"
  # serverless
  "lambda-functions|lambda|lambda list-functions"
  "lambda-layers|lambda|lambda list-layers"
  "lambda-event-source-maps|lambda|lambda list-event-source-mappings"
  "stepfunctions-machines|stepfunctions|stepfunctions list-state-machines"
  "events-buses|events|events list-event-buses"
  "events-rules|events|events list-rules"
  "sqs-queues|sqs|sqs list-queues"
  "sns-topics|sns|sns list-topics"
  "sns-subscriptions|sns|sns list-subscriptions"
  "apigateway-rest-apis|apigateway|apigateway get-rest-apis"
  "apigatewayv2-apis|apigatewayv2|apigatewayv2 get-apis"
  "appsync-graphql-apis|appsync|appsync list-graphql-apis"
  # databases
  "rds-db-instances|rds|rds describe-db-instances"
  "rds-db-clusters|rds|rds describe-db-clusters"
  "rds-global-clusters|rds|rds describe-global-clusters"
  "rds-db-snapshots|rds|rds describe-db-snapshots --snapshot-type manual"
  "rds-subnet-groups|rds|rds describe-db-subnet-groups"
  "rds-proxies|rds|rds describe-db-proxies"
  "dynamodb-tables|dynamodb|dynamodb list-tables"
  "elasticache-clusters|elasticache|elasticache describe-cache-clusters --show-cache-node-info"
  "elasticache-repl-groups|elasticache|elasticache describe-replication-groups"
  "memorydb-clusters|memorydb|memorydb describe-clusters"
  "docdb-clusters|docdb|docdb describe-db-clusters"
  "neptune-clusters|neptune|neptune describe-db-clusters"
  "redshift-clusters|redshift|redshift describe-clusters"
  "redshift-serverless-wg|redshift|redshift-serverless list-workgroups"
  "opensearch-domains|opensearch|opensearch list-domain-names"
  # storage
  "efs-file-systems|efs|efs describe-file-systems"
  "fsx-file-systems|fsx|fsx describe-file-systems"
  "backup-plans|backup|backup list-backup-plans"
  "backup-vaults|backup|backup list-backup-vaults"
  "backup-protected-resources|backup|backup list-protected-resources"
  # identity & security
  "kms-keys|kms|kms list-keys"
  "kms-aliases|kms|kms list-aliases"
  "secretsmanager-secrets|secretsmanager|secretsmanager list-secrets"
  "ssm-parameters|ssm|ssm describe-parameters"
  "acm-certificates|acm|acm list-certificates"
  "cognito-user-pools|cognito|cognito-idp list-user-pools --max-results 60"
  "guardduty-detectors|guardduty|guardduty list-detectors"
  "securityhub-standards|securityhub|securityhub get-enabled-standards"
  "config-rules|config|configservice describe-config-rules"
  "accessanalyzer-analyzers|accessanalyzer|accessanalyzer list-analyzers"
  "ram-resources-self|ram|ram list-resources --resource-owner SELF"
  "ram-resources-other|ram|ram list-resources --resource-owner OTHER-ACCOUNTS"
  # data & integration
  "kinesis-streams|kinesis|kinesis list-streams"
  "firehose-streams|firehose|firehose list-delivery-streams"
  "msk-clusters|kafka|kafka list-clusters-v2"
  "glue-jobs|glue|glue get-jobs"
  "glue-crawlers|glue|glue get-crawlers"
  "athena-workgroups|athena|athena list-work-groups"
  "emr-clusters|emr|emr list-clusters --cluster-states RUNNING WAITING STARTING"
  # observability
  "logs-log-groups|logs|logs describe-log-groups"
  "cloudwatch-alarms|cloudwatch|cloudwatch describe-alarms"
  "cloudwatch-dashboards|cloudwatch|cloudwatch list-dashboards"
  "cloudtrail-trails|cloudtrail|cloudtrail describe-trails"
  # devops & iac
  "cloudformation-stacks|cloudformation|cloudformation describe-stacks"
  "cloudformation-stack-sets|cloudformation|cloudformation list-stack-sets"
  "codecommit-repositories|codecommit|codecommit list-repositories"
  "codebuild-projects|codebuild|codebuild list-projects"
  "codepipeline-pipelines|codepipeline|codepipeline list-pipelines"
  "codedeploy-applications|codedeploy|codedeploy list-applications"
  # other
  "ses-email-identities|sesv2|sesv2 list-email-identities"
  "amplify-apps|amplify|amplify list-apps"
  "mq-brokers|mq|mq list-brokers"
  "transfer-servers|transfer|transfer list-servers"
  "sagemaker-endpoints|sagemaker|sagemaker list-endpoints"
  "workspaces|workspaces|workspaces describe-workspaces"
)

# ---------------------------------------------------------------------------
# Read-only guard
# ---------------------------------------------------------------------------
assert_read_only() {
  local entry="$1"
  local cli_args verb
  cli_args="${entry#*|*|}"
  verb="$(awk '{print $2}' <<<"$cli_args")"
  if [[ ! "$verb" =~ $ALLOWED_VERBS ]]; then
    echo "BLOCKED: '$cli_args' is not a read-only operation." >&2
    exit 1
  fi
}
for e in "${GLOBAL_OPS[@]}" "${DISCOVERY_OPS[@]}" "${INVENTORY_OPS[@]}"; do assert_read_only "$e"; done

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
classify_error() {
  local msg="$1"
  if   grep -qiE 'AccessDenied|UnauthorizedOperation|not authorized|AuthorizationError' <<<"$msg"; then echo "coverage-gap"
  elif grep -qiE 'OptInRequired|SubscriptionRequired|is not subscribed'                 <<<"$msg"; then echo "not-in-use"
  elif grep -qiE 'Could not connect to the endpoint|EndpointConnectionError|UnknownOperation|InvalidAction' <<<"$msg"; then echo "not-available"
  elif grep -qiE 'ExpiredToken|InvalidClientTokenId|TokenRefreshRequired|SSO session'   <<<"$msg"; then echo "auth"
  elif grep -qiE 'ResourceNotFound|NoSuch|NotFoundException'                            <<<"$msg"; then echo "not-in-use"
  elif grep -qiE 'Throttling|RequestLimitExceeded|TooManyRequests|Rate exceeded|SlowDown' <<<"$msg"; then echo "throttled-exhausted"
  else echo "other"; fi
}

# run_op <file> <service> <cli-args> <region|global> <account-root> <account-id> <cli-version>
run_op() {
  local fname="$1" service="$2" cli_args="$3" region="$4" root="$5" acct="$6" cliv="$7"
  local outfile region_flag attempt=1 max=6 raw rc cls count

  outfile="$root/$region/$fname.json"
  [[ -f "$outfile" && $FORCE -eq 0 ]] && return 0
  mkdir -p "$root/$region"

  region_flag=""
  [[ "$region" != "global" ]] && region_flag="--region $region"

  while :; do
    # shellcheck disable=SC2086
    raw="$(aws $cli_args $region_flag $AWS_PROFILE_ARG --output json --no-cli-pager 2>&1)"
    rc=$?
    if [[ $rc -eq 0 ]]; then break; fi

    if grep -qiE 'Throttling|RequestLimitExceeded|TooManyRequests|Rate exceeded|SlowDown' <<<"$raw" && [[ $attempt -lt $max ]]; then
      sleep "$(awk -v a="$attempt" 'BEGIN{srand(); print (2^a)*0.5 + rand()*0.4}')"
      attempt=$((attempt + 1))
      continue
    fi

    cls="$(classify_error "$raw")"
    printf '%s\n' "$(jq -nc --arg r "$region" --arg s "$service" --arg o "$cli_args" --arg c "$cls" --arg m "$raw" \
      '{region:$r,service:$s,operation:$o,class:$c,message:$m}')" >> "$root/_errors.ndjson"
    return 0
  done

  count="$(jq -r '[ to_entries[] | select(.key|test("Token|Marker|ResponseMetadata")|not) | select(.value|type=="array") | (.value|length) ] | add // 0' <<<"$raw" 2>/dev/null || echo 0)"

  jq -n --argjson d "$raw" \
        --arg acct "$acct" --arg region "$region" --arg service "$service" \
        --arg op "$cli_args" --arg ts "$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
        --argjson count "${count:-0}" --arg cliv "$cliv" \
    '{_meta:{accountId:$acct,region:$region,service:$service,operation:$op,collectedAt:$ts,itemCount:$count,cliVersion:$cliv},data:$d}' \
    > "$outfile"

  printf '%s\n' "$(jq -nc --arg r "$region" --arg s "$service" --arg f "$fname" --argjson c "${count:-0}" \
    '{region:$r,service:$s,file:$f,count:$c}')" >> "$root/_summary.ndjson"
}
export -f run_op classify_error

# ---------------------------------------------------------------------------
# Identity
# ---------------------------------------------------------------------------
echo "AWS Account Assessment — read-only sweep"
printf '%.0s-' {1..60}; echo

# shellcheck disable=SC2086
IDENTITY="$(aws sts get-caller-identity $AWS_PROFILE_ARG --output json --no-cli-pager 2>&1)" || {
  echo "Cannot determine caller identity: $IDENTITY" >&2; exit 1; }

ACCOUNT_ID="$(jq -r '.Account' <<<"$IDENTITY")"
CALLER_ARN="$(jq -r '.Arn' <<<"$IDENTITY")"
CLI_VERSION="$(aws --version 2>&1)"

echo "Account : $ACCOUNT_ID"
echo "Caller  : $CALLER_ARN"
echo "CLI     : $CLI_VERSION"

# ---------------------------------------------------------------------------
# Regions
# ---------------------------------------------------------------------------
if [[ -z "$REGIONS" ]]; then
  # shellcheck disable=SC2086
  REGIONS="$(aws account list-regions --region-opt-status-contains ENABLED ENABLED_BY_DEFAULT \
    --region us-east-1 $AWS_PROFILE_ARG --output json --no-cli-pager 2>/dev/null \
    | jq -r '.Regions[].RegionName' | sort | tr '\n' ' ')"
fi
if [[ -z "${REGIONS// }" ]]; then
  # shellcheck disable=SC2086
  REGIONS="$(aws ec2 describe-regions --all-regions --region us-east-1 $AWS_PROFILE_ARG \
    --output json --no-cli-pager \
    | jq -r '.Regions[] | select(.OptInStatus=="opt-in-not-required" or .OptInStatus=="opted-in") | .RegionName' \
    | sort | tr '\n' ' ')"
fi
[[ -z "${REGIONS// }" ]] && { echo "Cannot enumerate regions" >&2; exit 1; }

read -r -a REGION_ARR <<<"$REGIONS"

case "$PHASE" in
  discovery) OPS=("${DISCOVERY_OPS[@]}") ;;
  inventory) OPS=("${INVENTORY_OPS[@]}") ;;
  all)       OPS=("${DISCOVERY_OPS[@]}" "${INVENTORY_OPS[@]}") ;;
  *) echo "Invalid --phase: $PHASE" >&2; exit 1 ;;
esac

echo "Regions : ${#REGION_ARR[@]} -> $REGIONS"
echo "Phase   : $PHASE (${#OPS[@]} regional ops x ${#REGION_ARR[@]} regions + ${#GLOBAL_OPS[@]} global)"
echo "Output  : $OUTPUT_ROOT/$ACCOUNT_ID"
printf '%.0s-' {1..60}; echo

if [[ $DRY_RUN -eq 1 ]]; then
  echo "DRY RUN — no data will be collected."
  for e in "${OPS[@]}";        do echo "  regional: aws ${e#*|*|}"; done
  for e in "${GLOBAL_OPS[@]}"; do echo "  global  : aws ${e#*|*|}"; done
  exit 0
fi

ACCOUNT_ROOT="$OUTPUT_ROOT/$ACCOUNT_ID"
mkdir -p "$ACCOUNT_ROOT"
: > "$ACCOUNT_ROOT/_summary.ndjson"
: > "$ACCOUNT_ROOT/_errors.ndjson"
STARTED=$(date -u +%s)

export FORCE AWS_PROFILE_ARG

# ---------------------------------------------------------------------------
# Global operations
# ---------------------------------------------------------------------------
echo "[global] collecting ${#GLOBAL_OPS[@]} operations..."
for entry in "${GLOBAL_OPS[@]}"; do
  IFS='|' read -r fname service cli_args <<<"$entry"
  run_op "$fname" "$service" "$cli_args" "global" "$ACCOUNT_ROOT" "$ACCOUNT_ID" "$CLI_VERSION"
done

# ---------------------------------------------------------------------------
# Regional operations (parallel by region)
# ---------------------------------------------------------------------------
# Bash cannot export arrays, so the catalog is serialized and rebuilt in each child shell.
OPS_SERIALIZED="$(printf '%s\n' "${OPS[@]}")"
export OPS_SERIALIZED ACCOUNT_ROOT ACCOUNT_ID CLI_VERSION

printf '%s\n' "${REGION_ARR[@]}" | xargs -P "$CONCURRENCY" -I {} bash -c '
  region="$1"
  mapfile -t OPS <<< "$OPS_SERIALIZED"
  for entry in "${OPS[@]}"; do
    IFS="|" read -r fname service cli_args <<< "$entry"
    run_op "$fname" "$service" "$cli_args" "$region" "$ACCOUNT_ROOT" "$ACCOUNT_ID" "$CLI_VERSION"
  done
  echo "[$region] done"
' _ {}

# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------
ELAPSED=$(( $(date -u +%s) - STARTED ))

TOTAL_ITEMS="$(jq -s 'map(.count) | add // 0' "$ACCOUNT_ROOT/_summary.ndjson")"
BY_REGION="$(jq -s 'group_by(.region) | map({region: .[0].region, items: (map(.count)|add), operations: length}) | sort_by(-.items)' "$ACCOUNT_ROOT/_summary.ndjson")"
BY_SERVICE="$(jq -s 'group_by(.service) | map({service: .[0].service, items: (map(.count)|add)}) | sort_by(-.items)' "$ACCOUNT_ROOT/_summary.ndjson")"
EMPTY_REGIONS="$(jq -r --argjson br "$BY_REGION" -n '$br | map(select(.items==0) | .region)')"
ERROR_COUNT="$(wc -l < "$ACCOUNT_ROOT/_errors.ndjson" | tr -d ' ')"
COVERAGE_GAPS="$(jq -s 'map(select(.class=="coverage-gap")) | length' "$ACCOUNT_ROOT/_errors.ndjson")"

jq -n \
  --arg acct "$ACCOUNT_ID" --arg arn "$CALLER_ARN" --arg phase "$PHASE" \
  --arg finished "$(date -u +%Y-%m-%dT%H:%M:%SZ)" --argjson elapsed "$ELAPSED" \
  --argjson regions "$(printf '%s\n' "${REGION_ARR[@]}" | jq -R . | jq -s .)" \
  --argjson total "$TOTAL_ITEMS" --argjson byRegion "$BY_REGION" --argjson byService "$BY_SERVICE" \
  --argjson empty "$EMPTY_REGIONS" --argjson errCount "$ERROR_COUNT" --argjson gaps "$COVERAGE_GAPS" \
  --arg cliv "$CLI_VERSION" \
  '{accountId:$acct,callerArn:$arn,phase:$phase,finishedAt:$finished,elapsedSecs:$elapsed,
    regionsScanned:$regions,totalItems:$total,byRegion:$byRegion,byService:$byService,
    emptyRegions:$empty,errorCount:$errCount,coverageGaps:$gaps,cliVersion:$cliv}' \
  > "$ACCOUNT_ROOT/_summary.json"

jq -s '.' "$ACCOUNT_ROOT/_errors.ndjson" > "$ACCOUNT_ROOT/_errors.json"
rm -f "$ACCOUNT_ROOT/_summary.ndjson" "$ACCOUNT_ROOT/_errors.ndjson"

printf '%.0s-' {1..60}; echo
echo "Done in $((ELAPSED / 60)) min $((ELAPSED % 60)) s"
echo "Total items      : $TOTAL_ITEMS"
echo "Coverage gaps    : $COVERAGE_GAPS"
echo "Summary          : $ACCOUNT_ROOT/_summary.json"
echo "Errors           : $ACCOUNT_ROOT/_errors.json"
