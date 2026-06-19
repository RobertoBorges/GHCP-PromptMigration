# Skill: Stack Adapter — Delphi / Visual Basic 6 (Stub)

> **Stub adapter.** Provides classification + Azure target tendencies. Phase 2 effort for these stacks is typically **L or XL** with frequent **rebuild** recommendations. Pair with the Architect early.

## File Evidence

`*.dpr`, `*.pas`, `*.dpk`, `*.dfm` (Delphi); `*.vbp`, `*.frm`, `*.bas`, `*.cls` (VB6)

## Version Targets

Delphi 11/12 still active. VB6 is out of all Microsoft support since 2008.

## Sub-Stack Detection

| Sub-stack | Signal | Azure target |
|-----------|--------|--------------|
| Delphi VCL (Win) | `*.dpr` + `*.dfm` | Rewrite to .NET / web — no PaaS for VCL |
| Delphi FMX (cross-platform) | FireMonkey forms | Rewrite to MAUI or web |
| VB6 thick client | `*.vbp` | Rewrite to .NET WinForms (interim) → ASP.NET Core (target) |
| VB6 COM components | COM+ services | Rewrite as .NET; expose via REST |

## Risks / Migration Constraints

- **VB6 has no supported runtime path.** Out of support since 2008.
- COM dependencies often deep (Office automation, ActiveX, custom OCX).
- Third-party visual components often discontinued.
- BDE / IBX / dbExpress data access → replace with ADO.NET or EF Core.
- Typical recommendation: **rebuild** on .NET. Cost Engineer must scope effort.

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