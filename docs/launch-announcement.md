# Launch announcement — drafts

> Reusable draft posts for announcing the Azure Migration Squad. Pick the platform that fits your audience; adapt voice as needed.

---

## 📣 LinkedIn (long-form, ~250 words)

🚀 **Just shipped: `@robertoborges/azure-migration-squad` on npm**

For the last several weeks I've been building something that turns GitHub Copilot + [Squad](https://github.com/bradygaster/squad) into a **universal Azure migration platform**.

The idea is simple: most migration tooling is built for one stack (usually .NET or Java) and one source (usually on-prem). Real engagements are messier — PHP on AWS, Oracle Forms on bare metal, COBOL on z/OS, Node.js on Kubernetes. So I built a Discovery-first squad of **15 specialist agents** that handles them all:

🔎 **Discovery Engineer** (Saul Bloom Jr.) — characterizes the app with evidence + confidence labels
🏗️ **Architect** (Danny Ocean) — approves strategy, picks Azure targets
💻 **Coder, Tester, Azure Specialist, DevOps, Database, Security, Cost, Cutover** — execute Phase 1–6

Behind it: 60+ source/stack/workload adapters, a 12-branch migration-strategy decision tree (because 6Rs alone is too coarse), and a Capability Matrix YAML that every phase consumes mechanically. No more "we'll figure it out later" hand-offs.

**Try it in 30 seconds:**
```
npm install -g @bradygaster/squad-cli
squad init
npx @robertoborges/azure-migration-squad@insider init
# In Copilot Chat: /assess-any-application
```

Built in the open — MIT license, telemetry opt-out by default (PostHog, anonymous). Source: github.com/RobertoBorges/GHCP-PromptMigration

Huge shoutout to @bradygaster for Squad — none of this would exist without that runtime.

Would love to hear your migration war stories. What's the weirdest stack you've ever moved to Azure?

#Azure #GitHubCopilot #Migration #AI #DevTools

---

## 📰 dev.to / Hashnode (~600 words)

# I built a universal Azure migration squad for GitHub Copilot. Here's why monolithic prompts don't scale.

Every Azure migration project I've worked on starts the same way: a customer hands over a mix of artifacts — CMDB export here, RVTools dump there, "and don't forget the COBOL job that runs every night" — and asks "how long?"

The honest answer used to be "give me three weeks to figure out what you have."

That's not a tooling problem. It's a **workflow** problem. Migration tools are great at the destination (Bicep, Azure DMS, App Service slot swaps) but rarely structured at the origin: classify the app, score the data gravity, pick a 6Rs strategy backed by evidence, hand off to the right specialists without losing context.

So I built one. It ships today as `@robertoborges/azure-migration-squad` — a Squad/GitHub Copilot plugin that adds 15 specialist agents and 60+ source/stack/workload adapters to your repo.

## The opinionated bit

The squad **refuses to start Phase 1 without a Capability Matrix**. That's a YAML artifact the Discovery Engineer produces after probing your source — file extensions, manifests, integration points, data gravity, all with `evidence_confidence: high|medium|low` labels. Every subsequent phase reads it. If an axis is `low` confidence, Discovery is sent back for more probes before code generation can start.

This solves the biggest failure mode I've seen in copilot-driven migrations: the model confidently invents an architecture that's wrong for the actual app because nobody made it slow down and gather evidence first.

## Why a squad, not one big prompt?

Originally I tried the obvious thing — one giant 500-line prompt that knows about migration. It was brittle:

- New stack (PHP? Node? COBOL?) meant editing the One Prompt
- Reviewers couldn't tell where security ended and cost optimization began
- No way to govern phase transitions
- Couldn't reuse migration knowledge across customer engagements

The squad model fixes all of these. Each agent has a charter, owns their scope, dispatches sub-agents in parallel, and writes durable decisions back to `.squad/decisions.md`. The Coder doesn't have to think about Phase 5 CI/CD — that's DevOps Engineer's job, with their own skill set loaded.

## What surprised me

**The decision tree matters more than the 6Rs label.** 6Rs (Rehost/Replatform/Refactor/Rearchitect/Rebuild/Retire/Retain) is what you write in the executive deck. But the *reasoning* — "we're refactoring because business priority is modernize + source is supported + tests exist + data gravity is medium" — is what predicts whether the migration actually succeeds. I built that as a 12-branch decision tree skill that produces both the label and the trace.

