import os
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR

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
    add_table,
    add_speaker_notes,
    add_circle,
    add_column_card,
    add_metric_card,
    add_stat_card,
    ACCENT1,
    ACCENT2,
    ACCENT3,
    ACCENT4,
    ACCENT5,
    ACCENT6,
    SLATE,
    GREEN,
    BLUE_TEXT,
    WHITE,
    BODY_TEXT,
    SUBTITLE,
)
TOTAL_SLIDES = 17
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_PATH = os.path.join(BASE_DIR, "..", "decks", "Oceans_Fourteen_Squad_vs_Prompting.pptx")

prs = load_template()

def add_arrow(slide, left, top, width, color=ACCENT2):
    shape = slide.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, left, top, width, Inches(0.25))
    shape.fill.solid()
    shape.fill.fore_color.rgb = color
    shape.line.fill.background()
    shape.shadow.inherit = False

# ── Additional utilities ──

def add_box(slide, left, top, width, height, text, fill_color, text_color=WHITE,
            font_size=13, bold=True, rounded=True, line_color=None, align=PP_ALIGN.CENTER):
    shape_type = MSO_SHAPE.ROUNDED_RECTANGLE if rounded else MSO_SHAPE.RECTANGLE
    shape = slide.shapes.add_shape(shape_type, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill_color
    if line_color:
        shape.line.color.rgb = line_color
        shape.line.width = Pt(1)
    else:
        shape.line.fill.background()
    shape.shadow.inherit = False
    tf = shape.text_frame
    tf.clear()
    tf.word_wrap = True
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf.paragraphs[0]
    p.text = text
    p.font.size = Pt(font_size)
    p.font.color.rgb = text_color
    p.font.bold = bold
    p.font.name = "Aptos"
    p.alignment = align
    return shape

def add_connector(slide, x1, y1, x2, y2, color=ACCENT2, width=2):
    line = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, x1, y1, x2, y2)
    line.line.color.rgb = color
    line.line.width = Pt(width)
    return line

def add_step(slide, number, top, text):
    add_circle(slide, Inches(0.75), top, Inches(0.34), ACCENT2, str(number), font_size=12)
    add_text(slide, Inches(1.2), top - Inches(0.01), Inches(10.8), Inches(0.32),
             text, font_size=15, color=BODY_TEXT, bold=False)

# ════════════════════════════════════════════════════════════
# SLIDE 1 — TITLE
# ════════════════════════════════════════════════════════════
slide = add_slide(prs, 0)
# Keep template's native blue background with decorative swirls
add_text(slide, Inches(0.8), Inches(0.75), Inches(4.2), Inches(0.3),
         "Roberto Borges presents", font_size=14, color=RGBColor(0xC5, 0xD7, 0xF2), font_name="Aptos")
add_text(slide, Inches(0.8), Inches(1.65), Inches(11.4), Inches(1.2),
         "Ocean's Fourteen — The Azure Heist 🎰", font_size=28, color=WHITE, bold=True, font_name="Aptos Display")
add_text(slide, Inches(0.8), Inches(2.85), Inches(10.8), Inches(0.6),
         "Why Squad Orchestration Beats Monolithic Prompting", font_size=22, color=RGBColor(0xC7, 0xE3, 0xFF), font_name="Aptos Display")
add_text(slide, Inches(0.8), Inches(3.6), Inches(10.6), Inches(0.5),
         "A GitHub Copilot Migration Architecture for Architects", font_size=15, color=RGBColor(0xA6, 0xC5, 0xE8), font_name="Aptos")
add_text(slide, Inches(0.8), Inches(5.25), Inches(7.2), Inches(0.4),
         "From one giant prompt to a coordinated crew of specialists", font_size=16, color=WHITE, bold=False)
add_text(slide, Inches(0.8), Inches(6.15), Inches(5.0), Inches(0.3),
         "Roberto Borges | Microsoft | 2026", font_size=12, color=RGBColor(0xB7, 0xC5, 0xD8))
add_circle(slide, Inches(10.7), Inches(1.35), Inches(0.55), ACCENT3)
add_circle(slide, Inches(11.35), Inches(1.35), Inches(0.55), ACCENT2)
add_circle(slide, Inches(12.0), Inches(1.35), Inches(0.55), ACCENT5)
add_footer(slide, prs, 1, TOTAL_SLIDES)
add_speaker_notes(slide, """SPEAKER NOTES - Slide 1: Title
Open with the metaphor: this is not about prompting harder, it is about orchestrating a crew.
Frame the audience: architects care about operating models, governance, and scale.
Explain that Ocean's Fourteen is the migration pattern: specialized roles, coordinated handoffs, reusable skills, and visible quality gates.""")

# ════════════════════════════════════════════════════════════
# SLIDE 2 — THE PROBLEM
# ════════════════════════════════════════════════════════════
slide = add_slide(prs)
set_white_bg(slide)
add_title_bar(slide, prs, "The Problem: Legacy Migration at Scale")
add_footer(slide, prs, 2, TOTAL_SLIDES)

