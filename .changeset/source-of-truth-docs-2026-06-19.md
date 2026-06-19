---
'@robertoborges/azure-migration-squad': patch
---

Source-of-truth clarity + edit-guard:

**Docs**
- Root `README.md` now opens with a "Source-of-truth rule" section + table mapping every editable area to its canonical location
- Repository structure tree marks every directory as ✏️ EDIT or ❌ DO NOT EDIT
- Package `README.md` gains a "For contributors — source-of-truth rule" section
- New `packages/azure-migration-squad/templates/README.md` is a big DO-NOT-EDIT sign at the entry of the auto-generated folder
- `docs/contributing-adapters.md` opens with a "Critical first rule — where to edit" section

**CI guard**
- New `scripts/check-templates-not-edited.mjs` snapshots `templates/`, re-runs sync, and fails the build if any file differs (i.e., someone edited `templates/` directly instead of the canonical root location)
- Wired into both `azure-migration-squad-ci.yml` and `release.yml` as a step BEFORE sync/build
- New root script: `npm run validate:templates-not-edited`
- `validate:all` now includes the guard

**Workflow comments**
- Both GitHub Actions workflows (`azure-migration-squad-ci.yml` and `release.yml`) gain a prominent ASCII-bordered comment at the top describing the source-of-truth rule so anyone reading the workflow YAML sees it

**Misc**
- `clean-templates.mjs` now preserves `README.md` and `.npmignore` across syncs (in addition to `.gitkeep`) — they're intentional, not noise
- `.npmignore` inside `templates/` excludes `README.md` from the published tarball (it's a repo-only warning sign, not user content)
