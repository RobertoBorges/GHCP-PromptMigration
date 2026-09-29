# 🎯 WCF Service Migration — CLI Walkthrough

> **Source:** WCF .NET 3.5 (SOAP, ServiceContract) | **Target:** REST API + Azure Container Apps
> **Roles involved:** The Architect, The Coder, The Azure Specialist, The Performance Engineer, The Security Auditor, The Tester
> ⚠ **The target runtime shown above is an example, not a default.** `/phase1-plan` presents supported LTS options with tradeoffs and records your answer in `reports/Decisions-Required.md`. Later steps hard-stop until that decision is `✅ DECIDED`.

## How This Works

```mermaid
flowchart LR
    A[WCF SOAP services] --> B{The Architect<br/>Assesses contracts}
    B --> C[The Coder<br/>Builds .NET 8 REST API]
    C --> D[The Azure Specialist<br/>Prepares Container Apps]
    C --> E[The Performance Engineer<br/>Checks API shape and scale]
    D --> F[Deploy containers]
    E --> F
    F --> G[DevOps Engineer + Tester<br/>CI/CD and validation]
```

## Prerequisites

- [ ] Copilot CLI is available and signed in
- [ ] Azure CLI and AZD are installed and authenticated
- [ ] .NET 8 SDK is installed
- [ ] Docker Desktop is available for container validation
- [ ] The sample exists at `Use-cases/03-WCFNet35`
- [ ] You can inspect `WCFDemo.Service`, `WCFDemo.Host`, and `WCFDemo.Client`

## The Full Migration (One Shot)

> For teams that want one prompt to start the whole redesign:

```text
@agent Migrate Use-cases/03-WCFNet35 from WCF .NET 3.5 to a .NET 8 REST API on Azure Container Apps. Assess the SOAP contracts, redesign the service surface, modernize the host, define the client transition, generate container-ready Azure infrastructure, deploy it, and set up CI/CD. Fan out contract mapping, API conversion, platform design, and validation.
```

**What happens:** The Architect scopes the redesign, the Coder rebuilds the API, the Azure Specialist prepares Azure, and the Performance Engineer keeps an eye on scale and fit.
**You'll get:** Assessment reports, REST design guidance, modernized API code, container-ready infrastructure, deployment output, and release guidance.

## Step by Step

### Step 1: Discovery — triage (`/assess-any-application`)

```text
@agent Give me a fast triage for Use-cases/03-WCFNet35. Review WCFDemo.Service, WCFDemo.Host, and WCFDemo.Client separately, identify the hardest SOAP contracts, note binding or hosting blockers, and tell me what will break for clients when we move to REST.
```

**What happens:** The Architect decides whether the job is a clean translation or a deeper service redesign.
**You'll get:** A feasibility summary, the hardest contract risks, and the best next move.
**Follow-up if needed:**

```text
@agent Explain which ServiceContract or client dependency creates the most migration risk and why it cannot stay exactly as-is.
```

### Step 2: Plan — assessment (`/phase1-plan`)

```text
/assess-any-application Use-cases/03-WCFNet35. Map ServiceContract and OperationContract usage, binding assumptions, config dependencies, host behavior, client proxy impact, auth expectations, and Azure Container Apps fit. Fan out architecture, security, and performance review.
```

**What happens:** The Architect runs the readout while the Security Auditor checks exposure and the Performance Engineer looks for API shape or scaling traps.
**You'll get:** `reports/Quick-Assessment-Report.md`, `reports/WCF-Migration-Report.md`, `reports/Application-Assessment-Report.md`, and `reports/Report-Status.md`.
**Follow-up if needed:**

```text
@agent Show me the top three service redesign risks and tell me which contract should become the first REST endpoint.
```

### Step 3: Migrate code (`/phase2-migrate-code`)

```text
@agent Start the migration for Use-cases/03-WCFNet35. Convert the WCF service to a .NET 8 REST API, map contracts to endpoints and DTOs, replace SOAP-specific assumptions, modernize configuration, and define how WCFDemo.Client should transition to HttpClient or an OpenAPI-based client.
```

