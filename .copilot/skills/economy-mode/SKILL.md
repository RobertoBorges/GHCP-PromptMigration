---
name: "economy-mode"
description: "Shifts model selection to cost-optimized alternatives when economy mode is active"
domain: "model-selection"
confidence: "medium"
source: "adapted from squad-sdk"
---

# Economy Mode

> Reduces model costs across the squad without sacrificing critical migration quality.

## SCOPE

✅ THIS SKILL PRODUCES:
- A modified model selection table applied when economy mode is active
- `economyMode: true` written to `.squad/config.json` when activated persistently
- Spawn acknowledgments with `💰` indicator when economy mode is active

❌ THIS SKILL DOES NOT PRODUCE:
- Code, tests, or documentation
- Cost reports or billing artifacts
- Changes to explicit user model overrides (user intent always wins)

## Activation Methods

| Method | How |
|--------|-----|
| Session phrase | "use economy mode", "save costs", "go cheap", "reduce costs" |
| Persistent config | `"economyMode": true` in `.squad/config.json` |

**Deactivation:** "turn off economy mode", "disable economy mode", or remove `economyMode` from `config.json`.

## Economy Model Selection Table

When economy mode is **active**, auto-selection shifts down one tier:

| Task Type | Normal Model | Economy Model |
|-----------|-------------|---------------|
| Code migration | claude-sonnet-4.6 | claude-haiku-4.5 |
| Architecture | claude-opus-4.6 | claude-sonnet-4.6 |
| Documentation | claude-haiku-4.5 | claude-haiku-4.5 |
| Security review | claude-sonnet-4.6 | claude-haiku-4.5 |
| Infrastructure | claude-sonnet-4.6 | claude-haiku-4.5 |
| Cost analysis | claude-haiku-4.5 | claude-haiku-4.5 |
| Discovery | claude-sonnet-4.6 | claude-haiku-4.5 |

## When NOT to Use Economy Mode

- During security hardening phases (precision matters)
- For complex multi-service architecture decisions
- When Discovery confidence is low and re-classification is needed
