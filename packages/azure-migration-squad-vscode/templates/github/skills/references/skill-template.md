# Skill Templates — copy-paste starters for `skill-creator`

> Loaded on demand by `.github/skills/skill-creator.md`. Six family templates for creating a new skill on the fly. Copy the section matching the target family, then fill in the placeholders. All templates follow the anatomy in `references/skill-anatomy.md`.

## Placeholder legend

Anywhere you see `<X>` or `<X.Y>` in the templates below, replace with real content. Never ship a skill with unfilled placeholders.

- `<name>` — short kebab-case name for the skill (`elixir`, `nutanix`, `iot-edge`)
- `<Name>` — human-readable title-case (`Elixir`, `Nutanix AHV`, `IoT Edge`)
- `<family>` — one of `stack`, `source`, `workload`, `integration`, `pattern`, `risk`
- `<triggers>` — comma-separated capability-matrix values or keywords
- `<citation>` — a real URL from Step 3 research

---

## Template — stack

Filename: `.github/skills/stack-<name>.md`

```markdown
---
name: stack-<name>
description: Stack adapter for <Name> applications. Load whenever Capability-Matrix.stack.primary_stack is `<name>`, or when discovery finds <specific file patterns>, OR when the user mentions <Name>, <framework 1>, <framework 2>, or <keyword> in a migration context. Covers version upgrade paths (<from-version> → <to-version>), Azure hosting options (<Azure services>), authentication modernization to Entra ID, observability wiring to Application Insights, and Azure-compatibility gotchas specific to <Name>.
family: stack
triggers: <name>, <framework 1>, <framework 2>, <keyword>
---

# Skill: Stack Adapter — <Name>

> <One-paragraph overview: what apps this covers, common variants, why it matters for Azure migration.>

## When to Use

- `stack.primary_stack: <name>` in the Capability Matrix
- File evidence: <list glob patterns — e.g., `*.ex`, `mix.exs`, `*.eex`>
- Keywords in user intent: <keywords>

## Sub-Stack Detection

| Sub-stack | Detection signal | Typical Azure target |
|-----------|------------------|----------------------|
| **<variant 1>** | <how to detect> | <App Service Linux / Container Apps / Functions / AKS> |
| **<variant 2>** | <how to detect> | <target> |
| **<variant 3>** | <how to detect> | <target> |

## Version Compatibility with Azure

| Current version | Azure PaaS support | Recommended target | Notes |
|-----------------|--------------------|--------------------|-------|
| <version X> | ❌ unsupported | <target version> | <breaking changes to expect> |
| <version Y> | ⚠️ container only | <target version> | <containerize path> |
| <version Z> | ✅ App Service Linux | (stay) | <notes> |

## Migration Patterns

### Rehost (containerize, no code changes)
- <specific pattern for this stack — e.g., "Use official `<name>:<version>` base image, expose <default port>, add health-check endpoint">
- Blockers: <list — e.g., "native BEAM clustering across nodes needs Container Apps VNet integration">

### Replatform (upgrade runtime + minimal changes)
- <specific pattern — e.g., "Upgrade Elixir 1.14 → 1.17, keep Phoenix version, add Application Insights auto-instrumentation">
- Blockers: <list>

### Refactor (code changes + PaaS optimization)
- <specific pattern>
- Blockers: <list>

## Configuration Transformation

Swap on-prem-style config for Azure-native equivalents:

| On-prem | Azure equivalent | Migration approach |
|---------|------------------|--------------------|
| <local config file> | <Environment variables + Key Vault reference> | <how> |
| <in-process cache> | <Azure Cache for Redis> | <how> |
| <local file share> | <Azure Files / Blob Storage> | <how> |

## Authentication → Entra ID

- SDK: <name of the language's Azure Identity SDK — e.g., `azure_identity` gem for Ruby, `@azure/identity` for Node, `azure-identity` for Python>
- Recommended pattern: <DefaultAzureCredential / ClientSecretCredential / Managed Identity Credential>
- Sample code: <minimal snippet>

## Observability → Application Insights

- Recommended: <OpenTelemetry package name> + <OTLP endpoint>
- Alternative: <native App Insights SDK if applicable>
- Log correlation: <how to preserve trace IDs across service boundaries>

## Tradeoffs

| Strategy | When to pick | When to avoid |
|----------|--------------|---------------|
| Rehost | <criteria> | <criteria> |
| Replatform | <criteria> | <criteria> |
| Refactor | <criteria> | <criteria> |
| Rearchitect | <criteria> | <criteria> |

## Common Gotchas

- <specific gotcha 1 — e.g., "BEAM's distributed Erlang cookie must be sourced from Key Vault, not baked into the image">
- <specific gotcha 2>
- <specific gotcha 3>

## References

- <citation 1: official language docs>
- <citation 2: Azure hosting docs for this stack>
- <citation 3: migration guide from a reputable source>
- <citation 4: LTS release notes>
- <citation 5: real-world case study>
```

