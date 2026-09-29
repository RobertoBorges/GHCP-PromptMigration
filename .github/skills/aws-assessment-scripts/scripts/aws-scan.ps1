#Requires -Version 7.0
<#
.SYNOPSIS
    Read-only AWS multi-region resource sweep for account assessment.

.DESCRIPTION
    Collects inventory data from the currently authenticated AWS account across all
    enabled regions and writes normalized JSON to reports/raw/<account-id>/<region>/.

    Every operation is read-only. The script refuses to execute any AWS CLI verb that
    is not in the allow-list, so it cannot create, modify or delete anything.

.EXAMPLE
    pwsh ./aws-scan.ps1
.EXAMPLE
    pwsh ./aws-scan.ps1 -Phase discovery -AwsProfile prod-account
.EXAMPLE
    pwsh ./aws-scan.ps1 -Regions us-east-1,sa-east-1 -Concurrency 8 -Force
#>
[CmdletBinding()]
param(
    [ValidateSet('discovery', 'inventory', 'all')]
    [string]$Phase = 'all',

    [string]$OutputRoot = './reports/raw',

    [string[]]$Regions,

    [string]$AwsProfile,

    [ValidateRange(1, 20)]
    [int]$Concurrency = 5,

    [switch]$Force,

    [switch]$DryRun
)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

# Adaptive retries in the CLI itself, on top of the script-level backoff.
$env:AWS_RETRY_MODE = 'adaptive'
$env:AWS_MAX_ATTEMPTS = '10'

# ---------------------------------------------------------------------------
# Read-only guard
# ---------------------------------------------------------------------------
$AllowedVerbPattern = '^(describe|list|get|lookup|search|select|batch-get|generate-credential-report)'

function Assert-ReadOnly {
    param([string[]]$Args)
    $operation = $Args[1]
    if ($operation -notmatch $AllowedVerbPattern) {
        throw "BLOCKED: '$($Args[0]) $operation' is not a read-only operation. This script only executes describe/list/get/lookup/search/select verbs."
    }
}

# ---------------------------------------------------------------------------
# Operation catalog
# ---------------------------------------------------------------------------
# f = output file name, s = service label, a = AWS CLI argument array
$GlobalOps = @(
    @{ f = 'sts-caller-identity';        s = 'sts';           a = @('sts', 'get-caller-identity') }
    @{ f = 'iam-users';                  s = 'iam';           a = @('iam', 'list-users') }
    @{ f = 'iam-roles';                  s = 'iam';           a = @('iam', 'list-roles') }
    @{ f = 'iam-groups';                 s = 'iam';           a = @('iam', 'list-groups') }
    @{ f = 'iam-policies-local';         s = 'iam';           a = @('iam', 'list-policies', '--scope', 'Local') }
    @{ f = 'iam-account-summary';        s = 'iam';           a = @('iam', 'get-account-summary') }
    @{ f = 'iam-account-aliases';        s = 'iam';           a = @('iam', 'list-account-aliases') }
    @{ f = 'iam-saml-providers';         s = 'iam';           a = @('iam', 'list-saml-providers') }
    @{ f = 'iam-oidc-providers';         s = 'iam';           a = @('iam', 'list-open-id-connect-providers') }
    @{ f = 'iam-authorization-details';  s = 'iam';           a = @('iam', 'get-account-authorization-details') }
    @{ f = 's3-buckets';                 s = 's3';            a = @('s3api', 'list-buckets') }
    @{ f = 'route53-hosted-zones';       s = 'route53';       a = @('route53', 'list-hosted-zones') }
    @{ f = 'route53-health-checks';      s = 'route53';       a = @('route53', 'list-health-checks') }
    @{ f = 'cloudfront-distributions';   s = 'cloudfront';    a = @('cloudfront', 'list-distributions') }
    @{ f = 'organizations-describe';     s = 'organizations'; a = @('organizations', 'describe-organization') }
    @{ f = 'organizations-accounts';     s = 'organizations'; a = @('organizations', 'list-accounts') }
    @{ f = 'organizations-roots';        s = 'organizations'; a = @('organizations', 'list-roots') }
)

