#!/usr/bin/env node

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const repoRoot = path.resolve(__dirname, '..');
const promptsDir = path.join(repoRoot, '.github', 'prompts');
const chatmodesDir = path.join(repoRoot, '.github', 'chatmodes');
const githubSkillsDir = path.join(repoRoot, '.github', 'skills');

const REQUIRED_FIELDS = ['agent', 'model', 'tools', 'description'];
const EXEMPT_HOOK_PROMPTS = new Set([
  'InteractiveMigrationInterview.prompt.md',
  'TeamSkillAssessment.prompt.md',
]);
const STALE_CLI_PATTERN = /\/phase[0-9]\b|\/getstatus\b|\/securityhardening\b|\/costoptimization\b|\/databasemigration\b/i;
const ALLOWED_STALE_HEADINGS = /when to use|run it with|prompt catalog|actual prompt triggers|trigger descriptions?|entry prompts?/i;
const GUIDANCE_HEADINGS = /next steps?|completion|complete|follow-?through|handoff|closing|final steps?|recommended next/i;
const GUIDANCE_LINES = /next steps?|after (this|that|completion)|follow-?through|recommended next|recommended command|then run|from here|continue with/i;

function toPosix(filePath) {
  return filePath.replace(/\\/g, '/');
}

function relativePath(filePath) {
  return toPosix(path.relative(repoRoot, filePath));
}

function readText(filePath) {
  return fs.readFileSync(filePath, 'utf8');
}

