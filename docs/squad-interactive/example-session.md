# Example Session — Interactive Migration Interview

```text
User: @squad I have a legacy app to migrate.
Architect (Danny Ocean): Happy to lead the heist.
Architect: What application do you want to migrate? Point me to the folder or repo.
Architect: What's your target? (Azure App Service, Container Apps, AKS, etc.)
User: The app is in Use-cases\02-NetFramework30-ASPNET-WEB.
User: Target Azure App Service.
Architect: Got it. I'm scanning the codebase now.
Architect: Here's what I found. Correct?
Architect: - ASP.NET WebForms on .NET Framework 3.0
Architect: - C# solution with multiple projects
Architect: - SQL Server access through ADO.NET-style patterns
Architect: - `web.config` plus clear IIS hosting assumptions
Architect: - `.aspx` pages, code-behind, and ViewState risk
Architect: - No strong signal yet for CI/CD or IaC
Architect: Top concerns: WebForms rewrite, config modernization, and data-access coupling.
User: That's right.
Architect: Good. A few things the scan could not prove yet.
Architect: Do you want to stay on SQL Server via Azure SQL, or switch engines?
Architect: For IaC, do you prefer Bicep or Terraform?
Architect: For CI/CD, GitHub Actions or Azure DevOps?
Architect: Any compliance or timeline pressure I should plan around?
User: Keep SQL Server semantics, so Azure SQL.
User: Use Bicep.
User: GitHub Actions.
User: Small team, about eight weeks, no special compliance beyond standard secrets handling.
Architect: Perfect. Based on the scan and your answers, here's the migration plan.
Architect: Phase │ Status    │ What                               │ Lead Agent         │ Key Concerns
Architect: ──────┼───────────┼────────────────────────────────────┼────────────────────┼────────────────────────
Architect: 0     │ ⬜ Ready   │ Triage & codebase scan             │ Architect          │ WebForms, IIS, web.config
Architect: 1     │ ⬜ Pending │ Full assessment + risk matrix      │ Architect          │ ViewState, auth, SQL coupling
Architect: 2     │ ⬜ Pending │ Code migration to Azure App Service│ Coder              │ UI rewrite, EF Core path, config
Architect: 3     │ ⬜ Pending │ Generate Bicep                     │ Azure Specialist   │ App Service, Azure SQL, secrets
Architect: 4     │ ⬜ Pending │ Deploy to Azure App Service        │ DevOps Engineer    │ env config, smoke tests
Architect: 5     │ ⬜ Pending │ CI/CD pipeline                     │ DevOps Engineer    │ GitHub Actions, approvals
Architect: 6     │ ⬜ Pending │ Monitoring + operations            │ Observability Engineer │ App Insights, alerts, runbooks
Architect: I saved this to reports\Migration-Plan.md in the app directory.
Architect: Say `show phase 2`, `run phase 0 and 1, fan out`, `run all, fan out`, or `status`.
User: show phase 2
Architect: Phase 2 — Code migration to Azure App Service
Architect: What it does:
Architect: - Retarget the application from .NET Framework to .NET 8
Architect: - Replace WebForms-specific patterns that do not survive the move
Architect: - Modernize configuration and data access where needed
Architect: Likely files affected: `*.csproj`, `web.config`, startup/bootstrap files, WebForms pages, code-behind files, and data-access classes.
Architect: Estimated effort: 3-4 weeks of focused migration work.
Architect: Risks: UI parity drift, hidden ViewState behavior, and auth/session differences.
Architect: Mitigations: migrate incrementally, keep parity checkpoints, and validate high-risk pages first.
Architect: Exact CLI prompt:
Architect: `@squad run phase 2 for Use-cases\02-NetFramework30-ASPNET-WEB; migrate the app to Azure App Service on .NET 8, use Azure SQL, prefer Razor Pages, and fan out where safe.`
User: run phase 0 and 1, fan out
Architect: Copy that. Fan-out mode enabled.
Architect: Phase 0 is now 🔄 In Progress with Architect.
Architect: Phase 1 is now 🔄 In Progress with Architect support from Azure Specialist and Security Auditor.
Architect: I am validating framework inventory, app boundaries, auth patterns, and top risks in parallel.
Architect: Phase 0 complete.
Architect: Phase 1 assessment drafted.
Architect: Key findings:
Architect: - Windows/IIS hosting assumptions must be removed
Architect: - Forms auth needs a modern replacement decision
Architect: - ADO.NET usage is broad enough that EF Core should be phased in, not forced everywhere on day one
Architect: - Azure App Service remains the best initial landing zone
User: status
Architect: Phase │ Status    │ What                               │ Lead Agent         │ Key Concerns
Architect: ──────┼───────────┼────────────────────────────────────┼────────────────────┼────────────────────────
Architect: 0     │ ✅ Complete│ Triage & codebase scan             │ Architect          │ WebForms, IIS, web.config
Architect: 1     │ ✅ Complete│ Full assessment + risk matrix      │ Architect          │ ViewState, auth, SQL coupling
Architect: 2     │ ⬜ Pending │ Code migration to Azure App Service│ Coder              │ UI rewrite, EF Core path, config
Architect: 3     │ ⬜ Pending │ Generate Bicep                     │ Azure Specialist   │ App Service, Azure SQL, secrets
Architect: 4     │ ⬜ Pending │ Deploy to Azure App Service        │ DevOps Engineer    │ env config, smoke tests
Architect: 5     │ ⬜ Pending │ CI/CD pipeline                     │ DevOps Engineer    │ GitHub Actions, approvals
Architect: 6     │ ⬜ Pending │ Monitoring + operations            │ Observability Engineer │ App Insights, alerts, runbooks
Architect: Next best move: `@squad run phase 2 for Use-cases\02-NetFramework30-ASPNET-WEB and keep me posted on decision points.`
User: run phase 2
Architect: Phase 2 is now 🔄 In Progress.
Architect: Rusty Ryan is taking the code migration lead.
Architect: We are retargeting the solution, mapping WebForms pages, and identifying the safest UI migration path.
Architect: Decision needed before I continue.
Architect: WebForms UI can land as **Razor Pages** or **MVC**.
Architect: Recommended default: **Razor Pages** — it maps page-centric flows more directly and reduces ceremony for this app.
Architect: Alternative: **MVC** — stronger if you expect heavier controller/view separation or future API-style expansion.
Architect: Trade-off: Razor Pages is usually faster for WebForms replacement; MVC gives more structural separation but may increase rewrite effort.
Architect: Which do you want?
User: Go with Razor Pages.
Architect: Good choice. Continuing Phase 2.
Architect: We'll preserve page-oriented behavior where practical, move config toward `appsettings.json`, and stage ADO.NET-to-EF Core changes behind the highest-value paths first.
Architect: I'll surface the next decision if auth or data migration needs a deeper fork.
```
