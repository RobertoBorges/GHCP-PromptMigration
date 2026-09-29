# Skill: Stack Adapter — C++ on Windows (legacy) (Stub)

> **Stub adapter.** Provides classification + Azure target tendencies. Phase 2 effort for these stacks is typically **L or XL** with frequent **rebuild** recommendations. Pair with the Architect early.

## File Evidence

`*.cpp`, `*.h`, `*.hpp`, `*.vcxproj`, `CMakeLists.txt` (with Windows-specific paths)

## Version Targets

Modern C++ 17/20/23 supported; many legacy apps on Visual Studio 6 / 2003.

## Sub-Stack Detection

| Sub-stack | Signal | Azure target |
|-----------|--------|--------------|
| MFC desktop | MFC headers; `afxwin.h` | Rewrite to web; or run on Win VM |
| ATL/COM server | `atlbase.h`; COM registration | Rewrite as .NET or run on Win VM |
| Native Windows service | `CreateService` / SCM | Container Apps with Windows container; or rewrite |
| C++/CLI | `/clr` flag in project | Refactor C++/CLI boundary; target .NET-side |
| Cross-platform C++ | CMake + portable code | Container Apps (Linux container) |

## Risks / Migration Constraints

- MFC + ATL apps are typically Windows-only; Linux Container Apps is not a target.
- 32-bit-only apps need explicit Windows container 32-bit support.
- COM registration requires registry access — incompatible with most PaaS.
- Native dependencies (third-party DLLs, hardware DRM dongles) often kill PaaS option.
- Default recommendation: **rehost** to Azure VMs (Windows) when source is unavailable; **rewrite** otherwise.

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