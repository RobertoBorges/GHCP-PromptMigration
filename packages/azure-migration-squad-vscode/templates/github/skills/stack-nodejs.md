# Skill: Stack Adapter — Node.js

> Stack adapter for any Node.js application: Express, NestJS, Koa, Fastify, Hapi, Next.js, Nuxt, SvelteKit, Remix, plain Node, TypeScript, serverless handlers.

## When to Use

- `stack.primary_stack: nodejs` in the Capability Matrix
- File evidence: `package.json`, `*.js`, `*.mjs`, `*.cjs`, `*.ts`, `*.tsx`, `*.jsx`, `node_modules/`, lockfiles

## Sub-Stack Detection

| Sub-stack | Detection signal | Typical migration target |
|-----------|------------------|--------------------------|
| **Express** | `express` in deps; `app.listen()` | App Service Linux Node / Container Apps |
| **NestJS** | `@nestjs/core` in deps; `NestFactory.create` | App Service / Container Apps |
| **Koa** | `koa` in deps | App Service / Container Apps |
| **Fastify** | `fastify` in deps | App Service / Container Apps / Functions |
| **Hapi** | `@hapi/hapi` in deps | App Service / Container Apps |
| **Next.js** | `next` in deps; `pages/` or `app/` directory; `next.config.js` | Static Web Apps (if SSG-heavy) or App Service / Container Apps |
| **Nuxt** | `nuxt` in deps | Static Web Apps / App Service / Container Apps |
| **Remix** | `@remix-run/*` in deps | App Service / Container Apps |
| **SvelteKit** | `@sveltejs/kit` in deps | Static Web Apps (with adapter-azure) |
| **Plain Node (no framework)** | `node` shebang scripts; CLI bins | Container Apps Jobs / Functions |
| **AWS Lambda handlers** | `exports.handler = async (event, context) =>`; `serverless.yml` | Azure Functions (v4 Node model) |
| **TypeScript** | `tsconfig.json`; `*.ts` files; `typescript` in devDeps | All above, with `tsc` build step |

## Node Version Detection

In priority order:

1. `engines.node` in `package.json`
2. `.nvmrc`
3. `Dockerfile` `FROM node:<version>` line
4. CI config → `node-version:` in GitHub Actions / `.tool-versions` (asdf)
5. `package-lock.json` `lockfileVersion` (rough indicator)

Target Azure-supported LTS: **Node 20** (current), Node 22 (next). Apps on Node ≤16 must upgrade.

## Package Manager Detection

| Lockfile present | Manager |
|------------------|---------|
| `package-lock.json` | npm |
| `pnpm-lock.yaml` | pnpm |
| `yarn.lock` | yarn (classic) |
| `yarn.lock` + `.yarnrc.yml` + `.yarn/` | yarn berry (v2+) |
| `bun.lockb` | bun |
| (none) | npm by convention |

Preserve the manager in CI/CD (Phase 5).

## Probes

### Manifest inspection

- `package.json`:
  - `engines.node`, `engines.npm`, `engines.pnpm`
  - `scripts` → especially `start`, `build`, `dev`, `test`
  - `main` / `module` / `exports` → entry points
  - `type: "module"` → ESM vs CommonJS
  - `dependencies` vs `devDependencies` → top deps
  - `private: true` → not published; standalone app

### Entry point inspection

- `scripts.start` → typical entry: `node server.js` / `node dist/main.js` / `nest start` / `next start`
- For NestJS / TypeScript apps, build artifact in `dist/`

### TypeScript build

- `tsconfig.json` → `target`, `module`, `moduleResolution`, `outDir`
- `tsc` build vs `swc` / `esbuild` / `tsx` / `ts-node` (runtime TS)

### Bundlers / build tools

| Tool | Files |
|------|-------|
| Webpack | `webpack.config.js` |
| Vite | `vite.config.js` / `vite.config.ts` |
| esbuild | `esbuild.*` script in package.json |
| Turbopack | `next.config.js` with `experimental.turbo` |
| Rollup | `rollup.config.js` |
| Parcel | `.parcelrc` |

### Database libraries

