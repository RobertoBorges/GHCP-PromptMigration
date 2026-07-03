# Style Guide & Output Standards — Reference

Loaded by the `migration-strategy-report` skill at HTML generation time. Defines the executive presentation deck format: dimensions, colors, typography, components, and absolute output rules.

> **Sources:** `migration-strategy-reports/migration-strategy-report/SKILL.md` (lines 1292–1343, 1036–1041) and `migration-strategy-reports/README.md` (Important Rules + Customization sections).

---

## Output File Requirements

- **Format:** Single, self-contained HTML file — no external CDN dependencies, no separate CSS files, no JavaScript libraries fetched at runtime.
- **Inline CSS only:** All styles must be embedded in a `<style>` block in `<head>`. Never reference an external stylesheet.
- **No external fonts:** Use system font stacks only (see Typography section). Do not load Google Fonts or any web font CDN.
- **Encoding:** UTF-8. Always include `<meta charset="UTF-8">` and `<meta name="viewport" content="width=device-width, initial-scale=1.0">`.
- **Confidentiality footer:** Mark every slide footer with `[ORG NAME] Confidential`.

### File Naming Convention

```
{CustomerName}_Migration_Strategy_Report.html
```

Examples:
- `Contoso_Migration_Strategy_Report.html`
- `Fabrikam_Migration_Strategy_Report.html`

Place the file in the customer's project subfolder (e.g., `Customers/Contoso/`).

---

## CRITICAL: Never Use PowerShell to Write HTML

**NEVER write HTML files using PowerShell heredocs (`@"..."@`).** PowerShell interprets `$` as variable references and **silently strips all dollar signs** from the output — e.g., `$702K/mo` becomes `/mo`, `$1.21M` becomes `.21M`. There is no warning; the file simply has wrong data.

**ALWAYS use one of these safe methods:**

1. **`create_file` tool** *(preferred)* — write HTML content directly via the VS Code/Copilot tool.
2. **Python script** — `open(path, 'w', encoding='utf-8')` with the HTML as a Python string literal.
3. **Python `create_file` function** — use the workspace `create_file` helper.

**Emergency fallback (not recommended for large files):** If PowerShell is unavoidable, use the single-quoted form `@'...'@` (no variable interpolation). Even then, verify dollar signs survived before saving.

The `export_to_pdf.py` script includes a pre-flight check: if it prints `*** No $ signs found but cost patterns detected ***`, the HTML was damaged by PowerShell — regenerate using a safe method above.

---

## Slide Dimensions & Print Settings

| Property | Value |
|---|---|
| Slide width | 1280 px |
| Slide height | 720 px |
| Aspect ratio | 16:9 |
| Print size | A4 / US Letter |
| Page orientation | Landscape |

**Print-friendly rules:**
- Each slide must be a discrete block with `page-break-after: always` (or `break-after: page`) so printing or PDF export produces one slide per page.
- Avoid `position: fixed` or viewport-relative units inside slides — they break PDF rendering.
- Backgrounds and colors must print: use `-webkit-print-color-adjust: exact; print-color-adjust: exact` on slide containers.

---

## Brand Identity

### Primary Brand Colors

| Role | Hex | Usage |
|---|---|---|
| Microsoft Blue (primary) | `#0078d4` | Header bars, primary buttons, KPI card accents, donut chart dominant segment |
| Deep Blue (header gradient end) | `#005a9e` | Gradient partner for header bar (`linear-gradient(135deg, #0078d4, #005a9e)`) |
| White | `#ffffff` | Slide background, card backgrounds, text on dark bars |
| Dark text | `#323130` | Body text, table content |
| Medium grey | `#605e5c` | Secondary text, captions, footnotes |
| Light grey (borders) | `#edebe9` | Table borders, card borders, dividers |
| Light grey (backgrounds) | `#f3f2f1` | Alternating table rows, slide background tint |

### Semantic / Status Colors

| Role | Hex | Usage |
|---|---|---|
| Success / Green | `#107c10` | On-track indicators, ≥80% coverage, positive KPI delta |
| Warning / Orange | `#d83b01` or `#ff8c00` | At-risk indicators, 50–79% coverage, medium risk |
| Critical / Red | `#a80000` | Blocker indicators, <50% coverage, high risk |
| Factory Blue | `#0078d4` | Factory ownership segment in donuts |
| Partner/ISD Amber | `#ff8c00` | ISD / Partner ownership segment |
| Unknown Grey | `#a19f9d` | Unknown / unclassified segment |
| Retire segment | `#d83b01` | Retire strategy in 6 Rs donut |
| Retain segment | `#605e5c` | Retain strategy in 6 Rs donut |

### Customer Brand Override

To apply a customer's brand color, change every instance of `#0078d4` in the generated HTML to the customer's primary color. The gradient pair (`#005a9e`) should be darkened proportionally. Document the override in the report footer or title slide notes.

---

## Typography

### Font Stack

```css
font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, 'Helvetica Neue', Arial, sans-serif;
```

