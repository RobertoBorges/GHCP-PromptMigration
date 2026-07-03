# Skill: Stack Adapter — PowerBuilder (Stub)

> **Stub adapter.** Provides classification + Azure target tendencies. Phase 2 effort for these stacks is typically **L or XL** with frequent **rebuild** recommendations. Pair with the Architect early.

## File Evidence

`*.pbl`, `*.pbt`, `*.pbw`, `*.sru`

## Version Targets

PowerBuilder 2022 R3 still supported; older versions end-of-life.

## Sub-Stack Detection

| Sub-stack | Signal | Azure target |
|-----------|--------|--------------|
| Client/server desktop | DataWindow + thick client | Rewrite to .NET / Java web — **no PaaS for PB** |
| PowerBuilder .NET (legacy) | `*.pbproj` for .NET | Rewrite to ASP.NET Core |
| PowerServer (web) | PowerServer Toolkit | Rewrite to modern web stack |
| Appeon (cloud/mobile) | Appeon for PowerBuilder | Container migration possible; specialist needed |

## Risks / Migration Constraints

- **PowerBuilder is almost always a rewrite.** Talent shortage; vendor (Appeon) is the only support chain.
- DataWindow object → unique to PowerBuilder; must be redesigned for modern web.
- ODBC / OLE DB dependencies often hardcoded.
- Sybase Adaptive Server Enterprise often paired; database migration is part of the project.
- Default recommendation: **rebuild** on .NET / Java web; old app stays running until parity.

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