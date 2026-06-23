---
"azure-migration-squad-vscode": patch
---

**Fix: AMS agents now register with Squad CLI's Copilot Chat dropdown after `Initialize`**

When the user installed AMS via the VS Code extension, the agent charters landed on disk at `.squad/agents/<name>/charter.md` but Copilot Chat's `@`-agent dropdown didn't pick them up. Root cause: passing `--force` to `ams init` bypasses `squad init`, which is the call that registers agents with the Squad CLI's chat participant registry.

This release closes the loop without making Squad CLI mandatory:

- After `ams init` succeeds, the extension prompts:
  - **If Squad CLI is on PATH:** "Register agents with Squad CLI? Opens a terminal with `squad init` pre-typed." User reviews and presses Enter to run.
  - **If Squad CLI is not installed:** "Install Squad CLI globally for `@`-agent dispatch?" Opens a terminal with `npm install -g @bradygaster/squad-cli` ready.
  - Both prompts have "Don't ask again" / "Learn more" options.
- A second prompt offers to **reload the VS Code window** (needed so new `.github/chatmodes/` files register with Copilot Chat).
- New Command Palette entry: `Azure Migration: Register agents with Squad CLI (squad init)` — same flow, available any time.
- New setting `azureMigrationSquad.promptSquadInit` (default `true`) to permanently disable the post-init prompt for users who prefer slash commands only.

Slash-command users (`/assess-any-application`, `/Phase1-PlanAndAssess`, etc.) are unaffected and still get a fully functional setup with no Squad CLI install required.
