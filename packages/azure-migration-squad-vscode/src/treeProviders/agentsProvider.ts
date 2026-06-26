/**
 * Agents tree view — reads .github/agents/*.agent.md from the workspace.
 *
 * The Azure Migration Agent is defined as a single .agent.md file at
 * .github/agents/Code-Migration-Modernization.agent.md. The tree shows that
 * file (plus any other .agent.md files the user adds).
 */

import { AmsTreeProviderBase } from './baseProvider';

export class AgentsProvider extends AmsTreeProviderBase {
  getRelativeDir(): string {
    return '.github/agents';
  }
  getIconId(): string {
    return 'person';
  }
  isRecursive(): boolean {
    return false;
  }
  getFileSuffix(): string {
    return '.agent.md';
  }
}
