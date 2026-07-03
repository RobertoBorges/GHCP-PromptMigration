# Infrastructure-Pillar Slide Specifications — Reference

Slide specs and field references that apply ONLY when the Infrastructure pillar is detected. Loaded by the `migration-strategy-report` skill conditionally.

---

## Infrastructure Input Fields

*For RVTools, Azure Migrate, vCenter, SCCM data.*

| Field | Description | Example |
|-------|-------------|--------|
| VM/Server Name | Hostname or VM name | SQLPROD-01, WEB-FRONT-03 |
| Physical vs Virtual | Whether physical or VM | Virtual (VMware) |
| Hypervisor | Virtualization platform | VMware ESXi 7.0, Hyper-V 2019, KVM |
| CPU (vCPU) | Allocated CPU cores | 8 vCPU |
| RAM (GB) | Allocated memory | 32 GB |
| Disk (GB) | Provisioned storage | 500 GB |
| CPU Utilization % | Average/peak CPU usage | Avg 35%, Peak 72% |
| RAM Utilization % | Average/peak memory usage | Avg 60%, Peak 88% |
| Operating System | OS name and version | Windows Server 2016, RHEL 8.6, Ubuntu 22.04 |
| IP Address / VLAN | Network assignment | 10.1.5.22 / VLAN 150 |
| Datacenter / Cluster | Physical location or vSphere cluster | DC-East / Cluster-Prod-01 |
| Workload Type | Role of the server | SQL Server, Web Server, File Server, Domain Controller, App Server |
| Powered On | Whether VM is active | Yes / No |
| Snapshot Count | Number of snapshots (VMware) | 3 |
| Last Boot Time | Last restart date | 2025-11-15 |
| Owner / BU | Responsible team | Infrastructure Team, Finance |
| Environment | Prod / Dev / Test / DR | Production |
| Migration Phase | Assigned wave (if pre-assigned) | Wave 2 |

---

## Network / Storage / Identity Input Fields

*For landing zone and dependency planning.*

| Field | Description | Example |
|-------|-------------|--------|
| Subnet / VLAN | Network segmentation | 10.1.5.0/24 - Prod-DB |
| Firewall Rules Count | Inbound/outbound rules | 47 rules |
| Load Balancer | LB type and VIPs | F5 BIG-IP, 3 VIPs |
| DNS Zones | Internal/external zones | corp.internal, app.customer.com |
| ExpressRoute / VPN | WAN connectivity | 1 Gbps ExpressRoute to Azure East US |
| Storage Type | SAN/NAS/DAS/local | NetApp FAS, Pure Storage, local SSD |
| Storage IOPS | Performance requirements | 5000 IOPS sustained |
| Backup Solution | Current backup platform | Veeam, Commvault, NetBackup |
| AD Forest / Domain | Directory structure | corp.local, 3 child domains |
| Domain Controller Count | DC inventory | 8 DCs across 3 sites |
| ADFS / Federation | Identity federation | ADFS 4.0, 5 relying parties |
| Certificate Authority | PKI infrastructure | Internal CA, 2-tier hierarchy |

---

## Slide 4b (Infra Portion): EOS Impact & ESU Strategy — Infrastructure

### Slide 4b: End-of-Support (EOS) Impact & ESU Strategy (WHEN EOL DATA EXISTS)

This is a **dedicated slide** whenever EOS/EOL data is present (OS versions, DB versions, middleware versions with dates). It is distinct from the Obsolescence Assessment slide — that slide scores technical debt breadth; this one focuses on **security exposure timeline, mitigation options, and cost implications**.

**Always include when:** RVTools data, Azure Migrate assessments, or any VM/server inventory shows OS/DB versions with known EOS dates.

**Content structure:**
- 4 KPI cards: Total EOS VMs/servers, ESU-eligible count, no-mitigation count, supported count
- **Timeline table:** Platform | EOS Date | Count | Months Unsupported (calculated from current date) | CVE Risk Badge
- **Azure Arc ESU section:** How Factory delivers ESU in ~15 days, enrollment windows, back-charge billing model
- **Three-tier action cards:**
  - **Red (No mitigation available):** Platforms past ESU window (WS2008, Win7, WS2003, CentOS) — must migrate/retire immediately
  - **Orange (ESU bridge available — act now):** Platforms with active ESU window (WS2012/R2, SQL 2014) — deploy Arc ESU as bridge
  - **Green (Supported — migrate on schedule):** Platforms in mainstream/extended support — no urgency
- **SQL Server discovery gap callout** if SQL version data is missing
- **Executive summary callout** with total no-mitigation VMs, ESU-eligible VMs, and recommended immediate action

**Azure OS Endorsement Exceptions sub-section (WHEN RVTools/vCenter DATA EXISTS):**

