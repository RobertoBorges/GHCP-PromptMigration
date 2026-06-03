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
    ACCENT5,
    ACCENT6,
    SLATE,
    GREEN,
    BLUE_TEXT,
    WHITE,
    BODY_TEXT,
    SUBTITLE,
)
TOTAL_SLIDES = 15
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_PATH = os.path.join(BASE_DIR, "..", "decks", "Borges_Brady_Squad_Power.pptx")

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
add_text(slide, Inches(0.8), Inches(1.45), Inches(11.3), Inches(0.95),
         "The Migration Factory: Roberto Borges × Brady Squad", font_size=28, color=WHITE, bold=True, font_name="Aptos Display")
add_text(slide, Inches(0.8), Inches(2.35), Inches(11.0), Inches(0.55),
         "From Expert Knowledge to Scalable Delivery Engine", font_size=20, color=RGBColor(0xC7, 0xE3, 0xFF), font_name="Aptos Display")
add_text(slide, Inches(0.8), Inches(6.05), Inches(6.0), Inches(0.3),
         "Microsoft | Accelerated Factory | 2026", font_size=12, color=RGBColor(0xB7, 0xC5, 0xD8))
add_circle(slide, Inches(10.7), Inches(1.25), Inches(0.55), ACCENT3)
add_circle(slide, Inches(11.35), Inches(1.25), Inches(0.55), ACCENT2)
add_circle(slide, Inches(12.0), Inches(1.25), Inches(0.55), ACCENT5)
add_footer(slide, prs, 1, TOTAL_SLIDES)
add_speaker_notes(slide, """SPEAKER NOTES - Slide 1: Title
Open with a future-facing story, not a tool demo.
Position this as the evolution from expert-led migrations to a true delivery factory.
Roberto brings hard-won migration knowledge from real legacy programs. Brady brings the operating system that turns that knowledge into repeatable team execution.
The audience should leave this slide understanding that the partnership is about scale, confidence, and factory throughput.""")

# ════════════════════════════════════════════════════════════
# SLIDE 2 — THE BURNING PLATFORM
# ════════════════════════════════════════════════════════════
slide = add_slide(prs)
set_white_bg(slide)
add_title_bar(slide, prs, "Why Legacy Migration Stalls")
add_metric_card(slide, Inches(0.65), Inches(1.8), Inches(3.6), Inches(2.15), "72%", "of migrations miss deadlines", "Execution breaks when expert knowledge cannot scale", ACCENT1)
add_metric_card(slide, Inches(4.87), Inches(1.8), Inches(3.6), Inches(2.15), "3.2x", "average cost overrun", "Rework compounds when sequencing and governance are weak", ACCENT3)
add_metric_card(slide, Inches(9.09), Inches(1.8), Inches(3.6), Inches(2.15), "47%", "delivered with critical gaps", "Quality slips when teams cannot coordinate across phases", ACCENT5)
add_text(slide, Inches(1.05), Inches(5.0), Inches(11.1), Inches(0.5),
         "The problem isn't knowledge. It's orchestration at scale.",
         font_size=21, color=BODY_TEXT, bold=True, alignment=PP_ALIGN.CENTER, font_name="Aptos Display")
add_footer(slide, prs, 2, TOTAL_SLIDES)
add_speaker_notes(slide, """SPEAKER NOTES - Slide 2: The burning platform
Frame these numbers as industry patterns, not a critique of any one team.
The point is that migrations fail systemically when delivery depends on a few experts carrying too much context in their heads.
Enterprises already have smart people. What they lack is a system that can preserve knowledge, coordinate specialists, and keep quality high while moving fast.
That is the burning platform for a migration factory.""")

