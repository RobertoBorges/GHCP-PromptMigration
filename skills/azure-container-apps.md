# Azure Container Apps

> **REFERENCE ONLY** — This root `skills/` copy is for reference and onboarding. Prompts must reference the authoritative prompt-local copy at `#file:.github/skills/azure-container-apps.md`.

Use this skill when the target workload is containerized, stateless or event-driven, and does not require full Kubernetes control.

## Best fit

Choose Container Apps for:

- HTTP APIs packaged as containers
- background workers or jobs
- scale-to-zero or KEDA-driven event processing
- microservices that need simple ingress, revisions, and managed environment support

## Core pattern

- Container Apps Environment
- App or job resources per workload
- Managed identity
- Azure Container Registry
- Log Analytics and Application Insights
- Secrets supplied through Container Apps secrets or Key Vault references

## Example `azure.yaml`

```yaml
services:
  api:
    project: src/BusReservation
    language: java
    host: containerapp
```

## Container settings checklist

- expose port 8080 unless the app requires a different port
- configure readiness/liveness probes
- set min/max replicas based on traffic shape
- keep the container stateless
- inject config via environment variables and secrets

## Scaling guidance

- HTTP scale rules for APIs
- queue/topic rules for workers
- set `minReplicas: 0` only when cold start is acceptable
- cap `maxReplicas` to a sane cost boundary

## Validation checklist

- Image builds reproducibly.
- App starts under non-root user where practical.
- Probes, scaling, and revision settings are explicit.
- Identity, secrets, and observability are configured.
