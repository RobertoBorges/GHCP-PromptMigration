# Skill: Workload Pattern — API Service

> Workload pattern for machine-facing API services: REST, gRPC, GraphQL, WebSocket, SOAP. No browser UI.

## When to Use

- `workload.primary_pattern: api-service` in the Capability Matrix
- Evidence: REST controllers / route handlers / OpenAPI spec, no UI views, machine clients

## Defining Characteristics

- **Client:** other services / mobile / partners / SDKs
- **Entry:** HTTP(S) JSON / gRPC / GraphQL / WS / SOAP request
- **State:** typically stateless per request (JWT for auth)
- **Latency:** SLO-driven (p95 < 200ms is common; 10ms for internal)
- **Throughput:** sustained QPS; spikier for partner-facing APIs
- **Lifecycle:** long-running; auto-restarted on crash

## Sub-Patterns

| Sub-pattern | Detection signal | Azure target tendency |
|-------------|------------------|----------------------|
| **REST (JSON)** | Controllers / route handlers; OpenAPI 3.x spec | App Service / Container Apps / Functions |
| **gRPC** | `*.proto` files; HTTP/2; gRPC server | Container Apps (gRPC native) / AKS |
| **GraphQL** | `schema.graphql`; Apollo/Hot Chocolate/express-graphql | Container Apps / App Service |
| **WebSocket / SignalR** | persistent connections; `ws` library, SignalR hubs | App Service (WebSocket support) / Container Apps; Azure SignalR Service |
| **SOAP** | WSDL files; XML envelopes; `[ServiceContract]` (WCF) | Refactor to REST (preferred); CoreWCF if SOAP must stay |
| **Webhook receiver** | Signed webhook endpoints; idempotent handlers | Functions (HTTP trigger) / Container Apps |
| **Public API behind APIM** | API key / OAuth2 / Bearer | APIM as edge + backend on App Service / Container Apps |
| **Internal microservice** | Called only from VNet / cluster | Container Apps with internal ingress / AKS |

## Probes

### API surface

- Endpoint inventory (OpenAPI spec → route count, method distribution)
- Versioning strategy (URL path `/v1`, header `Api-Version`, query string)
- Auth method (Bearer JWT, API key, OAuth client credentials, mTLS, none-internal)
- Rate limit headers / throttling logic
- Caching headers (ETag, Cache-Control)
- Error response shape (RFC 7807 Problem Details? custom?)

### Contract artifacts

- OpenAPI 3.x spec (`openapi.yaml`, `swagger.json`)
- gRPC `.proto` files
- GraphQL `schema.graphql`
- WSDL (for SOAP)
- AsyncAPI for event/async APIs

### Performance

- Request/response sizes
- Long-poll / WebSocket presence (lifetime of a connection)
- Streaming responses
- Connection pool sizing (DB, downstream HTTP)
- Cold-start sensitivity (if going to Functions)

### Downstream dependencies

- DB calls (which engine, pool size, query latency)
- Other services (HTTP, gRPC, queue)
- External APIs (vendor SDKs, rate limits, fallback behavior)

### Observability

- Structured logging (JSON?)
- Distributed tracing (OpenTelemetry? Application Insights? X-Ray? Datadog?)
- Metrics (Prometheus / OpenMetrics / vendor)

### Security

- Input validation
- Authentication (token validation path)
- Authorization (per-endpoint roles / scopes)
- Secrets handling (env vars → Key Vault)
- Rate limiting + WAF

## Phase Emphasis (per migration strategy)

| Strategy | API emphasis |
|----------|--------------|
| Rehost | Phase 3 + Phase 4; risk = cold-start on container start |
| Replatform | Phase 2 (containerize), Phase 3 (managed compute), Phase 4 |
| Refactor | Phase 2 (auth modernization, OpenAPI generation, structured logging) |
| Rearchitect | Phase 1 (split monolith API into microservices), Phase 2 (per-service), Phase 3 |
| Rebuild | Greenfield with modern stack |

## Target Azure Mapping

| API shape | Primary Azure target | Notes |
|-----------|----------------------|-------|
| REST (low scale) | **App Service Linux** | Easy; cheap; deployment slots |
| REST (containerized, modern) | **Container Apps** | Managed scale; revisions for blue/green |
| REST (event-shaped, low utilization) | **Azure Functions** | Pay-per-call; cold start to manage |
| gRPC | **Container Apps** (native HTTP/2 support) | AKS for complex topology |
| GraphQL | **Container Apps** | Same as REST |
| WebSocket (broadcast / fanout) | **App Service** + Azure SignalR Service | Offload connection management |
| SOAP | Container Apps with CoreWCF | Modernize to REST when external clients allow |
| Webhook receiver | **Functions** (HTTP trigger) | Naturally event-shaped |
| High QPS public API | **APIM** in front + Container Apps backend | Auth, rate limit, transformation at APIM |
| Partner-facing API | APIM + Front Door + Backend | Add WAF |

## Cross-Cutting API Requirements (always add to plan)

- **OpenAPI spec generation/maintenance** (used by APIM import, SDK generation)
- **Application Insights** + OpenTelemetry instrumentation
- **Key Vault references** for backend credentials
- **Managed identity** for downstream Azure resources (no connection strings)
- **APIM** for any externally-exposed API (versioning, throttling, JWT validation)
- **Health endpoints** (`/health`, `/livez`, `/readyz`) for Container Apps / AKS probes
- **CORS** policy (especially if SPA frontend on different domain)
- **HTTPS-only** + HSTS

## Anti-Patterns

- Don't expose backend directly without APIM (or App Gateway) for public APIs. You lose rate limiting, auth, and observability.
- Don't keep custom rate-limiting code when APIM can do it.
- Don't ship without an OpenAPI spec. APIM, SDK gen, and contract tests all depend on it.
- Don't use App Service for low-utilization webhook receivers. Functions is cheaper.
- Don't terminate gRPC at App Service Windows. Use Container Apps for gRPC.
- Don't preserve cookie-based session in an API service. Move to stateless JWT.
- Don't migrate WCF SOAP "as-is" without checking whether the external clients can move to REST.

## Output Checklist

- [ ] API sub-pattern identified
- [ ] Endpoint count + OpenAPI spec captured (or noted as missing)
- [ ] Auth method captured
- [ ] Rate limiting / throttling captured
- [ ] Streaming / WebSocket presence captured
- [ ] Performance SLOs documented
- [ ] Downstream dependencies mapped
- [ ] Observability instrumentation captured
- [ ] APIM placement decision logged (yes/no, where)
- [ ] Health endpoints presence captured
- [ ] Target Azure compute selected
- [ ] SDK/client distribution implications captured (if customer-facing)
