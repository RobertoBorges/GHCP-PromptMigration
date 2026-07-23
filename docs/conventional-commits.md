# Conventional Commits — quick primer

This repo uses [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) so that **release-please** can auto-generate the version bump + changelog for every release.

## Format

```
<type>[optional scope]: <description>

[optional body]

[optional footer]
```

## Types that affect the version

| Prefix | Effect | Example |
|--------|--------|---------|
| `feat:` | **Minor** bump (0.2.0 → 0.3.0) | `feat(status-bar): show migration phase counter` |
| `fix:` | **Patch** bump (0.2.0 → 0.2.1) | `fix(commands): initialize no longer fails on empty workspace` |
| `perf:` | **Patch** bump | `perf(sync): parallelize template copy` |
| `revert:` | **Patch** bump | `revert: undo change from 3b63a0f` |
| `feat!:` OR `BREAKING CHANGE:` in body | **Major** bump (0.2.0 → 1.0.0) | `feat!(config): remove deprecated setting X` |

## Types that do NOT affect the version

Use for changes that don't need to ship a new release on their own:

- `chore:` — housekeeping (deps, config)
- `docs:` — documentation only
- `refactor:` — code cleanup, no behavior change
- `test:` — test-only changes
- `build:` — build system / tooling
- `ci:` — CI config

These still appear in commit history but don't trigger a release.

## Scope (optional)

Add a component in parentheses when it helps readers:

```
feat(commands): add "Reload" command
fix(templates): correct sync path for chatmodes
refactor(statusBar): extract phase-inference logic
```

Common scopes in this repo: `commands`, `templates`, `sync`, `statusBar`, `treeView`, `welcome`, `docs`, `ci`, `deps`.

## Body

Anything else you want to say. release-please picks up `BREAKING CHANGE:` markers from the body:

```
feat: drop the sync command from the CLI

BREAKING CHANGE: users must now use "Azure Migration: Initialize"
from the Command Palette instead of running `npm run sync` manually.
```

## Examples

```bash
# Adds a feature — bumps minor
git commit -m "feat(welcome): add first-run walkthrough panel"

# Fixes a bug — bumps patch
git commit -m "fix(sync): handle missing templates folder gracefully"

# Cleanup — no version change
git commit -m "refactor(commands): extract shared workspace-detection logic"

# Breaking change — bumps major
git commit -m "feat!(config): rename setting X to Y

BREAKING CHANGE: users on X must update their settings.json."
```

## Common mistakes

| ❌ Wrong | ✅ Right |
|---------|---------|
| `Fixed a bug` | `fix: correct pending decisions counter` |
| `Add feature` | `feat: add decisions tree view` |
| `feat: Add UI` (capital letter after `:`) | `feat: add UI` (lowercase preferred) |
| `feat:missing space` | `feat: missing space` |
| `feat: added feature` (past tense) | `feat: add feature` (imperative mood) |

## Enforcement

There's no lint-on-commit hook (yet). release-please will simply ignore commits that don't follow the convention, meaning **no version bump will be triggered** for those commits. If you push only `chore:` and `docs:` commits between releases, no Release PR opens. That's by design.

## Where release-please parses these

- Config: `release-please-config.json` at the repo root
- Manifest: `.release-please-manifest.json` (tracks the last-released version)
- Workflow: `.github/workflows/release-please.yml`

## Learn more

- Full spec: https://www.conventionalcommits.org/en/v1.0.0/
- release-please docs: https://github.com/googleapis/release-please
