---
name: workload-adapters
description: |
  Routes discovery and planning to workload-pattern guidance for Azure migrations. Use when evidence identifies how the application runs: browser web app, API service, scheduled batch job, data pipeline, event-driven worker, serverless function, desktop client-server app, or packaged/vendor application. Helps select probes, risks, cross-cutting requirements, and Azure target signals after source and stack evidence are known.
user-invocable: false
---

# Workload Adapters Router

## When to use this skill

Use this router after or during source and stack discovery when evidence shows the application's runtime pattern. Workload adapters explain behaviour, operational concerns, target Azure signals, risks, and planning emphasis. A single system can contain multiple workload patterns; route each meaningful component separately.

## Selection table

| Detected signal or evidence | Read this reference |
|---|---|
| Browser-facing UI, HTTP server on 80/443, server-rendered pages, SPA shell, templates such as Razor/JSP/Blade/EJS/ERB, session cookies, static assets | [Web Application](./references/workload-webapp.md) |
| Machine-facing HTTP API, REST controllers, route handlers, OpenAPI/Swagger, GraphQL, gRPC, SOAP endpoint, no browser UI, partner/mobile/service clients | [API Service](./references/workload-api-service.md) |
| Cron, Windows Task Scheduler, Kubernetes CronJob, Airflow DAG, Control-M, TWS, one-shot executable, file/DB input to processed output, finite runtime | [Batch Job](./references/workload-batch-job.md) |
| ETL/ELT, SSIS, Informatica, Talend, Airflow, Azure Data Factory, AWS Glue, dbt, Databricks, Spark, source-to-target movement, warehouse/lake/BI output | [Data Pipeline](./references/workload-data-pipeline.md) |
| Queue/topic/stream consumer, SQS/SNS/EventBridge/Kinesis, Kafka, RabbitMQ, Service Bus, Pub/Sub, message-driven bean, Celery, bullmq, Functions queue trigger | [Event-Driven](./references/workload-event-driven.md) |
| Function app or cloud function model, HTTP/queue/timer/blob/change-feed triggers, per-invocation scale, cold starts, durable state outside the function | [Serverless](./references/workload-serverless.md) |
| Installed Windows/macOS/Linux desktop client, MSI/ClickOnce/vendor installer, thick client, direct database connection, per-user deployment | [Desktop Client-Server](./references/workload-desktop-client-server.md) |
| Vendor-owned application, source code unavailable, licensed support model, vendor installer/image/managed service, configuration or plugin customisations | [Packaged / Vendor Application](./references/workload-packaged-app.md) |

## How to use

1. Choose the workload reference that matches runtime behaviour, not just programming language.
2. Read the selected reference before writing migration phases, risks, target options, or operational requirements.
3. For mixed systems, read one workload reference per component and record component boundaries in the Capability Matrix.
4. Treat target Azure mappings as signals for user-owned architecture decisions, not automatic choices.
