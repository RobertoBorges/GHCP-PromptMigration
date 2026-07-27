# Azure Migration Agent — VS Code extension

> **Migrate any application to Azure** — directly from your editor.
> One agent definition, 19 prompts, 85 skills. Stack-agnostic. Discovery-first. Hard-stop user-decision gates.

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## What it does

Drops a `.github/agents/Code-Migration-Modernization.agent.md` and the full prompt+skill+chatmode catalog into any VS Code workspace. The agent walks you through:

1. **Discovery** — what is this app? (source, stack, workload, data, integrations)
2. **Plan** — a migration plan + 18 major decisions you need to answer
3. **Execute** — Phases 2-6: migrate code, generate infra, deploy, set up CI/CD, run ops

The agent **never picks framework / database / hosting / IaC tool on your behalf**. It surfaces options + tradeoffs and waits.

## Supported languages, frameworks, and platforms

**Not just .NET and Java.** The agent handles any application in any of these stacks — with a dedicated skill file per stack that knows the modernization patterns, Azure hosting options, and common blockers:

**15 stack adapters (languages / frameworks):**
`.NET` (Framework 2.x → 10 LTS) · `Java` (8/11 → 17/21 LTS + Spring Boot 3.x) · `Python` (2.x → 3.12+, Django/Flask/FastAPI) · `Node.js` (12/14/16 → 20/22 LTS, Express/NestJS/Next) · `PHP` (5.x/7.x → 8.3+, Laravel/Symfony) · `Ruby` (2.x → 3.3+, Rails) · `Go` (≤ 1.19 → 1.22+) · `Perl` · `Rust` · `Scala/Kotlin` · `Oracle Forms` (→ APEX / Spring Boot) · `PowerBuilder` · `Delphi/VB6` · `C++ Windows`

**Plus on-the-fly skill authoring:** if you show up with a stack the 15 adapters don't cover (Elixir, F#, Julia, Clojure, ABAP, etc.), the built-in **skill-creator** meta-skill offers to research authoritative docs and author a new skill on the spot (~2-5 minutes).

**10 source adapters (where the app runs today):** On-premise · AWS · GCP · Oracle Cloud · VMware / RVTools · Kubernetes · container registries (ACR / ECR / Docker Hub) · GitHub repo · ZIP archive · escalation path for SaaS-embedded (Salesforce Apex, ServiceNow, SharePoint on-prem, Power Platform, SAP ABAP) and mainframe/midrange workloads

**8 workload patterns:** Web app · API service · Batch job · Event-driven · Serverless (Functions) · Data pipeline · Desktop / client-server · Packaged app

> **Out of scope as a first-class family:** mainframe / midrange code migration (z/OS, IBM i, COBOL / RPG / Natural). These route to a specialist-partner playbook instead of pretending we can migrate their code.

## Where this extension fits alongside Microsoft's other migration options

Microsoft ships two first-party migration tools that are excellent when they cover your scenario. This extension complements them:

### 🔷 [GitHub Copilot Upgrade](https://marketplace.visualstudio.com/items?itemName=ms-dotnettools.upgrade-agent)
**In-place .NET code upgrades.** .NET Framework/Core → .NET 8/9/10, Web Forms → Blazor, Azure Functions in-process → isolated, SDK-style conversion, Newtonsoft → System.Text.Json, SqlClient migration, and more. If you have a .NET app and want an in-place upgrade, **start there**.

### 🔷 [Azure Migrate](https://learn.microsoft.com/en-us/azure/migrate/migrate-services-overview)
**Infrastructure discovery + lift-and-shift.** VMware/Hyper-V/physical servers → Azure VMs, SQL Server → Azure SQL (via Data Migration Assistant + Azure DMS), ASP.NET on VMware → App Service (via App Service Migration Assistant), business case analysis, dependency mapping. If you have on-prem VMs/databases to move as-is, **start there**.

### 🟢 What this extension does differently

| Capability | This extension | Copilot Upgrade | Azure Migrate |
|------------|----------------|-----------------|---------------|
| Non-.NET stacks (Java, Python, Node.js, PHP, Ruby, Go, +8 more) | ✅ 15 stack adapters | ❌ .NET only | ⚠ IaaS lift only, no code changes |
| Universal source intake (GitHub repo, ZIP, "describe-only", any cloud) | ✅ 10 source adapters | ⚠ workspace only | ✅ VMware / Hyper-V / physical / other cloud |
| **Decision Hardstop Protocol** — 18 architecture Qs answered before code changes; never silently defaults framework, DB engine, hosting, IaC tool | ✅ | ❌ | ❌ |
| **On-the-fly skill authoring** — mid-migration, agent researches + writes a new skill for any novel stack | ✅ | ❌ | ❌ |
| **Cross-session trace memory** — canonical Action Log with per-action token accounting | ✅ | ❌ | ❌ |
| **Portfolio 6Rs strategy report** — CIO-ready HTML deck with Factory / ISD-Partner ownership | ✅ | ❌ | ✅ (business case, different format) |
| **Cross-stack post-migration observability** — App Insights + OpenTelemetry recipes for 11+ languages | ✅ | ❌ | ❌ |

