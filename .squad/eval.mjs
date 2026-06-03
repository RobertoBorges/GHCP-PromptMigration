#!/usr/bin/env node
/**
 * Squad governance self-check for Ocean's Twelve — The Azure Heist.
 *
 * What this script validates:
 * - core governance files exist and reference the live 14-agent squad
 * - all 14 agent charters are present
 * - the 13 guided workflow prompts, 7 support/intake prompts, and 8 chatmodes use current names
 * - routing.md still contains the prompt map, auto-routing triggers, and phase gates
 * - scorecard, MCP guidance, portfolio, and use-case index stay aligned to the current control surface
 *
 * Run from repo root:
 *   node .squad/eval.mjs
 */

import { readFileSync, existsSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const root = join(__dirname, '..');

const agents = [
  'architect',
  'coder',
  'tester',
  'azure-specialist',
  'devops-engineer',
  'observability-engineer',
  'database-specialist',
  'performance-engineer',
  'security-auditor',
  'cost-engineer',
  'evaluator',
  'cutover-commander',
  'scribe',
  'presentation-specialist'
];

const guidedPrompts = [
  'QuickAssessment',
  'Phase0-Multi-repo-assessment',
  'Phase1-PlanAndAssess',
  'Phase2-MigrateCode',
  'DatabaseMigration',
  'Phase3-GenerateInfra',
  'SecurityHardening',
  'Phase4-DeployToAzure',
  'Phase5-SetupCICD',
  'Phase6-PostMigrationOps',
  'Phase-Rollback',
  'CostOptimization',
  'GetStatus'
];

const supportPrompts = [
  'InteractiveMigrationInterview',
  'QuickTriage',
  'TeamSkillAssessment',
  'Assess-ClassicASP-Migration',
  'Assess-DotNet-Upgrade',
  'Assess-WebForms-Migration',
  'Assess-WCF-Migration',
  'Assess-Java-Upgrade'
];

const chatmodes = [
  'Azure-Infrastructure',
  'Code-Migration-Modernization',
  'Cost-Optimization',
  'Debug-Migration',
  'Migration-Orchestrator',
  'Onboarding',
  'Quick-Assessment',
  'Security-Review'
];

const useCases = [
  '01-ASPClassicApp',
  '02-NetFramework30-ASPNET-WEB',
  '03-WCFNet35',
  '04-ContosoUniversityDiPS',
  '05-BookShop',
  '06-Java-API-BusReservation',
  '07-PartsUnlimited-aspnet45'
];

let pass = 0;
let fail = 0;
const fails = [];

const g = (s) => `\x1b[32m${s}\x1b[0m`;
const r = (s) => `\x1b[31m${s}\x1b[0m`;
const b = (s) => `\x1b[1m${s}\x1b[0m`;
const d = (s) => `\x1b[2m${s}\x1b[0m`;

function check(name, ok) {
  if (ok) {
    pass++;
    console.log(g(`  ✅ ${name}`));
    return;
  }

  fail++;
  fails.push(name);
  console.log(r(`  ❌ ${name}`));
}

function repoPath(...parts) {
  return join(root, ...parts);
}

function has(...parts) {
  return existsSync(repoPath(...parts));
}

function read(...parts) {
  const filePath = repoPath(...parts);
  return existsSync(filePath) ? readFileSync(filePath, 'utf-8') : '';
}

function fileCheck(parts, label) {
  check(label || parts.join('/'), has(...parts));
}

function contentCheck(parts, pattern, label) {
  check(label, pattern.test(read(...parts)));
}

const team = read('.squad', 'team.md');
const routing = read('.squad', 'routing.md');
const scorecard = read('.squad', 'SCORECARD.md');
const portfolio = read('PORTFOLIO.md');
const mcpConfig = read('.squad', 'mcp-config.md');

console.log(`\n${b("  Squad Governance Self-Check — Ocean's Twelve") }\n`);

console.log(d('  File Existence'));
for (const filePath of [
  ['AGENTS.md'],
  ['CLAUDE.md'],
  ['JOURNAL.md'],
  ['PORTFOLIO.md'],
  ['Use-cases', 'README.md'],
  ['.github', 'copilot-instructions.md'],
  ['.squad', 'team.md'],
  ['.squad', 'routing.md'],
  ['.squad', 'decisions.md'],
  ['.squad', 'SCORECARD.md'],
  ['.squad', 'eval.mjs'],
  ['.squad', 'mcp-config.md']
]) {
  fileCheck(filePath);
}
for (const agent of agents) {
  fileCheck(['.squad', 'agents', agent, 'charter.md'], `charter exists: ${agent}`);
}

console.log(d('\n  Squad Identity'));
contentCheck(['AGENTS.md'], /Ocean's Twelve|Ocean''s Twelve/i, 'AGENTS.md references Ocean\'s Twelve');
contentCheck(['CLAUDE.md'], /Ocean's Twelve|Ocean''s Twelve/i, 'CLAUDE.md references Ocean\'s Twelve');
check('team.md contains 14 active agents', (team.match(/\| \d+ \|/g) || []).length >= 14);
check('team.md contains all 7 targets', useCases.every((useCase) => team.includes(useCase)));
contentCheck(['.squad', 'SCORECARD.md'], /14-agent|14 agents/i, 'SCORECARD references 14-agent squad');
contentCheck(['.squad', 'SCORECARD.md'], /7 migration targets|7 use-cases|7 use cases/i, 'SCORECARD references 7 use-cases');
contentCheck(['.squad', 'SCORECARD.md'], /Phase Gate Compliance/i, 'SCORECARD includes phase gate section');
contentCheck(['PORTFOLIO.md'], /QuickAssessment/i, 'PORTFOLIO references QuickAssessment');
contentCheck(['PORTFOLIO.md'], /GetStatus/i, 'PORTFOLIO references GetStatus');
check('PORTFOLIO lists all 7 use-cases', useCases.every((useCase) => portfolio.includes(useCase)));
contentCheck(['.squad', 'mcp-config.md'], /chatmodes/i, 'MCP config mentions chatmodes');
contentCheck(['.squad', 'mcp-config.md'], /prompts/i, 'MCP config mentions prompts');

console.log(d('\n  Routing'));
contentCheck(['.squad', 'routing.md'], /## Work Type → Agent/i, 'routing work-type table exists');
contentCheck(['.squad', 'routing.md'], /## Prompt & Chatmode → Agent Dispatch Map/i, 'routing prompt map exists');
contentCheck(['.squad', 'routing.md'], /## Phase Quality Gates/i, 'routing phase gates exist');
contentCheck(['.squad', 'routing.md'], /## Auto-Routing Triggers/i, 'routing auto-routing triggers exist');
for (const agent of [
  'Architect',
  'Coder',
  'Tester',
  'Azure Specialist',
  'DevOps Engineer',
  'Observability Engineer',
  'Database Specialist',
  'Performance Engineer',
  'Security Auditor',
  'Cost Engineer',
  'Evaluator',
  'Cutover Commander',
  'Scribe',
  'Presentation Specialist'
]) {
  check(`routing references ${agent}`, routing.includes(agent));
}
for (const prompt of guidedPrompts) {
  check(`routing maps ${prompt}`, routing.includes(prompt));
}

console.log(d('\n  Prompt Catalog'));
for (const prompt of guidedPrompts) {
  fileCheck(['.github', 'prompts', `${prompt}.prompt.md`], `guided prompt exists: ${prompt}`);
}
for (const prompt of supportPrompts) {
  fileCheck(['.github', 'prompts', `${prompt}.prompt.md`], `support prompt exists: ${prompt}`);
}
for (const chatmode of chatmodes) {
  fileCheck(['.github', 'chatmodes', `${chatmode}.chatmode.md`], `chatmode exists: ${chatmode}`);
}

console.log(d('\n  Governance Surfaces'));
contentCheck(['.squad', 'SCORECARD.md'], /Agent Coverage per Use-Case/i, 'SCORECARD includes use-case coverage section');
contentCheck(['.squad', 'SCORECARD.md'], /Prompt Quality Metrics/i, 'SCORECARD includes prompt metrics section');
contentCheck(['.squad', 'SCORECARD.md'], /Skill Coverage/i, 'SCORECARD includes skill coverage section');
contentCheck(['PORTFOLIO.md'], /Current portfolio status/i, 'PORTFOLIO includes status snapshot');
contentCheck(['Use-cases', 'README.md'], /docs\\walkthroughs/i, 'Use-cases README points to walkthroughs');
contentCheck(['Use-cases', 'README.md'], /docs\\use-case-cheatsheets/i, 'Use-cases README points to cheatsheets');

console.log(d('\n  Charter Quality'));
for (const agent of agents) {
  const charter = read('.squad', 'agents', agent, 'charter.md');
  check(`${agent}: Identity section`, /## Identity/.test(charter));
  check(`${agent}: How I Work section`, /## How I Work/.test(charter));
  check(`${agent}: Voice section`, /## Voice/.test(charter));
}

const total = pass + fail;
const rate = total > 0 ? ((pass / total) * 100).toFixed(0) : '0';
const icon = fail === 0 ? g('PASS ✅') : r('FAIL ❌');

console.log(`\n${b(`  ${pass}/${total} checks (${rate}%) — ${icon}`)}\n`);
if (fails.length) {
  console.log(r('  Failed:'));
  for (const failure of fails) {
    console.log(r(`    - ${failure}`));
  }
  console.log('');
}

process.exit(fail > 0 ? 1 : 0);
