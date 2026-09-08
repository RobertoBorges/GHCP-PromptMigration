---
name: Phase0-SetupAndScope
description: Validate AWS CLI access, enumerate accounts and enabled regions, and define the assessment scope
argument-hint: "Optionally name the profile or account, e.g., 'Assess profile prod-account' or 'Scan my whole AWS Organization'"
agent: AWS Account Assessment Agent
---

# Phase 0 — Setup & Scope

## Assessment Scope

This guided assessment helps you:
- ✅ Discover every resource across every account and every enabled region
- ✅ Understand ownership: tags, creation date, creator identity, cost center
- ✅ Map how resources connect to each other
- ✅ Surface security, governance and cost risks

This assessment is **strictly read-only** and does **NOT**:
- ❌ Create, modify or delete any AWS resource
- ❌ Read secret values from Secrets Manager or Parameter Store
- ❌ Migrate or move any workload or data

---

## Step 1: Verify Tooling

Confirm the AWS CLI is installed and current:

```powershell
aws --version
```

Expected: AWS CLI **v2.x**. If v1 is detected, warn the user that some commands used later (`aws account list-regions`, `aws resource-explorer-2`, `aws ecs describe-clusters --include TAGS`) require v2 and offer the upgrade link.

Also check for optional accelerators:

```powershell
aws configure list-profiles
```

---

## Step 2: Identify The Caller (REQUIRED)

```powershell
aws sts get-caller-identity --output json --no-cli-pager
```

Present the result to the user in a table:

| Field | Value |
|-------|-------|
| Account ID | `...` |
| ARN | `...` |
| User ID | `...` |
| Principal type | IAM user / assumed role / SSO session / root |

**⚠️ STOP and confirm with the user that this is the account they intend to assess.**

If the call fails, help the user authenticate:

| Credential model | Command |
|------------------|---------|
| AWS IAM Identity Center (SSO) | `aws sso login --profile <profile>` |
| Named profile | `aws sts get-caller-identity --profile <profile>` |
| Environment variables | Confirm `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_SESSION_TOKEN` are set |
| EC2/ECS instance role | Confirm the instance metadata endpoint is reachable |

Never ask the user to paste credentials into chat — instruct them to run the login command in their own terminal.

---

## Step 3: Determine The Account Model

Load the **aws-account-discovery** skill.

Try Organizations access:

```powershell
aws organizations describe-organization --output json --no-cli-pager
```

### 3.a — Organizations available
Enumerate the estate:

```powershell
aws organizations list-accounts --output json --no-cli-pager
aws organizations list-roots --output json --no-cli-pager
aws organizations list-organizational-units-for-parent --parent-id <root-id> --output json --no-cli-pager
aws organizations list-policies --filter SERVICE_CONTROL_POLICY --output json --no-cli-pager
```

Then ask: **"Which accounts do you want to assess?"**
- [ ] All accounts in the organization
- [ ] Specific OUs only
- [ ] A specific list of account IDs

Ask which cross-account role to assume:
- `OrganizationAccountAccessRole` (default for Organizations-created accounts)
- `ReadOnlyAccess` / `SecurityAudit` / `ViewOnlyAccess`
- A customer-specific read-only role name

**Verify assumption works for one account before proceeding to all of them.**

### 3.b — Organizations NOT available (single-account / manual login mode)
This is expected and fully supported. Tell the user:

> Organizations access is not available with these credentials. The assessment will run in **per-account mode**: I will scan the account you are currently authenticated to, save its results under `reports/raw/<account-id>/`, and then you can log in to the next account and re-run Phase 1. All reports are re-aggregated across every account already scanned, so nothing is lost between sessions.

Ask the user to list the account IDs they plan to assess so `Report-Status.md` can track done/pending.

---

## Step 4: Enumerate Enabled Regions (REQUIRED)

Never hard-code a region list. Query it:

```powershell
aws account list-regions --region-opt-status-contains ENABLED ENABLED_BY_DEFAULT --output json --no-cli-pager
```

Fallback when the `account` API is not permitted:

```powershell
aws ec2 describe-regions --all-regions --output json --no-cli-pager
```

Filter to `OptInStatus` of `opt-in-not-required` or `opted-in`. Present the region count and list.

Then ask: **"Which regions should I scan?"**
- [ ] All enabled regions (recommended — this is how shadow resources are found)
- [ ] Only regions where resources are expected
- [ ] A specific list

⚠️ Warn: restricting regions is the single most common cause of an incomplete assessment.

---

## Step 5: Confirm Assessment Options

Ask the user to confirm each:

| Option | Choices | Default |
|--------|---------|---------|
| **Creator attribution** | CloudTrail lookup (90-day window) / Athena over CloudTrail S3 (full history) / tags only / skip | CloudTrail lookup |
| **Cost analysis** | Include Cost Explorer (billed per API request) / skip | Ask |
| **Security findings** | Include GuardDuty + Security Hub + Config + Inspector + Access Analyzer / config-derived checks only / skip | Include |
| **Account ID masking** | Mask account IDs in Markdown reports / show in full | Show in full |
| **Sweep concurrency** | Regions scanned in parallel (1–10) | 5 |

Detect whether an organization CloudTrail with an S3 destination exists (enables >90-day attribution):

```powershell
aws cloudtrail describe-trails --output json --no-cli-pager
aws cloudtrail get-trail-status --name <trail-name> --output json --no-cli-pager
```

Detect whether an AWS Config aggregator exists (dramatically speeds up discovery):

```powershell
aws configservice describe-configuration-aggregators --output json --no-cli-pager
```

Detect whether Resource Explorer is indexed:

```powershell
aws resource-explorer-2 list-indexes --output json --no-cli-pager
```

Report which accelerators are available — they change the Phase 1 strategy.

---

## Step 6: Consent Gate (REQUIRED)

Present a summary and **DO NOT PROCEED UNTIL THE USER EXPLICITLY CONFIRMS**:

```
Assessment plan
---------------
Accounts:        <n> (<ids or 'current account only'>)
Regions:         <n> enabled regions
Services:        <n> service domains, ~<n> API operations per region
Estimated calls: ~<n> read-only API requests
Estimated time:  <range>
Billable APIs:   Cost Explorer (<n> requests, ~$0.01 each) [only if enabled]
Mode:            READ-ONLY — no resource will be created, modified or deleted
Output:          ./reports/
```

---

## Step 7: Initialize Tracking

Create the reports scaffold:

- `reports/Report-Status.md` — using the status template from the **aws-inventory-reporting** skill, pre-populated with:
  - Assessment start timestamp
  - Account model (Organizations / per-account)
  - Account list with `Pending` status for each
  - Region list
  - Selected options
  - Empty coverage-gap table
- `reports/raw/` — directory for raw JSON output
- `.gitignore` entry for `reports/raw/` if the workspace is a git repository (ask first)

---

## Exit Criteria

- [ ] AWS CLI v2 confirmed
- [ ] Caller identity confirmed by the user
- [ ] Account model determined (Organizations or per-account)
- [ ] Account list defined and recorded
- [ ] Enabled regions enumerated and scope confirmed
- [ ] Assessment options confirmed
- [ ] Accelerators (Config aggregator / Resource Explorer / CloudTrail S3) detected
- [ ] Explicit consent obtained
- [ ] `reports/Report-Status.md` created

**Next step:** proceed to `/AWSAssess-phase1-resourcediscovery`
