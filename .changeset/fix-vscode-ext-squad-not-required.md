---
"azure-migration-squad-vscode": patch
---

**Fix: clicking "Azure Migration Squad not installed in this workspace" no longer dead-ends with `Squad runtime not detected`**

The extension now detects whether `.squad/` exists in the workspace and passes `--force` to `npx ams init` when it doesn't. This is safe because the AMS package's templates include the entire `.squad/agents/` charter tree — passing `--force` produces a fully-functional setup without requiring a separate global `@bradygaster/squad-cli` install.

What changed:

- New `src/util/squadDetection.ts` module classifies workspace state into 4 buckets (`no-squad` / `cli-available` / `squad-initialized` / `ams-installed`) and returns the right `ams init` flags for each.
- `cmdInitialize` now consults the detection module, prints a clear status line in the output channel ("Squad CLI not detected — that's OK"), and runs `npx ams init --force` when needed.
- Tree-view "Not installed" item relabeled to **"Click to install Azure Migration Squad here"** with a rocket icon. Tooltip clarifies Squad CLI is optional.
- New optional command **`Azure Migration: Install Squad CLI globally (optional)`** — opens a terminal pre-filled with `npm install -g @bradygaster/squad-cli`. Power users only.
- 4 new unit tests covering each squad-state → init-flags transition.

Before this fix, a user clicking the tree item on a fresh workspace would see:
```
✗ Squad runtime not detected in this directory.
  ... please initialize Squad first ...
◀ exit 1
```
and the toast: "Azure Migration Squad: init failed with exit 1".

After: init succeeds, prompts/skills/agents land in the workspace, the welcome doc auto-opens.
