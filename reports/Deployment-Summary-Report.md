# Deployment Summary Report — PartsUnlimited

**Status:** ⏳ Ready to deploy (commands prepared, user-executed)
**Target environment:** `partsunlimited-dev` in `westeurope`
**Subscription:** Azure Migrate Demo Subscription (`6785ea1f-ac40-4244-a9ce-94b12fd832ca`)
**Deployer:** roborges@microsoft.com (`9b4d5892-2a08-4ff7-992b-b5318e37e64f`)

---

## 1. Pre-flight Verification

| Check | Result |
|---|---|
| `azd` installed | ✅ 1.23.13 (upgrade to 1.25.2 optional) |
| `az` installed | ✅ 2.80.0 |
| Azure login | ✅ `roborges@microsoft.com` |
| Subscription selected | ✅ Azure Migrate Demo Subscription |
| Phase 2 build | ✅ `dotnet build` — 0 errors |
| Phase 3 Bicep | ✅ `az bicep build` — 0 errors |
| azd environment | ✅ `partsunlimited-dev` created (`.azure/partsunlimited-dev/`) |
| Required env values | ✅ AZURE_LOCATION, AZURE_PRINCIPAL_ID, AZURE_PRINCIPAL_NAME, SQL_ADMIN_LOGIN |
| Docker (for build) | ⚠️ Required for `azd up`. Verify with `docker info`. |

---

## 2. Deployment Commands

Run these from `c:\git\GHCP-PromptMigration\PartsUnlimited-Migrated\`:

```pwsh
# (optional) verify Docker is running
docker info | Select-String -Pattern '^Server Version|^OSType'

# Provision infrastructure + build container + push to ACR + deploy to Container Apps
azd up

# OR run the two phases separately:
azd provision   # creates RG, ACR, ACA Env, SQL, Key Vault, App Insights, MI
azd deploy web  # builds Dockerfile, pushes to ACR, updates Container App revision
```

`azd up` will:

1. Create resource group `rg-partsunlimited-dev` in `westeurope`.
2. Deploy `infra/main.bicep` — Container Apps Env, Container App, ACR, Azure SQL Server + Serverless DB, Key Vault, Managed Identity, Log Analytics, App Insights, plus RBAC role assignments.
3. Build the .NET 10 container from `src/PartsUnlimited.Web/Dockerfile`, push to ACR.
4. Update the Container App revision to use the newly built image.
5. Print the deployment URL (`SERVICE_WEB_URI`).

---

## 3. Resource Inventory (as defined in Bicep)

| Resource | Name pattern | Notes |
|---|---|---|
| Resource Group | `rg-partsunlimited-dev` | All resources scoped here |
| User-Assigned Managed Identity | `id-<token>` | Used for ACR pull, Key Vault, SQL AAD auth |
| Container Registry | `acr<token>` | Basic SKU, admin disabled, anon pull disabled |
| Container Apps Environment | `cae-<token>` | Logs → Log Analytics |
| Container App | `ca-<token>` | Ingress port 8080 external HTTPS, 1-3 replicas, HTTP scaler |
| Azure SQL Server | `sql-<token>` | Entra ID admin set to deployer; min TLS 1.2 |
| Azure SQL Database | `partsunlimited` | Serverless GP_S_Gen5_2, 0.5 vCore min, auto-pause 60 min |
| Key Vault | `kv-<token>` | RBAC-only, soft-delete + purge protection |
| Log Analytics | `log-<token>` | 30-day retention, PerGB2018 |
| Application Insights | `appi-<token>` | Workspace-based |

`<token>` = `uniqueString(subscription.id, resourceGroup.id, environmentName)` — deterministic 13-char hash.

---

## 4. Security Configuration

- **Identity-first auth**: Managed Identity used for ACR pull (AcrPull role), Key Vault access (Key Vault Secrets User), Application Insights publishing (Monitoring Metrics Publisher), and Azure SQL access (`Authentication=Active Directory Default` in connection string — no SQL passwords used at runtime).
- **SQL admin password**: Auto-generated `newGuid()` in Bicep; kept only in deployment outputs, not surfaced to runtime. Entra ID admin (the deployer or designated group) is the primary admin path.
- **Key Vault**: RBAC-only authorization, soft-delete enabled, purge protection enabled. No access policies.
- **Container Apps ingress**: External HTTPS only (`allowInsecure: false`). TLS terminated at the platform edge.
- **ACR**: Admin user disabled, anonymous pull disabled. Pulls authenticated via Managed Identity.
- **SQL Server**: Min TLS 1.2. Firewall rule `AllowAllWindowsAzureIps` (`0.0.0.0`) enables Azure-internal access for Container Apps.

### Open security items (recommended for production)

- Replace the broad `AllowAllWindowsAzureIps` SQL firewall rule with private endpoints + VNet integration on Container Apps.
- Add VNet integration to Container Apps Environment for east-west traffic isolation.
- Move SQL admin password into Key Vault (currently in deployment parameters only).
- Add Azure DDoS Network Protection if exposed to public internet.

---

## 5. Monitoring & Observability

- **Application Insights**: Connection string injected into the container as `ApplicationInsights__ConnectionString`. Server-side telemetry via `Microsoft.ApplicationInsights.AspNetCore 2.23.0`.
- **Log Analytics**: Container `stdout`/`stderr` streamed via Container Apps log destination. 30-day retention.
- **Health probes**: Liveness + Readiness HTTP probes against `/` on port 8080.

Useful KQL queries (run in Log Analytics or App Insights):

```kusto
// Recent container logs
ContainerAppConsoleLogs_CL
| where TimeGenerated > ago(1h)
| where ContainerAppName_s startswith "ca-"
| project TimeGenerated, Log_s
| order by TimeGenerated desc

