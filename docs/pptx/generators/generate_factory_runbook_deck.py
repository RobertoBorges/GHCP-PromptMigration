"""
Generate PowerPoint: Accelerate Factory Operations Runbook (Complete)
20 slides covering all 15 runbook sections + appendices
Design: GCS theme from LATAM-MCSA-AccountStatus_0410.pptx template
Speaker notes on every slide.
"""
import os
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

from latam_gcs_template import (
    load_template,
    add_slide,
    set_white_bg,
    add_title_bar,
    add_section_label,
    add_text,
    add_multiline,
    add_card,
    add_footer,
    ACCENT1,
    ACCENT2,
    ACCENT3,
    ACCENT4,
    ACCENT5,
    ACCENT6,
    SLATE,
    GREEN,
    RED,
    WHITE,
    BODY_TEXT,
    LIGHT_BG,
    CARD_BG,
    BORDER_GRAY,
)

# ── Base directory for relative paths ──
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

NAVY = RGBColor(0x1B, 0x2A, 0x4A)

TOTAL_SLIDES = 20

prs = load_template()

def add_colored_card(slide, left, top, width, height, fill_color, border_color=None):
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    shape.fill.solid(); shape.fill.fore_color.rgb = fill_color
    if border_color:
        shape.line.color.rgb = border_color; shape.line.width = Pt(1)
    else:
        shape.line.fill.background()
    shape.shadow.inherit = False; return shape

def add_rect_card(slide, left, top, width, height, fill_color, border_color=None):
    shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, height)
    shape.fill.solid(); shape.fill.fore_color.rgb = fill_color
    if border_color:
        shape.line.color.rgb = border_color; shape.line.width = Pt(1)
    else:
        shape.line.fill.background()
    shape.shadow.inherit = False; return shape

def add_icon_circle(slide, left, top, size, color, text, text_size=14):
    shape = slide.shapes.add_shape(MSO_SHAPE.OVAL, left, top, Inches(size), Inches(size))
    shape.fill.solid(); shape.fill.fore_color.rgb = color
    shape.line.fill.background(); shape.shadow.inherit = False
    tf = shape.text_frame; tf.word_wrap = False; tf.paragraphs[0].alignment = PP_ALIGN.CENTER
    p = tf.paragraphs[0]; p.text = text
    p.font.size = Pt(text_size); p.font.color.rgb = WHITE; p.font.bold = True; p.font.name = "Aptos"

def add_arrow(slide, left, top, width, color=ACCENT2):
    shape = slide.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, left, top, width, Inches(0.25))
    shape.fill.solid(); shape.fill.fore_color.rgb = color
    shape.line.fill.background(); shape.shadow.inherit = False

def add_notes(slide, text):
    slide.notes_slide.notes_text_frame.text = text

# =====================================================================
# SLIDE 1 -- TITLE (LATAM layout 0)
# =====================================================================
s = prs.slides.add_slide(prs.slide_layouts[0])
for sp in list(s.placeholders):
    sp_elem = sp._element; sp_elem.getparent().remove(sp_elem)

add_text(s, Inches(0.8), Inches(1.2), Inches(11), Inches(0.5),
         "Microsoft Accelerated Factory", font_size=18, color=WHITE,
         font_name="Segoe Sans Display Semibold")
add_text(s, Inches(0.8), Inches(2.0), Inches(11), Inches(1.2),
         "Factory Operations Runbook",
         font_size=50, color=WHITE, bold=True, font_name="Aptos Display")
add_text(s, Inches(0.8), Inches(3.5), Inches(11), Inches(0.6),
         "Central Squad + Snap Presets + SubSquads + Skills System",
         font_size=22, color=RGBColor(0xCC, 0xE5, 0xFF), font_name="Aptos Display")
add_text(s, Inches(0.8), Inches(4.5), Inches(9), Inches(0.8),
         "Production-grade operations guide for AI-driven delivery\nacross the Accelerate Factory at enterprise scale",
         font_size=14, color=RGBColor(0xB0, 0xD0, 0xF0))
add_text(s, Inches(0.8), Inches(6.0), Inches(6), Inches(0.7),
         "Audience: Engineers, Architects, Delivery Leads, PMs\nVersion 1.0  |  May 2026  |  Classification: Confidential",
         font_size=11, color=RGBColor(0x90, 0xB8, 0xE0))
add_footer(s, prs, 1, TOTAL_SLIDES)
add_notes(s,
    "This is the complete Factory Operations Runbook. It covers all 15 sections from "
    "executive overview through appendix templates. Follow it step by step for new engagements. "
    "Each slide maps to one or two runbook sections.")

# =====================================================================
# SLIDE 2 -- TABLE OF CONTENTS
# =====================================================================
s = add_slide(prs); set_white_bg(s)
add_title_bar(s, prs, "Runbook Contents — 15 Sections")

toc = [
    ("01", "Executive Overview", ACCENT2),
    ("02", "Operating Model", ACCENT5),
    ("03", "Repo & Artifact Standards", ACCENT6),
    ("04", "Snap Squads (Presets)", GREEN),
    ("05", "Snap Governance + Lifecycle", ACCENT3),
    ("06", "Agent Lifecycle + Governance", ACCENT1),
    ("07", "Skills System", ACCENT2),
    ("08", "Promotion + Escalation", ACCENT5),
    ("09", "Data Sanitization", RED),
    ("10", "Factory Phase Mapping", ACCENT6),
    ("11", "Replace Meetings", GREEN),
    ("12", "Metrics & ROI", ACCENT3),
    ("13", "Anti-Patterns", ACCENT1),
    ("14", "Quick Start + 30-Day Plan", ACCENT4),
    ("15", "Appendix Templates", SLATE),
]

for i, (num, title, color) in enumerate(toc):
    col = i % 3
    row = i // 3
    left = Inches(0.4 + col * 4.2)
    top = Inches(1.1 + row * 1.05)
    add_icon_circle(s, left, top + Inches(0.08), 0.35, color, num, 10)
    add_text(s, left + Inches(0.45), top + Inches(0.05), Inches(3.5), Inches(0.35),
             title, font_size=12, color=color, bold=True)

add_footer(s, prs, 2, TOTAL_SLIDES)
add_notes(s, "15 sections organized into foundational (1-3), operational (4-8), governance (9), "
    "execution (10-11), measurement (12), guardrails (13), and getting started (14-15).")

# =====================================================================
# SLIDE 3 -- EXECUTIVE OVERVIEW (Section 1)
# =====================================================================
s = add_slide(prs); set_white_bg(s)
add_title_bar(s, prs, "01  Executive Overview")

add_text(s, Inches(0.5), Inches(1.0), Inches(12), Inches(0.35),
         "This runbook solves three structural problems that prevent Factory teams from scaling.",
         font_size=13, color=SLATE)

# Three problems
problems = [
    ("Manual Fragmentation", "Teams use portal-driven execution,\nwrite templates from scratch,\nand coordinate through meetings.", ACCENT1),
    ("No Reuse Infrastructure", "Every engagement starts from zero.\nNo shared agents, no skill library,\nno standard team configurations.", ACCENT3),
    ("Knowledge Loss", "When projects end, patterns and\nlessons leave with the team.\nThe next team repeats every mistake.", ACCENT5),
]

for i, (title, desc, color) in enumerate(problems):
    left = Inches(0.4 + i * 4.15)
    add_card(s, left, Inches(1.55), Inches(3.85), Inches(1.8), color)
    add_text(s, left + Inches(0.15), Inches(1.65), Inches(3.55), Inches(0.3),
             title, font_size=14, color=color, bold=True)
    add_multiline(s, left + Inches(0.15), Inches(2.0), Inches(3.55), Inches(1.0),
                  desc.split('\n'), font_size=10, color=BODY_TEXT)

# Target model
add_colored_card(s, Inches(0.5), Inches(3.6), Inches(12), Inches(0.4), NAVY)
add_text(s, Inches(0.8), Inches(3.63), Inches(11.4), Inches(0.3),
         "TARGET:  Central Squad (control plane)  +  Snap Presets (fast teams)  +  SubSquads (execution)  +  Skills (compounding)",
         font_size=11, color=WHITE, bold=True, alignment=PP_ALIGN.CENTER)

