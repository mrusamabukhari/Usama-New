from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.platypus import KeepTogether

GREEN  = colors.HexColor("#1a7a3c")
GOLD   = colors.HexColor("#c8a200")
RED    = colors.HexColor("#c0392b")
LIGHT  = colors.HexColor("#f4f8f4")
DARK   = colors.HexColor("#1a2e1a")
WHITE  = colors.white
GREY   = colors.HexColor("#f0f0f0")
MIDGREY= colors.HexColor("#cccccc")

doc = SimpleDocTemplate(
    "/home/user/Usama-New/Pakistan_vs_India_DRC_Scorecard.pdf",
    pagesize=A4,
    rightMargin=1.8*cm, leftMargin=1.8*cm,
    topMargin=1.8*cm, bottomMargin=1.8*cm
)

styles = getSampleStyleSheet()

title_style = ParagraphStyle("title", fontSize=20, leading=26,
    textColor=WHITE, alignment=TA_CENTER, fontName="Helvetica-Bold")
sub_style = ParagraphStyle("sub", fontSize=11, leading=15,
    textColor=GOLD, alignment=TA_CENTER, fontName="Helvetica-Bold")
label_style = ParagraphStyle("label", fontSize=9, leading=12,
    textColor=DARK, fontName="Helvetica-Bold")
body_style = ParagraphStyle("body", fontSize=9, leading=13,
    textColor=DARK, fontName="Helvetica")
caption_style = ParagraphStyle("caption", fontSize=8, leading=11,
    textColor=colors.HexColor("#555555"), alignment=TA_CENTER, fontName="Helvetica-Oblique")
section_style = ParagraphStyle("section", fontSize=12, leading=16,
    textColor=WHITE, fontName="Helvetica-Bold", alignment=TA_CENTER)
verdict_style = ParagraphStyle("verdict", fontSize=10, leading=14,
    textColor=DARK, fontName="Helvetica-Bold", alignment=TA_CENTER)
win_style = ParagraphStyle("win", fontSize=13, leading=18,
    textColor=GREEN, fontName="Helvetica-Bold", alignment=TA_CENTER)

story = []

# ── HEADER BANNER ──────────────────────────────────────────────────────────
header_data = [[
    Paragraph("🇵🇰  Pakistan vs India  🇮🇳", title_style),
]]
header_table = Table(header_data, colWidths=[17.4*cm])
header_table.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,-1), GREEN),
    ("ROUNDEDCORNERS", [8]),
    ("TOPPADDING",    (0,0), (-1,-1), 14),
    ("BOTTOMPADDING", (0,0), (-1,-1), 10),
    ("LEFTPADDING",   (0,0), (-1,-1), 10),
    ("RIGHTPADDING",  (0,0), (-1,-1), 10),
]))
story.append(header_table)

sub_data = [[Paragraph("Summary Scorecard — Rice Export to Democratic Republic of Congo (DRC)", sub_style)]]
sub_table = Table(sub_data, colWidths=[17.4*cm])
sub_table.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,-1), DARK),
    ("TOPPADDING",    (0,0), (-1,-1), 8),
    ("BOTTOMPADDING", (0,0), (-1,-1), 8),
]))
story.append(sub_table)
story.append(Spacer(1, 0.4*cm))

# ── MAIN SCORECARD TABLE ────────────────────────────────────────────────────
col_w = [5.8*cm, 5.8*cm, 5.8*cm]

def cell(txt, style=body_style):
    return Paragraph(txt, style)

hdr_cell = ParagraphStyle("hdr", fontSize=10, leading=14,
    textColor=WHITE, fontName="Helvetica-Bold", alignment=TA_CENTER)
pak_cell = ParagraphStyle("pak", fontSize=9, leading=13,
    textColor=DARK, fontName="Helvetica", alignment=TA_CENTER)
ind_cell  = ParagraphStyle("ind", fontSize=9, leading=13,
    textColor=DARK, fontName="Helvetica", alignment=TA_CENTER)