// Application errors
exceptions
| where timestamp > ago(1h)
| project timestamp, type, outerMessage, operation_Name
| order by timestamp desc

// Request latency P95
requests
| where timestamp > ago(1h)
| summarize p95=percentile(duration, 95) by bin(timestamp, 5m), name
| render timechart
```

---

## 6. Post-Deployment Verification

```pwsh
# Get the deployed URL
azd env get-values | Select-String SERVICE_WEB_URI

# Tail container logs
azd monitor --logs

# Or with az
az containerapp logs show --name ca-<token> --resource-group rg-partsunlimited-dev --follow

# Smoke test
$url = (azd env get-values | Select-String 'SERVICE_WEB_URI=' | ForEach-Object { ($_ -split '=',2)[1].Trim('"') })
Invoke-WebRequest $url -UseBasicParsing | Select-Object StatusCode, StatusDescription
```

### Functional checklist (manual)

- [ ] Home page loads (top-selling + new products visible)
- [ ] Category browse works (`/Store/Browse?category=Brakes`)
- [ ] Product details page loads with image + spec table
- [ ] Add-to-cart works for an anonymous user
- [ ] Search box returns results for plural and singular queries
- [ ] Register a new user via Identity Razor Pages
- [ ] Login + checkout with promo code `FREE`
- [ ] Order shows up in `/Orders` for the logged-in user
- [ ] Application Insights `Live Metrics` shows incoming requests

---

## 7. Performance Baseline

Capture once deployment is live (record in this file):

| Metric | Target | Measured | Notes |
|---|---|---|---|
| Cold start (first request after scale-to-zero) | < 8s | _TBD_ | Min replicas = 1 by default, so cold start only at first deploy |
| Steady-state response time (home page) | < 500ms P95 | _TBD_ | |
| SQL connection establishment | < 1s | _TBD_ | First connection after auto-pause may take 30-60s |
| Concurrent users at 1 replica | ~50 | _TBD_ | HTTP scaler triggers at 50 concurrent requests |

Quick load test with [autocannon](https://github.com/mcollina/autocannon) or `hey`:

```pwsh
# 30 sec, 10 concurrent connections
hey -z 30s -c 10 $url
```

---

## 8. Cost Estimate (steady-state, no traffic)

| Resource | Monthly est. | Notes |
|---|---|---|
| Container Apps (1 replica, 0.5 vCPU, 1 GiB) | ~$15 | Consumption plan; scales to 0 if `minReplicas=0` |
| Azure SQL Serverless (0.5 vCore min, auto-pause) | ~$5-10 | Near-zero when idle; pays only for storage |
| ACR Basic | ~$5 | |
| Key Vault | ~$0.03 | Per 10k ops |
| Log Analytics (PerGB2018) | ~$2-5 | First 5 GB/month free |
| Application Insights | $0 | Workspace-based, billed via Log Analytics |
| Managed Identity | $0 | Free |
| **Total** | **~$25-35/month** | Idle |

### Cost optimization recommendations

- Set `minReplicas: 0` on Container App for dev environments (accepts cold start in exchange for true scale-to-zero).
- Lower Log Analytics daily cap (`dailyQuotaGb`) on dev workspaces.
- Use Azure SQL Free Offer (where available) for dev/test, or migrate to a Basic-tier dedicated DB if usage is predictable.
- Set Cost Management budget + alert at $50/month/RG.

---

## 9. Troubleshooting

| Symptom | Investigation |
|---|---|
| `azd provision` fails on RBAC | Confirm deployer has `Owner` or `User Access Administrator` on the subscription/RG. Role assignments in Bicep require write access to `Microsoft.Authorization/roleAssignments`. |
| `azd deploy` fails on `docker push` | Verify Docker daemon running (`docker info`). Re-run `az acr login --name <acr>`. |
| Container App stuck in `Activating` | `az containerapp revision list -n <app> -g <rg> -o table` and `az containerapp logs show ...` for image-pull or startup errors. |
| App returns 500 on first DB access | Confirm SQL firewall allows Azure services and Managed Identity has been granted a DB user. See §10. |
| App Insights shows no telemetry | Confirm `ApplicationInsights__ConnectionString` env var is set on the container (`az containerapp show ... --query properties.template.containers[0].env`). |

Diagnostic commands:

```pwsh
az containerapp show -n ca-<token> -g rg-partsunlimited-dev --query properties.provisioningState
az containerapp revision list -n ca-<token> -g rg-partsunlimited-dev -o table
az containerapp logs show -n ca-<token> -g rg-partsunlimited-dev --tail 100
az monitor activity-log list --resource-group rg-partsunlimited-dev --max-events 20 -o table
```

---

## 10. Required Post-Deploy Database Step ⚠️

The Container App authenticates to SQL as its **Managed Identity**, but Azure SQL requires that identity to be **created as a contained database user** before queries succeed.

Run **once**, signed in as the SQL Entra admin (the deployer):

```pwsh
# Replace with values from `azd env get-values`
$server = "<AZURE_SQL_SERVER_FQDN>"
$db     = "partsunlimited"
$mi     = "<AZURE_MANAGED_IDENTITY_NAME>"   # e.g. id-abc123

