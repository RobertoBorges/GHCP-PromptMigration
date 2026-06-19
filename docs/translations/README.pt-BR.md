# GHCP-PromptMigration — Hub de Documentação do Azure Migration Squad

> **Agentes universais de migração para Azure no GitHub Copilot + Squad.** Qualquer origem. Qualquer stack. Um comando.

[![npm](https://img.shields.io/npm/v/@robertoborges/azure-migration-squad?label=npm&color=blue)](https://www.npmjs.com/package/@robertoborges/azure-migration-squad)
[![Squad](https://img.shields.io/badge/squad--cli-compatible-blueviolet?logo=githubcopilot)](https://github.com/bradygaster/squad)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](../../LICENSE)

> 🌎 Tradução do inglês — para a versão mais atualizada, consulte sempre [README.md](../../README.md).

Este é o **hub de documentação canônico** do Azure Migration Squad. O time migra **qualquer aplicação** — não importa onde rode hoje ou em que foi escrita — para Azure. Discovery primeiro, baseado em evidências, orquestrado pelo squad.

## Três formas de instalar

### 🥇 Opção 1 — npm (principal, recomendada)

```bash
# 1. Instalar o Squad (uma vez só)
npm install -g @bradygaster/squad-cli
squad init

# 2. Adicionar o Azure Migration Squad
npx @robertoborges/azure-migration-squad@insider init

# 3. Abrir o GitHub Copilot Chat e rodar:
/assess-any-application
```

### 🥈 Opção 2 — Marketplace do Squad

```bash
squad plugin marketplace add RobertoBorges/GHCP-PromptMigration
squad plugin install azure-migration-squad
```

### 🥉 Opção 3 — Template do GitHub *(em breve — Wave D)*

## O squad — 15 especialistas

| # | Agente | Codinome | Especialidade |
|---|--------|----------|---------------|
| 1 | **Discovery Engineer** | Saul Bloom Jr. | Intake, classificação, recomendação 6Rs, Matriz de Capacidades |
| 2 | Architect | Danny Ocean | Aprovação de estratégia, arquitetura alvo, sequenciamento |
| 3 | Coder | Rusty Ryan | Modernização de código, upgrade de frameworks |
| 4 | Tester | Linus Caldwell | Validação, smoke tests, QA de prompts |
| 5 | Azure Specialist | Basher Tarr | Hosting Azure, identidade, landing zones |
| 6 | DevOps Engineer | Turk Malloy | CI/CD, automação de deploy |
| 7 | Observability Engineer | Livingston Dell | Monitoramento, App Insights, alertas |
| 8 | Database Specialist | The Amazing Yen | Migração de schema, cutover, validação de dados |
| 9 | Performance Engineer | Virgil Malloy | Carga, baselines, escalonamento |
| 10 | Security Auditor | Frank Catton | Auth, segredos, RBAC, compliance |
| 11 | Evaluator | Saul Bloom | Qualidade de prompts, revisão de regressões |
| 12 | Cutover Commander | Reuben Tishkoff | Rollout, rollback, go-live |
| 13 | Scribe | Roman Nagel | Journal, log de decisões |
| 14 | Presentation Specialist | Tess Ocean | Decks de status, resumos executivos |
| 15 | Cost Engineer | The Accountant | Modelos de custo, right-sizing, FinOps |

## Cobertura

**Ambientes de origem:** on-premise, AWS, GCP, Oracle, VMware, Kubernetes, container registries, repositórios GitHub, ZIPs, mainframes

**Stacks:** .NET, Java, Python, Node.js, PHP, Ruby, Go, Perl, Rust, COBOL, Oracle Forms, PowerBuilder, Delphi/VB6, Scala/Kotlin, C++ Windows

**Estratégias:** Rehost / Replatform / Refactor / Rearchitect / Rebuild / Retire / Retain — escolhidas por uma árvore de decisão de 12 ramos (vai além de só rotular 6Rs)

## Telemetria — opt-out por padrão

```bash
# Qualquer uma dessas desliga a telemetria:
azure-migration-squad telemetry off
export AZURE_MIGRATION_SQUAD_TELEMETRY=0
export DO_NOT_TRACK=1
```

Política completa: [docs/telemetry.md](../telemetry.md) (em inglês)
Política de privacidade: [docs/privacy-policy.md](../privacy-policy.md) (em inglês)

## Contribuir

Aceitamos contribuições em qualquer idioma. Guia completo: [docs/contributing-adapters.md](../contributing-adapters.md) (em inglês).

Se você quiser traduzir mais documentação para português ou espanhol, abra um PR em `docs/translations/`.

## Licença

MIT © Roberto Borges
