# Skill: Stack Adapter — Ruby (Stub)

> **Stub adapter.** Provides classification + Azure target tendencies. Phase 2 effort for these stacks is typically **L or XL** with frequent **rebuild** recommendations. Pair with the Architect early.

## File Evidence

`*.rb`, `Gemfile`, `Gemfile.lock`, `Rakefile`, `*.erb`, `*.rake`, `config.ru`

## Version Targets

Ruby 3.3+ (target). Ruby 2.x is end-of-life; mandatory upgrade.

## Sub-Stack Detection

| Sub-stack | Signal | Azure target |
|-----------|--------|--------------|
| Rails | `rails` in Gemfile; `config/application.rb`; `app/` MVC dirs | App Service Linux Ruby / Container Apps |
| Sinatra | `sinatra` in Gemfile; `config.ru` | App Service / Container Apps |
| Hanami | `hanami` in Gemfile | App Service / Container Apps |
| Sidekiq (worker) | `sidekiq` in Gemfile; `config/sidekiq.yml` | Container Apps + KEDA (Redis) |
| Plain Rack | `config.ru` only | App Service / Container Apps |

## Risks / Migration Constraints

- Ruby 2.x end-of-life — mandatory upgrade to 3.x.
- `bundler` lockfile version compatibility across Ruby version changes.
- Native gems (`nokogiri`, `pg`, `mysql2`) may need build dependencies in container.
- Asset pipeline (Sprockets vs Webpacker vs jsbundling-rails) — pick one for Phase 2.
- Action Cable WebSocket → needs sticky session OR Azure SignalR.
- Sidekiq Pro / Enterprise licenses if used.

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