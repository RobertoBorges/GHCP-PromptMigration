---
name: aws-service-mapping
description: Decision matrix for choosing the right Azure service based on specific AWS usage patterns. Each mapping includes selection criteria, trade-offs, and migration complexity — NOT a simple lookup table. Covers compute (EC2/ECS/Fargate/EKS/Lambda/Beanstalk), storage (S3/EFS/EBS/FSx), databases (RDS/Aurora/DynamoDB/Redshift), messaging (SQS/SNS/EventBridge/Kinesis), containers, and data services. Use during Phase 1 planning.
---

# AWS → Azure Service Mapping Decision Matrix

> **Purpose**: Help migration teams choose the right Azure service based on their specific AWS usage patterns.
> This is a **decision matrix**, not a simple lookup table — each mapping includes selection criteria, trade-offs, and migration complexity.

---

## How to Use This Matrix

1. **Identify** the AWS services in your application (Phase 1 Assessment)
2. **Match** each service to the Azure equivalents below
3. **Evaluate** the "When to Choose" criteria against your workload requirements
4. **Document** your decisions using the [service mapping template](templates/service-mapping-template.md)
5. **Note** the migration complexity to plan timelines accurately

### Migration Complexity Legend

| Rating | Meaning | Typical Effort |
|--------|---------|----------------|
| 🟢 Low | Near drop-in replacement, SDK swap | Days |
| 🟡 Medium | API differences, moderate code changes | 1–2 weeks |
| 🟠 High | Significant redesign or feature gaps | 2–6 weeks |
| 🔴 Very High | Architectural rethink, no direct equivalent | 6+ weeks |

---

## 1. Compute

### EC2 → Azure Virtual Machines / Azure VM Scale Sets

| Aspect | Details |
|--------|---------|
| **AWS Service** | EC2 (Elastic Compute Cloud) |
| **Azure Equivalent(s)** | **Azure Virtual Machines**, **Azure VM Scale Sets (VMSS)** |
| **Migration Complexity** | 🟢 Low |

| Azure Option | When to Choose |
|--------------|----------------|
| Azure Virtual Machines | Single-instance or small-count workloads; lift-and-shift VMs; need for specific OS images or custom configurations |
| Azure VM Scale Sets | Auto-scaling groups of identical VMs; stateless web/API tiers; high-availability deployments behind a load balancer |

**Feature Gaps & Limitations**:
- EC2 Spot Instances → Azure Spot VMs (similar but eviction policies differ)
- EC2 Placement Groups → Azure Proximity Placement Groups (similar functionality)
- EC2 instance store → Azure temporary disk (not all VM sizes include one)
- AMI → Azure Managed Images or Azure Compute Gallery (different sharing model)
- EC2 Instance Connect → Azure Bastion or SSH via public IP

**Key Considerations**:
- VM size families don't map 1:1; use [Azure VM selector](https://azure.microsoft.com/en-us/pricing/vm-selector/) to find equivalents
- Reserved Instances and Savings Plans exist on both platforms but terms differ
- User Data scripts → Azure Custom Script Extension or cloud-init
- If migrating from EC2 to PaaS, consider App Service or Container Apps instead

---

### Lambda → Azure Functions / Azure Container Apps

| Aspect | Details |
|--------|---------|
| **AWS Service** | Lambda |
| **Azure Equivalent(s)** | **Azure Functions**, **Azure Container Apps (serverless)** |
| **Migration Complexity** | 🟡 Medium |

| Azure Option | When to Choose |
|--------------|----------------|
| Azure Functions (Consumption) | Event-driven, short-lived functions; pay-per-execution; sub-15-min runtime; tight integration with Azure services via bindings |
| Azure Functions (Flex Consumption) | Need always-ready instances, VNet integration, or larger instance sizes with consumption pricing |
| Azure Functions (Dedicated/Premium) | Need VNet integration, longer timeouts, predictable performance; pre-warmed instances to avoid cold starts |
| Azure Container Apps (serverless) | Container-based functions; need custom runtimes; long-running jobs; scale-to-zero with container flexibility |

**Feature Gaps & Limitations**:
- Lambda Layers → Azure Functions don't have an equivalent; use shared libraries or container deployment
- Lambda@Edge → Azure Functions with Front Door or CDN rules (less tightly integrated)
- Lambda SnapStart (Java) → Azure Functions Premium pre-warmed instances (different mechanism)
- Lambda Provisioned Concurrency → Azure Functions Premium always-ready instances
- Lambda Extensions → No direct equivalent; use Application Insights or sidecar patterns
- Max execution time: Lambda 15 min vs Azure Functions Consumption 10 min (Premium unlimited)

**Key Considerations**:
- Azure Functions bindings reduce boilerplate for queue, blob, and event triggers
- Lambda runtime model (handler function) maps well to Azure Functions trigger model
- Environment variable patterns are similar; both support secrets references
- If using Lambda with API Gateway, consider Azure Functions HTTP trigger or Azure API Management

---

### Elastic Beanstalk → Azure App Service

| Aspect | Details |
|--------|---------|
| **AWS Service** | Elastic Beanstalk |
| **Azure Equivalent(s)** | **Azure App Service** |
| **Migration Complexity** | 🟢 Low |

| Azure Option | When to Choose |
|--------------|----------------|
| Azure App Service | Web apps, REST APIs; managed platform with built-in CI/CD, SSL, custom domains, auto-scaling; supports .NET, Java, Node.js, Python, PHP |

**Feature Gaps & Limitations**:
- Beanstalk Worker Environments → App Service WebJobs or Azure Functions
- Beanstalk `.ebextensions` → App Service app settings, ARM/Bicep templates, or startup scripts
- Beanstalk managed platform updates → App Service automatic OS patching
- Multi-container Docker on Beanstalk → App Service supports single container or use Container Apps

**Key Considerations**:
- App Service deployment slots provide blue/green deployment similar to Beanstalk environment swaps
- App Service Plan pricing tiers map roughly to Beanstalk instance types
- Both support health checks, logging, and monitoring out of the box

---

### ECS / Fargate → Azure Container Apps / Azure Container Instances

| Aspect | Details |
|--------|---------|
| **AWS Service** | ECS (Elastic Container Service), Fargate |
| **Azure Equivalent(s)** | **Azure Container Apps**, **Azure Container Instances (ACI)** |
| **Migration Complexity** | 🟡 Medium |

| Azure Option | When to Choose |
|--------------|----------------|
| Azure Container Apps | Microservices, event-driven apps; built-in Dapr support; scale-to-zero; ingress routing; revision management; replaces most ECS/Fargate use cases |
| Azure Container Instances | Simple single-container or sidecar workloads; batch jobs; burst compute; no orchestration needed; quick container runs |

**Feature Gaps & Limitations**:
- ECS Service Discovery → Container Apps built-in service discovery or Dapr
- ECS Task Definitions → Container Apps container specs (different schema)
- Fargate Spot → Container Apps consumption plan (automatic spot-like pricing)
- ECS Exec → Container Apps console (preview); ACI exec
- ECS capacity providers → Container Apps workload profiles

**Key Considerations**:
- ECS task definitions need conversion to Container Apps YAML manifests
- Container Apps is the recommended target for most ECS/Fargate workloads
- ACI is better for simple, short-lived containers or sidecar scenarios
- If using ECS with heavy ALB integration, Container Apps built-in ingress replaces this

---

### EKS → Azure Kubernetes Service (AKS)

| Aspect | Details |
|--------|---------|
| **AWS Service** | EKS (Elastic Kubernetes Service) |
| **Azure Equivalent(s)** | **Azure Kubernetes Service (AKS)** |
| **Migration Complexity** | 🟡 Medium |

| Azure Option | When to Choose |
|--------------|----------------|
| AKS | Complex multi-container orchestration; need full Kubernetes API; existing Helm charts and operators; multi-team workloads with namespace isolation |

**Feature Gaps & Limitations**:
- EKS Fargate profiles → AKS virtual nodes (Azure Container Instances backed)
- EKS managed node groups → AKS node pools (similar)
- EKS add-ons → AKS extensions and add-ons (different marketplace)
- AWS Load Balancer Controller → Azure application routing add-on or NGINX ingress
- EKS Pod Identity → AKS Workload Identity (Microsoft Entra ID based)
- AWS VPC CNI → Azure CNI or Azure CNI Overlay

**Key Considerations**:
- Kubernetes manifests are mostly portable; main changes are cloud-specific annotations and storage classes
- AKS control plane is free; EKS charges for control plane
- AKS integrates natively with Entra ID for RBAC; EKS uses IAM
- Consider Container Apps if you don't need full Kubernetes complexity

---

### AWS Batch → Azure Batch

| Aspect | Details |
|--------|---------|
| **AWS Service** | AWS Batch |
| **Azure Equivalent(s)** | **Azure Batch**, **Azure Container Apps Jobs** |
| **Migration Complexity** | 🟡 Medium |

| Azure Option | When to Choose |
|--------------|----------------|
| Azure Batch | Large-scale HPC, rendering, or parallel compute workloads; need fine-grained pool and node management; tight integration with low-priority VMs |
| Container Apps Jobs | Simpler batch/cron workloads; event-driven jobs; container-based processing without infrastructure management |

**Feature Gaps & Limitations**:
- AWS Batch compute environments → Azure Batch pools (different configuration model)
- AWS Batch job queues → Azure Batch job scheduling (similar concept, different API)
- AWS Batch array jobs → Azure Batch task collections

**Key Considerations**:
- Azure Batch supports Docker containers, similar to AWS Batch
- For simpler scheduled jobs, Container Apps Jobs or Azure Functions timer triggers may suffice
- Azure Batch Shipyard provides Docker-native batch processing

---

## 2. Storage

### S3 → Azure Blob Storage

| Aspect | Details |
|--------|---------|
| **AWS Service** | S3 (Simple Storage Service) |
| **Azure Equivalent(s)** | **Azure Blob Storage** |
| **Migration Complexity** | 🟢 Low |

| Azure Option | When to Choose |
|--------------|----------------|
| Azure Blob Storage (Hot) | Frequently accessed data; equivalent to S3 Standard |
| Azure Blob Storage (Cool) | Infrequently accessed data (30+ day retention); equivalent to S3 Standard-IA |
| Azure Blob Storage (Cold) | Rarely accessed data (90+ day retention); lower cost than Cool |
| Azure Blob Storage (Archive) | Long-term archival; equivalent to S3 Glacier (see Glacier section below) |
| Azure Data Lake Storage Gen2 | Analytics workloads; hierarchical namespace; equivalent to S3 + S3 Select for data lake patterns |

