from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame,
                                 Table, TableStyle, Paragraph, Spacer, Image)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT

# ── Brand colours ──────────────────────────────────────────────────────────────
MAROON    = colors.HexColor('#6B1535')
GOLD      = colors.HexColor('#C9A84C')
GOLD_LITE = colors.HexColor('#E8D5A3')
CREAM     = colors.HexColor('#FDF8F0')
CREAM2    = colors.HexColor('#FAF3E5')
WHITE     = colors.white
DARK      = colors.HexColor('#1E1E1E')
MID       = colors.HexColor('#5A5A5A')
RED       = colors.HexColor('#C0392B')
RED_LT    = colors.HexColor('#FDECEA')
ORANGE    = colors.HexColor('#D35400')
ORANGE_LT = colors.HexColor('#FEF0E7')
GREEN     = colors.HexColor('#1A6B3C')
GREEN_LT  = colors.HexColor('#E8F5EE')
NAVY      = colors.HexColor('#1B2A4A')
YELLOW    = colors.HexColor('#F39C12')
YELLOW_LT = colors.HexColor('#FEF9E7')

LOGO_PATH = "/root/.claude/uploads/821548fa-6491-4125-8b13-35cb95ca5b0f/bbf1cd60-1000645012.jpg"
OUT_PATH  = "/home/user/Usama-New/AKH_Sourcing_Comparison.pdf"

WA    = "+92 334 006 5781"
EMAIL = "akhlinenhouse@gmail.com"
W, H  = A4
CW    = 179*mm

def page_border(c, doc):
    c.saveState()
    c.setStrokeColor(GOLD);  c.setLineWidth(2)
    c.roundRect(7*mm, 7*mm, W-14*mm, H-14*mm, 4, stroke=1, fill=0)
    c.setStrokeColor(MAROON); c.setLineWidth(0.5)
    c.roundRect(9.5*mm, 9.5*mm, W-19*mm, H-19*mm, 3, stroke=1, fill=0)
    c.restoreState()

doc = BaseDocTemplate(OUT_PATH, pagesize=A4,
                      rightMargin=14*mm, leftMargin=14*mm,
                      topMargin=12*mm, bottomMargin=12*mm)
frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id='main')
doc.addPageTemplates([PageTemplate(id='main', frames=frame, onPage=page_border)])

story = []

def ps(name, size=8, color=DARK, font='Helvetica', align=TA_LEFT,
       leading=None, bold=False):
    if bold: font += '-Bold'
    return ParagraphStyle(name, fontSize=size, textColor=color,
                          fontName=font, alignment=align,
                          leading=leading or size * 1.3)

def cell(text, size=7.5, color=DARK, bg=None, bold=False,
         align=TA_LEFT, pad=4):
    p = Paragraph(text, ps('c', size, color, align=align, bold=bold,
                            leading=size*1.3))
    t = Table([[p]], colWidths=[None])
    styles = [
        ('TOPPADDING',    (0,0),(-1,-1), pad),
        ('BOTTOMPADDING', (0,0),(-1,-1), pad),
        ('LEFTPADDING',   (0,0),(-1,-1), pad+1),
        ('RIGHTPADDING',  (0,0),(-1,-1), pad+1),
        ('VALIGN',        (0,0),(-1,-1), 'TOP'),
    ]
    if bg: styles.append(('BACKGROUND', (0,0),(-1,-1), bg))
    t.setStyle(TableStyle(styles))
    return t

def badge(text, bg, fg=WHITE, size=7, bold=True):
    p = Paragraph(text, ps('b', size, fg, align=TA_CENTER, bold=bold,
                            leading=size*1.3))
    t = Table([[p]])
    t.setStyle(TableStyle([
        ('BACKGROUND',    (0,0),(-1,-1), bg),
        ('TOPPADDING',    (0,0),(-1,-1), 2),
        ('BOTTOMPADDING', (0,0),(-1,-1), 2),
        ('LEFTPADDING',   (0,0),(-1,-1), 5),
        ('RIGHTPADDING',  (0,0),(-1,-1), 5),
        ('BOX',           (0,0),(-1,-1), 0.5, fg),
    ]))
    return t

