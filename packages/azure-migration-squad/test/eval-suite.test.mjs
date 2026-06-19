/**
 * Evaluator-driven prompt evaluation suite.
 *
 * Goal: catch regressions in prompt content/structure BEFORE they ship.
 * Runs in CI on every PR. Fails the build when any fixture's expected
 * properties don't hold against the installed prompt files.
 *
 * Run: node test/eval-suite.test.mjs
 */

import { test } from 'node:test';
import assert from 'node:assert/strict';
import { promises as fs, readFileSync, existsSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const pkgRoot = path.resolve(__dirname, '..');
const templatesDir = path.join(pkgRoot, 'templates');

// ────────────────────────────────────────────────────────────────────────────
// Fixture-based assertions about prompt/skill content shape.
// Each fixture is a (file, [predicates]) tuple — the file must satisfy every
// predicate to pass. Predicates are pure functions of file content.
// ────────────────────────────────────────────────────────────────────────────

const fixtures = [
  // The universal entry prompt MUST point at the Discovery Engineer
  {
    file: 'templates/github/prompts/Assess-Any-Application.prompt.md',
    description: 'Universal intake routes to Discovery Engineer',
    predicates: [
      (c) => c.includes('Discovery Engineer'),
      (c) => c.includes('Saul Bloom Jr'),
      (c) => c.includes('Capability Matrix') || c.includes('capability-matrix'),
      (c) => c.includes('reports/Discovery-Dossier.md'),
      (c) => c.includes('reports/Capability-Matrix.yaml'),
    ],
  },

  // Build-Migration-Plan MUST be Architect-led and require dossier+matrix
  {
    file: 'templates/github/prompts/Build-Migration-Plan.prompt.md',
    description: 'Plan-build is Architect-led and gated on discovery contract',
    predicates: [
      (c) => c.includes('Architect') && c.includes('Danny Ocean'),
      (c) => c.includes('reports/Discovery-Dossier.md'),
      (c) => c.includes('reports/Capability-Matrix.yaml'),
      (c) => c.includes('reports/Migration-Plan.md'),
    ],
  },

  // Migration-Orchestrator chatmode MUST list all 15 agents
  {
    file: 'templates/github/chatmodes/Migration-Orchestrator.chatmode.md',
    description: 'Orchestrator chatmode references all 15 agents',
    predicates: [
      (c) => c.includes('Discovery Engineer'),
      (c) => c.includes('Architect'),
      (c) => c.includes('Cost Engineer'),
      (c) => c.includes('Cutover Commander'),
      (c) => c.includes('Capability Matrix'),
      (c) => /15.*[Aa]gents?|15.*[Ss]pecialists?/.test(c),
    ],
  },

  // Decision tree MUST have at least 10 branches
  {
    file: 'templates/github/skills/migration-strategy-decision-tree.md',
    description: 'Decision tree has at least 10 branches and lists all 6Rs+',
    predicates: [
      (c) => (c.match(/^### Branch \d+/gm) || []).length >= 10,
      (c) => /rehost/i.test(c),
      (c) => /replatform/i.test(c),
      (c) => /refactor/i.test(c),
      (c) => /rearchitect/i.test(c),
      (c) => /rebuild/i.test(c),
      (c) => /retire/i.test(c),
      (c) => /retain/i.test(c),
    ],
  },

  // Capability Matrix skill MUST document all axes
  {
    file: 'templates/github/skills/capability-matrix.md',
    description: 'Capability Matrix skill covers all axes and required fields',
    predicates: [
      (c) => c.includes('source:'),
      (c) => c.includes('stack:'),
      (c) => c.includes('workload:'),
      (c) => c.includes('data:'),
      (c) => c.includes('evidence_confidence'),
      (c) => c.includes('migration_strategy'),
      (c) => c.includes('risk_flags'),
    ],
  },

  // Discovery Engineer charter MUST enforce evidence + handoff boundary
  {
    file: 'templates/squad/agents/discovery-engineer/charter.md',
    description: 'Discovery Engineer charter enforces evidence + Architect handoff',
    predicates: [
      (c) => /evidence/i.test(c),
      (c) => /confidence/i.test(c),
      (c) => c.includes('Architect'),
      (c) => /[Dd]o not own/.test(c) || /What I [Dd]on.{1,5}t [Oo]wn/.test(c),
      (c) => /escalat/i.test(c),
    ],
  },

  // Routing rules MUST be capability-based and list all key agents
  {
    file: 'templates/squad/routing.md',
    description: 'Routing rules are capability-based and list all key agents',
    predicates: [
      (c) => /capability.based|Capability.Based/.test(c),
      (c) => c.includes('Discovery Engineer'),
      (c) => c.includes('Architect'),
      (c) => c.includes('source-'),
      (c) => /stack[-.]/.test(c),    // matches stack-dotnet OR stack.primary_stack
      (c) => /workload[-.]/.test(c),
    ],
  },
];

// ────────────────────────────────────────────────────────────────────────────
// Coverage assertions: certain content categories must have minimum counts
// ────────────────────────────────────────────────────────────────────────────

async function countMatching(dir, pattern) {
  if (!existsSync(dir)) return 0;
  const entries = await fs.readdir(dir);
  return entries.filter((e) => pattern.test(e)).length;
}

// ────────────────────────────────────────────────────────────────────────────
// Tests
// ────────────────────────────────────────────────────────────────────────────

for (const fixture of fixtures) {
  test(fixture.description, () => {
    const filePath = path.join(pkgRoot, fixture.file);
    assert.ok(existsSync(filePath), `fixture file does not exist: ${fixture.file}`);
    const content = readFileSync(filePath, 'utf-8');
    for (const [i, predicate] of fixture.predicates.entries()) {
      assert.ok(
        predicate(content),
        `predicate ${i + 1} failed for ${fixture.file}: ${predicate.toString().slice(0, 120)}`
      );
    }
  });
}

test('Coverage: at least 9 source adapters present', async () => {
  const count = await countMatching(
    path.join(templatesDir, 'github', 'skills'),
    /^source-.+\.md$/
  );
  assert.ok(count >= 9, `expected ≥9 source adapters, got ${count}`);
});

test('Coverage: at least 14 stack adapters present', async () => {
  const count = await countMatching(
    path.join(templatesDir, 'github', 'skills'),
    /^stack-.+\.md$/
  );
  // 15 stack adapters + stack-detection.md = 16
  assert.ok(count >= 14, `expected ≥14 stack adapters, got ${count}`);
});

test('Coverage: at least 9 workload patterns present', async () => {
  const count = await countMatching(
    path.join(templatesDir, 'github', 'skills'),
    /^workload-.+\.md$/
  );
  assert.ok(count >= 9, `expected ≥9 workload patterns, got ${count}`);
});

test('Coverage: all 15 agent charters present', async () => {
  const agentsDir = path.join(templatesDir, 'squad', 'agents');
  const entries = await fs.readdir(agentsDir, { withFileTypes: true });
  const charters = entries.filter((e) => e.isDirectory()).length;
  assert.equal(charters, 15, `expected exactly 15 agents, got ${charters}`);

  // Each must have a charter.md
  for (const e of entries) {
    if (!e.isDirectory()) continue;
    const charter = path.join(agentsDir, e.name, 'charter.md');
    assert.ok(existsSync(charter), `agent missing charter.md: ${e.name}`);
  }
});

test('Coverage: Phase 1-6 prompts all present', () => {
  for (const n of [1, 2, 3, 4, 5, 6]) {
    const matches = [
      path.join(templatesDir, 'github', 'prompts', `Phase${n}-PlanAndAssess.prompt.md`),
      path.join(templatesDir, 'github', 'prompts', `Phase${n}-MigrateCode.prompt.md`),
      path.join(templatesDir, 'github', 'prompts', `Phase${n}-GenerateInfra.prompt.md`),
      path.join(templatesDir, 'github', 'prompts', `Phase${n}-DeployToAzure.prompt.md`),
      path.join(templatesDir, 'github', 'prompts', `Phase${n}-SetupCICD.prompt.md`),
      path.join(templatesDir, 'github', 'prompts', `Phase${n}-PostMigrationOps.prompt.md`),
    ];
    const exists = matches.some((m) => existsSync(m));
    assert.ok(exists, `Phase ${n} prompt missing`);
  }
});

test('Hard gates: every Phase/DB/Security/Cost prompt has the Capability Matrix gate', () => {
  const GATED_PROMPTS = [
    'Phase1-PlanAndAssess.prompt.md',
    'Phase2-MigrateCode.prompt.md',
    'Phase3-GenerateInfra.prompt.md',
    'Phase4-DeployToAzure.prompt.md',
    'Phase5-SetupCICD.prompt.md',
    'Phase6-PostMigrationOps.prompt.md',
    'DatabaseMigration.prompt.md',
    'SecurityHardening.prompt.md',
    'CostOptimization.prompt.md',
  ];
  const promptsDir = path.join(templatesDir, 'github', 'prompts');
  for (const f of GATED_PROMPTS) {
    const fp = path.join(promptsDir, f);
    assert.ok(existsSync(fp), `prompt missing: ${f}`);
    const content = readFileSync(fp, 'utf-8');
    assert.match(content, /BEGIN: capability-matrix-gate/, `${f}: gate sentinel missing — re-run scripts/inject-capability-matrix-gates.mjs`);
    assert.match(content, /reports\/Capability-Matrix\.yaml/, `${f}: gate doesn't reference Capability-Matrix.yaml`);
    assert.match(content, /reports\/Discovery-Dossier\.md/, `${f}: gate doesn't reference Discovery-Dossier.md`);
    assert.match(content, /MANDATORY OPENING CHECK/, `${f}: gate doesn't have the mandatory-opening-check heading`);
  }
});
