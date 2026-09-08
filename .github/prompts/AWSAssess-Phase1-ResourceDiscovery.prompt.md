---
name: Phase1-ResourceDiscovery
description: Perform the broad multi-region sweep and build the raw resource index for the account in scope
argument-hint: "Optionally scope the sweep, e.g., 'Scan only us-east-1 and sa-east-1' or 'Sweep account 123456789012'"
agent: AWS Account Assessment Agent
---

# Phase 1 — Broad Resource Discovery

**Goal:** produce a fast, complete index of *every* resource ARN in the account, across every in-scope region, before spending time on per-service detail.

**Prerequisite:** Phase 0 completed and `reports/Report-Status.md` exists.

---

## Step 1: Select The Discovery Strategy

Load the **aws-resource-inventory** skill. Choose the strategy based on what Phase 0 detected:

| Accelerator available | Strategy | Why |
|-----------------------|----------|-----|
| **AWS Config aggregator** | `select-aggregate-resource-config` | Fastest and broadest; single query covers all accounts and regions already recorded by Config |
| **Resource Explorer index** | `resource-explorer-2 search` | Cross-region search from one aggregator region; good ARN + tag coverage |
| **Neither** | `resourcegroupstaggingapi get-resources` per region | Universal fallback; works with `ReadOnlyAccess`, returns ARN + tags |

Always run the **Resource Groups Tagging API** pass regardless of strategy — it is the only source that reliably returns tags for every taggable resource type.

### 1.a — AWS Config aggregator query

```powershell
aws configservice select-aggregate-resource-config `
  --configuration-aggregator-name <aggregator> `
  --expression "SELECT resourceId, resourceName, resourceType, awsRegion, accountId, tags, resourceCreationTime" `
  --limit 100 `
  --output json --no-cli-pager
```

Paginate with `--next-token` until exhausted.

### 1.b — Resource Explorer query

```powershell
aws resource-explorer-2 search --query-string "*" --max-results 1000 --output json --no-cli-pager
```

### 1.c — Resource Groups Tagging API (per region, universal)

```powershell
aws resourcegroupstaggingapi get-resources `
  --region <region> `
  --resources-per-page 100 `
  --output json --no-cli-pager
