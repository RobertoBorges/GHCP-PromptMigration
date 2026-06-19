/**
 * Remove everything in templates/ except the directory itself, .gitkeep, and README.md
 * so the next sync starts from a clean slate.
 *
 * README.md in templates/ is a "DO NOT EDIT" sign for anyone opening the folder —
 * it's intentionally preserved across syncs.
 *
 * On Windows, file deletion can race with other tools (the guard's snapshot walk,
 * editors holding readonly handles, etc.) and produce EBUSY. We retry a few times
 * with backoff before giving up.
 */

import { promises as fs } from 'node:fs';
import { existsSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const templatesDir = path.resolve(__dirname, '..', 'templates');

const PRESERVE = new Set(['.gitkeep', 'README.md']);

/** Sleep for a number of milliseconds. */
const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

/** Remove a path with retries on EBUSY/EPERM (common on Windows). */
async function robustRm(p) {
  const maxAttempts = 4;
  let lastErr;
  for (let attempt = 1; attempt <= maxAttempts; attempt++) {
    try {
      await fs.rm(p, { recursive: true, force: true, maxRetries: 3, retryDelay: 100 });
      return;
    } catch (err) {
      lastErr = err;
      if (err.code !== 'EBUSY' && err.code !== 'EPERM' && err.code !== 'ENOTEMPTY') {
        throw err;
      }
      // Backoff: 200ms, 500ms, 1s
      const delay = attempt === 1 ? 200 : attempt === 2 ? 500 : 1000;
      console.warn(`[clean-templates] ${err.code} on ${p}, retry ${attempt}/${maxAttempts} after ${delay}ms`);
      await sleep(delay);
    }
  }
  throw lastErr;
}

async function main() {
  if (!existsSync(templatesDir)) {
    await fs.mkdir(templatesDir, { recursive: true });
    return;
  }

  const entries = await fs.readdir(templatesDir);
  for (const entry of entries) {
    if (PRESERVE.has(entry)) continue;
    await robustRm(path.join(templatesDir, entry));
  }

  console.log(`[clean-templates] cleaned ${templatesDir} (preserved: ${[...PRESERVE].join(', ')})`);
}

main().catch((err) => {
  console.error('[clean-templates] FAILED:', err);
  process.exit(1);
});
