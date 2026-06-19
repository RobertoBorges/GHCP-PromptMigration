# Skill: Capability Matrix

> The machine-readable contract between Discovery Engineer and every downstream Phase prompt. The Discovery Dossier is for humans; the Capability Matrix is for the squad.

## Output File

`reports/Capability-Matrix.yaml`

## When to Use

- Produced by Discovery Engineer at the end of `/assess-any-application`
- Consumed by every Phase prompt (Phase 1–6) to know which source/stack/workload skills to load and which specialists to dispatch
- Updated by Architect when strategy is refined
- Re-emitted by Discovery Engineer when re-discovery is triggered

## Schema (canonical)

```yaml
# reports/Capability-Matrix.yaml
# Schema version: 1.0
# Authored: <YYYY-MM-DD> by Discovery Engineer (Saul Bloom Jr.)
# Approved: <YYYY-MM-DD or "pending"> by Architect (Danny Ocean)

schema_version: 1.0
authored_date: <YYYY-MM-DD>
approved_date: <YYYY-MM-DD | "pending">

application:
  name: <string>
  owner: <string | "unknown">
  purpose: <one-line>
  criticality: <mission-critical | important | nice-to-have>
  business_priority: <speed | modernize | cost | risk>

source:
  primary_adapter: <source-github-repo | source-zip-filesystem | source-on-premise | source-aws | source-gcp | source-oracle-db | source-vmware-rvtools | source-mainframe | source-kubernetes-cluster | source-container-registry | source-unsupported-escalation>
  access_method: <git-url | ssh | aws-profile | gcp-project | filesystem-path | rvtools-export | kubectl-context | acr-url | describe-only>
  secondary_adapters: []                    # e.g., DB on a separate source
  evidence_confidence: <high | medium | low>
  evidence_paths:
    - <relative file path or command>

stack:
  primary_stack: <dotnet | java | python | nodejs | php | ruby | go | perl | rust | cobol-mainframe | oracle-forms | powerbuilder | delphi-vb6 | scala-kotlin | cpp-windows | unknown>
  primary_framework: <e.g., spring-boot-3 | aspnet-core-8 | django-4 | laravel-10 | none>
  secondary_stacks: []
  build_system: <msbuild | maven | gradle | npm | pnpm | yarn | pip | poetry | composer | bundler | cargo | go-modules | sbt | mix | make | cmake | unknown>
  runtime_version_detected: <e.g., dotnet8.0 | java-17 | python-3.11 | node-20 | php-8.3 | unknown>
  evidence_confidence: <high | medium | low>
  evidence_paths:
    - <relative file path>

workload:
  primary_pattern: <webapp | api-service | batch-job | event-driven | serverless | desktop-client-server | packaged-app | data-pipeline | mainframe-transactional>
  secondary_patterns: []
  entry_points:
    - <e.g., src/Program.cs main()>
    - <e.g., crontab entry: /opt/app/run-nightly.sh>
  evidence_confidence: <high | medium | low>

data:
  primary_datastore: <sql-server | azure-sql | oracle | postgresql | mysql | mongo | dynamodb | cosmos | files | s3 | gcs | blob | hdfs | mainframe-vsam | unknown>
  datastore_version: <e.g., "SQL Server 2016" | "PostgreSQL 14" | unknown>
  data_gravity: <none | small | medium | large | very-large>
  schema_highlights:
    - <e.g., "412 tables, ~80 stored procedures, 12 triggers">
  evidence_confidence: <high | medium | low>

integrations:
  - name: <integration name>
    direction: <inbound | outbound | bidirectional>
    protocol: <REST | SOAP | SFTP | JMS | AMQP | SMB | gRPC | Kafka | other>
    criticality: <high | medium | low>
    notes: <free-form>

identity:
  current_provider: <ad | ldap | saml | oauth-custom | oauth-azuread | hardcoded | none>
  target_provider: <entra-id-workload-identity | entra-id-b2c | preserve-existing>

network:
  on_prem_dependencies: [<list of on-prem systems referenced>]
  private_endpoints_needed: <true | false>
  egress_constraints: <e.g., "must reach legacy ESB at 10.0.0.5">

risk_flags:
  # Add any that apply — these auto-dispatch specialists per .squad/routing.md
  - <regulated-data | production-only-system | large-data-gravity | no-source-code-available | unsupported-runtime | vendor-licensed-runtime | tight-cutover-window | mainframe | saas-embedded | high-integration-fanout | low-evidence-confidence>

compliance:
  regulations: [<pii | pci | hipaa | gdpr | sox | fedramp | other>]
  residency_requirement: <e.g., "EU-only" | "none">
  audit_logging_required: <true | false>

operational:
  rto: <e.g., "4 hours" | "unknown">
  rpo: <e.g., "1 hour" | "unknown">
  cutover_window: <e.g., "Sat 22:00 - Sun 06:00 ET" | "unknown">
  current_sla: <e.g., "99.9%" | "unknown">

migration_strategy:
  recommendation: <rehost | replatform | refactor | rearchitect | rebuild | retire | retain>
  rationale: <multi-line: which decision-tree branches were taken>
  decision_path:
    - <branch and outcome>
    - <branch and outcome>
  alternatives_considered:
    - alternative: <other 6R>
      rejected_because: <reason>
    - alternative: <other 6R>
      rejected_because: <reason>
  target_azure_candidates:
    - service: <Azure service>
      fit: <high | medium | low>
      fit_notes: <one-line>
    - service: <...>
      fit: <...>
      fit_notes: <...>

required_specialists:
  - <agent name from squad>
  - ...

unresolved_questions:
  - id: Q1
    question: <text>
    impact: <why it matters>
    recommended_probe: <action to raise confidence>

assumptions:
  - assumption: <text>
    impact_if_wrong: <text>

handoff:
  next_command: /build-migration-plan
  next_lead: Architect (Danny Ocean)
  notes: <optional 3-5 lines>
```

