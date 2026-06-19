# MCP Configuration Notes — Ocean's Twelve — The Azure Heist

> MCP is optional in this repository. The core migration workflow is driven by `.github\prompts\`, `.github\chatmodes\`, `.github\skills\`, and `.github\hooks\`.

## Current State

- **No repository-level MCP config is currently checked in.** There is no committed `.copilot\mcp-config.json` in the repo root.
- **No workspace-level MCP config is currently checked in.** There is no committed `.vscode\mcp.json` for this repo.
- **User-level MCP remains optional.** Individual operators can use their own `~\\.copilot\\mcp-config.json` if they need extra tools.

## What MCP Should and Should Not Do Here

| Use MCP for | Do not use MCP for |
|-------------|--------------------|
| External systems or tools that are not already covered by the built-in CLI, prompts, or skills | Replacing `.github\prompts\` or `.github\chatmodes\` as the primary operator surface |
| Safe, repeatable integrations that can be documented and shared | Referencing undeclared server names from prompts or chatmodes |
| Optional enhancements that improve discovery, reporting, or external lookup | Hiding required repo behavior in a user-local config nobody else can see |

## Tooling Alignment Rules

1. Treat `.github\prompts\` and `.github\chatmodes\` as the canonical workflow entrypoints.
2. Only mention an MCP server in prompt/chatmode docs if the server name, purpose, and setup steps are documented.
3. If a repo-level or workspace-level MCP config is added later, update this file and the relevant operator docs in the same change.
4. Prefer prompt-local `#file:` references, hooks, and built-in CLI commands before introducing MCP dependencies.

## Config Locations

1. **Repository-level:** `.copilot\mcp-config.json`
2. **Workspace-level:** `.vscode\mcp.json`
3. **User-level:** `~\\.copilot\\mcp-config.json`

## Change Checklist

Before treating a new MCP dependency as real:

- [ ] The config file is actually committed at repo or workspace scope, or clearly called out as user-local only.
- [ ] Prompt/chatmode references match the real server name.
- [ ] Authentication/setup steps are documented.
- [ ] The MCP dependency is optional unless the repo explicitly adopts it as a required part of the workflow.

