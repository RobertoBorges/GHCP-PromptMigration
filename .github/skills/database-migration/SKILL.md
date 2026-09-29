---
name: database-migration
description: Plans database migration, validation, and cutover for Azure targets.
user-invocable: true
disable-model-invocation: true
---

<!-- BEGIN: capability-matrix-gate (auto-managed by inject-capability-matrix-gates.mjs) -->

## 🚦 MANDATORY OPENING CHECK — Capability Matrix Required

**Before doing ANY work for Database Migration, verify the Discovery contract:**

| Required artifact | Location | If missing |
|-------------------|----------|------------|
| Discovery Dossier | `reports/Discovery-Dossier.md` | **STOP** — run `/assess-any-application` first |
| Capability Matrix | `reports/Capability-Matrix.yaml` | **STOP** — run `/assess-any-application` first |
| Approved Migration Plan | `reports/Migration-Plan.md` | **STOP** — run `/phase1-plan` (or the `/build-migration-plan` add-on) |

### If ANY of those three artifacts is missing

Reply with exactly:

```
🚨 Database Migration cannot proceed without the Discovery contract.

Missing artifacts:
  - reports/Discovery-Dossier.md          [missing/present]
  - reports/Capability-Matrix.yaml         [missing/present]
  - reports/Migration-Plan.md              [missing/present]

Required steps before re-running this phase:
  1. Open Copilot Chat → /assess-any-application  (or in CLI: "assess this application")
  2. Then: /phase1-plan                            (produces the Migration Plan, or use /build-migration-plan add-on)
  3. Then: /database-migration

To override (skip Discovery and accept risk), log a waiver entry in
reports/Decision-Log.md with `Waiver: skip-discovery=<reason>` and re-invoke
this skill with the `--accept-risk` natural-language flag in your request.
```

**Do NOT proceed past this gate unless:**
- All three artifacts exist, OR
- A waiver entry exists in `reports/Decision-Log.md` AND the user explicitly said "skip discovery" or similar

### When the gate passes

1. Read `reports/Capability-Matrix.yaml` and extract these fields you must honor:
   - `source.primary_adapter` → load the matching `source-*` skill
   - `stack.primary_stack` + `stack.secondary_stacks` → load matching `stack-*` skills
   - `workload.primary_pattern` → load matching `workload-*` skill
   - `migration_strategy.recommendation` → adjust phase emphasis based on the recommended strategy
   - `risk_flags` → load the matching risk skills (e.g., `risk-cross-region-data.md`)
   - `unresolved_questions` → if any remain unanswered, surface them BEFORE starting work
2. **Skill Gap Check (belt + suspenders)** — for each value above, verify a matching `<family>-<value>.md` exists in `.github/skills/`. If any is missing, invoke `.github/skills/skill-creator/SKILL.md` to author it on the fly. Ask a single Y/n/N-for-session confirmation; default is Y.
3. Read `reports/Migration-Plan.md` for approved sequencing and any app-specific extra gates.
4. Confirm Phase prerequisites are met.

<!-- END: capability-matrix-gate -->

<!-- BEGIN: decision-hardstop-gate (auto-managed by inject-decision-gates.mjs) -->

## 🛑 MANDATORY DECISION GATE — Major decisions required for Database Migration

The Code Migration Modernization Agent does **not** decide major architecture on your behalf.
Before Database Migration can do any work, every decision below must be **DECIDED** in
`reports/Decisions-Required.md` (or marked **🚫 N/A** if genuinely not applicable).

| Catalog ID | Decision | Required status |
|-----------|----------|-----------------|
| D-04 | Database engine | ✅ DECIDED (or 🚫 N/A) |
| D-05 | Database migration tool | ✅ DECIDED (or 🚫 N/A) |
| D-15 | Acceptable downtime | ✅ DECIDED (or 🚫 N/A) |

### Check sequence (run this BEFORE anything else in this skill)

1. Open `reports/Decisions-Required.md`.
2. For each row in the table above, locate its section and read **Status**.
3. Any decision still at `⏸ PENDING` → STOP. Do not proceed.
4. Apply the **Decision Hardstop protocol** from `.github/skills/migration-decisions/references/decision-hardstop.md`:
   - Post the 🛑 DECISION REQUIRED block in chat with options + tradeoffs from `.github/skills/migration-decisions/references/decision-catalog.md`.
   - Wait for the user's reply (or for the file to be updated).
   - Record the answer in `reports/Decision-Log.md`.
   - Update Status to `✅ DECIDED <ISO date>` in `reports/Decisions-Required.md`.
   - THEN re-run the check sequence.
5. If `reports/Decisions-Required.md` is missing → STOP and route the user to `/phase1-plan`.

### Hard rules

- **Never assume.** Newer is not automatically better. "What most projects use" is not a decision.
- **Never silently pick.** If a value is missing, ask. Don't infer.
- **Never accept brief replies.** "Use SQL" is not enough — confirm engine, tier, region.
- **Never bypass with an expert flag.** This protocol applies on every project.

See [`.github/skills/migration-decisions/references/decision-hardstop.md`](../migration-decisions/references/decision-hardstop.md) for the full protocol
and [`.github/skills/migration-decisions/references/decision-catalog.md`](../migration-decisions/references/decision-catalog.md) for canonical option matrices.

<!-- END: decision-hardstop-gate -->

<!-- BEGIN: action-log-contract (auto-managed by inject-action-log-contract.mjs) -->

## 📜 Action Log Contract

**After each meaningful action** in this skill, append one single-line entry to the `## 📜 Action Log` section at the bottom of `reports/Report-Status.md`.

Canonical format:
```
- <ISO-8601-UTC> | actor=DatabaseMigration | action=<verb-phrase> | files=<+created,~modified,-deleted> | tokens=~<bucket> | turn=<n> | notes="<free text>"
```

Rules:
- Use `actor=DatabaseMigration` for actions taken by this skill.
- Use `actor=User` for actions taken by the user (e.g., answering a decision).
- Log **only meaningful actions**: phase transitions, artifact production, decision events, gate passes/blocks, user inputs, rollback events. Do NOT log every internal grep or file read.
- Estimate `tokens` in buckets: `~0`, `~500`, `~2k`, `~8k`, `~30k`. The `turn` counter is exact; token estimate is best-effort. Point users to Copilot Dashboard for authoritative counts.
- If `reports/Report-Status.md` doesn't exist yet, create it from `.github/skills/migration-artifacts/references/migration-report-template.md` first — it already includes the `## 📜 Action Log` section.

Full spec: `.github/skills/migration-artifacts/references/action-log-format.md`.

<!-- END: action-log-contract -->


