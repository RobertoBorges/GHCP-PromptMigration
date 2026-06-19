"""Shared LATAM GCS palette and slide helpers for squad PPTX generators."""

import os

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN
from pptx.oxml.ns import qn
from pptx.util import Inches, Pt

# Template path: set LATAM_TEMPLATE_PATH env var, or use default
TEMPLATE_PATH = os.environ.get(
    "LATAM_TEMPLATE_PATH",
    r"C:\Users\v-dguncet\source\repos\LATAM Deck possible to automate\docs\LATAM-MCSA-AccountStatus_0410.pptx",
)

# ── GCS Theme Colors (from LATAM-MCSA-AccountStatus_0410.pptx) ──
DK1 = RGBColor(0x1A, 0x1A, 0x1A)
LT1 = RGBColor(0xFF, 0xFF, 0xFF)
DK2 = RGBColor(0x2A, 0x44, 0x6F)
LT2 = RGBColor(0xF2, 0xF2, 0xF2)
ACCENT1 = RGBColor(0xD8, 0x3B, 0x02)
ACCENT2 = RGBColor(0x01, 0x78, 0xD4)
ACCENT3 = RGBColor(0xFE, 0x8B, 0x00)
ACCENT4 = RGBColor(0x00, 0xBC, 0xF2)
ACCENT5 = RGBColor(0x46, 0x36, 0x68)
ACCENT6 = RGBColor(0x22, 0x5B, 0x62)

# ── Extended palette ──
SLATE = RGBColor(0x4A, 0x4E, 0x66)
GREEN = RGBColor(0x00, 0xB0, 0x50)
RED = RGBColor(0xEE, 0x00, 0x00)
AMBER = RGBColor(0xFF, 0xC0, 0x00)
ORANGE = RGBColor(0xED, 0x7D, 0x31)
BLUE_TEXT = RGBColor(0x00, 0x70, 0xC0)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
BLACK = RGBColor(0x00, 0x00, 0x00)
BODY_TEXT = RGBColor(0x33, 0x33, 0x33)
SUBTITLE = RGBColor(0x66, 0x66, 0x66)
LIGHT_BG = RGBColor(0xF2, 0xF7, 0xFA)
CARD_BG = RGBColor(0xF8, 0xF8, 0xFA)
BORDER_GRAY = RGBColor(0xD0, 0xD0, 0xD8)
DARK_BG = RGBColor(0x1E, 0x29, 0x3B)


def load_template(template_path=TEMPLATE_PATH):
    if not os.path.exists(template_path):
        raise FileNotFoundError(
            f"PPTX template not found: {template_path}\n"
            "Set LATAM_TEMPLATE_PATH environment variable to the correct path.\n"
            "See docs/pptx/README.md for setup instructions."
        )
    prs = Presentation(template_path)
    while len(prs.slides) > 0:
        rel_id = prs.slides._sldIdLst[0].get(qn("r:id"))
        prs.part.drop_rel(rel_id)
        prs.slides._sldIdLst.remove(prs.slides._sldIdLst[0])
    return prs


def add_slide(prs, layout_index=6):
    layout = prs.slide_layouts[layout_index]
    slide = prs.slides.add_slide(layout)
    for placeholder in list(slide.placeholders):
        placeholder_element = placeholder._element
        placeholder_element.getparent().remove(placeholder_element)
    return slide


def set_white_bg(slide):
    fill = slide.background.fill
    fill.solid()
    fill.fore_color.rgb = WHITE


def set_dark_bg(slide):
    fill = slide.background.fill
    fill.solid()
    fill.fore_color.rgb = DARK_BG


def add_title_bar(slide, prs, text, font_size=28):
    shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, Inches(0.1), prs.slide_width, Inches(0.65))
    shape.fill.solid()
    shape.fill.fore_color.rgb = ACCENT2
    shape.line.fill.background()
    shape.shadow.inherit = False

    text_frame = shape.text_frame
    text_frame.word_wrap = True
    paragraph = text_frame.paragraphs[0]
    paragraph.text = text
    paragraph.font.size = Pt(font_size)
    paragraph.font.color.rgb = WHITE
    paragraph.font.bold = True
    paragraph.font.name = "Aptos Display"
    paragraph.alignment = PP_ALIGN.LEFT
    return shape


def add_section_label(slide, left, top, text, width=None, color=SLATE):
    label_width = width or Inches(len(text) * 0.11 + 0.5)
    shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, label_width, Inches(0.30))
    shape.fill.solid()
    shape.fill.fore_color.rgb = color
    shape.line.fill.background()
    shape.shadow.inherit = False

    text_frame = shape.text_frame
    text_frame.word_wrap = False
    text_frame.margin_left = Pt(6)
    text_frame.margin_right = Pt(6)
    paragraph = text_frame.paragraphs[0]
    paragraph.text = text
    paragraph.font.size = Pt(11)
    paragraph.font.color.rgb = WHITE
    paragraph.font.bold = True
    paragraph.font.name = "Aptos"
    return shape