No web fonts. Segoe UI is available on Windows (all modern versions); the stack degrades gracefully to system sans-serif on macOS and Linux.

### Type Scale

| Element | Size | Weight | Color |
|---|---|---|---|
| Slide title (header bar) | 22–24 px | 600 (semibold) | `#ffffff` |
| Section heading (h2) | 18–20 px | 600 | `#323130` |
| KPI card value (big number) | 36–42 px | 700 (bold) | `#0078d4` |
| KPI card label | 11–13 px | 400 | `#605e5c` |
| KPI card sub-label / delta | 11–12 px | 400 | `#605e5c` |
| Table header | 12–13 px | 600 | `#ffffff` (on `#0078d4` background) |
| Table body | 12–13 px | 400 | `#323130` |
| Body / narrative text | 13–14 px | 400 | `#323130` |
| Caption / footnote | 11 px | 400 | `#605e5c` |
| Callout / risk card title | 14–16 px | 600 | inherits or `#ffffff` |
| Callout / risk card body | 12–13 px | 400 | inherits or `#ffffff` |

---

## Component Styles

### KPI Cards

KPI cards sit at the top of data slides in a horizontal row (typically 4 cards in a 1×4 grid, or 6 cards in a 3×2 grid for mixed-pillar overview).

**Layout rules:**
- Cards use `display: flex; flex-direction: column; align-items: center; justify-content: center`.
- Equal width via `flex: 1` in a flex-row container, or a CSS Grid `repeat(4, 1fr)` / `repeat(3, 1fr)` track.
- Minimum height: 100 px; recommended 110–120 px for the 4-card variant.
- Padding: 16–20 px.
- Border radius: 8 px.
- Background: `#ffffff`; box-shadow: `0 2px 8px rgba(0,0,0,0.08)`.
- Top accent bar: 4 px solid `#0078d4` (border-top).

**Content structure (top → bottom):**
1. Big number value (KPI metric) — 36–42 px, bold, `#0078d4`
2. Short label (1–4 words) — 12 px, regular, `#605e5c`
3. Optional: secondary sub-label or delta — 11 px, `#605e5c`

**KPI card variants by slide:**
- Portfolio Overview (Apps): Total Portfolio · In-Scope · DB-Dependent · Mission Critical
- Portfolio Overview (Infra): Total Servers/VMs · Powered-On (Active) · Physical vs Virtual · Total Compute (vCPU + RAM)
- Portfolio Overview (DB): Total DB Instances · Total Databases · Total Data Volume (TB) · Migration-Ready %
- Portfolio Overview (Mixed / 3 pillars): 6 cards in 3×2 — top 2 KPIs per pillar; 2-pillar fallback: 4 cards in 2×2
- EOS/ESU: Total EOS VMs/Servers · ESU-Eligible · No-Mitigation · Supported
- Network: Total VLANs/Subnets · Firewall Rule Count · ExpressRoute/VPN Circuits · Domain Controller Count
- DB Migration: Total DB Instances · Total Databases · Total Data Volume (TB) · Migration-Ready %
- Dependency Mapping: Total Dependency Points · High-Fan-Out Apps · Dependency Hubs · External/Third-Party Dependencies
- Move Groups: Total Move Groups · Largest Group Size · Independent Movers · Cross-Group Dependencies

### Tables

**Header row:**
- Background: `#0078d4`; text: `#ffffff`; font-weight: 600; font-size: 12–13 px.
- Padding: 10–12 px horizontal, 8 px vertical.

**Body rows:**
- Alternating row colors: odd `#ffffff`, even `#f3f2f1`.
- Border: 1 px solid `#edebe9` (bottom border per row, or full border on all cells).
- Padding: 8–10 px horizontal, 6–8 px vertical.
- Font size: 12–13 px; color: `#323130`.

**Responsive behavior:**
- Tables must not overflow the 1280 px slide width. Use `table-layout: fixed` with `word-break: break-word` on cells, or set `overflow-x: auto` on a wrapper `<div>`.
- Column widths: let content drive widths or set explicit `%`-based widths that sum to 100%.

**Status badges in tables:**
- Inline `<span>` chips with 4 px border-radius, 4–6 px padding, colored background matching semantic colors (green / amber / red / grey).

### Callout / Risk Cards

Used on risk slides, decision-required banners, and scope summary callouts.

**Layout:**
- `border-left: 4px solid {accent-color}` (the defining visual cue).
- Background: tinted version of accent (e.g., `rgba(0,120,212,0.06)` for informational blue, `rgba(168,0,0,0.06)` for critical red).
- Padding: 12–16 px.
- Border-radius: 4–6 px.
- Margin: 8–12 px between cards.

**Risk severity accent colors:**
| Severity | Border Color | Background Tint |
|---|---|---|
| Critical / High | `#a80000` | `rgba(168,0,0,0.06)` |
| Medium | `#ff8c00` | `rgba(255,140,0,0.06)` |
| Low / Informational | `#0078d4` | `rgba(0,120,212,0.06)` |

