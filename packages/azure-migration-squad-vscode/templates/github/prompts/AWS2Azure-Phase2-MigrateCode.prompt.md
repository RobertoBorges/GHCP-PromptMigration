---
name: Phase2-MigrateCode
description: Migrate AWS SDKs to Azure SDKs, convert service integrations, and update configurations
argument-hint: "Specify language or service focus, e.g., 'Migrate Python boto3 to Azure SDK' or 'Convert SQS to Service Bus'"
agent: AWS to Azure Migration Agent
---

Migrate application code from AWS services to Azure services.

Use the assessment report generated in Phase 1 to inform the migration process. The assessment report can be found in the 'reports' folder.

## Skills to Load

Load the appropriate skills based on migration needs:
- **business-logic-mapping** skill — **ALWAYS** use to track and preserve business logic during migration
- **aws-sdk-migration** skill — SDK migration patterns for the detected language
- **config-transformation** skill — AWS config → Azure config patterns
- **azure-compatibility-assessment** skill — Reference the remediation list from Phase 1

## Pre-Migration: Compatibility Remediation

Before starting service migration, address ALL items from the Phase 1 compatibility remediation list:
1. **Upgrade runtime/framework versions** if needed for Azure SDK support
2. **Replace AWS-proprietary features** with Azure-compatible alternatives
3. **Update container base images** for Azure compatibility
4. **Refactor database access code** for Azure-compatible patterns
5. **Replace AWS-locked third-party libraries** with portable or Azure-native equivalents

## Business Logic Preservation (Critical)

Before making any code changes:
1. **Create** `reports/Business-Logic-Mapping.md` to track all business logic
2. **Identify** all business logic in the application — including cloud service interaction patterns
3. **Document** each business logic item with source location
4. **Update** the mapping document as you migrate each item
5. **Verify** each migrated item produces the same results

Categories to track:
- Calculations (pricing, tax, discounts, etc.)
- Validations (business rules, constraints)
- Workflows (state machines, approval chains)
- Transformations (data conversions, aggregations)
- Cloud Service Integrations (storage, messaging, database calls)
- Authentication flows (IAM, Cognito, STS)
- Event-driven patterns (EventBridge, SNS/SQS triggers)
- Scheduled jobs (CloudWatch Events, cron-based Lambda)

## Code Migration Process

### Step 1: AWS Credential Removal
- Remove all hardcoded AWS credentials (access keys, secret keys, session tokens)
- Remove AWS credential file references (`.aws/credentials`, `.aws/config`)
- Replace with Azure `DefaultAzureCredential` / Managed Identity pattern
- Update environment variable names (`AWS_*` → `AZURE_*`)
- Remove AWS STS `AssumeRole` patterns — replace with Entra ID token acquisition

### Step 2: AWS SDK → Azure SDK Migration

Load **aws-sdk-migration** skill for language-specific patterns.

**For .NET Applications:**
- Replace `AWSSDK.*` NuGet packages with `Azure.*` packages
- Replace AWS credential providers with `Azure.Identity`
- Migrate S3 operations → `Azure.Storage.Blobs`
- Migrate SQS operations → `Azure.Messaging.ServiceBus`
- Migrate DynamoDB operations → `Microsoft.Azure.Cosmos`
- Migrate Secrets Manager → `Azure.Security.KeyVault.Secrets`
- Use `get_errors` to validate after each package migration

**For Java Applications:**
- Replace `software.amazon.awssdk` dependencies with `com.azure` packages
- Replace AWS credentials with `azure-identity` `DefaultAzureCredentialBuilder`
- Migrate S3 → `azure-storage-blob`
- Migrate SQS → `azure-messaging-servicebus`
- Migrate DynamoDB → `azure-cosmos`
- Migrate Secrets Manager → `azure-security-keyvault-secrets`

**For Python Applications:**
- Replace `boto3`/`botocore` with `azure-*` packages
- Replace `boto3.Session` with `DefaultAzureCredential`
- Migrate S3 → `azure-storage-blob`
- Migrate SQS → `azure-servicebus`
- Migrate DynamoDB → `azure-cosmos`
- Migrate Secrets Manager → `azure-keyvault-secrets`

