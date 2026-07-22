# Skill: Skill Creator — author new migration skills on the fly

> When the migration agent detects a gap — a stack, source environment, workload pattern, integration, migration pattern, or risk that no existing skill covers — this meta-skill authors a new skill file in `.github/skills/` **in the same session**, so the current migration and every future migration benefits.

**When to use this skill** (agent invokes proactively, does NOT wait for the user to ask):

- The Capability Matrix would classify `stack.primary_stack` as a value with **no matching `.github/skills/stack-*.md`** — e.g., discovered app is Elixir/Phoenix but only `stack-elixir.md` is missing
- Similar for `source.primary_adapter` (no `source-*.md`), `workload.primary_pattern` (no `workload-*.md`), any integration in `integrations` (no `integration-*.md`), or a risk with no `risk-*.md`
- A phase prompt encounters a **recurring migration pattern** that would help future migrations (e.g., "COM+ interop replacement", "custom RMI-over-SSL transport") — create a `pattern-*.md`
- The user explicitly says "create a skill for X", "add a skill", "we need a skill for this", "research this and create a skill", or types `/skill-creator`

**Default behavior:** ALWAYS ask a short Y/n confirmation before writing (see Step 2 below). Default is Yes. Never silently create files.

---

## Overview

At a high level, on-the-fly skill creation follows this flow:

1. **Detect the gap** — enumerate the value that has no matching skill file
2. **Confirm with the user** — one short Y/n/N-for-this-session prompt
3. **Research** — use `web` / `fetch` / `githubRepo` tools to gather authoritative docs (3-5 sources)
4. **Draft the skill** using the family template from `references/skill-template.md`
5. **Smoke-test** — check the new file against the anatomy in `references/skill-anatomy.md`
6. **Log the creation** to `reports/Report-Status.md` via the Action Log Contract (see `action-log-format.md`)
7. **Continue the migration** using the newly-authored skill

The whole flow should take **~2-5 minutes** including research. This is a *lightweight* meta-skill — do not build a full eval-viewer or SDK loop. If the skill turns out to be low-quality, the user can refine it in a follow-up turn.

## Skill families this meta-skill can create

The output goes into `.github/skills/` following our existing naming convention. Pick the right family up-front:

| Family | Filename pattern | Use when |
|--------|------------------|----------|
| **Stack** | `stack-<name>.md` | New language/framework — Elixir, Clojure, Erlang, Haskell, F#, D, Zig, Nim, Crystal, Julia, Racket, Lua, R, MATLAB, etc. |
| **Source** | `source-<name>.md` | New source environment — Nutanix, HP-UX, Solaris, OpenVMS, custom on-prem appliance, private cloud not covered (mainframe / IBM i / midrange should NOT be handled here — route to `source-unsupported-escalation.md` instead) |
| **Workload** | `workload-<name>.md` | Unusual workload pattern — IoT edge device, HPC cluster job, machine-learning training pipeline, real-time trading system, media-encoding farm |
| **Integration** | `integration-<name>.md` | External system integration — TIBCO EMS, MuleSoft, SAP RFC, Kerberos-only realm, Novell eDirectory |
| **Pattern** | `pattern-<name>.md` | Reusable migration pattern — COM+ interop replacement, custom RMI-over-SSL transport, session-state externalization, thick-client to web-client |
| **Risk** | `risk-<name>.md` | Migration risk — data-sovereignty jurisdiction change, latency-sensitive DR failover, third-party dependency EOL, licensing constraint |

If unsure which family, ask the user. Do not create a skill in the wrong family — it makes discovery harder for future agents.

## Step 1: Detect the gap

Detection is automatic and happens during Discovery (`/assess-any-application`) or `/Phase1-Plan`. The Skill Gap Check step in those prompts:

1. Reads the `Capability-Matrix.yaml` values (or the in-progress classification if not yet written)
2. For each axis, does a `file_search` in `.github/skills/` for a matching filename:
   - `stack.primary_stack: elixir` → look for `stack-elixir.md`
   - `source.primary_adapter: nutanix` → look for `source-nutanix.md`
   - `workload.primary_pattern: iot-edge` → look for `workload-iot-edge.md`
   - each entry in `integrations[]` → look for `integration-<name>.md`
3. **Any miss → gap detected. Invoke this skill.**

For pattern and risk families, detection is opportunistic — a phase prompt may notice a recurring pattern and hand it off to this skill.

**Announce the gap plainly** before Step 2:

> *"I've classified this app's stack as **Elixir/Phoenix**, but I don't yet have a `stack-elixir.md` skill. Without it, Phase 2 (code migration) won't know Elixir-specific patterns for Azure hosting, dependency management, or observability."*

## Step 2: Confirm with the user

Ask **one short question**, exactly like this:

> **I don't have a skill for `<value>` as a `<family>`. I can create one now — I'll research authoritative docs (~2-5 min) and write the skill so this migration and future migrations benefit. Should I proceed? [Y / n / N-for-this-session-only]**
>
> - **Y** (default) — create the skill now
> - **n** — skip this specific gap; continue the migration with reduced guidance
> - **N-for-this-session-only** — skip all skill-gap prompts for the rest of this session

