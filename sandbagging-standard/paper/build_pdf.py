"""Build the publication PDF from PAPER_DRAFT.md using ReportLab."""
from __future__ import annotations

import html
import re
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    BaseDocTemplate,
    Flowable,
    Frame,
    KeepTogether,
    ListFlowable,
    ListItem,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "PAPER_DRAFT.md"
OUTPUT = HERE.parents[1] / "output" / "pdf" / "xysera_sandbagging_evidence_standard_v1.0-rc1.pdf"

NAVY = colors.HexColor("#102A43")
BLUE = colors.HexColor("#2878B5")
TEAL = colors.HexColor("#2A9D8F")
PALE = colors.HexColor("#EAF2F8")
INK = colors.HexColor("#243B53")
MUTED = colors.HexColor("#627D98")
RULE = colors.HexColor("#BCCCDC")


def ascii_text(value: str) -> str:
    replacements = {
        "\u2010": "-", "\u2011": "-", "\u2012": "-", "\u2013": "-", "\u2014": "-",
        "\u2212": "-", "\u2192": "->", "\u2265": ">=", "\u2264": "<=", "\u03c1": "rho",
        "\u2018": "'", "\u2019": "'", "\u201c": '"', "\u201d": '"', "\u00b1": "+/-",
    }
    for old, new in replacements.items():
        value = value.replace(old, new)
    return value


def inline(value: str) -> str:
    value = html.escape(ascii_text(value), quote=False)
    value = re.sub(r"arXiv:(\d{4}\.\d{5})", r'<link href="https://arxiv.org/abs/\1" color="#2878B5">arXiv:\1</link>', value)
    value = value.replace(
        "https://proceedings.mlr.press/v306/yulong26a.html",
        '<link href="https://proceedings.mlr.press/v306/yulong26a.html" color="#2878B5">PMLR paper page</link>',
    )
    value = re.sub(r"`([^`]+)`", r'<font name="Courier">\1</font>', value)
    value = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", value)
    value = re.sub(r"\*([^*]+)\*", r"<i>\1</i>", value)
    return value


class PageNumberCanvasMixin:
    pass


