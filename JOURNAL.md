# JOURNAL.md — Build Story

> How this project was built, the steering moments that shaped it, and why things are the way they are.
> Maintained by **Scribe** (Historian / Build Journalist). Update after milestones.

## 2026-05-29 — PPTX Generators Synced to Ocean's Fourteen

### What Happened

Updated the active PPTX generator set under `docs\pptx\generators\` so the live squad decks now say **Ocean's Fourteen**, show 14-agent counts, include Tess Ocean and The Accountant in roster views, and emit the renamed flagship comparison deck `Oceans_Fourteen_Squad_vs_Prompting.pptx`. Also rebalanced roster slide layouts in the comparison and sample squad decks so the extra specialists fit without touching the shared LATAM helper module.

### Why

The deck library had drifted behind the repo's live squad state. That made presentation assets risky: the codebase already knew about agents #13 and #14, but several slides still sold a 12-agent story.

### Steering Moment

The key choice was to update only the deck-local generator logic and layout math instead of refactoring shared PPTX helpers. That kept the change surgical, honored the no-shared-module rule, and let each deck preserve its own visual style while still landing the current roster.

### Impact

Deck regeneration will now produce presentation assets that match the current Ocean's Fourteen identity and specialist roster, which reduces demo drift and keeps stakeholder-facing materials aligned with the repo's operating model.

---

## 2026-05-29 — README Synced to the 14-Agent Current State

### What Happened

Updated `README.md` in one pass to reflect the live Ocean's Fourteen surface: renamed the title and identity references, fixed 14-agent counts, added The Accountant to the crew roster, added the missing Developer Tools entries, documented the CI workflows, refreshed repository structure details, and called out the Onboarding chatmode in training guidance.

### Why

The README had become a drift zone after the FinOps expansion, onboarding additions, health automation, and prompt-governance tooling landed. New operators could still learn the repo, but they were learning from stale counts and missing capabilities.

### Steering Moment

The key choice was to update only the stale facts instead of rewriting sections wholesale. That preserved the README's current structure and voice while bringing the operator-facing inventory back into sync with the repository.

### Impact

The repo front door now accurately describes the 14-agent squad, current tools, current workflows, and current onboarding path, which makes validation, adoption, and stakeholder walkthroughs less error-prone.

---

## 2026-05-29 — Agent #14 The Accountant Joined to Own Cost Intelligence

### What Happened

Added Agent #14, **The Accountant** / **Cost Engineer**, as the squad's dedicated FinOps specialist. Created a new charter, updated the squad roster and routing rules, switched the Cost Optimization prompt/chatmode lead to Cost Engineer, and extended the hook surface with cost-aware dispatch, gate, and checklist coverage.

### Why

Cost optimization was already part of the migration workflow, but ownership was still implicit under Azure Specialist. The squad needed one clearly named specialist to own right-sizing, budget guardrails, reservation guidance, and savings accountability after migration.

### Steering Moment

The key choice was to create a dedicated agent instead of stretching Azure Specialist further. Cost optimization has its own prompt, chatmode, operating vocabulary, and success metric — every recommendation should carry an estimated dollars-per-month impact — so it deserved an explicit owner.

### Impact

Cost, budget, spending, right-size, reserved instance, and savings work now route to a dedicated specialist. The squad can treat FinOps as a first-class migration outcome alongside architecture, security, deployment, and operations.

---

## 2026-05-29 — Root Skills Catalog Reframed as Reference-Only

### What Happened

Clarified the root `skills/` folder as a reference catalog, rewrote `skills/INDEX.md`, updated `skills/README.md`, stamped duplicated root skill files with `REFERENCE ONLY`, and confirmed prompts under `.github/prompts/` do not point at root `skills/`.

### Why

The repo needed one unmistakable prompt-authoring source of truth while still preserving a broader skills catalog for browsing and reuse.

### Steering Moment

The key move was to preserve the root catalog instead of deleting or relocating it, while making `.github/skills/` the only authoritative prompt-local layer.

### Impact

Prompt authors now have a cleaner mental model, duplicate-path confusion is reduced, and future prompt references have a single canonical destination.

---

## 2026-05-29 — Heist Dashboard Added for Squad Health and Demo Readiness

### What Happened

Added `.squad\dashboard.html`, a polished single-file browser dashboard that presents the Ocean's Thirteen header, the current 14-agent roster, quick stats, visual placeholders for linter/eval JSON, copyable operator commands, and a timestamp panel.

### Why

The squad had strong validation scripts, but no showcase surface that turned those results into something easy to demo or scan quickly. A static dashboard closes that gap without introducing a server, build step, or external dependency.

### Steering Moment

The key choice was to keep the dashboard entirely self-contained and treat health results as pasted or loaded JSON instead of wiring live process execution into the page. That preserved the zero-setup requirement while still making the linter and evaluator feel visual and operator-friendly.

### Impact

Operators now have a local control-room artifact they can open instantly, use in demos, and refresh with exported health payloads while keeping the repo's governance commands one copy-paste away.

---

## 2026-05-29 — Decisions Log Got a Terminal Timeline Viewer

### What Happened

Added `.squad\view-decisions.mjs`, a zero-dependency Node.js viewer for `.squad\decisions.md`, and verified it from the CLI so the squad can scan decision history without opening the raw markdown file.

### Why

The decision log had grown into durable repo memory, but it was becoming slower to skim for recent moves, monthly patterns, and repeated themes directly in terminal sessions.

### Steering Moment

The key choice was to keep the tool as a forgiving viewer instead of a validator: parse the existing heading-and-bullet pattern, infer status from section headings when explicit status lines are absent, support `--search` and `--last`, and always exit 0 even if the markdown shape is imperfect.

### Impact

Operators can now run `node .squad\view-decisions.mjs`, `node .squad\view-decisions.mjs --search "agent"`, or `node .squad\view-decisions.mjs --last 5` to inspect the timeline faster and carry less decision context in working memory.

---

## 2026-05-29 — Release Tags Can Now Generate PPTX Decks

### What Happened

Added `.github\workflows\pptx-generate.yml` so published GitHub releases can regenerate the deck library automatically, and operators can also run the workflow manually with a specific generator selector. The workflow installs the Python PPTX dependencies, resolves the LATAM template path, runs the matching `docs\pptx\generators\generate_*.py` scripts, and uploads the resulting `.pptx` files as release assets or workflow artifacts.

### Why

The repo already had a mature PPTX generator library, but regeneration was still a local/manual step that depended on whoever had the template file configured on their machine. That made release packaging inconsistent and easy to forget.

### Steering Moment

The key choice was to treat the workflow as best-effort automation instead of a critical gate. If the LATAM template is unavailable on the runner, the workflow emits a warning and skips generation cleanly rather than failing the whole release flow.

### Impact

Release tags now have a lightweight path to ship fresh deck assets when the template is available, and manual dispatch provides an easy way to regenerate one deck or the full set without relying on local-only steps.

---

## 2026-05-29 — Interactive Onboarding Chatmode Added

### What Happened

Added `.github\chatmodes\Onboarding.chatmode.md` as a first-run guided tour for new operators, then aligned the repo surface by updating README chatmode counts, the evaluator manifest, prompt version tracking, and onboarding docs to recognize the new entrypoint.

### Why

The squad had rich prompts, skills, hooks, and walkthroughs, but first-time users still had to reverse-engineer how the crew fit together before they could confidently start a migration workflow.

### Steering Moment

The key choice was to keep onboarding separate from `Migration-Orchestrator`. That preserves the orchestrator as an execution surface while giving new users a lower-pressure place to learn the agents, the prompts -> skills -> hooks stack, and the health checks that validate the repo.

### Impact

New contributors now have a dedicated heist-themed starting point that introduces all 13 agents, surfaces the most common workflows, and points directly to the files and commands that keep the squad healthy.

---

## 2026-05-29 — Interactive Onboarding Chatmode Added

### What Happened

Added `.github\chatmodes\Onboarding.chatmode.md` as a first-run guided tour for new operators, then aligned the repo surface by updating README chatmode counts, the evaluator manifest, prompt version tracking, and onboarding docs to recognize the new entrypoint.

### Why

The squad had rich prompts, skills, hooks, and walkthroughs, but first-time users still had to reverse-engineer how the crew fit together before they could confidently start a migration workflow.

### Steering Moment

The key choice was to keep onboarding separate from `Migration-Orchestrator`. That preserves the orchestrator as an execution surface while giving new users a lower-pressure place to learn the agents, the prompts -> skills -> hooks stack, and the health checks that validate the repo.

### Impact

New contributors now have a dedicated heist-themed starting point that introduces all 13 agents, surfaces the most common workflows, and points directly to the files and commands that keep the squad healthy.

---

## 2026-05-29 — Squad Health Checks Became a PR Gate

### What Happened

Added `.github\workflows\squad-health.yml`, a GitHub Actions workflow that runs `node .squad\lint-prompts.mjs` and `node .squad\eval.mjs` on pull requests that touch the squad's governance surface and on manual dispatch.

### Why

The repo already had the right governance checks, but they still relied on contributors remembering to run them locally. That made drift detectable in theory without making it reliably visible during review.

### Steering Moment

The key choice was to scope the workflow to governance-relevant paths instead of every change. That turns the canonical linter and evaluator into a practical review gate without adding noisy CI to unrelated edits.

### Impact

Prompt-library structure and squad-governance integrity now get validated before merge, making drift harder to introduce and easier to catch while the change is still in review.

---

## 2026-05-29 — Prompt Version Tracking Baseline Added

### What Happened

Added `.squad\prompt-versions.md` as a human-readable ledger for all 21 prompts and 7 chatmodes, created `.squad\track-versions.mjs` to hash every prompt/chatmode file, and initialized the machine baseline in `.squad\.prompt-hashes.json`.

### Why

Prompt quality work needed a fast way to see both the declared version of each asset and whether the file content had drifted since the last recorded baseline. Before this change, that state lived only in manual comparison and memory.

### Steering Moment

The key choice was to split the system into two layers: a markdown ledger for maintainers and a hash-based tracker for automation. That keeps version summaries readable while still giving the Evaluator a deterministic drift signal on every run.

### Impact

Future prompt and chatmode reviews can start from one command — `node .squad\track-versions.mjs` — and one ledger, making it easier to spot drift, update versions intentionally, and preserve a clear baseline for regression work.

---

## 2026-05-29 — Release Tags Can Now Generate PPTX Decks

### What Happened

Added `.github\workflows\pptx-generate.yml` so published GitHub releases can regenerate the deck library automatically, and operators can also run the workflow manually with a specific generator selector. The workflow installs the Python PPTX dependencies, resolves the LATAM template path, runs the matching `docs\pptx\generators\generate_*.py` scripts, and uploads the resulting `.pptx` files as release assets or workflow artifacts.

### Why

The repo already had a mature PPTX generator library, but regeneration was still a local/manual step that depended on whoever had the template file configured on their machine. That made release packaging inconsistent and easy to forget.

### Steering Moment

The key choice was to treat the workflow as best-effort automation instead of a critical gate. If the LATAM template is unavailable on the runner, the workflow emits a warning and skips generation cleanly rather than failing the whole release flow.

### Impact

Release tags now have a lightweight path to ship fresh deck assets when the template is available, and manual dispatch provides an easy way to regenerate one deck or the full set without relying on local-only steps.

---

## 2026-05-29 — Governance Cleanup Brought the Squad's Control Surface Back Into Sync

### What Happened

Refreshed `.squad\SCORECARD.md`, `.squad\eval.mjs`, `.squad\mcp-config.md`, `PORTFOLIO.md`, and added `Use-cases\README.md` so the repo's governance layer now matches the live Ocean's Twelve operating model: 13 agents, 21 prompts, 7 chatmodes, 23 prompt-local skills, and 7 migration targets.

### Why

Those files had become a drift zone. Some still described the old Fast Squad, some showed sample placeholder portfolio data, and the `Use-cases\` root had no index telling operators how those folders mapped to the seven canonical targets.

### Steering Moment

The key choice was to treat governance artifacts as operator-facing product surface instead of passive metadata. That meant tightening the scorecard and evaluator around the real roster and prompt catalog, updating MCP guidance to the current chatmode/prompt-first workflow, and adding only the smallest new document needed: a `Use-cases\README.md` index without changing the folder path.

### Impact

Future operators and maintainers now get a cleaner control surface: scorecard expectations align to routing, eval checks the real squad shape, portfolio docs no longer look like placeholders, and the top-level use-case folders are discoverable without breaking external references.

---

## 2026-05-29 — Prompt Library Got a Real Linter

### What Happened

Added `.squad\lint-prompts.mjs`, a Node-based linter that audits prompt frontmatter, prompt skill references, required hook references, stale CLI patterns in prompt/chatmode guidance, chatmode frontmatter, and `.github\skills\` cross-reference coverage. After wiring it in, the first run exposed six prompt files missing `phase-gates` and `agent-dispatch` references, and those prompts were updated so the linter now passes with only two advisory warnings: `pptx-generation.md` and `secret-management.md` remain valid assets but are not currently referenced by prompts.

### Why

The prompt library had grown large enough that consistency drift was becoming easier to introduce than to notice. The repo needed one fast, repeatable check that could catch structural breakage before another manual audit was required.

### Steering Moment

The key choice was to separate hard failures from advisory cleanup: missing metadata and broken prompt skill references now fail the run, while hook gaps, stale CLI wording, and prompt-scope coverage gaps surface as warnings unless they truly break prompt composition.

### Impact

Prompt maintenance is now auditable in one command — `node .squad\lint-prompts.mjs` — and the targeted assessment/triage prompts were brought back into hook-aware squad canon at the same time.

---

## 2026-05-29 — All 7 Chatmodes Audited and Brought Back to Squad Canon

### What Happened

Reviewed and refreshed every chatmode under `.github\chatmodes\` — `Azure-Infrastructure`, `Code-Migration-Modernization`, `Cost-Optimization`, `Debug-Migration`, `Migration-Orchestrator`, `Quick-Assessment`, and `Security-Review`. The pass standardized YAML frontmatter by adding `agent`, aligned agent names to the live squad roster, added hook references to `.github\hooks\phase-gates.md` and `.github\hooks\agent-dispatch.md`, normalized skill references and command wording to repo canon, and converted stale completion guidance to CLI-first `@squad` follow-through while keeping slash names only where they are true prompt-trigger references. Tess Ocean awareness was also added where presentation/reporting support matters most: `Migration-Orchestrator`, `Security-Review`, and `Cost-Optimization`.

### Why

The chatmode layer had drifted from the repo's current operating model. Metadata, routing cues, follow-through commands, and specialist awareness were no longer consistent across the seven entry points.

### Steering Moment

The key choice was to standardize aggressively without erasing useful trigger vocabulary: make `agent` and hook references universal, make completion guidance consistently CLI-first, and preserve slash names only when they still identify actual prompt triggers.

### Impact

The seven chatmodes now read as one coherent orchestration surface: roster-aligned, hook-aware, CLI-consistent, and better prepared to dispatch the right specialist — including presentation support when stakeholder-facing output is part of the path.

---

## 2026-05-29 — README Synced to the 13-Agent CLI-First Squad

### What Happened

Updated `README.md` so the repo front door now matches the current system state: 13 specialist agents, 19 prompt-local skills, Tess Ocean in the crew roster, a new PPTX deck library section, refreshed scenario tables using `@squad` commands, and a new "Best Prompts for Working With This Squad" section near the end.

### Why

The repo had already evolved through new security skills, CLI-first prompt handoffs, and the Presentation Specialist/PPTX workflow, but the main README still described the previous inventory and showed outdated slash-style operator commands in multiple walkthrough sections.

### Steering Moment

The key decision was not to erase every slash reference blindly. User-facing examples were converted to `@squad` commands, while README tables that explicitly catalog prompt identities were left on slash names so maintainers can still map documentation back to the underlying prompt files.

### Impact

The README now works again as an accurate operator guide and stakeholder overview: the counts match the repo, PPTX capabilities are discoverable, and the recommended commands align with the current CLI-first squad workflow.

---

## 2026-05-29 — All LATAM PPTX Generators Moved to the Shared Helper Module

### What Happened

Refactored all eight generators in `docs\pptx\generators\` to import shared colors and helper functions from `latam_gcs_template.py` instead of duplicating the LATAM GCS palette and common slide-building code inline. Validation passed by importing each generator from `docs\pptx\generators`, which regenerated decks successfully for Oceans Twelve (17), Borges/Brady (15), squad v3 (15), factory runbook (20), runbook (16), snap (15), snap runbook (15), and SOW (14).

### Why

The shared template module already existed, but every deck still carried its own copy of the same constants and helper functions. That made presentation fixes high-risk because branded behavior could drift from one generator to another.

### Steering Moment

The key choice was to migrate each deck to the shared API without flattening deck-specific behavior: keep custom helpers inline where needed, but force all common slide operations through the shared module, including the `prs`-aware `add_slide`, `add_title_bar`, and `add_footer` signatures.

### Impact

There is now one canonical LATAM/GCS PPTX helper surface actively used by every generator in the folder, so future palette, footer, card, and layout fixes can be made once and picked up consistently across all decks.

---

## 2026-05-29 — PPTX Authoring Skill and Deck README Expanded

### What Happened

Added `.github\skills\pptx-generation.md` to document the shared LATAM GCS deck-generation pattern and expanded `docs\pptx\README.md` with `@squad` prompts, manual creation steps, reusable slide layout snippets, a minimal generator example, and a current generator inventory table.

### Why

The PPTX generators had become reusable enough to deserve operator-facing guidance, but contributors still had to reverse-engineer the pattern from Python files and scattered comments before creating or updating a deck.

### Steering Moment

The key choice was to document the shared-helper workflow in two layers: a reusable skill for agents and prompts, plus a README for humans working directly in the `docs\pptx` folder. That keeps deck creation discoverable without duplicating the helper implementation itself.

### Impact

Future deck work can now start from an explicit skill, clearer `@squad` prompts, and proven layout snippets instead of ad hoc exploration of existing generators.

---

## 2026-05-29 — Three Root Skills Promoted into Authoritative Orchestration Copies

### What Happened

Promoted `managed-identity.md`, `rbac-least-privilege.md`, and `secret-management.md` into new authoritative `.github\skills\` versions, and standardized prompt completion guidance across `.github\prompts\` on CLI-first `@squad` follow-up commands while preserving slash-command names in each prompt's **When to Use** trigger section.

### Why

The repo needed one clearer authority layer for orchestration-ready skills and one consistent operator story for how prompts hand users to the next step without rewriting the recognizable prompt entry names.

### Steering Moment

The key choice was to modernize the completion path and skill authority model without renaming the trigger vocabulary operators already know: keep the slash-command names visible in **When to Use**, but make the actual completion guidance and next-step flow consistently `@squad`-driven.

### Impact

Prompt handoffs now read more consistently in Copilot CLI, security and identity guidance is reusable from the `.github\skills\` layer, and contributors have a cleaner canonical source for these three cross-cutting orchestration skills.

---

## 2026-05-29 — Borges-Brady Deck Reframed as a Factory Story

### What Happened

Rewrote `docs\generate_borges_brady_deck.py` into a new 15-slide persuasive narrative focused on Factory scale, regenerated `docs\Borges_Brady_Squad_Power.pptx`, and verified the deck now contains 15 slides with speaker notes on every slide.

### Why

The prior deck explained the Roberto Borges and Brady Squad partnership, but it did not sell the future-facing value hard enough for Factory delivery, repeatability, and growth.

### Steering Moment

The key move was to keep the existing LATAM template and helper functions intact while replacing the story architecture completely: open on the migration failure pattern, prove why orchestration changes the economics, show the factory pipeline and ROI, then close on the roadmap and transformation message.

### Impact

The deck now reads like an executive persuasion tool instead of a feature inventory, making it stronger for stakeholder briefings about why this partnership should become a scalable migration engine.

---

## 2026-05-29 — Security Hardening Retargeted to Focused Azure Security Skills

### What Happened

Added four new security-focused skills — `.github\skills\azure-keyvault-secrets.md`, `.github\skills\azure-network-security.md`, `.github\skills\azure-defender-compliance.md`, and `.github\skills\owasp-top10-review.md` — and updated `.github\prompts\SecurityHardening.prompt.md` to reference them directly alongside `azure-entra-id.md`.

### Why

The security hardening phase needed direct, reusable guidance for secrets, perimeter controls, Defender/compliance posture, and OWASP review instead of depending on generic migration skills that were only tangentially related to security.

### Steering Moment

The key choice was to keep the prompt centered on audit flow and deliverables while moving deep domain guidance into focused security skills, so the prompt stays readable and the skill content can evolve independently.

### Impact

Security-focused prompts in the repo now have clearer Azure-specific reuse for Key Vault, network hardening, Defender for Cloud, compliance mapping, secret scanning context, and OWASP-based remediation.

---

## 2026-05-29 — Borges-Brady Deck Overlay and Card Fill Fix Applied

### What Happened

Updated `docs\generate_borges_brady_deck.py` so accent bars can be drawn inset inside rounded cards, switched the standard deck cards to white fills, and regenerated `docs\Borges_Brady_Squad_Power.pptx` successfully.

### Why

The first generated version let accent lines ride above the rounded card edge and kept several cards on a light gray fill, which made the deck look less polished than intended.

### Steering Moment

Rather than patching slide coordinates one by one, the fix was pushed into the shared helpers and the three card-builder wrappers so every repeated card pattern inherits the corrected inset accent behavior.

### Impact

The regenerated deck now keeps its accent lines visually inside the card chrome and uses white card bodies for the main content blocks, making the presentation cleaner for demos and executive review.

---

## 2026-05-29 — Shared LATAM GCS Template Module Added for PPTX Generators

### What Happened
Created `docs\latam_gcs_template.py`, a shared Python module that centralizes the LATAM GCS template path, canonical theme palette, and reusable slide helpers used across the squad's PowerPoint generators.

### Why
The Oceans Twelve and Borges/Brady deck generators had duplicated palette constants and helper code. Pulling those pieces into one module reduces drift and creates one place to evolve branded slide behaviors such as inside accent lines, shared card styles, table formatting, and footer rendering.

### Steering Moment
The key choice was to keep this change surgical: build the shared module now, using the richer Oceans Twelve helper implementations as the baseline, but defer generator rewiring to a follow-up change so the new asset can be validated independently first.

### Impact
The repo now has one canonical LATAM/GCS PPTX helper surface ready for multiple decks to import, which lowers maintenance cost and makes future template refinements more consistent.

---

## 2026-05-29 — Borges and Brady Comparison Deck Added as a Native PPTX Generator

### What Happened

Created `docs\generate_borges_brady_deck.py` and ran it to produce `docs\Borges_Brady_Squad_Power.pptx`, a 12-slide PowerPoint deck that explains how Roberto Borges' migration expertise and Brady Gaster's squad framework reinforce each other.

### Why

The repo already had a strong Ocean's Twelve architecture story, but this request needed a focused executive-ready narrative about the power of combining migration knowledge with multi-agent orchestration. Building it as code keeps the deck repeatable, editable, and easy to refresh.

### Steering Moment

The key choice was to copy the existing LATAM/GCS generator pattern exactly instead of improvising a new slide framework. That preserved brand consistency, footer and notes behavior, and made it easy to validate slide count, notes coverage, and boundary safety programmatically.

### Impact

The repository now has a second presentation generator and a ready-to-share `.pptx` artifact that can be regenerated on demand for demos, briefings, and stakeholder conversations about Ocean's Twelve.

---

## 2026-05-29 — Generic Interactive Interview Became the New Migration Front Door

### What Happened

Added `.github/prompts/InteractiveMigrationInterview.prompt.md` plus `docs/squad-interactive/README.md` and `docs/squad-interactive/example-session.md` to replace BookShop-shaped prompt starters with one app-agnostic, conversational squad intake.

### Why

Fresh migrations should begin from the user's repo and target platform, not from a historical sample app. The new flow lets Danny Ocean interview the operator, scan the codebase, confirm findings, generate a phase-aware plan, and keep execution navigable through `show phase`, `run phase`, `run all`, `status`, and `fan out`.

### Steering Moment

The key choice was to make the entrypoint generic without making it vague. The prompt now carries explicit scan expectations, smart defaults, and decision gates so the interview feels conversational but still behaves like a controlled migration intake.

### Impact

Operators now have one reusable squad starting point for legacy migrations, with supporting docs that explain the flow and show a realistic CLI conversation from intake through mid-phase architecture decisions.

---

## 2026-05-29 — BookShop Prompt Docs Archived as Historical Migration Examples

### What Happened

Added log coverage for the BookShop docs shift: the prompt reference set under `Use-cases\05-BookShop\docs` is now framed as completed-migration evidence, with a README/index and document banners steering fresh work to the interactive squad interview.

### Why

The repo's onboarding story has moved to a CLI-first, interview-led flow. Leaving BookShop prompt references looking like starter templates would blur that entrypoint and invite operators to begin from historical artifacts instead of the guided squad conversation.

### Steering Moment

We chose to preserve the BookShop material for examples and provenance, but to relabel it plainly as archive/reference content rather than generic migration scaffolding.

### Impact

New migrations have one clear starting point, while teams still keep the BookShop documents as concise, trustworthy examples of what a finished migration package can look like.

---

## 2026-05-29 — Walkthroughs 04 and 05 Rewritten as Pure CLI Squad Flows

### What Happened

Rewrote the Contoso University and Bookshop Reference walkthroughs as pure Copilot CLI guides driven by natural-language `@squad` prompts, with explicit fan-out language and single-surface phase flows.

### Why

The walkthrough set needed one consistent operating model. Mixed CLI/chat guidance added friction and weakened the story that the squad can be steered from one command surface.

### Steering Moment

We chose to make `fan out` explicit in the prompts and to frame each scenario by its real migration shape: Contoso as the largest multi-project modernization, and Bookshop as the SAP CAP Java to Azure Container Apps + PostgreSQL path.

### Impact

Both guides now teach clearer operator habits, align with the CLI-first repo direction, and make complex parallel work easier to understand and demo.

---

## 2026-05-29 — Walkthroughs 01-03 Rewritten as Pure CLI Heist Flows

### What Happened

Rebuilt the Classic ASP, .NET 3.0 WebForms, and WCF walkthroughs as pure Copilot CLI guides driven entirely by natural-language `@squad` prompts, added Mermaid phase diagrams, and pushed Chat Panel shortcuts into a tiny appendix instead of the main path.

### Why

These are the first migration journeys many users open, so they need to teach one clear operating model. Mixed-surface walkthroughs made the squad feel harder to use than it is and diluted the story that the crew can be led like a team from one CLI prompt at a time.

### Steering Moment

The key choice was to keep the Ocean's Twelve personality and phase-by-phase depth while removing chatmode choreography from the main instructions. The rewrite preserves advanced escape hatches, but only after the core flow has already taught the simpler habit.

### Impact

The Antique, The Fossil, and The Wire now read like clean command-line runbooks: one prompt, explicit fan-out, clear artifacts, natural follow-up questions, and a visible mapping of which crew member owns each stage.

---

## 2026-05-29 — Walkthroughs 06 and 07 Reframed as Pure CLI Squad Flows

### What Happened

Rewrote the Java API and Parts Unlimited walkthroughs as pure Copilot CLI experiences built around natural-language `@squad` prompts, added Mermaid phase diagrams, and removed chatmode-switching guidance from the main flow.

### Why

The walkthrough library already existed to make the migration system easier to drive by use case, but the two later guides still taught a mixed interface model. That made demos noisier, increased operator context switching, and weakened the story that the squad can be led from one command surface.

### Steering Moment

The key trade-off was to optimize for one canonical path instead of preserving every power-user shortcut in the main body. Advanced equivalents still exist, but they are now compressed into a short appendix so the walkthrough itself reads like one clean conversation with the crew.

### Impact

Use cases 06 and 07 now align with the repo's CLI-first guidance more cleanly, keep the Ocean's Twelve identity visible, and show where to ask the squad to fan out without forcing users to learn chatmode choreography first.

---
## 2026-05-29 — Walkthroughs Recast as a CLI-First Migration Index

### What Happened

Rewrote `docs/walkthroughs/README.md` into a CLI-first landing page with a shared squad-flow diagram, a practical "How to Use These Guides" section, and a single quick-start table covering all seven migration walkthroughs.

### Why

The earlier index still implied a mixed CLI and chat-panel operating model. The repo now needs the walkthrough layer to reinforce the simpler story: start with `@squad`, describe the migration in natural language, and let the squad route the work.

### Steering Moment

Instead of introducing separate instructions per scenario at the top level, the rewrite standardized the entry pattern across all use cases and made "fan out" the explicit signal for parallel squad execution.

### Impact

New operators can now discover the right walkthrough faster, trust that every use case starts from the same CLI surface, and understand the shared squad pattern before diving into scenario-specific detail.

---

## 2026-05-29 — Walkthroughs 06 and 07 Reframed as Pure CLI Squad Flows

### What Happened

Rewrote the Java API and Parts Unlimited walkthroughs as pure Copilot CLI experiences built around natural-language `@squad` prompts, added Mermaid phase diagrams, and removed chatmode-switching guidance from the main flow.

### Why

The walkthrough library already existed to make the migration system easier to drive by use case, but the two later guides still taught a mixed interface model. That made demos noisier, increased operator context switching, and weakened the story that the squad can be led from one command surface.

### Steering Moment

The key trade-off was to optimize for one canonical path instead of preserving every power-user shortcut in the main body. Advanced equivalents still exist, but they are now compressed into a short appendix so the walkthrough itself reads like one clean conversation with the crew.

### Impact

Use cases 06 and 07 now align with the repo's CLI-first guidance more cleanly, keep the Ocean's Twelve identity visible, and show where to ask the squad to fan out without forcing users to learn chatmode choreography first.

---
## 2026-05-28 — Skill Catalog and Project Hierarchy Consolidated

### What Happened

Audited the duplicate skill files split across root `skills/` and `.github/skills/`, identified the 10 overlapping names, chose the more complete `.github/skills/` versions as canonical for those overlaps, and added three navigation artifacts: `skills/INDEX.md`, `docs/PROJECT-MAP.md`, and `docs/PROMPT-CATALOG.md`.

### Why

The repository had grown into a strong migration control tower, but navigation was drifting: prompts, chatmodes, docs, and skills were spread across multiple layers, and duplicate skill filenames made it hard to know which content should be trusted or updated.

### Steering Moment

Instead of deleting duplicates blindly, the restructuring treated compatibility as a first-class constraint. The better `.github/skills/` copies were declared authoritative for overlaps, while the root catalog was preserved for legacy references and documented clearly enough that a future cleanup can happen safely.

### Impact

Architects and prompt authors now have a verified map of the repo, a prompt catalog for all 20 slash-command entrypoints, and one canonical index that shows where every skill lives, which prompts use it, and where overlap still exists.

---

## 2026-05-29 — Walkthroughs 06 and 07 Reframed as Pure CLI Squad Flows

### What Happened

Rewrote the Java API and Parts Unlimited walkthroughs as pure Copilot CLI experiences built around natural-language `@squad` prompts, added Mermaid phase diagrams, and removed chatmode-switching guidance from the main flow.

### Why

The walkthrough library already existed to make the migration system easier to drive by use case, but the two later guides still taught a mixed interface model. That made demos noisier, increased operator context switching, and weakened the story that the squad can be led from one command surface.

### Steering Moment

The key trade-off was to optimize for one canonical path instead of preserving every power-user shortcut in the main body. Advanced equivalents still exist, but they are now compressed into a short appendix so the walkthrough itself reads like one clean conversation with the crew.

### Impact

Use cases 06 and 07 now align with the repo's CLI-first guidance more cleanly, keep the Ocean's Twelve identity visible, and show where to ask the squad to fan out without forcing users to learn chatmode choreography first.

---
## 2026-05-28 — Identity Drift and Prompt Metadata Audit Completed

### What Happened

Aligned the squad control files to Ocean's Twelve — The Azure Heist, rewrote the three core charters around Azure migration work instead of a TypeScript app stack, standardized prompt frontmatter, and clarified the Phase 5 handoff into Phase 6 operations.

### Why

The repo had already evolved into a .NET/Java Azure migration control tower, but several core docs still described the older fast-squad identity and the original JavaScript/Vitest assumptions. That mismatch risked bad routing, wrong expectations, and prompt drift.

### Steering Moment

Rather than patch only the visible squad names, the audit treated identity, charters, prompt metadata, and phase language as one consistency problem so the repo reads like one coherent system instead of a renamed scaffold.

### Impact

Future sessions should route more accurately, core agents now advertise the right Azure migration duties, prompt files expose consistent metadata, and Phase 5 no longer conflicts with the existence of post-migration operations in Phase 6.

---

## 2026-05-29 — Walkthroughs 06 and 07 Reframed as Pure CLI Squad Flows

### What Happened

Rewrote the Java API and Parts Unlimited walkthroughs as pure Copilot CLI experiences built around natural-language `@squad` prompts, added Mermaid phase diagrams, and removed chatmode-switching guidance from the main flow.

### Why

The walkthrough library already existed to make the migration system easier to drive by use case, but the two later guides still taught a mixed interface model. That made demos noisier, increased operator context switching, and weakened the story that the squad can be led from one command surface.

### Steering Moment

The key trade-off was to optimize for one canonical path instead of preserving every power-user shortcut in the main body. Advanced equivalents still exist, but they are now compressed into a short appendix so the walkthrough itself reads like one clean conversation with the crew.

### Impact

Use cases 06 and 07 now align with the repo's CLI-first guidance more cleanly, keep the Ocean's Twelve identity visible, and show where to ask the squad to fan out without forcing users to learn chatmode choreography first.

---
## 2026-05-28 — README Navigation Restructured with Collapsible Sections

### What Happened

Restructured the root `README.md` to introduce a clear two-level hierarchy: a top-level navigation index followed by collapsible `<details>` blocks for each major section (crew roster, phase workflow, hook mechanics, target portfolio, usage examples, etc.).

### Why

The previous README was already comprehensive (D-014), but its linear layout made it hard for readers to orient quickly. Architects needed a map before diving into detail; developers needed to jump to examples without scrolling past diagrams. Collapsible sections reduce visual noise for casual readers while keeping the full narrative intact for those who expand everything.

### Steering Moment

The builder asked specifically for restructured navigation and collapsible sections to create a better content hierarchy — optimizing for multiple audience types (architect, developer, stakeholder) rather than one linear reading order.

### Impact

The README now serves as both a quick-reference index and a full technical narrative. First-time visitors can scan the top-level navigation, click into only what is relevant to their role, and reach the right section without losing context. This lowers onboarding friction and makes the control-tower README easier to maintain as new agents, prompts, and use-cases are added.

---

## 2026-05-29 — Walkthroughs 06 and 07 Reframed as Pure CLI Squad Flows

### What Happened

Rewrote the Java API and Parts Unlimited walkthroughs as pure Copilot CLI experiences built around natural-language `@squad` prompts, added Mermaid phase diagrams, and removed chatmode-switching guidance from the main flow.

### Why

The walkthrough library already existed to make the migration system easier to drive by use case, but the two later guides still taught a mixed interface model. That made demos noisier, increased operator context switching, and weakened the story that the squad can be led from one command surface.

### Steering Moment

The key trade-off was to optimize for one canonical path instead of preserving every power-user shortcut in the main body. Advanced equivalents still exist, but they are now compressed into a short appendix so the walkthrough itself reads like one clean conversation with the crew.

### Impact

Use cases 06 and 07 now align with the repo's CLI-first guidance more cleanly, keep the Ocean's Twelve identity visible, and show where to ask the squad to fan out without forcing users to learn chatmode choreography first.

---
## 2026-05-28 — Use-Case CLI Walkthrough Set Added

### What Happened

Added a new `docs/walkthroughs/` documentation set with seven use-case-specific CLI migration walkthroughs plus an index `README.md` that routes operators to the right flow for each sample application.

### Why

The repo already had prompts, skills, routing, and training assets, but it still lacked a task-focused walkthrough layer that shows how to drive the migration workflow from the CLI for each concrete use case.

### Steering Moment

The key choice was to organize the guidance by migration scenario instead of by generic phase alone, so builders can start from the app they have and still follow the repo's existing command surface and squad-routing model.

### Impact

Operators now have a clearer, lower-friction path from sample app to command sequence, which improves onboarding, reduces prompt-selection ambiguity, and makes the migration workflow easier to demo and reuse.

---

## 2026-05-29 — Walkthroughs 06 and 07 Reframed as Pure CLI Squad Flows

### What Happened

Rewrote the Java API and Parts Unlimited walkthroughs as pure Copilot CLI experiences built around natural-language `@squad` prompts, added Mermaid phase diagrams, and removed chatmode-switching guidance from the main flow.

### Why

The walkthrough library already existed to make the migration system easier to drive by use case, but the two later guides still taught a mixed interface model. That made demos noisier, increased operator context switching, and weakened the story that the squad can be led from one command surface.

### Steering Moment

The key trade-off was to optimize for one canonical path instead of preserving every power-user shortcut in the main body. Advanced equivalents still exist, but they are now compressed into a short appendix so the walkthrough itself reads like one clean conversation with the crew.

### Impact

Use cases 06 and 07 now align with the repo's CLI-first guidance more cleanly, keep the Ocean's Twelve identity visible, and show where to ask the squad to fan out without forcing users to learn chatmode choreography first.

---
## 2026-05-28 — README Reframed Ocean's Twelve as an Architect-Ready Control Tower

### What Happened

Rewrote the root `README.md` into a visual-first, Mermaid-rich guide that explains the Ocean's Twelve squad system as an orchestrated Azure migration model instead of a loose collection of prompts.

### Why

The repo already had the working assets — agents, routing, prompts, hooks, skills, training docs, and use-cases — but the first document most people read did not yet make the case for orchestration strongly enough for architects or delivery leads.

### Steering Moment

The builder asked for a persuasive README that could stand on its own: hero narrative, old-vs-new comparison, layered architecture, crew roster, workflow phases, hook mechanics, target portfolio, and copy-pasteable usage examples.

### Impact

Architects can now understand the control plane from one file, developers get a faster path into the right chatmode and prompt, and stakeholders see why specialist orchestration is better than monolithic prompting.

---

## 2026-05-29 — Walkthroughs 06 and 07 Reframed as Pure CLI Squad Flows

### What Happened

Rewrote the Java API and Parts Unlimited walkthroughs as pure Copilot CLI experiences built around natural-language `@squad` prompts, added Mermaid phase diagrams, and removed chatmode-switching guidance from the main flow.

### Why

The walkthrough library already existed to make the migration system easier to drive by use case, but the two later guides still taught a mixed interface model. That made demos noisier, increased operator context switching, and weakened the story that the squad can be led from one command surface.

### Steering Moment

The key trade-off was to optimize for one canonical path instead of preserving every power-user shortcut in the main body. Advanced equivalents still exist, but they are now compressed into a short appendix so the walkthrough itself reads like one clean conversation with the crew.

### Impact

Use cases 06 and 07 now align with the repo's CLI-first guidance more cleanly, keep the Ocean's Twelve identity visible, and show where to ask the squad to fan out without forcing users to learn chatmode choreography first.

---
## 2026-05-28 — Persuasive PPTX Deck Framed the Case for Squad Orchestration

### What Happened

Added `docs/generate_oceans_twelve_deck.py` and generated `docs/Oceans_Twelve_Squad_vs_Prompting.pptx`, a 15-slide LATAM-themed presentation that contrasts monolithic prompting with the Ocean's Twelve squad model for Azure migration.

### Why

The repository already proved orchestration in prompts, skills, routing, and agent handoffs, but Roberto Borges also needed an architect-friendly narrative artifact that can persuade stakeholders visually, not just technically.

### Steering Moment

The builder asked for a professional, fully regenerable deck that uses the same LATAM template and helper-function pattern as the existing presentation generators while making the value of specialization, composability, memory, and quality gates obvious slide by slide.

### Impact

The project now has a presentation-ready story for architects and decision makers. The deck can be regenerated from code, updated alongside the orchestration system, and reused in training, demos, and migration planning conversations.

---

## 2026-05-29 — Walkthroughs 06 and 07 Reframed as Pure CLI Squad Flows

### What Happened

Rewrote the Java API and Parts Unlimited walkthroughs as pure Copilot CLI experiences built around natural-language `@squad` prompts, added Mermaid phase diagrams, and removed chatmode-switching guidance from the main flow.

### Why

The walkthrough library already existed to make the migration system easier to drive by use case, but the two later guides still taught a mixed interface model. That made demos noisier, increased operator context switching, and weakened the story that the squad can be led from one command surface.

### Steering Moment

The key trade-off was to optimize for one canonical path instead of preserving every power-user shortcut in the main body. Advanced equivalents still exist, but they are now compressed into a short appendix so the walkthrough itself reads like one clean conversation with the crew.

### Impact

Use cases 06 and 07 now align with the repo's CLI-first guidance more cleanly, keep the Ocean's Twelve identity visible, and show where to ask the squad to fan out without forcing users to learn chatmode choreography first.

---
## 2026-05-28 — Routing System Expanded for the Full Twelve-Agent Workflow

### What Happened

`.squad/routing.md` was upgraded from a lightweight fast-squad router into a full migration coordination map covering all 12 squad agents, the full prompt library, phase-level quality gates, automatic secondary-routing triggers, and use-case-based routing guidance.

### Why

The repo had grown beyond a simple Architect/Coder/Tester flow. With more prompts, more specialist agents, and more migration scenarios, routing needed to become explicit so work could be assigned consistently across phases, specialties, and real-world Azure migration use cases.

### Steering Moment

The builder pushed for a routing model that was operational, not symbolic: every agent accounted for, every prompt placed in a workflow, and every phase guarded by clear quality checks and auto-routing rules.

### Impact

The squad now has a clearer control tower. Future migration work can route faster, trigger the right specialists earlier, and maintain better handoffs across assessment, implementation, validation, cutover, and documentation.

---

## 2026-05-29 — Walkthroughs 06 and 07 Reframed as Pure CLI Squad Flows

### What Happened

Rewrote the Java API and Parts Unlimited walkthroughs as pure Copilot CLI experiences built around natural-language `@squad` prompts, added Mermaid phase diagrams, and removed chatmode-switching guidance from the main flow.

### Why

The walkthrough library already existed to make the migration system easier to drive by use case, but the two later guides still taught a mixed interface model. That made demos noisier, increased operator context switching, and weakened the story that the squad can be led from one command surface.

### Steering Moment

The key trade-off was to optimize for one canonical path instead of preserving every power-user shortcut in the main body. Advanced equivalents still exist, but they are now compressed into a short appendix so the walkthrough itself reads like one clean conversation with the crew.

### Impact

Use cases 06 and 07 now align with the repo's CLI-first guidance more cleanly, keep the Ocean's Twelve identity visible, and show where to ask the squad to fan out without forcing users to learn chatmode choreography first.

---
## 2026-05-28 — Migration Orchestrator Replaced the Monolith

### What Happened

Added `Migration-Orchestrator.chatmode.md` as the master squad-aware coordinator, created focused chatmodes for quick assessment, security review, Azure infrastructure, and cost optimization, and reduced `Code-Migration-Modernization.chatmode.md` to a Phase 2 specialist.

### Why

The previous migration chatmode tried to do every phase itself. That made routing opaque, handoffs weak, and specialist knowledge hard to reuse. The new structure makes the workflow explicit: orchestrator for coordination, specialist chatmodes for execution, skills for reusable technical guidance.

### Steering Moment

The builder asked for the difference between prompting and orchestrating to be visible in the product itself, not just in architecture notes. That forced the design to center on agent dispatch, phase gates, and artifact-based handoffs.

### Impact

Robert's team can now enter through one master chatmode, route to the right specialist, reuse the 13 prompt entrypoints, and manage single-app or portfolio migrations with cleaner quality gates.

---

## 2026-05-29 — Walkthroughs 06 and 07 Reframed as Pure CLI Squad Flows

### What Happened

Rewrote the Java API and Parts Unlimited walkthroughs as pure Copilot CLI experiences built around natural-language `@squad` prompts, added Mermaid phase diagrams, and removed chatmode-switching guidance from the main flow.

### Why

The walkthrough library already existed to make the migration system easier to drive by use case, but the two later guides still taught a mixed interface model. That made demos noisier, increased operator context switching, and weakened the story that the squad can be led from one command surface.

### Steering Moment

The key trade-off was to optimize for one canonical path instead of preserving every power-user shortcut in the main body. Advanced equivalents still exist, but they are now compressed into a short appendix so the walkthrough itself reads like one clean conversation with the crew.

### Impact

Use cases 06 and 07 now align with the repo's CLI-first guidance more cleanly, keep the Ocean's Twelve identity visible, and show where to ask the squad to fan out without forcing users to learn chatmode choreography first.

---
## 2026-05-28 — Production Training Docs Landed for Ocean's Twelve

### What Happened

Created a production-ready training documentation set for Roberto Borges' Ocean's Twelve migration team. The milestone includes `docs/skills-map.md`, seven use-case cheat sheets under `docs/use-case-cheatsheets/`, `docs/dotnet-version-guide.md`, and `docs/training-exercises.md`, all anchored to the repo's seven sample migration scenarios and the existing prompt and skills catalog.

### Why

The repo already had strong migration prompts and skills, but it still needed an operator-friendly training layer so team members could quickly see which prompts, skills, Azure targets, and squad agents apply to each use-case.

### Steering Moment

A key call was to standardize on the slash commands that already exist and pair them with exact natural-language prompts for scenario-specific steering. The docs teach the real workflow the team can run now instead of inventing a separate training-only command set.

### Impact

Ocean's Twelve now has a practical onboarding and enablement package. New team members can map skills to use-cases faster, follow consistent dispatch sequences, and rehearse migrations against the same command surface they will use in delivery.

---

## 2026-05-29 — Walkthroughs 06 and 07 Reframed as Pure CLI Squad Flows

### What Happened

Rewrote the Java API and Parts Unlimited walkthroughs as pure Copilot CLI experiences built around natural-language `@squad` prompts, added Mermaid phase diagrams, and removed chatmode-switching guidance from the main flow.

### Why

The walkthrough library already existed to make the migration system easier to drive by use case, but the two later guides still taught a mixed interface model. That made demos noisier, increased operator context switching, and weakened the story that the squad can be led from one command surface.

### Steering Moment

The key trade-off was to optimize for one canonical path instead of preserving every power-user shortcut in the main body. Advanced equivalents still exist, but they are now compressed into a short appendix so the walkthrough itself reads like one clean conversation with the crew.

### Impact

Use cases 06 and 07 now align with the repo's CLI-first guidance more cleanly, keep the Ocean's Twelve identity visible, and show where to ask the squad to fan out without forcing users to learn chatmode choreography first.

---
## 2026-05-28 — Targeted Assessment Prompts Added

### What Happened

Added seven production-ready prompt files for targeted migration assessment and readiness work: `Assess-DotNet-Upgrade.prompt.md`, `Assess-Java-Upgrade.prompt.md`, `Assess-WCF-Migration.prompt.md`, `Assess-WebForms-Migration.prompt.md`, `Assess-ClassicASP-Migration.prompt.md`, `TeamSkillAssessment.prompt.md`, and `QuickTriage.prompt.md`. The root `README.md` was also updated so the new slash-command entrypoints are discoverable.

### Why

The repository already had a strong general Phase 1 assessment, but Robert Borges' team also needed focused prompts for concrete upgrade paths, technology-specific blockers, skill readiness, and fast triage across the seven use-cases.

### Steering Moment

The builder asked specifically for production-ready prompt files with full YAML frontmatter, structured numbered steps, rules, deliverables, and output checklists that follow the `Phase1-PlanAndAssess.prompt.md` pattern.

### Impact

Migration teams can now run dedicated assessments for .NET version upgrades, Java modernization, WCF services, WebForms estates, Classic ASP rewrites, team readiness, and 5-minute intake without overloading the generic planning prompt.

---

## 2026-05-29 — Walkthroughs 06 and 07 Reframed as Pure CLI Squad Flows

### What Happened

Rewrote the Java API and Parts Unlimited walkthroughs as pure Copilot CLI experiences built around natural-language `@squad` prompts, added Mermaid phase diagrams, and removed chatmode-switching guidance from the main flow.

### Why

The walkthrough library already existed to make the migration system easier to drive by use case, but the two later guides still taught a mixed interface model. That made demos noisier, increased operator context switching, and weakened the story that the squad can be led from one command surface.

### Steering Moment

The key trade-off was to optimize for one canonical path instead of preserving every power-user shortcut in the main body. Advanced equivalents still exist, but they are now compressed into a short appendix so the walkthrough itself reads like one clean conversation with the crew.

### Impact

Use cases 06 and 07 now align with the repo's CLI-first guidance more cleanly, keep the Ocean's Twelve identity visible, and show where to ask the squad to fan out without forcing users to learn chatmode choreography first.

---
## 2026-05-28 — Skills and Hooks Orchestration Wired

### What Happened

Added a production-ready `.github/skills/` library for .NET, Java, Azure, data, handoff, and rollback guidance plus a new `.github/hooks/` orchestration layer for phase gates, automatic agent dispatch, and per-use-case routing. All 13 prompt entrypoints were updated to reference the new skill and hook files directly.

### Why

The prompts had reusable knowledge in pieces, but they still behaved like isolated instructions. Moving the reusable content next to the prompt assets and adding explicit hook files makes chatmodes, prompts, and specialist agents operate like one coordinated workflow.

### Steering Moment

The builder asked specifically for the missing glue: reusable skills plus orchestration hooks that turn standalone prompts into a coordinated squad workflow with enforced handoffs.

### Impact

Prompt authors now have a production-ready place to add migration knowledge and routing rules without bloating individual prompts. The migration flow has explicit phase gates, dispatch triggers, and use-case overrides ready to compose.

---

## 2026-05-29 — Walkthroughs 06 and 07 Reframed as Pure CLI Squad Flows

### What Happened

Rewrote the Java API and Parts Unlimited walkthroughs as pure Copilot CLI experiences built around natural-language `@squad` prompts, added Mermaid phase diagrams, and removed chatmode-switching guidance from the main flow.

### Why

The walkthrough library already existed to make the migration system easier to drive by use case, but the two later guides still taught a mixed interface model. That made demos noisier, increased operator context switching, and weakened the story that the squad can be led from one command surface.

### Steering Moment

The key trade-off was to optimize for one canonical path instead of preserving every power-user shortcut in the main body. Advanced equivalents still exist, but they are now compressed into a short appendix so the walkthrough itself reads like one clean conversation with the crew.

### Impact

Use cases 06 and 07 now align with the repo's CLI-first guidance more cleanly, keep the Ocean's Twelve identity visible, and show where to ask the squad to fan out without forcing users to learn chatmode choreography first.

---
## 2026-05-28 — Skills Catalog Added

### What Happened

A new root-level `skills/` catalog was added with 26 reusable migration skill files plus a `skills/README.md` index. The Phase 1, Phase 2, and Phase 3 prompts now reference these skills directly with `#file:skills/...` syntax.

