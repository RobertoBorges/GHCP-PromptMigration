/**
 * Mocha test entry point. Loads all *.test.js files under test/suite/.
 */

import * as path from 'path';
import * as fs from 'fs';
import Mocha from 'mocha';

export function run(): Promise<void> {
  const mocha = new Mocha({
    ui: 'tdd',
    color: true,
    timeout: 30000,
  });

  const testsRoot = path.resolve(__dirname, '.');

  return new Promise((resolve, reject) => {
    try {
      const files = fs
        .readdirSync(testsRoot)
        .filter((f) => f.endsWith('.test.js'));
      for (const file of files) {
        mocha.addFile(path.resolve(testsRoot, file));
      }

      mocha.run((failures) => {
        if (failures > 0) {
          reject(new Error(`${failures} test(s) failed.`));
        } else {
          resolve();
        }
      });
    } catch (err) {
      reject(err);
    }
  });
}
