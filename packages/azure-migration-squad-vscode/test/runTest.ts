/**
 * Test runner: launches a headless VS Code instance, installs the extension,
 * and runs the Mocha test suite inside it.
 *
 * Uses a pinned stable VS Code version to avoid:
 *   - Inno Setup updater mutex conflicts on Windows with a host VS Code
 *     install (which is why we don't use the default 'stable' channel)
 *   - Insiders auto-update churn that locks node_modules.asar mid-test
 *
 * The pinned version must be >= the extension's engines.vscode minimum.
 * Bump it when we adopt newer VS Code APIs.
 *
 * Reference: https://code.visualstudio.com/api/working-with-extensions/testing-extension
 */

import * as path from 'path';
import { runTests } from '@vscode/test-electron';

// Pinned VS Code version for tests. Must be >= engines.vscode in package.json.
const VSCODE_TEST_VERSION = '1.95.0';

async function main() {
  try {
    const extensionDevelopmentPath = path.resolve(__dirname, '../..');
    const extensionTestsPath = path.resolve(__dirname, './suite/index');

    await runTests({
      version: VSCODE_TEST_VERSION,
      extensionDevelopmentPath,
      extensionTestsPath,
      launchArgs: ['--disable-extensions', '--disable-updates'],
    });
  } catch (err) {
    console.error('Failed to run tests:', err);
    process.exit(1);
  }
}

main();
