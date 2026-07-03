/**
 * Parser for reports/Decisions-Required.md (the Wave H artifact).
 *
 * Returns a structured representation that tree views and the status bar can
 * render. Tolerant of formatting variations — looks for the H2 "Decision N:"
 * heading and the "Status:" line to extract each decision.
 *
 * Schema mirrors .github/skills/decisions-required-template.md.
 */

import * as fs from 'node:fs';
import * as path from 'node:path';

export type DecisionStatus = 'pending' | 'decided' | 'locked' | 'na' | 'unknown';

export interface Decision {
  /** Numeric ID from the section heading (1, 2, 3, ...). May be a catalog ID like "D-04" if present in line. */
  id: string;
  /** Decision name from the heading (everything after "Decision N:"). */
  name: string;
  /** Parsed status. */
  status: DecisionStatus;
  /** Raw status text (e.g., "✅ DECIDED 2026-06-25"). */
  statusText: string;
  /** Required-for phase if found. */
  requiredFor?: string;
  /** Line number where the decision section starts (1-indexed). Used for open-at-line. */
  line: number;
}

export interface DecisionsFileSummary {
  filePath: string;
  exists: boolean;
  decisions: Decision[];
  pending: number;
  decided: number;
  locked: number;
  na: number;
  unknown: number;
  parseError?: string;
}

/**
 * Parse `reports/Decisions-Required.md` for the given workspace root.
 * Returns a summary even when the file is missing — callers check `.exists`.
 */
export function parseDecisionsFile(workspaceRoot: string): DecisionsFileSummary {
  const filePath = path.join(workspaceRoot, 'reports', 'Decisions-Required.md');
  const empty = (): DecisionsFileSummary => ({
    filePath,
    exists: false,
    decisions: [],
    pending: 0,
    decided: 0,
    locked: 0,
    na: 0,
    unknown: 0,
  });

  if (!fs.existsSync(filePath)) {
    return empty();
  }

  let content: string;
  try {
    content = fs.readFileSync(filePath, 'utf-8');
  } catch (err) {
    return { ...empty(), exists: true, parseError: `Failed to read file: ${(err as Error).message}` };
  }

  return parseDecisions(content, filePath);
}

/**
 * Parse decisions from already-loaded markdown content. Exported for tests.
 */
export function parseDecisions(content: string, filePath = ''): DecisionsFileSummary {
  const lines = content.split(/\r?\n/);
  const decisions: Decision[] = [];

  // Pattern: ## Decision <id>: <name>
  // id can be: a number (1, 2, 3) or a catalog ID like "D-04"
  const headingRe = /^##\s+Decision\s+(D-\d{2}|\d+)\s*[:\-]\s*(.+?)\s*$/i;

  let current: Partial<Decision> | null = null;
  let currentStartLine = 0;

  function commit() {
    if (current && current.name && current.id !== undefined) {
      decisions.push({
        id: String(current.id),
        name: current.name,
        status: current.status ?? 'unknown',
        statusText: current.statusText ?? '',
        requiredFor: current.requiredFor,
        line: currentStartLine,
      });
    }
    current = null;
  }

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    const headingMatch = line.match(headingRe);

    if (headingMatch) {
      // New decision starts — commit previous if any.
      commit();
      current = { id: headingMatch[1], name: headingMatch[2].trim() };
      currentStartLine = i + 1;
      continue;
    }

    if (!current) continue;

    // Status line — bold marker, very forgiving.
    const statusMatch = line.match(/^\*\*Status:\*\*\s+(.+?)\s*$/i);
    if (statusMatch && current.status === undefined) {
      const raw = statusMatch[1].trim();
      current.statusText = raw;
      current.status = parseStatusText(raw);
      continue;
    }

    // Required-for line.
    const requiredMatch = line.match(/^\*\*Required\s+for:\*\*\s+(.+?)\s*$/i);
    if (requiredMatch && current.requiredFor === undefined) {
      current.requiredFor = requiredMatch[1].trim();
      continue;
    }

    // Next H2 means we've left this decision (commit handled at top of loop).
    // No-op here.
  }

  commit();

  const counts = {
    pending: 0,
    decided: 0,
    locked: 0,
    na: 0,
    unknown: 0,
  };
  for (const d of decisions) {
    counts[d.status]++;
  }

  return {
    filePath,
    exists: true,
    decisions,
    ...counts,
  };
}

/**
 * Map free-text status to enum. Tolerates emoji presence/absence and
 * case variations.
 */
function parseStatusText(raw: string): DecisionStatus {
  const lower = raw.toLowerCase();
  if (lower.includes('pending') || lower.includes('⏸')) return 'pending';
  if (lower.includes('decided') || lower.includes('✅')) return 'decided';
  if (lower.includes('locked') || lower.includes('🔒')) return 'locked';
  if (lower.includes('n/a') || lower.includes('🚫')) return 'na';
  return 'unknown';
}
