# Go AWS SDK → Azure SDK Migration Checklist

> **Application:** `{{APP_NAME}}`
> **Date:** `{{DATE}}`
> **Migrated by:** `{{AUTHOR}}`

## Authentication

| Step | Status | Notes |
|------|--------|-------|
| Remove `github.com/aws/aws-sdk-go-v2/config` | [ ] | |
| Remove `github.com/aws/aws-sdk-go-v2/credentials` | [ ] | |
| Add `github.com/Azure/azure-sdk-for-go/sdk/azidentity` | [ ] | `go get` |
| Replace `config.LoadDefaultConfig()` → `azidentity.NewDefaultAzureCredential()` | [ ] | |
| Remove AWS region configuration | [ ] | Azure uses resource-specific endpoints |
| Configure Managed Identity for deployed environments | [ ] | |

## Module Replacements

### Storage (S3 → Azure Blob Storage)

| Step | Status | Notes |
|------|--------|-------|
| Remove `github.com/aws/aws-sdk-go-v2/service/s3` | [ ] | |
| Add `github.com/Azure/azure-sdk-for-go/sdk/storage/azblob` | [ ] | |
| Replace `s3.NewFromConfig()` → `azblob.NewClient()` | [ ] | |
| Replace `PutObject()` → `UploadStream()` / `UploadBuffer()` | [ ] | |
| Replace `GetObject()` → `DownloadStream()` | [ ] | |
| Replace `ListObjectsV2()` → `NewListBlobsFlatPager()` | [ ] | |
| Replace `DeleteObject()` → `DeleteBlob()` | [ ] | |
| Replace presigned URLs → SAS tokens via `sas.BlobSignatureValues` | [ ] | |

### Messaging (SQS → Azure Service Bus)

| Step | Status | Notes |
|------|--------|-------|
| Remove `github.com/aws/aws-sdk-go-v2/service/sqs` | [ ] | |
| Add `github.com/Azure/azure-sdk-for-go/sdk/messaging/azservicebus` | [ ] | |
| Replace `sqs.NewFromConfig()` → `azservicebus.NewClient()` | [ ] | |
| Replace `SendMessage()` → `Sender.SendMessage()` | [ ] | |
| Replace `ReceiveMessage()` → `Receiver.ReceiveMessages()` | [ ] | |
| Replace `DeleteMessage()` → `Receiver.CompleteMessage()` | [ ] | |
| Replace queue URL → fully qualified namespace + queue name | [ ] | |
| Ensure `Sender.Close()` / `Receiver.Close()` are called | [ ] | Use `defer` |

### NoSQL (DynamoDB → Cosmos DB)

| Step | Status | Notes |
|------|--------|-------|
| Remove `github.com/aws/aws-sdk-go-v2/service/dynamodb` | [ ] | |
| Remove `github.com/aws/aws-sdk-go-v2/feature/dynamodb/attributevalue` | [ ] | |
| Add `github.com/Azure/azure-sdk-for-go/sdk/data/azcosmos` | [ ] | |
| Replace `dynamodb.NewFromConfig()` → `azcosmos.NewClient()` | [ ] | |
| Replace `PutItem()` → `UpsertItem()` | [ ] | |
| Replace `GetItem()` → `ReadItem()` | [ ] | |
| Replace `Query()` → `NewQueryItemsPager()` | [ ] | SQL-like syntax |
| Map DynamoDB key schema → Cosmos DB partition key | [ ] | |
| Replace `attributevalue.MarshalMap()` → `json.Marshal()` | [ ] | |

### Secrets (Secrets Manager → Key Vault)

| Step | Status | Notes |
|------|--------|-------|
| Remove `github.com/aws/aws-sdk-go-v2/service/secretsmanager` | [ ] | |
| Add `github.com/Azure/azure-sdk-for-go/sdk/security/keyvault/azsecrets` | [ ] | |
| Replace `secretsmanager.NewFromConfig()` → `azsecrets.NewClient()` | [ ] | |
| Replace `GetSecretValue()` → `GetSecret()` | [ ] | |
| Replace `CreateSecret()` → `SetSecret()` | [ ] | |
| Configure Key Vault RBAC | [ ] | |

### Serverless (Lambda invocation → Functions HTTP call)

| Step | Status | Notes |
|------|--------|-------|
| Remove `github.com/aws/aws-sdk-go-v2/service/lambda` | [ ] | |
| Replace `lambda.Invoke()` → `http.Post()` | [ ] | Use `net/http` |
| Configure Function App URL and authentication | [ ] | |

### Observability (CloudWatch → Application Insights)

| Step | Status | Notes |
|------|--------|-------|
| Remove `github.com/aws/aws-sdk-go-v2/service/cloudwatch` | [ ] | |
| Add OpenTelemetry Azure Monitor exporter | [ ] | `go.opentelemetry.io/otel` |
| Replace `PutMetricData()` → OpenTelemetry meter API | [ ] | |
| Configure `APPLICATIONINSIGHTS_CONNECTION_STRING` env variable | [ ] | |

## Configuration Cleanup

| Step | Status | Notes |
|------|--------|-------|
| Remove all `github.com/aws/aws-sdk-go-v2` modules | [ ] | |
| Run `go mod tidy` | [ ] | |
| Remove AWS-related environment variables | [ ] | `AWS_ACCESS_KEY_ID`, `AWS_REGION`, etc. |
| Add Azure service endpoints to config | [ ] | |

## Verification

| Step | Status | Notes |
|------|--------|-------|
| `go build ./...` succeeds without AWS SDK imports | [ ] | |
| No remaining `aws-sdk-go` imports | [ ] | `grep -r "aws-sdk-go" .` |
| Unit tests pass with mocked Azure clients | [ ] | |
| Integration tests pass against Azure services | [ ] | |
