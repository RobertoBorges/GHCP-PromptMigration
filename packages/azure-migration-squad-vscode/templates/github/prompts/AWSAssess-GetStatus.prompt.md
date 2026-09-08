---
name: GetStatus
description: Check the current status of the AWS account assessment, including which accounts are done and what to run next
argument-hint: "Example: 'What is the status of the assessment?' or 'Which accounts are still pending?'"
agent: AWS Account Assessment Agent
---

# Assessment Status Check

Report the current state of the AWS assessment. Do **not** run any AWS API call for this — read the local artifacts only, unless the user explicitly asks to verify live state.

---

## Step 1: Read The Local State

Read, when present:
- `reports/Report-Status.md`
- `reports/raw/**/_index.json` (one folder per account scanned)
- `reports/raw/**/_inventory-enriched.json`
- `reports/raw/**/_edges.json`
- `reports/inventory.csv`

Derive from the folders on disk rather than trusting the status file alone — the folders are the source of truth for what was actually collected.

If nothing exists, tell the user no assessment has started and point them to `/AWSAssess-phase0-setupandscope`.

---

## Step 2: Report Phase Progress

| Phase | Status |
|-------|--------|
| 0 — Setup & Scope | ✅ / ⏳ / ⬜ |
| 1 — Resource Discovery | ✅ / ⏳ / ⬜ |
| 2 — Deep Inventory | ✅ / ⏳ / ⬜ |
| 3 — Enrichment | ✅ / ⏳ / ⬜ |
| 4 — Relationships & Topology | ✅ / ⏳ / ⬜ |
| 5 — Reports | ✅ / ⏳ / ⬜ |
| 6 — Azure Readiness | ✅ / ⏳ / ⬜ / N/A |

---

## Step 3: Report Per-Account Progress

This is the most important table when the user is logging in to accounts one at a time:

| Account | Alias | P1 | P2 | P3 | P4 | Resources | Regions with resources | Last scanned |
|---------|-------|----|----|----|----|-----------|------------------------|--------------|
| 111111111111 | prod-workloads | ✅ | ✅ | ✅ | ✅ | 549 | 4 | 2026-08-19 14:02 |
| 222222222222 | prod-data | ✅ | ✅ | ⬜ | ⬜ | 212 | 2 | 2026-08-19 15:40 |
| 333333333333 | dev-sandbox | ⬜ | ⬜ | ⬜ | ⬜ | — | — | pending |

---

## Step 4: Report Estate Snapshot

From the data already collected:

| Metric | Value |
|--------|-------|
| Accounts scanned | 2 of 3 |
| Regions scanned | 17 |
| Total resources | 761 |
| Services in use | 34 |
| Internet-exposed resources | 12 |
| Untagged resources | 118 |
| Resources with unknown owner | 87 |
| Open findings (Critical/High) | 4 / 17 |
| Coverage gaps | 3 |

---

## Step 5: Report Coverage Gaps

| Account | Region | Service | Operation | Reason |
|---------|--------|---------|-----------|--------|
| 111111111111 | ap-east-1 | eks | `eks:ListClusters` | AccessDeniedException |

State clearly whether each gap is a permission issue the user can fix, or an inherent limitation.

---

## Step 6: State The Exact Next Action

Be specific and copy-pasteable. Examples:

**When accounts remain and the user logs in manually:**
> Account `222222222222` needs Phases 3–4. Run `/AWSAssess-phase3-enrichment`.
> After that, account `333333333333` is still pending. Log in to it in your terminal:
> ```powershell
> aws sso login --profile dev-sandbox
> aws sts get-caller-identity --profile dev-sandbox
> ```
> then run `/AWSAssess-phase1-resourcediscovery`. I will detect the new account and append it without touching the data already collected.

**When Organizations mode is active:**
> `/AWSAssess-phase1-resourcediscovery` will assume `arn:aws:iam::333333333333:role/OrganizationAccountAccessRole` and continue automatically.

**When everything is done:**
> All accounts are complete. Run `/AWSAssess-phase5-reports` to regenerate the consolidated report set, or `/AWSAssess-phase6-azurereadiness` if Azure migration is in scope.

---

## Step 7: Surface Anything That Needs A Decision

List open questions blocking progress, for example:
- Required tag set not yet defined
- Cost Explorer not yet authorized by the user
- Cross-account role name unknown for pending accounts
- CloudTrail attribution window exceeded and no S3/Athena trail available
- Reports contain unmasked account IDs and the user has not decided on masking
