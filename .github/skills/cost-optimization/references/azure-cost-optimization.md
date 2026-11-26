# Azure Cost Optimization

Use this reference when comparing Azure targets, selecting SKUs, or tuning scaling and operational settings. Recommendations must be based on workload evidence, not assumed demand.

## Decision process

1. Record the workload's measured or estimated demand, availability, performance, and data requirements.
2. Compare viable hosting and data options against those requirements.
3. Right-size compute and storage; set bounded autoscaling based on credible metrics.
4. Review observability ingestion, retention, non-production schedules, and network/data-transfer costs.
5. Consider reservations or savings plans only after steady-state usage is established and commitment tradeoffs are accepted.

## Validation

- Explain the assumptions and tradeoffs behind every proposed SKU.
- Identify which estimates require measurement or a user decision.
- Revisit cost after deployment using actual consumption and performance.

## Current sources

See [Azure Guidance Sources](../../azure-infrastructure/references/azure-guidance-sources.md) and [Microsoft Cost Management](https://learn.microsoft.com/azure/cost-management-billing/costs/).
