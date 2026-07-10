# Skill Anatomy — reference for `skill-creator`

> Loaded on demand by `.github/skills/skill-creator.md` when authoring a new skill. Explains the two skill shapes (single-file vs folder-form), progressive disclosure, and when to add scripts / references / assets.

## Two skill shapes

### 1. Single-file skill (default — 90% of our skills)

Layout:
```
.github/skills/<family>-<name>.md
```

Use when the skill fits in ~200-500 lines of markdown. This is the shape of every `stack-*.md`, `source-*.md`, `workload-*.md`, and most other skills in this repo. The file has YAML frontmatter + a markdown body with the family's canonical sections.

**Rule of thumb**: if you're not sure, start single-file. Split into folder-form later if needed.

### 2. Folder-form skill (complex, multi-file)

Layout:
```
.github/skills/<skill-name>/
├── SKILL.md          (required — main entry point)
├── references/       (optional — docs loaded on demand)
│   ├── <topic>.md
│   └── <topic>.md
├── templates/        (optional — files copied into user's project)
│   ├── <template>.bicep
│   └── <template>.yml
├── examples/         (optional — worked examples)
│   └── <example>.md
└── scripts/          (optional — helper scripts, e.g., .py or .mjs)
    └── <helper>.py
```

Use folder-form when:
- The skill is >500 lines OR needs supporting resources
- You have templates (Dockerfiles, Bicep, YAML) that get copied into user projects
- You have reference docs that shouldn't always be loaded (progressive disclosure)
- You have helper scripts (Python / Node / shell) that automate part of the skill

**Examples of folder-form skills in our repo:**
- `.github/skills/azure-containerization/` — has `templates/` for Dockerfiles
- `.github/skills/azure-infrastructure/` — has `templates/` for Bicep + Terraform
- `.github/skills/migration-strategy-report/` — has `references/`, `scripts/` (Python), rich content
- `.github/skills/business-logic-mapping/` — has `examples/` in multiple languages
- `.github/skills/dotnet-modernization/`, `java-modernization/`, `wcf-to-rest-migration/`, `migration-unit-testing/` — all have `templates/`

## Progressive disclosure (three loading levels)

Loosely modeled on Anthropic's spec — sized for a Copilot Chat agent:

**Level 1 — Metadata (always loaded when the agent's context is initialized)**
- Skill name
- Description (the primary triggering mechanism)
- Family + triggers
- Cost: ~100 words of context per skill × ~66 existing skills = manageable

**Level 2 — SKILL.md body (loaded when the skill is triggered)**
- Full markdown body of the skill file
- Cost: 500-1000 lines of content per skill
- Only loaded for skills whose triggers match — typically 3-6 per migration turn

**Level 3 — Bundled resources (loaded on demand)**
- `references/` — extra docs the agent reads only when needed
- `templates/` — copied into the user's project as-is
- `examples/` — read only when the agent needs a worked example
- `scripts/` — executed as tools, not loaded into context

**When to move content from Level 2 → Level 3:**
- If a skill exceeds ~500 lines, move the deep-dive sections into `references/<topic>.md`
- Add a pointer in SKILL.md: `> For <specific topic>, see \`references/<topic>.md\`.`
- Only pointers are Level 2; the reference content stays Level 3

## YAML frontmatter — required fields

Every skill starts with YAML frontmatter. Required for both single-file and folder-form skills (in folder-form, it lives at the top of `SKILL.md`).

```yaml
---
name: <family>-<short-name>
description: |
  <one-line-ish description — see writing rules below>
family: <stack | source | workload | integration | pattern | risk | other>
triggers: <comma-separated values from Capability Matrix that should invoke this>
---
```

### `name`

- Lowercase, hyphen-separated
- Matches the filename (minus `.md`)
- For folder-form skills, matches the folder name
- Examples: `stack-elixir`, `source-as400`, `workload-iot-edge`, `integration-ibm-mq`, `pattern-com-plus-interop`, `risk-data-sovereignty`

### `description`

The primary triggering mechanism. **Models tend to undertrigger — descriptions must be specific about triggering contexts and slightly pushy.**

Rules:
1. Start with the family name and what it does — 1 sentence
2. Follow with **when** to load — Capability Matrix values, file evidence, keywords
3. Follow with what topics it covers — 1-2 sentences
4. Total: 60-120 words

**Bad** (undertriggers):
```yaml
description: Elixir migration patterns.
```

**Good** (specific triggers, mildly pushy):
```yaml
description: Stack adapter for Elixir / Phoenix applications. Load whenever Capability-Matrix.stack.primary_stack is `elixir`, or when discovery finds `mix.exs`, `*.ex`, `*.eex`, `*.leex`, `*.exs` files, OR when the user mentions Elixir, Phoenix, Ecto, LiveView, BEAM, or Erlang/OTP in a migration context. Covers version upgrade paths (1.14 → 1.17), Azure hosting options (Container Apps, AKS, Functions custom handler), OTP supervision-tree cutover, ETS/Mnesia externalization, and Distillery/Mix.Release packaging.
```

### `family`

One of the fixed families:
- `stack` — language / framework adapter
- `source` — source environment adapter
- `workload` — workload pattern adapter
- `integration` — external system integration
- `pattern` — reusable migration pattern
- `risk` — migration risk / warning
- `other` — reserved (avoid if possible)

### `triggers`

Comma-separated list of Capability Matrix values or keywords that should cause the agent to load this skill. This is somewhat redundant with the description — but it's parseable, and enables tooling to build a skill-router later.

Examples:
- `elixir, phoenix, mix, ecto` (stack)
- `as400, iseries, i5os, ibm-i` (source)
- `iot-edge, mqtt-broker, edge-compute` (workload)
- `ibm-mq, websphere-mq, mq-series` (integration)

## Body sections per family

Each family has canonical sections. Follow them — they enable other agents to find information quickly.

See `references/skill-template.md` for copy-paste starters.

## Writing style rules

1. **Imperative form** — "Use App Service when...", "Load the sub-stack skill matching..."
2. **Explain the WHY** — don't just say "ALWAYS use X". Say why. Models are smart; they respond well to reasoning.
3. **Avoid heavy-handed MUSTs** — reserve for real safety issues (secrets, data loss, security). Overuse dilutes their signal.
4. **Tables for comparisons** — sub-stacks, sizing, tradeoffs, options
5. **Code fences for exact syntax** — bash commands, YAML config, JSON payloads
6. **Progressive complexity** — start simple, add nuance later in the section. Not everyone needs the deep-dive.

## Length guide

| Content | Approximate length |
|---------|-------------------|
| Small pattern / risk skill | 100-250 lines |
| Stack / source / workload skill | 250-500 lines |
| Complex folder-form skill | 500-2000 lines total (with SKILL.md ≤500) |

## Common pitfalls

1. **Description too generic** — "Elixir migration patterns" → undertriggers. Be specific about WHEN.
2. **No `Azure Targets` section** — every stack/workload skill must map to concrete Azure services.
3. **No `References` section** — undermines trust; makes updates hard.
4. **Rewriting content instead of citing** — link to Microsoft Docs / vendor docs; don't paraphrase 3 paragraphs of official content.
5. **Making assumptions the user hasn't made** — never assume target framework, hosting platform, or IaC tool. See `decision-hardstop.md`.
6. **Copying `.NET` or `Java` patterns verbatim** — for a new stack, adapt language-specific idioms (Python's `logging` module, not .NET's `ILogger`).

## Sync + distribution

Any new skill file created under `.github/skills/`:

1. Is picked up automatically by `scripts/sync-templates.mjs` on the next build (no manual registration)
2. Ships in the VS Code extension's next `.vsix` (bundled as a workspace template)
3. Appears in the extension's sidebar tree view under **Add-ons > Specialized deep-dives** or the equivalent group (based on family)
4. Is discoverable by the agent on the next turn (SessionStart hook loads `.github/skills/` content into context)

No separate registration file. No manifest to update. Just create the `.md` file and it flows through.

## When to escalate to a folder-form skill

Signs a single-file skill is outgrowing its shape:

- The file is >500 lines
- You have >3 templates the user should copy into their project
- You have topic areas that should be loaded selectively (progressive disclosure)
- You have executable helper scripts

To escalate:

1. Create `.github/skills/<name>/` folder
2. Move the old file to `<name>/SKILL.md`
3. Split deep-dive sections into `<name>/references/<topic>.md`
4. Add pointers in `SKILL.md` to each reference file
5. Add templates to `<name>/templates/`
6. Update the `description` in frontmatter to mention the new resources
7. Log the reshape as an Action Log entry with `action=reshaped-skill`

## References

- Anthropic's skill-creator: https://github.com/anthropics/skills/tree/main/skills/skill-creator
- Existing folder-form examples in this repo: `.github/skills/azure-containerization/`, `.github/skills/migration-strategy-report/`
- Existing single-file examples: `.github/skills/stack-python.md`, `.github/skills/source-aws.md`, `.github/skills/workload-webapp.md`