$RegionalOps = @(
    # --- broad discovery (always collected) ---
    @{ f = 'tagging-resources';          s = 'tagging';       a = @('resourcegroupstaggingapi', 'get-resources'); phase = 'discovery' }
    @{ f = 'config-recorders';           s = 'config';        a = @('configservice', 'describe-configuration-recorders'); phase = 'discovery' }
    @{ f = 'config-aggregators';         s = 'config';        a = @('configservice', 'describe-configuration-aggregators'); phase = 'discovery' }

    # --- networking ---
    @{ f = 'ec2-vpcs';                   s = 'ec2';           a = @('ec2', 'describe-vpcs') }
    @{ f = 'ec2-subnets';                s = 'ec2';           a = @('ec2', 'describe-subnets') }
    @{ f = 'ec2-route-tables';           s = 'ec2';           a = @('ec2', 'describe-route-tables') }
    @{ f = 'ec2-internet-gateways';      s = 'ec2';           a = @('ec2', 'describe-internet-gateways') }
    @{ f = 'ec2-nat-gateways';           s = 'ec2';           a = @('ec2', 'describe-nat-gateways') }
    @{ f = 'ec2-vpc-endpoints';          s = 'ec2';           a = @('ec2', 'describe-vpc-endpoints') }
    @{ f = 'ec2-vpc-peering';            s = 'ec2';           a = @('ec2', 'describe-vpc-peering-connections') }
    @{ f = 'ec2-security-groups';        s = 'ec2';           a = @('ec2', 'describe-security-groups') }
    @{ f = 'ec2-network-acls';           s = 'ec2';           a = @('ec2', 'describe-network-acls') }
    @{ f = 'ec2-network-interfaces';     s = 'ec2';           a = @('ec2', 'describe-network-interfaces') }
    @{ f = 'ec2-addresses';              s = 'ec2';           a = @('ec2', 'describe-addresses') }
    @{ f = 'ec2-flow-logs';              s = 'ec2';           a = @('ec2', 'describe-flow-logs') }
    @{ f = 'ec2-transit-gateways';       s = 'ec2';           a = @('ec2', 'describe-transit-gateways') }
    @{ f = 'ec2-tgw-attachments';        s = 'ec2';           a = @('ec2', 'describe-transit-gateway-attachments') }
    @{ f = 'ec2-vpn-connections';        s = 'ec2';           a = @('ec2', 'describe-vpn-connections') }
    @{ f = 'directconnect-connections';  s = 'directconnect'; a = @('directconnect', 'describe-connections') }
    @{ f = 'elbv2-load-balancers';       s = 'elbv2';         a = @('elbv2', 'describe-load-balancers') }
    @{ f = 'elbv2-target-groups';        s = 'elbv2';         a = @('elbv2', 'describe-target-groups') }
    @{ f = 'elb-load-balancers';         s = 'elb';           a = @('elb', 'describe-load-balancers') }
    @{ f = 'wafv2-web-acls-regional';    s = 'wafv2';         a = @('wafv2', 'list-web-acls', '--scope', 'REGIONAL') }

    # --- compute ---
    @{ f = 'ec2-instances';              s = 'ec2';           a = @('ec2', 'describe-instances') }
    @{ f = 'ec2-volumes';                s = 'ec2';           a = @('ec2', 'describe-volumes') }
    @{ f = 'ec2-snapshots';              s = 'ec2';           a = @('ec2', 'describe-snapshots', '--owner-ids', 'self') }
    @{ f = 'ec2-images';                 s = 'ec2';           a = @('ec2', 'describe-images', '--owners', 'self') }
    @{ f = 'ec2-key-pairs';              s = 'ec2';           a = @('ec2', 'describe-key-pairs') }
    @{ f = 'ec2-launch-templates';       s = 'ec2';           a = @('ec2', 'describe-launch-templates') }
    @{ f = 'ec2-reserved-instances';     s = 'ec2';           a = @('ec2', 'describe-reserved-instances') }
    @{ f = 'autoscaling-groups';         s = 'autoscaling';   a = @('autoscaling', 'describe-auto-scaling-groups') }
    @{ f = 'beanstalk-applications';     s = 'elasticbeanstalk'; a = @('elasticbeanstalk', 'describe-applications') }
    @{ f = 'beanstalk-environments';     s = 'elasticbeanstalk'; a = @('elasticbeanstalk', 'describe-environments') }
    @{ f = 'batch-compute-environments'; s = 'batch';         a = @('batch', 'describe-compute-environments') }
    @{ f = 'apprunner-services';         s = 'apprunner';     a = @('apprunner', 'list-services') }
    @{ f = 'lightsail-instances';        s = 'lightsail';     a = @('lightsail', 'get-instances') }
    @{ f = 'ssm-instance-information';   s = 'ssm';           a = @('ssm', 'describe-instance-information') }

    # --- containers ---
    @{ f = 'ecs-clusters';               s = 'ecs';           a = @('ecs', 'list-clusters') }
    @{ f = 'ecs-task-definitions';       s = 'ecs';           a = @('ecs', 'list-task-definitions', '--status', 'ACTIVE') }
    @{ f = 'eks-clusters';               s = 'eks';           a = @('eks', 'list-clusters') }
    @{ f = 'ecr-repositories';           s = 'ecr';           a = @('ecr', 'describe-repositories') }

    # --- serverless ---
    @{ f = 'lambda-functions';           s = 'lambda';        a = @('lambda', 'list-functions') }
    @{ f = 'lambda-layers';              s = 'lambda';        a = @('lambda', 'list-layers') }
    @{ f = 'lambda-event-source-maps';   s = 'lambda';        a = @('lambda', 'list-event-source-mappings') }
    @{ f = 'stepfunctions-machines';     s = 'stepfunctions'; a = @('stepfunctions', 'list-state-machines') }
    @{ f = 'events-buses';               s = 'events';        a = @('events', 'list-event-buses') }
    @{ f = 'events-rules';               s = 'events';        a = @('events', 'list-rules') }
    @{ f = 'sqs-queues';                 s = 'sqs';           a = @('sqs', 'list-queues') }
    @{ f = 'sns-topics';                 s = 'sns';           a = @('sns', 'list-topics') }
    @{ f = 'sns-subscriptions';          s = 'sns';           a = @('sns', 'list-subscriptions') }
    @{ f = 'apigateway-rest-apis';       s = 'apigateway';    a = @('apigateway', 'get-rest-apis') }
    @{ f = 'apigatewayv2-apis';          s = 'apigatewayv2';  a = @('apigatewayv2', 'get-apis') }
    @{ f = 'appsync-graphql-apis';       s = 'appsync';       a = @('appsync', 'list-graphql-apis') }

    # --- databases ---
    @{ f = 'rds-db-instances';           s = 'rds';           a = @('rds', 'describe-db-instances') }
    @{ f = 'rds-db-clusters';            s = 'rds';           a = @('rds', 'describe-db-clusters') }
    @{ f = 'rds-global-clusters';        s = 'rds';           a = @('rds', 'describe-global-clusters') }
    @{ f = 'rds-db-snapshots';           s = 'rds';           a = @('rds', 'describe-db-snapshots', '--snapshot-type', 'manual') }
    @{ f = 'rds-subnet-groups';          s = 'rds';           a = @('rds', 'describe-db-subnet-groups') }
    @{ f = 'rds-proxies';                s = 'rds';           a = @('rds', 'describe-db-proxies') }
    @{ f = 'dynamodb-tables';            s = 'dynamodb';      a = @('dynamodb', 'list-tables') }
    @{ f = 'elasticache-clusters';       s = 'elasticache';   a = @('elasticache', 'describe-cache-clusters', '--show-cache-node-info') }
    @{ f = 'elasticache-repl-groups';    s = 'elasticache';   a = @('elasticache', 'describe-replication-groups') }
    @{ f = 'memorydb-clusters';          s = 'memorydb';      a = @('memorydb', 'describe-clusters') }
    @{ f = 'docdb-clusters';             s = 'docdb';         a = @('docdb', 'describe-db-clusters') }
    @{ f = 'neptune-clusters';           s = 'neptune';       a = @('neptune', 'describe-db-clusters') }
    @{ f = 'redshift-clusters';          s = 'redshift';      a = @('redshift', 'describe-clusters') }
    @{ f = 'redshift-serverless-wg';     s = 'redshift';      a = @('redshift-serverless', 'list-workgroups') }
    @{ f = 'opensearch-domains';         s = 'opensearch';    a = @('opensearch', 'list-domain-names') }

    # --- storage ---
    @{ f = 'efs-file-systems';           s = 'efs';           a = @('efs', 'describe-file-systems') }
    @{ f = 'fsx-file-systems';           s = 'fsx';           a = @('fsx', 'describe-file-systems') }
    @{ f = 'backup-plans';               s = 'backup';        a = @('backup', 'list-backup-plans') }
    @{ f = 'backup-vaults';              s = 'backup';        a = @('backup', 'list-backup-vaults') }
    @{ f = 'backup-protected-resources'; s = 'backup';        a = @('backup', 'list-protected-resources') }

    # --- identity & security ---
    @{ f = 'kms-keys';                   s = 'kms';           a = @('kms', 'list-keys') }
    @{ f = 'kms-aliases';                s = 'kms';           a = @('kms', 'list-aliases') }
    @{ f = 'secretsmanager-secrets';     s = 'secretsmanager'; a = @('secretsmanager', 'list-secrets') }
    @{ f = 'ssm-parameters';             s = 'ssm';           a = @('ssm', 'describe-parameters') }
    @{ f = 'acm-certificates';           s = 'acm';           a = @('acm', 'list-certificates') }
    @{ f = 'cognito-user-pools';         s = 'cognito';       a = @('cognito-idp', 'list-user-pools', '--max-results', '60') }
    @{ f = 'guardduty-detectors';        s = 'guardduty';     a = @('guardduty', 'list-detectors') }
    @{ f = 'securityhub-standards';      s = 'securityhub';   a = @('securityhub', 'get-enabled-standards') }
    @{ f = 'config-rules';               s = 'config';        a = @('configservice', 'describe-config-rules') }
    @{ f = 'accessanalyzer-analyzers';   s = 'accessanalyzer'; a = @('accessanalyzer', 'list-analyzers') }
    @{ f = 'ram-resources-self';         s = 'ram';           a = @('ram', 'list-resources', '--resource-owner', 'SELF') }
    @{ f = 'ram-resources-other';        s = 'ram';           a = @('ram', 'list-resources', '--resource-owner', 'OTHER-ACCOUNTS') }

    # --- data & integration ---
    @{ f = 'kinesis-streams';            s = 'kinesis';       a = @('kinesis', 'list-streams') }
    @{ f = 'firehose-streams';           s = 'firehose';      a = @('firehose', 'list-delivery-streams') }
    @{ f = 'msk-clusters';               s = 'kafka';         a = @('kafka', 'list-clusters-v2') }
    @{ f = 'glue-jobs';                  s = 'glue';          a = @('glue', 'get-jobs') }
    @{ f = 'glue-crawlers';              s = 'glue';          a = @('glue', 'get-crawlers') }
    @{ f = 'athena-workgroups';          s = 'athena';        a = @('athena', 'list-work-groups') }
    @{ f = 'emr-clusters';               s = 'emr';           a = @('emr', 'list-clusters', '--cluster-states', 'RUNNING', 'WAITING', 'STARTING') }

    # --- observability ---
    @{ f = 'logs-log-groups';            s = 'logs';          a = @('logs', 'describe-log-groups') }
    @{ f = 'cloudwatch-alarms';          s = 'cloudwatch';    a = @('cloudwatch', 'describe-alarms') }
    @{ f = 'cloudwatch-dashboards';      s = 'cloudwatch';    a = @('cloudwatch', 'list-dashboards') }
    @{ f = 'cloudtrail-trails';          s = 'cloudtrail';    a = @('cloudtrail', 'describe-trails') }

    # --- devops & iac ---
    @{ f = 'cloudformation-stacks';      s = 'cloudformation'; a = @('cloudformation', 'describe-stacks') }
    @{ f = 'cloudformation-stack-sets';  s = 'cloudformation'; a = @('cloudformation', 'list-stack-sets') }
    @{ f = 'codecommit-repositories';    s = 'codecommit';    a = @('codecommit', 'list-repositories') }
    @{ f = 'codebuild-projects';         s = 'codebuild';     a = @('codebuild', 'list-projects') }
    @{ f = 'codepipeline-pipelines';     s = 'codepipeline';  a = @('codepipeline', 'list-pipelines') }
    @{ f = 'codedeploy-applications';    s = 'codedeploy';    a = @('codedeploy', 'list-applications') }

    # --- other ---
    @{ f = 'ses-email-identities';       s = 'sesv2';         a = @('sesv2', 'list-email-identities') }
    @{ f = 'amplify-apps';               s = 'amplify';       a = @('amplify', 'list-apps') }
    @{ f = 'mq-brokers';                 s = 'mq';            a = @('mq', 'list-brokers') }
    @{ f = 'transfer-servers';           s = 'transfer';      a = @('transfer', 'list-servers') }
    @{ f = 'sagemaker-endpoints';        s = 'sagemaker';     a = @('sagemaker', 'list-endpoints') }
    @{ f = 'workspaces';                 s = 'workspaces';    a = @('workspaces', 'describe-workspaces') }
)

