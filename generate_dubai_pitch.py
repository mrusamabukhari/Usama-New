from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.platypus import (SimpleDocTemplate, Table, TableStyle,
                                 Paragraph, Spacer, Image)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.platypus import BaseDocTemplate, PageTemplate, Frame

# ── Brand colours ─────────────────────────────────────────────────────────────
MAROON    = colors.HexColor('#6B1535')
GOLD      = colors.HexColor('#C9A84C')
GOLD_LITE = colors.HexColor('#E8D5A3')
CREAM     = colors.HexColor('#FDF8F0')
CREAM2    = colors.HexColor('#FAF3E5')
WHITE     = colors.white
DARK      = colors.HexColor('#1E1E1E')
MID       = colors.HexColor('#4A4A4A')
GREEN     = colors.HexColor('#1A6B3C')
GREEN_LT  = colors.HexColor('#E8F5EE')

LOGO_PATH = "/root/.claude/uploads/821548fa-6491-4125-8b13-35cb95ca5b0f/bbf1cd60-1000645012.jpg"
OUT_PATH  = "/home/user/Usama-New/AKH_Dubai_Pitch_Flyer.pdf"

WA    = "+92 334 006 5781"
EMAIL = "akhlinenhouse@gmail.com"
W, H  = A4
CW    = 178*mm

def page_border(c, doc):
    c.saveState()
    c.setStrokeColor(GOLD);  c.setLineWidth(2.5)
    c.roundRect(8*mm, 8*mm, W-16*mm, H-16*mm, 4, stroke=1, fill=0)
    c.setStrokeColor(MAROON); c.setLineWidth(0.6)
    c.roundRect(10.5*mm, 10.5*mm, W-21*mm, H-21*mm, 3, stroke=1, fill=0)
    c.restoreState()

doc = BaseDocTemplate(
    OUT_PATH, pagesize=A4,
    rightMargin=16*mm, leftMargin=16*mm,
    topMargin=13*mm, bottomMargin=13*mm,
)
frame = Frame(doc.leftMargin, doc.bottomMargin,
              doc.width, doc.height, id='main')
template = PageTemplate(id='main', frames=frame, onPage=page_border)
doc.addPageTemplates([template])

story = []

def ps(name, size=8, color=DARK, font='Helvetica', align=TA_LEFT,
       leading=None, bold=False, leftIndent=0):
    if bold: font += '-Bold'
    return ParagraphStyle(name, fontSize=size, textColor=color,
                          fontName=font, alignment=align,
                          leading=leading or size*1.35,
                          leftIndent=leftIndent)

# ══════════════════════════════════════════════════════════════════════════════
# HEADER
# ══════════════════════════════════════════════════════════════════════════════
logo = Image(LOGO_PATH, width=48*mm, height=32*mm)

co_info = [
    Paragraph("AKH LINEN HOUSE",
              ps('cn', 20, MAROON, bold=True, align=TA_LEFT, leading=24)),
    Spacer(1, 1*mm),
    Paragraph("Pakistani Textile Export Agency",
              ps('cs', 9, GOLD, align=TA_LEFT, leading=13)),
    Paragraph("Bed Linen  •  Towels  •  Macawiis  •  Fabric  •  Prayer Mats",
              ps('cp', 7.5, MID, align=TA_LEFT, leading=11)),
    Spacer(1, 2*mm),
    Paragraph(f"WhatsApp: {WA}",
              ps('cw', 8.5, DARK, bold=True, align=TA_LEFT, leading=12)),
    Paragraph(f"Email: {EMAIL}",
              ps('ce', 8, DARK, align=TA_LEFT, leading=11)),
]

badge = Table(
    [[Paragraph("DIRECT FACTORY", ps('b1', 10, WHITE, bold=True, align=TA_CENTER, leading=13))],
     [Paragraph("PAKISTAN SUPPLIER", ps('b2', 10, WHITE, bold=True, align=TA_CENTER, leading=13))],
     [Paragraph("FOB  •  CIF  •  Samples Available", ps('b3', 7, GOLD_LITE, align=TA_CENTER, leading=10))]],
    colWidths=[55*mm])
