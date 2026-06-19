# PPTX Deck Library

All PowerPoint presentations and their Python generators live here.

## Structure

```
docs/pptx/
├── README.md              ← you are here
├── generators/            ← Python scripts that build each deck
│   ├── latam_gcs_template.py          ← shared GCS palette + helpers
│   ├── extract_theme.py               ← extract colors from template
│   ├── generate_oceans_twelve_deck.py ← Ocean's Twelve (17 slides)
│   ├── generate_borges_brady_deck.py  ← Borges+Brady Factory (15 slides)
│   ├── generate_squad_deck_v3.py      ← Squad Factory Proposal
│   ├── generate_factory_runbook_deck.py
│   ├── generate_runbook_deck.py
│   ├── generate_snap_deck.py
│   ├── generate_snap_runbook_deck.py
│   └── generate_sow_deck.py
└── decks/                 ← generated .pptx output files
    ├── Oceans_Twelve_Squad_vs_Prompting.pptx
    ├── Borges_Brady_Squad_Power.pptx
    ├── Copilot_Squad_Factory_Proposal_v3.pptx
    ├── Copilot_Squad_Runbook.pptx
    ├── Copilot_Squad_Runbook_v2.pptx
    ├── Copilot_Squad_Snap_Model.pptx
    ├── Copilot_Squad_Snap_Runbook.pptx
    └── Copilot_Squad_SOW.pptx
```

## Quick Commands

```bash
# Regenerate a specific deck
cd docs/pptx/generators
python generate_oceans_twelve_deck.py
python generate_borges_brady_deck.py

# Or ask the squad
@squad regenerate the Ocean's Twelve PPTX
@squad regenerate the Borges+Brady deck
```

## Setup

### Template File
All generators require the LATAM GCS template PPTX. Set the path:

```bash
# Option 1: Environment variable
export LATAM_TEMPLATE_PATH="/path/to/LATAM-MCSA-AccountStatus_0410.pptx"

# Option 2: Copy .env.example to .env and edit the path
cp .env.example .env
```

If not set, generators will look for the template at the default development path.

> Note: the generators read `LATAM_TEMPLATE_PATH` from the environment. Copying `.env.example` to `.env` is only useful if your shell, editor, or tooling loads `.env` files for you. On PowerShell, you can also run `$env:LATAM_TEMPLATE_PATH = "C:\path\to\LATAM-MCSA-AccountStatus_0410.pptx"` before generating a deck.

## Template

All generators use the **LATAM GCS theme** from:
```
LATAM-MCSA-AccountStatus_0410.pptx
```

Shared colors and helpers are in `generators/latam_gcs_template.py`.

## Design Rules

- **Fonts**: Aptos Display (titles), Aptos (body)
- **Title bar**: ACCENT2 blue, full-width, `Inches(0.65)` tall
- **Cards**: `ROUNDED_RECTANGLE` with `adj=6000` corner radius
- **Accent lines**: Use `inside=True` so lines sit inside card corners
- **Card backgrounds**: WHITE for content cards, template bg for title/closing
- **Slide boundaries**: 13.33" × 7.5", content within 0.5"-12.7" × 0.9"-6.7"

## Creating a New Deck

### Using @squad prompts

```bash
# Create a new deck from scratch
@squad create a 10-slide PPTX about Azure migration ROI with metrics and case studies

# Modify an existing deck
@squad add 2 slides to the Borges+Brady deck showing Q3 results

# Regenerate after content changes
@squad regenerate all PPTX decks

# Create a deck from a prompt topic
@squad create a PPTX proposal for migrating Contoso University to Azure Container Apps
```

For existing decks, reference the generator or deck name explicitly when possible so the squad can target the correct file.

### Manual creation

1. Create `docs/pptx/generators/generate_your_deck.py`
2. Import from `latam_gcs_template` (see skill reference: `#file:.github/skills/pptx-generation.md`)
3. Follow the Quick Start template in the skill
4. Set `LATAM_TEMPLATE_PATH` in your environment (or copy `.env.example` to `.env` and load it in your shell/tooling)
5. Run: `cd docs/pptx/generators && python generate_your_deck.py`
6. Output appears in `docs/pptx/decks/`

### Skill Reference

The full API reference, color palette, and reusable patterns are documented in:

```
.github/skills/pptx-generation.md
```

## Example: Minimal 5-Slide Deck

