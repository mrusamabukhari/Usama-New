from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame,
                                 Table, TableStyle, Paragraph, Spacer, Image)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.pdfgen import canvas as pdfcanvas

# ── Brand & palette ────────────────────────────────────────────────────────────
MAROON    = colors.HexColor('#6B1535')
MAROON2   = colors.HexColor('#8B1F42')
GOLD      = colors.HexColor('#C9A84C')
GOLD_LITE = colors.HexColor('#E8D5A3')
NAVY      = colors.HexColor('#0F1F3D')
NAVY2     = colors.HexColor('#1B2A4A')
WHITE     = colors.white
CREAM     = colors.HexColor('#FDF8F0')
CREAM2    = colors.HexColor('#F5EDD8')
DARK      = colors.HexColor('#1E1E1E')
MID       = colors.HexColor('#555555')

# Country accent colours
C_RED     = colors.HexColor('#B71C1C')
C_RED_BG  = colors.HexColor('#FFEBEE')
C_RED_MID = colors.HexColor('#FFCDD2')
C_ORG     = colors.HexColor('#BF360C')
C_ORG_BG  = colors.HexColor('#FBE9E7')
C_ORG_MID = colors.HexColor('#FFCCBC')
C_GRN     = colors.HexColor('#1B5E20')
C_GRN_BG  = colors.HexColor('#E8F5E9')
C_GRN_MID = colors.HexColor('#C8E6C9')

# Badge colours
B_GREEN  = colors.HexColor('#2E7D32')
B_AMBER  = colors.HexColor('#E65100')
B_RED    = colors.HexColor('#C62828')
B_GREY   = colors.HexColor('#455A64')

LOGO_PATH = "/root/.claude/uploads/821548fa-6491-4125-8b13-35cb95ca5b0f/bbf1cd60-1000645012.jpg"
OUT_PATH  = "/home/user/Usama-New/AKH_Sourcing_Comparison.pdf"
WA        = "+92 334 006 5781"
EMAIL     = "akhlinenhouse@gmail.com"
W, H      = A4
CW        = 181*mm

# ── Doc setup ─────────────────────────────────────────────────────────────────
def border_cb(c, doc):
    c.saveState()
    c.setStrokeColor(GOLD); c.setLineWidth(2.2)
    c.roundRect(6*mm, 6*mm, W-12*mm, H-12*mm, 4, stroke=1, fill=0)
    c.setStrokeColor(MAROON); c.setLineWidth(0.5)
    c.roundRect(8.5*mm, 8.5*mm, W-17*mm, H-17*mm, 3, stroke=1, fill=0)
    c.restoreState()

doc = BaseDocTemplate(OUT_PATH, pagesize=A4,
                      rightMargin=13*mm, leftMargin=13*mm,
                      topMargin=11*mm, bottomMargin=11*mm)
fr = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id='main')
doc.addPageTemplates([PageTemplate(id='p', frames=fr, onPage=border_cb)])
story = []

# ── Style helpers ──────────────────────────────────────────────────────────────
def S(name, sz=8, col=DARK, font='Helvetica', align=TA_LEFT, lh=None, bold=False):
    if bold: font += '-Bold'
    return ParagraphStyle(name, fontSize=sz, textColor=col, fontName=font,
                          alignment=align, leading=lh or sz*1.3)

def P(txt, sz=8, col=DARK, align=TA_LEFT, bold=False, lh=None):
    return Paragraph(txt, S('_', sz, col, align=align, bold=bold, lh=lh))

def badge(text, bg, fg=WHITE, sz=6.5):
    """Colored chip badge for summary table."""
    p = Paragraph(text, S('_', sz, fg, align=TA_CENTER, bold=True, lh=sz*1.25))
    t = Table([[p]])
    t.setStyle(TableStyle([
        ('BACKGROUND',    (0,0),(-1,-1), bg),
        ('TOPPADDING',    (0,0),(-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0),(-1,-1), 2.5),
        ('LEFTPADDING',   (0,0),(-1,-1), 4),
        ('RIGHTPADDING',  (0,0),(-1,-1), 4),
        ('ROUNDEDCORNERS',(0,0),(-1,-1), [3,3,3,3]),
    ]))
    return t