add_stat_card(slide, Inches(0.6), Inches(1.55), Inches(3.95), Inches(2.25), ACCENT2,
              "7 Legacy Applications", "Classic ASP, .NET 3.0-4.5, WCF, Java 8", headline="7")
add_stat_card(slide, Inches(4.68), Inches(1.55), Inches(3.95), Inches(2.25), ACCENT3,
              "12+ Migration Concerns", "Security, Performance, DB, CI/CD, Monitoring, Cost", headline="12+")
add_stat_card(slide, Inches(8.76), Inches(1.55), Inches(3.95), Inches(2.25), ACCENT5,
              "1 Developer", "Can't hold all context at once", headline="1")
add_text(slide, Inches(1.0), Inches(4.75), Inches(11.3), Inches(0.8),
         "How do you orchestrate 7 migrations across 12 domains without losing quality?",
         font_size=22, color=BODY_TEXT, bold=True, alignment=PP_ALIGN.CENTER, font_name="Aptos Display")
add_text(slide, Inches(2.0), Inches(5.45), Inches(9.2), Inches(0.45),
         "That is an architecture problem, not a prompting problem.",
         font_size=14, color=SUBTITLE, alignment=PP_ALIGN.CENTER)
add_speaker_notes(slide, """SPEAKER NOTES - Slide 2: The problem
Stress the scale mismatch. The migration portfolio spans seven very different applications and more than a dozen engineering concerns.
A single person or single prompt cannot reliably hold architecture, security, data, deployment, and operations context at once.
This is the forcing function that makes orchestration necessary.""")

# ════════════════════════════════════════════════════════════
# SLIDE 3 — OLD APPROACH
# ════════════════════════════════════════════════════════════
slide = add_slide(prs)
set_white_bg(slide)
add_title_bar(slide, prs, "The Old Way: Monolithic Prompting")
add_footer(slide, prs, 3, TOTAL_SLIDES)
add_section_label(slide, Inches(0.65), Inches(1.0), "Before", Inches(1.1), ACCENT1)

user_box = add_box(slide, Inches(0.9), Inches(2.35), Inches(1.35), Inches(0.8), "User", SLATE)
prompt_box = add_box(slide, Inches(2.85), Inches(2.1), Inches(2.85), Inches(1.3), "Single Prompt File\n(500+ lines)", ACCENT1, font_size=15)
copilot_box = add_box(slide, Inches(6.3), Inches(2.35), Inches(1.6), Inches(0.8), "Copilot", ACCENT2)
add_arrow(slide, Inches(2.3), Inches(2.63), Inches(0.45), ACCENT1)
add_arrow(slide, Inches(5.82), Inches(2.63), Inches(0.38), ACCENT1)
add_text(slide, Inches(1.15), Inches(3.75), Inches(6.95), Inches(0.45),
         "Linear, sequential, one-size-fits-all", font_size=15, color=SUBTITLE, alignment=PP_ALIGN.CENTER)

pain_left = Inches(8.05)
pain_top = Inches(1.45)
pain_width = Inches(4.5)
pain_height = Inches(4.5)
add_card(slide, pain_left, pain_top, pain_width, pain_height, border_color=RGBColor(0xF0, 0xC5, 0xC0), bg_color=RGBColor(0xFE, 0xF7, 0xF6))
add_accent_line(slide, pain_left, pain_top, pain_width, ACCENT1)
add_text(slide, pain_left + Inches(0.18), pain_top + Inches(0.22), Inches(3.3), Inches(0.4),
         "Pain points", font_size=16, color=ACCENT1, bold=True, font_name="Aptos Display")
add_multiline(slide, pain_left + Inches(0.22), pain_top + Inches(0.75), Inches(4.0), Inches(3.6), [
    "❌ One giant prompt tries to cover everything",
    "❌ No specialization — same prompt for security AND database AND performance",
    "❌ No memory between sessions",
    "❌ No quality gates or validation",
    "❌ Context window overflow on complex tasks",
    "❌ No parallel execution",
], font_size=12, color=BODY_TEXT)
add_speaker_notes(slide, """SPEAKER NOTES - Slide 3: The old way
Walk the audience through the anti-pattern. One huge prompt becomes the architecture, the checklist, the team, and the memory system.
That means every concern competes for the same context window and the same generic reasoning path.
The result is fragile quality, no reuse, and no scalable delivery model.""")

# ════════════════════════════════════════════════════════════
# SLIDE 4 — NEW APPROACH
# ════════════════════════════════════════════════════════════
slide = add_slide(prs)
set_white_bg(slide)
add_title_bar(slide, prs, "The New Way: Ocean's Fourteen Squad")
add_footer(slide, prs, 4, TOTAL_SLIDES)
add_section_label(slide, Inches(0.65), Inches(1.0), "After", Inches(1.0), GREEN)

