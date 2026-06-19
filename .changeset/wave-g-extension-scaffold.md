---
"azure-migration-squad-vscode": minor
---

**Phase 2 scaffold: VS Code extension package shipped (scaffold only)**

New monorepo package `packages/azure-migration-squad-vscode/` — a real VS Code extension that will eventually surface the full Azure Migration Squad as a native VS Code experience.

This release establishes the foundation:

- TypeScript + esbuild build (bundles to `dist/extension.js`, CJS, Node 20 target)
- One smoke-test command: `Azure Migration: Hello (smoke test)`
- `@vscode/test-electron` headless test runner with 4 activation tests (all green)
- `.vsix` packaging via `@vscode/vsce`
- Placeholder 128×128 icon (AMS on Azure blue) — will be replaced before marketplace launch
- CI: builds + packages + tests the extension on every push, uploads .vsix as artifact
- MIT licensed, marketplace listing draft in README.md, CHANGELOG with full roadmap

**Out of scope for this release** (coming in Phases 3-5):

- Sidebar tree view of agents/prompts/skills (Phase 3)
- Command Palette commands beyond `hello` (Phase 3)
- Status bar widget showing migration phase (Phase 4)
- Settings UI (Phase 4)
- First-run welcome WebView + walkthrough (Phase 5)
- Marketplace publishing automation (Phase 6)

For real migration work today, use the [`@robertoborges/azure-migration-squad`](https://www.npmjs.com/package/@robertoborges/azure-migration-squad) CLI directly.
