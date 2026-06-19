# Project Map

Verified against the filesystem on 2026-05-29. Counts below reflect the current repo state after reorganizing the docs tree into `docs/architecture/`, `docs/guides/`, and `docs/onboarding/`.

## Repository Snapshot

- Root files: **7**
- Root directories: **5**
- `.github/prompts/`: **21** prompt entrypoints
- `.github/chatmodes/`: **7** chatmodes
- `.github/skills/`: **23** prompt-local skills
- `skills/`: **28** files total (**26** legacy skills + `README.md` + `INDEX.md`)
- `.squad/agents/`: **13** agent charters
- `docs/`: **0** root files + **7** subdirectories
- `Use-cases/`: **7** migration target applications

## Hierarchy

```text
GHCP-PromptMigration/
├── .git/                              # Git metadata
├── .github/                           # GitHub Copilot config and orchestration assets
│   ├── chatmodes/ (7)
│   │   ├── Azure-Infrastructure.chatmode.md
│   │   ├── Code-Migration-Modernization.chatmode.md
│   │   ├── Cost-Optimization.chatmode.md
│   │   ├── Debug-Migration.chatmode.md
│   │   ├── Migration-Orchestrator.chatmode.md
│   │   ├── Quick-Assessment.chatmode.md
│   │   ├── Security-Review.chatmode.md
│   ├── hooks/ (3)
│   │   ├── agent-dispatch.md
│   │   ├── phase-gates.md
│   │   ├── use-case-routing.md
│   ├── modernize/ (1)
│   │   └── java-upgrade/
│   │       ├── .gitignore
│   │       └── hooks/
│   │           └── scripts/
│   │               ├── recordToolUse.ps1
│   │               └── recordToolUse.sh
│   ├── prompts/ (21)
│   │   ├── Assess-ClassicASP-Migration.prompt.md
│   │   ├── Assess-DotNet-Upgrade.prompt.md
│   │   ├── Assess-Java-Upgrade.prompt.md
│   │   ├── Assess-WCF-Migration.prompt.md
│   │   ├── Assess-WebForms-Migration.prompt.md
│   │   ├── CostOptimization.prompt.md
│   │   ├── DatabaseMigration.prompt.md
│   │   ├── GetStatus.prompt.md
│   │   ├── InteractiveMigrationInterview.prompt.md
│   │   ├── Phase-Rollback.prompt.md
│   │   ├── Phase0-Multi-repo-assessment.prompt.md
│   │   ├── Phase1-PlanAndAssess.prompt.md
│   │   ├── Phase2-MigrateCode.prompt.md
│   │   ├── Phase3-GenerateInfra.prompt.md
│   │   ├── Phase4-DeployToAzure.prompt.md
│   │   ├── Phase5-SetupCICD.prompt.md
│   │   ├── Phase6-PostMigrationOps.prompt.md
│   │   ├── QuickAssessment.prompt.md
│   │   ├── QuickTriage.prompt.md
│   │   ├── SecurityHardening.prompt.md
│   │   ├── TeamSkillAssessment.prompt.md
│   ├── skills/ (23)
│   │   ├── asp-classic-to-dotnet.md
│   │   ├── azure-app-service.md
│   │   ├── azure-container-apps.md
│   │   ├── azure-defender-compliance.md
│   │   ├── azure-entra-id.md
│   │   ├── azure-keyvault-secrets.md
│   │   ├── azure-network-security.md
│   │   ├── bicep-modules.md
│   │   ├── config-transformation.md
│   │   ├── docker-containerize.md
│   │   ├── dotnet-framework-to-dotnet8.md
│   │   ├── ef-migration.md
│   │   ├── java8-to-java21.md
│   │   ├── managed-identity.md
│   │   ├── migration-handoff.md
│   │   ├── migration-report-template.md
│   │   ├── owasp-top10-review.md
│   │   ├── pptx-generation.md
│   │   ├── rbac-least-privilege.md
│   │   ├── rollback-strategy.md
│   │   ├── secret-management.md
│   │   ├── wcf-to-rest-api.md
│   │   ├── webforms-to-razor.md
│   └── copilot-instructions.md
├── .squad/                            # Squad config, routing, evals, and agent charters
│   ├── SCORECARD.md
│   ├── decisions.md
│   ├── eval.mjs
│   ├── mcp-config.md
│   ├── routing.md
│   ├── team.md
│   └── agents/ (13)
│       ├── architect/charter.md
│       ├── azure-specialist/charter.md
│       ├── coder/charter.md
│       ├── cutover-commander/charter.md
│       ├── database-specialist/charter.md
│       ├── devops-engineer/charter.md
│       ├── evaluator/charter.md
│       ├── observability-engineer/charter.md
│       ├── performance-engineer/charter.md
│       ├── presentation-specialist/charter.md
│       ├── scribe/charter.md
│       ├── security-auditor/charter.md
│       └── tester/charter.md
├── AGENTS.md
├── CLAUDE.md
├── JOURNAL.md
├── LICENSE
├── PORTFOLIO.md
├── README.md
├── skills/                            # Legacy reusable skills + canonical index
│   ├── INDEX.md
│   ├── README.md
│   ├── asp-classic-to-dotnet.md
│   ├── azd-configuration.md
│   ├── azure-aks.md
│   ├── azure-app-service.md
│   ├── azure-container-apps.md
│   ├── azure-devops-pipelines.md
│   ├── azure-entra-id.md
│   ├── azure-key-vault.md
│   ├── azure-monitor-appinsights.md
│   ├── azure-sql-migration.md
│   ├── bicep-modules.md
│   ├── config-transformation.md
│   ├── cost-optimization.md
│   ├── docker-containerize.md
│   ├── dotnet-framework-to-dotnet8.md
│   ├── ef-migration.md
│   ├── github-actions-cicd.md
│   ├── java8-to-java21.md
│   ├── managed-identity.md
│   ├── migration-report-template.md
│   ├── rbac-least-privilege.md
│   ├── rollback-strategy.md
│   ├── secret-management.md
│   ├── terraform-azure.md
│   ├── wcf-to-rest-api.md
│   ├── webforms-to-razor.md
├── docs/                              # Structured architecture, guide, onboarding, and operator docs
│   ├── architecture/ (3)
│   │   ├── ARCHITECTURE.md
│   │   ├── PROJECT-MAP.md
│   │   └── PROMPT-CATALOG.md
│   ├── guides/ (4)
│   │   ├── dotnet-version-guide.md
│   │   ├── handoff-protocol.md
│   │   ├── skills-map.md
│   │   └── squad-dispatch-cheatsheet.md
│   ├── onboarding/ (5)
│   │   ├── onboarding.md
│   │   ├── team-guide.md
│   │   ├── team-onboarding-prompts.md
│   │   ├── training-exercises.md
│   │   └── training-program.md
│   ├── pptx/                          # PPTX deck library
│   │   ├── README.md
│   │   ├── generators/                # Python scripts that build decks
│   │   │   ├── latam_gcs_template.py
│   │   │   ├── generate_oceans_twelve_deck.py
│   │   │   ├── generate_borges_brady_deck.py
│   │   │   └── (6 more LATAM generators)
│   │   └── decks/                     # Generated .pptx output files
│   │       ├── Oceans_Twelve_Squad_vs_Prompting.pptx
│   │       ├── Borges_Brady_Squad_Power.pptx
│   │       └── (6 more LATAM decks)
│   ├── squad-interactive/
│   ├── walkthroughs/ (8)
│   │   ├── 01-classic-asp-walkthrough.md
│   │   ├── 02-dotnet30-webforms-walkthrough.md
│   │   ├── 03-wcf-to-rest-walkthrough.md
│   │   ├── 04-contoso-university-walkthrough.md
│   │   ├── 05-bookshop-reference-walkthrough.md
│   │   ├── 06-java-api-walkthrough.md
│   │   ├── 07-parts-unlimited-walkthrough.md
│   │   └── README.md
│   └── use-case-cheatsheets/ (7)
│       ├── 01-asp-classic.md
│       ├── 02-dotnet30-webforms.md
│       ├── 03-wcf-net35.md
│       ├── 04-contoso-university.md
│       ├── 05-bookshop-reference.md
│       ├── 06-java-api.md
│       └── 07-parts-unlimited.md
└── Use-cases/ (7)
    ├── 01-ASPClassicApp/  # 14 files, 3 subdirectories
    ├── 02-NetFramework30-ASPNET-WEB/  # 22 files, 2 subdirectories
    ├── 03-WCFNet35/  # 47 files, 24 subdirectories
    ├── 04-ContosoUniversityDiPS/  # 393 files, 126 subdirectories
    ├── 05-BookShop/  # 931 files, 265 subdirectories
    ├── 06-Java-API-BusReservation/  # 23 files, 16 subdirectories
    └── 07-PartsUnlimited-aspnet45/  # 363 files, 58 subdirectories
```

