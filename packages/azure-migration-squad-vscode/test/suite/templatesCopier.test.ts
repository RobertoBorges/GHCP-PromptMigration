/**
 * Tests for the obsolete-file cleanup in copyTemplatesToWorkspace.
 */

import * as assert from 'assert';
import * as fs from 'fs';
import * as os from 'os';
import * as path from 'path';
import * as vscode from 'vscode';
import { copyTemplatesToWorkspace, OBSOLETE_FILES } from '../../src/util/templatesCopier';

suite('templatesCopier obsolete-file cleanup', () => {
  let extRoot: string;
  let wsRoot: string;

  setup(() => {
    extRoot = fs.mkdtempSync(path.join(os.tmpdir(), 'ams-ext-'));
    wsRoot = fs.mkdtempSync(path.join(os.tmpdir(), 'ams-ws-'));
    fs.mkdirSync(path.join(extRoot, 'templates', 'github', 'hooks'), { recursive: true });
    fs.writeFileSync(path.join(extRoot, 'templates', 'github', 'hooks', 'validation.json'), '{}');
    for (const rel of OBSOLETE_FILES) {
      const target = path.join(wsRoot, rel);
      fs.mkdirSync(path.dirname(target), { recursive: true });
      fs.writeFileSync(target, 'stale');
    }
  });

  teardown(() => {
    fs.rmSync(extRoot, { recursive: true, force: true });
    fs.rmSync(wsRoot, { recursive: true, force: true });
  });

  test('upgrade removes obsolete blocking hooks', async () => {
    const result = await copyTemplatesToWorkspace(vscode.Uri.file(extRoot), wsRoot, {
      overwrite: true,
    });
    assert.deepStrictEqual(result.removedFiles, OBSOLETE_FILES);
    for (const rel of OBSOLETE_FILES) {
      assert.strictEqual(fs.existsSync(path.join(wsRoot, rel)), false, `${rel} removed`);
    }
    assert.ok(fs.existsSync(path.join(wsRoot, '.github', 'hooks', 'validation.json')));
  });

  test('first-time initialize leaves existing files untouched', async () => {
    const result = await copyTemplatesToWorkspace(vscode.Uri.file(extRoot), wsRoot, {
      overwrite: false,
    });
    assert.deepStrictEqual(result.removedFiles, []);
    for (const rel of OBSOLETE_FILES) {
      assert.ok(fs.existsSync(path.join(wsRoot, rel)), `${rel} kept`);
    }
  });
});