LBCOL = 25*mm   # label column
CCOL  = (CW - LBCOL) / 3  # each country column = ~52mm

# ══════════════════════════════════════════════════════════════════════════════
# 1. MAIN HEADER BANNER
# ══════════════════════════════════════════════════════════════════════════════
logo = Image(LOGO_PATH, width=26*mm, height=17*mm)

title_block = [
    [P("WHERE SHOULD YOU SOURCE MACAWIIS FROM?", 15, WHITE, TA_LEFT, bold=True, lh=18)],
    [P("THE BIG PICTURE FOR SOMALIA TEXTILE BUYERS", 11, GOLD, TA_LEFT, bold=True, lh=14)],
    [P("You're not just buying from a supplier. You're choosing a country.", 8, GOLD_LITE, TA_LEFT, lh=11)],
]
title_tbl = Table(title_block, colWidths=[151*mm])
title_tbl.setStyle(TableStyle([('TOPPADDING',(0,0),(-1,-1),1),('BOTTOMPADDING',(0,0),(-1,-1),1),
                                ('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(-1,-1),0)]))

banner = Table([[logo, title_tbl]], colWidths=[28*mm, 153*mm])
banner.setStyle(TableStyle([
    ('BACKGROUND',    (0,0),(-1,-1), NAVY),
    ('VALIGN',        (0,0),(-1,-1), 'MIDDLE'),
    ('TOPPADDING',    (0,0),(-1,-1), 7),
    ('BOTTOMPADDING', (0,0),(-1,-1), 7),
    ('LEFTPADDING',   (0,0),(-1,-1), 5),
    ('RIGHTPADDING',  (0,0),(-1,-1), 5),
    ('BOX',           (0,0),(-1,-1), 2, GOLD),
]))
story.append(banner)
story.append(Spacer(1,2*mm))

# ══════════════════════════════════════════════════════════════════════════════
# 2. COUNTRY HEADER COLUMNS
# ══════════════════════════════════════════════════════════════════════════════
def cty_hdr(flag, name, tagline, bg, fg=WHITE):
    t = Table([
        [P(flag,    20, fg, TA_CENTER, lh=24)],
        [P(name,    12, fg, TA_CENTER, bold=True, lh=15)],
        [P(tagline,  6.5, fg, TA_CENTER, lh=9)],
    ], colWidths=[CCOL])
    t.setStyle(TableStyle([
        ('BACKGROUND',    (0,0),(-1,-1), bg),
        ('TOPPADDING',    (0,0),(-1,-1), 5),
        ('BOTTOMPADDING', (0,0),(-1,-1), 5),
        ('LEFTPADDING',   (0,0),(-1,-1), 3),
        ('RIGHTPADDING',  (0,0),(-1,-1), 3),
        ('BOX',           (0,0),(-1,-1), 1.2, GOLD),
    ]))
    return t

corner = Table([[P('')]], colWidths=[LBCOL])
corner.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),NAVY),
                             ('BOX',(0,0),(-1,-1),1,GOLD)]))

hdr_row = Table([[corner,
                  cty_hdr('🇨🇳','CHINA',   'World\'s Largest Manufacturer', C_RED),
                  cty_hdr('🇮🇳','INDIA',   'South Asia\'s Flexible Supplier', C_ORG),
                  cty_hdr('🇵🇰','PAKISTAN','★ Recommended for Somalia ★', C_GRN),
                 ]], colWidths=[LBCOL,CCOL,CCOL,CCOL])
