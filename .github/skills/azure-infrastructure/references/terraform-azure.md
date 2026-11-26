# Terraform for Azure

Use this reference when the user selects Terraform for Azure infrastructure.

## Baseline guidance

- Pin Terraform and provider constraints that are compatible with the project's configuration.
- Use remote state with appropriate access controls, encryption, and locking.
- Organize reusable modules around stable workload boundaries.
- Prefer federated identity or managed identity for pipeline authentication.
- Protect state and plan artifacts; avoid placing secrets in variables, outputs, or state.

## Validation

- Run `terraform fmt -check`, `terraform validate`, and a reviewable plan.
- Confirm the workspace, backend, subscription, and target environment before planning or applying.
- Require explicit approval before applying infrastructure changes.

## Current sources

See [Azure Guidance Sources](./azure-guidance-sources.md), [Terraform on Azure](https://learn.microsoft.com/azure/developer/terraform/), and the [AzureRM provider reference](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs). Verify current provider constraints and resource arguments rather than copying pinned versions from old examples.
