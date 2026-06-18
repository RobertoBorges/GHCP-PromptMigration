# Decisions Archive — Ocean's Twelve — The Azure Heist

> Old decisions (2026-05-28 through 2026-05-29) preserved append-only. Managed by Scribe. For active decisions, see `.squad/decisions.md`.

---

### D-001: Squad bootstrapped from the fast preset
- **By:** snap-squad
- **Date:** 2026-05-28
- **Context:** Project initialized using snap-squad warm-start before the Azure migration specialization was fully defined.
- **Decision:** Start from the `fast` preset as scaffolding, then evolve the repo into Ocean's Twelve — The Azure Heist once the twelve-agent Azure migration model is established.

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

### D-004: Team workflow docs treat specialist roles as functional overlays
- **By:** Tester/DevRel
- **Date:** 2026-05-28
- **Context:** The repo already has Architect, Coder, and Tester, but Robert's migration team also needs guidance for Cloud Engineer, DevOps, Security, and QA responsibilities.
- **Decision:** Document those roles as workflow responsibilities with mapped squad-agent equivalents and explicit fallbacks when Azure Specialist or Security Auditor agents are not yet present in `.squad/team.md`.
- **Trade-off:** The guidance is immediately usable without restructuring the squad, but teams must understand that some specialist names are conceptual role mappings rather than preconfigured squad members.

### D-005: Skills live in a single root-level catalog
- **By:** Coder
- **Date:** 2026-05-28
- **Context:** The migration prompts need reusable building blocks that can be referenced consistently from `.github/prompts/*.prompt.md` without duplicating migration guidance.
- **Decision:** Adopt a single root-level `skills/` catalog for reusable migration guidance, with prompts in `.github/prompts/` referencing skills via `#file:skills/<skill>.md`; prioritize 8 fully authored cross-phase skills and keep the remaining 18 as structured outlines to maximize reuse while controlling authoring cost.
- **Alternatives considered:** Keep all guidance embedded in each phase prompt; place skills under `.github/skills`; fully author all 26 skills before wiring prompt references.
- **Trade-offs:** Root-level `skills/` keeps references predictable and prompt files thin, but requires catalog discipline and ongoing curation to prevent overlap.

### D-007: Training docs standardize on current commands and the implemented BookShop reference
- **By:** Tester/DevRel
- **Date:** 2026-05-28

### D-008: Azure training defaults follow use-case-specific hosting and data baselines
- **By:** Azure Specialist
- **Date:** 2026-05-28
- **Context:** The new training program needed one opinionated Azure path per use-case so architects do not mix legacy implementation details with the intended modernization targets.
- **Decision:** Standardize training on App Service for classic/.NET web monoliths, Container Apps for containerized API-first modernizations, AKS only when Kubernetes control is justified, Azure SQL for the relational .NET tracks, PostgreSQL-first for the Java API unless Cosmos DB is explicitly justified, and Bicep + AVM + azd as the default IaC/deployment path. **Exception:** BookShop remains the practical reference implementation for App Service + Azure SQL because the checked-in artifacts are the benchmark the team can study today.
- **Trade-off:** The training stays opinionated without ignoring the implemented BookShop benchmark, but the guide must now distinguish between default modernization targets and the repo's current reference architecture when those differ.

### D-009: Technology-specific assessment prompts mirror the Phase1 structure
- **By:** Coder
- **Date:** 2026-05-28
- **Context:** Roberto Borges' team needed production-ready prompts for version-specific .NET and Java upgrades, WCF/WebForms/Classic ASP triage, team readiness evaluation, and ultra-fast intake beyond the generic Phase 1 assessment.
- **Decision:** Add focused assessment prompts under `.github/prompts/` that keep the standard YAML frontmatter, numbered workflow steps, rules, deliverables, and output checklists while tailoring report outputs and guidance to each legacy technology and use-case.
- **Alternatives considered:** Expand `Phase1-PlanAndAssess.prompt.md` with more conditionals; keep only a single quick assessment prompt.
- **Trade-offs:** More prompt files increase catalog size, but they reduce ambiguity for migration teams, improve reuse across the seven use-cases, and make targeted assessments easier to dispatch and review.

### D-010: Training program becomes the canonical use-case map
- **By:** Architect
- **Date:** 2026-05-28
- **Context:** The repo already had prompts, skills, onboarding docs, and a BookShop benchmark, but it lacked one canonical document that joins use-cases, squad roles, skill files, prompt order, learning paths, and readiness checks.
- **Decision:** Use `docs/training-program.md` as the primary enablement document for the 7 use-cases. Keep it grounded in the current slash commands, exact `skills/` files, and the BookShop reference implementation, while explicitly calling out gaps such as the missing PostgreSQL-specific skill file.
- **Trade-off:** A single source of truth reduces onboarding confusion and prompt drift, but it must be curated whenever prompts, skills, or benchmark architectures change.

