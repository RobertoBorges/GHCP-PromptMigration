# HTML Portfolio Report — multi-level site scaffold

A structural reference for the drill-down HTML site the `migration-strategy-report` skill can produce when the user wants **more than a single deck** — a full navigable site with per-customer, per-app, per-domain pages.

## When to use this scaffold

Use this when:

- The portfolio has **multiple customer groups** or **many applications** (10+)
- The customer stakeholders need to click through from a portfolio overview → a customer → an application → a specific AWS/Azure domain view
- The output will be shared with an executive audience who wants to skim + drill down on their own
- The single-deck HTML output from the default `migration-strategy-report` skill is not enough

For a single-app or portfolio-summary-only engagement, the standard deck output from the skill is sufficient.

## Recommended site structure

```
<site-root>/
├── index.html                          # Global landing (all customer groups)
├── overview.html                       # Cross-customer overview + aggregate 6Rs
├── assets/
│   ├── style.css                       # (starter provided — see below)
│   └── app.js                          # Navigation config (author per engagement)
└── <customer-group-slug>/              # One folder per customer group
    ├── index.html                      # Customer group landing
    ├── assessment.html                 # Group-level assessment
    ├── portfolio-deck.html             # Executive deck
    ├── status.html                     # Current progress
    └── <app-slug>/                     # One folder per app
        ├── dashboard.html              # App at-a-glance
        ├── assessment.html             # Per-app assessment
        ├── landing-zone.html           # Target Azure landing zone
        ├── waves.html                  # Migration wave planning
        ├── responsibilities.html       # RACI for this app
        ├── portfolio-deck.html         # App-level exec summary
        └── source-inventory/           # Per-domain source inventory (adapt to source cloud)
            ├── overview.html
            ├── compute.html            # e.g. EC2 / VMs / Container Apps
            ├── containers.html         # e.g. ECS / EKS / AKS
            ├── data-stores.html        # RDS / Cosmos / Blob
            ├── network-edge.html       # VPC / VNet
            ├── observability-devops.html
            ├── security-identity.html
            ├── integration.html        # Messaging / queues / event grid
            ├── regions.html
            └── azure-targets.html      # Overlay: what maps to what in Azure
```

Adjust folder names for the actual source cloud — the pattern is the same for AWS, GCP, on-prem, or hybrid.

## Provided starting assets

Files in `assets/` in this folder:

- **`style.css`** (6 KB) — a starter stylesheet using a Microsoft Fluent-inspired visual language:
  - Primary color: `#0078d4` (Azure Blue)
  - Card layouts, KPI tiles, donut charts (SVG-based), tab panes, section spacing
  - Font stack: Segoe UI / system-ui fallback
  - Ownership badges as inline colored pills (customize the palette for your engagement)

Use this as-is, or theme it for the customer's brand.

## What is NOT provided

- **`app.js` / navigation config** — every engagement has a different customer/app/domain layout. Author your own nav-config from Discovery data.
- **Sample HTML pages** — those would contain either real customer data (NDA violation) or synthetic content that quickly becomes stale. Generate them from the Discovery Dossier + Capability Matrix + assessment reports.
- **A build system** — the pages are static HTML. If you want a build pipeline, use whatever the customer's org uses (Vite, Astro, plain scripting).

## Generating the site

The `migration-strategy-report` skill's default output is a single HTML deck. For a multi-level site, the recommended agent flow is:

1. **`/PortfolioStrategy`** produces the standard single-deck output first
2. Ask the agent for a **multi-level site expansion**: `Convert the portfolio deck into a multi-level HTML site under reports/site/, one page per app per domain, using the scaffold at .github/skills/migration-strategy-report/templates/html-report-scaffold/`
3. The agent will:
   - Read the assessment reports the skill already produced
   - Read this scaffold's style.css
   - Generate per-customer / per-app / per-domain pages populated from the assessment data
   - Write a nav-config `app.js` reflecting the actual customer/app/domain structure

## Customization

Common changes per engagement:

- **Language:** many portfolio decks are internationalized. Add a language toggle in the nav-config or generate per-language folders.
- **Ownership buckets:** the visual palette in `style.css` uses 4 badges (Microsoft, Partner, No-Migration-Needed, Unknown). Rename or add per engagement.
- **Source cloud domain pages:** the domain page inventory (`compute.html`, `containers.html`, etc.) is AWS-specific. Adapt names for on-prem (`vms.html`, `hyperv.html`), GCP (`gce.html`, `gke.html`), or hybrid.

## Provenance

The visual language (CSS + site structure) is adapted from real-world customer engagements. The specific pages and nav-config in this scaffold intentionally contain NO sample customer content — each engagement authors its own from Discovery output.
