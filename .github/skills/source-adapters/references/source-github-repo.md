# Skill: Source Adapter — GitHub Repository

> Characterizes an application whose source lives in a Git repository (GitHub, GitHub Enterprise, GitLab, Azure DevOps Repos, Bitbucket).

## When to Use

- User provides a Git URL or has cloned a repo locally
- The application's primary source is in version control
- Multi-repo solutions: run once per repo and aggregate

## Inputs

- Git URL (`https://github.com/<org>/<repo>` or SSH equivalent), OR
- Local clone path (filesystem path to a `.git` repo root)
- Optional: branch / tag / commit SHA to anchor discovery
- Optional: credentials / PAT (do NOT store in repo)

## Probes (in order)

1. **Repo metadata**
   - `git remote -v` → upstream URL
   - `git log --pretty=format:"%h %s" -10` → recent activity (signal of liveness)
   - `git branch -a` → branch model (gitflow, trunk-based, etc.)
   - `git tag --sort=-creatordate | head -5` → release cadence

2. **Top-level shape**
   - `ls -la` at root → manifests, READMEs, dockerfiles, CI configs
   - Look for `monorepo` indicators: `lerna.json`, `pnpm-workspace.yaml`, `nx.json`, `rush.json`, `apps/`, `packages/`, multiple `*.csproj` files in subdirs
   - Count source files by language → feed `stack-detection`

3. **Build manifests** (handoff to `stack-detection`)
   - `*.sln`, `*.csproj`, `pom.xml`, `build.gradle`, `package.json`, `requirements.txt`, `pyproject.toml`, `composer.json`, `Gemfile`, `go.mod`, `Cargo.toml`, `Makefile`, `CMakeLists.txt`

4. **CI/CD existing automation**
   - `.github/workflows/*.yml` → existing GitHub Actions
   - `azure-pipelines.yml` → Azure DevOps
   - `.gitlab-ci.yml`, `Jenkinsfile`, `.circleci/config.yml`, `bitbucket-pipelines.yml`
   - Captures the **current deployment shape** — used in Phase 5

5. **Containerization signals**
   - `Dockerfile`, `docker-compose.yml`, `*.dockerfile`
   - `k8s/`, `kubernetes/`, `helm/`, `manifests/`, `*.yaml` with `kind:`
   - Captures the **current packaging** — used in Phase 3

6. **IaC existing**
   - `infra/`, `terraform/`, `bicep/`, `*.tf`, `*.bicep`, `azure.yaml` (azd)
   - If present, may reuse / extend rather than generate from scratch

7. **Configuration files**
   - `appsettings*.json`, `application*.yml`, `web.config`, `app.config`, `.env*`, `config/`
   - Captures **secret references** → flagged for Key Vault migration in Phase 3

8. **Test surface**
   - `tests/`, `test/`, `__tests__/`, `*Test*.java`, `*Tests.cs`, `*_test.go`, `*.spec.ts`
   - Test count + coverage signal → influences refactor vs rebuild decision in `migration-strategy-decision-tree`

9. **Documentation**
   - `README.md`, `docs/`, `ARCHITECTURE.md`
   - Read top-level README for app purpose and stated dependencies

## Output Evidence (feed to Discovery Dossier)

```yaml
source:
  primary_adapter: source-github-repo
  access_method: git-url       # or filesystem-path
  evidence_confidence: high    # repo is in hand
  evidence_paths:
    - <repo URL or local clone path>
    - <key manifest paths>
  notes: |
    - Branch model: <gitflow | trunk | other>
    - Last commit: <date>
    - Monorepo: <yes/no — count of sub-projects>
    - Existing CI: <yes/no — which platform>
    - Containerized today: <yes/no>
    - IaC present: <yes/no — which tool>
    - Tests present: <yes/no — approximate coverage>
```

## Migration Constraints / Risks

- **Secrets in source.** Grep for `password=`, `connectionstring=`, `token=`, AWS access keys, `BEGIN PRIVATE KEY`. If found → add `risk_flags: [secrets-in-source]` and route to Security Auditor.
- **Submodules / vendored deps.** `git submodule status`, `vendor/`, third-party SDKs checked in. Affects build reproducibility.
- **Large binary artifacts in Git.** `git lfs ls-files`, files >100MB. May require LFS or split.
- **License files.** Note OSS licenses for downstream compliance.
- **Repo size and history depth.** Very large or very deep histories slow clone/CI; may need shallow clone strategy.

## Multi-Repo Engagements

If the application spans multiple repos:

1. Run this adapter once per repo
2. Aggregate into a single Capability Matrix with `source.secondary_adapters` listing the other repos
3. Capture inter-repo dependencies as `integrations` with `direction: bidirectional`
4. Route to Phase 0 (`/phase0-multi-repo-assessment`) before Phase 1

## Target Azure Mapping (signals)

Repo as a source doesn't dictate Azure target — that's downstream. But this adapter feeds:

- **Phase 5 / CI/CD:** repo platform (GitHub vs Azure DevOps) drives pipeline choice
- **Phase 3 / IaC:** existing IaC presence drives reuse vs greenfield
- **Phase 4 / Deploy:** existing Dockerfile drives container vs PaaS Code path

## Anti-Patterns

- Don't deep-clone if shallow works. `git clone --depth 50` is enough for fingerprinting.
- Don't read entire vendor directories. Skip `node_modules/`, `vendor/`, `Pods/`, `target/`.
- Don't infer architecture from README alone. The README is often stale. Cross-check against manifests and entry points.
- Don't classify based on the most recent commits. Look at the steady-state shape.

## Output Checklist

- [ ] Repo URL or path captured
- [ ] Branch model, last-activity, release cadence noted
- [ ] All build manifests inventoried (handoff to `stack-detection`)
- [ ] Existing CI/CD detected
- [ ] Containerization signals captured
- [ ] IaC presence captured
- [ ] Test surface noted
- [ ] Secrets-in-source check performed
- [ ] Monorepo flag set if applicable
- [ ] Evidence cells populated with file paths
