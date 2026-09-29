/**
 * Add-ons tree provider — surfaces optional workflow skills grouped by purpose.
 *
 * The main path (Assess + Phase 1 → Phase 6) is shown in MainPathProvider;
 * the remaining user-invocable skills in `.github/skills/` are grouped here
 * into 4 collapsible sections.
 */

import * as path from 'path';
import * as fs from 'fs';
import * as vscode from 'vscode';
import { AmsTreeItem, NotInstalledItem } from './baseProvider';
import { findAmsWorkspace, extractDescription } from '../util/workspace';

interface AddonGroup {
  label: string;
  description: string;
  iconId: string;
  skills: string[]; // folder names within .github/skills/
}

const ADDON_GROUPS: AddonGroup[] = [
  {
    label: 'Alternative intakes',
    description: 'Alternative entry points',
    iconId: 'search',
    skills: [
      'build-migration-plan',
      'quick-assessment',
      'quick-triage',
      'interactive-migration-interview',
      'team-skill-assessment',
    ],
  },
  {
    label: 'Portfolio / multi-app',
    description: 'Multi-app engagements',
    iconId: 'organization',
    skills: ['portfolio-strategy', 'phase0-multi-repo-assessment'],
  },
  {
    label: 'Specialized deep-dives',
    description: 'Focused specialist work',
    iconId: 'tools',
    skills: ['database-migration', 'security-hardening', 'cost-optimization'],
  },
  {
    label: 'Utility / recovery',
    description: 'Status + rollback',
    iconId: 'debug-alt',
    skills: ['phase-rollback', 'get-status'],
  },
];

class AddonGroupItem extends vscode.TreeItem {
  constructor(public readonly group: AddonGroup, public readonly skillsDir: string) {
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

    const skillsDir = path.join(ws.root, '.github', 'skills');

    if (!element) {
      // Root — return the 4 collapsible groups.
      return ADDON_GROUPS.map((group) => new AddonGroupItem(group, skillsDir));
    }

    if (element instanceof AddonGroupItem) {
      const items: vscode.TreeItem[] = [];
      for (const skill of element.group.skills) {
        const filePath = path.join(element.skillsDir, skill, 'SKILL.md');
        // Skill missing — surface a subtle marker but keep the row.
        const description = fs.existsSync(filePath)
          ? extractDescription(filePath)
          : '(missing)';
        items.push(new AmsTreeItem(`/${skill}`, description, filePath, 'zap'));
      }
      return items;
    }

    return [];
  }
}