hdr_row.setStyle(TableStyle([
    ('VALIGN',(0,0),(-1,-1),'TOP'),
    ('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(-1,-1),0),
    ('TOPPADDING',(0,0),(-1,-1),0),('BOTTOMPADDING',(0,0),(-1,-1),0),
]))
story.append(hdr_row)
story.append(Spacer(1,1*mm))

# ══════════════════════════════════════════════════════════════════════════════
# 3. CRITERIA ROWS
# ══════════════════════════════════════════════════════════════════════════════
def label_cell(icon, title):
    t = Table([
        [P(icon,  12, GOLD,  TA_CENTER, lh=15)],
        [P(title,  6.5, WHITE, TA_CENTER, bold=True, lh=9)],
    ], colWidths=[LBCOL])
    t.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,-1),MAROON),
        ('TOPPADDING',(0,0),(-1,-1),4),('BOTTOMPADDING',(0,0),(-1,-1),4),
        ('LEFTPADDING',(0,0),(-1,-1),2),('RIGHTPADDING',(0,0),(-1,-1),2),
        ('BOX',(0,0),(-1,-1),0.5,GOLD),
    ]))
    return t

def content_cell(text, bg, border_col, highlight=False):
    p = Paragraph(text, S('_', 7, DARK if not highlight else C_GRN,
                           lh=10.5, bold=highlight))
    t = Table([[p]], colWidths=[CCOL])
    bw = 1.2 if highlight else 0.3
    t.setStyle(TableStyle([
        ('BACKGROUND',    (0,0),(-1,-1), bg),
        ('TOPPADDING',    (0,0),(-1,-1), 5),
        ('BOTTOMPADDING', (0,0),(-1,-1), 5),
        ('LEFTPADDING',   (0,0),(-1,-1), 5),
        ('RIGHTPADDING',  (0,0),(-1,-1), 5),
        ('BOX',           (0,0),(-1,-1), bw, border_col),
        ('VALIGN',        (0,0),(-1,-1), 'TOP'),
    ]))
    return t