foreach ($op in ($GlobalOps + $RegionalOps)) { Assert-ReadOnly -Args $op.a }

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
function Invoke-AwsCli {
    param(
        [string[]]$Args,
        [string]$Region,
        [string]$AwsProfile,
        [int]$MaxAttempts = 6
    )

    $full = @($Args)
    if ($Region) { $full += @('--region', $Region) }
    if ($AwsProfile) { $full += @('--profile', $AwsProfile) }
    $full += @('--output', 'json', '--no-cli-pager')

    for ($attempt = 1; $attempt -le $MaxAttempts; $attempt++) {
        $stdout = & aws @full 2>&1
        if ($LASTEXITCODE -eq 0) {
            try { return @{ ok = $true; data = ($stdout | Out-String | ConvertFrom-Json -Depth 40) } }
            catch { return @{ ok = $true; data = ($stdout | Out-String) } }
        }

        $text = ($stdout | Out-String)

        if ($text -match 'Throttling|RequestLimitExceeded|TooManyRequests|Rate exceeded|SlowDown') {
            if ($attempt -lt $MaxAttempts) {
                Start-Sleep -Milliseconds ([math]::Min(30000, [math]::Pow(2, $attempt) * 500 + (Get-Random -Max 400)))
                continue
            }
            return @{ ok = $false; class = 'throttled-exhausted'; message = $text.Trim() }
        }

        $class = switch -Regex ($text) {
            'AccessDenied|UnauthorizedOperation|not authorized|AuthorizationError' { 'coverage-gap'; break }
            'OptInRequired|SubscriptionRequired|is not subscribed'                 { 'not-in-use'; break }
            'Could not connect to the endpoint|EndpointConnectionError|InvalidAction|UnknownOperation' { 'not-available'; break }
            'ExpiredToken|InvalidClientTokenId|TokenRefreshRequired|SSO session'   { 'auth'; break }
            'ResourceNotFound|NoSuch|NotFoundException'                            { 'not-in-use'; break }
            default { 'other' }
        }
        return @{ ok = $false; class = $class; message = $text.Trim() }
    }
}

