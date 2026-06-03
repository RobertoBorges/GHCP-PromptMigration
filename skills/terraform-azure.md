# Terraform for Azure

Use this skill when infrastructure must be authored with Terraform instead of Bicep.

## Baseline rules

- Pin `azurerm` and other providers.
- Use remote state with locking.
- Organize by modules rather than a single flat file.
- Prefer OIDC or managed identity for pipeline authentication.
- Avoid writing secrets to state when an Azure-native identity flow exists.

## Recommended structure

```text
infra/
  providers.tf
  main.tf
  variables.tf
  outputs.tf
  modules/
    app_service/
    container_app/
    aks/
    monitoring/
    identity/
    database/
```

## Example provider block

```hcl
terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 4.0"
    }
  }
}

provider "azurerm" {
  features {}
}
```

## Validation checklist

- `terraform fmt -check` passes.
- `terraform validate` passes.
- Plans are environment-safe and reviewable.
- Module boundaries match workload boundaries.