# ════════════════════════════════════════════════════════════
# SLIDE 3 — THE REAL COST OF STATUS QUO
# ════════════════════════════════════════════════════════════
slide = add_slide(prs)
set_white_bg(slide)
add_title_bar(slide, prs, "What Happens Without a System")
left = Inches(0.7)
card_top = Inches(1.55)
card_w = Inches(5.65)
card_h = Inches(4.75)
add_card(slide, left, card_top, card_w, card_h, border_color=RGBColor(0xF0, 0xC5, 0xC0), bg_color=WHITE)
add_accent_line(slide, left, card_top, card_w, ACCENT1, inside=True)
add_text(slide, left + Inches(0.2), card_top + Inches(0.25), card_w - Inches(0.4), Inches(0.38),
         "Without Orchestration", font_size=17, color=ACCENT1, bold=True, alignment=PP_ALIGN.CENTER, font_name="Aptos Display")
add_multiline(slide, left + Inches(0.28), card_top + Inches(0.85), card_w - Inches(0.56), Inches(3.55), [
    "Knowledge trapped in individuals",
    "Sequential execution (one expert bottleneck)",
    "No memory between sessions",
    "Quality depends on who's running it",
    "Onboarding takes weeks per new team member",
], font_size=13, color=BODY_TEXT, bullet=True)
right = Inches(6.95)
add_card(slide, right, card_top, card_w, card_h, border_color=RGBColor(0xC0, 0xE8, 0xC5), bg_color=WHITE)
add_accent_line(slide, right, card_top, card_w, GREEN, inside=True)
add_text(slide, right + Inches(0.2), card_top + Inches(0.25), card_w - Inches(0.4), Inches(0.38),
         "With Squad Orchestration", font_size=17, color=GREEN, bold=True, alignment=PP_ALIGN.CENTER, font_name="Aptos Display")
add_multiline(slide, right + Inches(0.28), card_top + Inches(0.85), card_w - Inches(0.56), Inches(3.55), [
    "Knowledge encoded in reusable skills",
    "Parallel fan-out across specialists",
    "Shared decisions and journal persist",
    "Quality enforced by hooks and gates",
    'Onboarding: clone + "@squad who are you?"',
], font_size=13, color=BODY_TEXT, bullet=True)
add_footer(slide, prs, 3, TOTAL_SLIDES)
add_speaker_notes(slide, """SPEAKER NOTES - Slide 3: Real cost of the status quo
This is the hidden tax of migration work.
Without a system, progress is fragile. It depends on who is available, what they remember, and whether the next person can reconstruct the context.
With orchestration, the same expertise becomes durable and reusable. That changes the economics of delivery, because the team no longer resets every time work changes hands.""")

# ════════════════════════════════════════════════════════════
# SLIDE 4 — ROBERTO'S FOUNDATION
# ════════════════════════════════════════════════════════════
slide = add_slide(prs)
set_white_bg(slide)
add_title_bar(slide, prs, "Roberto Borges: The Migration Playbook")
add_column_card(slide, Inches(0.7), Inches(1.55), Inches(5.65), Inches(4.55), "Battle-Tested Knowledge", [
    "7 real-world legacy stacks migrated",
    "21 phase-aware migration prompts",
    "26+ reusable modernization skills",
    "Patterns for COM, WCF, WebForms, EF, Java",
], ACCENT2)
add_column_card(slide, Inches(6.95), Inches(1.55), Inches(5.65), Inches(4.55), "Proven Migration Phases", [
    "Phase 0: Portfolio assessment",
    "Phase 1-2: Plan, assess, migrate",
    "Phase 3-4: Infrastructure + deploy",
    "Phase 5-6: CI/CD + operations",
    "Security hardening + rollback",
], GREEN)
add_text(slide, Inches(1.0), Inches(6.15), Inches(11.0), Inches(0.35),
         "This is not theory. This is operational reality.",
         font_size=18, color=BODY_TEXT, bold=True, alignment=PP_ALIGN.CENTER, font_name="Aptos Display")
add_footer(slide, prs, 4, TOTAL_SLIDES)
add_speaker_notes(slide, """SPEAKER NOTES - Slide 4: Roberto's foundation
Make it clear that Roberto's value is credibility.
These prompts and skills were not invented in a vacuum. They came from real migration work across multiple legacy stacks, where issues like COM dependencies, SOAP contracts, ViewState, EF behavior, and deployment constraints show up in production.
That foundation matters because factories only scale when the underlying playbook is real.""")