---

## Template — source

Filename: `.github/skills/source-<name>.md`

```markdown
---
name: source-<name>
description: Source-environment adapter for <Name>. Load whenever Capability-Matrix.source.primary_adapter is `<name>`, OR when the user mentions <Name>, <variant 1>, <variant 2> as the current hosting environment. Covers extracting code / config / data from <Name>, Azure landing-zone options, common blockers, and when to escalate to specialist tooling.
family: source
triggers: <name>, <alt-name>, <keyword>
---

# Skill: Source Adapter — <Name>

> <One-paragraph overview: what this source is, who typically runs it, common characteristics.>

## When to Use

- `source.primary_adapter: <name>` in the Capability Matrix
- User describes their current environment as <Name> or one of the aliases: <list>
- File evidence indicative of <Name>: <list>

## Access Method

How to extract code + config + data from this source:

- **Code extraction**: <method — e.g., "Rehost as VM image via Azure Migrate; use vendor export tooling for filesystem snapshots">
- **Config extraction**: <method>
- **Data extraction**: <method — e.g., "IBM DB2 → Azure SQL via Azure DMS with pre-migration schema conversion">

## Discovery Approach

Before migrating, inventory:

- <what to catalog: OS version, hardware profile, runtime dependencies>
- <application inventory: LPARs, jobs, batch schedules>
- <integration inventory: MQ queues, external partners, file feeds>
- <data volumes, retention policies, regulatory constraints>

## Azure Landing Zone Options

| Azure target | When to pick | Compatibility gotchas |
|--------------|--------------|-----------------------|
| **Azure VMs** | <criteria — e.g., "you need custom kernel or specialty hardware"> | <notes> |
| **Azure VMware Solution (AVS)** | <criteria> | <notes> |
| **Azure PaaS (App Service / Container Apps)** | <criteria — e.g., "workload can run in a modern Linux container"> | <notes> |
| **Azure AKS** | <criteria> | <notes> |

## Common Blockers

- <blocker 1: e.g., "Cross-region latency to on-prem AD if identity stays on-prem">
- <blocker 2>
- <blocker 3>

## Escalation Path

If discovery reveals conditions this skill can't handle, escalate to:

- **<Specialist tool or partner 1>** — for <specific scenario>
- **<Specialist tool or partner 2>** — for <specific scenario>
- **`source-unsupported-escalation.md`** — for SaaS-embedded code

## References

- <citation 1: vendor documentation>
- <citation 2: Azure Migrate compatibility matrix>
- <citation 3: migration case study>
- <citation 4: escalation-partner reference>
```

---

## Template — workload

Filename: `.github/skills/workload-<name>.md`

