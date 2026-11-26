/**
 * Insert/refresh the Capability Matrix hard-gate preamble in all Phase + Database
 * Migration + Security Hardening + Cost Optimization skills.
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
const skillsDir = path.resolve(__dirname, '..', '.github', 'skills');

// Each skill: (dir, phase, requiresPlan) — `dir` is the folder under
// .github/skills/ and doubles as the user-invocable command slug.
// Phase 1 produces the Migration Plan, so it doesn't require it as a precondition.
// All other skills DO require it (or the /build-migration-plan add-on) to exist.
const SKILLS = [
  { dir: 'phase1-plan',               phase: 'Phase 1 — Plan',               requiresPlan: false },
  { dir: 'phase2-migrate-code',       phase: 'Phase 2 — Migrate Code',       requiresPlan: true  },
  { dir: 'phase3-generate-infra',     phase: 'Phase 3 — Generate Infra',     requiresPlan: true  },
  { dir: 'phase4-deploy-to-azure',    phase: 'Phase 4 — Deploy to Azure',    requiresPlan: true  },
  { dir: 'phase5-setup-cicd',         phase: 'Phase 5 — Setup CI/CD',        requiresPlan: true  },
  { dir: 'phase6-post-migration-ops', phase: 'Phase 6 — Post-Migration Ops', requiresPlan: true  },
  { dir: 'database-migration',        phase: 'Database Migration',           requiresPlan: true  },
  { dir: 'security-hardening',        phase: 'Security Hardening',           requiresPlan: true  },
  { dir: 'cost-optimization',         phase: 'Cost Optimization',            requiresPlan: true  },
];

const SENTINEL_START = '<!-- BEGIN: capability-matrix-gate (auto-managed by inject-capability-matrix-gates.mjs) -->';
const SENTINEL_END = '<!-- END: capability-matrix-gate -->';

function buildGate(phase, requiresPlan, slug) {
  const artifactRows = [
    '| Discovery Dossier | `reports/Discovery-Dossier.md` | **STOP** — run `/assess-any-application` first |',
    '| Capability Matrix | `reports/Capability-Matrix.yaml` | **STOP** — run `/assess-any-application` first |',
  ];
  if (requiresPlan) {
    artifactRows.push('| Approved Migration Plan | `reports/Migration-Plan.md` | **STOP** — run `/phase1-plan` (or the `/build-migration-plan` add-on) |');
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
        '  2. Then: /phase1-plan                            (produces the Migration Plan, or use /build-migration-plan add-on)',
        '  3. Then: /' + slug,
      ]
    : [
        '  1. Open Copilot Chat → /assess-any-application  (or in CLI: "assess this application")',
        '  2. Then re-run: /phase1-plan',
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
    'this skill with the `--accept-risk` natural-language flag in your request.',
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
    '2. **Skill Gap Check (belt + suspenders)** — for each value above, verify a matching `<family>-<value>.md` exists in `.github/skills/`. If any is missing, invoke `.github/skills/skill-creator/SKILL.md` to author it on the fly. Ask a single Y/n/N-for-session confirmation; default is Y.',
    requiresPlan
      ? '3. Read `reports/Migration-Plan.md` for approved sequencing and any app-specific extra gates.'
      : '3. If `reports/Migration-Plan.md` exists, read it for approved sequencing. Otherwise Phase 1 will produce it as part of its work.',
    '4. Confirm Phase prerequisites are met.',
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
 * Inject the gate AFTER the YAML frontmatter (which ends with `---`) but BEFORE
 * any other markdown body.
 *
 * Returns `null` when the file has no parseable frontmatter; the caller reports
 * it and skips the write rather than splicing above the `---` block.
 */
function injectGate(content, gateBlock) {
  // Remove any existing gate
  const stripped = content.replace(GATE_RE, '');

  const { frontmatter, body } = splitFrontmatter(stripped);
  if (!frontmatter) return null;

  return frontmatter + '\n' + gateBlock + (body ? '\n' + body : '');
}

let problems = 0;
let updated = 0;

for (const { dir, phase, requiresPlan } of SKILLS) {
  const label = `${dir}/SKILL.md`;
  const fp = path.join(skillsDir, dir, 'SKILL.md');
  if (!existsSync(fp)) {
    console.error(`✗ ${label} — missing`);
    problems++;
    continue;
  }
  const content = readFileSync(fp, 'utf-8');
  const gate = buildGate(phase, requiresPlan, dir);
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
    console.log(`✓ ${label} — gate injected/refreshed`);
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

console.log(`\n[inject-capability-matrix-gates] ${updated} file(s) updated; ${problems} problem(s).`);
if (problems > 0) process.exit(1);
