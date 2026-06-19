/**
 * Validate plugin.manifest.json against Squad SDK constraints.
 *
 * Implements the same validation rules as the squad-sdk parser:
 *   - https://github.com/bradygaster/squad/blob/main/packages/squad-sdk/src/marketplace/plugin-manifest.ts
 *
 * Validates:
 *   - Required top-level fields (id, name, version, files)
 *   - Component keys are limited to the COMPONENT_KINDS allowlist
 *   - File targets start with one of ALLOWED_TARGET_ROOTS
 *   - File sources are not absolute paths
 *   - File extensions are not in EXECUTABLE_EXTENSIONS for files that shouldn't be code
 *   - Provider type/mode/protocol enums are valid
 *
 * Exits non-zero on any failure.
 */

import { readFileSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const manifestPath = path.resolve(__dirname, '..', 'plugin.manifest.json');

// From squad-sdk plugin-manifest.ts
const COMPONENT_KINDS = new Set([
  'agents', 'ceremonies', 'decisions', 'instructions', 'knowledge',
  'memory', 'routing', 'templates', 'workflows', 'hooks', 'adapters',
]);

const ALLOWED_TARGET_ROOTS = new Set([
  'agents', 'ceremonies', 'decisions', 'instructions', 'knowledge',
  'memory', 'plugins', 'prompts', 'routing', 'templates', 'workflows',
]);

const PROVIDER_TYPES = new Set(['memory', 'knowledge', 'persistence', 'event', 'policy']);
const PROVIDER_MODES = new Set(['read', 'write', 'read-write']);
const PROVIDER_PROTOCOLS = new Set(['static-artifact', 'mcp']);

const EXECUTABLE_EXTENSIONS = new Set([
  '.bat', '.cmd', '.com', '.cjs', '.exe', '.js', '.mjs', '.ps1', '.sh', '.ts', '.tsx',
]);

let problems = 0;
const fail = (msg) => { console.error(`  ✗ ${msg}`); problems++; };
const ok = (msg) => console.log(`  ✓ ${msg}`);

console.log(`[validate-plugin-manifest] Checking ${manifestPath}\n`);

let manifest;
try {
  manifest = JSON.parse(readFileSync(manifestPath, 'utf-8'));
} catch (err) {
  console.error(`✗ Failed to parse manifest: ${err.message}`);
  process.exit(1);
}

// Required fields
for (const field of ['id', 'name', 'version', 'files']) {
  if (!(field in manifest)) fail(`missing required field: ${field}`);
}
if (typeof manifest.id !== 'string' || !manifest.id) fail('id must be a non-empty string');
if (typeof manifest.name !== 'string' || !manifest.name) fail('name must be a non-empty string');
if (typeof manifest.version !== 'string' || !manifest.version) fail('version must be a non-empty string');
if (!Array.isArray(manifest.files)) fail('files must be an array');

if (problems === 0) ok('Required top-level fields present');

// Components keys
if (manifest.components) {
  for (const key of Object.keys(manifest.components)) {
    if (!COMPONENT_KINDS.has(key)) {
      fail(`components.${key} is not in allowed COMPONENT_KINDS (${[...COMPONENT_KINDS].join(', ')})`);
    }
  }
  ok(`components keys valid: ${Object.keys(manifest.components).join(', ')}`);
}

// File deployments
if (Array.isArray(manifest.files)) {
  for (const [i, file] of manifest.files.entries()) {
    if (typeof file.source !== 'string' || !file.source) {
      fail(`files[${i}]: source must be a non-empty string`);
      continue;
    }
    if (typeof file.target !== 'string' || !file.target) {
      fail(`files[${i}]: target must be a non-empty string`);
      continue;
    }
    if (path.isAbsolute(file.source)) {
      fail(`files[${i}].source is absolute (must be relative): ${file.source}`);
    }
    if (path.isAbsolute(file.target)) {
      fail(`files[${i}].target is absolute (must be relative): ${file.target}`);
    }
    // Normalize and check target root
    const normalized = file.target.replace(/\\/g, '/');
    const targetRoot = normalized.split('/')[0];
    if (!ALLOWED_TARGET_ROOTS.has(targetRoot)) {
      fail(`files[${i}].target "${file.target}" root "${targetRoot}" not in ALLOWED_TARGET_ROOTS (${[...ALLOWED_TARGET_ROOTS].join(', ')})`);
    }
    // No path traversal
    if (file.source.includes('..') || file.target.includes('..')) {
      fail(`files[${i}] contains '..' path component (path traversal not allowed)`);
    }
    // Check for executable extensions in target (warning, not error — squad allows these)
    const ext = path.extname(file.target).toLowerCase();
    if (EXECUTABLE_EXTENSIONS.has(ext) && file.type !== 'asset') {
      console.warn(`  ⚠ files[${i}].target has executable extension ${ext} — declare type:"asset" if intentional`);
    }
  }
  ok(`All ${manifest.files.length} file deployments validated`);
}

// Providers
if (Array.isArray(manifest.providers)) {
  for (const [i, p] of manifest.providers.entries()) {
    if (!p.id) fail(`providers[${i}].id required`);
    if (!p.type) fail(`providers[${i}].type required`);
    if (p.type && !PROVIDER_TYPES.has(p.type)) {
      fail(`providers[${i}].type "${p.type}" not in PROVIDER_TYPES (${[...PROVIDER_TYPES].join(', ')})`);
    }
    if (p.mode && !PROVIDER_MODES.has(p.mode)) {
      fail(`providers[${i}].mode "${p.mode}" not in PROVIDER_MODES`);
    }
    if (p.protocol && !PROVIDER_PROTOCOLS.has(p.protocol)) {
      fail(`providers[${i}].protocol "${p.protocol}" not in PROVIDER_PROTOCOLS`);
    }
  }
  ok(`All ${manifest.providers.length} providers validated`);
}

// Cross-check: source files actually exist
const repoRoot = path.resolve(__dirname, '..');
import('node:fs').then(({ existsSync }) => {
  let missing = 0;
  for (const file of manifest.files || []) {
    const sourcePath = path.join(repoRoot, file.source);
    if (!existsSync(sourcePath)) {
      console.error(`  ✗ source file does not exist on disk: ${file.source}`);
      missing++;
    }
  }
  if (missing === 0) {
    ok(`All ${manifest.files.length} source files exist on disk`);
  } else {
    problems += missing;
  }

  console.log('');
  if (problems > 0) {
    console.error(`[validate-plugin-manifest] FAILED — ${problems} problem(s).`);
    process.exit(1);
  }
  console.log('[validate-plugin-manifest] all checks passed.');
});