user = add_box(slide, Inches(5.5), Inches(1.1), Inches(2.1), Inches(0.5), "User", SLATE, font_size=14)
orchestrator = add_box(slide, Inches(4.7), Inches(1.85), Inches(3.7), Inches(0.65), "Migration Orchestrator (Chatmode)", ACCENT2, font_size=16)
add_connector(slide, Inches(6.55), Inches(1.6), Inches(6.55), Inches(1.85), ACCENT2, 2)
add_arrow(slide, Inches(6.37), Inches(1.66), Inches(0.36), ACCENT2)

col_x = [Inches(0.7), Inches(3.8), Inches(7.05), Inches(9.95)]
col_width = Inches(2.45)
box_h = Inches(0.43)
col1_y = [Inches(2.95), Inches(3.45), Inches(3.95)]
col2_y = [Inches(2.95), Inches(3.45), Inches(3.95)]
col3_y = [Inches(2.95), Inches(3.45), Inches(3.95), Inches(4.45)]
col4_y = [Inches(2.95), Inches(3.45), Inches(3.95), Inches(4.45)]

for x in [Inches(1.92), Inches(5.02), Inches(8.27), Inches(11.17)]:
    add_connector(slide, Inches(6.55), Inches(2.5), x, Inches(2.8), ACCENT2, 1)

add_box(slide, col_x[0], col1_y[0], col_width, box_h, "Architect", GREEN, font_size=12)
add_box(slide, col_x[0], col1_y[1], col_width, box_h, "Coder", GREEN, font_size=12)
add_box(slide, col_x[0], col1_y[2], col_width, box_h, "Tester", GREEN, font_size=12)

add_box(slide, col_x[1], col2_y[0], col_width, box_h, "Azure Specialist", ACCENT4, font_size=11)
add_box(slide, col_x[1], col2_y[1], col_width, box_h, "DevOps", ACCENT4, font_size=12)
add_box(slide, col_x[1], col2_y[2], col_width, box_h, "Observability", ACCENT4, font_size=11)

add_box(slide, col_x[2], col3_y[0], col_width, box_h, "Database", ACCENT3, font_size=12)
add_box(slide, col_x[2], col3_y[1], col_width, box_h, "Performance", ACCENT3, font_size=11)
add_box(slide, col_x[2], col3_y[2], col_width, box_h, "Cost Engineer", ACCENT3, font_size=11)
add_box(slide, col_x[2], col3_y[3], col_width, box_h, "Scribe", ACCENT3, font_size=12)

add_box(slide, col_x[3], col4_y[0], col_width, box_h, "Security", ACCENT5, font_size=12)
add_box(slide, col_x[3], col4_y[1], col_width, box_h, "Evaluator", ACCENT5, font_size=12)
add_box(slide, col_x[3], col4_y[2], col_width, box_h, "Cutover", ACCENT5, font_size=12)
add_box(slide, col_x[3], col4_y[3], col_width, box_h, "Presentation", ACCENT5, font_size=11)

add_text(slide, Inches(0.78), Inches(2.58), Inches(2.25), Inches(0.22), "Core team", font_size=11, color=GREEN, bold=True, alignment=PP_ALIGN.CENTER)
add_text(slide, Inches(3.9), Inches(2.58), Inches(2.25), Inches(0.22), "Infrastructure", font_size=11, color=ACCENT4, bold=True, alignment=PP_ALIGN.CENTER)
add_text(slide, Inches(7.15), Inches(2.58), Inches(2.25), Inches(0.22), "Data + ops", font_size=11, color=ACCENT3, bold=True, alignment=PP_ALIGN.CENTER)
add_text(slide, Inches(10.05), Inches(2.58), Inches(2.25), Inches(0.22), "Quality + launch", font_size=11, color=ACCENT5, bold=True, alignment=PP_ALIGN.CENTER)

add_box(slide, Inches(1.2), Inches(5.15), Inches(11.0), Inches(0.48), "Skills Library (26 reusable modules)", ACCENT6, font_size=14)
add_box(slide, Inches(1.2), Inches(5.82), Inches(11.0), Inches(0.48), "7 Use-Case Targets", SLATE, font_size=14)
add_speaker_notes(slide, """SPEAKER NOTES - Slide 4: The new way
Show the architectural inversion. The user no longer pushes detail into one giant prompt.
Instead, the orchestrator routes work to specialists, each with a clear charter, while reusable skills sit underneath the whole system.
This makes ownership, parallelism, and governance explicit.""")

# ════════════════════════════════════════════════════════════
# SLIDE 5 — SIDE-BY-SIDE COMPARISON
# ════════════════════════════════════════════════════════════
slide = add_slide(prs)
set_white_bg(slide)
add_title_bar(slide, prs, "Head-to-Head: Old Prompting vs Squad")
add_footer(slide, prs, 5, TOTAL_SLIDES)

