# Ocean's Twelve — The Azure Heist 🎰💎

> Fifteen specialists. Any source. Any stack. One mission: migrate everything to Azure.

> **Universal-mode update (2026-06-01):** The squad is no longer pinned to seven specific use-cases or to .NET/Java alone. A new **Discovery Engineer (Saul Bloom Jr.)** owns intake, source/stack/workload classification, and the migration strategy recommendation. The team can now assess and migrate applications from **on-premise, AWS, GCP, Oracle, VMware, Kubernetes, container registries, GitHub repos, ZIPs, and mainframes** across **.NET, Java, Python, Node.js, PHP, Ruby, Go, Perl, Rust, COBOL, Oracle Forms, PowerBuilder, Delphi/VB6, Scala/Kotlin, and C++ Windows** stacks. The seven legacy use-cases below remain useful as **reference examples**, not as a fixed catalog.

## Coordinator

| Name | Role | Notes |
|------|------|-------|
| Danny Ocean | Coordinator | Routes work, enforces handoffs and reviewer gates. Does not generate domain artifacts. |

## The Crew

### Core Team (Original 3)

| # | Name | Alias | Role | Charter | Status |
|---|------|-------|------|---------|--------|
| 1 | Architect | Danny Ocean | Lead / Architect — the mastermind | `.squad/agents/architect/charter.md` | ✅ Active |
| 2 | Coder | Rusty Ryan | Full-Stack Dev — gets it done, no drama | `.squad/agents/coder/charter.md` | ✅ Active |
| 3 | Tester | Linus Caldwell | Tester + DevRel — verifies everything | `.squad/agents/tester/charter.md` | ✅ Active |

### Azure & Infrastructure Specialists

| # | Name | Alias | Role | Charter | Status |
|---|------|-------|------|---------|--------|
| 4 | Azure Specialist | Basher Tarr | Azure Platform Architect — the explosives expert | `.squad/agents/azure-specialist/charter.md` | ✅ Active |
| 5 | DevOps Engineer | Turk Malloy | CI/CD & Pipeline Lead — builds the getaway route | `.squad/agents/devops-engineer/charter.md` | ✅ Active |
| 6 | Observability Engineer | Livingston Dell | Monitoring & Ops — eyes on every screen | `.squad/agents/observability-engineer/charter.md` | ✅ Active |

### Data & Performance

| # | Name | Alias | Role | Charter | Status |
|---|------|-------|------|---------|--------|
| 7 | Database Specialist | The Amazing Yen | Data Migration Lead — precision in tight spaces | `.squad/agents/database-specialist/charter.md` | ✅ Active |
| 8 | Performance Engineer | Virgil Malloy | Perf & Scale — drives fast, benchmarks everything | `.squad/agents/performance-engineer/charter.md` | ✅ Active |

### Security & Quality

| # | Name | Alias | Role | Charter | Status |
|---|------|-------|------|---------|--------|
| 9 | Security Auditor | Frank Catton | Security Review Lead — finds every vulnerability | `.squad/agents/security-auditor/charter.md` | ✅ Active |
| 10 | Evaluator | Saul Bloom | Prompt Quality Engineer — spots fakes | `.squad/agents/evaluator/charter.md` | ✅ Active |

### Release & Documentation

| # | Name | Alias | Role | Charter | Status |
|---|------|-------|------|---------|--------|
| 11 | Cutover Commander | Reuben Tishkoff | Release & Go-Live Lead — the closer | `.squad/agents/cutover-commander/charter.md` | ✅ Active |
| 12 | Scribe | Roman Nagel | Session Logger — documents the whole heist | `.squad/agents/scribe/charter.md` | ✅ Active |

### Visual Communication

| # | Name | Alias | Role | Charter | Status |
|---|------|-------|------|---------|--------|
| 13 | Presentation Specialist | Tess Ocean | PPTX & Visual Storytelling — sells the story | `.squad/agents/presentation-specialist/charter.md` | ✅ Active |

### Cost & FinOps

| # | Name | Alias | Role | Charter | Status |
|---|------|-------|------|---------|--------|
| 14 | Cost Engineer | The Accountant | Cost Engineer — every dollar has a destination | `.squad/agents/cost-engineer/charter.md` | ✅ Active |

### Discovery & Intake (universal entry point)

