---
name: aws-observability-migration
description: Migrate AWS observability (CloudWatch Logs / Metrics / Alarms / Dashboards, X-Ray, CloudTrail) to Azure Monitor, Application Insights, Log Analytics, Azure Monitor Alerts, Azure Monitor Workbooks, and Distributed Tracing. Covers OpenTelemetry integration, KQL query examples, and cost-conscious log-retention patterns. Use during Phase 2 code migration and Phase 5 CI/CD wiring.
---

# AWS Observability to Azure Monitor Migration Guide

This skill provides comprehensive guidance for migrating AWS observability services (CloudWatch, X-Ray, CloudTrail) to Azure Monitor and its sub-services.

---

## Service Mapping

| AWS Service | Azure Equivalent | Notes |
|---|---|---|
| CloudWatch Metrics | Azure Monitor Metrics | Platform metrics auto-collected for all Azure resources |
| CloudWatch Logs | Azure Monitor Logs (Log Analytics) | KQL query language replaces CloudWatch Insights syntax |
| CloudWatch Alarms | Azure Monitor Alerts | Action Groups for notifications (email, SMS, webhook, Logic App) |
| CloudWatch Dashboards | Azure Dashboards / Workbooks | Workbooks are more powerful with parameterization and interactivity |
| CloudWatch Insights | Log Analytics queries (KQL) | KQL is a purpose-built query language for log analytics |
| X-Ray | Application Insights (distributed tracing) | Integrated APM with auto-instrumentation support |
| X-Ray Service Map | Application Insights Application Map | Auto-discovered dependency topology |
| CloudTrail | Azure Activity Log | Audit and governance for control-plane operations |
| CloudTrail Insights | Azure Monitor anomaly detection | Dynamic thresholds detect anomalous patterns |
| CloudWatch Synthetics | Application Insights Availability Tests | URL ping tests and multi-step web tests |
| CloudWatch RUM | Application Insights (browser telemetry) | JavaScript SDK for client-side telemetry |
| CloudWatch Container Insights | Azure Monitor for Containers | Native AKS integration with Prometheus metrics |
| CloudWatch Lambda Insights | Application Insights for Functions | Auto-instrumentation for Azure Functions |
| AWS Health Dashboard | Azure Service Health | Service issues, planned maintenance, health advisories |
| AWS Config | Azure Policy + Azure Resource Graph | Compliance evaluation and resource inventory queries |

---

## Key Architecture Difference

AWS splits observability across **three separate services**:

- **CloudWatch** — metrics, logs, dashboards, alarms
- **X-Ray** — distributed tracing and service maps
- **CloudTrail** — audit trail and governance events

Azure **consolidates everything under Azure Monitor** with specialized sub-services:

- **Azure Monitor Metrics** — platform and custom metrics with near real-time collection
- **Azure Monitor Logs (Log Analytics)** — centralized log store queryable with KQL
- **Application Insights** — APM, distributed tracing, availability tests, browser telemetry
- **Azure Activity Log** — control-plane audit trail for all resource operations
- **Azure Workbooks** — interactive reports, dashboards, and visualizations

This consolidation means:

1. A single pane of glass for all observability data
2. Correlated metrics, logs, and traces in one query
3. Shared alerting engine across all signal types
4. Unified RBAC and data retention policies

---

## SDK and Instrumentation Migration

### .NET

| AWS SDK/Library | Azure Replacement | Package |
|---|---|---|
| AWS X-Ray SDK (`AWSXRayRecorder`) | Azure Monitor OpenTelemetry Distro | `Azure.Monitor.OpenTelemetry.AspNetCore` |
| CloudWatch EMF (Embedded Metric Format) | Application Insights TelemetryClient custom metrics | `Microsoft.ApplicationInsights` |
| CloudWatch Logs SDK | ILogger → Log Analytics | Built-in with Application Insights provider |

**Before (AWS X-Ray):**

```csharp
// AWS X-Ray instrumentation
using Amazon.XRay.Recorder.Core;
using Amazon.XRay.Recorder.Handlers.AspNetCore;

var builder = WebApplication.CreateBuilder(args);
builder.Services.AddXRay();
app.UseXRay("MyService");
```

**After (Azure Monitor OpenTelemetry):**

