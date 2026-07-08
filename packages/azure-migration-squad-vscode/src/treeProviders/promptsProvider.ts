import * as path from 'path';
import { AmsTreeProviderBase } from './baseProvider';

/** Filenames that make up the main-path (Phase 1 → Phase 6). */
const MAIN_PATH_FILES = new Set([
  'Phase1-PlanAndAssess.prompt.md',
  'Phase2-MigrateCode.prompt.md',
  'Phase3-GenerateInfra.prompt.md',
  'Phase4-DeployToAzure.prompt.md',
  'Phase5-SetupCICD.prompt.md',
  'Phase6-PostMigrationOps.prompt.md',
]);

/**
 * Prompts tree view — main path only (Phase 1 → Phase 6).
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
