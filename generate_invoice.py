from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.platypus import (SimpleDocTemplate, Table, TableStyle,
                                 Paragraph, Spacer, Image)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from datetime import date

# ── Brand colours ─────────────────────────────────────────────────────────────
MAROON    = colors.HexColor('#6B1535')
GOLD      = colors.HexColor('#C9A84C')
GOLD_LITE = colors.HexColor('#E8D5A3')
CREAM     = colors.HexColor('#FDF8F0')
CREAM2    = colors.HexColor('#FAF3E5')
WHITE     = colors.white
DARK      = colors.HexColor('#1E1E1E')
MID       = colors.HexColor('#4A4A4A')
LIGHT_RED = colors.HexColor('#F9EEF2')

LOGO_PATH = "/root/.claude/uploads/821548fa-6491-4125-8b13-35cb95ca5b0f/bbf1cd60-1000645012.jpg"
OUT_PATH  = "/home/user/Usama-New/AKH_Linen_House_Proforma_Invoice.pdf"

WA    = "+92 334 006 5781"
EMAIL = "akhlinenhouse@gmail.com"
W, H  = A4
CW    = 178*mm

# ── Page border ────────────────────────────────────────────────────────────────
def page_border(c, doc):
    c.saveState()
    c.setStrokeColor(GOLD)
    c.setLineWidth(2.5)
    c.roundRect(8*mm, 8*mm, W-16*mm, H-16*mm, 4, stroke=1, fill=0)
    c.setStrokeColor(MAROON)
    c.setLineWidth(0.6)
    c.roundRect(10.5*mm, 10.5*mm, W-21*mm, H-21*mm, 3, stroke=1, fill=0)
    c.restoreState()

doc = SimpleDocTemplate(
    OUT_PATH, pagesize=A4,
    rightMargin=16*mm, leftMargin=16*mm,
    topMargin=13*mm, bottomMargin=13*mm,
)

story = []

# ── Style helper ───────────────────────────────────────────────────────────────
def ps(name, size=8, color=DARK, font='Helvetica', align=TA_LEFT,
       leading=None, bold=False, leftIndent=0):
    if bold: font += '-Bold'
    return ParagraphStyle(name, fontSize=size, textColor=color,
                          fontName=font, alignment=align,
                          leading=leading or size*1.4,
                          leftIndent=leftIndent)

# ══════════════════════════════════════════════════════════════════════════════
# HEADER — Logo + Company + Invoice Title
# ══════════════════════════════════════════════════════════════════════════════
logo = Image(LOGO_PATH, width=50*mm, height=34*mm)

company_info = [
    Paragraph("AKH LINEN HOUSE",
              ps('cn', 18, MAROON, bold=True, align=TA_LEFT, leading=22)),
    Spacer(1, 1*mm),
    Paragraph("Pakistani Textile Export Agency",
              ps('cs', 8.5, GOLD, align=TA_LEFT, leading=12)),
    Paragraph("Bed Linen  •  Towels  •  Fabric  •  Prayer Mats",
              ps('cp', 7.5, MID, align=TA_LEFT, leading=11)),
    Spacer(1, 2*mm),
    Paragraph(f"WhatsApp: {WA}",
              ps('cw', 8, DARK, align=TA_LEFT, leading=11)),
    Paragraph(f"Email: {EMAIL}",
              ps('ce', 8, DARK, align=TA_LEFT, leading=11)),
    Paragraph("Pakistan",
              ps('cc', 8, DARK, align=TA_LEFT, leading=11)),
]

inv_title_box = Table(
    [[Paragraph("PROFORMA INVOICE",
                ps('it', 14, WHITE, bold=True, align=TA_CENTER, leading=18))],
     [Paragraph("CIF — Mogadishu Port, Somalia",
                ps('is', 8.5, GOLD_LITE, align=TA_CENTER, leading=12))]],
    colWidths=[58*mm])
inv_title_box.setStyle(TableStyle([
    ('BACKGROUND',    (0,0),(-1,-1), MAROON),
    ('TOPPADDING',    (0,0),(-1,-1), 8),
    ('BOTTOMPADDING', (0,0),(-1,-1), 8),
    ('LEFTPADDING',   (0,0),(-1,-1), 6),
    ('RIGHTPADDING',  (0,0),(-1,-1), 6),
    ('BOX',           (0,0),(-1,-1), 1.5, GOLD),
]))