### Why

The repo's migration guidance had become repetitive across assessment, code migration, and infrastructure prompts. Splitting durable knowledge into skills makes the prompts easier to maintain and easier to compose for .NET, Java, App Service, Container Apps, and AKS scenarios.

### Steering Moment

The builder asked specifically for concrete, production-ready skill files that could serve as the building blocks of a modular migration framework rather than more monolithic prompt text.

### Impact

Future prompt work can reuse shared migration logic instead of copying it. New prompts can compose the catalog by scenario, and the repo now has a concrete reference model for modular prompt authoring.

---

## 2026-05-29 — Walkthroughs 06 and 07 Reframed as Pure CLI Squad Flows

### What Happened

Rewrote the Java API and Parts Unlimited walkthroughs as pure Copilot CLI experiences built around natural-language `@squad` prompts, added Mermaid phase diagrams, and removed chatmode-switching guidance from the main flow.

### Why

The walkthrough library already existed to make the migration system easier to drive by use case, but the two later guides still taught a mixed interface model. That made demos noisier, increased operator context switching, and weakened the story that the squad can be led from one command surface.

### Steering Moment

The key trade-off was to optimize for one canonical path instead of preserving every power-user shortcut in the main body. Advanced equivalents still exist, but they are now compressed into a short appendix so the walkthrough itself reads like one clean conversation with the crew.

