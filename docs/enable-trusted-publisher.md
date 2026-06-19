# Enable Trusted Publisher — One-Time Setup

> **Action required from you, takes 30 seconds.** Without this step, the next release won't be able to publish via GitHub Actions because we removed the `NPM_TOKEN` dependency from the workflow.

## What you're doing

Configuring npm to trust your GitHub Actions `release.yml` workflow, so it can publish via short-lived OIDC tokens instead of a long-lived `NPM_TOKEN` secret. **You'll never have to rotate an npm token again.**

## Step 1 — Open the npm package access page

Go to: **https://www.npmjs.com/package/@robertoborges/azure-migration-squad/access**

Sign in if asked. Use the `ghcp-migratior` account (or any account with write access to `@robertoborges/azure-migration-squad`).

## Step 2 — Add the Trusted Publisher

1. Scroll down to the **"Trusted Publisher"** section (it's below "Package settings")
2. Click **"Select your publisher"** → click the **GitHub Actions** button
3. Fill in exactly these values:

   | Field | Value |
   |-------|-------|
   | **Organization or user** | `RobertoBorges` |
   | **Repository** | `GHCP-PromptMigration` |
   | **Workflow filename** | `release.yml` |
   | **Environment name** | *(leave completely blank)* |

4. Click **Save** (or **Add Trusted Publisher** — exact label varies)

✅ Done. The next time `release.yml` runs on `main`, it publishes via OIDC.

## Step 3 — (Recommended) Lock it down

Once Trusted Publisher is set up, prevent anyone from publishing with a stolen token:

1. Still on the same package page → **Settings** → **Publishing access**
2. Select **"Require two-factor authentication and disallow tokens"**
3. Save

This means: even if your `npm_37GX...` token leaks, nobody can publish with it. Only the configured `release.yml` workflow can publish.

## Step 4 — Clean up the old NPM_TOKEN

You no longer need the `NPM_TOKEN` GitHub secret. Remove it:

```bash
gh secret delete NPM_TOKEN --repo RobertoBorges/GHCP-PromptMigration
```

And revoke the npm token itself:
1. Go to https://www.npmjs.com/settings/<your-account>/tokens
2. Find the `npm_37GX...` token (or whatever name you gave it)
3. Click **Delete** / **Revoke**

This is the token I was pasting into `~/.npmrc` to manually publish — it's no longer needed.

## Step 5 — Test the new flow

Once Step 2 is done, here's the test:

```bash
# In a fresh branch:
git checkout -b test-trusted-publisher
# Make some trivial change — e.g., bump version of a dep
npx changeset             # add a patch changeset
git add . && git commit -m "test: trusted publisher" && git push
gh pr create --fill
# Merge the PR
# → GitHub Actions opens a "chore(release): version packages" PR
# → Merge that PR
# → release.yml runs again, publishes via OIDC, no NPM_TOKEN needed
```

The published package should show a **"Built and signed on GitHub Actions"** badge on its npm page — that's the provenance attestation that's auto-generated when publishing via Trusted Publisher.

## Troubleshooting

| If you see... | Fix |
|---------------|-----|
| "Trusted Publisher" section is missing from the npm UI | Make sure you're on the **package**'s page, not the org's page. The URL must include `/package/@robertoborges/azure-migration-squad/access` |
| Save button is disabled | Double-check there are no typos in repository name / workflow filename (case-sensitive on the GitHub side) |
| First publish after Step 2 fails with `403 Forbidden` | The Trusted Publisher save may not have persisted; re-verify it appears in the UI as "Configured" |
| First publish after Step 4 fails with `404 Not Found` | You deleted `NPM_TOKEN` before configuring Trusted Publisher — re-add the token temporarily, complete Step 2, then re-delete |

## Full docs

- `docs/release-automation.md` — full release flow
- npm Trusted Publishers official docs: https://docs.npmjs.com/trusted-publishers/

## Why this matters

| Before (Wave B with NPM_TOKEN) | After (Wave B+OIDC) |
|--------------------------------|---------------------|
| `npm_...` token in GitHub Secrets | No secret |
| Token expires (Granular: 365d) OR is forever (Classic: leak risk) | Tokens are 5 minutes, minted per-publish |
| Any workflow with secret access can publish | Only `release.yml` can publish |
| Manual `--provenance` flag for signed builds | Provenance auto-attached, "Built on GitHub Actions" badge |
| Need to rotate quarterly | Zero rotation forever |
