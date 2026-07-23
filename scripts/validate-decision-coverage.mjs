/**
 * CI guard: validate that every decision in the canonical catalog is referenced
 * by at least one phase prompt's decision-hardstop gate.
 *
 * If a catalog item is orphaned (no phase depends on it), the catalog is either
 * stale (entry should be removed) OR a phase is missing a dependency (gate
 * should be updated). Either way, build fails until reconciled.
 *
 * Run via: node scripts/validate-decision-coverage.mjs
 */

import { readFileSync, existsSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const repoRoot = path.resolve(__dirname, '..');
const catalogPath = path.join(repoRoot, '.github', 'skills', 'decision-catalog.md');
const promptsDir = path.join(repoRoot, '.github', 'prompts');

if (!existsSync(catalogPath)) {
  console.error('✗ Catalog file missing: .github/skills/decision-catalog.md');
  process.exit(2);
}

// Extract decision IDs from catalog (D-NN headings).
const catalog = readFileSync(catalogPath, 'utf-8');
const catalogIds = Array.from(catalog.matchAll(/^##\s+(D-\d{2}):/gm)).map((m) => m[1]);

if (catalogIds.length === 0) {
  console.error('✗ Catalog has no D-NN entries — broken structure');
  process.exit(2);
}

// Each prompt's gate references catalog IDs. We grep across all phase prompts.
const PHASE_PROMPTS = [
  'Phase1-Plan.prompt.md',
  'Phase2-MigrateCode.prompt.md',
  'Phase3-GenerateInfra.prompt.md',
  'Phase4-DeployToAzure.prompt.md',
  'Phase5-SetupCICD.prompt.md',
  'Phase6-PostMigrationOps.prompt.md',
  'DatabaseMigration.prompt.md',
  'SecurityHardening.prompt.md',
  'CostOptimization.prompt.md',
];

const referencedIds = new Set();
const perPhase = {};

for (const file of PHASE_PROMPTS) {
  const fp = path.join(promptsDir, file);
  if (!existsSync(fp)) continue;
  const content = readFileSync(fp, 'utf-8');
  const ids = Array.from(content.matchAll(/\b(D-\d{2})\b/g)).map((m) => m[1]);
  perPhase[file] = ids;
  for (const id of ids) referencedIds.add(id);
}

console.log('[validate-decision-coverage] Catalog entries:', catalogIds.length);
console.log('[validate-decision-coverage] Referenced in prompts:', referencedIds.size);

const orphans = catalogIds.filter((id) => !referencedIds.has(id));
const unknown = [...referencedIds].filter((id) => !catalogIds.includes(id));

if (orphans.length > 0) {
  console.error('');
  console.error('✗ Orphaned catalog entries — defined but not referenced by any phase prompt:');
  for (const id of orphans) {
    // Extract the decision name for clearer messaging
    const match = catalog.match(new RegExp(`^##\\s+${id}:\\s*(.+)$`, 'm'));
    const name = match ? match[1] : '(unknown)';
    console.error(`  • ${id} — ${name}`);
  }
  console.error('');
  console.error('Fix: either reference each orphan from at least one phase prompt');
  console.error('     (via inject-decision-gates.mjs), or remove from .github/skills/decision-catalog.md.');
}

if (unknown.length > 0) {
  console.error('');
  console.error('✗ Phase prompts reference unknown decision IDs (not in catalog):');
  for (const id of unknown) {
    const where = Object.entries(perPhase)
      .filter(([, ids]) => ids.includes(id))
      .map(([f]) => f)
      .join(', ');
    console.error(`  • ${id} — referenced by: ${where}`);
  }
  console.error('');
  console.error('Fix: add the missing entries to .github/skills/decision-catalog.md or correct the typo.');
}

if (orphans.length === 0 && unknown.length === 0) {
  console.log('✓ All catalog entries are referenced. No unknown IDs.');
  process.exit(0);
}

process.exit(1);
