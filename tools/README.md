# Utility tools

Standalone helper tools that support Azure migration engagements without being part of the phased migration flow itself. Each tool is self-contained under its own subfolder.

## Available tools

### `GHCP-GitHub-BulkClone/`

Clone every accessible repository owned by a GitHub user or organization to your local machine.

- Includes public + private + archived repos + forks
- Resumable — skips already-cloned repos on rerun
- Repairs common Windows checkout failures (long paths, reserved filenames like `aux` / `con` / `nul`, invalid characters)
- Never pushes or modifies anything remote — local-only
- Ships as a standalone PowerShell script AND a GitHub Copilot agent

**Use it at the start of any engagement** where the customer says "here is our GitHub org — clone everything before you assess anything."

### `GHCP-AzureDevOps-BulkClone/`

Same shape as GitHub Bulk Clone but for Azure DevOps projects.

- Device-code login (no subscription required)
- Enumerates every Git repo in an Azure DevOps project
- Same Windows self-healing (long paths, reserved names, invalid characters)
- Local-only — never `git push`

## Usage patterns

Both tools work in two modes:

**1. Copilot agent mode (recommended for interactive engagements)**

Open the tool folder in VS Code with GitHub Copilot Chat installed. Select the agent from the picker and ask something like:

- `Clone all repositories from GitHub organization contoso into C:\Repos\contoso`
- `Clone all repos from the Azure DevOps project ContosoRetail into C:\Repos\contoso-retail`

**2. Standalone PowerShell script (recommended for automation / CI)**

```powershell
# GitHub
gh auth login --web --git-protocol https
.\tools\GHCP-GitHub-BulkClone\scripts\clone-all.ps1 -Owner "contoso" -DestinationPath "C:\Repos\contoso"

# Azure DevOps
.\tools\GHCP-AzureDevOps-BulkClone\scripts\clone-all.ps1 -Organization "contoso" -Project "ContosoRetail" -DestinationPath "C:\Repos\contoso-retail"
```

Both tools write a `repos.json` (visible repositories) and `clone-results.json` (per-repo outcome: `ok`, `skipped`, `ok-with-exclusions`, `fail`) to the destination folder.

## When to use these

| Situation | Which tool | Then |
|-----------|-----------|------|
| Customer's code lives in one GitHub org | GitHub Bulk Clone | Run `/assess-any-application` on each cloned repo |
| Customer's code lives in an Azure DevOps project | Azure DevOps Bulk Clone | Same |
| You need to see how many repos exist before quoting an engagement | Either (dry-run + `repos.json`) | Use the count to scope the assessment work |
| Multiple repos are one business solution | Either, then | Run `/Phase0-Multi-repo-assessment` |

## Where these came from

Adapted from the [GHCP Cloud Migration Toolkit](https://github.com/) — the Azure DevOps and GitHub bulk-clone components. Both scripts are proven-hardened for real customer engagements on Windows.
