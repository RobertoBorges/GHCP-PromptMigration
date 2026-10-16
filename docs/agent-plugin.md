# Azure Migration Agent plugin

The repository is also a native **Copilot-format agent plugin**. Its root `plugin.json` points directly to `.github/skills/` and `.github/agents/`: 65 skills (35 workflow commands and 30 knowledge skills) and 10 agents, including AWS account assessment and AWS-to-Azure migration.

This is the Copilot format supported by [VS Code agent plugins](https://code.visualstudio.com/docs/agent-customization/agent-plugins), not an Agent Plugins 1.0 package. It intentionally omits the Agent Plugins `$schema`, because that format discovers components from different directories and does not support these top-level custom paths.

## Choose an installation

| Option | What it provides |
|---|---|
| VS Code extension / VSIX | Workspace initialization, sidebar catalogs, pending-decisions view, status bar, welcome UI, and workspace instructions/hooks |
| Native agent plugin | The same skills and agents from their installed plugin directory, without copying them into each project |

The plugin does **not** register hooks, MCP servers, or workspace-wide `copilot-instructions.md`. In particular, installing it does not activate the AWS read-only command guard. Read-only assessment instructions remain in the AWS skills; use a read-only AWS identity and the VSIX workspace setup when executable workspace guards are required. The extension's UI is not part of the plugin.

Avoid enabling both copies of the same catalog in one workspace; duplicate agents and commands can be confusing. Neither mode publishes, deploys, or accesses a cloud account merely by being installed.

## Try locally before publishing

Clone this repository, then add its **root directory**, not `.github`, to VS Code's user settings:

```json
{
  "chat.plugins.enabled": true,
  "chat.pluginLocations": {
    "C:\\git\\GHCP-PromptMigration": true
  }
}
```

Use a VS Code version that offers agent plugins. Open **Chat: Open Customizations**, then **Plugins**, and verify `azure-migration-agent` is enabled. Check **Chat: Configure Skills** and the agent picker; start with **Code Migration Modernization Agent**, **Discovery Intake**, or **Debug Migration**.

Run `/assess-any-application` first, then `/phase1-plan` and Phase 2-6. Use the command spelling shown by your client's plugin skill picker if it namespaces plugin commands. The remaining seven agents are dispatched as specialists.

Bundled `.github/...` reference paths refer to resources in the **installed plugin repository**. Generated `reports/`, application edits, and deployment files belong in the **target application workspace**, not the plugin installation. If a workflow needs workspace-wide instructions or executable hooks, initialize that workspace with the extension instead of assuming the plugin installs them.

For a non-persistent CLI discovery check:

```powershell
copilot --plugin-dir C:\git\GHCP-PromptMigration plugin list --json
```

## Install from Git after the manifests are pushed

Run **Chat: Install Plugin From Source** and enter:

```text
https://github.com/RobertoBorges/GHCP-PromptMigration.git
```

The manifests must exist in the revision being installed. A local VSIX build alone does not publish the Git-sourced plugin.

## Discover through the repository marketplace

The `.github/plugin/marketplace.json` index exposes the root plugin. Once committed and pushed, add this repository to the VS Code user setting:

```json
{
  "chat.plugins.marketplaces": [
    "RobertoBorges/GHCP-PromptMigration"
  ]
}
```

In Extensions, search `@agentPlugins`, find **azure-migration-agent**, review the trust prompt and install. Alternatively, add the marketplace from the Plugins page of the Agent Customizations editor.

Use **Extensions: Check for Extension Updates** to refresh installed plugins. Plugin updates require a new `version` in both `plugin.json` and its marketplace entry.

## Release checks

The extension, root plugin, marketplace entry and workspace lockfile share one version. `npm run validate:plugin` checks version agreement and verifies that the component paths resolve and skill names match their directory names.

The local release script updates all four version locations. Release-please's `extra-files` configuration updates the plugin manifests and workspace lockfile in automated release PRs. `.release-please-manifest.json` tracks the last released version, not an unpublished local preview.

```powershell
npm run validate:all
npm run test:release
npm run package --workspace packages/azure-migration-squad-vscode
```

The CI and release content-pack artifacts also include `plugin.json` and the marketplace index, so an extracted content pack can be registered as a local plugin.

See [Publishing the extension](./publishing-vscode-extension.md) for VSIX publishing. No additional plugin registry account is required for Git-source or local-path installation.