**Feature Gaps & Limitations**:
- S3 Object Lock → Azure Blob immutable storage (WORM policies)
- S3 Select → Azure Blob query (limited SQL subset)
- S3 Transfer Acceleration → Azure CDN or Front Door (different approach)
- S3 event notifications → Azure Event Grid blob events
- S3 bucket policies → Azure RBAC + Storage access policies
- S3 Requester Pays → Not available in Azure Blob Storage
- S3 multi-part upload → Azure Block Blob staged upload (similar concept, different API)

**Key Considerations**:
- Storage account naming is global and has different constraints than S3 bucket naming
- Azure uses storage accounts as a container for blobs; S3 uses flat bucket namespace
- Use AzCopy or Azure Data Box for bulk data migration
- SDK migration: `aws-sdk S3Client` → `@azure/storage-blob` or `Azure.Storage.Blobs`
- S3 versioning → Azure Blob versioning (similar but lifecycle rules differ)

---

### EBS → Azure Managed Disks

| Aspect | Details |
|--------|---------|
| **AWS Service** | EBS (Elastic Block Store) |
| **Azure Equivalent(s)** | **Azure Managed Disks** |
| **Migration Complexity** | 🟢 Low |

| Azure Option | When to Choose |
|--------------|----------------|
| Standard HDD | Dev/test, backups, infrequent access; maps to EBS `sc1`/`st1` |
| Standard SSD | Light production workloads; maps to EBS `gp2` baseline |
| Premium SSD v2 | Production workloads needing tunable IOPS/throughput; maps to EBS `io2` |
| Ultra Disk | Extreme IOPS/low latency (databases, SAP); maps to EBS `io2 Block Express` |

**Feature Gaps & Limitations**:
- EBS snapshots → Azure Disk snapshots (similar)
- EBS multi-attach → Azure Shared Disks (limited VM count)
- EBS encryption → Azure Disk encryption (ADE) or server-side encryption with platform or customer-managed keys

**Key Considerations**:
- Disk performance tiers don't map 1:1; benchmark before migration
- Azure Managed Disks include built-in redundancy (LRS/ZRS)

---

### EFS → Azure Files / Azure NetApp Files

| Aspect | Details |
|--------|---------|
| **AWS Service** | EFS (Elastic File System) |
| **Azure Equivalent(s)** | **Azure Files**, **Azure NetApp Files** |
| **Migration Complexity** | 🟢 Low |

| Azure Option | When to Choose |
|--------------|----------------|
| Azure Files (SMB/NFS) | Shared file storage for cloud or hybrid; lift-and-shift NFS/SMB workloads; Azure File Sync for hybrid scenarios |
| Azure NetApp Files | High-performance NFS; enterprise workloads (SAP, HPC, databases); sub-millisecond latency |

**Feature Gaps & Limitations**:
- EFS lifecycle management → Azure Files access tier management (hot/cool)
- EFS throughput modes (bursting/provisioned) → Azure Files performance tiers or NetApp service levels
- EFS Access Points → Azure Files share-level permissions

**Key Considerations**:
- Azure Files supports both SMB and NFS protocols; EFS is NFS only
- For Linux NFS workloads, use Azure Files NFS or NetApp Files
- Azure File Sync enables caching on Windows servers

---

### FSx → Azure NetApp Files / Azure Files / Azure Managed Lustre

| Aspect | Details |
|--------|---------|
| **AWS Service** | FSx (for Lustre, Windows File Server, NetApp ONTAP, OpenZFS) |
| **Azure Equivalent(s)** | **Azure NetApp Files**, **Azure Files**, **Azure Managed Lustre** |
| **Migration Complexity** | 🟡 Medium |

| Azure Option | When to Choose |
|--------------|----------------|
| Azure NetApp Files | Replaces FSx for NetApp ONTAP; enterprise NAS; high-performance NFS/SMB |
| Azure Files | Replaces FSx for Windows File Server; SMB shares; Active Directory integration |
| Azure Managed Lustre | Replaces FSx for Lustre; HPC parallel file system workloads |

**Feature Gaps & Limitations**:
- FSx for OpenZFS → No direct Azure equivalent; use Azure NetApp Files or Azure Managed Disks with ZFS on Linux
- FSx Data Repository Associations (S3 integration) → Azure Managed Lustre with Blob integration

---

### S3 Glacier → Azure Blob Archive / Azure Blob Cold

| Aspect | Details |
|--------|---------|
| **AWS Service** | S3 Glacier, S3 Glacier Deep Archive |
| **Azure Equivalent(s)** | **Azure Blob Storage (Archive tier)**, **Azure Blob Storage (Cold tier)** |
| **Migration Complexity** | 🟢 Low |

| Azure Option | When to Choose |
|--------------|----------------|
| Azure Blob Archive | Long-term retention, compliance archival; maps to Glacier/Deep Archive; lowest cost; hours to rehydrate |
| Azure Blob Cold | Data accessed rarely but needs faster retrieval than Archive; 90-day minimum retention |

**Feature Gaps & Limitations**:
- Glacier Vault Lock → Azure Blob immutable storage policies
- Glacier retrieval tiers (Expedited/Standard/Bulk) → Azure rehydration priority (Standard/High)
- Glacier Instant Retrieval → Azure Cool tier (millisecond access)

**Key Considerations**:
- Archive tier rehydration can take up to 15 hours; plan for retrieval latency
- Use lifecycle management policies to automate tier transitions

---

## 3. Database

### DynamoDB → Azure Cosmos DB

| Aspect | Details |
|--------|---------|
| **AWS Service** | DynamoDB |
| **Azure Equivalent(s)** | **Azure Cosmos DB** (Table API or NoSQL API) |
| **Migration Complexity** | 🟡 Medium |

| Azure Option | When to Choose |
|--------------|----------------|
| Cosmos DB for NoSQL | Rich query support; JSON documents; most flexibility; recommended for new designs |
| Cosmos DB for Table | Closest API compatibility with DynamoDB; key-value patterns; easier migration of simple table workloads |

**Feature Gaps & Limitations**:
- DynamoDB Streams → Cosmos DB Change Feed (similar but different API)
- DynamoDB DAX (caching) → Cosmos DB integrated cache or dedicated caching tier
- DynamoDB Global Tables → Cosmos DB multi-region writes (more flexible)
- DynamoDB TTL → Cosmos DB TTL (similar)
- DynamoDB PartiQL → Cosmos DB SQL-like query language (for NoSQL API)
- DynamoDB On-Demand capacity → Cosmos DB serverless or autoscale throughput
- DynamoDB single-digit-ms reads → Cosmos DB guarantees <10ms reads (SLA-backed)

**Key Considerations**:
- Partition key design is critical in both; review key strategy during migration
- Cosmos DB pricing model (RU/s) differs significantly from DynamoDB (RCU/WCU)
- Cosmos DB offers five consistency levels vs DynamoDB's eventual/strong
- Use Azure Cosmos DB Data Migration Tool or Azure Data Factory for migration

---

### RDS → Azure SQL Database / Azure Database for PostgreSQL/MySQL

| Aspect | Details |
|--------|---------|
| **AWS Service** | RDS (PostgreSQL, MySQL, SQL Server, MariaDB, Oracle) |
| **Azure Equivalent(s)** | **Azure SQL Database**, **Azure Database for PostgreSQL**, **Azure Database for MySQL** |
| **Migration Complexity** | 🟢 Low – 🟡 Medium (depends on engine) |

| Azure Option | When to Choose |
|--------------|----------------|
| Azure SQL Database | RDS for SQL Server; fully managed; intelligent performance; built-in AI features |
| Azure SQL Managed Instance | Need near-100% SQL Server compatibility; cross-database queries; SQL Agent; CLR |
| Azure Database for PostgreSQL Flexible Server | RDS for PostgreSQL; extensions support; high availability; intelligent tuning |
| Azure Database for MySQL Flexible Server | RDS for MySQL or MariaDB; managed MySQL with flexible compute |

**Feature Gaps & Limitations**:
- RDS Multi-AZ → Azure zone-redundant HA (similar)
- RDS Read Replicas → Azure read replicas (similar)
- RDS Proxy → Azure SQL connection pooling or PgBouncer for PostgreSQL
- RDS Performance Insights → Azure SQL Intelligent Insights or Query Performance Insight
- RDS for Oracle → No Azure-managed Oracle; use Oracle on Azure VMs or Oracle Database@Azure
- RDS for MariaDB → Azure Database for MySQL (MariaDB compatible) or MariaDB on VMs

**Key Considerations**:
- Use Azure Database Migration Service (DMS) for online migration with minimal downtime
- Connection string changes required; update application configuration
- SSL/TLS enforcement is default on Azure managed databases
- Consider managed identity for passwordless authentication

---

### Aurora → Azure SQL Database / Azure Cosmos DB for PostgreSQL

| Aspect | Details |
|--------|---------|
| **AWS Service** | Aurora (MySQL-compatible, PostgreSQL-compatible) |
| **Azure Equivalent(s)** | **Azure SQL Database Hyperscale**, **Azure Database for PostgreSQL**, **Azure Cosmos DB for PostgreSQL** |
| **Migration Complexity** | 🟡 Medium |

| Azure Option | When to Choose |
|--------------|----------------|
| Azure Database for PostgreSQL Flexible Server | Aurora PostgreSQL; standard relational workloads; most direct migration path |
| Azure SQL Database Hyperscale | Aurora MySQL; need rapid scale-out; large databases (up to 100 TB); fast backups |
| Azure Cosmos DB for PostgreSQL | Distributed PostgreSQL (Citus-based); need horizontal sharding; multi-node scale-out |

**Feature Gaps & Limitations**:
- Aurora Serverless v2 → Azure SQL Serverless or PostgreSQL Flexible Server burstable tier
- Aurora Global Database → Azure SQL geo-replication or PostgreSQL read replicas
- Aurora Parallel Query → No direct equivalent; use Hyperscale or Cosmos DB for PostgreSQL
- Aurora zero-ETL to Redshift → Azure Synapse Link (different integration model)

**Key Considerations**:
- Aurora custom endpoints → Use Azure private endpoints and connection routing
- Aurora storage auto-scaling is similar to Hyperscale auto-grow
- Test performance characteristics as storage engines differ

---

### ElastiCache → Azure Cache for Redis / Azure Managed Redis

| Aspect | Details |
|--------|---------|
| **AWS Service** | ElastiCache (Redis, Memcached) |
| **Azure Equivalent(s)** | **Azure Cache for Redis**, **Azure Managed Redis** |
| **Migration Complexity** | 🟢 Low |

