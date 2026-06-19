# Azure Migration Squad — VS Code Extension

> **Migrate any application to Azure** — directly from your editor.
> 15 specialist agents, 60+ skills, Discovery-first workflow. Powered by GitHub Copilot.

[![npm](https://img.shields.io/npm/v/@robertoborges/azure-migration-squad?label=cli&color=blue)](https://www.npmjs.com/package/@robertoborges/azure-migration-squad)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## What it does

This extension makes the [`@robertoborges/azure-migration-squad`](https://www.npmjs.com/package/@robertoborges/azure-migration-squad) toolkit feel native inside VS Code. Coming features (Phases 3-5):

- **Sidebar tree view** of all 15 specialist agents, 26 prompts, and 60+ skills
- **Status bar widget** showing your current migration phase
- **Command Palette commands** to initialize, upgrade, run discovery, and check health
- **First-run welcome panel** that walks you through your first migration
- **Settings UI** for telemetry, channel selection, and language
- **Auto-prompts** to install required GitHub Copilot extensions (with your consent)

> ⚠️ **Status:** this is the **Phase 2 scaffold** — only the activation framework is in place today.
> Tree view, status bar, and command set ship in subsequent releases.
> For now, install [the npm CLI](https://www.npmjs.com/package/@robertoborges/azure-migration-squad) directly.

## Quick install (CLI today, full extension UX soon)

```bash
# 1. Install Squad (one-time)
npm install -g @bradygaster/squad-cli

# 2. Initialize Squad in your project
squad init

# 3. Add the Azure Migration Squad
npx @robertoborges/azure-migration-squad@latest init

# 4. Open MIGRATION-START-HERE.md
```

In GitHub Copilot Chat, run `/assess-any-application` — the Discovery Engineer (Saul Bloom Jr.) will walk you through intake.

## What you'll get in your project

- `.github/prompts/` — 26 slash commands (try `/assess-any-application`)
- `.github/chatmodes/` — 9 specialized chat modes
- `.github/skills/` — 60+ migration skills (stack + source + workload adapters)
- `.squad/agents/` — 15 specialist charter files (Ocean's Twelve theme)
- `MIGRATION-START-HERE.md` — your 60-second quickstart

## Supported tech (via the underlying CLI)

| Sources | Stacks | Workloads |
|---------|--------|-----------|
| On-premise, AWS, GCP, Oracle, VMware, Kubernetes, container registries, GitHub repos, ZIPs, mainframes | .NET, Java, Python, Node.js, PHP, Ruby, Go, Perl, Rust, COBOL, Oracle Forms, PowerBuilder, Delphi/VB6, Scala/Kotlin, C++ Windows | Web app, API service, batch job, event-driven, serverless, data pipeline, desktop, packaged, mainframe transactional |

## Requirements

- VS Code **≥ 1.85**
- [GitHub Copilot](https://marketplace.visualstudio.com/items?itemName=GitHub.copilot) + [GitHub Copilot Chat](https://marketplace.visualstudio.com/items?itemName=GitHub.copilot-chat) extensions
- Node.js **≥ 20** (the underlying CLI runs in Node)

## Roadmap

| Version | Feature set |
|---------|-------------|
| **0.1.0 (current — Phase 2)** | Extension scaffold + smoke test |
| 0.2.0 (Phase 3) | Sidebar tree view + Command Palette commands |
| 0.3.0 (Phase 4) | Status bar widget + settings UI |
| 0.4.0 (Phase 5) | First-run welcome + walkthrough + Copilot install prompts |
| 1.0.0 | Marketplace launch with full v1 feature set |

## Links

- 🏠 **Project home:** https://github.com/RobertoBorges/GHCP-PromptMigration
- 📦 **CLI on npm:** https://www.npmjs.com/package/@robertoborges/azure-migration-squad
- 🛠️ **Issues:** https://github.com/RobertoBorges/GHCP-PromptMigration/issues

## License

[MIT](./LICENSE)