function Get-ItemCount {
    param($Data)
    if ($null -eq $Data -or $Data -isnot [pscustomobject]) { return 0 }
    $total = 0
    foreach ($p in $Data.PSObject.Properties) {
        if ($p.Name -in @('NextToken', 'nextToken', 'Marker', 'NextMarker', 'PaginationToken', 'ResponseMetadata')) { continue }
        if ($p.Value -is [System.Array]) { $total += $p.Value.Count }
    }
    return $total
}

function Write-Envelope {
    param([string]$Path, [hashtable]$Meta, $Data)
    $dir = Split-Path -Parent $Path
    if (-not (Test-Path $dir)) { New-Item -ItemType Directory -Path $dir -Force | Out-Null }
    [pscustomobject]@{ _meta = $Meta; data = $Data } |
        ConvertTo-Json -Depth 40 |
        Set-Content -Path $Path -Encoding utf8NoBOM
}

# ---------------------------------------------------------------------------
# Identity
# ---------------------------------------------------------------------------
Write-Host "AWS Account Assessment — read-only sweep" -ForegroundColor Cyan
Write-Host ("-" * 60)

$idResult = Invoke-AwsCli -Args @('sts', 'get-caller-identity') -AwsProfile $AwsProfile
if (-not $idResult.ok) { throw "Cannot determine caller identity ($($idResult.class)): $($idResult.message)" }

