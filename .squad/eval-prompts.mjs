#!/usr/bin/env node

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const repoRoot = path.resolve(__dirname, '..');
const promptsDir = path.join(repoRoot, '.github', 'prompts');

const testCases = [
  {
    name: 'QuickAssessment',
    promptFile: 'QuickAssessment.prompt.md',
    sampleInput: 'Assess a .NET Framework 3.0 WebForms app with SQL Server',
    expectedMentions: [
      { label: 'complexity rating', keywords: ['complexity score', 'complexity rating'] },
      { label: 'target platform', keywords: ['target azure platform', 'target platform', 'landing zone', 'azure target services'] },
      { label: 'recommended phases', keywords: ['recommended migration phases', 'phase 1 plan and assess', 'phased migration tracks'] },
      { label: '@squad next command', keywords: ['@squad run phase 1 plan and assess', '@squad show migration status', '@squad run database migration review'] },
    ],
    requiredSections: ['## Agent Role', '## Deliverables', '## Completion Guidance', '## Output Checklist'],
  },
  {
    name: 'SecurityHardening',
    promptFile: 'SecurityHardening.prompt.md',
    sampleInput: 'Harden a containerized .NET 8 app on Azure Container Apps',
    expectedMentions: [
      { label: 'auth', keywords: ['authentication', 'authorization', 'auth'] },
      { label: 'secrets', keywords: ['secret', 'key vault'] },
      { label: 'RBAC', keywords: ['rbac', 'least privilege'] },
      { label: 'network', keywords: ['network security', 'private endpoint', 'firewall', 'nsg'] },
      { label: 'OWASP', keywords: ['owasp'] },
    ],
    requiredSections: ['## Agent Role', '## Step 2: Perform OWASP Top 10 Review', '## Deliverables', '## Output Checklist'],
  },
  {
    name: 'GetStatus',
    promptFile: 'GetStatus.prompt.md',
    sampleInput: 'Show migration status for Contoso University',
    expectedMentions: [
      { label: 'current phase', keywords: ['current phase'] },
      { label: 'blocker', keywords: ['blocker', 'blocking issues'] },
      { label: 'owner', keywords: ['owner', 'assignee'] },
      { label: 'next step', keywords: ['next recommended step', 'next step', 'specific command'] },
    ],
    requiredSections: ['## Agent Role', '# Rules for Status Tracking', '## Output Checklist'],
  },
];

function readText(filePath) {
  return fs.readFileSync(filePath, 'utf8');
}

function extractFrontmatter(text) {
  const match = text.match(/^---\r?\n([\s\S]*?)\r?\n---(?:\r?\n|$)/);
  if (!match) {
    return null;
  }

  return {
    raw: match[1],
    body: text.slice(match[0].length),
  };
}

function hasSimpleField(frontmatter, field) {
  return new RegExp(`(^|\\n)${field}\\s*:`, 'm').test(frontmatter.raw);
}

function hasToolsArray(frontmatter) {
  const lines = frontmatter.raw.split(/\r?\n/);

  for (let index = 0; index < lines.length; index += 1) {
    const line = lines[index];
    const match = line.match(/^tools\s*:\s*(.*)$/);
    if (!match) {
      continue;
    }

    const inlineValue = match[1].trim();
    if (inlineValue.startsWith('[') && inlineValue.endsWith(']')) {
      return true;
    }

    if (inlineValue === '') {
      for (let follow = index + 1; follow < lines.length; follow += 1) {
        const nextLine = lines[follow];
        if (/^\s*-\s+/.test(nextLine)) {
          return true;
        }
        if (/^[A-Za-z0-9_-]+\s*:/.test(nextLine)) {
          break;
        }
      }
    }

    return false;
  }

  return false;
}

