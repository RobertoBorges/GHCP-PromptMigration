# Skill: Source Adapter — On-Premise (Windows / Linux)

> Characterizes an application running on a customer-owned Windows or Linux server (physical or virtual), not in a hyperscaler.

## When to Use

- User says "it runs on a server in our data center"
- User has IIS, Windows Service, systemd unit, cron job, scheduled task, or a packaged installation as the runtime
- No public cloud is the source (AWS/GCP/Azure adapters take precedence if applicable)

## Inputs

- Hostnames or IPs (or "describe-only" if no access)
- Access method: SSH, WinRM, RDP, "user-provided artifacts only"
- Optional: configuration export, IIS metabase export, `systemd` units, Windows registry export

## Probes (apply what's accessible)

### Windows Server

1. **OS + runtime baseline**
   - `Get-ComputerInfo | Select-Object WindowsVersion, OsBuildNumber` → Windows version (Server 2008 / 2012 / 2016 / 2019 / 2022)
   - `Get-WindowsFeature | Where-Object Installed` → installed roles (IIS, .NET, AD, etc.)
   - `Get-Hotfix | Select-Object -Last 5` → patch cadence

2. **IIS-hosted apps**
   - `Get-Website` (PowerShell `WebAdministration` module) → site list, bindings, app pools
   - For each app pool: `Get-ItemProperty IIS:\AppPools\<name>` → `managedRuntimeVersion` (e.g., `v4.0`, `v2.0`), `enable32BitAppOnWin64`
   - Locate physical paths; tag each as `.NET Framework` / `Classic ASP` / static
   - Look for `web.config`, `global.asax`, `*.asp`, `bin/`

3. **Windows Services**
   - `Get-Service | Where-Object {$_.Status -eq 'Running'} | Select-Object Name, DisplayName, StartType`
   - `Get-CimInstance Win32_Service | Select-Object Name, PathName, StartName` → executable path + service account
   - Flag services running as `LocalSystem` for security review

4. **Scheduled Tasks**
   - `Get-ScheduledTask | Where-Object {$_.State -ne 'Disabled'}` → batch jobs
   - Captures `workload-batch-job` candidates

5. **Installed software**
   - `Get-WmiObject -Class Win32_Product` (slow; use registry alternative when possible)
   - Identifies vendor packages (Oracle Client, SQL Server, MQ Series, etc.)

6. **Network exposure**
   - `Get-NetTCPConnection -State Listen` → listening ports
   - Maps to inbound integrations

### Linux Server

1. **OS + runtime baseline**
   - `cat /etc/os-release` → distro + version (RHEL, CentOS, Ubuntu, SUSE, Amazon Linux, Debian)
   - `uname -a` → kernel
   - `uptime` → liveness signal

2. **Web/app server**
   - `systemctl list-units --type=service --state=running` → active services
   - Check for: `httpd`, `nginx`, `tomcat`, `jboss`, `weblogic`, `node`, `gunicorn`, `unicorn`, `php-fpm`
   - For each: config file paths (`/etc/nginx/`, `/etc/httpd/`, `/opt/tomcat/conf/`)

3. **Application processes**
   - `ps -ef | grep -v '^root'` → running app processes
   - `ss -tlnp` (or `netstat -tlnp`) → listening ports + binding processes
   - `lsof -p <pid>` → open files (helps find config + log paths)

4. **Cron / scheduled jobs**
   - `crontab -l` (per user) + `/etc/cron.*/`, `/etc/cron.d/`
   - `systemctl list-timers` → systemd timers

5. **Installed packages**
   - `rpm -qa` or `dpkg -l` → installed packages
   - Identify vendor software (Oracle, IBM MQ, SAP agents, etc.)

6. **File-system layout**
   - `/opt/<app>/`, `/var/www/`, `/srv/`, `/usr/local/<app>/` → app install locations
   - Capture source paths for `stack-detection`

## Output Evidence

```yaml
source:
  primary_adapter: source-on-premise
  access_method: <ssh | winrm | rdp | describe-only>
  evidence_confidence: <high if direct access; medium if exports only; low if describe-only>
  evidence_paths:
    - <host:port or describe-only>
    - <key paths captured>
  notes: |
    - OS: <Windows Server 2016 | RHEL 8 | Ubuntu 20.04 | ...>
    - Web/app server: <IIS 10 | Apache 2.4 | nginx 1.18 | Tomcat 9 | ...>
    - Service account: <LocalSystem | named svc account | non-root user>
    - Installed vendor packages: <list>
    - Listening ports: <list>
    - Scheduled jobs detected: <count>
    - Source code on disk: <yes/no — paths>
```

## Migration Constraints / Risks

- **Source-only-on-disk.** If source lives only on the server (no Git), getting a clean snapshot is part of Phase 1. Document this and assign to Coder + Architect.
- **Vendor software dependencies.** Oracle Client, IBM MQ, SAP agents, ODBC DSNs, COM components — each may be a blocking constraint or require a vendor-supported Azure SKU.
- **Service-account permissions.** Apps running as LocalSystem or root → flagged `regulated-data` or `over-privileged`.
- **Local-only state.** Local file shares, file-based databases (SQLite, Access, JET), local registry hives → must move to durable Azure storage.
- **Hardcoded hostnames/IPs.** Grep configs for the server's own hostname, IP, drive letters. Each must be parameterized.
- **License keys on disk.** Oracle, SQL Server, Office automation — note for Cost Engineer.
- **No backup/DR shape.** Document current RPO/RTO assumptions; will inform Phase 4 cutover plan.

## Target Azure Mapping (initial signals only — Architect decides)

| Today on-prem | Azure candidate (signals) |
|--------------|---------------------------|
| IIS-hosted ASP.NET | App Service (Windows) or Container Apps (containerize) |
| IIS-hosted Classic ASP | Container Apps with Windows base image; or rewrite |
| Windows Service | Container Apps Jobs or Functions or Web Job |
| systemd long-running daemon | Container Apps with `replicas≥1` |
| cron job | Container Apps Jobs or Logic Apps |
| Tomcat / JBoss / WebLogic | Azure Spring Apps, Container Apps, or AKS |
| nginx + PHP-FPM | App Service Linux or Container Apps |
| Generic packaged vendor app | Rehost to Azure VM (often the right answer) |

## Anti-Patterns

- Don't run `Win32_Product` if there are many machines — it's slow. Use registry uninstall keys.
- Don't assume the running process is the only deployment artifact — check for inactive services, archive directories, swap directories.
- Don't infer the application by the service name — read the executable path and walk up to find the install root.
- Don't ignore Windows scheduled tasks. They are often the silent batch tier of "the web app."

## Output Checklist

- [ ] OS + version captured
- [ ] Web/app server identified + version
- [ ] All running services + executable paths inventoried
- [ ] Service accounts + privilege noted
- [ ] Scheduled tasks / cron / timers captured
- [ ] Installed vendor packages listed
- [ ] Listening ports + integrations mapped
- [ ] Source-code location on disk identified (or marked missing)
- [ ] Hardcoded hostname/IP grep completed
- [ ] License-bearing software flagged for Cost Engineer
