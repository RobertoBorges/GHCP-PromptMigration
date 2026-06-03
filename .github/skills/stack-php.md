# Skill: Stack Adapter — PHP

> Stack adapter for any PHP application: Laravel, Symfony, CodeIgniter, CakePHP, Yii, Zend / Laminas, Slim, plain LAMP, WordPress, Magento, Drupal, Joomla.

## When to Use

- `stack.primary_stack: php` in the Capability Matrix
- File evidence: `*.php`, `composer.json`, `composer.lock`, `*.phtml`, `index.php`

## Sub-Stack Detection

| Sub-stack | Detection signal | Typical migration target |
|-----------|------------------|--------------------------|
| **Laravel** | `laravel/framework` in composer.json; `artisan` file; `app/`, `config/`, `routes/` | App Service Linux PHP / Container Apps |
| **Symfony** | `symfony/framework-bundle`; `bin/console`; `config/` | App Service / Container Apps |
| **CodeIgniter 4** | `codeigniter4/framework`; `spark` file | App Service / Container Apps |
| **CakePHP** | `cakephp/cakephp`; `bin/cake` | App Service / Container Apps |
| **Yii** | `yiisoft/yii2`; `yii` file | App Service / Container Apps |
| **Slim** | `slim/slim` | App Service / Container Apps |
| **WordPress** | `wp-config.php`; `wp-content/` | App Service for WordPress (managed) / Container Apps |
| **Magento 2** | `magento/product-community-edition`; `bin/magento` | Container Apps / AKS (heavy) |
| **Drupal** | `drupal/core`; `core/lib/Drupal.php` | App Service / Container Apps |
| **Joomla** | `joomla/cms`; `administrator/` | App Service / Container Apps |
| **Plain LAMP** | `index.php` + `*.php` includes; no framework | Containerize or rewrite |

## PHP Version Detection

In priority order:

1. `composer.json` → `require.php` (e.g., `"php": ">=8.1"`)
2. `composer.lock` → `platform.php`
3. `Dockerfile` → `FROM php:8.x-...`
4. `.php-version` file
5. CI config

Target Azure-supported: **PHP 8.3** (8.2 still supported). Apps on PHP ≤ 7.4 must upgrade.

## Probes

### Composer manifest inspection

- `composer.json`:
  - `require.php` → PHP version constraint
  - `require` → top deps (Laravel / Symfony / framework + extensions)
  - `require-dev` → testing tools
  - `autoload.psr-4` → namespace mapping
  - `scripts` → composer scripts (often used for build steps)

### Configuration files

| File | Framework / purpose |
|------|---------------------|
| `.env` + `.env.example` | Laravel / Symfony env config (secrets!) |
| `config/database.php` | Laravel DB config |
| `config/packages/doctrine.yaml` | Symfony Doctrine |
| `config/services.yaml` | Symfony DI |
| `wp-config.php` | WordPress (DB creds!) |
| `app/Mage.php` | Magento 1 (legacy) |
| `bin/magento` | Magento 2 |
| `sites/default/settings.php` | Drupal |
| `configuration.php` | Joomla |
| `phpunit.xml`, `phpunit.xml.dist` | Tests |
| `phpstan.neon`, `psalm.xml` | Static analysis |

### Database access

- Eloquent (Laravel)
- Doctrine ORM (Symfony / standalone)
- Active Record (CodeIgniter)
- Plain PDO
- `mysqli`
- `pdo_pgsql`, `pdo_mysql`, `pdo_sqlsrv`, `pdo_oci`

### Caching / queue

- Redis (predis / phpredis)
- Memcached
- Laravel Queue (database / Redis / SQS)
- Symfony Messenger
- WordPress object cache (W3 Total Cache, Redis Object Cache plugin)

### Web server

- Apache + mod_php → traditional LAMP
- nginx + PHP-FPM → modern preferred
- Caddy + PHP-FPM → modern
- Built-in PHP server (`php -S`) → dev only

For Azure: PHP-FPM on Linux is standard.

### CMS / e-commerce specifics

