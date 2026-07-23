# Action Log Format — canonical spec

This is the **single source of truth** for how prompts, hooks, and the agent write entries to `reports/Report-Status.md`. Every meaningful action taken during a migration must produce one log entry so the file becomes a **trace memory** — enough context to recover the migration if a session is lost.

## Where entries live

Entries go in a dedicated section at the bottom of `reports/Report-Status.md`:

```
## 📜 Action Log
<entries appended chronologically, newest at the bottom>
```

**Do not put entries anywhere else in the file.** The phase-status table + summary sections at the top stay separate — those are the "current state" view. The Action Log is the "history" view.

If `Report-Status.md` doesn't exist yet, create it with the standard template (see `migration-report-template.md`) which already includes an empty `## 📜 Action Log` section.

## Line format

Every entry is a **single line** starting with `- ` (Markdown list marker), followed by pipe-separated fields:

```
- <timestamp> | actor=<actor> | action=<action> | files=<files> | tokens=~<count> | turn=<n> | notes="<free text>"
```

**Required fields:** `timestamp`, `actor`, `action`, `turn`.
**Optional fields:** `files`, `tokens`, `notes`, `value`, `reason`.

The order MUST be `timestamp | actor | action | ...optional fields...`. Optional fields can appear in any order after `action`.

### Field spec

| Field | Format | Required | Example |
|-------|--------|----------|---------|
| `timestamp` | ISO 8601 UTC (`YYYY-MM-DDTHH:MMZ`) | ✅ | `2026-07-09T10:43Z` |
| `actor` | `Phase1-Plan`, `Phase2-MigrateCode`, ..., `User`, `hook`, `Assess-Any-Application`, `DatabaseMigration`, etc. | ✅ | `actor=Phase1-Plan` |
| `action` | short-kebab-case verb-phrase from the vocabulary below | ✅ | `action=produced-decisions-required` |
| `files` | `+path` for created, `~path` for modified, `-path` for deleted; comma-separate multiples | ⚠ if files changed | `files=+reports/Decisions-Required.md,~reports/Application-Assessment-Report.md` |
| `tokens` | `~<estimate>` in buckets (`~500`, `~2k`, `~8k`, `~30k`) or `~0` if no LLM work | ⚠ recommended | `tokens=~4k` |
| `turn` | integer turn counter for the current session | ✅ | `turn=3` |
| `notes` | short free text in double quotes; no pipes, no newlines | optional | `notes="14 decisions PENDING"` |
| `value` | user's decision or answer (for user actions), in double quotes | optional | `value=".NET 10 LTS"` |
| `reason` | short blocker/failure reason in double quotes | optional | `reason="D-04 database engine PENDING"` |

**Do NOT** use pipes (`|`) inside quoted fields. If you need one, substitute with `/` or spell it out.

## Action vocabulary

Use one of these action names (kebab-case, verb-phrase). Extend only when necessary.

**Session:**
- `session-started` — hook logs at SessionStart
- `session-ended` — hook logs at Stop
- `session-resumed` — SessionStart hook detected prior state and recovered

**Phase lifecycle:**
- `phase-started` — a phase prompt begins execution
- `phase-completed` — a phase prompt marks itself done in the status table
- `phase-blocked` — a phase can't proceed (gate failure); use with `reason=`

**Artifacts:**
- `produced-<artifact>` — created a new report file (e.g., `produced-discovery-dossier`, `produced-capability-matrix`, `produced-decisions-required`, `produced-application-assessment-report`, `produced-migration-plan`, `produced-infra-plan`, `produced-deployment-summary`)
- `updated-<artifact>` — modified an existing report file
- `deleted-<artifact>` — removed a report file

**Decisions:**
- `answered-decision` — user picked a value for a decision; use with `value=` and put decision ID in `notes` (e.g., `notes="D-01 target framework"`)
- `regenerated-decisions-required` — Phase 1 (or Build-Migration-Plan) regenerated the decisions file

**Gates:**
- `gate-passed` — a hard-stop gate was satisfied
- `gate-blocked` — a hard-stop gate blocked further work; use `reason=`

**User inputs:**
- `user-approved` — user OK'd a step (use `notes=` for what)
- `user-declined` — user rejected a step
- `user-waived` — user waived a gate (log the reason)

**Code changes** (Phase 2 specifically):
- `code-modernized` — applied a modernization change; use `files=` and `notes=` for what
- `dependency-updated` — bumped a dependency

**Infrastructure** (Phase 3-5):
- `infra-generated` — produced Bicep/Terraform
- `infra-validated` — ran predeploy validation
- `infra-deployed` — actually deployed to Azure (use `notes=` for env/resource group)
- `pipeline-created` — CI/CD pipeline file created

**Operations** (Phase 6):
- `alert-configured` — added an Azure Monitor alert
- `runbook-created` — produced an operational runbook

**Rollback:**
- `rollback-initiated` — `/Phase-Rollback` invoked; use `reason=`
- `rollback-completed` — rollback finished
- `rollback-blocked` — rollback failed

**Escalations:**
- `escalated-source-unsupported` — SaaS-embedded stack requires specialist (Salesforce Apex, ServiceNow, SharePoint on-prem, Power Platform)

## When to log — the moderate rule

**Log when:**
- A phase starts, completes, or blocks
- Any file in `reports/` or in the app's source tree is created or updated
- The user answers a decision, approves, or declines
- A gate passes or blocks
- An observable Azure change happens (deployment, alert, resource creation)
- A rollback is initiated or completed