badge.setStyle(TableStyle([
    ('BACKGROUND',    (0,0),(-1,-1), MAROON),
    ('TOPPADDING',    (0,0),(-1,-1), 7),
    ('BOTTOMPADDING', (0,0),(-1,-1), 7),
    ('LEFTPADDING',   (0,0),(-1,-1), 5),
    ('RIGHTPADDING',  (0,0),(-1,-1), 5),
    ('BOX',           (0,0),(-1,-1), 1.5, GOLD),
    ('LINEBELOW',     (0,0),(0,0),   0.5, GOLD),
    ('LINEBELOW',     (0,1),(0,1),   0.5, GOLD),
]))

hdr = Table([[logo, co_info, badge]], colWidths=[50*mm, 76*mm, 52*mm])
hdr.setStyle(TableStyle([
    ('VALIGN',       (0,0),(-1,-1), 'MIDDLE'),
    ('LEFTPADDING',  (0,0),(-1,-1), 0),
    ('RIGHTPADDING', (0,0),(-1,-1), 0),
    ('TOPPADDING',   (0,0),(-1,-1), 0),
    ('BOTTOMPADDING',(0,0),(-1,-1), 0),
]))
story.append(hdr)
story.append(Spacer(1, 3*mm))

# Gold divider
div = Table([['']], colWidths=[CW], rowHeights=[2])
div.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1), GOLD)]))
story.append(div)
story.append(Spacer(1, 3*mm))

# ══════════════════════════════════════════════════════════════════════════════
# ARABIC TAGLINE BANNER
# ══════════════════════════════════════════════════════════════════════════════
tagline = Table([
    [Paragraph("مورد مباشر من باكستان — أسعار المصنع — تسليم سريع",
               ps('ar', 11, WHITE, bold=True, align=TA_CENTER, leading=15)),
     Paragraph("Pakistan Direct • Factory Prices • Fast Delivery",
               ps('en', 9, GOLD_LITE, align=TA_CENTER, leading=13))]
], colWidths=[100*mm, 78*mm])
tagline.setStyle(TableStyle([
    ('BACKGROUND',    (0,0),(-1,-1), MAROON),
    ('TOPPADDING',    (0,0),(-1,-1), 6),
    ('BOTTOMPADDING', (0,0),(-1,-1), 6),
    ('LEFTPADDING',   (0,0),(-1,-1), 8),
    ('RIGHTPADDING',  (0,0),(-1,-1), 8),
    ('LINEAFTER',     (0,0),(0,-1),  0.5, GOLD),
    ('BOX',           (0,0),(-1,-1), 1, GOLD),
]))
story.append(tagline)
story.append(Spacer(1, 4*mm))

# ══════════════════════════════════════════════════════════════════════════════
# WHY BUY FROM US — 3 COLUMNS
# ══════════════════════════════════════════════════════════════════════════════
def reason_cell(icon, title, body):
    return [
        Paragraph(icon, ps('ic', 18, GOLD, align=TA_CENTER, leading=22)),
        Paragraph(title, ps('rt', 9, MAROON, bold=True, align=TA_CENTER, leading=12)),
        Paragraph(body,  ps('rb', 7.5, MID, align=TA_CENTER, leading=11)),
    ]

r1 = reason_cell("★", "Factory-Direct Prices", "No middlemen.\nLowest FOB Pakistan.")
r2 = reason_cell("✈", "CIF to Any Port", "We handle shipping.\nYou receive at your door.")
r3 = reason_cell("✓", "Trusted by Somali\n& Afghan Traders", "100+ shipments to\nDubai re-exporters.")
r4 = reason_cell("$", "Dahabshiil /\nBank Transfer", "Flexible payment.\n50% advance accepted.")

