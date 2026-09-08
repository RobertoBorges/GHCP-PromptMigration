---
name: aws-account-discovery
description: AWS credential validation, account enumeration via Organizations or per-account profiles, dynamic region discovery including opt-in regions, cross-account read-only role assumption, and resumable multi-account session handling. Use during Phase 0 and whenever the assessment moves to a new account.
---

# AWS Account Discovery Skill

Establishes *who you are*, *which accounts are in scope*, and *which regions must be swept* before any inventory work begins.

## When to Use
- Phase 0 — Setup & Scope
- Whenever the user switches credentials to assess another account
- Whenever a sweep fails with an authentication or authorization error

---

## 1. Credential Validation

Always the first command of any session:

```powershell
aws sts get-caller-identity --output json --no-cli-pager
```

```json
{
  "UserId": "AROAEXAMPLE:hbarbosa",
  "Account": "111111111111",
  "Arn": "arn:aws:sts::111111111111:assumed-role/AWSReservedSSO_ReadOnly_abc/hbarbosa"
}
```

### Interpreting the ARN

| ARN shape | Principal type | Notes |
|-----------|----------------|-------|
| `arn:aws:iam::<acct>:user/<name>` | IAM user | Long-lived keys; check key age in findings |
| `arn:aws:sts::<acct>:assumed-role/<role>/<session>` | Assumed role | Session name often identifies the human |
| `arn:aws:sts::<acct>:assumed-role/AWSReservedSSO_<permset>_<hash>/<user>` | IAM Identity Center (SSO) | Permission set name reveals the granted scope |
| `arn:aws:iam::<acct>:root` | Root user | Raise a Critical finding — root should not be used |
| `arn:aws:sts::<acct>:federated-user/<name>` | Federated | Check the identity provider |

### Authentication recovery

| Situation | What to tell the user (they run it themselves) |
|-----------|-----------------------------------------------|
| `ExpiredToken` / `InvalidClientTokenId` with SSO | `aws sso login --profile <profile>` |
| No default credentials | `aws configure list-profiles`, then re-run with `--profile <name>` or set `AWS_PROFILE` |
| MFA-protected role | The user obtains a session token themselves; never handle MFA codes or secrets in chat |
| `AccessDenied` on `sts:GetCallerIdentity` | SCP or permission boundary is blocking; escalate to the account admin |

**Never** ask the user to paste access keys, secret keys or session tokens into the conversation.

---

## 2. Minimum Permissions Required

The assessment works with any of these, in order of preference:

| Managed policy | Coverage |
|----------------|----------|
| `arn:aws:iam::aws:policy/ReadOnlyAccess` | Best coverage; includes most `describe`/`list`/`get` |
| `arn:aws:iam::aws:policy/SecurityAudit` | Good for identity/security domains, lighter on workloads |
| `arn:aws:iam::aws:policy/job-function/ViewOnlyAccess` | Metadata only; misses some attributes |
| `arn:aws:iam::aws:policy/AWSBillingReadOnlyAccess` | Needed only for Cost Explorer |

Cost Explorer additionally requires `ce:GetCostAndUsage`, `ce:GetRightsizingRecommendation`. Organizations enumeration requires `organizations:ListAccounts`, `organizations:DescribeOrganization`.

Record any permission the assessment lacks as a **coverage gap** — never silently skip.

---

## 3. Account Model Detection

```powershell
aws organizations describe-organization --output json --no-cli-pager
```

| Result | Mode | Behavior |
|--------|------|----------|
| Success, `MasterAccountId` == caller account | **Management account** | Full enumeration + cross-account role assumption |
| Success, caller is a delegated administrator | **Delegated admin** | Enumeration works; role assumption depends on the role deployed |
| `AWSOrganizationsNotInUseException` | **Standalone account** | Per-account mode |
| `AccessDeniedException` | **Member account without visibility** | Per-account mode |

### Organizations enumeration

```powershell
aws organizations describe-organization --output json --no-cli-pager
aws organizations list-roots --output json --no-cli-pager
aws organizations list-accounts --output json --no-cli-pager
aws organizations list-organizational-units-for-parent --parent-id <root-or-ou-id> --output json --no-cli-pager
aws organizations list-accounts-for-parent --parent-id <ou-id> --output json --no-cli-pager
aws organizations list-policies --filter SERVICE_CONTROL_POLICY --output json --no-cli-pager
aws organizations list-policies-for-target --target-id <account-or-ou-id> --filter SERVICE_CONTROL_POLICY --output json --no-cli-pager
aws organizations list-tags-for-resource --resource-id <account-id> --output json --no-cli-pager
aws organizations list-delegated-administrators --output json --no-cli-pager
```

