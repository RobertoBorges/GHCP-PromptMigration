/**
 * Unit tests for the squadDetection helper.
 *
 * Pure logic — exercises the `argsForAmsInit` mapping without needing a
 * real VS Code workspace or shell environment.
 */

import * as assert from 'assert';
import { argsForAmsInit } from '../../src/util/squadDetection';

suite('squadDetection.argsForAmsInit', () => {
  test('no-squad → --force', () => {
    assert.deepStrictEqual(argsForAmsInit('no-squad'), ['--force']);
  });

  test('cli-available → --force (no .squad/ yet, so --force is still needed)', () => {
    assert.deepStrictEqual(argsForAmsInit('cli-available'), ['--force']);
  });

  test('squad-initialized → no flags (init runs cleanly)', () => {
    assert.deepStrictEqual(argsForAmsInit('squad-initialized'), []);
  });

  test('ams-installed → no flags (callers should use upgrade instead)', () => {
    assert.deepStrictEqual(argsForAmsInit('ams-installed'), []);
  });
});