reasons = Table(
    [[Table([r1], colWidths=[40*mm]),
      Table([r2], colWidths=[40*mm]),
      Table([r3], colWidths=[40*mm]),
      Table([r4], colWidths=[40*mm])]],
    colWidths=[44.5*mm, 44.5*mm, 44.5*mm, 44.5*mm]
)
reasons.setStyle(TableStyle([
    ('VALIGN',       (0,0),(-1,-1), 'TOP'),
    ('BACKGROUND',   (0,0),(-1,-1), CREAM),
    ('BOX',          (0,0),(-1,-1), 1, GOLD),
    ('LINEBEFORE',   (1,0),(3,-1),  0.5, GOLD_LITE),
    ('TOPPADDING',   (0,0),(-1,-1), 6),
    ('BOTTOMPADDING',(0,0),(-1,-1), 6),
    ('LEFTPADDING',  (0,0),(-1,-1), 4),
    ('RIGHTPADDING', (0,0),(-1,-1), 4),
]))
story.append(reasons)
story.append(Spacer(1, 4*mm))

# ══════════════════════════════════════════════════════════════════════════════
# PRODUCTS & PRICING TABLE
# ══════════════════════════════════════════════════════════════════════════════
sec_hdr = Table(
    [[Paragraph("OUR PRODUCTS — WHOLESALE PRICES (FOB Karachi)",
                ps('sh', 10, WHITE, bold=True, align=TA_CENTER, leading=14))]],
    colWidths=[CW])
sec_hdr.setStyle(TableStyle([
    ('BACKGROUND',    (0,0),(-1,-1), MAROON),
    ('TOPPADDING',    (0,0),(-1,-1), 6),
    ('BOTTOMPADDING', (0,0),(-1,-1), 6),
    ('BOX',           (0,0),(-1,-1), 1, GOLD),
]))
story.append(sec_hdr)
story.append(Spacer(1, 1*mm))

col_w = [52*mm, 22*mm, 22*mm, 30*mm, 52*mm]
prod_hdr = ['Product', 'Unit', 'FOB Price', 'Min. Order', 'Notes']
rows = [
    ['Macawiis Checked Cotton\n(Somalia National Fabric)',
     '1 piece', '$1.20', '2,000 pcs',
     'Best seller in Somalia & East Africa.\nSizes: 72×48", 80×48"'],
    ['White Bed Sheet – Double\n(200 Thread Count Cotton)',
     '1 piece', '$5.20', '500 pcs',
     'UAE hotels, Dubai re-export.\nSize: 90"×108"'],
    ['White Bath Towel\n(500 GSM Cotton)',
     '1 piece', '$2.80', '500 pcs',
     'Hotel quality. 70×140 cm.\nHigh demand in Gulf & Africa'],
    ['Baati Fabric / Plain Cotton\n(Somalia Robe Fabric)',
     '1 meter', '$0.90', '500 m',
     'White & light colours.\n58" wide, 120 GSM'],
    ['Prayer Mat\n(Polyester Velvet, Foam)',
     '1 piece', '$2.00', '300 pcs',
     'Arabic motif design.\n70×110 cm, gift box available'],
    ['Plain Cotton Fabric\n(Grey / Bleached)',
     '1 meter', '$0.75', '1,000 m',
     'For garment factories.\n58–60" wide, 130 GSM'],
]

def style_row(row, alt=False):
    return [Paragraph(str(c), ps(f'r{i}', 7.5, DARK,
            align=TA_LEFT, leading=11)) for i, c in enumerate(row)]

tbl_data = [
    [Paragraph(h, ps(f'h{i}', 8, WHITE, bold=True, align=TA_CENTER, leading=11))
     for i, h in enumerate(prod_hdr)]
] + [style_row(r, i % 2 == 0) for i, r in enumerate(rows)]

tbl = Table(tbl_data, colWidths=col_w, repeatRows=1)
row_styles = [
    ('BACKGROUND',    (0,0),(-1,0),  MAROON),
    ('TEXTCOLOR',     (0,0),(-1,0),  WHITE),
    ('BOX',           (0,0),(-1,-1), 1, GOLD),
    ('INNERGRID',     (0,0),(-1,-1), 0.3, GOLD_LITE),
    ('TOPPADDING',    (0,0),(-1,-1), 5),
    ('BOTTOMPADDING', (0,0),(-1,-1), 5),
    ('LEFTPADDING',   (0,0),(-1,-1), 5),
    ('RIGHTPADDING',  (0,0),(-1,-1), 5),
    ('VALIGN',        (0,0),(-1,-1), 'MIDDLE'),
]
for i in range(1, len(tbl_data)):
    bg = CREAM if i % 2 == 1 else WHITE
    row_styles.append(('BACKGROUND', (0,i),(-1,i), bg))

