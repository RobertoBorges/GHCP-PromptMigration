/**
 * Phase 2 activation tests.
 *
 * Goal: prove the extension loads in a headless VS Code instance, registers
 * its commands, and can execute them without crashing.
 *
 * As we add features in Phases 3-5, this file grows with more tests.
 */

import * as assert from 'assert';
import * as vscode from 'vscode';

suite('Azure Migration Squad extension', () => {
  test('Extension is present', () => {
    const ext = vscode.extensions.getExtension(
      'robertoborges.azure-migration-squad-vscode'
    );
    assert.ok(ext, 'Extension is registered with VS Code');
  });

  test('Extension activates without errors', async () => {
    const ext = vscode.extensions.getExtension(
      'robertoborges.azure-migration-squad-vscode'
    );
    assert.ok(ext, 'Extension is registered');
    await ext.activate();
    assert.strictEqual(ext.isActive, true, 'Extension reports active');
  });

  test('Hello smoke-test command is registered', async () => {
    const allCommands = await vscode.commands.getCommands(true);
    assert.ok(
      allCommands.includes('azureMigrationSquad.hello'),
      'azureMigrationSquad.hello command exists'
    );
  });

  test('Hello smoke-test command runs without throwing', async () => {
    // We can't assert on the info-message UI in tests, but executing the
    // command must complete without throwing.
    await vscode.commands.executeCommand('azureMigrationSquad.hello');
  });
});
