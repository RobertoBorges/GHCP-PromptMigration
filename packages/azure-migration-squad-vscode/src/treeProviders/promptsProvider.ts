import * as path from 'path';
import { AmsTreeProviderBase } from './baseProvider';

/**
 * Main-path files, in canonical order:
 *   1. Assess (Discovery)
 *   2. Plan (Phase 1)
 *   3. Migrate Code (Phase 2)
 *   4. Generate Infra (Phase 3)
 *   5. Deploy (Phase 4)
 *   6. Setup CI/CD (Phase 5)
 *   7. Post-Migration Ops (Phase 6)
 */
const MAIN_PATH_FILES = new Set([
  'Assess-Any-Application.prompt.md',
  'Phase1-Plan.prompt.md',
  'Phase2-MigrateCode.prompt.md',
  'Phase3-GenerateInfra.prompt.md',
  'Phase4-DeployToAzure.prompt.md',
  'Phase5-SetupCICD.prompt.md',
  'Phase6-PostMigrationOps.prompt.md',
]);

/**
 * Prompts tree view — main path only (Assess + Phase 1 → Phase 6).
 * Optional add-ons live in the sibling AddonsProvider.
 */
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
  filterFile(absolutePath: string): boolean {
    return MAIN_PATH_FILES.has(path.basename(absolutePath));
  }
}