# Why it scales
add_section_label(s, Inches(0.5), Inches(4.2), "WHY THIS SCALES", color=GREEN, width=Inches(2.0))

scale_reasons = [
    ("Skills compound", "Every engagement makes agents and templates better for the next team"),
    ("Snaps standardize", "Pre-built team configs eliminate setup time and ensure consistency"),
    ("Governance controls risk", "Central ownership prevents fragmentation, data leaks, and drift"),
]

for i, (title, desc) in enumerate(scale_reasons):
    y = Inches(4.6 + i * 0.5)
    add_text(s, Inches(0.7), y, Inches(2.5), Inches(0.3),
             title, font_size=11, color=GREEN, bold=True)
    add_text(s, Inches(3.3), y, Inches(9.2), Inches(0.3),
             desc, font_size=10, color=BODY_TEXT)

# Non-negotiable principles
add_section_label(s, Inches(0.5), Inches(6.05), "NON-NEGOTIABLE", color=RED, width=Inches(1.8))
add_text(s, Inches(2.5), Inches(6.07), Inches(10), Inches(0.25),
         "Reuse > Rebuild  |  No client data in shared assets  |  Central Squad publishes  |  Human-in-the-loop always",
         font_size=9, color=RED, bold=True)

add_footer(s, prs, 3, TOTAL_SLIDES)
add_notes(s,
    "Three problems: manual fragmentation, no reuse, knowledge loss. "
    "Target model uses four building blocks: Central Squad, Snap Presets, SubSquads, and Skills. "
    "This scales because skills compound, snaps standardize, and governance controls risk.")

# =====================================================================
# SLIDE 4 -- OPERATING MODEL (Section 2)
# =====================================================================
s = add_slide(prs); set_white_bg(s)
add_title_bar(s, prs, "02  Operating Model: Central Squad + SubSquads")

add_text(s, Inches(0.5), Inches(1.0), Inches(12), Inches(0.35),
         "Clear boundary: Central Squad owns standards and shared assets. SubSquads own project execution.",
         font_size=13, color=SLATE)

# Central Squad
add_colored_card(s, Inches(0.4), Inches(1.55), Inches(5.8), Inches(4.2), CARD_BG, ACCENT2)
add_rect_card(s, Inches(0.4), Inches(1.55), Inches(5.8), Inches(0.5), ACCENT2)
add_text(s, Inches(0.55), Inches(1.6), Inches(5.5), Inches(0.4),
         "CENTRAL SQUAD (CONTROL PLANE)", font_size=14, color=WHITE, bold=True)

central_items = [
    "Shared agent library and skill library",
    "Snap preset library (production presets)",
    "Governance gates, versioning, approvals",
    "Standards: naming, artifact structure, quality",
    "Shared memory: decisions, patterns, templates",
    "Metrics and adoption reporting",
    "Certification of reusable assets",
]
for i, item in enumerate(central_items):
    add_text(s, Inches(0.6), Inches(2.2 + i * 0.4), Inches(5.4), Inches(0.3),
             f"  {item}", font_size=10, color=BODY_TEXT)

# SubSquads
add_colored_card(s, Inches(6.8), Inches(1.55), Inches(5.8), Inches(4.2), CARD_BG, ACCENT6)
add_rect_card(s, Inches(6.8), Inches(1.55), Inches(5.8), Inches(0.5), ACCENT6)
add_text(s, Inches(6.95), Inches(1.6), Inches(5.5), Inches(0.4),
         "SUBSQUADS (EXECUTION TEAMS)", font_size=14, color=WHITE, bold=True)

sub_items = [
    "Created per project or workload",
    "Initialize from Snap presets",
    "Execute Factory phases with shared agents",
    "Keep ALL client-specific context local",
    "Contribute improvements via promotion pipeline",
    "Candidate --> Approved --> Standard",
    "Cannot publish directly to Central",
]
for i, item in enumerate(sub_items):
    add_text(s, Inches(7.0), Inches(2.2 + i * 0.4), Inches(5.4), Inches(0.3),
             f"  {item}", font_size=10, color=BODY_TEXT)

# Boundary rule
add_colored_card(s, Inches(0.5), Inches(6.0), Inches(12), Inches(0.35), RGBColor(0xFF, 0xED, 0xED), RED)
add_text(s, Inches(0.8), Inches(6.03), Inches(11.4), Inches(0.3),
         "BOUNDARY: Client-specific = stays in SubSquad.  Reusable = sanitize + propose upward to Central.",
         font_size=10, color=RED, bold=True, alignment=PP_ALIGN.CENTER)

add_footer(s, prs, 4, TOTAL_SLIDES)
add_notes(s,
    "Central Squad owns everything shared. SubSquads own project execution. "
    "The boundary rule is simple: if it contains client data, it stays local. "
    "If it's reusable, sanitize it and propose it upward through the promotion pipeline.")

# =====================================================================
# SLIDE 5 -- REPO + ARTIFACT STANDARDS (Section 3)
# =====================================================================
s = add_slide(prs); set_white_bg(s)
add_title_bar(s, prs, "03  Repo & Artifact Standards")

add_text(s, Inches(0.5), Inches(1.0), Inches(12), Inches(0.35),
         "Every SubSquad repo follows the same structure. Consistency enables reuse.",
         font_size=13, color=SLATE)

# Repo structure
add_section_label(s, Inches(0.5), Inches(1.5), "REQUIRED REPO STRUCTURE", color=ACCENT5, width=Inches(2.8))

files = [
    ("AGENTS.md", "Operating instructions for all agents", ACCENT2),
    ("CLAUDE.md", "Session memory and project context", ACCENT5),
    (".squad/team.md", "Team roster and project metadata", ACCENT6),
    (".squad/routing.md", "Work type to agent mapping", GREEN),
    (".squad/decisions.md", "Active design decisions (shared memory)", ACCENT3),
    (".squad/agents/<name>/charter.md", "Individual agent identity + boundaries", ACCENT1),
    (".squad/skills/", "Reusable skills directory (export/import)", ACCENT2),
    (".squad/presets/", "Snap preset configurations (if applicable)", ACCENT5),
    ("JOURNAL.md", "Build history and engagement milestones", ACCENT6),
]

for i, (f, desc, color) in enumerate(files):
    y = Inches(1.9 + i * 0.35)
    add_text(s, Inches(0.7), y, Inches(4.5), Inches(0.25),
             f, font_size=10, color=color, bold=True)
    add_text(s, Inches(5.5), y, Inches(7.0), Inches(0.25),
             desc, font_size=10, color=BODY_TEXT)

# Naming conventions
add_section_label(s, Inches(0.5), Inches(5.0), "NAMING CONVENTIONS", color=ACCENT2, width=Inches(2.2))

naming = [
    ("Agents:", "agent-<domain>-<capability>  (e.g., agent-iac-bicep)"),
    ("Skills:", "skill-<domain>-<action>-v<N>  (e.g., skill-deploy-containerapp-v2)"),
    ("Snaps:", "snap-<type>-v<N>  (e.g., snap-backend-api-v1)"),
    ("Patterns:", "pattern-<stack>-<component>  (e.g., pattern-dotnet-api-scaffold)"),
]

for i, (label, example) in enumerate(naming):
    y = Inches(5.35 + i * 0.3)
    add_text(s, Inches(0.7), y, Inches(1.0), Inches(0.25),
             label, font_size=10, color=ACCENT2, bold=True)
    add_text(s, Inches(1.8), y, Inches(10.5), Inches(0.25),
             example, font_size=10, color=BODY_TEXT)

add_footer(s, prs, 5, TOTAL_SLIDES)
add_notes(s,
    "Every new SubSquad repo must have these artifacts. This is the minimum viable structure. "
    "Naming conventions are mandatory -- they enable search and discovery across the Central library. "
    "The .squad/skills/ directory is where reusable skills live and get exported from.")