factor_cell = ParagraphStyle("factor", fontSize=9, leading=13,
    textColor=DARK, fontName="Helvetica-Bold", alignment=TA_LEFT)

rows = [
    # header
    [Paragraph("Factor", hdr_cell),
     Paragraph("🇵🇰  Pakistan", hdr_cell),
     Paragraph("🇮🇳  India", hdr_cell)],

    # rows
    [Paragraph("Transit Time\nKarachi / Mumbai → Matadi", factor_cell),
     Paragraph("32–37 days\n✅  FASTEST", pak_cell),
     Paragraph("45–50 days\n❌  13 days slower", ind_cell)],

    [Paragraph("Rice Export Reliability\n(government bans)", factor_cell),
     Paragraph("Never banned exports\n✅  STABLE", pak_cell),
     Paragraph("Banned 2023–2024\n❌  14-month disruption", ind_cell)],

    [Paragraph("EU Food Safety Alerts\n(pesticide residues, 2024)", factor_cell),
     Paragraph("74 alerts\n✅  LOW RISK", pak_cell),
     Paragraph("264 alerts\n❌  3.6× more than Pakistan", ind_cell)],

    [Paragraph("EU Non-Basmati Rejections\n(2024)", factor_cell),
     Paragraph("2 rejections\n✅  EXCELLENT", pak_cell),
     Paragraph("37 rejections\n❌  18× more than Pakistan", ind_cell)],

    [Paragraph("Price (5% broken white)\nFOB per MT", factor_cell),
     Paragraph("~$445/MT\n✅  Competitive", pak_cell),
     Paragraph("~$400–430/MT\n⚠️  Slightly cheaper", ind_cell)],

    [Paragraph("Basmati Quality\n(Super Basmati, 1121)", factor_cell),
     Paragraph("World-class\nEU market growing +15%\n✅  PREMIUM", pak_cell),
     Paragraph("Good — but\ndeclining EU trust\n⚠️  Under pressure", ind_cell)],

    [Paragraph("Diplomatic Goodwill\nin DRC", factor_cell),
     Paragraph("MONUSCO peacekeeping\n20+ years\n✅  STRONG", pak_cell),
     Paragraph("Moderate\n—", ind_cell)],

    [Paragraph("Supply Diversification\nfor DRC Buyer", factor_cell),
     Paragraph("Safe backup source\n✅  REDUCES RISK", pak_cell),
     Paragraph("Single-source risk\n❌  2023 proved it", ind_cell)],

    # verdict row
    [Paragraph("OVERALL VERDICT", hdr_cell),
     Paragraph("WIN on reliability,\nsafety & speed", pak_cell),
     Paragraph("Price edge only\n(short-term)", ind_cell)],
]

