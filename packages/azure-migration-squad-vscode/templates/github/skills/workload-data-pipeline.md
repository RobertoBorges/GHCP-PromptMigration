# Skill: Workload Pattern — Data Pipeline

> Workload pattern for ETL / ELT, data movement, scheduled extracts, real-time streaming pipelines, BI feeds. Distinct from generic batch jobs because the unit of work is data transformation across systems.

## When to Use

- `workload.primary_pattern: data-pipeline` in the Capability Matrix
- Evidence: SSIS / Informatica / Talend / Airflow / Azure Data Factory / AWS Glue / dbt / Databricks notebooks / Spark jobs, source-to-target movement, scheduled extracts

## Defining Characteristics

- **Source:** databases, files, APIs, streams
- **Transformation:** column mapping, joins, aggregations, schema changes, type casting
- **Destination:** data warehouse, data lake, BI / reporting, downstream apps
- **Trigger:** scheduled / event-based / continuous
- **Volume:** GBs to TBs per run common
- **State:** incremental watermarks, last-loaded markers

## Sub-Patterns

| Sub-pattern | Detection signal | Azure target tendency |
|-------------|------------------|----------------------|
| **SSIS packages** | `*.dtsx` files | Azure Data Factory with SSIS IR (lift) or refactor to Mapping Data Flows |
| **Informatica PowerCenter** | `*.xml` mappings; PWC repository | Azure Data Factory / Synapse |
| **Talend** | `*.tos.xml` jobs | Azure Data Factory |
| **Apache Airflow** | `airflow.models.DAG` | Data Factory Managed Airflow / AKS |
| **AWS Glue / EMR** | Glue jobs; EMR steps | Synapse Spark / Databricks |
| **Databricks notebooks** | `.dbc` archives, notebook code | Azure Databricks |
| **dbt** | `dbt_project.yml`, `models/` | Continue dbt; runs on Synapse / Databricks / Snowflake / Fabric |
| **Custom Python ETL** | pandas / pyspark scripts; cron-driven | Container Apps Jobs / Data Factory / Synapse Spark |
| **Real-time stream pipeline** | Kafka / Kinesis / Event Hubs → transform → sink | Stream Analytics / Databricks Structured Streaming / Spark |
| **CDC pipeline** | Debezium / Qlik Replicate / GoldenGate / SQL Server CDC | Synapse Link / ADF Mapping Data Flows with watermark |
| **Reverse-ETL (warehouse → SaaS)** | Census / Hightouch / custom | Functions / Container Apps Jobs |

## Probes

### Source surface

- Connection inventory: DB engines, file shares, API endpoints, streams
- Auth method per source (DB user, service account, OAuth)
- Read volume per run (rows / MB / GB)
- Read pattern: full snapshot / incremental (watermark column?) / CDC

### Transformation surface

- Step count per pipeline
- Languages used: SQL, PySpark, Scala, T-SQL, Python, custom
- Joins / aggregations / window functions
- Reference data (lookup tables)
- Data quality rules / null handling / casting policies
- Custom UDFs (in any language)

### Destination surface

- Sink type: Data Warehouse (Synapse Dedicated SQL Pool / Snowflake / BigQuery), Data Lake (ADLS Gen2 / S3 / GCS), Data Lakehouse (Databricks Delta / Fabric Lakehouse), Operational DB
- Write semantics: overwrite / append / upsert / merge
- Schema evolution policy

### Scheduling

- Cron / RRULE / continuous
- Dependencies between pipelines (DAG)
- SLA per pipeline (deadline for completion)

### Tools and runtimes

- Orchestrator: ADF / Airflow / Glue / Step Functions / Control-M / cron
- Compute: Spark cluster / serverless SQL / VM / Container / Function
- Libraries: pandas / PySpark / Scala / dbt / Great Expectations / DataFlow

### Data quality + lineage

- DQ framework presence (Great Expectations / Soda / Deequ / custom)
- Lineage tracking (Purview / DataHub / Marquez / nothing)
- Auditing / row-counts validation

### Observability

- Run history (success rate, duration trend)
- Failure alerting destination

## Phase Emphasis (per migration strategy)

