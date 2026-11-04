import assert from 'node:assert/strict';
import { readFileSync, readdirSync, statSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const readJson = (file) => JSON.parse(readFileSync(path.join(root, file), 'utf8'));
const plugin = readJson('plugin.json');
const marketplace = readJson('.github/plugin/marketplace.json');
const extension = readJson('packages/azure-migration-squad-vscode/package.json');
const lock = readJson('package-lock.json');

assert.match(plugin.name, /^[a-z][a-z0-9-]*$/, 'Plugin name must be kebab-case');
assert.equal(plugin.$schema, undefined, 'Custom component paths require the Copilot plugin format');
assert.equal(plugin.version, extension.version, 'Plugin and VSIX versions must match');
assert.equal(lock.packages['packages/azure-migration-squad-vscode'].version, extension.version,
  'Workspace lockfile version must match the VSIX');
const entry = marketplace.plugins.find((candidate) => candidate.name === plugin.name);
assert.ok(entry, 'Plugin must be listed in the repository marketplace');
assert.equal(entry.source, './', 'Marketplace source must resolve to the repository root');
assert.equal(entry.version, plugin.version, 'Marketplace and plugin versions must match');

for (const field of ['hooks', 'mcpServers', 'lspServers']) {
  assert.equal(plugin[field], undefined, `This plugin must not automatically register ${field}`);
}

const componentRoot = (field) => {
  assert.equal(typeof plugin[field], 'string', `${field} must specify a component directory`);
  const resolved = path.resolve(root, plugin[field]);
  const relative = path.relative(root, resolved);
  assert.ok(relative && !relative.startsWith('..') && !path.isAbsolute(relative),
    `${field} must stay inside the plugin`);
  assert.ok(statSync(resolved).isDirectory(), `${field} directory must exist`);
  return resolved;
};
const skillsRoot = componentRoot('skills');
const agentsRoot = componentRoot('agents');
const skills = readdirSync(skillsRoot, { withFileTypes: true }).filter((entry) => entry.isDirectory());
assert.ok(skills.length, 'Plugin must discover skills');
for (const skill of skills) {
  const content = readFileSync(path.join(skillsRoot, skill.name, 'SKILL.md'), 'utf8');
  const name = content.match(/^---\r?\n[\s\S]*?^name:\s*([a-z0-9-]+)\s*$/m)?.[1];
  assert.equal(name, skill.name, `Invalid skill name or missing frontmatter: ${skill.name}`);
}
const agents = readdirSync(agentsRoot).filter((file) => file.endsWith('.agent.md'));
assert.ok(agents.length, 'Plugin must discover agents');
for (const agent of agents) {
  const content = readFileSync(path.join(agentsRoot, agent), 'utf8');
  assert.match(content, /^---\r?\n[\s\S]*?^name:\s*.+$/m, `Missing agent name: ${agent}`);
}

console.log(`Plugin ${plugin.name}@${plugin.version}: ${skills.length} skills and ${agents.length} agents; release versions aligned.`);