```csharp
// Azure Monitor OpenTelemetry instrumentation
using Azure.Monitor.OpenTelemetry.AspNetCore;

var builder = WebApplication.CreateBuilder(args);
builder.Services.AddOpenTelemetry().UseAzureMonitor(options =>
{
    options.ConnectionString = builder.Configuration["ApplicationInsights:ConnectionString"];
});
```

### Java

| AWS SDK/Library | Azure Replacement | Package |
|---|---|---|
| AWS X-Ray SDK (`com.amazonaws:aws-xray-recorder-sdk-core`) | Azure Monitor OpenTelemetry exporter | `azure-monitor-opentelemetry-exporter` |
| CloudWatch SDK (`software.amazon.awssdk:cloudwatch`) | Application Insights Web or OpenTelemetry | `applicationinsights-web` or OpenTelemetry |

**Before (AWS X-Ray):**

```java
// AWS X-Ray instrumentation
import com.amazonaws.xray.AWSXRay;
import com.amazonaws.xray.spring.aop.XRayEnabled;

@XRayEnabled
@SpringBootApplication
public class MyApplication {
    // X-Ray auto-instruments annotated classes
}
```

**After (Azure Monitor OpenTelemetry):**

```java
// Azure Monitor OpenTelemetry — use the Java agent (zero-code)
// Add JVM argument: -javaagent:applicationinsights-agent-3.x.x.jar
// Configure via applicationinsights.json:
// {
//   "connectionString": "<your-connection-string>",
//   "role": { "name": "MyService" }
// }
```

### Python

| AWS SDK/Library | Azure Replacement | Package |
|---|---|---|
| `aws-xray-sdk` | Azure Monitor OpenTelemetry Distro | `azure-monitor-opentelemetry` |
| `boto3` CloudWatch client | OpenTelemetry or opencensus extension | `opencensus-ext-azure` or `azure-monitor-opentelemetry` |

**Before (AWS X-Ray):**

```python
# AWS X-Ray instrumentation
from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.ext.flask.middleware import XRayMiddleware

app = Flask(__name__)
xray_recorder.configure(service='MyService')
XRayMiddleware(app, xray_recorder)
```

**After (Azure Monitor OpenTelemetry):**

```python
# Azure Monitor OpenTelemetry instrumentation
from azure.monitor.opentelemetry import configure_azure_monitor

configure_azure_monitor(
    connection_string="<your-connection-string>"
)

# Flask/Django auto-instrumentation is included
```

### Node.js

| AWS SDK/Library | Azure Replacement | Package |
|---|---|---|
| `aws-xray-sdk` | Azure Monitor OpenTelemetry | `@azure/monitor-opentelemetry` |
| CloudWatch SDK (`@aws-sdk/client-cloudwatch`) | Application Insights SDK | `applicationinsights` |

**Before (AWS X-Ray):**

```javascript
// AWS X-Ray instrumentation
const AWSXRay = require('aws-xray-sdk');
const express = require('express');

const app = express();
app.use(AWSXRay.express.openSegment('MyService'));
// ... routes ...
app.use(AWSXRay.express.closeSegment());
```

**After (Azure Monitor OpenTelemetry):**

```javascript
// Azure Monitor OpenTelemetry instrumentation
const { useAzureMonitor } = require('@azure/monitor-opentelemetry');

useAzureMonitor({
  azureMonitorExporterOptions: {
    connectionString: process.env.APPLICATIONINSIGHTS_CONNECTION_STRING,
  },
});

// Express auto-instrumentation is included
```

### Go

| AWS SDK/Library | Azure Replacement | Package |
|---|---|---|
| `aws-xray-sdk-go` | Azure Monitor OpenTelemetry exporter | `github.com/Azure/azure-sdk-for-go/sdk/monitor/query/azmetrics` |
| CloudWatch SDK (`github.com/aws/aws-sdk-go-v2/service/cloudwatch`) | Azure Monitor SDK | `github.com/Azure/azure-sdk-for-go/sdk/monitor` |

**Before (AWS X-Ray):**

```go
// AWS X-Ray instrumentation
import "github.com/aws/aws-xray-sdk-go/xray"

func main() {
    http.Handle("/", xray.Handler(
        xray.NewFixedSegmentNamer("MyService"),
        http.HandlerFunc(handler),
    ))
}
```