$accountId = $idResult.data.Account
$callerArn = $idResult.data.Arn
Write-Host "Account : $accountId"
Write-Host "Caller  : $callerArn"

$cliVersion = (& aws --version 2>&1 | Out-String).Trim()
Write-Host "CLI     : $cliVersion"

# ---------------------------------------------------------------------------
# Regions
# ---------------------------------------------------------------------------
if (-not $Regions) {
    $regionResult = Invoke-AwsCli -Args @('account', 'list-regions', '--region-opt-status-contains', 'ENABLED', 'ENABLED_BY_DEFAULT') -Region 'us-east-1' -AwsProfile $AwsProfile
    if ($regionResult.ok) {
        $Regions = @($regionResult.data.Regions | ForEach-Object { $_.RegionName })
    }
    else {
        $fallback = Invoke-AwsCli -Args @('ec2', 'describe-regions', '--all-regions') -Region 'us-east-1' -AwsProfile $AwsProfile
        if (-not $fallback.ok) { throw "Cannot enumerate regions: $($fallback.message)" }
        $Regions = @($fallback.data.Regions |
            Where-Object { $_.OptInStatus -in @('opt-in-not-required', 'opted-in') } |
            ForEach-Object { $_.RegionName })
    }
}
$Regions = @($Regions | Sort-Object -Unique)
Write-Host "Regions : $($Regions.Count) -> $($Regions -join ', ')"

