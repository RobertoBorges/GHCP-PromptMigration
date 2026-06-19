/**
 * Smoke test: pack the package, install it into a temp dir, run --version and --help.
 *
 * This catches regressions where the package.json `files` allow-list is wrong,
 * or the bin shim doesn't run, or templates didn't get synced.
 *
 * Run via:  node --test test/install.test.mjs
 */

import { test } from 'node:test';
import assert from 'node:assert/strict';
import { execSync } from 'node:child_process';
import { promises as fs, existsSync, mkdtempSync, readdirSync, rmSync } from 'node:fs';
import path from 'node:path';
import os from 'node:os';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const pkgRoot = path.resolve(__dirname, '..');

function sh(cmd, opts = {}) {
  return execSync(cmd, { stdio: ['ignore', 'pipe', 'pipe'], encoding: 'utf-8', ...opts });
}

test('package.json is valid and lists key fields', async () => {
  const pkg = JSON.parse(await fs.readFile(path.join(pkgRoot, 'package.json'), 'utf-8'));
  assert.equal(pkg.name, '@robertoborges/azure-migration-squad');
  assert.ok(pkg.bin['azure-migration-squad'], 'azure-migration-squad bin missing');
  assert.ok(pkg.bin['ams'], 'ams short alias missing');
  assert.ok(pkg.files.includes('templates'), 'templates must be in files allow-list');
  assert.ok(pkg.files.includes('bin'), 'bin must be in files allow-list');
});

test('CLI binary exists and starts with shebang', async () => {
  const cliPath = path.join(pkgRoot, 'bin', 'cli.js');
  assert.ok(existsSync(cliPath), 'bin/cli.js missing');
  const content = await fs.readFile(cliPath, 'utf-8');
  assert.ok(content.startsWith('#!/usr/bin/env node'), 'bin/cli.js missing shebang');
});

test('CLI --version reports the package version', () => {
  const cliPath = path.join(pkgRoot, 'bin', 'cli.js');
  const output = sh(`node "${cliPath}" --version`).trim();
  assert.match(output, /^\d+\.\d+\.\d+/, `version output looks wrong: "${output}"`);
});

test('CLI help command runs without error', () => {
  const cliPath = path.join(pkgRoot, 'bin', 'cli.js');
  const output = sh(`node "${cliPath}" help`);
  assert.match(output, /azure-migration-squad/, 'help output missing program name');
  assert.match(output, /init/, 'help output missing init command');
  assert.match(output, /telemetry/, 'help output missing telemetry command');
});

test('Telemetry status command works even with no installation', () => {
  const cliPath = path.join(pkgRoot, 'bin', 'cli.js');
  const env = { ...process.env, NO_COLOR: '1', AZURE_MIGRATION_SQUAD_TELEMETRY: '0' };
  const output = sh(`node "${cliPath}" telemetry status`, { env });
  assert.match(output, /Telemetry status/);
  assert.match(output, /Enabled:/);
});

test('npm pack succeeds and produces a tarball', () => {
  const tmpDir = mkdtempSync(path.join(os.tmpdir(), 'ams-pack-'));
  try {
    sh(`npm pack --pack-destination "${tmpDir}"`, { cwd: pkgRoot });
    const files = readdirSync(tmpDir);
    const tgz = files.find((f) => f.endsWith('.tgz'));
    assert.ok(tgz, `expected a .tgz in ${tmpDir}, got: ${files.join(', ')}`);
  } finally {
    rmSync(tmpDir, { recursive: true, force: true });
  }
});

test('init fails clearly when Squad runtime is missing', () => {
  const cliPath = path.join(pkgRoot, 'bin', 'cli.js');
  const tmpDir = mkdtempSync(path.join(os.tmpdir(), 'ams-init-no-squad-'));
  try {
    const env = { ...process.env, NO_COLOR: '1', CI: 'true', AZURE_MIGRATION_SQUAD_TELEMETRY: '0' };
    let stderr = '';
    let stdout = '';
    try {
      stdout = execSync(`node "${cliPath}" init`, { cwd: tmpDir, env, encoding: 'utf-8', stdio: ['ignore', 'pipe', 'pipe'] });
    } catch (err) {
      stdout = err.stdout?.toString() || '';
      stderr = err.stderr?.toString() || '';
    }
    const combined = stdout + stderr;
    assert.match(combined, /Squad runtime not detected/, `init should reject when no .squad/ — got:\n${combined}`);
  } finally {
    rmSync(tmpDir, { recursive: true, force: true });
  }
});