### Impact

Use cases 06 and 07 now align with the repo's CLI-first guidance more cleanly, keep the Ocean's Twelve identity visible, and show where to ask the squad to fan out without forcing users to learn chatmode choreography first.

---
## 2026-05-28 — Modular Prompt Architecture Designed

### What Happened

A new architecture direction was defined for the repository's migration prompts: thin slash-command entrypoints, a modular prompt-library split by phase/role/technology/skill, specialized chatmodes, and per-use-case override folders.

### Why

The existing flat prompt set and monolithic chatmode were becoming hard to scale across BookShop-sized use cases, team handoffs, and future stacks such as Node.js and Python.

### Steering Moment

The builder explicitly asked for a squad-aware, team-friendly redesign so Robert's team can assign phases, work in parallel, and reuse migration knowledge without copying giant reference docs.

### Impact

Future prompt work now has a clear target structure: reusable skills, smaller chatmodes, artifact-based handoffs, and use-case-local overrides instead of monolithic prompt files.

---

## 2026-05-29 — Walkthroughs 06 and 07 Reframed as Pure CLI Squad Flows

### What Happened

Rewrote the Java API and Parts Unlimited walkthroughs as pure Copilot CLI experiences built around natural-language `@squad` prompts, added Mermaid phase diagrams, and removed chatmode-switching guidance from the main flow.