$opsToRun = switch ($Phase) {
    'discovery' { @($RegionalOps | Where-Object { $_.ContainsKey('phase') -and $_.phase -eq 'discovery' }) }
    'inventory' { @($RegionalOps | Where-Object { -not ($_.ContainsKey('phase') -and $_.phase -eq 'discovery') }) }
    default     { $RegionalOps }
}

Write-Host "Phase   : $Phase  ($($opsToRun.Count) regional operations x $($Regions.Count) regions + $($GlobalOps.Count) global)"
Write-Host "Output  : $OutputRoot/$accountId"
Write-Host ("-" * 60)

if ($DryRun) {
    Write-Host "DRY RUN — no data will be collected." -ForegroundColor Yellow
    $opsToRun | ForEach-Object { Write-Host "  regional: aws $($_.a -join ' ')" }
    $GlobalOps | ForEach-Object { Write-Host "  global  : aws $($_.a -join ' ')" }
    return
}

$accountRoot = Join-Path $OutputRoot $accountId
$started = Get-Date
$errors = [System.Collections.Concurrent.ConcurrentBag[object]]::new()
$summary = [System.Collections.Concurrent.ConcurrentBag[object]]::new()

# ---------------------------------------------------------------------------
# Global operations
# ---------------------------------------------------------------------------
Write-Host "[global] collecting $($GlobalOps.Count) operations..." -ForegroundColor Green
foreach ($op in $GlobalOps) {
    $path = Join-Path $accountRoot 'global' "$($op.f).json"
    if ((Test-Path $path) -and -not $Force) { continue }

    $r = Invoke-AwsCli -Args $op.a -AwsProfile $AwsProfile
    if ($r.ok) {
        $count = Get-ItemCount -Data $r.data
        Write-Envelope -Path $path -Data $r.data -Meta @{
            accountId = $accountId; region = 'global'; service = $op.s
            operation = ($op.a -join ' '); collectedAt = (Get-Date).ToUniversalTime().ToString('o')
            itemCount = $count; cliVersion = $cliVersion
        }
        $summary.Add([pscustomobject]@{ region = 'global'; service = $op.s; file = $op.f; count = $count })
    }
    else {
        if ($r.class -eq 'auth') { throw "Credentials problem during global sweep: $($r.message)" }
        $errors.Add([pscustomobject]@{ region = 'global'; service = $op.s; operation = ($op.a -join ' '); class = $r.class; message = $r.message })
    }
}

# ---------------------------------------------------------------------------
# Regional operations (parallel by region)
# ---------------------------------------------------------------------------
$fnInvoke = ${function:Invoke-AwsCli}.ToString()
$fnCount = ${function:Get-ItemCount}.ToString()
$fnWrite = ${function:Write-Envelope}.ToString()

