/**
 * esbuild bundler for the Azure Migration Squad VS Code extension.
 *
 * Bundles src/extension.ts (and its imports) into a single CommonJS file
 * at dist/extension.js. CJS is required by VS Code's extension host.
 *
 * Pass --watch to rebuild on change while developing.
 *
 * Reference: https://code.visualstudio.com/api/working-with-extensions/bundling-extension
 */

import * as esbuild from 'esbuild';

const watch = process.argv.includes('--watch');

const options = {
  entryPoints: ['src/extension.ts'],
  bundle: true,
  format: 'cjs',
  platform: 'node',
  target: 'node20',
  outfile: 'dist/extension.js',
  external: ['vscode'],
  sourcemap: true,
  minify: !watch,
  logLevel: 'info',
};

if (watch) {
  const ctx = await esbuild.context(options);
  await ctx.watch();
  console.log('[esbuild] watching for changes...');
} else {
  await esbuild.build(options);
}