hdr = Table([[logo, company_info, inv_title_box]],
            colWidths=[52*mm, 78*mm, 48*mm])
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
div.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),GOLD)]))
story.append(div)
story.append(Spacer(1, 3*mm))

# ══════════════════════════════════════════════════════════════════════════════
# INVOICE META — Invoice No / Date / Validity
# ══════════════════════════════════════════════════════════════════════════════
today = date.today().strftime("%d %B %Y")
meta_data = [[
    Table([
        [Paragraph("Invoice No:", ps('ml', 8, GOLD, bold=True)),
         Paragraph("AKH-2026-001", ps('mv', 8, DARK, bold=True))],
        [Paragraph("Date:", ps('ml2', 8, GOLD, bold=True)),
         Paragraph(today, ps('mv2', 8, DARK))],
        [Paragraph("Valid For:", ps('ml3', 8, GOLD, bold=True)),
         Paragraph("30 Days", ps('mv3', 8, DARK))],
    ], colWidths=[22*mm, 40*mm]),

    Table([
        [Paragraph("Payment Terms:", ps('pl', 8, GOLD, bold=True)),
         Paragraph("50% Advance | 50% on B/L Copy", ps('pv', 8, DARK))],
        [Paragraph("Incoterm:", ps('pl2', 8, GOLD, bold=True)),
         Paragraph("CIF Mogadishu Port, Somalia", ps('pv2', 8, MAROON, bold=True))],
        [Paragraph("Delivery:", ps('pl3', 8, GOLD, bold=True)),
         Paragraph("14–21 Days from Order Confirmation", ps('pv3', 8, DARK))],
    ], colWidths=[28*mm, 58*mm]),
]]
meta = Table(meta_data, colWidths=[64*mm, 114*mm])
meta.setStyle(TableStyle([
    ('BACKGROUND',   (0,0),(-1,-1), CREAM2),
    ('BOX',          (0,0),(-1,-1), 1, GOLD),
    ('LINEAFTER',    (0,0),(0,-1),  0.5, GOLD),
    ('TOPPADDING',   (0,0),(-1,-1), 5),
    ('BOTTOMPADDING',(0,0),(-1,-1), 5),
    ('LEFTPADDING',  (0,0),(-1,-1), 8),
    ('RIGHTPADDING', (0,0),(-1,-1), 8),
    ('VALIGN',       (0,0),(-1,-1), 'MIDDLE'),
]))
story.append(meta)
story.append(Spacer(1, 3*mm))

# ══════════════════════════════════════════════════════════════════════════════
# BUYER + SELLER INFO
# ══════════════════════════════════════════════════════════════════════════════
def info_box(title, lines, w):
    hdr_p = Paragraph(title, ps('ibh', 8.5, WHITE, bold=True, align=TA_LEFT))
    hdr_t = Table([[hdr_p]], colWidths=[w-0*mm])
    hdr_t.setStyle(TableStyle([
        ('BACKGROUND',   (0,0),(-1,-1), MAROON),
        ('TOPPADDING',   (0,0),(-1,-1), 5),
        ('BOTTOMPADDING',(0,0),(-1,-1), 5),
        ('LEFTPADDING',  (0,0),(-1,-1), 8),
        ('RIGHTPADDING', (0,0),(-1,-1), 8),
        ('LINEBELOW',    (0,0),(-1,-1), 1, GOLD),
    ]))
    body_rows = [[Paragraph(l, ps('ibl', 8, DARK if not l.startswith('▸') else MAROON,
                                  leading=12, leftIndent=4))] for l in lines]
    body_t = Table(body_rows, colWidths=[w-0*mm])
    body_t.setStyle(TableStyle([
        ('BACKGROUND',   (0,0),(-1,-1), CREAM),
        ('TOPPADDING',   (0,0),(-1,-1), 3),
        ('BOTTOMPADDING',(0,0),(-1,-1), 3),
        ('LEFTPADDING',  (0,0),(-1,-1), 8),
        ('RIGHTPADDING', (0,0),(-1,-1), 8),
        ('BOX',          (0,0),(-1,-1), 0.8, GOLD),
    ]))
    return Table([[hdr_t],[body_t]], colWidths=[w])