### D-011: Orchestrated skills and hooks move under `.github/`
- **By:** Coder
- **Date:** 2026-05-28
- **Context:** The new orchestration layer must connect chatmodes, prompts, skills, and squad-agent handoffs using GitHub prompt-local file references and reusable hook rules.
- **Decision:** Add the production skill library under `.github/skills/` and orchestration rules under `.github/hooks/`, then wire all 13 prompt entrypoints to those references via `#file:.github/...` so prompt composition and dispatch guidance live next to the prompt assets they govern.
- **Alternatives considered:** Continue expanding the legacy root-level `skills/` catalog; keep orchestration embedded inside each prompt; document routing only in README/docs.
- **Trade-offs:** Duplicates some legacy guidance temporarily, but makes prompt-local composition clearer, reduces hidden coupling, and creates an explicit home for phase gates and agent dispatch rules.

### D-013: Presentation deck is generated as editable native PowerPoint shapes
- **By:** Coder
- **Date:** 2026-05-28
- **Context:** Roberto Borges needed a persuasive stakeholder deck comparing Ocean's Twelve squad orchestration against monolithic prompting, using the LATAM template and GCS theme.
- **Decision:** Build the deck as a Python-driven `python-pptx` presentation that reuses the LATAM template, copies the established helper-function pattern, and renders diagrams as native PowerPoint shapes so the output stays brand-aligned and editable.
- **Alternatives considered:** Depend on Mermaid image rendering for all diagrams; hand-author the presentation manually.
- **Trade-offs:** Native shapes require more layout code, but they keep the slides deterministic, editable by presenters, and visually consistent with the existing LATAM deck generators.

### D-014: README becomes the architect-facing control-tower narrative
- **By:** Tester/DevRel
- **Date:** 2026-05-28
- **Context:** The repository had strong prompts, skills, routing, and training assets, but the root README still read like a generic prompt library overview instead of a persuasive explanation of why Ocean's Twelve orchestration matters.
- **Decision:** Rewrite `README.md` as the canonical architect-and-developer entrypoint with visual-first Mermaid diagrams, an explicit squad-vs-monolith comparison, role-based navigation, examples, and a clear split between chatmodes, prompts, skills, hooks, and targets.
- **Alternatives considered:** Keep the short README and push readers into `docs/ARCHITECTURE.md`; add a lighter README with fewer diagrams.
- **Trade-offs:** The README is longer, but it now carries the full system story in one place and lowers onboarding cost for architects, developers, and stakeholders.

### D-016: Squad identity and migration charters are canonicalized
- **By:** Evaluator
- **Date:** 2026-05-28
- **Context:** Core squad docs still referenced the Fast Squad identity, the original three charters still described a TypeScript/Vitest/ESM app workflow, and prompt metadata was inconsistent across the migration prompt catalog.
- **Decision:** Standardize the repo on the Ocean's Twelve — The Azure Heist identity, rewrite the Architect/Coder/Tester charters for Azure migration work (.NET, Java, prompt authoring, IaC, validation, walkthroughs), normalize prompt frontmatter, and clarify that Phase 5 hands off to Phase 6 rather than declaring the migration complete.
- **Alternatives considered:** Patch only the most visible identity strings; leave the original fast-preset language and JavaScript-centric charter details in place.
- **Trade-offs:** The docs are denser and require coordinated updates across several files, but routing, prompt behavior, and squad expectations now match the actual Azure migration repository.

### D-017: README navigation favors grouped discovery over one flat index
- **By:** Tester/DevRel
- **Date:** 2026-05-28
- **Context:** `README.md` had grown into a long control-tower document with strong content, but the flat table of contents and always-expanded reference blocks made it harder to scan by audience intent.
- **Decision:** Keep the section content intact, but reorganize navigation into grouped overview/getting-started/migration/reference/documentation/decision-maker/community buckets, add a short navigation guide, and collapse the longest prompt catalogs so readers can progressively disclose detail.
- **Alternatives considered:** Reorder the entire README body; trim or rewrite repeated content across sections.
- **Trade-offs:** Grouped navigation improves discoverability without rewriting the document, but some repeated content remains in place because preserving section text was prioritized for this pass.

### D-018: Skill hierarchy is documented and overlapping skills resolve to `.github/skills/`
- **By:** Architect
- **Date:** 2026-05-28
- **Context:** The repo now contains both a legacy root `skills/` catalog and a prompt-local `.github/skills/` catalog, with 10 duplicated filenames referenced by different prompts and chatmodes. Without an explicit rule, contributors cannot tell which copy is authoritative.
- **Decision:** Keep both layers for now, but treat `.github/skills/` as the canonical copy for every overlapping skill because those variants are more complete and power the orchestrated workflow prompts. Add `skills/INDEX.md`, `docs/PROJECT-MAP.md`, and `docs/PROMPT-CATALOG.md` as the discovery and governance layer that explains references, overlap, and project structure.
- **Alternatives considered:** Delete the root duplicates immediately; move all prompt-local skills back into the root catalog; keep both catalogs without documentation.
- **Trade-offs:** Temporary duplication remains so existing chatmodes and legacy prompts do not break, but the repo now has an explicit authority model and a reliable navigation layer for future consolidation.