# ══════════════════════════════════════════════════════════════════════════════
# HEADER BANNER
# ══════════════════════════════════════════════════════════════════════════════
logo = Image(LOGO_PATH, width=28*mm, height=19*mm)

hdr_text = [
    [Paragraph("WHERE SHOULD YOU SOURCE MACAWIIS FROM?",
               ps('h1', 15, WHITE, bold=True, align=TA_LEFT, leading=18))],
    [Paragraph("THE SMART GUIDE FOR SOMALIA TEXTILE BUYERS  •  Pakistan vs China vs India",
               ps('h2', 8.5, GOLD_LITE, align=TA_LEFT, leading=12))],
    [Paragraph("You're not just buying from a supplier. You're choosing a country.",
               ps('h3', 8, GOLD, align=TA_LEFT, leading=11))],
]
hdr_txt_tbl = Table(hdr_text, colWidths=[147*mm])
hdr_txt_tbl.setStyle(TableStyle([
    ('TOPPADDING',    (0,0),(-1,-1), 1),
    ('BOTTOMPADDING', (0,0),(-1,-1), 1),
    ('LEFTPADDING',   (0,0),(-1,-1), 0),
    ('RIGHTPADDING',  (0,0),(-1,-1), 0),
]))

hdr_outer = Table([[logo, hdr_txt_tbl]], colWidths=[30*mm, 149*mm])
hdr_outer.setStyle(TableStyle([
    ('BACKGROUND',    (0,0),(-1,-1), MAROON),
    ('VALIGN',        (0,0),(-1,-1), 'MIDDLE'),
    ('TOPPADDING',    (0,0),(-1,-1), 8),
    ('BOTTOMPADDING', (0,0),(-1,-1), 8),
    ('LEFTPADDING',   (0,0),(-1,-1), 6),
    ('RIGHTPADDING',  (0,0),(-1,-1), 6),
    ('BOX',           (0,0),(-1,-1), 1.5, GOLD),
]))
story.append(hdr_outer)
story.append(Spacer(1, 2.5*mm))

# ══════════════════════════════════════════════════════════════════════════════
# COUNTRY COLUMN HEADERS
# ══════════════════════════════════════════════════════════════════════════════
LABEL_W = 26*mm
COL_W   = 51*mm

def country_hdr(flag, name, subtitle, bg, fg=WHITE):
    data = [
        [Paragraph(flag, ps('f', 18, fg, align=TA_CENTER, leading=22))],
        [Paragraph(name, ps('n', 13, fg, bold=True, align=TA_CENTER, leading=16))],
        [Paragraph(subtitle, ps('s', 6.5, fg, align=TA_CENTER, leading=9))],
    ]
    t = Table(data, colWidths=[COL_W])
    t.setStyle(TableStyle([
        ('BACKGROUND',    (0,0),(-1,-1), bg),
        ('TOPPADDING',    (0,0),(-1,-1), 4),
        ('BOTTOMPADDING', (0,0),(-1,-1), 4),
        ('LEFTPADDING',   (0,0),(-1,-1), 2),
        ('RIGHTPADDING',  (0,0),(-1,-1), 2),
        ('BOX',           (0,0),(-1,-1), 1, GOLD),
    ]))
    return t

col_hdrs = Table([[
    Table([[Paragraph("")]], colWidths=[LABEL_W]),   # empty label corner
    country_hdr("🇨🇳", "CHINA",   "World's Largest Manufacturer", RED),
    country_hdr("🇮🇳", "INDIA",   "South Asia's Flexible Supplier", ORANGE),
    country_hdr("🇵🇰", "PAKISTAN","Your Direct Supplier — CIF Mogadishu", GREEN),
]], colWidths=[LABEL_W, COL_W, COL_W, COL_W])
col_hdrs.setStyle(TableStyle([
    ('VALIGN',        (0,0),(-1,-1), 'TOP'),
    ('LEFTPADDING',   (0,0),(-1,-1), 0),
    ('RIGHTPADDING',  (0,0),(-1,-1), 0),
    ('TOPPADDING',    (0,0),(-1,-1), 0),
    ('BOTTOMPADDING', (0,0),(-1,-1), 0),
    ('ALIGN',         (0,0),(0,-1),  'CENTER'),
]))
story.append(col_hdrs)
story.append(Spacer(1, 1*mm))

