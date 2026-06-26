# Skill: Workload Pattern — Event-Driven

> Workload pattern for applications that react to events: message queue consumers, pub/sub subscribers, event-stream processors, change-data-capture consumers, webhook fan-out, IoT telemetry processors.

## When to Use

- `workload.primary_pattern: event-driven` in the Capability Matrix
- Evidence: SQS/SNS/EventBridge/Kinesis/Kafka/RabbitMQ/Service Bus/Pub-Sub consumer code; `@MessageDriven` (JEE); Celery worker; bullmq consumer; Functions queue trigger

## Defining Characteristics

- **Trigger:** message / event arrives in a queue / topic / stream
- **State:** typically stateless per message; durable store for state
- **Latency:** ms-to-second per message (sometimes faster)
- **Throughput:** can spike from 0 to thousands/sec
- **Scaling:** triggered by queue depth / lag
- **Failure mode:** dead-letter queue (DLQ) + retry

## Sub-Patterns

| Sub-pattern | Detection signal | Azure target tendency |
|-------------|------------------|----------------------|
| **Point-to-point queue consumer** | SQS / Service Bus Queue / Rabbit / IBM MQ consumer | Functions (Queue trigger) / Container Apps + KEDA |
| **Pub/sub topic subscriber** | SNS / Service Bus Topic / Kafka topic / Pub/Sub subscription | Functions / Container Apps + KEDA |
| **Stream processor** | Kinesis / Event Hubs / Kafka stream consumer; offsets managed | Stream Analytics / Functions / Container Apps |
| **Change-data-capture (CDC)** | DynamoDB Streams / Debezium / SQL CDC | Functions / Container Apps; or Synapse Link |
| **IoT telemetry** | MQTT broker; device telemetry hub | IoT Hub + Stream Analytics / Functions |
| **Webhook fan-out** | Inbound webhook → multiple downstream calls | Event Grid + Functions / Logic Apps |
| **Choreography (services emitting + listening)** | Many small services, each producer + consumer | Service Bus + Container Apps; or EDA on Event Grid |
| **Orchestration (saga)** | State-machine spanning multiple steps | Durable Functions / Logic Apps Standard |

## Probes

### Trigger surface

- Source(s) of events: which broker(s), which topic(s) / queue(s)
- Event payload format: JSON / Avro / Protobuf / XML / binary
- Event schema versioning strategy
- At-least-once / at-most-once / exactly-once semantics expected
- Ordering requirements (FIFO / partition-keyed / unordered)

### Consumer shape

- Singleton consumer vs N parallel consumers
- Batch size per pull (1 vs 10 vs 100 vs 1000)
- Long-poll / push behavior
- Manual vs auto-ack
- Visibility timeout / lock duration
- Pre-fetch count

### Processing

- Per-message work: CPU-bound? IO-bound? external API?
- Side effects: DB writes (idempotent?), downstream API calls (idempotent?), file writes
- Order-of-operations matters? (idempotency key strategy)
- Transactional boundary (per message? per batch?)

### Failure handling

- Retry policy (immediate? exponential backoff? max retries?)
- Dead-letter destination
- Poison message detection
- Alerting on DLQ depth growth

### Throughput / scaling

- Average / peak / burst rate
- Backpressure handling (throttling? buffer? shedding?)
- Cold-start tolerance (if going to Functions)

### Downstream dependencies

- DBs (write throughput needed)
- External APIs (rate limits)
- Other queues (fan-out target)
- File destinations

### Observability

- Per-message correlation id
- End-to-end trace (producer → broker → consumer → downstream)
- Lag metric publication
- DLQ metric

## Phase Emphasis (per migration strategy)

| Strategy | Event-driven emphasis |
|----------|----------------------|
| Rehost | Phase 3 (compute fit); often requires broker migration (SQS → Service Bus, etc.) |
| Replatform | Phase 2 (broker SDK swap if needed), Phase 3 (managed broker + Container Apps/Functions), Phase 4 |
| Refactor | Phase 2 (idempotency, observability, DLQ handling), Phase 3 |
| Rearchitect | Phase 1 (event-storming), Phase 2 (split consumers), Phase 3 (Event Grid / Service Bus / Event Hubs) |
| Rebuild | Greenfield EDA on Event Grid + Container Apps |

