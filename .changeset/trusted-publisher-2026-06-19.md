---
'@robertoborges/azure-migration-squad': patch
---

**Release auth migrated to npm Trusted Publisher (OIDC).** No more `NPM_TOKEN` rotation pain.

The `.github/workflows/release.yml` now publishes via short-lived OIDC tokens (npm CLI 11.5.1+ auto-detects the GitHub Actions OIDC env vars). Benefits:

- No `NPM_TOKEN` secret to rotate (npm's UI now caps Granular tokens at 365 days)
- Workflow-scoped — only `release.yml` can publish; a leak in another workflow can't be used
- Provenance attestation is auto-generated (the npm page will show "Built and signed on GitHub Actions")
- 5-minute publish tokens minted on demand; no long-lived secret can leak

**One-time maintainer action required:** configure Trusted Publisher in the npm UI at https://www.npmjs.com/package/@robertoborges/azure-migration-squad/access — full step-by-step in `docs/release-automation.md`.

After enabling Trusted Publisher, you can also revoke the existing `NPM_TOKEN` GitHub secret and enable "disallow tokens" on the package for maximum hardening.

This is a docs + workflow change only — no behavior change for end users of the package.