seller = info_box("SELLER / EXPORTER", [
    "AKH Linen House",
    "Pakistan",
    f"WhatsApp: {WA}",
    f"Email: {EMAIL}",
    "Country of Origin: Pakistan",
], 86*mm)

buyer = info_box("BUYER / CONSIGNEE", [
    "[Buyer Full Name]",
    "[Company Name]",
    "[Address, Mogadishu, Somalia]",
    "[Phone / WhatsApp]",
    "[Email Address]",
], 88*mm)

party_row = Table([[seller, Spacer(4*mm,1), buyer]],
                  colWidths=[86*mm, 4*mm, 88*mm])
party_row.setStyle(TableStyle([
    ('VALIGN',       (0,0),(-1,-1), 'TOP'),
    ('LEFTPADDING',  (0,0),(-1,-1), 0),
    ('RIGHTPADDING', (0,0),(-1,-1), 0),
]))
story.append(party_row)
story.append(Spacer(1, 3*mm))

# ══════════════════════════════════════════════════════════════════════════════
# PRODUCTS TABLE
# ══════════════════════════════════════════════════════════════════════════════
th = ps('th', 8, WHITE, bold=True, align=TA_CENTER)
td = ps('td', 8, DARK,  align=TA_CENTER)
tl = ps('tl', 8, DARK,  align=TA_LEFT)
tv = ps('tv', 8, MAROON, bold=True, align=TA_CENTER)
tb = ps('tb', 8.5, MAROON, bold=True, align=TA_RIGHT)
tbn= ps('tbn',8.5, DARK,   bold=True, align=TA_LEFT)

headers = ["#", "Product Description", "Spec", "Qty\n(pcs)", "Unit Price\nFOB (USD)",
           "Freight+Ins\nper unit", "CIF Price\nper unit", "Total CIF\n(USD)"]
col_w   = [8*mm, 42*mm, 30*mm, 16*mm, 18*mm, 18*mm, 18*mm, 20*mm]

products = [
    ["01",
     "Macawiis\nChecked Cotton Fabric",
     "100% Cotton\n150×200cm\n80–100 GSM",
     "5,000", "$1.20", "$0.11", "$1.31", "$6,550"],
    ["02",
     "White Bed Sheet\nDouble Size",
     "200 TC Cotton\n206×244cm\nWhite Only",
     "1,000", "$5.20", "$0.12", "$5.32", "$5,320"],
    ["03",
     "White Bath Towel\nHotel Grade",
     "400 GSM Cotton\n70×140cm\nWhite Only",
     "1,500", "$2.80", "$0.11", "$2.91", "$4,365"],
    ["04",
     "Baati Fabric\nPlain Cotton",
     "100% Cotton\n150cm wide\n60–80 GSM",
     "500 mtr", "$0.90", "$0.10", "$1.00", "$500"],
    ["05",
     "Prayer Mat\nJanamaz",
     "Cotton Velvet\n60×110cm\nGreen/Cream",
     "500", "$2.00", "$0.10", "$2.10", "$1,050"],
]

data = [[Paragraph(h, th) for h in headers]]
for i, row in enumerate(products):
    bg = CREAM if i % 2 == 0 else WHITE
    styled = ([Paragraph(row[0], td)] +
              [Paragraph(row[1], tl)] +
              [Paragraph(row[2], ps('ts', 7, MID, align=TA_LEFT, leading=10))] +
              [Paragraph(c, tv) for c in row[3:]])
    data.append(styled)

# Subtotals row
data.append([
    Paragraph("", td),
    Paragraph("", td),
    Paragraph("", td),
    Paragraph("", td),
    Paragraph("", td),
    Paragraph("", td),
    Paragraph("SUB TOTAL", ps('st', 8.5, MAROON, bold=True, align=TA_RIGHT)),
    Paragraph("$17,785", ps('sv', 9, MAROON, bold=True, align=TA_CENTER)),
])
# Sea freight row
data.append([
    Paragraph("", td),
    Paragraph("Sea Freight — Karachi to Mogadishu Port", tl),
    Paragraph("20ft FCL Container", ps('fr', 7.5, MID, align=TA_LEFT)),
    Paragraph("1", td),
    Paragraph("", td),
    Paragraph("", td),
    Paragraph("Freight", ps('frl', 8, GOLD, bold=True, align=TA_RIGHT)),
    Paragraph("$2,800", tv),
])
# Insurance row
data.append([
    Paragraph("", td),
    Paragraph("Marine Insurance (0.5% of FOB)", tl),
    Paragraph("Cargo insurance", ps('ir', 7.5, MID, align=TA_LEFT)),
    Paragraph("", td),
    Paragraph("", td),
    Paragraph("", td),
    Paragraph("Insurance", ps('irl', 8, GOLD, bold=True, align=TA_RIGHT)),
    Paragraph("$89", tv),
])
# Grand total
data.append([
    Paragraph("", td),
    Paragraph("", td),
    Paragraph("", td),
    Paragraph("", td),
    Paragraph("", td),
    Paragraph("", td),
    Paragraph("GRAND TOTAL\nCIF Mogadishu", ps('gt', 9, WHITE, bold=True, align=TA_RIGHT, leading=12)),
    Paragraph("$20,674", ps('gv', 11, WHITE, bold=True, align=TA_CENTER, leading=14)),
])

