---
name: Phase1-Plan
description: Generate the migration plan, Application-Assessment-Report, and Decisions-Required file for one application
argument-hint: "Specify the folder path to your legacy application, e.g., 'Plan the app in Use-cases/02-NetFramework30-ASPNET-WEB'"
agent: Code Migration Modernization Agent
model: Claude Sonnet 4.7 (copilot)
---

<!-- BEGIN: capability-matrix-gate (auto-managed by inject-capability-matrix-gates.mjs) -->

## 🚦 MANDATORY OPENING CHECK — Capability Matrix Required

**Before doing ANY work for Phase 1 — Plan, verify the Discovery contract:**

| Required artifact | Location | If missing |
|-------------------|----------|------------|
| Discovery Dossier | `reports/Discovery-Dossier.md` | **STOP** — run `/assess-any-application` first |
| Capability Matrix | `reports/Capability-Matrix.yaml` | **STOP** — run `/assess-any-application` first |

> **Note:** `reports/Migration-Plan.md` is **produced by Phase 1**. If it doesn't exist yet, Phase 1 will generate it. If you'd like to produce it separately first, use the `/build-migration-plan` add-on.

### If EITHER of those two artifacts is missing

Reply with exactly:

```
🚨 Phase 1 — Plan cannot proceed without the Discovery contract.

Missing artifacts:
  - reports/Discovery-Dossier.md          [missing/present]
  - reports/Capability-Matrix.yaml         [missing/present]

Required steps before re-running this phase:
  1. Open Copilot Chat → /assess-any-application  (or in CLI: "assess this application")
  2. Then re-run: /Phase1-Plan

To override (skip Discovery and accept risk), log a waiver entry in
reports/Decision-Log.md with `Waiver: skip-discovery=<reason>` and re-invoke
this prompt with the `--accept-risk` natural-language flag in your request.
```

**Do NOT proceed past this gate unless:**
- Both artifacts exist, OR
- A waiver entry exists in `reports/Decision-Log.md` AND the user explicitly said "skip discovery" or similar

### When the gate passes

1. Read `reports/Capability-Matrix.yaml` and extract these fields you must honor:
   - `source.primary_adapter` → load the matching `source-*` skill
   - `stack.primary_stack` + `stack.secondary_stacks` → load matching `stack-*` skills
   - `workload.primary_pattern` → load matching `workload-*` skill
   - `migration_strategy.recommendation` → adjust phase emphasis based on the recommended strategy
   - `risk_flags` → load the matching risk skills (e.g., `risk-cross-region-data.md`)
   - `unresolved_questions` → if any remain unanswered, surface them BEFORE starting work
2. If `reports/Migration-Plan.md` exists, read it for approved sequencing. Otherwise Phase 1 will produce it as part of its work.
3. Confirm Phase prerequisites are met.

<!-- END: capability-matrix-gate -->
# Plan a Single Application Migration to Azure

## Migration Scope

This guided migration helps you:
- ✅ **Make your application Azure-compatible** — replace on-prem-only dependencies (identity providers, file shares, in-process caches, machine keys, local certificate stores, etc.) with their Azure equivalents
- ✅ **Upgrade the runtime** to a version supported by your chosen Azure hosting platform (only when the current version is out-of-support or incompatible)
- ✅ **Generate infrastructure as code** for your target Azure platform
- ✅ **Set up CI/CD** for automated deployment

This migration does **NOT** include:
- ❌ **Data Migration tooling** — Use Azure Database Migration Service (DMS), Data Migration Assistant, or Azure Database Migration Service Extension. This prompt orchestrates but doesn't replace them.
- ❌ **Binary/Dependency Scanning** — Use stack-appropriate external tools (`.NET Upgrade Assistant`, `Spring Boot Migrator`, `Python 2to3`, `Node.js n`, etc.)
- ❌ **Wholesale rewrite to microservices / event-driven / cloud-native patterns** — that's an explicit `rearchitect` or `rebuild` migration strategy. The default is `replatform` or `refactor` — **minimum viable Azure compatibility**, not a re-architecture. Only run architecture rewrites when the user explicitly picks that strategy in Discovery.

**Goal:** Take an existing application — regardless of language, framework, or where it runs today — and make **only the changes required** to host it on your selected Azure platform (App Service, Container Apps, AKS, Functions, VMs, etc.). The specific changes are dictated by `reports/Capability-Matrix.yaml` (source, stack, workload, integrations, data).

---