### D-019: Walkthrough guidance is CLI-first and one-surface
- **By:** Tester/DevRel + Scribe
- **Date:** 2026-05-29
- **Context:** The initial walkthrough index mixed Copilot CLI guidance with chat-panel switching, even though the migration experience is now centered on natural-language squad orchestration from a single entry surface.
- **Decision:** Rewrite `docs/walkthroughs/README.md` as a CLI-first index that teaches `@squad` + natural language as the primary entrypoint, shows the shared squad fan-out pattern once, and presents all seven use cases through one consistent quick-start table with one-shot prompts.
- **Alternatives considered:** Keep mixed CLI/chat-panel instructions in the index; document each use case independently without a shared squad pattern.
- **Trade-offs:** The index is simpler and more repeatable for operators, but it is intentionally less focused on chatmode-specific steering at the top level because the walkthrough set now optimizes for one-surface onboarding first.

### D-020 through D-022: Walkthroughs 01-07 standardize on pure CLI `@squad` flows
- **By:** Tester/DevRel + Scribe
- **Date:** 2026-05-29
- **Decision:** Rewrite all seven legacy modernization walkthroughs as pure CLI walkthroughs driven by natural-language `@squad` prompts, with Mermaid phase diagrams, explicit fan-out prompts, and legacy shortcuts confined to appendix notes.

### D-023: BookShop prompt docs are archived examples, not migration starters
- **By:** Scribe
- **Date:** 2026-05-29
- **Decision:** Treat the BookShop prompt docs as archived completed-migration examples, add archive banners, and point new migration work to the interactive squad interview.

### D-024: Generic interactive interview is the default migration entrypoint
- **By:** Architect
- **Date:** 2026-05-29
- **Decision:** Add `.github/prompts/InteractiveMigrationInterview.prompt.md` as the canonical intake prompt for fresh migrations.

### D-025 through D-028: PPTX deck generation and LATAM template decisions
- **By:** Coder
- **Date:** 2026-05-29
- **Decision:** Standardized PPTX generation on LATAM template pattern, shared helper module, inset accents, and four-act Factory narrative structure.

### D-029: Security hardening prompt composes focused Azure security skills
- **By:** Security Auditor + Coder
- **Date:** 2026-05-29
- **Decision:** Add dedicated security skills for Key Vault, network security, Defender/compliance, and OWASP Top 10 review.

### D-030: Prompt handoffs standardize on CLI-first `@squad` commands
- **By:** Coder
- **Date:** 2026-05-29
- **Decision:** Replace slash-command references with CLI-first `@squad` commands in completion guidance while preserving slash trigger names in When to Use sections.

### D-031: Agent #13 — Tess Ocean (Presentation Specialist) added to squad
- **By:** Architect
- **Date:** 2026-05-29
- **Decision:** Added Agent #13 "Tess Ocean" as Presentation Specialist with auto-dispatch on deck/PPTX requests.

### D-032 through D-033: PPTX authoring guidance and shared module consolidation
- **By:** Coder
- **Date:** 2026-05-29
- **Decision:** Add `.github/skills/pptx-generation.md` as canonical deck skill and refactor all generators to shared `latam_gcs_template.py`.

### D-034: README reflects the 13-agent, 19-skill CLI-first operating model
- **By:** Tester/DevRel
- **Date:** 2026-05-29
- **Decision:** Updated README to canonical squad inventory (13 agents, 19 prompt-local skills, 21 prompts).

### D-035: Hook routing treats all 13 agents as first-class participants
- **By:** Coder
- **Date:** 2026-05-29
- **Decision:** Updated three hook documents so all 13 agents are named at least once.

### D-036: Docs root routes readers through purpose-based subfolders
- **By:** Tester/DevRel
- **Date:** 2026-05-29
- **Decision:** Reorganized flat docs root into `docs/architecture/`, `docs/guides/`, and `docs/onboarding/`.

### D-037: Prompt skill references standardize on `.github/skills/`
- **By:** Coder
- **Date:** 2026-05-29
- **Decision:** Standardized prompt-facing `#file:` references on `.github/skills/`.

### D-038: All 13 agent charters share a required baseline structure
- **By:** Architect + Scribe
- **Date:** 2026-05-29
- **Decision:** Standardized every charter around the same baseline skeleton.

### D-039: Chatmodes standardize on roster-aligned metadata and CLI-first follow-through
- **By:** Coder + Scribe
- **Date:** 2026-05-29
- **Decision:** Standardized all seven chatmodes on a shared canonical shape.