# ════════════════════════════════════════════════════════════
# SLIDE 5 — BRADY'S MULTIPLIER
# ════════════════════════════════════════════════════════════
slide = add_slide(prs)
set_white_bg(slide)
add_title_bar(slide, prs, "Brady Squad: The Operating System for Experts")
add_column_card(slide, Inches(0.7), Inches(1.55), Inches(5.65), Inches(4.55), "Orchestration Engine", [
    "14 named specialist agents",
    "Automatic routing by task type",
    "Fan-out parallelism (agents work simultaneously)",
    "Shared memory across sessions",
], ACCENT5)
add_column_card(slide, Inches(6.95), Inches(1.55), Inches(5.65), Inches(4.55), "Quality Architecture", [
    "Phase gates prevent skipping steps",
    "Agent charters define ownership",
    "Hooks trigger tests, docs, and reviews",
    "Every decision logged and traceable",
], GREEN)
add_text(slide, Inches(1.0), Inches(6.15), Inches(11.0), Inches(0.35),
         "Squad turns expertise into a team sport.",
         font_size=18, color=BODY_TEXT, bold=True, alignment=PP_ALIGN.CENTER, font_name="Aptos Display")
add_footer(slide, prs, 5, TOTAL_SLIDES)
add_speaker_notes(slide, """SPEAKER NOTES - Slide 5: Brady's multiplier
Brady's contribution is not just more AI. It is governed coordination.
The squad model makes ownership visible, enforces handoffs, preserves context, and triggers quality checks automatically.
That means expert knowledge no longer behaves like a private asset. It behaves like an operating system the whole delivery team can use.""")

# ════════════════════════════════════════════════════════════
# SLIDE 6 — THE FUSION
# ════════════════════════════════════════════════════════════
slide = add_slide(prs)
set_white_bg(slide)
add_title_bar(slide, prs, "Better Together: Ocean's Fourteen — The Azure Heist")
left_box = add_card(slide, Inches(0.75), Inches(1.7), Inches(3.0), Inches(1.1), border_color=ACCENT2, bg_color=WHITE)
add_accent_line(slide, Inches(0.75), Inches(1.7), Inches(3.0), ACCENT2, inside=True)
add_text(slide, Inches(0.95), Inches(2.0), Inches(2.6), Inches(0.38),
         "Roberto's Knowledge", font_size=17, color=ACCENT2, bold=True, alignment=PP_ALIGN.CENTER, font_name="Aptos Display")
center_box = add_card(slide, Inches(4.82), Inches(1.55), Inches(3.7), Inches(1.4), border_color=GREEN, bg_color=WHITE)
add_accent_line(slide, Inches(4.82), Inches(1.55), Inches(3.7), GREEN, inside=True)
add_text(slide, Inches(5.02), Inches(1.92), Inches(3.3), Inches(0.48),
         "Ocean's Fourteen", font_size=20, color=GREEN, bold=True, alignment=PP_ALIGN.CENTER, font_name="Aptos Display")
add_text(slide, Inches(5.1), Inches(2.36), Inches(3.15), Inches(0.28),
         "The Azure Heist", font_size=12, color=SUBTITLE, alignment=PP_ALIGN.CENTER)
right_box = add_card(slide, Inches(9.55), Inches(1.7), Inches(3.0), Inches(1.1), border_color=ACCENT5, bg_color=WHITE)
add_accent_line(slide, Inches(9.55), Inches(1.7), Inches(3.0), ACCENT5, inside=True)
add_text(slide, Inches(9.75), Inches(2.0), Inches(2.6), Inches(0.38),
         "Brady's Framework", font_size=17, color=ACCENT5, bold=True, alignment=PP_ALIGN.CENTER, font_name="Aptos Display")
