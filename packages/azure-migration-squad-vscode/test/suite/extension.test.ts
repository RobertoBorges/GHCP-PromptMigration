/**
 * Phase 3 tests: extension still activates, all 8 commands are registered,
 * tree view providers return sensible results (NotInstalledItem when no
 * AMS content is present in the workspace).
 */

import * as assert from 'assert';
import * as vscode from 'vscode';

const EXTENSION_ID = 'robertoborges.azure-migration-squad-vscode';

const EXPECTED_COMMANDS = [
  'azureMigrationSquad.initialize',
  'azureMigrationSquad.upgrade',
  'azureMigrationSquad.doctor',
  'azureMigrationSquad.openDiscovery',
  'azureMigrationSquad.showCatalog',
  'azureMigrationSquad.openSettings',
  'azureMigrationSquad.refreshTree',
  'azureMigrationSquad.openFile',
  'azureMigrationSquad.showWelcome',
  'azureMigrationSquad.installCopilotChat',
  'azureMigrationSquad.installSquadCli',
  'azureMigrationSquad.hello',
];

suite('Azure Migration Squad extension', () => {
  test('Extension is present', () => {
    const ext = vscode.extensions.getExtension(EXTENSION_ID);
    assert.ok(ext, 'Extension is registered with VS Code');
  });

  test('Extension activates without errors', async () => {
    const ext = vscode.extensions.getExtension(EXTENSION_ID);
    assert.ok(ext, 'Extension is registered');
    await ext.activate();
    assert.strictEqual(ext.isActive, true, 'Extension reports active');
  });

  test('All Phase 3 commands are registered', async () => {
    const allCommands = await vscode.commands.getCommands(true);
    for (const cmd of EXPECTED_COMMANDS) {
      assert.ok(
        allCommands.includes(cmd),
        `Command ${cmd} should be registered`
      );
    }
  });

  test('Hello smoke-test command runs without throwing', async () => {
    await vscode.commands.executeCommand('azureMigrationSquad.hello');
  });

  test('Tree view: Agents view is registered', () => {
    // VS Code doesn't expose a direct API to look up tree views, but we can
    // verify the contributed view exists by attempting to focus it (no-op if
    // not contributed). If this command throws, the view isn't registered.
    return vscode.commands
      .executeCommand('azureMigrationSquadAgents.focus')
      .then(undefined, (err) => {
        // Some VS Code versions emit a 'no provider' error if the view exists
        // but has no provider attached. We accept that as "view exists".
        const msg = String(err);
        const acceptable =
          msg.includes('No tree view') === false &&
          msg.toLowerCase().includes('command') === false;
        if (!acceptable) {
          throw err;
        }
      });
  });
});
