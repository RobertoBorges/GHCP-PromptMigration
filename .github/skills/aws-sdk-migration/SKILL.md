---
name: aws-sdk-migration
description: Language-specific SDK migration patterns for converting AWS service calls to Azure equivalents. Covers authentication (DefaultAzureCredential), storage, messaging, NoSQL, secrets, serverless invocation, and observability. Includes per-language templates for .NET (C#), Java, Python, Node.js / TypeScript, Go, and Rust. Use during Phase 2 of the AWS-to-Azure Migration flow.
---

# AWS SDK to Azure SDK Migration Patterns

> **Skill purpose:** Provide language-specific SDK migration patterns for converting AWS service calls to Azure equivalents. Covers authentication, storage, messaging, NoSQL, secrets, serverless invocation, and observability.

## Table of Contents

- [General Principles](#general-principles)
- [1. .NET (C#)](#1-net-c)
- [2. Java](#2-java)
- [3. Python](#3-python)
- [4. Node.js / TypeScript](#4-nodejs--typescript)
- [5. Go](#5-go)
- [6. Rust](#6-rust)
- [Service Mapping Quick Reference](#service-mapping-quick-reference)

---

## General Principles

| Principle | AWS | Azure |
|-----------|-----|-------|
| **Authentication** | IAM roles, access keys, `~/.aws/credentials` | Managed Identity, `DefaultAzureCredential` (chains multiple providers) |
| **Secret management** | Secrets Manager / Parameter Store | Key Vault with RBAC |
| **Configuration** | Environment variables, SSM | App Configuration, environment variables |
| **Naming convention** | `aws-sdk-*`, `boto3`, `@aws-sdk/*` | `Azure.*`, `com.azure:*`, `azure-*`, `@azure/*` |

**Key migration rule:** Replace all AWS credential mechanisms with `DefaultAzureCredential`. This single class automatically works in local dev (Azure CLI/VS auth), CI/CD (environment variables), and production (Managed Identity) without code changes.

---

## 1. .NET (C#)

### Package Mapping

| AWS Package | Azure Package | Service |
|-------------|---------------|---------|
| `AWSSDK.S3` | `Azure.Storage.Blobs` | Object storage |
| `AWSSDK.SQS` | `Azure.Messaging.ServiceBus` | Message queuing |
| `AWSSDK.DynamoDBv2` | `Microsoft.Azure.Cosmos` | NoSQL database |
| `AWSSDK.SecretsManager` | `Azure.Security.KeyVault.Secrets` | Secrets |
| `AWSSDK.Lambda` | `Azure.ResourceManager.AppService` | Serverless invocation |
| `AWSSDK.CloudWatch` | `Microsoft.ApplicationInsights` | Observability |
| `AWSSDK.Extensions.NETCore.Setup` | `Azure.Identity` | Authentication |

### Authentication

```csharp
// ❌ AWS
using Amazon;
using Amazon.Runtime;
var credentials = new BasicAWSCredentials("accessKey", "secretKey");
var client = new AmazonS3Client(credentials, RegionEndpoint.USEast1);

// ✅ Azure — works in local dev, CI/CD, and production automatically
using Azure.Identity;
var credential = new DefaultAzureCredential();
var client = new BlobServiceClient(new Uri("https://account.blob.core.windows.net"), credential);
```

### S3 → Azure Blob Storage

```csharp
// ❌ AWS — Upload object to S3
var s3Client = new AmazonS3Client();
await s3Client.PutObjectAsync(new PutObjectRequest
{
    BucketName = "my-bucket",
    Key = "files/data.json",
    InputStream = stream
});

// ✅ Azure — Upload blob
var blobServiceClient = new BlobServiceClient(connectionUri, new DefaultAzureCredential());
var containerClient = blobServiceClient.GetBlobContainerClient("my-container");
var blobClient = containerClient.GetBlobClient("files/data.json");
await blobClient.UploadAsync(stream, overwrite: true);
```

### SQS → Azure Service Bus

```csharp
// ❌ AWS — Send SQS message
var sqsClient = new AmazonSQSClient();
await sqsClient.SendMessageAsync(new SendMessageRequest
{
    QueueUrl = "https://sqs.us-east-1.amazonaws.com/123456/my-queue",
    MessageBody = JsonSerializer.Serialize(payload)
});

// ✅ Azure — Send Service Bus message
var client = new ServiceBusClient("namespace.servicebus.windows.net", new DefaultAzureCredential());
var sender = client.CreateSender("my-queue");
await sender.SendMessageAsync(new ServiceBusMessage(JsonSerializer.Serialize(payload)));
```

### DynamoDB → Cosmos DB

```csharp
// ❌ AWS — Put item in DynamoDB
var dynamoClient = new AmazonDynamoDBClient();
await dynamoClient.PutItemAsync("my-table", new Dictionary<string, AttributeValue>
{
    ["id"] = new AttributeValue { S = "123" },
    ["name"] = new AttributeValue { S = "item-name" }
});

// ✅ Azure — Upsert item in Cosmos DB
var cosmosClient = new CosmosClient("https://account.documents.azure.com:443/", new DefaultAzureCredential());
var container = cosmosClient.GetContainer("my-database", "my-container");
await container.UpsertItemAsync(new { id = "123", name = "item-name" }, new PartitionKey("123"));
```

### Secrets Manager → Key Vault

```csharp
// ❌ AWS — Retrieve secret
var smClient = new AmazonSecretsManagerClient();
var response = await smClient.GetSecretValueAsync(new GetSecretValueRequest
{
    SecretId = "my-secret"
});
string secretValue = response.SecretString;

// ✅ Azure — Retrieve secret
var kvClient = new SecretClient(new Uri("https://my-vault.vault.azure.net/"), new DefaultAzureCredential());
KeyVaultSecret secret = await kvClient.GetSecretAsync("my-secret");
string secretValue = secret.Value;
```

### Lambda Invocation → Azure Functions

```csharp
// ❌ AWS — Invoke Lambda
var lambdaClient = new AmazonLambdaClient();
var response = await lambdaClient.InvokeAsync(new InvokeRequest
{
    FunctionName = "my-function",
    Payload = JsonSerializer.Serialize(input)
});

// ✅ Azure — Call Azure Function via HTTP (Functions are HTTP-triggered)
var httpClient = new HttpClient();
var response = await httpClient.PostAsJsonAsync(
    "https://my-func-app.azurewebsites.net/api/my-function?code=<function-key>",
    input);
```

### CloudWatch → Application Insights

```csharp
// ❌ AWS — Custom CloudWatch metric
var cwClient = new AmazonCloudWatchClient();
await cwClient.PutMetricDataAsync(new PutMetricDataRequest
{
    Namespace = "MyApp",
    MetricData = new List<MetricDatum>
    {
        new MetricDatum { MetricName = "ProcessedItems", Value = 42, Unit = StandardUnit.Count }
    }
});

// ✅ Azure — Application Insights telemetry (add Microsoft.ApplicationInsights package)
// In Program.cs: builder.Services.AddApplicationInsightsTelemetry();
var telemetryClient = app.Services.GetRequiredService<TelemetryClient>();
telemetryClient.TrackMetric("ProcessedItems", 42);
```

---

## 2. Java

### Package Mapping

| AWS Package (Maven) | Azure Package (Maven) | Service |
|----------------------|-----------------------|---------|
| `software.amazon.awssdk:s3` | `com.azure:azure-storage-blob` | Object storage |
| `software.amazon.awssdk:sqs` | `com.azure:azure-messaging-servicebus` | Message queuing |
| `software.amazon.awssdk:dynamodb` | `com.azure:azure-cosmos` | NoSQL database |
| `software.amazon.awssdk:secretsmanager` | `com.azure:azure-security-keyvault-secrets` | Secrets |
| `software.amazon.awssdk:lambda` | *(HTTP call)* | Serverless invocation |
| `software.amazon.awssdk:cloudwatch` | `com.microsoft.azure:applicationinsights-web` | Observability |
| `software.amazon.awssdk:auth` | `com.azure:azure-identity` | Authentication |

### Authentication

```java
// ❌ AWS
import software.amazon.awssdk.auth.credentials.DefaultCredentialsProvider;
import software.amazon.awssdk.services.s3.S3Client;
S3Client s3 = S3Client.builder()
    .credentialsProvider(DefaultCredentialsProvider.create())
    .region(Region.US_EAST_1)
    .build();

// ✅ Azure
import com.azure.identity.DefaultAzureCredentialBuilder;
import com.azure.storage.blob.BlobServiceClient;
import com.azure.storage.blob.BlobServiceClientBuilder;
BlobServiceClient blobClient = new BlobServiceClientBuilder()
    .endpoint("https://account.blob.core.windows.net")
    .credential(new DefaultAzureCredentialBuilder().build())
    .buildClient();
```

### S3 → Azure Blob Storage

```java
// ❌ AWS
s3.putObject(PutObjectRequest.builder()
    .bucket("my-bucket").key("files/data.json").build(),
    RequestBody.fromInputStream(inputStream, length));

// ✅ Azure
BlobClient blob = blobClient.getBlobContainerClient("my-container")
    .getBlobClient("files/data.json");
blob.upload(inputStream, length, true);
```

### SQS → Azure Service Bus

```java
// ❌ AWS
SqsClient sqs = SqsClient.builder().build();
sqs.sendMessage(SendMessageRequest.builder()
    .queueUrl("https://sqs.us-east-1.amazonaws.com/123456/my-queue")
    .messageBody(jsonPayload).build());

// ✅ Azure
ServiceBusSenderClient sender = new ServiceBusClientBuilder()
    .fullyQualifiedNamespace("namespace.servicebus.windows.net")
    .credential(new DefaultAzureCredentialBuilder().build())
    .sender().queueName("my-queue").buildClient();
sender.sendMessage(new ServiceBusMessage(jsonPayload));
```

### DynamoDB → Cosmos DB

```java
// ❌ AWS
DynamoDbClient dynamo = DynamoDbClient.builder().build();
dynamo.putItem(PutItemRequest.builder().tableName("my-table")
    .item(Map.of(
        "id", AttributeValue.builder().s("123").build(),
        "name", AttributeValue.builder().s("item-name").build()))
    .build());

// ✅ Azure
CosmosClient cosmos = new CosmosClientBuilder()
    .endpoint("https://account.documents.azure.com:443/")
    .credential(new DefaultAzureCredentialBuilder().build())
    .buildClient();
CosmosContainer container = cosmos.getDatabase("my-database").getContainer("my-container");
container.upsertItem(Map.of("id", "123", "name", "item-name"));
```

### Secrets Manager → Key Vault

```java
// ❌ AWS
SecretsManagerClient sm = SecretsManagerClient.builder().build();
String secret = sm.getSecretValue(GetSecretValueRequest.builder()
    .secretId("my-secret").build()).secretString();

// ✅ Azure
SecretClient kvClient = new SecretClientBuilder()
    .vaultUrl("https://my-vault.vault.azure.net/")
    .credential(new DefaultAzureCredentialBuilder().build())
    .buildClient();
String secret = kvClient.getSecret("my-secret").getValue();
```

### Lambda → Azure Functions

```java
// ❌ AWS
LambdaClient lambda = LambdaClient.builder().build();
InvokeResponse resp = lambda.invoke(InvokeRequest.builder()
    .functionName("my-function").payload(SdkBytes.fromUtf8String(json)).build());

// ✅ Azure — Call Function via HTTP
HttpClient http = HttpClient.newHttpClient();
HttpResponse<String> resp = http.send(HttpRequest.newBuilder()
    .uri(URI.create("https://my-func-app.azurewebsites.net/api/my-function"))
    .POST(HttpRequest.BodyPublishers.ofString(json)).build(),
    HttpResponse.BodyHandlers.ofString());
```

### CloudWatch → Application Insights

```java
// ❌ AWS
CloudWatchClient cw = CloudWatchClient.builder().build();
cw.putMetricData(PutMetricDataRequest.builder().namespace("MyApp")
    .metricData(MetricDatum.builder()
        .metricName("ProcessedItems").value(42.0).unit(StandardUnit.COUNT).build())
    .build());

// ✅ Azure — Application Insights via applicationinsights-web
// Configured via APPLICATION_INSIGHTS_CONNECTION_STRING env var
TelemetryClient telemetry = new TelemetryClient();
telemetry.trackMetric("ProcessedItems", 42);
```

---

## 3. Python

### Package Mapping

| AWS Package | Azure Package | Service |
|-------------|---------------|---------|
| `boto3` (s3) | `azure-storage-blob` | Object storage |
| `boto3` (sqs) | `azure-servicebus` | Message queuing |
| `boto3` (dynamodb) | `azure-cosmos` | NoSQL database |
| `boto3` (secretsmanager) | `azure-keyvault-secrets` | Secrets |
| `boto3` (lambda) | *(HTTP call via `requests`)* | Serverless invocation |
| `boto3` (cloudwatch) | `opencensus-ext-azure` | Observability |
| `boto3` | `azure-identity` | Authentication |

### Authentication

```python
# ❌ AWS
import boto3
session = boto3.Session(
    aws_access_key_id="AKIA...",
    aws_secret_access_key="secret",
    region_name="us-east-1"
)
s3 = session.client("s3")

# ✅ Azure
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient
credential = DefaultAzureCredential()
blob_service = BlobServiceClient("https://account.blob.core.windows.net", credential=credential)
```

### S3 → Azure Blob Storage

```python
# ❌ AWS
s3 = boto3.client("s3")
s3.upload_fileobj(file_obj, "my-bucket", "files/data.json")

# ✅ Azure
blob_service = BlobServiceClient(account_url, credential=DefaultAzureCredential())
blob_client = blob_service.get_blob_client("my-container", "files/data.json")
blob_client.upload_blob(file_obj, overwrite=True)
```

### SQS → Azure Service Bus

```python
# ❌ AWS
sqs = boto3.client("sqs")
sqs.send_message(
    QueueUrl="https://sqs.us-east-1.amazonaws.com/123456/my-queue",
    MessageBody=json.dumps(payload)
)

# ✅ Azure
from azure.servicebus import ServiceBusClient, ServiceBusMessage
sb_client = ServiceBusClient("namespace.servicebus.windows.net", credential=DefaultAzureCredential())
with sb_client.get_queue_sender("my-queue") as sender:
    sender.send_messages(ServiceBusMessage(json.dumps(payload)))
```

### DynamoDB → Cosmos DB

```python
# ❌ AWS
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("my-table")
table.put_item(Item={"id": "123", "name": "item-name"})

# ✅ Azure
from azure.cosmos import CosmosClient
cosmos = CosmosClient("https://account.documents.azure.com:443/", credential=DefaultAzureCredential())
container = cosmos.get_database_client("my-database").get_container_client("my-container")
container.upsert_item({"id": "123", "name": "item-name"})
```

### Secrets Manager → Key Vault

```python
# ❌ AWS
sm = boto3.client("secretsmanager")
secret = sm.get_secret_value(SecretId="my-secret")["SecretString"]

# ✅ Azure
from azure.keyvault.secrets import SecretClient
kv_client = SecretClient("https://my-vault.vault.azure.net/", credential=DefaultAzureCredential())
secret = kv_client.get_secret("my-secret").value
```

### Lambda → Azure Functions

```python
# ❌ AWS
lambda_client = boto3.client("lambda")
response = lambda_client.invoke(FunctionName="my-function", Payload=json.dumps(input_data))

# ✅ Azure — Call Function via HTTP
import requests
response = requests.post(
    "https://my-func-app.azurewebsites.net/api/my-function",
    json=input_data
)
```

### CloudWatch → Application Insights

```python
# ❌ AWS
cw = boto3.client("cloudwatch")
cw.put_metric_data(Namespace="MyApp", MetricData=[
    {"MetricName": "ProcessedItems", "Value": 42, "Unit": "Count"}
])

# ✅ Azure — Application Insights via OpenCensus
from opencensus.ext.azure import metrics_exporter
exporter = metrics_exporter.new_metrics_exporter(connection_string="InstrumentationKey=...")
# Or use the Azure Monitor OpenTelemetry Distro:
# pip install azure-monitor-opentelemetry
```

---

## 4. Node.js / TypeScript

### Package Mapping

| AWS Package | Azure Package | Service |
|-------------|---------------|---------|
| `@aws-sdk/client-s3` | `@azure/storage-blob` | Object storage |
| `@aws-sdk/client-sqs` | `@azure/service-bus` | Message queuing |
| `@aws-sdk/client-dynamodb` | `@azure/cosmos` | NoSQL database |
| `@aws-sdk/client-secrets-manager` | `@azure/keyvault-secrets` | Secrets |
| `@aws-sdk/client-lambda` | *(HTTP call via `fetch`)* | Serverless invocation |
| `@aws-sdk/client-cloudwatch` | `applicationinsights` | Observability |
| `@aws-sdk/credential-providers` | `@azure/identity` | Authentication |

### Authentication

```typescript
// ❌ AWS
import { S3Client } from "@aws-sdk/client-s3";
const s3 = new S3Client({ region: "us-east-1" }); // uses ~/.aws/credentials

// ✅ Azure
import { DefaultAzureCredential } from "@azure/identity";
import { BlobServiceClient } from "@azure/storage-blob";
const credential = new DefaultAzureCredential();
const blobService = new BlobServiceClient("https://account.blob.core.windows.net", credential);
```

### S3 → Azure Blob Storage

```typescript
// ❌ AWS
import { PutObjectCommand } from "@aws-sdk/client-s3";
await s3.send(new PutObjectCommand({
  Bucket: "my-bucket", Key: "files/data.json", Body: buffer
}));

// ✅ Azure
const containerClient = blobService.getContainerClient("my-container");
const blobClient = containerClient.getBlockBlobClient("files/data.json");
await blobClient.upload(buffer, buffer.length);
```

### SQS → Azure Service Bus

```typescript
// ❌ AWS
import { SQSClient, SendMessageCommand } from "@aws-sdk/client-sqs";
const sqs = new SQSClient({});
await sqs.send(new SendMessageCommand({
  QueueUrl: "https://sqs.us-east-1.amazonaws.com/123456/my-queue",
  MessageBody: JSON.stringify(payload)
}));

// ✅ Azure
import { ServiceBusClient } from "@azure/service-bus";
const sbClient = new ServiceBusClient("namespace.servicebus.windows.net", credential);
const sender = sbClient.createSender("my-queue");
await sender.sendMessages({ body: JSON.stringify(payload) });
await sender.close();
```

### DynamoDB → Cosmos DB

```typescript
// ❌ AWS
import { DynamoDBClient, PutItemCommand } from "@aws-sdk/client-dynamodb";
const dynamo = new DynamoDBClient({});
await dynamo.send(new PutItemCommand({
  TableName: "my-table",
  Item: { id: { S: "123" }, name: { S: "item-name" } }
}));

// ✅ Azure
import { CosmosClient } from "@azure/cosmos";
const cosmos = new CosmosClient({ endpoint: "https://account.documents.azure.com:443/", aadCredentials: credential });
const container = cosmos.database("my-database").container("my-container");
await container.items.upsert({ id: "123", name: "item-name" });
```

### Secrets Manager → Key Vault

```typescript
// ❌ AWS
import { SecretsManagerClient, GetSecretValueCommand } from "@aws-sdk/client-secrets-manager";
const sm = new SecretsManagerClient({});
const { SecretString } = await sm.send(new GetSecretValueCommand({ SecretId: "my-secret" }));

// ✅ Azure
import { SecretClient } from "@azure/keyvault-secrets";
const kvClient = new SecretClient("https://my-vault.vault.azure.net/", credential);
const secret = await kvClient.getSecret("my-secret");
const secretValue = secret.value;
```

### Lambda → Azure Functions

```typescript
// ❌ AWS
import { LambdaClient, InvokeCommand } from "@aws-sdk/client-lambda";
const lambda = new LambdaClient({});
const resp = await lambda.send(new InvokeCommand({
  FunctionName: "my-function", Payload: JSON.stringify(input)
}));

// ✅ Azure — Call Function via HTTP
const resp = await fetch(
  "https://my-func-app.azurewebsites.net/api/my-function",
  { method: "POST", body: JSON.stringify(input), headers: { "Content-Type": "application/json" } }
);
```

### CloudWatch → Application Insights

```typescript
// ❌ AWS
import { CloudWatchClient, PutMetricDataCommand } from "@aws-sdk/client-cloudwatch";
const cw = new CloudWatchClient({});
await cw.send(new PutMetricDataCommand({
  Namespace: "MyApp",
  MetricData: [{ MetricName: "ProcessedItems", Value: 42, Unit: "Count" }]
}));

// ✅ Azure — Application Insights
import appInsights from "applicationinsights";
appInsights.setup(process.env.APPLICATIONINSIGHTS_CONNECTION_STRING).start();
const client = appInsights.defaultClient;
client.trackMetric({ name: "ProcessedItems", value: 42 });
```

---

## 5. Go

### Package Mapping

| AWS Package | Azure Package | Service |
|-------------|---------------|---------|
| `github.com/aws/aws-sdk-go-v2/service/s3` | `github.com/Azure/azure-sdk-for-go/sdk/storage/azblob` | Object storage |
| `github.com/aws/aws-sdk-go-v2/service/sqs` | `github.com/Azure/azure-sdk-for-go/sdk/messaging/azservicebus` | Message queuing |
| `github.com/aws/aws-sdk-go-v2/service/dynamodb` | `github.com/Azure/azure-sdk-for-go/sdk/data/azcosmos` | NoSQL database |
| `github.com/aws/aws-sdk-go-v2/service/secretsmanager` | `github.com/Azure/azure-sdk-for-go/sdk/security/keyvault/azsecrets` | Secrets |
| `github.com/aws/aws-sdk-go-v2/service/lambda` | *(HTTP call via `net/http`)* | Serverless invocation |
| `github.com/aws/aws-sdk-go-v2/service/cloudwatch` | `github.com/microsoft/ApplicationInsights-Go` | Observability |
| `github.com/aws/aws-sdk-go-v2/config` | `github.com/Azure/azure-sdk-for-go/sdk/azidentity` | Authentication |

### Authentication

```go
// ❌ AWS
import "github.com/aws/aws-sdk-go-v2/config"
cfg, _ := config.LoadDefaultConfig(ctx, config.WithRegion("us-east-1"))
s3Client := s3.NewFromConfig(cfg)

// ✅ Azure
import "github.com/Azure/azure-sdk-for-go/sdk/azidentity"
cred, _ := azidentity.NewDefaultAzureCredential(nil)
client, _ := azblob.NewClient("https://account.blob.core.windows.net/", cred, nil)
```

### S3 → Azure Blob Storage

```go
// ❌ AWS
s3Client.PutObject(ctx, &s3.PutObjectInput{
    Bucket: aws.String("my-bucket"),
    Key:    aws.String("files/data.json"),
    Body:   reader,
})

// ✅ Azure
client, _ := azblob.NewClient(serviceURL, cred, nil)
_, err := client.UploadStream(ctx, "my-container", "files/data.json", reader, nil)
```

### SQS → Azure Service Bus

```go
// ❌ AWS
sqsClient.SendMessage(ctx, &sqs.SendMessageInput{
    QueueUrl:    aws.String("https://sqs.us-east-1.amazonaws.com/123456/my-queue"),
    MessageBody: aws.String(jsonPayload),
})

// ✅ Azure
client, _ := azservicebus.NewClient("namespace.servicebus.windows.net", cred, nil)
sender, _ := client.NewSender("my-queue", nil)
sender.SendMessage(ctx, &azservicebus.Message{Body: []byte(jsonPayload)}, nil)
```

### DynamoDB → Cosmos DB

```go
// ❌ AWS
dynamoClient.PutItem(ctx, &dynamodb.PutItemInput{
    TableName: aws.String("my-table"),
    Item: map[string]types.AttributeValue{
        "id":   &types.AttributeValueMemberS{Value: "123"},
        "name": &types.AttributeValueMemberS{Value: "item-name"},
    },
})

// ✅ Azure
client, _ := azcosmos.NewClient("https://account.documents.azure.com:443/", cred, nil)
container, _ := client.NewContainer("my-database", "my-container")
pk := azcosmos.NewPartitionKeyString("123")
item, _ := json.Marshal(map[string]string{"id": "123", "name": "item-name"})
container.UpsertItem(ctx, pk, item, nil)
```

### Secrets Manager → Key Vault

```go
// ❌ AWS
smClient.GetSecretValue(ctx, &secretsmanager.GetSecretValueInput{
    SecretId: aws.String("my-secret"),
})

// ✅ Azure
client, _ := azsecrets.NewClient("https://my-vault.vault.azure.net/", cred, nil)
resp, _ := client.GetSecret(ctx, "my-secret", "", nil)
secretValue := *resp.Value
```

### Lambda → Azure Functions

```go
// ❌ AWS
lambdaClient.Invoke(ctx, &lambda.InvokeInput{
    FunctionName: aws.String("my-function"),
    Payload:      jsonBytes,
})

// ✅ Azure — Call Function via HTTP
resp, _ := http.Post(
    "https://my-func-app.azurewebsites.net/api/my-function",
    "application/json",
    bytes.NewReader(jsonBytes),
)
```

### CloudWatch → Application Insights

```go
// ❌ AWS
cwClient.PutMetricData(ctx, &cloudwatch.PutMetricDataInput{
    Namespace: aws.String("MyApp"),
    MetricData: []cwtypes.MetricDatum{{
        MetricName: aws.String("ProcessedItems"),
        Value:      aws.Float64(42),
        Unit:       cwtypes.StandardUnitCount,
    }},
})

// ✅ Azure — Application Insights via OpenTelemetry exporter
// Use github.com/microsoft/ApplicationInsights-Go or OpenTelemetry with Azure Monitor exporter
// go get go.opentelemetry.io/otel
// go get github.com/Azure/azure-sdk-for-go/sdk/monitor/azingest
```

---

## 6. Rust

> **⚠️ Note:** Azure's official Rust SDK has limited service coverage. Many services require using REST APIs via `azure_core::HttpClient`. The patterns below use official crates where available and note REST API fallbacks.

### Package Mapping

| AWS Crate | Azure Crate | Notes |
|-----------|-------------|-------|
| `aws-sdk-s3` | `azure_storage_blobs` | Official SDK available |
| `aws-sdk-sqs` | *(REST API via `azure_core`)* | No official Service Bus crate |
| `aws-sdk-dynamodb` | *(REST API via `azure_core`)* | No official Cosmos DB Rust crate |
| `aws-sdk-secretsmanager` | `azure_security_keyvault` | Official SDK available |
| `aws-sdk-lambda` | *(HTTP call via `reqwest`)* | Use standard HTTP |
| `aws-config` | `azure_identity` | Official SDK available |

### Authentication

```rust
// ❌ AWS
use aws_config::meta::region::RegionProviderChain;
let config = aws_config::defaults(BehaviorVersion::latest())
    .region(RegionProviderChain::default_provider().or_else("us-east-1"))
    .load().await;
let s3_client = aws_sdk_s3::Client::new(&config);

// ✅ Azure
use azure_identity::DefaultAzureCredential;
use azure_storage_blobs::prelude::*;
let credential = DefaultAzureCredential::default();
let blob_service = BlobServiceClient::new("https://account.blob.core.windows.net", credential.clone());
```

### S3 → Azure Blob Storage

```rust
// ❌ AWS
s3_client.put_object()
    .bucket("my-bucket")
    .key("files/data.json")
    .body(ByteStream::from(data))
    .send().await?;

// ✅ Azure
let container_client = blob_service.container_client("my-container");
let blob_client = container_client.blob_client("files/data.json");
blob_client.put_block_blob(data).await?;
```

### Secrets Manager → Key Vault

```rust
// ❌ AWS
let resp = sm_client.get_secret_value()
    .secret_id("my-secret")
    .send().await?;
let secret = resp.secret_string().unwrap();

// ✅ Azure
use azure_security_keyvault::SecretClient;
let kv_client = SecretClient::new("https://my-vault.vault.azure.net/", credential)?;
let secret = kv_client.get("my-secret").await?.value;
```

### Services Without Official Rust SDK

For SQS → Service Bus, DynamoDB → Cosmos DB, and other services without official Rust crates, use the Azure REST API directly:

```rust
// ✅ Azure REST API pattern (using azure_core + reqwest)
use azure_identity::DefaultAzureCredential;
use azure_core::auth::TokenCredential;

let credential = DefaultAzureCredential::default();
let token = credential.get_token(&["https://servicebus.azure.net/.default"]).await?;

let client = reqwest::Client::new();
let resp = client.post("https://namespace.servicebus.windows.net/my-queue/messages")
    .bearer_auth(token.token.secret())
    .header("Content-Type", "application/json")
    .body(json_payload)
    .send().await?;
```

---

## Service Mapping Quick Reference

| AWS Service | Azure Service | Key Difference |
|-------------|---------------|----------------|
| S3 | Azure Blob Storage | Buckets → Containers, Objects → Blobs |
| SQS | Azure Service Bus | Queue URL → Namespace + Queue name, supports sessions/topics |
| DynamoDB | Cosmos DB | Tables → Containers with partition keys, multiple consistency models |
| Secrets Manager | Key Vault | Flat names, RBAC-based access, also stores keys and certificates |
| Lambda | Azure Functions | SDK invocation → HTTP triggers, Durable Functions for orchestration |
| CloudWatch | Application Insights | Integrated APM, uses connection strings, OpenTelemetry support |
| IAM Roles | Managed Identity | Automatic credential via `DefaultAzureCredential`, no key rotation needed |
| Parameter Store | App Configuration | Feature flags support, Key Vault references for secrets |