| Azure Option | When to Choose |
|--------------|----------------|
| Azure Cache for Redis | Standard caching, session store, pub/sub; maps directly to ElastiCache for Redis |
| Azure Managed Redis (Redis Enterprise) | Need Redis modules (RediSearch, RedisJSON, RedisTimeSeries); active-active geo-replication; flash storage tier |

**Feature Gaps & Limitations**:
- ElastiCache Memcached → No managed Memcached on Azure; use Azure Cache for Redis or self-host
- ElastiCache Global Datastore → Azure Managed Redis active geo-replication
- ElastiCache reserved nodes → Azure Cache for Redis reserved capacity

**Key Considerations**:
- Redis protocol compatibility means minimal code changes (connection string update)
- Azure Cache for Redis supports clustering similar to ElastiCache
- For Memcached workloads, Azure Cache for Redis can serve as a replacement with minor code changes

---

### Redshift → Azure Synapse Analytics

| Aspect | Details |
|--------|---------|
| **AWS Service** | Redshift |
| **Azure Equivalent(s)** | **Azure Synapse Analytics**, **Microsoft Fabric** |
| **Migration Complexity** | 🟠 High |

| Azure Option | When to Choose |
|--------------|----------------|
| Azure Synapse Analytics (Dedicated SQL Pool) | Direct Redshift replacement; MPP data warehouse; complex SQL analytics |
| Azure Synapse Analytics (Serverless SQL Pool) | Ad-hoc queries over data lake; pay-per-query; no infrastructure management |
| Microsoft Fabric | Unified analytics platform; combines data warehouse, lake, and BI; newer strategic direction |

**Feature Gaps & Limitations**:
- Redshift Spectrum → Synapse serverless SQL over data lake
- Redshift ML → Synapse ML integration or Azure Machine Learning
- Redshift AQUA → Synapse result set caching and materialized views
- Redshift Streaming Ingestion → Synapse Data Explorer or Event Hubs integration
- Redshift data sharing → Synapse workspace data sharing (different model)

**Key Considerations**:
- SQL dialect differences require query rewriting (Redshift SQL → T-SQL)
- Use Azure Synapse Pathway for automated SQL translation
- Data distribution strategies differ; review distribution keys
- Microsoft Fabric is the strategic long-term direction; evaluate for new projects

---

### DocumentDB → Azure Cosmos DB

| Aspect | Details |
|--------|---------|
| **AWS Service** | Amazon DocumentDB (MongoDB-compatible) |
| **Azure Equivalent(s)** | **Azure Cosmos DB for MongoDB** |
| **Migration Complexity** | 🟢 Low |

| Azure Option | When to Choose |
|--------------|----------------|
| Azure Cosmos DB for MongoDB (RU-based) | MongoDB workloads; provisioned or autoscale throughput; global distribution |
| Azure Cosmos DB for MongoDB (vCore-based) | Familiar MongoDB experience; vCPU-based pricing; lift-and-shift; high compatibility |

**Feature Gaps & Limitations**:
- DocumentDB supports MongoDB 4.0/5.0 compatibility; Cosmos DB vCore supports up to 7.0
- DocumentDB elastic clusters → Cosmos DB vCore cluster tier
- Some MongoDB aggregation operators may differ in support level

**Key Considerations**:
- Cosmos DB for MongoDB vCore is the easiest migration path for DocumentDB
- Connection string change is often the primary code modification
- Use Azure Database Migration Service or native `mongodump`/`mongorestore`

---

### Neptune → Azure Cosmos DB for Gremlin / Azure Cosmos DB for Apache Gremlin

| Aspect | Details |
|--------|---------|
| **AWS Service** | Neptune (Graph Database) |
| **Azure Equivalent(s)** | **Azure Cosmos DB for Apache Gremlin** |
| **Migration Complexity** | 🟡 Medium |

| Azure Option | When to Choose |
|--------------|----------------|
| Azure Cosmos DB for Apache Gremlin | Graph workloads using Gremlin query language; global distribution; multi-model |

**Feature Gaps & Limitations**:
- Neptune SPARQL support → No direct Cosmos DB equivalent; consider third-party solutions
- Neptune Streams → Cosmos DB Change Feed
- Neptune ML → Azure Machine Learning integration (manual setup)
- Neptune full-text search → Not available in Cosmos DB Gremlin; use Azure AI Search alongside

**Key Considerations**:
- If using SPARQL, migration is significantly more complex (🟠 High)
- Gremlin queries are largely portable between Neptune and Cosmos DB
- Cosmos DB partition key design is critical for graph workloads

---

### MemoryDB for Redis → Azure Managed Redis

| Aspect | Details |
|--------|---------|
| **AWS Service** | MemoryDB for Redis |
| **Azure Equivalent(s)** | **Azure Managed Redis (Enterprise tier)** |
| **Migration Complexity** | 🟢 Low |

| Azure Option | When to Choose |
|--------------|----------------|
| Azure Managed Redis (Enterprise, Flash tier) | Durable Redis with persistence; primary database use cases; need Redis modules |

**Feature Gaps & Limitations**:
- MemoryDB's multi-AZ transactional log → Azure Managed Redis AOF persistence + zone redundancy
- MemoryDB as primary database → Azure Managed Redis supports similar patterns with persistence enabled

**Key Considerations**:
- Both services offer Redis-compatible APIs; connection string swap for basic use
- Evaluate persistence and durability requirements carefully

---

## 4. Messaging & Eventing

### SQS → Azure Queue Storage / Azure Service Bus

| Aspect | Details |
|--------|---------|
| **AWS Service** | SQS (Simple Queue Service) |
| **Azure Equivalent(s)** | **Azure Queue Storage**, **Azure Service Bus** |
| **Migration Complexity** | 🟢 Low – 🟡 Medium |

| Azure Option | When to Choose |
|--------------|----------------|
| Azure Queue Storage | Simple message queuing; high volume; no ordering guarantees needed; cost-sensitive; maps to SQS Standard |
| Azure Service Bus Queues | Enterprise messaging; need FIFO ordering, sessions, transactions, dead-letter queues, duplicate detection; maps to SQS FIFO |

**Feature Gaps & Limitations**:
- SQS Long Polling → Service Bus long-poll receive; Queue Storage polling
- SQS Visibility Timeout → Service Bus lock duration (similar)
- SQS Dead Letter Queue → Service Bus dead-letter queue (built-in); Queue Storage poison queue (via Azure Functions)
- SQS FIFO → Service Bus sessions (message grouping with ordering)
- SQS message size 256 KB → Service Bus 256 KB (Standard) or 100 MB (Premium); Queue Storage 64 KB

**Key Considerations**:
- For simple fire-and-forget messaging, Azure Queue Storage is cheapest
- For enterprise patterns (transactions, sessions, dead-letter), use Service Bus
- SQS batch operations → Service Bus batch send/receive (similar)

---

### SNS → Azure Service Bus Topics / Azure Event Grid

| Aspect | Details |
|--------|---------|
| **AWS Service** | SNS (Simple Notification Service) |
| **Azure Equivalent(s)** | **Azure Service Bus Topics**, **Azure Event Grid**, **Azure Notification Hubs** |
| **Migration Complexity** | 🟡 Medium |

| Azure Option | When to Choose |
|--------------|----------------|
| Azure Service Bus Topics | Pub/sub messaging; need subscriptions with filters; message ordering; enterprise integration |
| Azure Event Grid | Event routing; reactive event-driven architectures; lightweight event distribution |
| Azure Notification Hubs | Push notifications to mobile devices (maps to SNS mobile push) |

**Feature Gaps & Limitations**:
- SNS message filtering → Service Bus topic subscription filters (more powerful)
- SNS fan-out to SQS → Service Bus topic to queue forwarding
- SNS SMS → Azure Communication Services SMS
- SNS email → Azure Communication Services Email or SendGrid

**Key Considerations**:
- If using SNS for pub/sub messaging between services, use Service Bus Topics
- If using SNS for event routing/notifications, use Event Grid
- If using SNS for mobile push, use Notification Hubs

---

### EventBridge → Azure Event Grid

| Aspect | Details |
|--------|---------|
| **AWS Service** | EventBridge |
| **Azure Equivalent(s)** | **Azure Event Grid** |
| **Migration Complexity** | 🟡 Medium |

| Azure Option | When to Choose |
|--------------|----------------|
| Azure Event Grid | Event routing between services; custom topics; system events from Azure resources; event filtering and fan-out |

**Feature Gaps & Limitations**:
- EventBridge Schema Registry → Event Grid schema validation (less mature)
- EventBridge Archive & Replay → Event Grid event retention (limited; use Event Hubs for replay)
- EventBridge Pipes → No direct equivalent; use Azure Functions or Logic Apps for transformation
- EventBridge Scheduler → Azure Logic Apps or Azure Functions timer triggers
- EventBridge SaaS partner events → Event Grid partner events (growing ecosystem)
- EventBridge rules (pattern matching) → Event Grid advanced filters (different syntax)

**Key Considerations**:
- Event Grid is push-based, similar to EventBridge
- For complex event replay scenarios, pair Event Grid with Event Hubs
- Event Grid custom topics map to EventBridge custom event buses

---

### Kinesis → Azure Event Hubs

| Aspect | Details |
|--------|---------|
| **AWS Service** | Kinesis Data Streams, Kinesis Data Firehose |
| **Azure Equivalent(s)** | **Azure Event Hubs**, **Azure Event Hubs Capture** |
| **Migration Complexity** | 🟡 Medium |

| Azure Option | When to Choose |
|--------------|----------------|
| Azure Event Hubs | High-throughput event streaming; real-time data ingestion; Kafka-compatible; maps to Kinesis Data Streams |
| Azure Event Hubs Capture | Auto-capture events to Blob Storage or Data Lake; maps to Kinesis Data Firehose to S3 |

**Feature Gaps & Limitations**:
- Kinesis enhanced fan-out → Event Hubs dedicated consumer groups (similar)
- Kinesis shard splitting/merging → Event Hubs auto-inflate or partition management
- Kinesis Data Firehose transformations → Event Hubs + Azure Functions or Stream Analytics
- Kinesis Data Firehose to Redshift → Event Hubs + Synapse or Data Factory pipeline
- Kinesis KCL (Kinesis Client Library) → Event Hubs SDK or Event Processor Host

**Key Considerations**:
- Event Hubs supports Apache Kafka protocol; Kafka clients can connect directly
- Kinesis shards → Event Hubs partitions (similar concept)
- Event Hubs throughput units vs Kinesis shard capacity
- For Firehose delivery-to-storage, Event Hubs Capture is simpler but less flexible