## Agent Role
You are a migration specialist agent that guides users through application modernization to Azure. You will collect requirements, analyze the codebase, and produce comprehensive assessment reports with actionable migration plans.

## Step A: Gather Requirements

### Step 1: Collect User Preferences (REQUIRED)
Before proceeding with any analysis, gather the following information from the user:

#### 1.0 Check for Portfolio Handoff (PRIORITY)

**BEFORE asking any questions, check for `reports/portfolio-handoff.json`** — this file is written by the Portfolio Planning flow (`/PortfolioStrategy`) when the user has already classified this app at the portfolio level.

**If the file exists:**
1. Read it (JSON parse)
2. Confirm with the user the inherited app and its pre-classified setup:
   > 📥 **Inherited from portfolio plan** (`<source_deck>` → `<app.name>`):
   > - Modernization scope: based on **<app.six_r_strategy>** (e.g., Replatform = code remediation + version upgrade)
   > - Target platform: **<app.target_platform>**
   > - IaC tool: **<app.iac_preference>**
   > - Target database: **<app.database_strategy>**
   > - Stack: **<app.current_stack> → <app.target_stack>**
   > - Ownership: **<app.factory_or_partner>**
   > - Criticality: **<app.criticality>**
   > - Notes: <app.notes>
   >
   > **Use this configuration as-is, or override any field?**

3. If user confirms: SKIP section 1.1 (still generate `reports/Decisions-Required.md` with the handoff values pre-filled as `✅ DECIDED`) and proceed to Step B
4. If user wants to override specific fields: ask only about those, keep the rest from the handoff, then write `Decisions-Required.md` accordingly
5. If user wants to start fresh: fall through to section 1.1 normally

**If `reports/portfolio-handoff.json` does NOT exist:** proceed directly to section 1.1 below.

If a Migration Strategy Report HTML deck (`*_Migration_Strategy_Report.html`) exists but no handoff JSON exists yet, the user may not have completed the app-selection step. Offer to run `/PortfolioStrategy` to generate the handoff file, OR proceed with manual setup.

#### 1.1 Generate the Decisions-Required artifact (REPLACES old ad-hoc questions)

> **Wave H change:** Phase 1 no longer asks individual scope questions inline. Instead, it produces the canonical `reports/Decisions-Required.md` file from the catalog, then later phases hard-stop on each PENDING decision.
>
> See: [`.github/skills/decision-hardstop.md`](../skills/decision-hardstop.md), [`.github/skills/decision-catalog.md`](../skills/decision-catalog.md), [`.github/skills/decisions-required-template.md`](../skills/decisions-required-template.md)

**Action: Generate `reports/Decisions-Required.md`**

1. Read `.github/skills/decision-catalog.md` — the canonical list of 18 major decisions:
   - D-01 Target framework / runtime version
   - D-02 UI architecture
   - D-03 Backend / API style
   - D-04 Database engine
   - D-05 Database migration tool
   - D-06 Hosting platform
   - D-07 IaC tool
   - D-08 Region & data residency
   - D-09 Authentication
   - D-10 Multi-tenancy approach
   - D-11 Compliance scope
   - D-12 Cost ceiling
   - D-13 DR — RPO/RTO targets
   - D-14 Cutover strategy
   - D-15 Acceptable downtime
   - D-16 CI/CD platform
   - D-17 Observability stack
   - D-18 Container registry
2. Read `.github/skills/decisions-required-template.md` — the file structure.
3. For each catalog entry:
   - Copy the section into `reports/Decisions-Required.md` with **Status: ⏸ PENDING**.
   - Use the catalog's recommendation logic to pre-fill the "Default guess" subsection, citing only visible evidence from the Capability Matrix.
   - Always label the guess as a guess (`⚠ Default guess`) — never as "recommended" or "best choice."
   - **Stay-as-is must be option 1** in every options table.
4. Write the file with a status summary table at the top (one row per decision).
5. Apply the catalog's `condition` field — if a decision is genuinely N/A for this app (e.g., no UI for a batch-only workload), mark it `🚫 N/A — <reason>` instead of leaving PENDING.

**Action: Tell the user what's next**

After writing the file, post this message:

```
✅ I've generated reports/Decisions-Required.md with <N> major decisions
   needing your input.

   These decisions are NOT optional — Phases 2-4 will not run until each
   is marked ✅ DECIDED (or 🚫 N/A) in that file.

   Two ways to answer them:

   1. Reply to me one at a time in chat, OR
   2. Open reports/Decisions-Required.md, tick the option box and fill
      in your rationale for each section, then say "I've answered the
      decisions" and I'll re-read.

   Want to start with #1? Tell me which decision to start with, or say
   "go in order" and I'll walk you through them.
```