prod_table = Table(data, colWidths=col_w)
n = len(data)
prod_table.setStyle(TableStyle([
    # Header
    ('BACKGROUND',    (0,0),   (-1,0),   MAROON),
    ('LINEBELOW',     (0,0),   (-1,0),   1.5, GOLD),
    # Alternating rows
    ('ROWBACKGROUNDS',(0,1),   (-1, n-4), [CREAM, WHITE]),
    # Subtotal row
    ('BACKGROUND',    (0,n-3), (-1,n-3), CREAM2),
    ('LINEABOVE',     (0,n-3), (-1,n-3), 1.2, GOLD),
    # Freight row
    ('BACKGROUND',    (0,n-2), (-1,n-2), CREAM),
    # Insurance row  (n-2 is freight, n-1 should be insurance... let me recount)
    # Grand total row
    ('BACKGROUND',    (0,n-1), (-1,n-1), MAROON),
    ('LINEABOVE',     (0,n-1), (-1,n-1), 1.5, GOLD),
    # Grid
    ('GRID',          (0,0),   (-1,-1),  0.4, GOLD),
    ('VALIGN',        (0,0),   (-1,-1),  'MIDDLE'),
    ('TOPPADDING',    (0,0),   (-1,-1),  3),
    ('BOTTOMPADDING', (0,0),   (-1,-1),  3),
    ('LEFTPADDING',   (0,0),   (-1,-1),  3),
    ('RIGHTPADDING',  (0,0),   (-1,-1),  3),
    # Span last column label cells
    ('SPAN',          (6,n-3), (6,n-3)),
    ('SPAN',          (6,n-2), (6,n-2)),
]))
story.append(prod_table)
story.append(Spacer(1, 3*mm))

# ══════════════════════════════════════════════════════════════════════════════
# PAYMENT + BANK DETAILS
# ══════════════════════════════════════════════════════════════════════════════
pay_hdr = Paragraph("PAYMENT INSTRUCTIONS",
                    ps('ph', 8.5, WHITE, bold=True, align=TA_LEFT))
pay_hdr_t = Table([[pay_hdr]], colWidths=[CW])
pay_hdr_t.setStyle(TableStyle([
    ('BACKGROUND',   (0,0),(-1,-1), MAROON),
    ('TOPPADDING',   (0,0),(-1,-1), 5),
    ('BOTTOMPADDING',(0,0),(-1,-1), 5),
    ('LEFTPADDING',  (0,0),(-1,-1), 10),
    ('RIGHTPADDING', (0,0),(-1,-1), 10),
    ('LINEBELOW',    (0,0),(-1,-1), 1, GOLD),
]))
story.append(pay_hdr_t)

pay_items = [
    ["Step 1 — Advance (50%)", "Pay $10,337 via Dahabshiil / Bank TT before production starts"],
    ["Step 2 — Balance (50%)", "Pay $10,337 when Bill of Lading copy is shared"],
    ["Dahabshiil (Hawala)", "Fastest & most trusted — available across Somalia & Pakistan"],
    ["Bank Transfer (TT)", "Account details provided on order confirmation"],
    ["Reference",          "Always use Invoice No. AKH-2026-001 in payment reference"],
]
pay_rows = []
for label, value in pay_items:
    pay_rows.append([
        Paragraph(label, ps('pk', 8, GOLD, bold=True, align=TA_LEFT)),
        Paragraph(value,  ps('pv', 8, DARK, align=TA_LEFT)),
    ])
