#!/usr/bin/env node

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const decisionsPath = path.join(__dirname, 'decisions.md');

const ANSI = {
  reset: '\x1b[0m',
  bold: '\x1b[1m',
  dim: '\x1b[2m',
  red: '\x1b[31m',
  green: '\x1b[32m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
  magenta: '\x1b[35m',
  cyan: '\x1b[36m',
  gray: '\x1b[90m',
};

function paint(text, ...codes) {
  return `${codes.join('')}${text}${ANSI.reset}`;
}

function pad(value, length) {
  return String(value).padEnd(length, ' ');
}

function parseArgs(argv) {
  const options = {
    search: '',
    last: null,
  };

  for (let index = 0; index < argv.length; index += 1) {
    const arg = argv[index];

    if (arg === '--search' && index + 1 < argv.length) {
      options.search = argv[index + 1];
      index += 1;
      continue;
    }

    if (arg.startsWith('--search=')) {
      options.search = arg.slice('--search='.length);
      continue;
    }

    if (arg === '--last' && index + 1 < argv.length) {
      const parsed = Number.parseInt(argv[index + 1], 10);
      if (Number.isFinite(parsed) && parsed > 0) {
        options.last = parsed;
      }
      index += 1;
      continue;
    }

    if (arg.startsWith('--last=')) {
      const parsed = Number.parseInt(arg.slice('--last='.length), 10);
      if (Number.isFinite(parsed) && parsed > 0) {
        options.last = parsed;
      }
    }
  }

  return options;
}

function normalizeFieldName(fieldName) {
  return fieldName.trim().toLowerCase().replace(/\s+/g, '-');
}

function normalizeStatus(status) {
  return String(status || 'unknown')
    .trim()
    .toLowerCase()
    .replace(/[_\s]+/g, '-');
}

function inferStatus(section) {
  const lowered = String(section || '').trim().toLowerCase();

  if (!lowered) {
    return 'unknown';
  }

  if (lowered.includes('active')) {
    return 'active';
  }

  if (lowered.includes('superseded')) {
    return 'superseded';
  }

  if (lowered.includes('archived')) {
    return 'archived';
  }

  if (/^\d{4}-\d{2}-\d{2}$/.test(lowered)) {
    return 'recorded';
  }

  if (lowered.includes('decision')) {
    return 'recorded';
  }

  return 'unknown';
}

function parseDate(value, fallbackSection) {
  const candidate = String(value || fallbackSection || '').trim();
  if (!candidate) {
    return null;
  }

  const isoMatch = candidate.match(/^(\d{4}-\d{2}-\d{2})$/);
  if (isoMatch) {
    return isoMatch[1];
  }

  const parsed = new Date(candidate);
  if (Number.isNaN(parsed.getTime())) {
    return null;
  }

  return parsed.toISOString().slice(0, 10);
}

