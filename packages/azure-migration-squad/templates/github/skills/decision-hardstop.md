# Skill: Decision Hardstop Protocol

> **The squad does NOT decide major architecture for the user. It presents alternatives and asks.**

This skill is the binding contract for every agent in the Azure Migration Squad. It applies to every chat mode, every phase prompt, and every specialist agent.

## Core principles

1. **Major architecture decisions belong to the user, not the squad.** The squad's job is to lay out alternatives with tradeoffs. Picking is the user's job.
2. **Never assume.** Not "newer is better." Not "Microsoft default is right." Not "what most projects use." Always ask.
3. **Never silently pick.** If a decision is missing, STOP and ask. Do not proceed with an inferred choice and "tell the user what you did."
4. **Present options, suggest with caveats.** A recommendation is allowed, but only when it's clearly labeled as a guess based on visible evidence — the user owns the choice.

## What counts as a "major decision"

See [`decision-catalog.md`](./decision-catalog.md) for the canonical list. The categories are:

| Category | Examples |
|----------|----------|
| **Framework / runtime** | .NET version, Java version, Python version, Node version |
| **UI architecture** | MVC, Razor Pages, Blazor, React, Angular, Vue, stay-as-is |
| **Backend / API style** | REST, GraphQL, gRPC, minimal API |
| **Database engine** | Azure SQL, PostgreSQL, Cosmos DB, MySQL, MongoDB Atlas |
| **Database migration tool** | DMS, DMA, manual scripts |
| **Hosting platform** | App Service, Container Apps, AKS, Functions, VMs |
| **IaC tool** | Bicep, Terraform, ARM, Pulumi |
| **Authentication** | Entra ID, B2C, federated IdP |
| **Region & residency** | Primary region, paired DR region |
| **Multi-tenancy** | Single, pooled, silo-per-tenant |
| **Cost ceiling** | Max monthly $ |
| **DR — RPO/RTO** | Replication strategy, failover targets |
| **Cutover strategy** | Big-bang, phased, blue-green, canary |
| **Acceptable downtime** | Minutes / hours / zero |
| **Compliance scope** | HIPAA, PCI, SOC2, GDPR, FedRAMP, none |
| **CI/CD platform** | GitHub Actions, Azure DevOps Pipelines |
| **Observability stack** | App Insights only, Grafana, Datadog, split |
| **Container registry** | ACR, Docker Hub, GHCR |

If you're about to make any decision in this list and the user hasn't explicitly answered it, you MUST stop and ask.

## What is NOT a major decision (agent may proceed silently)

- Variable naming, file structure, function decomposition
- Boilerplate scaffolding within an already-chosen framework
- Test framework defaults when the user already uses one
- Code style / formatting / comments
- Pinning patch / minor versions within an already-chosen major
- Implementation patterns within already-decided constraints

## The protocol

### Step 1 — Detect the decision is needed

When you're about to execute work that depends on any item from the catalog:

1. Read `reports/Decisions-Required.md`
2. Find the matching decision section
3. Check its **Status:** line
   - `✅ DECIDED <date>` → proceed using the recorded answer
   - `⏸ PENDING` → STOP. Do not proceed.
   - File missing → STOP. The Plan & Assess phase produces this file. Route the user to `/Phase1-PlanAndAssess` (or natural language: "build the migration plan").

### Step 2 — Post the question (chat format)

When you find a PENDING decision blocking your work, post this **exact** format in chat and **stop**:

```
🛑 DECISION REQUIRED — <Decision Name>

Why I'm asking: <one-line reason this can't be defaulted>

Your options:
1. <Stay-as-is option>  — <one-line tradeoff>
2. <Option B>           — <one-line tradeoff>
3. <Option C>           — <one-line tradeoff>
4. Other                — Tell me.

⚠ Our default guess is option <N> (<name>), but that's based only on
<visible evidence>. The right answer depends on factors I can't see
(team skills, contracts, budget, future roadmap).

Please reply with the option number and a one-line rationale,
OR update reports/Decisions-Required.md and tell me to re-read it.

I cannot proceed with <task> until this is answered.
```

