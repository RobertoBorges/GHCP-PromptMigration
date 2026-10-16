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
  const script = path.join(root, packagePath, 'scripts', 'local-release.mjs');
  mkdirSync(path.dirname(script), { recursive: true });
  copyFileSync(path.join(repo, packagePath, 'scripts', 'local-release.mjs'), script);
  execFileSync('git', ['init', '--quiet', root]);
  return {
    read: (file) => JSON.parse(readFileSync(path.join(root, file), 'utf8')),
    run: (...args) => execFileSync(process.execPath, [script, '--minor', ...args], {
      cwd: root, encoding: 'utf8', stdio: ['ignore', 'pipe', 'pipe'],
    }),
  };
}

test('Local release updates every distributed version without marking it published', (t) => {
  const { read, run } = fixture(t);
  run('--yes', '--no-build');
  assert.equal(read(`${packagePath}/package.json`).version, '0.7.0');
  assert.equal(read('plugin.json').version, '0.7.0');
  assert.equal(read('.github/plugin/marketplace.json').plugins[0].version, '0.7.0');
  assert.equal(read('package-lock.json').packages[packagePath].version, '0.7.0');
  assert.equal(read('.release-please-manifest.json')[packagePath], '0.6.0');
});

test('Local release dry-run leaves extension, plugin, marketplace and lockfile unchanged', (t) => {
  const { read, run } = fixture(t);
  run('--dry-run');
  assert.equal(read(`${packagePath}/package.json`).version, '0.6.0');
  assert.equal(read('plugin.json').version, '0.6.0');
  assert.equal(read('.github/plugin/marketplace.json').plugins[0].version, '0.6.0');
  assert.equal(read('package-lock.json').packages[packagePath].version, '0.6.0');
});