---

### Amazon MQ → Azure Service Bus / Azure Event Hubs

| Aspect | Details |
|--------|---------|
| **AWS Service** | Amazon MQ (ActiveMQ, RabbitMQ) |
| **Azure Equivalent(s)** | **Azure Service Bus**, **RabbitMQ on Azure VMs/Container Apps** |
| **Migration Complexity** | 🟡 Medium – 🟠 High |

| Azure Option | When to Choose |
|--------------|----------------|
| Azure Service Bus | Modernize to cloud-native messaging; JMS bridge available; enterprise messaging patterns |
| Self-hosted RabbitMQ | Need RabbitMQ protocol compatibility; AMQP 0.9.1; minimal application changes |

**Feature Gaps & Limitations**:
- No managed ActiveMQ or RabbitMQ PaaS on Azure
- JMS to Service Bus requires the Service Bus JMS library
- AMQP 1.0 is supported by Service Bus; AMQP 0.9.1 (RabbitMQ) is not

**Key Considerations**:
- If using JMS (Java Message Service), Service Bus has a JMS 2.0 client
- For RabbitMQ workloads, consider self-hosting on Container Apps or AKS
- If modernizing, Service Bus is the recommended cloud-native path

---

### MSK (Kafka) → Azure Event Hubs / Azure HDInsight Kafka

| Aspect | Details |
|--------|---------|
| **AWS Service** | MSK (Managed Streaming for Apache Kafka) |
| **Azure Equivalent(s)** | **Azure Event Hubs (Kafka endpoint)**, **Azure HDInsight Kafka** |
| **Migration Complexity** | 🟡 Medium |

| Azure Option | When to Choose |
|--------------|----------------|
| Azure Event Hubs (Kafka protocol) | Kafka-compatible without managing clusters; pay-per-throughput; simpler operations; existing Kafka clients connect directly |
| Azure HDInsight Kafka | Need full Apache Kafka feature set; Kafka Streams, Kafka Connect with all connectors; custom configurations |

**Feature Gaps & Limitations**:
- MSK Connect → Event Hubs doesn't support Kafka Connect natively; use Azure Data Factory or self-hosted Connect
- MSK Serverless → Event Hubs Premium (Kafka-compatible, auto-scale)
- Kafka Streams → Not supported on Event Hubs; need HDInsight or self-managed Kafka
- Kafka topic compaction → Event Hubs supports compacted topics in Premium/Dedicated

**Key Considerations**:
- Event Hubs Kafka endpoint allows Kafka clients to connect with a config change
- For Kafka Connect workflows, evaluate Azure Data Factory as an alternative
- HDInsight provides full Kafka but requires cluster management

---

## 5. Networking

### VPC → Azure Virtual Network (VNet)

| Aspect | Details |
|--------|---------|
| **AWS Service** | VPC (Virtual Private Cloud) |
| **Azure Equivalent(s)** | **Azure Virtual Network (VNet)** |
| **Migration Complexity** | 🟡 Medium |

| Azure Option | When to Choose |
|--------------|----------------|
| Azure VNet | All private networking needs; subnet segmentation; network security groups; VNet peering |

**Feature Gaps & Limitations**:
- VPC Security Groups (stateful) → Azure Network Security Groups (NSGs) — stateful, similar
- VPC NACLs (stateless) → Azure NSGs at subnet level (stateful, not stateless)
- VPC Endpoints (Gateway) → Azure Service Endpoints or Private Endpoints
- VPC Endpoints (Interface) → Azure Private Endpoints (closest match)
- VPC Flow Logs → Azure NSG Flow Logs or VNet Flow Logs

**Key Considerations**:
- Azure VNets don't have an Internet Gateway concept; public IPs attach directly to resources
- Subnet CIDR planning is critical; Azure reserves 5 IPs per subnet vs AWS reserving 5
- VNet peering is non-transitive (same as VPC peering)
- Redesign subnets and NSGs during migration; don't copy AWS topology directly

---

### Route 53 → Azure DNS / Azure Traffic Manager / Azure Front Door

| Aspect | Details |
|--------|---------|
| **AWS Service** | Route 53 |
| **Azure Equivalent(s)** | **Azure DNS**, **Azure Traffic Manager**, **Azure Front Door** |
| **Migration Complexity** | 🟢 Low |

| Azure Option | When to Choose |
|--------------|----------------|
| Azure DNS | DNS hosting; zone management; record sets; maps to Route 53 hosted zones |
| Azure Traffic Manager | DNS-based traffic routing (failover, weighted, performance, geographic); maps to Route 53 routing policies |
| Azure Front Door | Global HTTP load balancing with CDN; health probes; WAF; combines Route 53 + CloudFront functionality |

**Feature Gaps & Limitations**:
- Route 53 domain registration → Azure does not offer domain registration; use third-party registrar
- Route 53 health checks → Traffic Manager health probes or Front Door health probes
- Route 53 DNSSEC → Azure DNS supports DNSSEC for public zones
- Route 53 Resolver → Azure DNS Private Resolver

---

### CloudFront → Azure Front Door / Azure CDN

| Aspect | Details |
|--------|---------|
| **AWS Service** | CloudFront |
| **Azure Equivalent(s)** | **Azure Front Door**, **Azure CDN** |
| **Migration Complexity** | 🟢 Low |

| Azure Option | When to Choose |
|--------------|----------------|
| Azure Front Door | Global load balancing + CDN + WAF; dynamic content acceleration; SSL offloading; recommended for most use cases |
| Azure CDN | Simple static content delivery; lower cost; multiple provider options (Microsoft, Akamai, Verizon) |

**Feature Gaps & Limitations**:
- CloudFront Functions → Azure Front Door Rules Engine (different model)
- Lambda@Edge → Azure Functions with Front Door (less tightly integrated)
- CloudFront signed URLs → Azure Front Door/CDN token authentication or SAS tokens
- CloudFront Origin Shield → Azure Front Door caching (built-in)

---

### API Gateway → Azure API Management

| Aspect | Details |
|--------|---------|
| **AWS Service** | API Gateway (REST, HTTP, WebSocket) |
| **Azure Equivalent(s)** | **Azure API Management (APIM)** |
| **Migration Complexity** | 🟡 Medium |

| Azure Option | When to Choose |
|--------------|----------------|
| Azure API Management (Consumption) | Serverless API management; pay-per-call; maps to API Gateway REST/HTTP APIs |
| Azure API Management (Standard v2/Premium v2) | Full-featured API gateway; developer portal; policy engine; caching; VNet integration |

**Feature Gaps & Limitations**:
- API Gateway Lambda integration → APIM + Azure Functions (similar via backend policies)
- API Gateway usage plans / API keys → APIM subscriptions and products
- API Gateway authorizers → APIM policies (JWT validation, OAuth2)
- API Gateway WebSocket → APIM WebSocket support (available in v2 tiers)
- API Gateway stage variables → APIM named values and backends

**Key Considerations**:
- APIM is more feature-rich but also more complex than API Gateway
- OpenAPI/Swagger import works on both platforms
- For simple HTTP proxying, Azure Functions HTTP trigger may suffice without APIM

---

### ALB / NLB → Azure Application Gateway / Azure Load Balancer

| Aspect | Details |
|--------|---------|
| **AWS Service** | ALB (Application Load Balancer), NLB (Network Load Balancer) |
| **Azure Equivalent(s)** | **Azure Application Gateway**, **Azure Load Balancer** |
| **Migration Complexity** | 🟢 Low |

| Azure Option | When to Choose |
|--------------|----------------|
| Azure Application Gateway (v2) | Layer 7 (HTTP/HTTPS) load balancing; path-based routing; SSL termination; WAF; maps to ALB |
| Azure Load Balancer | Layer 4 (TCP/UDP) load balancing; ultra-low latency; high throughput; maps to NLB |
| Azure Front Door | Global Layer 7 load balancing across regions; maps to ALB + Global Accelerator |

**Feature Gaps & Limitations**:
- ALB target groups → Application Gateway backend pools
- ALB listener rules → Application Gateway routing rules
- NLB cross-zone load balancing → Azure Load Balancer cross-zone (default)
- ALB authentication (Cognito/OIDC) → Application Gateway with Entra ID (via rewrite rules or APIM)

---

### Direct Connect → Azure ExpressRoute

| Aspect | Details |
|--------|---------|
| **AWS Service** | Direct Connect |
| **Azure Equivalent(s)** | **Azure ExpressRoute** |
| **Migration Complexity** | 🟠 High |

| Azure Option | When to Choose |
|--------------|----------------|
| Azure ExpressRoute | Private dedicated connectivity to Azure; hybrid cloud; consistent low latency; regulatory requirements |
| Azure VPN Gateway | Lower-cost alternative; encrypted over internet; S2S or P2S VPN |

**Feature Gaps & Limitations**:
- Direct Connect Gateway → ExpressRoute Gateway (similar)
- Direct Connect LAGs → ExpressRoute circuits (different aggregation model)
- Direct Connect hosted/dedicated → ExpressRoute partner/direct connections

**Key Considerations**:
- ExpressRoute circuit provisioning takes days to weeks
- ExpressRoute supports Microsoft Peering (for Microsoft 365) and Private Peering
- Plan connectivity migration carefully; may need parallel connectivity during transition

---

### Transit Gateway → Azure Virtual WAN / VNet Peering

| Aspect | Details |
|--------|---------|
| **AWS Service** | Transit Gateway |
| **Azure Equivalent(s)** | **Azure Virtual WAN**, **Azure VNet Peering (hub-spoke)** |
| **Migration Complexity** | 🟠 High |

| Azure Option | When to Choose |
|--------------|----------------|
| Azure Virtual WAN | Large-scale hub-and-spoke; branch connectivity; integrated VPN and ExpressRoute; managed routing |
| Hub-spoke VNet peering | Simpler topologies; manual routing control; cost-effective for smaller deployments |

**Feature Gaps & Limitations**:
- Transit Gateway route tables → Virtual WAN routing intent or UDRs
- Transit Gateway Connect → Virtual WAN NVA integration
- Transit Gateway peering → Virtual WAN inter-hub (global transit)

---

### PrivateLink → Azure Private Link

| Aspect | Details |
|--------|---------|
| **AWS Service** | PrivateLink |
| **Azure Equivalent(s)** | **Azure Private Link / Private Endpoints** |
| **Migration Complexity** | 🟢 Low |