**What happens:** The Coder replaces the SOAP surface, turning service contracts into HTTP endpoints, and keeps the host and client transition explicit.
**You'll get:** Modernized API code, endpoint mapping notes, client transition guidance, and build-readiness feedback.
**Follow-up if needed:**

```text
@agent Walk me through how the SOAP operations were mapped to HTTP verbs, status codes, and DTOs, and tell me where parity is intentionally different.
```

### Step 4: Generate infrastructure (`/phase3-generate-infra`)

```text
@agent Generate the Azure platform for the new REST API. Use Azure Container Apps, container registry, Key Vault, managed identity, and Application Insights. Keep the output ready for azd and show me any assumptions about ingress, secrets, and revisions.
```

**What happens:** The Azure Specialist sets up the container escape route and makes the new API deployable without guesswork.
**You'll get:** `infra/`, `azure.yaml`, container platform guidance, secret handling notes, and updated status tracking.
**Follow-up if needed:**

```text
@agent Explain why Container Apps is the right landing zone and show me how ingress, identity, and telemetry are wired.
```

### Step 5: Deploy to Azure (`/phase4-deploy-to-azure`)

```text
@agent Deploy the migrated REST API for Use-cases/03-WCFNet35 to Azure Container Apps when the platform is ready. Confirm endpoint reachability, summarize smoke tests, and document rollback points before sign-off.
```

**What happens:** The team ships the new API and makes sure the live surface is reachable and reversible.
**You'll get:** Deployment output, endpoint summary, smoke-test notes, and rollback guidance.
**Follow-up if needed:**

```text
@agent If deployment fails, tell me whether the problem is image build, container config, ingress, secrets, or code, and give me the fastest recovery path.
```

### Step 6: Set up CI/CD (`/phase5-setup-cicd`)

```text
@agent Set up CI/CD for Use-cases/03-WCFNet35. Include build, container image creation, API tests, security checks, Azure deployment, and release gates that protect contract changes and endpoint health.
```

**What happens:** The DevOps Engineer automates the route to production and Linus verifies the health checks actually mean something.
**You'll get:** `reports/cicd_setup_report.md`, pipeline guidance, image and release flow, and validation gates.
**Follow-up if needed:**

```text
@agent Show me how the pipeline proves the REST API is healthy before production and where contract-breaking changes should be caught.
```

## Step 7: Post-migration ops and final validation (`/phase6-post-migration-ops`)

```text
/get-status Use-cases/03-WCFNet35. Confirm the build passes, SOAP contracts are mapped, the REST API is deployable, Container Apps health is clean, CI/CD is wired, the client transition is documented, and the first-day monitoring and rollback checklist is ready.
```

**What happens:** The Tester closes the loop while the Performance Engineer and Security Auditor keep an eye on performance and exposure.
**You'll get:** A release-readiness summary, open risks, and the first operational watch list.
**Follow-up if needed:**

```text
@agent Tell me what to watch in the first release window for latency, error rates, ingress failures, and client breakage.
```

## Expected Artifacts

- `reports/Quick-Assessment-Report.md`
- `reports/WCF-Migration-Report.md`
- `reports/Application-Assessment-Report.md`
- `reports/Report-Status.md`
- Modernized .NET 8 REST API code
- Client transition guidance for `WCFDemo.Client`
- `infra/`
- `azure.yaml`
- `reports/cicd_setup_report.md`
- Deployment, validation, and rollback guidance

## 💡 Power-User Shortcut

> CLI-first follow-through commands:
> Assessment → `/phase1-plan` | Code → `/phase2-migrate-code` | Infra → `/phase3-generate-infra`
> Deploy → `/phase4-deploy-to-azure` | CI/CD → `/phase5-setup-cicd`
> Optional hardening → `/security-hardening` | Optional cost review → `/cost-optimization`
