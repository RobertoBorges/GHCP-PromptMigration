---
name: "model-selection"
description: "Determines which LLM model to use for each agent spawn"
domain: "orchestration"
confidence: "medium"
source: "adapted from squad-sdk"
---

# Model Selection

> Determines which LLM model to use for each agent spawn.

## SCOPE

✅ THIS SKILL PRODUCES:
- A resolved `model` parameter for every `task` tool call
- Persistent model preferences in `.squad/config.json`
- Spawn acknowledgments that include the resolved model

❌ THIS SKILL DOES NOT PRODUCE:
- Code, tests, or documentation
- Model performance benchmarks
- Cost reports or billing artifacts

## 5-Layer Model Resolution Hierarchy

Resolution is **first-match-wins** — the highest layer with a value wins.

| Layer | Name | Source | Persistence |
|-------|------|--------|-------------|
| **0a** | Per-Agent Config | `.squad/config.json` → `agentModelOverrides.{name}` | Persistent (survives sessions) |
| **0b** | Global Config | `.squad/config.json` → `defaultModel` | Persistent (survives sessions) |
| **1** | Session Directive | User said "use X" in current session | Session-only |
| **2** | Charter Preference | Agent's `charter.md` → `## Model` section | Persistent (in charter) |
| **3** | Task-Aware Auto | Code → sonnet, docs → haiku, architecture → opus | Computed per-spawn |
| **4** | Default | `claude-sonnet-4.6` | Hardcoded fallback |

## Task-Aware Auto-Selection (Layer 3)

| Task Type | Model | Rationale |
|-----------|-------|-----------|
| Code migration, refactoring | claude-sonnet-4.6 | Best balance of speed and code quality |
| Architecture, complex design | claude-opus-4.6 | Deep reasoning for migration planning |
| Documentation, walkthroughs | claude-haiku-4.5 | Fast, good enough for prose |
| Security review | claude-sonnet-4.6 | Needs precision for vulnerability detection |
| Infrastructure (Bicep/IaC) | claude-sonnet-4.6 | Template generation needs accuracy |
| Cost analysis | claude-haiku-4.5 | Structured output, lower complexity |
| Discovery & intake | claude-sonnet-4.6 | Classification needs broad knowledge |
| Presentation/PPTX | claude-haiku-4.5 | Slide generation is structured |

## User Commands

| Command | Effect |
|---------|--------|
| "use opus for architecture" | Sets Layer 1 override for architecture tasks |
| "always use sonnet" | Sets Layer 0b in `.squad/config.json` |
| "reset model preferences" | Clears Layer 0 overrides |