| Azure Option | When to Choose |
|--------------|----------------|
| Azure Private Endpoint | Access Azure PaaS services privately over VNet; maps directly to AWS PrivateLink endpoints |
| Azure Private Link Service | Expose your own services privately to consumers; maps to PrivateLink service provider model |

**Feature Gaps & Limitations**:
- Conceptually very similar; both create private IP endpoints for services
- Azure Private DNS zones integrate with Private Endpoints for name resolution

---

## 6. Identity & Security

### IAM → Microsoft Entra ID / Azure RBAC

| Aspect | Details |
|--------|---------|
| **AWS Service** | IAM (Identity and Access Management) |
| **Azure Equivalent(s)** | **Microsoft Entra ID (Azure AD)**, **Azure RBAC**, **Managed Identities** |
| **Migration Complexity** | 🟠 High |

| Azure Option | When to Choose |
|--------------|----------------|
| Microsoft Entra ID | User and group identity management; SSO; MFA; conditional access policies |
| Azure RBAC | Role-based access control for Azure resources; maps to IAM policies and roles |
| Managed Identities | Service-to-service authentication without credentials; maps to IAM roles for EC2/Lambda |

**Feature Gaps & Limitations**:
- IAM policies (JSON) → Azure RBAC role assignments (different model; no inline policies)
- IAM roles for services → Azure Managed Identities (system-assigned or user-assigned)
- IAM permission boundaries → Azure Entra ID administrative units or custom roles with limited scope
- IAM Identity Center (SSO) → Microsoft Entra ID (more comprehensive)
- Cross-account IAM roles → Azure Lighthouse or cross-tenant Entra ID federation

**Key Considerations**:
- Azure's identity model is fundamentally different: Entra ID is the identity provider, RBAC controls resource access
- Prefer managed identities over service principals with secrets
- Azure Policy provides governance (like AWS SCPs)
- IAM policy migration requires complete redesign; no automated translation tool

---

### Cognito → Microsoft Entra External ID / Azure AD B2C

| Aspect | Details |
|--------|---------|
| **AWS Service** | Cognito (User Pools, Identity Pools) |
| **Azure Equivalent(s)** | **Microsoft Entra External ID**, **Azure AD B2C** |
| **Migration Complexity** | 🟠 High |

| Azure Option | When to Choose |
|--------------|----------------|
| Microsoft Entra External ID | Customer-facing identity; new strategic direction; supports OIDC, SAML, social logins; CIAM (replaces Azure AD B2C for new projects) |
| Azure AD B2C | Existing B2C implementations; custom policies; established but strategic direction is Entra External ID |

**Feature Gaps & Limitations**:
- Cognito User Pools → Entra External ID user flows
- Cognito Identity Pools (federated identities) → Entra ID federated credentials
- Cognito hosted UI → Entra External ID customizable sign-in experience
- Cognito Lambda triggers → Entra External ID authentication extensions
- Cognito User Migration trigger → Entra External ID supports just-in-time migration

**Key Considerations**:
- User migration requires careful planning; passwords cannot be exported from Cognito
- JWT token claims will differ; update application token validation
- Social identity provider configuration needs reconfiguration

---

### Secrets Manager → Azure Key Vault

| Aspect | Details |
|--------|---------|
| **AWS Service** | Secrets Manager |
| **Azure Equivalent(s)** | **Azure Key Vault** |
| **Migration Complexity** | 🟢 Low |

| Azure Option | When to Choose |
|--------------|----------------|
| Azure Key Vault | Secrets, keys, and certificates management; RBAC access control; HSM-backed options |

**Feature Gaps & Limitations**:
- Secrets Manager automatic rotation → Key Vault rotation (via Azure Functions or built-in for some types)
- Secrets Manager cross-account sharing → Key Vault access across tenants (Entra ID federation)
- Secrets Manager resource policies → Key Vault RBAC (recommended) or access policies

**Key Considerations**:
- Use Key Vault RBAC (not access policies) for new deployments
- Azure App Configuration can complement Key Vault for non-secret configuration
- Managed identity access to Key Vault eliminates credential management

---

### Parameter Store → Azure App Configuration

| Aspect | Details |
|--------|---------|
| **AWS Service** | Systems Manager Parameter Store |
| **Azure Equivalent(s)** | **Azure App Configuration**, **Azure Key Vault** |
| **Migration Complexity** | 🟢 Low |

| Azure Option | When to Choose |
|--------------|----------------|
| Azure App Configuration | Application settings and feature flags; key-value store; references to Key Vault secrets; dynamic configuration |
| Azure Key Vault | Sensitive parameters (passwords, keys); maps to Parameter Store SecureString type |

**Feature Gaps & Limitations**:
- Parameter Store hierarchy (`/app/prod/db-host`) → App Configuration labels and key prefixes
- Parameter Store policies (expiration, notification) → App Configuration events (via Event Grid)

---

### KMS → Azure Key Vault (Keys) / Azure Key Vault Managed HSM

| Aspect | Details |
|--------|---------|
| **AWS Service** | KMS (Key Management Service) |
| **Azure Equivalent(s)** | **Azure Key Vault**, **Azure Key Vault Managed HSM** |
| **Migration Complexity** | 🟡 Medium |

| Azure Option | When to Choose |
|--------------|----------------|
| Azure Key Vault (Keys) | Software-protected or HSM-backed encryption keys; CMK for Azure services |
| Azure Key Vault Managed HSM | FIPS 140-2 Level 3 validated HSM; single-tenant; full HSM control; maps to KMS custom key stores |

**Feature Gaps & Limitations**:
- KMS multi-region keys → Key Vault doesn't support key replication; use separate keys per region
- KMS key policies → Key Vault RBAC or access policies
- KMS grants → No direct equivalent; use RBAC assignments

---

### WAF → Azure WAF (with Front Door / Application Gateway)

| Aspect | Details |
|--------|---------|
| **AWS Service** | AWS WAF |
| **Azure Equivalent(s)** | **Azure WAF** |
| **Migration Complexity** | 🟡 Medium |

| Azure Option | When to Choose |
|--------------|----------------|
| Azure WAF on Front Door | Global WAF protection; DDoS + WAF combined; maps to WAF with CloudFront |
| Azure WAF on Application Gateway | Regional WAF; maps to WAF with ALB |

**Feature Gaps & Limitations**:
- WAF rules/rule groups → Azure WAF managed rule sets and custom rules
- WAF Bot Control → Azure WAF bot protection (managed rule set)
- WAF Firewall Manager → Azure Firewall Manager for centralized policy

---

### GuardDuty → Microsoft Defender for Cloud

| Aspect | Details |
|--------|---------|
| **AWS Service** | GuardDuty |
| **Azure Equivalent(s)** | **Microsoft Defender for Cloud** |
| **Migration Complexity** | 🟡 Medium |

| Azure Option | When to Choose |
|--------------|----------------|
| Microsoft Defender for Cloud | Threat detection across Azure resources; vulnerability assessment; security recommendations; maps to GuardDuty + Inspector |

**Feature Gaps & Limitations**:
- GuardDuty findings → Defender for Cloud security alerts
- GuardDuty S3 protection → Defender for Storage
- GuardDuty EKS protection → Defender for Containers
- GuardDuty malware protection → Defender for Servers (malware scanning)

---

### Security Hub → Microsoft Defender for Cloud / Microsoft Sentinel

| Aspect | Details |
|--------|---------|
| **AWS Service** | Security Hub |
| **Azure Equivalent(s)** | **Microsoft Defender for Cloud**, **Microsoft Sentinel** |
| **Migration Complexity** | 🟡 Medium |

| Azure Option | When to Choose |
|--------------|----------------|
| Microsoft Defender for Cloud | Security posture management; compliance dashboards; CIS/NIST benchmarks; maps to Security Hub standards |
| Microsoft Sentinel | SIEM and SOAR; threat hunting; incident management; broader security operations |

**Feature Gaps & Limitations**:
- Security Hub integrations → Defender for Cloud connectors + Sentinel data connectors
- Security Hub automated remediations → Defender for Cloud auto-remediation or Sentinel playbooks

---

### Shield → Azure DDoS Protection

| Aspect | Details |
|--------|---------|
| **AWS Service** | Shield (Standard, Advanced) |
| **Azure Equivalent(s)** | **Azure DDoS Protection** |
| **Migration Complexity** | 🟢 Low |

| Azure Option | When to Choose |
|--------------|----------------|
| Azure DDoS Infrastructure Protection | Basic DDoS protection; free; always-on; maps to Shield Standard |
| Azure DDoS Network Protection | Advanced DDoS protection; adaptive tuning; cost protection; maps to Shield Advanced |

---

## 7. Observability

### CloudWatch → Azure Monitor

| Aspect | Details |
|--------|---------|
| **AWS Service** | CloudWatch (Metrics, Logs, Alarms, Dashboards) |
| **Azure Equivalent(s)** | **Azure Monitor**, **Application Insights**, **Log Analytics** |
| **Migration Complexity** | 🟡 Medium |

| Azure Option | When to Choose |
|--------------|----------------|
| Azure Monitor Metrics | Infrastructure metrics; VM, database, and service health; maps to CloudWatch Metrics |
| Azure Monitor Logs (Log Analytics) | Log aggregation and querying (KQL); maps to CloudWatch Logs + Logs Insights |
| Application Insights | Application performance monitoring (APM); auto-instrumentation; maps to CloudWatch Application Insights |
| Azure Monitor Alerts | Metric and log-based alerting; action groups; maps to CloudWatch Alarms |
| Azure Dashboards / Workbooks | Visualization; maps to CloudWatch Dashboards |

**Feature Gaps & Limitations**:
- CloudWatch Synthetics (canaries) → Application Insights availability tests
- CloudWatch RUM → Application Insights browser SDK
- CloudWatch Contributor Insights → Log Analytics queries (manual)
- CloudWatch Anomaly Detection → Azure Monitor dynamic thresholds
- CloudWatch Logs query syntax → KQL (Kusto Query Language) — requires rewriting queries
- CloudWatch Embedded Metric Format → Application Insights custom metrics

**Key Considerations**:
- KQL is more powerful than CloudWatch Logs Insights but requires learning
- Application Insights auto-instrumentation simplifies APM setup for .NET and Java
- Azure Monitor Agent replaces multiple CloudWatch agents

---

### X-Ray → Application Insights (Distributed Tracing)

| Aspect | Details |
|--------|---------|
| **AWS Service** | X-Ray |
| **Azure Equivalent(s)** | **Application Insights (Distributed Tracing)** |
| **Migration Complexity** | 🟡 Medium |

| Azure Option | When to Choose |
|--------------|----------------|
| Application Insights | Distributed tracing, dependency mapping, performance diagnostics; supports OpenTelemetry; maps to X-Ray tracing |

