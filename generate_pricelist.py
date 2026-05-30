from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.platypus import KeepTogether

# Colors matching the logo
MAROON    = colors.HexColor('#7B1C3E')
GOLD      = colors.HexColor('#C9A84C')
DARK_GOLD = colors.HexColor('#9A7A2A')
CREAM     = colors.HexColor('#FDF8F0')
WHITE     = colors.white
LIGHT_GRAY= colors.HexColor('#F5F5F5')
DARK_TEXT = colors.HexColor('#2C2C2C')

W, H = A4

doc = SimpleDocTemplate(
    "/home/user/Usama-New/AKH_Linen_House_PriceList.pdf",
    pagesize=A4,
    rightMargin=15*mm,
    leftMargin=15*mm,
    topMargin=10*mm,
    bottomMargin=12*mm,
)

styles = getSampleStyleSheet()
story  = []

# ── LOGO ──────────────────────────────────────────────────────────────────────
logo = Image(
    "/root/.claude/uploads/821548fa-6491-4125-8b13-35cb95ca5b0f/bbf1cd60-1000645012.jpg",
    width=55*mm, height=38*mm
)
logo.hAlign = 'CENTER'
story.append(logo)
story.append(Spacer(1, 2*mm))

# ── HEADER BANNER ─────────────────────────────────────────────────────────────
hdr_style = ParagraphStyle('hdr', fontSize=7.5, textColor=WHITE,
                            alignment=TA_CENTER, fontName='Helvetica',
                            spaceAfter=0, spaceBefore=0, leading=11)
hdr_data = [[
    Paragraph("WhatsApp: [Your Number]", hdr_style),
    Paragraph("AKH LINEN HOUSE — Pakistani Textile Export Agency",
              ParagraphStyle('hdr2', fontSize=7.5, textColor=GOLD,
                             alignment=TA_CENTER, fontName='Helvetica-Bold',
                             leading=11)),
    Paragraph("Email: [Your Email]", hdr_style),
]]
hdr_table = Table(hdr_data, colWidths=[55*mm, 72*mm, 53*mm])
hdr_table.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,-1), MAROON),
    ('VALIGN',     (0,0), (-1,-1), 'MIDDLE'),
    ('TOPPADDING', (0,0), (-1,-1), 4),
    ('BOTTOMPADDING',(0,0),(-1,-1),4),
    ('LEFTPADDING',(0,0),(-1,-1), 6),
    ('RIGHTPADDING',(0,0),(-1,-1),6),
]))
story.append(hdr_table)
story.append(Spacer(1, 3*mm))

# ── TITLE BOX ─────────────────────────────────────────────────────────────────
title_style = ParagraphStyle('title', fontSize=11, textColor=WHITE,
                              alignment=TA_CENTER, fontName='Helvetica-Bold',
                              leading=15)
sub_style   = ParagraphStyle('sub', fontSize=7.5, textColor=GOLD,
                              alignment=TA_CENTER, fontName='Helvetica',
                              leading=11)
title_data = [[
    Paragraph("WHOLESALE PRICE LIST — NAIF SOUK DUBAI", title_style),
    Paragraph("All Prices: FOB Karachi (USD)  |  Delivery: 7–10 Days  |  Payment: 30% Advance / 70% Before Shipment", sub_style),
]]
title_table = Table(title_data, colWidths=[180*mm])
title_table.setStyle(TableStyle([
    ('BACKGROUND', (0,0),(-1,-1), MAROON),
    ('TOPPADDING', (0,0),(-1,-1), 5),
    ('BOTTOMPADDING',(0,0),(-1,-1),5),
    ('LEFTPADDING',(0,0),(-1,-1),8),
    ('RIGHTPADDING',(0,0),(-1,-1),8),
    ('ROUNDEDCORNERS',[3,3,3,3]),
]))
story.append(title_table)
story.append(Spacer(1, 4*mm))

# ── HELPER: section header ─────────────────────────────────────────────────────
def section_header(number, title, subtitle):
    s = ParagraphStyle('sh', fontSize=9.5, textColor=WHITE,
                       fontName='Helvetica-Bold', leading=13)
    s2= ParagraphStyle('sh2',fontSize=7.5, textColor=GOLD,
                       fontName='Helvetica', leading=11)
    t = Table([[Paragraph(f"{number}.  {title}", s),
                Paragraph(subtitle, s2)]],
              colWidths=[90*mm, 90*mm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0),(-1,-1), MAROON),
        ('VALIGN',     (0,0),(-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0),(-1,-1), 5),
        ('BOTTOMPADDING',(0,0),(-1,-1),5),
        ('LEFTPADDING',(0,0),(-1,-1),8),
        ('RIGHTPADDING',(0,0),(-1,-1),8),
    ]))
    return t