### Why

The walkthrough library already existed to make the migration system easier to drive by use case, but the two later guides still taught a mixed interface model. That made demos noisier, increased operator context switching, and weakened the story that the squad can be led from one command surface.

### Steering Moment

The key trade-off was to optimize for one canonical path instead of preserving every power-user shortcut in the main body. Advanced equivalents still exist, but they are now compressed into a short appendix so the walkthrough itself reads like one clean conversation with the crew.

### Impact

Use cases 06 and 07 now align with the repo's CLI-first guidance more cleanly, keep the Ocean's Twelve identity visible, and show where to ask the squad to fan out without forcing users to learn chatmode choreography first.

---
## 2026-05-28 — Project Bootstrapped

**Squad:** The Fast Squad · **Vibe:** speed · **Theme:** Racing Crew

### The Team

Architect, Coder, Tester

### What Happened

Project initialized with the **The Fast Squad** squad preset via `npx snap-squad init`. The full `.squad/` directory, hook chain (AGENTS.md, CLAUDE.md, copilot-instructions.md), and this journal were generated automatically.

### Steering Moment

The builder chose **fast** — rapid poc squad — speed over ceremony, zero fluff, ship fast. This shapes everything that follows: who reviews code, how decisions get made, what gets tested first.

### What's Next

- [ ] First real feature or task
- [ ] Builder configures project context in `.squad/team.md`
- [ ] First decision logged to `.squad/decisions.md`

