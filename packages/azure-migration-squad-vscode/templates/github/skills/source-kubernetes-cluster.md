# Skill: Source Adapter — Kubernetes Cluster

> Characterizes an application currently running on a Kubernetes cluster (any flavor: vanilla K8s, EKS, GKE, OpenShift, Rancher, on-prem).

## When to Use

- User says "it runs on Kubernetes"
- Source environment is a cluster (regardless of which cloud or on-prem)
- The unit of deployment is workloads (Deployments / StatefulSets / DaemonSets) + Services / Ingresses + ConfigMaps / Secrets

## Inputs

- `kubeconfig` context name (preferred) — or read-only export of cluster state
- Cluster URL / API server endpoint
- Namespaces in scope (default: all, but usually narrow to app-owned namespaces)

## Probes (read-only `kubectl`)

### Cluster baseline

1. `kubectl version --short` → server + client version (drives compatibility / upgrade path)
2. `kubectl get nodes -o wide` → node count, OS, kernel, container runtime (containerd / cri-o / docker)
3. `kubectl get namespaces` → namespace inventory
4. `kubectl api-resources --verbs=list -o wide` → CRDs (operators, service mesh, etc.)
5. `kubectl get crd` → installed operators (Istio, ArgoCD, Prometheus Operator, KEDA, Strimzi, etc.)

### Workloads (per namespace)

6. `kubectl get deployments,statefulsets,daemonsets,cronjobs,jobs -n <ns>` → workload inventory
7. For each workload: `kubectl get deployment <X> -o yaml`
   - Capture: image, replicas, resources, env vars, volume mounts, init containers, sidecars
8. `kubectl get pods -n <ns> -o wide` → actual placement, restarts, ages

### Services & Ingress

9. `kubectl get services -n <ns>` → ClusterIP / NodePort / LoadBalancer / ExternalName
10. `kubectl get ingresses -n <ns>` → ingress rules, classes
11. `kubectl get gateway,httproute -n <ns>` → Gateway API (newer)
12. Service mesh: `kubectl get virtualservices,destinationrules -n <ns>` (Istio), `kubectl get serviceprofile -n <ns>` (Linkerd)

### Configuration & Secrets

13. `kubectl get configmaps -n <ns>` → name list (do NOT dump values unless explicitly allowed)
14. `kubectl get secrets -n <ns>` → name + type
15. ExternalSecrets / Sealed Secrets / SOPS markers → captures the current secret-management pattern

### Storage

16. `kubectl get pvc -n <ns>` → claims, storage class, size
17. `kubectl get pv` → underlying storage backends (EBS, GP3, Azure Disk, NFS, CSI driver, etc.)
18. `kubectl get storageclass` → provisioners

### Identity / RBAC

19. `kubectl get serviceaccount -n <ns>`, `kubectl get rolebinding,clusterrolebinding -n <ns>`
20. IRSA (AWS), Workload Identity (GCP/Azure), Pod Identity → capture which is in use

### Networking

21. NetworkPolicies: `kubectl get networkpolicies -n <ns>`
22. CNI: `kubectl get pods -n kube-system` → identify Calico / Cilium / Flannel / Azure CNI
23. DNS: CoreDNS config

### Observability stack

24. Prometheus / Grafana / Loki / Tempo / Jaeger / Fluent Bit / Fluentd / Datadog agents
25. `kubectl get servicemonitor,podmonitor,prometheusrule -n <ns>` (Prometheus Operator)

### GitOps / Delivery

26. ArgoCD: `kubectl get applications -n argocd`
27. Flux: `kubectl get gitrepositories,kustomizations -n flux-system`
28. Helm: `helm list --all-namespaces`

## Output Evidence

```yaml
source:
  primary_adapter: source-kubernetes-cluster
  access_method: <kubeconfig-context-name | cluster-url + token | export-only>
  evidence_confidence: <high if live API; medium if export>
  evidence_paths:
    - <cluster-url or context>
    - <namespaces in scope>
  notes: |
    - K8s version: <e.g., 1.27>
    - Distro: <vanilla | EKS | GKE | AKS | OpenShift | k3s | RKE2>
    - Node count: <N>
    - Container runtime: <containerd | cri-o | docker>
    - Service mesh: <istio | linkerd | none>
    - Ingress class: <nginx | alb | gce | traefik | gateway-api>
    - GitOps: <argocd | flux | helm-only | manual>
    - Observability: <prom+grafana | datadog | newrelic | logs-only>
    - Workloads in scope: <count of Deployments + StatefulSets + Jobs>
```