**Feature Gaps & Limitations**:
- X-Ray SDK → Application Insights SDK or OpenTelemetry SDK (recommended)
- X-Ray daemon → Application Insights Agent or OpenTelemetry Collector
- X-Ray service map → Application Insights Application Map
- X-Ray groups and sampling rules → Application Insights sampling configuration

**Key Considerations**:
- Migrate to OpenTelemetry as the common standard for both platforms
- Application Insights auto-instrumentation for .NET and Java reduces code changes

---

### CloudTrail → Azure Activity Log / Microsoft Entra Audit Logs

| Aspect | Details |
|--------|---------|
| **AWS Service** | CloudTrail |
| **Azure Equivalent(s)** | **Azure Activity Log**, **Microsoft Entra Audit Logs**, **Azure Monitor Diagnostic Settings** |
| **Migration Complexity** | 🟢 Low |

| Azure Option | When to Choose |
|--------------|----------------|
| Azure Activity Log | Control plane operations (resource create/update/delete); maps to CloudTrail management events |
| Microsoft Entra Audit Logs | Identity operations (sign-ins, role changes); maps to CloudTrail IAM events |
| Azure Monitor Diagnostic Settings | Data plane operations; resource-level logging; maps to CloudTrail data events |

**Feature Gaps & Limitations**:
- CloudTrail Lake → Log Analytics workspace (long-term query storage)
- CloudTrail Insights → Azure Monitor anomaly detection
- CloudTrail Organization trail → Azure Policy for diagnostic settings at scale

---

## 8. CI/CD

### CodePipeline → Azure DevOps Pipelines / GitHub Actions

| Aspect | Details |
|--------|---------|
| **AWS Service** | CodePipeline |
| **Azure Equivalent(s)** | **Azure DevOps Pipelines**, **GitHub Actions** |
| **Migration Complexity** | 🟡 Medium |

| Azure Option | When to Choose |
|--------------|----------------|
| GitHub Actions | GitHub-hosted repos; modern YAML workflows; extensive marketplace; tighter GitHub integration |
| Azure DevOps Pipelines | Enterprise ALM; need boards + repos + pipelines together; complex release gates; YAML or classic designer |

**Feature Gaps & Limitations**:
- CodePipeline stages/actions → GitHub Actions jobs/steps or Azure Pipelines stages/jobs
- CodePipeline manual approvals → GitHub Actions environments with required reviewers or Azure Pipelines approval gates
- CodePipeline custom actions → GitHub Actions custom actions or Azure Pipelines extensions

---

### CodeBuild → GitHub Actions / Azure DevOps Pipelines

| Aspect | Details |
|--------|---------|
| **AWS Service** | CodeBuild |
| **Azure Equivalent(s)** | **GitHub Actions runners**, **Azure DevOps Pipelines agents** |
| **Migration Complexity** | 🟡 Medium |

| Azure Option | When to Choose |
|--------------|----------------|
| GitHub Actions (hosted runners) | Managed build environments; Docker support; matrix builds; maps to CodeBuild managed images |
| GitHub Actions (self-hosted runners) | Custom build environments; GPU or special hardware; maps to CodeBuild custom images |
| Azure DevOps (Microsoft-hosted agents) | Managed build agents; supports Windows, Linux, macOS |
| Azure DevOps (self-hosted agents) | On-premises or custom build agents; VNet-connected builds |

**Feature Gaps & Limitations**:
- CodeBuild buildspec.yml → GitHub Actions workflow YAML or Azure Pipelines YAML
- CodeBuild caching (S3) → GitHub Actions cache action or Azure Pipelines pipeline caching
- CodeBuild reports → GitHub Actions test reporting or Azure Pipelines test results
- CodeBuild batch builds → GitHub Actions matrix strategy or Azure Pipelines parallel jobs

---

### CodeDeploy → GitHub Actions / Azure DevOps / Azure Deployment Center

| Aspect | Details |
|--------|---------|
| **AWS Service** | CodeDeploy |
| **Azure Equivalent(s)** | **GitHub Actions**, **Azure DevOps Release Pipelines**, **Azure Deployment Center** |
| **Migration Complexity** | 🟡 Medium |

| Azure Option | When to Choose |
|--------------|----------------|
| GitHub Actions deploy steps | Code deployment as part of CI/CD workflow; deploy to App Service, AKS, Container Apps |
| Azure DevOps Release Pipelines | Complex multi-stage deployments; stage gates and approvals |
| Azure Deployment Center | Simple App Service deployments directly from GitHub or Azure Repos |

**Feature Gaps & Limitations**:
- CodeDeploy Blue/Green → App Service deployment slots, AKS blue/green, or Container Apps revisions
- CodeDeploy Rolling → AKS rolling update strategy or App Service gradual rollout
- CodeDeploy appspec.yml → GitHub Actions workflow or Azure Pipelines release definition
- CodeDeploy lifecycle hooks → GitHub Actions steps or Azure Pipelines tasks

---

### CodeCommit → GitHub / Azure Repos

| Aspect | Details |
|--------|---------|
| **AWS Service** | CodeCommit (deprecated) |
| **Azure Equivalent(s)** | **GitHub**, **Azure Repos** |
| **Migration Complexity** | 🟢 Low |

| Azure Option | When to Choose |
|--------------|----------------|
| GitHub | Modern Git hosting; rich ecosystem; Actions CI/CD; Copilot integration; recommended for most teams |
| Azure Repos | Part of Azure DevOps; need integrated boards + repos + pipelines; TFVC support |

**Key Considerations**:
- CodeCommit is deprecated; migration is strongly recommended
- Standard Git migration; `git clone --mirror` and `git push --mirror`

---

### CodeArtifact → GitHub Packages / Azure Artifacts

| Aspect | Details |
|--------|---------|
| **AWS Service** | CodeArtifact |
| **Azure Equivalent(s)** | **GitHub Packages**, **Azure Artifacts** |
| **Migration Complexity** | 🟢 Low |

| Azure Option | When to Choose |
|--------------|----------------|
| GitHub Packages | npm, Maven, NuGet, Docker containers; integrated with GitHub repos and Actions |
| Azure Artifacts | npm, Maven, NuGet, Python, Universal Packages; integrated with Azure DevOps; upstream sources |

**Feature Gaps & Limitations**:
- CodeArtifact domains → Azure Artifacts feeds (different organizational model)
- CodeArtifact upstream repositories → Azure Artifacts upstream sources (similar)

---

## 9. Serverless & Integration

### Step Functions → Azure Logic Apps / Azure Durable Functions

| Aspect | Details |
|--------|---------|
| **AWS Service** | Step Functions |
| **Azure Equivalent(s)** | **Azure Durable Functions**, **Azure Logic Apps** |
| **Migration Complexity** | 🟡 Medium – 🟠 High |

| Azure Option | When to Choose |
|--------------|----------------|
| Azure Durable Functions | Code-first orchestration; developer-defined workflows in C#, JavaScript, Python, Java; complex retry/fan-out patterns; maps to Step Functions Standard |
| Azure Logic Apps (Consumption) | Low-code/visual designer; 400+ connectors; SaaS integrations; maps to Step Functions with service integrations |
| Azure Logic Apps (Standard) | Single-tenant; VNet integration; stateful/stateless workflows; enterprise integration patterns |

**Feature Gaps & Limitations**:
- Step Functions ASL (Amazon States Language) → Durable Functions code-based orchestration (no JSON workflow language)
- Step Functions Express Workflows → Durable Functions or Logic Apps stateless workflows
- Step Functions Map state → Durable Functions fan-out/fan-in pattern
- Step Functions service integrations → Logic Apps connectors (broader ecosystem)
- Step Functions Workflow Studio → Logic Apps designer (visual editor)

**Key Considerations**:
- ASL workflow definitions require rewriting; no automated translation
- Durable Functions provides more developer control; Logic Apps provides more connectors
- For AWS-integrated workflows (DynamoDB, SQS, etc.), Logic Apps connectors may cover the equivalent Azure services

---

### AppSync → Azure API Management / Azure Functions

| Aspect | Details |
|--------|---------|
| **AWS Service** | AppSync (GraphQL) |
| **Azure Equivalent(s)** | **Azure API Management (GraphQL)**, **Hot Chocolate on Azure Functions/App Service** |
| **Migration Complexity** | 🟡 Medium |

| Azure Option | When to Choose |
|--------------|----------------|
| Azure API Management (Synthetic GraphQL) | Managed GraphQL gateway; compose GraphQL from REST backends; policy engine |
| Azure API Management (Pass-through GraphQL) | Proxy existing GraphQL APIs; add authentication, rate limiting, monitoring |
| Self-hosted GraphQL (Hot Chocolate, Apollo) | Full control; custom resolvers; deploy on App Service, Container Apps, or AKS |

**Feature Gaps & Limitations**:
- AppSync real-time subscriptions → Self-hosted GraphQL with WebSocket; APIM doesn't support GraphQL subscriptions yet
- AppSync resolvers (VTL templates) → Custom resolver code (no VTL equivalent)
- AppSync caching → APIM response caching or application-level caching
- AppSync merged APIs → APIM GraphQL API composition

---

### Amplify → Azure Static Web Apps / Azure Developer CLI

| Aspect | Details |
|--------|---------|
| **AWS Service** | Amplify (Hosting + Backend) |
| **Azure Equivalent(s)** | **Azure Static Web Apps**, **Azure Developer CLI (azd)** |
| **Migration Complexity** | 🟡 Medium |

| Azure Option | When to Choose |
|--------------|----------------|
| Azure Static Web Apps | Frontend hosting with serverless API; integrated auth; staging environments; maps to Amplify Hosting |
| Azure Developer CLI (azd) | Full-stack provisioning and deployment templates; maps to Amplify's backend/infrastructure capabilities |

**Feature Gaps & Limitations**:
- Amplify CLI → `azd` CLI (different template model)
- Amplify DataStore → No direct equivalent; use Cosmos DB SDKs
- Amplify Auth → Static Web Apps built-in auth or Entra External ID
- Amplify Storage → Azure Blob Storage SDK
- Amplify Gen 2 (code-first) → Bicep/Terraform with azd

---

### SES → Azure Communication Services Email

| Aspect | Details |
|--------|---------|
| **AWS Service** | SES (Simple Email Service) |
| **Azure Equivalent(s)** | **Azure Communication Services (Email)**, **SendGrid (Azure Marketplace)** |
| **Migration Complexity** | 🟢 Low |

