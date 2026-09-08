---
name: aws-assessment-scripts
description: Ready-to-run PowerShell and Bash sweep scripts for read-only AWS multi-region inventory collection, with retry/backoff, region parallelism, resumability, error classification and normalized JSON output. Use during Phase 1 and Phase 2 instead of issuing hundreds of ad-hoc CLI commands.
---

# AWS Assessment Scripts Skill

Batch collectors that do the mechanical work of the sweep so the agent can focus on analysis. **Every command they issue is read-only.**

## Why use the scripts instead of ad-hoc commands

| Problem with ad-hoc commands | How the scripts solve it |
|------------------------------|--------------------------|
| Hundreds of tool calls flood the agent context | One invocation, one summary returned |
| Throttling kills a partial sweep | Exponential backoff with jitter, adaptive retry mode |
| A failed region silently disappears | Errors classified and written to `_errors.json` |
| Re-running re-queries everything | Files already present are skipped unless `-Force` |
| Inconsistent output shapes | Fixed `<account>/<region>/<service>.json` layout |
| No parallelism | Regions swept concurrently with a throttle limit |

---

## Files

| File | Platform | Purpose |
|------|----------|---------|
| `scripts/aws-scan.ps1` | PowerShell 7+ | Primary collector |
| `scripts/aws-scan.sh` | Bash 4+ | Linux/macOS equivalent |

---

## Usage — PowerShell

```powershell
# Full sweep of the currently authenticated account, all enabled regions
pwsh .github/skills/aws-assessment-scripts/scripts/aws-scan.ps1

# Broad discovery only (Phase 1)
pwsh ./aws-scan.ps1 -Phase discovery

# Specific profile and regions
pwsh ./aws-scan.ps1 -AwsProfile prod-account -Regions us-east-1,sa-east-1

# Higher concurrency, force re-collection
pwsh ./aws-scan.ps1 -Concurrency 8 -Force

# Preview the plan without calling AWS
pwsh ./aws-scan.ps1 -DryRun
```

## Usage — Bash

```bash
bash .github/skills/aws-assessment-scripts/scripts/aws-scan.sh
bash ./aws-scan.sh --phase discovery
bash ./aws-scan.sh --profile prod-account --regions "us-east-1 sa-east-1"
bash ./aws-scan.sh --concurrency 8 --force
bash ./aws-scan.sh --dry-run
```

---

## Parameters

| PowerShell | Bash | Default | Meaning |
|------------|------|---------|---------|
| `-Phase` | `--phase` | `all` | `discovery` (broad + global only), `inventory` (per-service), `all` |
| `-OutputRoot` | `--output-root` | `./reports/raw` | Where JSON is written |
| `-Regions` | `--regions` | auto-detected | Explicit region list; omit to enumerate enabled regions |
| `-AwsProfile` | `--profile` | ambient | Named AWS profile |
| `-Concurrency` | `--concurrency` | `5` | Regions swept in parallel |
| `-Force` | `--force` | off | Re-collect files that already exist |
| `-DryRun` | `--dry-run` | off | Print the plan; make no AWS calls beyond identity/regions |

---

## Output layout

```
reports/raw/
├── _scope.json                      # written by Phase 0
└── 111111111111/
    ├── _summary.json                # counts per region/service, timing
    ├── _errors.json                 # classified failures
    ├── global/
    │   ├── iam-roles.json
    │   ├── s3-buckets.json
    │   ├── route53-hosted-zones.json
    │   └── cloudfront-distributions.json
    └── sa-east-1/
        ├── tagging-resources.json
        ├── ec2-instances.json
        ├── rds-db-instances.json
        └── ...
```

Each file contains the raw AWS response plus a small envelope:

```json
{
  "_meta": {
    "accountId": "111111111111",
    "region": "sa-east-1",
    "service": "ec2",
    "operation": "describe-instances",
    "collectedAt": "2026-08-19T14:02:11Z",
    "pages": 3,
    "itemCount": 88,
    "cliVersion": "aws-cli/2.31.4"
  },
  "data": { }
}
```

---

## Error classification written to `_errors.json`

| Class | Meaning | Assessment impact |
|-------|---------|-------------------|
| `coverage-gap` | `AccessDenied` / `UnauthorizedOperation` | Must be reported — data is missing |
| `not-in-use` | `OptInRequired` / `SubscriptionRequired` | Service not enabled; normal |
| `not-available` | Endpoint not reachable in that region | Service not offered there; normal |
| `throttled-exhausted` | Retries exhausted | Re-run that region |
| `auth` | Expired or invalid credentials | Sweep must stop and re-authenticate |
| `other` | Anything else | Review manually |

---

## After the sweep

1. The agent (or a subagent) reads `_summary.json` and `_errors.json` — **not** the raw files
2. Raw files are parsed selectively when building the inventory, topology and findings
3. `_errors.json` entries of class `coverage-gap` are copied into `Report-Status.md`
4. Re-running the script is safe: existing files are skipped unless `-Force`

---

## Extending the catalog

Both scripts define the operation catalog as a data table near the top. To add a service:

```powershell
@{ f = 'apprunner-services'; s = 'apprunner'; a = @('apprunner','list-services') }
```

**Only add read-only verbs.** The scripts refuse to execute any operation whose verb is not in the allow-list, and will abort with an error if the catalog is edited to include one.