```markdown
---
name: workload-<name>
description: Workload-pattern adapter for <Name> applications. Load whenever Capability-Matrix.workload.primary_pattern is `<name>`, OR when the workload has these characteristics: <list — e.g., "sub-millisecond latency, MQTT protocol, gateway-to-cloud pattern, edge compute nodes">. Covers Azure hosting options for this pattern, migration approach per 6Rs strategy, data + state considerations, and cutover patterns specific to <Name>.
family: workload
triggers: <name>, <keyword 1>, <keyword 2>
---

# Skill: Workload Adapter — <Name>

## When to Use

- `workload.primary_pattern: <name>` in the Capability Matrix
- Workload shape matches: <describe traffic pattern, latency, scale, protocol>

## Workload Shape

| Attribute | Typical value | Notes |
|-----------|---------------|-------|
| Traffic pattern | <e.g., "bursty request/response", "streaming", "batch nightly"> | |
| Latency budget | <e.g., "<10ms p99"> | |
| Scale | <e.g., "10k concurrent connections", "1M events/hour"> | |
| Data volume | <e.g., "100 GB/day incoming"> | |
| Protocol | <e.g., "MQTT 5.0", "HTTP/2 + gRPC", "AMQP 1.0"> | |

## Azure Targets

| Option | Best for | Tradeoffs |
|--------|----------|-----------|
| **<Azure service 1>** | <criteria> | <cost / limits> |
| **<Azure service 2>** | <criteria> | <cost / limits> |
| **<Azure service 3>** | <criteria> | <cost / limits> |

## Migration Approach per Strategy

Note: default is **replatform** or **refactor** — minimum viable Azure compatibility. Do NOT default to rearchitect.

| Strategy | Phase 2 emphasis | Phase 3 emphasis | Phase 6 emphasis |
|----------|------------------|------------------|-------------------|
| Rehost | <what code changes> | <what infra> | <what ops> |
| Replatform | <what code changes> | <what infra> | <what ops> |
| Refactor | <what code changes> | <what infra> | <what ops> |
| Rearchitect | <what code changes — only if user explicitly picks this> | <what infra> | <what ops> |
| Rebuild | Greenfield | Greenfield | Greenfield |

## Data + State Considerations

- <what state / data must be preserved during cutover>
- <what state can be reset>
- <externalization strategy — Redis, Blob Storage, Cosmos, etc.>

## Cutover Pattern

- <blue-green vs canary vs cutover-window vs traffic-shift>
- <rollback triggers>
- <smoke-test suite>

## References

- <citation 1: Azure Well-Architected Framework guidance for this workload>
- <citation 2: Azure Architecture Center reference architecture>
- <citation 3: real-world case study>
- <citation 4: CNCF landscape or standards body reference if applicable>
```

---

## Template — integration

Filename: `.github/skills/integration-<name>.md`

```markdown
---
name: integration-<name>
description: Integration adapter for <Name>. Load whenever `<name>` appears in Capability-Matrix.integrations[], OR when Discovery finds evidence of <Name> in the app (<protocol markers, client-library dependencies, config keys>). Covers protocol/transport specifics, Azure equivalents, migration approach (in-place adapter vs replatform vs replace), and security + identity considerations.
family: integration
triggers: <name>, <alt-name>, <keyword>
---

# Skill: Integration Adapter — <Name>

## When to Use

- `integrations: [..., <name>, ...]` in the Capability Matrix
- Evidence in the codebase: <SDK imports, config keys, connection strings, protocol libraries>

## Protocol / Transport

- Protocol: <e.g., "AMQP 1.0", "MQ RFH2 headers", "SAP RFC">
- Transport: <TCP/UDP, HTTP, custom>
- Authentication: <how the client authenticates today>

## Azure Equivalents

| Azure service | Best fit for | Migration effort |
|---------------|--------------|------------------|
| **<Azure Service Bus / Event Grid / Event Hubs / Logic Apps / APIM / etc.>** | <use-case> | <low/medium/high> |
| **<Alternative>** | <use-case> | <low/medium/high> |
| **<Alternative>** | <use-case> | <low/medium/high> |

## Migration Approach

### Option 1: In-place adapter (keep the client, swap the server)
- <steps>
- Blockers: <list>

### Option 2: Replatform (move the integration to Azure equivalent)
- <steps>
- Blockers: <list>

### Option 3: Replace (retire the integration entirely; use a different pattern)
- <steps>
- When to pick: <criteria>

## Security + Identity Considerations

- Existing auth mechanism: <describe>
- Recommended target: <Entra ID + managed identity | OAuth2 | mTLS>
- Secret storage: <Key Vault + reference from app config>

## References

- <citation 1: vendor connector docs>
- <citation 2: Azure integration option docs>
- <citation 3: community migration write-up>
```