## Directory Purpose and Counts

| Directory | Verified count | Purpose |
|---|---:|---|
| `.github/` | 1 files, 5 dirs | Copilot-facing configuration root: chatmodes, prompts, hooks, prompt-local skills, and modernization hook scaffolding. |
| `.github/chatmodes/` | 7 files, 0 dirs | Seven conversation surfaces that route users into phase-focused or specialist experiences. |
| `.github/prompts/` | 21 files, 0 dirs | Twenty-one prompt entrypoints covering the main workflow, assessments, specialists, utilities, and the interactive interview. |
| `.github/skills/` | 23 files, 0 dirs | Prompt-local skill files used by the current orchestrated workflow prompts. |
| `.github/hooks/` | 3 files, 0 dirs | Reusable orchestration rules for phase gates, agent dispatch, and use-case-specific routing. |
| `.github/modernize/` | 0 files, 1 dirs | Experimental modernization scaffold; currently only a Java upgrade hook package. |
| `.squad/` | 6 files, 1 dirs | Ocean's Twelve control plane: team roster, routing, decisions, scorecard, MCP config, and eval script. |
| `.squad/agents/` | 0 files, 13 dirs | Thirteen agent charter folders, one charter per squad specialist. |
| `skills/` | 28 files, 0 dirs | Legacy reusable skill catalog plus `README.md` and the canonical `INDEX.md`. |
| `docs/` | 0 files, 7 dirs | Structured documentation root for architecture, guides, onboarding, presentations, walkthroughs, and examples. |
| `docs/architecture/` | 3 files, 0 dirs | Architecture references, repo map, and prompt catalog. |
| `docs/guides/` | 4 files, 0 dirs | Operational guides for versions, handoffs, routing, and skills coverage. |
| `docs/onboarding/` | 5 files, 0 dirs | Team onboarding, training, and starter prompt materials. |
| `docs/walkthroughs/` | 8 files, 0 dirs | CLI walkthrough set: one index plus seven use-case-specific walkthroughs. |
| `docs/use-case-cheatsheets/` | 7 files, 0 dirs | Seven quick-reference sheets aligned to the seven sample migration targets. |
| `Use-cases/` | 0 files, 7 dirs | Sample applications used as migration targets and training scenarios. |