def add_text(slide, left, top, width, height, text, font_size=14, color=BODY_TEXT, bold=False, alignment=PP_ALIGN.LEFT, font_name="Aptos"):
    text_box = slide.shapes.add_textbox(left, top, width, height)
    text_frame = text_box.text_frame
    text_frame.word_wrap = True
    paragraph = text_frame.paragraphs[0]
    paragraph.text = text
    paragraph.font.size = Pt(font_size)
    paragraph.font.color.rgb = color
    paragraph.font.bold = bold
    paragraph.font.name = font_name
    paragraph.alignment = alignment
    return text_frame


def add_multiline(slide, left, top, width, height, lines, font_size=12, color=BODY_TEXT, bold=False, line_spacing=Pt(4), bullet=False):
    text_box = slide.shapes.add_textbox(left, top, width, height)
    text_frame = text_box.text_frame
    text_frame.word_wrap = True

    for index, line in enumerate(lines):
        paragraph = text_frame.paragraphs[0] if index == 0 else text_frame.add_paragraph()
        prefix = chr(8226) + "  " if bullet else ""
        paragraph.text = prefix + line
        paragraph.font.size = Pt(font_size)
        paragraph.font.color.rgb = color
        paragraph.font.bold = bold
        paragraph.font.name = "Aptos"
        paragraph.space_after = line_spacing
    return text_frame


def add_card(slide, left, top, width, height, border_color=BORDER_GRAY, bg_color=CARD_BG):
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = bg_color
    shape.line.color.rgb = border_color
    shape.line.width = Pt(1)
    shape.shadow.inherit = False
    # Set a tight corner radius so accent lines don't overlap the curve
    from pptx.oxml.ns import qn as _qn
    sp_pr = shape._element.spPr
    prst = sp_pr.find(_qn('a:prstGeom'))
    if prst is not None:
        avLst = prst.find(_qn('a:avLst'))
        if avLst is None:
            from lxml import etree
            avLst = etree.SubElement(prst, _qn('a:avLst'))
        else:
            avLst.clear()
        from lxml import etree
        gd = etree.SubElement(avLst, _qn('a:gd'))
        gd.set('name', 'adj')
        gd.set('fmla', 'val 6000')  # ~3.6% corner radius
    return shape


def add_accent_line(slide, left, top, width, color=ACCENT2, inside=False):
    """Draw accent line. If inside=True, offsets down to sit inside a rounded card."""
    y = top + Inches(0.08) if inside else top
    x = left + (Inches(0.08) if inside else 0)
    w = width - (Inches(0.16) if inside else 0)
    shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, y, w, Inches(0.05))
    shape.fill.solid()
    shape.fill.fore_color.rgb = color
    shape.line.fill.background()
    return shape


def add_footer(slide, prs, slide_num, total_slides, footer_text=""):
    if footer_text:
        add_text(
            slide,
            Inches(0.35),
            Inches(6.85),
            prs.slide_width - Inches(2.2),
            Inches(0.3),
            footer_text,
            font_size=8,
            color=SUBTITLE,
        )
    add_text(
        slide,
        prs.slide_width - Inches(1.5),
        Inches(6.85),
        Inches(1.3),
        Inches(0.3),
        f"{slide_num} / {total_slides}",
        font_size=8,
        color=SUBTITLE,
        alignment=PP_ALIGN.RIGHT,
    )


def add_table(slide, left, top, width, rows_data, col_widths, header_color=ACCENT2, row_height=0.28):
    rows = len(rows_data)
    cols = len(rows_data[0])
    table_shape = slide.shapes.add_table(rows, cols, left, top, width, Inches(rows * row_height))
    table = table_shape.table

    for column_index, column_width in enumerate(col_widths):
        table.columns[column_index].width = column_width

    for row_index, row in enumerate(rows_data):
        for column_index, cell_text in enumerate(row):
            cell = table.cell(row_index, column_index)
            cell.text = cell_text
            for paragraph in cell.text_frame.paragraphs:
                paragraph.font.size = Pt(10)
                paragraph.font.name = "Aptos"
                if row_index == 0:
                    paragraph.font.bold = True
                    paragraph.font.color.rgb = WHITE
                else:
                    paragraph.font.color.rgb = BODY_TEXT

            cell.fill.solid()
            if row_index == 0:
                cell.fill.fore_color.rgb = header_color
            elif row_index % 2 == 0:
                cell.fill.fore_color.rgb = LIGHT_BG
            else:
                cell.fill.fore_color.rgb = WHITE
    return table_shape