#### WordPress
- Theme + plugin inventory (`wp-content/themes/`, `wp-content/plugins/`)
- Active vs inactive plugins (database query for `active_plugins` option)
- Media uploads (`wp-content/uploads/`) — needs Blob Storage / shared volume
- Multisite (`wp-config.php` → `WP_ALLOW_MULTISITE`)
- W3 Total Cache / WP Super Cache → integrate with Azure Cache for Redis

#### Magento
- Composer module inventory
- Customizations under `app/code/`
- Static content (`pub/static/`, `pub/media/`)
- Two-store-front pattern (admin + storefront)
- Heavy: needs Container Apps or AKS plus Azure Cache for Redis + Elasticsearch (→ Azure AI Search or Elastic Cloud)

#### Drupal
- Module inventory (`modules/contrib/`, `modules/custom/`)
- Composer-managed Drupal 9/10+
- Files directory needs Blob Storage

### Tests

- PHPUnit
- Pest
- Behat
- Codeception
- WordPress: WP-CLI tests, Playwright e2e

## Phase 2 Effort Mapping

| Sub-stack | Phase 2 effort | Notes |
|-----------|----------------|-------|
| Laravel 10/11 + PHP 8.2+ | S | Containerize + deploy |
| Laravel 9 / 8 → 10 + PHP 8.2 | M | Breaking changes documented; Carbon 3 migration |
| Symfony 6/7 + PHP 8.2+ | S | Containerize + deploy |
| Symfony 4/5 → 6/7 | M | DI changes; some bundle compat |
| PHP 7.4 → 8.3 | M | Strict types; nullable, attributes; tests crucial |
| PHP 5.x → 8.3 | XL | Often rewrite scope |
| WordPress | M | Plugin compatibility check is the long tail |
| Magento 2 | L | Composer modules, ES migration, perf tuning |
| Plain LAMP | L | Often refactor to a framework as part of Phase 2 |

## Identity Modernization

| Today | Target |
|-------|--------|
| Laravel built-in auth + Eloquent users | Add Laravel Socialite + `laravel/passport` or Entra ID OIDC |
| Symfony Security + UserProvider | Add `KnpUOAuth2ClientBundle` or `BAB` with Entra ID |
| WordPress users | Plugin: `WP OAuth Server` + Entra ID; or SAML SSO |
| Hardcoded users / .htpasswd | Replace with framework auth + Entra ID |

## Target Azure Mapping

| Sub-stack | Primary Azure target | Secondary |
|-----------|----------------------|-----------|
| Laravel / Symfony / CI / Cake / Yii (modern) | App Service Linux PHP | Container Apps |
| WordPress | **App Service for WordPress** (managed offering) | Container Apps with bitnami image |
| Magento 2 | Container Apps + Azure Cache for Redis + Azure AI Search | AKS |
| Drupal / Joomla | App Service Linux PHP | Container Apps |
| Plain LAMP | Container Apps with custom image | App Service Linux PHP |

## Anti-Patterns

- Don't ignore `.env` secrets. Migrate to Key Vault references in App Settings.
- Don't deploy WordPress without configuring Blob Storage for media. App Service local disk is ephemeral.
- Don't preserve `mysql_*` functions (PHP 5 era) — migrate to PDO or mysqli.
- Don't skip Composer dependency audit (`composer audit`) before migration.
- Don't deploy Magento on App Service tier without sizing the SKU — Magento is heavy; needs at least P2v3 or Container Apps with 4 vCPU.
- Don't try to lift OPcache config — Azure App Service has its own PHP image with tuned OPcache.

## Output Checklist

- [ ] Sub-stack identified (one of the 11 above)
- [ ] PHP version captured (target: 8.3)
- [ ] Composer dependencies inventoried
- [ ] Framework version captured
- [ ] DB access library captured (Eloquent / Doctrine / PDO / mysqli)
- [ ] Caching / queue strategy captured
- [ ] Web server captured (Apache mod_php vs PHP-FPM)
- [ ] CMS plugin / module inventory (WordPress / Drupal / Magento)
- [ ] Tests framework captured
- [ ] Static analysis tools captured (PHPStan / Psalm)
- [ ] `.env` secrets flagged for Key Vault migration
- [ ] Phase 2 effort label assigned (S/M/L/XL)
- [ ] Target Azure compute candidate noted
