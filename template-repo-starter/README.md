# <Your Application> — Azure Migration

> Generated from [`azure-migration-squad-template`](https://github.com/RobertoBorges/azure-migration-squad-template). Replace this README with details about your specific application.

## What this repo is

This is your **migration workspace**. It contains:

- The application source you want to migrate (`Use-cases/<your-app>/`)
- The Azure Migration Squad — 15 specialist agents that will walk you through discovery, planning, and execution

## First-time setup (5 minutes)

```bash
# 1. Install Squad (the agent runtime)
npm install -g @bradygaster/squad-cli
squad init

# 2. Install the Azure Migration Squad (the migration content)
npx @robertoborges/azure-migration-squad@insider init

# 3. Open this folder in VS Code with GitHub Copilot Chat
code .

# 4. Replace `Use-cases/sample-aspnet-app/` with your actual application
#    (or point the discovery process at any other path / repo / cloud)
```

## Kick off the migration

In Copilot Chat, run:

```
/assess-any-application
```

The **Discovery Engineer (Saul Bloom Jr.)** will ask you six fast questions, probe your source, and produce two artifacts:

- `reports/Discovery-Dossier.md` — evidence-bound narrative
- `reports/Capability-Matrix.yaml` — machine-readable contract every later phase consumes

Then run:

```
/build-migration-plan
```

The **Architect (Danny Ocean)** approves the strategy and writes `reports/Migration-Plan.md`. From there, Phase 1 → Phase 6 prompts execute the migration with the right specialists dispatched for your specific source/stack/workload.

## What you'll get

After full execution:

| Artifact | Path |
|----------|------|
| Discovery findings | `reports/Discovery-Dossier.md` |
| Capability matrix | `reports/Capability-Matrix.yaml` |
| Approved plan | `reports/Migration-Plan.md` |
| Detailed assessment | `reports/Application-Assessment-Report.md` |
| Migrated code | wherever your source originally lived (now Azure-compatible) |
| Infrastructure-as-Code | `infra/main.bicep` or `infra/main.tf` |
| Deployment + CI/CD | `.github/workflows/` |
| Operational runbooks + alerts | `reports/Post-Migration-Ops.md` |
| Security review | `reports/Security-Review-Report.md` |
| Cost optimization plan | `reports/Cost-Optimization-Report.md` |

## Need help?

- 📚 Docs: https://github.com/RobertoBorges/GHCP-PromptMigration
- 🐛 Issues: https://github.com/RobertoBorges/GHCP-PromptMigration/issues
- 🔍 Squad CLI: https://github.com/bradygaster/squad

## License

MIT — adapt as needed for your engagement.