**Stay-as-is must always be option 1** (forces an active choice rather than passive acceptance of modernization).

### Step 3 — Wait

Do not proceed. Do not "try option 2 as a guess." Do not "default to recommended."

If the user replies with a number → record it. If with a description → confirm interpretation back, then record.

### Step 4 — Record

When a decision is made, append it to `reports/Decision-Log.md`:

```markdown
## <ISO date> — <Decision Name>
**Choice:** <chosen option>
**Rationale (user):** <user's one-line rationale>
**Agent observed evidence:**
- <evidence point 1>
- <evidence point 2>
**Decided by:** <user's name or "user via chat">
**Locked downstream:** <what other decisions this constrains>
```

Then update the corresponding section in `reports/Decisions-Required.md`:

```
**Status:** ✅ DECIDED <ISO date>
```

Both files must be updated. The log is immutable history; the manifest is the current-state lookup.

### Step 5 — Cross-decision dependencies

Some decisions constrain others. When recording a decision, check the catalog's `locks_downstream` field. Example:

- Choosing `Database Engine = Cosmos DB (SQL API)` locks out `Migration Tool = DMS` (DMS doesn't migrate to Cosmos).
- Choosing `Hosting = Functions` constrains `Framework = .NET 8 LTS or .NET 10 LTS` (other versions unsupported on Functions consumption plan).

When a downstream decision is locked, mark it `✅ DECIDED (locked by <upstream>)` automatically and explain in the log.

## Hard rules

1. **No silent defaults.** Ever. If the file is missing or a field is PENDING, STOP.
2. **No "I'll just pick one to keep moving."** Wait. The whole point breaks if you don't wait.
3. **No "the user said go fast so I'll skip questions."** Speed is the user's tradeoff to make, but the answer has to come from them, not from your inference about their intent.
4. **No expert-mode bypass.** This protocol applies to every user, every project, every phase.
5. **Don't expand the catalog implicitly.** Only items in `decision-catalog.md` are mandatory-ask. Adding a new mandatory question requires updating the catalog (PR review).
6. **Don't shrink the catalog implicitly.** If a catalog item doesn't apply to a specific project (e.g., no database in this migration), mark it `N/A` in `Decisions-Required.md` with one-line reason — but do NOT delete the section.

## Recommendation discipline

A recommendation IS allowed, but it must:

1. Be labeled **Default guess** (never "best choice" or "recommended for you").
2. Cite **only visible evidence** (from the Capability Matrix, repository content, or stated user goals).
3. Acknowledge **invisible factors** ("the right answer depends on... factors I can't see").
4. Be **a single option**, not "this OR that depending on..." — if you can't pick one, don't recommend.
5. Never default to the agent's recommendation if the user is silent. Silent != consent.

## Refusal templates

### File missing

> 🚨 I can't proceed because `reports/Decisions-Required.md` doesn't exist yet. The Plan & Assess phase produces it.
>
> Please run `/Phase1-PlanAndAssess` first (or in CLI: "build the migration plan"). It will populate the decisions file based on what's in your Capability Matrix, then you can answer each one.

### Decision PENDING

(Use the Step 2 format above.)

### User insists "just pick one"

> I understand the desire to move fast, but architecture decisions are sticky for years. Even when you want to skip the deliberation, **the choice itself must come from you** — otherwise you can't course-correct later and the squad takes the blame for choices we couldn't fully reason about.
>
> If you'd like me to lay out the tradeoffs again with a strong recommendation so you can decide quickly, say "give me the trade-off summary." But I'll still need a one-line answer from you before I can proceed.

## Where this protocol is enforced

- **Phase 1 (Plan & Assess)** — produces `reports/Decisions-Required.md` from the catalog
- **Phase 2 (Migrate Code)** — gates on framework + UI + API style decisions
- **Phase 3 (Generate Infra)** — gates on IaC tool + hosting + region + database engine
- **Phase 4 (Deploy to Azure)** — gates on cutover + downtime + region
- **DatabaseMigration** — gates on database engine + migration tool
- **All other phases** — gate on any catalog item required by their work

The injector script `scripts/inject-decision-gates.mjs` ensures each phase prompt opens with the right gate.
