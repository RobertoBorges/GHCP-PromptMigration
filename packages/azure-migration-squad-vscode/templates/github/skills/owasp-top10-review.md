# OWASP Top 10 Review for Azure Migrations

Use this skill when performing a security review of a migrated application, API, or supporting Azure platform configuration against the OWASP Top 10 (2021).

## Use Cases

Apply this skill when the solution needs:

- post-migration security review before production sign-off
- risk-ranked review of app code, config, identity, and Azure infrastructure
- Azure-specific remediation guidance tied to OWASP categories
- evidence collection for security reports, go/no-go reviews, or audit readiness

## Review Method

For each OWASP category:

1. inspect evidence in code, configuration, IaC, and Azure resource settings
2. rate severity based on exploitability, exposure, and data sensitivity
3. recommend Azure-specific remediation steps
4. define how the fix will be validated

## Severity Guidance

| Severity | When to Use |
|---|---|
| 🔴 Critical | internet-exploitable auth bypass, exposed secrets, public admin path, or highly likely compromise path |
| 🟠 High | strong privilege escalation path, public data exposure, missing encryption, or exploitable vulnerable component |
| 🟡 Medium | issue requires chaining, limited exposure, or defense-in-depth gap |
| 🟢 Low | low-likelihood hardening improvement or documentation/control gap |

## OWASP Top 10 Review Table

| Category | Azure-Specific Evidence to Inspect | Typical Migration Findings | Severity Guidance | Remediation |
|---|---|---|---|---|
| **A01: Broken Access Control** | Entra ID app registrations, API scopes, app roles, RBAC assignments, App Service auth settings, admin endpoints, storage/database permissions | anonymous admin routes, coarse `Contributor` assignments, missing API authorization policy, shared service principals | Critical if privilege escalation or unauthenticated access exists; High if over-privileged roles expose sensitive data | use Entra ID, enforce scopes/app roles, replace shared credentials with managed identity, apply least-privilege RBAC, remove public admin surfaces |
| **A02: Cryptographic Failures** | TLS settings, Key Vault usage, certificate source, encryption-at-rest settings, app secrets, cookie settings | TLS 1.0/1.1 leftovers, secrets in config, self-signed prod certs, weak cookie protection, unmanaged cert expiry | Critical for exposed secrets or plaintext sensitive data; High for weak transport or key handling | store secrets and certs in Key Vault, enforce TLS 1.2+, enable encryption defaults, rotate keys/certs, review cookie flags and token protection |
| **A03: Injection** | SQL queries, ORM usage, shell execution, deserialization, request validation, WAF logs | string-concatenated SQL, unsafe dynamic queries, command injection risk, missing request validation on legacy MVC or Java endpoints | Critical if exploitable on internet-facing write paths; High for authenticated but reachable business paths | use parameterized queries, input validation, output encoding, safer ORM patterns, WAF coverage for public apps, code review of dangerous sinks |
| **A04: Insecure Design** | threat models, trust boundaries, privilege assumptions, architecture diagrams, secret and network design | no abuse-case review, admin features mixed with public paths, broad network trust, no compensating controls during staged migration | High when the design creates structural exposure even without a single bug; Medium when mitigations partially exist | perform threat modeling, separate trust zones, enforce least privilege, add defense in depth, document high-risk assumptions and retirement dates |
| **A05: Security Misconfiguration** | Defender recommendations, NSGs, CORS rules, verbose errors, default credentials, public endpoints, container base config | wildcard CORS, public SQL, debug pages enabled, broad NSG rules, missing HTTPS-only, unrestricted storage access | Critical for public admin or data-plane exposure; High for internet-facing misconfigurations; Medium for internal drift | apply secure defaults, close public endpoints, restrict CORS, turn off debug detail, enable Defender recommendations and policy guardrails |
| **A06: Vulnerable and Outdated Components** | package manifests, lockfiles, container images, base image tags, Dependabot alerts, GHAS findings | unsupported framework packages, vulnerable NuGet/Maven/npm dependency, `latest` container base image, no image scanning | High when a known reachable CVE affects public or privileged components; Medium for lower exposure libraries | run Dependabot and package audits, pin versions, scan images, upgrade unsupported libraries, track exceptions with owner and deadline |
| **A07: Identification and Authentication Failures** | token validation code, redirect URIs, MFA posture, session config, password flows, legacy auth remnants | forms auth left active, improper JWT validation, weak session timeout, local admin accounts, missing MFA for privileged users | Critical if auth can be bypassed or tokens are improperly trusted; High for weak admin auth or legacy fallback paths | migrate to Entra ID, validate issuer/audience/signing keys, require MFA for admins, remove legacy auth paths, harden session/token lifecycle |
| **A08: Software and Data Integrity Failures** | CI/CD controls, artifact provenance, signed packages, deployment permissions, SBOM, branch protections | unreviewed pipeline secrets, mutable build artifacts, unsigned packages, no SBOM, overly broad deployment credentials | High when attackers could tamper with builds or deployments; Medium when visibility is weak but controls partially exist | protect pipelines, require PR review, sign artifacts where possible, generate SBOM, reduce deployment permissions, secure GitHub Actions/Azure credentials |
| **A09: Security Logging and Monitoring Failures** | Application Insights, Log Analytics, diagnostic settings, audit logs, alert rules, incident ownership | no correlation IDs, missing audit logs, no alert for auth failures, logs without retention, no owner for Defender alerts | High if active attacks would go unseen; Medium for partial telemetry gaps | enable App Insights and diagnostic settings, centralize logs in Log Analytics, alert on auth and secret events, define ownership and retention |
| **A10: Server-Side Request Forgery (SSRF)** | outbound HTTP client code, metadata endpoint access, private resource access patterns, NSG and firewall egress rules | app can reach IMDS `169.254.169.254`, unrestricted outbound calls, internal admin APIs reachable from app tier, no egress policy | Critical if SSRF exposes managed identity tokens or internal control planes; High for broad internal reachability | restrict outbound access, block unnecessary IMDS exposure paths, prefer private endpoints, add allowlisted egress, validate and constrain outbound URLs |