rows = [
    ["Dimension", "Old Prompting", "Squad Orchestration"],
    ["Architecture", "1 monolithic prompt", "14 specialized agents"],
    ["Specialization", "None — generic", "Deep domain expertise per agent"],
    ["Reusability", "Copy-paste between projects", "26 composable skills"],
    ["Quality Gates", "Manual review only", "Automated hooks + agent handoffs"],
    ["Parallelism", "Sequential only", "Fan-out to multiple agents"],
    ["Memory", "Stateless per session", "Shared decisions + journal"],
    ["Onboarding", "Read the whole prompt", "Role-based training paths"],
    ["Scalability", "Breaks at complexity", "Scales with team size"],
]
add_table(slide, Inches(0.55), Inches(1.4), Inches(12.1), rows,
          [Inches(2.2), Inches(3.75), Inches(6.15)], row_height=0.48)
add_speaker_notes(slide, """SPEAKER NOTES - Slide 5: Head-to-head
Use this as the clean comparison slide for executives.
Every row translates a prompting weakness into an orchestration strength: specialization, reuse, memory, scale, and governance.
The key message: squad is not just a nicer UX, it is a better system design.""")

# ════════════════════════════════════════════════════════════
# SLIDE 6 — THE LAYERED ARCHITECTURE
# ════════════════════════════════════════════════════════════
slide = add_slide(prs)
set_white_bg(slide)
add_title_bar(slide, prs, "The 5-Layer Architecture")
add_footer(slide, prs, 6, TOTAL_SLIDES)

layers = [
    (1, ACCENT1, "Orchestration Layer", "Routing, hooks, quality gates", Inches(2.0)),
    (2, ACCENT2, "Chatmode Layer", "7 conversation modes", Inches(2.75)),
    (3, ACCENT3, "Prompt Layer", "21 prompts + Interactive Interview", Inches(3.5)),
    (4, ACCENT5, "Agent Layer", "14 specialized squad members with charters", Inches(4.25)),
    (5, ACCENT6, "Skills Layer", "26 reusable knowledge modules", Inches(5.0)),
]
for number, color, title, detail, top in layers:
    add_box(slide, Inches(1.2), top, Inches(10.8), Inches(0.58), f"{title} — {detail}", color, font_size=16)
    add_circle(slide, Inches(0.45), top + Inches(0.06), Inches(0.44), color, str(number), font_size=12)

add_text(slide, Inches(1.15), Inches(5.9), Inches(10.9), Inches(0.35),
         "Bottom layers are reusable assets. Top layers enforce flow, ownership, and quality.",
         font_size=14, color=SUBTITLE, alignment=PP_ALIGN.CENTER)
add_speaker_notes(slide, """SPEAKER NOTES - Slide 6: The layered architecture
Explain that squad is layered by design.
Skills capture durable knowledge, agents own execution, prompts structure tasks, chatmodes define user journeys, and orchestration governs routing and validation.
Architects should see this as a composable platform, not a pile of prompts.""")

# ════════════════════════════════════════════════════════════
# SLIDE 7 — AGENT ROSTER
# ════════════════════════════════════════════════════════════
slide = add_slide(prs)
set_white_bg(slide)
add_title_bar(slide, prs, "Meet the Crew 🎬")
add_footer(slide, prs, 7, TOTAL_SLIDES)

rows = [
    ["#", "Agent", "Alias", "Domain"],
    ["1", "Architect", "Danny Ocean", "Lead strategist"],
    ["2", "Coder", "Rusty Ryan", "Full-stack dev"],
    ["3", "Tester", "Linus Caldwell", "QA + DevRel"],
    ["4", "Azure Specialist", "Basher Tarr", "Cloud platform"],
    ["5", "DevOps Engineer", "Turk Malloy", "CI/CD pipelines"],
    ["6", "Observability", "Livingston Dell", "Monitoring"],
    ["7", "Database", "The Amazing Yen", "Data migration"],
    ["8", "Performance", "Virgil Malloy", "Benchmarks"],
    ["9", "Security Auditor", "Frank Catton", "Vuln scanning"],
    ["10", "Evaluator", "Saul Bloom", "Prompt quality"],
    ["11", "Cutover Commander", "Reuben Tishkoff", "Go-live"],
    ["12", "Scribe", "Roman Nagel", "Documentation"],
    ["13", "Presentation Specialist", "Tess Ocean", "PPTX & Visual Communication"],
    ["14", "Cost Engineer", "The Accountant", "FinOps & Cost Optimization"],
]
add_table(slide, Inches(0.55), Inches(1.28), Inches(12.1), rows,
          [Inches(0.55), Inches(3.0), Inches(3.15), Inches(5.4)], row_height=0.31)
add_speaker_notes(slide, """SPEAKER NOTES - Slide 7: Meet the crew
This slide makes the operating model human and memorable.
Each agent owns one domain, which reduces role confusion and prevents one prompt from acting like a god-object.
Use the aliases to keep the deck sticky, but anchor the value in functional ownership.""")

# ════════════════════════════════════════════════════════════
# SLIDE 8 — SKILLS COMPOSITION
# ════════════════════════════════════════════════════════════
slide = add_slide(prs)
set_white_bg(slide)
add_title_bar(slide, prs, "Composable Skills: Build Once, Use Everywhere")
add_footer(slide, prs, 8, TOTAL_SLIDES)