# =====================================================================
# SLIDE 6 -- SNAP SQUADS + GOVERNANCE (Sections 4-5)
# =====================================================================
s = add_slide(prs); set_white_bg(s)
add_title_bar(s, prs, "04-05  Snap Presets: Fast Teams + Governance")

add_text(s, Inches(0.5), Inches(1.0), Inches(12), Inches(0.35),
         "A Snap is a pre-built squad configuration. One initialization creates a full team. Central Squad governs all.",
         font_size=13, color=SLATE)

# Snap contents
add_section_label(s, Inches(0.5), Inches(1.5), "WHAT'S IN A SNAP", color=ACCENT5, width=Inches(2.0))

snap_parts = [
    ("Roles", "Architect, Dev, QA,\nDevRel, GitOps, etc.", ACCENT2),
    ("Agents", "Pre-built charters with\nidentity and boundaries", ACCENT5),
    ("Routing", "Work-type to agent\nmapping rules", ACCENT6),
    ("Memory", "Templates: CLAUDE.md,\ndecisions.md, AGENTS.md", GREEN),
]

for i, (title, desc, color) in enumerate(snap_parts):
    left = Inches(0.4 + i * 3.15)
    add_card(s, left, Inches(1.9), Inches(2.95), Inches(1.3), color)
    add_text(s, left + Inches(0.15), Inches(1.97), Inches(2.65), Inches(0.25),
             title, font_size=12, color=color, bold=True)
    add_multiline(s, left + Inches(0.15), Inches(2.25), Inches(2.65), Inches(0.7),
                  desc.split('\n'), font_size=9, color=BODY_TEXT)

# Lifecycle
add_section_label(s, Inches(0.5), Inches(3.4), "SNAP LIFECYCLE", color=ACCENT3, width=Inches(1.8))

lifecycle = [
    ("Create", ACCENT2), ("Validate", ACCENT5), ("Publish", ACCENT3),
    ("Adopt", GREEN), ("Improve", ACCENT6), ("Version", ACCENT1), ("Retire", SLATE),
]

for i, (stage, color) in enumerate(lifecycle):
    left = Inches(0.3 + i * 1.82)
    add_colored_card(s, left, Inches(3.8), Inches(1.6), Inches(0.45), color)
    add_text(s, left + Inches(0.05), Inches(3.83), Inches(1.5), Inches(0.3),
             stage, font_size=10, color=WHITE, bold=True, alignment=PP_ALIGN.CENTER)
    if i < 6:
        add_arrow(s, left + Inches(1.63), Inches(3.88), Inches(0.12), color)

# Governance rules
add_section_label(s, Inches(0.5), Inches(4.5), "GOVERNANCE RULES", color=RED, width=Inches(2.0))

gov = [
    "Central Squad is the ONLY publisher of production Snap presets",
    "SubSquads may propose improvements but CANNOT publish directly",
    "Every Snap update requires: validation + security review + version bump",
    "Single-owner, single-source-of-truth prevents competing presets",
    "Retirement: zero active SubSquads for 90+ days = eligible for sunset",
]

for i, rule in enumerate(gov):
    add_text(s, Inches(0.7), Inches(4.9 + i * 0.3), Inches(11.8), Inches(0.25),
             f"  {rule}", font_size=9, color=BODY_TEXT)

add_footer(s, prs, 6, TOTAL_SLIDES)
add_notes(s,
    "Snaps are the 'borrowed team' mechanism. One initialization gives you a full squad. "
    "Use official snap-squad preset initialization per the Snap repo documentation. "
    "Governance ensures one source of truth -- no competing or forked presets.")

# =====================================================================
# SLIDE 7 -- AGENT LIFECYCLE + GOVERNANCE (Section 6)
# =====================================================================
s = add_slide(prs); set_white_bg(s)
add_title_bar(s, prs, "06  Agent Lifecycle & Governance")

add_text(s, Inches(0.5), Inches(1.0), Inches(12), Inches(0.35),
         "Every agent is an organizational asset. Structured lifecycle + governance gates ensure safe reuse.",
         font_size=13, color=SLATE)

# Lifecycle
lifecycle = [
    ("CREATE", "Build charter:\nidentity, role,\nexpertise, bounds", ACCENT2),
    ("VALIDATE", "Test isolation:\nzero-context run,\nno client data", ACCENT5),
    ("PUBLISH", "PR to Central:\npeer + architect\napproval", ACCENT3),
    ("SHARE", "Available in\nCentral catalog\nfor all teams", GREEN),
    ("REUSE", "SubSquads pull\nand configure\n(never modify)", ACCENT6),
    ("IMPROVE", "Submit PRs\nwith enhancements\nback to Central", ACCENT1),
]

for i, (stage, desc, color) in enumerate(lifecycle):
    left = Inches(0.3 + i * 2.1)
    add_colored_card(s, left, Inches(1.5), Inches(1.9), Inches(2.3), CARD_BG, color)
    add_icon_circle(s, left + Inches(0.6), Inches(1.6), 0.5, color, str(i+1), 14)
    add_text(s, left + Inches(0.1), Inches(2.25), Inches(1.7), Inches(0.25),
             stage, font_size=11, color=color, bold=True, alignment=PP_ALIGN.CENTER)
    add_multiline(s, left + Inches(0.1), Inches(2.55), Inches(1.7), Inches(1.0),
                  desc.split('\n'), font_size=9, color=BODY_TEXT)
    if i < 5:
        add_arrow(s, left + Inches(1.95), Inches(1.8), Inches(0.1), color)

# Governance gates
add_section_label(s, Inches(0.5), Inches(4.0), "GOVERNANCE GATES (MINIMUM)", color=RED, width=Inches(3.0))

gates = [
    ("Validation gate", "Quality checks: charter completeness, routing rules, documentation"),
    ("Security gate", "No client data, no secrets, no PII, no hardcoded credentials"),
    ("Approval gate", "Central Squad architect sign-off + peer review"),
    ("Version gate", "Changelog entry + migration notes for breaking changes"),
]

for i, (gate, desc) in enumerate(gates):
    y = Inches(4.45 + i * 0.4)
    add_text(s, Inches(0.7), y, Inches(2.0), Inches(0.25),
             gate, font_size=10, color=RED, bold=True)
    add_text(s, Inches(2.8), y, Inches(9.7), Inches(0.25),
             desc, font_size=10, color=BODY_TEXT)

# When to create vs reuse
add_colored_card(s, Inches(0.5), Inches(6.1), Inches(12), Inches(0.3), LIGHT_BG, ACCENT2)
add_text(s, Inches(0.8), Inches(6.12), Inches(11.4), Inches(0.25),
         "RULE: Search existing agents first. Create new only when no agent covers >= 80% of the need AND architect approves.",
         font_size=9, color=ACCENT2, bold=True)

add_footer(s, prs, 7, TOTAL_SLIDES)
add_notes(s,
    "Six lifecycle stages. Four mandatory governance gates. "
    "The 80% rule: if an existing agent covers 80% of your need, reuse it and configure the rest. "
    "Human approval is required at every gate that changes shared assets.")

# =====================================================================
# SLIDE 8 -- SKILLS SYSTEM (Section 7)
# =====================================================================
s = add_slide(prs); set_white_bg(s)
add_title_bar(s, prs, "07  Skills System: Export, Import, Compound")

add_text(s, Inches(0.5), Inches(1.0), Inches(12), Inches(0.35),
         "Skills are reusable execution units. They teach agents how to do repeatable tasks and compound over time.",
         font_size=13, color=SLATE)

# Skill package template
add_section_label(s, Inches(0.5), Inches(1.5), "SKILL PACKAGE TEMPLATE", color=ACCENT5, width=Inches(2.8))

pkg_fields = [
    "Name: skill-<domain>-<action>-v<N>",
    "Version: semantic (1.0.0)",
    "Purpose: what this skill does",
    "Inputs: parameters required",
    "Outputs: what it produces",
    "Usage example (sanitized)",
    "Dependencies (if any)",
    "Maturity: draft | candidate | approved | standard",
]

