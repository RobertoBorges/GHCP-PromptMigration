# Azure DevOps Bulk Clone Agent

A generic GitHub Copilot custom agent (VS Code `.agent.md`) that authenticates to any
Azure DevOps organization, lists every Git repository in a project, and clones all of
them locally (default branch each) — self-healing the common Windows-only checkout
failures along the way. **Local-only**: it never pushes or modifies anything server-side.

## Why this exists

Cloning 100+ repos by hand from Azure DevOps runs into a handful of very Windows-specific,
very non-obvious failures that have nothing to do with permissions or network:

- **Reserved device names** — any file named `aux`, `con`, `prn`, `nul`, `com1`-`com9`,
  `lpt1`-`lpt9` (with *any* extension, e.g. `aux.py`) cannot exist on an NTFS/Windows
  filesystem. `git checkout` fails with `error: invalid path '...'` even though the clone
  itself (object transfer) succeeded.
- **Path length limits** — old/monorepo-style repos frequently have paths over Windows'
  260-character limit, failing with `Filename too long`.
- **Invalid/control characters** — `< > : " | ? *` or raw control bytes in a filename
  (yes, this happens — usually from a bad merge or a tool that generated garbage) are also
  rejected by Windows, independent of path length.

None of these are your fault, none of them mean the clone "didn't work," and none of them
require opening a browser or contacting an admin — they just need a few extra git commands
per affected repo. This agent automates that recovery.

## Usage

1. Open this folder (or copy `.github/agents/AzureDevOps-BulkClone.agent.md` into your
   own repo's `.github/agents/`) in VS Code with GitHub Copilot.
2. Invoke the agent and tell it your Azure DevOps organization URL, project name, and
   where you want the repos cloned.
3. The agent will:
   - Install the `azure-devops` az CLI extension if missing.
   - Log you in via device code (no subscription required — Azure DevOps only needs an
     authenticated identity).
   - List and clone every repo (idempotent — safe to re-run, skips what's already there).
   - Auto-repair any Windows-specific checkout failures.
   - Report a final ok / ok-with-exclusions / fail summary, with manual `git clone`
     commands for anything it couldn't resolve automatically.

## Files

- `.github/agents/AzureDevOps-BulkClone.agent.md` — the agent definition.
- `scripts/clone-all.ps1` — the parameterized PowerShell script the agent runs
  (`-OrgUrl`, `-Project`, `-DestinationPath`). Usable standalone too.

## Requirements

- Azure CLI (`az`)
- Git for Windows
- PowerShell
- Python (optional — only needed to auto-detect invalid/control-character filenames;
  everything else works without it)