# ── HELPER: spec line ──────────────────────────────────────────────────────────
def spec_para(text):
    return Paragraph(f"<font color='#{MAROON.hexval()[2:]}'>▸</font>  {text}",
                     ParagraphStyle('sp', fontSize=7.5, textColor=DARK_TEXT,
                                    fontName='Helvetica', leading=11,
                                    leftIndent=4))

# ── HELPER: price table ────────────────────────────────────────────────────────
def price_table(headers, rows, col_widths):
    h_style = ParagraphStyle('th', fontSize=8, textColor=WHITE,
                              fontName='Helvetica-Bold', alignment=TA_CENTER)
    r_style = ParagraphStyle('td', fontSize=8, textColor=DARK_TEXT,
                              fontName='Helvetica', alignment=TA_CENTER)
    b_style = ParagraphStyle('td2',fontSize=8, textColor=MAROON,
                              fontName='Helvetica-Bold', alignment=TA_CENTER)

    data = [[Paragraph(h, h_style) for h in headers]]
    for i, row in enumerate(rows):
        styled = []
        for j, cell in enumerate(row):
            if j == 0:
                styled.append(Paragraph(cell, r_style))
            else:
                styled.append(Paragraph(cell, b_style))
        data.append(styled)

    t = Table(data, colWidths=col_widths)
    ts = TableStyle([
        ('BACKGROUND', (0,0),(-1,0),  MAROON),
        ('BACKGROUND', (0,1),(-1,1),  CREAM),
        ('BACKGROUND', (0,2),(-1,2),  WHITE),
        ('BACKGROUND', (0,3),(-1,3),  CREAM),
        ('BACKGROUND', (0,4),(-1,4),  WHITE) if len(rows)>3 else ('SPAN',(0,0),(0,0)),
        ('ROWBACKGROUNDS',(0,1),(-1,-1),[CREAM, WHITE]),
        ('GRID',       (0,0),(-1,-1), 0.5, GOLD),
        ('VALIGN',     (0,0),(-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0),(-1,-1), 4),
        ('BOTTOMPADDING',(0,0),(-1,-1),4),
        ('LEFTPADDING',(0,0),(-1,-1), 4),
        ('RIGHTPADDING',(0,0),(-1,-1),4),
    ])
    t.setStyle(ts)
    return t

def moq_line(moq, lead):
    return Paragraph(
        f"<font color='#{MAROON.hexval()[2:]}'>MOQ:</font> <b>{moq}</b>    "
        f"<font color='#{MAROON.hexval()[2:]}'>Lead Time:</font> <b>{lead}</b>",
        ParagraphStyle('moq', fontSize=7.5, textColor=DARK_TEXT,
                       fontName='Helvetica', alignment=TA_RIGHT, leading=11)
    )

# ══════════════════════════════════════════════════════════════════════════════
# PRODUCT 1 — MACAWIIS
# ══════════════════════════════════════════════════════════════════════════════
story.append(section_header("1","MACAWIIS — Cotton Checked Fabric","Men's Traditional Sarong  |  Most Popular Somali Item"))
story.append(Spacer(1,2*mm))

spec_col = [
    spec_para("Material: 100% Cotton"),
    spec_para("Size: 150 cm × 200 cm (Ready-to-wear)"),
    spec_para("GSM: 80–100 GSM  |  Width: 150 cm"),
    spec_para("Pattern: Checked — White+Blue / White+Green / White+Red"),
]
pt1 = price_table(
    ["Quantity","Price / Piece","Price / Dozen"],
    [
        ["500 – 999 pcs",    "$ 2.50", "$ 28.00"],
        ["1,000 – 2,999 pcs","$ 2.20", "$ 25.00"],
        ["3,000 – 4,999 pcs","$ 1.90", "$ 22.00"],
        ["5,000 + pcs",      "$ 1.60", "$ 18.50"],
    ],
    [65*mm, 57.5*mm, 57.5*mm]
)
combo1 = Table([[Table([[s] for s in spec_col], colWidths=[88*mm]), pt1]],
               colWidths=[90*mm,90*mm])
