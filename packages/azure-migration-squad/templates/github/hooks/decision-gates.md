# Hook: Decision Gates

> Orchestration rules: **the squad never decides major architecture on behalf of the user**. It surfaces options and waits.

This hook is loaded by every migration chatmode (Migration-Orchestrator, Discovery-Intake, Code-Migration-Modernization, etc.) and applies to every agent in the squad. It is enforced via the Phase prompts' opening gates and the agent charters.

## Rule 1 — Read before acting

Before any agent does work that touches one of the decisions in [`decision-catalog.md`](../skills/decision-catalog.md), it MUST read `reports/Decisions-Required.md` and check the relevant decision's **Status**.

- If `✅ DECIDED <date>` → proceed using the recorded answer.
- If `⏸ PENDING` → STOP. Apply Rule 3 (ask format).
- If `🔒 LOCKED (by Decision N)` → use the locked-in answer.
- If `🚫 N/A` → skip this dimension entirely.
- If the file doesn't exist → STOP. Apply Rule 4 (file-missing).

## Rule 2 — Never assume

The squad does NOT:

- Assume defaults silently ("the user probably wants the newest version")
- Pick what "most projects use"
- Pick what's "Microsoft default"
- Pick to keep moving when a decision is ambiguous
- Treat user silence as consent
- Treat a brief / one-word user reply as confirmation of a multi-dimensional decision

If a major decision is needed and isn't recorded, **STOP and ask**.

## Rule 3 — Ask format (chat-native)

When stopping for a PENDING decision, post this exact pattern in chat:

```
🛑 DECISION REQUIRED — <Decision Name from catalog>

Why I'm asking: <one-line reason this can't be defaulted>

Your options:
1. <Stay-as-is option from catalog>  — <tradeoff>
2. <Option B>                        — <tradeoff>
3. <Option C>                        — <tradeoff>
4. Other                             — Tell me.

⚠ Our default guess is option <N> (<name>), but that's based only on
<visible evidence>. The right answer depends on factors I can't see
(team skills, contracts, budget, future roadmap).

Please reply with the option number and a one-line rationale,
OR update reports/Decisions-Required.md and tell me to re-read it.

I cannot proceed with <task name> until this is answered.
```

Then **stop**. Do not attempt the work with a guessed value.

**Stay-as-is is always option 1.** This forces the user to actively reject the conservative path.

## Rule 4 — File missing

If `reports/Decisions-Required.md` doesn't exist, the agent must NOT proceed and must NOT generate the file unilaterally. Respond with:

```
🚨 I cannot proceed because reports/Decisions-Required.md doesn't exist yet.

This file is produced by Phase 1 — Plan & Assess, which enumerates every
major architecture decision needed for your migration.

Please run:  /Phase1-PlanAndAssess
(or in CLI: "build the migration plan")

Once Phase 1 completes, I can resume work — but only against the decisions
you've actually made.
```

## Rule 5 — Recording

When the user replies with a choice:

1. Confirm understanding back in one sentence ("Got it — you want Azure SQL Database; I'll lock that in.")
2. Append to `reports/Decision-Log.md` with timestamp, choice, rationale, and your evidence.
3. Update `reports/Decisions-Required.md` Status line to `✅ DECIDED <ISO date>`.
4. Auto-lock any downstream decisions per catalog `locks_downstream`.
5. THEN proceed with the work the user originally asked for.

## Rule 6 — Recommendation discipline

A recommendation is allowed, but it must:

- Be labeled **default guess**, never "best choice" or "recommended."
- Cite **only visible evidence** (Capability Matrix, repo content, stated user goals).
- Acknowledge invisible factors ("the right answer depends on factors I can't see").
- Be a single option (not "it depends" — if you can't pick one, don't recommend).

**Silent acceptance ≠ consent.** If user doesn't reply within a chat turn, the agent does not proceed. It re-prompts.

## Rule 7 — Hard rules

1. No silent defaults. Ever.
2. No "I'll just pick one to keep moving."
3. No expert-mode bypass.
4. No "the user said go fast so I'll skip the question."
5. Don't expand the catalog implicitly. Adding a new mandatory question requires a catalog PR.
6. Don't shrink the catalog implicitly. If a decision genuinely doesn't apply, mark it `🚫 N/A` with reason — never delete.

## Rule 8 — Dispatching agents must propagate the gate

When the orchestrator dispatches a specialist (Architect, Database Specialist, DevOps Engineer, etc.), the dispatched agent inherits these rules. Specialists may not bypass them by "being more confident in my domain."

The specialist's job in the squad is to:
- **Read the catalog**
- **Lay out the alternatives**
- **Wait for the user**

NOT to "tell the user what they should do because I'm the specialist." Specialists provide expertise as evidence for the user's choice — they don't replace the user's choice.

## See also

- [`decision-hardstop.md`](../skills/decision-hardstop.md) — the binding protocol
- [`decision-catalog.md`](../skills/decision-catalog.md) — the canonical list
- [`decisions-required-template.md`](../skills/decisions-required-template.md) — the file structure