## Category-Specific Review Notes

### A01: Broken Access Control

Look for route-level authorization, API policy enforcement, RBAC scope, and whether workload identity is separated from user identity.

### A02: Cryptographic Failures

Check certificate source, expiry handling, TLS minimums, and whether secrets still exist outside Key Vault.

### A03: Injection

Prioritize data entry points, search endpoints, report filters, and legacy SQL access layers.

### A04: Insecure Design

Flag designs that rely on trusted internal networks, shared admin accounts, or one giant app identity.

### A05: Security Misconfiguration

Use Microsoft Defender for Cloud, Azure Policy, and platform defaults to find drift quickly.

### A06: Vulnerable and Outdated Components

Review app packages, container bases, OS patching state, and unsupported framework dependencies together.

### A07: Identification and Authentication Failures

Validate token issuer, audience, clock skew, logout behavior, admin protections, and legacy fallback paths.

### A08: Software and Data Integrity Failures

Check deployment provenance, environment protection rules, release approvals, and artifact immutability.

### A09: Security Logging and Monitoring Failures

Logs must support investigation: who did what, from where, against which resource, and what happened next.

### A10: SSRF

Treat access to metadata endpoints and internal-only Azure services as high risk even if the original bug looks small.

## Detection Tools

| Tool | Best Use |
|---|---|
| Microsoft Defender for Cloud | posture gaps, misconfiguration signals, plan-based threat detections |
| GitHub Advanced Security / CodeQL | code-level security findings, injection patterns, credential exposure, auth mistakes |
| GitHub secret scanning | repository and push-time credential detection |
| Dependabot | vulnerable package detection and upgrade flow |
| container image scanning | base image and OS package risk detection |
| Application Insights + Log Analytics | validation of logging, alerting, and investigation readiness |

## Evidence Checklist

Collect evidence from:

- source code and dependency manifests
- IaC files and deployment pipelines
- Azure configuration: identity, RBAC, networking, TLS, diagnostics
- Defender recommendations and alerts
- GitHub security findings, secret scanning alerts, and dependency alerts
- application logs, audit logs, and incident ownership records

## Validation Checklist

- all 10 OWASP categories were reviewed explicitly
- evidence exists for every severity rating
- remediation steps are Azure-specific and actionable
- detection tooling covers code, dependencies, platform, and runtime signals
- critical and high findings have clear owners and validation steps

## Output Expectations for Prompts

When this skill is applied, the prompt should:

- produce a full 10-category OWASP review table with evidence, severity, and remediation
- connect findings to Azure controls such as Entra ID, Key Vault, RBAC, WAF, NSG, private endpoints, and App Insights
- highlight Defender for Cloud, GitHub Advanced Security, CodeQL, GitHub secret scanning, and Dependabot as detection sources
- require explicit secret scanning and dependency review evidence in addition to the OWASP findings
- rank issues by production risk, not just by checklist completion
- make the go/no-go recommendation depend on unresolved critical and high findings