---

## 2026-05-29 — Walkthroughs 06 and 07 Reframed as Pure CLI Squad Flows

### What Happened

Rewrote the Java API and Parts Unlimited walkthroughs as pure Copilot CLI experiences built around natural-language `@squad` prompts, added Mermaid phase diagrams, and removed chatmode-switching guidance from the main flow.

### Why

The walkthrough library already existed to make the migration system easier to drive by use case, but the two later guides still taught a mixed interface model. That made demos noisier, increased operator context switching, and weakened the story that the squad can be led from one command surface.

### Steering Moment

The key trade-off was to optimize for one canonical path instead of preserving every power-user shortcut in the main body. Advanced equivalents still exist, but they are now compressed into a short appendix so the walkthrough itself reads like one clean conversation with the crew.

### Impact

Use cases 06 and 07 now align with the repo's CLI-first guidance more cleanly, keep the Ocean's Twelve identity visible, and show where to ask the squad to fan out without forcing users to learn chatmode choreography first.

---
## 2026-05-28 — Prompt Library Expanded

### What Happened

Added seven production-ready GitHub Copilot assets for the migration workflow: `Phase6-PostMigrationOps.prompt.md`, `Phase-Rollback.prompt.md`, `DatabaseMigration.prompt.md`, `SecurityHardening.prompt.md`, `CostOptimization.prompt.md`, `QuickAssessment.prompt.md`, and `Debug-Migration.chatmode.md`. The main migration chatmode and README were also updated so the new capabilities are discoverable.

