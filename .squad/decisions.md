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

> **Note:** Decisions D-001 through D-039 have been archived to `.squad/decisions-archive.md`. See that file for the full historical record.
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


