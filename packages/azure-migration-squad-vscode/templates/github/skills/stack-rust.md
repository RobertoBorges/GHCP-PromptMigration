# Skill: Stack Adapter — Rust (Stub)

> **Stub adapter.** Provides classification + Azure target tendencies. Phase 2 effort for these stacks is typically **L or XL** with frequent **rebuild** recommendations. Pair with the Architect early.

## File Evidence

`*.rs`, `Cargo.toml`, `Cargo.lock`

## Version Targets

Rust stable (current). Apps on Rust < 1.70 should bump.

## Sub-Stack Detection

| Sub-stack | Signal | Azure target |
|-----------|--------|--------------|
| Actix-web | `actix-web` | Container Apps |
| Axum | `axum` | Container Apps |
| Rocket | `rocket` | Container Apps |
| Tonic (gRPC) | `tonic` | Container Apps |
| CLI / one-shot | `main.rs` exits | Container Apps Jobs |
| WASM target | `wasm-pack` artifacts | Static Web Apps (browser side) |

## Risks / Migration Constraints

- Build time is significant; CI caching strategy matters.
- Cross-compile needed if dev OS != target Linux.
- Multi-stage Dockerfile mandatory (`cargo build --release` then copy binary).
- Some crates require system libs (OpenSSL, libpq) — pin to `rustls` where possible for portability.

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