## Field Conventions

### `evidence_confidence`

| Value | Meaning |
|-------|---------|
| `high` | Manifest, command output, or directly-observed artifact confirms it |
| `medium` | Strong indirect evidence (file extensions + framework signals) but no manifest |
| `low` | Only user statement or partial evidence; needs probing |

If any axis is `low`, that axis MUST have a corresponding entry in `unresolved_questions`.

### `data_gravity` bands

| Band | Range |
|------|-------|
| `none` | No persistent data |
| `small` | <1 GB |
| `medium` | 1 GB – 100 GB |
| `large` | 100 GB – 1 TB |
| `very-large` | >1 TB |

### `criticality`

| Value | Implication |
|-------|------------|
| `mission-critical` | Auto-add Cutover Commander, Security Auditor, Performance Engineer |
| `important` | Auto-add Cutover Commander |
| `nice-to-have` | Standard squad |

### `risk_flags`

Use only the canonical values (in `.squad/routing.md`). Each flag triggers auto-dispatch.

## Consumer Contract

Every Phase prompt (`/phase1-planandassess` through `/phase6-postmigrationops`) reads this matrix at startup. If the matrix is missing or `schema_version` doesn't match, the Phase prompt **must**:

1. Refuse to proceed
2. Print a clear error pointing to `/assess-any-application`
3. Suggest the user run the Discovery Engineer first

Phase prompts use these fields:

| Field | Used by |
|-------|---------|
| `source.primary_adapter` | All phases (selects source-* skill) |
| `stack.primary_stack` + `stack.secondary_stacks` | Phase 2, 3 (selects stack-* skill) |
| `workload.primary_pattern` | Phase 1, 3 (selects workload-* skill) |
| `data.*` | Phase 2 (Database Migration), Phase 3, Phase 6 |
| `integrations` | Phase 1, Phase 3, Phase 4 |
| `risk_flags` | All phases (auto-dispatch specialists) |
| `migration_strategy.recommendation` | All phases (which phases are emphasized) |
| `migration_strategy.target_azure_candidates` | Phase 1 (Architect picks), Phase 3 (IaC generation) |

## Update Discipline

The matrix is **append-only** in terms of fields. To change a value:

1. Discovery Engineer or Architect updates the relevant field
2. `approved_date` is set to today
3. A line is added to `.squad/decisions.md` recording the change:

```
Matrix-<app>-<YYYY-MM-DD>: changed <field> from <old> to <new>, reason=<short>
```

## Quality Gate

A matrix is **valid** when:

- [ ] `schema_version: 1.0` set
- [ ] All required keys present (use the canonical schema above)
- [ ] Every `evidence_confidence` filled
- [ ] Every `low`-confidence axis has at least one `unresolved_questions` entry
- [ ] `migration_strategy.recommendation` set with rationale + ≥2 alternatives
- [ ] `target_azure_candidates` has at least 1 entry (or "none" if retire/retain)
- [ ] `required_specialists` includes at least Architect + Azure Specialist + Tester + Scribe
- [ ] `handoff.next_command` set
