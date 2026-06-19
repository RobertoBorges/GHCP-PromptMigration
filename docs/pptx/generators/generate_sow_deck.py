"""
Generate Executive SOW PowerPoint: Centralized Copilot Squad Operating Model
Statement of Work for AI-Driven Delivery in the Microsoft Accelerate Factory
Design: GCS theme from LATAM-MCSA-AccountStatus_0410.pptx template
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
    add_accent_line,
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
    SUBTITLE,
    LIGHT_BG,
    CARD_BG,
    BORDER_GRAY,
)

# ── Base directory for relative paths ──
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

NAVY = RGBColor(0x1B, 0x2A, 0x4A)

TOTAL_SLIDES = 14

prs = load_template()

def add_colored_card(slide, left, top, width, height, fill_color, border_color=None):
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill_color
    if border_color:
        shape.line.color.rgb = border_color
        shape.line.width = Pt(1)
    else:
        shape.line.fill.background()
    shape.shadow.inherit = False
    return shape

def add_icon_circle(slide, left, top, size, color, text, text_size=14):
    shape = slide.shapes.add_shape(MSO_SHAPE.OVAL, left, top, Inches(size), Inches(size))
    shape.fill.solid()
    shape.fill.fore_color.rgb = color
    shape.line.fill.background()
    shape.shadow.inherit = False
    tf = shape.text_frame
    tf.word_wrap = False
    tf.paragraphs[0].alignment = PP_ALIGN.CENTER
    p = tf.paragraphs[0]
    p.text = text
    p.font.size = Pt(text_size)
    p.font.color.rgb = WHITE
    p.font.bold = True
    p.font.name = "Aptos"

def add_arrow(slide, left, top, width, color=ACCENT2):
    shape = slide.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, left, top, width, Inches(0.3))
    shape.fill.solid()
    shape.fill.fore_color.rgb = color
    shape.line.fill.background()
    shape.shadow.inherit = False

# ═══════════════════════════════════════════════════════════════
# SLIDE 1 — TITLE SLIDE (LATAM template layout 0 — blue gradient)
# ═══════════════════════════════════════════════════════════════
s = prs.slides.add_slide(prs.slide_layouts[0])
for sp in list(s.placeholders):
    sp_elem = sp._element
    sp_elem.getparent().remove(sp_elem)

add_text(s, Inches(0.8), Inches(1.2), Inches(11), Inches(0.5),
         "Microsoft Accelerated Factory", font_size=18, color=WHITE,
         font_name="Segoe Sans Display Semibold")

# Main title
add_text(s, Inches(0.8), Inches(2.2), Inches(11), Inches(1.0),
         "Statement of Work", font_size=54, color=WHITE, bold=True, font_name="Aptos Display")

add_text(s, Inches(0.8), Inches(3.5), Inches(11), Inches(0.6),
         "Centralized Copilot Squad Operating Model",
         font_size=26, color=RGBColor(0xCC, 0xE5, 0xFF), font_name="Aptos Display")

add_text(s, Inches(0.8), Inches(4.5), Inches(9), Inches(0.8),
         "AI-Driven Delivery at Scale with Central Squad + SubSquads",
         font_size=15, color=RGBColor(0xB0, 0xD0, 0xF0))

# Bottom details
add_text(s, Inches(0.8), Inches(6.0), Inches(6), Inches(0.7),
         "Prepared for: Accelerate Factory Leadership\nVersion 1.0  |  May 2026  |  Classification: Confidential",
         font_size=11, color=RGBColor(0x90, 0xB8, 0xE0))

add_footer(s, prs, 1, TOTAL_SLIDES)

# ═══════════════════════════════════════════════════════════════
# SLIDE 2 — EXECUTIVE SUMMARY
# ═══════════════════════════════════════════════════════════════
s = add_slide(prs)
set_white_bg(s)
add_title_bar(s, prs, "1. Executive Summary")

add_text(s, Inches(0.5), Inches(1.1), Inches(12), Inches(0.5),
         "Transforming Accelerate Factory delivery through AI-driven orchestration",
         font_size=16, color=SLATE, bold=True)

# Key message card
add_colored_card(s, Inches(0.5), Inches(1.7), Inches(12), Inches(1.2), LIGHT_BG, ACCENT2)
add_multiline(s, Inches(0.8), Inches(1.8), Inches(11.4), Inches(1.0), [
    "This Statement of Work defines the implementation of a Centralized Copilot Squad model that",
    "replaces manual, portal-driven execution with AI-orchestrated delivery. By establishing a Central",
    "Squad as the intelligence layer and SubSquads as project execution teams, the Factory achieves",
    "reusable automation, consistent governance, and scalable delivery across all engagements."
], font_size=13, color=BODY_TEXT)

# Three value pillars
y = Inches(3.2)
pillars = [
    ("⚡", "Speed", "Reduce delivery cycles\nthrough AI automation\nand agent reuse", ACCENT2),
    ("📐", "Scale", "SubSquads replicate proven\npatterns without rebuilding\nfrom scratch", ACCENT5),
    ("🔒", "Consistency", "Centralized governance\nensures quality and security\nacross all engagements", ACCENT6),
]
for i, (icon, title, desc, color) in enumerate(pillars):
    left = Inches(0.5 + i * 4.1)
    add_colored_card(s, left, y, Inches(3.8), Inches(2.4), CARD_BG, color)
    add_accent_line(s, left, y, Inches(3.8), color, inside=True)
    add_text(s, left + Inches(0.2), y + Inches(0.3), Inches(3.4), Inches(0.4),
             f"{icon}  {title}", font_size=20, color=color, bold=True)
    add_multiline(s, left + Inches(0.2), y + Inches(0.75), Inches(3.4), Inches(1.5),
                  desc.split('\n'), font_size=12, color=BODY_TEXT)

# Bottom stat bar
add_colored_card(s, Inches(0.5), Inches(5.9), Inches(12), Inches(0.7), NAVY)
stats = [
    ("60%+", "Reduction in manual effort"),
    ("3x", "Faster delivery cycles"),
    ("100%", "Agent reusability target"),
    ("Zero", "Client data exposure"),
]
for i, (val, label) in enumerate(stats):
    x = Inches(0.8 + i * 3.05)
    add_text(s, x, Inches(5.95), Inches(1.2), Inches(0.35), val,
             font_size=20, color=ACCENT4, bold=True)
    add_text(s, x + Inches(1.25), Inches(6.0), Inches(1.7), Inches(0.35), label,
             font_size=10, color=WHITE)

add_footer(s, prs, 2, TOTAL_SLIDES)

# ═══════════════════════════════════════════════════════════════
# SLIDE 3 — OBJECTIVES
# ═══════════════════════════════════════════════════════════════
s = add_slide(prs)
set_white_bg(s)
add_title_bar(s, prs, "2. Objectives")

objectives = [
    ("01", "Eliminate Manual Overhead", "Replace portal-driven, manual execution with AI-orchestrated workflows. Agents handle infrastructure, testing, documentation, and deployment automatically.", ACCENT2),
    ("02", "Enable Reusable Agents", "Build once, use everywhere. Agents are generic, template-based enterprise assets — not tied to any single project or client.", ACCENT5),
    ("03", "Scale with Central + SubSquads", "The Central Squad maintains shared intelligence; SubSquads spin up per project, pulling proven agents and patterns from the central library.", ACCENT6),
    ("04", "Drive Cross-Team Collaboration", "Improvements from any SubSquad feed back to the Central Squad. Every engagement makes the entire system smarter.", ACCENT1),
]

for i, (num, title, desc, color) in enumerate(objectives):
    y = Inches(1.1 + i * 1.42)
    add_card(s, Inches(0.5), y, Inches(12), Inches(1.25), color)
    add_accent_line(s, Inches(0.5), y + Inches(0.15), Inches(0.06), color)

    # Number circle
    add_icon_circle(s, Inches(0.75), y + Inches(0.18), 0.55, color, num, 16)

    add_text(s, Inches(1.55), y + Inches(0.15), Inches(10.5), Inches(0.35),
             title, font_size=17, color=color, bold=True)
    add_text(s, Inches(1.55), y + Inches(0.55), Inches(10.5), Inches(0.6),
             desc, font_size=12, color=BODY_TEXT)

add_footer(s, prs, 3, TOTAL_SLIDES)

# ═══════════════════════════════════════════════════════════════
# SLIDE 4 — SCOPE
# ═══════════════════════════════════════════════════════════════
s = add_slide(prs)
set_white_bg(s)
add_title_bar(s, prs, "3. Scope of Work")

# In Scope
add_section_label(s, Inches(0.5), Inches(1.1), "IN SCOPE", color=GREEN)
in_scope = [
    ("🤖", "Agent Creation & Sharing", "Design, build, validate, and publish reusable agents to the Central Squad library"),
    ("🏗️", "Squad-Based Orchestration", "Central Squad coordinates delivery; SubSquads execute using shared agents and skills"),
    ("☁️", "IaC-First Delivery", "All infrastructure defined as code — Bicep, Terraform, azd — no portal clicking"),
    ("📈", "SubSquad Scaling", "Spin up project-specific SubSquads that inherit Central Squad capabilities"),
    ("🔄", "Continuous Improvement", "SubSquads contribute improvements, patterns, and new agents back to Central"),
]

for i, (icon, title, desc) in enumerate(in_scope):
    y = Inches(1.6 + i * 0.72)
    add_text(s, Inches(0.7), y, Inches(0.4), Inches(0.3), icon, font_size=16)
    add_text(s, Inches(1.1), y, Inches(3.5), Inches(0.3), title, font_size=13, color=ACCENT2, bold=True)
    add_text(s, Inches(1.1), y + Inches(0.28), Inches(5.5), Inches(0.35), desc, font_size=11, color=BODY_TEXT)

# Out of Scope
add_section_label(s, Inches(7.2), Inches(1.1), "OUT OF SCOPE", color=RED)
out_scope = [
    "Client-specific business logic",
    "Custom agent training on proprietary data",
    "Third-party tool licensing / procurement",
    "Production operational support (BAU)",
    "Client data migration or ETL",
]

for i, item in enumerate(out_scope):
    y = Inches(1.65 + i * 0.55)
    add_text(s, Inches(7.4), y, Inches(0.3), Inches(0.25), "✕", font_size=13, color=RED, bold=True)
    add_text(s, Inches(7.8), y, Inches(4.5), Inches(0.4), item, font_size=12, color=BODY_TEXT)

# Deliverables box
add_colored_card(s, Inches(7.2), Inches(4.6), Inches(5.3), Inches(2.0), LIGHT_BG, ACCENT2)
add_section_label(s, Inches(7.2), Inches(4.6), "KEY DELIVERABLES", color=ACCENT2)
deliverables = [
    "Central Squad agent library (versioned)",
    "SubSquad deployment templates",
    "Governance & security framework",
    "Agent lifecycle documentation",
    "Success metrics dashboard",
]
for i, d in enumerate(deliverables):
    y = Inches(5.05 + i * 0.3)
    add_text(s, Inches(7.5), y, Inches(0.3), Inches(0.25), "✓", font_size=12, color=GREEN, bold=True)
    add_text(s, Inches(7.85), y, Inches(4.4), Inches(0.25), d, font_size=11, color=BODY_TEXT)

add_footer(s, prs, 4, TOTAL_SLIDES)

# ═══════════════════════════════════════════════════════════════
# SLIDE 5 — DELIVERY MODEL: CENTRAL SQUAD (THE BRAIN)
# ═══════════════════════════════════════════════════════════════
s = add_slide(prs)
set_white_bg(s)
add_title_bar(s, prs, "4a. Delivery Model — Central Squad (The Brain)")

add_text(s, Inches(0.5), Inches(1.1), Inches(12), Inches(0.4),
         "The Central Squad is the intelligence layer: shared agents, standards, governance, and institutional memory.",
         font_size=14, color=SLATE, bold=False)

# Core responsibilities
responsibilities = [
    ("🧠", "Shared Memory", "Maintains decisions, patterns, templates,\nand institutional knowledge across all projects", ACCENT2),
    ("📦", "Agent Library", "Owns reusable, anonymized agents.\nPrevents duplication across teams", ACCENT5),
    ("🛡️", "Governance", "Enforces security rules, approval gates,\nversion control, and auditability", ACCENT1),
    ("🔧", "Standards", "Defines coding patterns, IaC templates,\ntesting frameworks, and delivery playbooks", ACCENT6),
    ("📊", "Continuous Improvement", "Aggregates learnings from SubSquads.\nEvery engagement makes the system smarter", ACCENT3),
]

for i, (icon, title, desc, color) in enumerate(responsibilities):
    col = i % 3
    row = i // 3
    left = Inches(0.5 + col * 4.1)
    top = Inches(1.75 + row * 2.5)

    add_colored_card(s, left, top, Inches(3.8), Inches(2.1), CARD_BG, color)
    add_accent_line(s, left, top, Inches(3.8), color, inside=True)
    add_text(s, left + Inches(0.2), top + Inches(0.3), Inches(3.4), Inches(0.4),
             f"{icon}  {title}", font_size=16, color=color, bold=True)
    add_multiline(s, left + Inches(0.2), top + Inches(0.75), Inches(3.4), Inches(1.2),
                  desc.split('\n'), font_size=12, color=BODY_TEXT)

# Key principle banner
add_colored_card(s, Inches(0.5), Inches(6.1), Inches(12), Inches(0.6), NAVY)
add_text(s, Inches(0.8), Inches(6.15), Inches(11.4), Inches(0.5),
         "🔑  Core Principle: Agents are enterprise assets — reusable, anonymized, never containing client data",
         font_size=13, color=WHITE, bold=True)

add_footer(s, prs, 5, TOTAL_SLIDES)

# ═══════════════════════════════════════════════════════════════
# SLIDE 6 — DELIVERY MODEL: SUBSQUADS (EXECUTION TEAMS)
# ═══════════════════════════════════════════════════════════════
s = add_slide(prs)
set_white_bg(s)
add_title_bar(s, prs, "4b. Delivery Model — SubSquads (Execution Teams)")

add_text(s, Inches(0.5), Inches(1.1), Inches(12), Inches(0.4),
         "SubSquads are project-specific execution teams that pull from the Central Squad and contribute back.",
         font_size=14, color=SLATE)

# Flow: Central → SubSquad → Delivery
# Central Squad box
add_colored_card(s, Inches(0.5), Inches(1.8), Inches(3.2), Inches(3.5), LIGHT_BG, ACCENT2)
add_section_label(s, Inches(0.5), Inches(1.8), "CENTRAL SQUAD", color=ACCENT2, width=Inches(3.2))
central_items = [
    "Shared Agent Library",
    "Approved Patterns",
    "IaC Templates",
    "Governance Rules",
    "Decision History",
]
for i, item in enumerate(central_items):
    y = Inches(2.35 + i * 0.45)
    add_text(s, Inches(0.8), y, Inches(0.2), Inches(0.25), "→", font_size=13, color=ACCENT2, bold=True)
    add_text(s, Inches(1.1), y, Inches(2.4), Inches(0.3), item, font_size=12, color=BODY_TEXT)

# Arrow
add_arrow(s, Inches(3.9), Inches(3.3), Inches(0.7), ACCENT2)

# SubSquad boxes
subsquads = [
    ("SubSquad A", "Project Alpha", ["Pull agents from Central", "Execute delivery phases", "Report improvements back"]),
    ("SubSquad B", "Project Beta", ["Inherit shared skills", "Apply IaC templates", "Contribute new patterns"]),
]
for i, (name, project, items) in enumerate(subsquads):
    left = Inches(4.9)
    top = Inches(1.8 + i * 1.9)
    add_colored_card(s, left, top, Inches(3.6), Inches(1.7), CARD_BG, ACCENT5)
    add_text(s, left + Inches(0.15), top + Inches(0.1), Inches(3.3), Inches(0.3),
             f"{name}  •  {project}", font_size=13, color=ACCENT5, bold=True)
    for j, item in enumerate(items):
        add_text(s, left + Inches(0.15), top + Inches(0.45 + j * 0.35), Inches(3.3), Inches(0.3),
                 f"  ▸ {item}", font_size=11, color=BODY_TEXT)

# Arrow to Factory Phases
add_arrow(s, Inches(8.75), Inches(3.3), Inches(0.7), ACCENT5)

# Factory Phases
add_colored_card(s, Inches(9.7), Inches(1.8), Inches(2.8), Inches(3.5), CARD_BG, ACCENT6)
add_section_label(s, Inches(9.7), Inches(1.8), "FACTORY PHASES", color=ACCENT6, width=Inches(2.8))
phases = ["Intake", "Design", "Build", "Deploy", "Handover"]
phase_colors = [ACCENT2, ACCENT5, ACCENT3, GREEN, ACCENT6]
for i, (phase, pc) in enumerate(zip(phases, phase_colors)):
    y = Inches(2.35 + i * 0.55)
    add_icon_circle(s, Inches(9.95), y, 0.35, pc, str(i+1), 11)
    add_text(s, Inches(10.45), y + Inches(0.03), Inches(1.8), Inches(0.3),
             phase, font_size=13, color=BODY_TEXT, bold=True)

# Feedback loop
add_colored_card(s, Inches(0.5), Inches(5.7), Inches(12), Inches(0.9), LIGHT_BG, GREEN)
add_text(s, Inches(0.8), Inches(5.8), Inches(11.4), Inches(0.3),
         "🔄  Continuous Feedback Loop", font_size=14, color=GREEN, bold=True)
add_text(s, Inches(0.8), Inches(6.15), Inches(11.4), Inches(0.35),
         "SubSquads execute → Surface improvements → Central Squad validates & publishes → All SubSquads benefit",
         font_size=12, color=BODY_TEXT)

add_footer(s, prs, 6, TOTAL_SLIDES)

# ═══════════════════════════════════════════════════════════════
# SLIDE 7 — FACTORY ALIGNMENT
# ═══════════════════════════════════════════════════════════════
s = add_slide(prs)
set_white_bg(s)
add_title_bar(s, prs, "5. Accelerate Factory Phase Alignment")

add_text(s, Inches(0.5), Inches(1.1), Inches(12), Inches(0.4),
         "How the Copilot Squad model maps to each Factory delivery phase",
         font_size=14, color=SLATE)

phases_detail = [
    ("INTAKE", "Requirements gathering,\nscope definition,\nagent identification", "Architect + Researcher", ACCENT2),
    ("DESIGN", "Architecture decisions,\nagent selection,\nIaC planning", "Architect + Prompter", ACCENT5),
    ("BUILD", "Implementation,\nagent orchestration,\nautomated testing", "Coder + Tester", ACCENT3),
    ("DEPLOY", "IaC deployment,\nCI/CD pipelines,\nvalidation gates", "GitOps + Evaluator", GREEN),
    ("HANDOVER", "Documentation,\nknowledge transfer,\nagent contribution", "DevRel + Scribe", ACCENT6),
]

for i, (phase, activities, agents, color) in enumerate(phases_detail):
    left = Inches(0.3 + i * 2.55)
    # Phase card
    add_colored_card(s, left, Inches(1.7), Inches(2.3), Inches(4.5), CARD_BG, color)
    # Phase header
    add_colored_card(s, left, Inches(1.7), Inches(2.3), Inches(0.55), color)
    add_text(s, left + Inches(0.1), Inches(1.75), Inches(2.1), Inches(0.45),
             phase, font_size=16, color=WHITE, bold=True, alignment=PP_ALIGN.CENTER)

    # Activities
    add_section_label(s, left + Inches(0.1), Inches(2.45), "Activities", color=SLATE, width=Inches(1.2))
    add_multiline(s, left + Inches(0.15), Inches(2.85), Inches(2.0), Inches(1.5),
                  activities.split('\n'), font_size=11, color=BODY_TEXT)

    # Agents
    add_section_label(s, left + Inches(0.1), Inches(4.2), "Squad Agents", color=SLATE, width=Inches(1.4))
    add_text(s, left + Inches(0.15), Inches(4.6), Inches(2.0), Inches(0.6),
             agents, font_size=11, color=color, bold=True)

    # Arrow between phases
    if i < 4:
        add_arrow(s, left + Inches(2.35), Inches(1.9), Inches(0.18), color)

add_footer(s, prs, 7, TOTAL_SLIDES)

# ═══════════════════════════════════════════════════════════════
# SLIDE 8 — AGENT LIFECYCLE
# ═══════════════════════════════════════════════════════════════
s = add_slide(prs)
set_white_bg(s)
add_title_bar(s, prs, "6. Agent Lifecycle")

add_text(s, Inches(0.5), Inches(1.1), Inches(12), Inches(0.4),
         "Every agent follows a structured lifecycle from creation to continuous improvement",
         font_size=14, color=SLATE)

lifecycle_stages = [
    ("CREATE", "Design agent\ncharter, identity,\nand capabilities", "🛠️", ACCENT2),
    ("VALIDATE", "Test against\nquality gates\nand edge cases", "✅", GREEN),
    ("PUBLISH", "Register in\nCentral Squad\nagent library", "📦", ACCENT5),
    ("SHARE", "Make available\nto all SubSquads\nvia catalog", "🔗", ACCENT4),
    ("REUSE", "SubSquads pull\nagents for project\nexecution", "♻️", ACCENT3),
    ("IMPROVE", "Collect feedback,\nmerge improvements\nfrom SubSquads", "📈", ACCENT6),
    ("VERSION", "Publish updated\nversion with\nchangelog", "🏷️", ACCENT1),
]

for i, (stage, desc, icon, color) in enumerate(lifecycle_stages):
    left = Inches(0.3 + i * 1.78)
    top = Inches(1.8)

    # Icon circle
    add_icon_circle(s, left + Inches(0.45), top, 0.65, color, icon, 20)

    # Stage name
    add_text(s, left, top + Inches(0.8), Inches(1.6), Inches(0.3),
             stage, font_size=13, color=color, bold=True, alignment=PP_ALIGN.CENTER)

    # Description
    add_multiline(s, left, top + Inches(1.15), Inches(1.6), Inches(1.2),
                  desc.split('\n'), font_size=10, color=BODY_TEXT)

    # Arrow
    if i < 6:
        add_text(s, left + Inches(1.5), top + Inches(0.15), Inches(0.3), Inches(0.4),
                 "→", font_size=20, color=SUBTITLE, bold=True)

# Circular arrow back indicator
add_colored_card(s, Inches(0.5), Inches(4.6), Inches(12), Inches(0.5), LIGHT_BG, ACCENT2)
add_text(s, Inches(0.8), Inches(4.65), Inches(11.4), Inches(0.4),
         "🔄  Lifecycle is circular: Version → triggers new Create cycle with accumulated improvements",
         font_size=12, color=ACCENT2, bold=True)

# Governance gates
add_section_label(s, Inches(0.5), Inches(5.4), "GOVERNANCE GATES", color=ACCENT1)
gates = [
    ("Validation Gate", "Automated tests + peer review before publishing"),
    ("Security Gate", "No client data, anonymized patterns, template-based only"),
    ("Approval Gate", "Architect sign-off required for Central Squad inclusion"),
    ("Version Gate", "Semantic versioning with changelog and migration notes"),
]
for i, (gate, desc) in enumerate(gates):
    col = i % 2
    row = i // 2
    left = Inches(0.5 + col * 6.2)
    top = Inches(5.85 + row * 0.5)
    add_text(s, left, top, Inches(0.2), Inches(0.25), "🔒", font_size=11)
    add_text(s, left + Inches(0.3), top, Inches(1.8), Inches(0.25), gate, font_size=11, color=ACCENT1, bold=True)
    add_text(s, left + Inches(2.2), top, Inches(3.8), Inches(0.25), desc, font_size=10, color=BODY_TEXT)

add_footer(s, prs, 8, TOTAL_SLIDES)

# ═══════════════════════════════════════════════════════════════
# SLIDE 9 — GOVERNANCE & SECURITY
# ═══════════════════════════════════════════════════════════════
s = add_slide(prs)
set_white_bg(s)
add_title_bar(s, prs, "7. Governance & Security")

add_text(s, Inches(0.5), Inches(1.1), Inches(12), Inches(0.4),
         "Security is non-negotiable. Every layer enforces data isolation and auditability.",
         font_size=14, color=SLATE, bold=True)

# Critical rule banner
add_colored_card(s, Inches(0.5), Inches(1.7), Inches(12), Inches(0.7), RGBColor(0xFF, 0xED, 0xED), RED)
add_text(s, Inches(0.8), Inches(1.75), Inches(11.4), Inches(0.6),
         "🚫  CRITICAL RULE: No client-specific or sensitive data is EVER shared across teams or stored in shared agents",
         font_size=15, color=RED, bold=True)

# Security pillars
sec_pillars = [
    ("Data Isolation", [
        "Project config separated from shared logic",
        "Client data never enters Central Squad",
        "SubSquad memory is project-scoped only",
        "Agents are generic and template-based",
    ], ACCENT1),
    ("Approval Gates", [
        "Peer review for all shared agents",
        "Architect sign-off before publishing",
        "Automated security scanning",
        "Compliance validation checks",
    ], ACCENT2),
    ("Version Control", [
        "All agents version-controlled in Git",
        "Semantic versioning with changelogs",
        "Immutable release artifacts",
        "Full audit trail of changes",
    ], ACCENT5),
    ("Auditability", [
        "Decision logs for every engagement",
        "Agent usage tracking across SubSquads",
        "Governance compliance dashboard",
        "Regular security reviews",
    ], ACCENT6),
]

for i, (title, items, color) in enumerate(sec_pillars):
    left = Inches(0.5 + i * 3.1)
    top = Inches(2.7)
    add_colored_card(s, left, top, Inches(2.85), Inches(3.6), CARD_BG, color)
    add_colored_card(s, left, top, Inches(2.85), Inches(0.5), color)
    add_text(s, left + Inches(0.15), top + Inches(0.07), Inches(2.55), Inches(0.35),
             f"🛡️  {title}", font_size=14, color=WHITE, bold=True)

    for j, item in enumerate(items):
        y = top + Inches(0.7 + j * 0.65)
        add_text(s, left + Inches(0.2), y, Inches(2.45), Inches(0.5),
                 f"▸ {item}", font_size=11, color=BODY_TEXT)

add_footer(s, prs, 9, TOTAL_SLIDES)

# ═══════════════════════════════════════════════════════════════
# SLIDE 10 — ROLES & RESPONSIBILITIES
# ═══════════════════════════════════════════════════════════════
s = add_slide(prs)
set_white_bg(s)
add_title_bar(s, prs, "8. Roles & Responsibilities")

roles = [
    ("Architects", "Design patterns, define reusable agents,\nmake architectural decisions, review\nagent quality before Central publish", "🏛️", ACCENT2),
    ("Engineers", "Build and extend agents, implement\ndelivery automation, contribute\nimprovements back to Central", "⚡", ACCENT5),
    ("Central Squad", "Orchestrates shared library, enforces\ngovernance, tracks agent lifecycle,\nmaintains institutional memory", "🧠", ACCENT1),
    ("SubSquads", "Execute project delivery, pull agents\nfrom Central, apply shared patterns,\nreport learnings and improvements", "🚀", ACCENT6),
]

for i, (role, desc, icon, color) in enumerate(roles):
    col = i % 2
    row = i // 2
    left = Inches(0.5 + col * 6.25)
    top = Inches(1.2 + row * 2.6)

    add_colored_card(s, left, top, Inches(5.85), Inches(2.3), CARD_BG, color)
    add_accent_line(s, left, top, Inches(5.85), color, inside=True)

    add_icon_circle(s, left + Inches(0.2), top + Inches(0.4), 0.7, color, icon, 22)
    add_text(s, left + Inches(1.15), top + Inches(0.35), Inches(4.5), Inches(0.35),
             role, font_size=18, color=color, bold=True)
    add_multiline(s, left + Inches(1.15), top + Inches(0.8), Inches(4.5), Inches(1.4),
                  desc.split('\n'), font_size=12, color=BODY_TEXT)

# RACI note
add_colored_card(s, Inches(0.5), Inches(6.2), Inches(12), Inches(0.5), LIGHT_BG, ACCENT2)
add_text(s, Inches(0.8), Inches(6.25), Inches(11.4), Inches(0.4),
         "📋  RACI Matrix: Architects = Accountable  |  Engineers = Responsible  |  Central = Consulted  |  SubSquads = Informed",
         font_size=12, color=ACCENT2, bold=True)

add_footer(s, prs, 10, TOTAL_SLIDES)

# ═══════════════════════════════════════════════════════════════
# SLIDE 11 — VALUE & BENEFITS
# ═══════════════════════════════════════════════════════════════
s = add_slide(prs)
set_white_bg(s)
add_title_bar(s, prs, "9. Value & Benefits")

# Before vs After
add_section_label(s, Inches(0.5), Inches(1.1), "BEFORE: Manual Factory", color=RED, width=Inches(3))
add_section_label(s, Inches(6.7), Inches(1.1), "AFTER: Copilot Squad Model", color=GREEN, width=Inches(3.5))

before_items = [
    "Portal-driven, click-heavy execution",
    "Each team builds from scratch",
    "Knowledge locked in individual heads",
    "Inconsistent delivery quality",
    "Slow onboarding for new projects",
    "Manual documentation and handover",
]

after_items = [
    "AI-orchestrated, code-driven delivery",
    "Reusable agents from Central library",
    "Shared memory across all engagements",
    "Consistent quality via governance gates",
    "Instant SubSquad spin-up with shared skills",
    "Automated docs, journals, and handover",
]

for i, item in enumerate(before_items):
    y = Inches(1.6 + i * 0.55)
    add_text(s, Inches(0.7), y, Inches(0.2), Inches(0.25), "✕", font_size=13, color=RED, bold=True)
    add_text(s, Inches(1.0), y, Inches(5.2), Inches(0.4), item, font_size=12, color=BODY_TEXT)

for i, item in enumerate(after_items):
    y = Inches(1.6 + i * 0.55)
    add_text(s, Inches(6.9), y, Inches(0.2), Inches(0.25), "✓", font_size=13, color=GREEN, bold=True)
    add_text(s, Inches(7.2), y, Inches(5.2), Inches(0.4), item, font_size=12, color=BODY_TEXT)

# Divider
shape = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(6.3), Inches(1.1), Inches(0.03), Inches(3.2))
shape.fill.solid()
shape.fill.fore_color.rgb = BORDER_GRAY
shape.line.fill.background()

# Value metrics
add_section_label(s, Inches(0.5), Inches(5.0), "QUANTIFIED VALUE", color=ACCENT2, width=Inches(2.5))

metrics = [
    ("60%+", "Reduction in\nmanual effort", ACCENT2),
    ("3x", "Faster delivery\ncycles", GREEN),
    ("80%+", "Agent reuse\nacross projects", ACCENT5),
    ("Zero", "Duplicated agents\nacross teams", ACCENT1),
    ("100%", "IaC coverage\nno portal ops", ACCENT6),
]

for i, (val, label, color) in enumerate(metrics):
    left = Inches(0.5 + i * 2.5)
    add_colored_card(s, left, Inches(5.5), Inches(2.2), Inches(1.3), CARD_BG, color)
    add_text(s, left + Inches(0.15), Inches(5.6), Inches(1.9), Inches(0.5),
             val, font_size=28, color=color, bold=True, alignment=PP_ALIGN.CENTER)
    add_multiline(s, left + Inches(0.15), Inches(6.1), Inches(1.9), Inches(0.6),
                  label.split('\n'), font_size=10, color=BODY_TEXT)

add_footer(s, prs, 11, TOTAL_SLIDES)

# ═══════════════════════════════════════════════════════════════
# SLIDE 12 — SUCCESS METRICS
# ═══════════════════════════════════════════════════════════════
s = add_slide(prs)
set_white_bg(s)
add_title_bar(s, prs, "10. Success Metrics & KPIs")

add_text(s, Inches(0.5), Inches(1.1), Inches(12), Inches(0.4),
         "Measurable outcomes that define success for the Copilot Squad operating model",
         font_size=14, color=SLATE)

kpis = [
    ("Agent Reuse Rate", "% of agents reused across\nmultiple SubSquads", "Target: ≥80%", "Current: Baseline", ACCENT2),
    ("Manual Effort Reduction", "Hours saved per engagement\nvs. manual execution", "Target: ≥60%", "Current: Baseline", GREEN),
    ("Cycle Time Improvement", "Time from Intake to Handover\ncompared to previous model", "Target: 3x faster", "Current: Baseline", ACCENT5),
    ("Cross-Team Adoption", "Number of SubSquads actively\nusing Central Squad agents", "Target: 100%", "Current: Pilot", ACCENT1),
    ("Security Compliance", "% of agents passing\nsecurity gate validation", "Target: 100%", "Current: N/A", ACCENT6),
    ("Contribution Rate", "Improvements contributed\nback to Central per quarter", "Target: ≥5/team", "Current: Baseline", ACCENT3),
]

for i, (metric, desc, target, current, color) in enumerate(kpis):
    col = i % 3
    row = i // 3
    left = Inches(0.5 + col * 4.1)
    top = Inches(1.7 + row * 2.5)

    add_colored_card(s, left, top, Inches(3.8), Inches(2.2), CARD_BG, color)
    add_accent_line(s, left, top, Inches(3.8), color, inside=True)

    add_text(s, left + Inches(0.2), top + Inches(0.3), Inches(3.4), Inches(0.3),
             metric, font_size=15, color=color, bold=True)
    add_multiline(s, left + Inches(0.2), top + Inches(0.65), Inches(3.4), Inches(0.8),
                  desc.split('\n'), font_size=11, color=BODY_TEXT)

    # Target and current
    add_colored_card(s, left + Inches(0.15), top + Inches(1.4), Inches(1.65), Inches(0.55), LIGHT_BG)
    add_text(s, left + Inches(0.25), top + Inches(1.45), Inches(1.45), Inches(0.2),
             "TARGET", font_size=8, color=SUBTITLE, bold=True)
    add_text(s, left + Inches(0.25), top + Inches(1.65), Inches(1.45), Inches(0.25),
             target.replace("Target: ", ""), font_size=12, color=color, bold=True)

    add_colored_card(s, left + Inches(1.95), top + Inches(1.4), Inches(1.65), Inches(0.55), LIGHT_BG)
    add_text(s, left + Inches(2.05), top + Inches(1.45), Inches(1.45), Inches(0.2),
             "CURRENT", font_size=8, color=SUBTITLE, bold=True)
    add_text(s, left + Inches(2.05), top + Inches(1.65), Inches(1.45), Inches(0.25),
             current.replace("Current: ", ""), font_size=12, color=SUBTITLE)

add_footer(s, prs, 12, TOTAL_SLIDES)

# ═══════════════════════════════════════════════════════════════
# SLIDE 13 — IMPLEMENTATION ROADMAP
# ═══════════════════════════════════════════════════════════════
s = add_slide(prs)
set_white_bg(s)
add_title_bar(s, prs, "11. Implementation Roadmap")

add_text(s, Inches(0.5), Inches(1.1), Inches(12), Inches(0.4),
         "Phased rollout from pilot to full-scale adoption",
         font_size=14, color=SLATE)

waves = [
    ("WAVE 1", "Foundation", "Weeks 1–4", [
        "Establish Central Squad structure",
        "Define governance framework",
        "Create first 5 core agents",
        "Set up agent library repository",
    ], ACCENT2),
    ("WAVE 2", "Pilot", "Weeks 5–8", [
        "Launch 2 pilot SubSquads",
        "Execute first project deliveries",
        "Validate agent reuse model",
        "Collect improvement feedback",
    ], ACCENT5),
    ("WAVE 3", "Scale", "Weeks 9–16", [
        "Onboard remaining teams",
        "Expand agent catalog to 15+",
        "Automate contribution pipeline",
        "Deploy metrics dashboard",
    ], ACCENT3),
    ("WAVE 4", "Optimize", "Ongoing", [
        "Continuous agent improvement",
        "Advanced AI orchestration",
        "Cross-factory knowledge sharing",
        "Quarterly governance reviews",
    ], ACCENT6),
]

for i, (wave, name, timeline, items, color) in enumerate(waves):
    left = Inches(0.3 + i * 3.18)
    top = Inches(1.7)

    add_colored_card(s, left, top, Inches(2.95), Inches(4.8), CARD_BG, color)

    # Wave header
    add_colored_card(s, left, top, Inches(2.95), Inches(0.9), color)
    add_text(s, left + Inches(0.15), top + Inches(0.05), Inches(2.65), Inches(0.3),
             wave, font_size=12, color=WHITE, bold=True)
    add_text(s, left + Inches(0.15), top + Inches(0.3), Inches(2.65), Inches(0.3),
             name, font_size=18, color=WHITE, bold=True)
    add_text(s, left + Inches(0.15), top + Inches(0.6), Inches(2.65), Inches(0.25),
             timeline, font_size=10, color=RGBColor(0xCC, 0xDD, 0xFF))

    for j, item in enumerate(items):
        y = top + Inches(1.1 + j * 0.75)
        add_text(s, left + Inches(0.15), y, Inches(2.65), Inches(0.6),
                 f"▸ {item}", font_size=11, color=BODY_TEXT)

    # Arrow between waves
    if i < 3:
        add_arrow(s, left + Inches(3.0), Inches(2.6), Inches(0.15), color)

add_footer(s, prs, 13, TOTAL_SLIDES)

# ═══════════════════════════════════════════════════════════════
# SLIDE 14 — CLOSING / NEXT STEPS (LATAM template layout 0)
# ═══════════════════════════════════════════════════════════════
s = prs.slides.add_slide(prs.slide_layouts[0])
for sp in list(s.placeholders):
    sp_elem = sp._element
    sp_elem.getparent().remove(sp_elem)

add_text(s, Inches(0.8), Inches(1.2), Inches(11), Inches(0.5),
         "Microsoft Accelerated Factory", font_size=18, color=WHITE,
         font_name="Segoe Sans Display Semibold")

add_text(s, Inches(0.8), Inches(2.2), Inches(11), Inches(0.7),
         "Next Steps", font_size=44, color=WHITE, bold=True, font_name="Aptos Display")

next_steps = [
    ("01", "Review & Approve", "Stakeholder review of this SOW and alignment on scope, timelines, and governance model"),
    ("02", "Establish Central Squad", "Stand up the Central Squad with initial architecture, governance framework, and agent library"),
    ("03", "Launch Pilot SubSquads", "Select 2 pilot projects and deploy SubSquads using Central Squad agents and patterns"),
    ("04", "Measure & Scale", "Track KPIs from pilot, iterate on the model, and roll out to all Factory teams"),
]

for i, (num, title, desc) in enumerate(next_steps):
    y = Inches(3.3 + i * 0.85)
    add_icon_circle(s, Inches(0.8), y, 0.5, RGBColor(0xCC, 0xE5, 0xFF), num, 14)
    add_text(s, Inches(1.55), y + Inches(0.0), Inches(10), Inches(0.3),
             title, font_size=18, color=WHITE, bold=True)
    add_text(s, Inches(1.55), y + Inches(0.35), Inches(10), Inches(0.4),
             desc, font_size=12, color=RGBColor(0x90, 0xB8, 0xE0))

# Contact
add_text(s, Inches(0.8), Inches(6.5), Inches(11), Inches(0.35),
         "Ready to transform Factory delivery  |  Let's build the future together",
         font_size=14, color=RGBColor(0xCC, 0xE5, 0xFF), bold=True)

add_footer(s, prs, 14, TOTAL_SLIDES)

# ═══════════════════════════════════════════════════════════════
# SAVE
# ═══════════════════════════════════════════════════════════════
OUTPUT = os.path.join(BASE_DIR, "..", "decks", "Copilot_Squad_SOW.pptx")
prs.save(OUTPUT)
print(f"SOW deck saved: {OUTPUT}")
print(f"{TOTAL_SLIDES} slides generated")
