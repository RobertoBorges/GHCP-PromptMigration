/**
 * Insert/refresh the Capability Matrix hard-gate preamble in all Phase + Database
 * Migration + Security Hardening + Cost Optimization prompts.
 *
 * Run via: node scripts/inject-capability-matrix-gates.mjs
 *
 * Idempotent: re-running produces the same output. Recognizes the existing gate
 * block by its sentinel markers and replaces in place.
 */

import { promises as fs, existsSync, readFileSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const promptsDir = path.resolve(__dirname, '..', '.github', 'prompts');

// Each prompt: (file, niceName, requiresPlan) — phase number for messaging
// Phase 1 produces the Migration Plan, so it doesn't require it as a precondition.
// All other prompts DO require it (or the /build-migration-plan add-on) to exist.
const PROMPTS = [
  { file: 'Phase1-Plan.prompt.md',                phase: 'Phase 1 — Plan',              requiresPlan: false },
  { file: 'Phase2-MigrateCode.prompt.md',         phase: 'Phase 2 — Migrate Code',      requiresPlan: true  },
  { file: 'Phase3-GenerateInfra.prompt.md',       phase: 'Phase 3 — Generate Infra',    requiresPlan: true  },
  { file: 'Phase4-DeployToAzure.prompt.md',       phase: 'Phase 4 — Deploy to Azure',   requiresPlan: true  },
  { file: 'Phase5-SetupCICD.prompt.md',           phase: 'Phase 5 — Setup CI/CD',       requiresPlan: true  },
  { file: 'Phase6-PostMigrationOps.prompt.md',    phase: 'Phase 6 — Post-Migration Ops', requiresPlan: true },
  { file: 'DatabaseMigration.prompt.md',          phase: 'Database Migration',          requiresPlan: true  },
  { file: 'SecurityHardening.prompt.md',          phase: 'Security Hardening',          requiresPlan: true  },
  { file: 'CostOptimization.prompt.md',           phase: 'Cost Optimization',           requiresPlan: true  },
];

const SENTINEL_START = '<!-- BEGIN: capability-matrix-gate (auto-managed by inject-capability-matrix-gates.mjs) -->';
const SENTINEL_END = '<!-- END: capability-matrix-gate -->';

function buildGate(phase, requiresPlan) {
  const artifactRows = [
    '| Discovery Dossier | `reports/Discovery-Dossier.md` | **STOP** — run `/assess-any-application` first |',
    '| Capability Matrix | `reports/Capability-Matrix.yaml` | **STOP** — run `/assess-any-application` first |',
  ];
  if (requiresPlan) {
    artifactRows.push('| Approved Migration Plan | `reports/Migration-Plan.md` | **STOP** — run `/Phase1-Plan` (or the `/build-migration-plan` add-on) |');
  }

  const missingLines = [
    '  - reports/Discovery-Dossier.md          [missing/present]',
    '  - reports/Capability-Matrix.yaml         [missing/present]',
  ];
  if (requiresPlan) {
    missingLines.push('  - reports/Migration-Plan.md              [missing/present]');
  }

  const requiredSteps = requiresPlan
    ? [
        '  1. Open Copilot Chat → /assess-any-application  (or in CLI: "assess this application")',
        '  2. Then: /Phase1-Plan                            (produces the Migration Plan, or use /build-migration-plan add-on)',
        '  3. Then: /' + phase.split(' ')[0].toLowerCase() + '...',
      ]
    : [
        '  1. Open Copilot Chat → /assess-any-application  (or in CLI: "assess this application")',
        '  2. Then re-run: /Phase1-Plan',
      ];

  const passRequirements = requiresPlan ? 'All three artifacts exist' : 'Both artifacts exist';
  const missingCondition = requiresPlan ? 'ANY of those three artifacts' : 'EITHER of those two artifacts';
  const noteBlock = requiresPlan
    ? ''
    : '\n> **Note:** `reports/Migration-Plan.md` is **produced by Phase 1**. If it doesn\'t exist yet, Phase 1 will generate it. If you\'d like to produce it separately first, use the `/build-migration-plan` add-on.\n';

  const gate = [
    SENTINEL_START,
    '',
    `## 🚦 MANDATORY OPENING CHECK — Capability Matrix Required`,
    '',
    `**Before doing ANY work for ${phase}, verify the Discovery contract:**`,
    '',
    '| Required artifact | Location | If missing |',
    '|-------------------|----------|------------|',
    ...artifactRows,
    noteBlock,
    `### If ${missingCondition} is missing`,
    '',
    'Reply with exactly:',
    '',
    '```',
    `🚨 ${phase} cannot proceed without the Discovery contract.`,
    '',
    'Missing artifacts:',
    ...missingLines,
    '',
    'Required steps before re-running this phase:',
    ...requiredSteps,
    '',
    'To override (skip Discovery and accept risk), log a waiver entry in',
    'reports/Decision-Log.md with `Waiver: skip-discovery=<reason>` and re-invoke',
    'this prompt with the `--accept-risk` natural-language flag in your request.',
    '```',
    '',
    '**Do NOT proceed past this gate unless:**',
    `- ${passRequirements}, OR`,
    '- A waiver entry exists in `reports/Decision-Log.md` AND the user explicitly said "skip discovery" or similar',
    '',
    '### When the gate passes',
    '',
    '1. Read `reports/Capability-Matrix.yaml` and extract these fields you must honor:',
    '   - `source.primary_adapter` → load the matching `source-*` skill',
    '   - `stack.primary_stack` + `stack.secondary_stacks` → load matching `stack-*` skills',
    '   - `workload.primary_pattern` → load matching `workload-*` skill',
    '   - `migration_strategy.recommendation` → adjust phase emphasis based on the recommended strategy',
    '   - `risk_flags` → load the matching risk skills (e.g., `risk-cross-region-data.md`)',
    '   - `unresolved_questions` → if any remain unanswered, surface them BEFORE starting work',
    requiresPlan
      ? '2. Read `reports/Migration-Plan.md` for approved sequencing and any app-specific extra gates.'
      : '2. If `reports/Migration-Plan.md` exists, read it for approved sequencing. Otherwise Phase 1 will produce it as part of its work.',
    '3. Confirm Phase prerequisites are met.',
    '',
    SENTINEL_END,
    '',
  ].filter((line) => line !== undefined).join('\n');

  return gate;
}

function escapeRegex(s) {
  return s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

const GATE_RE = new RegExp(
  `${escapeRegex(SENTINEL_START)}[\\s\\S]*?${escapeRegex(SENTINEL_END)}\\s*`,
  'g'
);

/**
 * Inject the gate AFTER the YAML frontmatter (which ends with `---`) but BEFORE
 * any other markdown body.
 */
function injectGate(content, gateBlock) {
  // Remove any existing gate
  const stripped = content.replace(GATE_RE, '');

  // Split off frontmatter
  const fmMatch = stripped.match(/^(---\s*\r?\n[\s\S]*?\r?\n---\s*\r?\n)/);
  if (fmMatch) {
    const fm = fmMatch[1];
    const rest = stripped.slice(fm.length);
    return fm + '\n' + gateBlock + rest;
  }
  // No frontmatter — just prepend
  return gateBlock + stripped;
}

let problems = 0;
let updated = 0;

for (const { file, phase, requiresPlan } of PROMPTS) {
  const fp = path.join(promptsDir, file);
  if (!existsSync(fp)) {
    console.error(`✗ ${file} — missing`);
    problems++;
    continue;
  }
  const content = readFileSync(fp, 'utf-8');
  const gate = buildGate(phase, requiresPlan);
  const next = injectGate(content, gate);
  if (next !== content) {
    await fs.writeFile(fp, next);
    console.log(`✓ ${file} — gate injected/refreshed`);
    updated++;
  } else {
    console.log(`= ${file} — already up to date`);
  }
}

console.log(`\n[inject-capability-matrix-gates] ${updated} file(s) updated; ${problems} problem(s).`);
if (problems > 0) process.exit(1);