tbl.setStyle(TableStyle(row_styles))
story.append(tbl)
story.append(Spacer(1, 4*mm))

# ══════════════════════════════════════════════════════════════════════════════
# DEAL TERMS + PITCH POINTS — 2 COLUMNS
# ══════════════════════════════════════════════════════════════════════════════
def term_table(title, rows_data, col_a=42*mm, col_b=40*mm):
    header = [[Paragraph(title, ps('tt', 9, WHITE, bold=True, align=TA_CENTER, leading=12))]]
    hdr_t = Table(header, colWidths=[col_a + col_b])
    hdr_t.setStyle(TableStyle([
        ('BACKGROUND',    (0,0),(-1,-1), MAROON),
        ('TOPPADDING',    (0,0),(-1,-1), 5),
        ('BOTTOMPADDING', (0,0),(-1,-1), 5),
        ('BOX',           (0,0),(-1,-1), 1, GOLD),
    ]))
    body_rows = [
        [Paragraph(k, ps(f'tk{i}', 7.5, MAROON, bold=True, leading=11)),
         Paragraph(v, ps(f'tv{i}', 7.5, DARK, leading=11))]
        for i, (k, v) in enumerate(rows_data)
    ]
    body = Table(body_rows, colWidths=[col_a, col_b])
    body.setStyle(TableStyle([
        ('BOX',          (0,0),(-1,-1), 1, GOLD),
        ('LINEAFTER',    (0,0),(0,-1),  0.5, GOLD_LITE),
        ('INNERGRID',    (0,0),(-1,-1), 0.2, GOLD_LITE),
        ('TOPPADDING',   (0,0),(-1,-1), 4),
        ('BOTTOMPADDING',(0,0),(-1,-1), 4),
        ('LEFTPADDING',  (0,0),(-1,-1), 5),
        ('RIGHTPADDING', (0,0),(-1,-1), 5),
    ]))
    for i in range(len(body_rows)):
        bg = CREAM if i % 2 == 0 else WHITE
        body.setStyle(TableStyle([('BACKGROUND', (0,i),(-1,i), bg)]))
    return Table([[hdr_t], [body]], colWidths=[col_a + col_b])

terms_data = [
    ("Payment:",    "50% advance + 50% on B/L copy"),
    ("Method:",     "Dahabshiil / Bank TT / LC"),
    ("Incoterm:",   "FOB Karachi  or  CIF Dubai"),
    ("Samples:",    "Free — courier cost on buyer"),
    ("Lead Time:",  "21–28 days from order"),
    ("Container:",  "20ft FCL or LCL available"),
]

pitch_data = [
    ("Re-Export to:", "Somalia, Kenya, Ethiopia, Djibouti"),
    ("Duty (UAE):",   "0% — Dubai Free Zone"),
    ("Profit margin:","30–50% on Macawiis in Somalia"),
    ("Exclusivity:",  "Area exclusivity on request"),
    ("Certifications:","OEKO-TEX, ISO on request"),
    ("Visit Pakistan:","We arrange factory tours"),
]

two_col = Table(
    [[term_table("ORDER & PAYMENT TERMS", terms_data, 32*mm, 54*mm),
      Spacer(6*mm, 1),
      term_table("WHY RE-EXPORT WITH US", pitch_data, 36*mm, 52*mm)]],
    colWidths=[88*mm, 6*mm, 84*mm]
)
two_col.setStyle(TableStyle([
    ('VALIGN',      (0,0),(-1,-1), 'TOP'),
    ('LEFTPADDING', (0,0),(-1,-1), 0),
    ('RIGHTPADDING',(0,0),(-1,-1), 0),
    ('TOPPADDING',  (0,0),(-1,-1), 0),
    ('BOTTOMPADDING',(0,0),(-1,-1), 0),
]))
story.append(two_col)
story.append(Spacer(1, 4*mm))

