# Azure Network Security and Perimeter Controls

Use this skill when reviewing or designing network isolation, ingress controls, egress controls, TLS posture, and segmentation for Azure-hosted applications.

## Use Cases

Apply this skill when the solution needs:

- internet-facing web security controls for migrated apps or APIs
- private connectivity to databases, storage, Key Vault, or internal services
- PaaS network isolation for App Service, Container Apps, SQL, Storage, or Key Vault
- review of NSGs, firewall rules, WAF, TLS, and IP restrictions
- remediation of public exposure or overly permissive network rules

## Core Rules

Default to least exposure.

- public ingress only when business traffic requires it
- private endpoints for data services in production
- deny-by-default NSG posture
- HTTPS-only with TLS 1.2 or later
- no open admin ports to the internet

## Network Segmentation Pattern

| Tier | Common Azure Services | Expected Network Control |
|---|---|---|
| Edge | Front Door, Application Gateway, WAF, CDN | only internet-facing tier |
| App | App Service, Container Apps, Functions, AKS | ingress restricted, outbound routed intentionally |
| Data | Azure SQL, PostgreSQL, Storage, Key Vault | private endpoint or tightly scoped firewall |
| Management | Bastion, jump host, automation, monitoring | no public admin plane from arbitrary IPs |

## NSG Guidance

Use NSGs to control subnet and NIC traffic.

Important facts:

- valid custom priorities are `100` to `4096`
- lower number wins
- first matching rule applies
- default rules still exist at priorities `65000`, `65001`, and `65500`

| Priority Example | Rule | Why |
|---|---|---|
| `100` | allow Front Door/App Gateway to web tier | explicit trusted ingress |
| `200` | allow app tier to data tier on required ports only | least-privilege east-west traffic |
| `300` | allow monitoring or management flows | operational access |
| `4000` | deny broad or legacy traffic that is still being phased out | transition control |

Do not create wildcard `Allow *` rules unless the environment is disposable and the exception is documented.

## NSG Bicep Pattern

```bicep
resource webNsg 'Microsoft.Network/networkSecurityGroups@2023-09-01' = {
  name: 'nsg-web-prod'
  location: location
  properties: {
    securityRules: [
      {
        name: 'AllowHttpsFromFrontDoor'
        properties: {
          priority: 100
          direction: 'Inbound'
          access: 'Allow'
          protocol: 'Tcp'
          sourceAddressPrefix: 'AzureFrontDoor.Backend'
          sourcePortRange: '*'
          destinationAddressPrefix: '*'
          destinationPortRange: '443'
        }
      }
    ]
  }
}
```

## Private Endpoints

Use private endpoints for high-value PaaS dependencies.

| Service | Private Endpoint | Notes |
|---|---|---|
| Azure SQL / SQL Managed Instance | yes | default production choice for private app tiers |
| Storage | yes | use for blob, file, queue, and table access where isolation matters |
| Key Vault | yes | strongly recommended for production secret stores |
| Cosmos DB | yes | use with private DNS planning |
| App Service | partial | private endpoint for inbound access; separate VNet integration handles outbound |
| Container Apps environment dependencies | depends on architecture | combine internal environments, UDR, and private service access |

Plan for private DNS zones and name resolution before enabling private endpoints.

## Service Endpoints vs Private Endpoints

| Requirement | Prefer | Why |
|---|---|---|
| Eliminate public exposure to a PaaS resource | Private Endpoint | resource gets a private IP in your VNet |
| Lightweight subnet-scoped access to supported Azure services | Service Endpoint | simpler but still uses public service endpoint model |
| Strong compliance boundary or exfiltration concern | Private Endpoint | tighter isolation and private DNS control |
| Temporary hardening for legacy subnet-based access | Service Endpoint | acceptable only when private endpoint is not yet feasible |

Service endpoints do not make the resource private; they only restrict access to selected subnets.

## WAF Selection

Use a WAF for public-facing applications.

| Service | Use When | Notes |
|---|---|---|
| Azure Front Door WAF | global edge entry, CDN, multi-region routing | best default for internet-facing apps with global users |
| Application Gateway WAF | regional ingress, VNet-local apps, internal L7 routing | strong fit for regional apps and private backends |
| No WAF | only for private-only or tightly controlled internal workloads | document the reason |