$Regions | ForEach-Object -ThrottleLimit $Concurrency -Parallel {
    ${function:Invoke-AwsCli} = $using:fnInvoke
    ${function:Get-ItemCount} = $using:fnCount
    ${function:Write-Envelope} = $using:fnWrite

    $region = $_
    $ops = $using:opsToRun
    $root = $using:accountRoot
    $acct = $using:accountId
    $prof = $using:AwsProfile
    $frc = $using:Force
    $cliV = $using:cliVersion
    $errBag = $using:errors
    $sumBag = $using:summary

    $collected = 0
    foreach ($op in $ops) {
        $path = Join-Path $root $region "$($op.f).json"
        if ((Test-Path $path) -and -not $frc) { continue }

        $r = Invoke-AwsCli -Args $op.a -Region $region -AwsProfile $prof
        if ($r.ok) {
            $count = Get-ItemCount -Data $r.data
            Write-Envelope -Path $path -Data $r.data -Meta @{
                accountId = $acct; region = $region; service = $op.s
                operation = ($op.a -join ' '); collectedAt = (Get-Date).ToUniversalTime().ToString('o')
                itemCount = $count; cliVersion = $cliV
            }
            $sumBag.Add([pscustomobject]@{ region = $region; service = $op.s; file = $op.f; count = $count })
            $collected += $count
        }
        else {
            $errBag.Add([pscustomobject]@{ region = $region; service = $op.s; operation = ($op.a -join ' '); class = $r.class; message = $r.message })
        }
    }
    Write-Host ("[{0,-16}] {1,6} items" -f $region, $collected)
}

# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------
$summaryArr = @($summary)
$errorArr = @($errors)
$elapsed = (Get-Date) - $started

$byRegion = $summaryArr | Group-Object region | ForEach-Object {
    [pscustomobject]@{ region = $_.Name; items = ($_.Group | Measure-Object count -Sum).Sum; operations = $_.Count }
} | Sort-Object items -Descending

$byService = $summaryArr | Group-Object service | ForEach-Object {
    [pscustomobject]@{ service = $_.Name; items = ($_.Group | Measure-Object count -Sum).Sum }
} | Sort-Object items -Descending

$emptyRegions = @($byRegion | Where-Object { $_.items -eq 0 } | ForEach-Object { $_.region })

if (-not (Test-Path $accountRoot)) { New-Item -ItemType Directory -Path $accountRoot -Force | Out-Null }

[pscustomobject]@{
    accountId     = $accountId
    callerArn     = $callerArn
    phase         = $Phase
    startedAt     = $started.ToUniversalTime().ToString('o')
    finishedAt    = (Get-Date).ToUniversalTime().ToString('o')
    elapsedSecs   = [math]::Round($elapsed.TotalSeconds, 1)
    regionsScanned = $Regions
    totalItems    = ($summaryArr | Measure-Object count -Sum).Sum
    byRegion      = $byRegion
    byService     = $byService
    emptyRegions  = $emptyRegions
    errorCount    = $errorArr.Count
    coverageGaps  = @($errorArr | Where-Object { $_.class -eq 'coverage-gap' }).Count
    cliVersion    = $cliVersion
} | ConvertTo-Json -Depth 12 | Set-Content -Path (Join-Path $accountRoot '_summary.json') -Encoding utf8NoBOM

$errorArr | ConvertTo-Json -Depth 12 | Set-Content -Path (Join-Path $accountRoot '_errors.json') -Encoding utf8NoBOM

Write-Host ("-" * 60)
Write-Host "Done in $([math]::Round($elapsed.TotalMinutes,1)) min" -ForegroundColor Cyan
Write-Host "Total items      : $(($summaryArr | Measure-Object count -Sum).Sum)"
Write-Host "Regions w/ data  : $(($byRegion | Where-Object { $_.items -gt 0 }).Count) of $($Regions.Count)"
Write-Host "Empty regions    : $($emptyRegions.Count)"
Write-Host "Coverage gaps    : $(@($errorArr | Where-Object { $_.class -eq 'coverage-gap' }).Count)"
Write-Host "Summary          : $accountRoot/_summary.json"
Write-Host "Errors           : $accountRoot/_errors.json"