def crit_row(icon, title, ch_txt, ind_txt, pak_txt, alt=False):
    ch_bg  = C_RED_MID if alt else C_RED_BG
    ind_bg = C_ORG_MID if alt else C_ORG_BG
    pak_bg = C_GRN_MID if alt else C_GRN_BG
    t = Table([[
        label_cell(icon, title),
        content_cell(ch_txt,  ch_bg,  C_RED),
        content_cell(ind_txt, ind_bg, C_ORG),
        content_cell(pak_txt, pak_bg, C_GRN, highlight=True),
    ]], colWidths=[LBCOL,CCOL,CCOL,CCOL])
    t.setStyle(TableStyle([
        ('VALIGN',(0,0),(-1,-1),'TOP'),
        ('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(-1,-1),0),
        ('TOPPADDING',(0,0),(-1,-1),0),('BOTTOMPADDING',(0,0),(-1,-1),0),
    ]))
    return t

criteria = [
  ("📦","MOQ",
   "Very High. 5,000–10,000 pcs minimum. Not flexible for small or trial orders. Forces heavy upfront investment.",
   "Medium. 1,000–3,000 pcs. More flexible than China. Some suppliers accept 500 pcs for repeat buyers.",
   "✅ Most Flexible. 500–2,000 pcs minimum. Trial orders welcome. Scale up at your pace without overstock risk.",
   False),
  ("⏱","LEAD TIME\n(To Mogadishu)",
   "Slowest. 45–60 days production + 20–25 days sea via multiple transshipment ports. Total: 65–85 days.",
   "Moderate. 30–45 days production + 18–22 days sea via Colombo or Dubai. Total: 48–67 days.",
   "✅ Fastest. 21–28 days production + 10–14 days DIRECT Karachi→Mogadishu (Maersk Musafir Express). Total: 31–42 days.",
   True),
  ("⭐","MACAWIIS\nQUALITY",
   "⚠ Mostly synthetic polyester/viscose blends. Somali men dislike the feel. Not genuine checked cotton fabric.",
   "Good cotton lungi available. Limited checked patterns. Quality varies by region — Gujarat is best.",
   "✅ Best 100% Cotton. Authentic checked weave from Faisalabad. Exact feel Somali market demands. World-class quality.",
   False),
  ("💰","PRICE\n(CIF Mogadishu)",
   "Low unit price. But long shipping adds $0.40–0.60/pc freight. Hidden quality issues reduce the advantage.",
   "Mid-range pricing. No direct Mogadishu route — transshipped via Dubai or Colombo raises landed cost.",
   "✅ Best Total Value. $1.20–1.40 CIF Mogadishu. Shortest sea route = lowest freight cost. Best price per quality.",
   True),
  ("✔","COMPLIANCE\n& PAYMENT",
   "OEKO-TEX only from large factories. Small suppliers uncertified. Payment: LC or TT only. No Dahabshiil.",
   "BSCI, OEKO-TEX improving. Better than China. LC / TT payment only. Dahabshiil NOT accepted.",
   "✅ OEKO-TEX certified. ISO 9001. WeBOC export certified. ✅ Dahabshiil accepted. 50% advance + 50% on B/L copy.",
   False),
  ("⚠","WEAKNESS\nFor Somalia",
   "Synthetic macawiis rejected by Somali buyers. Longest shipping route. Language barrier. No cultural ties.",
   "No direct Mogadishu shipping. Slower transit. Some Somali buyers prefer to avoid Indian suppliers.",
   "✅ No major weakness. Smaller factory capacity vs China — covered by flexible MOQ and direct shipping advantage.",
   True),
]

for icon, title, ch, ind, pak, alt in criteria:
    story.append(crit_row(icon, title, ch, ind, pak, alt))
    story.append(Spacer(1, 0.7*mm))

story.append(Spacer(1, 2*mm))

# ══════════════════════════════════════════════════════════════════════════════
# 4. HONEST SUMMARY TABLE  (colored badge chips)
# ══════════════════════════════════════════════════════════════════════════════
sum_title = Table([[P("THE HONEST SUMMARY", 10, WHITE, TA_CENTER, bold=True, lh=13)]],
                  colWidths=[CW])
sum_title.setStyle(TableStyle([
    ('BACKGROUND',(0,0),(-1,-1),NAVY),
    ('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5),
    ('BOX',(0,0),(-1,-1),1.5,GOLD),
]))
story.append(sum_title)

SL = 36*mm
SC = (CW - SL) / 3

def sum_lbl(txt):
    return Paragraph(txt, S('_', 7.5, MAROON, bold=True, lh=10))

rows = [
    # (label, china_badge, china_color, india_badge, india_color, pak_badge, pak_color)
    ("💰  PRICE (CIF Mogadishu)",    "MEDIUM",     B_AMBER, "MEDIUM",     B_AMBER, "✅ BEST VALUE",   B_GREEN),
    ("📦  MOQ",                       "VERY HIGH",  B_RED,   "MEDIUM",     B_AMBER, "✅ FLEXIBLE",     B_GREEN),
    ("⏱  LEAD TIME",                  "SLOWEST",    B_RED,   "SLOW",       B_AMBER, "✅ FASTEST",      B_GREEN),
    ("⭐  MACAWIIS QUALITY",           "SYNTHETIC",  B_RED,   "GOOD",       B_AMBER, "✅ BEST COTTON",  B_GREEN),
    ("✔  COMPLIANCE",                 "MEDIUM",     B_AMBER, "GROWING",    B_AMBER, "✅ STRONG",       B_GREEN),
    ("💳  DAHABSHIIL PAYMENT",         "❌ NO",       B_RED,   "❌ NO",       B_RED,   "✅ YES",          B_GREEN),
    ("🚢  DIRECT TO MOGADISHU",        "❌ NO",       B_RED,   "❌ NO",       B_RED,   "✅ YES (Maersk)", B_GREEN),
    ("🤝  SOMALIA TRUST LEVEL",        "LOW",        B_GREY,  "MEDIUM",     B_AMBER, "✅ HIGH",         B_GREEN),
]

# Header row
sum_hdr_data = [
    P("CRITERIA", 7.5, WHITE, TA_LEFT, bold=True),
    P("🇨🇳  CHINA",   8, WHITE, TA_CENTER, bold=True),
    P("🇮🇳  INDIA",   8, WHITE, TA_CENTER, bold=True),
    P("🇵🇰  PAKISTAN",8, WHITE, TA_CENTER, bold=True),
]
table_data = [sum_hdr_data]
for lbl_txt, c_txt, c_bg, i_txt, i_bg, p_txt, p_bg in rows:
    table_data.append([
        sum_lbl(lbl_txt),
        badge(c_txt, c_bg),
        badge(i_txt, i_bg),
        badge(p_txt, p_bg),
    ])

sum_tbl = Table(table_data, colWidths=[SL, SC, SC, SC])
sum_styles = [
    ('BACKGROUND',    (0,0),(-1,0),  NAVY),
    ('TEXTCOLOR',     (0,0),(-1,0),  WHITE),
    ('BOX',           (0,0),(-1,-1), 1.2, GOLD),
    ('LINEBELOW',     (0,0),(-1,0),  0.8, GOLD),
    ('INNERGRID',     (0,0),(-1,-1), 0.3, GOLD_LITE),
    ('TOPPADDING',    (0,0),(-1,-1), 4),
    ('BOTTOMPADDING', (0,0),(-1,-1), 4),
    ('LEFTPADDING',   (0,0),(-1,-1), 5),
    ('RIGHTPADDING',  (0,0),(-1,-1), 5),
    ('VALIGN',        (0,0),(-1,-1), 'MIDDLE'),
    ('ALIGN',         (1,0),(-1,-1), 'CENTER'),
]
for i in range(1, len(table_data)):
    bg = CREAM2 if i % 2 == 0 else CREAM
    sum_styles.append(('BACKGROUND', (0,i),(0,i), bg))
    sum_styles.append(('BACKGROUND', (1,i),(2,i), bg))
    sum_styles.append(('BACKGROUND', (3,i),(3,i), C_GRN_BG))

sum_tbl.setStyle(TableStyle(sum_styles))
story.append(sum_tbl)
story.append(Spacer(1, 2*mm))

# ══════════════════════════════════════════════════════════════════════════════
# 5. REAL INSIGHT  (3 panels)
# ══════════════════════════════════════════════════════════════════════════════
ins_title = Table([[P("THE REAL INSIGHT FOR SOMALIA BUYERS — 2026", 9, WHITE, TA_CENTER, bold=True, lh=12)]],
                  colWidths=[CW])
ins_title.setStyle(TableStyle([
    ('BACKGROUND',(0,0),(-1,-1),MAROON),
    ('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5),
    ('BOX',(0,0),(-1,-1),1.5,GOLD),
]))
story.append(ins_title)

PW = (CW - 4*mm) / 3

def insight_panel(flag, country, body, bg, tc, bc):
    t = Table([
        [P(flag,    16, tc, TA_CENTER, lh=20)],
        [P(country,  9, tc, TA_CENTER, bold=True, lh=12)],
        [Spacer(1,1*mm)],
        [P(body,     7, tc, TA_CENTER, lh=10.5)],
    ], colWidths=[PW])
    t.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,-1),bg),
        ('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6),
        ('LEFTPADDING',(0,0),(-1,-1),5),('RIGHTPADDING',(0,0),(-1,-1),5),
        ('BOX',(0,0),(-1,-1),1.5,bc),
        ('TOPPADDING',(2,0),(2,0),1),('BOTTOMPADDING',(2,0),(2,0),1),
    ]))
    return t