# ══════════════════════════════════════════════════════════════════════════════
# CRITERIA ROWS
# ══════════════════════════════════════════════════════════════════════════════
def lbl(icon, title):
    data = [
        [Paragraph(icon,  ps('li', 13, GOLD, align=TA_CENTER, leading=16))],
        [Paragraph(title, ps('lt', 6.5, WHITE, bold=True, align=TA_CENTER, leading=9))],
    ]
    t = Table(data, colWidths=[LABEL_W])
    t.setStyle(TableStyle([
        ('BACKGROUND',    (0,0),(-1,-1), MAROON),
        ('TOPPADDING',    (0,0),(-1,-1), 4),
        ('BOTTOMPADDING', (0,0),(-1,-1), 4),
        ('LEFTPADDING',   (0,0),(-1,-1), 2),
        ('RIGHTPADDING',  (0,0),(-1,-1), 2),
        ('BOX',           (0,0),(-1,-1), 0.5, GOLD),
    ]))
    return t

def row(icon, title, c_china, c_india, c_pak, alt=False):
    bg = CREAM2 if alt else WHITE
    def col_cell(txt, bg=bg):
        return Paragraph(txt, ps('rc', 7, DARK, leading=10))
    row_data = [[
        lbl(icon, title),
        Table([[col_cell(c_china)]],  colWidths=[COL_W],
              style=TableStyle([('BACKGROUND',(0,0),(-1,-1),RED_LT if alt else CREAM),
                                ('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5),
                                ('LEFTPADDING',(0,0),(-1,-1),5),('RIGHTPADDING',(0,0),(-1,-1),5),
                                ('BOX',(0,0),(-1,-1),0.3,GOLD_LITE),('VALIGN',(0,0),(-1,-1),'TOP')])),
        Table([[col_cell(c_india)]],  colWidths=[COL_W],
              style=TableStyle([('BACKGROUND',(0,0),(-1,-1),ORANGE_LT if alt else CREAM),
                                ('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5),
                                ('LEFTPADDING',(0,0),(-1,-1),5),('RIGHTPADDING',(0,0),(-1,-1),5),
                                ('BOX',(0,0),(-1,-1),0.3,GOLD_LITE),('VALIGN',(0,0),(-1,-1),'TOP')])),
        Table([[col_cell(c_pak)]],    colWidths=[COL_W],
              style=TableStyle([('BACKGROUND',(0,0),(-1,-1),GREEN_LT),
                                ('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5),
                                ('LEFTPADDING',(0,0),(-1,-1),5),('RIGHTPADDING',(0,0),(-1,-1),5),
                                ('BOX',(0,0),(-1,-1),0.5,GREEN),('VALIGN',(0,0),(-1,-1),'TOP')])),
    ]]
    t = Table(row_data, colWidths=[LABEL_W, COL_W, COL_W, COL_W])
    t.setStyle(TableStyle([
        ('VALIGN',        (0,0),(-1,-1), 'TOP'),
        ('LEFTPADDING',   (0,0),(-1,-1), 0),
        ('RIGHTPADDING',  (0,0),(-1,-1), 0),
        ('TOPPADDING',    (0,0),(-1,-1), 0),
        ('BOTTOMPADDING', (0,0),(-1,-1), 0),
    ]))
    return t

rows_data = [
    ("📦", "MOQ",
     "Very High.\n5,000–10,000 pcs minimum.\nNot flexible for small buyers.\nForces you to overstock.",
     "Medium.\n1,000–3,000 pcs.\nMore flexible than China.\nSome suppliers do 500 pcs.",
     "✅ Flexible.\n500–2,000 pcs minimum.\nSmall trial orders welcome.\nScale up at your pace.",
     False),

    ("⏱", "LEAD TIME\n(to Mogadishu)",
     "Slowest overall.\n45–60 days production.\n+20–25 days sea shipping.\n= 65–85 days total.",
     "Moderate.\n30–45 days production.\n+18–22 days shipping\nvia Colombo or Dubai.",
     "✅ Fastest.\n21–28 days production.\n+10–14 days DIRECT shipping\nKarachi→Mogadishu (Maersk).",
     True),

    ("⭐", "MACAWIIS\nQUALITY",
     "⚠ Mostly Synthetic.\nPolyester/viscose blends.\nSomali men dislike the feel.\nNot authentic checked cotton.",
     "Good Cotton Lungi.\nCoarser weave. Limited\nchecked patterns. Gujarat\nsuppliers are best.",
     "✅ Best Cotton Quality.\n100% checked cotton.\nFaisalabad weave = authentic\nfeel Somali market demands.",
     False),

    ("💰", "PRICE\n(CIF Mogadishu)",
     "Lowest unit price.\nBUT: longer shipping adds\n$0.30–0.50/pc freight cost.\nHidden costs reduce advantage.",
     "Medium price.\nSimilar to Pakistan.\nNo direct shipping route\nraises landed cost.",
     "✅ Best Value.\n$1.20–1.40 CIF Mogadishu.\nShortest route = lowest\nfreight. Best total cost.",
     True),

    ("✔", "COMPLIANCE\n& PAYMENT",
     "OEKO-TEX from large\nfactories only. Small ones\nnot certified. Payment via\nLC or TT only. No Dahabshiil.",
     "BSCI, OEKO-TEX growing.\nBetter than China.\nPayment via LC/TT.\nNo Dahabshiil accepted.",
     "✅ Full Compliance.\nOEKO-TEX, ISO 9001, WeBOC\ncertified exports.\n✅ Dahabshiil accepted.\n50% advance, 50% on B/L.",
     False),

    ("⚠", "WEAKNESS\nfor Somalia",
     "Synthetic macawiis not\npreferred. Language barrier.\nNo cultural connection.\nLong shipping, higher freight.",
     "No direct Mogadishu\nshipping — via Colombo\nor Dubai. Slower. Some\nSomali buyers hesitant.",
     "✅ No major weakness.\nSmaller factory capacity\nvs China. But flexible\nMOQ covers this gap.",
     True),
]

for icon, title, china, india, pak, alt in rows_data:
    story.append(row(icon, title, china, india, pak, alt))
    story.append(Spacer(1, 0.8*mm))

story.append(Spacer(1, 2*mm))

# ══════════════════════════════════════════════════════════════════════════════
# HONEST SUMMARY TABLE
# ══════════════════════════════════════════════════════════════════════════════
sum_hdr = Table([[
    Paragraph("THE HONEST SUMMARY FOR SOMALIA MACAWIIS BUYERS",
              ps('sh', 9, WHITE, bold=True, align=TA_CENTER, leading=12))
]], colWidths=[CW])
sum_hdr.setStyle(TableStyle([
    ('BACKGROUND',    (0,0),(-1,-1), NAVY),
    ('TOPPADDING',    (0,0),(-1,-1), 5),
    ('BOTTOMPADDING', (0,0),(-1,-1), 5),
    ('BOX',           (0,0),(-1,-1), 1.5, GOLD),
]))
story.append(sum_hdr)

def rating(text, color, fg=WHITE):
    p = Paragraph(text, ps('r', 7, fg, bold=True, align=TA_CENTER, leading=9))
    t = Table([[p]])
    t.setStyle(TableStyle([
        ('BACKGROUND',    (0,0),(-1,-1), color),
        ('TOPPADDING',    (0,0),(-1,-1), 3),
        ('BOTTOMPADDING', (0,0),(-1,-1), 3),
        ('LEFTPADDING',   (0,0),(-1,-1), 3),
        ('RIGHTPADDING',  (0,0),(-1,-1), 3),
        ('BOX',           (0,0),(-1,-1), 0.5, WHITE),
    ]))
    return t

POOR   = RED
MED    = YELLOW
GOOD   = GREEN

sum_rows = [
    ["CRITERIA",        "🇨🇳  CHINA",             "🇮🇳  INDIA",         "🇵🇰  PAKISTAN"],
    ["💰 Price (CIF)",  "MEDIUM",                "MEDIUM",            "✅ BEST VALUE"],
    ["📦 MOQ",          "VERY HIGH",             "MEDIUM",            "✅ FLEXIBLE"],
    ["⏱ Shipping Speed","SLOWEST (65–85 days)",  "SLOW (48–67 days)", "✅ FASTEST (31–42 days)"],
    ["⭐ Macawiis Quality","⚠ SYNTHETIC",         "GOOD COTTON",       "✅ BEST COTTON"],
    ["✔ Compliance",    "MEDIUM",                "GROWING",           "✅ STRONG"],
    ["💳 Dahabshiil",   "❌ NO",                  "❌ NO",              "✅ YES"],
    ["🚢 Direct to Mog","❌ NO",                  "❌ NO",              "✅ YES (Maersk)"],
    ["🤝 Somalia Trust","LOW",                   "MEDIUM",            "✅ HIGH (rice partner)"],
]

SL = 30*mm
CL = (CW - SL) / 3

def sum_cell(txt, bg=CREAM, fg=DARK, bold=False, size=7):
    return Paragraph(txt, ps('sc', size, fg, bold=bold, align=TA_CENTER, leading=9))

sum_data = []
for i, r in enumerate(sum_rows):
    if i == 0:
        sum_data.append([
            Paragraph(r[0], ps('sh2', 7.5, WHITE, bold=True, align=TA_CENTER, leading=10)),
            Paragraph(r[1], ps('sh3', 8, WHITE,   bold=True, align=TA_CENTER, leading=10)),
            Paragraph(r[2], ps('sh4', 8, WHITE,   bold=True, align=TA_CENTER, leading=10)),
            Paragraph(r[3], ps('sh5', 8, WHITE,   bold=True, align=TA_CENTER, leading=10)),
        ])
    else:
        bg = CREAM2 if i % 2 == 0 else WHITE
        sum_data.append([
            Paragraph(r[0], ps('sl', 7, MAROON, bold=True, align=TA_LEFT,   leading=9)),
            Paragraph(r[1], ps('sc', 7, DARK,           align=TA_CENTER, leading=9)),
            Paragraph(r[2], ps('si', 7, DARK,           align=TA_CENTER, leading=9)),
            Paragraph(r[3], ps('sp', 7, GREEN, bold=True, align=TA_CENTER, leading=9)),
        ])

sum_tbl = Table(sum_data, colWidths=[SL, CL, CL, CL])
sum_styles = [
    ('BACKGROUND',    (0,0),(-1,0),  NAVY),
    ('TEXTCOLOR',     (0,0),(-1,0),  WHITE),
    ('BOX',           (0,0),(-1,-1), 1, GOLD),
    ('INNERGRID',     (0,0),(-1,-1), 0.3, GOLD_LITE),
    ('TOPPADDING',    (0,0),(-1,-1), 4),
    ('BOTTOMPADDING', (0,0),(-1,-1), 4),
    ('LEFTPADDING',   (0,0),(-1,-1), 4),
    ('RIGHTPADDING',  (0,0),(-1,-1), 4),
    ('VALIGN',        (0,0),(-1,-1), 'MIDDLE'),
    ('BACKGROUND',    (3,1),(-1,-1), GREEN_LT),
]
for i in range(1, len(sum_data)):
    if i % 2 == 0:
        sum_styles.append(('BACKGROUND', (0,i),(2,i), CREAM2))
    else:
        sum_styles.append(('BACKGROUND', (0,i),(2,i), WHITE))
    sum_styles.append(('BACKGROUND', (3,i),(3,i), GREEN_LT))

sum_tbl.setStyle(TableStyle(sum_styles))
story.append(sum_tbl)
story.append(Spacer(1, 2*mm))

# ══════════════════════════════════════════════════════════════════════════════
# REAL INSIGHT PANEL
# ══════════════════════════════════════════════════════════════════════════════
insight_hdr = Table([[
    Paragraph("THE REAL INSIGHT FOR SOMALIA BUYERS 2026",
              ps('ih', 9, WHITE, bold=True, align=TA_CENTER, leading=12))
]], colWidths=[CW])
insight_hdr.setStyle(TableStyle([
    ('BACKGROUND',    (0,0),(-1,-1), MAROON),
    ('TOPPADDING',    (0,0),(-1,-1), 5),
    ('BOTTOMPADDING', (0,0),(-1,-1), 5),
    ('BOX',           (0,0),(-1,-1), 1.5, GOLD),
]))
story.append(insight_hdr)

def insight_panel(flag, country, msg, bg, fg, border):
    data = [
        [Paragraph(flag, ps('if', 16, fg, align=TA_CENTER, leading=20))],
        [Paragraph(country, ps('ic', 9, fg, bold=True, align=TA_CENTER, leading=12))],
        [Paragraph(msg, ps('im', 7, fg, align=TA_CENTER, leading=10))],
    ]
    t = Table(data, colWidths=[(CW/3) - 2*mm])
    t.setStyle(TableStyle([
        ('BACKGROUND',    (0,0),(-1,-1), bg),
        ('TOPPADDING',    (0,0),(-1,-1), 6),
        ('BOTTOMPADDING', (0,0),(-1,-1), 6),
        ('LEFTPADDING',   (0,0),(-1,-1), 5),
        ('RIGHTPADDING',  (0,0),(-1,-1), 5),
        ('BOX',           (0,0),(-1,-1), 1.5, border),
    ]))
    return t

i1 = insight_panel("🇨🇳", "CHINA",
    "Use only for synthetic garments\nor household goods.\nNOT recommended for Macawiis.\nSomali market rejects synthetic feel.",
    RED_LT, RED, RED)

i2 = insight_panel("🇮🇳", "INDIA",
    "Good for variety & flexibility.\nBut no direct Mogadishu route\nand no Dahabshiil payment.\nHigher total landed cost.",
    ORANGE_LT, ORANGE, ORANGE)

i3 = insight_panel("🇵🇰", "PAKISTAN ✅",
    "BEST CHOICE for Macawiis &\nTextiles to Somalia.\nFastest route • Best cotton quality\nDahabshiil accepted • Lowest CIF cost.",
    GREEN_LT, GREEN, GREEN)

panels = Table([[i1, Spacer(2*mm, 1), i2, Spacer(2*mm, 1), i3]],
               colWidths=[(CW/3)-2*mm, 2*mm, (CW/3)-2*mm, 2*mm, (CW/3)-2*mm])
panels.setStyle(TableStyle([
    ('VALIGN',        (0,0),(-1,-1), 'TOP'),
    ('LEFTPADDING',   (0,0),(-1,-1), 0),
    ('RIGHTPADDING',  (0,0),(-1,-1), 0),
    ('TOPPADDING',    (0,0),(-1,-1), 0),
    ('BOTTOMPADDING', (0,0),(-1,-1), 0),
]))
story.append(panels)
story.append(Spacer(1, 2*mm))

# ══════════════════════════════════════════════════════════════════════════════
# FOOTER
# ══════════════════════════════════════════════════════════════════════════════
footer = Table([[
    Paragraph("AKH LINEN HOUSE  —  Pakistan Direct Textile Exporter  |  CIF Mogadishu Available",
              ps('fl', 8, WHITE, bold=True, align=TA_LEFT, leading=11)),
    Paragraph(f"WhatsApp: {WA}   |   {EMAIL}",
              ps('fr', 8, GOLD_LITE, align=TA_RIGHT, leading=11)),
]], colWidths=[110*mm, 69*mm])
footer.setStyle(TableStyle([
    ('BACKGROUND',    (0,0),(-1,-1), MAROON),
    ('TOPPADDING',    (0,0),(-1,-1), 6),
    ('BOTTOMPADDING', (0,0),(-1,-1), 6),
    ('LEFTPADDING',   (0,0),(-1,-1), 8),
    ('RIGHTPADDING',  (0,0),(-1,-1), 8),
    ('BOX',           (0,0),(-1,-1), 1.5, GOLD),
]))
story.append(footer)

doc.build(story)
print("Sourcing Comparison PDF generated successfully!")
