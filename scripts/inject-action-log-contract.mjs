/**
 * Insert/refresh the Action Log Contract preamble in every prompt.
 *
 * Run via: node scripts/inject-action-log-contract.mjs
 *
 * Idempotent: re-running produces the same output. Recognizes the existing
 * contract block by its sentinel markers and replaces in place.
 *
 * The contract tells the agent, at the top of every prompt, that after each
 * meaningful action it must append a single line to `## 📜 Action Log` in
 * `reports/Report-Status.md`. Full spec at .github/skills/action-log-format.md.
 */

import { promises as fs, existsSync, readFileSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const promptsDir = path.resolve(__dirname, '..', '.github', 'prompts');

// Every prompt in the main path + add-ons gets the contract.
// Legacy prompts (.github/prompts/legacy/) are excluded — they're deprecated.
const PROMPTS = [
  // Main path
  { file: 'Assess-Any-Application.prompt.md',     actor: 'Assess-Any-Application' },
  { file: 'Phase1-Plan.prompt.md',                actor: 'Phase1-Plan' },
  { file: 'Phase2-MigrateCode.prompt.md',         actor: 'Phase2-MigrateCode' },
  { file: 'Phase3-GenerateInfra.prompt.md',       actor: 'Phase3-GenerateInfra' },
  { file: 'Phase4-DeployToAzure.prompt.md',       actor: 'Phase4-DeployToAzure' },
  { file: 'Phase5-SetupCICD.prompt.md',           actor: 'Phase5-SetupCICD' },
  { file: 'Phase6-PostMigrationOps.prompt.md',    actor: 'Phase6-PostMigrationOps' },
  // Add-ons
  { file: 'Build-Migration-Plan.prompt.md',       actor: 'Build-Migration-Plan' },
  { file: 'DatabaseMigration.prompt.md',          actor: 'DatabaseMigration' },
  { file: 'SecurityHardening.prompt.md',          actor: 'SecurityHardening' },
  { file: 'CostOptimization.prompt.md',           actor: 'CostOptimization' },
  { file: 'PortfolioStrategy.prompt.md',          actor: 'PortfolioStrategy' },
  { file: 'Phase0-Multi-repo-assessment.prompt.md', actor: 'Phase0-Multi-repo-assessment' },
  { file: 'Phase-Rollback.prompt.md',             actor: 'Phase-Rollback' },
  { file: 'GetStatus.prompt.md',                  actor: 'GetStatus' },
  { file: 'QuickAssessment.prompt.md',            actor: 'QuickAssessment' },
  { file: 'QuickTriage.prompt.md',                actor: 'QuickTriage' },
  { file: 'InteractiveMigrationInterview.prompt.md', actor: 'InteractiveMigrationInterview' },
  { file: 'TeamSkillAssessment.prompt.md',        actor: 'TeamSkillAssessment' },
];

const SENTINEL_START = '<!-- BEGIN: action-log-contract (auto-managed by inject-action-log-contract.mjs) -->';
const SENTINEL_END = '<!-- END: action-log-contract -->';

function buildContract(actor) {
  return [
    SENTINEL_START,
    '',
    '## 📜 Action Log Contract',
    '',
    `**After each meaningful action** in this prompt, append one single-line entry to the \`## 📜 Action Log\` section at the bottom of \`reports/Report-Status.md\`.`,
    '',
    'Canonical format:',
    '```',
    `- <ISO-8601-UTC> | actor=${actor} | action=<verb-phrase> | files=<+created,~modified,-deleted> | tokens=~<bucket> | turn=<n> | notes="<free text>"`,
    '```',
    '',
    'Rules:',
    `- Use \`actor=${actor}\` for actions taken by this prompt.`,
    '- Use `actor=User` for actions taken by the user (e.g., answering a decision).',
    '- Log **only meaningful actions**: phase transitions, artifact production, decision events, gate passes/blocks, user inputs, rollback events. Do NOT log every internal grep or file read.',
    '- Estimate `tokens` in buckets: `~0`, `~500`, `~2k`, `~8k`, `~30k`. The `turn` counter is exact; token estimate is best-effort. Point users to Copilot Dashboard for authoritative counts.',
    '- If `reports/Report-Status.md` doesn\'t exist yet, create it from `.github/skills/migration-report-template.md` first — it already includes the `## 📜 Action Log` section.',
    '',
    'Full spec: `.github/skills/action-log-format.md`.',
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

// Recognize the capability-matrix-gate block so we can insert the contract AFTER it.
const CAP_GATE_START = '<!-- BEGIN: capability-matrix-gate (auto-managed by inject-capability-matrix-gates.mjs) -->';
const CAP_GATE_END = '<!-- END: capability-matrix-gate -->';
const CAP_GATE_RE = new RegExp(
  `${escapeRegex(CAP_GATE_START)}[\\s\\S]*?${escapeRegex(CAP_GATE_END)}`,
  'g'
);

/**
 * Inject the Action Log Contract AFTER the YAML frontmatter AND AFTER the
 * capability-matrix-gate block (if present), so the two contracts sit
 * consecutively at the top of the prompt body.
 */
function injectContract(content, contractBlock) {
  // Remove any existing contract
  const stripped = content.replace(CONTRACT_RE, '');

  // Find frontmatter boundary
  const fmMatch = stripped.match(/^(---\s*\r?\n[\s\S]*?\r?\n---\s*\r?\n)/);
  const fm = fmMatch ? fmMatch[1] : '';
  const afterFm = stripped.slice(fm.length);

  // Find capability-matrix-gate boundary (if it exists in the body)
  const capMatch = afterFm.match(CAP_GATE_RE);
  if (capMatch) {
    const gateBlock = capMatch[0];
    const gateEnd = afterFm.indexOf(gateBlock) + gateBlock.length;
    const beforeAfterGate = afterFm.slice(0, gateEnd);
    const restAfterGate = afterFm.slice(gateEnd).replace(/^\s*/, '\n\n');
    return fm + beforeAfterGate + '\n\n' + contractBlock + restAfterGate;
  }

  // No capability-matrix-gate — insert directly after frontmatter
  return fm + '\n' + contractBlock + afterFm;
}

let problems = 0;
let updated = 0;

for (const { file, actor } of PROMPTS) {
  const fp = path.join(promptsDir, file);
  if (!existsSync(fp)) {
    console.error(`✗ ${file} — missing`);
    problems++;
    continue;
  }
  const content = readFileSync(fp, 'utf-8');
  const contract = buildContract(actor);
  const next = injectContract(content, contract);
  if (next !== content) {
    await fs.writeFile(fp, next);
    console.log(`✓ ${file} — action-log contract injected/refreshed`);
    updated++;
  } else {
    console.log(`= ${file} — already up to date`);
  }
}

console.log(`\n[inject-action-log-contract] ${updated} file(s) updated; ${problems} problem(s).`);
if (problems > 0) process.exit(1);