def add_speaker_notes(slide, notes_text):
    slide.notes_slide.notes_text_frame.text = notes_text


def add_circle(slide, left, top, size, color, text="", font_size=14):
    shape = slide.shapes.add_shape(MSO_SHAPE.OVAL, left, top, size, size)
    shape.fill.solid()
    shape.fill.fore_color.rgb = color
    shape.line.fill.background()
    shape.shadow.inherit = False

    if text:
        text_frame = shape.text_frame
        text_frame.word_wrap = True
        paragraph = text_frame.paragraphs[0]
        paragraph.text = text
        paragraph.font.size = Pt(font_size)
        paragraph.font.color.rgb = WHITE
        paragraph.font.bold = True
        paragraph.font.name = "Aptos"
        paragraph.alignment = PP_ALIGN.CENTER
    return shape


def add_column_card(slide, left, top, width, height, title, lines, accent_color):
    add_card(slide, left, top, width, height, bg_color=WHITE)
    add_accent_line(slide, left, top, width, accent_color, inside=True)
    add_text(
        slide,
        left + Inches(0.18),
        top + Inches(0.22),
        width - Inches(0.36),
        Inches(0.4),
        title,
        font_size=16,
        color=accent_color,
        bold=True,
        font_name="Aptos Display",
        alignment=PP_ALIGN.CENTER,
    )
    add_multiline(
        slide,
        left + Inches(0.22),
        top + Inches(0.8),
        width - Inches(0.44),
        height - Inches(1.0),
        lines,
        font_size=13,
        color=BODY_TEXT,
        bullet=True,
    )


def add_metric_card(slide, left, top, width, height, number, label, detail, color):
    add_card(slide, left, top, width, height, bg_color=WHITE)
    add_accent_line(slide, left, top, width, color, inside=True)
    add_text(
        slide,
        left + Inches(0.18),
        top + Inches(0.28),
        width - Inches(0.36),
        Inches(0.8),
        number,
        font_size=30,
        color=color,
        bold=True,
        font_name="Aptos Display",
        alignment=PP_ALIGN.CENTER,
    )
    add_text(
        slide,
        left + Inches(0.18),
        top + Inches(1.05),
        width - Inches(0.36),
        Inches(0.42),
        label,
        font_size=14,
        color=BODY_TEXT,
        bold=True,
        alignment=PP_ALIGN.CENTER,
    )
    add_text(
        slide,
        left + Inches(0.18),
        top + Inches(1.48),
        width - Inches(0.36),
        Inches(0.55),
        detail,
        font_size=10,
        color=SUBTITLE,
        alignment=PP_ALIGN.CENTER,
    )


def add_stat_card(slide, left, top, width, height, accent_color, title, body, headline=None):
    add_card(slide, left, top, width, height, bg_color=WHITE)
    add_accent_line(slide, left, top, width, accent_color, inside=True)
    if headline:
        add_text(
            slide,
            left + Inches(0.16),
            top + Inches(0.28),
            width - Inches(0.32),
            Inches(0.5),
            headline,
            font_size=28,
            color=accent_color,
            bold=True,
            font_name="Aptos Display",
            alignment=PP_ALIGN.CENTER,
        )
        title_top = top + Inches(0.88)
    else:
        title_top = top + Inches(0.28)

    add_text(
        slide,
        left + Inches(0.16),
        title_top,
        width - Inches(0.32),
        Inches(0.45),
        title,
        font_size=16,
        color=BODY_TEXT,
        bold=True,
        alignment=PP_ALIGN.CENTER,
    )
    add_text(
        slide,
        left + Inches(0.18),
        title_top + Inches(0.52),
        width - Inches(0.36),
        height - Inches(1.0),
        body,
        font_size=12,
        color=SUBTITLE,
        alignment=PP_ALIGN.CENTER,
    )


__all__ = [
    "TEMPLATE_PATH",
    "DK1",
    "LT1",
    "DK2",
    "LT2",
    "ACCENT1",
    "ACCENT2",
    "ACCENT3",
    "ACCENT4",
    "ACCENT5",
    "ACCENT6",
    "SLATE",
    "GREEN",
    "RED",
    "AMBER",
    "ORANGE",
    "BLUE_TEXT",
    "WHITE",
    "BLACK",
    "BODY_TEXT",
    "SUBTITLE",
    "LIGHT_BG",
    "CARD_BG",
    "BORDER_GRAY",
    "DARK_BG",
    "load_template",
    "add_slide",
    "set_white_bg",
    "set_dark_bg",
    "add_title_bar",
    "add_section_label",
    "add_text",
    "add_multiline",
    "add_card",
    "add_accent_line",
    "add_footer",
    "add_table",
    "add_speaker_notes",
    "add_circle",
    "add_column_card",
    "add_metric_card",
    "add_stat_card",
]