sqlcmd -S $server -d $db -G -Q @"
CREATE USER [$mi] FROM EXTERNAL PROVIDER;
ALTER ROLE db_datareader ADD MEMBER [$mi];
ALTER ROLE db_datawriter ADD MEMBER [$mi];
ALTER ROLE db_ddladmin   ADD MEMBER [$mi];
"@
```

Alternative: replace the demo `db.Database.EnsureCreated()` pattern with EF Core migrations + an `azd hooks postdeploy` action that runs `dotnet ef database update`.

---

## 11. Operational Procedures

- **Scale up replicas**: `az containerapp update -n ca-<token> -g rg-partsunlimited-dev --min-replicas 2 --max-replicas 10`
- **Roll back to previous revision**: `az containerapp revision activate -n ca-<token> -g rg-partsunlimited-dev --revision <previous>`
- **Drain & redeploy**: `azd deploy web` (creates a new revision; old one drains automatically)
- **Tear down environment**: `azd down --purge --force` (purges Key Vault soft-deleted resources)

---

## 12. Next Steps

- Run `azd up` to provision and deploy. Record actual outputs (URLs, resource names) back into §3 and §7 above.
- Run the SQL `CREATE USER ... FROM EXTERNAL PROVIDER` step (§10).
- Verify the functional checklist (§6).
- Run **`/Phase5-SetupCICD`** to configure GitHub Actions (or Azure DevOps) for automated deployment.