function parseDecisions(markdown) {
  const lines = markdown.split(/\r?\n/);
  const decisions = [];
  let currentSection = 'Uncategorized';
  let current = null;
  let currentField = null;

  function finalizeCurrent() {
    if (!current) {
      return;
    }

    const date = parseDate(current.fields.date, current.section);
    const status = normalizeStatus(current.fields.status || inferStatus(current.section));
    const searchText = [
      current.id,
      current.title,
      current.section,
      date || '',
      status,
      ...Object.values(current.fields),
      ...current.notes,
    ]
      .join(' ')
      .toLowerCase();

    decisions.push({
      ...current,
      date,
      status,
      searchText,
      order: decisions.length,
    });

    current = null;
    currentField = null;
  }

  for (const line of lines) {
    const sectionMatch = line.match(/^##\s+(.+)$/);
    if (sectionMatch) {
      finalizeCurrent();
      currentSection = sectionMatch[1].trim();
      continue;
    }

    const decisionMatch = line.match(/^###\s+(D-\d+):\s*(.+)$/);
    if (decisionMatch) {
      finalizeCurrent();
      current = {
        id: decisionMatch[1],
        title: decisionMatch[2].trim(),
        section: currentSection,
        fields: {},
        notes: [],
      };
      currentField = null;
      continue;
    }

    if (!current) {
      continue;
    }

    const fieldMatch = line.match(/^- \*\*(.+?):\*\*\s*(.*)$/);
    if (fieldMatch) {
      currentField = normalizeFieldName(fieldMatch[1]);
      current.fields[currentField] = fieldMatch[2].trim();
      continue;
    }

    if (currentField && line.trim() && !/^###\s+/.test(line) && !/^##\s+/.test(line) && !/^- \*\*.+?:\*\*/.test(line)) {
      current.fields[currentField] = `${current.fields[currentField]} ${line.trim()}`.trim();
      continue;
    }

    if (line.trim()) {
      current.notes.push(line.trim());
    }
  }

  finalizeCurrent();
  return decisions;
}

function compareDecisions(left, right) {
  const leftTime = left.date ? Date.parse(left.date) : Number.NEGATIVE_INFINITY;
  const rightTime = right.date ? Date.parse(right.date) : Number.NEGATIVE_INFINITY;

  if (leftTime !== rightTime) {
    return rightTime - leftTime;
  }

  return left.order - right.order;
}

function monthKey(date) {
  return date ? date.slice(0, 7) : 'no-date';
}

function monthLabel(key) {
  if (key === 'no-date') {
    return 'No date';
  }

  const [year, month] = key.split('-').map(Number);
  const labelDate = new Date(Date.UTC(year, month - 1, 1));
  return labelDate.toLocaleDateString('en-US', {
    month: 'long',
    year: 'numeric',
    timeZone: 'UTC',
  });
}

function statusColor(status) {
  switch (status) {
    case 'active':
      return ANSI.green;
    case 'superseded':
      return ANSI.yellow;
    case 'archived':
      return ANSI.gray;
    case 'recorded':
      return ANSI.blue;
    default:
      return ANSI.magenta;
  }
}

function printTimeline(decisions, options) {
  console.log(paint('Decision Timeline', ANSI.bold, ANSI.cyan));
  console.log(paint(`Source: ${decisionsPath}`, ANSI.dim));

  const filters = [];
  if (options.search) {
    filters.push(`search=${JSON.stringify(options.search)}`);
  }
  if (options.last) {
    filters.push(`last=${options.last}`);
  }
  if (filters.length > 0) {
    console.log(paint(`Filters: ${filters.join(', ')}`, ANSI.dim));
  }

  if (decisions.length === 0) {
    console.log(`\n${paint('No decisions matched.', ANSI.yellow)}`);
    console.log(`\n${paint('Summary', ANSI.bold)}`);
    console.log(`  ${paint('Total', ANSI.cyan)}: 0`);
    return;
  }

  const groups = new Map();
  for (const decision of decisions) {
    const key = monthKey(decision.date);
    const bucket = groups.get(key) || [];
    bucket.push(decision);
    groups.set(key, bucket);
  }

  for (const [key, group] of groups) {
    console.log(`\n${paint(monthLabel(key), ANSI.bold, ANSI.cyan)}`);
    for (const decision of group) {
      const dateLabel = decision.date || 'no-date';
      const statusLabel = `[${decision.status}]`;
      const line = [
        `  ${paint(pad(decision.id, 7), ANSI.bold, ANSI.cyan)}`,
        paint(pad(dateLabel, 10), ANSI.dim),
        decision.title,
        paint(statusLabel, statusColor(decision.status)),
      ].join(' ');
      console.log(line);
    }
  }

  const byStatus = new Map();
  for (const decision of decisions) {
    byStatus.set(decision.status, (byStatus.get(decision.status) || 0) + 1);
  }

  console.log(`\n${paint('Summary', ANSI.bold)}`);
  console.log(`  ${paint('Total', ANSI.cyan)}: ${decisions.length}`);
  for (const [status, count] of [...byStatus.entries()].sort((a, b) => a[0].localeCompare(b[0]))) {
    console.log(`  ${paint(status, statusColor(status))}: ${count}`);
  }
}

function main() {
  const options = parseArgs(process.argv.slice(2));
  const markdown = fs.readFileSync(decisionsPath, 'utf8');
  const allDecisions = parseDecisions(markdown).sort(compareDecisions);

  let filtered = allDecisions;
  if (options.search) {
    const needle = options.search.toLowerCase();
    filtered = filtered.filter((decision) => decision.searchText.includes(needle));
  }

  if (options.last) {
    filtered = filtered.slice(0, options.last);
  }

  printTimeline(filtered, options);
}

try {
  main();
} catch (error) {
  const message = error instanceof Error ? error.message : String(error);
  console.log(paint('Decision timeline viewer could not complete.', ANSI.bold, ANSI.red));
  console.log(paint(message, ANSI.red));
}

process.exitCode = 0;