Walk the OU tree recursively from each root to build the hierarchy for the account-hierarchy diagram.

Capture per account: `Id`, `Name`, `Email`, `Status` (`ACTIVE`/`SUSPENDED`), `JoinedMethod`, `JoinedTimestamp`, parent OU, applied SCPs, tags. **Suspended accounts still hold resources and still cost money** — include them and flag them.

---

## 4. Cross-Account Role Assumption (Organizations mode)

Common read-only role names, in order of likelihood:

1. `OrganizationAccountAccessRole` — created automatically for accounts provisioned by Organizations
2. `AWSControlTowerExecution` — Control Tower environments
3. `ReadOnlyAccess` / `SecurityAudit` / `ViewOnlyAccess` — customer-deployed
4. A customer-specific name — always ask

```powershell
$assumed = aws sts assume-role `
  --role-arn "arn:aws:iam::<target-account>:role/<RoleName>" `
  --role-session-name "aws-assessment-$(Get-Date -Format yyyyMMddHHmm)" `
  --duration-seconds 3600 `
  --output json --no-cli-pager | ConvertFrom-Json

$env:AWS_ACCESS_KEY_ID     = $assumed.Credentials.AccessKeyId
$env:AWS_SECRET_ACCESS_KEY = $assumed.Credentials.SecretAccessKey
$env:AWS_SESSION_TOKEN     = $assumed.Credentials.SessionToken

aws sts get-caller-identity --output json --no-cli-pager
```

```bash
eval "$(aws sts assume-role \
  --role-arn "arn:aws:iam::<target-account>:role/<RoleName>" \
  --role-session-name "aws-assessment-$(date +%Y%m%d%H%M)" \
  --query 'Credentials.[AccessKeyId,SecretAccessKey,SessionToken]' \
  --output text | awk '{print "export AWS_ACCESS_KEY_ID="$1"\nexport AWS_SECRET_ACCESS_KEY="$2"\nexport AWS_SESSION_TOKEN="$3}')"
```

### Rules
- **Always tell the user which role ARN is being assumed before assuming it.**
- Verify with `get-caller-identity` immediately after, and confirm the account ID changed.
- Sessions expire (default 1h) — re-assume when a sweep runs long, and record the re-assumption in the status file.
- **Always unset the temporary variables** when moving to the next account so a stale session cannot silently attribute data to the wrong account:

```powershell
Remove-Item Env:AWS_ACCESS_KEY_ID, Env:AWS_SECRET_ACCESS_KEY, Env:AWS_SESSION_TOKEN -ErrorAction SilentlyContinue
```

A cleaner alternative when the user's `~/.aws/config` supports it — profile chaining, no manual env juggling:

```ini
[profile member-prod]
role_arn       = arn:aws:iam::222222222222:role/OrganizationAccountAccessRole
source_profile = management
region         = sa-east-1
```

```powershell
aws sts get-caller-identity --profile member-prod --output json --no-cli-pager
```

---

## 5. Per-Account Mode (manual login, one account at a time)

This is the default when Organizations is unavailable, and it is a **fully supported first-class path**.

### Loop

1. User authenticates to account *N* in their own terminal
2. Agent runs `aws sts get-caller-identity` and reads the account ID
3. Agent checks whether `reports/raw/<account-id>/` already exists
   - Exists → ask whether to re-scan (overwrite) or skip
   - New → proceed
4. Agent runs Phases 1–4 for that account, writing only into `reports/raw/<account-id>/`
5. Agent runs Phase 5, which **regenerates all reports from every account folder present**
6. Agent updates `Report-Status.md` with done/pending and prints the exact next command
7. User logs in to account *N+1* and the loop repeats — possibly days later, in a new session

### Session resumption

Because all state lives on disk under `reports/raw/`, a new chat session can resume by reading those folders. `Report-Status.md` is a convenience view; **the folders are the source of truth**.

Never delete or overwrite another account's folder. Never merge two accounts' raw data into one folder.

---

