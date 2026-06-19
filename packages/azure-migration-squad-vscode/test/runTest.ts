/**
 * Test runner: launches a headless VS Code instance, installs the extension,
 * and runs the Mocha test suite inside it.
 *
 * Uses VS Code Insiders to avoid mutex conflicts with a host VS Code install
 * (the stable channel holds an Inno Setup updater mutex on Windows that
 * blocks parallel launches of the same channel).
 *
 * Reference: https://code.visualstudio.com/api/working-with-extensions/testing-extension
 */

import * as path from 'path';
import { runTests } from '@vscode/test-electron';

async function main() {
  try {
    const extensionDevelopmentPath = path.resolve(__dirname, '../..');
    const extensionTestsPath = path.resolve(__dirname, './suite/index');

    await runTests({
      version: 'insiders',
      extensionDevelopmentPath,
      extensionTestsPath,
      launchArgs: ['--disable-extensions'],
    });
  } catch (err) {
    console.error('Failed to run tests:', err);
    process.exit(1);
  }
}

main();
