import { AmsTreeProviderBase } from './baseProvider';

export class AgentsProvider extends AmsTreeProviderBase {
  getRelativeDir(): string {
    return '.squad/agents';
  }
  getIconId(): string {
    return 'person';
  }
  isRecursive(): boolean {
    // Charters are at .squad/agents/<name>/charter.md — need recursion to find them.
    return true;
  }
}