combo1.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),
                             ('LEFTPADDING',(0,0),(-1,-1),0),
                             ('RIGHTPADDING',(0,0),(-1,-1),0),]))
story.append(combo1)
story.append(moq_line("500 pieces","10–14 days"))
story.append(Spacer(1,4*mm))

# ══════════════════════════════════════════════════════════════════════════════
# PRODUCT 2 — BAATI FABRIC
# ══════════════════════════════════════════════════════════════════════════════
story.append(section_header("2","BAATI FABRIC — Plain Cotton","Women's House Dress Fabric  |  White & Light Colors"))
story.append(Spacer(1,2*mm))

spec_col2 = [
    spec_para("Material: 100% Cotton / Cotton-Rayon Blend"),
    spec_para("Width: 150 cm  |  GSM: 60–80 GSM"),
    spec_para("Color: White, Cream, Light Colors, Soft Prints"),
    spec_para("Sold by meter or full roll (60 meters/roll)"),
]
pt2 = price_table(
    ["Quantity","Price / Meter","Price / Roll (60m)"],
    [
        ["200 – 499 meters",  "$ 1.20","$ 68.00"],
        ["500 – 999 meters",  "$ 1.05","$ 60.00"],
        ["1,000 – 1,999 mtr", "$ 0.90","$ 52.00"],
        ["2,000 + meters",    "$ 0.75","$ 43.00"],
    ],
    [65*mm, 57.5*mm, 57.5*mm]
)
combo2 = Table([[Table([[s] for s in spec_col2], colWidths=[88*mm]), pt2]],
               colWidths=[90*mm,90*mm])
combo2.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),
                             ('LEFTPADDING',(0,0),(-1,-1),0),
                             ('RIGHTPADDING',(0,0),(-1,-1),0),]))
story.append(combo2)
story.append(moq_line("200 meters","7–10 days"))
story.append(Spacer(1,4*mm))

# ══════════════════════════════════════════════════════════════════════════════
# PRODUCT 3 — BED SHEET
# ══════════════════════════════════════════════════════════════════════════════
story.append(section_header("3","WHITE BED SHEET — Double Size","100% Cotton  |  200 TC  |  Hotel & Household"))
story.append(Spacer(1,2*mm))

spec_col3 = [
    spec_para("Size: 81\" × 96\" (206 × 244 cm)  — Double"),
    spec_para("Thread Count: 200 TC  |  Material: 100% Cotton"),
    spec_para("Color: White Only"),
    spec_para("Set = 1 Flat Sheet + 2 Pillowcases (20\"×26\")"),
]
pt3 = price_table(
    ["Quantity","Price / Piece","Price / Set (+2 PC)"],
    [
        ["200 – 499 pcs",    "$ 6.50","$ 9.00"],
        ["500 – 999 pcs",    "$ 5.80","$ 8.00"],
        ["1,000 – 2,999 pcs","$ 5.20","$ 7.20"],
        ["3,000 + pcs",      "$ 4.50","$ 6.20"],
    ],
    [65*mm, 57.5*mm, 57.5*mm]
)
combo3 = Table([[Table([[s] for s in spec_col3], colWidths=[88*mm]), pt3]],
               colWidths=[90*mm,90*mm])
combo3.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),
                             ('LEFTPADDING',(0,0),(-1,-1),0),
                             ('RIGHTPADDING',(0,0),(-1,-1),0),]))
story.append(combo3)
story.append(moq_line("200 pieces","10–12 days"))
story.append(Spacer(1,4*mm))

# ══════════════════════════════════════════════════════════════════════════════
# PRODUCT 4 — BATH TOWEL
# ══════════════════════════════════════════════════════════════════════════════
story.append(section_header("4","WHITE BATH TOWEL — Hotel Grade","70×140 cm  |  400 GSM  |  100% Cotton Ring Spun"))
story.append(Spacer(1,2*mm))

