# Python AWS SDK → Azure SDK Migration Checklist

> **Application:** `{{APP_NAME}}`
> **Date:** `{{DATE}}`
> **Migrated by:** `{{AUTHOR}}`

## Authentication

| Step | Status | Notes |
|------|--------|-------|
| Remove `boto3` / `botocore` from `requirements.txt` | [ ] | |
| Add `azure-identity` to `requirements.txt` | [ ] | |
| Replace `boto3.Session()` → `DefaultAzureCredential()` | [ ] | |
| Remove AWS region / profile configuration | [ ] | Azure uses resource-specific endpoints |
| Configure Managed Identity for deployed environments | [ ] | |

## Package Replacements

### Storage (S3 → Blob Storage)

| Step | Status | Notes |
|------|--------|-------|
| Add `azure-storage-blob` to `requirements.txt` | [ ] | |
| Replace `boto3.client("s3")` → `BlobServiceClient()` | [ ] | |
| Replace `upload_fileobj()` / `put_object()` → `BlobClient.upload_blob()` | [ ] | |
| Replace `download_fileobj()` / `get_object()` → `BlobClient.download_blob()` | [ ] | |
| Replace `list_objects_v2()` → `ContainerClient.list_blobs()` | [ ] | |
| Replace `delete_object()` → `BlobClient.delete_blob()` | [ ] | |
| Replace `generate_presigned_url()` → `generate_blob_sas()` | [ ] | |
| Update bucket names → container names | [ ] | Lowercase only in Azure |

### Messaging (SQS → Service Bus)

| Step | Status | Notes |
|------|--------|-------|
| Add `azure-servicebus` to `requirements.txt` | [ ] | |
| Replace `boto3.client("sqs")` → `ServiceBusClient()` | [ ] | |
| Replace `send_message()` → `ServiceBusSender.send_messages()` | [ ] | |
| Replace `receive_message()` → `ServiceBusReceiver.receive_messages()` | [ ] | |
| Replace `delete_message()` → `ServiceBusReceiver.complete_message()` | [ ] | |
| Replace queue URL → fully qualified namespace + queue name | [ ] | |
| Handle dead-letter queue differences | [ ] | Built-in DLQ in Service Bus |

### NoSQL (DynamoDB → Cosmos DB)

| Step | Status | Notes |
|------|--------|-------|
| Add `azure-cosmos` to `requirements.txt` | [ ] | |
| Replace `boto3.resource("dynamodb")` → `CosmosClient()` | [ ] | |
| Replace `table.put_item()` → `container.upsert_item()` | [ ] | |
| Replace `table.get_item()` → `container.read_item()` | [ ] | Requires `partition_key` param |
| Replace `table.query()` → `container.query_items()` | [ ] | SQL-like syntax |
| Replace `table.scan()` → cross-partition query | [ ] | Avoid full scans |
| Map DynamoDB key schema → Cosmos DB partition key | [ ] | |
| Convert DynamoDB item format → plain Python dicts | [ ] | No `Decimal` type issues in Cosmos |

### Secrets (Secrets Manager → Key Vault)

| Step | Status | Notes |
|------|--------|-------|
| Add `azure-keyvault-secrets` to `requirements.txt` | [ ] | |
| Replace `boto3.client("secretsmanager")` → `SecretClient()` | [ ] | |
| Replace `get_secret_value()["SecretString"]` → `get_secret().value` | [ ] | |
| Replace `create_secret()` / `put_secret_value()` → `set_secret()` | [ ] | |
| Configure Key Vault RBAC | [ ] | |

### Serverless (Lambda invocation → Functions HTTP call)

| Step | Status | Notes |
|------|--------|-------|
| Replace `boto3.client("lambda").invoke()` → `requests.post()` | [ ] | |
| Add `requests` to `requirements.txt` (if not present) | [ ] | |
| Configure Function App URL and key | [ ] | |

### Observability (CloudWatch → Application Insights)

| Step | Status | Notes |
|------|--------|-------|
| Replace `boto3.client("cloudwatch")` calls | [ ] | |
| Add `azure-monitor-opentelemetry` to `requirements.txt` | [ ] | |
| Configure `APPLICATIONINSIGHTS_CONNECTION_STRING` env variable | [ ] | |
| Replace `put_metric_data()` → OpenTelemetry metrics API | [ ] | |
| Replace CloudWatch Logs → Python `logging` (auto-captured) | [ ] | |

## Configuration Cleanup

| Step | Status | Notes |
|------|--------|-------|
| Remove `boto3`, `botocore`, `s3transfer` from `requirements.txt` | [ ] | |
| Remove AWS-related environment variables from config | [ ] | `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, etc. |
| Remove `~/.aws/credentials` references from docs | [ ] | |
| Add Azure service endpoints to environment config | [ ] | |

## Verification

| Step | Status | Notes |
|------|--------|-------|
| `pip install -r requirements.txt` succeeds | [ ] | |
| No `boto3` / `botocore` imports remain | [ ] | |
| Unit tests pass with mocked Azure clients | [ ] | |
| Integration tests pass against Azure services | [ ] | |
