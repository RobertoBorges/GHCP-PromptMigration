/**
 * Add-ons tree provider — surfaces optional workflow skills grouped by purpose.
 *
 * The main path (Assess + Phase 1 → Phase 6) is shown in MainPathProvider;
 * the remaining user-invocable skills in `.github/skills/` are grouped here
 * into collapsible sections.
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
    label: 'AWS account assessment',
    description: 'Read-only estate discovery',
    iconId: 'cloud',
    skills: [
      'aws-assess-phase0-setup-and-scope',
      'aws-assess-phase1-resource-discovery',
      'aws-assess-phase2-deep-inventory',
      'aws-assess-phase3-enrichment',
      'aws-assess-phase4-relationships',
      'aws-assess-phase5-reports',
      'aws-assess-phase6-azure-readiness',
      'aws-assess-get-status',
    ],
  },
  {
    label: 'AWS-to-Azure migration',
    description: 'Workload migration',
    iconId: 'arrow-swap',
    skills: [
      'aws2azure-phase0-multi-repo-assessment',
      'aws2azure-phase1-plan',
      'aws2azure-phase2-migrate-code',
      'aws2azure-phase3-generate-infra',
      'aws2azure-phase4-deploy-to-azure',
      'aws2azure-phase5-setup-cicd',
      'aws2azure-get-status',
    ],
  },
  {
    label: 'Utility / recovery',
    description: 'Status, rollback + skill authoring',
    iconId: 'debug-alt',
    skills: ['phase-rollback', 'get-status', 'skill-creator'],
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
  constructor(private readonly getWorkspace = findAmsWorkspace) {}

  private _onDidChangeTreeData = new vscode.EventEmitter<vscode.TreeItem | undefined | void>();
  readonly onDidChangeTreeData = this._onDidChangeTreeData.event;

  refresh(): void {
    this._onDidChangeTreeData.fire();
  }

  getTreeItem(element: vscode.TreeItem): vscode.TreeItem {
    return element;
  }

  async getChildren(element?: vscode.TreeItem): Promise<vscode.TreeItem[]> {
    const ws = this.getWorkspace();
    if (!ws || !ws.isInstalled) {
      return element ? [] : [new NotInstalledItem()];
    }

    const skillsDir = path.join(ws.root, '.github', 'skills');

    if (!element) {
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