**Default is Y.** Do not require the user to type it; treat an empty response or `<enter>` as Y.

Log the user's response to Action Log:

```
- <UTC> | actor=skill-creator | action=gap-confirmed | value="<family>-<name>" | tokens=~0 | turn=<n> | notes="user chose Y|n|N-for-session"
```

If **n** or **N-for-session** — skip Steps 3-7 and continue the migration. Log the skip.

## Step 3: Research

For any Y answer, gather 3-5 authoritative sources using the tools you have.

**Preferred sources per family:**

- **Stack** — official language docs, framework docs, Azure App Service / Container Apps / Functions runtime docs for that language, LTS release notes, migration guides from major versions
- **Source** — vendor docs (IBM, HP, Oracle, VMware), Azure Migrate compatibility matrix, third-party migration case studies
- **Workload** — Azure Well-Architected Framework guidance for the workload, Azure Architecture Center reference architectures, CNCF landscape (for cloud-native workloads)
- **Integration** — vendor connector docs, Azure integration options (Service Bus, Logic Apps, APIM, Event Grid), community migration write-ups
- **Pattern** — RFCs, standards bodies, .NET / Java / Python community best practices for the specific pattern
- **Risk** — Azure compliance docs (Trust Center, CAF), Microsoft Learn, industry regulator publications

**Tools to use:**

- `web` — fetch official docs, blog posts, migration case studies
- `fetch` — retrieve specific URLs the user cites
- `githubRepo` — inspect reference implementations
- `Azure MCP` / `Microsoft Docs` (if available) — first-party Azure guidance
- `search/codebase` (this repo) — check if we already have partial coverage in a related skill

**Time budget:** 3-5 sources, 2-3 minutes of fetching. Do NOT go deeper unless the user explicitly asks. Skill-creator is a **fast path**, not a research assistant. Cite each source in a `## References` section at the bottom of the new skill.

## Step 4: Draft the skill

Load `references/skill-template.md` and pick the section matching the target family. Copy the template into a new file at `.github/skills/<family>-<name>.md`, then fill in:

1. **YAML frontmatter** (required):
   ```yaml
   ---
   name: <family>-<name>
   description: <one-line description — see Description Writing rules below>
   family: <stack | source | workload | integration | pattern | risk>
   triggers: <comma-separated Capability Matrix values that should invoke this>
   ---
   ```

