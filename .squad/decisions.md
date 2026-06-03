# Decisions — Ocean's Twelve — The Azure Heist

> Significant decisions made during development. Check before starting work.

## Active Decisions

### D-052: PPTX roster decks standardize on Ocean's Fourteen branding and 14-agent crew data
- **By:** Presentation Specialist
- **Date:** 2026-05-29
- **Context:** Multiple PPTX generator scripts under `docs\pptx\generators\` still mixed Ocean's Twelve wording, 12-agent counts, and pre-expansion roster data even after Presentation Specialist (#13) and Cost Engineer (#14) were added to the squad.
- **Decision:** Update the generator set to use Ocean's Fourteen branding where those decks describe the live heist squad, rename the main comparison deck output to `Oceans_Fourteen_Squad_vs_Prompting.pptx`, and extend roster-driven deck content to include Tess Ocean and The Accountant while preserving the shared LATAM helper module untouched.
- **Alternatives considered:** Update only the flagship deck; leave legacy naming in example decks; refactor the shared PPTX helper at the same time.
- **Trade-offs:** Some example decks still represent smaller Snap examples rather than the full 14-agent heist, so only roster sections directly tied to those examples were expanded instead of forcing every narrative slide to pretend it uses the full squad.

### D-047: Agent #14 — The Accountant (Cost Engineer) becomes the dedicated FinOps specialist
- **By:** Architect
- **Date:** 2026-05-29
- **Context:** Cost optimization already existed in the migration workflow, but lead ownership still sat with Azure Specialist while the squad roster had no dedicated FinOps or cost-governance specialist. That blurred who should own right-sizing, reservation guidance, budget guardrails, and post-migration spend reviews.
- **Decision:** Add Agent #14, **The Accountant** / **Cost Engineer**, as the lead for cost-focused work. Update the squad roster, routing, prompt and chatmode ownership, and hook guidance so cost, budget, spending, right-size, reserved instance, and savings triggers dispatch a dedicated specialist. Although the request referenced D-044, that identifier was already assigned earlier, so this addition is logged as D-047 to preserve stable decision references.
- **Alternatives considered:** Keep Azure Specialist as the lead for all cost work; treat cost optimization as a secondary concern under Architect; document FinOps guidance only in prompts without adding a dedicated agent.
- **Trade-offs:** Adds another specialist to coordinate, but it creates clear accountability for Azure spend optimization and makes monthly-savings estimates a first-class quality bar instead of an optional follow-up.

### D-051: Root `skills/` is now reference-only; `.github/skills/` remains the prompt authority
- **By:** Architect + Scribe
- **Date:** 2026-05-29
- **Context:** The repo carried both a root `skills/` catalog and a prompt-local `.github/skills/` layer, which risked implying equal authority for prompt wiring.
- **Decision:** Clarify root `skills/` as a reference-only catalog, keep `.github/skills/` as the authoritative prompt-local skill layer, rewrite `skills/INDEX.md` and `skills/README.md` to make that split explicit, add `REFERENCE ONLY` headers to duplicated root skill files, and verify `.github/prompts/` does not reference root `skills/`.
- **Alternatives considered:** Delete the root catalog; keep both folders undocumented; move every root skill into `.github/skills/` immediately.
- **Trade-offs:** The repo intentionally keeps duplicate-looking material in two places, but the ownership line is now explicit: root for catalog/reference, `.github/skills/` for prompt composition.

### D-048: PPTX release automation stays best-effort and template-aware
- **By:** DevOps Engineer + Tester
- **Date:** 2026-05-29
- **Context:** The repo already had multiple PPTX generators under docs\pptx\generators\, but producing decks for a release still depended on manual local execution and a LATAM template file that may not exist on GitHub-hosted runners.
- **Decision:** Add .github\workflows\pptx-generate.yml to run on published releases and manual dispatch. The workflow uses Python 3.11, installs python-pptx plus python-dotenv, resolves LATAM_TEMPLATE_PATH from an environment variable or committed fallback path, runs all or a selected generate_*.py script, and uploads resulting decks as release assets or workflow artifacts. If the template is missing, it warns and skips generation instead of failing the workflow.
- **Alternatives considered:** Fail the workflow when the template is missing; require the template to be committed in-repo before automation exists; create separate workflows per deck generator.
- **Trade-offs:** The workflow is intentionally non-blocking, so some runs may finish with warnings or partial deck output instead of a hard failure. That is acceptable because PPTX generation is a convenience release task, not a production deployment gate.

### D-049: Decision history gets a dedicated CLI timeline viewer
- **By:** Scribe
- **Date:** 2026-05-29
- **Context:** `.squad\decisions.md` had become dense enough that operators could read the raw file, but not quickly scan it by month, search for themes, or get a compact terminal summary.
- **Decision:** Add `.squad\view-decisions.mjs` as a zero-dependency Node.js viewer that parses decision headings and metadata, colorizes one-line timeline output, supports `--search` and `--last` filters, groups dated entries by month, and ends with a status summary while always exiting 0.
- **Alternatives considered:** Keep using the raw markdown file; rely on ad hoc grep commands; add a heavier dependency-based CLI formatter.
- **Trade-offs:** The parser assumes the current markdown decision pattern and infers status from section headings when explicit status lines are missing, but that keeps the tool lightweight and fast for daily squad scanning.

### D-050: The squad dashboard is a static browser artifact with pasted JSON health inputs
- **By:** Coder + Presentation Specialist + Scribe
- **Date:** 2026-05-29
- **Context:** The repo needed a polished showcase dashboard for squad health, roster visibility, quick stats, and operator commands, but the request explicitly required a single self-contained HTML file with no server or external dependencies.
- **Decision:** Add `.squad\dashboard.html` as a static, browser-opened control surface with inline CSS and JavaScript, hardcode the current 14-agent roster from `.squad\team.md`, and treat linter/eval rendering as paste-or-load JSON inputs rather than a live backend integration. Keep the quick-stats strip aligned to the live control surface at 14 agents and 8 chatmodes.
- **Alternatives considered:** Build a small local web app with a server; fetch script output dynamically from Node; keep the dashboard as a pure visual mock without pasteable health data.
- **Trade-offs:** The dashboard is portable and demo-friendly with zero setup, but users must paste or load exported results manually instead of seeing live script execution in-browser.

### D-046: Prompt and chatmode versioning uses file hashes as the baseline signal
- **By:** Evaluator + Scribe
- **Date:** 2026-05-29
- **Context:** The repo had 21 prompts and 7 chatmodes, but no lightweight registry showing their current version labels or any automated way to detect content drift between edits. That made prompt-quality reviews more manual than necessary and left the baseline state implicit.
- **Decision:** Add `.squad\prompt-versions.md` as the human-readable version ledger and `.squad\track-versions.mjs` plus `.squad\.prompt-hashes.json` as the machine-readable baseline. Use the first 8 characters of each file's SHA-256 hash to detect changes across `.github\prompts\` and `.github\chatmodes\`, and initialize every asset in the ledger at `v1.0` dated `2026-05-29`.
- **Alternatives considered:** Track versions only in markdown without automation; embed version metadata inside every prompt/chatmode file; use timestamps alone instead of content hashes.
- **Trade-offs:** The hash baseline is simple and low-maintenance, but it detects that content changed without describing semantic impact, so maintainers still need the markdown ledger to summarize what changed and why.

### D-045: Governance checks run in CI on governance-relevant pull requests
- **By:** DevOps Engineer + Evaluator + Scribe
- **Date:** 2026-05-29
- **Context:** D-043 established governance artifacts as the canonical squad operating surface, and D-044 established `.squad\lint-prompts.mjs` as the canonical prompt-library linter. Those controls still depended on contributors remembering to run them manually, which meant structural drift or governance regressions could survive until after review.
- **Decision:** Add a GitHub Actions pull-request workflow that runs the prompt linter and governance evaluator whenever a PR changes governance-relevant assets covered by the squad health path filters, while also allowing manual runs through `workflow_dispatch`.
- **Alternatives considered:** Run the checks only manually; run them on every PR regardless of scope; gate only on the linter and leave governance evaluation out of CI.
- **Trade-offs:** Path scoping keeps CI signal high and avoids penalizing unrelated changes, but the include list must stay current as the governance surface evolves.

### D-043: Governance artifacts become the canonical squad operating surface
- **By:** Evaluator + Tester + Scribe
- **Date:** 2026-05-29
- **Context:** `.squad\SCORECARD.md`, `.squad\eval.mjs`, `.squad\mcp-config.md`, `PORTFOLIO.md`, and the top-level `Use-cases\` entry point had drifted away from the live 13-agent, 7-target squad. Some files still described the old Fast Squad, some still used sample data, and the use-case root had no index explaining how it mapped to the current operator journey.
- **Decision:** Treat these governance/support files as part of the repo's active control surface. Refresh them to the current Ocean's Twelve roster, current prompt/chatmode catalog, current phase-gate language, and current 7-target portfolio view. Add `Use-cases\README.md` as a lightweight index, but do not move the folder because external references may depend on its path.
- **Alternatives considered:** Leave the files as low-priority templates; move `Use-cases\` under `docs\`; keep `PORTFOLIO.md` as a generic sample board with placeholder owners and dates.
- **Trade-offs:** This adds a little governance maintenance overhead, but it removes operator confusion and keeps routing, evaluation, MCP guidance, and portfolio navigation aligned to the repo's real workflow.

### D-044: Prompt linting treats broken structure as errors and coverage gaps as warnings
- **By:** Coder + Evaluator
- **Date:** 2026-05-29
- **Context:** The repo now carries 21 prompts, 23 prompt-local skills, 7 chatmodes, and multiple orchestration hooks. Structural drift was easy to introduce, but not every inconsistency should block contributors equally.
- **Decision:** Add `.squad\lint-prompts.mjs` as the canonical prompt-library linter. It fails on missing prompt/chatmode frontmatter fields or broken prompt skill references, warns on missing prompt hook references, prompt-scoped stale CLI patterns, root-path skill references, and unreferenced `.github\skills\` assets, and treats `InteractiveMigrationInterview` plus `TeamSkillAssessment` as the only hook-exempt prompts.
- **Alternatives considered:** Block on every warning; lint only prompts and ignore chatmodes; keep doing manual audits without a script.
- **Trade-offs:** Warning-level checks keep the linter actionable without turning informational gaps into hard failures, but some warnings (such as `pptx-generation.md` and `secret-management.md`, which are valid assets not currently referenced by prompts) remain intentionally advisory rather than proof of dead content.

### D-039: Chatmodes standardize on roster-aligned metadata and CLI-first follow-through
- **By:** Coder + Scribe
- **Date:** 2026-05-29
- **Context:** The seven chatmodes under `.github\chatmodes\` had drifted in structure and wording. Some lacked explicit `agent` metadata, some still pointed users toward stale completion phrasing, hook references were not consistently surfaced, and specialist awareness did not fully reflect the current 13-agent squad — especially for presentation/reporting scenarios.
- **Decision:** Standardize all seven chatmodes on a shared canonical shape: add `agent` to YAML frontmatter, align agent names to the current squad roster, include `.github\hooks\phase-gates.md` and `.github\hooks\agent-dispatch.md` as the common orchestration hook references, normalize skill references and command wording to repo canon, and convert completion guidance to CLI-first `@squad` follow-through. Preserve slash-style names only where they are true prompt-trigger references. Add Presentation Specialist awareness to `Migration-Orchestrator`, `Security-Review`, and `Cost-Optimization`.
- **Alternatives considered:** Leave each chatmode to evolve independently; preserve legacy slash-command completion guidance for familiarity; add Presentation Specialist references only in routing docs and not in chatmodes.
- **Trade-offs:** This makes the chatmodes more uniform and slightly less free-form, but the gain is a cleaner, auditable operator surface where metadata, routing, hooks, and next-step guidance all match the repo's current squad model.

### D-038: All 13 agent charters now share a required baseline structure
- **By:** Architect + Scribe
- **Date:** 2026-05-29
- **Context:** The 13 squad charters had grown unevenly: some already covered ownership and dispatch rules, while others only had identity and role-specific guidance. That inconsistency made it harder to route work automatically or understand each agent's boundaries at a glance.
- **Decision:** Standardize every charter around the same baseline skeleton — title, tagline, identity, How I Work, Domain Ownership, Core Capabilities, Auto-Dispatch Triggers, Quality Bar, Voice, Model, and Collaboration — while preserving existing role-specific guidance and only adding missing sections or missing identity/collaboration details.
- **Alternatives considered:** Rewrite every charter from scratch into a perfectly uniform template; leave richer charters alone and only patch the thinnest ones; move role-specific guidance out of the charters into a central file.
- **Trade-offs:** The charters remain slightly different in their role-specific middle sections, but the common baseline now makes routing, review, and future edits much more predictable without throwing away good existing content.

### D-037: Prompt skill references standardize on `.github/skills/`
- **By:** Coder
- **Date:** 2026-05-29
- **Context:** Assessment and triage prompts were still split between legacy root `skills/` references and prompt-local `.github/skills/` references, which blurred the authoritative orchestration layer and left some shared prompt dependencies outside the prompt-local catalog.
- **Decision:** Standardize prompt-facing `#file:` references on `.github/skills/`, promote the four missing prompt-consumed skills (`migration-report-template.md`, `asp-classic-to-dotnet.md`, `docker-containerize.md`, `azure-container-apps.md`) into `.github/skills/`, and update `skills/README.md` to document the two-layer convention while telling maintainers to promote any root-only skill before wiring it into a prompt.
- **Alternatives considered:** Keep mixed prompt references; move all skills back to the root catalog; copy the entire root catalog into `.github/skills/` immediately.
- **Trade-offs:** The repo still carries a broader root knowledge catalog, but prompt authors now have one canonical skill path and a clearer promotion rule for any future skill a prompt needs.