score_table = Table(rows, colWidths=col_w, repeatRows=1)
score_table.setStyle(TableStyle([
    # header row
    ("BACKGROUND",    (0,0), (-1,0),  DARK),
    ("TEXTCOLOR",     (0,0), (-1,0),  WHITE),
    ("FONTNAME",      (0,0), (-1,0),  "Helvetica-Bold"),
    ("FONTSIZE",      (0,0), (-1,0),  10),
    ("ALIGN",         (0,0), (-1,0),  "CENTER"),
    ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),

    # alternating rows
    ("BACKGROUND",    (0,1), (-1,1),  LIGHT),
    ("BACKGROUND",    (0,2), (-1,2),  WHITE),
    ("BACKGROUND",    (0,3), (-1,3),  LIGHT),
    ("BACKGROUND",    (0,4), (-1,4),  WHITE),
    ("BACKGROUND",    (0,5), (-1,5),  LIGHT),
    ("BACKGROUND",    (0,6), (-1,6),  WHITE),
    ("BACKGROUND",    (0,7), (-1,7),  LIGHT),
    ("BACKGROUND",    (0,8), (-1,8),  WHITE),

    # verdict row highlight
    ("BACKGROUND",    (0,9), (-1,9),  DARK),
    ("TEXTCOLOR",     (0,9), (-1,9),  WHITE),
    ("FONTNAME",      (0,9), (-1,9),  "Helvetica-Bold"),

    # Pakistan column — green tint
    ("BACKGROUND",    (1,1), (1,8),   colors.HexColor("#e8f5ec")),
    ("BACKGROUND",    (1,9), (1,9),   GREEN),
    ("TEXTCOLOR",     (1,9), (1,9),   WHITE),

    # India column — slight red tint
    ("BACKGROUND",    (2,1), (2,8),   colors.HexColor("#fdf0ef")),
    ("BACKGROUND",    (2,9), (2,9),   colors.HexColor("#8b1a1a")),
    ("TEXTCOLOR",     (2,9), (2,9),   WHITE),

    # grid
    ("GRID",          (0,0), (-1,-1), 0.5, MIDGREY),
    ("LINEBELOW",     (0,0), (-1,0),  1.5, GREEN),
    ("LINEBELOW",     (0,8), (-1,8),  1.5, DARK),

    # padding
    ("TOPPADDING",    (0,0), (-1,-1), 8),
    ("BOTTOMPADDING", (0,0), (-1,-1), 8),
    ("LEFTPADDING",   (0,0), (-1,-1), 8),
    ("RIGHTPADDING",  (0,0), (-1,-1), 8),
]))
story.append(score_table)
story.append(Spacer(1, 0.5*cm))

# ── KEY STATS STRIP ─────────────────────────────────────────────────────────
stat_style = ParagraphStyle("stat", fontSize=14, leading=18,
    textColor=GREEN, fontName="Helvetica-Bold", alignment=TA_CENTER)
stat_label = ParagraphStyle("stlbl", fontSize=8, leading=11,
    textColor=DARK, fontName="Helvetica", alignment=TA_CENTER)

stats = [
    [Paragraph("13 Days", stat_style),   Paragraph("3.6×", stat_style),
     Paragraph("18×", stat_style),        Paragraph("$445/MT", stat_style)],
    [Paragraph("Faster delivery\nthan India", stat_label),
     Paragraph("Fewer EU food\nsafety alerts", stat_label),
     Paragraph("Fewer EU\nrejections", stat_label),
     Paragraph("Competitive FOB\nprice (5% broken)", stat_label)],
]
stats_table = Table(stats, colWidths=[4.35*cm]*4)
stats_table.setStyle(TableStyle([
    ("BACKGROUND",    (0,0), (-1,-1), GREY),
    ("LINEBELOW",     (0,0), (-1,0),  1, MIDGREY),
    ("GRID",          (0,0), (-1,-1), 0.5, MIDGREY),
    ("TOPPADDING",    (0,0), (-1,-1), 8),
    ("BOTTOMPADDING", (0,0), (-1,-1), 6),
    ("LEFTPADDING",   (0,0), (-1,-1), 4),
    ("RIGHTPADDING",  (0,0), (-1,-1), 4),
]))
story.append(stats_table)
story.append(Spacer(1, 0.5*cm))

# ── PITCH SUMMARY BOX ───────────────────────────────────────────────────────
pitch_hdr = [[Paragraph("Key Pitch Points for a DRC Buyer Already Buying from India", section_style)]]
pitch_hdr_t = Table(pitch_hdr, colWidths=[17.4*cm])
pitch_hdr_t.setStyle(TableStyle([
    ("BACKGROUND",    (0,0), (-1,-1), GREEN),
    ("TOPPADDING",    (0,0), (-1,-1), 8),
    ("BOTTOMPADDING", (0,0), (-1,-1), 8),
]))
story.append(pitch_hdr_t)

