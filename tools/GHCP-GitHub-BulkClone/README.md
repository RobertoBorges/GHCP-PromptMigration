# GitHub Bulk Clone Agent

A GitHub Copilot custom agent for VS Code that authenticates with GitHub, lists every accessible repository owned by a user or organization, and clones each repository's default branch locally. It is resumable, includes public/private repositories, archived repositories, and forks, and repairs common Windows checkout failures.

The workflow is local-only: it never pushes or changes GitHub repositories.

## Usage

1. Open this folder in VS Code with GitHub Copilot.
2. Select **GitHub Bulk Clone Agent** from the agent picker.
3. Ask it to clone an owner, for example: `Clone all repositories from my-org into C:\Repos\my-org`.
4. Complete GitHub's browser/device authentication if prompted.

The agent previews how many repositories are visible, runs the clone, and reports `ok`, `skipped`, `ok-with-exclusions`, and `fail` totals.

## Standalone script

After authenticating with GitHub CLI, the PowerShell script can be run directly:

```powershell
gh auth login --web --git-protocol https
.\scripts\clone-all.ps1 -Owner "my-org" -DestinationPath "C:\Repos\my-org"
```

The destination receives two report files:

- `repos.json`: repositories visible to the authenticated GitHub account.
- `clone-results.json`: result and excluded paths for each repository.

Existing complete Git checkouts are skipped, so rerunning the command safely resumes an interrupted batch. An existing incomplete directory is reported as failed and left untouched. The script clones through GitHub CLI and never embeds an access token in clone URLs.

## Windows recovery

The script enables Git long-path support for each clone without changing global Git configuration, and retries clones that downloaded successfully but failed during checkout. It detects and excludes filenames Windows cannot represent, including reserved device names (`aux`, `con`, `nul`, and similar names) and invalid/control characters. Such repositories are explicitly reported as `ok-with-exclusions`.

Python is optional and is used only for invalid/control-character filename detection.

## Requirements

- GitHub CLI (`gh`)
- Git for Windows
- PowerShell
- Python (optional)

The authenticated GitHub account must have read access to private repositories. Organizations using SAML SSO may require separate browser authorization for the GitHub CLI credential.

## Files

- `.github/agents/GitHub-BulkClone.agent.md`: custom agent definition.
- `scripts/clone-all.ps1`: parameterized bulk-clone implementation.