def on_page(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(RULE)
    canvas.setLineWidth(0.45)
    canvas.line(22 * mm, 16 * mm, A4[0] - 22 * mm, 16 * mm)
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(MUTED)
    canvas.drawString(22 * mm, 10.5 * mm, "Ethreidge / Xysera Research | preprint v1.0-rc1 | SES v0.5 | not peer reviewed")
    canvas.drawRightString(A4[0] - 22 * mm, 10.5 * mm, str(doc.page))
    canvas.restoreState()


class EvidenceLadder(Flowable):
    def __init__(self, width=160 * mm, height=63 * mm):
        super().__init__()
        self.width = width
        self.height = height

    def draw(self):
        c = self.canv
        labels = [
            ("L4", "Behaviour consistent with strategic sandbagging", TEAL),
            ("L3", "Consequence-sensitive underperformance", colors.HexColor("#46A6A0")),
            ("L2", "Manipulation-attributable underperformance", BLUE),
            ("L1", "Underperformance; L1-ctx if neutral context reproduces it", colors.HexColor("#5C91C8")),
            ("L0", "No underperformance detected within the fixed margin", colors.HexColor("#8AA8C2")),
        ]
        h = 10.5 * mm
        gap = 1.5 * mm
        for i, (level, label, colour) in enumerate(labels):
            y = self.height - (i + 1) * h - i * gap
            inset = i * 4.0 * mm
            w = self.width - 2 * inset
            c.setFillColor(colour)
            c.roundRect(inset, y, w, h, 2.2 * mm, fill=1, stroke=0)
            c.setFillColor(colors.white)
            c.setFont("Helvetica-Bold", 9)
            c.drawString(inset + 4 * mm, y + 3.5 * mm, level)
            c.setFont("Helvetica", 8.2)
            c.drawString(inset + 17 * mm, y + 3.5 * mm, label)


class WorkedResultsChart(Flowable):
    def __init__(self, width=160 * mm, height=62 * mm):
        super().__init__()
        self.width = width
        self.height = height

    def draw(self):
        c = self.canv
        models = ["Qwen2.5-7B", "Llama-3.1-8B", "Phi-3.5-mini", "Qwen3-4B", "Gemma-3-4B"]
        context = [2.34, 4.48, 2.10, 3.12, 4.36]
        d1 = [0.26, -0.08, 0.08, 0.16, -0.12]
        left = 36 * mm
        top = self.height - 8 * mm
        scale = 20 * mm
        c.setFont("Helvetica-Bold", 8.5)
        c.setFillColor(INK)
        c.drawString(0, self.height - 3 * mm, "Worked Study 1 contrasts (percentage points)")
        c.setStrokeColor(RULE)
        c.line(left, 4 * mm, left, top)
        for tick in [-1, 0, 1, 2, 3, 4, 5]:
            x = left + tick * scale
            c.setStrokeColor(colors.HexColor("#E4E7EB"))
            c.line(x, 5 * mm, x, top)
            c.setFillColor(MUTED)
            c.setFont("Helvetica", 7)
            c.drawCentredString(x, 1.5 * mm, str(tick))
        row = 9.5 * mm
        for i, model in enumerate(models):
            y = top - (i + 0.7) * row
            c.setFillColor(INK)
            c.setFont("Helvetica", 7.8)
            c.drawRightString(left - 3 * mm, y + 1.1 * mm, model)
            c.setFillColor(BLUE)
            c.rect(left, y + 2.6 * mm, context[i] * scale, 2.5 * mm, fill=1, stroke=0)
            c.setFillColor(TEAL)
            x0 = left + min(0, d1[i]) * scale
            c.rect(x0, y - 0.8 * mm, abs(d1[i]) * scale, 2.5 * mm, fill=1, stroke=0)
        c.setFont("Helvetica", 7.4)
        c.setFillColor(BLUE)
        c.rect(left + 79 * mm, self.height - 5 * mm, 4 * mm, 2.5 * mm, fill=1, stroke=0)
        c.setFillColor(INK)
        c.drawString(left + 85 * mm, self.height - 4.6 * mm, "No-note minus neutral")
        c.setFillColor(TEAL)
        c.rect(left + 79 * mm, self.height - 9 * mm, 4 * mm, 2.5 * mm, fill=1, stroke=0)
        c.setFillColor(INK)
        c.drawString(left + 85 * mm, self.height - 8.6 * mm, "D1: reward minus penalty")


def styles():
    s = getSampleStyleSheet()
    s.add(ParagraphStyle(name="PaperTitle", parent=s["Title"], fontName="Helvetica-Bold", fontSize=20,
                         leading=24, textColor=NAVY, alignment=TA_LEFT, spaceAfter=7 * mm))
    s.add(ParagraphStyle(name="Meta", parent=s["Normal"], fontSize=9.2, leading=13, textColor=MUTED,
                         spaceAfter=7 * mm))
    s.add(ParagraphStyle(name="H2x", parent=s["Heading2"], fontName="Helvetica-Bold", fontSize=13,
                         leading=16, textColor=NAVY, spaceBefore=6 * mm, spaceAfter=2.5 * mm,
                         keepWithNext=True))
    s.add(ParagraphStyle(name="H3x", parent=s["Heading3"], fontName="Helvetica-Bold", fontSize=10.5,
                         leading=13, textColor=BLUE, spaceBefore=4 * mm, spaceAfter=1.5 * mm,
                         keepWithNext=True))
    s.add(ParagraphStyle(name="Bodyx", parent=s["BodyText"], fontName="Helvetica", fontSize=9.25,
                         leading=13.2, textColor=INK, spaceAfter=2.6 * mm, alignment=TA_LEFT))
    s.add(ParagraphStyle(name="Captionx", parent=s["BodyText"], fontName="Helvetica-Oblique", fontSize=8,
                         leading=10.5, textColor=MUTED, spaceBefore=1.5 * mm, spaceAfter=4 * mm))
    s.add(ParagraphStyle(name="Refx", parent=s["BodyText"], fontName="Helvetica", fontSize=7.0,
                         leading=8.4, textColor=INK, leftIndent=4 * mm, firstLineIndent=-4 * mm,
                         spaceAfter=0.45 * mm))
    s.add(ParagraphStyle(name="TableCell", parent=s["BodyText"], fontName="Helvetica", fontSize=7.3,
                         leading=9.2, textColor=INK))
    s.add(ParagraphStyle(name="TableHead", parent=s["BodyText"], fontName="Helvetica-Bold", fontSize=7.2,
                         leading=9, textColor=colors.white))
    return s


def parse_table(lines, sty):
    rows = []
    for line in lines:
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if all(re.fullmatch(r":?-+:?", c) for c in cells):
            continue
        style = sty["TableHead"] if not rows else sty["TableCell"]
        rows.append([Paragraph(inline(c), style) for c in cells])
    if len(rows[0]) == 5:
        widths = [32 * mm, 30 * mm, 32 * mm, 40 * mm, 26 * mm]
    else:
        widths = [28 * mm] + [(160 * mm - 28 * mm) / (len(rows[0]) - 1)] * (len(rows[0]) - 1)
    table = Table(rows, colWidths=widths, repeatRows=1, hAlign="LEFT")
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.35, RULE),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, PALE]),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 2 * mm),
        ("RIGHTPADDING", (0, 0), (-1, -1), 2 * mm),
        ("TOPPADDING", (0, 0), (-1, -1), 1.4 * mm),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 1.4 * mm),
    ]))
    return table


