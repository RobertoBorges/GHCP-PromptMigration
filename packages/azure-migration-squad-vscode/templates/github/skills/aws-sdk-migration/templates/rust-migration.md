# Rust AWS SDK → Azure SDK Migration Checklist

> **Application:** `{{APP_NAME}}`
> **Date:** `{{DATE}}`
> **Migrated by:** `{{AUTHOR}}`

> **⚠️ Important:** Azure's official Rust SDK has limited service coverage. Many services require REST API calls via `azure_core`. This checklist notes where official crates exist and where REST API fallbacks are needed.

## Authentication

| Step | Status | Notes |
|------|--------|-------|
| Remove `aws-config` from `Cargo.toml` | [ ] | |
| Remove `aws-credential-types` if present | [ ] | |
| Add `azure_identity` to `Cargo.toml` | [ ] | |
| Replace `aws_config::defaults().load()` → `DefaultAzureCredential::default()` | [ ] | |
| Remove AWS region configuration | [ ] | Azure uses resource-specific endpoints |
| Configure Managed Identity for deployed environments | [ ] | |

## Crate Replacements

### Storage (S3 → Azure Blob Storage) — ✅ Official SDK

| Step | Status | Notes |
|------|--------|-------|
| Remove `aws-sdk-s3` from `Cargo.toml` | [ ] | |
| Add `azure_storage_blobs` to `Cargo.toml` | [ ] | |
| Replace `aws_sdk_s3::Client::new()` → `BlobServiceClient::new()` | [ ] | |
| Replace `put_object()` → `put_block_blob()` | [ ] | |
| Replace `get_object()` → `get_blob()` | [ ] | |
| Replace `list_objects_v2()` → `list_blobs()` | [ ] | |
| Replace `delete_object()` → `delete_blob()` | [ ] | |
| Replace presigned URLs → SAS tokens | [ ] | |

### Messaging (SQS → Azure Service Bus) — ⚠️ REST API Required

| Step | Status | Notes |
|------|--------|-------|
| Remove `aws-sdk-sqs` from `Cargo.toml` | [ ] | |
| Add `azure_core`, `reqwest`, `azure_identity` | [ ] | No official Service Bus crate |
| Implement REST client for Service Bus API | [ ] | `POST https://{ns}.servicebus.windows.net/{queue}/messages` |
| Use `DefaultAzureCredential` for token with scope `https://servicebus.azure.net/.default` | [ ] | |
| Implement send via `POST` with `BrokerProperties` header | [ ] | |
| Implement receive via `POST .../messages/head` | [ ] | |
| Implement complete via `DELETE` on lock URI | [ ] | |
| **Alternative:** Consider using `azure_messaging_servicebus` if available | [ ] | Check crates.io for latest |

### NoSQL (DynamoDB → Cosmos DB) — ⚠️ REST API Required

| Step | Status | Notes |
|------|--------|-------|
| Remove `aws-sdk-dynamodb` from `Cargo.toml` | [ ] | |
| Add `azure_core`, `reqwest`, `azure_identity` | [ ] | No official Cosmos DB Rust crate |
| Implement REST client for Cosmos DB SQL API | [ ] | Uses custom auth headers |
| Use `DefaultAzureCredential` for AAD token | [ ] | Scope: `https://{account}.documents.azure.com/.default` |
| Implement `POST` for upsert (`x-ms-documentdb-is-upsert: true`) | [ ] | |
| Implement `GET` for point reads | [ ] | |
| Implement `POST` with SQL query body for queries | [ ] | |
| Map DynamoDB key schema → Cosmos DB partition key | [ ] | |
| **Alternative:** Consider community crate `azure_data_cosmos` if available | [ ] | Check crates.io |

### Secrets (Secrets Manager → Key Vault) — ✅ Official SDK

| Step | Status | Notes |
|------|--------|-------|
| Remove `aws-sdk-secretsmanager` from `Cargo.toml` | [ ] | |
| Add `azure_security_keyvault` to `Cargo.toml` | [ ] | |
| Replace `get_secret_value()` → `SecretClient.get()` | [ ] | |
| Replace `create_secret()` → `SecretClient.set()` | [ ] | |
| Configure Key Vault RBAC | [ ] | |

### Serverless (Lambda invocation → Functions HTTP call)

| Step | Status | Notes |
|------|--------|-------|
| Remove `aws-sdk-lambda` from `Cargo.toml` | [ ] | |
| Replace `invoke()` → `reqwest::Client::post()` | [ ] | Standard HTTP call |
| Configure Function App URL and authentication | [ ] | |

### Observability (CloudWatch → Application Insights) — ⚠️ REST API / OpenTelemetry

| Step | Status | Notes |
|------|--------|-------|
| Remove `aws-sdk-cloudwatch` from `Cargo.toml` | [ ] | |
| Add `opentelemetry` + Azure Monitor exporter | [ ] | Use OpenTelemetry Rust SDK |
| Replace `put_metric_data()` → OTel meter API | [ ] | |
| Configure `APPLICATIONINSIGHTS_CONNECTION_STRING` | [ ] | |
| **Alternative:** Send telemetry via App Insights REST API | [ ] | `POST /v2/track` |

## REST API Fallback Pattern

For services without official Rust crates, use this pattern:

```rust
use azure_identity::DefaultAzureCredential;
use azure_core::auth::TokenCredential;

let credential = DefaultAzureCredential::default();
let token = credential
    .get_token(&["https://<service>.azure.net/.default"])
    .await?;

let client = reqwest::Client::new();
let response = client
    .post("https://<resource>.<service>.azure.net/<path>")
    .bearer_auth(token.token.secret())
    .header("Content-Type", "application/json")
    .body(payload)
    .send()
    .await?;
```

## Configuration Cleanup

| Step | Status | Notes |
|------|--------|-------|
| Remove all `aws-sdk-*` and `aws-config` from `Cargo.toml` | [ ] | |
| Run `cargo update` | [ ] | |
| Remove AWS-related environment variables | [ ] | |
| Add Azure service endpoints to config | [ ] | |

## Verification

| Step | Status | Notes |
|------|--------|-------|
| `cargo build` succeeds without AWS SDK crates | [ ] | |
| No remaining `aws_sdk_*` or `aws_config` use statements | [ ] | |
| Unit tests pass with mocked Azure clients | [ ] | |
| Integration tests pass against Azure services | [ ] | |
| REST API fallback endpoints return expected responses | [ ] | |
