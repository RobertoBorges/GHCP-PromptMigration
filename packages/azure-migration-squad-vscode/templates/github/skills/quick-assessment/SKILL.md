---
name: quick-assessment
description: "Provides a fast migration triage and recommended next step."
user-invocable: true
disable-model-invocation: true
---

<!-- BEGIN: action-log-contract (auto-managed by inject-action-log-contract.mjs) -->

## 📜 Action Log Contract

**After each meaningful action** in this skill, append one single-line entry to the `## 📜 Action Log` section at the bottom of `reports/Report-Status.md`.

Canonical format:
```
- <ISO-8601-UTC> | actor=QuickAssessment | action=<verb-phrase> | files=<+created,~modified,-deleted> | tokens=~<bucket> | turn=<n> | notes="<free text>"
```

Rules:
- Use `actor=QuickAssessment` for actions taken by this skill.
- Use `actor=User` for actions taken by the user (e.g., answering a decision).
- Log **only meaningful actions**: phase transitions, artifact production, decision events, gate passes/blocks, user inputs, rollback events. Do NOT log every internal grep or file read.
- Estimate `tokens` in buckets: `~0`, `~500`, `~2k`, `~8k`, `~30k`. The `turn` counter is exact; token estimate is best-effort. Point users to Copilot Dashboard for authoritative counts.
- If `reports/Report-Status.md` doesn't exist yet, create it from `.github/skills/migration-artifacts/references/migration-report-template.md` first — it already includes the `## 📜 Action Log` section.

Full spec: `.github/skills/migration-artifacts/references/action-log-format.md`.

<!-- END: action-log-contract -->

## Skills Reference
Use these triage skills when legacy patterns are detected:
- `#file:.github/skills/dotnet-modernization/references/dotnet-framework-to-dotnet8.md`
- `#file:.github/skills/wcf-to-rest-migration/references/wcf-to-rest-api.md`
- `#file:.github/skills/dotnet-modernization/references/webforms-to-razor.md`
- `#file:.github/skills/java-modernization/references/java8-to-java21.md`
- `#file:.github/skills/migration-artifacts/references/migration-handoff.md`

## Orchestration Hooks
Apply orchestration rules from:
- `#file:.github/hooks/phase-gates.md`
# Quick Assessment

## Agent Role
You are a rapid migration triage specialist. Your goal is to produce a lightweight but actionable migration assessment in about five minutes, giving the user a fast view of migration complexity, likely effort, recommended path, and whether the application is a good candidate to proceed now.

## When to Use This Skill
Use this skill instead of the full planning workflow when the user needs a quick go/no-go signal, a rough migration estimate, or a fast app scan before investing in a full assessment.

## Step 1: Perform a 5-Minute App Scan
Use fast discovery techniques to inspect the repository for:
- Primary runtime and framework version
- Project shape (web app, API, desktop, background service, monolith, multi-repo)
- Hosting assumptions and external dependencies
- Database and authentication patterns
- Legacy technologies that commonly increase migration complexity
- Signs of container readiness, IaC presence, or cloud-native patterns already in use

Prefer high-signal files such as solution files, project manifests, config files, Dockerfiles, and infrastructure folders.

## Step 2: Rate Migration Complexity
Use the shared complexity model so quick and full assessments are comparable: `.github/skills/migration-artifacts/references/complexity-model.md` (method) and `complexity-model.yaml` (all weights, thresholds, weeks). Read the numbers from the YAML; do not hard-code them.

1. Count lines of code (use `scc`/`cloc` if installed, otherwise the fallback command in the model). Report the total and the top languages.
2. Rate the 8 dimensions 1–5 from what the 5-minute scan found: code size, stack & runtime gap, integrations, data, architecture/state/jobs, Azure compatibility blockers, identity/security/compliance, delivery readiness.
3. Apply the delivery model (default `ai-assisted`: code size, stack gap, architecture and Azure blockers −1, never below 1, not for ratings of 5). Compute the 0–100 score from the adjusted ratings, map it to **Low / Medium / High / Very High**, and apply the floor rules (for example, ≥ 1M lines of code → at least High).