### Why

The existing library covered assessment through CI/CD, but it had gaps around post-deployment operations, rollback safety, database-heavy migrations, focused security reviews, cost tuning, rapid triage, and structured debugging. Filling those gaps makes the prompt set more complete for real modernization programs.

### Steering Moment

The builder explicitly asked for ready-to-use prompt files that follow the stronger `Phase1` structure rather than loose instruction blocks. That led to a consistent pattern: frontmatter, agent role, ordered steps, rules, deliverables, and output checklists.

### Impact

The repository now supports a fuller migration lifecycle, including operations and recovery workflows, plus a dedicated troubleshooting chatmode for failed migrations.

---

## 2026-05-29 — Walkthroughs 06 and 07 Reframed as Pure CLI Squad Flows

### What Happened

Rewrote the Java API and Parts Unlimited walkthroughs as pure Copilot CLI experiences built around natural-language `@squad` prompts, added Mermaid phase diagrams, and removed chatmode-switching guidance from the main flow.

### Why

The walkthrough library already existed to make the migration system easier to drive by use case, but the two later guides still taught a mixed interface model. That made demos noisier, increased operator context switching, and weakened the story that the squad can be led from one command surface.

### Steering Moment

The key trade-off was to optimize for one canonical path instead of preserving every power-user shortcut in the main body. Advanced equivalents still exist, but they are now compressed into a short appendix so the walkthrough itself reads like one clean conversation with the crew.

