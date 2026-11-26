# Azure Developer CLI Configuration

Use this reference when the user selects Azure Developer CLI (`azd`) to coordinate application build, provisioning, deployment, or monitoring.

## Configuration guidance

- Define services in `azure.yaml` with paths and host values matching the selected target.
- Keep environment-specific values out of source defaults; use reviewed parameters and secure identity flows.
- Keep hooks limited to repeatable build or packaging steps.
- Confirm that provision and deploy target the intended environment and subscription before execution.
- Do not run commands that create or change Azure resources without explicit user consent.

## Validation

- Check `azure.yaml` against the current `azd` schema and service model.
- Run non-mutating validation first where available.
- Present planned resource changes and environment context for user approval before provisioning.

## Current sources

See [Azure Guidance Sources](./azure-guidance-sources.md) and the [Azure Developer CLI documentation](https://learn.microsoft.com/azure/developer/azure-developer-cli/).