**For Node.js Applications:**
- Replace `@aws-sdk/*` packages with `@azure/*` packages
- Replace AWS credential providers with `@azure/identity`
- Migrate `@aws-sdk/client-s3` → `@azure/storage-blob`
- Migrate `@aws-sdk/client-sqs` → `@azure/service-bus`
- Migrate `@aws-sdk/client-dynamodb` → `@azure/cosmos`
- Migrate `@aws-sdk/client-secrets-manager` → `@azure/keyvault-secrets`

**For Go Applications:**
- Replace `github.com/aws/aws-sdk-go-v2` with Azure SDK modules
- Replace AWS config with `azidentity.NewDefaultAzureCredential`
- Migrate S3 → `azblob`
- Migrate SQS → `azservicebus`
- Migrate DynamoDB → `azcosmos`

**For Rust Applications:**
- Replace `aws-sdk-*` crates with `azure_*` crates where available
- Note: Azure Rust SDK has limited coverage — use `azure_core` for REST API fallback
- Migrate `aws-sdk-s3` → `azure_storage_blobs`
- For services without Rust SDK: implement REST API calls with `azure_core::HttpClient`

### Step 3: Service Integration Migration

For each AWS service used, convert to the Azure equivalent per the assessment mapping:

| Migration | Key Changes |
|-----------|------------|
| S3 → Blob Storage | Bucket → Container, Key → Blob name, pre-signed URLs → SAS tokens |
| SQS → Service Bus | Queue URL → Queue name + connection, message attributes → custom properties |
| SNS → Service Bus Topics / Event Grid | Topic ARN → Topic name, subscriptions → topic subscriptions |
| DynamoDB → Cosmos DB | Table → Container, partition key mapping, query syntax changes |
| Lambda invoke → Azure Functions HTTP | Invoke API → HTTP trigger URL |
| Secrets Manager → Key Vault | Secret ARN → Vault URL + secret name |
| SES → Azure Communication Services | SES API → ACS Email API |
| CloudWatch metrics → Application Insights | `PutMetricData` → `TrackMetric` / custom metrics |
| EventBridge → Event Grid | `PutEvents` → publish events to topic |
| Step Functions → Durable Functions | State machine JSON → orchestrator function code |

### Step 4: Configuration Migration

Load **config-transformation** skill:
- Replace AWS region references with Azure region/location
- Replace ARNs with Azure Resource IDs
- Replace AWS service endpoints with Azure endpoints
- Update connection strings for Azure services
- Externalize sensitive configuration to Azure Key Vault
- Update environment variables (`AWS_REGION` → `AZURE_REGION`, etc.)

### Step 5: Authentication Migration
- Replace IAM role-based auth with Azure Managed Identity
- Replace Cognito with Entra ID (if applicable)
- Replace STS `AssumeRole` with Entra ID app-to-app authentication
- Update middleware/interceptors for Azure auth patterns
- Migrate OAuth2/OIDC provider references from Cognito to Entra ID

### Step 6: Build and Validate
- Build the application after each major migration step
- Use `get_errors` to detect issues
- Run existing tests to verify no regressions
- Create new tests for Azure service integrations (load **migration-unit-testing** skill)
- Validate all business logic mappings are preserved

## Media and Asset Preservation

Track and copy all media assets:
- Images, CSS, JavaScript, fonts
- User uploads and documents
- Email templates, report templates
- Localization/resource files

Update `reports/Business-Logic-Mapping.md` with asset migration status.

## General Rules

- Always read 2000 lines of code at a time to ensure you have enough context
- Before editing, always read the relevant file contents
- Make small, testable, incremental changes
- If a patch is not applied correctly, reapply it
- Build the application as you migrate, fix errors as you go
- Create a '[App-Name-Azure]' folder for the migrated project
- Document all changes in the Business-Logic-Mapping report
- Suggest `/AWS2Azure-phase3-generateinfra` as the next step
- Update `reports/Report-Status.md` at the end

