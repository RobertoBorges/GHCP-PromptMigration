# Changesets

This repo uses [Changesets](https://github.com/changesets/changesets) to manage versions and the CHANGELOG.

## Adding a changeset

When you make a change worth releasing, run:

```bash
npx changeset
```

This walks you through:
1. **Which packages changed** (currently only `@robertoborges/azure-migration-squad`)
2. **What kind of change** (major / minor / patch)
3. **Summary** (one-liner for the CHANGELOG)

A new `.md` file is written to `.changeset/`. Commit it with your PR.

## Releasing

A maintainer runs:

```bash
npx changeset version    # consume all .changeset/*.md, bump versions, update CHANGELOG.md
npx changeset publish    # publish to npm
```

For `insider` releases:

```bash
npx changeset pre enter insider    # enter prerelease mode
# ... make changes, add changesets ...
npx changeset version              # bumps to e.g. 0.2.0-insider.0
npx changeset publish              # publishes to insider tag
npx changeset pre exit             # exit prerelease mode when ready for stable
```

## Conventions

- **Major** — breaking change to CLI commands, file layout, or schema
- **Minor** — new adapter, new agent, new skill, new feature
- **Patch** — bug fix, doc fix, description trim, dependency bump

## See also

- [Changesets docs](https://github.com/changesets/changesets/blob/main/docs/intro-to-using-changesets.md)
- [package CHANGELOG](../packages/azure-migration-squad/CHANGELOG.md)
