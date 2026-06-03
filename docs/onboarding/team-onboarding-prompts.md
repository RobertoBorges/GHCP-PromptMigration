# 🎬 Ocean's Twelve — Team Onboarding Prompts

> **Copy-paste these prompts into Copilot CLI.** No prior squad experience needed.

## How to Start

1. Open **VS Code Terminal**
2. Type `ghcs` to launch Copilot CLI
3. Copy any prompt below and paste it

---

## 🟢 Getting Started (First Time)

| What you want | Paste this |
|---------------|-----------|
| Meet the squad | `@squad who are you? introduce the team and what you can do` |
| See migration phases | `@squad show me the migration phases and what each one does` |
| See available apps | `@squad what apps do we have in the Use-cases folder? summarize each` |
| Understand the architecture | `@squad explain the 5-layer architecture and how skills, agents, and prompts work together` |

---

## 🔍 Assessment & Planning

| What you want | Paste this |
|---------------|-----------|
| Start a new migration | `@squad I have a legacy app to migrate. Let's plan it.` |
| Assess a specific app | `@squad assess Use-cases/05-BookShop and tell me the risks and effort` |
| Compare all use cases | `@squad compare the 7 use cases — which is easiest to migrate first?` |
| Get platform advice | `@squad what's the recommended Azure target for a .NET 3.5 WebForms app?` |
| Portfolio triage | `@squad I have multiple legacy apps to assess. Triage all repos, fan out` |

---

## 🚀 Running Migration Phases

| What you want | Paste this |
|---------------|-----------|
| See pending phases | `@squad show me pending phases and what's blocking` |
| Run specific phases | `@squad run phase 0 and 1, fan out` |
| Drill into a phase | `@squad show me details for phase 2` |
| Check progress | `@squad status` |
| Run full migration | `@squad run all phases for Use-cases/07-PartsUnlimited, fan out` |
| One-shot everything | `@squad migrate Use-cases/01-ASPClassicApp to .NET 8 on Azure — full pipeline, fan out` |

---

## 🧐 Decisions & Architecture Advice

| What you want | Paste this |
|---------------|-----------|
| UI framework choice | `@squad should I use Razor Pages or MVC for this WebForms replacement?` |
| Database choice | `@squad what database should I target — Azure SQL or PostgreSQL?` |
| IaC choice | `@squad is Bicep or Terraform better for our team?` |
| Risk analysis | `@squad what are the biggest risks if we migrate the WCF service first?` |
| Sequencing advice | `@squad what order should we migrate these 5 apps and why?` |

---

## 🔒 Security & Cost

| What you want | Paste this |
|---------------|-----------|
| Security review | `@squad run a security hardening review on our migrated code` |
| Cost comparison | `@squad estimate Azure costs for App Service vs Container Apps` |
| Secrets scan | `@squad check for secrets or credentials in the codebase` |
| Compliance check | `@squad review our infra for security best practices and compliance` |

---

## 📊 Status & Reporting

| What you want | Paste this |
|---------------|-----------|
| Executive summary | `@squad give me an executive summary of all migrations in progress` |
| Stakeholder report | `@squad generate a status report I can share with stakeholders` |
| Production readiness | `@squad what's left to do before we can deploy to production?` |
| Phase history | `@squad show me what was completed in each phase so far` |

---

## 🛠️ Troubleshooting

| What you want | Paste this |
|---------------|-----------|
| Build failures | `@squad the build is failing after migration — help me debug` |
| EF Core issues | `@squad my EF Core migration isn't working — what's wrong?` |
| Deployment errors | `@squad the deployed app returns 500 errors — diagnose it` |
| Rollback | `@squad roll back the last phase and show me what changed` |

---

## 💡 Pro Tips

| Tip | Example |
|-----|---------|
| **Add "fan out"** to parallelize | `@squad assess all 7 use cases, fan out` |
| **Ask follow-up questions** naturally | `@squad why did you choose App Service over Container Apps?` |
| **Be specific** for better results | `@squad assess the WCF bindings in Use-cases/03-WCFNet35` |
| **Say "status"** anytime | `@squad status` |
| **Say "show details"** to drill in | `@squad show me details for phase 3` |

---

## 📋 Copy-Paste for Teams

Share this message with your team to get them started:

> **🎬 Ocean's Twelve Squad — Quick Start**
>
> We're using an AI squad to help migrate our legacy apps to Azure. Here's how to get started:
>
> 1. Open **VS Code Terminal** → type `ghcs` to launch Copilot CLI
> 2. Try these prompts:
>    - `@squad who are you?` — meet the 13 specialist agents
>    - `@squad I have a legacy app to migrate` — start a guided interview
>    - `@squad status` — check migration progress
>    - `@squad show me pending phases` — see what's next
>
> The squad will ask you questions and guide you through everything — no need to memorize commands!
>
> 📖 Full prompt list: see `docs/onboarding/team-onboarding-prompts.md` in the repo
> 📖 Full guide: see `README.md` in the repo

---

## 📊 PPTX Deck Management

| What you want | Paste this |
|---------------|-----------|
| Regenerate the deck | `@squad regenerate the PPTX by running docs/pptx/generators/generate_oceans_twelve_deck.py` |
| Update outdated content | `@squad the PPTX deck is outdated. Compare slide content against actual project state, fix mismatches, and regenerate` |
| Fix layout issues | `@squad fix PPTX boundary overflows. Study LATAM template patterns and match them. Regenerate.` |
| Add a new slide | `@squad add a new slide to the PPTX about [TOPIC]. Follow LATAM GCS theme patterns. Regenerate.` |
| Full audit + regenerate | `@squad audit the PPTX end-to-end: check all counts, verify boundaries, fix everything, regenerate. Fan out.` |
