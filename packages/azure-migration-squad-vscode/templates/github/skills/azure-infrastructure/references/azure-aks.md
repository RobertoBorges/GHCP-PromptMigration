# Azure Kubernetes Service (AKS)

Use AKS when the workload has a demonstrated need for Kubernetes primitives, custom networking or policy, or cluster-level control—and the team can operate the platform. Compare App Service and Container Apps first when their capabilities meet the requirements.

## Baseline considerations

- Define cluster, identity, network, ingress, registry, observability, and upgrade ownership.
- Use workload identity and least-privilege RBAC; avoid long-lived credentials.
- Set resource requests and limits. Configure readiness and liveness probes.
- Use autoscaling only with suitable metrics and a tested capacity range.
- Keep Helm charts and environment-specific configuration reviewable.

## Validation

- Document why AKS is required over a simpler target.
- Validate region, quota, Kubernetes version support, and upgrade policy.
- Check network, identity, image, policy, and operational dependencies.
- Test deployment, health probes, scaling, and rollback.

## Current sources

See [Azure Guidance Sources](./azure-guidance-sources.md). Start with [AKS documentation](https://learn.microsoft.com/azure/aks/) and verify current platform guidance before generating cluster configuration.