| # | Name | Alias | Role | Charter | Status |
|---|------|-------|------|---------|--------|
| 15 | Discovery Engineer | Saul Bloom Jr. | Intake & Classification Lead — characterizes any application before the heist begins | `.squad/agents/discovery-engineer/charter.md` | ✅ Active |

## Coding Agent

<!-- copilot-auto-assign: false -->

| Name | Role | Charter | Status |
|------|------|---------|--------|
| @copilot | Coding Agent | — | 🤖 Coding Agent |

### Capabilities

**🟢 Good fit — auto-route when enabled:**
- Bug fixes with clear reproduction steps
- Documentation fixes and README updates
- Prompt and skill file edits with clear specs
- Adding or updating agent charters from templates
- Small isolated configuration changes (Bicep parameters, appsettings, YAML)
- Boilerplate/scaffolding generation for new use-cases
- Routing and hook document updates

**🟡 Needs review — route to @copilot but flag for squad member PR review:**
- New prompt or chatmode authoring (needs Evaluator review)
- Migration code changes across multiple files
- Infrastructure-as-Code generation (Bicep/Terraform)
- CI/CD pipeline modifications
- Security-related configuration changes
- New skill file creation

**🔴 Not a fit — comment on issue suggesting reassignment:**
- Live Azure resource provisioning or modification
- Database migration execution (schema changes, data movement)
- Production deployment or cutover operations
- Cost optimization requiring Azure portal analysis
- Security audit requiring vulnerability scanning tools
- Performance testing requiring load generation

## The Targets 🎯

The squad migrates **any** application to Azure. Discovery is the universal entry point.

### Universal Targeting (default)

| What we accept | How discovery handles it |
|----------------|--------------------------|
| Source code in a Git repo | `source-github-repo` adapter + stack detection |
| Code in a local filesystem or ZIP | `source-zip-filesystem` adapter |
| On-premise Windows/Linux server | `source-on-premise` adapter (inventory + extraction plan) |
| AWS workload (EC2, ECS, Lambda, RDS, S3) | `source-aws` adapter |
| GCP workload (Compute, GKE, Cloud Run, Cloud SQL) | `source-gcp` adapter |
| Oracle Database / Forms / WebLogic | `source-oracle-db` + `stack-oracle-forms` |
| VMware estate (RVTools export) | `source-vmware-rvtools` adapter |
| Mainframe (z/OS, COBOL, CICS, JCL) | `source-mainframe` + `stack-cobol-mainframe` |
| Kubernetes cluster | `source-kubernetes-cluster` adapter |
| Container registry image(s) | `source-container-registry` adapter |
| SaaS-embedded (Salesforce/SharePoint/ServiceNow) | Escalation via `source-unsupported-escalation` |

### Legacy Reference Examples (7 known use-cases)

These remain in the repository as **reference walkthroughs** that demonstrate the universal flow against well-understood inputs. They are not a fixed catalog.

| # | Use-Case | Codename | Source Stack | Target |
|---|----------|----------|-------------|--------|
| 1 | `01-ASPClassicApp` | The Antique | Classic ASP | App Service + Azure SQL |
| 2 | `02-NetFramework30-ASPNET-WEB` | The Fossil | .NET Framework 3.0 | App Service + Azure SQL |
| 3 | `03-WCFNet35` | The Wire | WCF .NET 3.5 | Container Apps + REST API |
| 4 | `04-ContosoUniversityDiPS` | The Campus | ASP.NET MVC | App Service + Azure SQL |
| 5 | `05-BookShop` | The Vault | .NET 3.5 WebForms | Container Apps + Azure SQL |
| 6 | `06-Java-API-BusReservation` | The Express | Java 8 API | Container Apps + PostgreSQL |
| 7 | `07-PartsUnlimited-aspnet45` | The Machine | ASP.NET 4.5 | App Service + Azure SQL |

## Project Context

- **Owner:** Roberto Borges
- **Squad:** Ocean's Twelve — The Azure Heist
- **Stack:** GitHub Copilot prompts, chatmodes, and skills for migrating .NET, Java, and legacy workloads to Azure
- **Description:** Fourteen specialist agents orchestrating AI-assisted migration across 7 legacy applications to Azure cloud.
- **Universe:** Ocean's Eleven 🎬
- **Created:** 2026-05-28