add_multiline(s, Inches(0.7), Inches(1.9), Inches(5.5), Inches(2.5),
              pkg_fields, font_size=10, color=BODY_TEXT)

# Skill lifecycle
add_section_label(s, Inches(6.5), Inches(1.5), "SKILL PROMOTION LIFECYCLE", color=GREEN, width=Inches(2.8))

skill_levels = [
    ("Local", "SubSquad only.\nNot yet proposed.", ACCENT3),
    ("Candidate", "Proposed to Central.\nUnder review.", ACCENT5),
    ("Approved", "Validated + versioned.\nAvailable in catalog.", GREEN),
    ("Standard", "Default in Snaps.\nWidely adopted.", ACCENT2),
]

for i, (level, desc, color) in enumerate(skill_levels):
    top = Inches(1.9 + i * 0.85)
    add_colored_card(s, Inches(6.5), top, Inches(6.0), Inches(0.7), CARD_BG, color)
    add_text(s, Inches(6.7), top + Inches(0.05), Inches(1.4), Inches(0.25),
             level, font_size=11, color=color, bold=True)
    add_multiline(s, Inches(8.2), top + Inches(0.05), Inches(4.1), Inches(0.55),
                  desc.split('\n'), font_size=9, color=BODY_TEXT)
    if i < 3:
        add_arrow(s, Inches(9.0), top + Inches(0.7), Inches(0.15), color)

# Compounding loop
add_colored_card(s, Inches(0.5), Inches(5.0), Inches(12), Inches(0.9), NAVY)
add_text(s, Inches(0.8), Inches(5.05), Inches(11.4), Inches(0.25),
         "SKILL COMPOUNDING LOOP", font_size=11, color=ACCENT4, bold=True)

loop = ["USE", "IMPROVE", "SHARE", "REUSE", "SCALE"]
lcolors = [ACCENT2, GREEN, ACCENT5, ACCENT3, ACCENT4]
for i, (stage, lc) in enumerate(zip(loop, lcolors)):
    x = Inches(1.0 + i * 2.3)
    add_icon_circle(s, x, Inches(5.4), 0.35, lc, stage, 8)
    if i < 4:
        add_arrow(s, x + Inches(0.45), Inches(5.48), Inches(0.25), lc)

# Rules
add_section_label(s, Inches(0.5), Inches(6.05), "RULES", color=ACCENT2, width=Inches(0.9))
add_text(s, Inches(1.6), Inches(6.07), Inches(11), Inches(0.25),
         "Improve existing skills (don't duplicate)  |  Convert project learnings into generic patterns  |  Central curates top skills into Snaps",
         font_size=9, color=BODY_TEXT)

add_footer(s, prs, 8, TOTAL_SLIDES)
add_notes(s,
    "Skills live in .squad/skills/. They follow a four-level promotion path: "
    "Local, Candidate, Approved, Standard. The compounding loop is the core mechanism: "
    "use, improve, share, reuse, scale. Always improve existing skills rather than creating duplicates.")

# =====================================================================
# SLIDE 9 -- PROMOTION + ESCALATION (Section 8)
# =====================================================================
s = add_slide(prs); set_white_bg(s)
add_title_bar(s, prs, "08  Promotion & Escalation Model")

add_text(s, Inches(0.5), Inches(1.0), Inches(12), Inches(0.35),
         "Improvements must not stay local. Clear promotion levels ensure the best work scales to all teams.",
         font_size=13, color=SLATE)

# Promotion levels
levels = [
    ("L0", "LOCAL", "SubSquad only.\nProject-specific usage.\nNot proposed upward.", ACCENT3),
    ("L1", "CANDIDATE", "Proposed to Central.\nSanitized and documented.\nAwaiting review.", ACCENT5),
    ("L2", "APPROVED", "Validated by Central.\nVersioned and cataloged.\nAvailable to all teams.", GREEN),
    ("L3", "STANDARD", "Embedded in Snap presets.\nDefault for new engagements.\nWidely adopted.", ACCENT2),
]

for i, (level, title, desc, color) in enumerate(levels):
    left = Inches(0.35 + i * 3.15)
    add_colored_card(s, left, Inches(1.55), Inches(2.95), Inches(2.5), CARD_BG, color)
    add_icon_circle(s, left + Inches(1.1), Inches(1.7), 0.55, color, level, 14)
    add_text(s, left + Inches(0.1), Inches(2.4), Inches(2.75), Inches(0.3),
             title, font_size=13, color=color, bold=True, alignment=PP_ALIGN.CENTER)
    add_multiline(s, left + Inches(0.1), Inches(2.75), Inches(2.75), Inches(1.0),
                  desc.split('\n'), font_size=9, color=BODY_TEXT)
    if i < 3:
        add_arrow(s, left + Inches(3.0), Inches(1.8), Inches(0.12), color)

# Escalation model
add_section_label(s, Inches(0.5), Inches(4.3), "ESCALATION MODEL", color=ACCENT1, width=Inches(2.0))

add_text(s, Inches(0.5), Inches(4.7), Inches(12), Inches(0.35),
         "When SubSquads hit repeated friction (manual steps, portal-only actions, missing skills), escalate to Central for system-level fixes.",
         font_size=11, color=SLATE)

esc_items = [
    ("Repeated manual step", "Central creates automation skill or agent improvement"),
    ("Portal-only action", "Central creates IaC pattern to replace portal dependency"),
    ("Missing capability", "Central evaluates: new agent, new skill, or Snap update"),
    ("Cross-team conflict", "Central resolves: update standards, clarify boundaries"),
]

for i, (trigger, resolution) in enumerate(esc_items):
    y = Inches(5.15 + i * 0.35)
    add_text(s, Inches(0.7), y, Inches(3.0), Inches(0.25),
             trigger, font_size=10, color=ACCENT1, bold=True)
    add_text(s, Inches(3.8), y, Inches(8.7), Inches(0.25),
             resolution, font_size=10, color=BODY_TEXT)

add_footer(s, prs, 9, TOTAL_SLIDES)
add_notes(s,
    "Four promotion levels: Local, Candidate, Approved, Standard. "
    "The escalation principle: fix the system, not just the project. "
    "If a SubSquad encounters the same friction twice, it's a system problem for Central to solve.")

# =====================================================================
# SLIDE 10 -- DATA SANITIZATION (Section 9)
# =====================================================================
s = add_slide(prs); set_white_bg(s)
add_title_bar(s, prs, "09  Client Data Sanitization & Certification")

# Critical rule
add_colored_card(s, Inches(0.5), Inches(1.0), Inches(12), Inches(0.5), RGBColor(0xFF, 0xED, 0xED), RED)
add_text(s, Inches(0.8), Inches(1.05), Inches(11.4), Inches(0.4),
         "MANDATORY: All shared assets must pass sanitization before leaving the SubSquad boundary.",
         font_size=12, color=RED, bold=True)

# What must be removed
add_section_label(s, Inches(0.5), Inches(1.7), "MUST REMOVE", color=RED, width=Inches(1.5))

remove_items = [
    "Customer/client names",
    "Tenant IDs, subscription IDs, GUIDs",
    "Endpoints, URLs, email addresses",
    "Resource group names",
    "Secrets, tokens, connection strings",
    "File paths revealing customer identity",
]

for i, item in enumerate(remove_items):
    col = i % 2
    row = i // 2
    left = Inches(0.5 + col * 6.3)
    y = Inches(2.1 + row * 0.32)
    add_text(s, left, y, Inches(5.5), Inches(0.25),
             f"  X  {item}", font_size=10, color=RED)

# Placeholder standard
add_section_label(s, Inches(0.5), Inches(3.15), "REPLACE WITH", color=GREEN, width=Inches(1.5))

placeholders = [
    "<customer-name>", "<tenant-id>", "<subscription-id>",
    "<resource-group>", "<endpoint>", "<secret>",
    "<repo-url>", "<database-name>", "<service-name>", "<environment>",
]

