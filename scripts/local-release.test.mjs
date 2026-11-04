import assert from 'node:assert/strict';
import { execFileSync } from 'node:child_process';
import { copyFileSync, mkdirSync, mkdtempSync, readFileSync, rmSync, writeFileSync } from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { test } from 'node:test';

const repo = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const packagePath = 'packages/azure-migration-squad-vscode';

function fixture(t) {
  const root = mkdtempSync(path.join(os.tmpdir(), 'azure-migration-release-'));
  t.after(() => rmSync(root, { recursive: true, force: true }));
  const writeJson = (file, value) => {
    const target = path.join(root, file);
    mkdirSync(path.dirname(target), { recursive: true });
    writeFileSync(target, JSON.stringify(value, null, 2) + '\n');
  };
  writeJson(`${packagePath}/package.json`, { version: '0.6.0' });
  writeJson('plugin.json', { version: '0.6.0' });
  writeJson('.github/plugin/marketplace.json', {
    plugins: [{ name: 'azure-migration-agent', version: '0.6.0' }],
  });
  writeJson('package-lock.json', { packages: { [packagePath]: { version: '0.6.0' } } });
  writeJson('.release-please-manifest.json', { [packagePath]: '0.6.0' });
  copyFileSync(path.join(repo, 'release-please-config.json'), path.join(root, 'release-please-config.json'));
  const doc = path.join(root, 'docs', 'publishing-vscode-extension.md');
  mkdirSync(path.dirname(doc), { recursive: true });
  writeFileSync(doc, [
    'Example tag vscode-v0.2.1 stays untouched.',
    '<!-- x-release-please-start-version -->',
    'Current source version: **0.6.0** → azure-migration-squad-vscode-0.6.0.vsix',
    '<!-- x-release-please-end -->',
    '',
  ].join('\n'));
  const script = path.join(root, packagePath, 'scripts', 'local-release.mjs');
  mkdirSync(path.dirname(script), { recursive: true });
  copyFileSync(path.join(repo, packagePath, 'scripts', 'local-release.mjs'), script);
  execFileSync('git', ['init', '--quiet', root]);
  return {
    read: (file) => JSON.parse(readFileSync(path.join(root, file), 'utf8')),
    readText: (file) => readFileSync(path.join(root, file), 'utf8'),
    run: (...args) => execFileSync(process.execPath, [script, ...args], {
      cwd: root, encoding: 'utf8', stdio: ['ignore', 'pipe', 'pipe'],
    }),
  };
}

test('Local release updates every distributed version without marking it published', (t) => {
  const { read, run } = fixture(t);
  run('--minor', '--yes', '--no-build');
  assert.equal(read(`${packagePath}/package.json`).version, '0.7.0');
  assert.equal(read('plugin.json').version, '0.7.0');
  assert.equal(read('.github/plugin/marketplace.json').plugins[0].version, '0.7.0');
  assert.equal(read('package-lock.json').packages[packagePath].version, '0.7.0');
  assert.equal(read('.release-please-manifest.json')[packagePath], '0.6.0');
});

test('Explicit version updates JSON files and only marked doc versions', (t) => {
  const { read, readText, run } = fixture(t);
  run('0.6.3', '--yes', '--no-build');
  assert.equal(read(`${packagePath}/package.json`).version, '0.6.3');
  assert.equal(read('plugin.json').version, '0.6.3');
  const doc = readText('docs/publishing-vscode-extension.md');
  assert.match(doc, /\*\*0\.6\.3\*\* → azure-migration-squad-vscode-0\.6\.3\.vsix/);
  assert.match(doc, /vscode-v0\.2\.1 stays untouched/);
});

test('Local release dry-run leaves extension, plugin, marketplace and lockfile unchanged', (t) => {
  const { read, run } = fixture(t);
  run('--minor', '--dry-run');
  assert.equal(read(`${packagePath}/package.json`).version, '0.6.0');
  assert.equal(read('plugin.json').version, '0.6.0');
  assert.equal(read('.github/plugin/marketplace.json').plugins[0].version, '0.6.0');
  assert.equal(read('package-lock.json').packages[packagePath].version, '0.6.0');
});
