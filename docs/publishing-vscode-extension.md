# Publishing the VS Code extension

The `azure-migration-squad-vscode` package is a VS Code extension that ships independently from the npm CLI. It's published to **two registries**:

1. **Visual Studio Marketplace** — used by Visual Studio Code (the main one)
2. **Open VSX Registry** — used by VS Codium, Gitpod, Eclipse Theia (open-source forks)

This doc walks through one-time setup + the per-release workflow.

---

## One-time setup

### Step 1 — Create a Visual Studio Marketplace publisher

The publisher is the namespace your extension lives under (e.g. `robertoborges.azure-migration-squad-vscode`).

1. Go to https://marketplace.visualstudio.com/manage
2. Sign in with your Microsoft account
3. Click **Create publisher**
4. Pick an ID that matches `publisher` in `packages/azure-migration-squad-vscode/package.json` (currently `robertoborges`)
5. Fill in display name + description

> If you choose a different publisher ID, update `package.json` `publisher` and `repository.url` accordingly, AND update `EXTENSION_ID` in `test/suite/extension.test.ts`.

### Step 2 — Generate a Personal Access Token (PAT) for vsce

`vsce` (the publishing CLI) authenticates via an **Azure DevOps PAT** — NOT a GitHub token.

1. Go to https://dev.azure.com (any organization — create one if you don't have one)
2. Top-right user menu → **Personal access tokens**
3. Click **New Token**
4. Settings:
   - **Name:** `azure-migration-squad-vscode publishing`
   - **Organization:** **All accessible organizations** ← critical
   - **Expiration:** maximum allowed (typically 1 year)
   - **Scopes:** **Custom defined** → check **Marketplace > Manage**
5. Click **Create**, copy the token

### Step 3 — Add the PAT to GitHub Secrets

1. Go to https://github.com/RobertoBorges/GHCP-PromptMigration/settings/secrets/actions
2. Click **New repository secret**
3. Name: `VSCE_PAT`
4. Value: paste the PAT from Step 2
5. Click **Add secret**

### Step 4 (optional) — Set up Open VSX publishing

Open VSX is the open-source extension registry. Recommended for max reach.

1. Sign in at https://open-vsx.org with GitHub
2. Click your avatar → **Settings** → **Access Tokens**
3. Create a token (any name, e.g. `github-actions`)
4. Add to GitHub Secrets as `OVSX_PAT`

If `OVSX_PAT` is missing, the publish workflow simply skips the Open VSX step (non-fatal).

---

## How to release a new version

### Option A — Tag-based release (recommended)

1. Bump the version in `packages/azure-migration-squad-vscode/package.json` (e.g. `0.1.0` → `0.2.0`)
2. Update `packages/azure-migration-squad-vscode/CHANGELOG.md` with the new version's notes
3. Commit and push to `main`:

   ```bash
   git add packages/azure-migration-squad-vscode/
   git commit -m "chore(vscode-ext): release v0.2.0"
   git push origin main
   ```

4. Create and push a tag matching the new version with the `vscode-v` prefix:

   ```bash
   git tag vscode-v0.2.0
   git push origin vscode-v0.2.0
   ```

5. The `.github/workflows/release-vscode-extension.yml` workflow runs, builds the `.vsix`, and publishes to both registries.

### Option B — Manual dispatch (for testing)

1. Go to https://github.com/RobertoBorges/GHCP-PromptMigration/actions/workflows/release-vscode-extension.yml
2. Click **Run workflow**
3. Pick branch `main`
4. **Dry-run only:** select `true` (default) for a build-only test, or `false` to actually publish
5. Click **Run workflow**

The dry-run mode builds the `.vsix` and uploads it as a workflow artifact, but skips both publish steps. Useful for verifying the build pipeline before a real release.

---

## Verifying a release

After publishing:

1. **Visual Studio Marketplace:** https://marketplace.visualstudio.com/items?itemName=robertoborges.azure-migration-squad-vscode
   - Takes ~5 minutes to appear after `vsce publish` succeeds.
2. **Open VSX Registry:** https://open-vsx.org/extension/robertoborges/azure-migration-squad-vscode
   - Usually instant.
3. **Install fresh in VS Code:**

   ```
   Ctrl+Shift+X → search "Azure Migration Squad" → Install
   ```

4. **Check the version matches** in the Extensions sidebar.

---

## Troubleshooting

| Error | Cause | Fix |
|-------|-------|-----|
| `Failed Request: Forbidden(403)` from vsce | PAT expired or wrong scope | Regenerate PAT with **Marketplace > Manage** scope across **all organizations** |
| `Publisher 'X' was not found` | PAT belongs to a different MS account than the publisher | Use the same Microsoft account for the publisher and the PAT |
| `Version X.Y.Z already published` | You forgot to bump the version | Increment `package.json` version, commit, retag |
| `Missing required field 'icon'` | `media/icon.png` is missing | Generate or copy the placeholder icon. CI already does this. |
| `License field is required` | LICENSE file not in `.vsix` | Verify `.vscodeignore` doesn't exclude `LICENSE` |
| Open VSX `Namespace 'X' not found` | Publisher namespace doesn't exist on Open VSX | Sign in at open-vsx.org and create the namespace once |

---

## Future improvements

- **Pre-release channel:** add `--pre-release` flag to `vsce publish` for insider builds. Tags like `vscode-v0.2.0-insider.1` could automatically map to pre-release.
- **Changesets integration:** wire the VS Code extension into changesets so version bumps + changelog updates flow from the same PRs as the npm package.
- **Signed extensions:** explore VS Code's extension signing (when generally available) for additional trust.
