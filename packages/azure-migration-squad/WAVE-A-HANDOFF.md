# Wave A — PUBLISHED ✅

> **Status (2026-06-18, FINAL):** v0.1.0-insider.0 is LIVE on npm. Installable today via `npx @robertoborges/azure-migration-squad@insider init`. End-to-end verified from public npm registry.

## 🎉 Publish results

| Field | Value |
|-------|-------|
| **Package** | `@robertoborges/azure-migration-squad` |
| **Version** | `0.1.0-insider.0` |
| **Dist-tag** | `insider` (also `latest` — npm auto-set) |
| **Access** | `public` |
| **Tarball** | `https://registry.npmjs.org/@robertoborges/azure-migration-squad/-/azure-migration-squad-0.1.0-insider.0.tgz` |
| **Package size** | 368.1 kB |
| **Unpacked size** | 1.3 MB |
| **Total files** | 187 |
| **Shasum** | `be83bd4461a6f78eae8b50d429627e886e66beea` |
| **Integrity** | `sha512-ozvQwyW4ttQpVk+d8T5b1MfkkKtz1OTnpcZz99GmrQIz4DDku9JJF43eua8L/skH/cOUHsfKS13aPdVdnMugag==` |
| **Maintainer** | `ghcp-migratior` (publishing service account in `@robertoborges` org) |
| **Telemetry** | ✅ Active (PostHog Cloud US, key `phc_nYir...`) — opt-out by default |

## 🧪 Live install verification (just ran)

```
npx --yes @robertoborges/azure-migration-squad@insider init
→ Installed 175 file(s)
→ 177 total files in target dir (incl. manifest)

npx --yes @robertoborges/azure-migration-squad@insider doctor
→ Squad runtime detected
→ Manifest present (v0.1.0-insider.0)
→ All 4 required agents installed
→ All 4 required skills installed
→ All 2 required prompts installed
→ All checks passed ✓
```

## 📝 What end users do now

```bash
# 1. Set up Squad (one-time)
npm install -g @bradygaster/squad-cli
squad init

# 2. Add the Azure Migration Squad
npx @robertoborges/azure-migration-squad@insider init

# 3. Open GitHub Copilot Chat → run:
/assess-any-application
```

## 🔄 To publish a new version later

The npm token (`npm_37GX...`) was REMOVED from `~/.npmrc` after this publish (security hygiene). To publish again:

1. Re-add the auth line to `~/.npmrc`:
   ```
   //registry.npmjs.org/:_authToken=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
   ```
2. Bump version: `cd packages/azure-migration-squad && npm version prerelease --preid=insider`
3. Publish: `npm publish --tag insider --access public`
4. Remove the token line again

For a stable release on `latest`:
- Bump to `0.1.0` (no `-insider` prefix)
- `npm publish --tag latest --access public`

## 🐛 Issues found and fixed during deploy

1. **`./bin/cli.js` was invalid in package.json** — npm silently strips `./` prefix and the bin entries would have been removed. Fixed to `bin/cli.js`.
2. **`--version` flag returned help instead of version** — argparser didn't catch flag-style invocation. Fixed in main dispatcher.
3. **404 on first verify** — package was published as private by default (despite `publishConfig.access: public`). Used `npm access set status=public` to flip it. Future publishes will inherit public access from `publishConfig`.

## ⏭️ Next waves (NOT in scope for Wave A)

- **Wave B:** Squad plugin marketplace registration (`.squad-plugin.json` + submission to bradygaster)
- **Wave C:** Docs hub repositioning (README rewrite featuring the npm install path)
- **Wave D:** GitHub template repo + Marketplace listing
- **Wave E:** PostHog dashboards (telemetry data is already flowing) + Evaluator-driven eval suite + Changesets release automation
- **Wave F:** Adoption push (Factory pilot, conference talks, multi-language docs)

## 📊 PostHog dashboard reminder

Telemetry is live and flowing to `azure-migration-squad` project in your `robertoborges` PostHog org. Build dashboards at https://us.posthog.com when you have time:

Recommended insights:
- Weekly installs (`cli.install`, breakdown by `$lib_version`)
- DAU/WAU/MAU (using `cli.command`)
- Command popularity (`cli.command`, breakdown by `command_name`)
- Squad-adoption funnel (`cli.install` → `cli.doctor` with squad_detected=true)
- OS/Node distribution
- Error rate (`cli.error`)
- Opt-out rate (`telemetry.disabled`)

Make one dashboard public and link from `docs/telemetry.md` for transparency (open question #2 from your earlier answers).

## 📦 Final file inventory

```
GHCP-PromptMigration/
├── package.json                                                  # NEW (monorepo root, workspaces)
├── packages/azure-migration-squad/
│   ├── package.json                                              # NEW (publishConfig.access=public)
│   ├── README.md                                                 # NEW
│   ├── CHANGELOG.md                                              # NEW (telemetry active)
│   ├── LICENSE                                                   # NEW (MIT)
│   ├── WAVE-A-HANDOFF.md                                         # THIS FILE
│   ├── bin/cli.js                                                # NEW (525 lines)
│   ├── lib/
│   │   ├── telemetry.js                                          # NEW (REAL PostHog key)
│   │   └── telemetry-consent.js                                  # NEW
│   ├── schemas/
│   │   ├── capability-matrix.schema.json                         # NEW
│   │   └── discovery-dossier.schema.json                         # NEW
│   ├── scripts/
│   │   ├── sync-from-root.mjs                                    # NEW
│   │   ├── clean-templates.mjs                                   # NEW
│   │   ├── validate-build.mjs                                    # NEW
│   │   └── lint.mjs                                              # NEW
│   ├── templates/                                                # build artifact
│   │   └── .gitkeep                                              # NEW
│   └── test/install.test.mjs                                     # NEW (7 tests, all passing)
└── .github/workflows/azure-migration-squad-ci.yml                # NEW

Live on npm: https://www.npmjs.com/package/@robertoborges/azure-migration-squad
```

Wave A is COMPLETE and PUBLISHED. 🎰💎