**After (Azure Monitor OpenTelemetry):**

```go
// Azure Monitor OpenTelemetry exporter
import (
    "go.opentelemetry.io/otel"
    "github.com/Azure/azure-sdk-for-go/sdk/monitor/azingest"
    // Use OpenTelemetry SDK with Azure Monitor exporter
)

// Configure OpenTelemetry with Azure Monitor exporter
// See: https://learn.microsoft.com/azure/azure-monitor/app/opentelemetry-enable
```

---

## Logging Migration

| AWS Pattern | Azure Pattern | Migration Notes |
|---|---|---|
| CloudWatch Log Groups | Log Analytics Workspace | One workspace per environment recommended |
| CloudWatch Log Streams | Log tables / custom tables | Use Data Collection Rules (DCR) for custom tables |
| CloudWatch Insights queries | KQL queries in Log Analytics | KQL is more expressive; see query mapping below |
| Log retention policies | Log Analytics retention settings | Per-table retention (default 30 days, up to 730 days) |
| Log subscription filters | Azure Monitor diagnostic settings | Route resource logs to Log Analytics, Storage, or Event Hubs |
| Cross-account log sharing | Cross-workspace queries | Use `workspace()` function in KQL for cross-workspace joins |

### Common Query Mapping: CloudWatch Insights → KQL

**Filter by field value:**

```
// CloudWatch Insights
fields @timestamp, @message
| filter @message like /ERROR/
| sort @timestamp desc
| limit 50

// KQL equivalent
AppTraces
| where Message contains "ERROR"
| order by TimeGenerated desc
| take 50
```

**Aggregate by time interval:**

```
// CloudWatch Insights
stats count(*) as errorCount by bin(30m)
| filter @message like /ERROR/

// KQL equivalent
AppTraces
| where Message contains "ERROR"
| summarize errorCount = count() by bin(TimeGenerated, 30m)
```

**Parse structured fields:**

```
// CloudWatch Insights
fields @timestamp, @message
| parse @message "user=* action=* status=*" as user, action, status
| filter status = "FAILED"

// KQL equivalent
AppTraces
| parse Message with * "user=" user " action=" action " status=" status
| where status == "FAILED"
```

**Top N by count:**

```
// CloudWatch Insights
stats count(*) as cnt by statusCode
| sort cnt desc
| limit 10

// KQL equivalent
AppRequests
| summarize cnt = count() by ResultCode
| top 10 by cnt desc
```

**Percentile latency:**

```
// CloudWatch Insights
stats pct(@duration, 50) as p50,
      pct(@duration, 95) as p95,
      pct(@duration, 99) as p99

// KQL equivalent
AppRequests
| summarize p50 = percentile(DurationMs, 50),
            p95 = percentile(DurationMs, 95),
            p99 = percentile(DurationMs, 99)
```

---

## Alerting Migration

| AWS Pattern | Azure Pattern | Migration Notes |
|---|---|---|
| CloudWatch Alarm → SNS → Lambda | Azure Alert → Action Group → Logic App/Function | Action Groups support multiple action types |
| CloudWatch Metric Alarm | Azure Monitor Metric Alert | Supports static and dynamic thresholds |
| CloudWatch Anomaly Detection | Azure Monitor dynamic thresholds | ML-based baseline with configurable sensitivity |
| CloudWatch Composite Alarms | Azure Monitor alert processing rules | Suppress, route, or enrich alerts based on rules |
| SNS notification topics | Action Groups (email, SMS, webhook, Logic App, etc.) | Single Action Group can have multiple receivers |

### Alert Rule Example

**AWS CloudWatch Alarm (JSON):**

```json
{
  "AlarmName": "HighCPU",
  "MetricName": "CPUUtilization",
  "Namespace": "AWS/EC2",
  "Statistic": "Average",
  "Period": 300,
  "EvaluationPeriods": 3,
  "Threshold": 80,
  "ComparisonOperator": "GreaterThanThreshold",
  "AlarmActions": ["arn:aws:sns:us-east-1:123456789:alerts"]
}
```

**Azure Monitor Metric Alert (Bicep):**

