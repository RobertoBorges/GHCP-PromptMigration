# Rollback Strategy

Use this skill when planning deployment cutover, validation, and recovery.

## Preferred rollback patterns

- App Service deployment slot swap rollback
- Container revision rollback in Container Apps
- Helm release rollback in AKS
- database changes designed for backward-compatible deploys

## Rollback checklist

1. define success metrics before cutover
2. keep previous artifact and infra state identifiable
3. verify backups and recovery paths
4. separate app rollback from irreversible data changes
5. document who approves rollback and how it is triggered

## Validation checklist

- Rollback steps are scripted or documented.
- Health checks gate promotion.
- Database migrations are reversible or guarded by compatibility windows.
