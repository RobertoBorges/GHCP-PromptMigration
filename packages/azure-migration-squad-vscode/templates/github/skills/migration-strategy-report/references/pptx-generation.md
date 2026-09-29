# PPTX Generation Skill

Use this skill when creating, extending, or regenerating PowerPoint decks that should follow the agent's shared LATAM GCS presentation pattern.

## Overview

This skill teaches agents how to create professional PowerPoint presentations using the agent's shared LATAM GCS template system.

## Architecture

All PPTX generators follow a shared module pattern:

- **Shared module:** `docs/pptx/generators/latam_gcs_template.py` — colors, helpers, template loading
- **Generators:** `docs/pptx/generators/generate_*.py` — deck-specific slide content
- **Output:** `docs/pptx/decks/*.pptx` — generated presentations

## Guardrails

- Reuse `latam_gcs_template.py` instead of re-implementing colors or helper functions.
- Keep new generators under `docs/pptx/generators/` and outputs under `docs/pptx/decks/`.
- Do not invent helper APIs that are not exported by `latam_gcs_template.py`.
- The current template is loaded from the external path stored in `TEMPLATE_PATH`; verify that dependency before regenerating decks.
- Prefer exact generator names, deck names, and slide counts rather than vague references.

## Quick Start — Creating a New Deck

### Step 1: Create the generator file

```python
"""
Generate <Your Deck Name> PowerPoint
Design: GCS theme from LATAM-MCSA-AccountStatus_0410.pptx template
"""
import os

from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches

from latam_gcs_template import (
    ACCENT1,
    ACCENT2,
    ACCENT3,
    ACCENT4,
    ACCENT5,
    ACCENT6,
    AMBER,
    BODY_TEXT,
    GREEN,
    RED,
    SLATE,
    SUBTITLE,
    WHITE,
    add_accent_line,
    add_card,
    add_circle,
    add_column_card,
    add_footer,
    add_metric_card,
    add_multiline,
    add_section_label,
    add_slide,
    add_speaker_notes,
    add_stat_card,
    add_table,
    add_text,
    add_title_bar,
    load_template,
    set_white_bg,
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_PATH = os.path.join(BASE_DIR, "..", "decks", "Your_Deck_Name.pptx")
TOTAL_SLIDES = 3  # adjust to your deck

prs = load_template()

# ── Slide 1: Title (uses template background) ──
slide = add_slide(prs, 0)  # layout 0 = title slide with blue bg
add_text(
    slide,
    Inches(0.8),
    Inches(2.5),
    Inches(11.5),
    Inches(1.5),
    "Your Deck Title",
    font_size=40,
    color=WHITE,
    bold=True,
    font_name="Aptos Display",
)
add_text(
    slide,
    Inches(0.8),
    Inches(4.0),
    Inches(11.5),
    Inches(0.8),
    "Subtitle text here",
    font_size=20,
    color=WHITE,
)

# ── Slide 2: Content with cards ──
slide = add_slide(prs)  # layout 6 = blank
set_white_bg(slide)
add_title_bar(slide, prs, "Section Title")

# 3-column card layout
for i, (title, lines, color) in enumerate([
    ("Card 1", ["Point A", "Point B"], ACCENT2),
    ("Card 2", ["Point C", "Point D"], ACCENT3),
    ("Card 3", ["Point E", "Point F"], GREEN),
]):
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

add_footer(slide, prs, 2, TOTAL_SLIDES)

# ── Example closing card ──
slide = add_slide(prs)
set_white_bg(slide)
add_title_bar(slide, prs, "Closing")
add_card(
    slide,
    Inches(2.0),
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
add_footer(slide, prs, 3, TOTAL_SLIDES)

# ── Save ──
prs.save(OUTPUT_PATH)
print(f"✅ Saved {TOTAL_SLIDES}-slide deck → {OUTPUT_PATH}")
```

## Shared Module API Reference

### Template & Slide Management

