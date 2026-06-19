# Cost Optimization

Use this skill when selecting Azure SKUs, scaling rules, and operational settings for the migrated solution.

## Primary levers

- choose the simplest hosting platform that meets requirements
- right-size plans and node pools
- cap autoscale ranges
- tune log retention and sampling
- use reserved capacity only for proven steady-state workloads

## Service-specific guidance

- **App Service:** start with an appropriate tier, enable autoscale only when load justifies it.
- **Container Apps:** control `maxReplicas`, idle scale, and workload profile choice.
- **AKS:** avoid oversized node pools and idle clusters.
- **Azure SQL:** pick compute/storage tier from measured demand, not guesses.

## Validation checklist

- The report explains why the chosen SKU is sufficient.
- Monitoring retention and sampling are intentional.
- Non-production environments have lower-cost defaults.
