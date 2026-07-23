# Publishing the Azure Migration Agent VS Code extension

The extension is published to **two registries**:

1. **Visual Studio Marketplace** — used by Visual Studio Code (the main one)
2. **Open VSX Registry** — used by VS Codium, Gitpod, Eclipse Theia (open-source forks)

Versioning is fully automated via [release-please](https://github.com/googleapis/release-please). You **never edit `package.json` version by hand** for a normal release.

---

## The two flows

### 🤖 Flow 1 — Automated (the normal path)

```
you push conventional-commit PRs → merge to main → release-please opens
a "Release PR" → you merge it → tag fires → marketplace publishes
```

Details in [Flow 1 walkthrough](#flow-1-walkthrough) below.

### 🧪 Flow 2 — Local dry-run (preview / emergency hotfix)

```powershell
cd packages/azure-migration-squad-vscode
npm run release:local -- --dry-run    # preview only
npm run release:local -- --patch      # or --minor / --major
```

Details in [Flow 2 walkthrough](#flow-2-walkthrough) below. **The local script never pushes.**

---

## One-time setup (before the first automated release)

### Step 1 — Create a Visual Studio Marketplace publisher

1. Go to https://marketplace.visualstudio.com/manage
2. Sign in with your Microsoft account
3. Click **Create publisher**
4. Pick the ID `robertoborges` (matches `publisher` in `packages/azure-migration-squad-vscode/package.json`)
5. Fill in display name + description

### Step 2 — Generate the Azure DevOps PAT

`vsce` (the publishing CLI) authenticates via an **Azure DevOps PAT** — NOT a GitHub token.

1. https://dev.azure.com (any org — create one if you don't have one)
2. Top-right user menu → **Personal access tokens**
3. **New Token**:
   - **Name:** `vscode-marketplace-publishing`
   - **Organization:** **All accessible organizations** ← critical
   - **Expiration:** maximum allowed (typically 1 year)
   - **Scopes:** **Custom defined** → check **Marketplace > Manage**
4. Copy the token

### Step 3 — Add secrets to GitHub

Go to https://github.com/RobertoBorges/GHCP-PromptMigration/settings/secrets/actions and add:

| Secret name | Value | Required? |
|-------------|-------|-----------|
| `VSCE_PAT` | The Azure DevOps PAT from Step 2 | **Required** |
| `OVSX_PAT` | Token from https://open-vsx.org (see Step 4) | Optional — but recommended for VS Codium reach |
| `RELEASE_PLEASE_TOKEN` | A GitHub Fine-Grained PAT with `contents:write` + `pull-requests:write` | Optional but recommended (see note below) |

**About `RELEASE_PLEASE_TOKEN`:** When release-please creates the tag using the default `GITHUB_TOKEN`, GitHub does NOT trigger downstream workflows (a security feature). So `release-vscode-extension.yml` won't fire, and nothing publishes. If you provide `RELEASE_PLEASE_TOKEN`, the tag fires downstream workflows normally. Without it, you'll need to push the tag manually.

Create the PAT at https://github.com/settings/personal-access-tokens/new. Scope it to this single repo with `contents:write` + `pull-requests:write`.

### Step 4 (optional) — Open VSX setup

1. Sign in at https://open-vsx.org with GitHub
2. Avatar → **Settings** → **Access Tokens** → generate
3. Add to GitHub Secrets as `OVSX_PAT`

If `OVSX_PAT` is missing, the publish workflow simply skips the Open VSX step (non-fatal).

---

## Flow 1 walkthrough — normal releases

### Step 1 — Write conventional commits

Use `feat:` / `fix:` / `perf:` / `feat!:` prefixes so release-please can categorize them. See [`docs/conventional-commits.md`](./conventional-commits.md).

Example:

```bash
git commit -m "fix(sync): handle missing templates folder gracefully"
git commit -m "feat(commands): add Reload command to the palette"
```

### Step 2 — Open a PR, merge to `main`

Normal GitHub PR flow. Merge when green.

### Step 3 — release-please opens a Release PR

On the merge to `main`, the `.github/workflows/release-please.yml` workflow runs. It:

- Parses conventional commits since the last release tag
- Decides the semver bump (patch/minor/major)
- Opens (or updates) a PR titled **`chore(main): release vscode-v0.2.1`** with two changes:
  1. `packages/azure-migration-squad-vscode/package.json` — version bumped
  2. `packages/azure-migration-squad-vscode/CHANGELOG.md` — new entry with the commits

If there are no `feat:` / `fix:` / `perf:` / breaking commits since the last release, **no Release PR opens.** That's by design — chore/docs/refactor changes shouldn't trigger a release.

### Step 4 — Review + merge the Release PR

Merge when you're happy with the version + changelog.

### Step 5 — Auto-tag + auto-publish

The moment the Release PR merges, release-please:

- Creates a git tag `vscode-v0.2.1`
- Creates a GitHub Release with the changelog content

The tag push triggers `.github/workflows/release-vscode-extension.yml`, which:

- Runs the tag-vs-package.json version guard (fail-fast on mismatch)
- Builds the extension (`npm run sync && npm run build`)
- Packages the `.vsix` (`vsce package`)
- Publishes to VS Code Marketplace (`vsce publish` with `VSCE_PAT`)
- Publishes to Open VSX (with `OVSX_PAT`, if present)
- Uploads the `.vsix` as a workflow artifact (90-day retention)

Marketplace listing goes live in ~5 minutes.

### Step 6 — Verify

- **VS Code Marketplace:** https://marketplace.visualstudio.com/items?itemName=robertoborges.azure-migration-squad-vscode
- **Open VSX:** https://open-vsx.org/extension/robertoborges/azure-migration-squad-vscode
- **Fresh install** in VS Code: `Ctrl+Shift+X` → search "Azure Migration Agent" → verify the version number

---

## Flow 2 walkthrough — local preview / emergency hotfix

### When to use it

- **Preview** what release-please will do before you merge the Release PR
- **Test a specific version's .vsix** locally before publishing
- **Ship an emergency hotfix** when you can't wait for the PR-review cycle (rare)

### Commands

```powershell
cd packages/azure-migration-squad-vscode

# Preview only (no file changes)
npm run release:local -- --dry-run

# Auto-detect bump from commits (asks confirmation)
npm run release:local

# Force a specific bump
npm run release:local -- --patch
npm run release:local -- --minor
npm run release:local -- --major

# Skip the confirmation prompt (CI-friendly)
npm run release:local -- --patch --yes

# Skip the build step (just update files)
npm run release:local -- --patch --no-build

# Custom tag prefix (if you fork)
npm run release:local -- --patch --tag-prefix=my-prefix-v
```

### What the local script does

1. Reads current version from `package.json`
2. Finds the last `vscode-v*` tag
3. Parses commits since that tag
4. Decides the semver bump (or uses the flag you passed)
5. Shows you the plan (version + CHANGELOG entry)
6. Asks confirmation (unless `--yes` or `--dry-run`)
7. Updates `package.json` version
8. Prepends a new entry to `CHANGELOG.md`
9. Runs `npm run build && npm run package` to produce the versioned `.vsix`

### What the local script does NOT do

- Commit
- Create a git tag
- Push
- Publish to any marketplace

**You inspect and commit yourself.** The script prints the exact git commands to run:

```bash
git diff packages/azure-migration-squad-vscode/package.json packages/azure-migration-squad-vscode/CHANGELOG.md
git add packages/azure-migration-squad-vscode/{package.json,CHANGELOG.md}
git commit -m "chore: release vscode-v0.2.1"
git tag vscode-v0.2.1
git push origin HEAD vscode-v0.2.1
```

---

## Troubleshooting

| Error | Cause | Fix |
|-------|-------|-----|
| `Failed Request: Forbidden(403)` from vsce | PAT expired or wrong scope | Regenerate PAT with **Marketplace > Manage** scope across **all organizations** |
| `Publisher 'X' was not found` | PAT belongs to a different MS account than the publisher | Use the same Microsoft account for the publisher and the PAT |
| `Version X.Y.Z already published` | You retagged the same version | Bump the version (via release-please or `--patch`), commit, retag |
| `Missing required field 'icon'` | `media/icon.png` is missing | `git status` and confirm it's committed |
| `License field is required` | LICENSE file not in `.vsix` | Verify `.vscodeignore` doesn't exclude `LICENSE` |
| Open VSX `Namespace 'X' not found` | Publisher namespace doesn't exist on Open VSX | Sign in at open-vsx.org and create the namespace once |
| **release-please doesn't open a PR** | No `feat:` / `fix:` / `perf:` commits since last release | That's by design — only `feat/fix/perf` + breaking changes trigger releases. Add a `feat:` commit if you want to force one, or use the local flow. |
| **Tag pushed but marketplace didn't publish** | The tag was created by the default `GITHUB_TOKEN` (release-please), which doesn't trigger downstream workflows | Set `RELEASE_PLEASE_TOKEN` (see Step 3 above), OR push the tag manually |
| `Tag $TAG does not match package.json version` | You bumped one without the other | Never edit `package.json` version by hand — use release-please or the local script |

---

## Future improvements (deferred)

- **Pre-release channel:** add `--pre-release` flag to `vsce publish` for insider builds. Configure via a separate tag pattern (e.g., `vscode-v*-insider`).
- **Version-sync between root and extension:** if we add other packages later, coordinate their versions via release-please's monorepo mode.
- **Signed extensions:** explore VS Code's extension signing (when generally available) for additional trust.