add_connector(slide, Inches(3.8), Inches(2.25), Inches(4.72), Inches(2.25), ACCENT2, 2)
add_arrow(slide, Inches(4.28), Inches(2.12), Inches(0.28), ACCENT2)
add_text(slide, Inches(3.88), Inches(1.8), Inches(0.8), Inches(0.22), "FEEDS", font_size=10, color=ACCENT2, bold=True, alignment=PP_ALIGN.CENTER)
add_connector(slide, Inches(9.47), Inches(2.25), Inches(8.58), Inches(2.25), ACCENT5, 2)
left_arrow = slide.shapes.add_shape(MSO_SHAPE.LEFT_ARROW, Inches(8.82), Inches(2.12), Inches(0.28), Inches(0.25))
left_arrow.fill.solid(); left_arrow.fill.fore_color.rgb = ACCENT5; left_arrow.line.fill.background(); left_arrow.shadow.inherit = False
add_text(slide, Inches(8.55), Inches(1.8), Inches(1.05), Inches(0.22), "POWERED BY", font_size=10, color=ACCENT5, bold=True, alignment=PP_ALIGN.CENTER)
add_metric_card(slide, Inches(0.85), Inches(4.0), Inches(3.7), Inches(1.8), "14 Agents", "Named specialists", "Not one generic AI", ACCENT2)
add_metric_card(slide, Inches(4.82), Inches(4.0), Inches(3.7), Inches(1.8), "21 Prompts", "Every migration phase covered", "Assessment through operations", GREEN)
add_metric_card(slide, Inches(8.79), Inches(4.0), Inches(3.7), Inches(1.8), "37+ Skills", "Reusable knowledge", "Across all migration use cases", ACCENT5)
add_text(slide, Inches(1.2), Inches(6.08), Inches(10.9), Inches(0.32),
         "One system. Fourteen specialists. Zero gaps.",
         font_size=18, color=BODY_TEXT, bold=True, alignment=PP_ALIGN.CENTER, font_name="Aptos Display")
add_footer(slide, prs, 6, TOTAL_SLIDES)
add_speaker_notes(slide, """SPEAKER NOTES - Slide 6: The fusion
This is the key message of the deck.
Roberto supplies migration intelligence. Brady supplies the system that makes that intelligence routable, durable, and enforceable.
Together, they create something far more valuable than a prompt library or an agent framework on its own: a migration delivery engine that can scale across teams and customers.""")

# ════════════════════════════════════════════════════════════
# SLIDE 7 — FACTORY DELIVERY MODEL
# ════════════════════════════════════════════════════════════
slide = add_slide(prs)
set_white_bg(slide)
add_title_bar(slide, prs, "From Expert Tool to Factory Engine")
flow_y = Inches(2.0)
box_w = Inches(1.72)
box_h = Inches(0.82)
step_x = [Inches(0.55), Inches(2.58), Inches(4.61), Inches(6.64), Inches(8.67), Inches(10.7)]
step_texts = [
    "Customer\nIntake",
    "Squad\nInterview",
    "Automated\nAssessment",
    "Parallel\nMigration",
    "Quality\nGates",
    "Azure\nDelivery",
]
step_colors = [SLATE, ACCENT2, ACCENT6, ACCENT3, GREEN, ACCENT5]
for i in range(6):
    add_box(slide, step_x[i], flow_y, box_w, box_h, step_texts[i], step_colors[i], font_size=12)
    if i < 5:
        add_arrow(slide, step_x[i] + box_w + Inches(0.08), flow_y + Inches(0.28), Inches(0.22), ACCENT2)
add_stat_card(slide, Inches(0.85), Inches(4.2), Inches(3.75), Inches(1.65), ACCENT2, "Repeatable", "Same process, different apps, consistent results")
add_stat_card(slide, Inches(4.79), Inches(4.2), Inches(3.75), Inches(1.65), GREEN, "Measurable", "Every phase tracked, every decision logged")
add_stat_card(slide, Inches(8.73), Inches(4.2), Inches(3.75), Inches(1.65), ACCENT5, "Scalable", "Add new use cases without rebuilding the system")
add_footer(slide, prs, 7, TOTAL_SLIDES)
add_speaker_notes(slide, """SPEAKER NOTES - Slide 7: Factory delivery model
Translate the partnership into a factory story.
A factory is not just automation. It is repeatable intake, consistent assessment, parallel work, visible gates, and a reliable output.
That is why this matters for Factory delivery: the system can take more opportunities, process them with less reinvention, and preserve quality as volume grows.""")