| Azure Option | When to Choose |
|--------------|----------------|
| Azure Communication Services Email | First-party Azure email; integrated with Azure ecosystem; transactional email |
| SendGrid (via Azure Marketplace) | High-volume email; marketing campaigns; advanced analytics; established email platform |

**Feature Gaps & Limitations**:
- SES templates → SendGrid dynamic templates or Communication Services templates
- SES sending statistics → SendGrid analytics or Communication Services logs
- SES dedicated IPs → SendGrid dedicated IPs

---

### Pinpoint → Azure Communication Services / Azure Notification Hubs

| Aspect | Details |
|--------|---------|
| **AWS Service** | Pinpoint |
| **Azure Equivalent(s)** | **Azure Communication Services**, **Azure Notification Hubs** |
| **Migration Complexity** | 🟡 Medium |

| Azure Option | When to Choose |
|--------------|----------------|
| Azure Communication Services | SMS, email, voice, chat; customer engagement; maps to Pinpoint channels |
| Azure Notification Hubs | Mobile push notifications at scale; maps to Pinpoint push |

**Feature Gaps & Limitations**:
- Pinpoint campaign management → No direct equivalent; use third-party marketing automation
- Pinpoint analytics/segmentation → Azure communication logs + custom analytics
- Pinpoint journeys → Logic Apps or custom workflow (no direct equivalent)

---

## 10. Analytics & Data

### AWS Glue → Azure Data Factory / Azure Synapse Pipelines

| Aspect | Details |
|--------|---------|
| **AWS Service** | AWS Glue (ETL, Crawler, Data Catalog) |
| **Azure Equivalent(s)** | **Azure Data Factory**, **Azure Synapse Pipelines**, **Microsoft Purview** |
| **Migration Complexity** | 🟡 Medium |

| Azure Option | When to Choose |
|--------------|----------------|
| Azure Data Factory | Managed ETL/ELT; data integration; 90+ connectors; visual pipeline designer; maps to Glue ETL + crawlers |
| Azure Synapse Pipelines | Data integration within Synapse workspace; same engine as Data Factory; maps to Glue within analytics context |
| Microsoft Purview | Data catalog and governance; data lineage; maps to Glue Data Catalog |

**Feature Gaps & Limitations**:
- Glue crawlers → Data Factory mapping data flows or Purview scanning
- Glue PySpark jobs → Data Factory mapping data flows (Spark-based) or Synapse Spark pools
- Glue Data Catalog → Microsoft Purview Data Catalog
- Glue Schema Registry → Purview or Azure Schema Registry (Event Hubs)
- Glue DataBrew → Data Factory data wrangling (Power Query based)

---

### Athena → Azure Synapse Serverless SQL

| Aspect | Details |
|--------|---------|
| **AWS Service** | Athena |
| **Azure Equivalent(s)** | **Azure Synapse Analytics (Serverless SQL Pool)** |
| **Migration Complexity** | 🟡 Medium |

| Azure Option | When to Choose |
|--------------|----------------|
| Synapse Serverless SQL Pool | Ad-hoc SQL queries over data lake (Parquet, CSV, JSON); pay-per-query; no infrastructure |

**Feature Gaps & Limitations**:
- Athena workgroups → Synapse workspace RBAC
- Athena Federated Query → Synapse serverless external tables (limited federation)
- Athena CTAS → Synapse CETAS (Create External Table As Select)
- Athena Iceberg/Hudi support → Synapse Delta Lake (preferred format; Iceberg support limited)
- Presto/Trino SQL → T-SQL (syntax differences require query rewriting)

---

### EMR → Azure HDInsight / Azure Synapse Spark / Azure Databricks

| Aspect | Details |
|--------|---------|
| **AWS Service** | EMR (Elastic MapReduce) |
| **Azure Equivalent(s)** | **Azure HDInsight**, **Azure Synapse Spark**, **Azure Databricks** |
| **Migration Complexity** | 🟡 Medium – 🟠 High |

| Azure Option | When to Choose |
|--------------|----------------|
| Azure HDInsight | Open-source Hadoop/Spark/HBase/Kafka clusters; most direct EMR replacement |
| Azure Synapse Spark Pools | Spark integrated with Synapse analytics workspace; serverless Spark |
| Azure Databricks | Unified analytics platform; collaborative notebooks; MLflow integration; Delta Lake; premium Spark experience |

**Feature Gaps & Limitations**:
- EMR Studio → Databricks workspace or Synapse Studio
- EMR Serverless → Synapse Spark serverless pools or Databricks serverless
- EMR on EKS → Spark on AKS (self-managed)
- EMR step functions → Databricks Jobs or Synapse pipelines

**Key Considerations**:
- Databricks is the most feature-rich Spark platform on Azure
- For new projects, Databricks or Synapse Spark are preferred over HDInsight
- PySpark code is largely portable; main changes are storage paths and configurations

---

### Lake Formation → Microsoft Purview / Azure Data Lake Storage

| Aspect | Details |
|--------|---------|
| **AWS Service** | Lake Formation |
| **Azure Equivalent(s)** | **Microsoft Purview**, **Azure Data Lake Storage Gen2** |
| **Migration Complexity** | 🟠 High |

| Azure Option | When to Choose |
|--------------|----------------|
| Microsoft Purview | Data governance, cataloging, lineage, access policies; maps to Lake Formation governance |
| Azure Data Lake Storage Gen2 | Data lake storage with hierarchical namespace; maps to Lake Formation managed S3 data lake |

**Feature Gaps & Limitations**:
- Lake Formation fine-grained access control → Purview access policies (evolving) or storage ACLs
- Lake Formation blueprints → No direct equivalent; use Data Factory templates
- Lake Formation governed tables → Delta Lake tables with Purview governance

---

### Kinesis Data Analytics → Azure Stream Analytics

| Aspect | Details |
|--------|---------|
| **AWS Service** | Kinesis Data Analytics (Apache Flink) |
| **Azure Equivalent(s)** | **Azure Stream Analytics**, **Azure Databricks Structured Streaming** |
| **Migration Complexity** | 🟡 Medium – 🟠 High |

| Azure Option | When to Choose |
|--------------|----------------|
| Azure Stream Analytics | SQL-based stream processing; real-time analytics; IoT scenarios; simpler streaming jobs |
| Azure Databricks Structured Streaming | Complex stream processing; Spark-based; need joins, windowing, ML on streams |

**Feature Gaps & Limitations**:
- Kinesis Analytics Apache Flink → No managed Flink on Azure; use HDInsight Flink or Databricks
- Kinesis Analytics SQL → Stream Analytics SQL (different dialect)

---

## 11. AI/ML

### SageMaker → Azure Machine Learning

| Aspect | Details |
|--------|---------|
| **AWS Service** | SageMaker |
| **Azure Equivalent(s)** | **Azure Machine Learning** |
| **Migration Complexity** | 🟠 High |

| Azure Option | When to Choose |
|--------------|----------------|
| Azure Machine Learning | End-to-end ML platform; training, deployment, MLOps; notebooks, pipelines, endpoints; maps to SageMaker Studio |

**Feature Gaps & Limitations**:
- SageMaker Studio → Azure ML Studio
- SageMaker Pipelines → Azure ML Pipelines
- SageMaker Feature Store → Azure ML managed feature store
- SageMaker Endpoints → Azure ML managed endpoints (online/batch)
- SageMaker Ground Truth → Azure ML data labeling
- SageMaker Canvas (no-code) → Azure ML designer (visual)
- SageMaker JumpStart → Azure ML model catalog
- SageMaker built-in algorithms → Azure ML built-in algorithms (different set)

**Key Considerations**:
- Model artifacts need re-packaging; container formats differ
- Training scripts (PyTorch, TensorFlow) are largely portable
- MLOps pipelines require rewriting

---

### Bedrock → Azure AI Foundry / Azure OpenAI Service

| Aspect | Details |
|--------|---------|
| **AWS Service** | Bedrock |
| **Azure Equivalent(s)** | **Azure AI Foundry**, **Azure OpenAI Service** |
| **Migration Complexity** | 🟡 Medium |

| Azure Option | When to Choose |
|--------------|----------------|
| Azure OpenAI Service | GPT-4, GPT-4o, DALL-E, Whisper; enterprise-grade OpenAI models; maps to Bedrock's Claude, Titan, etc. |
| Azure AI Foundry | Build, evaluate, and deploy AI applications; model catalog; prompt flow; maps to Bedrock's agent and RAG capabilities |

**Feature Gaps & Limitations**:
- Bedrock model variety (Anthropic, Cohere, Meta, etc.) → Azure AI model catalog (OpenAI, Meta, Mistral, etc.; different model selection)
- Bedrock Knowledge Bases → Azure AI Search + Azure OpenAI (RAG pattern)
- Bedrock Agents → Azure AI Foundry agents
- Bedrock Guardrails → Azure AI Content Safety

**Key Considerations**:
- API formats differ (Bedrock API vs OpenAI-compatible API)
- Model availability varies by region on both platforms
- Azure OpenAI provides GPT-4 models not available on Bedrock; Bedrock provides Claude models not on Azure OpenAI

---

### Comprehend → Azure AI Language

| Aspect | Details |
|--------|---------|
| **AWS Service** | Comprehend |
| **Azure Equivalent(s)** | **Azure AI Language** |
| **Migration Complexity** | 🟡 Medium |

| Azure Option | When to Choose |
|--------------|----------------|
| Azure AI Language | Sentiment analysis, entity recognition, key phrase extraction, PII detection, language detection; maps to Comprehend |

**Feature Gaps & Limitations**:
- Comprehend custom classification → Azure AI Language custom text classification
- Comprehend custom entity recognition → Azure AI Language custom NER
- Comprehend Flywheel → Azure AI Language model evaluation (different management model)

---

### Rekognition → Azure AI Vision

| Aspect | Details |
|--------|---------|
| **AWS Service** | Rekognition |
| **Azure Equivalent(s)** | **Azure AI Vision**, **Azure AI Face** |
| **Migration Complexity** | 🟡 Medium |

| Azure Option | When to Choose |
|--------------|----------------|
| Azure AI Vision | Image analysis, OCR, object detection, image tagging |
| Azure AI Face | Face detection, verification, identification (regulated; requires approval for some features) |
| Azure AI Video Indexer | Video analysis; maps to Rekognition Video |

**Feature Gaps & Limitations**:
- Rekognition face comparison → Azure AI Face (requires limited access approval)
- Rekognition Celebrity recognition → Limited in Azure AI (privacy restrictions)
- Rekognition Content Moderation → Azure AI Content Safety
- Rekognition Custom Labels → Azure AI Vision custom models

