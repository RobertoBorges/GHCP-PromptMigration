# Skill: Workload Pattern — Batch Job

> Workload pattern for scheduled or on-demand batch processing: nightly ETL, report generation, payroll runs, COBOL batch jobs, cron-driven scripts, file-import jobs.

## When to Use

- `workload.primary_pattern: batch-job` in the Capability Matrix
- Evidence: scheduler (cron, Windows Task Scheduler, K8s CronJob, Airflow DAG, Control-M, TWS), main entry that exits on completion, file/DB-input → processed → output pattern

## Defining Characteristics

- **Trigger:** schedule (cron / RRULE / cluster timer) OR explicit invocation
- **Duration:** seconds to many hours
- **State:** progress checkpoint, often resumable
- **Output:** files, DB writes, downstream signals
- **Failure mode:** retry-able with idempotency; partial completion sometimes acceptable
- **Concurrency:** typically singleton per run (or sharded by input range)

## Sub-Patterns

| Sub-pattern | Detection signal | Azure target tendency |
|-------------|------------------|----------------------|
| **Linux cron** | `crontab -l`, `/etc/cron.*` entries | Container Apps Jobs (cron) |
| **Windows Scheduled Task** | `Get-ScheduledTask` entries | Container Apps Jobs (cron) |
| **K8s CronJob** | `kind: CronJob` manifests | Container Apps Jobs (lift) |
| **K8s Job (one-shot)** | `kind: Job` manifests | Container Apps Jobs (manual trigger) |
| **AWS Batch** | `aws batch describe-job-queues` | Azure Batch |
| **AWS Step Functions** | state-machine state.json | Logic Apps Standard / Durable Functions |
| **Airflow DAG** | `airflow.models.DAG` import | Data Factory Managed Airflow / AKS |
| **Spring Batch** | `spring-boot-starter-batch`; `Job`, `Step` beans | Container Apps Jobs (jar) / Spring Apps |
| **Mainframe JCL** | `*.jcl` files (z/OS) | Container Apps Jobs after refactor / Azure Batch |
| **SSIS / Data Factory packages** | `*.dtsx` files | Azure Data Factory |

## Probes

### Trigger surface

- Cron expression(s) — what timezone?
- Trigger type: time-based / event-based / manual
- Idempotency guarantee (can it be re-run safely?)
- Overlap policy (if a run takes too long and the next fires)

### Input

- Source: file (path? S3? Blob? SFTP?), DB query, queue, manifest
- Volume per run: rows, files, bytes
- Schema / format

### Processing

- Steps: extract → transform → load (ETL classic) OR custom logic
- Stateful (checkpoint resumable) vs stateless (rerun from start)
- Parallelism: single-threaded? multi-threaded? sharded?
- Long-running concerns: memory growth, file handles, DB connections

### Output

- Destination: file (path? S3? Blob? SFTP?), DB writes, queue messages, downstream API calls
- Atomicity: is partial output OK?
- Downstream consumers (who waits for this job?)

### Failure handling

- Retry policy
- Dead-letter / quarantine destination
- Alerting on failure (email, PagerDuty, Slack, monitoring tool)

### Resources

- Peak memory
- CPU profile (burst vs sustained)
- Disk I/O (scratch space)
- Network I/O (downloads / uploads)

### Runtime

- Language / framework (handoff to stack adapter)
- Entry point command
- Expected duration (min / max / p50 / p95)

## Phase Emphasis (per migration strategy)

| Strategy | Batch emphasis |
|----------|---------------|
| Rehost | Phase 3 (compute fit), Phase 4 (schedule cutover) |
| Replatform | Phase 2 (containerize), Phase 3 (Jobs / Batch), Phase 4 (schedule migration with overlap window) |
| Refactor | Phase 2 (idempotency, checkpoint, observability) |
| Rearchitect | Phase 1 (split monolith batch into pipeline steps), Phase 2, Phase 3 (Data Factory / Functions) |

## Target Azure Mapping

| Batch shape | Primary Azure target | Why |
|-------------|----------------------|-----|
| Cron-triggered container | **Container Apps Jobs (Cron)** | Direct fit; serverless-style |
| Manual / API-triggered | **Container Apps Jobs (Manual)** | Same; trigger via REST |
| Event-triggered (queue / Service Bus) | **Container Apps Jobs (Event)** with KEDA | Scale per message |
| Spark / Hadoop batch | **HDInsight** / **Azure Synapse Spark** / **Databricks Jobs** | Big-data shape |
| Many small short jobs (high concurrency) | **Azure Functions** with Timer / Queue trigger | Cheap; serverless |
| Long-running compute-heavy (>1h) | **Azure Batch** with pool of VMs | HPC pattern |
| Data-pipeline orchestration | **Azure Data Factory** | Visual + scheduling |
| Workflow with branches & retries | **Logic Apps Standard** / **Durable Functions** | Orchestration semantics |
| Airflow DAGs | **Data Factory Managed Airflow** | Vendor-managed Airflow |
| Spring Batch | **Container Apps Jobs** (run the jar) | Preserves Spring Batch model |
| SSIS packages | **Azure Data Factory** with SSIS IR | Lift SSIS |

## Cross-Cutting Batch Requirements (always add to plan)

- **Idempotency** — every job should be safely re-runnable. Document the idempotency key (run-id, date partition, etc.).
- **Checkpoint / resume** for long jobs.
- **Observability** — emit logs/metrics to Application Insights or Log Analytics. Include run-id in every log line.
- **Failure alerting** — Action Group on job failure metric.
- **Schedule migration plan** — old scheduler runs in parallel with new for one cycle; document switchover.
- **Input/output durable storage** — Blob Storage with lifecycle policies for retention.

## Anti-Patterns

- Don't migrate batch jobs to App Service "Always On" — they're not long-running web apps.
- Don't preserve cron-based scheduling when an event-trigger is more appropriate (e.g., "every 5 minutes, check for new files" → use Event Grid blob-created trigger).
- Don't ignore overlap risk. If a batch job runs every 15 minutes but sometimes takes 20 minutes, what happens? Document overlap policy.
- Don't lift SSIS packages to a self-hosted IR forever. Plan a refactor to Data Factory mapping data flows.
- Don't ignore the scheduler migration. The legacy scheduler (TWS / Control-M / Autosys) may still need to coexist for dependencies.
- Don't run a >1h job on Functions Consumption plan — it has time limits.

## Output Checklist

- [ ] Batch sub-pattern identified
- [ ] Schedule (cron / event / manual) captured with timezone
- [ ] Input source + volume captured
- [ ] Output destination + atomicity captured
- [ ] Idempotency guarantee documented
- [ ] Checkpoint / resume capability captured
- [ ] Resource profile (CPU/RAM/disk/network) captured
- [ ] Expected duration captured
- [ ] Downstream consumers mapped
- [ ] Failure alerting destination captured
- [ ] Schedule migration / overlap plan documented
- [ ] Target Azure compute selected
- [ ] Observability instrumentation plan captured