This is a **sub-section within the EOS slide** — distinct from the EOS timeline above. EOS asks "is this OS still patched by the vendor?" while OS Endorsement asks "will Azure support this OS after migration?" A VM can be current on vendor support but still not Azure-endorsed (e.g., VMware Photon OS, appliance OS).

**Always include when:** RVTools, vCenter, or Azure Migrate data contains guest OS strings. Scan every guest OS value against Microsoft's endorsed lists:
- [Endorsed Linux distributions on Azure](https://learn.microsoft.com/azure/virtual-machines/linux/endorsed-distros)
- [Microsoft server software support for Azure VMs](https://learn.microsoft.com/troubleshoot/azure/virtual-machines/server-software-support)

**Classification algorithm:**
1. **Known-unsupported** — OS explicitly NOT on Azure endorsed list: VMware Photon OS, ESXi, Solaris, AIX, HP-UX, FreeBSD (unless Microsoft-published FreeBSD 13 image), Windows 8/8.1 (desktop OS), Windows Server 2003, Acano OS, custom appliance OS
2. **Generic / non-endorsed Linux** — vSphere reports generic kernel strings like "Other 2.6.x Linux", "Other 3.x Linux", "Other 4.x or later Linux" — cannot map to an endorsed distro. Need manual identification via `/etc/os-release`
3. **Unidentified** — blank, "unknown", or "other" guest OS field — need Azure Migrate appliance discovery or manual login to identify

**Content structure for this sub-section:**
- **Section title:** "Azure OS Endorsement Exceptions"
- **3 KPI cards (inline):** Known-unsupported count | Generic/non-endorsed count | Unidentified count
- **Callout:** Total exceptions, % of estate, estimated monthly Azure cost at risk
- **Top OS strings bar chart** (if space allows) — top 5-8 non-endorsed OS strings by count
- **Remediation guidance per class:**
  - Known-unsupported → rebuild on endorsed OS, consider Azure VMware Solution for VMware appliances, or retain on-prem
  - Generic/non-endorsed → identify actual distro via `cat /etc/os-release`, rebuild if needed
  - Unidentified → run Azure Migrate appliance with agent-based discovery, or manual `systeminfo`/`/etc/os-release`
- **Link to detailed OS Exceptions Report** if a separate per-VM report has been generated

**Note:** Many unidentified/generic VMs will be templates, powered-off appliances, or duplicates. Filter to powered-on VMs only when computing the count. VMware Photon OS VMs are typically vCenter/vRealize appliances — confirm whether they are in-scope for migration or should be excluded (they usually are NOT migrated since Azure replaces vSphere management).

**Key EOS dates to reference (as of 2025):**
- Windows Server 2003: Jul 2015 (no ESU)
- Windows Server 2008/R2: Jan 2020 (ESU expired Jan 2023)
- Windows 7: Jan 2020 (ESU expired Jan 2023)
- Windows Server 2012/R2: Oct 2023 (ESU via Azure Arc until Oct 2026)
- SQL Server 2012: Jul 2022 (ESU expired Jul 2025)
- SQL Server 2014: Jul 2024 (ESU via Azure Arc until Jul 2027)
- CentOS 6: Nov 2020 (no ESU equivalent)
- ESXi 6.7: Oct 2023 (no ESU — upgrade or migrate)

---

## Slide 4c: Infrastructure Discovery & Sizing

### Slide 4c: Infrastructure Discovery & Sizing (WHEN INFRASTRUCTURE DATA EXISTS)

This is a **conditional slide** — include when VM/server inventory data is detected (RVTools, Azure Migrate, vCenter exports, SCCM, Movere, or any server inventory spreadsheet). This slide does NOT exist in app-only reports. For infra-only migrations, this becomes one of the primary slides.

**Data sources that trigger this slide:**
- RVTools export (vInfo, vCPU, vMemory, vDisk, vNetwork tabs)
- Azure Migrate appliance data
- vCenter / SCCM / Movere / MAP Toolkit exports
- Any spreadsheet with VM/server names + CPU/RAM/disk columns
- Manual server inventory lists

**Content structure:**
- **4 KPI cards:** Total Servers/VMs, Physical vs Virtual split, Powered-On vs Powered-Off, Total Compute (aggregate vCPU & RAM)
- **Environment Breakdown:** Prod | Dev/Test | DR | Unknown — count and % per environment
- **Compute Summary Table:**
  | Metric | Current On-Prem | Azure Right-Sized (est.) | Savings Opportunity |
  |--------|----------------|-------------------------|---------------------|
  | Total vCPU | sum | estimated (70-80% of current if utilization data shows overprovisioning) | % reduction |
  | Total RAM (TB) | sum | estimated | % reduction |
  | Total Disk (TB) | sum | estimated | % reduction |
  | VM Count | total powered-on | after retire/consolidate candidates removed | reduction count |
- **Hypervisor Landscape:** Pie/donut chart — VMware ESXi (by version) vs Hyper-V vs KVM vs Physical vs Other
  - Flag unsupported hypervisor versions (ESXi 6.x, Hyper-V 2012)
  - VMware workloads → highlight AVS migration path
- **OS Distribution:** Bar chart — Windows Server (by version) | RHEL | Ubuntu | CentOS | SLES | Other Linux | Other
  - Color-code by support status (supported / ESU-eligible / unsupported)
- **Workload Type Classification:** Bar chart or table — what the servers actually do
  | Workload Type | Count | % | Migration Path |
  |--------------|-------|---|----------------|
  | SQL Server | n | % | Azure SQL MI/DB/VM via DMS |
  | Web Server (IIS/Apache/Nginx) | n | % | App Service / Container Apps |
  | Application Server | n | % | Azure VM / App Service |
  | File Server | n | % | Azure Files / NetApp Files |
  | Domain Controller | n | % | Azure AD DS / ISD / Partner scope |
  | Print Server | n | % | Azure Universal Print / Retire |
  | Citrix / RDS | n | % | AVD migration |
  | Monitoring / Management | n | % | Azure Monitor / Retire |
  | Other / Unknown | n | % | Assessment needed |
- **Right-Sizing Opportunity (when utilization data exists):**
  - Count of VMs with <10% avg CPU utilization (shutdown candidates)
  - Count of VMs with <20% avg CPU AND <30% RAM (downsize candidates)
  - Count of VMs not powered on for 30+ days (retire candidates)
  - Estimated % cost avoidance from right-sizing before migration
- **Datacenter / Location Summary:** Table of physical sites or vSphere clusters with VM counts — drives Azure region selection and migration wave grouping
- **Snapshot Hygiene (VMware):** Count of VMs with snapshots, total snapshot disk consumption — must be cleaned pre-migration

**Key Principle:** This slide answers: *"What does the server estate look like, what's the cloud landing footprint, and where are the quick wins (retire, right-size, consolidate)?"*

---

## Slide 4d: Network & Landing Zone Readiness

### Slide 4d: Network & Landing Zone Readiness (WHEN NETWORK/IDENTITY DATA EXISTS)

This is a **conditional slide** — include when network topology, firewall rules, VPN/ExpressRoute, DNS, or Active Directory data is present. For pure app-centric reports with no infra data, skip entirely.

**Content structure:**
- **4 KPI cards:** Total VLANs/Subnets, Firewall Rule Count, ExpressRoute/VPN Circuits, Domain Controller Count
- **Network Topology Summary:**
  | Network Segment | VLAN/Subnet | Purpose | VM Count | Azure VNet Mapping |
  |----------------|-------------|---------|----------|-------------------|
  - Map on-prem segments to proposed Azure VNet/Subnet design
  - Flag segments requiring NSG rule migration
- **Connectivity Architecture:**
  - ExpressRoute / Site-to-Site VPN / Point-to-Site — existing circuits, bandwidth, latency requirements
  - Proposed Azure connectivity (ExpressRoute to Azure region X, backup VPN)
  - Internet egress path changes
- **Identity & Access:**
  - AD Forest structure (forests, domains, trusts, child domains)
  - Domain Controller locations and count
  - ADFS / Federation services → Entra ID migration path
  - Certificate Authority / PKI → Azure Key Vault / Entra Certificate-Based Auth
  - GPO count and complexity → Intune / Azure Policy mapping
- **DNS & Load Balancing:**
  - Internal DNS zones and record counts
  - External DNS zones and registrar info
  - Load balancer inventory (F5, NetScaler, HAProxy, NLB) → Azure Load Balancer / Application Gateway / Front Door
- **Landing Zone Readiness Checklist:**
  | Requirement | Status | Notes |
  |------------|--------|-------|
  | Azure Landing Zone (ALZ) deployed | Yes/No/Partial | Hub-spoke / VWAN |
  | ExpressRoute / VPN configured | Yes/No/In progress | Circuit ID, bandwidth |
  | Azure AD Connect / Entra Connect Sync | Yes/No/Planned | Sync scope |
  | Azure Backup configured | Yes/No/Planned | Vault regions |
  | Azure Monitor / Log Analytics | Yes/No/Planned | Workspace setup |
  | Defender for Cloud enabled | Yes/No/Planned | Plans selected |
  | Azure Policy baseline applied | Yes/No/Planned | Regulatory compliance |

**Key Principle:** This slide answers: *"Is the Azure landing zone ready to receive workloads, and what networking/identity work must happen before migration waves start?"*
