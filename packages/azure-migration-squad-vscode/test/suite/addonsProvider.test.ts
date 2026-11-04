import * as assert from 'assert';
import * as fs from 'fs';
import * as os from 'os';
import * as path from 'path';
import * as vscode from 'vscode';
import { AddonsProvider } from '../../src/treeProviders/addonsProvider';

suite('Optional add-ons catalog', () => {
  test('Every bundled optional workflow is discoverable exactly once', async () => {
    const extension = vscode.extensions.getExtension('robertoborges.azure-migration-squad-vscode');
    assert.ok(extension);
    const root = fs.mkdtempSync(path.join(os.tmpdir(), 'azure-migration-addons-'));
    try {
      fs.cpSync(path.join(extension.extensionPath, 'templates', 'github'), path.join(root, '.github'), {
        recursive: true,
      });
      const provider = new AddonsProvider(() => ({
        root, hasAgent: true, hasSkills: true, hasCopilotInstructions: true, isInstalled: true,
      }));
      const mainPath = new Set([
        'assess-any-application', 'phase1-plan', 'phase2-migrate-code', 'phase3-generate-infra',
        'phase4-deploy-to-azure', 'phase5-setup-cicd', 'phase6-post-migration-ops',
      ]);
      const skillsDir = path.join(root, '.github', 'skills');
      const expected = fs.readdirSync(skillsDir).filter((skill) => {
        const content = fs.readFileSync(path.join(skillsDir, skill, 'SKILL.md'), 'utf8');
        return /^user-invocable:\s*true\s*$/m.test(content) && !mainPath.has(skill);
      }).map((skill) => `/${skill}`).sort();
      const groups = await provider.getChildren();
      const items = (await Promise.all(groups.map((group) => provider.getChildren(group)))).flat();
      const actual = items.map((item) => item.label).sort();
      assert.deepStrictEqual(actual, expected, 'Sidebar must include AWS tracks and skill authoring without duplicates');
      assert.ok(items.every((item) => item.description !== '(missing)'), 'All sidebar entries must resolve');
    } finally {
      fs.rmSync(root, { recursive: true, force: true });
    }
  });
});
