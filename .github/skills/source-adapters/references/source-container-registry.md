# Skill: Source Adapter — Container Registry

> Characterizes an application whose primary artifact is a container image (or set of images) in a registry — when source code may not be available, but the runtime image is.

## When to Use

- User provides a registry path (Docker Hub, ACR, ECR, GCR, GHCR, Harbor, Quay, JFrog)
- Source code is not in scope or not accessible — the image is the unit of work
- Rehost or replatform with existing container as starting point

## Inputs

- Registry URL(s): `docker.io/<org>/<repo>:<tag>`, `<acct>.dkr.ecr.<region>.amazonaws.com/<repo>:<tag>`, `<acr>.azurecr.io/<repo>:<tag>`
- Credentials (read-only) to pull / inspect
- List of image tags currently in production use

## Probes

### Image inspection

1. **Pull (or inspect remotely) the production image(s)**
   - `docker pull <image>` (or `skopeo inspect`, `crane manifest`)
   - `docker inspect <image>` → labels, env vars, exposed ports, entrypoint, cmd, working dir, user

2. **Image manifest + layers**
   - `docker history <image> --no-trunc` → layer composition (signals what's installed at each layer)
   - `crane export <image> | tar -tv` → file system content
   - `dive <image>` (interactive) → wasted layers, base size, file count per layer

3. **Base image identification**
   - First `FROM` if Dockerfile accessible, otherwise heuristics from labels (`org.opencontainers.image.base.name`) or the bottom-most layer
   - Common bases: `mcr.microsoft.com/dotnet/aspnet:8.0`, `eclipse-temurin:21-jre`, `python:3.12-slim`, `node:20-alpine`, `nginx:1.25`, `tomcat:9-jdk17`, `php:8.3-fpm`

4. **OCI labels**
   - `org.opencontainers.image.source` → may point at the source repo
   - `org.opencontainers.image.revision` → commit SHA
   - `org.opencontainers.image.created` → build timestamp
   - `org.opencontainers.image.title`, `.description`, `.licenses`

5. **Runtime configuration**
   - `Entrypoint` + `Cmd` → primary process
   - `ExposedPorts` → listening ports → workload pattern hint
   - `Env` → default env vars (redact any obvious secrets but note keys)
   - `Volumes` → mount points (state dependencies)
   - `User` → root vs non-root (security flag)
   - `Healthcheck` → presence / shape

### Vulnerability + dependency scan (optional, recommended)

6. **`trivy image <image>`** → CVEs, OS package list, application-level dep list (pip / npm / gem / cargo)
7. **`syft <image>`** → SBOM
8. **`grype <image>`** → vulnerability listing
9. Captures the **actual runtime dependency surface** even when source is missing

### Registry inventory

10. **List tags + sizes**
    - ACR: `az acr repository show-manifests --name <acr> --repository <repo>`
    - ECR: `aws ecr describe-images --repository-name <repo>`
    - GHCR / Docker Hub: REST API
11. **Image signing / attestations**
    - Cosign signatures, SLSA provenance → captures supply-chain maturity

## Output Evidence

```yaml
source:
  primary_adapter: source-container-registry
  access_method: <docker-pull | skopeo-remote | registry-read-only-token>
  evidence_confidence: <high if pulled and inspected; medium if metadata-only>
  evidence_paths:
    - <image references>
    - <SBOM file path if produced>
  notes: |
    - Image: <fqn:tag>
    - Image size: <MB / GB>
    - Base image: <e.g., eclipse-temurin:21-jre-alpine>
    - Detected runtime: <e.g., Java 21, Spring Boot 3.2>
    - Detected app deps: <top 10 from SBOM>
    - Exposed ports: <list>
    - Entrypoint: <command>
    - User: <root | non-root UID>
    - Healthcheck: <present | absent>
    - Vulnerabilities: <CRITICAL: N, HIGH: N, MEDIUM: N>
    - Source repo (from label): <URL | unknown>
```

## Migration Constraints / Risks

- **No source code.** If only the image exists, code changes are impossible. Strategy bias → **rehost** or **replatform-to-managed-host**, not refactor.
- **Insecure base image.** Out-of-support OS, CVE-heavy base → must replace base in Phase 2 (or accept risk via Security Auditor).
- **Root user / overly-privileged process.** Container Apps and AKS both prefer non-root. Refactor to non-root may require a small Dockerfile change.
- **Built-in secrets / hardcoded env values.** Inspect `Env`; any sensitive-looking values must move to Key Vault.
- **External state coupled by mount path.** `Volumes:` declarations imply persistent state — pair with `source-on-premise` or `source-aws` to find the underlying storage.
- **Multi-arch.** ARM64 vs AMD64 — Azure compute supports both, but pick the one that matches.
- **Image size > 1 GB.** Slow pulls in production; Phase 5 should consider multi-stage Dockerfile rebuild.
- **No source label (`org.opencontainers.image.source`).** Provenance is unknown — flag for Security Auditor.

## Workload Pattern Inference (from container)

| Image signal | Workload pattern |
|--------------|------------------|
| Exposed port 80 / 8080 / 443 + nginx/apache/iis/tomcat | `webapp` or `api-service` |
| Single-process Python/Node with HTTP framework + EXPOSE | `api-service` |
| `CMD ["python", "worker.py"]` consuming a queue lib | `event-driven` |
| `CMD` runs once and exits (cron in container, or batch) | `batch-job` |
| `CMD ["dotnet", "MyApp.Worker.dll"]` | `event-driven` (likely) |
| Static content (nginx + static HTML) | `webapp` (static) |

## Target Azure Mapping (signals)

| Image shape | Azure candidate |
|-------------|-----------------|
| Generic OCI image, single port HTTP | **Container Apps** (first) — managed, no K8s |
| Multi-container compose (Dockerfile + docker-compose.yml) | Container Apps with multiple revisions, or AKS |
| Image expects Kubernetes APIs (DOWNWARD API, in-cluster DNS) | **AKS** |
| Web-only, no scaling tricks | **App Service** with custom container |
| Short-lived batch image | **Container Apps Jobs** |
| Function-shaped image (sub-second cold start, small) | **Azure Functions** with custom image |

## Anti-Patterns

- Don't try to refactor an image you can't see the source of. Rehost or replatform first; revisit refactor later if source is recovered.
- Don't migrate an image with HIGH/CRITICAL CVEs as-is. Rebuild the base in Phase 2.
- Don't assume EXPOSE means anything. Many Dockerfiles leave it stale. Confirm by network inspection of running containers.
- Don't dump full env value strings. Capture keys only.
- Don't trust the tag. Always pin to the digest (`@sha256:...`) when capturing evidence.

## Output Checklist

- [ ] Production image(s) identified by fully-qualified name + digest
- [ ] Image size + layer count captured
- [ ] Base image identified
- [ ] Runtime + framework inferred from layers / SBOM
- [ ] Exposed ports captured
- [ ] Entrypoint + Cmd captured
- [ ] User (root / non-root) captured
- [ ] Healthcheck presence captured
- [ ] Env keys captured (values redacted)
- [ ] Volume mounts captured
- [ ] SBOM produced (or marked as not-run)
- [ ] CVE scan summary captured
- [ ] Source-repo label captured (or marked unknown — security flag)