## Use-Case Directories

| Use-case | Totals | Purpose / shape |
|---|---:|---|
| `01-ASPClassicApp` | 14 files, 3 dirs | Classic ASP sample (`.asp`, `global.asa`, includes, simple DB folder) used for rewrite-first assessment patterns. |
| `02-NetFramework30-ASPNET-WEB` | 22 files, 2 dirs | Small ASP.NET Web Forms sample (`.aspx`, `Web.config`, `.sln/.csproj`) for early .NET modernization. |
| `03-WCFNet35` | 47 files, 24 dirs | WCF sample with client, host, and service projects for service-contract modernization to REST/gRPC. |
| `04-ContosoUniversityDiPS` | 393 files, 126 dirs | Larger multi-project ASP.NET sample with tests and SPA/API components; used for full-stack modernization drills. |
| `05-BookShop` | 931 files, 265 dirs | Large reference implementation with solution, tests, docs, Docker assets, and deployment guides; the repo's benchmark modernization app. |
| `06-Java-API-BusReservation` | 23 files, 16 dirs | Java/Maven API sample (`pom.xml`, `mvnw`, `src/`) for Java 8 -> 21 and Azure API migration flows. |
| `07-PartsUnlimited-aspnet45` | 363 files, 58 dirs | Large ASP.NET 4.5 sample with docs, env, src, and test folders for enterprise-style modernization scenarios. |

## Notes

- The repo now has **two explicit skill layers**: root `skills/` for reusable catalog content and `.github/skills/` for prompt-local orchestration content.
- `.github/modernize/` is easy to miss because it is not part of the main prompt tree, but it is present on disk and included here.
- `docs/pptx/` contains PPTX generators, the shared LATAM palette module, and generated slide decks.