### D-036: Docs root now routes readers through purpose-based subfolders
- **By:** Tester/DevRel
- **Date:** 2026-05-29
- **Context:** `docs\` had accumulated a dozen loose markdown files at the root, which made navigation noisier and left path references scattered across README, onboarding materials, the project map, decisions, and the journal.
- **Decision:** Reorganize the flat docs root into `docs\architecture\`, `docs\guides\`, and `docs\onboarding\`, keep existing specialized folders (`walkthroughs`, `use-case-cheatsheets`, `squad-interactive`, `pptx`) in place, remove `docs\__pycache__`, and refresh internal references so operators can follow the new structure without dead paths.
- **Alternatives considered:** Leave the flat layout in place; move only a subset of files; add an index without changing the filesystem layout.
- **Trade-offs:** The reorganization touches many references and makes some historical notes point to relocated files, but the docs tree becomes easier to scan and future additions now have clear homes.

### D-035: Hook routing now treats all 13 agents as first-class participants
- **By:** Coder
- **Date:** 2026-05-29
- **Context:** The migration hooks in `.github\hooks\agent-dispatch.md`, `.github\hooks\phase-gates.md`, and `.github\hooks\use-case-routing.md` still reflected only a partial squad roster. Tess Ocean (Presentation Specialist) and several other agents were missing from dispatch triggers, phase gate language, or use-case routing coverage.
- **Decision:** Update the three hook documents so all 13 agents are named at least once, add Presentation Specialist auto-dispatch for deliverables/reports/executive summaries/deck and PPTX requests, make phase gate descriptions explicitly call out relevant specialists by name, and reserve Phase 6 for stakeholder-ready reporting with Presentation Specialist support.
- **Alternatives considered:** Keep Presentation Specialist implied through PPTX skills only; add the missing agents only to one central table; postpone hook cleanup until more prompt rewrites landed.
- **Trade-offs:** The hook docs are slightly more verbose, but routing is now explicit, easier to audit, and less likely to omit specialist dispatch during migration orchestration.

### D-034: README now reflects the 13-agent, 19-skill CLI-first operating model
- **By:** Tester/DevRel
- **Date:** 2026-05-29
- **Context:** The repo added Tess Ocean as Agent #13, expanded `.github\skills\` to 19 prompt-local skills, introduced PPTX authoring guidance, and shifted prompt handoffs toward CLI-first `@squad` commands, but `README.md` still showed stale counts and several old slash-style operator examples.
- **Decision:** Update `README.md` to treat the current squad inventory as canonical (13 agents, 19 prompt-local skills, 21 prompts), add the PPTX deck library reference, insert Tess Ocean anywhere the crew is enumerated, and translate user-facing scenario/example commands to the current `@squad` equivalents while preserving slash-command names only where the README is explicitly documenting prompt identities.
- **Alternatives considered:** Leave the README partially stale; rewrite every slash reference including prompt-name reference tables; document PPTX only in `docs\pptx\README.md`.
- **Trade-offs:** The README now mixes CLI-first operator commands with a few preserved slash-command reference tables, but that split better matches how the repo is used today: operators run `@squad`, while maintainers still need the underlying prompt names for routing and catalog documentation.

### D-033: PPTX generators now consume the shared LATAM helper module
- **By:** Coder
- **Date:** 2026-05-29
- **Context:** Eight deck generators under `docs\pptx\generators\` still duplicated the LATAM GCS color palette and ~200 lines of helper logic even after `latam_gcs_template.py` existed as the canonical shared module.
- **Decision:** Refactor all eight generators to import only the shared colors/helpers they actually use from `latam_gcs_template.py`, keep deck-specific helpers inline, and align every shared helper call site to the module API by passing `prs` into `add_slide`/`add_title_bar` and `prs, TOTAL_SLIDES` into `add_footer`.
- **Alternatives considered:** Leave each generator self-contained; centralize only colors while keeping helper duplication; postpone the migration and keep the shared module unused.
- **Trade-offs:** The refactor required touching many call sites and preserving a few deck-specific helper functions/constants such as `NAVY`, but it removes drift across decks and makes future template changes land in one place.

### D-032: PPTX deck authoring guidance lives in a shared skill plus deck README
- **By:** Coder
- **Date:** 2026-05-29
- **Context:** The repo already had shared PPTX helpers in `docs\pptx\generators\latam_gcs_template.py` and several deck generators, but there was no single operator-facing skill explaining the shared module pattern, reusable layouts, and how to ask the squad to create or modify decks.
- **Decision:** Add `.github\skills\pptx-generation.md` as the canonical skill for deck generation and expand `docs\pptx\README.md` with creation steps, `@squad` prompts, reusable layout samples, and a generator inventory table.
- **Alternatives considered:** Keep PPTX guidance only in source code comments; document only the README without a reusable skill; create deck-specific instructions in each generator.
- **Trade-offs:** This adds another authoritative skill file to maintain, but it makes deck creation more discoverable, reduces repeated explanation in future prompts, and keeps generator usage aligned to the shared helper surface.

### D-031: Agent #13 — Tess Ocean (Presentation Specialist) added to squad
- **By:** Architect
- **Date:** 2026-05-29
- **Context:** The squad had 8 PPTX generators, a shared template module, and frequent deck creation needs, but no agent owned this domain. The Tester handles docs/walkthroughs and the Scribe handles milestones — neither covers visual communication.
- **Decision:** Added Agent #13 "Tess Ocean" as Presentation Specialist with auto-dispatch on deck/PPTX requests. Also creating a `.github/skills/pptx-generation.md` skill and refactoring all generators to import from the shared `latam_gcs_template.py` module.
- **Trade-offs:** Adds coordination complexity (13 agents), but PPTX is a distinct domain requiring python-pptx expertise, GCS template knowledge, and visual design rules that don't fit other roles. The Ocean's Twelve theme extends naturally — Tess Ocean joins as the 13th member in the movie sequel.
- **Affected:** routing.md (new work type + auto-dispatch trigger), team.md (new member), AGENTS.md (quick reference + dispatch rules), all PPTX generators (refactored to shared module)

### D-030: Prompt handoffs standardize on CLI-first `@squad` commands while keeping slash trigger names
- **By:** Coder
- **Date:** 2026-05-29
- **Context:** The migration prompt library still mixed legacy slash-command references into completion guidance and next-step sections, even though the repo's operating model has been shifting toward Copilot CLI-first `@squad` orchestration. At the same time, `skills\managed-identity.md`, `skills\rbac-least-privilege.md`, and `skills\secret-management.md` needed authoritative `.github\skills\` copies that match the newer orchestration-skill style.
- **Decision:** Promote those three root skills into enhanced `.github\skills\` orchestration versions, keep the root copies unchanged as legacy catalog entries, and replace mapped slash-command references with CLI-first `@squad` commands everywhere in prompt completion guidance and recommendation text while deliberately preserving slash trigger names inside **When to Use** sections.
- **Alternatives considered:** Leave the legacy skill files as the only source; replace every slash-command mention everywhere including trigger sections; keep mixed slash and `@squad` guidance in completion text.
- **Trade-offs:** The repo now carries parallel legacy and authoritative copies of some skills, but operators get clearer canonical orchestration guidance and prompts keep recognizable VS Code trigger names where users still need them.

### D-029: Security hardening prompt composes focused Azure security skills
- **By:** Security Auditor + Coder
- **Date:** 2026-05-29
- **Context:** `.github\prompts\SecurityHardening.prompt.md` previously kept `azure-entra-id.md` but paired it with generic migration skills that did not directly cover secrets, network hardening, Defender for Cloud, or OWASP review depth.
- **Decision:** Add dedicated security skills for Key Vault and secret handling, network security, Defender/compliance posture, and OWASP Top 10 review, while keeping `azure-entra-id.md` as the identity anchor for the security hardening flow.
- **Alternatives considered:** Keep expanding the prompt inline; retain generic migration skills and rely on ad hoc security guidance; create one monolithic security skill instead of four focused modules.
- **Trade-offs:** The prompt now depends on more skill files, but the security guidance is more reusable, easier to maintain, and better aligned to the hardening workflow.

### D-028: Borges-Brady deck shifts to a four-act Factory narrative
- **By:** Coder
- **Date:** 2026-05-29
- **Context:** `docs\generate_borges_brady_deck.py` needed to stop reading like an informational comparison deck and instead persuade Factory stakeholders that Roberto Borges' migration playbook plus Brady Squad orchestration creates a scalable delivery engine.
- **Decision:** Rebuild the deck as a 15-slide four-act story (problem, solution, factory scale, future evolution), keep the LATAM GCS template and existing helper set unchanged, and express the strongest differentiators through white cards with inset accents, explicit ROI claims, and detailed speaker notes on every slide.
- **Alternatives considered:** Keep the earlier 12-slide informational structure; add only a few persuasion slides without changing the narrative arc; redesign the helpers and visual system at the same time.
- **Trade-offs:** The longer narrative takes more slide real estate, but it creates a clearer executive arc for Factory growth while preserving the existing branded generator pattern and editable native PowerPoint output.

### D-027: LATAM GCS PPTX helpers move into a shared palette module
- **By:** Coder
- **Date:** 2026-05-29
- **Context:** `docs\generate_oceans_twelve_deck.py` and `docs\generate_borges_brady_deck.py` both carried near-identical LATAM GCS color constants and slide helper functions, which makes future deck fixes easy to miss or apply inconsistently.
- **Decision:** Add `docs\latam_gcs_template.py` as the canonical shared module for the LATAM template path, palette constants, and common helper functions, using `generate_oceans_twelve_deck.py` as the source of truth for the richer helper variants such as `add_accent_line(..., inside=True)` and white card helpers.
- **Alternatives considered:** Keep duplicating helpers in each generator; fully refactor both generators in the same change; create a narrower colors-only module.
- **Trade-offs:** Centralizing the helpers lowers drift and makes future deck updates safer, but this task intentionally stops short of rewiring the generators so adoption can happen in a separate low-risk change.

### D-026: Borges-Brady deck cards use inset accents on white fills
- **By:** Coder
- **Date:** 2026-05-29
- **Context:** `docs\generate_borges_brady_deck.py` generated rounded metric, column, and stat cards with the accent line placed flush at the card boundary and with the default card fill inherited from `CARD_BG`, which made the line appear to float above the rounded corners and left the cards grayer than intended.
- **Decision:** Update `add_accent_line` to support `inside=True`, use that inset mode for every accent line drawn immediately after a card, and standardize those deck cards on `bg_color=WHITE` while preserving the one intentionally dark quote card.
- **Alternatives considered:** Leave the line at the outer edge; manually offset only a subset of card accents; keep the gray fill and adjust only the line placement.
- **Trade-offs:** The fix adds a small amount of helper logic and explicit card fill arguments, but it makes the generated slides render cleanly inside rounded corners and aligns the card surfaces with the intended white presentation style.

### D-025: Comparison deck generators stay native to the LATAM PowerPoint pattern
- **By:** Coder
- **Date:** 2026-05-29
- **Context:** The repo already had `docs\generate_oceans_twelve_deck.py` using the LATAM template, GCS theme colors, and a large helper-function set to generate editable stakeholder decks as native PowerPoint shapes.
- **Decision:** Add `docs\generate_borges_brady_deck.py` by preserving that exact generator pattern, reusing the same template path, helpers, theme tokens, slide cleanup flow, footer format, and speaker-note approach while creating a new 12-slide story focused on why Roberto Borges' migration expertise and Brady Gaster's squad framework are stronger together.
- **Alternatives considered:** Hand-build the presentation in PowerPoint; create a one-off generator with a different helper set or theme; export static images instead of editable shapes.
- **Trade-offs:** Reusing the established pattern keeps the output visually consistent, editable, and low-risk, but it requires meticulous slide layout work to stay within deck boundaries and match the existing generator conventions.

### D-024: Generic interactive interview is the default migration entrypoint
- **By:** Architect
- **Date:** 2026-05-29
- **Context:** The repo still contains BookShop-specific prompt references under `Use-cases\05-BookShop\docs`, but new migration work needs an app-agnostic front door that interviews the user, validates answers against the codebase, and produces a reusable phase plan.
- **Decision:** Add `.github/prompts/InteractiveMigrationInterview.prompt.md` as the canonical intake prompt for fresh migrations, supported by `docs/squad-interactive/README.md` and `docs/squad-interactive/example-session.md` so operators learn one conversational flow with scan, clarifying questions, phase navigation, status, and fan-out execution.
- **Alternatives considered:** Keep starting from BookShop-specific reference docs; add more per-use-case starter prompts instead of one generic interview; keep the flow conceptual without a concrete example session.
- **Trade-offs:** The generic interview lowers onboarding friction and fits more applications, but it shifts more responsibility into discovery quality and requires the prompt to be explicit about decision points, defaults, and phase controls.


### D-023: BookShop prompt docs are archived examples, not migration starters
- **By:** Scribe
- **Date:** 2026-05-29
- **Context:** Recent walkthrough and index work has been reframing the repo around a CLI-first operating model. In `Use-cases\05-BookShop\docs`, the BookShop prompt references risk reading like reusable starter templates unless the docs explicitly mark them as historical outputs from a completed migration.
- **Decision:** Treat the BookShop prompt docs as archived completed-migration examples, add a local README/index plus top-of-file banners that say they are reference material, and point new migration work to the interactive squad interview as the generic entrypoint.
- **Alternatives considered:** Leave the existing filenames and prose to imply historical context; keep the docs reusable as prompt templates for fresh migrations; push the archive warning into only one central index.
- **Trade-offs:** The archive framing reduces ambiguity for new operators and protects the CLI-first onboarding story, but these BookShop documents become less reusable as copy-paste starting prompts because they are now intentionally positioned as historical references.

### D-022: Walkthroughs 04 and 05 standardize on pure CLI `@squad` flows
- **By:** Tester/DevRel + Scribe
- **Date:** 2026-05-29
- **Context:** The Contoso University and Bookshop walkthroughs still needed legacy mixed-surface guidance removed so the walkthrough set could teach one consistent Copilot CLI operating model across the largest multi-project .NET case and the SAP CAP Java migration case.
- **Decision:** Rewrite `docs/walkthroughs/04-contoso-university-walkthrough.md` and `05-bookshop-reference-walkthrough.md` as pure CLI walkthroughs driven by natural-language `@squad` prompts, add Mermaid phase diagrams, make `fan out` explicit where parallelism matters, and confine old slash-style equivalents to a short appendix note.
- **Alternatives considered:** Keep the mixed CLI plus Chat Panel flow; shorten the guides to one-shot prompts only; preserve old shortcuts inline in every phase.
- **Trade-offs:** The main path is now cleaner and more demoable, but advanced operators see fewer embedded alternate controls because legacy shortcuts are intentionally compressed into the appendix.

### D-020: Walkthroughs 01-03 standardize on pure CLI `@squad` flows
- **By:** Tester/DevRel + Scribe
- **Date:** 2026-05-29
- **Context:** The first three legacy modernization walkthroughs still taught a mixed interface model with mainline Chat Panel references, even though the repo's operator story now centers on a single Copilot CLI surface led by natural-language `@squad` prompts.
- **Decision:** Rewrite `docs/walkthroughs/01-classic-asp-walkthrough.md`, `02-dotnet30-webforms-walkthrough.md`, and `03-wcf-to-rest-walkthrough.md` as pure CLI walkthroughs with Mermaid phase diagrams, explicit fan-out prompts where parallel work helps, natural follow-up questions, and only a short power-user appendix for Chat Panel shortcuts.
- **Alternatives considered:** Keep the mixed CLI plus Chat Panel format; document only one-shot prompts; remove advanced shortcuts entirely.
- **Trade-offs:** The walkthroughs now tell a cleaner single-surface story and are easier to demo, but advanced users see fewer in-line alternate controls because those have been intentionally moved to the appendix.

### D-021: Walkthroughs 06 and 07 standardize on pure CLI `@squad` flows
- **By:** Tester/DevRel
- **Date:** 2026-05-29
- **Context:** The Java API and Parts Unlimited walkthroughs still mixed Copilot CLI prompts with chatmode switching and Chat Panel instructions, which diluted the single-surface operator story the walkthrough set is supposed to teach.
- **Decision:** Rewrite walkthroughs 06 and 07 so the main flow is entirely natural-language `@squad` prompts in Copilot CLI, add Mermaid phase diagrams to visualize the handoffs, and move old advanced equivalents into a short appendix instead of embedding alternate surfaces throughout the guide.
- **Alternatives considered:** Keep the mixed CLI plus chatmode format; split each walkthrough into separate basic and advanced versions; leave the old flow and add only a short note.
- **Trade-offs:** The walkthroughs are now clearer and more consistent for operators and demos, but advanced users see fewer in-line shortcuts because alternate surfaces are intentionally pushed to the appendix.

### D-019: Walkthrough guidance is CLI-first and one-surface
- **By:** Tester/DevRel + Scribe
- **Date:** 2026-05-29
- **Context:** The initial walkthrough index mixed Copilot CLI guidance with chat-panel switching, even though the migration experience is now centered on natural-language squad orchestration from a single entry surface.
- **Decision:** Rewrite `docs/walkthroughs/README.md` as a CLI-first index that teaches `@squad` + natural language as the primary entrypoint, shows the shared squad fan-out pattern once, and presents all seven use cases through one consistent quick-start table with one-shot prompts.
- **Alternatives considered:** Keep mixed CLI/chat-panel instructions in the index; document each use case independently without a shared squad pattern.
- **Trade-offs:** The index is simpler and more repeatable for operators, but it is intentionally less focused on chatmode-specific steering at the top level because the walkthrough set now optimizes for one-surface onboarding first.

### D-018: Skill hierarchy is documented and overlapping skills resolve to `.github/skills/`
- **By:** Architect
- **Date:** 2026-05-28
- **Context:** The repo now contains both a legacy root `skills/` catalog and a prompt-local `.github/skills/` catalog, with 10 duplicated filenames referenced by different prompts and chatmodes. Without an explicit rule, contributors cannot tell which copy is authoritative.
- **Decision:** Keep both layers for now, but treat `.github/skills/` as the canonical copy for every overlapping skill because those variants are more complete and power the orchestrated workflow prompts. Add `skills/INDEX.md`, `docs/PROJECT-MAP.md`, and `docs/PROMPT-CATALOG.md` as the discovery and governance layer that explains references, overlap, and project structure.
- **Alternatives considered:** Delete the root duplicates immediately; move all prompt-local skills back into the root catalog; keep both catalogs without documentation.
- **Trade-offs:** Temporary duplication remains so existing chatmodes and legacy prompts do not break, but the repo now has an explicit authority model and a reliable navigation layer for future consolidation.

### D-017: README navigation favors grouped discovery over one flat index
- **By:** Tester/DevRel
- **Date:** 2026-05-28
- **Context:** `README.md` had grown into a long control-tower document with strong content, but the flat table of contents and always-expanded reference blocks made it harder to scan by audience intent.
- **Decision:** Keep the section content intact, but reorganize navigation into grouped overview/getting-started/migration/reference/documentation/decision-maker/community buckets, add a short navigation guide, and collapse the longest prompt catalogs so readers can progressively disclose detail.
- **Alternatives considered:** Reorder the entire README body; trim or rewrite repeated content across sections.
- **Trade-offs:** Grouped navigation improves discoverability without rewriting the document, but some repeated content remains in place because preserving section text was prioritized for this pass.

### D-016: Squad identity and migration charters are canonicalized
- **By:** Evaluator
- **Date:** 2026-05-28
- **Context:** Core squad docs still referenced the Fast Squad identity, the original three charters still described a TypeScript/Vitest/ESM app workflow, and prompt metadata was inconsistent across the migration prompt catalog.
- **Decision:** Standardize the repo on the Ocean's Twelve — The Azure Heist identity, rewrite the Architect/Coder/Tester charters for Azure migration work (.NET, Java, prompt authoring, IaC, validation, walkthroughs), normalize prompt frontmatter, and clarify that Phase 5 hands off to Phase 6 rather than declaring the migration complete.
- **Alternatives considered:** Patch only the most visible identity strings; leave the original fast-preset language and JavaScript-centric charter details in place.
- **Trade-offs:** The docs are denser and require coordinated updates across several files, but routing, prompt behavior, and squad expectations now match the actual Azure migration repository.

### D-014: README becomes the architect-facing control-tower narrative
- **By:** Tester/DevRel
- **Date:** 2026-05-28
- **Context:** The repository had strong prompts, skills, routing, and training assets, but the root README still read like a generic prompt library overview instead of a persuasive explanation of why Ocean's Twelve orchestration matters.
- **Decision:** Rewrite `README.md` as the canonical architect-and-developer entrypoint with visual-first Mermaid diagrams, an explicit squad-vs-monolith comparison, role-based navigation, examples, and a clear split between chatmodes, prompts, skills, hooks, and targets.
- **Alternatives considered:** Keep the short README and push readers into `docs/ARCHITECTURE.md`; add a lighter README with fewer diagrams.
- **Trade-offs:** The README is longer, but it now carries the full system story in one place and lowers onboarding cost for architects, developers, and stakeholders.

### D-013: Presentation deck is generated as editable native PowerPoint shapes
- **By:** Coder
- **Date:** 2026-05-28
- **Context:** Roberto Borges needed a persuasive stakeholder deck comparing Ocean's Twelve squad orchestration against monolithic prompting, using the LATAM template and GCS theme.
- **Decision:** Build the deck as a Python-driven `python-pptx` presentation that reuses the LATAM template, copies the established helper-function pattern, and renders diagrams as native PowerPoint shapes so the output stays brand-aligned and editable.
- **Alternatives considered:** Depend on Mermaid image rendering for all diagrams; hand-author the presentation manually.
- **Trade-offs:** Native shapes require more layout code, but they keep the slides deterministic, editable by presenters, and visually consistent with the existing LATAM deck generators.

### D-001: Squad bootstrapped from the fast preset
- **By:** snap-squad
- **Date:** 2026-05-28
- **Context:** Project initialized using snap-squad warm-start before the Azure migration specialization was fully defined.
- **Decision:** Start from the `fast` preset as scaffolding, then evolve the repo into Ocean's Twelve — The Azure Heist once the twelve-agent Azure migration model is established.

### D-004: Team workflow docs treat specialist roles as functional overlays
- **By:** Tester/DevRel
- **Date:** 2026-05-28
- **Context:** The repo already has Architect, Coder, and Tester, but Robert's migration team also needs guidance for Cloud Engineer, DevOps, Security, and QA responsibilities.
- **Decision:** Document those roles as workflow responsibilities with mapped squad-agent equivalents and explicit fallbacks when Azure Specialist or Security Auditor agents are not yet present in `.squad/team.md`.
- **Trade-off:** The guidance is immediately usable without restructuring the squad, but teams must understand that some specialist names are conceptual role mappings rather than preconfigured squad members.

### D-002: New migration skills follow the Phase1 structured template
- **By:** Coder
- **Date:** 2026-05-28
- **Context:** The prompt library was expanded with post-migration operations, rollback, database, security, cost, quick assessment, and debugging support.
- **Decision:** New prompt and chatmode additions use the existing frontmatter, step-based structure, explicit rules, and output checklists so they remain consistent with `Phase1-PlanAndAssess.prompt.md` and easy to adopt in the current workflow.

### D-003: Prompt system moves to thin entrypoints plus modular libraries
- **By:** Architect
- **Date:** 2026-05-28
- **Context:** The current migration experience is centered on a monolithic chatmode and flat phase prompts, which makes reuse, team routing, per-use-case overrides, and role-based ownership hard to scale.
- **Decision:** Keep slash-command compatibility in `.github/prompts/`, but move authoring to a modular `prompt-library/` split by phase, role, technology, and reusable skills, with specialized chatmodes and per-use-case override folders.
- **Alternatives considered:** Keep the flat prompt layout and only add more prompts; move everything into use-case-specific docs.
- **Trade-offs:** Adds more files and a composition model, but sharply reduces duplication, enables squad routing, and prevents giant reference documents from becoming the source of truth.

### D-005: Skills live in a single root-level catalog
- **By:** Coder
- **Date:** 2026-05-28
- **Context:** The migration prompts need reusable building blocks that can be referenced consistently from `.github/prompts/*.prompt.md` without duplicating migration guidance.
- **Decision:** Adopt a single root-level `skills/` catalog for reusable migration guidance, with prompts in `.github/prompts/` referencing skills via `#file:skills/<skill>.md`; prioritize 8 fully authored cross-phase skills and keep the remaining 18 as structured outlines to maximize reuse while controlling authoring cost.
- **Alternatives considered:** Keep all guidance embedded in each phase prompt; place skills under `.github/skills`; fully author all 26 skills before wiring prompt references.
- **Trade-offs:** Root-level `skills/` keeps references predictable and prompt files thin, but requires catalog discipline and ongoing curation to prevent overlap.

### D-011: Orchestrated skills and hooks move under `.github/`
- **By:** Coder
- **Date:** 2026-05-28
- **Context:** The new orchestration layer must connect chatmodes, prompts, skills, and squad-agent handoffs using GitHub prompt-local file references and reusable hook rules.
- **Decision:** Add the production skill library under `.github/skills/` and orchestration rules under `.github/hooks/`, then wire all 13 prompt entrypoints to those references via `#file:.github/...` so prompt composition and dispatch guidance live next to the prompt assets they govern.
- **Alternatives considered:** Continue expanding the legacy root-level `skills/` catalog; keep orchestration embedded inside each prompt; document routing only in README/docs.
- **Trade-offs:** Duplicates some legacy guidance temporarily, but makes prompt-local composition clearer, reduces hidden coupling, and creates an explicit home for phase gates and agent dispatch rules.

### D-008: Azure training defaults follow use-case-specific hosting and data baselines
- **By:** Azure Specialist
- **Date:** 2026-05-28
- **Context:** The new training program needed one opinionated Azure path per use-case so architects do not mix legacy implementation details with the intended modernization targets.
- **Decision:** Standardize training on App Service for classic/.NET web monoliths, Container Apps for containerized API-first modernizations, AKS only when Kubernetes control is justified, Azure SQL for the relational .NET tracks, PostgreSQL-first for the Java API unless Cosmos DB is explicitly justified, and Bicep + AVM + azd as the default IaC/deployment path. **Exception:** BookShop remains the practical reference implementation for App Service + Azure SQL because the checked-in artifacts are the benchmark the team can study today.
- **Trade-off:** The training stays opinionated without ignoring the implemented BookShop benchmark, but the guide must now distinguish between default modernization targets and the repo's current reference architecture when those differ.

### D-010: Training program becomes the canonical use-case map
- **By:** Architect
- **Date:** 2026-05-28
- **Context:** The repo already had prompts, skills, onboarding docs, and a BookShop benchmark, but it lacked one canonical document that joins use-cases, squad roles, skill files, prompt order, learning paths, and readiness checks.
- **Decision:** Use `docs/training-program.md` as the primary enablement document for the 7 use-cases. Keep it grounded in the current slash commands, exact `skills/` files, and the BookShop reference implementation, while explicitly calling out gaps such as the missing PostgreSQL-specific skill file.
- **Trade-off:** A single source of truth reduces onboarding confusion and prompt drift, but it must be curated whenever prompts, skills, or benchmark architectures change.

### D-009: Technology-specific assessment prompts mirror the Phase1 structure
- **By:** Coder
- **Date:** 2026-05-28
- **Context:** Roberto Borges' team needed production-ready prompts for version-specific .NET and Java upgrades, WCF/WebForms/Classic ASP triage, team readiness evaluation, and ultra-fast intake beyond the generic Phase 1 assessment.
- **Decision:** Add focused assessment prompts under `.github/prompts/` that keep the standard YAML frontmatter, numbered workflow steps, rules, deliverables, and output checklists while tailoring report outputs and guidance to each legacy technology and use-case.
- **Alternatives considered:** Expand `Phase1-PlanAndAssess.prompt.md` with more conditionals; keep only a single quick assessment prompt.
- **Trade-offs:** More prompt files increase catalog size, but they reduce ambiguity for migration teams, improve reuse across the seven use-cases, and make targeted assessments easier to dispatch and review.

### D-007: Training docs standardize on current commands and the implemented BookShop reference
- **By:** Tester/DevRel
- **Date:** 2026-05-28
- **Context:** Roberto Borges needed production-ready training material that maps skills, prompts, and squad dispatch patterns across the repo's seven migration use-cases.
- **Decision:** Build the training set around the slash commands and skills that already exist in the repository, and use exact natural-language prompt recipes for scenario-specific steering. Document BookShop's implemented target architecture as App Service + Azure SQL because the repository artifacts are the authoritative reference implementation.
- **Alternatives considered:** Invent new training-only slash commands; mirror the stale target note from `.squad/team.md`; keep the docs conceptual instead of copy-pasteable.
- **Trade-offs:** The docs stay truthful and executable today, but they must carry more prompt examples because the command surface is phase-based rather than use-case-specific.

### D-006: Migration chat experience uses a master orchestrator plus specialist chatmodes
- **By:** Architect
- **Date:** 2026-05-28
- **Context:** `Code-Migration-Modernization.chatmode.md` had grown into a monolithic workflow prompt that mixed assessment, code migration, infrastructure, deployment, CI/CD, and quality rules in one place.
- **Decision:** Replace the monolith with `Migration-Orchestrator.chatmode.md` as the master coordinator, slim `Code-Migration-Modernization.chatmode.md` down to a Phase 2 specialist, and add focused chatmodes for quick assessment, security review, Azure infrastructure, and cost optimization.
- **Alternatives considered:** Keep extending the monolith; create only specialist chatmodes without a master coordinator.
- **Trade-offs:** The orchestrator model adds more files and routing metadata, but it makes ownership explicit, enables cleaner handoffs, and lets prompts and skills evolve independently.

### D-012: Routing becomes the authoritative twelve-agent dispatch map
- **By:** Architect
- **Date:** 2026-05-28
- **Context:** `.squad/routing.md` still reflected the original fast-squad shorthand even though the repository now has 12 active agents, 13 prompt files, a dedicated debugging chatmode, and 7 migration use-cases.
- **Decision:** Rewrite `.squad/routing.md` as the authoritative control-tower document with full work-type ownership, prompt-to-agent dispatch mapping, phase quality gates, automatic secondary-routing triggers, and use-case-specific critical agent guidance.
- **Alternatives considered:** Keep the lightweight routing table and infer specialist dispatch ad hoc; split routing across several smaller documents.
- **Trade-offs:** The routing file is now denser and must stay synchronized with the prompt library, but the squad gains explicit ownership, faster dispatch decisions, and fewer handoff gaps.

### D-015: CLI walkthroughs are organized by use case with a shared index
- **By:** Tester/DevRel + Scribe
- **Date:** 2026-05-28
- **Context:** The repository had strong phase-based prompts and training docs, but users still needed concrete CLI-first guidance for each of the seven migration scenarios.
- **Decision:** Add `docs/walkthroughs/README.md` plus seven scenario-specific walkthroughs, organized by use case rather than only by migration phase, while keeping all guidance aligned to the existing prompts, chatmodes, skills, and routing model.
- **Alternatives considered:** Keep walkthrough content inside `docs/training-program.md`; create one generic CLI walkthrough for all apps.
- **Trade-offs:** This adds more documentation files to maintain, but it makes the workflow easier to follow, improves discoverability, and reduces ambiguity for scenario-specific migrations.

### D-016: Add a dedicated onboarding chatmode as the default entrypoint for new operators
- **By:** Tester/DevRel
- **Date:** 2026-05-29
- **Context:** New users had prompt lists and walkthrough docs, but no single interactive chatmode that introduced the squad, explained the control surface, and pointed them to the first useful commands.
- **Decision:** Add `.github/chatmodes/Onboarding.chatmode.md` as a guided squad tour that explains the 13 agents, the prompts -> skills -> hooks model, common workflows, key files, and health-check commands, while referencing the migration report template skill and agent-dispatch hook.
- **Alternatives considered:** Keep onboarding split across README and docs only; overload `Migration-Orchestrator` with first-time user education.
- **Trade-offs:** This adds another chatmode to maintain and keeps repo counts/docs in sync, but it gives first-time users a clearer starting point without diluting the migration-focused specialist modes.

### D-016: Add a dedicated onboarding chatmode as the default entrypoint for new operators
- **By:** Tester/DevRel
- **Date:** 2026-05-29
- **Context:** New users had prompt lists and walkthrough docs, but no single interactive chatmode that introduced the squad, explained the control surface, and pointed them to the first useful commands.
- **Decision:** Add `.github/chatmodes/Onboarding.chatmode.md` as a guided squad tour that explains the 13 agents, the prompts -> skills -> hooks model, common workflows, key files, and health-check commands, while referencing the migration report template skill and agent-dispatch hook.
- **Alternatives considered:** Keep onboarding split across README and docs only; overload `Migration-Orchestrator` with first-time user education.
- **Trade-offs:** This adds another chatmode to maintain and keeps repo counts/docs in sync, but it gives first-time users a clearer starting point without diluting the migration-focused specialist modes.

## 2026-05-29
- Rewrote SecurityHardening.prompt.md to be dynamic and squad-aware while preserving YAML frontmatter. Standardized CLI-first @squad commands, added lightweight readiness gating, severity checkpoints, and routing via existing agent-dispatch hooks instead of duplicating squad logic.

### D-045: Prompt eval harness scores static quality per named workflow
- **By:** Evaluator
- **Date:** 2026-05-29
- **Context:** The repo already had a broad governance evaluator and prompt linter, but no focused harness that validates whether specific high-value prompts structurally support expected operator outputs for representative migration requests.
- **Decision:** Add `.squad\eval-prompts.mjs` as a static, prompt-specific eval harness for `QuickAssessment`, `SecurityHardening`, and `GetStatus`. The harness parses frontmatter, resolves `#file:` references, checks required sections, scores expected output coverage from prompt text, prints a per-test-case score table, and exits non-zero on any failure. Tighten the three prompts just enough to make target platform, recommended phases, auth/RBAC, and owner expectations explicit for static evaluation.
- **Alternatives considered:** Rely only on `.squad\lint-prompts.mjs`; run live LLM evaluations; keep the prompts implicit and teach the harness to infer missing intent.
- **Trade-offs:** Static checks are cheaper and deterministic, but they validate prompt structure and coverage rather than true generation quality. The prompt wording becomes slightly more explicit, but evaluation criteria and operator expectations are now easier to audit.


