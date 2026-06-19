# GHCP-PromptMigration — Hub de Documentación para el Azure Migration Squad

> **Agentes universales de migración a Azure para GitHub Copilot + Squad.** Cualquier origen. Cualquier stack. Un comando.

[![npm](https://img.shields.io/npm/v/@robertoborges/azure-migration-squad?label=npm&color=blue)](https://www.npmjs.com/package/@robertoborges/azure-migration-squad)
[![Squad](https://img.shields.io/badge/squad--cli-compatible-blueviolet?logo=githubcopilot)](https://github.com/bradygaster/squad)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](../../LICENSE)

> 🌎 Translated from English — for the latest, always check [README.md](../../README.md).

Este es el **hub de documentación canónico** del Azure Migration Squad. El equipo migra **cualquier aplicación** — sin importar dónde se ejecute hoy o con qué esté construida — a Azure. Descubrimiento primero, basado en evidencia, orquestado por el squad.

## Tres formas de instalar

### 🥇 Opción 1 — npm (principal, recomendada)

```bash
# 1. Instalar Squad (una vez)
npm install -g @bradygaster/squad-cli
squad init

# 2. Añadir el Azure Migration Squad
npx @robertoborges/azure-migration-squad@insider init

# 3. Abrir GitHub Copilot Chat y ejecutar:
/assess-any-application
```

### 🥈 Opción 2 — Marketplace de Squad

```bash
squad plugin marketplace add RobertoBorges/GHCP-PromptMigration
squad plugin install azure-migration-squad
```

### 🥉 Opción 3 — Plantilla de GitHub *(próximamente — Wave D)*

## El squad — 15 especialistas

| # | Agente | Alias | Especialidad |
|---|--------|-------|--------------|
| 1 | **Discovery Engineer** | Saul Bloom Jr. | Intake, clasificación, recomendación de 6Rs, Matriz de Capacidades |
| 2 | Architect | Danny Ocean | Aprobación de estrategia, arquitectura objetivo, secuenciación |
| 3 | Coder | Rusty Ryan | Modernización de código, actualización de frameworks |
| 4 | Tester | Linus Caldwell | Validación, pruebas de humo, QA de prompts |
| 5 | Azure Specialist | Basher Tarr | Hosting Azure, identidad, landing zones |
| 6 | DevOps Engineer | Turk Malloy | CI/CD, automatización de despliegues |
| 7 | Observability Engineer | Livingston Dell | Monitoreo, App Insights, alertas |
| 8 | Database Specialist | The Amazing Yen | Migración de esquemas, cutover, validación de datos |
| 9 | Performance Engineer | Virgil Malloy | Carga, baselines, escalado |
| 10 | Security Auditor | Frank Catton | Auth, secrets, RBAC, cumplimiento |
| 11 | Evaluator | Saul Bloom | Calidad de prompts, revisión de regresiones |
| 12 | Cutover Commander | Reuben Tishkoff | Lanzamiento, rollback, go-live |
| 13 | Scribe | Roman Nagel | Journal, log de decisiones |
| 14 | Presentation Specialist | Tess Ocean | Decks de estado, resúmenes ejecutivos |
| 15 | Cost Engineer | The Accountant | Modelos de costo, right-sizing, FinOps |

## Cobertura

**Entornos de origen:** on-premise, AWS, GCP, Oracle, VMware, Kubernetes, registros de contenedores, repos de GitHub, ZIPs, mainframes

**Stacks:** .NET, Java, Python, Node.js, PHP, Ruby, Go, Perl, Rust, COBOL, Oracle Forms, PowerBuilder, Delphi/VB6, Scala/Kotlin, C++ Windows

**Estrategias:** Rehost / Replatform / Refactor / Rearchitect / Rebuild / Retire / Retain — elegidas por un árbol de decisión de 12 ramas (no solo 6Rs)

## Telemetría — opt-out por defecto

```bash
# Cualquiera de estas desactiva la telemetría:
azure-migration-squad telemetry off
export AZURE_MIGRATION_SQUAD_TELEMETRY=0
export DO_NOT_TRACK=1
```

Política completa: [docs/telemetry.md](../telemetry.md) (en inglés)
Política de privacidad: [docs/privacy-policy.md](../privacy-policy.md) (en inglés)

## Contribuir

Aceptamos contribuciones en cualquier idioma. Guía completa: [docs/contributing-adapters.md](../contributing-adapters.md) (en inglés).

Si quieres traducir más documentación al español o portugués, abre un PR contra `docs/translations/`.

## Licencia

MIT © Roberto Borges
