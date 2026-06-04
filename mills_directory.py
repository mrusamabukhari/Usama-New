from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, HRFlowable
)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT

GREEN   = colors.HexColor("#1a7a3c")
GOLD    = colors.HexColor("#c8a200")
RED     = colors.HexColor("#c0392b")
DARK    = colors.HexColor("#1a2e1a")
WHITE   = colors.white
GREY    = colors.HexColor("#f0f0f0")
LGREEN  = colors.HexColor("#e8f5ec")
MIDGREY = colors.HexColor("#cccccc")
LBLUE   = colors.HexColor("#f0f4ff")

doc = SimpleDocTemplate(
    "/home/user/Usama-New/Gujranwala_Rice_Mills_Directory.pdf",
    pagesize=A4,
    rightMargin=1.5*cm, leftMargin=1.5*cm,
    topMargin=1.5*cm, bottomMargin=1.5*cm
)

W = 18.0*cm

def S(name, **kw):
    base = dict(fontName="Helvetica", fontSize=9, leading=13, textColor=DARK, alignment=TA_LEFT)
    base.update(kw)
    return ParagraphStyle(name, **base)

title_s  = S("title", fontSize=20, leading=26, textColor=WHITE, fontName="Helvetica-Bold", alignment=TA_CENTER)
sub_s    = S("sub",   fontSize=10, leading=14, textColor=GOLD,  fontName="Helvetica-Bold", alignment=TA_CENTER)
head_s   = S("head",  fontSize=9,  leading=13, textColor=WHITE, fontName="Helvetica-Bold", alignment=TA_CENTER)
body_s   = S("body",  fontSize=8,  leading=12, textColor=DARK,  fontName="Helvetica")
bold_s   = S("bold",  fontSize=8,  leading=12, textColor=DARK,  fontName="Helvetica-Bold")
green_s  = S("green", fontSize=8,  leading=12, textColor=GREEN, fontName="Helvetica-Bold")
gold_s   = S("gold",  fontSize=8,  leading=12, textColor=GOLD,  fontName="Helvetica-Bold")
num_s    = S("num",   fontSize=11, leading=15, textColor=WHITE, fontName="Helvetica-Bold", alignment=TA_CENTER)
mill_s   = S("mill",  fontSize=10, leading=14, textColor=DARK,  fontName="Helvetica-Bold")
cap_s    = S("cap",   fontSize=7,  leading=10, textColor=colors.HexColor("#666666"), fontName="Helvetica-Oblique", alignment=TA_CENTER)
tip_s    = S("tip",   fontSize=8,  leading=12, textColor=DARK,  fontName="Helvetica-Oblique")

def p(txt, style=body_s): return Paragraph(txt, style)
def sp(h=0.3): return Spacer(1, h*cm)

story = []

# ── HEADER ────────────────────────────────────────────────────────────────────
hdr = Table([[p("🏭  Gujranwala Rice Mills Directory", title_s)]], colWidths=[W])
hdr.setStyle(TableStyle([
    ("BACKGROUND",    (0,0),(-1,-1), GREEN),
    ("TOPPADDING",    (0,0),(-1,-1), 14),
    ("BOTTOMPADDING", (0,0),(-1,-1), 10),
    ("LEFTPADDING",   (0,0),(-1,-1), 10),
    ("RIGHTPADDING",  (0,0),(-1,-1), 10),
]))
story.append(hdr)

sub = Table([[p("Pakistan's Rice Capital — 25 Verified Mills with Contact Details", sub_s)]], colWidths=[W])
sub.setStyle(TableStyle([
    ("BACKGROUND",    (0,0),(-1,-1), DARK),
    ("TOPPADDING",    (0,0),(-1,-1), 7),
    ("BOTTOMPADDING", (0,0),(-1,-1), 7),
]))
story.append(sub)
story.append(sp(0.4))