function extractFileReferences(content) {
  return [...content.matchAll(/#file:([^`\s)]+)/g)].map((match) => match[1]);
}

function resolveRef(ref) {
  return path.resolve(repoRoot, ...ref.split('/'));
}

function includesAnyKeyword(body, keywords) {
  const lowerBody = body.toLowerCase();
  return keywords.some((keyword) => lowerBody.includes(keyword.toLowerCase()));
}

function check(label, passed, details) {
  return { label, passed, details };
}

function pad(value, width) {
  return String(value).padEnd(width, ' ');
}

function makeTable(rows) {
  const headers = ['Test Case', 'Checks', 'Pass', 'Fail', 'Score', 'Result'];
  const widths = headers.map((header, index) => Math.max(header.length, ...rows.map((row) => String(row[index]).length)));
  const line = `+-${widths.map((width) => '-'.repeat(width)).join('-+-')}-+`;
  const headerRow = `| ${headers.map((header, index) => pad(header, widths[index])).join(' | ')} |`;
  const bodyRows = rows.map((row) => `| ${row.map((value, index) => pad(value, widths[index])).join(' | ')} |`);
  return [line, headerRow, line, ...bodyRows, line].join('\n');
}

const summaries = [];
let overallPass = true;

console.log('Static Prompt Eval Harness');
console.log('Validates structure only; no model calls are made.\n');

for (const testCase of testCases) {
  const promptPath = path.join(promptsDir, testCase.promptFile);
  const checks = [];

  checks.push(check('prompt file exists', fs.existsSync(promptPath), testCase.promptFile));

  if (fs.existsSync(promptPath)) {
    const content = readText(promptPath);
    const frontmatter = extractFrontmatter(content);
    const body = frontmatter?.body ?? '';
    const refs = extractFileReferences(body);
    const missingRefs = refs.filter((ref) => !fs.existsSync(resolveRef(ref)));

    checks.push(check('frontmatter parses', Boolean(frontmatter), frontmatter ? 'ok' : 'missing or malformed'));

    if (frontmatter) {
      checks.push(check('frontmatter has agent', hasSimpleField(frontmatter, 'agent'), 'agent'));
      checks.push(check('frontmatter has model', hasSimpleField(frontmatter, 'model'), 'model'));
      checks.push(check('frontmatter has tools', hasToolsArray(frontmatter), 'tools'));
      checks.push(check('frontmatter has description', hasSimpleField(frontmatter, 'description'), 'description'));
    }

    checks.push(
      check(
        '#file references resolve',
        missingRefs.length === 0,
        missingRefs.length === 0 ? `${refs.length} reference(s)` : `missing: ${missingRefs.join(', ')}`,
      ),
    );

    for (const section of testCase.requiredSections) {
      checks.push(check(`contains section: ${section}`, body.includes(section), section));
    }

    for (const expected of testCase.expectedMentions) {
      checks.push(
        check(
          `covers expected output: ${expected.label}`,
          includesAnyKeyword(body, expected.keywords),
          expected.keywords.join(' | '),
        ),
      );
    }
  }

  const passed = checks.filter((item) => item.passed).length;
  const failed = checks.length - passed;
  const score = checks.length === 0 ? 0 : Math.round((passed / checks.length) * 100);
  const result = failed === 0 ? 'PASS' : 'FAIL';
  overallPass = overallPass && failed === 0;

  summaries.push([testCase.name, checks.length, passed, failed, `${score}%`, result]);

  console.log(`- ${testCase.name}`);
  console.log(`  Sample input: ${testCase.sampleInput}`);
  for (const item of checks) {
    const icon = item.passed ? 'PASS' : 'FAIL';
    console.log(`  [${icon}] ${item.label}`);
    if (!item.passed && item.details) {
      console.log(`         ${item.details}`);
    }
  }
  console.log('');
}

console.log(makeTable(summaries));

const totalChecks = summaries.reduce((sum, row) => sum + Number(row[1]), 0);
const totalPassed = summaries.reduce((sum, row) => sum + Number(row[2]), 0);
const totalFailed = summaries.reduce((sum, row) => sum + Number(row[3]), 0);
const totalScore = totalChecks === 0 ? 0 : Math.round((totalPassed / totalChecks) * 100);

console.log(`\nOverall: ${totalPassed}/${totalChecks} checks passed (${totalScore}%)`);

process.exit(overallPass ? 0 : 1);
