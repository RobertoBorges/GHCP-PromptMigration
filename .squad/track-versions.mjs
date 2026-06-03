#!/usr/bin/env node
import { createHash } from 'node:crypto';
import { existsSync, readFileSync, readdirSync, writeFileSync } from 'node:fs';
import { dirname, join, relative } from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const root = join(__dirname, '..');
const promptsDir = join(root, '.github', 'prompts');
const chatmodesDir = join(root, '.github', 'chatmodes');
const hashFile = join(__dirname, '.prompt-hashes.json');

function getTrackedFiles(directory, suffix) {
  return readdirSync(directory)
    .filter((name) => name.endsWith(suffix))
    .sort((a, b) => a.localeCompare(b))
    .map((name) => join(directory, name));
}

function shortHash(filePath) {
  return createHash('sha256')
    .update(readFileSync(filePath))
    .digest('hex')
    .slice(0, 8);
}

function loadStoredHashes() {
  if (!existsSync(hashFile)) {
    return {};
  }

  return JSON.parse(readFileSync(hashFile, 'utf8'));
}

function printTable(rows) {
  const headers = ['Filename', 'Stored Hash', 'Current Hash', 'Changed?'];
  const widths = headers.map((header, index) =>
    Math.max(header.length, ...rows.map((row) => row[index].length))
  );

  const formatRow = (row) =>
    `| ${row.map((cell, index) => cell.padEnd(widths[index])).join(' | ')} |`;

  const divider = `|-${widths.map((width) => '-'.repeat(width)).join('-|-')}-|`;

  console.log(formatRow(headers));
  console.log(divider);
  rows.forEach((row) => console.log(formatRow(row)));
}

const storedHashes = loadStoredHashes();
const isInitialBaseline = !existsSync(hashFile);
const files = [
  ...getTrackedFiles(promptsDir, '.prompt.md'),
  ...getTrackedFiles(chatmodesDir, '.chatmode.md')
];

const rows = [];
const nextHashes = {};
const changedFiles = [];

for (const filePath of files) {
  const relPath = relative(root, filePath).replaceAll('\\', '/');
  const currentHash = shortHash(filePath);
  const storedHash = storedHashes[relPath] ?? '-';
  const changed = storedHash === currentHash ? 'no' : 'yes';

  rows.push([relPath, storedHash, currentHash, changed]);
  nextHashes[relPath] = currentHash;

  if (changed === 'yes') {
    changedFiles.push(relPath);
  }
}

writeFileSync(hashFile, `${JSON.stringify(nextHashes, null, 2)}\n`, 'utf8');

if (isInitialBaseline) {
  console.log('Initial baseline created.');
} else if (changedFiles.length === 0) {
  console.log('No prompt or chatmode changes detected.');
} else {
  console.log(`Changed files since last run: ${changedFiles.length}`);
}

printTable(rows);

if (!isInitialBaseline) {
  if (changedFiles.length === 0) {
    console.log('\nChanged files: none');
  } else {
    console.log(`\nChanged files: ${changedFiles.join(', ')}`);
  }
}
