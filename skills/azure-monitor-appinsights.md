# Azure Monitor + Application Insights

Use this skill when the migrated solution needs baseline observability, tracing, metrics, logs, and alerting.

## Minimum observable platform

- Application Insights for app telemetry
- Log Analytics workspace for centralized logs
- health endpoint per service
- correlation IDs across HTTP/database/dependency calls
- alerts for availability, errors, and saturation

## Implementation guidance

- Use `ILogger` in .NET or SLF4J in Java with structured logs.
- Capture request, dependency, exception, and custom business events.
- Tag telemetry with service name, environment, and version.
- Configure sensible retention to avoid excess cost.

## .NET example

```csharp
builder.Services.AddApplicationInsightsTelemetry();
builder.Services.AddHealthChecks();
app.MapHealthChecks("/health");
```

## Validation checklist

- Requests and dependencies appear in Application Insights.
- Health probes are accessible to the platform.
- Alerts and dashboards align with the deployment target.
- Sampling and retention are tuned for cost and signal.