function listMarkdownFiles(dirPath, suffix) {
  return fs
    .readdirSync(dirPath)
    .filter((name) => name.endsWith(suffix))
    .map((name) => path.join(dirPath, name))
    .sort((a, b) => a.localeCompare(b));
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

function extractSkillReferences(content) {
  const matches = [...content.matchAll(/#file:((?:\.github\/skills|skills)\/[^`\s)]+\.md)/g)];
  return matches.map((match) => ({
    ref: match[1],
    absolutePath: path.join(repoRoot, ...match[1].split('/')),
  }));
}

function hasHookReference(content, hookPath) {
  return content.includes(`#file:${hookPath}`);
}

function detectStaleCliPatterns(content, filePath) {
  const findings = [];
  const lines = content.split(/\r?\n/);
  let currentHeading = '';
  let inFence = false;
  const recentLines = [];

  for (let index = 0; index < lines.length; index += 1) {
    const rawLine = lines[index];
    const line = rawLine.trim();

    if (/^```/.test(line)) {
      inFence = !inFence;
      continue;
    }

    if (/^#{1,6}\s+/.test(line)) {
      currentHeading = line.replace(/^#{1,6}\s+/, '').trim();
    }

    recentLines.push(line);
    if (recentLines.length > 4) {
      recentLines.shift();
    }

    if (inFence || !STALE_CLI_PATTERN.test(line)) {
      continue;
    }

    if (/^entryPrompts\s*:/.test(line)) {
      continue;
    }

    const contextSample = recentLines.join(' ').trim();
    const allowedContext = ALLOWED_STALE_HEADINGS.test(currentHeading) || ALLOWED_STALE_HEADINGS.test(contextSample);
    const guidanceContext = GUIDANCE_HEADINGS.test(currentHeading) || GUIDANCE_LINES.test(contextSample);

    if (allowedContext || !guidanceContext) {
      continue;
    }

    findings.push({
      file: relativePath(filePath),
      line: index + 1,
      heading: currentHeading || '(no heading)',
      text: line,
    });
  }

  return findings;
}

function statusLine(icon, message) {
  return `  ${icon} ${message}`;
}

function sectionTitle(title) {
  console.log(`\n${title}`);
}

const promptFiles = listMarkdownFiles(promptsDir, '.prompt.md');
const chatmodeFiles = listMarkdownFiles(chatmodesDir, '.chatmode.md');
const githubSkillFiles = listMarkdownFiles(githubSkillsDir, '.md');

const errors = [];
const warnings = [];

const promptFrontmatterValid = [];
const promptHookOk = [];
const promptHookMissing = [];
const promptBrokenSkillRefs = [];
const promptRootSkillRefs = [];
const referencedGithubSkills = new Set();
const promptStalePatterns = [];
const chatmodeFrontmatterValid = [];
const chatmodeStalePatterns = [];

for (const promptFile of promptFiles) {
  const fileName = path.basename(promptFile);
  const displayName = fileName.replace(/\.prompt\.md$/, '');
  const content = readText(promptFile);
  const frontmatter = extractFrontmatter(content);

  if (!frontmatter) {
    errors.push(`${displayName}: missing YAML frontmatter`);
  } else {
    const missingFields = [];
    for (const field of REQUIRED_FIELDS) {
      if (field === 'tools') {
        if (!hasToolsArray(frontmatter)) {
          missingFields.push('tools (array)');
        }
      } else if (!hasSimpleField(frontmatter, field)) {
        missingFields.push(field);
      }
    }

    if (missingFields.length > 0) {
      errors.push(`${displayName}: missing frontmatter fields -> ${missingFields.join(', ')}`);
    } else {
      promptFrontmatterValid.push(promptFile);
    }

    const body = frontmatter.body;
    const skillRefs = extractSkillReferences(body);
    for (const skillRef of skillRefs) {
      if (!fs.existsSync(skillRef.absolutePath)) {
        promptBrokenSkillRefs.push(`${displayName}: ${skillRef.ref}`);
        errors.push(`${displayName}: broken skill reference -> ${skillRef.ref}`);
        continue;
      }

      if (skillRef.ref.startsWith('skills/')) {
        promptRootSkillRefs.push(`${displayName}: ${skillRef.ref}`);
        warnings.push(`${displayName}: root skill reference should use .github/skills -> ${skillRef.ref}`);
      } else {
        referencedGithubSkills.add(path.basename(skillRef.absolutePath));
      }
    }

    const hasPhaseGate = hasHookReference(body, '.github/hooks/phase-gates.md');
    const hasAgentDispatch = hasHookReference(body, '.github/hooks/agent-dispatch.md');
    if (EXEMPT_HOOK_PROMPTS.has(fileName)) {
      promptHookOk.push(promptFile);
    } else if (hasPhaseGate && hasAgentDispatch) {
      promptHookOk.push(promptFile);
    } else {
      const missingHooks = [];
      if (!hasPhaseGate) {
        missingHooks.push('phase-gates');
      }
      if (!hasAgentDispatch) {
        missingHooks.push('agent-dispatch');
      }
      const message = `${displayName}: missing hook reference(s) -> ${missingHooks.join(', ')}`;
      promptHookMissing.push(message);
      warnings.push(message);
    }

    promptStalePatterns.push(...detectStaleCliPatterns(body, promptFile));
  }
}

for (const chatmodeFile of chatmodeFiles) {
  const fileName = path.basename(chatmodeFile);
  const displayName = fileName.replace(/\.chatmode\.md$/, '');
  const content = readText(chatmodeFile);
  const frontmatter = extractFrontmatter(content);

  if (!frontmatter) {
    errors.push(`${displayName}: missing YAML frontmatter`);
  } else {
    const missingFields = [];
    for (const field of REQUIRED_FIELDS) {
      if (field === 'tools') {
        if (!hasToolsArray(frontmatter)) {
          missingFields.push('tools (array)');
        }
      } else if (!hasSimpleField(frontmatter, field)) {
        missingFields.push(field);
      }
    }

    if (missingFields.length > 0) {
      errors.push(`${displayName}: missing frontmatter fields -> ${missingFields.join(', ')}`);
    } else {
      chatmodeFrontmatterValid.push(chatmodeFile);
    }

    chatmodeStalePatterns.push(...detectStaleCliPatterns(frontmatter.body, chatmodeFile));
  }
}

for (const finding of promptStalePatterns) {
  warnings.push(`stale CLI pattern in ${finding.file}:${finding.line}`);
}
for (const finding of chatmodeStalePatterns) {
  warnings.push(`stale CLI pattern in ${finding.file}:${finding.line}`);
}

const unreferencedGithubSkills = githubSkillFiles
  .map((filePath) => path.basename(filePath))
  .filter((fileName) => !referencedGithubSkills.has(fileName));

for (const skillName of unreferencedGithubSkills) {
  warnings.push(`unreferenced .github skill -> ${skillName}`);
}

console.log('🔍 Prompt Linter — Ocean\'s Twelve');
console.log('═══════════════════════════════════');

sectionTitle(`📋 Prompts (${promptFiles.length} files)`);
if (promptFrontmatterValid.length === promptFiles.length) {
  console.log(statusLine('✅', `${promptFrontmatterValid.length}/${promptFiles.length} have valid YAML frontmatter`));
} else {
  console.log(statusLine('❌', `${promptFrontmatterValid.length}/${promptFiles.length} have valid YAML frontmatter`));
}

const expectedHookCount = promptFiles.length;
if (promptHookMissing.length === 0) {
  console.log(statusLine('✅', `${promptHookOk.length}/${expectedHookCount} reference hooks (2 exempt: InteractiveMigrationInterview, TeamSkillAssessment)`));
} else {
  console.log(statusLine('⚠️', `${promptHookOk.length}/${expectedHookCount} reference hooks (${promptHookMissing.length} missing, 2 exempt: InteractiveMigrationInterview, TeamSkillAssessment)`));
  for (const item of promptHookMissing) {
    console.log(`     - ${item}`);
  }
}

if (promptBrokenSkillRefs.length === 0) {
  console.log(statusLine('✅', '0 broken skill references'));
} else {
  console.log(statusLine('❌', `${promptBrokenSkillRefs.length} broken skill reference(s)`));
  for (const item of promptBrokenSkillRefs) {
    console.log(`     - ${item}`);
  }
}

if (promptStalePatterns.length === 0) {
  console.log(statusLine('✅', '0 stale CLI patterns found'));
} else {
  console.log(statusLine('⚠️', `${promptStalePatterns.length} stale CLI pattern(s) found`));
  for (const finding of promptStalePatterns) {
    console.log(`     - ${finding.file}:${finding.line} [${finding.heading}] ${finding.text}`);
  }
}

sectionTitle(`🎭 Chatmodes (${chatmodeFiles.length} files)`);
if (chatmodeFrontmatterValid.length === chatmodeFiles.length) {
  console.log(statusLine('✅', `${chatmodeFrontmatterValid.length}/${chatmodeFiles.length} have valid YAML frontmatter`));
} else {
  console.log(statusLine('❌', `${chatmodeFrontmatterValid.length}/${chatmodeFiles.length} have valid YAML frontmatter`));
}

if (chatmodeStalePatterns.length === 0) {
  console.log(statusLine('✅', '0 stale CLI patterns found'));
} else {
  console.log(statusLine('⚠️', `${chatmodeStalePatterns.length} stale CLI pattern(s) found`));
  for (const finding of chatmodeStalePatterns) {
    console.log(`     - ${finding.file}:${finding.line} [${finding.heading}] ${finding.text}`);
  }
}

sectionTitle(`📚 Skills (${githubSkillFiles.length} files in .github/skills/)`);
console.log(statusLine('✅', `${githubSkillFiles.length}/${githubSkillFiles.length} exist on disk`));
console.log(statusLine('✅', `${referencedGithubSkills.size}/${githubSkillFiles.length} referenced by at least one prompt`));
if (unreferencedGithubSkills.length === 0) {
  console.log(statusLine('✅', '0 unreferenced .github skills'));
} else {
  console.log(statusLine('⚠️', `${unreferencedGithubSkills.length} unreferenced: ${unreferencedGithubSkills.join(', ')}`));
}

sectionTitle('🔗 Cross-references');
if (promptBrokenSkillRefs.length === 0) {
  console.log(statusLine('✅', 'All prompt skill references resolve'));
} else {
  console.log(statusLine('❌', 'Some prompt skill references do not resolve'));
}

if (promptRootSkillRefs.length === 0) {
  console.log(statusLine('✅', '0 root-path references remaining'));
} else {
  console.log(statusLine('⚠️', `${promptRootSkillRefs.length} root-path reference(s) remaining`));
  for (const item of promptRootSkillRefs) {
    console.log(`     - ${item}`);
  }
}

console.log('\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
const warningCount = warnings.length;
const result = errors.length > 0 ? '❌ FAIL' : '✅ PASS';
console.log(`Result: ${result} (${warningCount} warning${warningCount === 1 ? '' : 's'})`);

if (errors.length > 0) {
  console.log('\nErrors:');
  for (const error of errors) {
    console.log(`  - ${error}`);
  }
}

process.exit(errors.length > 0 ? 1 : 0);