### Impact

Use cases 06 and 07 now align with the repo's CLI-first guidance more cleanly, keep the Ocean's Twelve identity visible, and show where to ask the squad to fan out without forcing users to learn chatmode choreography first.

---
## 2026-05-28 — Team Workflow Enablement Added

### What Happened

Added production-ready team enablement docs for migration delivery: `docs/team-guide.md`, `docs/handoff-protocol.md`, `docs/squad-dispatch-cheatsheet.md`, `docs/onboarding.md`, and `PORTFOLIO.md`. The root `README.md` was also updated so the new guidance is discoverable.

### Why

The repo already proved the technical workflow with BookShop, but it lacked clear instructions for how humans and squad agents should divide work, hand off phases, onboard new teammates, and track multiple migrations at once.

### Steering Moment

The builder explicitly asked for production-ready workflow patterns, onboarding guidance, handoff rules, dispatch guidance, and a portfolio dashboard anchored on the existing 5-phase migration approach.

### Impact

New contributors now have a clear operating model for single-app and portfolio migrations, with BookShop positioned as the maturity benchmark and `reports/Report-Status.md` established as the formal handoff document.

---

## 2026-05-29 — Walkthroughs 06 and 07 Reframed as Pure CLI Squad Flows

### What Happened

Rewrote the Java API and Parts Unlimited walkthroughs as pure Copilot CLI experiences built around natural-language `@squad` prompts, added Mermaid phase diagrams, and removed chatmode-switching guidance from the main flow.