# ════════════════════════════════════════════════════════════
# SLIDE 8 — THE AGENT ROSTER
# ════════════════════════════════════════════════════════════
slide = add_slide(prs)
set_white_bg(slide)
add_title_bar(slide, prs, "Your Migration Crew")
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
    ["9", "Security Auditor", "Frank Catton", "Vulnerability review"],
    ["10", "Evaluator", "Saul Bloom", "Prompt quality"],
    ["11", "Cutover Commander", "Reuben Tishkoff", "Go-live"],
    ["12", "Scribe", "Roman Nagel", "Documentation"],
    ["13", "Presentation Specialist", "Tess Ocean", "PPTX & Visual Communication"],
    ["14", "Cost Engineer", "The Accountant", "FinOps & Cost Optimization"],
]
add_table(slide, Inches(0.55), Inches(1.35), Inches(12.0), rows,
          [Inches(0.55), Inches(3.0), Inches(3.15), Inches(5.3)], row_height=0.28)
add_text(slide, Inches(1.0), Inches(6.05), Inches(11.0), Inches(0.28),
         "Named specialists create trust, ownership, and true parallel delivery.",
         font_size=15, color=SUBTITLE, alignment=PP_ALIGN.CENTER)
add_footer(slide, prs, 8, TOTAL_SLIDES)
add_speaker_notes(slide, """SPEAKER NOTES - Slide 8: Agent roster
This is important because it shows the system is not a single opaque AI persona.
Each specialist has a domain, which means work can be routed cleanly and reviewed with more confidence.
For Factory delivery, that matters because trust grows when people can see who owns architecture, code, testing, security, cutover, and documentation.""")

# ════════════════════════════════════════════════════════════
# SLIDE 9 — REAL USE CASES
# ════════════════════════════════════════════════════════════
slide = add_slide(prs)
set_white_bg(slide)
add_title_bar(slide, prs, "7 Legacy Stacks, 1 Playbook")
rows = [
    ["Target", "Codename", "Stack", "Difficulty"],
    ["01-ASPClassicApp", "The Antique", "Classic ASP", "High"],
    ["02-NetFramework30-ASPNET-WEB", "The Fossil", ".NET Framework 3.0", "High"],
    ["03-WCFNet35", "The Wire", "WCF .NET 3.5", "Very High"],
    ["04-ContosoUniversityDiPS", "The Campus", "ASP.NET MVC", "Medium"],
    ["05-BookShop", "The Vault", ".NET 3.5 WebForms", "Very High"],
    ["06-Java-API-BusReservation", "The Express", "Java 8 API", "Medium"],
    ["07-PartsUnlimited-aspnet45", "The Machine", "ASP.NET 4.5", "High"],
]
add_table(slide, Inches(0.55), Inches(1.45), Inches(12.0), rows,
          [Inches(3.45), Inches(2.15), Inches(3.9), Inches(2.5)], row_height=0.48)
add_text(slide, Inches(1.0), Inches(6.0), Inches(11.0), Inches(0.32),
         "Each stack validated. Each pattern encoded. Each lesson reusable.",
         font_size=18, color=BODY_TEXT, bold=True, alignment=PP_ALIGN.CENTER, font_name="Aptos Display")
add_footer(slide, prs, 9, TOTAL_SLIDES)
add_speaker_notes(slide, """SPEAKER NOTES - Slide 9: Real use cases
This is the proof point behind the persuasive story.
The playbook has already been exercised across Classic ASP, WCF, WebForms, Java, and ASP.NET estates.
That breadth is exactly what makes the factory credible: each migration teaches the system something reusable instead of forcing the next team to start from zero.""")

