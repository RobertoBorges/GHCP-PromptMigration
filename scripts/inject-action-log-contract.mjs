/**
 * Insert/refresh the Action Log Contract preamble in every workflow skill.
 *
 * Run via: node scripts/inject-action-log-contract.mjs
 *
 * Idempotent: re-running produces the same output. Recognizes the existing
 * contract block by its sentinel markers and replaces in place.
 *
 * The contract tells the agent, at the top of every workflow skill, that after
 * each meaningful action it must append a single line to `## 📜 Action Log` in
 * `reports/Report-Status.md`. Full spec at .github/skills/migration-artifacts/references/action-log-format.md.
 */

import { promises as fs, existsSync, readFileSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const skillsDir = path.resolve(__dirname, '..', '.github', 'skills');

// Every workflow skill in the main path + add-ons gets the contract.
// `dir` is the skill folder under .github/skills/; the body always lives at
// <dir>/SKILL.md. `actor` is the Action Log actor token — keep these in sync
// with .github/skills/migration-artifacts/references/action-log-format.md.
const SKILLS = [
  // Main path
  { dir: 'assess-any-application',          actor: 'Assess-Any-Application' },
  { dir: 'phase1-plan',                     actor: 'Phase1-Plan' },
  { dir: 'phase2-migrate-code',             actor: 'Phase2-MigrateCode' },
  { dir: 'phase3-generate-infra',           actor: 'Phase3-GenerateInfra' },
  { dir: 'phase4-deploy-to-azure',          actor: 'Phase4-DeployToAzure' },
  { dir: 'phase5-setup-cicd',               actor: 'Phase5-SetupCICD' },
  { dir: 'phase6-post-migration-ops',       actor: 'Phase6-PostMigrationOps' },
  // Add-ons
  { dir: 'build-migration-plan',            actor: 'Build-Migration-Plan' },
  { dir: 'database-migration',              actor: 'DatabaseMigration' },
  { dir: 'security-hardening',              actor: 'SecurityHardening' },
  { dir: 'cost-optimization',               actor: 'CostOptimization' },
  { dir: 'portfolio-strategy',              actor: 'PortfolioStrategy' },
  { dir: 'phase0-multi-repo-assessment',    actor: 'Phase0-Multi-repo-assessment' },
  { dir: 'phase-rollback',                  actor: 'Phase-Rollback' },
  { dir: 'get-status',                      actor: 'GetStatus' },
  { dir: 'quick-assessment',                actor: 'QuickAssessment' },
  { dir: 'quick-triage',                    actor: 'QuickTriage' },
  { dir: 'interactive-migration-interview', actor: 'InteractiveMigrationInterview' },
  { dir: 'team-skill-assessment',           actor: 'TeamSkillAssessment' },
];

const SENTINEL_START = '<!-- BEGIN: action-log-contract (auto-managed by inject-action-log-contract.mjs) -->';
const SENTINEL_END = '<!-- END: action-log-contract -->';

function buildContract(actor) {
  return [
    SENTINEL_START,
    '',
    '## 📜 Action Log Contract',
    '',
    `**After each meaningful action** in this skill, append one single-line entry to the \`## 📜 Action Log\` section at the bottom of \`reports/Report-Status.md\`.`,
    '',
    'Canonical format:',
    '```',
    `- <ISO-8601-UTC> | actor=${actor} | action=<verb-phrase> | files=<+created,~modified,-deleted> | tokens=~<bucket> | turn=<n> | notes="<free text>"`,
    '```',
    '',
    'Rules:',
    `- Use \`actor=${actor}\` for actions taken by this skill.`,
    '- Use `actor=User` for actions taken by the user (e.g., answering a decision).',
    '- Log **only meaningful actions**: phase transitions, artifact production, decision events, gate passes/blocks, user inputs, rollback events. Do NOT log every internal grep or file read.',
    '- Estimate `tokens` in buckets: `~0`, `~500`, `~2k`, `~8k`, `~30k`. The `turn` counter is exact; token estimate is best-effort. Point users to Copilot Dashboard for authoritative counts.',
    '- If `reports/Report-Status.md` doesn\'t exist yet, create it from `.github/skills/migration-artifacts/references/migration-report-template.md` first — it already includes the `## 📜 Action Log` section.',
    '',
    'Full spec: `.github/skills/migration-artifacts/references/action-log-format.md`.',
    '',
    SENTINEL_END,
    '',
  ].join('\n');
}

function escapeRegex(s) {
  return s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

const CONTRACT_RE = new RegExp(
  `${escapeRegex(SENTINEL_START)}[\\s\\S]*?${escapeRegex(SENTINEL_END)}\\s*`,
  'g'
);

// Recognize the auto-managed gate blocks so we can insert the contract AFTER them.
const CAP_GATE_START = '<!-- BEGIN: capability-matrix-gate (auto-managed by inject-capability-matrix-gates.mjs) -->';
const CAP_GATE_END = '<!-- END: capability-matrix-gate -->';
const CAP_GATE_RE = new RegExp(
  `${escapeRegex(CAP_GATE_START)}[\\s\\S]*?${escapeRegex(CAP_GATE_END)}`,
  'g'
);

const DECISION_GATE_START = '<!-- BEGIN: decision-hardstop-gate (auto-managed by inject-decision-gates.mjs) -->';
const DECISION_GATE_END = '<!-- END: decision-hardstop-gate -->';
const DECISION_GATE_RE = new RegExp(
  `${escapeRegex(DECISION_GATE_START)}[\\s\\S]*?${escapeRegex(DECISION_GATE_END)}`,
  'g'
);

// Leading YAML frontmatter. Tolerates a UTF-8 BOM, leading blank lines, CRLF,
// and a closing `---` at EOF with no trailing newline. `[ \t]*` (not `\s*`)
// after each `---` so the match never swallows the blank lines that follow.
const FRONTMATTER_RE = /^\uFEFF?(?:[ \t]*\r?\n)*---[ \t]*\r?\n[\s\S]*?\r?\n---[ \t]*(?:\r?\n|$)/;

/**
 * Split a markdown file into its YAML frontmatter block and the body that
 * follows it.
 *
 * Deliberately tolerant: accepts a UTF-8 BOM, leading blank lines, CRLF, and a
 * closing `---` that sits at EOF with no trailing newline. The returned
 * frontmatter is normalized to `<bom?>---\n…\n---\n` so repeated runs are a
 * fixed point. Frontmatter *content* is never rewritten — fields such as
 * `name:`, `user-invocable:` and `disable-model-invocation:` pass through
 * untouched.
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
 * Inject the Action Log Contract AFTER the YAML frontmatter AND AFTER every
 * auto-managed gate block (capability-matrix gate, decision-hardstop gate), so
 * the preambles sit consecutively at the top of the skill body in a stable
 * order: capability gate → decision gate → action-log contract.
 *
 * Anchoring on the LAST gate keeps this script idempotent no matter what order
 * the three injectors run in — inject-decision-gates.mjs always re-inserts its
 * block immediately after the capability gate, i.e. before this one.
 *
 * Returns `null` when the file has no parseable frontmatter; the caller reports
 * it and skips the write rather than splicing above the `---` block.
 */
function injectContract(content, contractBlock) {
  // Remove any existing contract
  const stripped = content.replace(CONTRACT_RE, '');

  const { frontmatter, body } = splitFrontmatter(stripped);
  if (!frontmatter) return null;

  // Find the end of the last gate block (if any exist in the body)
  let gateEnd = -1;
  for (const re of [CAP_GATE_RE, DECISION_GATE_RE]) {
    re.lastIndex = 0;
    const m = re.exec(body);
    if (m) gateEnd = Math.max(gateEnd, m.index + m[0].length);
  }
  if (gateEnd >= 0) {
    const beforeAfterGate = body.slice(0, gateEnd);
    const restAfterGate = body.slice(gateEnd).replace(/^\s*/, '\n\n');
    return frontmatter + '\n' + beforeAfterGate + '\n\n' + contractBlock + restAfterGate;
  }

  // No gate blocks — insert directly after the frontmatter
  return frontmatter + '\n' + contractBlock + '\n' + body;
}

let problems = 0;
let updated = 0;

for (const { dir, actor } of SKILLS) {
  const label = `${dir}/SKILL.md`;
  const fp = path.join(skillsDir, dir, 'SKILL.md');
  if (!existsSync(fp)) {
    console.error(`✗ ${label} — missing`);
    problems++;
    continue;
  }
  const content = readFileSync(fp, 'utf-8');
  const contract = buildContract(actor);
  const next = injectContract(content, contract);
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
    console.log(`✓ ${label} — action-log contract injected/refreshed`);
    updated++;
  } else {
    try {
      assertFrontmatterIntact(fp, label);
    } catch (err) {
      console.error(`✗ ${err.message}`);
      problems++;
      continue;
    }
    console.log(`= ${label} — already up to date`);
  }
}

console.log(`\n[inject-action-log-contract] ${updated} file(s) updated; ${problems} problem(s).`);
if (problems > 0) process.exit(1);
