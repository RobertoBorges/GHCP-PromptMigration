# Java AWS SDK → Azure SDK Migration Checklist

> **Application:** `{{APP_NAME}}`
> **Date:** `{{DATE}}`
> **Migrated by:** `{{AUTHOR}}`

## Authentication

| Step | Status | Notes |
|------|--------|-------|
| Remove `software.amazon.awssdk:auth` from `pom.xml` / `build.gradle` | [ ] | |
| Add `com.azure:azure-identity` dependency | [ ] | |
| Replace `DefaultCredentialsProvider` → `DefaultAzureCredentialBuilder` | [ ] | |
| Remove AWS region configuration | [ ] | Azure uses resource-specific endpoints |
| Configure Managed Identity for deployed environments | [ ] | |

## Dependency Replacements (Maven)

### Storage (S3 → Blob Storage)

| Step | Status | Notes |
|------|--------|-------|
| Remove `software.amazon.awssdk:s3` | [ ] | |
| Add `com.azure:azure-storage-blob` | [ ] | |
| Replace `S3Client` → `BlobServiceClient` via `BlobServiceClientBuilder` | [ ] | |
| Replace `putObject()` → `BlobClient.upload()` | [ ] | |
| Replace `getObject()` → `BlobClient.downloadStream()` | [ ] | |
| Replace `listObjectsV2()` → `BlobContainerClient.listBlobs()` | [ ] | |
| Replace `deleteObject()` → `BlobClient.delete()` | [ ] | |
| Replace presigned URLs → SAS tokens via `BlobSasPermission` | [ ] | |

### Messaging (SQS → Service Bus)

| Step | Status | Notes |
|------|--------|-------|
| Remove `software.amazon.awssdk:sqs` | [ ] | |
| Add `com.azure:azure-messaging-servicebus` | [ ] | |
| Replace `SqsClient` → `ServiceBusClientBuilder` chain | [ ] | |
| Replace `sendMessage()` → `ServiceBusSenderClient.sendMessage()` | [ ] | |
| Replace `receiveMessage()` → `ServiceBusReceiverClient.receiveMessages()` | [ ] | |
| Replace `deleteMessage()` → `ServiceBusReceiverClient.complete()` | [ ] | |
| Replace queue URL → fully qualified namespace + queue name | [ ] | |
| Handle dead-letter queue differences | [ ] | Service Bus has built-in DLQ |

### NoSQL (DynamoDB → Cosmos DB)

| Step | Status | Notes |
|------|--------|-------|
| Remove `software.amazon.awssdk:dynamodb` | [ ] | |
| Add `com.azure:azure-cosmos` | [ ] | |
| Replace `DynamoDbClient` → `CosmosClient` via `CosmosClientBuilder` | [ ] | |
| Replace `putItem()` → `CosmosContainer.upsertItem()` | [ ] | |
| Replace `getItem()` → `CosmosContainer.readItem()` | [ ] | |
| Replace `query()` → `CosmosContainer.queryItems()` | [ ] | Uses SQL-like syntax |
| Map DynamoDB key schema → Cosmos DB partition key | [ ] | |
| Replace `AttributeValue` maps → POJOs | [ ] | |
| Remove `@DynamoDbBean` / `@DynamoDbPartitionKey` annotations | [ ] | |

### Secrets (Secrets Manager → Key Vault)

| Step | Status | Notes |
|------|--------|-------|
| Remove `software.amazon.awssdk:secretsmanager` | [ ] | |
| Add `com.azure:azure-security-keyvault-secrets` | [ ] | |
| Replace `SecretsManagerClient` → `SecretClient` via `SecretClientBuilder` | [ ] | |
| Replace `getSecretValue()` → `getSecret().getValue()` | [ ] | |
| Replace `createSecret()` → `setSecret()` | [ ] | |
| Configure Key Vault RBAC | [ ] | |

### Serverless (Lambda invocation → Functions HTTP call)

| Step | Status | Notes |
|------|--------|-------|
| Remove `software.amazon.awssdk:lambda` | [ ] | |
| Replace `LambdaClient.invoke()` → `HttpClient.send()` POST | [ ] | |
| Configure Function App URL and authentication | [ ] | |

### Observability (CloudWatch → Application Insights)

| Step | Status | Notes |
|------|--------|-------|
| Remove `software.amazon.awssdk:cloudwatch` | [ ] | |
| Add `com.microsoft.azure:applicationinsights-web` | [ ] | |
| Replace `putMetricData()` → `TelemetryClient.trackMetric()` | [ ] | |
| Configure `APPLICATION_INSIGHTS_CONNECTION_STRING` env variable | [ ] | |
| Replace CloudWatch Logs → SLF4J / Logback (auto-captured) | [ ] | |

## Configuration Cleanup

| Step | Status | Notes |
|------|--------|-------|
| Remove AWS SDK BOM from `pom.xml` / `build.gradle` | [ ] | `software.amazon.awssdk:bom` |
| Add Azure SDK BOM: `com.azure:azure-sdk-bom` | [ ] | |
| Remove `~/.aws/credentials` references from documentation | [ ] | |
| Add Azure service endpoints to `application.properties` / `application.yml` | [ ] | |
| Remove all AWS access key / secret key references | [ ] | |

## Verification

| Step | Status | Notes |
|------|--------|-------|
| Project builds without AWS SDK dependencies | [ ] | `mvn clean compile` / `gradle build` |
| Unit tests pass with mocked Azure clients | [ ] | |
| Integration tests pass against Azure services | [ ] | |
| No remaining `software.amazon.awssdk` imports | [ ] | |
| No remaining `com.amazonaws` imports (v1 SDK) | [ ] | |
