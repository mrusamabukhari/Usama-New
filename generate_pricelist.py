from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.platypus import (SimpleDocTemplate, Table, TableStyle,
                                 Paragraph, Spacer, Image)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.pdfgen import canvas
from reportlab.platypus import BaseDocTemplate, PageTemplate, Frame

# ── Brand colours (from logo) ─────────────────────────────────────────────────
MAROON    = colors.HexColor('#6B1535')
MAROON2   = colors.HexColor('#8B1F42')
GOLD      = colors.HexColor('#C9A84C')
GOLD_LITE = colors.HexColor('#E8D5A3')
CREAM     = colors.HexColor('#FDF8F0')
CREAM2    = colors.HexColor('#FAF3E5')
WHITE     = colors.white
DARK      = colors.HexColor('#1E1E1E')
MID       = colors.HexColor('#4A4A4A')

LOGO_PATH = "/root/.claude/uploads/821548fa-6491-4125-8b13-35cb95ca5b0f/bbf1cd60-1000645012.jpg"
OUT_PATH  = "/home/user/Usama-New/AKH_Linen_House_PriceList.pdf"

WA    = "+92 334 006 5781"
EMAIL = "akhlinenhouse@gmail.com"

W, H = A4  # 210 × 297 mm

# ── Page border decorator ──────────────────────────────────────────────────────
def page_border(c, doc):
    c.saveState()
    # Outer gold border
    c.setStrokeColor(GOLD)
    c.setLineWidth(2.5)
    c.roundRect(8*mm, 8*mm, W-16*mm, H-16*mm, 4, stroke=1, fill=0)
    # Inner thin maroon border
    c.setStrokeColor(MAROON)
    c.setLineWidth(0.6)
    c.roundRect(10.5*mm, 10.5*mm, W-21*mm, H-21*mm, 3, stroke=1, fill=0)
    c.restoreState()

# ── Document setup ─────────────────────────────────────────────────────────────
doc = SimpleDocTemplate(
    OUT_PATH, pagesize=A4,
    rightMargin=16*mm, leftMargin=16*mm,
    topMargin=13*mm, bottomMargin=13*mm,
    onPage=page_border,
)

story = []
CW = 178*mm   # usable content width

# ── Paragraph style factory ────────────────────────────────────────────────────
def ps(name, size=8, color=DARK, font='Helvetica', align=TA_CENTER,
       leading=None, bold=False, leftIndent=0, spaceAfter=0):
    if bold:
        font = font + '-Bold'
    return ParagraphStyle(name, fontSize=size, textColor=color,
                          fontName=font, alignment=align,
                          leading=leading or size*1.35,
                          leftIndent=leftIndent, spaceAfter=spaceAfter)

# ══════════════════════════════════════════════════════════════════════════════
# HEADER — Logo + company name + contact strip
# ══════════════════════════════════════════════════════════════════════════════
logo = Image(LOGO_PATH, width=52*mm, height=36*mm)

company_block = [
    Paragraph("AKH LINEN HOUSE",
              ps('co', 20, MAROON, bold=True, leading=24)),
    Spacer(1, 1.5*mm),
    Paragraph("Pakistani Textile Export Agency",
              ps('co2', 9, GOLD, leading=12)),
    Spacer(1, 1*mm),
    Paragraph("Bed Linen  •  Towels  •  Fabric  •  Prayer Mats",
              ps('co3', 7.5, MID, leading=11)),
]

hdr_inner = Table(
    [[logo, [Spacer(1,6*mm)] + company_block]],
    colWidths=[56*mm, 122*mm]
)
hdr_inner.setStyle(TableStyle([
    ('VALIGN',        (0,0),(-1,-1), 'MIDDLE'),
    ('LEFTPADDING',   (0,0),(-1,-1), 0),
    ('RIGHTPADDING',  (0,0),(-1,-1), 0),
    ('TOPPADDING',    (0,0),(-1,-1), 0),
    ('BOTTOMPADDING', (0,0),(-1,-1), 0),
]))
story.append(hdr_inner)
story.append(Spacer(1, 3*mm))