```python
"""Generate a minimal example deck."""
import os

from pptx.util import Inches

from latam_gcs_template import (
    ACCENT2,
    ACCENT3,
    BODY_TEXT,
    GREEN,
    SUBTITLE,
    WHITE,
    add_column_card,
    add_footer,
    add_slide,
    add_text,
    add_title_bar,
    load_template,
    set_white_bg,
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_PATH = os.path.join(BASE_DIR, "..", "decks", "Example_Deck.pptx")
TOTAL = 5

prs = load_template()

# Slide 1: Title
s = add_slide(prs, 0)
add_text(
    s,
    Inches(0.8),
    Inches(2.5),
    Inches(11.5),
    Inches(1.5),
    "My Deck Title",
    font_size=40,
    color=WHITE,
    bold=True,
    font_name="Aptos Display",
)

# Slide 2: Three columns
s = add_slide(prs)
set_white_bg(s)
add_title_bar(s, prs, "Key Points")
for i, (t, lines, c) in enumerate([
    ("Speed", ["50% faster delivery", "Automated pipelines"], ACCENT2),
    ("Quality", ["Zero-downtime deploys", "Full test coverage"], ACCENT3),
    ("Scale", ["7 apps per quarter", "Repeatable process"], GREEN),
]):
    add_column_card(
        s,
        Inches(0.5 + i * 4.2),
        Inches(1.2),
        Inches(3.8),
        Inches(4.5),
        t,
        lines,
        c,
    )
add_footer(s, prs, 2, TOTAL)

# ... slides 3-5 ...

prs.save(OUTPUT_PATH)
print(f"✅ Saved {TOTAL}-slide deck → {OUTPUT_PATH}")
```

## Common Patterns

### 3-Column Comparison

```python
cols = [
    ("Before", ["Manual", "Slow", "Risky"], ACCENT1),
    ("During", ["Guided", "Automated", "Tracked"], ACCENT2),
    ("After", ["Modern", "Fast", "Secure"], GREEN),
]
for i, (title, lines, color) in enumerate(cols):
    add_column_card(
        slide,
        Inches(0.5 + i * 4.2),
        Inches(1.2),
        Inches(3.8),
        Inches(4.5),
        title,
        lines,
        color,
    )
```

### 4-Metric Dashboard

```python
metrics = [
    ("87%", "Faster", "vs manual migration", ACCENT2),
    ("3x", "More Apps", "per quarter", GREEN),
    ("40%", "Cost Savings", "in Azure spend", ACCENT3),
    ("0", "Downtime", "during cutover", ACCENT5),
]
for i, (num, label, detail, color) in enumerate(metrics):
    add_metric_card(
        slide,
        Inches(0.4 + i * 3.25),
        Inches(1.5),
        Inches(2.9),
        Inches(2.2),
        num,
        label,
        detail,
        color,
    )
```

### Quote/Closing Card

```python
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches

add_card(
    slide,
    Inches(2),
    Inches(2.5),
    Inches(9.3),
    Inches(2.8),
    bg_color=RGBColor(0x00, 0x5A, 0xA0),
    border_color=WHITE,
)
add_text(
    slide,
    Inches(2.5),
    Inches(2.9),
    Inches(8.3),
    Inches(1.5),
    '"The future is already here — it just needs to be deployed."',
    font_size=22,
    color=WHITE,
    font_name="Aptos Display",
    alignment=PP_ALIGN.CENTER,
)
```

## All Available Generators

| Generator | Slides | Description | Command |
|-----------|--------|-------------|---------|
| `generate_oceans_twelve_deck.py` | 17 | Squad vs Prompting comparison | `python generate_oceans_twelve_deck.py` |
| `generate_borges_brady_deck.py` | 15 | Borges+Brady Factory narrative | `python generate_borges_brady_deck.py` |
| `generate_squad_deck_v3.py` | 15 | Factory Delivery Model proposal | `python generate_squad_deck_v3.py` |
| `generate_factory_runbook_deck.py` | — | Factory runbook | `python generate_factory_runbook_deck.py` |
| `generate_runbook_deck.py` | — | Standard runbook | `python generate_runbook_deck.py` |
| `generate_snap_deck.py` | — | SNAP model overview | `python generate_snap_deck.py` |
| `generate_snap_runbook_deck.py` | — | SNAP runbook | `python generate_snap_runbook_deck.py` |
| `generate_sow_deck.py` | 14 | Statement of Work | `python generate_sow_deck.py` |
