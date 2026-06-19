# @robertoborges/azure-migration-squad

> **Azure migration agents for GitHub Copilot + Squad.** Any source. Any stack. One command.

[![npm](https://img.shields.io/npm/v/@robertoborges/azure-migration-squad?label=npm&color=blue)](https://www.npmjs.com/package/@robertoborges/azure-migration-squad)
[![Squad](https://img.shields.io/badge/squad--cli-compatible-blueviolet?logo=githubcopilot)](https://github.com/bradygaster/squad)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

A drop-in extension for [Squad](https://github.com/bradygaster/squad) that turns it into a universal Azure migration platform: 15 specialist agents, 60+ skills, and a Discovery-first workflow that handles **any application, from any source, in any stack** — and produces an evidence-bound migration plan ready for Azure.

---

## What you get

- **15 specialist agents** — Discovery Engineer, Architect, Coder, Tester, Azure Specialist, DevOps Engineer, Database Specialist, Observability Engineer, Performance Engineer, Security Auditor, Cost Engineer, Cutover Commander, Evaluator, Scribe, Presentation Specialist
- **Source adapters** for on-premise, AWS, GCP, Oracle, VMware, Kubernetes, container registries, GitHub repos, ZIPs, mainframes
- **Stack adapters** for .NET, Java, Python, Node.js, PHP, Ruby, Go, Perl, Rust, COBOL, Oracle Forms, PowerBuilder, Delphi/VB6, Scala/Kotlin, C++ Windows
- **Workload patterns** for webapp, api-service, batch-job, event-driven, serverless, data-pipeline, desktop-client-server, packaged-app, mainframe-transactional
- **Migration strategy decision tree** — a 12-branch decision engine that goes far beyond a 6Rs label
- **Discovery Dossier + Capability Matrix** — evidence-bound, schema-validated artifacts every Phase prompt consumes
- **Phase 1–6 prompts** — Plan, Migrate Code, Generate Infra, Deploy, Set up CI/CD, Post-Migration Ops

---

## Requirements

- **Node.js ≥ 20**
- **[Squad](https://github.com/bradygaster/squad) (`@bradygaster/squad-cli`)** installed and initialized in your repo
- **GitHub Copilot** (CLI or Chat)

---

## Install

### One-shot (recommended for first try)

```bash
# 1. Set up Squad in your project
npm install -g @bradygaster/squad-cli
squad init

# 2. Add the migration agents
npx @robertoborges/azure-migration-squad@insider init

# 3. Open Copilot Chat → /assess-any-application
```

### Global install (for repeated use)

```bash
npm install -g @robertoborges/azure-migration-squad@insider
azure-migration-squad init     # or:  ams init
```

### Insider channel vs stable

```bash
npm install -g @robertoborges/azure-migration-squad@latest    # stable
npm install -g @robertoborges/azure-migration-squad@insider   # preview builds
```

---

## Commands

```
azure-migration-squad <command> [options]
ams <command> [options]                       # short alias

Commands:
  init                  Scaffold the migration squad into the current repo
  upgrade               Refresh squad content to the latest version
  doctor                Validate squad integrity
  list                  List installed adapters
  telemetry <sub>       Manage telemetry — sub: on | off | status
  help                  Show this help
  version               Print version

Flags:
  --force               (init)    Bypass Squad-detection check
  --overwrite           (init)    Replace existing files instead of skipping
  --no-telemetry        (any)     Skip telemetry for this invocation
```

### Typical workflow

**GitHub Copilot CLI** (terminal):
```bash
# In your project dir, after `squad init` + `npx @robertoborges/azure-migration-squad init`:
copilot --agent squad
# Then talk naturally — slash commands are NOT auto-registered in the CLI:
> Assess this application for Azure migration
# Discovery Engineer walks you through 6 questions, produces:
#   reports/Discovery-Dossier.md + reports/Capability-Matrix.yaml
> Build the migration plan
# Architect approves strategy, produces reports/Migration-Plan.md
> Phase 1 plan and assess
# ... through Phase 6
```

**VS Code Copilot Chat:** slash commands ARE auto-registered. Type:
```
/assess-any-application
/build-migration-plan
/phase1-planandassess
...
```

Both produce identical outcomes.

---

## How it integrates with Squad

`azure-migration-squad init` installs content into the directories Squad already manages:

| Target | What lands |
|--------|------------|
| `.squad/agents/` | 15 agent charters (Discovery Engineer is new; others extend / replace defaults) |
| `.github/chatmodes/` | Migration-Orchestrator, Discovery-Intake, plus 7 specialized chatmodes |
| `.github/prompts/` | Assess-Any-Application, Build-Migration-Plan, Phase 0–6 prompts |
| `.github/skills/` | 60+ source/stack/workload/universal skill files |
| `.github/hooks/` | agent-dispatch, phase-gates, quality-checklist |
| `AGENTS.md` | Squad-aware operator instructions |
| `.azure-migration-squad/manifest.json` | Installation tracking |

Your `reports/`, `.squad/decisions.md`, and history files are **never touched** by `init` or `upgrade`.

---

## Telemetry — opt-out by default

This CLI collects **anonymous** usage data to help us prioritize fixes and new adapters:

**What we collect:**
- Anonymous install ID (random UUID)
- Package version + command name + OS family + Node major version
- Whether Squad was detected
- Error class names (NOT messages, NOT stack traces)

**What we NEVER collect:**
- File paths, project names, source code, prompts, customer data
- IPs, emails, git remote URLs

**How to opt out** (all options work — first match disables):

```bash
# Per-invocation
azure-migration-squad init --no-telemetry

# Persistent — CLI
azure-migration-squad telemetry off

# Persistent — env var
export AZURE_MIGRATION_SQUAD_TELEMETRY=0

# Industry-standard convention (also honored)
export DO_NOT_TRACK=1

# CI environments — auto-disabled by default (CI=true)
```

**Backend:** PostHog Cloud, US region. Public dashboard available — see [docs/telemetry.md](https://github.com/RobertoBorges/GHCP-PromptMigration/blob/main/docs/telemetry.md).

---

## See also

- [GHCP-PromptMigration](https://github.com/RobertoBorges/GHCP-PromptMigration) — docs hub, walkthroughs, 7 sample use-cases
- [Squad](https://github.com/bradygaster/squad) — the multi-agent runtime
- [GitHub Copilot CLI](https://github.com/github/copilot-cli)

## License

MIT © Roberto Borges