**Then wait.** Do not proceed past this step until the user has either:
- Answered all decisions (or marked N/A), confirmed by re-reading the file, OR
- Explicitly chose to defer some decisions ("I'll fill in the file later"). In that case, Phase 1 finishes assessment but warns: "Phases 2-4 will hard-stop on PENDING decisions until you fill them in."

**Do NOT silently default any decision.** Even when a "Default guess" is shown, it stays PENDING until the user actively confirms it.

## Step B: Analyze Application

### Step 3: Environment Setup
1. **Create reports folder** if it doesn't exist: `reports/`
2. **Build the solution** to verify all dependencies resolve. Pick the command for the stack in `Capability-Matrix.stack.primary_stack`:

   | Stack | Build command |
   |-------|---------------|
   | `dotnet` (Framework or Core) | `dotnet build` (or `msbuild` for legacy SDK-style projects) |
   | `java` | `mvn compile` (or `gradle build`) |
   | `nodejs` | `npm install && npm run build` (script may be missing — that's a signal) |
   | `python` | `pip install -r requirements.txt` (or `poetry install` / `uv pip install`) |
   | `php` | `composer install` |
   | `ruby` | `bundle install` |
   | `go` | `go build ./...` |
   | `perl` | `cpanm --installdeps .` |
   | `rust` | `cargo build` |
   | `scala` / `kotlin` | `sbt compile` or `gradle build` |
   | `cobol-mainframe` | Vendor-specific (Micro Focus / Astadia / OpenCOBOL) |
   | `oracle-forms` / `powerbuilder` / `delphi-vb6` / `cpp-windows` | Vendor IDE — typically no headless build. Document the manual build step. |
   | Other / unknown | Skip; ask the user for the build command they use today. |
3. **Document any build failures** — these indicate migration blockers.

### Step 4: Automated Discovery
Use the following tools to analyze the codebase:

#### 4.1 Project Detection
```
Use `file_search` for stack-appropriate manifests:
  .NET:      *.csproj, *.sln, *.fsproj, *.vbproj, web.config, app.config
  Java:      pom.xml, build.gradle, build.gradle.kts, web.xml
  Node.js:   package.json, package-lock.json, tsconfig.json
  Python:    requirements.txt, pyproject.toml, setup.py, Pipfile, poetry.lock
  PHP:       composer.json, composer.lock
  Ruby:      Gemfile, Gemfile.lock, *.gemspec
  Go:        go.mod, go.sum
  Perl:      cpanfile, Makefile.PL, dist.ini
  Rust:      Cargo.toml, Cargo.lock
  Scala/Kotlin: build.sbt, build.gradle.kts
  COBOL:     *.cbl, *.cob, *.cpy (with mainframe compile decks)
Use `grep_search` to identify framework versions in the detected manifests.
```

#### 4.2 Application Type Analysis

**Load only the sections that match `Capability-Matrix.stack.primary_stack`** (and `.stack.secondary_stacks`). Skip the rest.

**For `dotnet`:**
| Discovery Target | Tool & Pattern |
|-----------------|----------------|
| Framework version | `grep_search`: `<TargetFramework`, `<TargetFrameworkVersion` |
| WCF Services | `semantic_search`: "ServiceContract", "OperationContract", ".svc" |
| WebForms | `file_search`: `*.aspx`, `*.ascx`, `*.master` |
| MVC/Razor | `file_search`: `*.cshtml`, Controllers/, Views/ |
| Authentication | `grep_search`: "Windows Authentication", "Forms Authentication", "Identity" |
| Database access | `semantic_search`: "SqlConnection", "DbContext", "EntityFramework" |
| Config files | `grep_search` in `web.config`, `app.config`, `appsettings.json` |

**For `java`:**
| Discovery Target | Tool & Pattern |
|-----------------|----------------|
| Java/Spring version | `grep_search`: `<java.version>`, `sourceCompatibility`, `spring-boot` |
| SOAP Services | `semantic_search`: "@WebService", "JAX-WS", "wsdl" |
| Servlets/JSP | `file_search`: `*.jsp`, `web.xml`, "@WebServlet" |
| Spring Boot | `grep_search`: `@SpringBootApplication`, `spring-boot-starter` |
| Authentication | `semantic_search`: "JAAS", "Spring Security", "@Secured" |
| Database access | `semantic_search`: "JdbcTemplate", "JPA", "@Repository", "Hibernate" |
| Config files | `grep_search` in `application.properties`, `application.yml` |

**For `python`:**
| Discovery Target | Tool & Pattern |
|-----------------|----------------|
| Python version | `grep_search`: `python_requires`, `python = "`, `.python-version`, `runtime.txt` |
| Web framework | `grep_search`: `Django`, `Flask`, `FastAPI`, `Starlette`, `Tornado`, `Bottle` |
| WSGI/ASGI entry | `file_search`: `wsgi.py`, `asgi.py`, `app.py`, `main.py`; grep for `gunicorn` / `uvicorn` |
| Authentication | `grep_search`: `django.contrib.auth`, `flask-login`, `authlib`, `msal`, `authentik` |
| Database access | `grep_search`: `django.db.models`, `sqlalchemy`, `psycopg2`, `pymysql`, `cx_Oracle` |
| Config files | `grep_search` in `settings.py`, `.env`, `config.py`, `pyproject.toml` |

**For `nodejs`:**
| Discovery Target | Tool & Pattern |
|-----------------|----------------|
| Node version | `grep_search`: `"engines"`, `.nvmrc`, `package.json.engines.node` |
| Framework | `grep_search`: `express`, `fastify`, `koa`, `nestjs`, `hapi`, `next`, `nuxt` |
| Authentication | `grep_search`: `passport`, `express-session`, `jsonwebtoken`, `@azure/msal-node` |
| Database access | `grep_search`: `mongoose`, `sequelize`, `typeorm`, `prisma`, `pg`, `mysql2` |
| Config files | `grep_search` in `.env`, `config/`, `dotenv`, `next.config.js` |

**For `php`:**
| Discovery Target | Tool & Pattern |
|-----------------|----------------|
| PHP version | `grep_search`: `composer.json.require.php`, `php_version` in Dockerfile |
| Framework | `grep_search`: `Laravel`, `Symfony`, `CodeIgniter`, `CakePHP`, `Slim`, `Yii` |
| Web server config | `file_search`: `.htaccess`, `nginx.conf`, `php.ini` |
| Authentication | `grep_search`: `auth.php`, `Illuminate\\Auth`, `Symfony\\Component\\Security` |
| Database access | `grep_search`: `PDO`, `mysqli`, `Eloquent`, `Doctrine`, `ADOdb` |

**For `ruby`:**
| Discovery Target | Tool & Pattern |
|-----------------|----------------|
| Ruby version | `grep_search`: `Gemfile.ruby`, `.ruby-version` |
| Framework | `grep_search`: `Rails`, `Sinatra`, `Hanami`, `Padrino` |
| Authentication | `grep_search`: `devise`, `warden`, `sorcery`, `omniauth` |
| Database access | `grep_search`: `ActiveRecord`, `Sequel`, `pg`, `mysql2` |

**For `go`:**
| Discovery Target | Tool & Pattern |
|-----------------|----------------|
| Go version | `grep_search`: `go 1.` in `go.mod`, `runtime.Version()` |
| Framework | `grep_search`: `gin-gonic`, `echo`, `fiber`, `net/http`, `chi`, `gorilla/mux` |
| Authentication | `grep_search`: `jwt-go`, `oauth2`, `casbin`, `azuread` |
| Database access | `grep_search`: `database/sql`, `gorm.io`, `pgx`, `sqlx` |

**For `perl` / `rust` / `scala-kotlin` / `cobol-mainframe` / `oracle-forms` / `powerbuilder` / `delphi-vb6` / `cpp-windows`:**
Load the matching `stack-*.md` skill for its detection patterns and Azure compatibility guidance.

**Mixed-stack applications** (`.stack.secondary_stacks` is non-empty): run the discovery for each stack in scope, then reconcile findings in the assessment report.

#### 4.3 Dependency Analysis
- Extract all third-party dependencies from project files
- Check for deprecated or incompatible packages
- Identify dependencies with known Azure compatibility issues

#### 4.4 Azure Resource Check (Optional)
Use `azure_resources-query_azure_resource_graph` to check for existing Azure resources that might be related to this application.

### Step 5: Risk Assessment Matrix
Evaluate and categorize findings:

| Risk Level | Criteria | Action Required |
|------------|----------|-----------------|
| 🔴 **Critical** | Breaking changes, deprecated APIs, unsupported frameworks | Must address before migration |
| 🟠 **High** | Complex refactoring needed, significant code changes | Plan mitigation strategy |
| 🟡 **Medium** | Configuration changes, minor code updates | Include in migration tasks |
| 🟢 **Low** | Optional improvements, best practices | Nice-to-have enhancements |

### Step 6: Generate Assessment Report
Create comprehensive `reports/Application-Assessment-Report.md` with:

```markdown
# Application Assessment Report
**Generated:** [DATE/TIME]
**Application:** [NAME]
**Assessment Type:** Planning & Assessment

## Executive Summary
[Brief overview of findings and recommendations]

## Migration Configuration
- **Modernization Scope:** [User selection]
- **Target Platform:** [App Service/Container Apps/AKS]
- **IaC Tool:** [Bicep/Terraform]
- **Target Database:** [Azure SQL/Cosmos DB/etc.]

## Current Architecture
[Mermaid diagram of current application architecture]

## Target Azure Architecture
[Mermaid diagram of proposed Azure architecture]

## Application Analysis
### Technology Stack
### Dependencies
### Authentication & Authorization
### Data Access Patterns
### External Integrations

## Risk Assessment
[Table with all identified risks, severity, and mitigation strategies]

## Migration Plan
### Step 1: Preparation
### Step 2: Code Modernization
### Step 3: Infrastructure Setup
### Step 4: Deployment & Testing
### Step 5: Cutover & Validation

## Effort Estimation
[Timeline and resource estimates per phase]

## Cost Estimation (T-Shirt Sizing)

Provide a preliminary Azure cost estimate based on application characteristics:

| Size | Criteria | Estimated Monthly Cost Range |
|------|----------|------------------------------|
| **S (Small)** | Single web app, < 100 concurrent users, basic database | $50-150/month |
| **M (Medium)** | Web app + API, 100-500 users, standard database, caching | $150-500/month |
| **L (Large)** | Multiple services, 500-2000 users, premium database, CDN | $500-1500/month |
| **XL (Enterprise)** | Microservices, 2000+ users, HA/DR, premium everything | $1500+/month |

Based on the application analysis:
- **Recommended Size:** [S/M/L/XL]
- **Key Cost Drivers:** [List main cost components]
- **Cost Optimization Tips:** [Recommendations for cost savings]

Note: For detailed cost estimates, use the [Azure Pricing Calculator](https://azure.microsoft.com/pricing/calculator/).

## Change Report
[Detailed list of required changes with:]
- Issue/Breaking Change description
- Refactoring approach
- Supporting documentation links
- Objective and constraints
- Verification criteria

## Next Steps
Proceed to code migration using `/Phase2-MigrateCode`
```

## Rules & Constraints

### Code Reading
- Read **2000 lines at a time** for sufficient context
- Repeat reads as necessary until full understanding is achieved
- Use `semantic_search` for cross-file pattern discovery

### Report Management
- If `Application-Assessment-Report.md` exists, ask user:
  - **Overwrite?** Delete existing and create new
  - **Create new file?** Use timestamped filename
- Always update `reports/Report-Status.md` with current phase status

### Change Recommendations
Before suggesting any code changes:
1. **Verify** the change produces the intended result
2. **Document** standards and constraints:
   - Performance impact
   - Security implications
   - Readability/maintainability
3. **DO NOT MODIFY CODE** unless change can be confidently verified
4. **Flag for review** if not confident in the result
5. Explain what additional context/testing is needed for uncertain changes

### Report Quality
- Make reports **human-readable** with clear Markdown formatting
- Use headings, bullet points, tables, and Mermaid diagrams
- Include date/time at report beginning
- Clearly document **breaking changes** with handling guidance
- Provide specific guidance if assessment fails due to insufficient information

---

## Output Checklist
Before completing, ensure:
- [ ] User requirements fully captured and confirmed
- [ ] Solution builds successfully (or failures documented)
- [ ] All project files and dependencies analyzed
- [ ] Risk assessment completed with severity ratings
- [ ] Current architecture diagram created
- [ ] Target Azure architecture diagram created
- [ ] Migration plan with phases and timeline
- [ ] Change report with all required modifications
- [ ] `Report-Status.md` updated with assessment status
- [ ] Next steps clearly communicated: `/Phase2-MigrateCode`

---

## Next Steps

When Phase 1 is complete:

1. ✅ Update `reports/Report-Status.md` to mark **Phase 1: Planning & Assessment** as complete.
2. ▶️ Output the following Next Steps block to the user:

   > **Next Steps**
   >
   > Run **`/Phase2-MigrateCode`** to begin code modernization.
   >
   > Or click **🔧 Migrate code to target framework** if the handoff button is visible in your UI.