# Gold divider line
div = Table([['']], colWidths=[CW], rowHeights=[1.8])
div.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),GOLD)]))
story.append(div)
story.append(Spacer(1, 2*mm))

# Contact strip
contact_data = [[
    Paragraph(f"<b>WhatsApp:</b>  {WA}",
              ps('ct1', 8, WHITE, align=TA_LEFT,  leading=11)),
    Paragraph("WHOLESALE PRICE LIST",
              ps('ct2', 9, GOLD,  align=TA_CENTER, leading=12, bold=True)),
    Paragraph(f"<b>Email:</b>  {EMAIL}",
              ps('ct3', 8, WHITE, align=TA_RIGHT, leading=11)),
]]
ct = Table(contact_data, colWidths=[62*mm, 62*mm, 54*mm])
ct.setStyle(TableStyle([
    ('BACKGROUND',    (0,0),(-1,-1), MAROON),
    ('VALIGN',        (0,0),(-1,-1), 'MIDDLE'),
    ('TOPPADDING',    (0,0),(-1,-1), 5),
    ('BOTTOMPADDING', (0,0),(-1,-1), 5),
    ('LEFTPADDING',   (0,0),(-1,-1), 8),
    ('RIGHTPADDING',  (0,0),(-1,-1), 8),
    ('LINEBELOW',     (0,0),(-1,0),  1, GOLD),
]))
story.append(ct)
story.append(Spacer(1, 2*mm))

# Sub-info strip
info_data = [[
    Paragraph("All Prices: FOB Karachi (USD)",
              ps('inf1', 7.5, MAROON, align=TA_LEFT,   bold=True)),
    Paragraph("Delivery: Karachi → Dubai  7–10 Days",
              ps('inf2', 7.5, MAROON, align=TA_CENTER, bold=True)),
    Paragraph("Payment: 30% Advance / 70% Before Shipment",
              ps('inf3', 7.5, MAROON, align=TA_RIGHT,  bold=True)),
]]
inf = Table(info_data, colWidths=[60*mm, 70*mm, 48*mm])
inf.setStyle(TableStyle([
    ('BACKGROUND',    (0,0),(-1,-1), CREAM2),
    ('VALIGN',        (0,0),(-1,-1), 'MIDDLE'),
    ('TOPPADDING',    (0,0),(-1,-1), 4),
    ('BOTTOMPADDING', (0,0),(-1,-1), 4),
    ('LEFTPADDING',   (0,0),(-1,-1), 8),
    ('RIGHTPADDING',  (0,0),(-1,-1), 8),
    ('BOX',           (0,0),(-1,-1), 0.8, GOLD),
]))
story.append(inf)
story.append(Spacer(1, 4*mm))

# ── HELPERS ────────────────────────────────────────────────────────────────────
def sec_hdr(num, title, subtitle):
    left = Paragraph(
        f'<font color="#C9A84C"><b>{num}</b></font>'
        f'<font color="#FFFFFF">  {title}</font>',
        ps('sh', 10, WHITE, bold=False, align=TA_LEFT, leading=14))
    right = Paragraph(subtitle, ps('sh2', 7.5, GOLD_LITE, align=TA_RIGHT, leading=11))
    t = Table([[left, right]], colWidths=[105*mm, 73*mm])
    t.setStyle(TableStyle([
        ('BACKGROUND',    (0,0),(-1,-1), MAROON),
        ('VALIGN',        (0,0),(-1,-1), 'MIDDLE'),
        ('TOPPADDING',    (0,0),(-1,-1), 6),
        ('BOTTOMPADDING', (0,0),(-1,-1), 6),
        ('LEFTPADDING',   (0,0),(-1,-1), 10),
        ('RIGHTPADDING',  (0,0),(-1,-1), 10),
        ('LINEBELOW',     (0,0),(-1,-1), 1.5, GOLD),
    ]))
    return t

def spec(text):
    return Paragraph(
        f'<font color="#6B1535"><b>›</b></font>  {text}',
        ps('sp', 7.5, MID, align=TA_LEFT, leading=12, leftIndent=3))