```

Paginate with `--pagination-token`.

---

## Step 2: Run The Sweep

Use the sweep scripts from the **aws-assessment-scripts** skill rather than issuing hundreds of ad-hoc commands:

```powershell
pwsh .github/skills/aws-assessment-scripts/scripts/aws-scan.ps1 -Phase Discovery -OutputRoot ./reports/raw
```

```bash
bash .github/skills/aws-assessment-scripts/scripts/aws-scan.sh --phase discovery --output-root ./reports/raw
```

**Delegate the sweep to a subagent.** The raw JSON is large and must not flood the main context — the subagent should return only:
- Resource counts per region
- Resource counts per service
- Regions with zero resources
- Any permission or throttling errors encountered

### Sweep rules
- Scan every in-scope region, including ones the user believes are empty
- Paginate to exhaustion — a truncated page is a silent data loss
- On `ThrottlingException` / `RequestLimitExceeded`: exponential backoff, then reduce concurrency
- On `AccessDenied` / `UnauthorizedOperation`: record a **coverage gap** entry, do not abort the sweep
- On `OptInRequired` / service unavailable in region: record as "service not available in region", not as a gap

---

## Step 3: Cover The Global And Single-Region Services

Some services are not regional and would be missed by a per-region loop. Query them once:

| Service | Where to query | Command |
|---------|----------------|---------|
| IAM | Global | `aws iam list-users` / `list-roles` / `list-groups` / `list-policies --scope Local` |
| S3 (bucket list) | Global | `aws s3api list-buckets` — then resolve each bucket's region with `get-bucket-location` |
| Route 53 | Global | `aws route53 list-hosted-zones` |
| CloudFront | Global | `aws cloudfront list-distributions` |
| WAFv2 (CloudFront scope) | `us-east-1` | `aws wafv2 list-web-acls --scope CLOUDFRONT --region us-east-1` |
| Organizations | `us-east-1` | `aws organizations list-accounts` |
| Global Accelerator | `us-west-2` | `aws globalaccelerator list-accelerators --region us-west-2` |
| Route 53 Domains | `us-east-1` | `aws route53domains list-domains --region us-east-1` |
| Cost Explorer | `us-east-1` | `aws ce get-cost-and-usage ...` |
| Shield Advanced | `us-east-1` | `aws shield describe-subscription --region us-east-1` |

---

## Step 4: Normalize Into The Resource Index

Write every discovered resource into `reports/raw/<account-id>/_index.json` using this schema:

```json
{
  "accountId": "123456789012",
  "accountAlias": "prod-workloads",
  "scanTimestamp": "2026-08-19T14:02:11Z",
  "resources": [
    {
      "arn": "arn:aws:ec2:sa-east-1:123456789012:instance/i-0abc123",
      "resourceId": "i-0abc123",
      "resourceName": "web-01",
      "service": "ec2",
      "resourceType": "AWS::EC2::Instance",
      "region": "sa-east-1",
      "tags": { "Environment": "prod", "Owner": "platform-team" },
      "discoveredBy": "resourcegroupstaggingapi"
    }
  ],
  "coverageGaps": [
    { "region": "ap-east-1", "service": "eks", "reason": "AccessDeniedException", "operation": "eks:ListClusters" }
  ],
  "emptyRegions": ["me-central-1", "af-south-1"]
}
```

---

## Step 5: Produce The Discovery Summary

Update `reports/Report-Status.md` and present to the user:

### Resource distribution by region

| Region | Resources | Top services |
|--------|-----------|--------------|
| `sa-east-1` | 412 | EC2 (88), Lambda (61), RDS (12) |
| `us-east-1` | 137 | S3 (44), CloudWatch (31), IAM roles (22) |
| ... | ... | ... |

### Resource distribution by service

| Service | Count | Regions present |
|---------|-------|-----------------|
| EC2 instances | 88 | sa-east-1, us-east-1 |
| ECS services | 24 | sa-east-1 |
| RDS/Aurora | 12 | sa-east-1 |
| ... | ... | ... |

### Coverage report

| Metric | Value |
|--------|-------|
| Regions scanned | 17 of 17 enabled |
| Regions with resources | 4 |
| Regions confirmed empty | 13 |
| Coverage gaps (permission denied) | 2 |
| Total resources indexed | 549 |

**Highlight anything surprising**: resources in regions the user did not expect, resources with no tags, resources outside the primary region — these are the classic shadow-IT signals.

---

## Step 6: Multi-Account Continuation

If more accounts remain in scope:

### Organizations mode
Assume the read-only role in the next account and repeat Phase 1 automatically:

```powershell
aws sts assume-role `
  --role-arn arn:aws:iam::<next-account-id>:role/<ReadOnlyRoleName> `
  --role-session-name aws-assessment `
  --output json --no-cli-pager
```

Tell the user which role is being assumed before doing it.

### Per-account mode
Stop and tell the user exactly what to do next:

> Account `<id>` is complete — `<n>` resources indexed under `reports/raw/<id>/`.
> To continue, log in to the next account in your terminal (`aws sso login --profile <next>` or export the next set of credentials), then run `/AWSAssess-phase1-resourcediscovery` again. I will detect the new account ID and append it without touching the data already collected.

Update `Report-Status.md`: mark this account `Discovered`, leave the others `Pending`.

---

## Exit Criteria

- [ ] Every in-scope region swept (or explicitly recorded as a coverage gap)
- [ ] Global/single-region services queried
- [ ] `reports/raw/<account-id>/_index.json` written
- [ ] Coverage gaps and empty regions recorded
- [ ] Discovery summary presented to the user
- [ ] `Report-Status.md` updated with per-account progress

**Next step:** proceed to `/AWSAssess-phase2-deepinventory` (or repeat Phase 1 for the next account)