# ════════════════════════════════════════════════════════════
# SLIDE 10 — FACTORY ROI
# ════════════════════════════════════════════════════════════
slide = add_slide(prs)
set_white_bg(slide)
add_title_bar(slide, prs, "The Business Case")
add_stat_card(slide, Inches(0.55), Inches(1.85), Inches(2.85), Inches(2.7), ACCENT2, "Reduction in assessment time", "Automated codebase scanning + pattern matching", headline="60-80%")
add_stat_card(slide, Inches(3.62), Inches(1.85), Inches(2.85), Inches(2.7), GREEN, "Onboarding speed", "Clone repo, talk to squad, start migrating", headline="5× Faster")
add_stat_card(slide, Inches(6.69), Inches(1.85), Inches(2.85), Inches(2.7), ACCENT3, "Knowledge loss between sessions", "Shared memory, decisions journal, handoff docs", headline="Zero")
add_stat_card(slide, Inches(9.76), Inches(1.85), Inches(2.85), Inches(2.7), ACCENT5, "Phase coverage", "No step skipped, no gate bypassed", headline="100%")
add_text(slide, Inches(0.95), Inches(5.15), Inches(11.2), Inches(0.45),
         "This is how migration work moves from artisanal to industrial.",
         font_size=18, color=BODY_TEXT, bold=True, alignment=PP_ALIGN.CENTER, font_name="Aptos Display")
add_footer(slide, prs, 10, TOTAL_SLIDES)
add_speaker_notes(slide, """SPEAKER NOTES - Slide 10: Factory ROI
Now make the business case explicit.
The value is not only better technical execution. It is lower assessment cost, faster onboarding, no knowledge reset between sessions, and complete phase coverage.
That combination is what Factory leaders need: better throughput, more predictable quality, and less dependence on heroic individuals.""")

# ════════════════════════════════════════════════════════════
# SLIDE 11 — EVOLUTION ROADMAP
# ════════════════════════════════════════════════════════════
slide = add_slide(prs)
set_white_bg(slide)
add_title_bar(slide, prs, "The Path Forward: Always Evolving")
add_column_card(slide, Inches(0.55), Inches(1.55), Inches(3.9), Inches(4.8), "Today", [
    "7 use cases proven",
    "14 agents operational",
    "CLI-first UX live",
    "Interactive interview system",
], ACCENT2)
add_column_card(slide, Inches(4.72), Inches(1.55), Inches(3.9), Inches(4.8), "Next Quarter", [
    "Custom agent training per customer",
    "Self-improving prompt evaluation",
    "Multi-repo portfolio orchestration",
    "Automated compliance reporting",
], GREEN)
add_column_card(slide, Inches(8.89), Inches(1.55), Inches(3.9), Inches(4.8), "Future", [
    "Cross-team federation (multiple squads)",
    "AI-assisted architecture decisions",
    "Continuous migration-as-a-service",
    "Industry-specific migration accelerators",
], ACCENT5)
add_footer(slide, prs, 11, TOTAL_SLIDES)
add_speaker_notes(slide, """SPEAKER NOTES - Slide 11: Evolution roadmap
This slide turns the partnership from a point solution into a platform story.
The system already works today, but the more important message is that it can keep learning and expanding.
That makes it strategic for Factory growth: every customer engagement can improve the engine, widen the playbook, and strengthen the next delivery.""")

# ════════════════════════════════════════════════════════════
# SLIDE 12 — CUSTOMER IMPACT VISION
# ════════════════════════════════════════════════════════════
slide = add_slide(prs)
set_white_bg(slide)
add_title_bar(slide, prs, "What Customers Get")
add_stat_card(slide, Inches(0.7), Inches(1.85), Inches(3.75), Inches(2.45), ACCENT2, "Portfolio Assessment", "vs weeks of manual analysis", headline="1 Day")
add_stat_card(slide, Inches(4.79), Inches(1.85), Inches(3.75), Inches(2.45), GREEN, "Migration Plan", "vs months of planning cycles", headline="1 Week")
add_stat_card(slide, Inches(8.88), Inches(1.85), Inches(3.75), Inches(2.45), ACCENT5, "Team Onboarding", "vs days of training and documentation", headline="Minutes")
add_text(slide, Inches(0.95), Inches(5.1), Inches(11.2), Inches(0.6),
         "From months to days. From individuals to teams. From one-time to repeatable.",
         font_size=20, color=BODY_TEXT, bold=True, alignment=PP_ALIGN.CENTER, font_name="Aptos Display")