| Strategy | Data pipeline emphasis |
|----------|------------------------|
| Rehost | Rarely chosen — pipelines tend to need at least replatform |
| Replatform | Phase 2 (refactor to target orchestrator), Phase 3 (compute), Phase 4 (cutover with parallel run) |
| Refactor | Phase 2 (rewrite transformations in target tech), Phase 3, Phase 6 (DQ + lineage) |
| Rearchitect | Phase 1 (lakehouse / medallion architecture), Phase 2, Phase 3 (Fabric / Synapse / Databricks) |
| Rebuild | Greenfield Lakehouse on Fabric / Databricks |

## Target Azure Mapping

### Orchestration mapping

| Today | Azure |
|-------|-------|
| SSIS | ADF with SSIS IR (lift); ADF Mapping Data Flows (refactor) |
| Informatica | ADF |
| Talend | ADF |
| Airflow | ADF Managed Airflow / AKS Airflow |
| AWS Glue | Synapse Pipelines / ADF / Databricks Jobs |
| AWS Step Functions (data) | Logic Apps Standard / Durable Functions / ADF |
| Control-M / TWS | Keep on-prem orchestration that calls Azure pipelines, OR replace with ADF triggers |
| cron + scripts | ADF / Container Apps Jobs / Functions Timer |

### Compute mapping

| Today | Azure |
|-------|-------|
| EMR | Synapse Spark Pool / Databricks |
| Glue Spark jobs | Synapse Spark / Databricks |
| Databricks (any cloud) | Azure Databricks |
| HDInsight | Synapse Spark / Databricks |
| Custom Spark on K8s | AKS + Spark Operator / Databricks |
| SQL-based ETL | Synapse Dedicated SQL Pool / Fabric Warehouse / Azure SQL |
| Python pandas | Container Apps Jobs / ADF Mapping Data Flows |

### Storage mapping

| Today | Azure |
|-------|-------|
| S3 (data lake) | ADLS Gen2 |
| GCS | ADLS Gen2 |
| HDFS | ADLS Gen2 (with hierarchical namespace) |
| Snowflake | Snowflake on Azure (or migrate to Synapse / Fabric) |
| BigQuery | Synapse / Fabric |
| Redshift | Synapse Dedicated SQL Pool / Fabric Warehouse |

## Cross-Cutting Data Pipeline Requirements (always add to plan)

- **Watermarks / idempotency** — every incremental pipeline tracks last-loaded watermark; runs are re-runnable.
- **Schema evolution policy** — backwards-compatible schema changes (additive) vs forward-incompatible.
- **Data quality gates** — fail fast on null / unique / range violations.
- **Lineage capture** — Purview integration for governance.
- **Parallel-run window** — for cutover, old and new pipelines run side-by-side for a period; row-count reconciliation.
- **Cost monitoring** — Spark cluster size + auto-pause; Synapse pool pause/resume; Databricks job-cluster vs all-purpose.
- **Secret handling** — Key Vault references in ADF linked services; never embed credentials.

## Anti-Patterns

- Don't lift SSIS forever. SSIS IR is a stepping stone; long-term, refactor to ADF Mapping Data Flows or Spark.
- Don't migrate notebook-driven prototypes to production without code review. Notebook chaos is a major data-pipeline risk.
- Don't preserve incremental watermarks that depend on source-system clock. Use commit timestamps or sequence columns.
- Don't run Databricks all-purpose clusters for scheduled jobs — use job clusters (cheaper, ephemeral).
- Don't deploy a data pipeline without a downstream row-count check.
- Don't migrate without lineage. If the team doesn't know what reports consume the warehouse, parallel-run is impossible.

## Output Checklist

- [ ] Pipeline sub-pattern identified
- [ ] Source connections + auth captured
- [ ] Read volumes captured per source
- [ ] Read pattern (full / incremental / CDC) captured with watermark column
- [ ] Transformation step count + languages captured
- [ ] Custom UDFs / reference data captured
- [ ] Destination + write semantics captured
- [ ] Schedule + dependencies + SLA captured
- [ ] DQ framework captured (or marked as missing)
- [ ] Lineage tracking captured (or marked as missing)
- [ ] Orchestration target chosen
- [ ] Compute target chosen
- [ ] Storage target chosen
- [ ] Parallel-run / cutover plan captured
- [ ] Cost optimization (cluster sizing, pause) captured
