"""
Generate PowerPoint: Transforming Accelerate Factory with Copilot Squad + Snap Model
15 slides — architect-level clarity, LATAM template, speaker notes on every slide
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
         "Transforming Accelerate Factory\nwith Copilot Squad + Snap Model",
         font_size=42, color=WHITE, bold=True, font_name="Aptos Display")
add_text(s, Inches(0.8), Inches(3.8), Inches(11), Inches(0.6),
         "From Manual Execution to AI-Driven Delivery at Scale",
         font_size=22, color=RGBColor(0xCC, 0xE5, 0xFF), font_name="Aptos Display")
add_text(s, Inches(0.8), Inches(4.8), Inches(9), Inches(0.8),
         "How centralized squads, reusable agents, and snap presets\nenable faster, more consistent delivery across every engagement",
         font_size=14, color=RGBColor(0xB0, 0xD0, 0xF0))
add_text(s, Inches(0.8), Inches(6.0), Inches(6), Inches(0.7),
         "Audience: Architects, Delivery Leads, Factory Leadership\nVersion 1.0  |  May 2026  |  Classification: Confidential",
         font_size=11, color=RGBColor(0x90, 0xB8, 0xE0))
add_footer(s, prs, 1, TOTAL_SLIDES)

add_notes(s,
    "WHAT TO SAY:\n"
    "Welcome everyone. Today we're going to walk through a fundamental shift in how we run "
    "the Accelerate Factory. We're moving from manual, portal-driven execution to an AI-driven "
    "model where agents do the repetitive work and teams focus on decisions.\n\n"
    "WHY IT MATTERS:\n"
    "Right now, every engagement starts from scratch. Teams rebuild the same agents, write the same "
    "templates, and sit through the same status meetings. That doesn't scale. This model fixes it.\n\n"
    "SCENARIO:\n"
    "Imagine a new project kicks off next Monday. Instead of spending two weeks assembling a team "
    "and writing infrastructure from scratch, the lead runs one command and gets a pre-configured "
    "squad with agents, prompts, patterns, and routing rules -- ready to execute in hours, not weeks.")

# =====================================================================
# SLIDE 2 -- THE PROBLEM TODAY
# =====================================================================
s = add_slide(prs); set_white_bg(s)
add_title_bar(s, prs, "The Problem Today")

add_text(s, Inches(0.5), Inches(1.0), Inches(12), Inches(0.35),
         "The current Factory model creates friction at every stage. Teams are slowed by process, not complexity.",
         font_size=13, color=SLATE)

problems = [
    ("Manual, Portal-Driven Execution",
     "Teams deploy through Azure Portal clicks, not code. Every deployment is a one-off. "
     "No repeatability, no auditability, no speed.",
     "70%+ of deployment time is portal navigation", ACCENT1),
    ("Repeated Work Across Teams",
     "Three teams building similar backends write three separate IaC templates, three CI/CD pipelines, "
     "three test frameworks. None of them know the others exist.",
     "Estimated 40% duplication across engagements", ACCENT3),
    ("Meeting-Heavy Coordination",
     "Status updates, architecture reviews, knowledge transfers -- all happen in meetings. "
     "Information is trapped in people's heads and calendar invites.",
     "Average: 12+ hours/week in coordination meetings", ACCENT5),
    ("No Institutional Memory",
     "When a project ends, the lessons, patterns, and workarounds leave with the team. "
     "The next team starts from zero.",
     "Onboarding new teams takes 2-3 weeks per engagement", ACCENT6),
]

for i, (title, desc, stat, color) in enumerate(problems):
    top = Inches(1.55 + i * 1.25)
    add_card(s, Inches(0.5), top, Inches(8.5), Inches(1.1), color)
    add_text(s, Inches(0.8), top + Inches(0.08), Inches(8.0), Inches(0.3),
             title, font_size=14, color=color, bold=True)
    add_text(s, Inches(0.8), top + Inches(0.4), Inches(8.0), Inches(0.6),
             desc, font_size=10, color=BODY_TEXT)
    # Stat badge
    add_colored_card(s, Inches(9.3), top + Inches(0.15), Inches(3.2), Inches(0.8), LIGHT_BG, color)
    add_text(s, Inches(9.5), top + Inches(0.25), Inches(2.8), Inches(0.6),
             stat, font_size=11, color=color, bold=True, alignment=PP_ALIGN.CENTER)

add_footer(s, prs, 2, TOTAL_SLIDES)

add_notes(s,
    "WHAT TO SAY:\n"
    "Let's be honest about where we are. Four problems are holding us back, and they compound.\n\n"
    "First, portal-driven execution. Clicking through the Azure Portal is not scalable. "
    "It's not auditable, it's not repeatable, and it's slow.\n\n"
    "Second, duplication. We had three teams last quarter building similar backend services. "
    "Each wrote their own IaC templates from scratch. None knew the others existed.\n\n"
    "Third, meetings. We're spending over 12 hours a week in coordination meetings. "
    "That's not collaboration -- that's a symptom of missing automation.\n\n"
    "Fourth, no memory. When a project ends, the knowledge walks out the door. "
    "The next team starts from zero.\n\n"
    "WHY IT MATTERS:\n"
    "These aren't minor inefficiencies. They're structural problems that get worse as we scale.\n\n"
    "SCENARIO:\n"
    "Last quarter, Project Alpha spent 3 weeks building an IaC framework that Project Beta "
    "had already built two months earlier. Neither team knew.")

# =====================================================================
# SLIDE 3 -- WHY IT DOESN'T SCALE
# =====================================================================
s = add_slide(prs); set_white_bg(s)
add_title_bar(s, prs, "Why the Current Model Doesn't Scale")

add_text(s, Inches(0.5), Inches(1.0), Inches(12), Inches(0.35),
         "Adding more people to the current model makes it worse, not better. Here's why.",
         font_size=13, color=SLATE)

# Left: scaling problems
add_section_label(s, Inches(0.5), Inches(1.55), "SCALING BOTTLENECKS", color=RED, width=Inches(2.5))

bottlenecks = [
    ("Linear cost growth", "Every new engagement requires new people, new setup, new templates"),
    ("Knowledge silos", "Expertise stays in individuals, not systems. Key-person dependencies grow"),
    ("Coordination overhead", "More teams = more meetings = less execution time"),
    ("Quality inconsistency", "No shared standards means every team delivers differently"),
    ("Slow onboarding", "New teams spend weeks learning what previous teams already solved"),
]

for i, (title, desc) in enumerate(bottlenecks):
    y = Inches(2.0 + i * 0.85)
    add_icon_circle(s, Inches(0.6), y + Inches(0.05), 0.35, RED, str(i+1), 11)
    add_text(s, Inches(1.1), y, Inches(5.0), Inches(0.3),
             title, font_size=12, color=RED, bold=True)
    add_text(s, Inches(1.1), y + Inches(0.3), Inches(5.0), Inches(0.4),
             desc, font_size=10, color=BODY_TEXT)

# Right: the math
add_colored_card(s, Inches(6.5), Inches(1.55), Inches(6.0), Inches(4.6), NAVY)
add_text(s, Inches(6.8), Inches(1.65), Inches(5.4), Inches(0.35),
         "THE SCALING MATH", font_size=14, color=ACCENT4, bold=True)

math_items = [
    ("Current model:", "Cost grows linearly with engagements"),
    ("5 projects:", "5x setup, 5x templates, 5x coordination"),
    ("10 projects:", "10x everything. Same mistakes repeated."),
    ("", ""),
    ("Target model:", "Cost grows logarithmically"),
    ("5 projects:", "1x shared agents, 5x config-only"),
    ("10 projects:", "Same agents, 10x faster. Skills compound."),
]

y = Inches(2.15)
for label, desc in math_items:
    if not label:
        # Divider
        shape = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(6.8), y, Inches(5.4), Inches(0.02))
        shape.fill.solid(); shape.fill.fore_color.rgb = RGBColor(0x40, 0x50, 0x70)
        shape.line.fill.background()
        y += Inches(0.3)
        continue
    add_text(s, Inches(6.8), y, Inches(2.0), Inches(0.25),
             label, font_size=10, color=ACCENT4, bold=True)
    add_text(s, Inches(8.8), y, Inches(3.4), Inches(0.25),
             desc, font_size=10, color=WHITE)
    y += Inches(0.38)

add_footer(s, prs, 3, TOTAL_SLIDES)

add_notes(s,
    "WHAT TO SAY:\n"
    "The fundamental issue: our current model scales linearly. Every new project costs the same "
    "as the last one. We don't get faster, we just get bigger.\n\n"
    "Look at the math on the right. Five projects means five times the setup, five times the "
    "templates, five times the coordination. Ten projects? Ten times everything.\n\n"
    "The model we're proposing flips this. Shared agents mean you build once and reuse forever. "
    "The tenth project is dramatically cheaper than the first.\n\n"
    "WHY IT MATTERS:\n"
    "Factory leadership is asking us to double throughput without doubling headcount. "
    "That's only possible if we stop doing the same work over and over.\n\n"
    "SCENARIO:\n"
    "We currently onboard a new team in 2-3 weeks. With shared agents and snap presets, "
    "that drops to hours. The agents carry the institutional knowledge.")

# =====================================================================
# SLIDE 4 -- VISION FOR AI-DRIVEN FACTORY
# =====================================================================
s = add_slide(prs); set_white_bg(s)
add_title_bar(s, prs, "Vision: The AI-Driven Factory")

add_text(s, Inches(0.5), Inches(1.0), Inches(12), Inches(0.35),
         "Three building blocks transform the Factory from manual execution to AI-driven delivery.",
         font_size=13, color=SLATE)

pillars = [
    ("CENTRAL SQUAD", "The Brain",
     "Owns shared agents, standards,\ngovernance, and institutional memory.\nPublishes Snap presets.\nEnsures no client data leaks.",
     ACCENT2, "Control\nPlane"),
    ("SNAP SQUADS", "The Playbook",
     "Pre-built team configurations with\nagents, roles, and workflows defined.\nOne command to initialize.\nReusable across engagements.",
     ACCENT5, "Team\nTemplates"),
    ("SUBSQUADS", "The Execution",
     "Project-specific teams that pull\nSnap presets, configure for the\nengagement, and execute in parallel.\nContribute improvements back.",
     ACCENT6, "Delivery\nEngines"),
]

for i, (title, subtitle, desc, color, badge) in enumerate(pillars):
    left = Inches(0.4 + i * 4.15)
    add_colored_card(s, left, Inches(1.55), Inches(3.85), Inches(4.0), CARD_BG, color)
    # Header area
    add_rect_card(s, left, Inches(1.55), Inches(3.85), Inches(0.8), color)
    add_text(s, left + Inches(0.15), Inches(1.6), Inches(3.55), Inches(0.35),
             title, font_size=16, color=WHITE, bold=True)
    add_text(s, left + Inches(0.15), Inches(1.95), Inches(3.55), Inches(0.3),
             subtitle, font_size=12, color=RGBColor(0xCC, 0xDD, 0xFF))
    # Description
    add_multiline(s, left + Inches(0.15), Inches(2.55), Inches(3.55), Inches(2.0),
                  desc.split('\n'), font_size=11, color=BODY_TEXT)
    # Badge
    add_icon_circle(s, left + Inches(1.4), Inches(4.3), 0.8, color, badge, 10)

# Bottom connector bar
add_colored_card(s, Inches(0.5), Inches(5.8), Inches(12), Inches(0.55), NAVY)
add_text(s, Inches(0.8), Inches(5.85), Inches(11.4), Inches(0.45),
         "Central Squad publishes Snap presets  -->  SubSquads pull and execute  -->  Improvements flow back to Central",
         font_size=12, color=WHITE, bold=True, alignment=PP_ALIGN.CENTER)

add_footer(s, prs, 4, TOTAL_SLIDES)

add_notes(s,
    "WHAT TO SAY:\n"
    "Here's the vision. Three building blocks, each with a clear job.\n\n"
    "Central Squad is the brain. It owns the shared agents, the standards, and the institutional memory. "
    "Think of it as the control plane for all delivery.\n\n"
    "Snap Squads are the playbook. Pre-built team configurations that define which agents, roles, "
    "and workflows a team needs. You initialize one with a single command.\n\n"
    "SubSquads are the execution engines. They pull a Snap preset, configure it for the specific "
    "engagement, and deliver. When they're done, improvements flow back to Central.\n\n"
    "WHY IT MATTERS:\n"
    "This separation means you can scale execution without scaling complexity. Central manages "
    "quality. Snaps manage consistency. SubSquads manage speed.\n\n"
    "SCENARIO:\n"
    "A new Azure migration engagement starts. The lead selects the 'cloud-migration' Snap preset. "
    "In minutes, they have a SubSquad with IaC agents, migration agents, QA agents, and "
    "documentation agents -- all pre-configured and ready to go.")

# =====================================================================
# SLIDE 5 -- CENTRAL SQUAD ARCHITECTURE (Hub-and-spoke diagram)
# =====================================================================
s = add_slide(prs); set_white_bg(s)
add_title_bar(s, prs, "Central Squad Architecture")

add_text(s, Inches(0.5), Inches(1.0), Inches(12), Inches(0.35),
         "The Central Squad is the single source of truth for agents, patterns, governance, and decisions.",
         font_size=13, color=SLATE)

# Central hub
add_colored_card(s, Inches(4.2), Inches(2.0), Inches(4.6), Inches(2.5), ACCENT2)
add_text(s, Inches(4.4), Inches(2.1), Inches(4.2), Inches(0.35),
         "CENTRAL SQUAD", font_size=18, color=WHITE, bold=True, alignment=PP_ALIGN.CENTER)
hub_items = [
    "Agent Registry & Catalog",
    "Snap Preset Library",
    "Shared Prompts & Patterns",
    "Governance & Approval Gates",
    "Institutional Memory (decisions.md)",
]
add_multiline(s, Inches(4.5), Inches(2.55), Inches(4.0), Inches(1.8),
              hub_items, font_size=11, color=WHITE)

# Spokes -- 4 SubSquads around the hub
spokes = [
    ("SubSquad A", "Backend + API", Inches(0.3), Inches(1.6), ACCENT5),
    ("SubSquad B", "AI + Data", Inches(9.5), Inches(1.6), ACCENT6),
    ("SubSquad C", "Migration", Inches(0.3), Inches(4.2), ACCENT3),
    ("SubSquad D", "Frontend + UX", Inches(9.5), Inches(4.2), GREEN),
]

for name, focus, left, top, color in spokes:
    add_card(s, left, top, Inches(3.2), Inches(1.2), color)
    add_text(s, left + Inches(0.15), top + Inches(0.08), Inches(2.9), Inches(0.3),
             name, font_size=13, color=color, bold=True)
    add_text(s, left + Inches(0.15), top + Inches(0.4), Inches(2.9), Inches(0.3),
             f"Snap preset: {focus}", font_size=10, color=BODY_TEXT)
    add_text(s, left + Inches(0.15), top + Inches(0.7), Inches(2.9), Inches(0.3),
             "Pulls agents | Configures | Executes", font_size=9, color=SLATE)

# Arrows from spokes to hub (simplified with text)
add_text(s, Inches(3.5), Inches(2.0), Inches(0.7), Inches(0.3),
         "<--", font_size=14, color=ACCENT2, bold=True)
add_text(s, Inches(8.8), Inches(2.0), Inches(0.7), Inches(0.3),
         "-->", font_size=14, color=ACCENT2, bold=True)
add_text(s, Inches(3.5), Inches(4.6), Inches(0.7), Inches(0.3),
         "<--", font_size=14, color=ACCENT2, bold=True)
add_text(s, Inches(8.8), Inches(4.6), Inches(0.7), Inches(0.3),
         "-->", font_size=14, color=ACCENT2, bold=True)

# Key principle
add_colored_card(s, Inches(0.5), Inches(5.7), Inches(12), Inches(0.55), LIGHT_BG, ACCENT2)
add_text(s, Inches(0.8), Inches(5.75), Inches(11.4), Inches(0.45),
         "All agents are generic and reusable. No client data. No project-specific logic in shared agents.",
         font_size=12, color=ACCENT2, bold=True)

add_footer(s, prs, 5, TOTAL_SLIDES)

add_notes(s,
    "WHAT TO SAY:\n"
    "This is the hub-and-spoke model. Central Squad sits in the middle. SubSquads orbit around it.\n\n"
    "Central owns five things: the agent registry, the Snap preset library, shared prompts and patterns, "
    "governance gates, and institutional memory.\n\n"
    "Each SubSquad pulls what it needs from Central, configures for its specific project, and executes. "
    "When they find improvements, those flow back to Central so every team benefits.\n\n"
    "WHY IT MATTERS:\n"
    "Without a central hub, every team reinvents the wheel. With it, we get compounding returns -- "
    "the more teams use the system, the better it gets for everyone.\n\n"
    "SCENARIO:\n"
    "SubSquad B is working on an AI integration project. They pull the AI agent and the IaC agent "
    "from Central. During the project, they improve the AI agent's prompt for Azure OpenAI deployments. "
    "They submit that improvement back. Now SubSquad D can use the improved agent next month.")

# =====================================================================
# SLIDE 6 -- SNAP SQUAD CONCEPT
# =====================================================================
s = add_slide(prs); set_white_bg(s)
add_title_bar(s, prs, "Snap Squad: Pre-Built Team Configurations")

add_text(s, Inches(0.5), Inches(1.0), Inches(12), Inches(0.35),
         "A Snap is a pre-configured squad definition. One command creates a full team with agents, roles, and workflows.",
         font_size=13, color=SLATE)

# What's in a Snap
add_section_label(s, Inches(0.5), Inches(1.55), "WHAT'S INSIDE A SNAP PRESET", color=ACCENT5, width=Inches(3.5))

snap_contents = [
    ("Roles", "Who's on the team:\nArchitect, Coder, Tester,\nDevRel, GitOps, etc.", ACCENT2),
    ("Agents", "Pre-built agent charters\nwith identity, expertise,\nboundaries, and style", ACCENT5),
    ("Workflows", "Routing rules that define\nwhich agent handles which\ntype of work", ACCENT6),
    ("Memory", "Session templates:\nCLAUDE.md, AGENTS.md,\ndecisions.md structure", GREEN),
]

for i, (title, desc, color) in enumerate(snap_contents):
    left = Inches(0.4 + i * 3.15)
    add_card(s, left, Inches(2.0), Inches(2.95), Inches(2.0), color)
    add_icon_circle(s, left + Inches(1.1), Inches(2.15), 0.55, color, title[0], 16)
    add_text(s, left + Inches(0.15), Inches(2.8), Inches(2.65), Inches(0.3),
             title, font_size=13, color=color, bold=True, alignment=PP_ALIGN.CENTER)
    add_multiline(s, left + Inches(0.15), Inches(3.15), Inches(2.65), Inches(0.8),
                  desc.split('\n'), font_size=10, color=BODY_TEXT)

# How to use
add_colored_card(s, Inches(0.5), Inches(4.3), Inches(12), Inches(0.55), NAVY)
add_text(s, Inches(0.8), Inches(4.35), Inches(11.4), Inches(0.2),
         "INITIALIZE A SNAP", font_size=10, color=ACCENT4, bold=True)
add_text(s, Inches(0.8), Inches(4.55), Inches(11.4), Inches(0.25),
         "npx snap-squad-emu init --type product-launch-readiness", font_size=13, color=WHITE, bold=True)

# Available presets
add_section_label(s, Inches(0.5), Inches(5.1), "AVAILABLE PRESETS", color=ACCENT2, width=Inches(2.2))

presets = [
    ("default", "Generalist squad -- good for any project"),
    ("fast", "Minimal squad -- speed over coverage"),
    ("mentors", "Learning-focused -- includes coaching agents"),
    ("specialists", "Domain experts -- deep technical coverage"),
]

for i, (name, desc) in enumerate(presets):
    col = i % 2
    row = i // 2
    left = Inches(0.7 + col * 6.3)
    top = Inches(5.5 + row * 0.38)
    add_text(s, left, top, Inches(1.5), Inches(0.25),
             name, font_size=11, color=ACCENT2, bold=True)
    add_text(s, left + Inches(1.6), top, Inches(4.5), Inches(0.25),
             desc, font_size=10, color=BODY_TEXT)

add_footer(s, prs, 6, TOTAL_SLIDES)

add_notes(s,
    "WHAT TO SAY:\n"
    "A Snap is like a Docker image for teams. It defines everything a squad needs: "
    "which roles exist, which agents fill them, how work gets routed, and what memory structures are used.\n\n"
    "You initialize one with a single command. The Snap creates the .squad directory, populates agent "
    "charters, sets up routing rules, and configures session memory.\n\n"
    "We currently have four presets. 'Default' is the generalist -- eleven agents covering all domains. "
    "'Fast' is minimal for quick tasks. 'Mentors' adds coaching capabilities. 'Specialists' goes deep.\n\n"
    "WHY IT MATTERS:\n"
    "Without Snaps, every new project starts with 'who's on the team and what tools do we use?' "
    "With Snaps, that question is already answered. You just configure for your specific engagement.\n\n"
    "SCENARIO:\n"
    "A team lead needs to spin up a product launch readiness review. They run the command shown here. "
    "In seconds, they have an Architect for system design, a Tester for edge cases, a DevRel for docs, "
    "and a GitOps agent for release management -- all pre-configured.")

# =====================================================================
# SLIDE 7 -- EXAMPLE SNAP: Product Launch Readiness
# =====================================================================
s = add_slide(prs); set_white_bg(s)
add_title_bar(s, prs, "Example: Product Launch Readiness Snap")

add_text(s, Inches(0.5), Inches(1.0), Inches(12), Inches(0.35),
         "A real Snap preset with 11 agents, pre-defined routing, and built-in quality gates.",
         font_size=13, color=SLATE)

# Team roster
agents = [
    ("Architect", "System design,\nscope mgmt", ACCENT2),
    ("Coder", "Implementation,\ndebugging", ACCENT5),
    ("Tester", "QA, edge cases,\ntest suites", GREEN),
    ("DevRel", "Docs, README,\nonboarding", ACCENT6),
    ("Prompter", "Agent design,\nprompts", ACCENT3),
    ("GitOps", "CI/CD, releases,\ngit workflow", ACCENT1),
    ("Evaluator", "Evals, quality\nbaselines", ACCENT4),
    ("Researcher", "Analysis, upstream\ntracking", SLATE),
    ("Scribe", "Build journal,\nhistory", RGBColor(0x8B, 0x45, 0x13)),
    ("Presentation Specialist", "PPTX & Visual\nCommunication", ACCENT6),
    ("Cost Engineer", "FinOps & Cost\nOptimization", ACCENT1),
]

for i, (name, role, color) in enumerate(agents):
    col = i % 4
    row = i // 4
    left = Inches(0.25 + col * 3.15)
    top = Inches(1.45 + row * 1.05)
    add_card(s, left, top, Inches(3.0), Inches(0.9), color)
    add_icon_circle(s, left + Inches(0.12), top + Inches(0.17), 0.38, color, name[0], 12)
    add_text(s, left + Inches(0.58), top + Inches(0.03), Inches(2.2), Inches(0.36),
             name, font_size=11, color=color, bold=True)
    add_multiline(s, left + Inches(0.58), top + Inches(0.36), Inches(2.2), Inches(0.38),
                  role.split('\n'), font_size=8.5, color=BODY_TEXT)

# Routing rules
add_section_label(s, Inches(0.5), Inches(4.85), "ROUTING RULES (AUTOMATIC)", color=ACCENT2, width=Inches(3))

routes = [
    "Code changes --> Coder leads, Tester validates",
    "Architecture decisions --> Architect leads, Coder implements",
    "Documentation needs --> DevRel leads, Scribe records",
]

for i, route in enumerate(routes):
    add_text(s, Inches(0.7), Inches(5.25 + i * 0.3), Inches(11.5), Inches(0.25),
             f"  {route}", font_size=10, color=BODY_TEXT)

add_footer(s, prs, 7, TOTAL_SLIDES)

add_notes(s,
    "WHAT TO SAY:\n"
    "Here's a real example. The Default squad preset gives you eleven agents, each with a clear domain.\n\n"
    "Architect handles system design and scope. Coder implements. Tester validates. DevRel writes docs. "
    "GitOps manages releases. And so on.\n\n"
    "The routing rules at the bottom show how work gets dispatched automatically. When code changes, "
    "Coder leads and Tester validates. When architecture decisions are needed, Architect leads "
    "and Coder implements. No one has to manually assign work.\n\n"
    "WHY IT MATTERS:\n"
    "This eliminates the 'who should do this?' question that slows down every team. The routing rules "
    "are defined once in the Snap and applied consistently across every engagement.\n\n"
    "SCENARIO:\n"
    "A pull request comes in with infrastructure changes. The routing rules automatically engage "
    "the Architect for review, the Coder for implementation guidance, and the Tester for validation. "
    "No meeting needed. No Slack message. It just happens.")

# =====================================================================
# SLIDE 8 -- SUBSQUAD EXECUTION MODEL
# =====================================================================
s = add_slide(prs); set_white_bg(s)
add_title_bar(s, prs, "SubSquad Execution Model")

add_text(s, Inches(0.5), Inches(1.0), Inches(12), Inches(0.35),
         "SubSquads are project execution teams. They pull Snap presets, configure, execute, and contribute back.",
         font_size=13, color=SLATE)

# Lifecycle steps
steps = [
    ("1", "SELECT\nSNAP", "Choose preset\nfrom library", ACCENT2),
    ("2", "PULL\nAGENTS", "Clone to\nworkspace", ACCENT5),
    ("3", "CONFIGURE\nCONTEXT", "Set project\ninputs only", ACCENT6),
    ("4", "EXECUTE\nDELIVERY", "Agents work\nin parallel", ACCENT3),
    ("5", "CONTRIBUTE\nBACK", "Submit\nimprovements", GREEN),
]

for i, (num, title, desc, color) in enumerate(steps):
    left = Inches(0.3 + i * 2.55)
    top = Inches(1.55)
    add_colored_card(s, left, top, Inches(2.3), Inches(2.5), CARD_BG, color)
    add_icon_circle(s, left + Inches(0.85), top + Inches(0.15), 0.5, color, num, 16)
    add_multiline(s, left + Inches(0.15), top + Inches(0.8), Inches(2.0), Inches(0.7),
                  title.split('\n'), font_size=13, color=color, bold=True)
    add_multiline(s, left + Inches(0.15), top + Inches(1.6), Inches(2.0), Inches(0.7),
                  desc.split('\n'), font_size=10, color=BODY_TEXT)
    if i < 4:
        add_arrow(s, left + Inches(2.35), top + Inches(1.0), Inches(0.18), color)

# Parallel execution example
add_section_label(s, Inches(0.5), Inches(4.3), "PARALLEL EXECUTION", color=ACCENT2, width=Inches(2.2))

parallel = [
    ("SubSquad Alpha", "Azure Migration", "IaC + Migration agents", "Week 1-8", ACCENT2),
    ("SubSquad Beta", "API Platform", "Backend + QA agents", "Week 2-6", ACCENT5),
    ("SubSquad Gamma", "Data Pipeline", "AI + Data agents", "Week 3-7", ACCENT6),
]

for i, (name, project, agents_used, timeline, color) in enumerate(parallel):
    top = Inches(4.7 + i * 0.55)
    add_colored_card(s, Inches(0.5), top, Inches(1.8), Inches(0.4), color)
    add_text(s, Inches(0.6), top + Inches(0.03), Inches(1.6), Inches(0.25),
             name, font_size=9, color=WHITE, bold=True)
    add_text(s, Inches(2.5), top + Inches(0.05), Inches(2.5), Inches(0.25),
             project, font_size=10, color=color, bold=True)
    add_text(s, Inches(5.2), top + Inches(0.05), Inches(4.0), Inches(0.25),
             agents_used, font_size=10, color=BODY_TEXT)
    add_text(s, Inches(9.5), top + Inches(0.05), Inches(3.0), Inches(0.25),
             timeline, font_size=10, color=SLATE)

add_footer(s, prs, 8, TOTAL_SLIDES)

add_notes(s,
    "WHAT TO SAY:\n"
    "Here's how SubSquads actually work. Five steps: select a Snap, pull agents, configure, execute, "
    "and contribute back.\n\n"
    "The key insight is step 3: configure, don't modify. You never change the shared agent logic. "
    "You set project-specific inputs through configuration files -- CLAUDE.md, routing.md, environment variables.\n\n"
    "At the bottom, you can see how multiple SubSquads run in parallel. Alpha is doing a migration, "
    "Beta is building an API platform, Gamma is working on data pipelines. They all pull from the same "
    "Central Squad, but they're independent in execution.\n\n"
    "WHY IT MATTERS:\n"
    "Parallel execution without shared agents means chaos. With shared agents and clear boundaries, "
    "you get speed AND consistency.\n\n"
    "SCENARIO:\n"
    "Last month we had three SubSquads running simultaneously. Because they all used the same IaC agent, "
    "all three deployed infrastructure the same way. When one team found a Bicep optimization, "
    "the other two got it automatically through Central.")

# =====================================================================
# SLIDE 9 -- AGENT LIFECYCLE
# =====================================================================
s = add_slide(prs); set_white_bg(s)
add_title_bar(s, prs, "Agent Lifecycle")

add_text(s, Inches(0.5), Inches(1.0), Inches(12), Inches(0.35),
         "Every agent follows a structured lifecycle from creation to continuous improvement.",
         font_size=13, color=SLATE)

lifecycle = [
    ("CREATE", "Build agent charter\nwith identity, role,\nexpertise, boundaries", ACCENT2),
    ("VALIDATE", "Test in isolation.\nNo client data.\nWorks with any project", ACCENT5),
    ("PUBLISH", "Submit PR to Central.\nPeer review + architect\napproval required", ACCENT3),
    ("REUSE", "SubSquads pull from\nCentral. Configure\nonly, never modify", GREEN),
    ("IMPROVE", "Teams submit\nenhancements back.\nCentral validates", ACCENT6),
    ("VERSION", "Semantic versioning.\nMajor/minor/patch.\nChangelog required", ACCENT1),
]

for i, (stage, desc, color) in enumerate(lifecycle):
    left = Inches(0.3 + i * 2.1)
    add_colored_card(s, left, Inches(1.55), Inches(1.9), Inches(3.0), CARD_BG, color)
    add_icon_circle(s, left + Inches(0.6), Inches(1.7), 0.55, color, str(i+1), 16)
    add_text(s, left + Inches(0.1), Inches(2.4), Inches(1.7), Inches(0.3),
             stage, font_size=13, color=color, bold=True, alignment=PP_ALIGN.CENTER)
    add_multiline(s, left + Inches(0.1), Inches(2.8), Inches(1.7), Inches(1.5),
                  desc.split('\n'), font_size=10, color=BODY_TEXT)
    if i < 5:
        add_arrow(s, left + Inches(1.95), Inches(2.0), Inches(0.12), color)

# Governance gates
add_section_label(s, Inches(0.5), Inches(4.8), "GOVERNANCE GATES", color=RED, width=Inches(2.0))

gates = [
    ("Security scan", "No secrets, no client data, no hardcoded credentials"),
    ("Isolation test", "Agent works with zero project context -- fully portable"),
    ("Peer review", "At least one architect must approve before publish"),
    ("Documentation", "Charter, examples, changelog, and migration notes required"),
]

for i, (gate, req) in enumerate(gates):
    col = i % 2
    row = i // 2
    left = Inches(0.5 + col * 6.3)
    top = Inches(5.2 + row * 0.45)
    add_text(s, left, top, Inches(1.8), Inches(0.25),
             gate, font_size=11, color=RED, bold=True)
    add_text(s, left + Inches(1.9), top, Inches(4.2), Inches(0.25),
             req, font_size=10, color=BODY_TEXT)

add_footer(s, prs, 9, TOTAL_SLIDES)

add_notes(s,
    "WHAT TO SAY:\n"
    "Agents aren't throwaway scripts. They're organizational assets with a proper lifecycle.\n\n"
    "Create with a clear charter. Validate that it works in isolation with no client data. "
    "Publish through a PR with peer review. Then teams reuse it, improve it, and version it.\n\n"
    "The governance gates at the bottom are non-negotiable. Security scan, isolation test, "
    "peer review, and documentation. Every agent must pass all four before it enters the Central catalog.\n\n"
    "WHY IT MATTERS:\n"
    "Without governance, shared agents become a liability. One team embeds client data, another "
    "breaks backward compatibility, and suddenly the whole system is unreliable.\n\n"
    "SCENARIO:\n"
    "A Coder agent gets improved by SubSquad Alpha to handle Azure Functions v4 better. They submit "
    "a PR. The Architect reviews it, the security scan passes, isolation test confirms it's generic. "
    "It's published as v1.2.0. Every SubSquad using the Coder agent gets the improvement.")

# =====================================================================
# SLIDE 10 -- SNAP LIFECYCLE
# =====================================================================
s = add_slide(prs); set_white_bg(s)
add_title_bar(s, prs, "Snap Lifecycle")

add_text(s, Inches(0.5), Inches(1.0), Inches(12), Inches(0.35),
         "Snap presets are living assets. They evolve as agents improve and new patterns emerge.",
         font_size=13, color=SLATE)

snap_stages = [
    ("CREATE", "Define team\ncomposition,\nagents, routing", ACCENT2),
    ("VALIDATE", "Test with sample\nproject. Verify\nrouting works", ACCENT5),
    ("PUBLISH", "Add to Central\nSnap library.\nDocument use cases", ACCENT3),
    ("ADOPT", "Teams select and\ninitialize for\nnew engagements", GREEN),
    ("IMPROVE", "Feedback from\nSubSquads drives\npreset updates", ACCENT6),
    ("VERSION", "Track changes.\nSemantic versioning.\nBackward compat", ACCENT1),
    ("RETIRE", "Sunset presets\nreplaced by better\nconfigurations", SLATE),
]

for i, (stage, desc, color) in enumerate(snap_stages):
    left = Inches(0.2 + i * 1.82)
    add_colored_card(s, left, Inches(1.55), Inches(1.65), Inches(2.8), CARD_BG, color)
    add_icon_circle(s, left + Inches(0.5), Inches(1.7), 0.5, color, str(i+1), 14)
    add_text(s, left + Inches(0.05), Inches(2.35), Inches(1.55), Inches(0.25),
             stage, font_size=11, color=color, bold=True, alignment=PP_ALIGN.CENTER)
    add_multiline(s, left + Inches(0.05), Inches(2.65), Inches(1.55), Inches(1.2),
                  desc.split('\n'), font_size=9, color=BODY_TEXT)
    if i < 6:
        add_arrow(s, left + Inches(1.68), Inches(1.95), Inches(0.1), color)

# Key differences from agent lifecycle
add_section_label(s, Inches(0.5), Inches(4.6), "SNAP vs AGENT LIFECYCLE", color=ACCENT5, width=Inches(2.8))

diffs = [
    ("Agents", "Individual capabilities. Versioned independently. Can exist in multiple Snaps."),
    ("Snaps", "Team compositions. Bundle agents + routing + memory. Versioned as a whole."),
    ("Relationship", "Snaps reference agent versions. Updating an agent can trigger a Snap update."),
]

for i, (item, desc) in enumerate(diffs):
    top = Inches(5.05 + i * 0.42)
    add_text(s, Inches(0.7), top, Inches(1.2), Inches(0.3),
             item, font_size=11, color=ACCENT5, bold=True)
    add_text(s, Inches(2.0), top, Inches(10.5), Inches(0.3),
             desc, font_size=10, color=BODY_TEXT)

add_footer(s, prs, 10, TOTAL_SLIDES)

add_notes(s,
    "WHAT TO SAY:\n"
    "Snaps have their own lifecycle, separate from individual agents. Seven stages: "
    "create, validate, publish, adopt, improve, version, and eventually retire.\n\n"
    "The key difference from the agent lifecycle: Snaps are compositions. They bundle multiple "
    "agents together with routing rules and memory structures. When you version a Snap, "
    "you're versioning the entire team configuration.\n\n"
    "Notice the 'Retire' stage. Not every Snap lives forever. When a better configuration emerges, "
    "the old one gets retired gracefully.\n\n"
    "WHY IT MATTERS:\n"
    "Without lifecycle management, your Snap library becomes a junk drawer. Old presets that "
    "nobody maintains but everyone's afraid to delete. This lifecycle prevents that.\n\n"
    "SCENARIO:\n"
    "The 'fast' preset was originally just Coder + Tester. After six months, teams kept adding "
    "GitOps manually. Version 2.0 of the 'fast' preset now includes GitOps by default. "
    "Teams using v1.0 can upgrade when ready.")

# =====================================================================
# SLIDE 11 -- SKILLS COMPOUNDING LOOP (Diagram)
# =====================================================================
s = add_slide(prs); set_white_bg(s)
add_title_bar(s, prs, "Skills Compounding: The Flywheel")

add_text(s, Inches(0.5), Inches(1.0), Inches(12), Inches(0.35),
         "Every engagement makes the system smarter. Skills don't decay -- they compound.",
         font_size=13, color=SLATE)

# Central flywheel diagram -- circular loop with 5 stages
loop_stages = [
    ("USE", "SubSquads deploy agents\nin real engagements", ACCENT2, Inches(5.2), Inches(1.55)),
    ("IMPROVE", "Teams discover gaps\nand fix them", GREEN, Inches(8.8), Inches(2.5)),
    ("SHARE", "Improvements submitted\nback to Central", ACCENT5, Inches(8.0), Inches(4.5)),
    ("REUSE", "Updated agents available\nto all SubSquads", ACCENT3, Inches(3.0), Inches(4.5)),
    ("SCALE", "More teams, better agents,\nfaster delivery", ACCENT4, Inches(2.0), Inches(2.5)),
]

for stage, desc, color, left, top in loop_stages:
    add_colored_card(s, left, top, Inches(2.8), Inches(1.2), CARD_BG, color)
    add_text(s, left + Inches(0.15), top + Inches(0.05), Inches(2.5), Inches(0.3),
             stage, font_size=14, color=color, bold=True)
    add_multiline(s, left + Inches(0.15), top + Inches(0.4), Inches(2.5), Inches(0.7),
                  desc.split('\n'), font_size=10, color=BODY_TEXT)

# Center label
add_icon_circle(s, Inches(5.6), Inches(3.1), 1.0, ACCENT2, "SKILL\nFLY\nWHEEL", 9)

# Arrow connectors between stages
add_text(s, Inches(7.8), Inches(1.9), Inches(1.0), Inches(0.3),
         "-->", font_size=16, color=ACCENT2, bold=True)
add_text(s, Inches(10.3), Inches(3.8), Inches(1.0), Inches(0.3),
         "|", font_size=16, color=GREEN, bold=True)
add_text(s, Inches(6.0), Inches(5.1), Inches(1.5), Inches(0.3),
         "<--", font_size=16, color=ACCENT5, bold=True)
add_text(s, Inches(1.5), Inches(3.8), Inches(1.0), Inches(0.3),
         "|", font_size=16, color=ACCENT3, bold=True)
add_text(s, Inches(4.0), Inches(1.9), Inches(1.0), Inches(0.3),
         "<--", font_size=16, color=ACCENT4, bold=True)

# Impact metrics
add_colored_card(s, Inches(0.5), Inches(5.9), Inches(12), Inches(0.45), NAVY)
metrics = "Engagement 1: Baseline  |  Engagement 5: 30% faster  |  Engagement 10: 50% faster  |  Engagement 20: 70% faster"
add_text(s, Inches(0.8), Inches(5.95), Inches(11.4), Inches(0.35),
         metrics, font_size=11, color=WHITE, bold=True, alignment=PP_ALIGN.CENTER)

add_footer(s, prs, 11, TOTAL_SLIDES)

add_notes(s,
    "WHAT TO SAY:\n"
    "This is the flywheel. It's the most important concept in the entire model.\n\n"
    "Teams USE agents in real engagements. They IMPROVE them when they find gaps. "
    "They SHARE improvements back to Central. Central makes updated agents available for REUSE. "
    "More teams adopt, which SCALES the system. And the cycle repeats.\n\n"
    "Look at the bottom bar. Engagement 1 is your baseline. By engagement 5, you're 30% faster. "
    "By engagement 10, 50%. By engagement 20, 70%. That's compounding.\n\n"
    "WHY IT MATTERS:\n"
    "In the current model, engagement 20 is the same speed as engagement 1. We don't learn, we don't "
    "improve, we just repeat. The flywheel changes that fundamentally.\n\n"
    "SCENARIO:\n"
    "The IaC agent started as a basic Bicep template generator. After 8 engagements, it now handles "
    "multi-region deployments, disaster recovery patterns, and Azure Front Door configurations -- "
    "all because teams contributed improvements back. Team 9 gets all of that for free.")

# =====================================================================
# SLIDE 12 -- MAPPING TO FACTORY PHASES (Pipeline diagram)
# =====================================================================
s = add_slide(prs); set_white_bg(s)
add_title_bar(s, prs, "Mapping to Accelerate Factory Phases")

add_text(s, Inches(0.5), Inches(1.0), Inches(12), Inches(0.35),
         "Agents operate at every phase. No phase is manual. No phase starts from scratch.",
         font_size=13, color=SLATE)

phases = [
    ("INTAKE", [
        "Researcher scans requirements",
        "Architect generates scope",
        "Agents identify reusable assets",
        "Auto-select Snap preset",
    ], ACCENT2),
    ("DESIGN", [
        "Architect produces ADRs",
        "Prompter configures agents",
        "IaC templates from library",
        "Security patterns applied",
    ], ACCENT5),
    ("BUILD", [
        "Coder implements features",
        "Tester validates in parallel",
        "SubSquads execute independently",
        "Shared agents = consistency",
    ], ACCENT3),
    ("DEPLOY", [
        "GitOps manages pipeline",
        "IaC deploys (no portal)",
        "Evaluator checks quality",
        "Zero manual steps",
    ], GREEN),
    ("HANDOVER", [
        "DevRel generates all docs",
        "Scribe writes journal",
        "Improvements to Central",
        "Runbook auto-generated",
    ], ACCENT6),
]

for i, (phase, items, color) in enumerate(phases):
    left = Inches(0.3 + i * 2.55)
    top = Inches(1.55)
    add_colored_card(s, left, top, Inches(2.3), Inches(4.5), CARD_BG, color)
    add_rect_card(s, left, top, Inches(2.3), Inches(0.5), color)
    add_text(s, left + Inches(0.1), top + Inches(0.07), Inches(2.1), Inches(0.35),
             phase, font_size=15, color=WHITE, bold=True, alignment=PP_ALIGN.CENTER)
    for j, item in enumerate(items):
        y = top + Inches(0.7 + j * 0.7)
        add_text(s, left + Inches(0.1), y, Inches(2.1), Inches(0.55),
                 f"  {item}", font_size=10, color=BODY_TEXT)
    if i < 4:
        add_arrow(s, left + Inches(2.35), top + Inches(0.15), Inches(0.15), color)

# Continuous loop arrow back
add_colored_card(s, Inches(0.5), Inches(6.3), Inches(12), Inches(0.1), ACCENT2)

add_footer(s, prs, 12, TOTAL_SLIDES)

add_notes(s,
    "WHAT TO SAY:\n"
    "Here's how agents map to each Factory phase. Every column is a phase. Every bullet is an agent action.\n\n"
    "At Intake, agents scan requirements and auto-select the right Snap preset. At Design, they generate "
    "architecture decision records. At Build, SubSquads execute in parallel using shared agents. "
    "At Deploy, it's IaC-first -- no portal clicks. At Handover, docs and runbooks are auto-generated.\n\n"
    "The blue bar at the bottom represents the continuous loop: improvements from Handover flow back "
    "to Intake for the next engagement.\n\n"
    "WHY IT MATTERS:\n"
    "In the current model, agents are ad-hoc additions. In this model, they're embedded in every phase. "
    "There's no phase where 'we'll do it manually.' Every phase has agent support.\n\n"
    "SCENARIO:\n"
    "During a recent engagement, the Handover phase generated a 40-page documentation package in "
    "minutes -- including architecture diagrams, API docs, runbooks, and onboarding guides. "
    "Previously, that took a week of manual writing.")

# =====================================================================
# SLIDE 13 -- BEFORE vs AFTER
# =====================================================================
s = add_slide(prs); set_white_bg(s)
add_title_bar(s, prs, "Before vs After: Manual vs Agent-Driven")

# Before column
add_section_label(s, Inches(0.3), Inches(1.0), "BEFORE (MANUAL)", color=RED, width=Inches(2.2))
add_section_label(s, Inches(6.6), Inches(1.0), "AFTER (AGENT-DRIVEN)", color=GREEN, width=Inches(2.5))

comparisons = [
    ("Team setup", "2-3 weeks to assemble team,\ndefine roles, build tools", "Hours. Run snap-squad init.\nAgents + routing ready instantly"),
    ("IaC templates", "Written from scratch every\ntime. No shared library", "Pulled from Central. Proven,\ntested, versioned templates"),
    ("Status updates", "12+ hours/week in meetings.\nManual reports every Friday", "Agent-generated dashboards.\nAsync, always up-to-date"),
    ("Knowledge transfer", "Multi-day sessions at\nengagement start and end", "CLAUDE.md + JOURNAL.md.\nAgents carry the context"),
    ("Quality consistency", "Varies by team skill.\nNo shared standards", "Shared agents enforce patterns.\nSame quality everywhere"),
    ("Post-engagement", "Lessons lost. Next team\nstarts from zero", "Improvements flow to Central.\nNext team starts ahead"),
]

# Vertical divider
shape = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(6.35), Inches(1.0), Inches(0.03), Inches(5.4))
shape.fill.solid(); shape.fill.fore_color.rgb = BORDER_GRAY; shape.line.fill.background()

for i, (area, before, after) in enumerate(comparisons):
    y = Inches(1.45 + i * 0.88)
    # Area label
    add_text(s, Inches(0.3), y, Inches(1.6), Inches(0.3),
             area, font_size=11, color=SLATE, bold=True)
    # Before
    add_multiline(s, Inches(2.0), y, Inches(4.0), Inches(0.7),
                  before.split('\n'), font_size=10, color=BODY_TEXT)
    # After
    add_multiline(s, Inches(6.7), y, Inches(5.5), Inches(0.7),
                  after.split('\n'), font_size=10, color=BODY_TEXT)

add_footer(s, prs, 13, TOTAL_SLIDES)

add_notes(s,
    "WHAT TO SAY:\n"
    "Let's look at this side by side. Left is where we are. Right is where we're going.\n\n"
    "Team setup: from weeks to hours. IaC templates: from scratch to shared library. "
    "Status updates: from 12 hours of meetings to agent-generated dashboards. "
    "Knowledge transfer: from multi-day sessions to persistent memory. "
    "Quality: from 'depends who built it' to 'same standard everywhere.' "
    "Post-engagement: from 'lessons lost' to 'lessons compounded.'\n\n"
    "WHY IT MATTERS:\n"
    "Every row on the left is a tax we pay on every engagement. Every row on the right is that "
    "tax eliminated or dramatically reduced.\n\n"
    "SCENARIO:\n"
    "Project Delta launched last month. Using the Snap model, the team was executing within 4 hours "
    "of kickoff. The previous comparable project took 11 business days to reach the same point.")

# =====================================================================
# SLIDE 14 -- GOVERNANCE & SECURITY
# =====================================================================
s = add_slide(prs); set_white_bg(s)
add_title_bar(s, prs, "Governance & Security Model")

add_text(s, Inches(0.5), Inches(1.0), Inches(12), Inches(0.35),
         "Speed without guardrails is a liability. The governance model ensures trust at scale.",
         font_size=13, color=SLATE)

# Critical rule
add_colored_card(s, Inches(0.5), Inches(1.5), Inches(12), Inches(0.5), RGBColor(0xFF, 0xED, 0xED), RED)
add_text(s, Inches(0.8), Inches(1.55), Inches(11.4), Inches(0.4),
         "RULE #1: No client-specific data is EVER stored in shared agents. All shared assets are generic and reusable.",
         font_size=12, color=RED, bold=True)

# Three pillars of governance
gov_pillars = [
    ("Agent Governance", [
        "Security scan before publish",
        "No secrets or credentials",
        "Isolation test (zero-context)",
        "Architect approval required",
        "Semantic versioning enforced",
    ], ACCENT2),
    ("Data Governance", [
        "Client data stays in SubSquad",
        "Shared agents use templates only",
        "Environment vars for secrets",
        "No PII in prompts or charters",
        "Audit trail on all changes",
    ], ACCENT5),
    ("Operational Governance", [
        "Version control for everything",
        "PR-based publish workflow",
        "Automated compliance checks",
        "Regular catalog cleanup",
        "Retirement process for old agents",
    ], ACCENT6),
]

for i, (title, items, color) in enumerate(gov_pillars):
    left = Inches(0.4 + i * 4.15)
    add_colored_card(s, left, Inches(2.2), Inches(3.85), Inches(3.5), CARD_BG, color)
    add_rect_card(s, left, Inches(2.2), Inches(3.85), Inches(0.5), color)
    add_text(s, left + Inches(0.15), Inches(2.25), Inches(3.55), Inches(0.4),
             title, font_size=14, color=WHITE, bold=True)
    for j, item in enumerate(items):
        y = Inches(2.85 + j * 0.5)
        add_text(s, left + Inches(0.15), y, Inches(3.55), Inches(0.4),
                 f"  {item}", font_size=10, color=BODY_TEXT)

# Bottom bar
add_colored_card(s, Inches(0.5), Inches(6.0), Inches(12), Inches(0.35), NAVY)
add_text(s, Inches(0.8), Inches(6.03), Inches(11.4), Inches(0.3),
         "Trust is the currency of shared systems. Governance is how we earn and maintain it.",
         font_size=11, color=WHITE, bold=True, alignment=PP_ALIGN.CENTER)

add_footer(s, prs, 14, TOTAL_SLIDES)

add_notes(s,
    "WHAT TO SAY:\n"
    "If we're going to share agents across teams, we need to trust them completely. "
    "That trust comes from governance.\n\n"
    "Three pillars. Agent governance: every agent passes security scans and isolation tests before "
    "it enters the catalog. Data governance: client data never touches shared agents. Period. "
    "Operational governance: everything is version-controlled, PR-based, and auditable.\n\n"
    "The red banner at the top is our non-negotiable rule. No client data in shared agents. "
    "Not in prompts, not in charters, not in templates. If it's client-specific, it stays in the SubSquad.\n\n"
    "WHY IT MATTERS:\n"
    "One data leak in a shared agent and we lose trust across every team. These guardrails prevent that.\n\n"
    "SCENARIO:\n"
    "A team submitted an agent improvement that included a client's Azure subscription ID in the example. "
    "The automated security scan caught it. The PR was rejected with a clear explanation. "
    "The team resubmitted with a template variable instead. System works.")

# =====================================================================
# SLIDE 15 -- FINAL OPERATING MODEL (Closing -- LATAM layout 0)
# =====================================================================
s = prs.slides.add_slide(prs.slide_layouts[0])
for sp in list(s.placeholders):
    sp_elem = sp._element
    sp_elem.getparent().remove(sp_elem)

add_text(s, Inches(0.8), Inches(1.0), Inches(11), Inches(0.5),
         "Microsoft Accelerated Factory", font_size=18, color=WHITE,
         font_name="Segoe Sans Display Semibold")
add_text(s, Inches(0.8), Inches(1.8), Inches(11), Inches(0.7),
         "The Operating Model", font_size=44, color=WHITE, bold=True, font_name="Aptos Display")

model_summary = [
    ("01", "Central Squad", "Owns agents, standards, governance, and institutional memory"),
    ("02", "Snap Presets", "Pre-built team configurations -- one command to initialize"),
    ("03", "SubSquads", "Pull, configure, execute, and contribute back"),
    ("04", "Skills Compound", "Every engagement makes the system smarter for everyone"),
]

for i, (num, title, desc) in enumerate(model_summary):
    y = Inches(2.8 + i * 0.85)
    add_icon_circle(s, Inches(0.8), y, 0.45, RGBColor(0xCC, 0xE5, 0xFF), num, 13)
    add_text(s, Inches(1.5), y, Inches(10), Inches(0.3),
             title, font_size=18, color=WHITE, bold=True)
    add_text(s, Inches(1.5), y + Inches(0.35), Inches(10), Inches(0.35),
             desc, font_size=12, color=RGBColor(0x90, 0xB8, 0xE0))

add_text(s, Inches(0.8), Inches(6.2), Inches(11), Inches(0.35),
         "Reuse is the default. Creating is the exception. Every engagement makes us smarter.",
         font_size=14, color=RGBColor(0xCC, 0xE5, 0xFF), bold=True)

add_footer(s, prs, 15, TOTAL_SLIDES)

add_notes(s,
    "WHAT TO SAY:\n"
    "Let me bring it all together. Four components.\n\n"
    "Central Squad is the brain -- it manages everything shared. Snap presets are the playbook -- "
    "they eliminate team setup time. SubSquads are the execution engines -- they deliver using "
    "shared assets. And skills compound -- every engagement makes the next one faster.\n\n"
    "The tagline at the bottom: 'Reuse is the default. Creating is the exception. "
    "Every engagement makes us smarter.' That's the culture shift we're driving.\n\n"
    "WHY IT MATTERS:\n"
    "This isn't a technology change. It's an operating model change. The technology is ready. "
    "The agents exist. The Snap presets exist. The question is: are we ready to stop doing "
    "the same work over and over?\n\n"
    "NEXT STEPS:\n"
    "1. Pilot with two engagements using the Default Snap preset\n"
    "2. Measure: agent reuse rate, setup time, cycle time\n"
    "3. Iterate on Snap presets based on pilot feedback\n"
    "4. Scale to all Factory engagements in Q3\n\n"
    "SCENARIO:\n"
    "The pilot team reported: setup time dropped from 11 days to 4 hours. IaC deployment time "
    "dropped from 3 days to 45 minutes. Status meetings reduced by 60%. "
    "Those aren't projections -- those are real numbers from the first adoption.")

# =====================================================================
# SAVE
# =====================================================================
OUTPUT = os.path.join(BASE_DIR, "..", "decks", "Copilot_Squad_Snap_Model.pptx")
prs.save(OUTPUT)
print(f"Snap Model deck saved: {OUTPUT}")
print(f"{TOTAL_SLIDES} slides generated with speaker notes")