---

## Template — pattern

Filename: `.github/skills/pattern-<name>.md`

```markdown
---
name: pattern-<name>
description: Migration pattern for <Name>. Load whenever the agent encounters <specific pattern in code>, OR when the Capability Matrix flags this pattern in `risk_flags` or `integrations`. Covers what the pattern is, why it blocks Azure hosting, replacement options, and step-by-step migration.
family: pattern
triggers: <keyword 1>, <keyword 2>, <keyword 3>
---

# Skill: Migration Pattern — <Name>

## When to Use

- Discovery or code review finds <specific pattern>
- User asks about migrating <specific pattern>

## The Pattern

- What it is: <description>
- Typical implementation: <describe common variants>
- Where it appears: <framework or scenario>

## Why It Blocks Azure

- <specific reason 1: e.g., "COM+ requires DCOM which is not available in App Service">
- <specific reason 2>
- <specific reason 3>

## Replacement Options

| Option | Best for | Effort | Notes |
|--------|----------|--------|-------|
| **Option 1: <name>** | <criteria> | <low/medium/high> | <tradeoffs> |
| **Option 2: <name>** | <criteria> | <low/medium/high> | <tradeoffs> |
| **Option 3: <name>** | <criteria> | <low/medium/high> | <tradeoffs> |

## Migration Steps

1. <step 1>
2. <step 2>
3. <step 3>
4. <smoke test>
5. <rollback trigger>

## References

- <citation 1: RFC / standards doc>
- <citation 2: framework migration guide>
- <citation 3: community best-practice article>
```

---

## Template — risk

Filename: `.github/skills/risk-<name>.md`

```markdown
---
name: risk-<name>
description: Migration risk — <Name>. Load whenever discovery flags <specific risk condition> in `Capability-Matrix.risk_flags`, OR when the user mentions <keyword risk>. Covers what the risk is, severity + likelihood framework, how to detect it in a codebase, mitigations, and when to escalate.
family: risk
triggers: <name>, <keyword>
---

# Skill: Migration Risk — <Name>

## When to Use

- `risk_flags` in Capability Matrix contains `<name>`
- Discovery finds <specific condition>
- User asks about <keyword>

## The Risk

- What could go wrong: <describe outcome — e.g., "data residency violation triggers GDPR fines">
- Blast radius: <who is impacted>
- Time-to-detect: <how quickly you'd notice>

## Severity + Likelihood

| Severity | Definition |
|----------|------------|
| Critical | <criteria — e.g., "regulatory violation, data loss, security breach"> |
| High | <criteria> |
| Medium | <criteria> |
| Low | <criteria> |

| Likelihood | Definition |
|------------|------------|
| Very likely | <criteria> |
| Likely | <criteria> |
| Possible | <criteria> |
| Unlikely | <criteria> |

## Detection Signals

- <signal 1 — code pattern, config, dependency>
- <signal 2>
- <signal 3>

## Mitigations

| Mitigation | Effort | Reduces severity to | Notes |
|------------|--------|---------------------|-------|
| **<mitigation 1>** | <low/medium/high> | <after severity> | <tradeoffs> |
| **<mitigation 2>** | <low/medium/high> | <after severity> | <tradeoffs> |

## Escalation Path

- <when to involve specialists — e.g., "always for regulatory risks">
- <who to escalate to — e.g., "Azure Compliance CSA, legal team">
- <internal artifacts to produce — e.g., "add entry to reports/Risk-Register.md">

## References

- <citation 1: regulator publication or Azure compliance doc>
- <citation 2: industry best practice>
- <citation 3: real-world incident write-up>
```

---

## Notes for `skill-creator` using these templates

- **Don't ship placeholder text.** Every `<X>` must be replaced with real content from the research step. If you can't fill a section, delete it — an empty section is worse than no section.
- **Keep the section order.** Downstream agents expect these sections in a specific order for their skill family.
- **Cite real sources.** Every skill needs 3-5 references. Anthropic-style, use real URLs.
- **Match description writing rules** (see `references/skill-anatomy.md`). Descriptions are the primary triggering mechanism; be specific and slightly pushy.
