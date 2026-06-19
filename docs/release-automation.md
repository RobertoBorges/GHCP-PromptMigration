# Release Automation

> Releases ship via **npm Trusted Publisher** (OIDC). No long-lived `NPM_TOKEN` to rotate.

## TL;DR for maintainers

```bash
# 1. After making changes, add a changeset
npx changeset
# (pick the package, severity, write a one-line summary)

# 2. Commit and push
git add . && git commit -m "feat: ..." && git push

# 3. GitHub Actions does the rest:
#    - Opens a "chore(release): version packages" PR
#    - When that PR merges → publishes to npm via OIDC (no token)
```

That's it. No `npm login`, no token rotation, ever.

---

## One-time setup — enable Trusted Publisher in npmjs.com

This is the **only** manual step. Do it once. Takes 30 seconds.

### Step 1 — Make sure the package exists on npm

Trusted Publisher can only be added to a package that's already published at least once. We did this in v0.1.0-insider.0, so this prerequisite is already satisfied.

### Step 2 — Configure the Trusted Publisher

1. Go to your package's access page:
   **https://www.npmjs.com/package/@robertoborges/azure-migration-squad/access**
2. Scroll down to the **"Trusted Publisher"** section
3. Click **"Select your publisher"** → **GitHub Actions**
4. Fill in:

   | Field | Value |
   |-------|-------|
   | Organization or user | `RobertoBorges` |
   | Repository | `GHCP-PromptMigration` |
   | Workflow filename | `release.yml` |
   | Environment name | *(leave blank)* |

5. Click **Save**

That's it. The next time `release.yml` runs on `main`, npm will accept its OIDC token instead of requiring `NPM_TOKEN`.

### Step 3 — (Recommended) Restrict token publishing

Once Trusted Publisher works:

1. Go to **Settings** → **Publishing access** on the same package page
2. Select **"Require two-factor authentication and disallow tokens"**
3. Save

This blocks anyone from publishing with a stolen npm token. Only the configured Trusted Publisher workflow can publish.

### Step 4 — Revoke any old NPM_TOKEN

If you set up the `NPM_TOKEN` GitHub secret earlier:

1. https://www.npmjs.com/settings/<your-account>/tokens — delete the old `npm_...` token
2. `gh secret delete NPM_TOKEN --repo RobertoBorges/GHCP-PromptMigration`

---

## How it actually works

```
You merge "Version Packages" PR
            │
            ▼
GitHub Actions runs release.yml
            │
            ├─ permissions.id-token: write  →  GitHub provides ACTIONS_ID_TOKEN_REQUEST_URL/_TOKEN env vars
            │
            ▼
   changesets/action@v1 → npm run changeset:publish → npm publish
            │
            ├─ npm CLI (11.5.1+) auto-detects OIDC env vars
            ├─ requests an ID token from GitHub Actions
            └─ sends it to npm registry
                        │
                        ▼
   npm verifies: signed by GitHub Actions? from RobertoBorges/GHCP-PromptMigration?
                 workflow == release.yml? → if all yes:
                        │
                        ├─ issues a 5-min short-lived publish token
                        ├─ accepts the package
                        └─ auto-generates Provenance attestation (sigstore-signed)
```

The published package shows a **"Built and signed on GitHub Actions"** badge on its npm page.

---

## Day-to-day release flow

### Adding a changeset

```bash
npx changeset
```

Pick:
1. **Which packages changed** — currently only `@robertoborges/azure-migration-squad`
2. **What kind of change**:
   - **patch** — bug fix, doc fix, dep bump
   - **minor** — new adapter, new agent, new skill, new feature
   - **major** — breaking change to CLI commands, file layout, or schema
3. **Summary** — one-liner for the CHANGELOG (markdown supported)

A new `.md` file lands in `.changeset/`. Commit it.

### After merge

1. Push to `main`
2. `release.yml` runs
3. If `.changeset/*.md` files exist → opens "chore(release): version packages" PR
4. You merge that PR
5. `release.yml` runs again → publishes via OIDC

---

## Prerelease mode (`insider` channel)

The repo is currently in **prerelease mode** with tag `insider`. Every `changeset version` bump produces `0.1.0-insider.N`.

To **exit prerelease mode** and ship a stable `0.1.0`:

```bash
npx changeset pre exit
```

Then add a final changeset and merge — it publishes to the `latest` tag.

To **re-enter prerelease** later:

```bash
npx changeset pre enter insider
```

---

## Manual fallback (emergency only)

If GitHub Actions is unavailable AND Trusted Publisher is set to "disallow tokens":

1. **Settings → Publishing access** → switch back to "Require two-factor authentication" (without disallowing tokens)
2. Generate a temporary Classic Automation Token at https://www.npmjs.com/settings/<account>/tokens/new (these don't expire)
3. `echo "//registry.npmjs.org/:_authToken=npm_<token>" >> ~/.npmrc`
4. `npx changeset` → `npx changeset version` → `cd packages/azure-migration-squad && npm publish --tag insider --access public`
5. **CRITICAL:** remove the token from `~/.npmrc`, revoke it on npm, re-enable "disallow tokens"

This should be very rare. Prefer waiting for Actions.

---

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| Workflow fails with `npm error 403 Forbidden` | Trusted Publisher not configured on npm side | Complete Step 2 above |
| Workflow fails with `npm ERR! No OIDC token available` | `permissions: id-token: write` missing | Already set in `release.yml`; verify it wasn't removed |
| Workflow fails with `npm warn workspaces` | OK to ignore — only a warning | No action needed |
| "No changesets" but you expected a release | You didn't commit a `.changeset/*.md` file | `npx changeset` then commit |
| Version PR keeps reopening with stale content | Old draft PR still open | Close the old PR; Changesets opens a fresh one |
| `npm publish` succeeds but no provenance badge | Trusted Publisher not active (still using token) | Confirm Step 2 done |

---

## Why Trusted Publisher beats long-lived tokens

| Concern | `NPM_TOKEN` | Trusted Publisher (OIDC) |
|---------|------------|--------------------------|
| Token rotation | Required (Granular: 365d max; Classic: never expires but still a secret) | **None — no token exists** |
| Leak risk | A leaked token can publish from anywhere | **Tokens are 5-min and workflow-scoped** |
| Workflow scope | Any workflow with access to the secret | **Only `release.yml` can publish** |
| Provenance | Manual `--provenance` flag | **Automatic — "Built and signed on GitHub Actions" badge** |
| Setup | Generate token → copy → `gh secret set` → store securely | **5 clicks in the npm UI** |
| Supported by | Anything | GitHub Actions, GitLab CI, CircleCI |

---

## Files involved

| File | Role |
|------|------|
| `package.json` (root) | Declares `@changesets/cli` devDep + `changeset` scripts |
| `.changeset/config.json` | Changesets config |
| `.changeset/pre.json` | Records prerelease mode + tag |
| `.changeset/<random-name>.md` | A pending change description |
| `.github/workflows/release.yml` | Runs `changesets/action@v1` using OIDC |
| `packages/azure-migration-squad/CHANGELOG.md` | Auto-updated by `changeset version` |

## Reference

- npm Trusted Publishers: https://docs.npmjs.com/trusted-publishers/
- Changesets: https://github.com/changesets/changesets
- `changesets/action`: https://github.com/changesets/action
- GitHub OIDC: https://docs.github.com/en/actions/deployment/security-hardening-your-deployments/about-security-hardening-with-openid-connect
- Provenance: https://docs.npmjs.com/generating-provenance-statements
