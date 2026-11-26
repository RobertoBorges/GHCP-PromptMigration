/**
 * Validate discoverable Agent Skill metadata and prompt/chatmode file links.
 */

import { promises as fs } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const repoRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const referenceDirs = ['.github'];
const skillsDir = path.join(repoRoot, '.github', 'skills');
const problems = [];

async function* walkMarkdown(dir) {
  for (const entry of await fs.readdir(dir, { withFileTypes: true })) {
    const file = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      yield* walkMarkdown(file);
    } else if (entry.isFile() && entry.name.endsWith('.md')) {
      yield file;
    }
  }
}

for (const relativeDir of referenceDirs) {
  const directory = path.join(repoRoot, relativeDir);
  try {
    await fs.access(directory);
  } catch (error) {
    if (error.code === 'ENOENT') continue;
    throw error;
  }
  for await (const file of walkMarkdown(directory)) {
    const content = await fs.readFile(file, 'utf8');
    const pattern = /#file:([A-Za-z0-9._/-]+)/g;
    for (const match of content.matchAll(pattern)) {
      const reference = match[1];
      const relativeFile = path.relative(repoRoot, file);
      if (reference.startsWith('skills/')) {
        problems.push(`${relativeFile}: root skills/ reference is not shipped by the extension: ${reference}`);
        continue;
      }
      if (!reference.startsWith('.github/')) {
        problems.push(`${relativeFile}: unsupported #file path: ${reference}`);
        continue;
      }

      const target = path.join(repoRoot, ...reference.split('/'));
      try {
        const stat = await fs.stat(target);
        if (!stat.isFile()) {
          problems.push(`${relativeFile}: #file target is not a file: ${reference}`);
        }
      } catch (error) {
        if (error.code !== 'ENOENT') throw error;
        problems.push(`${relativeFile}: #file target does not exist: ${reference}`);
      }
    }
  }
}

for (const entry of await fs.readdir(skillsDir, { withFileTypes: true })) {
  if (!entry.isDirectory()) continue;

  const skillName = entry.name;
  const skillFile = path.join(skillsDir, skillName, 'SKILL.md');
  let content;
  try {
    content = await fs.readFile(skillFile, 'utf8');
  } catch (error) {
    if (error.code !== 'ENOENT') throw error;
    problems.push(`.github/skills/${skillName}/: missing SKILL.md`);
    continue;
  }

  const frontmatter = content.match(/^---\s*\r?\n([\s\S]*?)\r?\n---/);
  if (!frontmatter) {
    problems.push(`.github/skills/${skillName}/SKILL.md: missing YAML frontmatter`);
    continue;
  }

  const declaredName = frontmatter[1].match(/^name:\s*(.+?)\s*$/m)?.[1];
  const description = frontmatter[1].match(/^description:\s*(.*?)\s*$/m)?.[1];
  const hasBlockDescription = /^[|>][+-]?$/.test(description ?? '')
    && /^description:\s*[|>][+-]?\s*\r?\n(?:[ \t]+[^\r\n]*\r?\n?)+/m.test(frontmatter[1]);
  if (declaredName !== skillName) {
    problems.push(`.github/skills/${skillName}/SKILL.md: name must match directory (${skillName})`);
  }
  if ((!description || /^[|>][+-]?$/.test(description)) && !hasBlockDescription) {
    problems.push(`.github/skills/${skillName}/SKILL.md: description must be present in frontmatter`);
  }
}

if (problems.length > 0) {
  console.error('✗ Agent content validation failed:');
  for (const problem of problems) console.error(`  - ${problem}`);
  process.exit(1);
}

console.log('✓ Agent Skill metadata and .github file references are valid.');
