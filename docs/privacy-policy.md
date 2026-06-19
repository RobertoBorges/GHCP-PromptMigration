# Privacy Policy — Azure Migration Squad

> Last updated: 2026-06-18 · Effective: 2026-06-18

## Who this applies to

This privacy policy applies to users of the `@robertoborges/azure-migration-squad` npm package, the GitHub Copilot agents and skills it installs, and visitors to the [GHCP-PromptMigration](https://github.com/RobertoBorges/GHCP-PromptMigration) GitHub repository.

This policy does **not** apply to:
- The GitHub Copilot product itself (governed by [Microsoft's privacy policy](https://privacy.microsoft.com/en-us/privacystatement))
- The `@bradygaster/squad-cli` runtime (governed by its own policy)
- Azure services your migration ends up on (governed by your Azure agreement)
- Any external APIs the squad recommends (PostHog, GitHub, etc. — each has its own policy)

## Data we collect

### From CLI users (`@robertoborges/azure-migration-squad`)
**Anonymous usage telemetry** — see [docs/telemetry.md](./telemetry.md) for the full event/property list. No PII. Opt-out at any time.

### From GitHub repository visitors
GitHub records visitor counts, geographic regions, and referrers via the standard GitHub Insights feature. We see only what GitHub shows us in the repo Insights tab — same as any other repo.

### From GitHub issues / PRs
Whatever you voluntarily provide in an issue or PR — your GitHub username, comment text, and any files you attach. Standard GitHub behavior; nothing extra is collected.

## How long we keep data

| Data | Retention |
|------|-----------|
| Anonymous CLI telemetry events | 7 days (PostHog Cloud free-tier default) |
| Anonymous install ID (`distinct_id`) | Forever, until you ask us to delete it |
| GitHub Insights data | Per GitHub's retention (typically 14 days for visitor traffic) |
| Issue/PR content | Forever, until you delete it from GitHub |

## Third parties

| Vendor | What they receive | Purpose | Privacy policy |
|--------|-------------------|---------|----------------|
| [PostHog Cloud (US)](https://posthog.com) | Anonymous telemetry events from the CLI | Product analytics | https://posthog.com/privacy |
| [GitHub / Microsoft](https://github.com) | Repository data, Issues, PRs, visitor info | Hosting + collaboration | https://privacy.microsoft.com |
| [npm Inc.](https://www.npmjs.com) | npm package downloads | Package distribution | https://www.npmjs.com/policies/privacy |

We do not sell data. We do not use data for ad targeting. We do not run retargeting pixels.

## Your rights

You have the right to:

1. **Opt out of telemetry** at any time — see [docs/telemetry.md#opt-out-options](./telemetry.md#opt-out-options). No login needed; no questions asked.
2. **Request deletion** of your anonymous install ID from PostHog — open an issue with your install ID (found in `~/.config/azure-migration-squad/config.json`). We'll process within 7 days.
3. **Access** what we have — same channel; we'll respond with any events tied to your install ID.
4. **Object** — same channel; we'll comply unless we have a documented legal reason not to (there are no current legal-retention requirements for this dataset).

These rights are guaranteed for everyone, not just EU/CA residents. We hold ourselves to the GDPR + CCPA standard globally.

## What about my code / my customer's code?

When you run the squad against your application:
- **Source code, prompts, customer data, capability matrices, discovery dossiers** stay on your machine. The CLI never uploads them.
- **GitHub Copilot itself** sees what you send to it in chat — that's between you and Microsoft, governed by Microsoft's policy.
- **Azure deployments** are between you and Azure.

The migration squad does not have a backend. There is no SaaS. There is no remote evaluation. Everything except the small telemetry events runs entirely on your machine.

## Security

- The npm package has zero runtime dependencies — no supply-chain risk from transitive deps.
- The PostHog API key shipped in the CLI is a **write-only** Project Key — it cannot read or delete data.
- Telemetry network calls have a 2-second timeout and fail silently.
- The CLI never reads files outside the project root unless you point `init` at a different path.
- All build artifacts and the published npm package are reproducible from this monorepo via `npm run build`.

## Children

The npm package is a developer tool not intended for children. We don't knowingly collect any data from anyone under 13.

## Changes to this policy

Material changes will be:
1. Documented in [CHANGELOG.md](../packages/azure-migration-squad/CHANGELOG.md) with a `### Privacy` section
2. Announced in the release notes
3. Reflected here with a "Last updated" bump and a banner at the top of the page for 30 days

We will never silently change this policy.

## Contact

Open an issue at https://github.com/RobertoBorges/GHCP-PromptMigration/issues for any privacy question or request.

---

This policy is open source. Read it, audit it, propose improvements via PR.