Run WAF in detection mode only for tuning windows. Production should move to prevention mode.

## TLS Enforcement

Enforce HTTPS and modern TLS everywhere.

### App Service

```powershell
az webapp update --name app-contoso-prod --resource-group rg-contoso-prod --set httpsOnly=true
az webapp config set --name app-contoso-prod --resource-group rg-contoso-prod --min-tls-version 1.2
```

### Container Apps

```bicep
configuration: {
  ingress: {
    external: true
    targetPort: 8080
    allowInsecure: false
  }
}
```

Certificate rules:

- centralize certificate ownership
- prefer managed certificates where the platform supports them
- use Key Vault-backed certificates when multiple services or custom automation require it
- never leave expired or self-signed production certs in place without an approved exception

## IP Restrictions

Use IP restrictions when the app should only accept trusted ingress.

### App Service access restriction

```powershell
az webapp config access-restriction add --resource-group rg-contoso-prod --name app-contoso-prod --rule-name AllowCorpEgress --action Allow --ip-address 203.0.113.0/24 --priority 200
```

### Container Apps ingress restriction pattern

```bicep
ingress: {
  external: true
  allowInsecure: false
  targetPort: 8080
  ipSecurityRestrictions: [
    {
      name: 'AllowCorpEgress'
      action: 'Allow'
      ipAddressRange: '203.0.113.0/24'
    }
    {
      name: 'DenyAll'
      action: 'Deny'
      ipAddressRange: '0.0.0.0/0'
    }
  ]
}
```

If access is global or dynamic, prefer Front Door or App Gateway with WAF rather than maintaining large allowlists directly on the app.

## VNet Integration for PaaS

| Service | What It Solves | Limitation |
|---|---|---|
| App Service VNet integration | private outbound connectivity from app to VNet resources | not the same as inbound private access |
| App Service private endpoint | private inbound access to the site | pair with VNet integration for full private patterns |
| Container Apps environment networking | subnet-based deployment, private ingress, controlled egress | requires environment-level design early |
| Functions on App Service plan | same patterns as App Service | validate storage and Key Vault connectivity |

## Azure Firewall vs NSG

| Control | Use For | Not a Replacement For |
|---|---|---|
| NSG | subnet/NIC allow-deny filtering | application-layer inspection or centralized egress policy |
| Azure Firewall | centralized egress filtering, DNAT, FQDN rules, policy management | subnet-local micro-segmentation |

Use NSGs for local segmentation. Use Azure Firewall when multiple subnets or workloads need shared egress control, threat intel, or central policy.

## DDoS Protection

| Option | When to Use |
|---|---|
| Basic | default platform coverage for all public Azure endpoints |
| Standard | business-critical public workloads needing telemetry, tuning, cost protection, and incident support |

DDoS Standard is most relevant when the workload has significant public exposure or formal resilience requirements.

## Common Anti-Patterns

Treat these as hardening findings:

- Azure SQL, PostgreSQL, or Storage left open to all public IPs
- inbound `3389` or `22` exposed to the internet
- NSG rules with `source=*` and `destination=*` for convenience
- public Key Vault or admin endpoints with no justification
- no private DNS planning for private endpoints
- assuming service endpoints provide the same isolation as private endpoints

## Validation Checklist

- public ingress is justified and documented
- WAF placement is defined for public web traffic
- NSG rules are ordered intentionally and avoid broad wildcards
- data-tier services use private endpoints or tightly scoped network controls
- HTTPS-only and TLS 1.2+ are enforced
- App Service or Container Apps ingress restrictions match the intended audience
- management access uses Bastion, JIT, or equivalent controlled paths

## Output Expectations for Prompts

When this skill is applied, the prompt should:

- describe the expected network boundary for edge, app, data, and management tiers
- choose between private endpoints and service endpoints with explicit reasoning
- call out NSG, WAF, TLS, and IP restriction requirements concretely
- flag public databases, open admin ports, and wildcard rules as high risk
- produce Azure-ready remediation steps for App Service and Container Apps networking