## 6. Region Discovery (never hard-code)

Preferred:

```powershell
aws account list-regions --region-opt-status-contains ENABLED ENABLED_BY_DEFAULT --output json --no-cli-pager
```

Fallback (works with `ReadOnlyAccess`):

```powershell
aws ec2 describe-regions --all-regions --output json --no-cli-pager
```

Keep regions whose `OptInStatus` is `opt-in-not-required` or `opted-in`. Drop `not-opted-in` — the APIs are not reachable there.

### Why "all enabled regions" matters

Opt-in regions (`af-south-1`, `ap-east-1`, `ap-south-2`, `ap-southeast-3/4/5`, `ca-west-1`, `eu-central-2`, `eu-south-1/2`, `il-central-1`, `me-central-1`, `me-south-1`) are where forgotten resources and shadow IT most often live. Skipping them is the most common reason an assessment misses cost and risk.

Also account for partitions when relevant: `aws-us-gov`, `aws-cn`. These require separate credentials and a different partition in every ARN — treat them as separate assessments.

### Global vs regional services

| Query once, globally | Query in a fixed region | Query in every region |
|----------------------|-------------------------|-----------------------|
| IAM, Organizations, Route 53, CloudFront, S3 bucket list, WAF Classic global | Cost Explorer (`us-east-1`), Global Accelerator (`us-west-2`), Route 53 Domains (`us-east-1`), Shield (`us-east-1`), WAFv2 CLOUDFRONT scope (`us-east-1`) | Everything else |

S3 is a special case: the bucket **list** is global, but each bucket lives in a region — resolve it with `aws s3api get-bucket-location --bucket <name>` (a `null`/empty `LocationConstraint` means `us-east-1`).

---

## 7. Throttling And Concurrency

| Symptom | Response |
|---------|----------|
| `ThrottlingException`, `RequestLimitExceeded`, `TooManyRequestsException`, `Rate exceeded` | Exponential backoff starting at 1s, up to 6 retries with jitter |
| Repeated throttling in one region | Halve the concurrency for that region |
| Throttling across all regions | Reduce global concurrency to 2 and continue — never drop results |

Enable adaptive retries in the CLI itself:

```powershell
$env:AWS_RETRY_MODE = "adaptive"
$env:AWS_MAX_ATTEMPTS = "10"
```

Recommended default concurrency: **5 regions in parallel**, sequential services within a region.

---

## 8. Error Classification

Classify every failure — this determines whether it is a coverage gap or a normal result:

| Error | Classification | Action |
|-------|----------------|--------|
| `AccessDeniedException`, `UnauthorizedOperation`, `AccessDenied` | **Coverage gap** | Record account/region/service/operation; continue |
| `OptInRequired`, `SubscriptionRequiredException` | Service not enabled | Record as "not in use"; continue |
| `InvalidClientTokenId`, `ExpiredToken` | Credential problem | Stop and re-authenticate |
| `EndpointConnectionError`, `Could not connect to the endpoint URL` | Service not available in region | Record as "service not available"; continue |
| `ResourceNotFoundException` on a list operation | Normal empty result | Record zero resources |
| `ThrottlingException` | Transient | Backoff and retry |
| `ValidationException` on a required parameter | Wrong CLI usage | Fix the command; do not record as a gap |

---

## 9. Phase 0 Output Contract

Write to `reports/raw/_scope.json`:

```json
{
  "assessmentStart": "2026-08-19T13:40:00Z",
  "accountModel": "organizations",
  "organizationId": "o-example123",
  "managementAccountId": "111111111111",
  "crossAccountRoleName": "OrganizationAccountAccessRole",
  "accounts": [
    { "id": "111111111111", "alias": "prod-workloads", "ou": "Production", "status": "ACTIVE", "assessmentStatus": "pending" }
  ],
  "regions": ["us-east-1", "sa-east-1", "eu-west-1"],
  "options": {
    "creatorAttribution": "cloudtrail-90d",
    "costAnalysis": true,
    "securityFindings": true,
    "maskAccountIds": false,
    "concurrency": 5
  },
  "accelerators": {
    "configAggregator": "org-aggregator",
    "resourceExplorerIndex": true,
    "cloudTrailS3Bucket": "org-cloudtrail-logs",
    "athenaTable": null
  }
}
```

Every later phase reads this file to know its scope.
