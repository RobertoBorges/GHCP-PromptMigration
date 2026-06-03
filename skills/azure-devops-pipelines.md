# Azure DevOps Pipelines

Use this skill when the organization standard is Azure DevOps rather than GitHub Actions.

## Pipeline model

- CI stage for restore/build/test
- IaC validation stage
- deployment stages for dev, test, and prod
- approvals and checks on protected environments
- secure service connections to Azure

## Baseline YAML shape

```yaml
trigger:
- main

stages:
- stage: Build
- stage: Deploy_Dev
- stage: Deploy_Prod
```

## Guidance

- Use variable groups or Key Vault-backed secrets.
- Prefer workload identity/service connections over embedded credentials.
- Publish build artifacts once; promote them between stages.
- Keep rollback instructions alongside deployment stages.

## Validation checklist

- Environments, approvals, and service connections are defined.
- Infra and app deployment responsibilities are explicit.
- Secrets stay out of source-controlled YAML.
