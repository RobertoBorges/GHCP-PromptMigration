---
name: migration-decisions
description: |
  Binding decision-gate router for Azure migration phases. Use whenever work may depend on architecture choices such as runtime, UI/API style, database, hosting, IaC, auth, region, cost, DR, cutover, CI/CD, observability, or container registry. The agent must not choose for the user: if reports/Decisions-Required.md is missing, pending, or not marked decided/N/A for required items, stop and ask using the hardstop protocol.
user-invocable: false
---

# Migration Decisions

## When to use

Use this router whenever planning or execution depends on a major architecture decision. This skill is binding: architecture decisions belong to the user, never the agent.

Project boundary: the migration system is universal across supported app stacks and source environments, but mainframe/midrange workloads such as z/OS, IBM i, COBOL, RPG, Natural, PL/I, CICS, IMS, and VSAM are out of scope for code-level migration and route to specialist escalation.

Hard rules:

- [Decision hardstop protocol](./references/decision-hardstop.md) is mandatory. If a required decision is missing or pending, stop and wait for the user.
- [Decision catalog](./references/decision-catalog.md) contains the closed list of 18 canonical decisions. Adding, removing, or silently bypassing catalog entries requires PR review.
- Phase 2, Phase 3, Phase 4, and database-migration work are gated by `reports/Decisions-Required.md`.
- A gate passes only when each required decision is marked `✅ DECIDED` or `🚫 N/A`.
- No silent defaults. No "newer is better." No expert-mode bypass. No "I'll pick one to keep moving."
- Any recommendation must be labeled `⚠ Default guess`, cite visible evidence, and state that the user owns the choice.
- "Stay as-is" or the lowest-disruption path is always option 1 in every option block.

## Signal to reference selection

| Signal in the task or evidence | Load this reference | Use it for |
|---|---|---|
| Any phase is about to act on runtime, UI, API style, database, migration tooling, hosting, IaC, auth, region, tenancy, compliance, cost, DR, cutover, downtime, CI/CD, observability, or registry | [Decision hardstop protocol](./references/decision-hardstop.md) | Detect gate requirements, check `reports/Decisions-Required.md`, ask the exact blocking question, wait, and record decisions. |
| Need the canonical list of decisions, IDs, dependencies, required phases, options, recommendation logic, or locked downstream choices | [Decision catalog](./references/decision-catalog.md) | Generate or validate decision sections for D-01 through D-18 without expanding or shrinking the catalog. |
| Creating or updating `reports/Decisions-Required.md`, marking choices decided/N/A/locked, or showing option tables and default guesses | [Decisions Required template](./references/decisions-required-template.md) | Use the required file structure, status summary, per-decision template, option blocks, rationale fields, and update steps. |
| Discovery or planning needs to recommend a 6R strategy, target Azure service candidates, required specialists, or alternatives considered | [Migration strategy decision tree](./references/migration-strategy-decision-tree.md) | Derive rehost/replatform/refactor/rearchitect/rebuild/retire/retain from evidence instead of preference; document path and alternatives. |

## How to use

1. Before Phase 2, Phase 3, Phase 4, or database-migration work, read `reports/Decisions-Required.md`.
2. For every catalog item required by the work, proceed only if status is `✅ DECIDED` or `🚫 N/A`.
3. If the file is missing, route the user to Phase 1 planning; do not infer decisions from repository evidence.
4. If any required status is `⏸ PENDING`, ask using the hardstop protocol and stop. Do not implement, scaffold, deploy, or rewrite against a guessed option.
5. When the user decides, update the decision section, status summary, and immutable decision log as described by the references.
6. When producing a default guess, label it exactly as a guess, include "Stay as-is" as option 1, and make clear that silent user acceptance is not consent.
