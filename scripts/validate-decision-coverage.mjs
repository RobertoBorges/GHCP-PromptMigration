/**
 * CI guard: validate that every decision in the canonical catalog is referenced
 * by at least one phase skill's decision-hardstop gate.
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
const catalogPath = path.join(
  repoRoot,
  '.github',
  'skills',
  'migration-decisions',
  'references',
  'decision-catalog.md'
);
const skillsDir = path.join(repoRoot, '.github', 'skills');

if (!existsSync(catalogPath)) {
  console.error('✗ Catalog file missing: .github/skills/migration-decisions/references/decision-catalog.md');
  process.exit(2);
}

// Extract decision IDs from catalog (D-NN headings).
const catalog = readFileSync(catalogPath, 'utf-8');
const catalogIds = Array.from(catalog.matchAll(/^##\s+(D-\d{2}):/gm)).map((m) => m[1]);

if (catalogIds.length === 0) {
  console.error('✗ Catalog has no D-NN entries — broken structure');
  process.exit(2);
}

// Each phase skill's gate references catalog IDs. We grep across all phase skills.
const PHASE_SKILLS = [
  'phase1-plan',
  'phase2-migrate-code',
  'phase3-generate-infra',
  'phase4-deploy-to-azure',
  'phase5-setup-cicd',
  'phase6-post-migration-ops',
  'database-migration',
  'security-hardening',
  'cost-optimization',
];

const referencedIds = new Set();
const perPhase = {};

for (const dir of PHASE_SKILLS) {
  const fp = path.join(skillsDir, dir, 'SKILL.md');
  if (!existsSync(fp)) continue;
  const content = readFileSync(fp, 'utf-8');
  const ids = Array.from(content.matchAll(/\b(D-\d{2})\b/g)).map((m) => m[1]);
  perPhase[`${dir}/SKILL.md`] = ids;
  for (const id of ids) referencedIds.add(id);
}

console.log('[validate-decision-coverage] Catalog entries:', catalogIds.length);
console.log('[validate-decision-coverage] Referenced in skills:', referencedIds.size);

const orphans = catalogIds.filter((id) => !referencedIds.has(id));
const unknown = [...referencedIds].filter((id) => !catalogIds.includes(id));

if (orphans.length > 0) {
  console.error('');
  console.error('✗ Orphaned catalog entries — defined but not referenced by any phase skill:');
  for (const id of orphans) {
    // Extract the decision name for clearer messaging
    const match = catalog.match(new RegExp(`^##\\s+${id}:\\s*(.+)$`, 'm'));
    const name = match ? match[1] : '(unknown)';
    console.error(`  • ${id} — ${name}`);
  }
  console.error('');
  console.error('Fix: either reference each orphan from at least one phase skill');
  console.error('     (via inject-decision-gates.mjs), or remove from .github/skills/migration-decisions/references/decision-catalog.md.');
}

if (unknown.length > 0) {
  console.error('');
  console.error('✗ Phase skills reference unknown decision IDs (not in catalog):');
  for (const id of unknown) {
    const where = Object.entries(perPhase)
      .filter(([, ids]) => ids.includes(id))
      .map(([f]) => f)
      .join(', ');
    console.error(`  • ${id} — referenced by: ${where}`);
  }
  console.error('');
  console.error('Fix: add the missing entries to .github/skills/migration-decisions/references/decision-catalog.md or correct the typo.');
}

if (orphans.length === 0 && unknown.length === 0) {
  console.log('✓ All catalog entries are referenced. No unknown IDs.');
  process.exit(0);
}

process.exit(1);
