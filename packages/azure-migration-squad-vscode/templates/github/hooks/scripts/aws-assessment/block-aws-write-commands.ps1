# Hook: PreToolUse - Enforce read-only AWS CLI usage
# Denies any AWS CLI invocation whose operation verb is not read-only.
$ErrorActionPreference = "SilentlyContinue"

try {
    $inputText = [Console]::In.ReadToEnd()
    $hookInput = $inputText | ConvertFrom-Json
} catch {
    Write-Output '{"continue":true}'
    exit 0
}

$toolName = $hookInput.tool_name
if ($toolName -notin @("runInTerminal", "runTerminalCommand", "terminal", "awaitTerminal")) {
    Write-Output '{"continue":true}'
    exit 0
}

$command = ""
if ($hookInput.tool_input.command) { $command = $hookInput.tool_input.command }
elseif ($hookInput.tool_input.input) { $command = $hookInput.tool_input.input }

if (-not $command) {
    Write-Output '{"continue":true}'
    exit 0
}

function Deny([string]$reason) {
    $result = @{
        hookSpecificOutput = @{
            hookEventName            = "PreToolUse"
            permissionDecision       = "deny"
            permissionDecisionReason = $reason
        }
    }
    Write-Output ($result | ConvertTo-Json -Depth 5 -Compress)
    exit 0
}

# --- 1. Generic destructive commands -------------------------------------------------
$destructivePatterns = @(
    'rm\s+-rf\s+/',
    'rmdir\s+/s\s+/q\s+[A-Z]:\\',
    'Remove-Item\s+.*-Recurse.*-Force.*[/\\]$',
    'terraform\s+(destroy|apply)',
    'kubectl\s+(delete|apply|patch|scale|drain)',
    'DROP\s+(TABLE|DATABASE|SCHEMA)',
    'TRUNCATE\s+TABLE',
    'git\s+push\s+.*(--force|-f)\s'
)
foreach ($p in $destructivePatterns) {
    if ($command -match $p) {
        Deny "Destructive command blocked. The AWS Account Assessment Agent is read-only. Run this manually if it is genuinely intended."
    }
}

# --- 2. AWS CLI read-only enforcement ------------------------------------------------
# Match every 'aws <service> <operation>' occurrence in the command line.
$awsCalls = [regex]::Matches($command, '(?i)\baws\s+(?:[a-z0-9\-]+\s+)?([a-z0-9\-]+)\s+([a-z0-9\-]+)')

$allowedVerb = '^(describe|list|get|lookup|search|select|batch-get|generate-credential-report|help)'
$serviceWords = @('s3api','s3control','sts','ec2','iam','rds','ecs','eks','ecr','lambda','logs','ce',
                  'elbv2','elb','sqs','sns','kms','ssm','acm','efs','fsx','glue','emr','ram','mq',
                  'configservice','cloudtrail','cloudwatch','cloudformation','cloudfront','route53',
                  'organizations','autoscaling','elasticbeanstalk','elasticache','memorydb','docdb',
                  'neptune','redshift','redshift-serverless','opensearch','dynamodb','apigateway',
                  'apigatewayv2','appsync','stepfunctions','events','scheduler','kinesis','firehose',
                  'kafka','athena','guardduty','securityhub','inspector2','accessanalyzer','macie2',
                  'secretsmanager','cognito-idp','cognito-identity','backup','directconnect','wafv2',
                  'globalaccelerator','shield','network-firewall','resourcegroupstaggingapi',
                  'resource-explorer-2','account','apprunner','batch','lightsail','amplify','transfer',
                  'workspaces','sagemaker','bedrock','sesv2','ses','codecommit','codebuild',
                  'codepipeline','codedeploy','codeartifact','servicecatalog','service-quotas',
                  'compute-optimizer','sso-admin','identitystore','acm-pca','storagegateway',
                  'timestream-write','keyspaces','qldb','emr-serverless','quicksight','lakeformation',
                  'datapipeline','xray','synthetics','application-insights','detective','support',
                  'route53resolver','route53domains','ecr-public','es','iot','greengrassv2','connect',
                  'pinpoint','mediaconvert','elastictranscoder','devicefarm','outposts')

foreach ($m in $awsCalls) {
    $first  = $m.Groups[1].Value
    $second = $m.Groups[2].Value

    # 'aws s3 ls' style: first token is the service, second is the operation
    $operation = $second
    if ($first -notin $serviceWords -and $first -notmatch '^(--|-)') {
        $operation = $second
    }

    if ($operation -match '^(--|-)') { continue }              # flag, not an operation
    if ($operation -match $allowedVerb) { continue }           # allowed
    if ($first -eq 's3' -and $operation -in @('ls')) { continue }

    Deny "READ-ONLY VIOLATION: 'aws $first $operation' is not a read-only operation. This agent may only run describe-*, list-*, get-*, lookup-*, search-*, select-* and batch-get-* operations. If a mutating action is genuinely required, run it yourself outside this agent."
}

# --- 3. Explicitly forbidden AWS operations even though the verb looks read-only ------
$forbidden = @(
    @{ p = 'aws\s+secretsmanager\s+get-secret-value';                       r = 'Reading secret values is forbidden. Inventory secrets by name/ARN only.' },
    @{ p = 'aws\s+ssm\s+get-parameter[s]?(-by-path)?[^\r\n]*--with-decryption'; r = 'Reading decrypted SSM parameters is forbidden. Inventory parameter names/types only.' },
    @{ p = 'aws\s+kms\s+(decrypt|generate-data-key)';                       r = 'Producing plaintext key material is forbidden.' },
    @{ p = 'aws\s+configure\s+set';                                         r = 'Modifying local AWS configuration is out of scope for this agent.' },
    @{ p = 'aws\s+s3\s+(rm|rb|mv|cp|sync)\s';                               r = 'S3 data operations are forbidden. Use s3api list/get metadata operations only.' },
    @{ p = 'aws\s+cloudformation\s+detect-stack-drift';                     r = 'detect-stack-drift starts a job. Use describe-stack-drift-detection-status to read an existing result.' },
    @{ p = 'aws\s+dynamodb\s+(scan|query)\s';                               r = 'Reading table data is out of scope. Use describe-table for metadata.' }
)
foreach ($f in $forbidden) {
    if ($command -match "(?i)$($f.p)") { Deny "BLOCKED: $($f.r)" }
}

Write-Output '{"continue":true}'