def story_from_markdown(text: str):
    sty = styles()
    lines = text.splitlines()
    story = []
    i = 0
    in_refs = False
    table_count = 0
    chart_after_caption = False
    while i < len(lines):
        line = lines[i].strip()
        if not line:
            i += 1
            continue
        if line.startswith("# "):
            story.append(Paragraph(inline(line[2:]), sty["PaperTitle"]))
            i += 1
            continue
        if line.startswith("## "):
            title = line[3:]
            in_refs = title == "References"
            story.append(Paragraph(inline(title), sty["H2x"]))
            i += 1
            continue
        if line.startswith("### "):
            story.append(Paragraph(inline(line[4:]), sty["H3x"]))
            i += 1
            continue
        if line.startswith("|"):
            block = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                block.append(lines[i])
                i += 1
            table_count += 1
            story.append(Spacer(1, 1.5 * mm))
            story.append(parse_table(block, sty))
            story.append(Spacer(1, 2 * mm))
            if table_count == 1:
                story.append(KeepTogether([EvidenceLadder(), Paragraph("Figure 1. Cumulative SES evidence ladder.", sty["Captionx"]), Spacer(1, 3 * mm)]))
            elif table_count == 3:
                chart_after_caption = True
            continue
        if re.match(r"^(?:- |\d+\. )", line):
            items = []
            numbered = bool(re.match(r"^\d+\. ", line))
            while i < len(lines) and re.match(r"^(?:- |\d+\. )", lines[i].strip()):
                value = re.sub(r"^(?:- |\d+\. )", "", lines[i].strip())
                items.append(ListItem(Paragraph(inline(value), sty["Bodyx"]), leftIndent=4 * mm))
                i += 1
            story.append(ListFlowable(items, bulletType="1" if numbered else "bullet", leftIndent=7 * mm,
                                      bulletFontName="Helvetica", bulletFontSize=8))
            story.append(Spacer(1, 1.5 * mm))
            continue
        para = [line]
        i += 1
        if not in_refs:
            while i < len(lines) and lines[i].strip() and not re.match(r"^(#|\||- |\d+\. )", lines[i].strip()):
                para.append(lines[i].strip())
                i += 1
        value = " ".join(para)
        if value.startswith("**Torin Ethreidge.**"):
            story.append(Paragraph(inline(value), sty["Meta"]))
        elif value.startswith("*Table ") or value.startswith("*Figure "):
            story.append(Paragraph(inline(value), sty["Captionx"]))
            if chart_after_caption:
                story.append(KeepTogether([WorkedResultsChart(), Paragraph("Figure 2. Generic context effects are visibly larger than the preregistered consequence contrast D1 in all five models.", sty["Captionx"])]))
                chart_after_caption = False
        elif in_refs:
            story.append(Paragraph(inline(value), sty["Refx"]))
        else:
            story.append(Paragraph(inline(value), sty["Bodyx"]))
    return story


def build():
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    doc = BaseDocTemplate(
        str(OUTPUT), pagesize=A4, title="Toward an Evidence Standard for Sandbagging Claims",
        author="Torin Ethreidge (Xysera Research)", subject="Sandbagging Evidence Standard preprint v1.0-rc1; frozen rules v0.5; not peer reviewed",
        leftMargin=22 * mm, rightMargin=22 * mm, topMargin=18 * mm, bottomMargin=22 * mm,
    )
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="body")
    doc.addPageTemplates([PageTemplate(id="paper", frames=[frame], onPage=on_page)])
    doc.build(story_from_markdown(SOURCE.read_text(encoding="utf-8")))
    print(OUTPUT)


if __name__ == "__main__":
    build()
