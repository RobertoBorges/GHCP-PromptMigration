---
"azure-migration-squad-vscode": minor
---

**v0.1.3: Wave H surface — Decisions Required tree view + status bar**

Surfaces the Wave H Decision Hardstop Protocol in the VS Code UI.

- **New "🛑 Decisions Required" tree view** at the top of the AMS sidebar. Shows each major architecture decision from `reports/Decisions-Required.md` with status icons (⏸ pending / ✅ decided / 🔒 locked / 🚫 N/A). Click any entry → file opens scrolled to that section.
- **Status bar shows pending decision count.** When any decision is pending, the AMS status bar widget switches to "🛑 AMS: 3/18 decisions pending" with a warning-colored background. Click → opens the file. Once all decisions are made, reverts to normal phase indicator.
- **Auto-refresh** when `reports/Decisions-Required.md` is created or modified.
- **2 new Command Palette commands** — Show decisions required (opens file), Open decision at line (internal).
- **8 new unit tests** for the markdown parser.

Bundle: 91 KB minified, .vsix 23.46 KB.
Tests: 17/17 passing.
