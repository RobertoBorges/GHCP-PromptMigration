import { AmsTreeProviderBase } from './baseProvider';

export class PromptsProvider extends AmsTreeProviderBase {
  getRelativeDir(): string {
    return '.github/prompts';
  }
  getIconId(): string {
    return 'zap';
  }
  isRecursive(): boolean {
    // Top-level only — legacy/ folder is intentionally excluded.
    return false;
  }
}