**Most migrations need an escape valve.** Not every app has an Azure-native target. Mainframe, SaaS-embedded apps (Salesforce Apex, ServiceNow), packaged software where the source is binary-only. The squad has explicit `source-unsupported-escalation` paths so the Architect can call partners or rebuild rather than silently fudge.

## Install it

```bash
npm install -g @bradygaster/squad-cli
squad init
npx @robertoborges/azure-migration-squad@insider init
# Open Copilot Chat → /assess-any-application
```

MIT licensed. Telemetry opt-out by default (anonymous, PostHog, see [`docs/telemetry.md`](https://github.com/RobertoBorges/GHCP-PromptMigration/blob/main/docs/telemetry.md)). Contributing guide for new adapters: [`docs/contributing-adapters.md`](https://github.com/RobertoBorges/GHCP-PromptMigration/blob/main/docs/contributing-adapters.md).

## What's next

- **Wave D:** GitHub template repo for one-click starts
- **Wave E:** Evaluator-driven eval suite + Changesets + PostHog public dashboards
- **Wave F:** Multi-language docs (Spanish + Portuguese drafts already in `docs/translations/`)

Issues, PRs, and migration war stories welcome at [github.com/RobertoBorges/GHCP-PromptMigration](https://github.com/RobertoBorges/GHCP-PromptMigration).

---

## 🐦 X / Bluesky (short-form thread)

🧵 1/ Just shipped `@robertoborges/azure-migration-squad` — a GitHub Copilot squad that migrates *any* app to Azure. Any source (on-prem/AWS/GCP/Oracle/mainframe). Any stack (.NET/Java/Python/Node/PHP/Ruby/Go/COBOL/...).

2/ The trick: a **Discovery Engineer** agent characterizes the app FIRST. Output is a `Capability Matrix` YAML with `evidence_confidence: high|medium|low` per axis. Every later phase reads it. No more "model invents an architecture."

3/ 15 specialist agents (Architect, Coder, Azure Specialist, DBA, Security, DevOps, Cutover, ...). 60+ source/stack/workload adapters. A 12-branch migration-strategy decision tree (6Rs is one output, not the engine).

4/ Try it:
```
npm i -g @bradygaster/squad-cli
squad init
npx @robertoborges/azure-migration-squad@insider init
# In Copilot Chat: /assess-any-application
```

5/ MIT, telemetry opt-out by default. Built on @bradygaster's Squad runtime. Source: github.com/RobertoBorges/GHCP-PromptMigration

What stack should I add an adapter for next? 👇

---

## 📨 Internal Microsoft Teams / TechCommunity (~150 words)

**New tool for Azure migration engagements**

Hey team — sharing something I built that might help on your next migration engagement.

`@robertoborges/azure-migration-squad` is an open-source npm package that adds 15 specialist migration agents to any GitHub Copilot session via [Squad](https://github.com/bradygaster/squad). It's designed for the messy reality of customer engagements: any source (on-prem/AWS/GCP/Oracle/VMware/K8s/mainframe), any stack (.NET/Java/Python/Node/PHP/Ruby/Go/COBOL/...), any workload pattern (webapp/api/batch/event-driven/data-pipeline/...).

Key feature: the **Discovery Engineer** produces an evidence-bound Capability Matrix BEFORE any code generation. Every phase reads it. Cuts down on the "model confidently invents the wrong architecture" failure mode.

Try it: docs at github.com/RobertoBorges/GHCP-PromptMigration

Free, MIT licensed, telemetry opt-out by default. Feedback / pilot engagements welcome — open an issue or DM me.

---

## How to use these drafts

1. Pick the platform
2. Replace any personal pronouns / framing as needed for your voice
3. Cross-link the URLs (npmjs.com page, GitHub repo, docs)
4. Add screenshots if posting on visual-heavy platforms (LinkedIn, dev.to)
5. Tag relevant people / accounts:
   - `@github` (npm + Copilot)
   - `@AzureSupp` (Azure team)
   - `@bradygaster` (Squad maintainer)
6. Post + monitor responses

After posting, log the announcement in `JOURNAL.md` so we have a public-comms trail.