**How to combine them:**
- .NET app needing an in-place upgrade → **GitHub Copilot Upgrade**
- On-prem VMs / SQL / web apps to lift into Azure → **Azure Migrate**
- Java / Python / Node.js / PHP / Ruby / Go / other-stack modernization → **this extension**
- Mixed-stack portfolio needing a CIO plan → **this extension** for the 6Rs report, then hand off IaaS candidates to Azure Migrate and .NET candidates to GitHub Copilot Upgrade

## Quick install

1. `Ctrl+Shift+X` in VS Code → search **"Azure Migration Agent"** → Install
2. Open the folder you want to migrate
3. Accept the welcome notification → click **Get started**
4. The extension copies content into `.github/` and `MIGRATION-START-HERE.md`
5. In Copilot Chat (`Ctrl+Alt+I`), type `/assess-any-application`

Full walkthrough: [docs/vscode-quickstart.md](https://github.com/RobertoBorges/GHCP-PromptMigration/blob/main/docs/vscode-quickstart.md)

## What you'll see in your sidebar

Open the **rocket icon 🚀** in the Activity Bar:

```
🛑 DECISIONS REQUIRED           ← pending architecture decisions (from reports/Decisions-Required.md)
AGENT                            ← The Code Migration Modernization Agent
🟢 MAIN PATH (Assess + Phase 1-6) ← the 7-step migration flow
🔵 OPTIONAL ADD-ONS              ← Alternative intakes · Portfolio · Specialized deep-dives · Utility
```

The **status bar** (bottom-left) shows your current migration phase, or **"⚠ AMA: N/M decisions pending"** with a warning background when you have unanswered architecture decisions.

## Standout features

- **🎯 Decision Hardstop Protocol** — Phases 2-6 hard-stop until you answer 18 canonical architecture decisions. No silent defaults, no expert-mode bypass. Stay-as-is is always option 1.
- **🧠 On-the-fly skill authoring** — `skill-creator` writes new stack/source/workload skills mid-migration when it hits an unknown, inspired by [Anthropic's skill-creator](https://github.com/anthropics/skills/tree/main/skills/skill-creator).
- **📜 Action Log (trace memory)** — every meaningful action logs one line to `reports/Report-Status.md` in a canonical format. New sessions recover from the last 5 log entries. Includes per-action turn count + best-effort token estimate.
- **✅ Universal, stack-agnostic wording** — every prompt was swept to remove ".NET or Java only" phrasing. Default goal is minimum viable Azure compatibility, NOT rewriting to microservices.

## Requirements

- **VS Code** ≥ 1.85
- **GitHub Copilot Chat** extension — the extension offers to install it for you on first use
- **Node.js** is NOT required to run the extension (it bundles all content)

## Settings

`Ctrl+,` → search **"Azure Migration"**:

| Setting | Default | Description |
|---------|---------|-------------|
| `azureMigrationSquad.autoInstallCopilot` | `prompt` | `prompt` / `auto` / `never` — Copilot Chat install behavior |
| `azureMigrationSquad.statusBar.enabled` | `true` | Show migration phase + pending decisions in the status bar |

## How it works

The extension is **self-contained**:

- Bundles all migration content under `templates/` (built from the canonical `.github/*` at the repo root via `scripts/sync-templates.mjs`)
- On Initialize, copies `templates/` into the user's workspace under `.github/`
- All Copilot Chat slash commands work via the bundled `.github/prompts/*.prompt.md` files
- The agent definition at `.github/agents/Code-Migration-Modernization.agent.md` orchestrates everything
- Session-lifecycle hooks read/write `reports/Report-Status.md` so recovery works across sessions

No npm CLI. No external Squad framework. Just the extension and Copilot Chat.

## Links

- 🏠 **Repo:** https://github.com/RobertoBorges/GHCP-PromptMigration
- 📚 **Quickstart:** [docs/vscode-quickstart.md](https://github.com/RobertoBorges/GHCP-PromptMigration/blob/main/docs/vscode-quickstart.md)
- 🛠️ **Issues:** https://github.com/RobertoBorges/GHCP-PromptMigration/issues

## License

[MIT](./LICENSE)