- `pg` / `postgres` → PostgreSQL
- `mysql2` / `mysql` → MySQL
- `mssql` → SQL Server
- `mongodb` → MongoDB
- `prisma` → Prisma ORM (any DB)
- `typeorm` → TypeORM
- `sequelize` → Sequelize ORM
- `knex` → Query builder
- `mongoose` → MongoDB ODM
- `redis` / `ioredis` → Redis

### Cloud SDK usage

- `aws-sdk` v2 / `@aws-sdk/*` v3 → will need translation to `@azure/*` SDKs (or keep dual-cloud)
- `@google-cloud/*` → will need translation
- `@azure/*` already → cloud-portable

### Worker / async patterns

- `bullmq` / `bull` → Redis-backed job queue → Container Apps with KEDA
- `node-cron` / `node-schedule` → in-process scheduler → Container Apps Jobs
- `agenda` → MongoDB-backed scheduler

### Tests

- `jest` / `vitest` / `mocha` / `ava` / `tap` / `node:test` (built-in)
- `supertest` for HTTP tests
- `playwright` / `cypress` for e2e

## Phase 2 Effort Mapping

| Sub-stack | Phase 2 effort | Notes |
|-----------|----------------|-------|
| Node 18/20/22 + modern framework | S | Containerize + deploy |
| Node 14/16 → Node 20 | S–M | Some npm package compatibility |
| Node ≤12 → Node 20 | M | Major library version bumps |
| Express + npm | S | Trivial |
| NestJS | S | Trivial |
| Next.js (SSR) | M | Output mode + Azure adapter selection |
| Next.js (SSG only) | S | Static Web Apps deployment |
| Lambda handlers → Functions | M | Trigger binding rewrite (event shapes differ) |
| Plain TS without build pipeline | M | Add `tsc` / `esbuild` build step |
| Yarn berry (PnP) | M | Compatibility issues with some hosting providers |

## Identity Modernization

| Today | Target |
|-------|--------|
| Passport.js with local strategy | Passport + `passport-azure-ad` or MSAL Node |
| JWT custom | MSAL Node (validates Entra tokens) |
| Auth0 / Cognito | Entra ID External Identities (or keep + integrate) |
| Session cookies (express-session) | Stateless JWT preferred; or session backed by Redis |

## Target Azure Mapping

| Sub-stack | Primary Azure target | Secondary |
|-----------|----------------------|-----------|
| Express / Fastify / Koa / Hapi | App Service Linux Node | Container Apps |
| NestJS | App Service Linux Node | Container Apps |
| Next.js (SSR) | App Service Linux Node | Container Apps; Static Web Apps with Standard tier |
| Next.js (SSG) | Static Web Apps | App Service |
| Nuxt | App Service Linux Node | Container Apps; Static Web Apps with adapter |
| SvelteKit | Static Web Apps (adapter-azure) | App Service |
| Lambda handlers | Azure Functions (v4 Node model) | Container Apps |
| Worker (BullMQ) | Container Apps + KEDA | AKS |
| Cron script | Container Apps Jobs (cron trigger) | Functions Timer |

## Anti-Patterns

- Don't deploy `node_modules` in the container. Build clean (`npm ci --omit=dev`).
- Don't run TypeScript at runtime in production (`ts-node`). Build to JS first.
- Don't preserve `tsx` watch mode in production CMD.
- Don't ignore `engines.node` mismatches between local and Azure. Pin the runtime.
- Don't migrate AWS Lambda handlers 1:1 to Functions. The trigger event shape differs — rewrite the binding layer.
- Don't keep AWS SDK v2 in 2026+ (sunset). Migrate to v3 or Azure SDK as part of Phase 2.

## Output Checklist

- [ ] Sub-stack identified (one of the 11 above)
- [ ] Node version captured (target: LTS)
- [ ] Package manager identified
- [ ] ESM vs CommonJS captured
- [ ] TypeScript usage captured (with build pipeline)
- [ ] Bundler / build tool captured
- [ ] Database libraries inventoried
- [ ] Cloud SDK dependencies flagged (AWS / GCP migration scope)
- [ ] Worker / scheduler pattern captured
- [ ] Tests framework captured
- [ ] Auth library captured
- [ ] Phase 2 effort label assigned (S/M/L/XL)
- [ ] Target Azure compute candidate noted