pitch_points = [
    ["1", "Supply Reliability",
     "India banned rice exports in 2023 for 14 months without warning. Pakistan has NEVER banned exports. Use Pakistan as your secure backup supplier."],
    ["2", "Food Safety",
     "Pakistan had only 74 EU food safety alerts vs 264 for India in 2024. Pakistani rice is safer for your customers and their families."],
    ["3", "Faster Delivery",
     "Karachi to Matadi is 32–37 days. Mumbai to Matadi is 45–50 days. You get your rice 2 weeks earlier — less port time, less spoilage, lower costs."],
    ["4", "Trial With Zero Risk",
     "Request 1–2 containers as a trial. Pay 30% advance + 70% on Bill of Lading. Free sample bag available before commitment."],
    ["5", "Diplomatic Trust",
     "Pakistan has served in UN MONUSCO peacekeeping in DRC for 20+ years. We are a long-term partner, not just a seller."],
]

p_num  = ParagraphStyle("pnum", fontSize=12, leading=16,
    textColor=WHITE, fontName="Helvetica-Bold", alignment=TA_CENTER)
p_head = ParagraphStyle("phead", fontSize=9, leading=13,
    textColor=GREEN, fontName="Helvetica-Bold")
p_body = ParagraphStyle("pbody", fontSize=9, leading=13,
    textColor=DARK, fontName="Helvetica")

pitch_rows = [[
    Paragraph(r[0], p_num),
    Paragraph(r[1], p_head),
    Paragraph(r[2], p_body),
] for r in pitch_points]

pitch_table = Table(pitch_rows, colWidths=[1*cm, 3.5*cm, 12.9*cm])
pitch_table.setStyle(TableStyle([
    ("BACKGROUND",    (0,0), (0,-1), GREEN),
    ("BACKGROUND",    (1,0), (-1,-1), WHITE),
    ("BACKGROUND",    (1,1), (-1,1),  GREY),
    ("BACKGROUND",    (1,3), (-1,3),  GREY),
    ("GRID",          (0,0), (-1,-1), 0.5, MIDGREY),
    ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
    ("TOPPADDING",    (0,0), (-1,-1), 8),
    ("BOTTOMPADDING", (0,0), (-1,-1), 8),
    ("LEFTPADDING",   (0,0), (-1,-1), 8),
    ("RIGHTPADDING",  (0,0), (-1,-1), 8),
]))
story.append(pitch_table)
story.append(Spacer(1, 0.5*cm))

# ── FINAL VERDICT ───────────────────────────────────────────────────────────
verdict_data = [[
    Paragraph(
        "✅  Pakistan CAN WIN — on Reliability, Food Safety, Speed & Diplomatic Trust.\n"
        "India's only edge is a small price difference — easily offset by lower spoilage, "
        "faster delivery, and zero supply-ban risk.",
        verdict_style)
]]
verdict_table = Table(verdict_data, colWidths=[17.4*cm])
verdict_table.setStyle(TableStyle([
    ("BACKGROUND",    (0,0), (-1,-1), colors.HexColor("#e8f5ec")),
    ("LINEABOVE",     (0,0), (-1,0),  2, GREEN),
    ("LINEBELOW",     (0,0), (-1,0),  2, GREEN),
    ("TOPPADDING",    (0,0), (-1,-1), 12),
    ("BOTTOMPADDING", (0,0), (-1,-1), 12),
    ("LEFTPADDING",   (0,0), (-1,-1), 12),
    ("RIGHTPADDING",  (0,0), (-1,-1), 12),
]))
story.append(verdict_table)
story.append(Spacer(1, 0.3*cm))

# ── FOOTER ──────────────────────────────────────────────────────────────────
story.append(HRFlowable(width="100%", thickness=0.5, color=MIDGREY))
story.append(Spacer(1, 0.15*cm))
story.append(Paragraph(
    "Sources: ProPakistani · S&P Global · Al Jazeera · Agri-Food Update · IFPRI · FW Freight · Concave Agri · TDAP",
    caption_style))

doc.build(story)
print("PDF created successfully.")