## Target Azure Mapping

### Broker mapping (often required first)

| Current broker | Azure target |
|----------------|--------------|
| AWS SQS | Service Bus Queue (transactional, ordered) or Storage Queue (simple) |
| AWS SNS | Event Grid (event routing) or Service Bus Topic (subscription model) |
| AWS Kinesis Data Streams | Event Hubs |
| AWS EventBridge | Event Grid |
| AWS MSK (Kafka) | Event Hubs (Kafka API) or HDInsight Kafka or Confluent on Azure |
| GCP Pub/Sub | Event Grid or Service Bus Topic |
| GCP Cloud Tasks | Service Bus Queue |
| RabbitMQ self-hosted | Service Bus Queue/Topic (managed) or rabbit on Container Apps (if vendor-locked) |
| Apache Kafka self-hosted | Event Hubs (Kafka API) or Confluent on Azure |
| IBM MQ | Service Bus (refactor); or IBM MQ Advanced on AKS (vendor-locked) |

### Consumer mapping

| Consumer shape | Primary Azure compute | Notes |
|----------------|----------------------|-------|
| Low-rate, simple per-message | **Functions** (Queue/Topic/Event Hub trigger) | Cheap; auto-scale |
| Steady high-rate | **Container Apps + KEDA** (queue scaler) | Scale 0 → N on depth |
| Order-sensitive partitioned | **Functions** with Event Hub partition affinity, or **Container Apps** | Match partition count to consumer count |
| Heavy per-message processing (>5 min) | **Container Apps** (long-running) | Not Functions Consumption |
| Saga / orchestration | **Durable Functions** | First-class orchestration |
| Workflow with branches | **Logic Apps Standard** | Visual; pay-per-action |
| Stream analytics (windowed) | **Stream Analytics** | SQL over streams |
| ML on stream | **Container Apps** with model | Pair with Event Hubs |

## Cross-Cutting Event-Driven Requirements (always add to plan)

- **Idempotency** — every consumer must handle duplicate messages safely (at-least-once is the norm).
- **Dead-letter queue** — explicit DLQ topology + alerting.
- **Correlation IDs** — every message carries an end-to-end correlation id.
- **Schema registry** — for Avro/Protobuf streams (Event Hubs Schema Registry).
- **Application Insights** with custom event tracking; configure correlation propagation.
- **Lag / depth monitoring** — alert before consumer can't keep up.
- **Backpressure plan** — when downstream APIs throttle, do we slow consumer or drop?
- **Replay / offset reset** — for stream-based, the operational procedure to replay events.
- **Poison message handling** — explicit pattern: max retries → DLQ → human review.

## Anti-Patterns

- Don't migrate a broker without a translation layer for headers / metadata. SQS message attributes ≠ Service Bus properties.
- Don't preserve in-process queues (BlockingQueue) — they break in multi-instance Azure compute.
- Don't depend on exactly-once semantics across broker migration. Re-derive idempotency at the consumer.
- Don't use Functions Consumption for >5 min processing.
- Don't expose your broker to consumers directly across cloud — use Service Bus + private endpoints + managed identity.
- Don't migrate a Kafka topology with thousands of partitions to Event Hubs without checking partition limits.

## Output Checklist

- [ ] Event-driven sub-pattern identified
- [ ] Source broker(s) captured with topic/queue inventory
- [ ] Event payload format + schema captured
- [ ] Delivery semantics captured (at-least-once / exactly-once)
- [ ] Ordering requirements captured
- [ ] Consumer concurrency model captured
- [ ] Retry + DLQ policy captured
- [ ] Throughput profile captured (avg / peak / burst)
- [ ] Downstream dependencies mapped
- [ ] Correlation/observability plan captured
- [ ] Broker mapping decision logged
- [ ] Consumer compute mapping decision logged
- [ ] Idempotency strategy documented per consumer