def price_tbl(headers, rows, widths):
    th = ps('th', 8, WHITE, bold=True, align=TA_CENTER)
    td = ps('td', 8, DARK,  align=TA_CENTER)
    tv = ps('tv', 8, MAROON, bold=True, align=TA_CENTER)
    data = [[Paragraph(h, th) for h in headers]]
    for r in rows:
        data.append([Paragraph(r[0], td)] +
                    [Paragraph(c, tv) for c in r[1:]])
    t = Table(data, colWidths=widths)
    t.setStyle(TableStyle([
        ('BACKGROUND',    (0,0),  (-1,0),  MAROON),
        ('ROWBACKGROUNDS',(0,1),  (-1,-1), [CREAM, WHITE]),
        ('GRID',          (0,0),  (-1,-1), 0.5, GOLD),
        ('VALIGN',        (0,0),  (-1,-1), 'MIDDLE'),
        ('TOPPADDING',    (0,0),  (-1,-1), 4),
        ('BOTTOMPADDING', (0,0),  (-1,-1), 4),
        ('LEFTPADDING',   (0,0),  (-1,-1), 4),
        ('RIGHTPADDING',  (0,0),  (-1,-1), 4),
        ('LINEBELOW',     (0,-1), (-1,-1), 1, GOLD),
    ]))
    return t

def moq(qty, days):
    return Paragraph(
        f'<font color="#6B1535"><b>MOQ:</b></font> {qty}'
        f'&nbsp;&nbsp;&nbsp;'
        f'<font color="#6B1535"><b>Lead Time:</b></font> {days}',
        ps('mq', 7.5, MID, align=TA_RIGHT, leading=11))

def product_row(specs, pt, spec_w=88*mm, tbl_w=90*mm):
    inner = Table([[s] for s in specs], colWidths=[spec_w-2*mm])
    inner.setStyle(TableStyle([
        ('TOPPADDING',    (0,0),(-1,-1), 1),
        ('BOTTOMPADDING', (0,0),(-1,-1), 1),
        ('LEFTPADDING',   (0,0),(-1,-1), 0),
        ('RIGHTPADDING',  (0,0),(-1,-1), 0),
    ]))
    combo = Table([[inner, pt]], colWidths=[spec_w, tbl_w])
    combo.setStyle(TableStyle([
        ('VALIGN',        (0,0),(-1,-1), 'TOP'),
        ('LEFTPADDING',   (0,0),(-1,-1), 0),
        ('RIGHTPADDING',  (0,0),(-1,-1), 0),
        ('TOPPADDING',    (0,0),(-1,-1), 2),
        ('BOTTOMPADDING', (0,0),(-1,-1), 2),
    ]))
    return combo

# ══════════════════════════════════════════════════════════════════════════════
# 1. MACAWIIS
# ══════════════════════════════════════════════════════════════════════════════
story.append(sec_hdr("01", "MACAWIIS — Cotton Checked Fabric",
                     "Men's Traditional Sarong  |  #1 Somali Item"))
story.append(Spacer(1, 2*mm))
story.append(product_row(
    [spec("Material: 100% Cotton  |  GSM: 80–100"),
     spec("Size (finished): 150 cm × 200 cm"),
     spec("Pattern: Checked — White+Blue / White+Green / White+Red"),
     spec("Custom colours available on bulk orders")],
    price_tbl(
        ["Quantity", "Price / Piece", "Price / Dozen"],
        [["500 – 999 pcs",     "$ 2.50", "$ 28.00"],
         ["1,000 – 2,999 pcs", "$ 2.20", "$ 25.00"],
         ["3,000 – 4,999 pcs", "$ 1.90", "$ 22.00"],
         ["5,000 + pcs",       "$ 1.60", "$ 18.50"]],
        [64*mm, 58*mm, 58*mm]
    )
))
story.append(moq("500 pieces", "10–14 days"))
story.append(Spacer(1, 3.5*mm))

# ══════════════════════════════════════════════════════════════════════════════
# 2. BAATI FABRIC
# ══════════════════════════════════════════════════════════════════════════════
story.append(sec_hdr("02", "BAATI FABRIC — Plain Cotton",
                     "Women's House Dress Fabric  |  White & Soft Colours"))
