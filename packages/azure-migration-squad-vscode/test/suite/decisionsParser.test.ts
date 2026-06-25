/**
 * Unit tests for decisionsParser.
 *
 * Pure logic — uses inline markdown fixtures, no filesystem dependency.
 */

import * as assert from 'assert';
import { parseDecisions } from '../../src/util/decisionsParser';

const SAMPLE_FILE = `
# Decisions Required — Demo App

> Generated 2026-06-25

## Status summary

| # | Decision | Status |
|---|----------|--------|
| 1 | Target framework | ⏸ PENDING |
| 2 | Database engine | ✅ DECIDED |

---

## Decision 1: Target framework / runtime version

**Status:** ⏸ PENDING
**Required for:** Phase 2 — Migrate Code

Body...

## Decision 2: Database engine

**Status:** ✅ DECIDED 2026-06-25
**Required for:** Phase 2 + DatabaseMigration

Choice: Azure SQL.

## Decision 3: Database migration tool

**Status:** 🔒 LOCKED — Determined by Decision 2 (Azure SQL → DMS).
**Required for:** DatabaseMigration

## Decision 4: UI architecture

**Status:** 🚫 N/A — Workload is API-only

## Decision D-05: IaC tool

**Status:** ⏸ PENDING

## Decision 6: something with weird status

**Status:** wat
`;

suite('decisionsParser.parseDecisions', () => {
  test('Extracts all decision sections', () => {
    const result = parseDecisions(SAMPLE_FILE);
    assert.strictEqual(result.exists, true);
    assert.strictEqual(result.decisions.length, 6);
  });

  test('Captures status types correctly', () => {
    const result = parseDecisions(SAMPLE_FILE);
    const byId = Object.fromEntries(result.decisions.map((d) => [d.id, d]));
    assert.strictEqual(byId['1'].status, 'pending');
    assert.strictEqual(byId['2'].status, 'decided');
    assert.strictEqual(byId['3'].status, 'locked');
    assert.strictEqual(byId['4'].status, 'na');
    assert.strictEqual(byId['D-05'].status, 'pending');
    assert.strictEqual(byId['6'].status, 'unknown');
  });

  test('Captures required-for', () => {
    const result = parseDecisions(SAMPLE_FILE);
    const d1 = result.decisions.find((d) => d.id === '1');
    assert.strictEqual(d1?.requiredFor, 'Phase 2 — Migrate Code');
  });

  test('Tally counts each status', () => {
    const result = parseDecisions(SAMPLE_FILE);
    assert.strictEqual(result.pending, 2);
    assert.strictEqual(result.decided, 1);
    assert.strictEqual(result.locked, 1);
    assert.strictEqual(result.na, 1);
    assert.strictEqual(result.unknown, 1);
  });

  test('Captures line numbers', () => {
    const result = parseDecisions(SAMPLE_FILE);
    for (const d of result.decisions) {
      assert.ok(d.line > 0, `Decision ${d.id} should have a positive line number`);
    }
  });

  test('Empty file returns empty decisions array', () => {
    const result = parseDecisions('# Empty\n\nNo decisions here.\n');
    assert.strictEqual(result.exists, true);
    assert.strictEqual(result.decisions.length, 0);
    assert.strictEqual(result.pending, 0);
  });

  test('Catalog-ID headings (D-NN) parse correctly', () => {
    const result = parseDecisions(`## Decision D-12: Cost ceiling\n\n**Status:** ⏸ PENDING\n`);
    assert.strictEqual(result.decisions.length, 1);
    assert.strictEqual(result.decisions[0].id, 'D-12');
    assert.strictEqual(result.decisions[0].status, 'pending');
  });

  test('Status line variations parse correctly', () => {
    const cases = [
      { input: '**Status:** ⏸ PENDING', expect: 'pending' },
      { input: '**Status:** PENDING', expect: 'pending' },
      { input: '**Status:** ✅ DECIDED 2026-06-25', expect: 'decided' },
      { input: '**Status:** DECIDED', expect: 'decided' },
      { input: '**Status:** 🔒 LOCKED (by Decision 2)', expect: 'locked' },
      { input: '**Status:** 🚫 N/A — no DB', expect: 'na' },
    ];
    for (const c of cases) {
      const md = `## Decision 1: Test\n\n${c.input}\n`;
      const result = parseDecisions(md);
      assert.strictEqual(result.decisions[0].status, c.expect, `Status "${c.input}" should be "${c.expect}"`);
    }
  });
});
