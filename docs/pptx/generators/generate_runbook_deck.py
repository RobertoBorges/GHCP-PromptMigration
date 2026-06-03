"""
Generate Runbook PowerPoint: Copilot Squad Operations Runbook
Step-by-step guide for teams using Central Squad + SubSquads
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
DARK_GREEN = RGBColor(0x1A, 0x5C, 0x2E)

TOTAL_SLIDES = 16

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
    """Rectangle card (no rounded corners) for header bars inside cards."""
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

def add_step_row(slide, left, top, num, title, desc, color, width=5.5):
    """Compact numbered step with title and description."""
    add_icon_circle(slide, left, top + Inches(0.02), 0.35, color, str(num), 12)
    add_text(slide, left + Inches(0.45), top, Inches(width), Inches(0.25),
             title, font_size=12, color=color, bold=True)
    add_text(slide, left + Inches(0.45), top + Inches(0.25), Inches(width), Inches(0.25),
             desc, font_size=10, color=BODY_TEXT)

# ═══════════════════════════════════════════════════════════════
# SLIDE 1 — TITLE (LATAM template layout 0 — blue gradient)
# ═══════════════════════════════════════════════════════════════
s = prs.slides.add_slide(prs.slide_layouts[0])
for sp in list(s.placeholders):
    sp_elem = sp._element
    sp_elem.getparent().remove(sp_elem)

add_text(s, Inches(0.8), Inches(1.2), Inches(11), Inches(0.5),
         "Microsoft Accelerated Factory", font_size=18, color=WHITE,
         font_name="Segoe Sans Display Semibold")
add_text(s, Inches(0.8), Inches(2.2), Inches(11), Inches(1.0),
         "Operations Runbook", font_size=54, color=WHITE, bold=True, font_name="Aptos Display")
add_text(s, Inches(0.8), Inches(3.5), Inches(11), Inches(0.6),
         "Copilot Squad: Central + SubSquad Model",
         font_size=26, color=RGBColor(0xCC, 0xE5, 0xFF), font_name="Aptos Display")
add_text(s, Inches(0.8), Inches(4.5), Inches(9), Inches(0.8),
         "Step-by-step guide for creating, sharing, and reusing agents at scale",
         font_size=15, color=RGBColor(0xB0, 0xD0, 0xF0))
add_text(s, Inches(0.8), Inches(6.0), Inches(6), Inches(0.7),
         "Audience: Engineers, Architects, Delivery Leads\nVersion 1.0  |  May 2026  |  Classification: Confidential",
         font_size=11, color=RGBColor(0x90, 0xB8, 0xE0))
add_footer(s, prs, 1, TOTAL_SLIDES)

# ═══════════════════════════════════════════════════════════════
# SLIDE 2 — TABLE OF CONTENTS
# ═══════════════════════════════════════════════════════════════
s = add_slide(prs); set_white_bg(s)
add_title_bar(s, prs, "Runbook Contents")

toc = [
    ("01", "Central Squad Setup", "Agent registry, shared memory, naming standards"),
    ("02", "SubSquad Creation", "Form project teams, pull agents, configure"),
    ("03", "Creating Agents", "When to reuse vs. create, avoiding client data"),
    ("04", "Publishing & Sharing", "Submit, version, approve, catalog"),
    ("05", "Reusing Agents", "Discover, pull, adapt, contribute back"),
    ("06", "Agents Become Skills", "Compounding capabilities over time"),
    ("07", "Multi-Team Coordination", "Parallel execution, shared consistency"),
    ("08", "Reduce Meetings", "Replace status meetings with automation"),
    ("09", "SNAP Model", "Borrow capabilities, not people"),
    ("10", "Factory Phase Execution", "Intake through Handover with agents"),
    ("11", "Continuous Improvement", "Capture, update, grow the skills library"),
]

for i, (num, title, desc) in enumerate(toc):
    col = i % 2
    row = i // 2
    left = Inches(0.5 + col * 6.3)
    top = Inches(1.1 + row * 0.88)
    color = [ACCENT2, ACCENT5, ACCENT6, ACCENT1, ACCENT3, GREEN, ACCENT2, ACCENT5, ACCENT6, ACCENT1, ACCENT3][i]
    add_icon_circle(s, left, top + Inches(0.05), 0.4, color, num, 11)
    add_text(s, left + Inches(0.5), top, Inches(5.5), Inches(0.3), title,
             font_size=14, color=color, bold=True)
    add_text(s, left + Inches(0.5), top + Inches(0.3), Inches(5.5), Inches(0.3), desc,
             font_size=10, color=SUBTITLE)

add_footer(s, prs, 2, TOTAL_SLIDES)

# ═══════════════════════════════════════════════════════════════
# SLIDE 3 — KEY PRINCIPLES
# ═══════════════════════════════════════════════════════════════
s = add_slide(prs); set_white_bg(s)
add_title_bar(s, prs, "Key Principles — Before You Start")

# Critical rule banner
add_colored_card(s, Inches(0.5), Inches(1.0), Inches(12), Inches(0.55), RGBColor(0xFF, 0xED, 0xED), RED)
add_text(s, Inches(0.8), Inches(1.05), Inches(11.4), Inches(0.45),
         "RULE: No client-specific or sensitive data is EVER stored in shared agents. All shared assets must be generic.",
         font_size=13, color=RED, bold=True)

principles = [
    ("Reuse First", "Always search the Central Squad registry before creating a new agent. Duplicate work is waste.",
     "Search registry -> Evaluate fit -> Adapt config -> Only then create new", ACCENT2),
    ("Agents Are Assets", "Agents belong to the organization, not individuals or projects. They are versioned, documented, and maintained.",
     "Named consistently -> Version-controlled -> Documented -> Maintained centrally", ACCENT5),
    ("Config Over Code", "Project-specific needs are handled through configuration, not by modifying shared agent code.",
     "Shared logic stays generic -> Project inputs via config files -> Never hardcode client data", ACCENT6),
    ("Compound, Don't Repeat", "Every engagement should make the system smarter. Improvements flow back to Central Squad.",
     "Use agent -> Find improvement -> Submit PR -> Central validates -> All teams benefit", GREEN),
]

for i, (title, desc, flow, color) in enumerate(principles):
    top = Inches(1.75 + i * 1.25)
    add_card(s, Inches(0.5), top, Inches(12), Inches(1.1), color)
    add_text(s, Inches(0.8), top + Inches(0.05), Inches(2.2), Inches(0.3),
             title, font_size=14, color=color, bold=True)
    add_text(s, Inches(0.8), top + Inches(0.35), Inches(5.0), Inches(0.5),
             desc, font_size=10, color=BODY_TEXT)
    # Flow
    add_section_label(s, Inches(6.2), top + Inches(0.05), "WORKFLOW", color=color, width=Inches(1.1))
    add_text(s, Inches(6.2), top + Inches(0.4), Inches(6.0), Inches(0.6),
             flow, font_size=9, color=SLATE)

add_footer(s, prs, 3, TOTAL_SLIDES)

# ═══════════════════════════════════════════════════════════════
# SLIDE 4 — CENTRAL SQUAD SETUP
# ═══════════════════════════════════════════════════════════════
s = add_slide(prs); set_white_bg(s)
add_title_bar(s, prs, "01  Central Squad Setup")

add_text(s, Inches(0.5), Inches(1.0), Inches(12), Inches(0.35),
         "The Central Squad is the brain: it stores agents, prompts, patterns, and institutional memory.",
         font_size=13, color=SLATE)

# Four storage areas
stores = [
    ("Agents", "Reusable agent charters with\nidentity, role, expertise, and\nbehavior rules", [
        ".squad/agents/<name>/charter.md",
        "Each agent has: name, role, expertise",
        "Style guide and domain boundaries",
        "Cross-agent handoff rules",
    ], ACCENT2),
    ("Prompts", "System prompts and templates\nthat encode organizational\nthinking patterns", [
        "AGENTS.md (operating instructions)",
        "CLAUDE.md (session memory)",
        "Routing rules (.squad/routing.md)",
        "Response format standards",
    ], ACCENT5),
    ("Patterns", "Reusable code patterns,\nIaC templates, and delivery\nplaybooks", [
        "Bicep/Terraform templates",
        "CI/CD pipeline templates",
        "Testing frameworks",
        "Architecture decision records",
    ], ACCENT6),
    ("Decisions", "Institutional memory that\nprevents repeating mistakes\nand losing context", [
        ".squad/decisions.md (active decisions)",
        "JOURNAL.md (build history)",
        "Lessons learned per engagement",
        "Trade-off documentation",
    ], GREEN),
]

for i, (title, desc, items, color) in enumerate(stores):
    left = Inches(0.4 + i * 3.15)
    top = Inches(1.55)
    add_colored_card(s, left, top, Inches(2.95), Inches(4.8), CARD_BG, color)
    # Header bar
    add_rect_card(s, left, top, Inches(2.95), Inches(0.55), color)
    add_text(s, left + Inches(0.15), top + Inches(0.08), Inches(2.65), Inches(0.4),
             title, font_size=16, color=WHITE, bold=True)
    # Description
    add_multiline(s, left + Inches(0.15), top + Inches(0.7), Inches(2.65), Inches(0.9),
                  desc.split('\n'), font_size=10, color=BODY_TEXT)
    # Items
    add_section_label(s, left + Inches(0.1), top + Inches(1.7), "CONTENTS", color=SLATE, width=Inches(1.1))
    for j, item in enumerate(items):
        y = top + Inches(2.1 + j * 0.55)
        add_text(s, left + Inches(0.15), y, Inches(2.65), Inches(0.45),
                 f"  {item}", font_size=9, color=BODY_TEXT)

# Naming standards bar
add_colored_card(s, Inches(0.4), Inches(6.0), Inches(12.5), Inches(0.35), NAVY)
add_text(s, Inches(0.7), Inches(6.02), Inches(12), Inches(0.3),
         "Naming:  agent-<domain>-<capability>  |  prompt-<context>-<version>  |  pattern-<type>-<stack>",
         font_size=10, color=WHITE, bold=True)

add_footer(s, prs, 4, TOTAL_SLIDES)

# ═══════════════════════════════════════════════════════════════
# SLIDE 5 — SUBSQUAD CREATION
# ═══════════════════════════════════════════════════════════════
s = add_slide(prs); set_white_bg(s)
add_title_bar(s, prs, "02  SubSquad Creation (Project Teams)")

add_text(s, Inches(0.5), Inches(1.0), Inches(12), Inches(0.35),
         "SubSquads are project execution teams. They pull agents from Central and configure for the engagement.",
         font_size=13, color=SLATE)

# Steps
steps = [
    ("1", "Assess Project Needs", "Identify required capabilities: backend, IaC, QA, AI, DevOps. Map to Factory phases.", ACCENT2),
    ("2", "Search Central Registry", "npx snap-squad list   Browse available agents, prompts, and patterns. Check fit.", ACCENT5),
    ("3", "Pull Required Agents", "npx snap-squad init --type <preset>   Clone agents into project workspace.", ACCENT6),
    ("4", "Configure Project Context", "Update CLAUDE.md with project owner, stack, and description. Set project-specific inputs only.", GREEN),
    ("5", "Set Routing Rules", "Update .squad/routing.md to map work types to agents. Define handoff rules.", ACCENT1),
    ("6", "Start Execution", "SubSquad is ready. Agents handle implementation, testing, docs, and deployment.", ACCENT3),
]

for i, (num, title, desc, color) in enumerate(steps):
    col = i % 2
    row = i // 2
    left = Inches(0.5 + col * 6.3)
    top = Inches(1.55 + row * 1.65)

    add_card(s, left, top, Inches(5.9), Inches(1.4), color)
    add_icon_circle(s, left + Inches(0.25), top + Inches(0.3), 0.5, color, num, 16)
    add_text(s, left + Inches(0.9), top + Inches(0.1), Inches(4.7), Inches(0.3),
             title, font_size=14, color=color, bold=True)
    add_multiline(s, left + Inches(0.9), top + Inches(0.45), Inches(4.7), Inches(0.8),
                  desc.split('\n'), font_size=10, color=BODY_TEXT)

# Warning
add_colored_card(s, Inches(0.5), Inches(6.1), Inches(12), Inches(0.3), LIGHT_BG, ACCENT2)
add_text(s, Inches(0.8), Inches(6.12), Inches(11.4), Inches(0.25),
         "Never modify shared agent logic for project needs. Use configuration files for project-specific inputs.",
         font_size=10, color=ACCENT2, bold=True)

add_footer(s, prs, 5, TOTAL_SLIDES)

# ═══════════════════════════════════════════════════════════════
# SLIDE 6 — CREATING AGENTS
# ═══════════════════════════════════════════════════════════════
s = add_slide(prs); set_white_bg(s)
add_title_bar(s, prs, "03  Creating Agents")

# Decision tree: Reuse vs Create
add_section_label(s, Inches(0.5), Inches(1.0), "DECISION: REUSE OR CREATE?", color=ACCENT2, width=Inches(3.5))

# Reuse path
add_colored_card(s, Inches(0.5), Inches(1.5), Inches(5.8), Inches(2.5), RGBColor(0xE8, 0xF5, 0xE9), GREEN)
add_text(s, Inches(0.7), Inches(1.55), Inches(5.4), Inches(0.3),
         "REUSE (Default Path)", font_size=15, color=GREEN, bold=True)
reuse_when = [
    "An agent with similar capability exists in Central",
    "You can achieve the goal with configuration changes only",
    "The gap is < 20% of the agent's current capability",
    "Another team has solved a similar problem before",
]
for j, item in enumerate(reuse_when):
    y = Inches(1.95 + j * 0.4)
    add_text(s, Inches(0.9), y, Inches(5.2), Inches(0.3), f"  {item}", font_size=10, color=BODY_TEXT)

# Create path
add_colored_card(s, Inches(6.7), Inches(1.5), Inches(5.8), Inches(2.5), RGBColor(0xFF, 0xF3, 0xE0), ACCENT3)
add_text(s, Inches(6.9), Inches(1.55), Inches(5.4), Inches(0.3),
         "CREATE NEW (Exception Path)", font_size=15, color=ACCENT3, bold=True)
create_when = [
    "No agent with overlapping capability exists",
    "The domain is entirely new to the organization",
    "Configuration cannot bridge the gap",
    "Approved by Central Squad Architect",
]
for j, item in enumerate(create_when):
    y = Inches(1.95 + j * 0.4)
    add_text(s, Inches(7.1), y, Inches(5.2), Inches(0.3), f"  {item}", font_size=10, color=BODY_TEXT)

# How to create
add_section_label(s, Inches(0.5), Inches(4.3), "HOW TO CREATE A REUSABLE AGENT", color=ACCENT5, width=Inches(4))

create_steps = [
    ("1", "Define Charter", "Create .squad/agents/<name>/charter.md with identity, role, expertise, style, and boundaries"),
    ("2", "Keep Generic", "No client names, project IDs, or sensitive data. Use template variables for project-specific values"),
    ("3", "Add Routing", "Update routing.md to map work types to the new agent. Define when it should lead vs. support"),
    ("4", "Test Isolation", "Verify the agent works with zero project context. It must be usable by any SubSquad"),
    ("5", "Submit to Central", "Open PR to Central Squad repo. Include: charter, test results, usage examples"),
]

for i, (num, title, desc) in enumerate(create_steps):
    top = Inches(4.75 + i * 0.38)
    add_text(s, Inches(0.7), top, Inches(0.3), Inches(0.25), num, font_size=11, color=ACCENT5, bold=True)
    add_text(s, Inches(1.1), top, Inches(1.5), Inches(0.25), title, font_size=11, color=ACCENT5, bold=True)
    add_text(s, Inches(2.8), top, Inches(9.5), Inches(0.25), desc, font_size=10, color=BODY_TEXT)

add_footer(s, prs, 6, TOTAL_SLIDES)

# ═══════════════════════════════════════════════════════════════
# SLIDE 7 — PUBLISHING & SHARING
# ═══════════════════════════════════════════════════════════════
s = add_slide(prs); set_white_bg(s)
add_title_bar(s, prs, "04  Publishing & Sharing Agents")

add_text(s, Inches(0.5), Inches(1.0), Inches(12), Inches(0.35),
         "Every shared agent goes through a structured publish pipeline to ensure quality and security.",
         font_size=13, color=SLATE)

# Pipeline flow
pipeline = [
    ("DEVELOP", "Build and test\nagent locally in\nSubSquad context", ACCENT2),
    ("SUBMIT", "Open PR to\nCentral Squad\nrepository", ACCENT5),
    ("REVIEW", "Peer review +\nArchitect sign-off\nrequired", ACCENT3),
    ("VALIDATE", "Automated checks:\nsecurity scan,\nisolation test", GREEN),
    ("PUBLISH", "Merge to Central,\nassign version,\nupdate catalog", ACCENT6),
]

for i, (stage, desc, color) in enumerate(pipeline):
    left = Inches(0.3 + i * 2.55)
    top = Inches(1.55)
    add_colored_card(s, left, top, Inches(2.3), Inches(2.2), CARD_BG, color)
    add_rect_card(s, left, top, Inches(2.3), Inches(0.45), color)
    add_text(s, left + Inches(0.1), top + Inches(0.05), Inches(2.1), Inches(0.35),
             stage, font_size=14, color=WHITE, bold=True, alignment=PP_ALIGN.CENTER)
    add_multiline(s, left + Inches(0.15), top + Inches(0.6), Inches(2.0), Inches(1.2),
                  desc.split('\n'), font_size=11, color=BODY_TEXT)
    if i < 4:
        add_arrow(s, left + Inches(2.35), top + Inches(0.85), Inches(0.18), color)

# Versioning rules
add_section_label(s, Inches(0.5), Inches(4.0), "VERSIONING RULES", color=ACCENT1, width=Inches(2.2))

ver_rules = [
    ("MAJOR (v2.0)", "Breaking changes to agent charter or behavior", "Requires migration guide"),
    ("MINOR (v1.1)", "New capabilities added, backward compatible", "Requires changelog entry"),
    ("PATCH (v1.0.1)", "Bug fixes, prompt refinements, typo corrections", "Auto-approved if tests pass"),
]

for i, (version, desc, req) in enumerate(ver_rules):
    top = Inches(4.5 + i * 0.65)
    add_text(s, Inches(0.7), top, Inches(2.0), Inches(0.25), version, font_size=12, color=ACCENT1, bold=True)
    add_text(s, Inches(2.8), top, Inches(5.0), Inches(0.25), desc, font_size=11, color=BODY_TEXT)
    add_text(s, Inches(8.0), top, Inches(4.5), Inches(0.25), req, font_size=10, color=SLATE)

# Documentation checklist
add_section_label(s, Inches(0.5), Inches(5.9), "REQUIRED DOCUMENTATION", color=ACCENT6, width=Inches(2.8))
docs = ["Charter (.md)", "Usage examples", "Test results", "Changelog", "Migration notes (if major)"]
for i, d in enumerate(docs):
    x = Inches(0.7 + i * 2.45)
    add_text(s, x, Inches(6.15), Inches(2.2), Inches(0.25), f"  {d}", font_size=10, color=BODY_TEXT)

add_footer(s, prs, 7, TOTAL_SLIDES)

# ═══════════════════════════════════════════════════════════════
# SLIDE 8 — REUSING AGENTS (CORE BEHAVIOR)
# ═══════════════════════════════════════════════════════════════
s = add_slide(prs); set_white_bg(s)
add_title_bar(s, prs, "05  Reusing Agents (Core Behavior)")

# Core message
add_colored_card(s, Inches(0.5), Inches(1.0), Inches(12), Inches(0.5), LIGHT_BG, ACCENT2)
add_text(s, Inches(0.8), Inches(1.05), Inches(11.4), Inches(0.4),
         "Reuse is the DEFAULT. Creating new agents is the EXCEPTION. Search first, always.",
         font_size=14, color=ACCENT2, bold=True)

# Steps
reuse_steps = [
    ("1", "Discover", "Browse Central Squad agent catalog. Search by domain, capability, or keyword.\nnpx snap-squad list  or check .squad/team.md", ACCENT2),
    ("2", "Evaluate", "Review the agent's charter: does its expertise cover >= 80% of your need?\nCheck version history, last updated date, and usage across other SubSquads.", ACCENT5),
    ("3", "Pull", "Clone the agent into your SubSquad workspace.\nnpx snap-squad init --type <preset>  preserves Central linkage for updates.", ACCENT6),
    ("4", "Configure", "Adapt using project-specific configuration ONLY. Update CLAUDE.md and routing.md.\nNever modify the agent charter or shared logic. Use environment variables for secrets.", GREEN),
    ("5", "Execute", "Use the agent in your delivery workflow. It handles its domain autonomously.\nThe agent follows routing rules and hands off to other agents as defined.", ACCENT3),
    ("6", "Contribute", "Found an improvement? Submit a PR back to Central Squad with your enhancement.\nYour improvement benefits every SubSquad that uses this agent.", ACCENT1),
]

for i, (num, title, desc, color) in enumerate(reuse_steps):
    top = Inches(1.7 + i * 0.82)
    add_card(s, Inches(0.5), top, Inches(12), Inches(0.7), color)
    add_icon_circle(s, Inches(0.7), top + Inches(0.08), 0.38, color, num, 12)
    add_text(s, Inches(1.2), top + Inches(0.02), Inches(1.5), Inches(0.25),
             title, font_size=13, color=color, bold=True)
    add_multiline(s, Inches(2.8), top + Inches(0.02), Inches(9.5), Inches(0.6),
                  desc.split('\n'), font_size=9, color=BODY_TEXT)

add_footer(s, prs, 8, TOTAL_SLIDES)

# ═══════════════════════════════════════════════════════════════
# SLIDE 9 — AGENTS BECOME SKILLS
# ═══════════════════════════════════════════════════════════════
s = add_slide(prs); set_white_bg(s)
add_title_bar(s, prs, "06  How Agents Become Skills")

add_text(s, Inches(0.5), Inches(1.0), Inches(12), Inches(0.35),
         "Agents are not one-time tools. They compound into organizational skills that scale.",
         font_size=13, color=SLATE)

# Three skill types
skill_types = [
    ("Agents = Capabilities", "Reusable execution engines\nthat handle specific domains\nautonomously", [
        "Coder: writes and debugs code",
        "Tester: finds edge cases, writes tests",
        "GitOps: manages CI/CD and releases",
        "DevRel: generates documentation",
    ], ACCENT2),
    ("Prompts = Thinking", "Reusable reasoning patterns\nthat encode organizational\ndecision-making", [
        "Architecture decision templates",
        "Code review criteria",
        "Security validation checklists",
        "Routing and handoff logic",
    ], ACCENT5),
    ("Outputs = Templates", "Reusable deliverables that\neliminate starting from\nblank pages", [
        "IaC templates (Bicep/Terraform)",
        "API scaffolding patterns",
        "Test framework setups",
        "Documentation structures",
    ], ACCENT6),
]

for i, (title, desc, items, color) in enumerate(skill_types):
    left = Inches(0.5 + i * 4.1)
    top = Inches(1.55)
    add_colored_card(s, left, top, Inches(3.8), Inches(3.5), CARD_BG, color)
    add_rect_card(s, left, top, Inches(3.8), Inches(0.5), color)
    add_text(s, left + Inches(0.15), top + Inches(0.07), Inches(3.5), Inches(0.35),
             title, font_size=14, color=WHITE, bold=True)
    add_multiline(s, left + Inches(0.15), top + Inches(0.6), Inches(3.5), Inches(0.9),
                  desc.split('\n'), font_size=10, color=BODY_TEXT)
    for j, item in enumerate(items):
        y = top + Inches(1.55 + j * 0.42)
        add_text(s, left + Inches(0.15), y, Inches(3.5), Inches(0.3),
                 f"  {item}", font_size=10, color=BODY_TEXT)

# Compounding loop
add_colored_card(s, Inches(0.5), Inches(5.3), Inches(12), Inches(1.1), NAVY)
add_text(s, Inches(0.8), Inches(5.35), Inches(11.4), Inches(0.3),
         "THE COMPOUNDING LOOP", font_size=13, color=ACCENT4, bold=True)

loop_stages = ["USE", "IMPROVE", "SHARE", "REUSE", "SCALE"]
loop_colors = [ACCENT2, GREEN, ACCENT5, ACCENT3, ACCENT4]
for i, (stage, lc) in enumerate(zip(loop_stages, loop_colors)):
    x = Inches(1.0 + i * 2.3)
    add_icon_circle(s, x, Inches(5.75), 0.45, lc, stage, 9)
    if i < 4:
        add_arrow(s, x + Inches(0.55), Inches(5.85), Inches(0.35), lc)

add_text(s, Inches(0.8), Inches(6.3), Inches(11.4), Inches(0.3),
         "Every engagement makes the entire system smarter. Skills compound, they don't decay.",
         font_size=10, color=WHITE)

add_footer(s, prs, 9, TOTAL_SLIDES)

# ═══════════════════════════════════════════════════════════════
# SLIDE 10 — MULTI-TEAM COORDINATION
# ═══════════════════════════════════════════════════════════════
s = add_slide(prs); set_white_bg(s)
add_title_bar(s, prs, "07  Multi-Team Coordination")

add_text(s, Inches(0.5), Inches(1.0), Inches(12), Inches(0.35),
         "SubSquads work in parallel. Central Squad ensures consistency without bottlenecking execution.",
         font_size=13, color=SLATE)

# Central hub diagram
add_colored_card(s, Inches(4.5), Inches(1.6), Inches(4.0), Inches(1.8), LIGHT_BG, ACCENT2)
add_text(s, Inches(4.7), Inches(1.7), Inches(3.6), Inches(0.3),
         "CENTRAL SQUAD", font_size=16, color=ACCENT2, bold=True, alignment=PP_ALIGN.CENTER)
central_items = ["Agent Library  |  Governance  |  Standards", "Decisions  |  Patterns  |  Shared Memory"]
add_multiline(s, Inches(4.7), Inches(2.1), Inches(3.6), Inches(0.8),
              central_items, font_size=10, color=BODY_TEXT)

# SubSquads around it
subsquad_data = [
    ("SubSquad A", "Project Alpha\nBackend + IaC", Inches(0.5), Inches(1.8), ACCENT5),
    ("SubSquad B", "Project Beta\nAI + Data", Inches(9.5), Inches(1.8), ACCENT6),
    ("SubSquad C", "Project Gamma\nFrontend + API", Inches(0.5), Inches(4.0), ACCENT3),
    ("SubSquad D", "Project Delta\nMigration + QA", Inches(9.5), Inches(4.0), ACCENT1),
]

for name, desc, left, top, color in subsquad_data:
    add_colored_card(s, left, top, Inches(3.5), Inches(1.3), CARD_BG, color)
    add_rect_card(s, left, top, Inches(3.5), Inches(0.4), color)
    add_text(s, left + Inches(0.1), top + Inches(0.03), Inches(3.3), Inches(0.3),
             name, font_size=12, color=WHITE, bold=True)
    add_multiline(s, left + Inches(0.15), top + Inches(0.5), Inches(3.2), Inches(0.7),
                  desc.split('\n'), font_size=10, color=BODY_TEXT)

# Coordination rules
add_section_label(s, Inches(0.5), Inches(5.6), "COORDINATION RULES", color=ACCENT2, width=Inches(2.3))

rules = [
    ("No Duplication", "If Central has an agent, use it. Never rebuild what exists."),
    ("Shared Standards", "All SubSquads follow the same coding, testing, and documentation patterns."),
    ("Async by Default", "SubSquads do not wait for each other. Central Squad resolves conflicts asynchronously."),
    ("Contribute Back", "Every SubSquad must submit improvements to Central at engagement end."),
]

for i, (title, desc) in enumerate(rules):
    col = i % 2
    row = i // 2
    left = Inches(0.5 + col * 6.3)
    top = Inches(6.0 + row * 0.35)
    add_text(s, left, top, Inches(1.8), Inches(0.25), title, font_size=10, color=ACCENT2, bold=True)
    add_text(s, left + Inches(1.9), top, Inches(4.2), Inches(0.25), desc, font_size=9, color=BODY_TEXT)

add_footer(s, prs, 10, TOTAL_SLIDES)

# ═══════════════════════════════════════════════════════════════
# SLIDE 11 — REDUCE MEETINGS
# ═══════════════════════════════════════════════════════════════
s = add_slide(prs); set_white_bg(s)
add_title_bar(s, prs, "08  Replace Meetings with Automation")

add_text(s, Inches(0.5), Inches(1.0), Inches(12), Inches(0.35),
         "Most status meetings exist because information is trapped in people's heads. Agents fix that.",
         font_size=13, color=SLATE)

# Before/After
add_section_label(s, Inches(0.5), Inches(1.55), "REPLACE THIS...", color=RED, width=Inches(2.0))
add_section_label(s, Inches(6.7), Inches(1.55), "...WITH THIS", color=GREEN, width=Inches(1.8))

replacements = [
    ("Daily standup meetings", "Agent-generated status dashboard from git activity and task progress"),
    ("Weekly status reports", "Automated weekly summary from Scribe agent (JOURNAL.md)"),
    ("Architecture review meetings", "Architect agent generates ADRs; async review via PR comments"),
    ("Manual coordination emails", "Routing rules auto-dispatch work to the right agent"),
    ("Knowledge transfer sessions", "DevRel agent generates onboarding docs automatically"),
    ("Post-mortem meetings", "Decisions.md + JOURNAL.md capture lessons in real-time"),
]

for i, (before, after) in enumerate(replacements):
    y = Inches(2.0 + i * 0.65)
    # Before
    add_text(s, Inches(0.7), y, Inches(0.2), Inches(0.2), "X", font_size=11, color=RED, bold=True)
    add_text(s, Inches(1.0), y, Inches(5.2), Inches(0.5), before, font_size=11, color=BODY_TEXT)
    # After
    add_text(s, Inches(6.9), y, Inches(0.2), Inches(0.2), ">", font_size=11, color=GREEN, bold=True)
    add_text(s, Inches(7.2), y, Inches(5.5), Inches(0.5), after, font_size=10, color=BODY_TEXT)

# Divider
shape = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(6.35), Inches(1.55), Inches(0.03), Inches(4.3))
shape.fill.solid(); shape.fill.fore_color.rgb = BORDER_GRAY; shape.line.fill.background()

# Impact
add_colored_card(s, Inches(0.5), Inches(6.2), Inches(12), Inches(0.5), NAVY)
add_text(s, Inches(0.8), Inches(6.25), Inches(11.4), Inches(0.4),
         "Result: ~60% fewer recurring meetings. Information flows through agents, not calendars.",
         font_size=12, color=WHITE, bold=True)

add_footer(s, prs, 11, TOTAL_SLIDES)

# ═══════════════════════════════════════════════════════════════
# SLIDE 12 — SNAP MODEL
# ═══════════════════════════════════════════════════════════════
s = add_slide(prs); set_white_bg(s)
add_title_bar(s, prs, "09  SNAP Model (Borrow Capabilities)")

add_text(s, Inches(0.5), Inches(1.0), Inches(12), Inches(0.35),
         "Teams request capabilities, not people. Expertise is dynamically attached to SubSquads.",
         font_size=13, color=SLATE, bold=True)

# SNAP explanation
add_colored_card(s, Inches(0.5), Inches(1.55), Inches(5.5), Inches(2.0), LIGHT_BG, ACCENT2)
add_text(s, Inches(0.7), Inches(1.6), Inches(5.1), Inches(0.3),
         "HOW SNAP WORKS", font_size=14, color=ACCENT2, bold=True)
snap_steps = [
    "1. SubSquad identifies a capability gap (e.g., needs IaC expertise)",
    "2. Requests capability from Central Squad (not a specific person)",
    "3. Central attaches the relevant agent(s) to the SubSquad",
    "4. Agent operates within SubSquad for the needed duration",
    "5. Agent detaches when work completes, returns to Central pool",
]
add_multiline(s, Inches(0.7), Inches(2.0), Inches(5.1), Inches(1.4),
              snap_steps, font_size=10, color=BODY_TEXT)

# Available capabilities
add_section_label(s, Inches(6.5), Inches(1.55), "AVAILABLE CAPABILITIES", color=ACCENT5, width=Inches(3))

capabilities = [
    ("Backend", "API design, server logic, data layers", ACCENT2),
    ("IaC", "Bicep, Terraform, azd templates", ACCENT5),
    ("QA / Testing", "Test strategies, automation, edge cases", GREEN),
    ("AI / ML", "Model integration, prompt engineering", ACCENT6),
    ("DevOps", "CI/CD, pipelines, release management", ACCENT3),
    ("Security", "Compliance, scanning, access control", ACCENT1),
    ("Frontend", "UI components, frameworks, responsive", ACCENT4),
    ("Data", "Databases, migrations, analytics", SLATE),
]

for i, (cap, desc, color) in enumerate(capabilities):
    col = i % 2
    row = i // 2
    left = Inches(6.5 + col * 3.1)
    top = Inches(2.0 + row * 0.62)
    add_text(s, left, top, Inches(1.2), Inches(0.25), cap, font_size=10, color=color, bold=True)
    add_text(s, left + Inches(1.3), top, Inches(1.6), Inches(0.5), desc, font_size=9, color=BODY_TEXT)

# Key principle
add_colored_card(s, Inches(0.5), Inches(4.0), Inches(12), Inches(0.55), NAVY)
add_text(s, Inches(0.8), Inches(4.05), Inches(11.4), Inches(0.45),
         "SNAP = Scale capacity without moving people. Attach expertise. Detach when done. No reorgs needed.",
         font_size=13, color=WHITE, bold=True)

# Scaling diagram
add_section_label(s, Inches(0.5), Inches(4.8), "SCALING EXAMPLE", color=ACCENT6, width=Inches(2))

scale_phases = [
    ("Week 1-2", "SubSquad starts with\nCoder + Tester", "2 agents", ACCENT2),
    ("Week 3-4", "SNAPs in IaC +\nDevOps capability", "4 agents", ACCENT5),
    ("Week 5-6", "Adds AI agent\nfor ML integration", "5 agents", ACCENT6),
    ("Week 7-8", "Detaches AI + IaC\nafter completion", "3 agents", ACCENT3),
    ("Handover", "SNAPs in DevRel\nfor documentation", "3 agents", GREEN),
]

for i, (phase, desc, count, color) in enumerate(scale_phases):
    left = Inches(0.3 + i * 2.55)
    top = Inches(5.2)
    add_colored_card(s, left, top, Inches(2.3), Inches(1.3), CARD_BG, color)
    add_rect_card(s, left, top, Inches(2.3), Inches(0.35), color)
    add_text(s, left + Inches(0.1), top + Inches(0.03), Inches(2.1), Inches(0.25),
             phase, font_size=10, color=WHITE, bold=True)
    add_multiline(s, left + Inches(0.1), top + Inches(0.45), Inches(2.1), Inches(0.5),
                  desc.split('\n'), font_size=9, color=BODY_TEXT)
    add_text(s, left + Inches(0.1), top + Inches(1.0), Inches(2.1), Inches(0.2),
             count, font_size=10, color=color, bold=True)
    if i < 4:
        add_arrow(s, left + Inches(2.35), top + Inches(0.5), Inches(0.15), color)

add_footer(s, prs, 12, TOTAL_SLIDES)

# ═══════════════════════════════════════════════════════════════
# SLIDE 13 — FACTORY PHASE EXECUTION
# ═══════════════════════════════════════════════════════════════
s = add_slide(prs); set_white_bg(s)
add_title_bar(s, prs, "10  Execution by Factory Phase")

add_text(s, Inches(0.5), Inches(1.0), Inches(12), Inches(0.35),
         "What agents do at each phase of the Accelerate Factory delivery model.",
         font_size=13, color=SLATE)

phases = [
    ("INTAKE", [
        "Researcher scans requirements",
        "Architect generates scope doc",
        "Agent identifies reusable assets",
        "Auto-generates project skeleton",
    ], "Deliverables: scope doc, asset map,\nSubSquad composition", ACCENT2),
    ("DESIGN", [
        "Architect produces ADRs",
        "Prompter designs agent config",
        "IaC templates selected from lib",
        "Security patterns applied",
    ], "Deliverables: architecture docs,\nIaC plan, agent roster", ACCENT5),
    ("BUILD", [
        "Coder implements features",
        "Tester writes and runs tests",
        "SubSquads execute in parallel",
        "Shared agents ensure consistency",
    ], "Deliverables: working code,\ntest suites, automated builds", ACCENT3),
    ("DEPLOY", [
        "GitOps manages CI/CD pipeline",
        "IaC deploys infra (no portal)",
        "Evaluator validates quality gates",
        "Zero manual deployment steps",
    ], "Deliverables: deployed infra,\npipeline configs, validation report", GREEN),
    ("HANDOVER", [
        "DevRel generates all docs",
        "Scribe writes build journal",
        "Improvements submitted to Central",
        "Runbook auto-generated",
    ], "Deliverables: docs, runbook,\njournal, Central contributions", ACCENT6),
]

for i, (phase, steps, deliverables, color) in enumerate(phases):
    left = Inches(0.3 + i * 2.55)
    top = Inches(1.55)
    add_colored_card(s, left, top, Inches(2.3), Inches(5.0), CARD_BG, color)
    # Phase header
    add_rect_card(s, left, top, Inches(2.3), Inches(0.5), color)
    add_text(s, left + Inches(0.1), top + Inches(0.07), Inches(2.1), Inches(0.35),
             phase, font_size=15, color=WHITE, bold=True, alignment=PP_ALIGN.CENTER)
    # Steps
    add_section_label(s, left + Inches(0.1), top + Inches(0.65), "AGENT ACTIONS", color=SLATE, width=Inches(1.5))
    for j, step in enumerate(steps):
        y = top + Inches(1.05 + j * 0.5)
        add_text(s, left + Inches(0.1), y, Inches(2.1), Inches(0.4),
                 f"  {step}", font_size=9, color=BODY_TEXT)
    # Deliverables
    add_section_label(s, left + Inches(0.1), top + Inches(3.2), "OUTPUT", color=color, width=Inches(1.0))
    add_multiline(s, left + Inches(0.1), top + Inches(3.6), Inches(2.1), Inches(1.0),
                  deliverables.split('\n'), font_size=9, color=SLATE)
    # Arrow
    if i < 4:
        add_arrow(s, left + Inches(2.35), top + Inches(0.15), Inches(0.15), color)

add_footer(s, prs, 13, TOTAL_SLIDES)

# ═══════════════════════════════════════════════════════════════
# SLIDE 14 — CONTINUOUS IMPROVEMENT
# ═══════════════════════════════════════════════════════════════
s = add_slide(prs); set_white_bg(s)
add_title_bar(s, prs, "11  Continuous Improvement")

add_text(s, Inches(0.5), Inches(1.0), Inches(12), Inches(0.35),
         "The system gets smarter with every engagement. Here's how to make that happen.",
         font_size=13, color=SLATE)

# Improvement cycle
cycle = [
    ("CAPTURE", "During Execution", [
        "Log decisions in .squad/decisions.md",
        "Record lessons in JOURNAL.md",
        "Note agent gaps and workarounds",
        "Track what worked and what didn't",
    ], ACCENT2),
    ("UPDATE", "Post-Engagement", [
        "Submit PRs for agent improvements",
        "Update prompts with new patterns",
        "Add new IaC/code templates",
        "Refine routing rules",
    ], ACCENT5),
    ("VALIDATE", "Central Review", [
        "Architect reviews contributions",
        "Security scan on all changes",
        "Test isolation (no client data)",
        "Version and publish updates",
    ], GREEN),
    ("DISTRIBUTE", "All Teams Benefit", [
        "Updated agents available to all",
        "New patterns in shared library",
        "Improved prompts for everyone",
        "Catalog reflects latest versions",
    ], ACCENT6),
]

for i, (stage, timing, items, color) in enumerate(cycle):
    left = Inches(0.4 + i * 3.15)
    top = Inches(1.55)
    add_colored_card(s, left, top, Inches(2.95), Inches(3.8), CARD_BG, color)
    add_rect_card(s, left, top, Inches(2.95), Inches(0.7), color)
    add_text(s, left + Inches(0.1), top + Inches(0.03), Inches(2.75), Inches(0.3),
             stage, font_size=14, color=WHITE, bold=True)
    add_text(s, left + Inches(0.1), top + Inches(0.35), Inches(2.75), Inches(0.25),
             timing, font_size=10, color=RGBColor(0xCC, 0xDD, 0xFF))
    for j, item in enumerate(items):
        y = top + Inches(0.9 + j * 0.6)
        add_text(s, left + Inches(0.1), y, Inches(2.75), Inches(0.45),
                 f"  {item}", font_size=10, color=BODY_TEXT)
    if i < 3:
        add_arrow(s, left + Inches(3.0), top + Inches(0.25), Inches(0.15), color)

# Anti-patterns
add_section_label(s, Inches(0.5), Inches(5.6), "ANTI-PATTERNS TO AVOID", color=RED, width=Inches(2.5))

anti = [
    ("Rebuilding from scratch", "Always check Central first. If it exists, reuse it."),
    ("Hoarding improvements", "Improvements left in SubSquads die with the project."),
    ("Embedding client data", "Shared agents must be 100% generic. Use config for specifics."),
    ("Skipping documentation", "Undocumented improvements are invisible improvements."),
]

for i, (pattern, fix) in enumerate(anti):
    col = i % 2
    row = i // 2
    left = Inches(0.5 + col * 6.3)
    top = Inches(6.0 + row * 0.35)
    add_text(s, left, top, Inches(2.2), Inches(0.25), f"X  {pattern}", font_size=10, color=RED, bold=True)
    add_text(s, left + Inches(2.3), top, Inches(3.8), Inches(0.25), fix, font_size=9, color=BODY_TEXT)

add_footer(s, prs, 14, TOTAL_SLIDES)

# ═══════════════════════════════════════════════════════════════
# SLIDE 15 — QUICK REFERENCE CARD
# ═══════════════════════════════════════════════════════════════
s = add_slide(prs); set_white_bg(s)
add_title_bar(s, prs, "Quick Reference Card")

# Commands
add_section_label(s, Inches(0.5), Inches(1.0), "ESSENTIAL COMMANDS", color=ACCENT2, width=Inches(2.5))

commands = [
    ("npx snap-squad list", "See available presets and agents"),
    ("npx snap-squad init --type <preset>", "Initialize SubSquad with preset agents"),
    ("npx snap-squad init --type <preset> --force", "Reset or switch squad preset"),
    ("cat .squad/team.md", "View current team roster"),
    ("cat .squad/routing.md", "View work routing rules"),
    ("cat .squad/decisions.md", "View active decisions"),
]

for i, (cmd, desc) in enumerate(commands):
    y = Inches(1.45 + i * 0.35)
    add_text(s, Inches(0.7), y, Inches(5.5), Inches(0.25), cmd, font_size=10, color=ACCENT2, bold=True)
    add_text(s, Inches(6.5), y, Inches(6.0), Inches(0.25), desc, font_size=10, color=BODY_TEXT)

# File map
add_section_label(s, Inches(0.5), Inches(3.7), "KEY FILES", color=ACCENT5, width=Inches(1.5))

files = [
    ("AGENTS.md", "Operating instructions for all agents"),
    ("CLAUDE.md", "Session memory and project context"),
    (".squad/team.md", "Team roster and project metadata"),
    (".squad/routing.md", "Work type to agent mapping"),
    (".squad/decisions.md", "Active design decisions"),
    (".squad/agents/<name>/charter.md", "Individual agent charter"),
    ("JOURNAL.md", "Build history and milestones"),
]

for i, (f, desc) in enumerate(files):
    y = Inches(4.1 + i * 0.32)
    add_text(s, Inches(0.7), y, Inches(4.5), Inches(0.25), f, font_size=10, color=ACCENT5, bold=True)
    add_text(s, Inches(5.5), y, Inches(7.0), Inches(0.25), desc, font_size=10, color=BODY_TEXT)

# Checklist
add_section_label(s, Inches(0.5), Inches(5.9), "BEFORE EVERY ENGAGEMENT", color=GREEN, width=Inches(2.8))
checks = ["Search Central registry", "Pull agents (don't rebuild)", "Configure (don't modify)", "Contribute back at end"]
for i, c in enumerate(checks):
    x = Inches(0.7 + i * 3.0)
    add_text(s, x, Inches(6.15), Inches(2.8), Inches(0.25), f"  {c}", font_size=10, color=BODY_TEXT)

add_footer(s, prs, 15, TOTAL_SLIDES)

# ═══════════════════════════════════════════════════════════════
# SLIDE 16 — CLOSING (LATAM template layout 0 — blue gradient)
# ═══════════════════════════════════════════════════════════════
s = prs.slides.add_slide(prs.slide_layouts[0])
for sp in list(s.placeholders):
    sp_elem = sp._element
    sp_elem.getparent().remove(sp_elem)

add_text(s, Inches(0.8), Inches(1.2), Inches(11), Inches(0.5),
         "Microsoft Accelerated Factory", font_size=18, color=WHITE,
         font_name="Segoe Sans Display Semibold")
add_text(s, Inches(0.8), Inches(2.2), Inches(11), Inches(0.7),
         "Start Using the Runbook", font_size=44, color=WHITE, bold=True, font_name="Aptos Display")

closing_steps = [
    ("01", "Search First", "Check Central Squad registry before creating anything new"),
    ("02", "Configure, Don't Modify", "Use project-specific config. Never change shared agent logic"),
    ("03", "Contribute Back", "Every improvement you make should benefit every team"),
    ("04", "Compound Skills", "The system gets smarter with every engagement. Make it count"),
]

for i, (num, title, desc) in enumerate(closing_steps):
    y = Inches(3.3 + i * 0.85)
    add_icon_circle(s, Inches(0.8), y, 0.45, RGBColor(0xCC, 0xE5, 0xFF), num, 13)
    add_text(s, Inches(1.5), y + Inches(0.0), Inches(10), Inches(0.3),
             title, font_size=18, color=WHITE, bold=True)
    add_text(s, Inches(1.5), y + Inches(0.35), Inches(10), Inches(0.35),
             desc, font_size=12, color=RGBColor(0x90, 0xB8, 0xE0))

add_text(s, Inches(0.8), Inches(6.2), Inches(11), Inches(0.35),
         "Reuse is the default. Creating is the exception. Every engagement makes us smarter.",
         font_size=14, color=RGBColor(0xCC, 0xE5, 0xFF), bold=True)

add_footer(s, prs, 16, TOTAL_SLIDES)

# ═══════════════════════════════════════════════════════════════
# SAVE
# ═══════════════════════════════════════════════════════════════
OUTPUT = os.path.join(BASE_DIR, "..", "decks", "Copilot_Squad_Runbook.pptx")
prs.save(OUTPUT)
print(f"Runbook deck saved: {OUTPUT}")
print(f"{TOTAL_SLIDES} slides generated")
