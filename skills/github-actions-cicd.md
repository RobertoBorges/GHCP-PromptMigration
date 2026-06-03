# GitHub Actions CI/CD

Use this skill when the target repository should deploy through GitHub Actions.

## Core pipeline stages

1. checkout and dependency cache
2. build + unit tests
3. security/static analysis as available
4. infra validation (`bicep`, `terraform`, or `azd`)
5. deploy to non-prod
6. smoke test
7. production deployment with environment protection

## Security defaults

- Prefer GitHub OIDC federation to Azure over long-lived secrets.
- Store only minimal repository/environment secrets.
- Use protected environments for staging and production.

## Starter workflow shape

```yaml
name: ci-cd
on:
  push:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
```

## Validation checklist

- Build, test, and deploy stages are separated.
- Workflow auth uses OIDC where possible.
- Rollback or slot-swap strategy is documented.
- Environment-specific approvals exist for production.
