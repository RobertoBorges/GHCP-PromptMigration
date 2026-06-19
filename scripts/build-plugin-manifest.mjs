/**
 * Generate plugin.manifest.json from actual content on disk.
 *
 * Squad plugin marketplace consumes this manifest. It installs files under
 * `.squad/` (constrained to approved roots like agents/, knowledge/, prompts/).
 *
 * Run via: npm run build:plugin-manifest
 *
 * Note on scope:
 *   The Squad plugin install copies a curated subset into `.squad/`.
 *   For FULL Copilot integration (chatmodes, .github/prompts, .github/skills),
 *   users should install via npm: `npx @robertoborges/azure-migration-squad init`.
 *   The Squad plugin path is for Squad-discovery-first users who want the
 *   agents + universal skills as Squad knowledge artifacts.
 */

import { promises as fs, existsSync, readFileSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const repoRoot = path.resolve(__dirname, '..');

const PKG = JSON.parse(readFileSync(path.join(repoRoot, 'packages', 'azure-migration-squad', 'package.json'), 'utf-8'));

async function listAgents() {
  const agentsDir = path.join(repoRoot, '.squad', 'agents');
  const entries = await fs.readdir(agentsDir, { withFileTypes: true });
  const result = [];
  for (const e of entries) {
    if (!e.isDirectory()) continue;
    const charterPath = path.join(agentsDir, e.name, 'charter.md');
    if (existsSync(charterPath)) {
      result.push(e.name);
    }
  }
  return result.sort();
}

async function listSkills() {
  const skillsDir = path.join(repoRoot, '.github', 'skills');
  const entries = await fs.readdir(skillsDir, { withFileTypes: true });
  const flatSkills = [];
  for (const e of entries) {
    if (e.isFile() && e.name.endsWith('.md')) {
      flatSkills.push(e.name);
    }
  }
  return flatSkills.sort();
}

function categorizeSkill(name) {
  if (name.startsWith('source-')) return 'source';
  if (name.startsWith('stack-') && name !== 'stack-detection.md') return 'stack';
  if (name.startsWith('workload-')) return 'workload';
  return 'universal';
}

async function generate() {
  const agents = await listAgents();
  const skills = await listSkills();

  const files = [];

  // Agent charters → .squad/agents/<name>/charter.md
  for (const agent of agents) {
    files.push({
      source: `.squad/agents/${agent}/charter.md`,
      target: `agents/${agent}/charter.md`,
      type: 'agent',
    });
  }

  // Squad orchestration docs → routing/
  for (const f of ['team.md', 'routing.md']) {
    const p = path.join(repoRoot, '.squad', f);
    if (existsSync(p)) {
      files.push({
        source: `.squad/${f}`,
        target: `routing/${f}`,
        type: 'doc',
      });
    }
  }

  // Skills → knowledge/azure-migration/<category>/<name>
  for (const skill of skills) {
    const category = categorizeSkill(skill);
    files.push({
      source: `.github/skills/${skill}`,
      target: `knowledge/azure-migration/${category}/${skill}`,
      type: 'knowledge',
    });
  }

  // Top-level agent guidance → instructions/
  const copilotInstructions = path.join(repoRoot, '.github', 'copilot-instructions.md');
  if (existsSync(copilotInstructions)) {
    files.push({
      source: '.github/copilot-instructions.md',
      target: 'instructions/azure-migration-instructions.md',
      type: 'instruction',
    });
  }

  const manifest = {
    id: 'azure-migration-squad',
    name: 'Azure Migration Squad',
    version: PKG.version,
    description:
      'Universal Azure migration squad: 15 specialist agents + 60+ source/stack/workload adapters + migration-strategy-decision-tree. Discovery-first, evidence-bound, Squad-orchestrated.',
    authors: ['Roberto Borges'],
    license: 'MIT',
    squad: '>=0.10.0',
    components: {
      agents: agents,
      knowledge: ['azure-migration'],
      routing: ['azure-migration-routing'],
      instructions: ['azure-migration-instructions'],
    },
    repository: {
      type: 'github',
      url: 'https://github.com/RobertoBorges/GHCP-PromptMigration',
    },
    upstream: {
      package: '@robertoborges/azure-migration-squad',
      registry: 'npm',
      installCommand: 'npx @robertoborges/azure-migration-squad@insider init',
      docs: 'https://github.com/RobertoBorges/GHCP-PromptMigration#readme',
    },
    providers: [
      {
        id: 'azure-migration-knowledge',
        type: 'knowledge',
        mode: 'read',
        protocol: 'static-artifact',
        description:
          'Static knowledge artifacts covering source/stack/workload adapters and the migration-strategy-decision-tree.',
        artifact: 'knowledge/azure-migration/universal/migration-strategy-decision-tree.md',
        capabilities: [
          'migration-strategy',
          'discovery',
          'capability-matrix',
          'source-classification',
          'stack-classification',
          'workload-classification',
        ],
      },
    ],
    files,
  };

  const outPath = path.join(repoRoot, 'plugin.manifest.json');
  await fs.writeFile(outPath, JSON.stringify(manifest, null, 2) + '\n');

  console.log(`[build-plugin-manifest] Wrote ${outPath}`);
  console.log(`  agents:        ${agents.length}`);
  console.log(`  skills:        ${skills.length}`);
  console.log(`  total files:   ${files.length}`);
  console.log(`  version:       ${PKG.version}`);
}

generate().catch((err) => {
  console.error('[build-plugin-manifest] FAILED:', err);
  process.exit(1);
});