---

### Textract → Azure AI Document Intelligence

| Aspect | Details |
|--------|---------|
| **AWS Service** | Textract |
| **Azure Equivalent(s)** | **Azure AI Document Intelligence** (formerly Form Recognizer) |
| **Migration Complexity** | 🟡 Medium |

| Azure Option | When to Choose |
|--------------|----------------|
| Azure AI Document Intelligence | Document parsing, OCR, table/form extraction, custom document models |

**Feature Gaps & Limitations**:
- Textract AnalyzeDocument → Document Intelligence layout/read models
- Textract AnalyzeExpense → Document Intelligence invoice/receipt models
- Textract AnalyzeID → Document Intelligence ID document model
- Textract Lending → Document Intelligence mortgage models (custom training)

---

### Polly → Azure AI Speech

| Aspect | Details |
|--------|---------|
| **AWS Service** | Polly |
| **Azure Equivalent(s)** | **Azure AI Speech** (Text-to-Speech) |
| **Migration Complexity** | 🟢 Low |

| Azure Option | When to Choose |
|--------------|----------------|
| Azure AI Speech (TTS) | Text-to-speech with neural voices; SSML support; custom voice; real-time and batch synthesis |

**Feature Gaps & Limitations**:
- Polly neural voices → Azure Neural TTS voices (different voice set; Azure has more voices)
- Polly Speech Marks → Azure AI Speech viseme and word boundary events
- Polly lexicons → Azure AI Speech custom pronunciation

---

### Lex → Azure AI Bot Service / Azure AI Language (CLU)

| Aspect | Details |
|--------|---------|
| **AWS Service** | Lex |
| **Azure Equivalent(s)** | **Azure AI Bot Service**, **Azure AI Language (CLU)** |
| **Migration Complexity** | 🟡 Medium |

| Azure Option | When to Choose |
|--------------|----------------|
| Azure AI Bot Service | Conversational bot framework; multi-channel deployment; Bot Framework SDK |
| Azure AI Language (CLU) | Conversational language understanding; intent and entity recognition; maps to Lex intents/slots |

**Feature Gaps & Limitations**:
- Lex intents/slots → CLU intents/entities
- Lex fulfillment (Lambda) → Bot Framework activity handlers (Azure Functions backed)
- Lex V2 streaming → Bot Framework Direct Line Speech

---

### Translate → Azure AI Translator

| Aspect | Details |
|--------|---------|
| **AWS Service** | Amazon Translate |
| **Azure Equivalent(s)** | **Azure AI Translator** |
| **Migration Complexity** | 🟢 Low |

| Azure Option | When to Choose |
|--------------|----------------|
| Azure AI Translator | Text translation, document translation, custom translator; supports 100+ languages |

**Feature Gaps & Limitations**:
- Translate Active Custom Translation → Azure Custom Translator
- Translate parallel data → Custom Translator training data
- Both services support real-time and batch translation

---

## 12. Container & Registry

### ECR → Azure Container Registry (ACR)

| Aspect | Details |
|--------|---------|
| **AWS Service** | ECR (Elastic Container Registry) |
| **Azure Equivalent(s)** | **Azure Container Registry (ACR)** |
| **Migration Complexity** | 🟢 Low |

| Azure Option | When to Choose |
|--------------|----------------|
| ACR Basic | Dev/test; small teams; personal projects |
| ACR Standard | Production use; higher storage and throughput |
| ACR Premium | Geo-replication; private endpoints; content trust; enterprise-grade |

**Feature Gaps & Limitations**:
- ECR lifecycle policies → ACR retention policies (similar)
- ECR pull-through cache → ACR cache rules for upstream registries
- ECR image scanning → ACR integration with Microsoft Defender for Containers
- ECR cross-account access → ACR RBAC with Entra ID

**Key Considerations**:
- Use `az acr import` or `docker pull/push` to migrate images
- ACR Tasks can build images in the cloud (maps to ECR + CodeBuild)
- ACR integrates natively with AKS, Container Apps, and App Service

---

### App Runner → Azure Container Apps / Azure App Service

| Aspect | Details |
|--------|---------|
| **AWS Service** | App Runner |
| **Azure Equivalent(s)** | **Azure Container Apps**, **Azure App Service (containers)** |
| **Migration Complexity** | 🟢 Low |

| Azure Option | When to Choose |
|--------------|----------------|
| Azure Container Apps | Serverless containers; scale-to-zero; Dapr integration; event-driven; maps closely to App Runner's simplicity |
| Azure App Service (containers) | Custom container deployment on App Service; deployment slots; established platform |

**Feature Gaps & Limitations**:
- App Runner auto-deploy from ECR → Container Apps deployment from ACR with webhooks
- App Runner VPC connector → Container Apps VNet integration
- App Runner observability → Container Apps with Application Insights

**Key Considerations**:
- Container Apps is the closest Azure equivalent to App Runner's developer experience
- Both support automatic scaling and HTTPS ingress out of the box

---

## Quick Reference Summary

| AWS Service | Primary Azure Equivalent | Complexity |
|-------------|-------------------------|------------|
| EC2 | Azure Virtual Machines / VMSS | 🟢 Low |
| Lambda | Azure Functions | 🟡 Medium |
| Elastic Beanstalk | Azure App Service | 🟢 Low |
| ECS / Fargate | Azure Container Apps | 🟡 Medium |
| EKS | Azure Kubernetes Service (AKS) | 🟡 Medium |
| AWS Batch | Azure Batch / Container Apps Jobs | 🟡 Medium |
| S3 | Azure Blob Storage | 🟢 Low |
| EBS | Azure Managed Disks | 🟢 Low |
| EFS | Azure Files / Azure NetApp Files | 🟢 Low |
| FSx | Azure NetApp Files / Azure Files / Managed Lustre | 🟡 Medium |
| Glacier | Azure Blob Archive tier | 🟢 Low |
| DynamoDB | Azure Cosmos DB | 🟡 Medium |
| RDS | Azure SQL / PostgreSQL / MySQL Flexible Server | 🟢–🟡 |
| Aurora | Azure SQL Hyperscale / PostgreSQL Flexible | 🟡 Medium |
| ElastiCache | Azure Cache for Redis / Azure Managed Redis | 🟢 Low |
| Redshift | Azure Synapse Analytics / Microsoft Fabric | 🟠 High |
| DocumentDB | Azure Cosmos DB for MongoDB | 🟢 Low |
| Neptune | Azure Cosmos DB for Apache Gremlin | 🟡 Medium |
| MemoryDB | Azure Managed Redis (Enterprise) | 🟢 Low |
| SQS | Azure Queue Storage / Service Bus | 🟢–🟡 |
| SNS | Service Bus Topics / Event Grid / Notification Hubs | 🟡 Medium |
| EventBridge | Azure Event Grid | 🟡 Medium |
| Kinesis | Azure Event Hubs | 🟡 Medium |
| Amazon MQ | Azure Service Bus / self-hosted RabbitMQ | 🟡–🟠 |
| MSK (Kafka) | Azure Event Hubs (Kafka) / HDInsight Kafka | 🟡 Medium |
| VPC | Azure Virtual Network (VNet) | 🟡 Medium |
| Route 53 | Azure DNS / Traffic Manager / Front Door | 🟢 Low |
| CloudFront | Azure Front Door / Azure CDN | 🟢 Low |
| API Gateway | Azure API Management | 🟡 Medium |
| ALB / NLB | Application Gateway / Azure Load Balancer | 🟢 Low |
| Direct Connect | Azure ExpressRoute | 🟠 High |
| Transit Gateway | Azure Virtual WAN / VNet peering | 🟠 High |
| PrivateLink | Azure Private Link | 🟢 Low |
| IAM | Entra ID / Azure RBAC / Managed Identities | 🟠 High |
| Cognito | Microsoft Entra External ID | 🟠 High |
| Secrets Manager | Azure Key Vault | 🟢 Low |
| Parameter Store | Azure App Configuration / Key Vault | 🟢 Low |
| KMS | Azure Key Vault (Keys/Managed HSM) | 🟡 Medium |
| WAF | Azure WAF | 🟡 Medium |
| GuardDuty | Microsoft Defender for Cloud | 🟡 Medium |
| Security Hub | Defender for Cloud / Microsoft Sentinel | 🟡 Medium |
| Shield | Azure DDoS Protection | 🟢 Low |
| CloudWatch | Azure Monitor / Application Insights / Log Analytics | 🟡 Medium |
| X-Ray | Application Insights (Distributed Tracing) | 🟡 Medium |
| CloudTrail | Azure Activity Log / Entra Audit Logs | 🟢 Low |
| CodePipeline | GitHub Actions / Azure DevOps Pipelines | 🟡 Medium |
| CodeBuild | GitHub Actions / Azure DevOps Pipelines | 🟡 Medium |
| CodeDeploy | GitHub Actions / Azure DevOps | 🟡 Medium |
| CodeCommit | GitHub / Azure Repos | 🟢 Low |
| CodeArtifact | GitHub Packages / Azure Artifacts | 🟢 Low |
| Step Functions | Durable Functions / Logic Apps | 🟡–🟠 |
| AppSync | Azure API Management (GraphQL) | 🟡 Medium |
| Amplify | Azure Static Web Apps / azd | 🟡 Medium |
| SES | Azure Communication Services Email / SendGrid | 🟢 Low |
| Pinpoint | Azure Communication Services / Notification Hubs | 🟡 Medium |
| Glue | Azure Data Factory / Synapse Pipelines / Purview | 🟡 Medium |
| Athena | Azure Synapse Serverless SQL | 🟡 Medium |
| EMR | HDInsight / Synapse Spark / Databricks | 🟡–🟠 |
| Lake Formation | Microsoft Purview / ADLS Gen2 | 🟠 High |
| Kinesis Analytics | Azure Stream Analytics / Databricks Streaming | 🟡–🟠 |
| SageMaker | Azure Machine Learning | 🟠 High |
| Bedrock | Azure AI Foundry / Azure OpenAI Service | 🟡 Medium |
| Comprehend | Azure AI Language | 🟡 Medium |
| Rekognition | Azure AI Vision / Azure AI Face | 🟡 Medium |
| Textract | Azure AI Document Intelligence | 🟡 Medium |
| Polly | Azure AI Speech (TTS) | 🟢 Low |
| Lex | Azure AI Bot Service / CLU | 🟡 Medium |
| Translate | Azure AI Translator | 🟢 Low |
| ECR | Azure Container Registry (ACR) | 🟢 Low |
| App Runner | Azure Container Apps / App Service | 🟢 Low |