```bicep
resource cpuAlert 'Microsoft.Insights/metricAlerts@2018-03-01' = {
  name: 'HighCPU'
  location: 'global'
  properties: {
    severity: 2
    evaluationFrequency: 'PT5M'
    windowSize: 'PT15M'
    criteria: {
      'odata.type': 'Microsoft.Azure.Monitor.SingleResourceMultipleMetricCriteria'
      allOf: [
        {
          name: 'CPUOver80'
          metricName: 'Percentage CPU'
          operator: 'GreaterThan'
          threshold: 80
          timeAggregation: 'Average'
        }
      ]
    }
    actions: [
      {
        actionGroupId: actionGroup.id
      }
    ]
    scopes: [
      vm.id
    ]
  }
}
```

---

## Dashboard Migration

| AWS Pattern | Azure Pattern | Migration Notes |
|---|---|---|
| CloudWatch Dashboard (JSON) | Azure Dashboard / Workbook | Workbooks recommended for advanced scenarios |
| Custom widgets | Workbook visualizations | Charts, grids, maps, text, and custom tiles |
| Cross-region dashboards | Workbook cross-workspace queries | Use `workspace()` function for multi-workspace data |
| Embedded metrics widgets | Workbook metric chart steps | Pin metrics directly from Monitor |
| Dashboard sharing | Workbook sharing via RBAC | Gallery templates for reuse |

### Dashboard Equivalence

CloudWatch dashboards use a JSON widget model. Azure offers two options:

1. **Azure Dashboards** — portal-based, tile layout, good for operational views. Best for simple metric and log pinning.
2. **Azure Workbooks** — parameterized, interactive, supports KQL queries, metrics, and Azure Resource Graph. Best for advanced analysis, incident investigation, and reporting.

**Recommendation:** Use **Azure Workbooks** for most migration scenarios. They are more powerful than CloudWatch Dashboards and support:

- Parameters and dropdowns for dynamic filtering
- Conditional visibility for sections
- Cross-workspace and cross-subscription queries
- Export to PDF for compliance reporting
- Gallery templates for sharing across teams

---

## Best Practices

### Workspace Strategy

- **Use a single Log Analytics Workspace per environment** (dev, staging, prod) to simplify access control and billing
- For multi-team organizations, use table-level RBAC within a shared workspace rather than separate workspaces
- Exception: compliance-isolated workloads (PCI, HIPAA) may require dedicated workspaces

### Application Insights

- **Enable Application Insights for all application workloads** — web apps, APIs, Functions, container apps
- Use **connection strings** (not instrumentation keys) for configuration — instrumentation keys are deprecated
- Configure **sampling** to manage high-volume telemetry costs (adaptive sampling is the default for .NET)

### Instrumentation Strategy

- **Use OpenTelemetry for language-agnostic instrumentation** — Azure Monitor OpenTelemetry Distro is the recommended path for new and migrated applications
- OpenTelemetry provides vendor-neutral instrumentation that works with Azure Monitor and other backends
- For .NET and Java, Azure Monitor auto-instrumentation can capture telemetry with minimal code changes

### Diagnostic Settings

- **Configure diagnostic settings for all Azure resources** to send platform logs and metrics to Log Analytics
- Use Azure Policy to enforce diagnostic settings at scale
- Route logs to: Log Analytics (query), Storage Account (archive), Event Hubs (stream to SIEM)

### Alerting

- **Set up Azure Monitor Alerts with Action Groups** for proactive notification
- Use dynamic thresholds for metrics with seasonal or trending patterns
- Configure alert processing rules to suppress alerts during maintenance windows
- Create separate Action Groups for different severity levels and teams

### Dashboards and Reporting

- **Use Azure Workbooks for interactive reports** — they are significantly more powerful than CloudWatch Dashboards
- Pin frequently-used KQL queries as Workbook steps
- Create Workbook templates for common scenarios and share via the gallery

### Retention and Compliance

- **Retain logs per compliance requirements** — default is 30 days, configurable up to 730 days per table
- Use Basic Logs tier for high-volume, infrequently-queried data to reduce costs
- Archive to Storage Accounts for long-term retention beyond 730 days

### Cost Optimization

- Use **commitment tiers** for predictable Log Analytics ingestion volumes (100 GB/day+)
- Enable **data collection rules (DCR)** to filter and transform data before ingestion
- Review Application Insights sampling rates to balance cost vs. data fidelity
- Use the **Basic Logs** tier for verbose diagnostic logs that are rarely queried