for i, ph in enumerate(placeholders):
    col = i % 5
    row = i // 5
    left = Inches(0.5 + col * 2.5)
    y = Inches(3.55 + row * 0.3)
    add_text(s, left, y, Inches(2.3), Inches(0.25),
             ph, font_size=10, color=GREEN, bold=True)

# Sanitization gate checklist
add_section_label(s, Inches(0.5), Inches(4.3), "SANITIZATION GATE (PASS/FAIL)", color=ACCENT5, width=Inches(3.0))

checks = [
    "No client data present",
    "No secrets or credentials",
    "All inputs parameterized",
    "Examples use safe placeholders",
    "Reusable across projects",
    "Approved by Central Squad",
]

for i, check in enumerate(checks):
    col = i % 2
    row = i // 2
    left = Inches(0.5 + col * 6.3)
    y = Inches(4.7 + row * 0.35)
    add_text(s, left, y, Inches(5.5), Inches(0.25),
             f"  [ ]  {check}", font_size=10, color=BODY_TEXT)

# Separation rule + knowledge access
add_colored_card(s, Inches(0.5), Inches(5.8), Inches(12), Inches(0.55), NAVY)
add_text(s, Inches(0.8), Inches(5.83), Inches(11.4), Inches(0.2),
         "SEPARATION RULE", font_size=9, color=ACCENT4, bold=True)
add_text(s, Inches(0.8), Inches(6.03), Inches(11.4), Inches(0.25),
         "Shared asset = logic only  |  Project config = environment values  |  Validate knowledge source permissions before sharing",
         font_size=10, color=WHITE)

add_footer(s, prs, 10, TOTAL_SLIDES)
add_notes(s,
    "This is the most critical governance slide. Every shared asset must pass the sanitization gate "
    "before leaving the SubSquad. The placeholder standard ensures consistency. "
    "The separation rule is key: shared assets contain logic, project configs contain values. "
    "Also validate that knowledge sources respect access control before sharing broadly.")

# =====================================================================
# SLIDE 11 -- FACTORY PHASE MAPPING (Section 10)
# =====================================================================
s = add_slide(prs); set_white_bg(s)
add_title_bar(s, prs, "10  Factory Phase Mapping: Intake to Handover")

phases = [
    ("INTAKE", [
        "H: Define project scope",
        "A: Generate scope doc",
        "S: Reuse assessment skills",
        "Out: Scope doc, asset map",
        ">> Select Snap preset",
    ], ACCENT2),
    ("DESIGN", [
        "H: Review architecture",
        "A: Produce ADRs, IaC plan",
        "S: Architecture patterns",
        "Out: ADRs, IaC templates",
        ">> Identify reusable patterns",
    ], ACCENT5),
    ("BUILD", [
        "H: Validate decisions",
        "A: Code, test in parallel",
        "S: Test and build skills",
        "Out: Code, test suites",
        ">> Log skill improvements",
    ], ACCENT3),
    ("DEPLOY", [
        "H: Approve deployments",
        "A: IaC deploy (no portal)",
        "S: Deploy automation skills",
        "Out: Deployed infra",
        ">> Escalate portal gaps",
    ], GREEN),
    ("HANDOVER", [
        "H: Sign off delivery",
        "A: Generate docs, runbook",
        "S: Documentation skills",
        "Out: Docs, journal, runbook",
        ">> Promote all improvements",
    ], ACCENT6),
]

add_text(s, Inches(0.5), Inches(0.85), Inches(12), Inches(0.25),
         "H = Human  |  A = Agent  |  S = Skills  |  Out = Artifacts  |  >> = Central Contribution",
         font_size=9, color=SLATE)

for i, (phase, items, color) in enumerate(phases):
    left = Inches(0.3 + i * 2.55)
    top = Inches(1.2)
    add_colored_card(s, left, top, Inches(2.3), Inches(5.0), CARD_BG, color)
    add_rect_card(s, left, top, Inches(2.3), Inches(0.45), color)
    add_text(s, left + Inches(0.1), top + Inches(0.05), Inches(2.1), Inches(0.3),
             phase, font_size=14, color=WHITE, bold=True, alignment=PP_ALIGN.CENTER)
    for j, item in enumerate(items):
        y = top + Inches(0.6 + j * 0.75)
        fc = BODY_TEXT
        if item.startswith(">>"):
            fc = color
        add_text(s, left + Inches(0.1), y, Inches(2.1), Inches(0.6),
                 f"  {item}", font_size=9, color=fc)
    if i < 4:
        add_arrow(s, left + Inches(2.35), top + Inches(0.12), Inches(0.15), color)

add_footer(s, prs, 11, TOTAL_SLIDES)
add_notes(s,
    "Each phase defines human responsibilities, agent responsibilities, skills used, "
    "artifacts produced, and what gets proposed back to Central. "
    "The >> items are the reuse contributions. Every phase produces something Central can use.")

# =====================================================================
# SLIDE 12 -- REPLACE MEETINGS (Section 11)
# =====================================================================
s = add_slide(prs); set_white_bg(s)
add_title_bar(s, prs, "11  Replace Meetings with Agentic Coordination")

add_text(s, Inches(0.5), Inches(1.0), Inches(12), Inches(0.35),
         "Meetings exist because information is trapped in people's heads. Agents surface it automatically.",
         font_size=13, color=SLATE)

# Before/After
add_section_label(s, Inches(0.3), Inches(1.5), "REPLACE", color=RED, width=Inches(1.2))
add_section_label(s, Inches(6.5), Inches(1.5), "WITH", color=GREEN, width=Inches(0.9))

shape = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(6.2), Inches(1.5), Inches(0.03), Inches(3.0))
shape.fill.solid(); shape.fill.fore_color.rgb = BORDER_GRAY; shape.line.fill.background()

replacements = [
    ("Daily standup", "Agent-generated status from git activity + task progress"),
    ("Weekly status report", "Automated summary via Scribe agent (JOURNAL.md)"),
    ("Architecture review", "Architect agent generates ADRs; async PR review"),
    ("Coordination emails", "Routing rules auto-dispatch to right agent"),
    ("Knowledge transfer", "DevRel agent generates onboarding docs"),
]

for i, (before, after) in enumerate(replacements):
    y = Inches(1.9 + i * 0.5)
    add_text(s, Inches(0.5), y, Inches(5.5), Inches(0.4), f"  X  {before}", font_size=10, color=BODY_TEXT)
    add_text(s, Inches(6.7), y, Inches(5.8), Inches(0.4), f"  > {after}", font_size=10, color=BODY_TEXT)

# Templates
add_section_label(s, Inches(0.5), Inches(4.6), "TEMPLATES FOR ASYNC WORK", color=ACCENT5, width=Inches(2.8))

templates = [
    ("Weekly Update", "Status: [on track / at risk / blocked]\nCompleted: [list]\nNext: [list]\nBlockers: [list]", ACCENT2),
    ("Decision Log", "Decision: [what]\nContext: [why]\nAlternatives: [considered]\nOwner: [who]", ACCENT5),
    ("Handover Packet", "Architecture: [ADR links]\nCode: [repo + branch]\nDocs: [generated]\nSkills proposed: [list]", ACCENT6),
]

for i, (title, content, color) in enumerate(templates):
    left = Inches(0.4 + i * 4.15)
    add_card(s, left, Inches(5.0), Inches(3.85), Inches(1.3), color)
    add_text(s, left + Inches(0.15), Inches(5.05), Inches(3.55), Inches(0.25),
             title, font_size=11, color=color, bold=True)
    add_multiline(s, left + Inches(0.15), Inches(5.35), Inches(3.55), Inches(0.9),
                  content.split('\n'), font_size=8, color=BODY_TEXT)

add_footer(s, prs, 12, TOTAL_SLIDES)
add_notes(s,
    "Five meeting types replaced with agent-driven alternatives. "
    "Minimum cadence: weekly checkpoints only when required. Everything else is agent-generated. "
    "Three templates: weekly update, decision log, handover packet. Copy/paste ready.")

