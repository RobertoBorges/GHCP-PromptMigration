# Microsoft Defender for Cloud and Compliance Readiness

Use this skill when hardening Azure workloads with Microsoft Defender for Cloud, Secure Score, Azure Policy, and regulatory control mapping.

## Use Cases

Apply this skill when the solution needs:

- security posture review after migration
- Defender plan recommendations by resource type
- Secure Score prioritization for remediation backlog
- regulatory compliance evidence for SOC 2, GDPR, PCI DSS, or ISO 27001
- continuous export of findings to SIEM, ticketing, or incident workflows

## What Defender for Cloud Covers

Microsoft Defender for Cloud reviews security posture across Azure resources and can extend into multicloud or hybrid scope where configured.

| Area | Typical Coverage |
|---|---|
| Compute | Defender for Servers, VM posture, vulnerability findings |
| Containers | Defender for Containers, AKS and image posture |
| Databases | SQL, OSS databases, data-service recommendations where supported |
| Storage | public access, malware and threat protections where enabled |
| App Service | web app exposure and configuration findings |
| Key Vault | access, diagnostics, and secret-store hardening signals |
| DNS | DNS-layer threat detections when plan coverage applies |
| ARM / control plane | policy drift, secure configuration, governance findings |

## Foundational CSPM vs Defender Plans

Do not treat all recommendations the same.

| Layer | Purpose | Action |
|---|---|---|
| Foundational CSPM / Secure Score | posture baseline and security hygiene | enable broadly |
| Defender plans | workload-specific threat protection and deeper signals | enable per resource type that matters |
| Azure Policy initiatives | enforceable governance and preventive control | use for guardrails and drift control |

Defender for Cloud is subscription-scoped in Azure, while enterprise enforcement is often driven from management groups with Azure Policy.

## Secure Score Guidance

Secure Score is a prioritization tool, not a compliance certificate.

Use it this way:

1. fix high-impact recommendations that reduce broad attack surface first
2. prioritize controls affecting internet-exposed or sensitive-data workloads
3. separate quick wins from architectural remediations
4. record accepted risks instead of chasing score alone

| Secure Score Pattern | Recommended Response |
|---|---|
| low score from many easy configuration gaps | batch quick wins this sprint |
| low score driven by legacy architecture | create a tracked hardening backlog |
| high score but unresolved critical alerts | treat alerts as higher priority than score optics |

## High-Impact Quick Wins

| Recommendation Type | Why It Matters | Typical Action |
|---|---|---|
| missing MFA or privileged access controls | identity compromise blast radius | enforce MFA and least-privilege admin roles |
| public data services | direct exposure of crown jewels | add private endpoint or scoped firewall |
| missing diagnostic settings | no audit trail or evidence | route logs to Log Analytics |
| unmanaged secrets | credential leakage and weak rotation | move to Key Vault and managed identity |
| missing Defender plan on critical resource type | blind spot in detections | enable relevant plan |

## Defender Plans by Resource Type

| Resource Type | Typical Plan Decision |
|---|---|
| VMs and hybrid servers | enable Defender for Servers for production workloads |
| AKS or containerized workloads | enable Defender for Containers |
| App Service web apps/APIs | enable Defender for App Service for public or critical apps |
| Azure SQL and SQL MI | enable Defender for SQL |
| Storage accounts | enable Defender for Storage where sensitive data or public access risk exists |
| Key Vault | enable relevant monitoring and alerting coverage |
| APIs behind API Management | align API security coverage with the exposure pattern |

## Regulatory Compliance Dashboard

Use the regulatory compliance dashboard to map posture against built-in initiatives.

| Standard | What to Use It For |
|---|---|
| SOC 2 | access control, logging, change management, incident response evidence |
| GDPR | privacy, retention, deletion workflow, residency, minimization discussions |
| PCI DSS | payment-related segmentation and control evidence |
| ISO 27001 | broad security management control mapping |

Do not claim certification from dashboard results alone. Use them as evidence and readiness signals.

