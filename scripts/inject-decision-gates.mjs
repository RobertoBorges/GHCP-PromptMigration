/**
 * Insert/refresh the Decision Hardstop gate in Phase 2-4 + DatabaseMigration prompts.
 *
 * Each phase has a specific subset of catalog decisions it depends on. The gate
 * lists those decisions, points to the canonical artifact (reports/Decisions-Required.md),
 * and tells the agent to STOP if any are still PENDING.
 *
 * Run via: node scripts/inject-decision-gates.mjs
 *
 * Idempotent: re-running produces the same output. Recognizes the existing gate
 * block by its sentinel markers and replaces in place. Inserts AFTER the capability-
 * matrix gate so both checks run in order.
 *
 * v1 scope: Phase 2, 3, 4 + DatabaseMigration only (per Wave H scope).
 * Phase 5/6 follow in a later release.
 */

import { promises as fs, existsSync, readFileSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const promptsDir = path.resolve(__dirname, '..', '.github', 'prompts');

// Map each prompt to the catalog decisions it depends on. Keep in sync with
// .github/skills/decision-catalog.md.
const PROMPTS = [
  {
    file: 'Phase2-MigrateCode.prompt.md',
    phase: 'Phase 2 — Migrate Code',
    decisions: [
      { id: 'D-01', name: 'Target framework / runtime version' },
      { id: 'D-02', name: 'UI architecture' },
      { id: 'D-03', name: 'Backend / API style', condition: 'only when migration.strategy is rearchitect or rebuild' },
      { id: 'D-04', name: 'Database engine' },
      { id: 'D-09', name: 'Authentication' },
    ],
  },
  {
    file: 'Phase3-GenerateInfra.prompt.md',
    phase: 'Phase 3 — Generate Infra',
    decisions: [
      { id: 'D-06', name: 'Hosting platform' },
      { id: 'D-07', name: 'IaC tool' },
      { id: 'D-08', name: 'Region & data residency' },
      { id: 'D-10', name: 'Multi-tenancy approach', condition: 'only if app is multi-tenant' },
      { id: 'D-12', name: 'Cost ceiling' },
      { id: 'D-13', name: 'DR — RPO / RTO targets' },
      { id: 'D-18', name: 'Container registry', condition: 'only if hosting is container-based' },
    ],
  },
  {
    file: 'Phase4-DeployToAzure.prompt.md',
    phase: 'Phase 4 — Deploy to Azure',
    decisions: [
      { id: 'D-08', name: 'Region & data residency (confirm)' },
      { id: 'D-14', name: 'Cutover strategy' },
      { id: 'D-15', name: 'Acceptable downtime' },
    ],
  },
  {
    file: 'DatabaseMigration.prompt.md',
    phase: 'Database Migration',
    decisions: [
      { id: 'D-04', name: 'Database engine' },
      { id: 'D-05', name: 'Database migration tool' },
      { id: 'D-15', name: 'Acceptable downtime' },
    ],
  },
];

const SENTINEL_START = '<!-- BEGIN: decision-hardstop-gate (auto-managed by inject-decision-gates.mjs) -->';
const SENTINEL_END = '<!-- END: decision-hardstop-gate -->';

function buildGate(phase, decisions) {
  const rows = decisions
    .map((d) => {
      const cond = d.condition ? ` _(${d.condition})_` : '';
      return `| ${d.id} | ${d.name}${cond} | ✅ DECIDED (or 🚫 N/A) |`;
    })
    .join('\n');

  return [
    SENTINEL_START,
    '',
    `## 🛑 MANDATORY DECISION GATE — Major decisions required for ${phase}`,
    '',
    'The Code Migration Modernization Agent does **not** decide major architecture on your behalf.',
    `Before ${phase} can do any work, every decision below must be **DECIDED** in`,
    '`reports/Decisions-Required.md` (or marked **🚫 N/A** if genuinely not applicable).',
    '',
    '| Catalog ID | Decision | Required status |',
    '|-----------|----------|-----------------|',
    rows,
    '',
    '### Check sequence (run this BEFORE anything else in this prompt)',
    '',
    '1. Open `reports/Decisions-Required.md`.',
    '2. For each row in the table above, locate its section and read **Status**.',
    '3. Any decision still at `⏸ PENDING` → STOP. Do not proceed.',
    '4. Apply the **Decision Hardstop protocol** from `.github/skills/decision-hardstop.md`:',
    '   - Post the 🛑 DECISION REQUIRED block in chat with options + tradeoffs from `.github/skills/decision-catalog.md`.',
    '   - Wait for the user\'s reply (or for the file to be updated).',
    '   - Record the answer in `reports/Decision-Log.md`.',
    '   - Update Status to `✅ DECIDED <ISO date>` in `reports/Decisions-Required.md`.',
    '   - THEN re-run the check sequence.',
    '5. If `reports/Decisions-Required.md` is missing → STOP and route the user to `/Phase1-Plan`.',
    '',
    '### Hard rules',
    '',
    '- **Never assume.** Newer is not automatically better. "What most projects use" is not a decision.',
    '- **Never silently pick.** If a value is missing, ask. Don\'t infer.',
    '- **Never accept brief replies.** "Use SQL" is not enough — confirm engine, tier, region.',
    '- **Never bypass with an expert flag.** This protocol applies on every project.',
    '',
    'See [`.github/skills/decision-hardstop.md`](../skills/decision-hardstop.md) for the full protocol',
    'and [`.github/skills/decision-catalog.md`](../skills/decision-catalog.md) for canonical option matrices.',
    '',
    SENTINEL_END,
    '',
  ].join('\n');
}

function escapeRegex(s) {
  return s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

const GATE_RE = new RegExp(
  `${escapeRegex(SENTINEL_START)}[\\s\\S]*?${escapeRegex(SENTINEL_END)}\\s*`,
  'g'
);

const CAPABILITY_GATE_END = '<!-- END: capability-matrix-gate -->';

/**
 * Insert the decision gate AFTER the capability-matrix gate (if present),
 * otherwise after frontmatter. This preserves the order:
 *   1. Frontmatter
 *   2. Capability matrix gate
 *   3. Decision hardstop gate         ← us
 *   4. Phase body
 */
function injectGate(content, gateBlock) {
  // Remove any existing decision gate
  const stripped = content.replace(GATE_RE, '');

  const capIdx = stripped.indexOf(CAPABILITY_GATE_END);
  if (capIdx >= 0) {
    // Find end of capability gate (including trailing newlines)
    const after = capIdx + CAPABILITY_GATE_END.length;
    // Skip any trailing whitespace/newlines after the capability gate marker
    let insertAt = after;
    while (
      insertAt < stripped.length &&
      (stripped[insertAt] === '\n' || stripped[insertAt] === '\r' || stripped[insertAt] === ' ')
    ) {
      insertAt++;
    }
    return stripped.slice(0, insertAt) + gateBlock + '\n' + stripped.slice(insertAt);
  }

  // No capability gate present — fall back to inserting after frontmatter
  const fmMatch = stripped.match(/^(---\s*\r?\n[\s\S]*?\r?\n---\s*\r?\n)/);
  if (fmMatch) {
    const fm = fmMatch[1];
    const rest = stripped.slice(fm.length);
    return fm + '\n' + gateBlock + rest;
  }

  // No frontmatter either — just prepend
  return gateBlock + stripped;
}

let problems = 0;
let updated = 0;

for (const entry of PROMPTS) {
  const fp = path.join(promptsDir, entry.file);
  if (!existsSync(fp)) {
    console.error(`✗ ${entry.file} — missing`);
    problems++;
    continue;
  }
  const content = readFileSync(fp, 'utf-8');
  const gate = buildGate(entry.phase, entry.decisions);
  const next = injectGate(content, gate);
  if (next !== content) {
    await fs.writeFile(fp, next);
    console.log(`✓ ${entry.file} — decision gate injected/refreshed (${entry.decisions.length} decisions)`);
    updated++;
  } else {
    console.log(`= ${entry.file} — decision gate already up to date`);
  }
}

console.log(`\n[inject-decision-gates] ${updated} file(s) updated; ${problems} problem(s).`);
if (problems > 0) process.exit(1);