pay_body = Table(pay_rows, colWidths=[50*mm, 128*mm])
pay_body.setStyle(TableStyle([
    ('BACKGROUND',   (0,0),(-1,-1), CREAM),
    ('ROWBACKGROUNDS',(0,0),(-1,-1), [CREAM, WHITE]),
    ('GRID',         (0,0),(-1,-1), 0.4, GOLD),
    ('TOPPADDING',   (0,0),(-1,-1), 4),
    ('BOTTOMPADDING',(0,0),(-1,-1), 4),
    ('LEFTPADDING',  (0,0),(-1,-1), 8),
    ('RIGHTPADDING', (0,0),(-1,-1), 8),
    ('BOX',          (0,0),(-1,-1), 0.8, GOLD),
]))
story.append(pay_body)
story.append(Spacer(1, 3*mm))

# ══════════════════════════════════════════════════════════════════════════════
# SHIPPING + DOCUMENTS
# ══════════════════════════════════════════════════════════════════════════════
ship_data = [
    [Paragraph("SHIPPING DETAILS", ps('sh', 8.5, WHITE, bold=True)),
     Paragraph("DOCUMENTS PROVIDED", ps('dh', 8.5, WHITE, bold=True))],
    [Table([
        [Paragraph("Port of Loading:", ps('sl', 8, GOLD, bold=True)),
         Paragraph("Karachi / Port Qasim, Pakistan", ps('sv2', 8, DARK))],
        [Paragraph("Port of Discharge:", ps('sl2', 8, GOLD, bold=True)),
         Paragraph("Mogadishu Port, Somalia", ps('sv3', 8, MAROON, bold=True))],
        [Paragraph("Shipping Line:", ps('sl3', 8, GOLD, bold=True)),
         Paragraph("Maersk / MSC / CMA CGM", ps('sv4', 8, DARK))],
        [Paragraph("Container:", ps('sl4', 8, GOLD, bold=True)),
         Paragraph("20ft FCL", ps('sv5', 8, DARK))],
        [Paragraph("Transit Time:", ps('sl5', 8, GOLD, bold=True)),
         Paragraph("10–14 days (via Salalah hub)", ps('sv6', 8, DARK))],
        [Paragraph("Incoterm:", ps('sl6', 8, GOLD, bold=True)),
         Paragraph("CIF Mogadishu", ps('sv7', 8, MAROON, bold=True))],
    ], colWidths=[35*mm, 50*mm]),
     Table([
         [Paragraph("✓", ps('dc', 9, MAROON, bold=True)),
          Paragraph("Commercial Invoice (3 originals)", ps('dd', 8, DARK))],
         [Paragraph("✓", ps('dc2', 9, MAROON, bold=True)),
          Paragraph("Packing List", ps('dd2', 8, DARK))],
         [Paragraph("✓", ps('dc3', 9, MAROON, bold=True)),
          Paragraph("Bill of Lading (Original 3/3)", ps('dd3', 8, DARK))],
         [Paragraph("✓", ps('dc4', 9, MAROON, bold=True)),
          Paragraph("Certificate of Origin (Pakistan)", ps('dd4', 8, DARK))],
         [Paragraph("✓", ps('dc5', 9, MAROON, bold=True)),
          Paragraph("Packing & Weight Certificate", ps('dd5', 8, DARK))],
         [Paragraph("✓", ps('dc6', 9, MAROON, bold=True)),
          Paragraph("Marine Insurance Certificate", ps('dd6', 8, DARK))],
     ], colWidths=[8*mm, 72*mm]),
    ]
]
ship_table = Table(ship_data, colWidths=[87*mm, 91*mm])
ship_table.setStyle(TableStyle([
    ('BACKGROUND',   (0,0),(-1,0), MAROON),
    ('BACKGROUND',   (0,1),(-1,1), CREAM),
    ('LINEBELOW',    (0,0),(-1,0), 1, GOLD),
    ('LINEAFTER',    (0,0),(0,-1), 0.8, GOLD),
    ('BOX',          (0,0),(-1,-1), 1, GOLD),
    ('VALIGN',       (0,0),(-1,-1), 'TOP'),
    ('TOPPADDING',   (0,0),(-1,-1), 5),
    ('BOTTOMPADDING',(0,0),(-1,-1), 5),
    ('LEFTPADDING',  (0,0),(-1,-1), 6),
    ('RIGHTPADDING', (0,0),(-1,-1), 6),
]))
story.append(ship_table)
story.append(Spacer(1, 3*mm))