add_column_card(slide, Inches(0.6), Inches(1.55), Inches(3.95), Inches(3.35),
                "Phase 1 — Assessment", [
                    "dotnet-upgrade-paths",
                    "azure-app-service",
                    "code-analysis-patterns",
                    "Fast intake without rewriting guidance"
                ], ACCENT2)
add_column_card(slide, Inches(4.68), Inches(1.55), Inches(3.95), Inches(3.35),
                "Security Hardening", [
                    "owasp-top-10",
                    "azure-key-vault",
                    "identity-auth-patterns",
                    "Reuse the same security blocks across apps"
                ], GREEN)
add_column_card(slide, Inches(8.76), Inches(1.55), Inches(3.95), Inches(3.35),
                "Database Migration", [
                    "ef-core-migration",
                    "azure-sql-patterns",
                    "data-validation",
                    "Swap data strategy without duplicating prompts"
                ], ACCENT3)
add_text(slide, Inches(1.25), Inches(5.45), Inches(10.7), Inches(0.45),
         "26 skills × 20 prompts = Infinite combinations without duplication",
         font_size=20, color=BODY_TEXT, bold=True, alignment=PP_ALIGN.CENTER, font_name="Aptos Display")
add_speaker_notes(slide, """SPEAKER NOTES - Slide 8: Skills composition
Make the reuse story concrete.
Skills are the Lego bricks. Prompts are the assembly instructions. Agents are the specialists who execute the work.
That means the team can change one skill once and improve every workflow that references it.""")

# ════════════════════════════════════════════════════════════
# SLIDE 9 — ORCHESTRATION FLOW
# ════════════════════════════════════════════════════════════
slide = add_slide(prs)
set_white_bg(slide)
add_title_bar(slide, prs, "How a Migration Actually Runs")
add_footer(slide, prs, 9, TOTAL_SLIDES)

flow_y = Inches(2.65)
box_w = Inches(1.78)
step_texts = [
    "1. User selects\nchatmode",
    "2. Orchestrator\nroutes to prompt",
    "3. Prompt\nloads skills",
    "4. Agent executes\nwith charter",
    "5. Hooks validate\noutput",
    "6. Handoff to\nnext agent",
]
step_colors = [SLATE, ACCENT2, ACCENT6, GREEN, ACCENT3, ACCENT5]
step_x = [Inches(0.45), Inches(2.45), Inches(4.45), Inches(6.45), Inches(8.45), Inches(10.45)]
for i in range(6):
    add_box(slide, step_x[i], flow_y, box_w, Inches(0.9), step_texts[i], step_colors[i], font_size=12)
    if i < 5:
        add_arrow(slide, step_x[i] + box_w + Inches(0.08), flow_y + Inches(0.33), Inches(0.24), ACCENT2)

loop_y = Inches(4.55)
add_text(slide, Inches(4.85), Inches(5.25), Inches(3.6), Inches(0.25),
         "Feedback loop", font_size=11, color=SUBTITLE, alignment=PP_ALIGN.CENTER)
loop_line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(11.22), Inches(3.58), Inches(0.04), Inches(1.15))
loop_line.fill.solid(); loop_line.fill.fore_color.rgb = ACCENT2; loop_line.line.fill.background()
loop_line2 = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(2.95), loop_y, Inches(8.29), Inches(0.04))
loop_line2.fill.solid(); loop_line2.fill.fore_color.rgb = ACCENT2; loop_line2.line.fill.background()
up_arrow = slide.shapes.add_shape(MSO_SHAPE.UP_ARROW, Inches(2.95), Inches(4.06), Inches(0.26), Inches(0.74))
up_arrow.fill.solid(); up_arrow.fill.fore_color.rgb = ACCENT2; up_arrow.line.fill.background(); up_arrow.shadow.inherit = False
add_speaker_notes(slide, """SPEAKER NOTES - Slide 9: Orchestration flow
This is the runtime picture.
The user chooses the journey, the orchestrator selects the right prompt, the prompt loads reusable skills, the right agent executes, hooks validate, and then work hands off to the next specialist.
The feedback loop matters because failures do not disappear; they route back into the system.""")

# ════════════════════════════════════════════════════════════
# SLIDE 10 — USE CASE MAP
# ════════════════════════════════════════════════════════════
slide = add_slide(prs)
set_white_bg(slide)
add_title_bar(slide, prs, "7 Targets, 1 Playbook")
add_footer(slide, prs, 10, TOTAL_SLIDES)

rows = [
    ["Target", "Codename", "Stack", "Key Agents"],
    ["ASP Classic", "The Antique", "VBScript → .NET 8", "Architect, Coder, DB"],
    [".NET 3.0", "The Fossil", "WebForms → Razor", "Coder, Azure, DevOps"],
    ["WCF 3.5", "The Wire", "SOAP → REST", "Architect, Security"],
    ["Contoso U", "The Campus", "MVC → Modern", "Coder, Tester, DB"],
    ["BookShop", "The Vault", "WebForms → Containers", "All 14 agents"],
    ["Java 8", "The Express", "Maven → Container Apps", "Coder, Azure, DevOps"],
    ["Parts Unlimited", "The Machine", "ASP.NET 4.5 → Modern", "Coder, Perf, DevOps"],
]
add_table(slide, Inches(0.55), Inches(1.42), Inches(12.1), rows,
          [Inches(2.05), Inches(2.1), Inches(3.2), Inches(4.75)], row_height=0.46)