# =====================================================================
# SLIDE 13 -- METRICS & ROI (Section 12)
# =====================================================================
s = add_slide(prs); set_white_bg(s)
add_title_bar(s, prs, "12  Metrics, Observability & ROI")

add_text(s, Inches(0.5), Inches(1.0), Inches(12), Inches(0.35),
         "What gets measured gets improved. Central Squad owns reporting. Leadership gets monthly dashboards.",
         font_size=13, color=SLATE)

# KPI categories
kpis = [
    ("Reuse Metrics", [
        "Agent reuse rate (% reused vs created)",
        "Skill reuse rate (imports vs new)",
        "Snap reuse rate (presets adopted)",
    ], ACCENT2),
    ("Efficiency Metrics", [
        "Manual steps eliminated (count)",
        "Meetings reduced (hours/week)",
        "Cycle time per Factory phase",
    ], GREEN),
    ("Quality Metrics", [
        "Test coverage (if tracked)",
        "Defect escape rate (if available)",
        "Governance gate pass rate",
    ], ACCENT5),
    ("Adoption Metrics", [
        "Teams onboarded (count)",
        "Snaps in active use (count)",
        "Skills in Central catalog (count)",
    ], ACCENT6),
]

for i, (category, items, color) in enumerate(kpis):
    left = Inches(0.4 + i * 3.15)
    add_colored_card(s, left, Inches(1.55), Inches(2.95), Inches(2.8), CARD_BG, color)
    add_rect_card(s, left, Inches(1.55), Inches(2.95), Inches(0.45), color)
    add_text(s, left + Inches(0.15), Inches(1.6), Inches(2.65), Inches(0.3),
             category, font_size=12, color=WHITE, bold=True)
    for j, item in enumerate(items):
        y = Inches(2.15 + j * 0.6)
        add_text(s, left + Inches(0.15), y, Inches(2.65), Inches(0.5),
                 f"  {item}", font_size=9, color=BODY_TEXT)

# Reporting cadence
add_section_label(s, Inches(0.5), Inches(4.6), "REPORTING CADENCE", color=ACCENT3, width=Inches(2.0))

cadence = [
    ("Weekly", "Central Squad internal: reuse rates, adoption trends, open PRs"),
    ("Monthly", "Leadership dashboard: efficiency gains, ROI metrics, adoption growth"),
    ("Quarterly", "Strategic review: skill library growth, Snap preset evolution, system-level improvements"),
]

for i, (freq, desc) in enumerate(cadence):
    y = Inches(5.0 + i * 0.4)
    add_text(s, Inches(0.7), y, Inches(1.2), Inches(0.25),
             freq, font_size=10, color=ACCENT3, bold=True)
    add_text(s, Inches(2.0), y, Inches(10.5), Inches(0.25),
             desc, font_size=10, color=BODY_TEXT)

# Ownership
add_colored_card(s, Inches(0.5), Inches(6.15), Inches(12), Inches(0.25), LIGHT_BG, ACCENT2)
add_text(s, Inches(0.8), Inches(6.17), Inches(11.4), Inches(0.2),
         "OWNER: Central Squad is responsible for collecting, analyzing, and reporting all metrics.",
         font_size=9, color=ACCENT2, bold=True)

add_footer(s, prs, 13, TOTAL_SLIDES)
add_notes(s,
    "Four KPI categories: reuse, efficiency, quality, adoption. "
    "Central Squad owns all reporting. Three cadences: weekly internal, monthly leadership, quarterly strategic. "
    "These metrics prove ROI and justify continued investment in the model.")

# =====================================================================
# SLIDE 14 -- ANTI-PATTERNS (Section 13)
# =====================================================================
s = add_slide(prs); set_white_bg(s)
add_title_bar(s, prs, "13  Anti-Patterns: Do Not Do This")

add_text(s, Inches(0.5), Inches(1.0), Inches(12), Inches(0.35),
         "These behaviors kill the operating model. Each one has been observed in real engagements.",
         font_size=13, color=SLATE)

antipatterns = [
    ("Creating agents without searching", "Always check Central catalog first. If >= 80% match exists, reuse it.",
     "Duplicate agents fragment the library and waste effort", ACCENT1),
    ("Embedding client data in shared assets", "Use placeholders. Run sanitization gate. No exceptions.",
     "One leak breaks trust across every team", RED),
    ("Forking Snaps without governance", "Propose improvements through Central. Never fork and maintain separately.",
     "Competing presets = fragmentation = inconsistency", ACCENT3),
    ("Solving the same problem per project", "Escalate to Central for system-level fix. Fix the system, not just the project.",
     "Repeated friction = missing automation in Central", ACCENT5),
    ("Using portal when IaC/automation exists", "Default to IaC-first. Portal is the exception, not the rule.",
     "Portal steps are not repeatable, not auditable, not scalable", ACCENT6),
    ("Hoarding improvements locally", "Submit improvements to Central at engagement end. Don't let them die.",
     "Local improvements die with the project. Shared improvements compound.", GREEN),
    ("Skipping human-in-the-loop", "Agents propose, humans approve. No exceptions for code, infra, or governance.",
     "Unreviewed agent output in production = unacceptable risk", ACCENT1),
]

for i, (title, fix, why, color) in enumerate(antipatterns):
    y = Inches(1.45 + i * 0.72)
    add_text(s, Inches(0.5), y, Inches(0.2), Inches(0.2), "X", font_size=10, color=RED, bold=True)
    add_text(s, Inches(0.8), y, Inches(3.5), Inches(0.25),
             title, font_size=10, color=color, bold=True)
    add_text(s, Inches(4.5), y, Inches(4.2), Inches(0.55),
             fix, font_size=9, color=BODY_TEXT)
    add_text(s, Inches(8.9), y, Inches(3.6), Inches(0.55),
             why, font_size=8, color=SLATE)

add_footer(s, prs, 14, TOTAL_SLIDES)
add_notes(s,
    "Seven anti-patterns that kill the model. Each one includes the behavior to avoid, "
    "the correct alternative, and why it matters. "
    "Review this list during team onboarding and engagement kickoffs.")

# =====================================================================
# SLIDE 15 -- QUICK START DAY 1 (Section 14a)
# =====================================================================
s = add_slide(prs); set_white_bg(s)
add_title_bar(s, prs, "14a  Quick Start: Day 1")

add_text(s, Inches(0.5), Inches(1.0), Inches(12), Inches(0.35),
         "Five steps to go from zero to executing on Day 1 of a new engagement.",
         font_size=13, color=SLATE)

day1 = [
    ("1", "Select Snap Preset", "Assess project requirements. Browse Central catalog.\nMatch workload type to available Snap preset.", ACCENT2),
    ("2", "Initialize SubSquad", "Use official snap-squad initialization per Snap repo docs.\nCreates .squad/ directory with agents, routing, memory.", ACCENT5),
    ("3", "Validate Roster", "Review generated agents and routing rules.\nConfirm all required capabilities are present.\nRequest SNAP capability if gaps exist.", ACCENT6),
    ("4", "Configure Context", "Update CLAUDE.md: project owner, stack, description.\nSet environment variables. DO NOT modify agent charters.", GREEN),
    ("5", "Run First Workflow", "Execute first automated task using the squad.\nCapture first skill improvement candidate.\nLog first decision in decisions.md.", ACCENT3),
]

for i, (num, title, desc, color) in enumerate(day1):
    top = Inches(1.5 + i * 1.0)
    add_card(s, Inches(0.5), top, Inches(12), Inches(0.85), color)
    add_icon_circle(s, Inches(0.7), top + Inches(0.15), 0.45, color, num, 16)
    add_text(s, Inches(1.3), top + Inches(0.05), Inches(2.5), Inches(0.3),
             title, font_size=13, color=color, bold=True)
    add_multiline(s, Inches(4.0), top + Inches(0.05), Inches(8.3), Inches(0.7),
                  desc.split('\n'), font_size=9, color=BODY_TEXT)