story.append(Spacer(1, 2*mm))
story.append(product_row(
    [spec("Material: 100% Cotton / Cotton-Rayon Blend"),
     spec("Width: 150 cm  |  GSM: 60–80"),
     spec("Colours: White, Cream, Light Pastels, Soft Prints"),
     spec("Sold per meter or full roll (60 m/roll)")],
    price_tbl(
        ["Quantity", "Price / Meter", "Price / Roll (60m)"],
        [["200 – 499 m",       "$ 1.20", "$ 68.00"],
         ["500 – 999 m",       "$ 1.05", "$ 60.00"],
         ["1,000 – 1,999 m",   "$ 0.90", "$ 52.00"],
         ["2,000 + m",         "$ 0.75", "$ 43.00"]],
        [64*mm, 58*mm, 58*mm]
    )
))
story.append(moq("200 meters", "7–10 days"))
story.append(Spacer(1, 3.5*mm))

# ══════════════════════════════════════════════════════════════════════════════
# 3. WHITE BED SHEET
# ══════════════════════════════════════════════════════════════════════════════
story.append(sec_hdr("03", "WHITE BED SHEET — Double Size",
                     "100% Cotton  |  200 TC  |  Hotel & Household Grade"))
story.append(Spacer(1, 2*mm))
story.append(product_row(
    [spec("Size: 81\" × 96\"  (206 × 244 cm) — Double"),
     spec("Thread Count: 200 TC  |  Material: 100% Cotton"),
     spec("Colour: White Only  |  Export polybag packing"),
     spec("Set = 1 Flat Sheet + 2 Pillowcases (20\" × 26\")")],
    price_tbl(
        ["Quantity", "Price / Piece", "Set Price (+2 PC)"],
        [["200 – 499 pcs",     "$ 6.50", "$ 9.00"],
         ["500 – 999 pcs",     "$ 5.80", "$ 8.00"],
         ["1,000 – 2,999 pcs", "$ 5.20", "$ 7.20"],
         ["3,000 + pcs",       "$ 4.50", "$ 6.20"]],
        [64*mm, 58*mm, 58*mm]
    )
))
story.append(moq("200 pieces", "10–12 days"))
story.append(Spacer(1, 3.5*mm))

# ══════════════════════════════════════════════════════════════════════════════
# 4. BATH TOWEL
# ══════════════════════════════════════════════════════════════════════════════
story.append(sec_hdr("04", "WHITE BATH TOWEL — Hotel Grade",
                     "70×140 cm  |  400 GSM  |  100% Ring-Spun Cotton"))
story.append(Spacer(1, 2*mm))
story.append(product_row(
    [spec("Size: 70 × 140 cm  |  Weight: 400 GSM"),
     spec("Material: 100% Ring-Spun Cotton"),
     spec("Colour: White Only  |  Individually polybag packed"),
     spec("Set = Bath Towel + Hand Towel + Face Towel (3 pcs)")],
    price_tbl(
        ["Quantity", "Price / Piece", "3-Piece Set"],
        [["500 – 999 pcs",     "$ 3.20", "$ 5.50"],
         ["1,000 – 2,999 pcs", "$ 2.80", "$ 4.80"],
         ["3,000 – 4,999 pcs", "$ 2.40", "$ 4.20"],
         ["5,000 + pcs",       "$ 2.00", "$ 3.50"]],
        [64*mm, 58*mm, 58*mm]
    )
))
story.append(moq("500 pieces", "10–14 days"))
story.append(Spacer(1, 3.5*mm))

# ══════════════════════════════════════════════════════════════════════════════
# 5 & 6 — PRAYER MAT  +  PLAIN COTTON FABRIC  (side by side)
# ══════════════════════════════════════════════════════════════════════════════
def mini_sec(num, title, sub):
    tp = Paragraph(
        f'<font color="#C9A84C"><b>{num}</b></font>'
        f'<font color="#FFFFFF">  {title}</font>',
        ps('msh', 9, WHITE, bold=False, align=TA_LEFT, leading=13))
    sp2 = Paragraph(sub, ps('mss', 7, GOLD_LITE, align=TA_LEFT, leading=10))
    t = Table([[tp],[sp2]], colWidths=[85*mm])
    t.setStyle(TableStyle([
        ('BACKGROUND',    (0,0),(-1,-1), MAROON),
        ('TOPPADDING',    (0,0),(-1,-1), 5),
        ('BOTTOMPADDING', (0,0),(-1,-1), 5),
        ('LEFTPADDING',   (0,0),(-1,-1), 8),
        ('RIGHTPADDING',  (0,0),(-1,-1), 8),
        ('LINEBELOW',     (0,-1),(-1,-1), 1.5, GOLD),
    ]))
    return t