# ── STATS BAR ─────────────────────────────────────────────────────────────────
stat_num = S("sn", fontSize=16, leading=20, textColor=GREEN, fontName="Helvetica-Bold", alignment=TA_CENTER)
stat_lbl = S("sl", fontSize=8,  leading=11, textColor=DARK,  fontName="Helvetica",      alignment=TA_CENTER)

stats = Table([
    [p("60–65%", stat_num), p("1,000+", stat_num), p("Kamoke", stat_num),   p("IRRI-6", stat_num)],
    [p("of Pakistan's\nrice mills", stat_lbl), p("mills in\nGujranwala dist.", stat_lbl),
     p("G.T. Road —\nhub of mills", stat_lbl), p("main export\nvariety", stat_lbl)],
], colWidths=[4.5*cm]*4)
stats.setStyle(TableStyle([
    ("BACKGROUND",    (0,0),(-1,-1), GREY),
    ("GRID",          (0,0),(-1,-1), 0.4, MIDGREY),
    ("TOPPADDING",    (0,0),(-1,-1), 7),
    ("BOTTOMPADDING", (0,0),(-1,-1), 5),
]))
story.append(stats)
story.append(sp(0.4))

# ── MILLS TABLE HEADER ────────────────────────────────────────────────────────
col_hdr = Table([[
    p("#",          head_s),
    p("Company Name", head_s),
    p("Address",    head_s),
    p("Phone / WhatsApp", head_s),
    p("Email / Web", head_s),
]], colWidths=[0.7*cm, 4.2*cm, 5.5*cm, 3.8*cm, 3.8*cm])
col_hdr.setStyle(TableStyle([
    ("BACKGROUND",    (0,0),(-1,-1), DARK),
    ("TOPPADDING",    (0,0),(-1,-1), 7),
    ("BOTTOMPADDING", (0,0),(-1,-1), 7),
    ("LEFTPADDING",   (0,0),(-1,-1), 5),
    ("RIGHTPADDING",  (0,0),(-1,-1), 5),
    ("GRID",          (0,0),(-1,-1), 0.4, colors.HexColor("#444444")),
    ("VALIGN",        (0,0),(-1,-1), "MIDDLE"),
]))
story.append(col_hdr)