| Function | Parameters | Description |
|----------|-----------|-------------|
| `load_template(path?)` | Optional template path | Load LATAM template, clear slides, return `prs` |
| `add_slide(prs, layout_index=6)` | Presentation, layout index | Add a slide and remove placeholders |
| `set_white_bg(slide)` | Slide | Set white background |
| `set_dark_bg(slide)` | Slide | Set dark navy background |

### Content Elements

| Function | Key Parameters | Description |
|----------|---------------|-------------|
| `add_title_bar(slide, prs, text, font_size=28)` | Slide, prs, text | Blue `ACCENT2` bar at top |
| `add_text(slide, l, t, w, h, text, ...)` | Position, text, formatting | Single text block |
| `add_multiline(slide, l, t, w, h, lines, ...)` | Position, list of strings | Multi-line text with optional bullets |
| `add_section_label(slide, l, t, text, ...)` | Position, text, color | Small colored label badge |

### Card Components

| Function | Key Parameters | Description |
|----------|---------------|-------------|
| `add_card(slide, l, t, w, h, ...)` | Position, size, colors | Rounded rectangle with `adj=6000` corner radius |
| `add_accent_line(slide, l, t, w, color, inside=False)` | Position, color, inside flag | Decorative line; use `inside=True` for cards |
| `add_column_card(slide, l, t, w, h, title, lines, color)` | All-in-one | Card with accent line, title, bullet list |
| `add_metric_card(slide, l, t, w, h, number, label, detail, color)` | All-in-one | Big number + label card |
| `add_stat_card(slide, l, t, w, h, color, title, body, headline?)` | All-in-one | Stat or insight card |

### Utilities

| Function | Parameters | Description |
|----------|-----------|-------------|
| `add_footer(slide, prs, num, total, text="")` | Slide, prs, numbers | Page number + optional footer text |
| `add_table(slide, l, t, w, data, widths, ...)` | Position, data rows | Styled table with header |
| `add_circle(slide, l, t, size, color, text="")` | Position, size, color | Colored circle with optional text |
| `add_speaker_notes(slide, text)` | Slide, notes text | Add speaker notes to slide |

## Color Palette (GCS Theme)

| Constant | Hex | Use |
|----------|-----|-----|
| `ACCENT1` | `#D83B02` | Red-orange highlights, warnings |
| `ACCENT2` | `#0178D4` | Main blue — title bars, primary accent |
| `ACCENT3` | `#FE8B00` | Orange — secondary highlights |
| `ACCENT4` | `#00BCF2` | Light blue — tertiary accent |
| `ACCENT5` | `#463668` | Purple — special categories |
| `ACCENT6` | `#225B62` | Teal — complementary accent |
| `GREEN` | `#00B050` | Success, positive metrics |
| `RED` | `#EE0000` | Critical, negative metrics |
| `AMBER` | `#FFC000` | Warning, caution |
| `SLATE` | `#4A4E66` | Section labels, muted text |

## Design Rules

1. **Fonts:** Aptos Display for titles, Aptos for body text
2. **Title bar:** `ACCENT2` blue, full-width, `0.65"` tall, starts at `y=0.1"`
3. **Cards:** `ROUNDED_RECTANGLE` with `adj=6000` (3.6% corner radius)
4. **Accent lines:** Always use `inside=True` when placed on rounded cards
5. **Title slides:** Use layout `0` (template blue bg) — do not call `set_dark_bg()`
6. **Content slides:** Use layout `6` (blank) + `set_white_bg()`
7. **Slide bounds:** `13.33" × 7.5"`, content within `0.5"–12.7" × 0.9"–6.7"`
8. **Footer:** Always add footer with slide number using `add_footer()`

## Common Slide Patterns

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

## Output Expectations for Prompts

When this skill is applied, the prompt should:

- name the target generator file and output deck explicitly
- reuse `latam_gcs_template.py` instead of duplicating helper logic
- describe the slide narrative, layout patterns, and expected slide count
- mention regeneration steps and the external template dependency when relevant
- keep examples and API usage aligned with the shared helper surface
