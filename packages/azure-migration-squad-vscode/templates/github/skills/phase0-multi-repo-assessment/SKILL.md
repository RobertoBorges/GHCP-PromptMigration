---
name: phase0-multi-repo-assessment
description: Analyze multiple repositories of a business solution for migration planning
argument-hint: "Ensure codebase-repos.md exists with repository URLs, then run this command"
user-invocable: true
disable-model-invocation: true
---

<!-- BEGIN: action-log-contract (auto-managed by inject-action-log-contract.mjs) -->

## 📜 Action Log Contract

**After each meaningful action** in this skill, append one single-line entry to the `## 📜 Action Log` section at the bottom of `reports/Report-Status.md`.

Canonical format:
```
- <ISO-8601-UTC> | actor=Phase0-Multi-repo-assessment | action=<verb-phrase> | files=<+created,~modified,-deleted> | tokens=~<bucket> | turn=<n> | notes="<free text>"
```

Rules:
- Use `actor=Phase0-Multi-repo-assessment` for actions taken by this skill.
- Use `actor=User` for actions taken by the user (e.g., answering a decision).
- Log **only meaningful actions**: phase transitions, artifact production, decision events, gate passes/blocks, user inputs, rollback events. Do NOT log every internal grep or file read.
- Estimate `tokens` in buckets: `~0`, `~500`, `~2k`, `~8k`, `~30k`. The `turn` counter is exact; token estimate is best-effort. Point users to Copilot Dashboard for authoritative counts.
- If `reports/Report-Status.md` doesn't exist yet, create it from `.github/skills/migration-artifacts/references/migration-report-template.md` first — it already includes the `## 📜 Action Log` section.

Full spec: `.github/skills/migration-artifacts/references/action-log-format.md`.

<!-- END: action-log-contract -->