# ── MILLS DATA ────────────────────────────────────────────────────────────────
mills = [
    ("1",  "Waqar Rice Mills",
     "G.T. Road, Usman Nagar,\nKamoke, Gujranwala",
     "+92-55-6665522\nWA: +92-300-8999999",
     "info@waqarrice.com\nwaqarrice.com"),

    ("2",  "Amir Rice Mills (Pvt) Ltd ⭐",
     "G.T. Road, Near Ghania,\nKamoke, Gujranwala",
     "+92-340-8405555",
     "amirricemills@gmail.com\namirice.com"),

    ("3",  "M. Hussain Rice Mills",
     "Usman Nagar, Hinda Stop,\nG.T. Road, Kamoke",
     "+92-55-6663233",
     "info@hrmrice.com\nhrmrice.com"),

    ("4",  "Sardar Rice Mills",
     "Near Railway Line Cross,\nGhakkhar, Gujranwala",
     "+92-301-3832333\n+92-300-6430580",
     "sardarricemills@hotmail.com\nsardarricemills.com"),

    ("5",  "Galaxy Rice Mills (Pvt) Ltd ⭐",
     "Wahndo Road, Eminabad,\nGujranwala",
     "+92-55-3402184\n+92-55-3402284",
     "galaxyrice.com\n(Exports to Europe)"),

    ("6",  "Al Majeed Rice Mills ⭐",
     "Kamoke, G.T. Road,\nGujranwala",
     "+92-321-6439969",
     "almajeedrice@outlook.com\nalmajeedrice.com"),

    ("7",  "Sohail Rice Mills",
     "Near Railway Crossing,\nKassoke Road, Kamoke",
     "+92-55-6811656",
     "sohailrice.com"),

    ("8",  "Falcon Rice Mills (Pvt) Ltd",
     "College Road Industrial Estate,\nKamoke, Gujranwala",
     "+92-55-6816601\n+92-300-8454377",
     "—"),

    ("9",  "Meh's Enterprises",
     "Wakeel Khan Road,\nKamoke, Gujranwala",
     "+92-55-6813801\n+92-321-8640099",
     "—"),

    ("10", "M. Raheem Rice Mills ⭐",
     "Main G.T. Road,\nKamoke, Gujranwala",
     "—",
     "mraheemricemills.com\n(30+ years, REAP member)"),

    ("11", "Al Wahab Rice Mills (Pvt) Ltd",
     "Main G.T. Road, Sadhoke,\nGujranwala 52368",
     "WA: +92-308-8882506",
     "sales@alwahabrice.com\nalwahabrice.com"),

    ("12", "Riffino Rice Mills (Pvt) Ltd",
     "Opp. Canal Rest House,\nG.T. Road, Sadhoke",
     "+92-321-8111132\n+92-332-8111132",
     "riffinoricemills.com"),

    ("13", "Agroman Crystal Rice Mills",
     "Sayad Nagar Road,\nAli Pur Chattah, Gujranwala",
     "+92-55-6333865\n+92-300-4137538",
     "(Ships to USA & EU)"),

    ("14", "AITCO Enterprise ⭐",
     "Mozah Khiali Shah Pur,\nGujranwala",
     "WA: +92-300-6451430",
     "export.aitco.enterprise\n@gmail.com"),

    ("15", "Ikram Rice Mills ⭐",
     "N5, Eminabad More,\nMain G.T. Road, Gujranwala",
     "+92-300-8645900",
     "ikramrice.com\n(REAP, Est. 1972)"),

    ("16", "Al-Huda Rice Mills",
     "Sialkot Road, Islam Colony,\nCivil Lines, Gujranwala",
     "+92-300-7406367",
     "info@alhudaricemills.com\nalhudaricemills.com"),

    ("17", "Zarafa Rice (Marshal Rice Mills)",
     "G.T. Road, Pindi By-Pass,\nGujranwala",
     "+92-55-3892439\n+92-300-8629581",
     "marshalricemills@hotmail.com\nzarafarice.com"),

    ("18", "Falak Basmati Rice",
     "Wahndo Road, Eminabad,\nGujranwala",
     "+92-55-3264184",
     "—"),

    ("19", "Aftab Rice Mill",
     "Amrat Pura,\nGujranwala",
     "+92-55-3015255",
     "—"),

    ("20", "Al-Siraj Rice Mill",
     "Near Tomari Mandir,\nBadoki, Gujranwala",
     "+92-55-3013303",
     "—"),

    ("21", "Gill Rice Processing Mills",
     "Kashmir Colony, Kotli Pir\nAhmed Shah, Gujranwala",
     "+92-55-3417195",
     "—"),

    ("22", "Modern Rice & General Mills",
     "Ghallah Mandi, G.T. Road,\nGujranwala",
     "+92-55-3840298",
     "—"),

    ("23", "Millat Rice Mills",
     "Vaniawala,\nGujranwala",
     "+92-55-3202070",
     "—"),

    ("24", "Rice Specialist Processors",
     "3-Km, G.T. Road,\nKamoke, Gujranwala",
     "+92-55-6815452",
     "—"),

    ("25", "Al-Riaz Rice Mills ⭐",
     "G.T. Road, Kot Khizri,\nWazirabad, Gujranwala 52001",
     "—",
     "alriazrice.com\n(60,000 T/yr capacity)"),
]

col_w = [0.7*cm, 4.2*cm, 5.5*cm, 3.8*cm, 3.8*cm]