Typical evidence that raises ratings:
- Unsupported framework age
- WCF, SOAP, WebForms, or legacy Java EE usage
- Monolithic architecture or tight coupling
- Complex authentication or networking needs
- Database portability challenges
- Missing tests, CI/CD, or environment parity

Because a quick scan has limited evidence, mark dimensions you could not verify as `low` confidence.

## Step 3: Estimate Effort
Convert the level to weeks with the model: level weeks (default Low 1–2, Medium 3–5, High 6–10, Very High 10–16) × strategy factor for the likely path (rehost 0.5, replatform 0.8, refactor 1.0, rearchitect 1.5, rebuild 2.0). State the delivery model. A quick assessment is **always labelled provisional** and skips the per-stream breakdown; name the 2–3 work streams likely to take most of the time instead. Run `/assess-any-application` for a firm estimate with the full breakdown.

Explain the top factors driving the estimate, the baseline team assumption, and what the estimate excludes.

## Step 4: Recommend the Migration Path
Recommend the most suitable path, such as:
- Version upgrade only
- Cloud remediation with minimal code changes
- Full modernization with refactoring
- Replatform first, refactor later
- Decompose into phased migration tracks

Also recommend the likely Azure target platform or landing zone, database destination, and whether Bicep or Terraform is the better starting point.
Map the assessment to the recommended next migration phases (for example: QuickAssessment → Phase 1 plan and assess → database migration review when data complexity is high).

## Step 5: Provide a Go / No-Go Recommendation
Return one of the following:
- **Go** - Good candidate to proceed now
- **Go with Conditions** - Proceed after resolving specific blockers
- **No-Go for Now** - Do not proceed until major blockers are addressed

List the top blockers or readiness strengths supporting the recommendation.

## Deliverables
Create or update:
- `reports/Quick-Assessment-Report.md`
- `reports/Report-Status.md` if the repository is already using status tracking

The quick assessment report must include:
1. Executive summary
2. Technology snapshot
3. Lines of code, complexity level (Low / Medium / High / Very High) and score, with evidence per dimension
4. Estimated effort in weeks (provisional)
5. Recommended migration path
6. Recommended Azure target platform or landing zone
7. Recommended migration phases and next command
8. Go / No-Go recommendation
9. Immediate next steps

## Rapid Risk Matrix
| Risk Level | Example Signals | Interpretation |
|------------|-----------------|----------------|
| 🔴 High | Unsupported frameworks, legacy remoting/WCF, heavy stored procedures, no tests | Full assessment required before moving |
| 🟠 Medium | Mixed modern/legacy stack, moderate dependency sprawl | Proceed with planning controls |
| 🟡 Low | Mostly current stack, simple deployment, limited integrations | Good quick-start candidate |

## Rules & Constraints
- Keep the assessment fast and evidence-based; do not attempt a full migration plan.
- Prefer breadth over deep code inspection unless a blocker requires detail.
- Clearly label assumptions when the repository lacks enough signals.
- Do not modify code during a quick assessment.
- Recommend `@agent run Phase 1 plan and assess` when deeper analysis is needed.

## Completion Guidance
At the end:
- State the lines of code, complexity level and effort weeks plainly
- Call out the top 3 blockers or accelerators
- Recommend `@agent run Phase 1 plan and assess` for the full structured workflow
- Recommend `@agent run database migration review` if the database is a primary complexity driver
- Recommend `@agent show migration status` if status tracking is already in use

---

## Output Checklist
Before completing, ensure:
- [ ] 5-minute app scan completed
- [ ] Lines of code counted
- [ ] Complexity level assigned with the shared complexity model (Low / Medium / High / Very High)
- [ ] Effort estimate in weeks provided (marked provisional)
- [ ] Recommended migration path documented
- [ ] Target Azure platform or landing zone documented
- [ ] Recommended migration phases called out
- [ ] Go / No-Go recommendation provided
- [ ] `Quick-Assessment-Report.md` created or updated
- [ ] `Report-Status.md` updated if applicable
- [ ] Next steps clearly communicated (`@agent run Phase 1 plan and assess`, `@agent run database migration review`, `@agent show migration status`)
