# ⚠️ DO NOT EDIT FILES IN THIS FOLDER

This entire `templates/` directory is **auto-generated**. Edits made here will be silently overwritten the next time `npm run sync` runs — which happens:

- Automatically before every `npm pack` / `npm publish` (via the `prepack` → `prebuild` → `presync` → `sync` script chain)
- In CI on every PR (`.github/workflows/azure-migration-squad-ci.yml`)
- Anytime a maintainer runs `npm run sync` manually

## Where to edit instead

| File you want to change | Edit at this canonical location ✅ |
|--------------------------|-----------------------------------|
| `templates/github/prompts/*.prompt.md` | `.github/prompts/*.prompt.md` (at the monorepo root) |
| `templates/github/skills/*.md` and nested SKILLs | `.github/skills/*.md` |
| `templates/github/chatmodes/*.chatmode.md` | `.github/chatmodes/*.chatmode.md` |
| `templates/github/hooks/*.md` | `.github/hooks/*.md` |
| `templates/github/copilot-instructions.md` | `.github/copilot-instructions.md` |
| `templates/squad/agents/<name>/charter.md` | `.squad/agents/<name>/charter.md` |
| `templates/squad/team.md`, `templates/squad/routing.md` | `.squad/team.md`, `.squad/routing.md` |
| `templates/AGENTS.md` | `AGENTS.md` (at the monorepo root) |

After editing the canonical file, run `npm run sync` (from `packages/azure-migration-squad/`) to refresh this directory. Most contributors never need to run sync manually — it runs automatically.

## Why this layout exists

The monorepo dogfoods its own migration squad: the same `.github/` and `.squad/` folders that ship to end users are also active when you run Copilot/Squad against THIS repo. The `templates/` folder is what gets packaged into the npm tarball — it has to mirror the root content exactly.

## CI guard

`scripts/check-templates-not-edited.mjs` runs in CI and fails the build if a PR commits changes to `templates/` without the corresponding canonical file being changed in the same commit. If you see that error, undo your edit in `templates/` and re-apply at the source location.

## Audit trail

This directory contains a `SYNC-MANIFEST.json` file recording the last sync time + file count + source list. Don't edit it either.
