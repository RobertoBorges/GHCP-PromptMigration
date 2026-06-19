# Azure Kubernetes Service (AKS)

Use this skill when the target architecture genuinely requires Kubernetes orchestration, custom networking, or platform-level control.

## Best fit

Choose AKS only when one or more of these are true:

- multiple tightly coordinated services need Kubernetes primitives
- custom ingress, service mesh, or policy controls are required
- the team already operates Kubernetes successfully
- workload portability or cluster-level extensibility is a hard requirement

## Baseline AKS pattern

- AKS cluster with managed identity / workload identity
- Azure Container Registry
- Ingress controller
- Log Analytics / Azure Monitor for containers
- Key Vault integration through CSI or application-level secret retrieval
- Helm chart per deployable service

## Helm chart structure

```text
charts/
  app/
    Chart.yaml
    values.yaml
    templates/
      deployment.yaml
      service.yaml
      ingress.yaml
      hpa.yaml
```

## Deployment defaults

- define requests/limits
- configure readiness and liveness probes
- externalize config to ConfigMaps/secrets
- prefer Workload Identity over secret-based credentials
- enable HPA only with credible metrics

## Validation checklist

- Cluster need is explicitly justified.
- Images, manifests, and charts are environment-aware.
- RBAC, namespaces, ingress, and autoscaling are defined.
- Operational ownership for patching and upgrades is understood.