add_speaker_notes(slide, """SPEAKER NOTES - Slide 10: Use-case map
Show that one architecture can cover very different migration targets without collapsing into a generic blob.
The playbook is shared, but the active crew shifts by stack and risk profile.
That is exactly why orchestration is superior to one mega-prompt.""")

# ════════════════════════════════════════════════════════════
# SLIDE 11 — QUALITY GATES
# ════════════════════════════════════════════════════════════
slide = add_slide(prs)
set_white_bg(slide)
add_title_bar(slide, prs, "Built-In Quality: No More 'Hope It Works'")
add_footer(slide, prs, 11, TOTAL_SLIDES)

add_column_card(slide, Inches(0.6), Inches(1.55), Inches(3.95), Inches(3.9),
                "Pre-Migration", [
                    "Assessment validation",
                    "Dependency scan",
                    "Risk scoring",
                    "Go / no-go clarity before work starts"
                ], GREEN)
add_column_card(slide, Inches(4.68), Inches(1.55), Inches(3.95), Inches(3.9),
                "During Migration", [
                    "Agent handoff verification",
                    "Automated testing",
                    "Security scan",
                    "Issues surface before the next phase"
                ], ACCENT2)
add_column_card(slide, Inches(8.76), Inches(1.55), Inches(3.95), Inches(3.9),
                "Post-Migration", [
                    "Performance benchmarks",
                    "Smoke tests",
                    "Cost analysis",
                    "Operational confidence after cutover"
                ], ACCENT1)
add_speaker_notes(slide, """SPEAKER NOTES - Slide 11: Quality gates
This is where architects should lean in.
Monolithic prompting tends to rely on best effort. Squad introduces explicit gates before, during, and after migration.
That means quality is built into the workflow instead of being checked at the end when it is expensive.""")

# ════════════════════════════════════════════════════════════
# SLIDE 12 — METRICS THAT MATTER
# ════════════════════════════════════════════════════════════
slide = add_slide(prs)
set_white_bg(slide)
add_title_bar(slide, prs, "Measurable Impact")
add_footer(slide, prs, 12, TOTAL_SLIDES)

add_metric_card(slide, Inches(0.6), Inches(1.8), Inches(2.9), Inches(2.2), "14", "Specialized agents", "vs 1 generic prompt", ACCENT2)
add_metric_card(slide, Inches(3.75), Inches(1.8), Inches(2.9), Inches(2.2), "26", "Reusable skills", "vs copy-paste", GREEN)
add_metric_card(slide, Inches(6.9), Inches(1.8), Inches(2.9), Inches(2.2), "7", "Chatmodes", "vs 1 monolithic mode", ACCENT3)
add_metric_card(slide, Inches(10.05), Inches(1.8), Inches(2.9), Inches(2.2), "21", "Targeted prompts", "vs 1 mega-prompt", ACCENT5)
add_text(slide, Inches(1.2), Inches(4.85), Inches(10.9), Inches(0.55),
         "Each component is independently testable, version-controlled, and team-assignable",
         font_size=18, color=BODY_TEXT, bold=True, alignment=PP_ALIGN.CENTER, font_name="Aptos Display")
add_speaker_notes(slide, """SPEAKER NOTES - Slide 12: Metrics
These are architecture metrics, not vanity metrics.
Every number represents a unit of modularity and control: more agents, more skills, more task-specific prompts, more user journeys.
The result is a system that can be versioned, tested, and assigned like real engineering work.""")

# ════════════════════════════════════════════════════════════
# SLIDE 13 — FOR THE ARCHITECT
# ════════════════════════════════════════════════════════════
slide = add_slide(prs)
set_white_bg(slide)
add_title_bar(slide, prs, "Why Architects Should Care")
add_footer(slide, prs, 13, TOTAL_SLIDES)

for left, color, icon, title, body in [
    (Inches(0.6), ACCENT2, "SOC", "Separation of Concerns", "Each agent owns ONE domain. No god-objects, no god-prompts."),
    (Inches(4.68), GREEN, "LGO", "Composability", "Skills snap together like LEGO. Prompts reference skills. Agents execute prompts."),
    (Inches(8.76), ACCENT5, "GOV", "Governance", "Every decision logged. Every handoff tracked. Every output validated."),
]:
    add_card(slide, left, Inches(1.7), Inches(3.95), Inches(3.6), bg_color=WHITE)
    add_accent_line(slide, left, Inches(1.7), Inches(3.95), color, inside=True)
    add_circle(slide, left + Inches(1.55), Inches(2.0), Inches(0.62), color, icon, font_size=12)
    add_text(slide, left + Inches(0.18), Inches(2.8), Inches(3.6), Inches(0.45),
             title, font_size=16, color=color, bold=True, alignment=PP_ALIGN.CENTER, font_name="Aptos Display")
    add_text(slide, left + Inches(0.22), Inches(3.35), Inches(3.5), Inches(1.2),
             body, font_size=12, color=BODY_TEXT, alignment=PP_ALIGN.CENTER)
