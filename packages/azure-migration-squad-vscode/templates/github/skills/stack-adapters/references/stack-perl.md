# Skill: Stack Adapter — Perl (Stub)

> **Stub adapter.** Provides classification + Azure target tendencies. Phase 2 effort for these stacks is typically **L or XL** with frequent **rebuild** recommendations. Pair with the Architect early.

## File Evidence

`*.pl`, `*.pm`, `*.t`, `*.psgi`, `cpanfile`, `Makefile.PL`

## Version Targets

Perl 5.36+ recommended; many legacy apps run 5.8-5.10.

## Sub-Stack Detection

| Sub-stack | Signal | Azure target |
|-----------|--------|--------------|
| Mojolicious | `Mojolicious` in cpanfile | Container Apps |
| Dancer / Dancer2 | `Dancer2` | Container Apps / App Service |
| Catalyst | `Catalyst::Runtime` | Container Apps |
| PSGI / Plack | `Plack` + `app.psgi` | Container Apps |
| Legacy CGI | mod_perl / Apache CGI | Container Apps with Apache; or rewrite |

## Risks / Migration Constraints

- Perl is often a **rebuild candidate** — talent shortage is a real risk.
- CPAN dependency hell (binary compat across Perl versions).
- `mod_perl` apps often don't separate config from code.
- Custom build of Perl required for some legacy apps — container needs same.
- Often, recommended strategy is `rebuild` (rewrite to Python / Node / Go).

## Phase 2 Effort

Default: **L** (medium-to-large). Often **XL** when source predates current supported versions.

## Identity Modernization

Default: replace any custom auth with **Entra ID OIDC** at the app boundary. Map current users to Entra ID groups.

## Output Checklist

- [ ] Sub-stack identified
- [ ] Runtime version captured (and flagged if EOL)
- [ ] Top dependencies / vendor libs captured
- [ ] Native dependencies / Windows-only / hardware deps flagged
- [ ] Approach decided: `replatform` / `refactor` / `rebuild`
- [ ] Architect + (often) Cost Engineer flagged as required specialists
- [ ] Target Azure compute candidate noted (often **AKS**, **Container Apps**, or **VM**)