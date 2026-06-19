import { AmsTreeProviderBase } from './baseProvider';

export class SkillsProvider extends AmsTreeProviderBase {
  getRelativeDir(): string {
    return '.github/skills';
  }
  getIconId(): string {
    return 'book';
  }
  isRecursive(): boolean {
    // Skills may be flat .md files OR <skill-name>/SKILL.md folders.
    return true;
  }
}
