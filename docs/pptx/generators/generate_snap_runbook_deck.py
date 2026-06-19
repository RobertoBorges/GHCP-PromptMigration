"""
Generate PowerPoint: Copilot Squad + Snap Model Operations Runbook
15 slides -- practical step-by-step runbook for engineers and architects
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

TOTAL_SLIDES = 15

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
# SLIDE 1 -- TITLE (LATAM template layout 0)
# =====================================================================
s = prs.slides.add_slide(prs.slide_layouts[0])
for sp in list(s.placeholders):
    sp_elem = sp._element
    sp_elem.getparent().remove(sp_elem)

add_text(s, Inches(0.8), Inches(1.2), Inches(11), Inches(0.5),
         "Microsoft Accelerated Factory", font_size=18, color=WHITE,
         font_name="Segoe Sans Display Semibold")
add_text(s, Inches(0.8), Inches(2.0), Inches(11), Inches(1.2),
         "Snap Model Operations Runbook",
         font_size=50, color=WHITE, bold=True, font_name="Aptos Display")
add_text(s, Inches(0.8), Inches(3.5), Inches(11), Inches(0.6),
         "Central Squad + Snap Presets + SubSquads",
         font_size=24, color=RGBColor(0xCC, 0xE5, 0xFF), font_name="Aptos Display")
add_text(s, Inches(0.8), Inches(4.5), Inches(9), Inches(0.8),
         "Step-by-step guide for engineers and architects operating\nthe AI-driven delivery model at enterprise scale",
         font_size=14, color=RGBColor(0xB0, 0xD0, 0xF0))
add_text(s, Inches(0.8), Inches(6.0), Inches(6), Inches(0.7),
         "Audience: Engineers, Architects, Delivery Leads\nVersion 1.0  |  May 2026  |  Classification: Confidential",
         font_size=11, color=RGBColor(0x90, 0xB8, 0xE0))
add_footer(s, prs, 1, TOTAL_SLIDES)

add_notes(s,
    "WHAT TO SAY:\n"
    "This runbook is the operational guide for teams using the Snap Model inside the Accelerate "
    "Factory. It covers everything from Central Squad setup to SubSquad execution to continuous "
    "improvement. Follow it step by step when starting a new engagement.\n\n"
    "WHO IT'S FOR:\n"
    "Engineers implementing delivery, architects designing solutions, and delivery leads "
    "coordinating across SubSquads.\n\n"
    "KEY RULE:\n"
    "Reuse first. Always search the Central Squad library before creating anything new. "
    "The system gets smarter only when teams contribute improvements back.")

# =====================================================================
# SLIDE 2 -- TABLE OF CONTENTS
# =====================================================================
s = add_slide(prs); set_white_bg(s)
add_title_bar(s, prs, "Runbook Contents")

toc = [
    ("01", "Central Squad Setup", "Shared assets, naming, memory model", ACCENT2),
    ("02", "Snap Governance Model", "Publishing rules, security, approvals", ACCENT5),
    ("03", "Snap Lifecycle", "Create to retire -- 7 stages", ACCENT6),
    ("04", "SubSquad Creation", "Select, initialize, configure, execute", GREEN),
    ("05", "Agent Usage in Practice", "Switching agents, execution patterns", ACCENT3),
    ("06", "Creating New Agents", "When to create, how to keep generic", ACCENT1),
    ("07", "Publishing & Sharing", "Submit, validate, version, catalog", ACCENT2),
    ("08", "Agent to Skill Transformation", "Compounding knowledge over time", ACCENT5),
    ("09", "Accelerate Factory Mapping", "Agents at every phase", ACCENT6),
    ("10", "Reducing Manual Work", "Replace meetings with automation", GREEN),
    ("11", "SNAP Capability Model", "Request capabilities, not people", ACCENT3),
    ("12", "Governance & Security", "Data rules, audit, compliance", ACCENT1),
    ("13", "Continuous Improvement", "Capture, update, grow the library", ACCENT4),
]

for i, (num, title, desc, color) in enumerate(toc):
    col = i % 2
    row = i // 2
    left = Inches(0.5 + col * 6.3)
    top = Inches(1.1 + row * 0.78)
    add_icon_circle(s, left, top + Inches(0.02), 0.38, color, num, 10)
    add_text(s, left + Inches(0.5), top, Inches(5.5), Inches(0.28),
             title, font_size=13, color=color, bold=True)
    add_text(s, left + Inches(0.5), top + Inches(0.28), Inches(5.5), Inches(0.25),
             desc, font_size=9, color=SUBTITLE)

add_footer(s, prs, 2, TOTAL_SLIDES)

add_notes(s,
    "WHAT TO SAY:\n"
    "Thirteen sections. Each one is self-contained. You can follow them in order for a new "
    "engagement, or jump to the section you need.\n\n"
    "The first four sections -- Central Squad Setup, Snap Governance, Snap Lifecycle, and SubSquad "
    "Creation -- are the foundation. Start there.\n\n"
    "Sections 5-8 cover day-to-day agent operations. Sections 9-13 cover scaling, governance, "
    "and continuous improvement.")

# =====================================================================
# SLIDE 3 -- CENTRAL SQUAD SETUP
# =====================================================================
s = add_slide(prs); set_white_bg(s)
add_title_bar(s, prs, "01  Central Squad Setup")

add_text(s, Inches(0.5), Inches(1.0), Inches(12), Inches(0.35),
         "Central Squad is the control plane. It owns all shared assets, standards, and institutional memory.",
         font_size=13, color=SLATE)

# Four storage pillars
stores = [
    ("Agent Library", [
        ".squad/agents/<name>/charter.md",
        "Identity, role, expertise, boundaries",
        "Style guide per agent",
        "Cross-agent handoff rules",
    ], ACCENT2),
    ("Snap Presets", [
        ".squad/presets/<type>/",
        "Team composition definitions",
        "Routing rules per preset",
        "Memory templates (CLAUDE.md)",
    ], ACCENT5),
    ("Patterns & Templates", [
        "Bicep / Terraform modules",
        "CI/CD pipeline templates",
        "Test frameworks and fixtures",
        "Architecture decision records",
    ], ACCENT6),
    ("Shared Memory", [
        ".squad/decisions.md (active)",
        "JOURNAL.md (build history)",
        "Lessons learned per engagement",
        "Cross-team knowledge base",
    ], GREEN),
]

for i, (title, items, color) in enumerate(stores):
    left = Inches(0.4 + i * 3.15)
    top = Inches(1.55)
    add_colored_card(s, left, top, Inches(2.95), Inches(3.6), CARD_BG, color)
    add_rect_card(s, left, top, Inches(2.95), Inches(0.5), color)
    add_text(s, left + Inches(0.15), top + Inches(0.07), Inches(2.65), Inches(0.35),
             title, font_size=14, color=WHITE, bold=True)
    for j, item in enumerate(items):
        y = top + Inches(0.7 + j * 0.6)
        add_text(s, left + Inches(0.15), y, Inches(2.65), Inches(0.45),
                 f"  {item}", font_size=9, color=BODY_TEXT)

# Naming convention bar
add_colored_card(s, Inches(0.4), Inches(5.4), Inches(12.5), Inches(0.35), NAVY)
add_text(s, Inches(0.7), Inches(5.42), Inches(12), Inches(0.3),
         "Naming:  agent-<domain>-<capability>  |  snap-<type>-<version>  |  pattern-<stack>-<component>",
         font_size=10, color=WHITE, bold=True)

# Memory model
add_section_label(s, Inches(0.5), Inches(5.95), "SHARED MEMORY MODEL", color=ACCENT2, width=Inches(2.5))
mem = [
    "decisions.md = active design decisions (all teams reference)",
    "JOURNAL.md = engagement history (Scribe agent maintains)",
    "AGENTS.md = operating instructions (defines agent behavior)",
]
for i, m in enumerate(mem):
    add_text(s, Inches(0.7), Inches(6.25 + i * 0.07), Inches(12), Inches(0.25),
             f"  {m}", font_size=8, color=BODY_TEXT)

add_footer(s, prs, 3, TOTAL_SLIDES)

add_notes(s,
    "WHAT TO SAY:\n"
    "Before anything else, you need Central Squad set up. Four storage areas.\n\n"
    "Agent Library: all shared agent charters live here. Each agent has an identity, role, expertise "
    "boundaries, and handoff rules.\n\n"
    "Snap Presets: pre-built team configurations. Each preset defines which agents, what routing "
    "rules, and what memory templates a team uses.\n\n"
    "Patterns: reusable IaC templates, CI/CD pipelines, test frameworks. Not code -- patterns.\n\n"
    "Shared Memory: decisions.md tracks active design decisions. JOURNAL.md tracks build history. "
    "This is institutional memory that persists across engagements.\n\n"
    "PRACTICAL STEP:\n"
    "If Central Squad doesn't exist yet, create the repository structure. "
    "Start with the agent library and one Snap preset. Add patterns as they emerge from projects.")

# =====================================================================
# SLIDE 4 -- SNAP GOVERNANCE MODEL
# =====================================================================
s = add_slide(prs); set_white_bg(s)
add_title_bar(s, prs, "02  Snap Governance Model")

add_text(s, Inches(0.5), Inches(1.0), Inches(12), Inches(0.35),
         "Central Squad is the sole publisher of production Snap presets. SubSquads consume, they do not modify.",
         font_size=13, color=SLATE)

# Critical rule banner
add_colored_card(s, Inches(0.5), Inches(1.5), Inches(12), Inches(0.5), RGBColor(0xFF, 0xED, 0xED), RED)
add_text(s, Inches(0.8), Inches(1.55), Inches(11.4), Inches(0.4),
         "RULE: SubSquads CANNOT directly modify shared Snap presets. All changes go through Central Squad.",
         font_size=12, color=RED, bold=True)

# Governance rules in two columns
add_section_label(s, Inches(0.5), Inches(2.2), "PUBLISHING RULES", color=ACCENT2, width=Inches(2.0))
add_section_label(s, Inches(6.5), Inches(2.2), "UPDATE REQUIREMENTS", color=ACCENT5, width=Inches(2.3))

pub_rules = [
    "Only Central Squad architects can publish Snaps",
    "Every Snap must pass security review",
    "No client-specific data in any preset",
    "Documentation required: purpose, agents, routing",
    "At least 2 reviewer approvals on publish PR",
]

update_reqs = [
    "All Snap updates require version bump",
    "Breaking changes require major version (v2.0)",
    "Migration guide required for major versions",
    "Backward compatibility enforced for minor updates",
    "Automated validation pipeline must pass",
]

for i, rule in enumerate(pub_rules):
    add_text(s, Inches(0.7), Inches(2.65 + i * 0.5), Inches(5.5), Inches(0.4),
             f"  {rule}", font_size=10, color=BODY_TEXT)

for i, req in enumerate(update_reqs):
    add_text(s, Inches(6.7), Inches(2.65 + i * 0.5), Inches(5.5), Inches(0.4),
             f"  {req}", font_size=10, color=BODY_TEXT)

# Approval flow
add_section_label(s, Inches(0.5), Inches(5.25), "APPROVAL FLOW", color=GREEN, width=Inches(1.6))

flow_stages = [
    ("SubSquad\nSubmits PR", ACCENT3),
    ("Security\nScan", RED),
    ("Architect\nReview", ACCENT2),
    ("Peer\nReview", ACCENT5),
    ("Central\nPublishes", GREEN),
]

for i, (stage, color) in enumerate(flow_stages):
    left = Inches(0.5 + i * 2.5)
    add_colored_card(s, left, Inches(5.65), Inches(2.1), Inches(0.7), CARD_BG, color)
    add_multiline(s, left + Inches(0.15), Inches(5.68), Inches(1.8), Inches(0.6),
                  stage.split('\n'), font_size=9, color=color, bold=True)
    if i < 4:
        add_arrow(s, left + Inches(2.15), Inches(5.85), Inches(0.15), color)

add_footer(s, prs, 4, TOTAL_SLIDES)

add_notes(s,
    "WHAT TO SAY:\n"
    "Governance is what makes shared Snaps trustworthy. Here are the rules.\n\n"
    "Only Central Squad publishes production Snaps. SubSquads can propose changes through PRs, "
    "but they never modify shared presets directly.\n\n"
    "Every update goes through the approval flow at the bottom: SubSquad submits a PR, "
    "security scan runs automatically, an architect reviews, a peer reviews, "
    "and Central publishes with a version bump.\n\n"
    "PRACTICAL STEP:\n"
    "Set up a CI pipeline on the Central Squad repo that runs security scans automatically "
    "on every PR. The scan should check for hardcoded credentials, client identifiers, "
    "and PII in all agent charters and Snap configurations.")

# =====================================================================
# SLIDE 5 -- SNAP LIFECYCLE
# =====================================================================
s = add_slide(prs); set_white_bg(s)
add_title_bar(s, prs, "03  Snap Lifecycle")

add_text(s, Inches(0.5), Inches(1.0), Inches(12), Inches(0.35),
         "Every Snap preset follows a structured lifecycle from creation through retirement.",
         font_size=13, color=SLATE)

lifecycle = [
    ("CREATE", "Define team comp,\nagents, routing,\nmemory templates", ACCENT2),
    ("VALIDATE", "Test with sample\nproject. Verify\nall agents work", ACCENT5),
    ("PUBLISH", "Add to Central\nlibrary. Document\nuse cases", ACCENT3),
    ("REUSE", "SubSquads pull\npreset. Configure\nfor engagement", GREEN),
    ("IMPROVE", "Teams submit\nenhancements\nback via PR", ACCENT6),
    ("VERSION", "Semantic version.\nChangelog. Backward\ncompat check", ACCENT1),
    ("RETIRE", "Sunset when\nreplaced by better\nconfiguration", SLATE),
]

for i, (stage, desc, color) in enumerate(lifecycle):
    left = Inches(0.2 + i * 1.82)
    add_colored_card(s, left, Inches(1.55), Inches(1.65), Inches(2.8), CARD_BG, color)
    add_icon_circle(s, left + Inches(0.5), Inches(1.7), 0.5, color, str(i+1), 14)
    add_text(s, left + Inches(0.05), Inches(2.35), Inches(1.55), Inches(0.25),
             stage, font_size=11, color=color, bold=True, alignment=PP_ALIGN.CENTER)
    add_multiline(s, left + Inches(0.05), Inches(2.7), Inches(1.55), Inches(1.2),
                  desc.split('\n'), font_size=9, color=BODY_TEXT)
    if i < 6:
        add_arrow(s, left + Inches(1.68), Inches(1.95), Inches(0.1), color)

# Key rules
add_section_label(s, Inches(0.5), Inches(4.6), "LIFECYCLE RULES", color=ACCENT2, width=Inches(1.8))

rules = [
    ("Validation gate", "A Snap cannot be published without passing isolation tests on a sample project"),
    ("Deprecation path", "Mark deprecated Snaps with a sunset date. Provide migration instructions."),
    ("Version policy", "MAJOR = breaking changes, MINOR = new agents added, PATCH = bug fixes"),
    ("Retirement criteria", "Zero active SubSquads using the preset for 90+ days = eligible for retirement"),
]

for i, (rule, desc) in enumerate(rules):
    col = i % 2
    row = i // 2
    left = Inches(0.5 + col * 6.3)
    top = Inches(5.0 + row * 0.5)
    add_text(s, left, top, Inches(2.0), Inches(0.25),
             rule, font_size=10, color=ACCENT2, bold=True)
    add_text(s, left + Inches(2.1), top, Inches(4.0), Inches(0.4),
             desc, font_size=9, color=BODY_TEXT)

add_footer(s, prs, 5, TOTAL_SLIDES)

add_notes(s,
    "WHAT TO SAY:\n"
    "Seven stages. Every Snap goes through all of them.\n\n"
    "Create: define the team composition -- which agents, what routing rules, what memory templates. "
    "Validate: test it against a real (or simulated) project. Publish: add it to the Central library. "
    "Reuse: SubSquads pull it. Improve: teams submit enhancements. Version: track changes semantically. "
    "Retire: sunset when it's been replaced.\n\n"
    "The validation gate is critical. A Snap that hasn't been tested against a sample project "
    "cannot be published. We've seen teams skip this and publish broken presets that wasted days.\n\n"
    "PRACTICAL STEP:\n"
    "When creating a new Snap preset, always test it by running:\n"
    "  npx snap-squad-emu init --type <your-preset>\n"
    "Then verify: are all agents present? Do routing rules work? Does CLAUDE.md initialize correctly?")

# =====================================================================
# SLIDE 6 -- SUBSQUAD CREATION AND EXECUTION
# =====================================================================
s = add_slide(prs); set_white_bg(s)
add_title_bar(s, prs, "04  SubSquad Creation and Execution")

add_text(s, Inches(0.5), Inches(1.0), Inches(12), Inches(0.35),
         "Four steps to go from zero to executing. Follow them in order for every new engagement.",
         font_size=13, color=SLATE)

steps = [
    ("1", "SELECT SNAP", "Choose preset based on project type",
     ["Assess project requirements (backend, AI, migration, etc.)",
      "Browse Central Squad Snap catalog",
      "Match project needs to available presets",
      "If no preset fits: request new Snap from Central Squad"], ACCENT2),
    ("2", "INITIALIZE", "Run the command, get a full team",
     ["npx snap-squad-emu init --type <preset>",
      "Creates .squad/ directory with all agent charters",
      "Sets up routing.md, team.md, decisions.md",
      "Populates AGENTS.md and CLAUDE.md"], ACCENT5),
    ("3", "REVIEW & CONFIGURE", "Verify agents, add project context",
     ["Review generated agents and routing rules",
      "Update CLAUDE.md with: project owner, stack, description",
      "Set project-specific environment variables",
      "DO NOT modify agent charters or shared logic"], ACCENT6),
    ("4", "EXECUTE", "Start delivery using the squad",
     ["Agents handle: design, code, test, docs, deploy",
      "Work is routed automatically based on routing.md",
      "Human validates decisions before changes land",
      "At engagement end: submit improvements to Central"], GREEN),
]

for i, (num, title, subtitle, items, color) in enumerate(steps):
    left = Inches(0.35 + i * 3.15)
    add_colored_card(s, left, Inches(1.55), Inches(2.95), Inches(4.7), CARD_BG, color)
    add_icon_circle(s, left + Inches(1.1), Inches(1.7), 0.55, color, num, 18)
    add_text(s, left + Inches(0.1), Inches(2.4), Inches(2.75), Inches(0.3),
             title, font_size=13, color=color, bold=True, alignment=PP_ALIGN.CENTER)
    add_text(s, left + Inches(0.1), Inches(2.7), Inches(2.75), Inches(0.3),
             subtitle, font_size=9, color=SLATE, alignment=PP_ALIGN.CENTER)
    for j, item in enumerate(items):
        y = Inches(3.15 + j * 0.7)
        add_text(s, left + Inches(0.1), y, Inches(2.75), Inches(0.55),
                 f"  {item}", font_size=8, color=BODY_TEXT)

add_footer(s, prs, 6, TOTAL_SLIDES)

add_notes(s,
    "WHAT TO SAY:\n"
    "This is the core execution flow. Four steps, every engagement.\n\n"
    "Step 1: Select the right Snap preset. Don't guess -- check the catalog. If your project "
    "is a backend API, use the 'default' preset. If it's a quick prototype, use 'fast.'\n\n"
    "Step 2: Initialize. One command creates the entire squad structure. Agents, routing, memory -- "
    "all generated from the preset.\n\n"
    "Step 3: Review and configure. This is where you add project-specific context. Update CLAUDE.md "
    "with your project details. Set environment variables. But do NOT modify the agent charters. "
    "That's shared logic owned by Central Squad.\n\n"
    "Step 4: Execute. The agents handle the work. Routing rules dispatch tasks automatically. "
    "You validate decisions before they land. At the end, submit improvements back.\n\n"
    "CRITICAL:\n"
    "Step 3 is where most teams make mistakes. They modify the agent charters instead of using "
    "configuration. If you change the charter, your improvements can't flow back to Central, "
    "and you've forked from the shared standard.")

# =====================================================================
# SLIDE 7 -- AGENT USAGE IN PRACTICE
# =====================================================================
s = add_slide(prs); set_white_bg(s)
add_title_bar(s, prs, "05  Agent Usage in Practice")

add_text(s, Inches(0.5), Inches(1.0), Inches(12), Inches(0.35),
         "Agents live in the repo. Teams switch agents based on the task. Routing happens automatically.",
         font_size=13, color=SLATE)

# Repo structure
add_section_label(s, Inches(0.5), Inches(1.5), "REPO STRUCTURE", color=ACCENT5, width=Inches(1.8))

repo_files = [
    ("AGENTS.md", "Operating instructions for all agents"),
    ("CLAUDE.md", "Session memory and project context"),
    (".squad/team.md", "Team roster and metadata"),
    (".squad/routing.md", "Work type --> agent mapping"),
    (".squad/decisions.md", "Active design decisions"),
    (".squad/agents/<name>/charter.md", "Individual agent identity"),
]

for i, (f, desc) in enumerate(repo_files):
    y = Inches(1.9 + i * 0.32)
    add_text(s, Inches(0.7), y, Inches(4.0), Inches(0.25),
             f, font_size=10, color=ACCENT5, bold=True)
    add_text(s, Inches(4.8), y, Inches(3.0), Inches(0.25),
             desc, font_size=10, color=BODY_TEXT)

# Agent execution domains
add_section_label(s, Inches(6.5), Inches(1.5), "AGENT EXECUTION DOMAINS", color=ACCENT2, width=Inches(2.8))

domains = [
    ("Architect", "System design, scope, ADRs", ACCENT2),
    ("Coder", "Implementation, debugging", ACCENT5),
    ("Tester", "QA, edge cases, test suites", GREEN),
    ("DevRel", "Docs, README, onboarding", ACCENT6),
    ("GitOps", "CI/CD, releases, git workflow", ACCENT3),
    ("Evaluator", "Quality baselines, evals", ACCENT4),
]

for i, (name, domain, color) in enumerate(domains):
    y = Inches(1.9 + i * 0.35)
    add_text(s, Inches(6.7), y, Inches(1.2), Inches(0.25),
             name, font_size=10, color=color, bold=True)
    add_text(s, Inches(8.0), y, Inches(4.5), Inches(0.25),
             domain, font_size=10, color=BODY_TEXT)

# Routing example
add_section_label(s, Inches(0.5), Inches(4.2), "ROUTING IN ACTION", color=GREEN, width=Inches(2.0))

routing = [
    ("Code change submitted", "Coder leads implementation, Tester validates"),
    ("Architecture question", "Architect leads decision, logs to decisions.md"),
    ("Documentation needed", "DevRel generates docs, Scribe records in JOURNAL.md"),
    ("Release preparation", "GitOps manages pipeline, Evaluator checks quality gates"),
]

for i, (trigger, action) in enumerate(routing):
    y = Inches(4.65 + i * 0.42)
    add_text(s, Inches(0.7), y, Inches(3.5), Inches(0.3),
             trigger, font_size=10, color=ACCENT2, bold=True)
    add_arrow(s, Inches(4.3), y + Inches(0.02), Inches(0.2), ACCENT2)
    add_text(s, Inches(4.7), y, Inches(7.8), Inches(0.3),
             action, font_size=10, color=BODY_TEXT)

# Human in the loop
add_colored_card(s, Inches(0.5), Inches(6.4), Inches(12), Inches(0.0), ACCENT2)
add_colored_card(s, Inches(0.5), Inches(6.1), Inches(12), Inches(0.3), LIGHT_BG, ACCENT2)
add_text(s, Inches(0.8), Inches(6.12), Inches(11.4), Inches(0.25),
         "Human-in-the-loop: All agent outputs require human validation before landing in production.",
         font_size=10, color=ACCENT2, bold=True)

add_footer(s, prs, 7, TOTAL_SLIDES)

add_notes(s,
    "WHAT TO SAY:\n"
    "Agents aren't magic. They live in the repo, and they follow rules.\n\n"
    "Left side: the repo structure. Every squad has these files. AGENTS.md defines how agents "
    "behave. CLAUDE.md carries project context. Routing.md maps work types to agents.\n\n"
    "Right side: the execution domains. Each agent has a clear lane. Architect handles design. "
    "Coder handles implementation. Tester handles QA. No overlap, no confusion.\n\n"
    "Bottom: routing in action. When a code change is submitted, routing.md automatically "
    "dispatches Coder to lead and Tester to validate. No human needs to assign work.\n\n"
    "CRITICAL:\n"
    "Human-in-the-loop is non-negotiable. Agents propose, humans approve. "
    "No agent output goes to production without a human reviewing it first.")

# =====================================================================
# SLIDE 8 -- CREATING NEW AGENTS + PUBLISHING
# =====================================================================
s = add_slide(prs); set_white_bg(s)
add_title_bar(s, prs, "06-07  Creating & Publishing Agents")

# Decision: Reuse vs Create
add_section_label(s, Inches(0.5), Inches(1.0), "DECISION: REUSE OR CREATE?", color=ACCENT2, width=Inches(3.5))

add_colored_card(s, Inches(0.5), Inches(1.45), Inches(5.8), Inches(2.0), RGBColor(0xE8, 0xF5, 0xE9), GREEN)
add_text(s, Inches(0.7), Inches(1.5), Inches(5.4), Inches(0.3),
         "REUSE (Default -- always try this first)", font_size=13, color=GREEN, bold=True)
reuse_when = [
    "Similar agent exists in Central (>= 80% capability match)",
    "Gap can be bridged with configuration changes only",
    "Another team has solved a similar problem before",
]
for j, item in enumerate(reuse_when):
    add_text(s, Inches(0.9), Inches(1.9 + j * 0.4), Inches(5.2), Inches(0.3),
             f"  {item}", font_size=10, color=BODY_TEXT)

add_colored_card(s, Inches(6.7), Inches(1.45), Inches(5.8), Inches(2.0), RGBColor(0xFF, 0xF3, 0xE0), ACCENT3)
add_text(s, Inches(6.9), Inches(1.5), Inches(5.4), Inches(0.3),
         "CREATE NEW (Exception -- architect approval required)", font_size=13, color=ACCENT3, bold=True)
create_when = [
    "No agent with overlapping capability exists",
    "Domain is entirely new to the organization",
    "Central Squad architect approves the creation",
]
for j, item in enumerate(create_when):
    add_text(s, Inches(7.1), Inches(1.9 + j * 0.4), Inches(5.2), Inches(0.3),
             f"  {item}", font_size=10, color=BODY_TEXT)

# Creating checklist
add_section_label(s, Inches(0.5), Inches(3.7), "CREATING A NEW AGENT", color=ACCENT5, width=Inches(2.5))

create_steps = [
    ("1", "Write charter", "Define identity, role, expertise, style, and boundaries in charter.md", ACCENT2),
    ("2", "Keep generic", "No client names, project IDs, or sensitive data. Use template variables", ACCENT5),
    ("3", "Test isolation", "Verify agent works with zero project context. Must be fully portable", ACCENT6),
    ("4", "Document", "Purpose, inputs, outputs, usage examples, limitations", GREEN),
]

for i, (num, title, desc, color) in enumerate(create_steps):
    y = Inches(4.1 + i * 0.38)
    add_icon_circle(s, Inches(0.6), y, 0.25, color, num, 9)
    add_text(s, Inches(1.0), y, Inches(1.5), Inches(0.25),
             title, font_size=10, color=color, bold=True)
    add_text(s, Inches(2.6), y, Inches(9.8), Inches(0.25),
             desc, font_size=10, color=BODY_TEXT)

# Publishing pipeline
add_section_label(s, Inches(0.5), Inches(5.7), "PUBLISHING TO CENTRAL", color=ACCENT1, width=Inches(2.3))

pub = [
    ("Submit PR", ACCENT3), ("Security scan", RED), ("Peer review", ACCENT5),
    ("Architect approval", ACCENT2), ("Version + publish", GREEN),
]

for i, (stage, color) in enumerate(pub):
    left = Inches(0.5 + i * 2.5)
    add_colored_card(s, left, Inches(6.05), Inches(2.1), Inches(0.35), color)
    add_text(s, left + Inches(0.1), Inches(6.07), Inches(1.9), Inches(0.25),
             stage, font_size=9, color=WHITE, bold=True, alignment=PP_ALIGN.CENTER)
    if i < 4:
        add_arrow(s, left + Inches(2.15), Inches(6.1), Inches(0.12), color)

add_footer(s, prs, 8, TOTAL_SLIDES)

add_notes(s,
    "WHAT TO SAY:\n"
    "Two sections combined: when to create agents, and how to publish them.\n\n"
    "The decision tree is simple. Green path: reuse. This is the default. If an agent exists "
    "that covers 80% of your need, use it and configure the rest. Orange path: create new. "
    "This requires architect approval because it means we're adding to the shared library.\n\n"
    "When creating, the four-step checklist is mandatory: write the charter, keep it generic, "
    "test in isolation, and document everything.\n\n"
    "Publishing goes through a five-stage pipeline. The security scan is automated -- it checks "
    "for credentials, PII, and client-specific data. If it fails, the PR is blocked.\n\n"
    "PRACTICAL STEP:\n"
    "Before creating a new agent, run: 'npx snap-squad list' to see what already exists. "
    "If you find something close, open a PR to improve it instead of creating a duplicate.")

# =====================================================================
# SLIDE 9 -- AGENT TO SKILL TRANSFORMATION
# =====================================================================
s = add_slide(prs); set_white_bg(s)
add_title_bar(s, prs, "08  Agent to Skill Transformation")

add_text(s, Inches(0.5), Inches(1.0), Inches(12), Inches(0.35),
         "Agents compound into organizational skills. Every engagement makes the system smarter.",
         font_size=13, color=SLATE)

# Three skill types
skill_types = [
    ("Agents = Capabilities", "Reusable execution engines\nthat handle specific domains\nautonomously", [
        "Coder: writes and debugs code",
        "Tester: finds edge cases",
        "GitOps: manages CI/CD",
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
        "Onboarding documentation",
    ], ACCENT6),
]

for i, (title, desc, items, color) in enumerate(skill_types):
    left = Inches(0.5 + i * 4.1)
    add_colored_card(s, left, Inches(1.55), Inches(3.8), Inches(3.3), CARD_BG, color)
    add_rect_card(s, left, Inches(1.55), Inches(3.8), Inches(0.5), color)
    add_text(s, left + Inches(0.15), Inches(1.62), Inches(3.5), Inches(0.35),
             title, font_size=13, color=WHITE, bold=True)
    add_multiline(s, left + Inches(0.15), Inches(2.2), Inches(3.5), Inches(0.8),
                  desc.split('\n'), font_size=10, color=BODY_TEXT)
    for j, item in enumerate(items):
        y = Inches(3.05 + j * 0.38)
        add_text(s, left + Inches(0.15), y, Inches(3.5), Inches(0.3),
                 f"  {item}", font_size=9, color=BODY_TEXT)

# Compounding loop
add_colored_card(s, Inches(0.5), Inches(5.1), Inches(12), Inches(1.0), NAVY)
add_text(s, Inches(0.8), Inches(5.15), Inches(11.4), Inches(0.3),
         "THE COMPOUNDING LOOP", font_size=12, color=ACCENT4, bold=True)

loop_stages = ["USE", "IMPROVE", "SHARE", "REUSE", "SCALE"]
loop_colors = [ACCENT2, GREEN, ACCENT5, ACCENT3, ACCENT4]
for i, (stage, lc) in enumerate(zip(loop_stages, loop_colors)):
    x = Inches(1.0 + i * 2.3)
    add_icon_circle(s, x, Inches(5.55), 0.4, lc, stage, 9)
    if i < 4:
        add_arrow(s, x + Inches(0.5), Inches(5.65), Inches(0.3), lc)

add_text(s, Inches(0.8), Inches(6.05), Inches(11.4), Inches(0.25),
         "Every engagement adds to the system. Skills compound, they don't decay. The 10th project is faster than the 1st.",
         font_size=10, color=WHITE)

add_footer(s, prs, 9, TOTAL_SLIDES)

add_notes(s,
    "WHAT TO SAY:\n"
    "This is how individual agents become organizational skills.\n\n"
    "Three categories. Agents are capabilities -- they do work. Prompts are thinking -- they "
    "encode how we make decisions. Outputs are templates -- they eliminate blank pages.\n\n"
    "The compounding loop at the bottom: Use agents in real engagements. Improve them when you "
    "find gaps. Share improvements back to Central. Central makes them available for Reuse. "
    "More teams adopt, which Scales the system.\n\n"
    "KEY INSIGHT:\n"
    "In the old model, engagement 10 was exactly as hard as engagement 1. In this model, "
    "engagement 10 is dramatically easier because 9 previous teams contributed improvements. "
    "That's compounding.")

# =====================================================================
# SLIDE 10 -- ACCELERATE FACTORY MAPPING
# =====================================================================
s = add_slide(prs); set_white_bg(s)
add_title_bar(s, prs, "09  Mapping to Accelerate Factory Phases")

add_text(s, Inches(0.5), Inches(1.0), Inches(12), Inches(0.35),
         "Every Factory phase has agent support. No phase starts from scratch. No phase is fully manual.",
         font_size=13, color=SLATE)

phases = [
    ("INTAKE", [
        "Researcher scans requirements",
        "Architect generates scope doc",
        "Auto-identify reusable assets",
        "Select Snap preset for team",
    ], "Output: Scope doc,\nasset map, Snap selection", ACCENT2),
    ("DESIGN", [
        "Architect produces ADRs",
        "Prompter configures agents",
        "IaC templates from library",
        "Security patterns applied",
    ], "Output: Architecture docs,\nIaC plan, agent roster", ACCENT5),
    ("BUILD", [
        "Coder implements features",
        "Tester validates in parallel",
        "SubSquads execute independently",
        "Shared agents = consistency",
    ], "Output: Working code,\ntest suites, CI pipeline", ACCENT3),
    ("DEPLOY", [
        "GitOps manages pipeline",
        "IaC deploys (zero portal)",
        "Evaluator checks quality",
        "Zero manual deploy steps",
    ], "Output: Deployed infra,\nvalidation report", GREEN),
    ("HANDOVER", [
        "DevRel generates all docs",
        "Scribe writes journal",
        "Improvements to Central",
        "Runbook auto-generated",
    ], "Output: Docs, runbook,\nCentral contributions", ACCENT6),
]

for i, (phase, items, output, color) in enumerate(phases):
    left = Inches(0.3 + i * 2.55)
    top = Inches(1.55)
    add_colored_card(s, left, top, Inches(2.3), Inches(4.7), CARD_BG, color)
    add_rect_card(s, left, top, Inches(2.3), Inches(0.5), color)
    add_text(s, left + Inches(0.1), top + Inches(0.07), Inches(2.1), Inches(0.35),
             phase, font_size=14, color=WHITE, bold=True, alignment=PP_ALIGN.CENTER)
    add_section_label(s, left + Inches(0.1), top + Inches(0.6), "AGENT ACTIONS", color=SLATE, width=Inches(1.4))
    for j, item in enumerate(items):
        y = top + Inches(0.95 + j * 0.55)
        add_text(s, left + Inches(0.1), y, Inches(2.1), Inches(0.45),
                 f"  {item}", font_size=9, color=BODY_TEXT)
    add_section_label(s, left + Inches(0.1), top + Inches(3.25), "OUTPUT", color=color, width=Inches(0.9))
    add_multiline(s, left + Inches(0.1), top + Inches(3.6), Inches(2.1), Inches(0.8),
                  output.split('\n'), font_size=9, color=SLATE)
    if i < 4:
        add_arrow(s, left + Inches(2.35), top + Inches(0.15), Inches(0.15), color)

add_footer(s, prs, 10, TOTAL_SLIDES)

add_notes(s,
    "WHAT TO SAY:\n"
    "Here's how agents map to the Accelerate Factory phases.\n\n"
    "Intake: agents scan requirements and auto-select the right Snap preset. No manual setup.\n"
    "Design: architecture decision records are generated, IaC templates are pulled from the library.\n"
    "Build: SubSquads execute in parallel using shared agents. Consistency is automatic.\n"
    "Deploy: IaC-first. No portal clicks. Zero manual deployment steps.\n"
    "Handover: documentation and runbooks are auto-generated. Improvements flow back to Central.\n\n"
    "PRACTICAL STEP:\n"
    "At the start of every engagement, use this slide as a checklist. At each phase, verify "
    "that the relevant agents are active and the expected outputs are being generated.")

# =====================================================================
# SLIDE 11 -- REDUCING MANUAL WORK + SNAP CAPABILITY MODEL
# =====================================================================
s = add_slide(prs); set_white_bg(s)
add_title_bar(s, prs, "10-11  Reducing Manual Work + SNAP Capabilities")

# Left: meeting replacement
add_section_label(s, Inches(0.3), Inches(1.0), "REPLACE THIS...", color=RED, width=Inches(1.8))
add_section_label(s, Inches(6.5), Inches(1.0), "...WITH THIS", color=GREEN, width=Inches(1.5))

replacements = [
    ("Daily standup meetings", "Agent-generated status from git activity"),
    ("Weekly status reports", "Automated summary from Scribe (JOURNAL.md)"),
    ("Architecture reviews", "Architect agent generates ADRs, async PR review"),
    ("Manual coordination", "Routing rules auto-dispatch to right agent"),
    ("Knowledge transfer", "DevRel generates onboarding docs automatically"),
]

# Divider line
shape = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(6.2), Inches(1.0), Inches(0.03), Inches(3.8))
shape.fill.solid(); shape.fill.fore_color.rgb = BORDER_GRAY; shape.line.fill.background()

for i, (before, after) in enumerate(replacements):
    y = Inches(1.45 + i * 0.55)
    add_text(s, Inches(0.5), y, Inches(0.2), Inches(0.2), "X", font_size=10, color=RED, bold=True)
    add_text(s, Inches(0.8), y, Inches(5.0), Inches(0.4), before, font_size=10, color=BODY_TEXT)
    add_text(s, Inches(6.7), y, Inches(0.2), Inches(0.2), ">", font_size=10, color=GREEN, bold=True)
    add_text(s, Inches(7.0), y, Inches(5.5), Inches(0.4), after, font_size=10, color=BODY_TEXT)

# SNAP capability model
add_section_label(s, Inches(0.3), Inches(4.3), "SNAP CAPABILITY MODEL", color=ACCENT5, width=Inches(2.5))
add_text(s, Inches(0.3), Inches(4.7), Inches(6.0), Inches(0.3),
         "Teams request capabilities, not people. Snap provides agents per capability.",
         font_size=11, color=SLATE)

capabilities = [
    ("Backend", "API design, server logic", ACCENT2),
    ("IaC", "Bicep, Terraform, azd", ACCENT5),
    ("QA", "Test strategy, automation", GREEN),
    ("AI / ML", "Model integration, prompts", ACCENT6),
    ("DevOps", "CI/CD, pipelines, releases", ACCENT3),
    ("Security", "Compliance, scanning", ACCENT1),
]

for i, (cap, desc, color) in enumerate(capabilities):
    col = i % 3
    row = i // 3
    left = Inches(0.3 + col * 4.2)
    top = Inches(5.1 + row * 0.55)
    add_icon_circle(s, left, top + Inches(0.02), 0.3, color, cap[0], 10)
    add_text(s, left + Inches(0.4), top, Inches(1.2), Inches(0.25),
             cap, font_size=10, color=color, bold=True)
    add_text(s, left + Inches(1.7), top, Inches(2.3), Inches(0.4),
             desc, font_size=9, color=BODY_TEXT)

add_footer(s, prs, 11, TOTAL_SLIDES)

add_notes(s,
    "WHAT TO SAY:\n"
    "Two related topics: reducing manual work and the SNAP capability model.\n\n"
    "Top half: five types of meetings we replace. Daily standups become agent-generated dashboards. "
    "Weekly reports become automated summaries. Architecture reviews become async PR workflows. "
    "Result: approximately 60% fewer recurring meetings.\n\n"
    "Bottom half: the SNAP capability model. Instead of asking 'who has IaC experience?', "
    "the team requests the IaC capability. The Snap preset provides the right agents. "
    "No reorgs, no people shuffling -- just attach the capability and go.\n\n"
    "PRACTICAL STEP:\n"
    "For your next engagement, identify your top 3 recurring meetings. For each one, "
    "define which agent output would replace it. Then eliminate the meeting.")

# =====================================================================
# SLIDE 12 -- GOVERNANCE & SECURITY
# =====================================================================
s = add_slide(prs); set_white_bg(s)
add_title_bar(s, prs, "12  Governance & Security")

# Critical rule
add_colored_card(s, Inches(0.5), Inches(1.0), Inches(12), Inches(0.5), RGBColor(0xFF, 0xED, 0xED), RED)
add_text(s, Inches(0.8), Inches(1.05), Inches(11.4), Inches(0.4),
         "NON-NEGOTIABLE: No client-specific or sensitive data in shared agents, Snap presets, or templates.",
         font_size=12, color=RED, bold=True)

# Three governance pillars
pillars = [
    ("Agent Security", [
        "Security scan before every publish",
        "No secrets, credentials, or PII",
        "Isolation test (zero-context run)",
        "Architect approval required",
    ], ACCENT2),
    ("Data Protection", [
        "Client data stays in SubSquad ONLY",
        "Shared agents use template variables",
        "Environment vars for all secrets",
        "Audit trail on every change",
    ], ACCENT5),
    ("Operational Control", [
        "Version control for all assets",
        "PR-based publish workflow",
        "Automated compliance pipeline",
        "Regular catalog cleanup (90-day)",
    ], ACCENT6),
]

for i, (title, items, color) in enumerate(pillars):
    left = Inches(0.4 + i * 4.15)
    add_colored_card(s, left, Inches(1.7), Inches(3.85), Inches(3.1), CARD_BG, color)
    add_rect_card(s, left, Inches(1.7), Inches(3.85), Inches(0.5), color)
    add_text(s, left + Inches(0.15), Inches(1.77), Inches(3.55), Inches(0.35),
             title, font_size=14, color=WHITE, bold=True)
    for j, item in enumerate(items):
        y = Inches(2.35 + j * 0.5)
        add_text(s, left + Inches(0.15), y, Inches(3.55), Inches(0.4),
                 f"  {item}", font_size=10, color=BODY_TEXT)

# Audit trail
add_section_label(s, Inches(0.5), Inches(5.1), "AUDIT TRAIL", color=GREEN, width=Inches(1.5))

audit = [
    ("Repo changes", "Every modification tracked in git history"),
    ("Pull requests", "All publish actions require reviewed PRs"),
    ("Approvals", "Architect + peer sign-off logged per change"),
    ("Automated scans", "Security pipeline results stored per commit"),
]

for i, (item, desc) in enumerate(audit):
    col = i % 2
    row = i // 2
    left = Inches(0.5 + col * 6.3)
    top = Inches(5.5 + row * 0.4)
    add_text(s, left, top, Inches(1.6), Inches(0.25),
             item, font_size=10, color=GREEN, bold=True)
    add_text(s, left + Inches(1.7), top, Inches(4.4), Inches(0.25),
             desc, font_size=10, color=BODY_TEXT)

add_footer(s, prs, 12, TOTAL_SLIDES)

add_notes(s,
    "WHAT TO SAY:\n"
    "Governance is what makes this model trustworthy at enterprise scale.\n\n"
    "The red banner: no client data in shared assets. Ever. This is the one rule that, "
    "if violated, breaks the entire model.\n\n"
    "Three pillars. Agent Security: every agent passes automated scans and isolation tests. "
    "Data Protection: client data never leaves the SubSquad boundary. "
    "Operational Control: everything is versioned, PR-based, and auditable.\n\n"
    "The audit trail at the bottom shows how we maintain traceability: git history, PRs, "
    "approvals, and automated scan results. If anyone asks 'who approved this agent?', "
    "the answer is always in the PR history.\n\n"
    "PRACTICAL STEP:\n"
    "Set up a GitHub Actions workflow on the Central Squad repo that runs on every PR:\n"
    "1. Scan all .md files for patterns like subscription IDs, tenant IDs, email addresses\n"
    "2. Verify no hardcoded credentials exist\n"
    "3. Block merge if any check fails")

# =====================================================================
# SLIDE 13 -- CONTINUOUS IMPROVEMENT
# =====================================================================
s = add_slide(prs); set_white_bg(s)
add_title_bar(s, prs, "13  Continuous Improvement")

add_text(s, Inches(0.5), Inches(1.0), Inches(12), Inches(0.35),
         "The system gets smarter with every engagement. Here's how to make that happen systematically.",
         font_size=13, color=SLATE)

cycle = [
    ("CAPTURE", "During Engagement", [
        "Log decisions in decisions.md",
        "Record lessons in JOURNAL.md",
        "Note agent gaps / workarounds",
        "Track what worked and what didn't",
    ], ACCENT2),
    ("UPDATE", "Post-Engagement", [
        "Submit PRs for agent improvements",
        "Update prompts with new patterns",
        "Add new IaC / code templates",
        "Refine Snap routing rules",
    ], ACCENT5),
    ("VALIDATE", "Central Review", [
        "Architect reviews contributions",
        "Security scan on all changes",
        "Isolation test (no client data)",
        "Version and publish updates",
    ], GREEN),
    ("DISTRIBUTE", "All Teams Benefit", [
        "Updated agents available to all",
        "New patterns in shared library",
        "Improved Snaps for new projects",
        "Catalog reflects latest versions",
    ], ACCENT6),
]

for i, (stage, timing, items, color) in enumerate(cycle):
    left = Inches(0.4 + i * 3.15)
    top = Inches(1.55)
    add_colored_card(s, left, top, Inches(2.95), Inches(3.6), CARD_BG, color)
    add_rect_card(s, left, top, Inches(2.95), Inches(0.65), color)
    add_text(s, left + Inches(0.1), top + Inches(0.03), Inches(2.75), Inches(0.3),
             stage, font_size=14, color=WHITE, bold=True)
    add_text(s, left + Inches(0.1), top + Inches(0.32), Inches(2.75), Inches(0.25),
             timing, font_size=10, color=RGBColor(0xCC, 0xDD, 0xFF))
    for j, item in enumerate(items):
        y = top + Inches(0.85 + j * 0.55)
        add_text(s, left + Inches(0.1), y, Inches(2.75), Inches(0.45),
                 f"  {item}", font_size=10, color=BODY_TEXT)
    if i < 3:
        add_arrow(s, left + Inches(3.0), top + Inches(0.2), Inches(0.15), color)

# Anti-patterns
add_section_label(s, Inches(0.5), Inches(5.4), "ANTI-PATTERNS TO AVOID", color=RED, width=Inches(2.3))

anti = [
    ("Rebuilding from scratch", "Always check Central first. If it exists, improve it."),
    ("Hoarding improvements", "Improvements in SubSquads die with the project. Share them."),
    ("Embedding client data", "Shared agents must be 100% generic. Use config for specifics."),
    ("Skipping documentation", "Undocumented improvements are invisible. Document everything."),
]

for i, (pattern, fix) in enumerate(anti):
    col = i % 2
    row = i // 2
    left = Inches(0.5 + col * 6.3)
    top = Inches(5.8 + row * 0.35)
    add_text(s, left, top, Inches(2.2), Inches(0.25),
             f"X  {pattern}", font_size=9, color=RED, bold=True)
    add_text(s, left + Inches(2.3), top, Inches(3.8), Inches(0.25),
             fix, font_size=9, color=BODY_TEXT)

add_footer(s, prs, 13, TOTAL_SLIDES)

add_notes(s,
    "WHAT TO SAY:\n"
    "Continuous improvement is how the flywheel keeps spinning.\n\n"
    "Four stages, tied to the engagement lifecycle. During the engagement: capture decisions and "
    "lessons in real time. After the engagement: submit PRs with improvements. Central reviews "
    "and validates. Then distributes updated agents to all teams.\n\n"
    "At the bottom: the four anti-patterns that kill improvement. Rebuilding from scratch, "
    "hoarding improvements, embedding client data, and skipping documentation. "
    "These are the behaviors we need to change.\n\n"
    "PRACTICAL STEP:\n"
    "At engagement kickoff, add a standing item to your process: 'What improvements will we "
    "contribute back to Central?' Don't wait until the end. Identify improvements as you go.")

# =====================================================================
# SLIDE 14 -- QUICK REFERENCE CARD
# =====================================================================
s = add_slide(prs); set_white_bg(s)
add_title_bar(s, prs, "Quick Reference Card")

# Commands
add_section_label(s, Inches(0.5), Inches(1.0), "ESSENTIAL COMMANDS", color=ACCENT2, width=Inches(2.3))

commands = [
    ("npx snap-squad-emu list", "See available Snap presets and agents"),
    ("npx snap-squad-emu init --type <preset>", "Initialize SubSquad with preset"),
    ("npx snap-squad-emu init --type <preset> --force", "Reset or switch preset"),
    ("cat .squad/team.md", "View current team roster"),
    ("cat .squad/routing.md", "View work routing rules"),
]

for i, (cmd, desc) in enumerate(commands):
    y = Inches(1.4 + i * 0.33)
    add_text(s, Inches(0.7), y, Inches(5.5), Inches(0.25),
             cmd, font_size=10, color=ACCENT2, bold=True)
    add_text(s, Inches(6.5), y, Inches(6.0), Inches(0.25),
             desc, font_size=10, color=BODY_TEXT)

# Key files
add_section_label(s, Inches(0.5), Inches(3.15), "KEY FILES", color=ACCENT5, width=Inches(1.3))

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
    y = Inches(3.55 + i * 0.3)
    add_text(s, Inches(0.7), y, Inches(4.5), Inches(0.25),
             f, font_size=10, color=ACCENT5, bold=True)
    add_text(s, Inches(5.5), y, Inches(7.0), Inches(0.25),
             desc, font_size=10, color=BODY_TEXT)

# Checklists
add_section_label(s, Inches(0.5), Inches(5.7), "BEFORE EVERY ENGAGEMENT", color=GREEN, width=Inches(2.5))
checks = ["Search Central registry", "Select Snap preset", "Configure (don't modify)", "Contribute back at end"]
for i, c in enumerate(checks):
    x = Inches(0.7 + i * 3.0)
    add_text(s, x, Inches(6.05), Inches(2.8), Inches(0.25),
             f"  {c}", font_size=10, color=BODY_TEXT)

add_footer(s, prs, 14, TOTAL_SLIDES)

add_notes(s,
    "WHAT TO SAY:\n"
    "Keep this slide handy. It has the commands, files, and checklist you'll use every day.\n\n"
    "Essential commands: three snap-squad-emu commands cover initialization. "
    "Key files: seven files you need to know.\n\n"
    "The checklist at the bottom: four things to do at the start and end of every engagement. "
    "Search first, select a Snap, configure (don't modify), and contribute back.\n\n"
    "PRACTICAL STEP:\n"
    "Print this slide. Put it next to your monitor. Follow it every time you start a new project.")

# =====================================================================
# SLIDE 15 -- CLOSING (LATAM template layout 0)
# =====================================================================
s = prs.slides.add_slide(prs.slide_layouts[0])
for sp in list(s.placeholders):
    sp_elem = sp._element
    sp_elem.getparent().remove(sp_elem)

add_text(s, Inches(0.8), Inches(1.0), Inches(11), Inches(0.5),
         "Microsoft Accelerated Factory", font_size=18, color=WHITE,
         font_name="Segoe Sans Display Semibold")
add_text(s, Inches(0.8), Inches(1.8), Inches(11), Inches(0.7),
         "Start Using This Runbook", font_size=44, color=WHITE, bold=True, font_name="Aptos Display")

closing = [
    ("01", "Search First", "Check Central Squad registry before creating anything new"),
    ("02", "Use Snap Presets", "One command initializes your entire team with agents and routing"),
    ("03", "Configure, Don't Modify", "Project-specific inputs only. Never change shared agent logic"),
    ("04", "Contribute Back", "Every improvement you make should benefit every team"),
    ("05", "Compound Skills", "The system gets smarter with every engagement. Make it count"),
]

for i, (num, title, desc) in enumerate(closing):
    y = Inches(2.8 + i * 0.7)
    add_icon_circle(s, Inches(0.8), y, 0.4, RGBColor(0xCC, 0xE5, 0xFF), num, 12)
    add_text(s, Inches(1.4), y, Inches(10), Inches(0.3),
             title, font_size=16, color=WHITE, bold=True)
    add_text(s, Inches(1.4), y + Inches(0.3), Inches(10), Inches(0.3),
             desc, font_size=11, color=RGBColor(0x90, 0xB8, 0xE0))

add_text(s, Inches(0.8), Inches(6.2), Inches(11), Inches(0.35),
         "Reuse is the default. Creating is the exception. Every engagement makes us smarter.",
         font_size=14, color=RGBColor(0xCC, 0xE5, 0xFF), bold=True)

add_footer(s, prs, 15, TOTAL_SLIDES)

add_notes(s,
    "WHAT TO SAY:\n"
    "Five takeaways. Search first. Use Snap presets. Configure, don't modify. Contribute back. "
    "Compound skills.\n\n"
    "This runbook is a living document. As the model evolves, this runbook evolves with it. "
    "If you find something missing or unclear, submit a PR.\n\n"
    "NEXT STEPS:\n"
    "1. Set up Central Squad repository if it doesn't exist\n"
    "2. Create your first Snap preset based on the Default template\n"
    "3. Initialize a SubSquad for your next engagement\n"
    "4. Follow this runbook step by step\n"
    "5. At engagement end, submit at least one improvement to Central\n\n"
    "The goal is not perfection on day one. The goal is to start the flywheel spinning. "
    "Every engagement makes it faster.")

# =====================================================================
# SAVE
# =====================================================================
OUTPUT = os.path.join(BASE_DIR, "..", "decks", "Copilot_Squad_Snap_Runbook.pptx")
prs.save(OUTPUT)
print(f"Snap Runbook deck saved: {OUTPUT}")
print(f"{TOTAL_SLIDES} slides generated with speaker notes")
