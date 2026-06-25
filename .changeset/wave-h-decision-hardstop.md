---
"@robertoborges/azure-migration-squad": minor
---

**Wave H: Decision Hardstop Protocol — the squad never decides major architecture for you**

User feedback after the v0.1.2 extension release: "Agents are taking too many decisions by themselves. Major decisions — database engine, framework version, IaC tool, UI architecture — must come from the user, not from the squad."

This release implements that as a first-class architectural feature.

## What this changes

When you run `/Phase1-PlanAndAssess` (or "plan & assess" in CLI), the squad now produces **`reports/Decisions-Required.md`** — a canonical file listing **18 major architecture decisions** that the user must answer before later phases can run.

Phases 2-4 + DatabaseMigration have a new **🛑 MANDATORY DECISION GATE** at the top. If any decision they depend on is still `⏸ PENDING` in `Decisions-Required.md`, the agent STOPS, posts a `🛑 DECISION REQUIRED` block in chat with options + tradeoffs, and refuses to proceed until the user answers.

## What "major decision" means

The 18-item catalog (defined in `.github/skills/decision-catalog.md`):

| # | Decision | Required for |
|---|----------|--------------|
| D-01 | Target framework / runtime version | Phase 2 |
| D-02 | UI architecture | Phase 2 |
| D-03 | Backend / API style (when rewriting) | Phase 2 |
| D-04 | Database engine | Phase 2 + DatabaseMigration |
| D-05 | Database migration tool | DatabaseMigration |
| D-06 | Hosting platform | Phase 3 |
| D-07 | IaC tool (Bicep / Terraform / etc.) | Phase 3 |
| D-08 | Region & data residency | Phase 3 + 4 |
| D-09 | Authentication provider | Phase 2 + 3 |
| D-10 | Multi-tenancy approach | Phase 3 |
| D-11 | Compliance scope (HIPAA/PCI/SOC2/GDPR/...) | Phase 1 (constrains all) |
| D-12 | Cost ceiling | Phase 3 + 4 |
| D-13 | DR — RPO/RTO | Phase 3 + 4 |
| D-14 | Cutover strategy | Phase 4 |
| D-15 | Acceptable downtime | Phase 4 |
| D-16 | CI/CD platform | Phase 5 |
| D-17 | Observability stack | Phase 6 |
| D-18 | Container registry | Phase 3 (if containers) |

For every decision, **"Stay-as-is" is always option 1** so users have to actively reject the conservative path rather than passively accept modernization.

## The protocol — what an agent does when it hits a PENDING decision

```
🛑 DECISION REQUIRED — Target framework / runtime version

Why I'm asking: Locks in for years. Affects EOL dates, team skills,
library compatibility, and Microsoft support windows.

Your options:
1. Stay on .NET Framework 4.8.1  — Rehost only. Locked out of cloud-native.
2. .NET 8 LTS                    — Support ends Nov 2026.
3. .NET 10 LTS                   — Newest LTS. Support through Nov 2028.
4. .NET 9 STS                    — 18-month support. Risky as final target.
5. Other                          — Tell me.

⚠ Our default guess is option 3 (.NET 10 LTS), but that's based only
on "newest LTS = longest runway." The right answer depends on team
skills, library compatibility, and your roadmap — factors I can't see.

Please reply with the option number and a one-line rationale,
OR update reports/Decisions-Required.md and tell me to re-read it.

I cannot proceed with Phase 2 until this is answered.
```

The agent then **stops**. No silent default. No "I'll just pick one to keep moving."

## What got added

| File | Purpose |
|------|---------|
| `.github/skills/decision-hardstop.md` | Binding protocol referenced by all agents |
| `.github/skills/decision-catalog.md` | The 18 canonical decisions with option matrices + tradeoffs |
| `.github/skills/decisions-required-template.md` | Structure of `reports/Decisions-Required.md` |
| `.github/hooks/decision-gates.md` | Orchestration rules loaded into every migration chatmode |
| `scripts/inject-decision-gates.mjs` | Adds the hard-stop gate to Phase 2-4 + DatabaseMigration prompts |
| `scripts/validate-decision-coverage.mjs` | CI guard: every catalog item must be referenced by a phase |

## What got updated

- **Phase 1 (Plan & Assess)** now generates `reports/Decisions-Required.md` from the catalog instead of asking 4 inline questions.
- **Phase 2 / Phase 3 / Phase 4 / DatabaseMigration** all open with a `🛑 MANDATORY DECISION GATE` block listing the catalog IDs they require.
- **Agent charters** for Architect, Coder, Database Specialist, DevOps Engineer, and Azure Specialist now include a `## Decision Hardstop Protocol` section reminding the agent that decisions belong to the user.
- **`copilot-instructions.md`** has a new top-level "🛑 Architecture decisions belong to the user" rule.
- **CI workflow** now runs `npm run validate:decision-coverage` to prevent orphaned catalog entries or unknown ID references.

## Scope for v1

Phases 2, 3, 4 + DatabaseMigration have hard-stop gates. Phases 5 (CI/CD) and 6 (Post-Migration Ops) reference D-16 and D-17 in their decisions but don't yet have hard-stop gates — those follow in a later release. The Plan phase produces the full 18-decision artifact regardless.

## Why this matters

A migration agent making a wrong call on database engine, hosting platform, or IaC tool costs the user **months** of rework. These are not "implementation details" the squad can default. By design, the squad now:

- Surfaces evidence
- Lays out alternatives
- Acknowledges what it can't see
- Waits

That's the right division of labor between an AI assistant and an architect.

## No expert-mode bypass

Deliberately. The whole point breaks if we add a "just accept defaults" flag.
