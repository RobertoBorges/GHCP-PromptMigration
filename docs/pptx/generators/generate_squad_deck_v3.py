"""
Generate Executive PowerPoint: Copilot Squad — Factory Delivery Model
v3: Replaces generic "Real Impact" slide with Arauco real case study (2 slides)
Design: LATAM-MCSA-AccountStatus_0410.pptx template (GCS theme)
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
    add_table,
    DK1,
    DK2,
    ACCENT1,
    ACCENT2,
    ACCENT3,
    ACCENT4,
    ACCENT5,
    ACCENT6,
    SLATE,
    GREEN,
    RED,
    ORANGE,
    WHITE,
    BODY_TEXT,
    SUBTITLE,
    LIGHT_BG,
    BORDER_GRAY,
)

# ── Base directory for relative paths ──
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

TOTAL_SLIDES = 15

prs = load_template()

def add_status_dot(slide, left, top, color):
    shape = slide.shapes.add_shape(MSO_SHAPE.OVAL, left, top, Inches(0.18), Inches(0.18))
    shape.fill.solid()
    shape.fill.fore_color.rgb = color
    shape.line.fill.background()

# ════════════════════════════════════════════════════════════
# SLIDE 1 — TITLE (Blue Gradient)
# ════════════════════════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[0])
for sp in list(slide.placeholders):
    sp_elem = sp._element
    sp_elem.getparent().remove(sp_elem)

add_text(slide, Inches(0.8), Inches(1.2), Inches(11), Inches(0.5),
         "Microsoft Accelerated Factory", font_size=18, color=WHITE,
         font_name="Segoe Sans Display Semibold")
add_text(slide, Inches(0.8), Inches(2.2), Inches(11), Inches(1.0),
         "Copilot Squad", font_size=54, color=WHITE, bold=True,
         font_name="Aptos Display")
add_text(slide, Inches(0.8), Inches(3.5), Inches(11), Inches(0.6),
         "A New Delivery Model for Accelerated Factory",
         font_size=26, color=RGBColor(0xCC, 0xE5, 0xFF), font_name="Aptos Display")
add_text(slide, Inches(0.8), Inches(4.5), Inches(9), Inches(0.8),
         "Multi-agent AI orchestration enabling parallel execution,\nshared memory, and end-to-end delivery at scale.",
         font_size=15, color=RGBColor(0xB0, 0xD0, 0xF0))
add_text(slide, Inches(0.8), Inches(6.0), Inches(6), Inches(0.7),
         "Prepared for: Factory Leadership\nMay 2026  |  Classification: Internal",
         font_size=11, color=RGBColor(0x90, 0xB8, 0xE0))
add_text(slide, Inches(8.5), Inches(6.2), Inches(4), Inches(0.3),
         "bradygaster.github.io/squad", font_size=11, color=RGBColor(0xCC, 0xE5, 0xFF))
add_footer(slide, prs, 1, TOTAL_SLIDES)

# ════════════════════════════════════════════════════════════
# SLIDE 2 — EXECUTIVE SUMMARY
# ════════════════════════════════════════════════════════════
slide = add_slide(prs)
set_white_bg(slide)
add_title_bar(slide, prs, "Executive Summary")
add_footer(slide, prs, 2, TOTAL_SLIDES)

add_section_label(slide, Inches(0.5), Inches(1.0), "What is Copilot Squad?", Inches(2.5))
add_multiline(slide, Inches(0.5), Inches(1.45), Inches(5.8), Inches(4.5), [
    "Copilot Squad is an open-source multi-agent AI framework that",
    "deploys a coordinated team of specialized AI agents directly",
    "inside your code repository.",
    "",
    "  \u2022  Specialized agents (Architect, Developer, Tester, Docs,",
    "     GitOps) work in parallel \u2014 like a real engineering team",
    "",
    "  \u2022  A Coordinator routes work to the right specialist",
    "     automatically, enforcing review gates and handoffs",
    "",
    "  \u2022  Persistent shared memory means agents remember decisions,",
    "     conventions, and architecture across all sessions",
    "",
    "  \u2022  Built-in governance: reviewer lockout, file-write guards,",
    "     escalation protocols, and human oversight at every step",
    "",
    "  \u2022  Repository-native: lives as .squad/ in your repo \u2014 commit it,",
    "     clone it, share it. No external orchestration required.",
], font_size=13)

add_section_label(slide, Inches(6.8), Inches(1.0), "Why It Matters Now", Inches(2.3))
add_multiline(slide, Inches(6.8), Inches(1.45), Inches(5.8), Inches(4.5), [
    "Factory delivery is growing in complexity \u2014 more offerings,",
    "more regions, tighter timelines, higher quality bars.",
    "",
    "  \u2022  Individual Copilot usage is ad-hoc and uncoordinated \u2014",
    "     each engineer prompts independently with no shared context",
    "",
    "  \u2022  Squad shifts AI from \"individual tool\" to \"delivery model\"",
    "     that scales across teams and projects",
    "",
    "  \u2022  Featured at Microsoft Build 2026 by Brady Gaster (GitHub)",
    "     as the future of developer productivity",
    "",
    "  \u2022  Open source (MIT), installable today, compatible with",
    "     GitHub Copilot and VS Code",
    "",
    "  \u2022  Early adopters gain competitive advantage in delivery",
    "     speed, quality, and governance",
], font_size=13)

shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(6.5), Inches(1.2), Inches(0.03), Inches(5.2))
shape.fill.solid()
shape.fill.fore_color.rgb = BORDER_GRAY
shape.line.fill.background()

# ════════════════════════════════════════════════════════════
# SLIDE 3 — CURRENT CHALLENGES
# ════════════════════════════════════════════════════════════
slide = add_slide(prs)
set_white_bg(slide)
add_title_bar(slide, prs, "Current Challenges in Factory Delivery")
add_footer(slide, prs, 3, TOTAL_SLIDES)

challenges = [
    ("Fragmented Execution",
     "Work is split across multiple tools, platforms, and individuals with no unified orchestration or coordination layer.",
     ACCENT1, "\u26A1"),
    ("Sequential Bottlenecks",
     "Development \u2192 Testing \u2192 Documentation \u2192 Review runs serially. Each handoff adds latency and critical context loss.",
     ORANGE, "\U0001F517"),
    ("Knowledge Silos",
     "Critical project context, architecture decisions, and conventions live in people's heads. When people rotate, knowledge is lost.",
     ACCENT2, "\U0001F9E0"),
    ("IC Dependency",
     "Key deliverables depend on specific individual contributors. No standardized execution pattern exists across projects.",
     ACCENT5, "\U0001F464"),
    ("E2E Inefficiency",
     "End-to-end delivery lacks automation. Teams spend significant time on manual reporting, status chasing, and rework cycles.",
     RED, "\U0001F4C9"),
]

for i, (title, desc, color, icon) in enumerate(challenges):
    left = Inches(0.3 + i * 2.55)
    top = Inches(1.1)
    card = add_card(slide, left, top, Inches(2.35), Inches(5.6))
    add_accent_line(slide, left + Inches(0.05), top + Inches(0.05), Inches(2.25), color)
    add_text(slide, left + Inches(0.15), top + Inches(0.2), Inches(2.0), Inches(0.4),
             icon, font_size=28, color=color)
    add_text(slide, left + Inches(0.15), top + Inches(0.7), Inches(2.0), Inches(0.4),
             title, font_size=15, color=DK1, bold=True)
    add_text(slide, left + Inches(0.15), top + Inches(1.2), Inches(2.0), Inches(3.5),
             desc, font_size=12, color=BODY_TEXT)
    add_status_dot(slide, left + Inches(1.0), top + Inches(5.1), color)

# ════════════════════════════════════════════════════════════
# SLIDE 4 — WHAT IS COPILOT SQUAD
# ════════════════════════════════════════════════════════════
slide = add_slide(prs)
set_white_bg(slide)
add_title_bar(slide, prs, "What is Copilot Squad")
add_footer(slide, prs, 4, TOTAL_SLIDES)

add_text(slide, Inches(0.5), Inches(0.9), Inches(12), Inches(0.3),
         "A multi-agent AI team that lives inside your repository \u2014 coordinated, governed, and persistent.",
         font_size=13, color=SUBTITLE)

coord_shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(4.2), Inches(1.4), Inches(4.8), Inches(0.7))
coord_shape.fill.solid()
coord_shape.fill.fore_color.rgb = ACCENT2
coord_shape.line.fill.background()
coord_shape.shadow.inherit = False
tf = coord_shape.text_frame
p = tf.paragraphs[0]
p.text = "\U0001F3AF  COORDINATOR  \u2014  Routes work  |  Enforces gates  |  Manages handoffs"
p.font.size = Pt(12)
p.font.color.rgb = WHITE
p.font.bold = True
p.font.name = "Aptos"
p.alignment = PP_ALIGN.CENTER

agents_data = [
    ("\U0001F3DB\uFE0F Architect", "Lead / Architect", "System design, scope management,\ntrade-offs, code review", DK2),
    ("\u2328\uFE0F Developer", "Core Dev", "Feature implementation, debugging,\nruntime, file operations", ACCENT2),
    ("\U0001F9EA Tester", "Tester / QA", "Tests, quality gates, edge cases,\ncoverage, CI/CD validation", GREEN),
    ("\U0001F4D6 DevRel", "Docs / DevRel", "README, documentation, messaging,\nonboarding, examples", ACCENT3),
    ("\U0001F680 GitOps", "GitOps / Release", "Git workflow, PRs, releases,\nGitHub auth, CI/CD pipeline", ACCENT5),
    ("\U0001F4DC Scribe", "Historian", "Decision logging, session history,\nteam memory, journal updates", ACCENT6),
    ("\U0001F3A8 Presentation Specialist", "PPTX & Visual Communication", "Decks, visual storytelling,\nexecutive messaging, demos", ACCENT4),
    ("\U0001F4B0 Cost Engineer", "FinOps & Cost Optimization", "Cost modeling, right-sizing,\nbudgets, savings plans", ACCENT1),
]

for i, (name, role, desc, color) in enumerate(agents_data):
    col = i % 3
    row = i // 3
    left = Inches(0.35 + col * 2.8)
    top = Inches(2.25 + row * 1.7)
    card = add_card(slide, left, top, Inches(2.55), Inches(1.55))
    add_accent_line(slide, left + Inches(0.05), top + Inches(0.05), Inches(2.45), color)
    add_text(slide, left + Inches(0.12), top + Inches(0.12), Inches(2.3), Inches(0.3),
             name, font_size=12, color=color, bold=True)
    add_text(slide, left + Inches(0.12), top + Inches(0.42), Inches(2.3), Inches(0.22),
             role, font_size=9.5, color=SUBTITLE)
    add_text(slide, left + Inches(0.12), top + Inches(0.7), Inches(2.3), Inches(0.65),
             desc, font_size=9.5, color=BODY_TEXT)

cap_left = Inches(9.0)
add_section_label(slide, cap_left, Inches(1.4), "Key Capabilities", Inches(2.0))
capabilities = [
    "\u2713  Parallel agent execution",
    "\u2713  Persistent shared memory",
    "\u2713  Repository-native (.squad/)",
    "\u2713  Human oversight & governance",
    "\u2713  Automatic role routing",
    "\u2713  Design reviews & retrospectives",
    "\u2713  Exportable team intelligence",
]
for i, cap in enumerate(capabilities):
    add_text(slide, cap_left, Inches(1.85 + i * 0.55), Inches(3.5), Inches(0.5),
             cap, font_size=10, color=BODY_TEXT)

# ════════════════════════════════════════════════════════════
# SLIDE 5 — KEY DIFFERENTIATORS
# ════════════════════════════════════════════════════════════
slide = add_slide(prs)
set_white_bg(slide)
add_title_bar(slide, prs, "Key Differentiators")
add_footer(slide, prs, 5, TOTAL_SLIDES)

add_text(slide, Inches(0.5), Inches(0.9), Inches(12), Inches(0.3),
         "What makes Squad fundamentally different from individual Copilot usage",
         font_size=13, color=SUBTITLE)

diffs = [
    ("Parallel Execution",
     "Multiple agents fan out and work simultaneously on architecture, code, tests, and documentation. No more sequential handoffs \u2014 a team task that took days completes in hours.",
     "Individual Copilot: One task at a time, sequential",
     "Squad: 5+ agents working in parallel on the same project",
     ACCENT2),
    ("Shared Memory & Knowledge",
     "All agents read decisions.md before every task. Conventions, architecture choices, and preferences persist across sessions and compound over time.",
     "Individual Copilot: Context lost every session",
     "Squad: Memory compounds, agents get smarter over time",
     GREEN),
    ("Repository-Native Orchestration",
     "Squad lives as .squad/ in your repo. No external platforms, no SaaS dependencies. Commit it, clone it, share it \u2014 your team travels with your code.",
     "Traditional: External orchestration tools and platforms",
     "Squad: Git-native, version-controlled, zero infrastructure",
     ACCENT3),
    ("Built-in Governance",
     "Reviewer lockout, file-write guards, PII scrubbing, escalation paths, and decision logging. Rules enforced in code, not suggestions. Audit-ready from day one.",
     "Individual Copilot: Trust-based, no enforcement",
     "Squad: Governance enforced, audit-ready, accountable",
     ACCENT5),
]

for i, (title, desc, before, after, color) in enumerate(diffs):
    row = i // 2
    col = i % 2
    left = Inches(0.3 + col * 6.5)
    top = Inches(1.3 + row * 2.95)
    card = add_card(slide, left, top, Inches(6.2), Inches(2.75))
    add_accent_line(slide, left + Inches(0.05), top + Inches(0.05), Inches(6.1), color)
    add_text(slide, left + Inches(0.2), top + Inches(0.15), Inches(5.8), Inches(0.3),
             title, font_size=16, color=color, bold=True)
    add_text(slide, left + Inches(0.2), top + Inches(0.5), Inches(5.8), Inches(0.9),
             desc, font_size=12, color=BODY_TEXT)
    add_status_dot(slide, left + Inches(0.2), top + Inches(1.55), RED)
    add_text(slide, left + Inches(0.5), top + Inches(1.5), Inches(5.5), Inches(0.3),
             before, font_size=10, color=SUBTITLE)
    add_status_dot(slide, left + Inches(0.2), top + Inches(1.9), GREEN)
    add_text(slide, left + Inches(0.5), top + Inches(1.85), Inches(5.5), Inches(0.3),
             after, font_size=10, color=BODY_TEXT, bold=True)

# ════════════════════════════════════════════════════════════
# SLIDE 6 — BUSINESS VALUE
# ════════════════════════════════════════════════════════════
slide = add_slide(prs)
set_white_bg(slide)
add_title_bar(slide, prs, "Business Value for Accelerated Factory")
add_footer(slide, prs, 6, TOTAL_SLIDES)

add_text(slide, Inches(0.5), Inches(0.9), Inches(12), Inches(0.3),
         "Quantifiable impact across delivery speed, quality, and scalability",
         font_size=13, color=SUBTITLE)

kpis = [
    ("2\u20133\u00D7", "Faster Delivery", "Parallel work replaces\nsequential handoffs", ACCENT2),
    ("40%+", "Less Rework", "Built-in testing & review\nagents catch issues early", GREEN),
    ("100%", "Standardization", "Reusable templates &\nagent roles across projects", ACCENT3),
    ("\u2191 Scale", "Per Engineer", "Each engineer operates\nwith a full AI team", ACCENT5),
]

for i, (metric, label, desc, color) in enumerate(kpis):
    left = Inches(0.3 + i * 3.2)
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, Inches(1.3), Inches(2.95), Inches(2.0))
    card.fill.solid()
    card.fill.fore_color.rgb = color
    card.line.fill.background()
    card.shadow.inherit = False
    add_text(slide, left + Inches(0.15), Inches(1.4), Inches(2.65), Inches(0.6),
             metric, font_size=34, color=WHITE, bold=True, alignment=PP_ALIGN.CENTER,
             font_name="Aptos Display")
    add_text(slide, left + Inches(0.15), Inches(2.0), Inches(2.65), Inches(0.3),
             label, font_size=14, color=WHITE, bold=True, alignment=PP_ALIGN.CENTER)
    add_text(slide, left + Inches(0.15), Inches(2.4), Inches(2.65), Inches(0.6),
             desc, font_size=10, color=RGBColor(0xE8, 0xE8, 0xF0), alignment=PP_ALIGN.CENTER)

values = [
    ("Faster End-to-End Delivery",
     "Architecture, development, testing, and documentation happen in parallel. Days of sequential work complete in hours."),
    ("Increased Productivity Per Engineer",
     "Each engineer is amplified by a full squad of AI agents. Context switching eliminated \u2014 agents remember across sessions."),
    ("Reduced Rework & Higher Quality",
     "Testing agents write test cases while code is being built. Review agents catch issues before production."),
    ("Standardization Across Projects",
     "Reusable squad configs, agent charters, and skill libraries create consistent delivery across all Factory offerings."),
    ("Improved Governance & Compliance",
     "Reviewer lockout, file-write guards, decision logging provide audit-ready governance without slowing delivery."),
]

for i, (title, desc) in enumerate(values):
    col = i % 3
    row = i // 3
    left = Inches(0.3 + col * 4.25)
    top = Inches(3.6 + row * 1.65)
    card = add_card(slide, left, top, Inches(4.05), Inches(1.45))
    add_accent_line(slide, left + Inches(0.05), top + Inches(0.05), Inches(3.95), ACCENT2)
    add_text(slide, left + Inches(0.15), top + Inches(0.15), Inches(3.75), Inches(0.3),
             title, font_size=12, color=ACCENT2, bold=True)
    add_text(slide, left + Inches(0.15), top + Inches(0.45), Inches(3.75), Inches(0.85),
             desc, font_size=10, color=BODY_TEXT)

# ════════════════════════════════════════════════════════════
# SLIDE 7 — END-TO-END SCOPE COVERAGE
# ════════════════════════════════════════════════════════════
slide = add_slide(prs)
set_white_bg(slide)
add_title_bar(slide, prs, "End-to-End Scope Coverage")
add_footer(slide, prs, 7, TOTAL_SLIDES)

add_text(slide, Inches(0.5), Inches(0.9), Inches(12), Inches(0.3),
         "Agents cover the full delivery lifecycle simultaneously \u2014 not sequentially",
         font_size=13, color=SUBTITLE)

stages = [
    ("Requirements", "Architect analyzes\nscope & trade-offs", DK2),
    ("Design", "Architect + Lead\ndefine contracts", ACCENT2),
    ("Development", "Coder agents\nbuild in parallel", ACCENT5),
    ("Testing", "Tester writes cases\nfrom requirements", GREEN),
    ("Documentation", "DevRel updates\ndocs automatically", ACCENT3),
    ("Release", "GitOps manages\nPRs & deployment", ACCENT1),
]

for i, (stage, desc, color) in enumerate(stages):
    left = Inches(0.3 + i * 2.15)
    if i > 0:
        arrow = slide.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW,
                                        left - Inches(0.25), Inches(1.85), Inches(0.25), Inches(0.25))
        arrow.fill.solid()
        arrow.fill.fore_color.rgb = BORDER_GRAY
        arrow.line.fill.background()

    stage_card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, Inches(1.4), Inches(1.95), Inches(1.6))
    stage_card.fill.solid()
    stage_card.fill.fore_color.rgb = color
    stage_card.line.fill.background()
    stage_card.shadow.inherit = False
    add_text(slide, left + Inches(0.1), Inches(1.5), Inches(1.75), Inches(0.3),
             stage, font_size=13, color=WHITE, bold=True, alignment=PP_ALIGN.CENTER)
    add_text(slide, left + Inches(0.1), Inches(1.85), Inches(1.75), Inches(0.8),
             desc, font_size=10, color=RGBColor(0xE8, 0xE8, 0xF0), alignment=PP_ALIGN.CENTER)

banner = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.5), Inches(3.3), Inches(12.3), Inches(0.5))
banner.fill.solid()
banner.fill.fore_color.rgb = ACCENT2
banner.line.fill.background()
banner.shadow.inherit = False
tf = banner.text_frame
p = tf.paragraphs[0]
p.text = "\u26A1  ALL STAGES EXECUTE IN PARALLEL \u2014 NOT SEQUENTIAL"
p.font.size = Pt(16)
p.font.color.rgb = WHITE
p.font.bold = True
p.font.name = "Aptos"
p.alignment = PP_ALIGN.CENTER

pillars = [
    ("Continuous Validation",
     "Testing agents validate code as it's written. Architecture agents review design decisions in real-time. Quality is built in, not bolted on.",
     ACCENT2),
    ("Shared Feedback Loops",
     "Agents share context through decisions.md and skills. When one agent makes an architectural choice, all others immediately incorporate it.",
     GREEN),
    ("Full Lifecycle Ownership",
     "From initial requirements through deployment and documentation, the same Squad handles the entire lifecycle. No context loss. No handoff delays.",
     ACCENT5),
]

for i, (title, desc, color) in enumerate(pillars):
    left = Inches(0.3 + i * 4.25)
    card = add_card(slide, left, Inches(4.1), Inches(4.05), Inches(2.5))
    add_accent_line(slide, left + Inches(0.05), Inches(4.15), Inches(3.95), color)
    add_text(slide, left + Inches(0.2), Inches(4.3), Inches(3.65), Inches(0.3),
             title, font_size=14, color=color, bold=True)
    add_text(slide, left + Inches(0.2), Inches(4.7), Inches(3.65), Inches(1.5),
             desc, font_size=12, color=BODY_TEXT)

# ════════════════════════════════════════════════════════════
# SLIDE 8 — ARAUCO CASE STUDY: Overview & Scope
# ════════════════════════════════════════════════════════════
slide = add_slide(prs)
set_white_bg(slide)
add_title_bar(slide, prs, "\U0001F3ED  Arauco \u2014 Parallel Application Modernization with Copilot Squad", 26)
add_footer(slide, prs, 8, TOTAL_SLIDES)

# Overview section
add_section_label(slide, Inches(0.3), Inches(0.95), "Overview", Inches(1.3))

overview_items = [
    ("Client:", "Arauco Maderas Chile (forestry & wood products, $5B+ revenue)"),
    ("Engagement:", "Modernize GMC (Gesti\u00F3n de Mejora Continua) \u2014 mission-critical industrial operations"),
    ("From:", "ASP.NET WebForms 4.8 / VB.NET (legacy, 15+ years)"),
    ("To:", ".NET 10 + Blazor Server + Azure + AI capabilities"),
]

for i, (label, value) in enumerate(overview_items):
    y = Inches(1.4 + i * 0.3)
    add_text(slide, Inches(0.5), y, Inches(1.3), Inches(0.25), label, font_size=11, color=ACCENT2, bold=True)
    add_text(slide, Inches(1.8), y, Inches(6.0), Inches(0.25), value, font_size=11, color=BODY_TEXT)

# Scope at a Glance table
add_section_label(slide, Inches(0.3), Inches(2.7), "Scope at a Glance", Inches(1.8))

scope_data = [
    ["Dimension", "Legacy", "Modernized"],
    ["Pages", "134 ASPX", "132 Razor pages"],
    ["Reports", "217 RDLC templates", "495 RDLC (expanded)"],
    ["Database Objects", "442 (211 tables, 178 SPs, 39 views)", "119 DbSets mapped"],
    ["Test Coverage", "0%", "3,243 tests \u00B7 83% line coverage"],
    ["Modules", "18", "17/18 complete (94%)"],
    ["AI Capabilities", "None", "AI Search + Chat + ACR Assistant"],
]

add_table(slide, Inches(0.3), Inches(3.1), Inches(7.8), scope_data,
          [Inches(1.6), Inches(3.1), Inches(3.1)], ACCENT2)

# Key Differentiator table (right side)
add_section_label(slide, Inches(8.3), Inches(0.95), "Key Differentiator", Inches(2.0))

diff_data = [
    ["Traditional Approach", "Copilot Squad"],
    ["1 app at a time, sequential phases", "Multiple apps/modules in parallel"],
    ["8\u201312 developers over 12+ months", "20 AI agents + 1 architect"],
    ["Manual analysis of legacy code", "Automated legacy scanning & gap analysis"],
    ["Test coverage as afterthought", "Tests built alongside code (83%)"],
    ["Knowledge silos per developer", "Shared context across entire team"],
]

add_table(slide, Inches(8.3), Inches(1.35), Inches(4.7), diff_data,
          [Inches(2.35), Inches(2.35)], SLATE)

# Execution model (right side bottom)
add_section_label(slide, Inches(8.3), Inches(4.15), "Execution Model", Inches(1.8))

exec_items = [
    "\u2022  20 AI agents (DAFT Maderas Chile Squad)",
    "\u2022  Parallel across all layers: frontend, backend,",
    "   database, auth, testing, docs",
    "\u2022  6 migration waves with reusable patterns",
    "\u2022  Fan-out: single prompt triggers parallel",
    "   investigation + implementation + validation",
]
add_multiline(slide, Inches(8.3), Inches(4.55), Inches(4.5), Inches(2.5),
              exec_items, font_size=11)

# ════════════════════════════════════════════════════════════
# SLIDE 9 — ARAUCO: Outcomes & Business Impact
# ════════════════════════════════════════════════════════════
slide = add_slide(prs)
set_white_bg(slide)
add_title_bar(slide, prs, "\U0001F3ED  Arauco \u2014 Outcomes & Business Impact", 26)
add_footer(slide, prs, 9, TOTAL_SLIDES)

# Outcomes (left side)
add_section_label(slide, Inches(0.3), Inches(0.95), "Outcomes", Inches(1.3))

outcomes = [
    ("\u2705  94% module migration complete", "17 of 18 modules fully operational", GREEN),
    ("\u2705  3,243 unit tests \u2014 100% pass rate", "Zero tests at project start", GREEN),
    ("\u2705  83% line coverage", "Exceeding the 80% target", GREEN),
    ("\u2705  Dual authentication", "Entra ID + legacy local login preserved", ACCENT2),
    ("\u2705  AI-powered features added", "Search, Chat, ACR Assistant (not in legacy)", ACCENT4),
    ("\u2705  Legacy UI fidelity", "Customer-approved Color Admin theme", ACCENT3),
    ("\u2705  Continuous deployment", "CI/CD to Azure with automated validation", ACCENT5),
]

for i, (title, detail, color) in enumerate(outcomes):
    y = Inches(1.35 + i * 0.55)
    add_status_dot(slide, Inches(0.4), y + Inches(0.05), color)
    add_text(slide, Inches(0.7), y, Inches(4.5), Inches(0.25),
             title, font_size=12, color=DK1, bold=True)
    add_text(slide, Inches(0.7), y + Inches(0.25), Inches(4.5), Inches(0.2),
             detail, font_size=10, color=SUBTITLE)

# Business Impact table (right side)
add_section_label(slide, Inches(6.0), Inches(0.95), "Business Impact", Inches(1.8))

impact_data = [
    ["Metric", "Impact"],
    ["Delivery Speed", "Multi-module parallel execution vs. traditional sequential approach"],
    ["Team Efficiency", "20 specialized AI agents replace equivalent of 8\u201312 person team"],
    ["Quality", "3,243 automated tests ensure regression-free delivery"],
    ["Scalability", "Reusable patterns (migration wizards, SP contract, CQRS) for other apps"],
    ["Time to Value", "Working modules deployed to Azure continuously, not at end of project"],
    ["Risk Reduction", "Legacy behavior preserved through SP-first architecture"],
]

add_table(slide, Inches(6.0), Inches(1.35), Inches(6.8), impact_data,
          [Inches(1.5), Inches(5.3)], ACCENT2)

# Key Takeaway banner at bottom
takeaway = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.3), Inches(5.2), Inches(12.5), Inches(1.5))
takeaway.fill.solid()
takeaway.fill.fore_color.rgb = LIGHT_BG
takeaway.line.color.rgb = ACCENT2
takeaway.line.width = Pt(2)
takeaway.shadow.inherit = False

add_section_label(slide, Inches(0.5), Inches(5.3), "\U0001F3AF Key Takeaway", Inches(1.8))

add_multiline(slide, Inches(0.5), Inches(5.7), Inches(12.0), Inches(0.9), [
    "Arauco demonstrates a scalable, repeatable model for parallel application modernization. A single architect directing",
    "a 20-agent Copilot Squad delivered what traditionally requires a 10+ person team over 12+ months \u2014 with higher test",
    "coverage, continuous deployment, and AI capabilities the legacy system never had.",
    "",
    "This is not a one-app story. This is a Factory model \u2014 the same squad, patterns, and execution framework can be applied to the next customer on Day 1.",
], font_size=12, color=DK1, bold=False)

# ════════════════════════════════════════════════════════════
# SLIDE 10 — DAFT LATAM AIRLINES: Execution & Portfolio
# ════════════════════════════════════════════════════════════
slide = add_slide(prs)
set_white_bg(slide)
add_title_bar(slide, prs, "\u2708\uFE0F  LATAM Airlines Peru \u2014 AI-Powered Parallel Migration at Scale", 24)
add_footer(slide, prs, 10, TOTAL_SLIDES)

add_text(slide, Inches(0.5), Inches(0.9), Inches(12), Inches(0.3),
         "15 legacy applications modernized to Azure through coordinated AI execution \u2014 one engineer, 8 agents, full documentation",
         font_size=12, color=SUBTITLE)

# Overview panel
add_section_label(slide, Inches(0.3), Inches(1.25), "Engagement Overview", Inches(2.2))

overview_items = [
    ("Client:", "LATAM Airlines Peru \u2014 Internal IT Division"),
    ("Scope:", "15 legacy applications (.NET 4.8, VB.NET, Python, SOAP)"),
    ("Target:", "Azure App Service + Entra ID + SQL Managed Instance"),
    ("Model:", "1 engineer + 8 AI agents per wave \u2014 parallel factory execution"),
]
for i, (label, value) in enumerate(overview_items):
    y = Inches(1.65 + i * 0.28)
    add_text(slide, Inches(0.5), y, Inches(1.0), Inches(0.23), label, font_size=10, color=ACCENT2, bold=True)
    add_text(slide, Inches(1.5), y, Inches(5.5), Inches(0.23), value, font_size=10, color=BODY_TEXT)

# Execution model table (right side)
add_section_label(slide, Inches(7.2), Inches(1.25), "Parallel Factory Execution Model", Inches(3.2))

exec_data = [
    ["Phase", "What Happened", "Squad Role"],
    ["Assess", "All 15 apps scanned simultaneously for\ndependencies, auth, and compatibility", "Halc\u00F3n (Discovery) profiled\nevery app in parallel"],
    ["Golden Pattern", "Proven template extracted from OSCE\n& COMAT \u2014 auth, bindings, hardening", "Forge + Sentinel validated\nthe pattern"],
    ["Apply at Scale", "Golden Pattern applied across all\nremaining apps concurrently", "8 agents worked in parallel\nper wave"],
    ["Validate", "Automated cross-app comparison\nreports against golden baseline", "Sentinel ran validation;\nCronista documented"],
    ["Document", "Full portfolio auto-generated: READMEs,\narchitecture diagrams, status reports", "Cronista produced all\nartifacts as delivery"],
]

add_table(slide, Inches(7.2), Inches(1.65), Inches(5.8), exec_data,
          [Inches(1.2), Inches(2.3), Inches(2.3)], SLATE)

# Portfolio table (bottom left)
add_section_label(slide, Inches(0.3), Inches(2.95), "Portfolio Delivered \u2014 15 Applications", Inches(3.0))

# Split portfolio into 2 columns of apps
apps_left = [
    ["#", "Application", "Framework", "Status"],
    ["1", "Seguridad", ".NET 8.0", "\u2705 Complete"],
    ["2", "API Seguridad", ".NET 8.0", "\u2705 Complete"],
    ["3", "SIVATM", ".NET 4.8", "\u2705 Complete"],
    ["4", "OSCE", ".NET 4.8", "\u2705 Golden Ref"],
    ["5", "API Vacaciones", "Python 3.x", "\u2705 Complete"],
    ["6", "API Mensajer\u00EDa", ".NET 4.8", "\u2705 Complete"],
    ["7", "COMAT", ".NET 4.8", "\u2705 Golden Ref"],
    ["8", "SICAV", ".NET 4.8", "\u2705 Complete"],
]

apps_right = [
    ["#", "Application", "Framework", "Status"],
    ["9", "SISMOV", ".NET 4.8", "\u2705 Gold Std (95/100)"],
    ["10", "SARA", ".NET 4.8", "\u2705 Complete"],
    ["11", "GERMAN (+Carga)", ".NET 4.8/9.0", "\u2705 Complete"],
    ["12", "SolicitudesWeb", "VB.NET 4.8", "\u2705 Complete"],
    ["13", "Flydoc", ".NET 4.8", "\u2705 Complete"],
]

add_table(slide, Inches(0.3), Inches(3.35), Inches(6.7), apps_left,
          [Inches(0.4), Inches(1.7), Inches(1.3), Inches(1.6)], ACCENT2)

add_table(slide, Inches(0.3), Inches(6.0), Inches(6.7), apps_right,
          [Inches(0.4), Inches(1.7), Inches(1.3), Inches(1.6)], ACCENT2)

# Key differentiators (bottom right)
add_section_label(slide, Inches(7.2), Inches(4.95), "Why This Matters", Inches(1.8))

diff_items = [
    ("\u26A1 Parallel execution", "8 AI agents worked concurrently per wave across assessment, migration, validation, and documentation", ACCENT2),
    ("\U0001F504 Golden Pattern reuse", "One proven template replicated across 15 apps \u2014 80% identical config, only app-specific values changed", GREEN),
    ("\U0001F4CB Docs as delivery", "Full per-app documentation, cross-app comparison reports, and architecture diagrams generated inline", ACCENT3),
    ("\U0001F527 Self-correcting", "Root-cause patterns discovered once and applied preventively across the entire portfolio", ACCENT5),
]

for i, (title, desc, color) in enumerate(diff_items):
    y = Inches(5.35 + i * 0.45)
    add_status_dot(slide, Inches(7.3), y + Inches(0.03), color)
    add_text(slide, Inches(7.6), y, Inches(2.0), Inches(0.2),
             title, font_size=9, color=color, bold=True)
    add_text(slide, Inches(7.6), y + Inches(0.2), Inches(5.0), Inches(0.2),
             desc, font_size=8, color=BODY_TEXT)

# ════════════════════════════════════════════════════════════
# SLIDE 11 — DAFT LATAM AIRLINES: Outcomes & Business Impact
# ════════════════════════════════════════════════════════════
slide = add_slide(prs)
set_white_bg(slide)
add_title_bar(slide, prs, "\u2708\uFE0F  LATAM Airlines Peru \u2014 Outcomes & Business Impact", 26)
add_footer(slide, prs, 11, TOTAL_SLIDES)

# Outcomes KPI cards across top
outcome_kpis = [
    ("15", "Apps Modernized", "Legacy .NET, VB.NET, Python\nto Azure App Service", ACCENT2),
    ("14", "Azure Deployments", "Unique App Service slots\nprovisioned and validated", GREEN),
    ("42+", "Patterns Identified", "Refactoring opportunities\nacross the portfolio", ACCENT3),
    ("30\u201340", "Dev-Weeks Saved/Yr", "Through shared components\nand eliminated duplication", ACCENT5),
]

for i, (metric, label, desc, color) in enumerate(outcome_kpis):
    left = Inches(0.3 + i * 3.2)
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, Inches(1.0), Inches(2.95), Inches(1.8))
    card.fill.solid()
    card.fill.fore_color.rgb = color
    card.line.fill.background()
    card.shadow.inherit = False
    add_text(slide, left + Inches(0.15), Inches(1.1), Inches(2.65), Inches(0.5),
             metric, font_size=34, color=WHITE, bold=True, alignment=PP_ALIGN.CENTER,
             font_name="Aptos Display")
    add_text(slide, left + Inches(0.15), Inches(1.6), Inches(2.65), Inches(0.25),
             label, font_size=13, color=WHITE, bold=True, alignment=PP_ALIGN.CENTER)
    add_text(slide, left + Inches(0.15), Inches(1.95), Inches(2.65), Inches(0.5),
             desc, font_size=9, color=RGBColor(0xE8, 0xE8, 0xF0), alignment=PP_ALIGN.CENTER)

# Business Impact table
add_section_label(slide, Inches(0.3), Inches(3.0), "Business Impact", Inches(1.6))

biz_data = [
    ["Dimension", "Impact for Factory"],
    ["Delivery Speed", "Wave-based parallel delivery dramatically reduced end-to-end timeline vs. sequential app-by-app migration"],
    ["Consistency", "Every application validated against the same golden baseline \u2014 zero configuration drift across the portfolio"],
    ["Predictability", "Repeatable factory model with clear gate enforcement: Assess \u2192 Prepare \u2192 Migrate \u2192 Validate \u2192 Document"],
    ["Team Efficiency", "1 engineer + 8 AI agents replaced the need for a large multi-person migration team"],
    ["Complete Deliverables", "Full documentation portfolio delivered alongside the migration \u2014 not as a separate phase"],
    ["Code Reduction", "60\u201370% of infrastructure code duplication eliminated through shared golden patterns"],
]

add_table(slide, Inches(0.3), Inches(3.4), Inches(12.5), biz_data,
          [Inches(1.8), Inches(10.7)], ACCENT2)

# Comparison: Traditional vs DAFT
add_section_label(slide, Inches(0.3), Inches(5.65), "Traditional vs. Copilot Squad Delivery", Inches(3.5))

compare_data = [
    ["Traditional Approach", "DAFT \u2014 Copilot Squad Model"],
    ["Sequential: 1 app at a time through all phases", "Parallel: 15 apps processed concurrently in waves"],
    ["Large migration team (8\u201312 developers)", "1 engineer + 8 specialized AI agents"],
    ["Documentation as afterthought (separate phase)", "Documentation generated as part of delivery pipeline"],
    ["Knowledge locked in individual developers", "Shared context, golden patterns, cross-app intelligence"],
    ["Months of sequential work", "Weeks of parallel execution with consistent quality"],
]

add_table(slide, Inches(0.3), Inches(6.0), Inches(12.5), compare_data,
          [Inches(6.25), Inches(6.25)], SLATE)

# Success quote banner
quote = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.3), Inches(6.85), Inches(12.5), Inches(0.45))
quote.fill.solid()
quote.fill.fore_color.rgb = LIGHT_BG
quote.line.color.rgb = ACCENT2
quote.line.width = Pt(2)
quote.shadow.inherit = False
tf = quote.text_frame
p = tf.paragraphs[0]
p.text = "\"15 applications, one factory model, full documentation, consistent quality. This is ready to replicate across every Factory engagement.\""
p.font.size = Pt(11)
p.font.color.rgb = ACCENT2
p.font.bold = True
p.font.name = "Aptos"
p.alignment = PP_ALIGN.CENTER

# ════════════════════════════════════════════════════════════
# SLIDE 12 — LATAM DASHBOARD CASE STUDY
# ════════════════════════════════════════════════════════════
slide = add_slide(prs)
set_white_bg(slide)
add_title_bar(slide, prs, "Use Scenario \u2014 LATAM MCSA Dashboard", 28)
add_footer(slide, prs, 12, TOTAL_SLIDES)

add_text(slide, Inches(0.5), Inches(0.9), Inches(12), Inches(0.3),
         "Real-world Squad deployment \u2014 automating daily reporting in Accelerated Factory",
         font_size=13, color=SUBTITLE)

# Problem / Solution / Results
panels = [
    ("The Problem", [
        "1 hour/day manual PowerPoint updates",
        "219 nominations, 90 columns, $22.2M ACR",
        "Chasing PMs for slide updates daily",
        "Static slides \u2014 no search or filtering",
        "Knowledge locked in one person",
    ], RED),
    ("Squad Solution", [
        "3 Coder agents worked in parallel",
        "Architect designed the full spec",
        "React dashboard with live analytics",
        "PowerPoint export preserved",
        "Built in a single session",
    ], ACCENT2),
    ("Results", [
        "1 hour \u2192 2 minutes daily process",
        "Searchable, filterable, visual data",
        "Richer analytics for leadership",
        "Automated PowerPoint generation",
        "Anyone can run it (no dependency)",
    ], GREEN),
]

for i, (title, items, color) in enumerate(panels):
    left = Inches(0.3 + i * 4.25)
    card = add_card(slide, left, Inches(1.3), Inches(4.05), Inches(2.5), color)
    add_section_label(slide, left + Inches(0.1), Inches(1.4), title, Inches(1.8))
    add_multiline(slide, left + Inches(0.2), Inches(1.85), Inches(3.6), Inches(1.8),
                  ["  \u2022  " + item for item in items], font_size=12)

# Squad operations
add_section_label(slide, Inches(0.3), Inches(4.05), "How the Squad Operated", Inches(2.8))

squad_ops = [
    ("Architect", "Analyzed 90-column data model, defined React+Vite+Tailwind spec, chose component architecture", DK2),
    ("Coder A", "Built upload page, app shell, glassmorphism dark theme, responsive layout system", ACCENT2),
    ("Coder B", "Built executive dashboard \u2014 KPI cards, ACR donut chart, region bars, pipeline chart", ACCENT5),
    ("Coder C", "Built nominations table, project detail view, analytics page, PowerPoint export", ACCENT3),
    ("Scribe", "Logged decisions (D-001, D-002), updated JOURNAL.md with build story and steering moments", ACCENT6),
]

for i, (role, work, color) in enumerate(squad_ops):
    top = Inches(4.45 + i * 0.4)
    add_status_dot(slide, Inches(0.5), top + Inches(0.05), color)
    add_text(slide, Inches(0.8), top, Inches(1.5), Inches(0.3),
             role, font_size=11, color=color, bold=True)
    add_text(slide, Inches(2.3), top, Inches(10.0), Inches(0.3),
             work, font_size=11, color=BODY_TEXT)

# Impact banner
impact_banner = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.3), Inches(6.5), Inches(12.4), Inches(0.4))
impact_banner.fill.solid()
impact_banner.fill.fore_color.rgb = LIGHT_BG
impact_banner.line.color.rgb = ACCENT2
impact_banner.line.width = Pt(1.5)
impact_banner.shadow.inherit = False
tf = impact_banner.text_frame
p = tf.paragraphs[0]
p.text = "IMPACT:  1 hour \u2192 2 min daily  |  219 nominations searchable  |  $22.2M ACR tracked real-time"
p.font.size = Pt(11)
p.font.color.rgb = ACCENT2
p.font.bold = True
p.font.name = "Aptos"
p.alignment = PP_ALIGN.CENTER

# ════════════════════════════════════════════════════════════
# SLIDE 13 — PARADIGM SHIFT
# ════════════════════════════════════════════════════════════
slide = add_slide(prs)
set_white_bg(slide)
add_title_bar(slide, prs, "The Paradigm Shift")
add_footer(slide, prs, 13, TOTAL_SLIDES)

add_text(slide, Inches(0.5), Inches(0.9), Inches(12), Inches(0.3),
         "From prompting to orchestration \u2014 from tools to teams \u2014 from ad-hoc to standardized",
         font_size=13, color=SUBTITLE)

shifts = [
    ("From Prompting \u2192 To Orchestration",
     "Stop writing individual prompts for each task. Start directing a team of specialists that coordinate automatically.",
     "Engineer writes 50 prompts/day  \u2192  Engineer directs 1 squad",
     ACCENT2),
    ("From Tools \u2192 To Teams",
     "Stop using AI as a single-purpose tool. Start deploying AI as a multi-agent delivery team with full project coverage.",
     "1 Copilot per engineer  \u2192  1 Squad of 5\u20137 agents per engineer",
     GREEN),
    ("From Ad-hoc \u2192 To Standardized",
     "Stop relying on individual prompt engineering skill. Start using reusable agent configurations and shared skill libraries.",
     "Tribal knowledge  \u2192  Portable, version-controlled team intelligence",
     ACCENT3),
]

for i, (title, desc, metric, color) in enumerate(shifts):
    top = Inches(1.35 + i * 1.85)
    card = add_card(slide, Inches(0.3), top, Inches(12.7), Inches(1.65))
    add_accent_line(slide, Inches(0.35), top + Inches(0.05), Inches(12.6), color)
    add_text(slide, Inches(0.6), top + Inches(0.15), Inches(6.0), Inches(0.35),
             title, font_size=18, color=color, bold=True, font_name="Aptos Display")
    add_text(slide, Inches(0.6), top + Inches(0.55), Inches(7.0), Inches(0.8),
             desc, font_size=12, color=BODY_TEXT)
    metric_box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(8.2), top + Inches(0.3), Inches(4.5), Inches(1.0))
    metric_box.fill.solid()
    metric_box.fill.fore_color.rgb = color
    metric_box.line.fill.background()
    metric_box.shadow.inherit = False
    tf = metric_box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = metric
    p.font.size = Pt(13)
    p.font.color.rgb = WHITE
    p.font.bold = True
    p.font.name = "Aptos"
    p.alignment = PP_ALIGN.CENTER

# ════════════════════════════════════════════════════════════
# SLIDE 14 — RECOMMENDED NEXT STEPS
# ════════════════════════════════════════════════════════════
slide = add_slide(prs)
set_white_bg(slide)
add_title_bar(slide, prs, "Recommended Next Steps")
add_footer(slide, prs, 14, TOTAL_SLIDES)

add_text(slide, Inches(0.5), Inches(0.9), Inches(12), Inches(0.3),
         "A phased approach to adopt Copilot Squad in Accelerated Factory",
         font_size=13, color=SUBTITLE)

phases = [
    ("Phase 1: Pilot", "Q3 2026",
     ["Select 2\u20133 Factory projects for Squad pilot",
      "Equip pilot teams with Squad CLI + VS Code",
      "Measure: delivery speed, rework, satisfaction",
      "Document learnings & refine agent configs"],
     ACCENT2),
    ("Phase 2: Standardize", "Q4 2026",
     ["Define reusable Squad templates per offering",
      "Create standard agent roles for Factory",
      "Build shared skill libraries (Azure, migrations)",
      "Establish governance & review gate standards"],
     GREEN),
    ("Phase 3: Train", "Q1 2027",
     ["Train Factory teams on agent-driven workflows",
      "Create onboarding materials & best practices",
      "Establish Squad Champions program per region",
      "Host internal hackathon to build skills"],
     ACCENT3),
    ("Phase 4: Scale", "Q2 2027",
     ["Roll out Squad as standard Factory pattern",
      "Integrate metrics into delivery dashboards",
      "Extend Squad to partner-led engagements",
      "Contribute back to Squad open-source"],
     ACCENT5),
]

for i, (phase, timeline, items, color) in enumerate(phases):
    left = Inches(0.2 + i * 3.25)
    card = add_card(slide, left, Inches(1.3), Inches(3.1), Inches(5.3))
    add_accent_line(slide, left + Inches(0.05), Inches(1.35), Inches(3.0), color)

    circle = slide.shapes.add_shape(MSO_SHAPE.OVAL, left + Inches(0.15), Inches(1.5), Inches(0.45), Inches(0.45))
    circle.fill.solid()
    circle.fill.fore_color.rgb = color
    circle.line.fill.background()
    circle.shadow.inherit = False
    tf = circle.text_frame
    p = tf.paragraphs[0]
    p.text = str(i + 1)
    p.font.size = Pt(16)
    p.font.color.rgb = WHITE
    p.font.bold = True
    p.font.name = "Aptos"
    p.alignment = PP_ALIGN.CENTER

    add_text(slide, left + Inches(0.7), Inches(1.5), Inches(2.2), Inches(0.3),
             phase, font_size=15, color=color, bold=True)
    add_text(slide, left + Inches(0.7), Inches(1.85), Inches(2.2), Inches(0.25),
             timeline, font_size=11, color=SUBTITLE)

    for j, item in enumerate(items):
        add_text(slide, left + Inches(0.2), Inches(2.3 + j * 0.65), Inches(2.7), Inches(0.6),
                 "\u2022  " + item, font_size=11, color=BODY_TEXT)

# ════════════════════════════════════════════════════════════
# SLIDE 15 — CLOSING / CALL TO ACTION
# ════════════════════════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[0])
for sp in list(slide.placeholders):
    sp_elem = sp._element
    sp_elem.getparent().remove(sp_elem)

add_text(slide, Inches(0.8), Inches(0.8), Inches(11), Inches(0.4),
         "Microsoft Accelerated Factory", font_size=14, color=RGBColor(0xB0, 0xD0, 0xF0),
         font_name="Segoe Sans Display Semibold")
add_text(slide, Inches(0.8), Inches(1.6), Inches(11), Inches(1.0),
         "The Future of Factory Delivery\nis Agent-Driven.",
         font_size=42, color=WHITE, bold=True, font_name="Aptos Display")
add_text(slide, Inches(0.8), Inches(3.2), Inches(9), Inches(0.9),
         "Copilot Squad transforms how Accelerated Factory delivers.\n"
         "From individual prompting to coordinated orchestration.\n"
         "From sequential bottlenecks to parallel execution at scale.",
         font_size=16, color=RGBColor(0xCC, 0xE5, 0xFF))

ctas = [
    ("\U0001F3AF  Approve Pilot", "Select 2\u20133 projects for Q3 2026 pilot"),
    ("\U0001F465  Assign Champions", "Identify leads per region to drive adoption"),
    ("\U0001F4CA  Define Metrics", "Set success criteria for pilot measurement"),
]

for i, (title, desc) in enumerate(ctas):
    left = Inches(0.8 + i * 3.8)
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, Inches(4.5), Inches(3.5), Inches(1.3))
    card.fill.solid()
    card.fill.fore_color.rgb = RGBColor(0x15, 0x55, 0xA0)
    card.line.color.rgb = RGBColor(0x40, 0x90, 0xD0)
    card.line.width = Pt(1)
    card.shadow.inherit = False
    add_text(slide, left + Inches(0.2), Inches(4.6), Inches(3.1), Inches(0.35),
             title, font_size=14, color=WHITE, bold=True)
    add_text(slide, left + Inches(0.2), Inches(5.0), Inches(3.1), Inches(0.5),
             desc, font_size=12, color=RGBColor(0xB0, 0xD0, 0xF0))

add_text(slide, Inches(0.8), Inches(6.2), Inches(11), Inches(0.4),
         "References:  bradygaster.github.io/squad  |  Microsoft Build 2026 (Brady Gaster)  |  github.com/bradygaster/squad",
         font_size=10, color=RGBColor(0x80, 0xA0, 0xC0))
add_footer(slide, prs, 15, TOTAL_SLIDES)

# ── Save ──
OUTPUT_PATH = os.path.join(BASE_DIR, "..", "decks", "Copilot_Squad_Factory_Proposal_v3.pptx")
prs.save(OUTPUT_PATH)
print("Deck saved to: " + OUTPUT_PATH)
print("Total slides: " + str(len(prs.slides)))