add_speaker_notes(slide, """SPEAKER NOTES - Slide 13: Why architects should care
Summarize the architectural payoff.
Squad respects separation of concerns, enables composition, and creates a governance trail.
That is the language architects need: cleaner boundaries, reusable building blocks, and auditable execution.""")

# ════════════════════════════════════════════════════════════
# SLIDE 14 — INTERACTIVE INTERVIEW (NEW)
# ════════════════════════════════════════════════════════════
slide = add_slide(prs)
set_white_bg(slide)
add_title_bar(slide, prs, "CLI-First: The Interactive Interview")
add_footer(slide, prs, 14, TOTAL_SLIDES)
add_section_label(slide, Inches(0.65), Inches(1.0), "New", Inches(1.0), GREEN)

# The one prompt
add_card(slide, Inches(0.6), Inches(1.55), Inches(12.0), Inches(0.65), border_color=ACCENT2, bg_color=RGBColor(0xF0, 0xF7, 0xFF))
add_text(slide, Inches(0.85), Inches(1.62), Inches(11.5), Inches(0.5),
         '@squad I have a legacy app to migrate. Let\'s plan it.', font_size=18, color=ACCENT2, bold=True, alignment=PP_ALIGN.CENTER, font_name="Aptos Display")

# Flow boxes
flow_items = [
    (Inches(0.6), ACCENT2, "1", "Squad\nInterviews"),
    (Inches(3.4), GREEN, "2", "Codebase\nScan"),
    (Inches(6.2), ACCENT3, "3", "Plan\nGenerated"),
    (Inches(9.0), ACCENT5, "4", "Phase\nNavigation"),
]
for x, color, num, label in flow_items:
    add_box(slide, x, Inches(2.7), Inches(2.5), Inches(0.9), label, color, font_size=13)
    add_circle(slide, x + Inches(1.0), Inches(2.45), Inches(0.38), color, num, font_size=11)
# Arrows between flow boxes
for x in [Inches(3.1), Inches(5.9), Inches(8.7)]:
    add_arrow(slide, x, Inches(3.08), Inches(0.3), SLATE)

# Comparison row
add_card(slide, Inches(0.6), Inches(4.15), Inches(5.7), Inches(2.1), border_color=RGBColor(0xF0, 0xC5, 0xC0), bg_color=WHITE)
add_accent_line(slide, Inches(0.6), Inches(4.15), Inches(5.7), ACCENT1, inside=True)
add_text(slide, Inches(0.8), Inches(4.35), Inches(5.3), Inches(0.32),
         "Old Way", font_size=14, color=ACCENT1, bold=True, font_name="Aptos Display")
add_multiline(slide, Inches(0.85), Inches(4.72), Inches(5.2), Inches(1.3), [
    "❌ Copy 1,000+ lines of app-specific prompts",
    "❌ Edit every prompt with your app name",
    "❌ Must know which phase to run next",
], font_size=11, color=BODY_TEXT)

add_card(slide, Inches(6.6), Inches(4.15), Inches(5.7), Inches(2.1), border_color=RGBColor(0xC0, 0xE8, 0xC5), bg_color=WHITE)
add_accent_line(slide, Inches(6.6), Inches(4.15), Inches(5.7), GREEN, inside=True)
add_text(slide, Inches(6.8), Inches(4.35), Inches(5.3), Inches(0.32),
         "New Way", font_size=14, color=GREEN, bold=True, font_name="Aptos Display")
add_multiline(slide, Inches(6.85), Inches(4.72), Inches(5.2), Inches(1.3), [
    "✅ One prompt — squad scans and builds the plan",
    "✅ Squad asks clarifying questions automatically",
    "✅ Phase table with status — just say 'run phase N'",
], font_size=11, color=BODY_TEXT)

add_speaker_notes(slide, """SPEAKER NOTES - Slide 14: Interactive Interview
This is the breakthrough UX improvement. Instead of copying hardcoded prompt files, the user types one natural language request.
The squad interviews them, scans the codebase, and generates a tailored migration plan with phases.
The user navigates phases by saying 'show phase 2' or 'run all, fan out'. No chatmode switching, no manual prompt editing.
This makes the system accessible to teams who have never used the squad before.""")

# ════════════════════════════════════════════════════════════
# SLIDE 15 — TEAM ONBOARDING PROMPTS (NEW)
# ════════════════════════════════════════════════════════════
slide = add_slide(prs)
set_white_bg(slide)
add_title_bar(slide, prs, "Team Quick Reference: Just Paste & Go")
add_footer(slide, prs, 15, TOTAL_SLIDES)

