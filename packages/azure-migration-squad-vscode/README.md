# Azure Migration Squad — VS Code Extension

> **Migrate any application to Azure** — directly from your editor.
> 15 specialist agents, 60+ skills, Discovery-first workflow. Powered by GitHub Copilot.

[![npm](https://img.shields.io/npm/v/@robertoborges/azure-migration-squad?label=cli&color=blue)](https://www.npmjs.com/package/@robertoborges/azure-migration-squad)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## What you get

- **Sidebar tree view** of all 15 specialist agents, 26 prompts, and 60+ skills — click any item to open its source file
- **Status bar widget** showing your current migration phase (Discovery → Phase 1 → … → Complete) — click to jump to the next recommended action
- **11 Command Palette commands** — Initialize, Upgrade, Doctor, Open Discovery, Show prompt catalog, settings, and more
- **First-run welcome panel** with one-click setup
- **VS Code Walkthrough** that guides you through your first migration in 4 steps
- **Settings UI** for telemetry, channel selection, language, and Copilot install behavior
- **Auto-prompt** to install GitHub Copilot Chat (with consent)

## Quick install

1. **`Ctrl+Shift+X`** in VS Code → search **"Azure Migration Squad"** → **Install**
2. Open the folder you want to migrate
3. Accept the welcome notification → click **"Get started"**
4. The extension drops the migration squad into your project (~30 seconds)
5. Open Copilot Chat (**`Ctrl+Alt+I`**) → type **`/assess-any-application`**

The **Discovery Engineer (Saul Bloom Jr.)** takes it from there.

Full walkthrough: [docs/vscode-quickstart.md](https://github.com/RobertoBorges/GHCP-PromptMigration/blob/main/docs/vscode-quickstart.md)

## What gets installed in your project

- `.github/prompts/` — 26 slash commands (try `/assess-any-application`)
- `.github/chatmodes/` — 9 specialized chat modes
- `.github/skills/` — 60+ migration skills (stack + source + workload adapters)
- `.squad/agents/` — 15 specialist charter files (Ocean's Twelve theme)
- `MIGRATION-START-HERE.md` — your 60-second quickstart at the project root

## Supported tech

| Sources | Stacks | Workloads |
|---------|--------|-----------|
| On-premise, AWS, GCP, Oracle, VMware, Kubernetes, container registries, GitHub repos, ZIPs, mainframes | .NET, Java, Python, Node.js, PHP, Ruby, Go, Perl, Rust, COBOL, Oracle Forms, PowerBuilder, Delphi/VB6, Scala/Kotlin, C++ Windows | Web app, API service, batch job, event-driven, serverless, data pipeline, desktop, packaged, mainframe transactional |

## Requirements

- **VS Code** ≥ 1.85
- **Node.js** ≥ 20 (the extension shells out to `npx` for content sync)
- **GitHub Copilot Chat** extension — the extension can install it for you on first use

> 💡 **Squad CLI is NOT required.** This extension bundles every `.squad/` file Copilot Chat needs. If you also want the standalone `squad` binary for `squad init` / `squad agent add` etc., the Command Palette has **"Azure Migration: Install Squad CLI globally (optional)"** — but skip it unless you specifically want the standalone tool.

## Settings

Open **VS Code Settings** → search **"Azure Migration Squad"**:

| Setting | Default | Description |
|---------|---------|-------------|
| `azureMigrationSquad.channel` | `latest` | npm dist-tag (`latest` or `insider`) used by Initialize/Upgrade |
| `azureMigrationSquad.telemetry.enabled` | `false` | Opt-in anonymous usage data — **off by default** |
| `azureMigrationSquad.language` | `en` | Migration content language (`en`, `pt-BR`, `es-ES`) |
| `azureMigrationSquad.autoInstallCopilot` | `prompt` | Behavior when Copilot Chat is missing (`prompt`/`auto`/`never`) |
| `azureMigrationSquad.statusBar.enabled` | `true` | Toggle the migration phase widget |

## How it works

This extension is a **GUI wrapper** around the [`@robertoborges/azure-migration-squad`](https://www.npmjs.com/package/@robertoborges/azure-migration-squad) npm CLI. All AMS-modifying commands (Initialize, Upgrade, Doctor) shell out to `npx` so the extension and the CLI share a **single source of truth**. When the npm package gets a new agent or skill, the extension picks it up automatically on next Initialize/Upgrade.

## Links

- 🏠 **Project home:** https://github.com/RobertoBorges/GHCP-PromptMigration
- 📦 **CLI on npm:** https://www.npmjs.com/package/@robertoborges/azure-migration-squad
- 📚 **Quickstart:** [docs/vscode-quickstart.md](https://github.com/RobertoBorges/GHCP-PromptMigration/blob/main/docs/vscode-quickstart.md)
- 🛠️ **Issues:** https://github.com/RobertoBorges/GHCP-PromptMigration/issues
- 📊 **Telemetry policy:** [docs/telemetry.md](https://github.com/RobertoBorges/GHCP-PromptMigration/blob/main/docs/telemetry.md)

## License

[MIT](./LICENSE)
