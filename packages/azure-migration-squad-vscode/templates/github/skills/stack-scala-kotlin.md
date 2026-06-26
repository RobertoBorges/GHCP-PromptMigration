# Skill: Stack Adapter — Scala / Kotlin (JVM modern) (Stub)

> **Stub adapter.** Provides classification + Azure target tendencies. Phase 2 effort for these stacks is typically **L or XL** with frequent **rebuild** recommendations. Pair with the Architect early.

## File Evidence

`*.scala` (Scala), `*.kt`, `*.kts` (Kotlin), `build.sbt` (Scala), `build.gradle.kts` (Kotlin Gradle)

## Version Targets

Scala 3.x / 2.13.x; Kotlin 2.x. Both run on Java 21 LTS.

## Sub-Stack Detection

| Sub-stack | Signal | Azure target |
|-----------|--------|--------------|
| Akka / Pekko | `akka-actor` / `org.apache.pekko` | Container Apps / AKS (cluster awareness) |
| Play (Scala/Java) | `play-framework` | App Service / Container Apps |
| Spark (Scala) | `spark-core` | Synapse Spark / Databricks |
| Spring Boot Kotlin | Spring Boot + Kotlin DSL | App Service / Container Apps |
| Ktor (Kotlin) | `io.ktor` | App Service / Container Apps |
| Android backend (Kotlin) | Mostly stdlib | Container Apps |

## Risks / Migration Constraints

- Akka licensing model change (Lightbend) — Pekko (Apache fork) is the migration target.
- Spark cluster sizing on Azure (Synapse vs Databricks) is its own decision.
- Scala 2 → Scala 3 is a significant migration.
- Kotlin Multiplatform projects have build complexity.
- Native Akka clustering requires cluster-aware infra (AKS), not Container Apps.

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