add_footer(s, prs, 15, TOTAL_SLIDES)
add_notes(s,
    "Day 1 is about getting the squad running. Five steps, done in order. "
    "The most common mistake is modifying agent charters (Step 4). "
    "Configuration goes in CLAUDE.md and environment variables only. "
    "By end of Day 1, you should have at least one skill improvement candidate identified.")

# =====================================================================
# SLIDE 16 -- FIRST 30 DAYS (Section 14b)
# =====================================================================
s = add_slide(prs); set_white_bg(s)
add_title_bar(s, prs, "14b  First 30 Days Rollout Plan")

add_text(s, Inches(0.5), Inches(1.0), Inches(12), Inches(0.35),
         "From Day 1 to Day 30: build the foundation, prove the model, establish governance.",
         font_size=13, color=SLATE)

weeks = [
    ("WEEK 1", "Foundation", [
        "Day 1: Select Snap, initialize, validate",
        "Day 2-3: Configure, run first workflows",
        "Day 4-5: Identify reusable patterns",
    ], ACCENT2),
    ("WEEK 2", "Execution", [
        "Execute Build phase with shared agents",
        "Log decisions and lessons real-time",
        "Capture skill improvement candidates",
    ], ACCENT5),
    ("WEEK 3", "Contribution", [
        "Submit first skill to Central (candidate)",
        "Establish governance gates on repo",
        "Set up metrics tracking baseline",
    ], ACCENT6),
    ("WEEK 4", "Scaling", [
        "Publish first approved skill/agent",
        "Convert top pain points to skills",
        "Establish metrics dashboard",
    ], GREEN),
]

for i, (week, theme, items, color) in enumerate(weeks):
    left = Inches(0.35 + i * 3.15)
    add_colored_card(s, left, Inches(1.55), Inches(2.95), Inches(3.2), CARD_BG, color)
    add_rect_card(s, left, Inches(1.55), Inches(2.95), Inches(0.6), color)
    add_text(s, left + Inches(0.1), Inches(1.6), Inches(2.75), Inches(0.25),
             week, font_size=13, color=WHITE, bold=True)
    add_text(s, left + Inches(0.1), Inches(1.85), Inches(2.75), Inches(0.22),
             theme, font_size=10, color=RGBColor(0xCC, 0xDD, 0xFF))
    for j, item in enumerate(items):
        y = Inches(2.3 + j * 0.7)
        add_text(s, left + Inches(0.1), y, Inches(2.75), Inches(0.6),
                 f"  {item}", font_size=9, color=BODY_TEXT)

# 30-day success criteria
add_section_label(s, Inches(0.5), Inches(5.0), "30-DAY SUCCESS CRITERIA", color=GREEN, width=Inches(2.5))

criteria = [
    "1-2 Snap presets piloted in real engagements",
    "First approved skills published to Central catalog",
    "Governance gates established and operational",
    "Metrics dashboard live with baseline measurements",
    "Top 3 manual pain points converted to skills/automation",
]

for i, c in enumerate(criteria):
    col = i % 2
    row = i // 2
    left = Inches(0.5 + col * 6.3)
    y = Inches(5.4 + row * 0.3)
    add_text(s, left, y, Inches(6.0), Inches(0.25),
             f"  {c}", font_size=9, color=BODY_TEXT)

add_footer(s, prs, 16, TOTAL_SLIDES)
add_notes(s,
    "Four weeks, each with a clear theme: Foundation, Execution, Contribution, Scaling. "
    "The 30-day success criteria at the bottom are your exit gate. "
    "If you hit all five, the model is operational and ready to scale.")

# =====================================================================
# SLIDE 17 -- APPENDIX: SKILL + SNAP TEMPLATES (Section 15a)
# =====================================================================
s = add_slide(prs); set_white_bg(s)
add_title_bar(s, prs, "15a  Appendix: Skill & Snap Templates")

# Skill package template
add_section_label(s, Inches(0.5), Inches(1.0), "SKILL PACKAGE TEMPLATE", color=ACCENT2, width=Inches(2.5))

skill_tmpl = [
    "Name: skill-<domain>-<action>-v<N>",
    "Version: <major>.<minor>.<patch>",
    "Purpose: <what this skill does>",
    "Inputs: <parameters required>",
    "Outputs: <what it produces>",
    "Usage Example: <sanitized example>",
    "Dependencies: <list or 'none'>",
    "Maturity: draft | candidate | approved | standard",
    "Author: <team name>",
    "Last Updated: <date>",
]

add_multiline(s, Inches(0.7), Inches(1.4), Inches(5.5), Inches(3.0),
              skill_tmpl, font_size=9, color=BODY_TEXT)

# Snap proposal template
add_section_label(s, Inches(6.5), Inches(1.0), "SNAP PROPOSAL TEMPLATE", color=ACCENT5, width=Inches(2.5))

snap_tmpl = [
    "Name: snap-<type>-v<N>",
    "Purpose: <workload this snap targets>",
    "Roles: <list of roles included>",
    "Agents: <list of agent charters>",
    "Routing Rules: <work-type to agent mapping>",
    "Memory Templates: <CLAUDE.md, decisions.md>",
    "Validation: <test project used>",
    "Version: <semantic version>",
    "Author: <team name>",
    "Central Squad Reviewer: <architect name>",
]

add_multiline(s, Inches(6.7), Inches(1.4), Inches(5.5), Inches(3.0),
              snap_tmpl, font_size=9, color=BODY_TEXT)

# Promotion request template
add_section_label(s, Inches(0.5), Inches(4.6), "PROMOTION REQUEST (CANDIDATE --> APPROVED)", color=GREEN, width=Inches(4.0))

promo_tmpl = [
    "Asset Name: <name + version>",
    "Type: agent | skill | snap | pattern",
    "Current Level: local | candidate",
    "Requested Level: candidate | approved | standard",
    "Sanitization: PASS / FAIL (attach checklist)",
    "Test Results: <link or summary>",
    "Documentation: charter / usage examples / changelog",
    "Submitted By: <team>    Reviewed By: <architect>",
]

add_multiline(s, Inches(0.7), Inches(5.0), Inches(12), Inches(1.5),
              promo_tmpl, font_size=9, color=BODY_TEXT)

add_footer(s, prs, 17, TOTAL_SLIDES)
add_notes(s,
    "Three copy/paste templates: Skill Package, Snap Proposal, and Promotion Request. "
    "Teams fill these out when creating new skills, proposing new Snaps, or requesting promotion "
    "from Local to Candidate/Approved/Standard.")

# =====================================================================
# SLIDE 18 -- APPENDIX: CHECKLISTS (Section 15b)
# =====================================================================
s = add_slide(prs); set_white_bg(s)
add_title_bar(s, prs, "15b  Appendix: Operational Checklists")

# Sanitization checklist
add_section_label(s, Inches(0.5), Inches(1.0), "SANITIZATION CHECKLIST", color=RED, width=Inches(2.3))

san_checks = [
    "[ ] No customer/client names present",
    "[ ] No tenant IDs, subscription IDs, or GUIDs",
    "[ ] No secrets, tokens, or connection strings",
    "[ ] No endpoints, URLs, or email addresses",
    "[ ] All inputs use <placeholder> format",
    "[ ] Examples are safe and generic",
    "[ ] Reusable across projects (tested)",
    "[ ] Central Squad architect approved",
]

add_multiline(s, Inches(0.7), Inches(1.4), Inches(5.5), Inches(2.5),
              san_checks, font_size=9, color=BODY_TEXT)

# Central Squad review checklist
add_section_label(s, Inches(6.5), Inches(1.0), "CENTRAL SQUAD REVIEW", color=ACCENT2, width=Inches(2.5))

review_checks = [
    "[ ] Asset follows naming conventions",
    "[ ] Sanitization checklist attached (all PASS)",
    "[ ] Documentation complete (charter, examples)",
    "[ ] Isolation test passed (zero-context run)",
    "[ ] No duplicate in existing catalog",
    "[ ] Version bump applied (semantic)",
    "[ ] Changelog entry present",
    "[ ] Migration notes (if breaking change)",
]