# ══════════════════════════════════════════════════════════════════════════════
# TERMS + FOOTER
# ══════════════════════════════════════════════════════════════════════════════
terms_items = [
    "Prices are valid for 30 days from invoice date.",
    "Goods remain property of AKH Linen House until full payment received.",
    "All disputes subject to Pakistani jurisdiction.",
    "Buyer responsible for import duty, port clearance and inland delivery in Somalia.",
    "Samples available on request — cost deducted from first order.",
]
terms_rows = [[Paragraph(f"• {t}", ps('tr', 7.5, MID, align=TA_LEFT, leading=11))]
              for t in terms_items]
terms_hdr = Table([[Paragraph("TERMS & CONDITIONS",
                               ps('tth', 8.5, WHITE, bold=True))]],
                  colWidths=[CW])
terms_hdr.setStyle(TableStyle([
    ('BACKGROUND',   (0,0),(-1,-1), MAROON),
    ('TOPPADDING',   (0,0),(-1,-1), 4),
    ('BOTTOMPADDING',(0,0),(-1,-1), 4),
    ('LEFTPADDING',  (0,0),(-1,-1), 10),
    ('RIGHTPADDING', (0,0),(-1,-1), 10),
    ('LINEBELOW',    (0,0),(-1,-1), 1, GOLD),
]))
terms_body = Table(terms_rows, colWidths=[CW])
terms_body.setStyle(TableStyle([
    ('BACKGROUND',   (0,0),(-1,-1), CREAM2),
    ('BOX',          (0,0),(-1,-1), 0.8, GOLD),
    ('TOPPADDING',   (0,0),(-1,-1), 3),
    ('BOTTOMPADDING',(0,0),(-1,-1), 3),
    ('LEFTPADDING',  (0,0),(-1,-1), 10),
    ('RIGHTPADDING', (0,0),(-1,-1), 10),
]))
story.append(terms_hdr)
story.append(terms_body)
story.append(Spacer(1, 3*mm))

# ── Signature + Footer ────────────────────────────────────────────────────────
sig_data = [[
    Table([
        [Paragraph("Authorised Signature:", ps('asl', 8, GOLD, bold=True))],
        [Spacer(1, 8*mm)],
        [Paragraph("_________________________________", ps('asl2', 8, DARK))],
        [Paragraph("AKH Linen House", ps('asl3', 8, DARK, bold=True))],
        [Paragraph("Pakistan", ps('asl4', 7.5, MID))],
    ], colWidths=[86*mm]),
    Table([
        [Paragraph("AKH  LINEN  HOUSE", ps('fl', 11, GOLD, bold=True, align=TA_CENTER))],
        [Paragraph("Bed Linen  •  Towels  •  Fabric  •  Prayer Mats",
                   ps('fl2', 7.5, GOLD_LITE, align=TA_CENTER))],
        [Spacer(1,2*mm)],
        [Paragraph(f"WhatsApp: {WA}   |   Email: {EMAIL}",
                   ps('fl3', 8, WHITE, bold=True, align=TA_CENTER))],
    ], colWidths=[88*mm]),
]]
sig_table = Table(sig_data, colWidths=[88*mm, 90*mm])
sig_table.setStyle(TableStyle([
    ('BACKGROUND',   (0,0),(0,0), CREAM),
    ('BACKGROUND',   (1,0),(1,0), MAROON),
    ('BOX',          (0,0),(-1,-1), 1.5, GOLD),
    ('LINEAFTER',    (0,0),(0,-1), 0.8, GOLD),
    ('VALIGN',       (0,0),(-1,-1), 'MIDDLE'),
    ('TOPPADDING',   (0,0),(-1,-1), 6),
    ('BOTTOMPADDING',(0,0),(-1,-1), 6),
    ('LEFTPADDING',  (0,0),(-1,-1), 8),
    ('RIGHTPADDING', (0,0),(-1,-1), 8),
]))
story.append(sig_table)

# ── Build ──────────────────────────────────────────────────────────────────────
doc.build(story, onFirstPage=page_border, onLaterPages=page_border)
print("Proforma Invoice PDF generated successfully!")
