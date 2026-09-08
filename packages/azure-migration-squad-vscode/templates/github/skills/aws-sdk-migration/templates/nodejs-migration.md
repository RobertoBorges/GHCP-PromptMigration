# Node.js AWS SDK → Azure SDK Migration Checklist

> **Application:** `{{APP_NAME}}`
> **Date:** `{{DATE}}`
> **Migrated by:** `{{AUTHOR}}`

## Authentication

| Step | Status | Notes |
|------|--------|-------|
| Remove `@aws-sdk/credential-providers` / `aws-sdk` from `package.json` | [ ] | |
| Add `@azure/identity` | [ ] | `npm install @azure/identity` |
| Replace AWS credential chain → `new DefaultAzureCredential()` | [ ] | |
| Remove AWS region configuration | [ ] | Azure uses resource-specific endpoints |
| Configure Managed Identity for deployed environments | [ ] | |

## Package Replacements

### Storage (S3 → Blob Storage)

| Step | Status | Notes |
|------|--------|-------|
| Remove `@aws-sdk/client-s3` | [ ] | |
| Add `@azure/storage-blob` | [ ] | |
| Replace `S3Client` + `PutObjectCommand` → `BlockBlobClient.upload()` | [ ] | |
| Replace `GetObjectCommand` → `BlobClient.download()` | [ ] | |
| Replace `ListObjectsV2Command` → `ContainerClient.listBlobsFlat()` | [ ] | |
| Replace `DeleteObjectCommand` → `BlobClient.delete()` | [ ] | |
| Replace presigned URLs → `generateBlobSASQueryParameters()` | [ ] | |
| Remove `@aws-sdk/s3-request-presigner` if present | [ ] | |

### Messaging (SQS → Service Bus)

| Step | Status | Notes |
|------|--------|-------|
| Remove `@aws-sdk/client-sqs` | [ ] | |
| Add `@azure/service-bus` | [ ] | |
| Replace `SQSClient` + `SendMessageCommand` → `ServiceBusSender.sendMessages()` | [ ] | |
| Replace `ReceiveMessageCommand` → `ServiceBusReceiver.receiveMessages()` | [ ] | |
| Replace `DeleteMessageCommand` → `ServiceBusReceiver.completeMessage()` | [ ] | |
| Replace queue URL → namespace + queue name | [ ] | |
| Ensure `sender.close()` / `receiver.close()` are called | [ ] | Service Bus clients must be closed |

### NoSQL (DynamoDB → Cosmos DB)

| Step | Status | Notes |
|------|--------|-------|
| Remove `@aws-sdk/client-dynamodb` | [ ] | |
| Remove `@aws-sdk/lib-dynamodb` (if using DocumentClient) | [ ] | |
| Add `@azure/cosmos` | [ ] | |
| Replace `DynamoDBClient` + `PutItemCommand` → `container.items.upsert()` | [ ] | |
| Replace `GetItemCommand` → `container.item(id, partitionKey).read()` | [ ] | |
| Replace `QueryCommand` → `container.items.query()` | [ ] | SQL-like syntax |
| Replace `ScanCommand` → cross-partition query | [ ] | Avoid full scans |
| Remove `marshall()` / `unmarshall()` helpers | [ ] | Cosmos uses plain JSON |
| Map DynamoDB key schema → Cosmos DB partition key | [ ] | |

### Secrets (Secrets Manager → Key Vault)

| Step | Status | Notes |
|------|--------|-------|
| Remove `@aws-sdk/client-secrets-manager` | [ ] | |
| Add `@azure/keyvault-secrets` | [ ] | |
| Replace `SecretsManagerClient` + `GetSecretValueCommand` → `SecretClient.getSecret()` | [ ] | |
| Replace `CreateSecretCommand` → `SecretClient.setSecret()` | [ ] | |
| Configure Key Vault RBAC | [ ] | |

### Serverless (Lambda invocation → Functions HTTP call)

| Step | Status | Notes |
|------|--------|-------|
| Remove `@aws-sdk/client-lambda` | [ ] | |
| Replace `LambdaClient` + `InvokeCommand` → `fetch()` POST call | [ ] | |
| Configure Function App URL and authentication | [ ] | |

### Observability (CloudWatch → Application Insights)

| Step | Status | Notes |
|------|--------|-------|
| Remove `@aws-sdk/client-cloudwatch` | [ ] | |
| Add `applicationinsights` npm package | [ ] | |
| Call `appInsights.setup(connectionString).start()` at app entry | [ ] | |
| Replace `PutMetricDataCommand` → `client.trackMetric()` | [ ] | |
| Set `APPLICATIONINSIGHTS_CONNECTION_STRING` env variable | [ ] | |

## Configuration Cleanup

| Step | Status | Notes |
|------|--------|-------|
| Remove all `@aws-sdk/*` packages from `package.json` | [ ] | |
| Run `npm install` to update `package-lock.json` | [ ] | |
| Remove AWS-related environment variables | [ ] | `AWS_ACCESS_KEY_ID`, `AWS_REGION`, etc. |
| Add Azure service endpoints to environment config | [ ] | |

## Verification

| Step | Status | Notes |
|------|--------|-------|
| `npm install` succeeds with no AWS SDK packages | [ ] | |
| No `@aws-sdk/*` or `aws-sdk` imports remain | [ ] | `grep -r "@aws-sdk\|aws-sdk" src/` |
| Unit tests pass with mocked Azure clients | [ ] | |
| Integration tests pass against Azure services | [ ] | |