p1 = insight_panel("🇨🇳","CHINA",
    "Use only for synthetic garments, electronics or household goods.\nFor Macawiis — NOT recommended.\nSomali market rejects synthetic feel and longest shipping route defeats price advantage.",
    C_RED_BG, C_RED, C_RED)

p2 = insight_panel("🇮🇳","INDIA",
    "Good for variety and flexibility.\nBut no direct Mogadishu sea route means higher landed cost.\nDahabshiil payment not accepted — complicates transactions for Somali buyers.",
    C_ORG_BG, C_ORG, C_ORG)

p3 = insight_panel("🇵🇰","PAKISTAN  ✅  BEST CHOICE",
    "Best cotton Macawiis quality + fastest sea route to Mogadishu + Dahabshiil accepted + lowest CIF cost.\nPakistan is already Somalia's #1 rice supplier — trusted country, smooth customs, strong relationship.",
    C_GRN_BG, C_GRN, C_GRN)

panels = Table([[p1, Spacer(2*mm,1), p2, Spacer(2*mm,1), p3]],
               colWidths=[PW, 2*mm, PW, 2*mm, PW])
panels.setStyle(TableStyle([
    ('VALIGN',(0,0),(-1,-1),'TOP'),
    ('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(-1,-1),0),
    ('TOPPADDING',(0,0),(-1,-1),0),('BOTTOMPADDING',(0,0),(-1,-1),0),
]))
story.append(panels)
story.append(Spacer(1, 2*mm))

# ══════════════════════════════════════════════════════════════════════════════
# 6. BOTTOM TAGLINE BAR
# ══════════════════════════════════════════════════════════════════════════════
tagline_bar = Table([[
    P("🏭  Source direct from factory",      7, GOLD_LITE, TA_CENTER, bold=True),
    P("🚢  Match country to product",         7, GOLD_LITE, TA_CENTER, bold=True),
    P("📦  Build reliable relationships",     7, GOLD_LITE, TA_CENTER, bold=True),
    P("💰  Diversify your sourcing",          7, GOLD_LITE, TA_CENTER, bold=True),
]], colWidths=[CW/4]*4)
tagline_bar.setStyle(TableStyle([
    ('BACKGROUND',    (0,0),(-1,-1), NAVY2),
    ('TOPPADDING',    (0,0),(-1,-1), 4),
    ('BOTTOMPADDING', (0,0),(-1,-1), 4),
    ('INNERGRID',     (0,0),(-1,-1), 0.3, GOLD),
    ('BOX',           (0,0),(-1,-1), 0.5, GOLD),
]))
story.append(tagline_bar)
story.append(Spacer(1, 1.5*mm))

# ══════════════════════════════════════════════════════════════════════════════
# 7. FOOTER
# ══════════════════════════════════════════════════════════════════════════════
footer = Table([[
    Image(LOGO_PATH, width=20*mm, height=13*mm),
    Table([
        [P("AKH LINEN HOUSE", 10, WHITE, TA_LEFT, bold=True, lh=13)],
        [P("Pakistan Direct Textile Exporter  —  CIF Mogadishu Available", 7.5, GOLD_LITE, TA_LEFT, lh=10)],
        [P("Bed Linen  •  Macawiis  •  Towels  •  Fabric  •  Prayer Mats", 7, GOLD, TA_LEFT, lh=10)],
    ], colWidths=[100*mm]),
    Table([
        [P(f"📱  {WA}", 8, WHITE, TA_RIGHT, bold=True, lh=11)],
        [P(f"✉  {EMAIL}", 8, GOLD_LITE, TA_RIGHT, lh=11)],
        [P("Pakistan  •  Direct Factory Prices", 7, GOLD, TA_RIGHT, lh=10)],
    ], colWidths=[55*mm]),
]], colWidths=[22*mm, 102*mm, 57*mm])
footer.setStyle(TableStyle([
    ('BACKGROUND',    (0,0),(-1,-1), MAROON),
    ('VALIGN',        (0,0),(-1,-1), 'MIDDLE'),
    ('TOPPADDING',    (0,0),(-1,-1), 6),
    ('BOTTOMPADDING', (0,0),(-1,-1), 6),
    ('LEFTPADDING',   (0,0),(-1,-1), 5),
    ('RIGHTPADDING',  (0,0),(-1,-1), 5),
    ('BOX',           (0,0),(-1,-1), 2, GOLD),
]))
story.append(footer)

doc.build(story)
print("✅  Sourcing Comparison PDF generated!")