# ══════════════════════════════════════════════════════════════════════════════
# PITCH SCRIPT BOX  (WhatsApp message in Arabic + English)
# ══════════════════════════════════════════════════════════════════════════════
script_title = Table(
    [[Paragraph("READY-TO-SEND WHATSAPP PITCH  (Copy & Send to Buyers at Naif Souk)",
                ps('st', 9, WHITE, bold=True, align=TA_CENTER, leading=13))]],
    colWidths=[CW])
script_title.setStyle(TableStyle([
    ('BACKGROUND',    (0,0),(-1,-1), MAROON),
    ('TOPPADDING',    (0,0),(-1,-1), 5),
    ('BOTTOMPADDING', (0,0),(-1,-1), 5),
    ('BOX',           (0,0),(-1,-1), 1, GOLD),
]))
story.append(script_title)

arabic_msg = (
    "السلام عليكم،\n"
    "نحن AKH LINEN HOUSE — مورد مباشر من باكستان للأقمشة والمفروشات.\n"
    "ماكاويس (لونجي) $1.20 — مناشف $2.80 — ملاءات سرير $5.20\n"
    "شحن CIF دبي متاح — عينات مجانية — دفع داحبشيل مقبول.\n"
    "واتساب: +92 334 006 5781"
)
english_msg = (
    "As-salamu alaykum,\n"
    "We are AKH LINEN HOUSE — direct factory supplier from Pakistan.\n"
    "Macawiis (lungi) $1.20 • Towels $2.80 • Bed Sheets $5.20\n"
    "CIF Dubai shipping available • Free samples • Dahabshiil accepted.\n"
    "WhatsApp: +92 334 006 5781"
)

script_body = Table(
    [[Paragraph(arabic_msg,  ps('am', 8, DARK, leading=13, align=TA_RIGHT)),
      Paragraph(english_msg, ps('em', 8, DARK, leading=13, align=TA_LEFT))]],
    colWidths=[88*mm, 90*mm])
script_body.setStyle(TableStyle([
    ('BACKGROUND',    (0,0),(-1,-1), GREEN_LT),
    ('BOX',           (0,0),(-1,-1), 1, GOLD),
    ('LINEAFTER',     (0,0),(0,-1),  0.5, GOLD),
    ('TOPPADDING',    (0,0),(-1,-1), 8),
    ('BOTTOMPADDING', (0,0),(-1,-1), 8),
    ('LEFTPADDING',   (0,0),(-1,-1), 8),
    ('RIGHTPADDING',  (0,0),(-1,-1), 8),
    ('VALIGN',        (0,0),(-1,-1), 'TOP'),
]))
story.append(script_body)
story.append(Spacer(1, 4*mm))

# ══════════════════════════════════════════════════════════════════════════════
# FOOTER
# ══════════════════════════════════════════════════════════════════════════════
footer = Table(
    [[Paragraph("AKH LINEN HOUSE  |  Pakistan Textile Exporter",
                ps('fl', 9, WHITE, bold=True, align=TA_LEFT, leading=13)),
      Paragraph(f"WhatsApp: {WA}   |   {EMAIL}",
                ps('fr', 9, GOLD_LITE, align=TA_RIGHT, leading=13))]],
    colWidths=[90*mm, 88*mm])
footer.setStyle(TableStyle([
    ('BACKGROUND',    (0,0),(-1,-1), MAROON),
    ('TOPPADDING',    (0,0),(-1,-1), 7),
    ('BOTTOMPADDING', (0,0),(-1,-1), 7),
    ('LEFTPADDING',   (0,0),(-1,-1), 8),
    ('RIGHTPADDING',  (0,0),(-1,-1), 8),
    ('BOX',           (0,0),(-1,-1), 1.5, GOLD),
]))
story.append(footer)

doc.build(story)
print("Dubai Pitch Flyer PDF generated successfully!")