rows = [
    ["What you want", "Paste this prompt"],
    ["Meet the squad", "@squad who are you?"],
    ["Start a migration", "@squad I have a legacy app to migrate"],
    ["Assess an app", "@squad assess Use-cases/05-BookShop"],
    ["See pending phases", "@squad show me pending phases"],
    ["Run phases in parallel", "@squad run phase 0 and 1, fan out"],
    ["Security review", "@squad run a security hardening review"],
    ["Check progress", "@squad status"],
]
add_table(slide, Inches(0.55), Inches(1.35), Inches(12.1), rows,
          [Inches(3.2), Inches(8.9)], row_height=0.45)

add_text(slide, Inches(1.0), Inches(5.2), Inches(11.2), Inches(0.45),
         'Full prompt list: docs/team-onboarding-prompts.md', font_size=14, color=BLUE_TEXT, bold=True, alignment=PP_ALIGN.CENTER)
add_speaker_notes(slide, """SPEAKER NOTES - Slide 15: Team onboarding
This is the slide to share with your team. Every row is a copy-paste prompt they can use immediately.
No training required. No documentation to read first. Just paste into Copilot CLI and the squad handles routing.
Point them to docs/team-onboarding-prompts.md for the full list organized by category.""")

# ════════════════════════════════════════════════════════════
# SLIDE 16 — GETTING STARTED
# ════════════════════════════════════════════════════════════
slide = add_slide(prs)
set_white_bg(slide)
add_title_bar(slide, prs, "Start Your Own Heist")
add_footer(slide, prs, 16, TOTAL_SLIDES)

steps = [
    "Clone the repo and open in VS Code",
    'Launch Copilot CLI: type ghcs in the terminal',
    '@squad who are you? — meet the crew',
    '@squad I have a legacy app to migrate — start interview',
    "Squad scans, interviews, generates phase plan",
    "Say 'run phase N' or 'run all, fan out'",
    "Review artifacts, ask follow-ups, ship to Azure",
]
step_top = Inches(1.35)
for idx, text in enumerate(steps, start=1):
    add_step(slide, idx, step_top + Inches((idx - 1) * 0.55), text)

line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.91), Inches(1.68), Inches(0.03), Inches(3.35))
line.fill.solid(); line.fill.fore_color.rgb = ACCENT2; line.line.fill.background()
add_text(slide, Inches(0.9), Inches(5.55), Inches(6.5), Inches(0.35),
         "github.com/v-dguncet_microsoft/GHCP-PromptMigration", font_size=14, color=BLUE_TEXT, bold=True)
add_text(slide, Inches(7.2), Inches(5.5), Inches(5.0), Inches(0.55),
         "Start small: one orchestrator, a few specialists, and reusable skills. Then scale.",
         font_size=12, color=SUBTITLE, alignment=PP_ALIGN.RIGHT)
add_speaker_notes(slide, """SPEAKER NOTES - Slide 16: Getting started
End with an implementation path, not just theory.
The key change: users start with the CLI and the interactive interview, not by editing config files.
Clone, launch CLI, type one prompt, and the squad takes over. That is the onboarding story.""")

# ════════════════════════════════════════════════════════════
# SLIDE 17 — CLOSING
# ════════════════════════════════════════════════════════════
slide = add_slide(prs, 0)
# Keep template's native blue background with decorative swirls
add_footer(slide, prs, 17, TOTAL_SLIDES)

add_text(slide, Inches(0.8), Inches(1.65), Inches(11.5), Inches(0.9),
         "Don't Prompt. Orchestrate. 🎰", font_size=30, color=WHITE, bold=True, font_name="Aptos Display", alignment=PP_ALIGN.CENTER)
add_text(slide, Inches(2.0), Inches(2.7), Inches(9.3), Inches(0.45),
         "Ocean's Fourteen — The Azure Heist", font_size=18, color=RGBColor(0xC7, 0xE3, 0xFF), font_name="Aptos Display", alignment=PP_ALIGN.CENTER)
quote_box = add_card(slide, Inches(1.6), Inches(3.45), Inches(10.1), Inches(1.35), border_color=WHITE, bg_color=RGBColor(0x00, 0x5A, 0xA0))
quote_box.line.color.rgb = WHITE
add_text(slide, Inches(1.95), Inches(3.82), Inches(9.4), Inches(0.55),
         '"Fourteen specialists. Seven targets. One mission: migrate everything to Azure."',
         font_size=18, color=WHITE, bold=True, alignment=PP_ALIGN.CENTER, font_name="Aptos Display")
add_text(slide, Inches(0.8), Inches(6.15), Inches(5.0), Inches(0.3),
         "Roberto Borges | Microsoft | 2026", font_size=12, color=RGBColor(0xB7, 0xC5, 0xD8))
add_speaker_notes(slide, """SPEAKER NOTES - Slide 17: Closing
Land the message with a call to action.
The shift is from isolated prompting to orchestrated delivery.
Close by reinforcing that architects should design AI systems the same way they design software systems: modular, governed, reusable, and scalable.""")

os.makedirs(BASE_DIR, exist_ok=True)
prs.save(OUTPUT_PATH)

print(f"Generated: {OUTPUT_PATH}")
print(f"Slides: {len(prs.slides)}")
