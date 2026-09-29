# Skill: Workload Pattern — Serverless (Stub)

> **Stub pattern.** Provides classification + Azure target tendencies. For complex engagements, deepen this skill with engagement-specific guidance.

## Overview

Workload pattern for serverless functions: AWS Lambda, GCP Cloud Functions, Azure Functions, Cloudflare Workers, Vercel Serverless. Stateless, per-invocation billing, cold-start sensitivity.

## Defining Characteristics

- **Trigger:** HTTP, queue, timer, blob, change feed, custom binding
- **State:** stateless per invocation; durable state in external store
- **Latency:** sub-second to seconds; cold start penalty
- **Throughput:** auto-scales 0 → many; per-invocation cost
- **Duration limit:** seconds to minutes (provider-dependent)

## Target Azure Mapping (signals — Architect decides)

| Today | Azure |
|-------|-------|
| AWS Lambda (HTTP via API Gateway) | Azure Functions (HTTP trigger) + APIM |
| AWS Lambda (SQS/Kinesis trigger) | Azure Functions (Queue / Event Hub trigger) |
| GCP Cloud Functions | Azure Functions |
| Cloudflare Workers | Azure Functions (Premium / Flex) or Static Web Apps API |
| Lambda@Edge | Azure CDN with rules engine, or Front Door Rules |
| Vercel Serverless | Static Web Apps API (Functions-backed) |

## Risks / Migration Constraints

- **Trigger binding shape differs.** Lambda event payload ≠ Functions event. Rewrite the binding layer.
- **Cold-start latency.** Functions Consumption: 1-5s cold start. Premium / Flex Consumption removes cold start at higher cost.
- **Execution time limits.** Consumption: 5 min default, 10 min max. Premium: 30 min default, unbounded with config.
- **Concurrency limits.** Per-function instance concurrency settings differ.
- **Languages and runtimes** support windows differ across providers.
- **Custom domains + auth.** Functions has function-key, EasyAuth, or APIM in front.

## Output Checklist

- [ ] Workload sub-pattern identified
- [ ] Source environment characterized
- [ ] Critical SLA / TPS / latency captured
- [ ] State + consistency model captured
- [ ] Vendor / license model captured (if applicable)
- [ ] Migration approach: `rehost` / `replatform` / `refactor` / `rebuild` / `retire` / `retain` selected
- [ ] Required specialists flagged (commonly Architect + Database Specialist + Cost Engineer)
- [ ] Target Azure compute + data tier identified