spec_col4 = [
    spec_para("Size: 70 × 140 cm  |  GSM: 400 GSM"),
    spec_para("Material: 100% Cotton (Ring Spun)"),
    spec_para("Color: White Only  |  Individually polybag packed"),
    spec_para("Set = Bath Towel + Hand Towel + Face Towel"),
]
pt4 = price_table(
    ["Quantity","Price / Piece","Set (Bath+Hand+Face)"],
    [
        ["500 – 999 pcs",    "$ 3.20","$ 5.50 / set"],
        ["1,000 – 2,999 pcs","$ 2.80","$ 4.80 / set"],
        ["3,000 – 4,999 pcs","$ 2.40","$ 4.20 / set"],
        ["5,000 + pcs",      "$ 2.00","$ 3.50 / set"],
    ],
    [65*mm, 57.5*mm, 57.5*mm]
)
combo4 = Table([[Table([[s] for s in spec_col4], colWidths=[88*mm]), pt4]],
               colWidths=[90*mm,90*mm])
combo4.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),
                             ('LEFTPADDING',(0,0),(-1,-1),0),
                             ('RIGHTPADDING',(0,0),(-1,-1),0),]))
story.append(combo4)
story.append(moq_line("500 pieces","10–14 days"))
story.append(Spacer(1,4*mm))

# ══════════════════════════════════════════════════════════════════════════════
# PRODUCTS 5 & 6 — PRAYER MAT + PLAIN FABRIC (side by side mini tables)
# ══════════════════════════════════════════════════════════════════════════════
# Left: Prayer Mat
pm_hdr = ParagraphStyle('pmh',fontSize=9,textColor=WHITE,
                         fontName='Helvetica-Bold',alignment=TA_CENTER,leading=13)
pm_sub = ParagraphStyle('pms',fontSize=7,textColor=GOLD,
                         fontName='Helvetica',alignment=TA_CENTER,leading=10)
pm_head = Table([[Paragraph("5.  PRAYER MAT — Janamaz",pm_hdr)],
                  [Paragraph("Cotton Velvet  |  60×110 cm",pm_sub)]],
                colWidths=[86*mm])
pm_head.setStyle(TableStyle([
    ('BACKGROUND',(0,0),(-1,-1),MAROON),
    ('TOPPADDING',(0,0),(-1,-1),4),('BOTTOMPADDING',(0,0),(-1,-1),4),
    ('LEFTPADDING',(0,0),(-1,-1),6),('RIGHTPADDING',(0,0),(-1,-1),6),
]))

pm_price = price_table(
    ["Quantity","Price / Piece"],
    [["500–999 pcs","$ 2.50"],["1,000–2,999","$ 2.00"],
     ["3,000–4,999","$ 1.60"],["5,000+ pcs", "$ 1.30"]],
    [43*mm, 43*mm]
)
pm_specs = [
    spec_para("Size: 60 × 110 cm"),
    spec_para("Material: Cotton/Polyester Velvet"),
    spec_para("Design: Mosque / Geometric"),
    spec_para("Colors: Green, Cream, Red, Blue"),
]
pm_block = Table(
    [[pm_head],[Table([[s] for s in pm_specs],colWidths=[86*mm])],[pm_price],
     [moq_line("500 pcs","7–10 days")]],
    colWidths=[86*mm]
)
pm_block.setStyle(TableStyle([('LEFTPADDING',(0,0),(-1,-1),0),
                               ('RIGHTPADDING',(0,0),(-1,-1),0),
                               ('TOPPADDING',(0,0),(-1,-1),1),
                               ('BOTTOMPADDING',(0,0),(-1,-1),1),]))

# Right: Plain Cotton Fabric
pf_hdr = ParagraphStyle('pfh',fontSize=9,textColor=WHITE,
                         fontName='Helvetica-Bold',alignment=TA_CENTER,leading=13)
pf_sub = ParagraphStyle('pfs',fontSize=7,textColor=GOLD,
                         fontName='Helvetica',alignment=TA_CENTER,leading=10)
pf_head = Table([[Paragraph("6.  PLAIN WHITE COTTON FABRIC",pf_hdr)],
                  [Paragraph("Bulk Roll  |  100% Cotton Poplin",pf_sub)]],
                colWidths=[86*mm])