# Prayer Mat block
pm_specs = [spec("Size: 60 × 110 cm  |  Cotton/Poly Velvet"),
            spec("Design: Mosque / Geometric prints"),
            spec("Colours: Green, Cream, Red, Blue")]
pm_pt = price_tbl(
    ["Quantity","Price / Piece"],
    [["500 – 999 pcs","$ 2.50"],["1,000 – 2,999","$ 2.00"],
     ["3,000 – 4,999","$ 1.60"],["5,000 + pcs",  "$ 1.30"]],
    [42.5*mm, 42.5*mm])
pm_blk = Table(
    [[mini_sec("05","PRAYER MAT — Janamaz","Cotton Velvet  |  60 × 110 cm")],
     [Table([[s] for s in pm_specs], colWidths=[85*mm])],
     [pm_pt],
     [moq("500 pcs","7–10 days")]],
    colWidths=[85*mm])
pm_blk.setStyle(TableStyle([
    ('LEFTPADDING',  (0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(-1,-1),0),
    ('TOPPADDING',   (0,0),(-1,-1),1),('BOTTOMPADDING',(0,0),(-1,-1),1),]))

# Plain Cotton block
pf_specs = [spec("Material: 100% Cotton Poplin"),
            spec("Width: 150 cm / 240 cm  |  GSM: 80–100"),
            spec("Colour: White Bleached / Off-White")]
pf_pt = price_tbl(
    ["Quantity","Price / Meter"],
    [["200 – 499 m",   "$ 1.10"],["500 – 999 m",   "$ 0.95"],
     ["1,000 – 2,999 m","$ 0.80"],["3,000 + m",     "$ 0.65"]],
    [42.5*mm, 42.5*mm])
pf_blk = Table(
    [[mini_sec("06","PLAIN WHITE COTTON FABRIC","Bulk Roll  |  100% Cotton Poplin")],
     [Table([[s] for s in pf_specs], colWidths=[85*mm])],
     [pf_pt],
     [moq("200 meters","7–10 days")]],
    colWidths=[85*mm])
pf_blk.setStyle(TableStyle([
    ('LEFTPADDING',  (0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(-1,-1),0),
    ('TOPPADDING',   (0,0),(-1,-1),1),('BOTTOMPADDING',(0,0),(-1,-1),1),]))

row56 = Table([[pm_blk, Spacer(8*mm,1), pf_blk]],
              colWidths=[87*mm, 4*mm, 87*mm])
row56.setStyle(TableStyle([
    ('VALIGN',       (0,0),(-1,-1),'TOP'),
    ('LEFTPADDING',  (0,0),(-1,-1),0),
    ('RIGHTPADDING', (0,0),(-1,-1),0),]))
story.append(row56)
story.append(Spacer(1, 4*mm))

# ── TERMS BAR ─────────────────────────────────────────────────────────────────
terms_items = [
    ("Payment", "30% Advance | 70% Before Shipment"),
    ("Prices",  "FOB Karachi (USD)"),
    ("Samples", "Available on Request"),
    ("Validity","30 Days from Date of Issue"),
]
ts_hdr = ps('tsh', 8, WHITE,  bold=True, align=TA_CENTER)
ts_val = ps('tsv', 7.5, DARK, align=TA_CENTER, leading=11)
ts_lbl = ps('tsl', 7,  GOLD,  align=TA_CENTER, leading=10)
terms_cells = [[Paragraph(l, ts_lbl), Paragraph(v, ts_val)]
               for l,v in terms_items]
terms_inner = Table(terms_cells,
                    colWidths=[22*mm, 22*mm, 18*mm, 22*mm,
                                18*mm, 28*mm, 18*mm, 30*mm])

# flatten into single row
flat_cells   = []
flat_widths  = []
for i,(l,v) in enumerate(terms_items):
    flat_cells.append(Paragraph(l, ts_lbl))
    flat_cells.append(Paragraph(v, ts_val))
    flat_widths += [22*mm, (CW//4 - 22*mm)]

terms_row = Table(
    [[Paragraph("TERMS & CONDITIONS", ts_hdr)]] +
    [[Table([[Paragraph(l,ts_lbl), Paragraph(v,ts_val)]
             for l,v in terms_items],
            colWidths=[20*mm,24*mm,16*mm,30*mm,16*mm,26*mm,18*mm,28*mm])]],
    colWidths=[CW])

# Simpler flat layout
tc_data = [[
    Paragraph(f'<font color="#C9A84C"><b>Payment:</b></font>  30% Advance | 70% Before Shipment', ts_val),
    Paragraph(f'<font color="#C9A84C"><b>Prices:</b></font>  FOB Karachi (USD)', ts_val),
    Paragraph(f'<font color="#C9A84C"><b>Samples:</b></font>  Available on Request', ts_val),
    Paragraph(f'<font color="#C9A84C"><b>Validity:</b></font>  30 Days from Issue', ts_val),
]]
tc = Table(
    [[Paragraph("TERMS & CONDITIONS", ts_hdr)], tc_data],
    colWidths=[CW])
tc.setStyle(TableStyle([
    ('BACKGROUND',    (0,0),(-1,0), MAROON),
    ('BACKGROUND',    (0,1),(-1,1), CREAM2),
    ('VALIGN',        (0,0),(-1,-1),'MIDDLE'),
    ('TOPPADDING',    (0,0),(-1,-1), 5),
    ('BOTTOMPADDING', (0,0),(-1,-1), 5),
    ('LEFTPADDING',   (0,0),(-1,-1), 8),
    ('RIGHTPADDING',  (0,0),(-1,-1), 8),
    ('BOX',           (0,0),(-1,-1), 1.2, GOLD),
    ('LINEABOVE',     (0,1),(-1,1), 0.8, GOLD),
]))
story.append(tc)
story.append(Spacer(1, 3*mm))

# ── CONTACT FOOTER ─────────────────────────────────────────────────────────────
cf_data = [
    [Paragraph("AKH  LINEN  HOUSE",
               ps('cf1', 11, GOLD, bold=True, align=TA_CENTER, leading=15))],
    [Paragraph("Bed Linen  •  Towels  •  Fabric  •  Prayer Mats",
               ps('cf2', 7.5, GOLD_LITE, align=TA_CENTER, leading=11))],
    [Spacer(1, 1*mm)],
    [Table([[
        Paragraph(f"WhatsApp:  {WA}",
                  ps('cf3', 8.5, WHITE, bold=True, align=TA_LEFT, leading=12)),
        Paragraph("Pakistan",
                  ps('cf4', 8.5, GOLD,  bold=True, align=TA_CENTER, leading=12)),
        Paragraph(f"Email:  {EMAIL}",
                  ps('cf5', 8.5, WHITE, bold=True, align=TA_RIGHT, leading=12)),
    ]], colWidths=[68*mm, 42*mm, 68*mm])],
]
cf = Table(cf_data, colWidths=[CW])
cf.setStyle(TableStyle([
    ('BACKGROUND',    (0,0),(-1,-1), MAROON),
    ('VALIGN',        (0,0),(-1,-1),'MIDDLE'),
    ('TOPPADDING',    (0,0),(-1,-1), 4),
    ('BOTTOMPADDING', (0,0),(-1,-1), 4),
    ('LEFTPADDING',   (0,0),(-1,-1), 10),
    ('RIGHTPADDING',  (0,0),(-1,-1), 10),
    ('BOX',           (0,0),(-1,-1), 1.5, GOLD),
    ('LINEABOVE',     (0,3),(-1,3), 0.8, GOLD),
]))
story.append(cf)

# ── BUILD ──────────────────────────────────────────────────────────────────────
doc.build(story, onFirstPage=page_border, onLaterPages=page_border)
print("PDF generated successfully!")
