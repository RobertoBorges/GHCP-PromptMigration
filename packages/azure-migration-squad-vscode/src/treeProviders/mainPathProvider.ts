import * as path from 'path';
import { AmsTreeProviderBase } from './baseProvider';

/**
 * Main-path workflow skills, in canonical order:
 *   1. Assess (Discovery)
 *   2. Plan (Phase 1)
 *   3. Migrate Code (Phase 2)
 *   4. Generate Infra (Phase 3)
 *   5. Deploy (Phase 4)
 *   6. Setup CI/CD (Phase 5)
 *   7. Post-Migration Ops (Phase 6)
 *
 * Each entry is a folder under `.github/skills/` containing a `SKILL.md`,
 * and is invoked in Copilot Chat as `/<skill-name>`.
 */
const MAIN_PATH_SKILLS = [
  'assess-any-application',
  'phase1-plan',
  'phase2-migrate-code',
  'phase3-generate-infra',
  'phase4-deploy-to-azure',
  'phase5-setup-cicd',
  'phase6-post-migration-ops',
];

/** `.../<skill-name>/SKILL.md` → `<skill-name>` */
function skillNameOf(absolutePath: string): string {
  return path.basename(path.dirname(absolutePath));
}

/**
 * Main path tree view — the 7 workflow skills (Assess + Phase 1 → Phase 6).
 * Optional add-ons live in the sibling AddonsProvider.
 */
export class MainPathProvider extends AmsTreeProviderBase {
  getRelativeDir(): string {
    return '.github/skills';
  }
  getIconId(): string {
    return 'zap';
  }
  isRecursive(): boolean {
    // Skills live one level down as `<skill-name>/SKILL.md`.
    return true;
  }
  filterFile(absolutePath: string): boolean {
    return (
      path.basename(absolutePath) === 'SKILL.md' &&
      MAIN_PATH_SKILLS.includes(skillNameOf(absolutePath))
    );
  }
  protected orderFiles(files: string[]): string[] {
    return [...files].sort(
      (a, b) =>
        MAIN_PATH_SKILLS.indexOf(skillNameOf(a)) - MAIN_PATH_SKILLS.indexOf(skillNameOf(b))
    );
  }
  protected labelFor(filePath: string): string {
    return `/${skillNameOf(filePath)}`;
  }
}
