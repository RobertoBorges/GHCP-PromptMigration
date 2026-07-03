# Quality Checklist

Use this hook to ensure migration outputs, prompt flows, and specialist reviews meet the agent's minimum quality bar before handoff.

## Global Checklist

- [ ] `reports/Report-Status.md` reflects the current phase, owner, blockers, and next command
- [ ] Required artifacts for the active prompt or chatmode are created or updated
- [ ] Assumptions, risks, and trade-offs are explicit
- [ ] Specialist reviews are named when their domain was touched
- [ ] Recommendations are actionable enough for the next agent to execute

## Specialist Checkpoints

| Specialist | Checkpoint |
|------------|------------|
| Architect | Scope, sequencing, and target-state rationale are explicit |
| Coder | Implementation changes are concrete, bounded, and reproducible |
| Tester | Validation evidence is present and user-facing guidance is understandable |
| Azure Specialist | Azure service choices, hosting fit, and identity/network implications are justified |
| DevOps Engineer | Deployment and automation steps are repeatable and environment-aware |
| Observability Engineer | Health signals, alert paths, and runbook expectations are defined |
| Database Specialist | Data migration path, validation checks, and cutover assumptions are documented |
| Performance Engineer | Scaling guidance includes baseline assumptions and measurable targets |
| Security Auditor | Auth, secrets, RBAC, and compliance trade-offs are reviewed and risk-ranked |
| Cost Engineer | Every savings recommendation includes estimated dollars/month impact, owners, and guardrails against reliability or security regressions |
| Evaluator | Prompt, hook, or agent-behavior changes are checked for structural drift |
| Cutover Commander | Rollout, rollback, and operational decision points are explicit |
| Scribe | Decisions and milestones are captured with enough context for future sessions |
| Presentation Specialist | Stakeholder-facing deliverables are clear, polished, and aligned to the requested narrative |

## Cost Optimization Exit Check

- [ ] Current cost drivers are identified
- [ ] Right-sizing actions are prioritized by impact and risk
- [ ] Reserved capacity or savings-plan recommendations include break-even assumptions
- [ ] Budget alerts, anomaly thresholds, and owners are documented
- [ ] Estimated savings are stated in dollars/month for each recommendation
