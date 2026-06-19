---
"@robertoborges/azure-migration-squad": minor
---

**VS Code adoption: Welcome guide auto-installed on `ams init`**

`ams init` now drops a `MIGRATION-START-HERE.md` at the repo root the first time you initialize. It's a 60-second quickstart with:

- Where everything got installed
- A 3-step walkthrough to your first migration
- A "which prompt do I use?" decision flow
- Full prompt catalog (all 19 prompts in one table)
- Squad member highlights with their aliases
- Troubleshooting (slash commands not showing, Copilot CLI vs Chat differences, etc.)
- Telemetry opt-in / opt-out

The welcome doc is **install-once, never overwritten** — you can annotate it, delete it, or keep it as team onboarding. `ams upgrade` won't touch it.

Next-steps output from `ams init` now leads with "Open `MIGRATION-START-HERE.md`" so new users have a clear entry point.

Part of **Wave G — VS Code adoption push**. The full VS Code extension (sidebar, status bar, Command Palette commands) is coming next.
