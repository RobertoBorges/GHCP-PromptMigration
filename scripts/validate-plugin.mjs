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

// Every location release-please bumps (release-please-config.json extra-files)
// must already carry the extension version, so docs can't silently go stale.
const releaseConfig = readJson('release-please-config.json');
const extensionPath = 'packages/azure-migration-squad-vscode';
const extraFiles = releaseConfig.packages?.[extensionPath]?.['extra-files'] ?? [];
assert.ok(extraFiles.length, `release-please-config.json must list extra-files for ${extensionPath}`);
const jsonPathGet = (data, expr) => {
  const segments = [...expr.slice(1).matchAll(/\.([A-Za-z_$][\w$-]*)|\[(\d+)\]|\['([^']+)'\]/g)]
    .map((m) => m[1] ?? (m[2] !== undefined ? Number(m[2]) : m[3]));
  return segments.reduce((node, key) => node?.[key], data);
};
const markedVersions = (text) => {
  const found = [];
  let inBlock = false;
  for (const line of text.split('\n')) {
    if (line.includes('x-release-please-start-version')) { inBlock = true; continue; }
    if (line.includes('x-release-please-end')) { inBlock = false; continue; }
    if (inBlock || line.includes('x-release-please-version')) {
      found.push(...(line.match(/\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?/g) ?? []));
    }
  }
  return found;
};
for (const spec of extraFiles.map((e) => (typeof e === 'string' ? { type: 'generic', path: e } : e))) {
  const relative = spec.path.startsWith('/') ? spec.path.slice(1) : `${extensionPath}/${spec.path}`;
  const text = readFileSync(path.join(root, relative), 'utf8');
  if (spec.type === 'json') {
    assert.equal(jsonPathGet(JSON.parse(text), spec.jsonpath), extension.version,
      `${relative} ${spec.jsonpath} must match the extension version ${extension.version}`);
  } else if (spec.type === 'generic') {
    const versions = markedVersions(text);
    assert.ok(versions.length, `${relative} is listed in extra-files but has no x-release-please version markers`);
    for (const version of versions) {
      assert.equal(version, extension.version,
        `${relative} has stale marked version ${version}; run "npm run version:set -- ${extension.version}"`);
    }
  }
}

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