for i, (num, name, addr, phone, contact) in enumerate(mills):
    bg = LGREEN if i % 2 == 0 else WHITE
    star = "⭐" in name
    name_clean = name
    row = Table([[
        p(num, S("n2", fontSize=9, leading=13, textColor=WHITE, fontName="Helvetica-Bold", alignment=TA_CENTER)),
        p(name_clean, S("nc", fontSize=8, leading=12, textColor=GREEN if star else DARK, fontName="Helvetica-Bold")),
        p(addr,   body_s),
        p(phone,  body_s),
        p(contact,body_s),
    ]], colWidths=col_w)
    row.setStyle(TableStyle([
        ("BACKGROUND",    (0,0),(0,0),   GREEN),
        ("BACKGROUND",    (1,0),(-1,0),  bg),
        ("GRID",          (0,0),(-1,-1), 0.4, MIDGREY),
        ("VALIGN",        (0,0),(-1,-1), "MIDDLE"),
        ("TOPPADDING",    (0,0),(-1,-1), 6),
        ("BOTTOMPADDING", (0,0),(-1,-1), 6),
        ("LEFTPADDING",   (0,0),(-1,-1), 5),
        ("RIGHTPADDING",  (0,0),(-1,-1), 5),
    ]))
    story.append(row)

story.append(sp(0.5))

# ── TOP 5 RECOMMENDATION ──────────────────────────────────────────────────────
rec_hdr = Table([[p("⭐  Best 5 Mills to Contact First (IRRI-6 Export Specialists)",
                    S("rh", fontSize=10, leading=14, textColor=WHITE, fontName="Helvetica-Bold", alignment=TA_CENTER))]],
                colWidths=[W])
rec_hdr.setStyle(TableStyle([
    ("BACKGROUND", (0,0),(-1,-1), GREEN),
    ("TOPPADDING", (0,0),(-1,-1), 8),
    ("BOTTOMPADDING",(0,0),(-1,-1), 8),
]))
story.append(rec_hdr)

rec_rows = [
    [p("Mill", head_s), p("Why Best", head_s), p("Contact", head_s)],
    [p("Waqar Rice Mills", bold_s),       p("24/7 WhatsApp, export-ready, IRRI-6 specialist", body_s), p("+92-300-8999999", green_s)],
    [p("Amir Rice Mills", bold_s),        p("Top-10 Pakistan exporter, Est. 1982, very reliable", body_s), p("+92-340-8405555", green_s)],
    [p("Ikram Rice Mills", bold_s),       p("REAP member, Est. 1972, explicitly lists IRRI-6", body_s), p("+92-300-8645900", green_s)],
    [p("Al-Riaz Rice Mills", bold_s),     p("Largest capacity — 60,000 tons/year, best bulk price", body_s), p("alriazrice.com", green_s)],
    [p("AITCO Enterprise", bold_s),       p("IRRI-6 specialist, 20+ years Africa export experience", body_s), p("+92-300-6451430", green_s)],
]
rec_t = Table(rec_rows, colWidths=[4.5*cm, 9*cm, 4.5*cm])
rec_t.setStyle(TableStyle([
    ("BACKGROUND",    (0,0),(-1,0),  DARK),
    ("BACKGROUND",    (0,1),(-1,1),  LGREEN),
    ("BACKGROUND",    (0,2),(-1,2),  WHITE),
    ("BACKGROUND",    (0,3),(-1,3),  LGREEN),
    ("BACKGROUND",    (0,4),(-1,4),  WHITE),
    ("BACKGROUND",    (0,5),(-1,5),  LGREEN),
    ("GRID",          (0,0),(-1,-1), 0.4, MIDGREY),
    ("VALIGN",        (0,0),(-1,-1), "MIDDLE"),
    ("TOPPADDING",    (0,0),(-1,-1), 7),
    ("BOTTOMPADDING", (0,0),(-1,-1), 7),
    ("LEFTPADDING",   (0,0),(-1,-1), 7),
    ("RIGHTPADDING",  (0,0),(-1,-1), 7),
]))
story.append(rec_t)
story.append(sp(0.4))

