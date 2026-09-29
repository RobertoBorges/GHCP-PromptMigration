# Skill: Stack Adapter — Oracle Forms / Reports

> Stack adapter for Oracle Forms / Reports / Oracle Application Express (APEX) migrations to Azure.

> **High-risk path.** Almost always pairs with `source-oracle-db` and `Architect` + `Database Specialist` + `Security Auditor`.

## When to Use

- `stack.primary_stack: oracle-forms` in the Capability Matrix
- File evidence: `*.fmb` / `*.fmx` (Forms), `*.rdf` / `*.rep` (Reports), `*.mmb` / `*.mmx` (Menus), `*.olb` (Object Libraries), `*.pll` / `*.plx` (PL/SQL libraries), `*.fmt` (text export of forms)
- User describes Oracle Forms Builder, Oracle Reports, Oracle WebLogic Forms Services

## Sub-Stack Detection

| Sub-stack | Detection signal | Typical migration target |
|-----------|------------------|--------------------------|
| **Oracle Forms (client/server)** | `*.fmb` / `*.fmx`; runs in Oracle Forms Runtime | Rewrite as web app (APEX / Java / .NET) — no PaaS Azure target preserves Forms |
| **Oracle Forms (Web / Forms Services)** | Hosted on WebLogic Forms Services | Rewrite, OR rehost on Azure VMs running WebLogic Forms |
| **Oracle Reports** | `*.rdf` / `*.rep` | Rewrite as Power BI / Azure Synapse reports |
| **Oracle APEX** | APEX workspace schema in DB; `f?p=` URLs | Continue using APEX on Azure (Oracle Database Service for Azure, or Oracle DB on Azure VMs) |
| **PL/SQL packages (heavy)** | Many `*.pks` / `*.pkb` files (or in-DB) | Migrate to Azure SQL with Babelfish-like translation tools (limited); or refactor logic to app tier |
| **Oracle Discoverer / Forms+Reports combo** | mixed `.fmb` + `.dis` | Rewrite both |

## Probes

### Forms inventory

For each `*.fmb` (binary) or `*.fmt` (text export):

- Form name
- Data blocks (table sources)
- Items (fields)
- Triggers (`WHEN-NEW-FORM-INSTANCE`, `WHEN-BUTTON-PRESSED`, etc.)
- LOVs (List of Values)
- PL/SQL units called
- External library references (`*.pll`)
- Forms-specific functions (`GO_BLOCK`, `EXECUTE_QUERY`, `COMMIT_FORM`)

If only `*.fmb` is available (binary), use Oracle Forms Compiler `frmcmp.exe` with `module_type=form` to extract `*.fmt` (text) for analysis.

### Reports inventory

For each `*.rdf`:

- Data model (queries)
- Layout sections (header / body / margin / trailer)
- Parameters
- Triggers
- Output formats

### PL/SQL library inventory

For each `*.pll` / `*.plx`:

- Package + procedure list
- Cross-form usage

### Forms environment

- `formsweb.cfg` — WebLogic Forms Services config
- `default.env` — environment variables (Forms paths)
- Java applets / Forms Java listener config (legacy)

### Database backing

- Schema owner(s) used by Forms
- Tables, views, sequences, triggers
- PL/SQL packages used (often the real business logic)
- Database links to other Oracle instances

### Authentication

- Oracle Forms typically uses DB users for authentication (`username/password@SID`)
- Schema-per-user pattern → must redesign for any modern target

## Phase 2 Effort Mapping

Forms migrations are **always L or XL**.

| Approach | Effort | When to choose |
|----------|--------|---------------|
| **Rewrite to Oracle APEX (stay Oracle-native)** | L | Customer wants minimal data-tier change; Oracle DB on Azure VMs or ODSA |
| **Rewrite to Java + Spring Boot (modernize)** | XL | Customer wants to escape Oracle vendor lock |
| **Rewrite to .NET + ASP.NET Core** | XL | Customer is .NET-shop; modernization goal |
| **Lift-and-shift Forms Services to Azure VM running WebLogic Forms** | M | Buying time; vendor license required; not strategic |
| **Migrate to Power Apps / Power BI (low-code)** | L | Small forms with simple workflows |

## Identity Modernization

| Today | Target |
|-------|--------|
| DB users for Forms login | Application-tier auth → Entra ID; DB connections via service identity |
| Schema-per-user | Single DB user (service account) + app-tier row-level security |

## Data Migration

Forms is tightly coupled to Oracle DB. Data migration is a separate workstream coordinated with **Database Specialist**:

| Source | Target options |
|--------|----------------|
| Oracle DB | Oracle Database Service for Azure (ODSA) — keep Oracle |
| Oracle DB | Azure SQL DB (significant schema/PL/SQL rewrite) |
| Oracle DB | PostgreSQL Flexible Server (popular open-source migration target; tools like Ora2Pg) |
| Oracle DB | Oracle DB on Azure VMs / AVS |

## Target Azure Mapping

| Approach | Compute (app tier) | Data tier |
|----------|--------------------|-----------|
| APEX rewrite | Oracle APEX (in DB) | Oracle DB on Azure VMs / ODSA |
| Java Spring Boot rewrite | App Service / Container Apps | PostgreSQL Flexible (preferred) or Oracle |
| .NET rewrite | App Service / Container Apps | Azure SQL or PostgreSQL |
| Lift WebLogic Forms Services | Azure VM (WebLogic) | Oracle DB on Azure VMs |
| Power Apps | Power Platform | Dataverse (small) or backing DB |

## Anti-Patterns

- Don't promise a "lift-and-shift" of Forms to App Service. App Service does not host Oracle Forms Runtime.
- Don't auto-translate PL/SQL packages to T-SQL during Forms migration. PL/SQL is often where business logic lives — review with Database Specialist, decide app-tier vs DB-tier per package.
- Don't migrate "the Form" — migrate the **business process** the Form represents. Forms often duplicate database CRUD; you may end up rewriting fewer screens than you have `*.fmb` files.
- Don't ignore Reports. They're often more business-critical than the Forms themselves.
- Don't underestimate UX rewrite cost. Forms apps have decades of muscle memory; user training is a real Phase 4 line item.

## Output Checklist

- [ ] Sub-stack identified (Forms client/server / Forms Web / Reports / APEX / mixed)
- [ ] Forms inventory captured (`*.fmb` count + form names)
- [ ] Reports inventory captured (`*.rdf` count)
- [ ] PL/SQL library inventory captured (`*.pll` count)
- [ ] Forms Services config captured (formsweb.cfg / default.env)
- [ ] DB schema + PL/SQL package list captured
- [ ] Authentication pattern captured
- [ ] Approach option(s) selected (APEX / Java / .NET / lift / Power Apps)
- [ ] Phase 2 effort label assigned (always L or XL)
- [ ] Target Azure compute + data tier identified
- [ ] Database Specialist + Security Auditor + Architect all flagged as required
