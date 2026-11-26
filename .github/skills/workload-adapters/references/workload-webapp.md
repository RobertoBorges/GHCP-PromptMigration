# Skill: Workload Pattern — Web Application

> Workload pattern for browser-facing web applications: server-rendered pages, single-page apps with backing API, static sites, hybrid.

## When to Use

- `workload.primary_pattern: webapp` in the Capability Matrix
- Evidence: HTTP server on port 80/443, MVC/Razor/JSP/Blade/EJS templates, session state, browser-targeted assets

## Defining Characteristics

- **Client:** browser (HTML / CSS / JS)
- **Entry:** HTTP(S) request → server-rendered HTML or static SPA shell
- **State:** typically session-aware (cookies, server-side session, JWT)
- **Latency:** human-perceptible (200ms target end-to-end)
- **Throughput:** request-per-user; bursty
- **Lifecycle:** long-running web process; auto-restarted on crash

## Sub-Patterns

| Sub-pattern | Detection signal | Azure target tendency |
|-------------|------------------|----------------------|
| **Server-rendered (MVC / Razor / JSP / Blade)** | Templating files; session in middleware | App Service / Container Apps |
| **SPA + API backend** | `index.html` + JS bundle + separate API project | Static Web Apps (frontend) + App Service/Container Apps (API) |
| **Static site (no backend)** | HTML + JS only; no DB | **Static Web Apps** (best fit) |
| **JAMstack with serverless functions** | SPA + edge functions | Static Web Apps + Functions |
| **WordPress / Drupal / packaged CMS** | known CMS layout | App Service for WordPress (managed); or Container Apps |

## Probes

### Request shape

- Routes / controllers / URL patterns
- Authentication flow (form login? OIDC? cookies?)
- Session storage (in-memory? Redis? DB? cookie-based?)
- CSRF / anti-forgery tokens
- File upload handlers (max size, storage destination)

### Asset shape

- Static asset path (`/wwwroot`, `/public`, `/static`)
- CSS/JS bundling (Webpack, Vite, esbuild, MIX, MSBuild bundler)
- CDN usage today (CloudFront, Cloudflare, Akamai) → Azure Front Door / CDN

### Session + state

- Where does session live? (in-process / Redis / DB / cookie-only)
- Multi-instance friendly? (stateless required for horizontal scale)

### Database access pattern

- Per-request DB calls
- N+1 risk
- Read-heavy vs write-heavy
- Caching layer (Redis, in-memory)

### Auth pattern

- Forms / cookies → modernize to OIDC at the edge
- Hardcoded admin / dev backdoors → flag
- Multi-factor → may need replatform of MFA flow
- Federation (SAML / OIDC) → Entra ID compatible

### Public exposure

- Behind WAF? (CloudFront, AWS WAF, Cloudflare, Akamai) → Azure Front Door + WAF policy
- Custom domain + TLS cert source (Let's Encrypt, vendor cert)
- Rate limiting / DDoS protection

### File uploads

- Local disk → must move to Blob Storage (App Service local disk is ephemeral)
- S3 / GCS upload → Blob Storage with managed identity

## Phase Emphasis (per migration strategy)

| Strategy | Webapp emphasis |
|----------|----------------|
| Rehost | Phase 3 (lift IaaS), Phase 4 (cutover); session migration is the hidden risk |
| Replatform | Phase 2 (containerize / runtime upgrade), Phase 3 (App Service / Container Apps), Phase 4 |
| Refactor | Phase 2 (heavier — middleware, session, auth), Phase 3, Phase 6 |
| Rearchitect | Phase 1 (decompose), Phase 2 (rewrite chunks), Phase 3 (modern compute) |
| Rebuild | All phases as greenfield |

## Target Azure Mapping

| Webapp shape | Primary Azure target | Why |
|--------------|----------------------|-----|
| Server-rendered (any stack) | **App Service Linux** (or Windows for .NET FW) | Managed PaaS; built-in deployment slots; minimal ops |
| Containerized | **Container Apps** | Managed Kubernetes; KEDA; revisions for blue/green |
| Complex routing + many services | **AKS** | When orchestration complexity is justified |
| Static SPA + API | **Static Web Apps** (frontend) + App Service / Container Apps (API) | Best DX; managed CDN; preview environments |
| Pure static | **Static Web Apps** | Free / very cheap tier |
| WordPress | **App Service for WordPress** | Managed offering |
| Magento | **Container Apps** + Cache for Redis + AI Search | Heavy CMS; right-sized |

## Cross-Cutting Webapp Requirements (always add to plan)

- **CDN / Front Door** at the edge (esp. for static assets + WAF)
- **Custom domain + managed TLS cert** (App Service Managed Certificate or Front Door)
- **Application Insights** with browser SDK (real user monitoring)
- **Key Vault references** for connection strings / API keys in App Settings
- **VNet integration + private endpoints** when DB/Storage should not be public
- **Identity:** Entra ID for users; managed identity for service-to-service
- **Session strategy:** Redis (Azure Cache for Redis) for multi-instance session

## Anti-Patterns

- Don't deploy a session-in-memory web app to App Service with >1 instance. It will break.
- Don't store uploaded files on App Service local disk. It's ephemeral and not shared across instances.
- Don't terminate TLS at the app process — terminate at App Gateway / Front Door / App Service.
- Don't preserve cookie-domain assumptions when changing domains. Update auth cookie config.
- Don't skip the static-asset path. Hot CDN cache hits are the cheap perf win.
- Don't enable App Service "Always On" for true serverless apps — those belong on Functions / Container Apps.

## Output Checklist

- [ ] Webapp sub-pattern identified (server-rendered / SPA+API / static / CMS / etc.)
- [ ] Route + controller inventory captured
- [ ] Session strategy captured (in-memory / Redis / DB / cookie)
- [ ] Auth flow captured (Forms / OIDC / SAML / custom)
- [ ] Static asset path captured
- [ ] CDN/edge currently used captured
- [ ] File upload destination captured (and flagged for Blob if local)
- [ ] DB access pattern characterized
- [ ] Target Azure compute selected
- [ ] Edge service (Front Door / CDN) decided
- [ ] Session-on-Redis decision logged (if multi-instance)