# ── PRO TIPS ──────────────────────────────────────────────────────────────────
tips_hdr = Table([[p("💡  Pro Tips — Before You Contact Any Mill",
                     S("th", fontSize=10, leading=14, textColor=WHITE, fontName="Helvetica-Bold", alignment=TA_CENTER))]],
                 colWidths=[W])
tips_hdr.setStyle(TableStyle([
    ("BACKGROUND", (0,0),(-1,-1), DARK),
    ("TOPPADDING", (0,0),(-1,-1), 7),
    ("BOTTOMPADDING",(0,0),(-1,-1), 7),
]))
story.append(tips_hdr)

tips = [
    ["WhatsApp First", "Pakistani mills respond faster to WhatsApp than email. Message in Urdu if possible."],
    ["Visit Kamoke G.T. Road", "80% of mills are on this single road — one visit = 10+ quotes in one day."],
    ["Ask for REAP Membership", "Confirms mill is a verified exporter. Check reap.com.pk member profiles."],
    ["Request Free Sample", "Always ask for 1–2 kg sample before any order. Serious mills always agree."],
    ["Get 3+ Quotes", "Contact minimum 3 mills and compare — use competing quotes to negotiate lower price."],
    ["Off-Season = Cheap", "Oct–Jan (after harvest) — prices are at their lowest. Best time to lock rates."],
    ["Pay Advance = Discount", "Offer 40–50% advance payment — mills typically give 3–5% price discount."],
    ["Verify Before Paying", "Visit mill physically or send a local agent before making any advance payment."],
]

tip_rows = [[
    p(t[0], bold_s),
    p(t[1], body_s),
] for t in tips]

for i in range(len(tip_rows)):
    bg = LGREEN if i % 2 == 0 else WHITE
    row = Table([tip_rows[i]], colWidths=[4*cm, 14*cm])
    row.setStyle(TableStyle([
        ("BACKGROUND",    (0,0),(0,0), colors.HexColor("#d4edda")),
        ("BACKGROUND",    (1,0),(1,0), bg),
        ("GRID",          (0,0),(-1,-1), 0.4, MIDGREY),
        ("VALIGN",        (0,0),(-1,-1), "MIDDLE"),
        ("TOPPADDING",    (0,0),(-1,-1), 6),
        ("BOTTOMPADDING", (0,0),(-1,-1), 6),
        ("LEFTPADDING",   (0,0),(-1,-1), 7),
        ("RIGHTPADDING",  (0,0),(-1,-1), 7),
    ]))
    story.append(row)

story.append(sp(0.4))

# ── KEY RESOURCES ─────────────────────────────────────────────────────────────
res_t = Table([[p(
    "Key Resources:  reap.com.pk  ·  tdap.gov.pk  ·  alibaba.com (search: Pakistan IRRI-6 rice supplier)",
    S("res", fontSize=8, leading=12, textColor=DARK, fontName="Helvetica", alignment=TA_CENTER)
)]], colWidths=[W])
res_t.setStyle(TableStyle([
    ("BACKGROUND",    (0,0),(-1,-1), colors.HexColor("#fffbea")),
    ("LINEABOVE",     (0,0),(-1,0),  1, GOLD),
    ("LINEBELOW",     (0,0),(-1,0),  1, GOLD),
    ("TOPPADDING",    (0,0),(-1,-1), 7),
    ("BOTTOMPADDING", (0,0),(-1,-1), 7),
]))
story.append(res_t)
story.append(sp(0.3))

# ── FOOTER ────────────────────────────────────────────────────────────────────
story.append(HRFlowable(width="100%", thickness=0.5, color=MIDGREY))
story.append(sp(0.1))
story.append(p("Pakistan Rice Export — Gujranwala Mills Directory  ·  Compiled from REAP, TDAP, Business Directories & Company Websites  ·  2025", cap_s))

doc.build(story)
print("PDF created: Gujranwala_Rice_Mills_Directory.pdf")
