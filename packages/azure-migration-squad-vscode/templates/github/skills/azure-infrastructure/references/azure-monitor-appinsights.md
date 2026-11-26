# Azure Monitor and Application Insights

Use this reference when the target needs application telemetry, distributed tracing, metrics, logs, health checks, or alerting.

## Baseline considerations

- Prefer the current Application Insights OpenTelemetry guidance for supported runtimes.
- Capture request, dependency, exception, and relevant business-event telemetry.
- Correlate telemetry across services and tag it with service, environment, and version.
- Set retention, sampling, access, and alert thresholds deliberately to balance signal, privacy, and cost.
- Confirm each health endpoint is suitable for the hosting platform's probes.

## Validation

- Verify expected request and dependency traces appear in the configured workspace.
- Test alerts against known conditions and confirm ownership and action paths.
- Review telemetry sampling, sensitive data, retention, and estimated ingestion cost.

## Current sources

See [Azure Guidance Sources](./azure-guidance-sources.md) and the [Application Insights OpenTelemetry overview](https://learn.microsoft.com/azure/azure-monitor/app/app-insights-overview). Verify SDK and instrumentation setup for the selected language and runtime.
