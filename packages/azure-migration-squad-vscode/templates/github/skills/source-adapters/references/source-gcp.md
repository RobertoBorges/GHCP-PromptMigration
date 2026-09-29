# Skill: Source Adapter — Google Cloud Platform (GCP) (Stub)

> **Stub adapter.** Provides recognition + escalation guidance. For deep migration, pair with a partner or extend this skill into a full adapter.

## Overview

Characterizes an application currently running on GCP (Compute Engine, GKE, Cloud Run, App Engine, Cloud Functions, Cloud SQL, Cloud Storage, Pub/Sub, BigQuery, Spanner) targeting Azure migration.

## When to Use

User says it runs on GCP, or GCP project/inventory surfaces resources backing the application

## Inputs

- GCP project ID(s) and region(s)
- Access: gcloud auth profile, service account JSON, or read-only export
- Optional: existing IaC (Deployment Manager / Terraform google provider)

## Probes

- `gcloud compute instances list` → Compute Engine VMs
- `gcloud run services list` → Cloud Run services (container shape)
- `gcloud functions list` → Cloud Functions (event-driven shape)
- `gcloud app describe` → App Engine apps
- `gcloud container clusters list` → GKE clusters (handoff to `source-kubernetes-cluster`)
- `gcloud sql instances list` → Cloud SQL (MySQL / Postgres / SQL Server)
- `gcloud spanner instances list` → Spanner (unique architecture)
- `gsutil ls` → Cloud Storage buckets
- `gcloud pubsub topics list` → Pub/Sub topology
- `gcloud bigquery datasets list` → BigQuery analytics datasets
- `gcloud iam service-accounts list` → workload identity

## Target Azure Mapping (signals only — Architect decides)

| GCP today | Azure candidate |
|-----------|-----------------|
| Compute Engine VM | Azure VM |
| GKE | AKS |
| Cloud Run | Container Apps |
| Cloud Functions | Azure Functions |
| App Engine Standard | App Service |
| App Engine Flexible | App Service / Container Apps |
| Cloud SQL Postgres | Azure PostgreSQL Flexible Server |
| Cloud SQL MySQL | Azure Database for MySQL Flexible Server |
| Cloud SQL SQL Server | Azure SQL DB / MI |
| Spanner | Cosmos DB (NoSQL/SQL API) — needs schema redesign |
| Firestore | Cosmos DB (Mongo / NoSQL API) |
| Cloud Storage | Blob Storage |
| Pub/Sub | Event Grid or Service Bus Topic |
| BigQuery | Azure Synapse / Microsoft Fabric |
| Cloud Tasks | Service Bus Queue |
| Cloud Scheduler | Container Apps Jobs (cron) / Logic Apps |

## Risks / Constraints

- **GCP-specific services with no direct Azure equivalent.** Spanner (multi-region strongly consistent SQL), Firestore (document with realtime), Dataflow (managed Beam), Pub/Sub Lite, BigTable. Each requires redesign, not 1:1 port.
- **Workload Identity Federation.** GCP WIF → Azure Workload Identity; mapping is conceptual not mechanical.
- **VPC Service Controls.** Re-derive with Azure Private Link + NSG rules.
- **Egress costs out of GCP** can be material for large data migrations.

## Output Checklist

- [ ] Source environment identified
- [ ] Available access method captured
- [ ] Existing inventory or export captured
- [ ] Risks flagged for Architect + Cost Engineer review
- [ ] Escalation path decided (if applicable)
- [ ] Confidence label set on `source.evidence_confidence`