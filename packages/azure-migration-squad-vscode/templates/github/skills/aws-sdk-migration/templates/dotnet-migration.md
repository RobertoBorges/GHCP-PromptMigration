# .NET AWS SDK → Azure SDK Migration Checklist

> **Application:** `{{APP_NAME}}`
> **Date:** `{{DATE}}`
> **Migrated by:** `{{AUTHOR}}`

## Authentication

| Step | Status | Notes |
|------|--------|-------|
| Remove `AWSSDK.Extensions.NETCore.Setup` | [ ] | |
| Add `Azure.Identity` NuGet package | [ ] | |
| Replace `AWSOptions` / `BasicAWSCredentials` with `DefaultAzureCredential` | [ ] | |
| Remove AWS region configuration | [ ] | Azure uses resource-specific endpoints |
| Configure Managed Identity for deployed environments | [ ] | |

## Package Replacements

### Storage (S3 → Blob Storage)

| Step | Status | Notes |
|------|--------|-------|
| Remove `AWSSDK.S3` | [ ] | |
| Add `Azure.Storage.Blobs` | [ ] | |
| Replace `AmazonS3Client` → `BlobServiceClient` | [ ] | |
| Replace `PutObjectRequest` → `BlobClient.UploadAsync()` | [ ] | |
| Replace `GetObjectRequest` → `BlobClient.DownloadAsync()` | [ ] | |
| Replace `ListObjectsV2Request` → `BlobContainerClient.GetBlobsAsync()` | [ ] | |
| Replace `DeleteObjectRequest` → `BlobClient.DeleteAsync()` | [ ] | |
| Update bucket names → container names | [ ] | Azure container names must be lowercase |
| Replace presigned URLs → SAS tokens via `BlobSasBuilder` | [ ] | |

### Messaging (SQS → Service Bus)

| Step | Status | Notes |
|------|--------|-------|
| Remove `AWSSDK.SQS` | [ ] | |
| Add `Azure.Messaging.ServiceBus` | [ ] | |
| Replace `AmazonSQSClient` → `ServiceBusClient` | [ ] | |
| Replace `SendMessageAsync` → `ServiceBusSender.SendMessageAsync()` | [ ] | |
| Replace `ReceiveMessageAsync` → `ServiceBusReceiver.ReceiveMessagesAsync()` | [ ] | |
| Replace `DeleteMessageAsync` → `ServiceBusReceiver.CompleteMessageAsync()` | [ ] | |
| Replace queue URL → namespace + queue name | [ ] | |
| Handle dead-letter queue differences | [ ] | Service Bus has built-in DLQ support |

### NoSQL (DynamoDB → Cosmos DB)

| Step | Status | Notes |
|------|--------|-------|
| Remove `AWSSDK.DynamoDBv2` | [ ] | |
| Add `Microsoft.Azure.Cosmos` | [ ] | |
| Replace `AmazonDynamoDBClient` → `CosmosClient` | [ ] | |
| Replace `PutItemAsync` → `Container.UpsertItemAsync()` | [ ] | |
| Replace `GetItemAsync` → `Container.ReadItemAsync()` | [ ] | |
| Replace `QueryAsync` → `Container.GetItemQueryIterator()` | [ ] | |
| Replace `ScanAsync` → cross-partition query | [ ] | Avoid full scans; use partition keys |
| Map DynamoDB key schema → Cosmos DB partition key | [ ] | |
| Convert `AttributeValue` maps → POCOs or `dynamic` | [ ] | |

### Secrets (Secrets Manager → Key Vault)

| Step | Status | Notes |
|------|--------|-------|
| Remove `AWSSDK.SecretsManager` | [ ] | |
| Add `Azure.Security.KeyVault.Secrets` | [ ] | |
| Replace `AmazonSecretsManagerClient` → `SecretClient` | [ ] | |
| Replace `GetSecretValueAsync` → `GetSecretAsync()` | [ ] | |
| Replace `CreateSecretAsync` → `SetSecretAsync()` | [ ] | |
| Configure Key Vault RBAC (not access policies) | [ ] | |

### Serverless (Lambda invocation → Functions HTTP call)

| Step | Status | Notes |
|------|--------|-------|
| Remove `AWSSDK.Lambda` | [ ] | |
| Replace `AmazonLambdaClient.InvokeAsync` → `HttpClient.PostAsync()` | [ ] | |
| Configure Function App URL and key | [ ] | Use Managed Identity where possible |

### Observability (CloudWatch → Application Insights)

| Step | Status | Notes |
|------|--------|-------|
| Remove `AWSSDK.CloudWatch` / `AWSSDK.CloudWatchLogs` | [ ] | |
| Add `Microsoft.ApplicationInsights.AspNetCore` | [ ] | |
| Call `builder.Services.AddApplicationInsightsTelemetry()` in `Program.cs` | [ ] | |
| Replace `PutMetricData` → `TelemetryClient.TrackMetric()` | [ ] | |
| Replace CloudWatch Logs → `ILogger` (auto-captured by App Insights) | [ ] | |
| Set `APPLICATIONINSIGHTS_CONNECTION_STRING` env variable | [ ] | |

## Configuration Cleanup

| Step | Status | Notes |
|------|--------|-------|
| Remove `AWS` section from `appsettings.json` | [ ] | |
| Remove `aws-lambda-tools-defaults.json` if present | [ ] | |
| Add Azure service endpoints to configuration | [ ] | |
| Remove all AWS access key / secret key references | [ ] | |

## Verification

| Step | Status | Notes |
|------|--------|-------|
| Solution builds without AWS SDK references | [ ] | |
| Unit tests pass with mocked Azure clients | [ ] | |
| Integration tests pass against Azure services | [ ] | |
| No remaining `Amazon.*` / `AWSSDK.*` using statements | [ ] | |
