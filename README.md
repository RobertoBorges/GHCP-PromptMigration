# GHCP-PromptMigration — Docs Hub for Azure Migration Squad

> **Universal Azure migration agents for GitHub Copilot + Squad.** Any source. Any stack. One command.

[![npm](https://img.shields.io/npm/v/@robertoborges/azure-migration-squad?label=npm&color=blue)](https://www.npmjs.com/package/@robertoborges/azure-migration-squad)
[![VS Code Marketplace](https://img.shields.io/visual-studio-marketplace/v/robertoborges.azure-migration-squad-vscode?label=VS%20Code&color=blueviolet&logo=visualstudiocode)](https://marketplace.visualstudio.com/items?itemName=robertoborges.azure-migration-squad-vscode)
[![Squad](https://img.shields.io/badge/squad--cli-compatible-blueviolet?logo=githubcopilot)](https://github.com/bradygaster/squad)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

This is the **canonical docs hub** for the Azure Migration Squad. The squad migrates **any application** — regardless of where it runs today or what it's built in — to Azure. Discovery-first, evidence-bound, squad-orchestrated.

The squad ships as:
- A **VS Code extension**: [`robertoborges.azure-migration-squad-vscode`](https://marketplace.visualstudio.com/items?itemName=robertoborges.azure-migration-squad-vscode) — easiest path for VS Code users
- An **npm package**: [`@robertoborges/azure-migration-squad`](https://www.npmjs.com/package/@robertoborges/azure-migration-squad) — CLI, also powers the extension
- A **Squad plugin marketplace** entry — for Squad-discovery-first users (see `plugin.manifest.json`)
- A **GitHub template** (coming in Wave D) — for new engagements that want sample code included
- This **monorepo** — the canonical source of truth; both the npm package and extension are built from this repo's `.github/` + `.squad/` content

---

## Four ways to install

### 🥇 Option 1 — VS Code extension (easiest for VS Code users)

One-click install gives you a sidebar with all 15 agents + 26 prompts + 60+ skills, a status bar showing your current migration phase, and Command Palette commands for Initialize / Upgrade / Doctor / Open Discovery.

```bash
# In VS Code:
Ctrl+Shift+X → search "Azure Migration Squad" → Install
# Or from terminal:
code --install-extension robertoborges.azure-migration-squad-vscode
```

After install, open any project folder and a welcome notification offers to set everything up. See [**docs/vscode-quickstart.md**](./docs/vscode-quickstart.md) for the full walkthrough with screenshots.

### 🥈 Option 2 — npm CLI (for terminal-first workflows)

```bash
# 1. Set up Squad (one-time)
npm install -g @bradygaster/squad-cli
squad init

# 2. Add the Azure Migration Squad — pick either:
npx @robertoborges/azure-migration-squad@latest init     # one-shot, no install
# OR
npm install -g @robertoborges/azure-migration-squad@latest
ams init                                                  # short alias for the rest of this session

# 3a. If using VS Code with GitHub Copilot Chat:
#     Slash commands work directly:
#       /assess-any-application
#
# 3b. If using GitHub Copilot CLI (the `copilot` terminal command):
#     Slash commands like /assess-any-application are NOT auto-registered.
#     Just describe what you want in plain English:
#       "Assess this application for Azure migration"
#       "Discover this app"
#       "Phase 2 — migrate the code"
#     The Squad agent reads the natural-language→action table in
#     .github/copilot-instructions.md and dispatches the right specialist.
```

> 💡 **`ams` is the short alias** for `azure-migration-squad` — both work for all commands. Use whichever you prefer. After `npm install -g`, both binaries are on your `PATH`.

### 🥉 Option 3 — Squad plugin marketplace

```bash
# 1. Register this repo as a marketplace
squad plugin marketplace add RobertoBorges/GHCP-PromptMigration

# 2. Install the plugin (curated subset: agents + universal skills + routing as Squad knowledge)
squad plugin install azure-migration-squad

# 3. For full Copilot integration (chatmodes + prompts + .github/skills), follow Option 2
```

**Trade-off:** Squad plugin install lands files under `.squad/` per Squad's plugin contract. For full Copilot Chat integration (chatmodes, slash commands), you still want the npm package.

### 🥉 Option 3 — GitHub template (coming soon — Wave D)

A starter repo with the squad pre-installed plus one sample use-case for instant exploration. Content lives in [`template-repo-starter/`](./template-repo-starter/) — push to a separate GitHub repo + toggle "Template repository" in Settings to make it one-click installable.

> **Translations:** [Español 🇪🇸](./docs/translations/README.es-ES.md) · [Português 🇧🇷](./docs/translations/README.pt-BR.md)

---

## What the squad does

```
USER ──► /assess-any-application
            │
            ▼
   ┌──────────────────────────────┐
   │  Discovery Engineer          │  ← intake + classification + evidence
   │  (Saul Bloom Jr.)            │
   │                              │
   │  Outputs:                    │
   │   • Discovery Dossier        │  reports/Discovery-Dossier.md
   │   • Capability Matrix        │  reports/Capability-Matrix.yaml
   │   • Strategy recommendation  │
   └────────────┬─────────────────┘
                │
                ▼
   ┌──────────────────────────────┐
   │  Architect (Danny Ocean)     │  ← approves/refines strategy
   │  /build-migration-plan       │     finalizes target Azure architecture
   └────────────┬─────────────────┘     produces reports/Migration-Plan.md
                │
                ▼
   Phase 1 → Phase 2 → Phase 3 → Phase 4 → Phase 5 → Phase 6
```

Covers source environments: **on-premise, AWS, GCP, Oracle, VMware, Kubernetes, container registries, GitHub repos, ZIPs, mainframes**

Covers stacks: **.NET, Java, Python, Node.js, PHP, Ruby, Go, Perl, Rust, COBOL, Oracle Forms, PowerBuilder, Delphi/VB6, Scala/Kotlin, C++ Windows**

Picks migration strategy via a **12-branch decision tree** (Rehost/Replatform/Refactor/Rearchitect/Rebuild/Retire/Retain — 6Rs is one output field, not the whole engine).

---

## 🚨 Source-of-truth rule — READ THIS BEFORE EDITING

This is a **monorepo** where the npm package is built from canonical content at the repo root. There are TWO locations that look similar — one is the source of truth, the other is a build artifact.

### Where to edit what

| If you want to change... | ✅ Edit here (source of truth) | ❌ NEVER edit here (auto-generated) |
|--------------------------|--------------------------------|--------------------------------------|
| Prompts (Phase 1–6, Assess-Any-Application, etc.) | `.github/prompts/` | `packages/azure-migration-squad/templates/github/prompts/` |
| Skills (source/stack/workload adapters, decision tree, etc.) | `.github/skills/` | `packages/azure-migration-squad/templates/github/skills/` |
| Chatmodes (Discovery-Intake, Migration-Orchestrator, …) | `.github/chatmodes/` | `packages/azure-migration-squad/templates/github/chatmodes/` |
| Hooks (agent-dispatch, phase-gates, etc.) | `.github/hooks/` | `packages/azure-migration-squad/templates/github/hooks/` |
| Agent charters (15 specialists) | `.squad/agents/<name>/charter.md` | `packages/azure-migration-squad/templates/squad/agents/` |
| Squad team + routing | `.squad/team.md`, `.squad/routing.md` | `packages/azure-migration-squad/templates/squad/` |
| Top-level operating docs | `AGENTS.md`, `.github/copilot-instructions.md` | `packages/azure-migration-squad/templates/AGENTS.md`, `templates/github/copilot-instructions.md` |

### Why this layout exists

- `.github/` and `.squad/` are also **actively used by Copilot/Squad when you're working in this repo itself** — that's how we dogfood the squad on its own codebase.
- `packages/azure-migration-squad/templates/` is what ships to npm — it must match the canonical content exactly. A sync script regenerates it before every publish.

### The sync flow

```
.github/   .squad/   AGENTS.md       ← ✏️  edit these
       │       │         │
       └───────┴─────────┘
                 │
                 ▼
       npm run sync          ← copy + flatten into templates/
                 │
                 ▼
   templates/   (build artifact — DO NOT EDIT BY HAND)
                 │
                 ▼
            npm publish     ← consumed by end users
```

The sync runs:
- **Automatically** before every `npm pack` / `npm publish` (via the `prepack` → `prebuild` → `presync` → `sync` script chain)
- **In CI** on every PR (see `.github/workflows/azure-migration-squad-ci.yml`)
- **On demand** anytime: `cd packages/azure-migration-squad && npm run sync`

### Safety nets we ship

1. **Every file under `templates/` has a top-of-file warning** noting it's auto-generated.
2. **`packages/azure-migration-squad/templates/README.md`** is a big "DO NOT EDIT" sign for anyone opening the folder.
3. **CI guard** (`scripts/check-templates-not-edited.mjs`) — fails the build if PR commits touch `templates/` without a matching source-of-truth change.
4. **Sync script is idempotent** — running it always wipes-then-rebuilds `templates/`, so manual edits there are silently lost. Better to fail loudly than silently.

**TL;DR:** edit at the root (`.github/`, `.squad/`, `AGENTS.md`). Never touch `packages/azure-migration-squad/templates/`.

---

## Repository structure

```
GHCP-PromptMigration/                            ← this monorepo
├── README.md                                    ← docs hub (you are here)
├── plugin.manifest.json                         ← Squad plugin marketplace metadata (auto-generated)
├── package.json                                 ← npm workspaces root
│
├── packages/
│   └── azure-migration-squad/                   ← published npm package
│       ├── package.json                         (@robertoborges/azure-migration-squad)
│       ├── bin/cli.js                           ← ✏️ EDIT (CLI source)
│       ├── lib/                                 ← ✏️ EDIT (telemetry + opt-out consent)
│       ├── schemas/                             ← ✏️ EDIT (JSON Schemas)
│       ├── scripts/                             ← ✏️ EDIT (sync, validate, lint)
│       ├── templates/                           ← ❌ DO NOT EDIT (auto-generated from root .github/ + .squad/)
│       └── WAVE-A-HANDOFF.md                    (publish runbook)
│
├── .github/                                     ← ✏️ SOURCE OF TRUTH (canonical content)
│   ├── chatmodes/                               (9 Copilot chatmodes)
│   ├── prompts/                                 (26 prompts: Assess-Any-Application, Phase 0-6, ...)
│   ├── skills/                                  (60+ source/stack/workload + universal skills)
│   ├── hooks/                                   (4 orchestration hooks)
│   ├── copilot-instructions.md
│   └── workflows/                               (CI: azure-migration-squad-ci.yml + others)
│
├── .squad/                                      ← ✏️ SOURCE OF TRUTH (Squad orchestration layer)
│   ├── agents/                                  (15 specialist charters)
│   ├── team.md                                  (roster)
│   ├── routing.md                               (capability-based routing)
│   └── decisions.md                             (durable decision log)
│
├── docs/                                        ← ✏️ EDIT (extended documentation)
│   ├── telemetry.md                             (data we collect + opt-out matrix)
│   ├── privacy-policy.md                        (privacy stance)
│   ├── release-automation.md                    (how releases ship via Changesets + GitHub Actions)
│   ├── contributing-adapters.md                 (how to add a new adapter)
│   ├── architecture/                            (system architecture)
│   ├── guides/                                  (onboarding + skills map)
│   ├── walkthroughs/                            (7 reference walkthroughs)
│   └── use-case-cheatsheets/                    (7 quick-reference cards)
│
├── Use-cases/                                   ← ✏️ EDIT (7 reference applications, samples)
│   ├── 01-ASPClassicApp/                        (Classic ASP)
│   ├── 02-NetFramework30-ASPNET-WEB/            (.NET Framework 3.0)
│   ├── 03-WCFNet35/                             (WCF .NET 3.5)
│   ├── 04-ContosoUniversityDiPS/                (ASP.NET MVC)
│   ├── 05-BookShop/                             (.NET 3.5 WebForms)
│   ├── 06-Java-API-BusReservation/              (Java 8 + Spring)
│   └── 07-PartsUnlimited-aspnet45/              (ASP.NET 4.5)
│
└── AGENTS.md, CLAUDE.md, JOURNAL.md, PORTFOLIO.md   ← ✏️ EDIT (squad operating docs)
```

---

## The squad (15 specialists)

| # | Agent | Alias | Best for |
|---|-------|-------|----------|
| 1 | **Discovery Engineer** | Saul Bloom Jr. | Intake, classification, 6Rs recommendation, Capability Matrix |
| 2 | Architect | Danny Ocean | Migration strategy approval, target architecture, sequencing |
| 3 | Coder | Rusty Ryan | Code modernization, framework upgrades, refactoring |
| 4 | Tester | Linus Caldwell | Validation, smoke testing, prompt QA |
| 5 | Azure Specialist | Basher Tarr | Azure hosting, identity, landing zones |
| 6 | DevOps Engineer | Turk Malloy | CI/CD, deployment automation |
| 7 | Observability Engineer | Livingston Dell | Monitoring, App Insights, alerts |
| 8 | Database Specialist | The Amazing Yen | Schema migration, cutover, data validation |
| 9 | Performance Engineer | Virgil Malloy | Load, baselines, scaling |
| 10 | Security Auditor | Frank Catton | Auth, secrets, RBAC, compliance |
| 11 | Evaluator | Saul Bloom | Prompt quality, regression review |
| 12 | Cutover Commander | Reuben Tishkoff | Rollout, rollback, go-live |
| 13 | Scribe | Roman Nagel | Journal, decision log |
| 14 | Presentation Specialist | Tess Ocean | Status decks, executive summaries |
| 15 | Cost Engineer | The Accountant | Cost models, right-sizing, FinOps |

Charters: [`.squad/agents/<name>/charter.md`](./.squad/agents/). Routing: [`.squad/routing.md`](./.squad/routing.md).

---

## Quality + telemetry

### Telemetry — opt-out by default
The npm CLI collects anonymous usage data (package version, command name, OS/Node, Squad-detected, error class). **Never** file paths, project content, prompts, customer data, IPs, or emails.

Opt out at any time:
```bash
azure-migration-squad telemetry off
# or
export AZURE_MIGRATION_SQUAD_TELEMETRY=0
# or industry-standard:
export DO_NOT_TRACK=1
```

Full policy: [docs/telemetry.md](./docs/telemetry.md) · Privacy: [docs/privacy-policy.md](./docs/privacy-policy.md)

### Quality gates
Every PR runs in CI (Ubuntu × Node 20):
- ✅ JSON Schema validation for the Capability Matrix
- ✅ Build validation (key files synced, all cross-references resolve)
- ✅ PII-leak lint (telemetry calls cannot leak file paths)
- ✅ Plugin manifest validation
- ✅ Install smoke test
- ✅ Squad governance evaluator + prompt linter
- ✅ Source-of-truth guard (templates/ not edited by hand)

> CI runs Linux-only because the package is pure Node.js with no native deps. macOS and Windows are spot-checked manually before each release.

---

## Contributing

We welcome contributions:

- 🆕 **New source adapter** (e.g. `source-azure-devops`, `source-bitbucket-cloud`) — see [docs/contributing-adapters.md](./docs/contributing-adapters.md)
- 🆕 **New stack adapter** (e.g. `stack-elixir`, `stack-haskell`)
- 🆕 **New workload pattern** (e.g. `workload-realtime-streaming`)
- 🌳 **New branches in `migration-strategy-decision-tree.md`**
- 📚 **Use-case walkthroughs** in `docs/walkthroughs/`
- 🌍 **Translations** — README is currently EN; pt-BR + es-ES drafts in `docs/translations/`

Open a PR. The **Evaluator** agent reviews prompt/skill changes for consistency. Releases use [Changesets](https://github.com/changesets/changesets).

---

## Roadmap

- ✅ **Wave A** — npm package published (`@robertoborges/azure-migration-squad@0.1.0-insider.1` on `insider` channel)
- ✅ **Wave B** — Squad plugin marketplace manifest (`plugin.manifest.json`) + validator
- ✅ **Wave C** — Docs hub repositioning (you're looking at it) + telemetry + privacy + contributing-adapters
- ✅ **Wave D** — Starter template content at [`template-repo-starter/`](./template-repo-starter/) (push to a separate GitHub repo when ready)
- ✅ **Wave E** — Evaluator-driven eval suite + Changesets config + Capability Matrix schema validation in `doctor`
- 🔄 **Wave F** — Multi-language docs ([🇪🇸](./docs/translations/README.es-ES.md) / [🇧🇷](./docs/translations/README.pt-BR.md) drafts shipped); Cloud Accelerate Factory pilot + conference talks pending. See [docs/launch-announcement.md](./docs/launch-announcement.md) for ready-to-post drafts.

---

## License

MIT © Roberto Borges
