# Legacy Assess-* Prompts (Deprecated 2026-06-01)

> These prompts were moved here as part of the **Universal Mode** refactor. They are preserved for reference but should NOT be used for new engagements. Use `/assess-any-application` (the universal entry point) instead.

## Why deprecated?

The old `Assess-*` prompts were narrow assessments tied to specific .NET / Java sub-stacks:

- `Assess-ClassicASP-Migration.prompt.md`
- `Assess-DotNet-Upgrade.prompt.md`
- `Assess-Java-Upgrade.prompt.md`
- `Assess-WCF-Migration.prompt.md`
- `Assess-WebForms-Migration.prompt.md`

Under Universal Mode, the **Discovery Engineer (Saul Bloom Jr.)** handles intake for any application via `/assess-any-application`. Stack-specific guidance is now delivered through stack adapter skills, which the Discovery Engineer loads dynamically based on the detected stack.

This avoids:
- Prompt explosion as we add more stacks (Python, Node, PHP, Oracle Forms, etc.)
- Stale routing pinned to a fixed set of use-cases
- Duplicate maintenance when a skill needs to be updated in multiple places

## Where did the content go?

Every Assess-* prompt's expertise was absorbed into one or more **stack adapter skills** (and sometimes workload pattern skills). Use this table to find the replacement:

| Old prompt | Replacement skill(s) | New entry point |
|------------|----------------------|-----------------|
| `Assess-ClassicASP-Migration.prompt.md` | `.github/skills/stack-dotnet.md` (Classic ASP sub-stack section) + `.github/skills/workload-webapp.md` | `/assess-any-application` |
| `Assess-DotNet-Upgrade.prompt.md` | `.github/skills/stack-dotnet.md` (all sub-stacks) | `/assess-any-application` |
| `Assess-Java-Upgrade.prompt.md` | `.github/skills/stack-java.md` (all sub-stacks) | `/assess-any-application` |
| `Assess-WCF-Migration.prompt.md` | `.github/skills/stack-dotnet.md` (WCF sub-stack) + `.github/skills/workload-api-service.md` (SOAP sub-pattern) | `/assess-any-application` |
| `Assess-WebForms-Migration.prompt.md` | `.github/skills/stack-dotnet.md` (WebForms sub-stack) + `.github/skills/workload-webapp.md` (server-rendered sub-pattern) | `/assess-any-application` |

The replacement skills are typically **more detailed** than the old prompts because they consolidate guidance for several related sub-stacks.

## How to migrate from an old prompt

If you were using `Assess-XYZ-Migration` in a script, chatmode, or external workflow:

1. Replace the trigger with `/assess-any-application` (or open the `Discovery-Intake` chatmode).
2. Provide the stack hint in your intake answer — e.g., "It's a WCF service on .NET Framework 4.7." The Discovery Engineer will load `stack-dotnet.md` automatically.
3. If you were depending on a specific report filename (e.g., `WCF-Migration-Report.md`), update the path to `Discovery-Dossier.md` + `Capability-Matrix.yaml`.

## Can I still run the old prompts?

The files are kept here so you can read them and copy useful narrative if you need it. But the agent routing (in `.github/copilot-instructions.md`) no longer references them. Running them directly will:

- Skip the Discovery Engineer (so no Capability Matrix is produced)
- Not be auto-routed by the Migration-Orchestrator
- Need manual handoff to the Architect

If you absolutely need the old behavior for a one-off engagement, document the reason in `reports/Decision-Log.md` so the Evaluator knows it was a conscious choice.

## See also

- Universal entry point: `.github/prompts/Assess-Any-Application.prompt.md`
- Architect handoff: `.github/prompts/Build-Migration-Plan.prompt.md`
- Discovery chatmode: `.github/chatmodes/Discovery-Intake.chatmode.md`
- Migration orchestration: `.github/chatmodes/Migration-Orchestrator.chatmode.md`
- Routing rules: `.github/copilot-instructions.md`
- Discovery Engineer charter: `.github/prompts/Assess-Any-Application.prompt.md`
