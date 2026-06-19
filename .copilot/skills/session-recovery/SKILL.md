---
name: "session-recovery"
description: "Find and resume interrupted Copilot CLI sessions using session_store queries"
domain: "workflow-recovery"
confidence: "high"
source: "adapted from squad-sdk"
---

# Session Recovery

> Find and resume interrupted Copilot CLI sessions.

## SCOPE

✅ THIS SKILL PRODUCES:
- Queries to find interrupted sessions
- Guidance on resuming partially-completed migration work
- Detection of orphaned branches or in-progress issues

❌ THIS SKILL DOES NOT PRODUCE:
- Automatic resumption without user confirmation
- Changes to session store data

## Context

Squad agents run in Copilot CLI sessions that can be interrupted — terminal crashes, network drops, machine restarts, or accidental window closes. When this happens, in-progress migration work may be left partially completed: branches with uncommitted changes, phases half-executed, or Discovery Dossiers incomplete.

## Patterns

### 1. Find Recent Sessions

```sql
SELECT
  s.id,
  s.summary,
  s.cwd,
  s.branch,
  s.updated_at,
  (SELECT title FROM checkpoints
   WHERE session_id = s.id
   ORDER BY checkpoint_number DESC LIMIT 1) AS last_checkpoint
FROM sessions s
WHERE s.updated_at >= datetime('now', '-24 hours')
ORDER BY s.updated_at DESC;
```

### 2. Find Sessions for This Repository

```sql
SELECT s.id, s.summary, s.branch, s.updated_at
FROM sessions s
WHERE s.repository ILIKE '%GHCP-PromptMigration%'
ORDER BY s.updated_at DESC
LIMIT 10;
```

### 3. Check for Orphaned Work

Look for sessions that modified files but may not have committed:

```sql
SELECT sf.session_id, sf.file_path, sf.tool_name
FROM session_files sf
JOIN sessions s ON s.id = sf.session_id
WHERE s.updated_at >= datetime('now', '-48 hours')
  AND sf.tool_name IN ('edit', 'create')
ORDER BY sf.first_seen_at DESC;
```

## Recovery Workflow

1. **Query** recent sessions for this repo
2. **Identify** the interrupted session's last checkpoint
3. **Check** git status for uncommitted changes on the session's branch
4. **Resume** from the last known good state, picking up where the migration phase left off
5. **Log** the recovery in `.squad/decisions.md`