add_footer(slide, prs, 12, TOTAL_SLIDES)
add_speaker_notes(slide, """SPEAKER NOTES - Slide 12: Customer impact vision
Bring the story back to customer outcomes.
Customers do not buy prompts. They buy speed, confidence, continuity, and an easier path through uncertainty.
This is why the partnership matters commercially: it compresses the front end of migration work and makes expert execution available much earlier in the engagement.""")

# ════════════════════════════════════════════════════════════
# SLIDE 13 — COMPETITIVE ADVANTAGE
# ════════════════════════════════════════════════════════════
slide = add_slide(prs)
set_white_bg(slide)
add_title_bar(slide, prs, "Why This Beats Everything Else")
left = Inches(0.7)
card_top = Inches(1.55)
card_w = Inches(5.65)
card_h = Inches(4.75)
add_card(slide, left, card_top, card_w, card_h, border_color=RGBColor(0xF0, 0xC5, 0xC0), bg_color=WHITE)
add_accent_line(slide, left, card_top, card_w, ACCENT1, inside=True)
add_text(slide, left + Inches(0.2), card_top + Inches(0.25), card_w - Inches(0.4), Inches(0.38),
         "Generic AI Tools", font_size=17, color=ACCENT1, bold=True, alignment=PP_ALIGN.CENTER, font_name="Aptos Display")
add_multiline(slide, left + Inches(0.28), card_top + Inches(0.85), card_w - Inches(0.56), Inches(3.55), [
    "One-size-fits-all prompts",
    "No migration domain knowledge",
    "No memory between sessions",
    "No quality governance",
    "No team coordination",
], font_size=13, color=BODY_TEXT, bullet=True)
right = Inches(6.95)
add_card(slide, right, card_top, card_w, card_h, border_color=RGBColor(0xC0, 0xE8, 0xC5), bg_color=WHITE)
add_accent_line(slide, right, card_top, card_w, GREEN, inside=True)
add_text(slide, right + Inches(0.2), card_top + Inches(0.25), card_w - Inches(0.4), Inches(0.38),
         "Roberto + Squad", font_size=17, color=GREEN, bold=True, alignment=PP_ALIGN.CENTER, font_name="Aptos Display")
add_multiline(slide, right + Inches(0.28), card_top + Inches(0.85), card_w - Inches(0.56), Inches(3.55), [
    "Battle-tested migration patterns",
    "Deep .NET, Java, and Azure expertise",
    "Persistent shared memory",
    "Phase gates + quality hooks",
    "14 coordinated specialists",
], font_size=13, color=BODY_TEXT, bullet=True)
add_text(slide, Inches(1.0), Inches(6.12), Inches(11.0), Inches(0.3),
         "This isn't AI-assisted migration. This is AI-orchestrated delivery.",
         font_size=18, color=BODY_TEXT, bold=True, alignment=PP_ALIGN.CENTER, font_name="Aptos Display")
add_footer(slide, prs, 13, TOTAL_SLIDES)
add_speaker_notes(slide, """SPEAKER NOTES - Slide 13: Competitive advantage
This is where the positioning gets sharp.
Many AI tools can generate text. Very few can carry migration-specific knowledge, preserve team context, enforce phases, and coordinate specialists as a delivery model.
That is the difference between assistance and orchestration, and it is the foundation of the competitive advantage.""")

# ════════════════════════════════════════════════════════════
# SLIDE 14 — GETTING STARTED
# ════════════════════════════════════════════════════════════
slide = add_slide(prs)
set_white_bg(slide)
add_title_bar(slide, prs, "Start Today")
steps = [
    "Clone the repo",
    "Launch Copilot CLI",
    "@squad who are you?",
    "@squad I have a legacy app to migrate",
    "Squad handles the rest",
]
step_top = Inches(1.55)
for idx, text in enumerate(steps, start=1):
    add_step(slide, idx, step_top + Inches((idx - 1) * 0.72), text)
