# Azure Developer CLI Configuration

Use this skill when the migration workflow should support `azd init`, `azd provision`, `azd deploy`, or `azd up`.

## Purpose

`azure.yaml` binds application services, infra, and deployment commands into one consistent Azure Developer CLI workflow.

## Baseline `azure.yaml`

```yaml
name: contoso-modernization
services:
  web:
    project: src/Contoso.Web
    language: dotnet
    host: appservice
```

## Guidance

- Keep service names stable across environments.
- Align `host` with the assessed target: `appservice`, `containerapp`, or `aks`.
- Pair `azure.yaml` with `infra/` templates and environment-aware parameters.
- Use pre/post hooks only for repeatable build or packaging work.

## Common commands

```bash
azd init
azd env new dev
azd provision
azd deploy
azd up
```

## Validation checklist

- `azd` can detect the service project path.
- Provision and deploy use the same naming and environment assumptions.
- Output endpoints and resource names are surfaced cleanly.
