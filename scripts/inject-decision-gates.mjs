/**
 * Insert/refresh the Decision Hardstop gate in the Phase 2-4 + database-migration skills.
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
 * v1 scope: Phase 2, 3, 4 + database-migration only (per Wave H scope).
 * Phase 5/6 follow in a later release.
 */

import { promises as fs, existsSync, readFileSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const skillsDir = path.resolve(__dirname, '..', '.github', 'skills');

// Relative link prefix used by the injected markdown. The host file lives at
// .github/skills/<dir>/SKILL.md, so `..` is .github/skills/.
const DECISION_REFS = '../migration-decisions/references';

// Map each skill to the catalog decisions it depends on. Keep in sync with
// .github/skills/migration-decisions/references/decision-catalog.md.
const SKILLS = [
  {
    dir: 'phase2-migrate-code',
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
    dir: 'phase3-generate-infra',
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
    dir: 'phase4-deploy-to-azure',
    phase: 'Phase 4 — Deploy to Azure',
    decisions: [
      { id: 'D-08', name: 'Region & data residency (confirm)' },
      { id: 'D-14', name: 'Cutover strategy' },
      { id: 'D-15', name: 'Acceptable downtime' },
    ],
  },
  {
    dir: 'database-migration',
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
    '### Check sequence (run this BEFORE anything else in this skill)',
    '',
    '1. Open `reports/Decisions-Required.md`.',
    '2. For each row in the table above, locate its section and read **Status**.',
    '3. Any decision still at `⏸ PENDING` → STOP. Do not proceed.',
    '4. Apply the **Decision Hardstop protocol** from `.github/skills/migration-decisions/references/decision-hardstop.md`:',
    '   - Post the 🛑 DECISION REQUIRED block in chat with options + tradeoffs from `.github/skills/migration-decisions/references/decision-catalog.md`.',
    '   - Wait for the user\'s reply (or for the file to be updated).',
    '   - Record the answer in `reports/Decision-Log.md`.',
    '   - Update Status to `✅ DECIDED <ISO date>` in `reports/Decisions-Required.md`.',
    '   - THEN re-run the check sequence.',
    '5. If `reports/Decisions-Required.md` is missing → STOP and route the user to `/phase1-plan`.',
    '',
    '### Hard rules',
    '',
    '- **Never assume.** Newer is not automatically better. "What most projects use" is not a decision.',
    '- **Never silently pick.** If a value is missing, ask. Don\'t infer.',
    '- **Never accept brief replies.** "Use SQL" is not enough — confirm engine, tier, region.',
    '- **Never bypass with an expert flag.** This protocol applies on every project.',
    '',
    `See [\`.github/skills/migration-decisions/references/decision-hardstop.md\`](${DECISION_REFS}/decision-hardstop.md) for the full protocol`,
    `and [\`.github/skills/migration-decisions/references/decision-catalog.md\`](${DECISION_REFS}/decision-catalog.md) for canonical option matrices.`,
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

// Leading YAML frontmatter. Tolerates a UTF-8 BOM, leading blank lines, CRLF,
// and a closing `---` at EOF with no trailing newline. `[ \t]*` (not `\s*`)
// after each `---` so the match never swallows the blank lines that follow.
const FRONTMATTER_RE = /^\uFEFF?(?:[ \t]*\r?\n)*---[ \t]*\r?\n[\s\S]*?\r?\n---[ \t]*(?:\r?\n|$)/;

/**
 * Split a markdown file into its YAML frontmatter block and the body that
 * follows it.
 *
 * The returned frontmatter is normalized to `<bom?>---\n…\n---\n` so repeated
 * runs are a fixed point. Frontmatter *content* is never rewritten — fields
 * such as `name:`, `user-invocable:` and `disable-model-invocation:` pass
 * through untouched.
 *
 * Returns `frontmatter: ''` ONLY when the file genuinely has no frontmatter
 * block. Callers MUST refuse to write in that case — splicing content above
 * the frontmatter silently breaks skill loading.
 */
function splitFrontmatter(content) {
  const m = content.match(FRONTMATTER_RE);
  if (!m) return { frontmatter: '', body: content };
  const bom = content.startsWith('\uFEFF') ? '\uFEFF' : '';
  const fm = bom + m[0].replace(/^\uFEFF?\s*/, '').replace(/\s*$/, '') + '\n';
  return { frontmatter: fm, body: content.slice(m[0].length).replace(/^\s*/, '') };
}

/**
 * Re-read a file after writing and fail loudly if the frontmatter no longer
 * survives. This is the backstop for the class of bug where an injected block
 * lands above the `---` block: a skill with no frontmatter silently fails to
 * load, so it must never escape this script.
 */
function assertFrontmatterIntact(fp, label) {
  const written = readFileSync(fp, 'utf-8').replace(/^\uFEFF/, '');
  if (!/^---[ \t]*\r?\n/.test(written)) {
    throw new Error(
      `${label} — FRONTMATTER GUARD FAILED: file no longer starts with '---'. ` +
        `Refusing to ship a skill that cannot load. First 80 chars: ${JSON.stringify(written.slice(0, 80))}`
    );
  }
  const { frontmatter } = splitFrontmatter(written);
  if (!frontmatter) {
    throw new Error(`${label} — FRONTMATTER GUARD FAILED: frontmatter block is not terminated by a closing '---'.`);
  }
  if (!/^name:[ \t]*\S/m.test(frontmatter)) {
    throw new Error(`${label} — FRONTMATTER GUARD FAILED: frontmatter has no 'name:' field.`);
  }
}

/**
 * Insert the decision gate AFTER the capability-matrix gate (if present),
 * otherwise directly after the frontmatter. This preserves the order:
 *   1. Frontmatter
 *   2. Capability matrix gate
 *   3. Decision hardstop gate         ← us
 *   4. Skill body
 *
 * Returns `null` when the file has no parseable frontmatter; the caller reports
 * it and skips the write rather than splicing above the `---` block.
 */
function injectGate(content, gateBlock) {
  // Remove any existing decision gate
  const stripped = content.replace(GATE_RE, '');

  const { frontmatter, body } = splitFrontmatter(stripped);
  if (!frontmatter) return null;

  const capIdx = body.indexOf(CAPABILITY_GATE_END);
  if (capIdx >= 0) {
    // Skip any trailing whitespace/newlines after the capability gate marker
    let insertAt = capIdx + CAPABILITY_GATE_END.length;
    while (
      insertAt < body.length &&
      (body[insertAt] === '\n' || body[insertAt] === '\r' || body[insertAt] === ' ')
    ) {
      insertAt++;
    }
    return frontmatter + '\n' + body.slice(0, insertAt) + gateBlock + '\n' + body.slice(insertAt);
  }

  // No capability gate present — insert directly after the frontmatter.
  return frontmatter + '\n' + gateBlock + (body ? '\n' + body : '');
}

let problems = 0;
let updated = 0;

for (const entry of SKILLS) {
  const label = `${entry.dir}/SKILL.md`;
  const fp = path.join(skillsDir, entry.dir, 'SKILL.md');
  if (!existsSync(fp)) {
    console.error(`✗ ${label} — missing`);
    problems++;
    continue;
  }
  const content = readFileSync(fp, 'utf-8');
  const gate = buildGate(entry.phase, entry.decisions);
  const next = injectGate(content, gate);
  if (next === null) {
    console.error(`✗ ${label} — no parseable YAML frontmatter; refusing to inject (would break skill loading)`);
    problems++;
    continue;
  }
  if (next !== content) {
    await fs.writeFile(fp, next);
    try {
      assertFrontmatterIntact(fp, label);
    } catch (err) {
      console.error(`✗ ${err.message}`);
      problems++;
      continue;
    }
    console.log(`✓ ${label} — decision gate injected/refreshed (${entry.decisions.length} decisions)`);
    updated++;
  } else {
    try {
      assertFrontmatterIntact(fp, label);
    } catch (err) {
      console.error(`✗ ${err.message}`);
      problems++;
      continue;
    }
    console.log(`= ${label} — decision gate already up to date`);
  }
}

console.log(`\n[inject-decision-gates] ${updated} file(s) updated; ${problems} problem(s).`);
if (problems > 0) process.exit(1);
