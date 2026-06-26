# Rollback Strategy

Use this skill when planning safe cutover, recovery, and release reversal for Azure migrations.

## Rollback Decision Matrix

| Condition | Preferred Response |
|---|---|
| Deployment failed before customer traffic moved | Fix forward or redeploy previous artifact |
| App Service staging slot unhealthy | Abort swap or swap back immediately |
| Container release causes runtime regression | Roll back to prior revision or image tag |
| Database migration is additive and backward compatible | Redeploy previous app version while keeping schema |
| Database migration is destructive or corrupting | Restore from backup / point-in-time restore |
| DNS cutover points users to unhealthy system | Revert DNS / traffic manager / Front Door routing |

## Core Rules

- define RTO/RPO before go-live
- preserve previous artifact, configuration, and infra version identifiers
- separate app rollback from database rollback decisions
- prefer backward-compatible migrations so app rollback stays possible
- document who can approve rollback and how the decision is triggered

## Blue-Green and Slot Swap Procedures

### App Service slot swap rollback

1. Deploy and validate in `staging`
2. Swap `staging` -> `production`
3. If health checks fail, swap back immediately
4. Re-run smoke tests and confirm config bindings
5. capture incident details in rollback artifacts

### Container Apps / blue-green style rollback

1. Keep previous revision active but not receiving traffic
2. Shift traffic to new revision gradually
3. If validation fails, route traffic back to prior stable revision
4. freeze further releases until root cause is known

## Database Rollback Guidance

Choose one of these strategies explicitly:

- **Backward-compatible release**: keep new schema additive so prior app version still works
- **Down migration**: only if fully tested and data-safe
- **Point-in-time restore**: preferred when destructive changes occurred
- **Dual-write / shadow copy**: use for high-risk cutovers where rollback speed matters

Document:

- expected downtime
- possible data loss window
- validation queries
- ownership for restore approval

## DNS Cutover Reversal

If traffic was moved through DNS, Front Door, Traffic Manager, or reverse proxy configuration:

1. restore the previous endpoint or routing weight
2. confirm TTL expectations and propagation behavior
3. verify TLS/certificate bindings still match the restored route
4. communicate user-visible recovery timing clearly

## Post-Mortem Template

```markdown
# Post-Mortem

## Incident Summary
- Date/time:
- Release / deployment ID:
- Trigger for rollback:
- Impact:

## Timeline
- Detection:
- Decision:
- Rollback start:
- Service restored:

## Root Cause
- Technical cause:
- Contributing factors:

## What Worked
- [items]

## What Failed or Was Missing
- [items]

## Corrective Actions
| Action | Owner | Due Date |
|---|---|---|
| [action] | [owner] | [date] |
```

## Validation Checklist

- rollback steps are scripted or copy/paste ready
- previous artifact and config are identifiable
- health checks gate release promotion and rollback completion
- database recovery path is documented separately from app rollback
- communications and post-mortem artifacts are part of the plan

## Output Expectations for Prompts

When this skill is applied, the prompt should:

- pick a rollback pattern based on evidence, not guesswork
- separate app, infra, data, and DNS rollback workstreams
- provide concrete rollback and validation steps
- generate post-mortem and communication artifacts as part of the response