pf_head.setStyle(TableStyle([
    ('BACKGROUND',(0,0),(-1,-1),MAROON),
    ('TOPPADDING',(0,0),(-1,-1),4),('BOTTOMPADDING',(0,0),(-1,-1),4),
    ('LEFTPADDING',(0,0),(-1,-1),6),('RIGHTPADDING',(0,0),(-1,-1),6),
]))
pf_price = price_table(
    ["Quantity","Price / Meter"],
    [["200–499 meters","$ 1.10"],["500–999 meters","$ 0.95"],
     ["1,000–2,999 mtr","$ 0.80"],["3,000+ meters","$ 0.65"]],
    [43*mm, 43*mm]
)
pf_specs = [
    spec_para("Material: 100% Cotton Poplin"),
    spec_para("Width: 150 cm / 240 cm available"),
    spec_para("GSM: 80–100 GSM"),
    spec_para("Color: White (bleached) / Off-White"),
]
pf_block = Table(
    [[pf_head],[Table([[s] for s in pf_specs],colWidths=[86*mm])],[pf_price],
     [moq_line("200 meters","7–10 days")]],
    colWidths=[86*mm]
)
pf_block.setStyle(TableStyle([('LEFTPADDING',(0,0),(-1,-1),0),
                               ('RIGHTPADDING',(0,0),(-1,-1),0),
                               ('TOPPADDING',(0,0),(-1,-1),1),
                               ('BOTTOMPADDING',(0,0),(-1,-1),1),]))

row56 = Table([[pm_block, pf_block]], colWidths=[88*mm,92*mm])
row56.setStyle(TableStyle([
    ('VALIGN',(0,0),(-1,-1),'TOP'),
    ('LEFTPADDING',(0,0),(-1,-1),0),
    ('RIGHTPADDING',(0,0),(-1,-1),0),
]))
story.append(row56)
story.append(Spacer(1,5*mm))

# ── TERMS FOOTER ──────────────────────────────────────────────────────────────
terms_title = ParagraphStyle('tt',fontSize=9,textColor=WHITE,
                              fontName='Helvetica-Bold',alignment=TA_CENTER,leading=13)
terms_body  = ParagraphStyle('tb',fontSize=7.5,textColor=DARK_TEXT,
                              fontName='Helvetica',alignment=TA_CENTER,leading=11)

terms_data = [
    [Paragraph("TERMS & CONDITIONS", terms_title)],
    [Table([[
        Paragraph("💳  Payment: 30% Advance | 70% Before Shipment", terms_body),
        Paragraph("📦  Prices: FOB Karachi (USD)", terms_body),
        Paragraph("🚢  Delivery: Karachi → Dubai 7–10 Days Sea", terms_body),
        Paragraph("📋  Samples: Available on Request", terms_body),
        Paragraph("⏱  Validity: 30 Days from Issue Date", terms_body),
    ]], colWidths=[35*mm,36*mm,43*mm,32*mm,34*mm])]
]
terms_table = Table(terms_data, colWidths=[180*mm])
terms_table.setStyle(TableStyle([
    ('BACKGROUND',(0,0),(-1,0), MAROON),
    ('BACKGROUND',(0,1),(-1,1), CREAM),
    ('TOPPADDING',(0,0),(-1,-1),4),
    ('BOTTOMPADDING',(0,0),(-1,-1),4),
    ('LEFTPADDING',(0,0),(-1,-1),6),
    ('RIGHTPADDING',(0,0),(-1,-1),6),
    ('BOX',(0,0),(-1,-1),1,GOLD),
]))
story.append(terms_table)
story.append(Spacer(1,3*mm))

# ── CONTACT FOOTER ────────────────────────────────────────────────────────────
contact_style = ParagraphStyle('cs',fontSize=8,textColor=WHITE,
                                fontName='Helvetica-Bold',alignment=TA_CENTER,leading=12)
contact_sub   = ParagraphStyle('css',fontSize=7.5,textColor=GOLD,
                                fontName='Helvetica',alignment=TA_CENTER,leading=11)
contact_data = [
    [Paragraph("AKH LINEN HOUSE — Bed Linen • Towel • Etc", contact_style)],
    [Paragraph("WhatsApp: [Your Number]   |   Email: [Your Email]   |   Pakistan", contact_sub)],
]
contact_table = Table(contact_data, colWidths=[180*mm])
contact_table.setStyle(TableStyle([
    ('BACKGROUND',(0,0),(-1,-1), MAROON),
    ('TOPPADDING',(0,0),(-1,-1),4),
    ('BOTTOMPADDING',(0,0),(-1,-1),4),
    ('LEFTPADDING',(0,0),(-1,-1),6),
    ('RIGHTPADDING',(0,0),(-1,-1),6),
]))
story.append(contact_table)

# ── BUILD ──────────────────────────────────────────────────────────────────────
doc.build(story)
print("PDF generated successfully!")