line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.91), Inches(1.88), Inches(0.03), Inches(2.95))
line.fill.solid(); line.fill.fore_color.rgb = ACCENT2; line.line.fill.background()
add_text(slide, Inches(0.9), Inches(5.55), Inches(6.8), Inches(0.35),
         "https://github.com/RobertoBorges/GHCP-PromptMigration", font_size=14, color=BLUE_TEXT, bold=True)
add_card(slide, Inches(7.55), Inches(2.1), Inches(4.7), Inches(2.2), border_color=RGBColor(0xC0, 0xE8, 0xC5), bg_color=WHITE)
add_accent_line(slide, Inches(7.55), Inches(2.1), Inches(4.7), GREEN, inside=True)
add_text(slide, Inches(7.8), Inches(2.45), Inches(4.2), Inches(0.38),
         "Why it matters", font_size=16, color=GREEN, bold=True, alignment=PP_ALIGN.CENTER, font_name="Aptos Display")
add_text(slide, Inches(7.82), Inches(3.02), Inches(4.15), Inches(0.92),
         "No prompt memorization. No phase guessing. Just start the conversation.",
         font_size=13, color=SUBTITLE, alignment=PP_ALIGN.CENTER)
add_footer(slide, prs, 14, TOTAL_SLIDES)
add_speaker_notes(slide, """SPEAKER NOTES - Slide 14: Getting started
End the operational story with low friction.
The factory is persuasive only if people believe they can enter it easily.
That is why the starting motion is simple: clone, launch, ask who the squad is, describe the legacy app, and let the system route the work.
Simple entry is how scalable delivery becomes adoptable delivery.""")

# ════════════════════════════════════════════════════════════
# SLIDE 15 — CLOSING
# ════════════════════════════════════════════════════════════
slide = add_slide(prs, 0)
# Keep template's native blue background with decorative swirls
add_text(slide, Inches(0.8), Inches(1.45), Inches(11.7), Inches(0.65),
         "Don't Just Migrate. Transform. 🚀", font_size=28, color=WHITE, bold=True, font_name="Aptos Display", alignment=PP_ALIGN.CENTER)
add_text(slide, Inches(2.8), Inches(2.35), Inches(7.8), Inches(0.35),
         "Roberto Borges × Brady Squad", font_size=18, color=RGBColor(0xC7, 0xE3, 0xFF), font_name="Aptos Display", alignment=PP_ALIGN.CENTER)
quote_box = add_card(slide, Inches(1.55), Inches(3.15), Inches(10.25), Inches(1.6), border_color=WHITE, bg_color=RGBColor(0x00, 0x5A, 0xA0))
quote_box.line.color.rgb = WHITE
add_text(slide, Inches(1.9), Inches(3.55), Inches(9.55), Inches(0.85),
         '"The best migration factory is a team that never forgets, never gets tired, and always follows the plan — then gets smarter every time."',
         font_size=17, color=WHITE, bold=True, alignment=PP_ALIGN.CENTER, font_name="Aptos Display")
add_text(slide, Inches(0.8), Inches(6.15), Inches(6.0), Inches(0.3),
         "Roberto Borges | Microsoft | Accelerated Factory | 2026", font_size=12, color=RGBColor(0xB7, 0xC5, 0xD8))
add_footer(slide, prs, 15, TOTAL_SLIDES)
add_speaker_notes(slide, """SPEAKER NOTES - Slide 15: Closing
Finish with the transformation message.
The ask is not to migrate one more app with a clever prompt. The ask is to build a migration factory that compounds knowledge, keeps quality high, and improves with every engagement.
That is why Roberto Borges and Brady Squad are powerful together: one brings the playbook, the other turns it into a scalable engine for Factory growth.""")

os.makedirs(BASE_DIR, exist_ok=True)
prs.save(OUTPUT_PATH)

print(f"Generated: {OUTPUT_PATH}")
print(f"Slides: {len(prs.slides)}")