**Content:**
- Title line: bold, 14–16 px, colored to match severity.
- Body: 12–13 px, `#323130`.
- Optional: `[DECISION REQUIRED]` banner as a full-width red strip above the card group.

**Three-tier action cards (EOS slide):**
- Used for ESU options: three equal-width cards side-by-side (`flex: 1`).
- Each card has a colored top border and an icon or emoji prefix.

### Charts (Donuts, Bars)

**Rendering approach: inline SVG** (preferred). Do not use `<canvas>` or any charting library (Chart.js, D3, etc.) — they require external scripts or runtime JavaScript, which breaks offline/print use.

**Donut chart rules:**
- Use SVG `<circle>` elements with `stroke-dasharray` / `stroke-dashoffset` to render segments.
- Center label: show total count (large, bold) and a one-word descriptor below (regular, grey).
- Legend: horizontal or vertical list of `●  Label  Count  (%)` using the semantic color palette.
- Segments order (clockwise from 12 o'clock): Factory (blue) → ISD / Partner (amber) → Unknown (grey) → No Migration Needed (light grey).
- For 6 Rs donuts: Rehost → Replatform → Refactor → Replace → Retire → Retain (order by count descending if no standard preference).

**Bar / horizontal bar chart rules:**
- Use SVG `<rect>` elements with inline `width` set as a percentage of total.
- Always show the count label at the end of each bar.
- Use `#0078d4` for primary bars; use semantic colors for status-coded bars.

**Pie chart alternative:** If segment count > 7, prefer a horizontal bar chart over a donut for readability.

---

## Executive Output Rules (MANDATORY)

These rules apply to every word of generated HTML report content. Violations require regeneration.

- **No internal/meta language** — never use phrases like "New Formula", "Updated Algorithm", "Step-by-Step formula trace", "Pillar Scenario", "Impact Analysis (New Formula)", "algorithm", "formula", "scenario", or "step-by-step trace" anywhere in the output HTML. These are internal implementation terms, not executive language.
- **No algorithm documentation in the report** — classification logic lives in SKILL.md. The report shows only the *result* (counts, criteria summary, verification totals), never the internal execution trace.
- **Never show zero-count platforms** — if no apps use Sybase, Teradata, Informix, etc., do NOT list them with "0 apps". Only show platforms/technologies/categories that actually appear in the data.
- **No zero-count chart segments** — omit legend entries and donut segments for any bucket with count = 0.
- **Executive vocabulary:**
  - Use **"Classification Note"** — not "Disclaimer"
  - Use **"Factory Scope Opportunity"** — not "Impact Analysis"
  - Use **"Recommendation"** — not "Action"
  - Write for a **CIO / leadership audience** — no jargon, no internal tool names, no engineering-level trace output
- **Single source citation** — cite the reference document once (e.g., *"Cloud Accelerate Factory — Service Descriptions, May 2026"*) without explaining version differences or changelogs.
- **Deterministic verification totals** — always show the math: e.g., "Factory 1,200 + ISD / Partner 180 + Unknown 45 = 1,425 ✓". Totals must reconcile.
- **Scope fluidity disclaimer** — on Factory/Partner ownership slides, include a standard note that ISD / Partner workloads can shift to Factory eligibility after OS upgrade, PCI clearance, or cluster decomposition.
- **Every claim traces to an artifact** — each major data point must be attributable to a specific source file listed in the Source Artifacts appendix slide.
- **Gap = finding, not blank** — missing data is surfaced as a leadership finding (e.g., "Discovery workshop needed for 40% of apps with no complexity rating"), never left as an empty cell or omitted section.

---

## Deck-Level Structure Rules

- **Quality over quantity** — 8 evidence-backed slides beats 12 padded ones. Only include slides with sufficient data support.
- **Always include:** Title slide, Key Findings summary, Risks & Dependencies, Recommended Next Steps, Source Artifacts & References appendix.
- **Appendix slide (mandatory, always last):** Lists all input files (D1, D2… for data; R1, R2… for references), dimensions (rows × columns, record count), which slides used each file, and a Data Quality Summary table with coverage % and color-coded indicators (green ≥80%, orange 50–79%, red <50%).
- **Slide header bar:** Full-width, `linear-gradient(135deg, #0078d4, #005a9e)`, white title text, 22–24 px semibold. Optionally includes customer logo area (right-aligned) and slide number.
- **Slide footer:** `[ORG NAME] Confidential` — left-aligned, 11 px, `#605e5c`.
- **Report title adapts to workload type:**
  - Apps only → *"Application Portfolio Migration Strategy"*
  - Infra only → *"Infrastructure Migration Strategy"*
  - DB only → *"Database Migration Strategy"*
  - Mixed (2+ pillars) → *"Enterprise Migration Strategy"*

---

## File Naming Convention

```
{CustomerName}_Migration_Strategy_Report.html
```

Placed in the customer's project folder (e.g., `Customers/{CustomerName}/`). The `Customers/` directory is `.gitignore`d — report files never get committed to the repo.