## Alert Routing and Incident Ownership

Every high-severity recommendation or alert needs an owner.

Define:

- who triages Defender alerts
- where alerts land: email, Teams, ticketing, SIEM, or SOC queue
- what severity requires immediate escalation
- what constitutes accepted risk versus required remediation
- who closes the loop with evidence after remediation

## Diagnostic Settings and Audit Logs

Enable diagnostic settings for security-relevant resources and centralize retention.

```powershell
az monitor diagnostic-settings create --name appservice-to-law --resource $resourceId --workspace $lawId --logs '[{"categoryGroup":"allLogs","enabled":true}]' --metrics '[{"category":"AllMetrics","enabled":true}]'
```

Baseline expectations:

- Log Analytics workspace for searchable evidence
- retention aligned to regulatory or internal policy
- immutable or archival path where required
- audit trail for privileged changes and security events

## Azure Policy Enforcement

Use Azure Policy for preventive control, not just reporting.

| Policy Goal | Example Enforcement |
|---|---|
| HTTPS-only required | deny or audit web apps without HTTPS-only |
| Key Vault RBAC and diagnostics | audit or deny noncompliant vault settings |
| public IP or public DB restrictions | deny unsafe networking patterns |
| tagging and ownership | enforce resource owner and environment tags |

CLI pattern:

```powershell
az policy assignment create --name require-https --scope /subscriptions/$subscriptionId --policy $policyDefinitionId
```

## Continuous Export and SIEM Integration

Route findings where operators already work.

| Destination | Why |
|---|---|
| Log Analytics | default investigation and KQL workflows |
| Event Hub | stream to external SIEM |
| Storage | long-term archive or evidence retention |
| ticketing/SOC automation | assign incidents and remediation tasks |

Use continuous export or workflow automation so Defender findings do not stay trapped in the portal.

## SOC 2 Mapping

| SOC 2 Theme | Azure Hardening Evidence |
|---|---|
| Access control | Entra ID, RBAC, MFA, PIM, managed identity |
| Logging and monitoring | Log Analytics, diagnostic settings, App Insights, Defender alerts |
| Change management | IaC, pull request review, policy assignments, deployment records |
| Incident response | alert routing, ownership, runbooks, escalation path |

## GDPR Mapping

| GDPR Concern | Azure Hardening Evidence |
|---|---|
| Data minimization | store only required data and review telemetry payloads |
| Retention | log retention and deletion policies documented |
| Deletion workflows | operational runbooks and app data deletion capability |
| Regional handling | approved Azure region selection and residency notes |
| Privacy controls | access reviews, encryption, audit trails, least privilege |

## Compliance Reporting and Evidence Collection

Capture evidence continuously, not only before audit.

Recommended evidence set:

- Defender recommendations and remediation history
- Secure Score trend over time
- Azure Policy compliance state
- diagnostic setting configuration snapshots
- alert routing ownership list
- screenshots or exports only when a durable system record is unavailable

## Common Anti-Patterns

Treat these as quality gaps:

- treating Secure Score as the end goal instead of risk reduction
- enabling no Defender plans on production subscriptions
- relying on portal screenshots without durable logs or policy state
- unclear incident owner for high-severity findings
- claiming SOC 2 or GDPR compliance without control evidence and legal review

## Validation Checklist

- relevant Defender plans are enabled for each production resource type
- Secure Score recommendations are prioritized by risk, not vanity score
- regulatory dashboard findings are mapped to real owners and evidence
- diagnostic settings feed Log Analytics or approved downstream systems
- Azure Policy enforces core security controls where possible
- continuous export or workflow automation exists for incident handling

## Output Expectations for Prompts

When this skill is applied, the prompt should:

- explain what Defender for Cloud covers for the workload in scope
- identify which Defender plans to enable and why
- prioritize Secure Score and recommendation fixes into a remediation backlog
- map SOC 2 and GDPR expectations to concrete Azure controls and evidence
- state clearly that posture and readiness are being assessed, not certification granted