add_multiline(s, Inches(6.7), Inches(1.4), Inches(5.5), Inches(2.5),
              review_checks, font_size=9, color=BODY_TEXT)

# Weekly update template
add_section_label(s, Inches(0.5), Inches(4.0), "WEEKLY UPDATE TEMPLATE", color=ACCENT5, width=Inches(2.3))

weekly = [
    "Status: [ on track | at risk | blocked ]",
    "Completed this week: <list of deliverables>",
    "Planned next week: <list of planned items>",
    "Blockers: <list or 'none'>",
    "Skills proposed to Central: <list or 'none'>",
    "Decisions logged: <count, link to decisions.md>",
]

add_multiline(s, Inches(0.7), Inches(4.4), Inches(5.5), Inches(2.0),
              weekly, font_size=9, color=BODY_TEXT)

# Handover checklist
add_section_label(s, Inches(6.5), Inches(4.0), "HANDOVER CHECKLIST", color=ACCENT6, width=Inches(2.0))

handover = [
    "[ ] Architecture docs generated (ADRs)",
    "[ ] Code and tests in repo (branch merged)",
    "[ ] Runbook auto-generated by DevRel agent",
    "[ ] JOURNAL.md updated with engagement story",
    "[ ] Skills submitted to Central (candidate+)",
    "[ ] Decisions.md current and complete",
]

add_multiline(s, Inches(6.7), Inches(4.4), Inches(5.5), Inches(2.0),
              handover, font_size=9, color=BODY_TEXT)

add_footer(s, prs, 18, TOTAL_SLIDES)
add_notes(s,
    "Four operational checklists: Sanitization, Central Squad Review, Weekly Update, and Handover. "
    "Teams use the Sanitization checklist before proposing any shared asset. "
    "Central Squad uses the Review checklist when evaluating submissions. "
    "Weekly Update and Handover templates replace meetings with structured async artifacts.")

# =====================================================================
# SLIDE 19 -- SUMMARY: THE COMPLETE MODEL
# =====================================================================
s = add_slide(prs); set_white_bg(s)
add_title_bar(s, prs, "The Complete Operating Model")

# Six pillars summary
pillars = [
    ("Central Squad", "Control plane.\nOwns standards,\nagents, skills, snaps.", ACCENT2),
    ("Snap Presets", "Fast teams.\nOne init creates\nfull squad.", ACCENT5),
    ("SubSquads", "Execution engines.\nPull, configure,\nexecute, contribute.", ACCENT6),
    ("Skills System", "Compounding.\nExport, import,\npromote, scale.", GREEN),
    ("Governance", "Trust at scale.\nSanitize, validate,\napprove, version.", ACCENT3),
    ("Metrics", "Prove ROI.\nReuse, efficiency,\nquality, adoption.", ACCENT1),
]

for i, (title, desc, color) in enumerate(pillars):
    left = Inches(0.3 + i * 2.1)
    add_colored_card(s, left, Inches(1.0), Inches(1.9), Inches(2.5), CARD_BG, color)
    add_icon_circle(s, left + Inches(0.6), Inches(1.15), 0.55, color, str(i+1), 16)
    add_text(s, left + Inches(0.1), Inches(1.85), Inches(1.7), Inches(0.25),
             title, font_size=11, color=color, bold=True, alignment=PP_ALIGN.CENTER)
    add_multiline(s, left + Inches(0.1), Inches(2.15), Inches(1.7), Inches(1.0),
                  desc.split('\n'), font_size=9, color=BODY_TEXT)

# Principles bar
add_colored_card(s, Inches(0.5), Inches(3.7), Inches(12), Inches(0.5), NAVY)
add_text(s, Inches(0.8), Inches(3.73), Inches(11.4), Inches(0.4),
         "Reuse > Rebuild  |  No client data in shared assets  |  Central publishes  |  Human-in-the-loop  |  Skills compound",
         font_size=11, color=WHITE, bold=True, alignment=PP_ALIGN.CENTER)

# Key numbers
add_section_label(s, Inches(0.5), Inches(4.4), "TARGET OUTCOMES", color=GREEN, width=Inches(2.0))

outcomes = [
    ("Setup time", "Weeks --> Hours", "Snap presets eliminate team assembly"),
    ("Manual steps", "-60%", "IaC-first, agent-driven automation"),
    ("Meetings", "-60%", "Agent-generated updates replace syncs"),
    ("Agent reuse", ">70%", "Central catalog + mandatory search-first"),
    ("Skill growth", "+10/quarter", "Compounding from every engagement"),
]

for i, (metric, target, how) in enumerate(outcomes):
    y = Inches(4.8 + i * 0.35)
    add_text(s, Inches(0.7), y, Inches(1.8), Inches(0.25),
             metric, font_size=10, color=GREEN, bold=True)
    add_text(s, Inches(2.6), y, Inches(1.5), Inches(0.25),
             target, font_size=10, color=ACCENT2, bold=True)
    add_text(s, Inches(4.2), y, Inches(8.3), Inches(0.25),
             how, font_size=10, color=BODY_TEXT)

add_footer(s, prs, 19, TOTAL_SLIDES)
add_notes(s,
    "The complete model in one slide: six pillars, five principles, five target outcomes. "
    "Use this slide when briefing leadership on the operating model. "
    "The target outcomes are achievable within the first 90 days of adoption.")

# =====================================================================
# SLIDE 20 -- CLOSING (LATAM layout 0)
# =====================================================================
s = prs.slides.add_slide(prs.slide_layouts[0])
for sp in list(s.placeholders):
    sp_elem = sp._element; sp_elem.getparent().remove(sp_elem)

add_text(s, Inches(0.8), Inches(1.0), Inches(11), Inches(0.5),
         "Microsoft Accelerated Factory", font_size=18, color=WHITE,
         font_name="Segoe Sans Display Semibold")
add_text(s, Inches(0.8), Inches(1.8), Inches(11), Inches(0.7),
         "Start Operating the Factory", font_size=44, color=WHITE, bold=True, font_name="Aptos Display")

closing = [
    ("01", "Search First", "Check Central Squad before creating anything new"),
    ("02", "Use Snap Presets", "One command initializes your entire team"),
    ("03", "Configure, Don't Modify", "Project inputs only. Never change shared logic"),
    ("04", "Sanitize Everything", "No client data leaves the SubSquad boundary"),
    ("05", "Contribute Back", "Every improvement benefits every team"),
    ("06", "Compound Skills", "The system gets smarter with every engagement"),
]

for i, (num, title, desc) in enumerate(closing):
    y = Inches(2.7 + i * 0.6)
    add_icon_circle(s, Inches(0.8), y, 0.38, RGBColor(0xCC, 0xE5, 0xFF), num, 11)
    add_text(s, Inches(1.4), y, Inches(10), Inches(0.25),
             title, font_size=16, color=WHITE, bold=True)
    add_text(s, Inches(1.4), y + Inches(0.25), Inches(10), Inches(0.25),
             desc, font_size=11, color=RGBColor(0x90, 0xB8, 0xE0))

add_text(s, Inches(0.8), Inches(6.2), Inches(11), Inches(0.35),
         "Reuse is the default. Creating is the exception. Every engagement makes us smarter.",
         font_size=14, color=RGBColor(0xCC, 0xE5, 0xFF), bold=True)

add_footer(s, prs, 20, TOTAL_SLIDES)
add_notes(s,
    "Six rules for every team. This is the culture shift. "
    "The technology is ready. The agents exist. The presets exist. "
    "The question is: are we ready to stop doing the same work over and over? "
    "Start with Day 1 Quick Start. Hit the 30-day milestones. Let the flywheel spin.")

# =====================================================================
# SAVE
# =====================================================================
OUTPUT = os.path.join(BASE_DIR, "..", "decks", "Factory_Operations_Runbook.pptx")
prs.save(OUTPUT)
print(f"Factory Operations Runbook saved: {OUTPUT}")
print(f"{TOTAL_SLIDES} slides generated with speaker notes")
