/**
 * Add-ons tree provider — surfaces optional prompts grouped by purpose.
 *
 * Wave L: replaces the old Skills tree view. The main path (Phase 1 → Phase 6)
 * is shown in PromptsProvider; everything else in `.github/prompts/` is
 * grouped here into 4 collapsible sections.
 */

import * as path from 'path';
import * as vscode from 'vscode';
import { AmsTreeItem, NotInstalledItem } from './baseProvider';
import { findAmsWorkspace, extractDescription } from '../util/workspace';

interface AddonGroup {
  label: string;
  description: string;
  iconId: string;
  files: string[]; // basenames within .github/prompts/
}

const ADDON_GROUPS: AddonGroup[] = [
  {
    label: 'Alternative intakes',
    description: 'Alternative entry points',
    iconId: 'search',
    files: [
      'Build-Migration-Plan.prompt.md',
      'QuickAssessment.prompt.md',
      'QuickTriage.prompt.md',
      'InteractiveMigrationInterview.prompt.md',
      'TeamSkillAssessment.prompt.md',
    ],
  },
  {
    label: 'Portfolio / multi-app',
    description: 'Multi-app engagements',
    iconId: 'organization',
    files: ['PortfolioStrategy.prompt.md', 'Phase0-Multi-repo-assessment.prompt.md'],
  },
  {
    label: 'Specialized deep-dives',
    description: 'Focused specialist work',
    iconId: 'tools',
    files: [
      'DatabaseMigration.prompt.md',
      'SecurityHardening.prompt.md',
      'CostOptimization.prompt.md',
    ],
  },
  {
    label: 'Utility / recovery',
    description: 'Status + rollback',
    iconId: 'debug-alt',
    files: ['Phase-Rollback.prompt.md', 'GetStatus.prompt.md'],
  },
];

class AddonGroupItem extends vscode.TreeItem {
  constructor(public readonly group: AddonGroup, public readonly promptsDir: string) {
    super(group.label, vscode.TreeItemCollapsibleState.Expanded);
    this.description = group.description;
    this.iconPath = new vscode.ThemeIcon(group.iconId);
    this.tooltip = `${group.label} — ${group.description}`;
    this.contextValue = 'addonGroup';
  }
}

export class AddonsProvider implements vscode.TreeDataProvider<vscode.TreeItem> {
  private _onDidChangeTreeData = new vscode.EventEmitter<vscode.TreeItem | undefined | void>();
  readonly onDidChangeTreeData = this._onDidChangeTreeData.event;

  refresh(): void {
    this._onDidChangeTreeData.fire();
  }

  getTreeItem(element: vscode.TreeItem): vscode.TreeItem {
    return element;
  }

  async getChildren(element?: vscode.TreeItem): Promise<vscode.TreeItem[]> {
    const ws = findAmsWorkspace();
    if (!ws || !ws.isInstalled) {
      return element ? [] : [new NotInstalledItem()];
    }

    const promptsDir = path.join(ws.root, '.github', 'prompts');

    if (!element) {
      // Root — return the 4 collapsible groups.
      return ADDON_GROUPS.map((group) => new AddonGroupItem(group, promptsDir));
    }

    if (element instanceof AddonGroupItem) {
      const items: vscode.TreeItem[] = [];
      for (const basename of element.group.files) {
        const filePath = path.join(element.promptsDir, basename);
        const label = basename.replace(/\.prompt\.md$/, '');
        let description = '';
        try {
          description = extractDescription(filePath);
        } catch {
          // File missing — surface a subtle marker but keep the row.
          description = '(missing)';
        }
        items.push(new AmsTreeItem(label, description, filePath, 'zap'));
      }
      return items;
    }

    return [];
  }
}