2. **Body sections** (in order — follow the family's template exactly):

   For **stack** family:
   - `## When to Use` (with Capability Matrix trigger + file evidence)
   - `## Sub-Stack Detection` (table: sub-stack | detection signal | typical Azure target)
   - `## Version Compatibility with Azure` (which versions of the runtime work on which Azure PaaS)
   - `## Migration Patterns` (common patterns for making the stack Azure-compatible)
   - `## Configuration Transformation` (how to swap on-prem config for Azure-native)
   - `## Authentication → Entra ID` (SDK reference)
   - `## Observability → Application Insights` (SDK / OpenTelemetry reference)
   - `## Tradeoffs` (when to rehost vs replatform vs refactor)
   - `## References` (3-5 citations from Step 3)

   For **source** family:
   - `## When to Use`
   - `## Access Method` (how to extract code/config/data from this source)
   - `## Discovery Approach` (what to inventory before migrating)
   - `## Azure Landing Zone Options` (which Azure targets are compatible)
   - `## Common Blockers` (things this source has that Azure doesn't)
   - `## Escalation Path` (when to call in specialist tools/partners)
   - `## References`

   For **workload** family:
   - `## When to Use`
   - `## Workload Shape` (traffic pattern, latency, scale)
   - `## Azure Targets` (table: option | best for | tradeoffs)
   - `## Migration Approach per Strategy` (rehost / replatform / refactor / rearchitect / rebuild)
   - `## Data + State Considerations`
   - `## Cutover Pattern`
   - `## References`

   For **integration** family:
   - `## When to Use`
   - `## Protocol/Transport` (what this integration uses)
   - `## Azure Equivalents` (which Azure service or third-party maps to it)
   - `## Migration Approach` (in-place adapter vs replatform vs replace)
   - `## Security + Identity Considerations`
   - `## References`

   For **pattern** family:
   - `## When to Use`
   - `## The Pattern` (what it is; typical implementation)
   - `## Why It Blocks Azure` (what makes it incompatible)
   - `## Replacement Options` (Azure-native alternatives)
   - `## Migration Steps`
   - `## References`

   For **risk** family:
   - `## When to Use`
   - `## The Risk` (what could go wrong)
   - `## Severity + Likelihood` (framework)
   - `## Detection Signals` (how to spot it in an app)
   - `## Mitigations`
   - `## Escalation Path`
   - `## References`

### Description Writing rules

The `description` in YAML frontmatter is the primary triggering mechanism for the agent. Anthropic's spec calls out that models tend to **undertrigger** — they don't invoke skills they should. To combat this, make the description **specific about triggering contexts** and slightly pushy:

**Bad** (undertriggers):
```yaml
description: Migration patterns for Elixir applications.
```

**Good** (specific triggers, mildly pushy):
```yaml
description: Stack adapter for Elixir / Phoenix applications. Load whenever Capability-Matrix.stack.primary_stack is `elixir`, or when discovery finds `mix.exs`, `*.ex`, `*.eex`, `*.leex`, `*.exs` files, OR when the user mentions Elixir, Phoenix, Ecto, LiveView, BEAM, or Erlang/OTP in a migration context. Covers version upgrade paths (1.14 → 1.17), Azure hosting options (Container Apps, AKS, Functions custom handler), OTP supervision-tree cutover, ETS/Mnesia externalization, and Distillery/Mix.Release packaging.
```

Keep to 100 words. Cover WHAT + WHEN + KEY TOPICS.

### Section length guide

Total skill length should target **300-500 lines**. Larger stacks/sources may need more. If you approach 500 lines and the content is still valuable, split into `skill-name/SKILL.md` + `skill-name/references/*.md` (folder-form skill; see `references/skill-anatomy.md`).

## Step 5: Smoke-test

Before saving, walk this **manual checklist**:

- [ ] YAML frontmatter has `name`, `description`, `family`, `triggers`
- [ ] `description` is specific about WHEN to load (Capability Matrix values, file evidence, keywords)
- [ ] All the family's required sections are present and non-empty
- [ ] At least 3 citations in `## References`
- [ ] File compiles as valid markdown (no unclosed code fences, no broken tables)
- [ ] Filename matches `<family>-<name>.md` (lowercase, hyphen-separated)
- [ ] Skill length is 200-500 lines (unless a folder-form skill is being created for larger content)

If any check fails, fix before saving.

## Step 6: Log the creation

Append a line to `reports/Report-Status.md` in the `## 📜 Action Log` section using the Wave O format:

```
- <ISO-8601-UTC> | actor=skill-creator | action=created-skill | files=+.github/skills/<family>-<name>.md | tokens=~8k | turn=<n> | notes="family=<family>, sources=<count>"
```

Also log a second entry when the skill is first *used* by a downstream phase — this proves the new skill actually paid off:

```
- <ISO-8601-UTC> | actor=<PhaseX> | action=loaded-skill | files=~.github/skills/<family>-<name>.md | tokens=~0 | turn=<n> | notes="first use of newly-created skill"
```

## Step 7: Continue the migration

**Do not stop after skill creation.** The whole point is to unblock the migration. Immediately after logging:

1. Return control to whatever phase was running (Discovery, Phase 1, etc.)
2. Have the phase re-classify or re-load with the new skill available
3. Continue as if the skill had existed all along

## Iteration and refinement

The first draft of an on-the-fly skill will not be perfect. That's OK — the user will refine it over time. If a subsequent turn in the same session reveals a gap in the skill (e.g., a version compatibility note was missed), the user can say "update the elixir skill" or the agent can proactively offer an edit.

For **major refinements**, invoke skill-creator again with the `--refine` mode (see below).

### Refine mode (`--refine`)

If the user says "the elixir skill is missing X" or "revise the source-nutanix skill", enter refine mode:

1. Load the existing skill file
2. Load the specific gap noted by the user
3. Re-fetch relevant sources (2-3, not 3-5)
4. Add or update the affected sections only — do NOT rewrite the whole file
5. Preserve existing citations; add new ones with dated fetch notes
6. Log to Action Log: `action=refined-skill | files=~.github/skills/<family>-<name>.md | notes="refinement=<what>"`

## Trigger Accuracy Checklist

After creating a skill, once the migration continues, watch for these signals in the next 1-2 turns:

- [ ] Did the newly-created skill actually get loaded by the next phase? (Check `loaded-skill` in Action Log)
- [ ] Did the phase produce output that referenced patterns from the new skill?
- [ ] Any confusion from the agent about which skill to load (over-triggering or under-triggering)?

If under-triggering, the `description` needs to be more pushy — edit it to be more specific about WHEN.
If over-triggering, the `description` is too broad — narrow the triggering contexts.

## What this meta-skill is NOT

- **Not a full eval-viewer / SDK loop** — Anthropic's skill-creator ships a Python + HTML review harness for benchmarking skills at scale. That's out of scope for a CLI agent. Our smoke-test + trigger-accuracy-checklist is intentionally lightweight.
- **Not for creating agent files or prompt files** — those live in `.github/agents/` and `.github/prompts/` and have different conventions.
- **Not for creating chatmodes** — those live in `.github/chatmodes/` and require different YAML frontmatter.
- **Not for creating templates** — templates for reports (e.g., `migration-report-template.md`) are hand-authored.

## References

- Anthropic's canonical skill-creator: https://github.com/anthropics/skills/tree/main/skills/skill-creator
- Our anatomy reference: `.github/skills/references/skill-anatomy.md`
- Our starter templates: `.github/skills/references/skill-template.md`
- Action Log Contract: `.github/skills/action-log-format.md`
- Existing skill families to model after: `.github/skills/stack-*.md`, `.github/skills/source-*.md`, `.github/skills/workload-*.md`