## Migration Constraints / Risks

- **Service mesh dependencies.** If the app relies on Istio mTLS or traffic-shifting, AKS migration must include the mesh choice (Istio add-on, Linkerd self-installed, or rip out the mesh).
- **Operator / CRD dependencies.** Cert-Manager, External-DNS, KEDA, Prometheus Operator must be re-installed on AKS. List as Phase 3 deliverables.
- **Storage class portability.** EBS gp3 PVCs don't move to Azure Disk automatically. Data has to be migrated (`velero`, restore from snapshot, app-level export).
- **In-cluster databases.** PostgreSQL/MySQL/MongoDB running as StatefulSets in-cluster → strongly prefer migrating to Azure managed PaaS (PostgreSQL Flexible, MySQL Flexible, Cosmos for Mongo) over running in AKS.
- **Custom controllers / operators.** May need re-coding or replacement.
- **Pod Security Standards / OPA Gatekeeper / Kyverno.** Re-implement on AKS.
- **Workload Identity translation.** IRSA (AWS) → Azure Workload Identity. GCP Workload Identity → Azure Workload Identity. Direct cluster → managed identity pattern.

## Workload Pattern Inference

| Cluster shape | Workload pattern |
|---------------|------------------|
| Deployment + Service + Ingress (web traffic) | `webapp` or `api-service` |
| Deployment + Service (no Ingress, called internally) | `api-service` (internal) |
| CronJob | `batch-job` |
| Job (one-shot) | `batch-job` |
| Deployment with KEDA scaler on queue depth | `event-driven` |
| StatefulSet (database, Kafka, ZK) | data-tier — usually migrate OUT to managed PaaS |
| DaemonSet | infrastructure (CNI / logging / monitoring) — replace with AKS native |

## Target Azure Mapping (signals)

| Cluster today | Azure candidate |
|---------------|-----------------|
| EKS / GKE / vanilla K8s | **AKS** (first) — preserves K8s portability |
| Simple Deployment + Service + Ingress | Consider **Container Apps** to escape K8s complexity (Architect decision) |
| Single Deployment with HTTP entry | App Service + container image (Architect decision) |
| CronJob | Container Apps Jobs |
| Job | Container Apps Jobs |
| KEDA-scaled Deployment | Container Apps (KEDA-native) or AKS with KEDA add-on |
| StatefulSet database | Migrate to Azure managed PaaS for that engine |
| Istio | AKS + Istio service-mesh add-on |
| ArgoCD | Keep ArgoCD (works on AKS) or migrate to GitHub Actions / Azure DevOps |

## Anti-Patterns

- Don't dump Secret values during discovery. Names + types only.
- Don't replicate the in-cluster database to AKS. Migrate to managed PaaS.
- Don't try to lift custom operators 1:1 to AKS without checking AKS add-on equivalents first.
- Don't ignore the StorageClass — it's a major migration blocker if overlooked.
- Don't assume `kubectl apply` of the same manifests works on AKS — IngressClass names, StorageClass names, and IRSA annotations differ.

## Output Checklist

- [ ] Cluster version + distro captured
- [ ] Namespaces in scope listed
- [ ] All in-scope workloads inventoried (Deployments / StatefulSets / Jobs / CronJobs)
- [ ] Services + Ingresses + Gateways captured
- [ ] ConfigMaps + Secrets names captured (values NOT dumped)
- [ ] PVCs + storage classes captured
- [ ] Service accounts + workload identity pattern captured
- [ ] CRDs + operators listed
- [ ] GitOps / delivery tool captured
- [ ] Observability stack captured
- [ ] In-cluster databases flagged for migration to PaaS
- [ ] Service mesh dependency flagged for Phase 3
