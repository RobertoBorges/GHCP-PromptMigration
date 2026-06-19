# Changelog

All notable changes to the Azure Migration Squad VS Code extension are documented here.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] — Phase 2 scaffold

Initial release. Establishes the extension package and activation framework so subsequent phases (tree view, status bar, commands, welcome panel) can ship incrementally.

### Added
- Extension activates on VS Code startup
- One smoke-test command: `Azure Migration: Hello (smoke test)` — proves the extension loads
- Headless test runner via `@vscode/test-electron`
- esbuild bundling to `dist/extension.js` (CJS, Node 20 target)
- Marketplace listing (README + icon TBD)

### Known limitations (intentional — added in upcoming phases)
- No tree view yet (Phase 3)
- No Command Palette commands beyond `hello` (Phase 3)
- No status bar widget (Phase 4)
- No settings UI (Phase 4)
- No first-run welcome (Phase 5)
- No marketplace icon yet (Phase 6)
- For real migration work, use the [`@robertoborges/azure-migration-squad`](https://www.npmjs.com/package/@robertoborges/azure-migration-squad) CLI directly today

### Notes
- Built as part of **Wave G** — VS Code adoption push for the Azure Migration Squad
- Companion to the npm package; same SemVer line eventually
