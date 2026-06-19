---
"@robertoborges/azure-migration-squad": patch
---

CI hardening:

- **Source-of-truth guard now line-ending-agnostic** — `scripts/check-templates-not-edited.mjs` normalizes CRLF/LF for text files before hashing, so it no longer fails when `templates/` is committed from Windows but synced on Linux.
- **`.gitattributes` enforces LF** for all text files (PowerShell scripts kept as CRLF).
- **CI matrix reduced to ubuntu-latest + Node 20 only** — package is pure Node.js with no native deps; cross-OS matrix wasted ~83% of CI minutes per push. macOS/Windows can be smoke-tested manually before releases.
- **Squad eval no longer expects deprecated `Assess-*` prompts** at `.github/prompts/` — they were moved to `.github/prompts/legacy/` during the Universal Mode redesign. Eval now verifies the archive instead.
- **Squad eval no longer requires `Use-cases/README.md`** — walkthroughs live under `docs/walkthroughs/` and `docs/use-case-cheatsheets/`.
- **Prompt linter `model` and `tools` fields are now optional** — Copilot CLI prompts use `name` + `argument-hint` format, not VS Code chat format. Both formats are now accepted.
- Phase / portfolio / status prompts added to lint hook-reference exemption list (they reference hooks indirectly through the Migration-Orchestrator chatmode).
