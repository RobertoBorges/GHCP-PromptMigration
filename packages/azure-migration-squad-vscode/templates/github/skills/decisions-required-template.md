# Skill: Decisions Required Template

> Defines the structure of `reports/Decisions-Required.md`. Phase 1 (Plan & Assess) generates this file by filling in the template based on the Capability Matrix and the canonical [`decision-catalog.md`](./decision-catalog.md).

## File location

```
reports/Decisions-Required.md
```

## File header (always include)

```markdown
# Decisions Required — <App Name>

> **This file lists the major architecture decisions the Code Migration Modernization Agent needs from you before it can do its work.**
> Each section has options laid out with tradeoffs. Pick one, fill in your rationale, and the agent will execute against your choice.
> **the agent will NOT proceed past gates with PENDING decisions.** This is by design — see `.github/skills/decision-hardstop.md`.

**Generated:** <ISO date> by Phase 1 — Plan & Assess
**Capability Matrix:** `reports/Capability-Matrix.yaml`
**Decision Log:** `reports/Decision-Log.md` (immutable history)

## Status summary

| # | Decision | Status | Required for |
|---|----------|--------|--------------|
| 1 | Target framework / runtime version | ⏸ PENDING | Phase 2 |
| 2 | UI architecture | ⏸ PENDING | Phase 2 |
| ... | ... | ... | ... |

Replace each row's status as you make decisions. Use:
- `⏸ PENDING` — not yet answered
- `✅ DECIDED <ISO date>` — answered, recorded in Decision-Log.md
- `🔒 LOCKED (by Decision N)` — determined as a side-effect of another decision
- `🚫 N/A — <reason>` — does not apply to this migration (e.g., no database)
```

## Per-decision section template

Repeat this block once per decision from the catalog. Pull the actual options + tradeoffs from `decision-catalog.md`.

```markdown
---

## Decision <N>: <Decision Name>

**Status:** ⏸ PENDING
**Required for:** <Phase / prompt that gates on this>
**Catalog reference:** [`decision-catalog.md#D-<NN>-<slug>`](../.github/skills/decision-catalog.md)

### Why we're asking

<One paragraph: why this can't be defaulted. Pull from catalog.>

### Your options

| # | Option | When to pick | Tradeoffs / risks |
|---|--------|--------------|-------------------|
| 1 | **<Stay-as-is option>** | <when> | <tradeoffs> |
| 2 | **<Option B>** | <when> | <tradeoffs> |
| 3 | **<Option C>** | <when> | <tradeoffs> |
| 4 | Other | When none of the above fit | Tell us in "Your rationale" |

### Our default guess

⚠ **Default guess: Option <N> (<name>)**, based only on <visible evidence from Capability Matrix>.

But the right answer depends on factors we can't see:
- Team skills and hiring plans
- Existing contracts / vendor relationships
- Budget ceilings and cost-allocation rules
- Compliance constraints we may not have seen yet
- Future product roadmap

This is a **guess**, not a recommendation. Please consider it your starting point, not your answer.

### Your decision

- [ ] Option 1 — <Stay-as-is>
- [ ] Option 2 — <name>
- [ ] Option 3 — <name>
- [ ] Other: ___________________

### Your rationale

<One or two sentences explaining WHY you picked this. the agent records this in the Decision Log so future you / future team can audit the reasoning.>

### Dependencies

This decision constrains:
- Decision <M> (e.g., Database Migration Tool — DMS doesn't migrate to Cosmos)

This decision depends on:
- Decision <K> (e.g., Hosting Platform — some frameworks only work on certain hosts)
```

## How to mark a decision DECIDED

After the user replies:

1. Tick the chosen option box: `- [x] Option 2 — Azure SQL Database`
2. Fill in the rationale field with the user's one-line reasoning.
3. Update the Status line at the top of the section:
   ```
   **Status:** ✅ DECIDED 2026-06-25
   ```
4. Update the Status summary table at the top of the file.
5. Append to `reports/Decision-Log.md` (see `decision-hardstop.md` Step 4).

## How to mark a decision N/A

If a decision genuinely doesn't apply (e.g., no database in this app), update:

```
**Status:** 🚫 N/A — <one-line reason>
```

Do not delete the section. Future re-assessments may flip N/A back to PENDING.

## How to mark a decision LOCKED

When one decision determines another, mark the dependent one LOCKED:

```
**Status:** 🔒 LOCKED — Determined by Decision 4 (Database Engine = Cosmos DB rules out DMS; using Cosmos DB Data Migration tool).
```

Add an entry to `Decision-Log.md` referencing the upstream decision.

## Example: a fully-decided section

```markdown
---

## Decision 1: Target framework / runtime version

**Status:** ✅ DECIDED 2026-06-25
**Required for:** Phase 2 — Migrate Code

### Why we're asking
.NET version determines support lifecycle, breaking changes, library compatibility, and team skill requirements for the next 3+ years.

### Your options
| # | Option | When to pick | Tradeoffs / risks |
|---|--------|--------------|-------------------|
| 1 | **Stay on .NET Framework 4.8.1** | Migration only (lift & shift). | Locked out of cloud-native features. Last resort. |
| 2 | **.NET 8 LTS** | You want mature LTS + low risk. | Support ends Nov 2026. May need re-upgrade soon. |
| 3 | **.NET 10 LTS** | Newest LTS, support through Nov 2028. | Larger jump from Framework 4.x. Some libraries lag. |
| 4 | **.NET 9 STS** | Only if you have a planned follow-up upgrade. | Short-term support — only 18 months. |

### Our default guess
⚠ Default guess: Option 3 (.NET 10 LTS), based on "newest LTS = longest runway." But the right answer depends on team familiarity and library compatibility.

### Your decision
- [ ] Option 1 — Stay on Framework 4.8.1
- [x] Option 2 — .NET 8 LTS
- [ ] Option 3 — .NET 10 LTS
- [ ] Option 4 — .NET 9 STS
- [ ] Other: ___________________

### Your rationale
Team is shipping production on .NET 8 elsewhere; library matrix is more proven; we'll re-evaluate moving to .NET 10 in early 2027 once .NET 8 EOL approaches.
```
