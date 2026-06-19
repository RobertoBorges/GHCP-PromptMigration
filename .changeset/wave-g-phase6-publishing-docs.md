---
"@robertoborges/azure-migration-squad": patch
"azure-migration-squad-vscode": minor
---

**Phase 6: Publishing pipeline + comprehensive docs refresh**

This is the **Wave G v1 landing release**. The full feature set across Phases 1-6 is now production-ready.

### Publishing automation (G-D22)

- New `.github/workflows/release-vscode-extension.yml`: builds + packages + publishes the extension to **VS Code Marketplace** (via `vsce`) and **Open VSX Registry** (via `ovsx`).
- Trigger options:
  - Tag push matching `vscode-vX.Y.Z` (recommended for releases)
  - Manual workflow_dispatch with dry-run toggle (great for verifying the build pipeline without publishing)
- Required secrets: `VSCE_PAT` (Azure DevOps PAT with Marketplace > Manage scope). `OVSX_PAT` is optional — if absent, the workflow skips Open VSX gracefully.
- `.vsix` always uploaded as a workflow artifact for download/verification.

### Publishing documentation (G-D21)

New `docs/publishing-vscode-extension.md` walks through:
- Creating the VS Code Marketplace publisher
- Generating the Azure DevOps PAT (with the exact scopes required)
- Adding GitHub Actions secrets
- Setting up Open VSX (optional)
- Per-release workflow (tag-based + dispatch-based)
- Verifying releases on both registries
- Troubleshooting table for common errors (`403 Forbidden`, version conflicts, missing license, etc.)

### Comprehensive VS Code quickstart (G-E3)

New `docs/vscode-quickstart.md` is the new user-facing "fastest path to first migration" doc. Covers **both** install paths:

| Path | Audience | Steps |
|------|----------|-------|
| 🚀 Extension | Most users | One Marketplace install → welcome notification → click "Get started" |
| 💻 CLI | Terminal-first users | `npm install -g` → `ams init` |

Includes a decision table for which approach to pick, common tasks for both, and an extensive troubleshooting section.

### README updates (G-E1, G-E2, G-E4)

- Root `README.md`: New VS Code badge alongside npm. "Three ways" → "Four ways to install". Extension is now Option 1 with one-click marketplace link.
- Package `README.md`: Top callout pointing VS Code users to the extension. Same source-of-truth, different surface.
- `MIGRATION-START-HERE.md`: Updated extension URL (corrected from `azure-migration-squad` to `azure-migration-squad-vscode`); removed "(coming soon)" markers since the extension is now real.
- Extension `README.md`: Rewritten from "Phase 2 scaffold" stub to a marketplace-ready listing with feature highlights, settings table, and architecture explanation.
- Extension `CHANGELOG.md`: Replaced Phase 2 placeholder with full 0.1.0 release notes covering all features (tree views, status bar, settings, welcome panel, walkthrough, Copilot install, publishing).

### Reliability fix: clean-templates retries on Windows EBUSY

`packages/azure-migration-squad/scripts/clean-templates.mjs` now retries with backoff (200ms → 500ms → 1s) when file deletion fails with EBUSY/EPERM/ENOTEMPTY. This eliminates intermittent failures on Windows when the CI guard's snapshot walk holds file handles briefly. Tested with 5 consecutive runs — all passing.

### What's NOT in this release

- **Marketplace icon** — still using a placeholder (Azure blue with "AMS" text). Real icon is queued for the next release.
- **Screenshots in marketplace listing** — empty for now. Will be captured manually after the first published release.
- **Version sync automation** between npm package and extension — manual for now. The `scripts/sync-extension-version.mjs` script idea is documented in `docs/publishing-vscode-extension.md` under "Future improvements".

### Migration path for first publish

1. Create publisher `robertoborges` on https://marketplace.visualstudio.com/manage (one-time)
2. Generate Azure DevOps PAT, add as `VSCE_PAT` secret in GitHub
3. (Optional) Sign in at https://open-vsx.org, generate token, add as `OVSX_PAT`
4. Push tag: `git tag vscode-v0.1.0 && git push origin vscode-v0.1.0`
5. Watch the `Release VS Code extension` workflow → marketplace listing live in ~5 min

Full instructions in `docs/publishing-vscode-extension.md`.
