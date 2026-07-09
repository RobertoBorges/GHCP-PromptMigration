# Azure Migration Agent — VS Code extension

> **Migrate any application to Azure** — directly from your editor.
> One agent definition, 19 prompts, 113 skills. Stack-agnostic. Discovery-first. Hard-stop user-decision gates.

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## What it does

Drops a `.github/agents/Code-Migration-Modernization.agent.md` and the full prompt+skill+chatmode catalog into any VS Code workspace. The agent walks you through:

1. **Discovery** — what is this app? (source, stack, workload, data, integrations)
2. **Plan** — a migration plan + 18 major decisions you need to answer
3. **Execute** — Phases 2-6: migrate code, generate infra, deploy, set up CI/CD, run ops

The agent **never picks framework / database / hosting / IaC tool on your behalf**. It surfaces options + tradeoffs and waits.

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
🛑 DECISIONS REQUIRED        ← Wave H artifact — pending architecture decisions
AGENT                         ← The Code Migration Modernization Agent
PROMPTS                       ← 19 slash commands
SKILLS                        ← 113 adapters & patterns
```

The **status bar** (bottom-left) shows your current migration phase, or **"⚠ AMA: N/M decisions pending"** with a warning background when you have unanswered architecture decisions.

## Supported tech

| Sources | Stacks | Workloads |
|---------|--------|-----------|
| On-premise, AWS, GCP, Oracle, VMware, Kubernetes, container registries, GitHub repos, ZIPs, mainframes | .NET, Java, Python, Node.js, PHP, Ruby, Go, Perl, Rust, COBOL, Oracle Forms, PowerBuilder, Delphi/VB6, Scala/Kotlin, C++ Windows | Web app, API, batch, event-driven, serverless, data pipeline, desktop, packaged, mainframe transactional |

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

No npm CLI. No external Squad framework. Just the extension and Copilot Chat.

## Links

- 🏠 **Repo:** https://github.com/RobertoBorges/GHCP-PromptMigration
- 📚 **Quickstart:** [docs/vscode-quickstart.md](https://github.com/RobertoBorges/GHCP-PromptMigration/blob/main/docs/vscode-quickstart.md)
- 🛠️ **Issues:** https://github.com/RobertoBorges/GHCP-PromptMigration/issues

## License

[MIT](./LICENSE)