### Why

The walkthrough library already existed to make the migration system easier to drive by use case, but the two later guides still taught a mixed interface model. That made demos noisier, increased operator context switching, and weakened the story that the squad can be led from one command surface.

### Steering Moment

The key trade-off was to optimize for one canonical path instead of preserving every power-user shortcut in the main body. Advanced equivalents still exist, but they are now compressed into a short appendix so the walkthrough itself reads like one clean conversation with the crew.

### Impact

Use cases 06 and 07 now align with the repo's CLI-first guidance more cleanly, keep the Ocean's Twelve identity visible, and show where to ask the squad to fan out without forcing users to learn chatmode choreography first.

---
## 2026-05-28 — Training Program Added for the Seven Migration Use-Cases

### What Happened

Created `docs/training-program.md`, a production-ready enablement guide that maps all 7 migration use-cases to the 12 squad agents, exact skill files, prompt order, role-based training paths, assessment prompts, and a .NET version upgrade guide. `docs/onboarding.md` was also updated to point new teammates at the training program.

### Why

The repo already had modular prompts, a reusable `skills/` catalog, onboarding docs, and a mature BookShop reference, but there was no single document that told the team exactly what to learn, which prompt to start with, and which squad roles matter for each migration scenario.

### Steering Moment

The builder asked specifically for a use-case-by-use-case training map that covers Robert Borges' seven apps, the full Ocean's Twelve agent roster, prompt sequencing, role-based learning paths, and readiness checks rather than another conceptual overview.

### Impact

New teammates now have one canonical training map. Team leads can route work faster, assess readiness more consistently, and use BookShop as a benchmark while still teaching the right Azure defaults for WebForms, WCF, Java, and MVC migrations.

---

## 2026-05-29 — Walkthroughs 06 and 07 Reframed as Pure CLI Squad Flows

### What Happened

Rewrote the Java API and Parts Unlimited walkthroughs as pure Copilot CLI experiences built around natural-language `@squad` prompts, added Mermaid phase diagrams, and removed chatmode-switching guidance from the main flow.

### Why

The walkthrough library already existed to make the migration system easier to drive by use case, but the two later guides still taught a mixed interface model. That made demos noisier, increased operator context switching, and weakened the story that the squad can be led from one command surface.

### Steering Moment

The key trade-off was to optimize for one canonical path instead of preserving every power-user shortcut in the main body. Advanced equivalents still exist, but they are now compressed into a short appendix so the walkthrough itself reads like one clean conversation with the crew.

### Impact

Use cases 06 and 07 now align with the repo's CLI-first guidance more cleanly, keep the Ocean's Twelve identity visible, and show where to ask the squad to fan out without forcing users to learn chatmode choreography first.

---
## How to Use This Journal

> *Scribe's guide for the builder and future contributors.*

This isn't a changelog. It's the **story of how the project was built** — the decisions, the pivots, the moments where the builder steered the squad in a new direction.

### What to capture

| Entry Type | When | Example |
|-----------|------|---------|
| **Steering Moment** | Builder redirects the squad | "Switched from REST to GraphQL after seeing the query complexity" |
| **Key Decision** | Trade-off was made | "Chose SQLite over Postgres — this is a CLI tool, not a service" |
| **Evolution** | Architecture shifted | "Split monolith into 3 modules after hitting circular deps" |
| **Milestone** | Something shipped | "v0.1.0 published to npm — first public release" |
| **Lesson Learned** | Something surprised you | "Vitest runs 10x faster than Jest for this project — switching permanently" |

### Template for new entries

```markdown
## YYYY-MM-DD — Title

### What Happened

(What was built, changed, or decided)

### Why

(The reasoning — what alternatives existed, what trade-offs were made)

### Steering Moment

(How the builder directed the work — what prompt, feedback, or redirection shaped the outcome)

### Impact

(What this changes going forward)
```

### Rules

1. **Write for future-you.** Six months from now, this journal explains *why* the code looks the way it does.
2. **Capture the steering, not the typing.** The git log shows what changed. The journal shows *why it changed*.
3. **Be honest about pivots.** The best journals include "we tried X, it didn't work, here's why we switched to Y."
4. **Update after milestones, not after every commit.** Quality over quantity.

---

## 2026-05-29 — Walkthroughs 06 and 07 Reframed as Pure CLI Squad Flows

### What Happened

Rewrote the Java API and Parts Unlimited walkthroughs as pure Copilot CLI experiences built around natural-language `@squad` prompts, added Mermaid phase diagrams, and removed chatmode-switching guidance from the main flow.

### Why

The walkthrough library already existed to make the migration system easier to drive by use case, but the two later guides still taught a mixed interface model. That made demos noisier, increased operator context switching, and weakened the story that the squad can be led from one command surface.

### Steering Moment

The key trade-off was to optimize for one canonical path instead of preserving every power-user shortcut in the main body. Advanced equivalents still exist, but they are now compressed into a short appendix so the walkthrough itself reads like one clean conversation with the crew.

### Impact

Use cases 06 and 07 now align with the repo's CLI-first guidance more cleanly, keep the Ocean's Twelve identity visible, and show where to ask the squad to fan out without forcing users to learn chatmode choreography first.

---
*The code shows what was built. The journal shows why.*



## 2026-05-29
- Updated .github/prompts/SecurityHardening.prompt.md to add Frank Catton's squad-aware security review flow, readiness checks, severity branching, dispatch guidance, and CLI-first @squad follow-up commands for post-migration hardening.

## 2026-05-29 — Static Prompt Eval Harness Added for Core Workflow Prompts

### What Happened

Added `.squad\eval-prompts.mjs`, a focused Node.js harness that evaluates `QuickAssessment`, `SecurityHardening`, and `GetStatus` without calling a model. The script loads each prompt from `.github\prompts\`, parses frontmatter, resolves `#file:` references, checks required sections and expected output cues, prints a score table, and exits non-zero if any test case fails. To make the checks meaningful, the three prompts were tightened so target platform, recommended phases, auth/RBAC, and owner expectations are explicit in the prompt text.

### Why

The squad already had repo-wide governance checks, but it did not have one quick evaluator aimed at the three prompts operators are most likely to trust for triage, hardening, and status. That left prompt quality review broad, but not very scenario-specific.

### Steering Moment

The key choice was to keep this harness static and deterministic instead of simulating model runs. That makes it fast enough for routine use while still forcing the prompt text itself to carry the structural cues operators depend on.

### Impact

Prompt quality for the most operator-visible workflows can now be checked in one command — `node .squad\eval-prompts.mjs` — and the resulting pass/fail table makes it obvious when one of these prompts drifts away from its expected migration guidance.