**Do NOT log:**
- Every internal file read or grep
- Every LLM turn where nothing was produced
- Advisory recommendations that the user did not act on
- Discovery-only reasoning (Discovery outputs get one `produced-discovery-dossier` entry, not one per question asked)

## Token estimates

The agent inside Copilot Chat **cannot directly observe its own token usage** — that data lives in the Copilot backend. Do your best-effort estimate based on:

- Input context loaded (skills, prompts, files read)
- Output produced (report files written, decisions produced)
- Number of tool calls in the turn

Use these buckets:
- `~0` — no LLM work (session hook, file-only operations by a script)
- `~500` — small action (single file update, quick lookup, decision answer)
- `~2k` — moderate action (multi-file grep + a small artifact)
- `~8k` — larger action (a full phase artifact like Application-Assessment-Report)
- `~30k` — very large action (full Discovery Dossier, portfolio analysis)

**For authoritative token counts, check the Copilot Dashboard** — the estimates here are best-effort magnitude only.

The `turn=N` counter is **exact** and is the more reliable cost signal. Sum the turn counters at the end of a migration for total round-trip count.

## Turn counter

The `turn` counter is per-session and starts at `1` on session start. Each new LLM round-trip increments it. If unsure of the current turn, use `turn=?` and it can be reconciled later.

For hook-emitted entries (`session-started`, `session-ended`), use `turn=0` and `turn=<final>` respectively.

## Examples

**Full Phase 1 lifecycle:**
```
## 📜 Action Log
- 2026-07-09T10:40Z | actor=hook | action=session-started | tokens=~0 | turn=0 | notes="new session"
- 2026-07-09T10:41Z | actor=Assess-Any-Application | action=phase-started | tokens=~500 | turn=1
- 2026-07-09T10:43Z | actor=Assess-Any-Application | action=produced-discovery-dossier | files=+reports/Discovery-Dossier.md,+reports/Capability-Matrix.yaml | tokens=~30k | turn=2 | notes="stack=dotnet, workload=webapp"
- 2026-07-09T10:44Z | actor=Assess-Any-Application | action=phase-completed | tokens=~500 | turn=3
- 2026-07-09T10:45Z | actor=Phase1-Plan | action=phase-started | tokens=~500 | turn=4
- 2026-07-09T10:47Z | actor=Phase1-Plan | action=gate-passed | tokens=~500 | turn=5 | notes="Capability-Matrix + Discovery-Dossier present"
- 2026-07-09T10:52Z | actor=Phase1-Plan | action=produced-decisions-required | files=+reports/Decisions-Required.md,+reports/Application-Assessment-Report.md,+reports/Migration-Plan.md | tokens=~8k | turn=6 | notes="18 decisions PENDING"
- 2026-07-09T10:55Z | actor=User | action=answered-decision | value=".NET 10 LTS" | tokens=~0 | turn=7 | notes="D-01 target framework"
- 2026-07-09T10:56Z | actor=User | action=answered-decision | value="Azure SQL Database" | tokens=~0 | turn=7 | notes="D-04 database engine"
- 2026-07-09T11:02Z | actor=Phase2-MigrateCode | action=phase-blocked | reason="D-06 hosting platform PENDING" | tokens=~500 | turn=8
- 2026-07-09T11:15Z | actor=hook | action=session-ended | tokens=~0 | turn=8 | notes="total turns this session=8"
```

**Recovery scenario** (SessionStart hook parses the last 5 entries and injects them into the agent's `additionalContext`):
```
Migration context:
Recent actions:
  - Phase1-Plan produced-decisions-required at 10:52Z (18 PENDING)
  - User answered D-01 = ".NET 10 LTS"
  - User answered D-04 = "Azure SQL Database"
  - Phase2-MigrateCode gate-blocked (D-06 hosting platform PENDING)
Session ended at 11:15Z after 8 turns.
```

## Machine-readable regex

For hook parsing:

```
^- (?P<timestamp>\d{4}-\d{2}-\d{2}T\d{2}:\d{2}Z) \| actor=(?P<actor>\S+) \| action=(?P<action>\S+)(?P<fields>.*)$
```

Field extraction (per key):
```
\| (?P<key>files|tokens|turn|notes|value|reason)=(?P<value>"[^"]*"|\S+)
```

## Session summary block

At session end, the Stop hook appends a **summary line** below the log entries (once per session):

```
### Session summary — 2026-07-09
- Turns: 8 | Estimated tokens: ~48k | Phases advanced: Discovery → Phase 1 (in progress) | Decisions answered: 2/18
```

At migration end (Phase 6 complete), a **migration total** is added:

```
### Migration total
- Sessions: 12 | Total turns: 87 | Estimated total tokens: ~340k | Duration: 2026-07-01 → 2026-07-14 (13 days)
- Check Copilot Dashboard for authoritative token counts.
```

## Rules for prompts + agent + hooks

Every prompt file that produces an artifact or transitions a phase MUST include this contract (see `inject-action-log-contract.mjs` for the boilerplate):

> **Action Log contract**: After each meaningful action (see `action-log-format.md`), append one line to `## 📜 Action Log` in `reports/Report-Status.md` using the canonical format.

The agent file has a top-level `@agent rule: ALWAYS append an Action Log entry after each meaningful action.`

Hooks (`load-migration-state.*`, `update-status-report.*`) emit entries using `actor=hook`.

---

**See also:** `.github/skills/migration-report-template.md` for the full Report-Status.md skeleton (includes the empty Action Log section).
