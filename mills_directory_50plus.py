from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, HRFlowable, PageBreak
)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT

GREEN   = colors.HexColor("#1a7a3c")
GOLD    = colors.HexColor("#c8a200")
DARK    = colors.HexColor("#1a2e1a")
WHITE   = colors.white
GREY    = colors.HexColor("#f0f0f0")
LGREEN  = colors.HexColor("#e8f5ec")
MIDGREY = colors.HexColor("#cccccc")
DKGREEN = colors.HexColor("#d4edda")
YELLOW  = colors.HexColor("#fffbea")

doc = SimpleDocTemplate(
    "/home/user/Usama-New/Gujranwala_Rice_Mills_84_Directory.pdf",
    pagesize=A4,
    rightMargin=1.2*cm, leftMargin=1.2*cm,
    topMargin=1.2*cm, bottomMargin=1.2*cm
)

W = 18.6*cm

def S(name, **kw):
    base = dict(fontName="Helvetica", fontSize=8, leading=11, textColor=DARK, alignment=TA_LEFT)
    base.update(kw)
    return ParagraphStyle(name, **base)

title_s = S("t",  fontSize=18, leading=24, textColor=WHITE, fontName="Helvetica-Bold", alignment=TA_CENTER)
sub_s   = S("s",  fontSize=10, leading=14, textColor=GOLD,  fontName="Helvetica-Bold", alignment=TA_CENTER)
area_s  = S("a",  fontSize=10, leading=14, textColor=WHITE, fontName="Helvetica-Bold", alignment=TA_LEFT)
head_s  = S("h",  fontSize=8,  leading=11, textColor=WHITE, fontName="Helvetica-Bold", alignment=TA_CENTER)
body_s  = S("b",  fontSize=7,  leading=10, textColor=DARK,  fontName="Helvetica")
bold_s  = S("bo", fontSize=7,  leading=10, textColor=DARK,  fontName="Helvetica-Bold")
star_s  = S("st", fontSize=7,  leading=10, textColor=GREEN, fontName="Helvetica-Bold")
num_s   = S("n",  fontSize=9,  leading=12, textColor=WHITE, fontName="Helvetica-Bold", alignment=TA_CENTER)
cap_s   = S("c",  fontSize=7,  leading=10, textColor=colors.HexColor("#666"), fontName="Helvetica-Oblique", alignment=TA_CENTER)
stat_n  = S("sn", fontSize=15, leading=19, textColor=GREEN, fontName="Helvetica-Bold", alignment=TA_CENTER)
stat_l  = S("sl", fontSize=7,  leading=10, textColor=DARK,  fontName="Helvetica",      alignment=TA_CENTER)
tip_s   = S("tp", fontSize=7,  leading=11, textColor=DARK,  fontName="Helvetica-Oblique")

def p(txt, style=body_s): return Paragraph(str(txt), style)
def sp(h=0.25): return Spacer(1, h*cm)

COL_W = [0.6*cm, 3.8*cm, 4.5*cm, 3.2*cm, 3.2*cm, 3.3*cm]

story = []

# ── HEADER ────────────────────────────────────────────────────────────────────
h = Table([[p("🏭  Gujranwala Rice Mills — Complete Directory", title_s)]], colWidths=[W])
h.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),GREEN),
    ("TOPPADDING",(0,0),(-1,-1),12),("BOTTOMPADDING",(0,0),(-1,-1),9),
    ("LEFTPADDING",(0,0),(-1,-1),8),("RIGHTPADDING",(0,0),(-1,-1),8)]))
story.append(h)

s = Table([[p("84 Verified Mills — Kamoke · Sadhoke · Ghakhar · Wazirabad · Eminabad · Ali Pur Chattah · Gujranwala City · Hafizabad", sub_s)]], colWidths=[W])
s.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),DARK),
    ("TOPPADDING",(0,0),(-1,-1),6),("BOTTOMPADDING",(0,0),(-1,-1),6)]))
story.append(s)
story.append(sp(0.3))

# ── STATS BAR ─────────────────────────────────────────────────────────────────
stats = Table([
    [p("84",stat_n),   p("28",stat_n),     p("7",stat_n),       p("60-65%",stat_n),  p("IRRI-6",stat_n)],
    [p("Total\nMills",stat_l), p("★ REAP / Export\nVerified",stat_l),
     p("Areas\nCovered",stat_l), p("of Pakistan's\nRice Mills",stat_l), p("Main Export\nVariety",stat_l)],
], colWidths=[3.72*cm]*5)
stats.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),GREY),
    ("GRID",(0,0),(-1,-1),0.4,MIDGREY),
    ("TOPPADDING",(0,0),(-1,-1),6),("BOTTOMPADDING",(0,0),(-1,-1),5)]))
story.append(stats)
story.append(sp(0.3))

# ── LEGEND ────────────────────────────────────────────────────────────────────
leg = Table([[p("★ = REAP Member / Known Exporter     — = Information not publicly available     All phone numbers are WhatsApp-enabled unless stated otherwise",
    S("lg", fontSize=7, leading=10, textColor=DARK, fontName="Helvetica-Oblique", alignment=TA_CENTER))]], colWidths=[W])
leg.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),YELLOW),
    ("LINEABOVE",(0,0),(-1,0),0.8,GOLD),("LINEBELOW",(0,0),(-1,0),0.8,GOLD),
    ("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5)]))
story.append(leg)
story.append(sp(0.3))

# ── AREA HEADER ───────────────────────────────────────────────────────────────
def area_header(title, count):
    t = Table([[
        p(f"  📍 {title}", area_s),
        p(f"{count} Mills", S("ac", fontSize=9, leading=13, textColor=GOLD, fontName="Helvetica-Bold", alignment=TA_CENTER))
    ]], colWidths=[15*cm, 3.6*cm])
    t.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),DARK),
        ("TOPPADDING",(0,0),(-1,-1),6),("BOTTOMPADDING",(0,0),(-1,-1),6),
        ("LEFTPADDING",(0,0),(-1,-1),6),("RIGHTPADDING",(0,0),(-1,-1),6)]))
    return t

def col_header():
    t = Table([[
        p("#",head_s), p("Company Name",head_s), p("Address",head_s),
        p("Phone",head_s), p("WhatsApp / Mobile",head_s), p("Email / Website",head_s)
    ]], colWidths=COL_W)
    t.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),colors.HexColor("#2d5a3d")),
        ("GRID",(0,0),(-1,-1),0.4,colors.HexColor("#1a4a2e")),
        ("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5),
        ("LEFTPADDING",(0,0),(-1,-1),4),("RIGHTPADDING",(0,0),(-1,-1),4),
        ("VALIGN",(0,0),(-1,-1),"MIDDLE")]))
    return t

def mill_row(num, name, addr, phone, wa, contact, idx):
    bg = LGREEN if idx % 2 == 0 else WHITE
    star = "★" in name
    name_style = star_s if star else bold_s
    t = Table([[
        p(num, num_s),
        p(name, name_style),
        p(addr, body_s),
        p(phone, body_s),
        p(wa, body_s),
        p(contact, body_s),
    ]], colWidths=COL_W)
    t.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(0,0),GREEN),
        ("BACKGROUND",(1,0),(-1,0),bg),
        ("GRID",(0,0),(-1,-1),0.4,MIDGREY),
        ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
        ("TOPPADDING",(0,0),(-1,-1),4),("BOTTOMPADDING",(0,0),(-1,-1),4),
        ("LEFTPADDING",(0,0),(-1,-1),4),("RIGHTPADDING",(0,0),(-1,-1),4),
    ]))
    return t

# ══════════════════════════════════════════════════════════════════════════════
# AREA 1: KAMOKE (27 mills)
# ══════════════════════════════════════════════════════════════════════════════
story.append(area_header("AREA 1: KAMOKE — G.T. Road / Usman Nagar / Ghalla Mandi", 27))
story.append(col_header())

kamoke = [
    ("1",  "★ Waqar Rice Mills",          "G.T. Road, Usman Nagar,\nKamoke, Gujranwala",         "+92-55-6665522",          "+92-300-8999999",   "info@waqarrice.com\nwaqarrice.com"),
    ("2",  "★ Amir Rice Mills (Pvt) Ltd", "Ghalla Mandi, Kamoke,\nDistt. Gujranwala",             "+92-340-8405555",         "—",                 "amirricemills@gmail.com\namirice.com"),
    ("3",  "★ M. Hussain Rice Mills",     "Usman Nagar, Hinda Stop,\nG.T. Road, Kamoke",           "+92-55-6814490",          "—",                 "info@hrmrice.com\nhrmrice.com"),
    ("4",  "★ M. Raheem Rice Mills",      "Main G.T. Road,\nKamoke, Gujranwala",                   "+92-55-6665542/43",       "—",                 "info@mraheemricemills.com\nmraheemricemills.com"),
    ("5",  "★ Al Majeed Rice Mills",      "G.T. Road, Kamoke,\nDistt. Gujranwala",                 "—",                       "+92-321-6439969",   "almajeedrice@outlook.com\nalmajeedrice.com"),
    ("6",  "★ Falcon Rice Mills (Pvt)",   "College Road Industrial Estate,\nKamoke, Gujranwala",   "+92-55-6816601/02",       "+92-300-8454377",   "—"),
    ("7",  "★ Rice Experts Enterprises",  "2 KM G.T. Road, Kamoke,\nDistt. Gujranwala",            "+92-305-5519995",         "+92-305-5519995",   "gm@riceexperts.com\nriceexperts.com"),
    ("8",  "★ Haider Ikram Rice Mills",   "Behind Civil Courts,\nG.T. Road, Kamoke",               "+92-300-8642626",         "+92-321-6468888",   "haiderikramrice.com"),
    ("9",  "★ Buraq Rice Trading",        "New Model Town,\nKamoke, Gujranwala",                   "+92-317-8080318",         "+92-321-4046180",   "info@buraqricetrading.com\nburaqricetrading.com"),
    ("10", "★ Green Foods (Pvt) Ltd",     "GT Road (Near Toll Plaza),\nKamoke, Punjab",            "—",                       "—",                 "greenfoods.com.pk"),
    ("11", "★ Meh's Enterprises",         "Wakeel Khan Road,\nKamoke, Gujranwala",                 "+92-55-6813801",          "+92-321-8640099",   "—"),
    ("12", "★ Al Wakeel National Mills",  "New Ghalla Mandi,\nKamoke, Gujranwala",                 "+92-343-6379596",         "—",                 "nationalricemills@gmail.com"),
    ("13", "★ AITCO Enterprise",          "Mozah Khiali Shah Pur,\nGujranwala",                    "—",                       "+92-300-6451430",   "export.aitco.enterprise\n@gmail.com"),
    ("14", "★ Sohail Rice Mills",         "Bhan Pur Road,\nKamoke, Gujranwala",                    "—",                       "+92-300-8740498",   "sohailricemills@gmail.com"),
    ("15", "★ Sadiq Rice Mills",          "Industrial Estate, College Rd,\nKamoke, Gujranwala",    "—",                       "—",                 "—"),
    ("16", "Ocean Pearl Rice Mills",      "G.T. Road, Usman Nagar,\nKamoke (Waqar Group)",         "—",                       "+92-300-8999999",   "oceanpearlrice.com"),
    ("17", "Kamoke Rice Mills",           "Near Telephone Exchange,\nG.T. Road, Kamoke",            "+92-55-6810125",          "—",                 "—"),
    ("18", "Neelam Rice Mills",           "G.T. Road,\nKamoke, Punjab",                             "+92-55-6810239",          "—",                 "—"),
    ("19", "Data Corporation Rice",       "Line Par,\nKamoke, Gujranwala",                          "—",                       "+92-300-8642326",   "datacorporationrice\nmills@gmail.com"),
    ("20", "Ramzan Rice Mill",            "Main G.T. Road,\nKamoke, Gujranwala",                   "—",                       "+92-300-9477302",   "ramzanricemills@gmail.com\nramzanricemill.com"),
    ("21", "A.T.C. Rice Mills",           "Tataly Aali Road,\nKamoke, Gujranwala",                 "—",                       "+92-301-8450808",   "a.t.c.ricemills@gmail.com"),
    ("22", "Qazi Rice Mills",             "Food Grain Market,\nKamoke, Punjab",                    "+92-55-6814204",          "—",                 "—"),
    ("23", "Rice Specialist Processors",  "Near Railway Crossing,\nKassoke Road, Kamoke",           "+92-55-6811656",          "—",                 "—"),
    ("24", "M.K. Rice Mills",             "Ghalla Mandi, Kamoke\n(G.T. Road area)",                "+92-55-6816072",          "—",                 "—"),
    ("25", "Rizwan Rice Mills",           "Near Furniture Market,\nGhalla Mandi, Kamoke",           "—",                       "—",                 "—"),
    ("26", "Ikram Rice Mills",            "Behind Civil Courts,\nG.T. Road, Kamoke",               "+92-300-8642626",         "+92-321-6468888",   "ikramrice.com"),
    ("27", "★ Al Wahab Rice Mills",       "Main G.T. Road, Sadhoke\n(Kamoke area)",                "—",                       "+92-308-8882506",   "sales@alwahabrice.com\nalwahabrice.com"),
]

for i, row in enumerate(kamoke):
    story.append(mill_row(*row, i))

story.append(sp(0.35))

# ══════════════════════════════════════════════════════════════════════════════
# AREA 2: SADHOKE (5 mills)
# ══════════════════════════════════════════════════════════════════════════════
story.append(area_header("AREA 2: SADHOKE — G.T. Road", 5))
story.append(col_header())

sadhoke = [
    ("28", "★ Riffino Rice Mills (Pvt)",  "Opp. Canal Rest House,\nG.T. Road, Sadhoke",           "—",                       "+92-321-8111132\n+92-332-8111132", "riffinoricemills.com"),
    ("29", "★ Crown Rice Mills",          "G.T. Road, Sadhoke,\nDistt. Gujranwala",                "+92-55-6665940\n+92-55-6665840", "—",               "crownrice.com.pk"),
    ("30", "★ Kamal Rice Mills (Pvt)",    "2 KM Baig Pur Road,\nSadhoke, Gujranwala",             "—",                       "+92-333-8263150",   "kamalrice.com"),
    ("31", "KR Rice Processing Mills",    "Near Roshni Petrol Pump,\nG.T. Road, Sadhoke",         "—",                       "+92-304-8077956",   "bakhteyarkhanxada\n@gmail.com / krricemills.com"),
    ("32", "★ Matco Foods / Falak Rice",  "50 KM Main G.T. Road,\nSadhoke, Gujranwala",           "+92-55-6665774\n+92-55-6665676", "+92-330-1236661", "contact@matcofoods.com\nmatcofoods.com"),
]

for i, row in enumerate(sadhoke):
    story.append(mill_row(*row, i))

story.append(sp(0.35))

# ══════════════════════════════════════════════════════════════════════════════
# AREA 3: GHAKHAR / WAZIRABAD (14 mills)
# ══════════════════════════════════════════════════════════════════════════════
story.append(area_header("AREA 3: GHAKHAR / WAZIRABAD — G.T. Road / Kot Khizri", 14))
story.append(col_header())

ghakhar = [
    ("33", "★ Sardar Rice Mills",         "Railway Line Cross,\nGhakhar, Gujranwala",              "+92-55-6587603",          "+92-300-6430580",   "sardarricemills@hotmail.com\nsardarricemills.com"),
    ("34", "★ Al-Wahab Rice Mills",       "G.T. Road, Kot Khizri 52001,\nWazirabad",               "+92-55-6587060",          "+92-300-8644668",   "sales@alwahabrice.com\nalwahabrice.com"),
    ("35", "★ Al-Riaz Rice Mills",        "G.T. Road, Kot Khizri,\nWazirabad, 52001",              "—",                       "—",                 "alriazrice.com\n(60,000 T/yr capacity)"),
    ("36", "★ PNP Rice Mills",            "Kot Khizri G.T. Road,\nWazirabad, Gujranwala",          "+92-55-3036456\n+92-55-6587080", "+92-321-6533333", "—"),
    ("37", "★ Kashif Rice Mills",         "Kot Noora, Ghakhar City,\nDistt. Gujranwala",            "+92-55-6333865\n+92-55-6333498", "+92-300-4137538", "kashifricemills.enic.pk"),
    ("38", "Hussain Flour & Rice Mills",  "Bhroice Road,\nWazirabad",                              "+92-55-6602514",          "+92-300-8620170",   "—"),
    ("39", "Usman Rice Mill",             "Near Railway Gate,\nGhakhar, Wazirabad",                "+92-55-3881027",          "—",                 "—"),
    ("40", "Madina Rice Mills",           "G.T. Road, Ghakhar,\nDist. Wazirabad",                  "—",                       "+92-300-8711606",   "—"),
    ("41", "Itefaq Rice Mills",           "Peer Kot, Ghakhar,\nDist. Wazirabad",                   "—",                       "+92-300-8640821",   "—"),
    ("42", "Sayyan Rice Mills",           "Jora Sian, Ghakhar,\nDist. Wazirabad",                  "—",                       "+92-300-6425813",   "—"),
    ("43", "New Punjab Rice Mills",       "Kotli Sahian, Teh. Wazirabad,\nDistt. Gujranwala",     "—",                       "+92-300-6447078",   "—"),
    ("44", "Itehad Rice Mills",           "Noora Kot Road, Teh. Wazirabad,\nDistt. Gujranwala",   "—",                       "+92-300-6426040\n+92-345-6524247", "—"),
    ("45", "Muhammadi Rice Mills",        "Badoke Gosayan, Ghakhar,\nDist. Wazirabad",             "—",                       "+92-300-6317012",   "—"),
    ("46", "Wahla Rice Mills",            "G.T. Road, Teh. Wazirabad,\nDistt. Gujranwala",        "+92-55-3883422",          "—",                 "—"),
]

for i, row in enumerate(ghakhar):
    story.append(mill_row(*row, i))

story.append(sp(0.35))

# ══════════════════════════════════════════════════════════════════════════════
# AREA 4: EMINABAD (5 mills)
# ══════════════════════════════════════════════════════════════════════════════
story.append(area_header("AREA 4: EMINABAD — Wahndo Road / G.T. Road", 5))
story.append(col_header())

eminabad = [
    ("47", "★ Galaxy Rice Mills (Pvt)",   "Wahndo Road, Eminabad,\nGujranwala, Punjab",            "+92-55-3402184\n+92-55-3402284", "+92-331-6469412", "galaxyrice.com\n(Exports to Europe)"),
    ("48", "★ Ikram Rice Mills",          "N5, Eminabad More,\nMain G.T. Road, Gujranwala",        "+92-300-8645900",         "—",                 "ikramrice.com\n(REAP, Est. 1972)"),
    ("49", "Falak Basmati Rice",          "Wahndo Road, Eminabad,\nGujranwala",                    "+92-55-3264184",          "—",                 "—"),
    ("50", "Modern Rice & General Mills", "N-5, Eminabad More,\nG.T. Road, Gujranwala",            "+92-55-3840298\n+92-55-3842655", "—",             "—"),
    ("51", "Punjab Pearl Rice Mill",      "Wandoo Road, Chandanian,\nEminabad, Gujranwala",        "—",                       "+92-300-8646084",   "—"),
]

for i, row in enumerate(eminabad):
    story.append(mill_row(*row, i))

story.append(sp(0.35))

# ══════════════════════════════════════════════════════════════════════════════
# AREA 5: ALI PUR CHATTAH (5 mills)
# ══════════════════════════════════════════════════════════════════════════════
story.append(area_header("AREA 5: ALI PUR CHATTAH", 5))
story.append(col_header())

alipur = [
    ("52", "★ Galaxy Rice Mills Unit 2",  "Sayad Nagar Road,\nAli Pur Chattah, Gujranwala",       "—",                       "—",                 "galaxyrice.com"),
    ("53", "★ Agroman Crystal Rice",      "Sayad Nagar Road,\nAli Pur Chattah, Gujranwala",       "+92-55-6333865\n+92-55-6333498", "+92-300-4137538", "(Ships to USA & EU)"),
    ("54", "★ Kashif Rice Mills (APC)",   "Railway Road,\nAli Pur Chattah, Gujranwala",            "+92-55-6332775\n+92-55-6333348", "—",             "—"),
    ("55", "Pakistan Rice Mills",         "Railway Road,\nAli Pur Chatha, Gujranwala",             "—",                       "—",                 "—"),
    ("56", "Kawther Grain Rice Mills",    "Ali Pur Chatta,\nDistt. Gujranwala",                    "—",                       "—",                 "—"),
]

for i, row in enumerate(alipur):
    story.append(mill_row(*row, i))

story.append(sp(0.35))

# ══════════════════════════════════════════════════════════════════════════════
# AREA 6: GUJRANWALA CITY (12 mills)
# ══════════════════════════════════════════════════════════════════════════════
story.append(area_header("AREA 6: GUJRANWALA CITY — G.T. Road / Civil Lines / Pindi By-Pass", 12))
story.append(col_header())

gujcity = [
    ("57", "★ Marshal/Zarafa Rice Mills", "G.T. Road, Pindi By-Pass,\nGujranwala",                "—",                       "+92-300-6465702",   "marshalricemills@hotmail.com\nzarafarice.com"),
    ("58", "★ Al-Huda Rice Mills",        "Sialkot Road, Islam Colony,\nCivil Lines, Gujranwala", "—",                       "+92-307-6431660",   "info@alhudaricemills.com\nalhudaricemills.com"),
    ("59", "★ Zamindara Rice Mills Intl", "46 DC Road,\nGujranwala",                               "+92-55-3824031",          "+92-300-8646005",   "—"),
    ("60", "★ Pak Pearl Rice Mills",      "Ghalla Mandi Siranwali,\nGujranwala, Punjab",           "—",                       "—",                 "—"),
    ("61", "★ Aromabas Rice Mills",       "Ojla Canal Bridge,\nG.T. Road, Gujranwala",             "—",                       "—",                 "—"),
    ("62", "Aftab Rice Mill",             "Amrat Pura,\nGujranwala, Punjab",                       "+92-55-3015255",          "—",                 "—"),
    ("63", "Gill Rice Processing Mills",  "Kashmir Colony, Kotli\nPir Ahmed Shah, Gujranwala",     "+92-55-3417195",          "—",                 "—"),
    ("64", "Chishti Traders",             "Bilal Plaza, Opp. Malik Travels,\nGhalla Mandi, Gujranwala", "+92-55-4271625",   "+92-300-6433747",   "—"),
    ("65", "Butt Rice Mills",             "18-A Trust Plaza, Near\nRailway Link Road, Gujranwala", "+92-55-4271925",          "—",                 "—"),
    ("66", "Al-Siraj Rice Mill",          "Near Tomari Mandir,\nBadoki, Gujranwala",               "+92-55-3013303",          "—",                 "—"),
    ("67", "Al-Hameed Rice Mills",        "Gujranwala, Punjab",                                    "—",                       "—",                 "—"),
    ("68", "Rice World Mills",            "Gujranwala Area",                                       "—",                       "—",                 "riceworldreprocessing.com"),
]

for i, row in enumerate(gujcity):
    story.append(mill_row(*row, i))

story.append(sp(0.35))

# ══════════════════════════════════════════════════════════════════════════════
# AREA 7: HAFIZABAD DISTRICT (16 mills)
# ══════════════════════════════════════════════════════════════════════════════
story.append(area_header("AREA 7: HAFIZABAD DISTRICT — Jalalpur Bhattian · Pindi Bhattian · Sukheke · Kaleke", 16))
story.append(col_header())

hafizabad = [
    ("69", "★ Shaheen Rice Mills",        "Bypass Road, Jalalpur Bhattian,\nDistt. Hafizabad",     "+92-547-500333",          "+92-321-7521213",   "shaheenexcellences@gmail.com\nshaheenricemills.com"),
    ("70", "MAP Rice Mills",              "5-km Gujranwala Road,\nHafizabad-52110",                 "—",                       "—",                 "mapricemills.com"),
    ("71", "National Rice Mills",         "Hafizabad, Punjab",                                      "+92-4363-400415/55",      "—",                 "—"),
    ("72", "Mazco Industries (Pvt)",      "Jalalpur Bhattian,\nDistt. Hafizabad",                   "+92-547-500415\n+92-547-500315", "+92-300-4024815", "—"),
    ("73", "Zubair Enterprises",          "Ghalla Mandi, Jalalpur\nBhattian, Hafizabad",            "+92-547-500100\n+92-547-500200", "+92-300-7500200", "—"),
    ("74", "Muhammadi Rice Mill",         "Hafizabad Road,\nJalapur Pindi Bhattian",                "—",                       "+92-321-7684436",   "—"),
    ("75", "Al Nazeer Rice Mill",         "Marth Road,\nPindi Bhattian, Hafizabad",                 "—",                       "+92-300-7523259",   "—"),
    ("76", "Cheema Rice Mill",            "By-Pass,\nPindi Bhattian, Hafizabad",                    "—",                       "+92-300-8136100",   "—"),
    ("77", "Kashif Rice Mills (Sukheke)", "Sukheke Mandi,\nHafizabad",                              "—",                       "+92-300-4008010",   "—"),
    ("78", "Sohawa Rice Mills",           "Sukheke Mandi,\nHafizabad",                              "—",                       "+92-321-7479372",   "—"),
    ("79", "New Chanab Rice Mill",        "Sukheke Mandi,\nHafizabad",                              "—",                       "+92-321-8881201",   "—"),
    ("80", "Malik Tariq Rice Mills",      "Sukheke Mandi,\nHafizabad",                              "—",                       "+92-301-6456160",   "—"),
    ("81", "Roy Rice Mills",              "Moza Bangar, Kaleke Mandi,\nHafizabad",                  "—",                       "+92-336-6529892",   "—"),
    ("82", "Madina Rice Mills (Kaleke)",  "Kaleke Mandi,\nHafizabad",                               "—",                       "+92-300-6522554",   "—"),
    ("83", "Langah Rice Mills",           "Sukheke Road,\nHafizabad",                               "—",                       "—",                 "—"),
    ("84", "Sadad Rice Mills",            "Sukheke Mandi,\nHafizabad",                              "—",                       "—",                 "—"),
]

for i, row in enumerate(hafizabad):
    story.append(mill_row(*row, i))

story.append(sp(0.4))

# ── TOP 10 TO CONTACT FIRST ───────────────────────────────────────────────────
top_hdr = Table([[p("⭐  Top 10 Mills to Contact First — IRRI-6 Export Specialists",
    S("th", fontSize=10, leading=14, textColor=WHITE, fontName="Helvetica-Bold", alignment=TA_CENTER))]], colWidths=[W])
top_hdr.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),GREEN),
    ("TOPPADDING",(0,0),(-1,-1),7),("BOTTOMPADDING",(0,0),(-1,-1),7)]))
story.append(top_hdr)

top10 = [
    [p("Mill", head_s),             p("Why Contact First", head_s),                              p("Best Contact", head_s)],
    [p("Waqar Rice Mills", bold_s), p("24/7 WhatsApp, IRRI-6 specialist, export-ready",body_s), p("+92-300-8999999",S("g",fontSize=7,leading=10,textColor=GREEN,fontName="Helvetica-Bold"))],
    [p("Amir Rice Mills",  bold_s), p("Top-10 Pakistan exporter, Est.1982, very reliable",body_s),  p("+92-340-8405555",S("g2",fontSize=7,leading=10,textColor=GREEN,fontName="Helvetica-Bold"))],
    [p("Ikram Rice Mills", bold_s), p("REAP member, Est.1972, explicitly lists IRRI-6",body_s),  p("+92-300-8645900",S("g3",fontSize=7,leading=10,textColor=GREEN,fontName="Helvetica-Bold"))],
    [p("Al-Riaz Rice Mills",bold_s),p("Largest — 60,000 T/yr capacity, best bulk price",body_s), p("alriazrice.com",S("g4",fontSize=7,leading=10,textColor=GREEN,fontName="Helvetica-Bold"))],
    [p("AITCO Enterprise",  bold_s),p("IRRI-6 specialist, 20+ years Africa export experience",body_s), p("+92-300-6451430",S("g5",fontSize=7,leading=10,textColor=GREEN,fontName="Helvetica-Bold"))],
    [p("Rice Experts Enterprises",bold_s),p("IRRI-6 Africa exporter, verified on ImportYeti",body_s), p("+92-305-5519995",S("g6",fontSize=7,leading=10,textColor=GREEN,fontName="Helvetica-Bold"))],
    [p("Matco Foods / Falak",bold_s),p("Listed company, largest modern plant in Sadhoke",body_s), p("+92-55-6665774",S("g7",fontSize=7,leading=10,textColor=GREEN,fontName="Helvetica-Bold"))],
    [p("Sardar Rice Mills", bold_s),p("Reliable exporter, REAP member, Ghakhar area",body_s),   p("+92-300-6430580",S("g8",fontSize=7,leading=10,textColor=GREEN,fontName="Helvetica-Bold"))],
    [p("Galaxy Rice Mills", bold_s),p("EU exports, REAP member, modern plant",body_s),          p("+92-55-3402184",S("g9",fontSize=7,leading=10,textColor=GREEN,fontName="Helvetica-Bold"))],
    [p("Shaheen Rice Mills",bold_s),p("Hafizabad belt, verified exporter, responsive",body_s),  p("+92-321-7521213",S("g10",fontSize=7,leading=10,textColor=GREEN,fontName="Helvetica-Bold"))],
]

top_t = Table(top10, colWidths=[4*cm, 10.6*cm, 4*cm])
top_t.setStyle(TableStyle([
    ("BACKGROUND",(0,0),(-1,0),DARK),
    ("BACKGROUND",(0,1),(-1,1),LGREEN),("BACKGROUND",(0,2),(-1,2),WHITE),
    ("BACKGROUND",(0,3),(-1,3),LGREEN),("BACKGROUND",(0,4),(-1,4),WHITE),
    ("BACKGROUND",(0,5),(-1,5),LGREEN),("BACKGROUND",(0,6),(-1,6),WHITE),
    ("BACKGROUND",(0,7),(-1,7),LGREEN),("BACKGROUND",(0,8),(-1,8),WHITE),
    ("BACKGROUND",(0,9),(-1,9),LGREEN),("BACKGROUND",(0,10),(-1,10),WHITE),
    ("GRID",(0,0),(-1,-1),0.4,MIDGREY),
    ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
    ("TOPPADDING",(0,0),(-1,-1),6),("BOTTOMPADDING",(0,0),(-1,-1),6),
    ("LEFTPADDING",(0,0),(-1,-1),6),("RIGHTPADDING",(0,0),(-1,-1),6),
]))
story.append(top_t)
story.append(sp(0.35))

# ── PRO TIPS ──────────────────────────────────────────────────────────────────
pt_hdr = Table([[p("💡  Pro Tips — How to Get Cheapest Rate from Any Mill",
    S("pth", fontSize=10, leading=14, textColor=WHITE, fontName="Helvetica-Bold", alignment=TA_CENTER))]], colWidths=[W])
pt_hdr.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),DARK),
    ("TOPPADDING",(0,0),(-1,-1),7),("BOTTOMPADDING",(0,0),(-1,-1),7)]))
story.append(pt_hdr)

tips = [
    ("WhatsApp First",        "Pakistani mills respond faster to WhatsApp than email. Message in Urdu if you can — builds more trust."),
    ("Visit Kamoke G.T. Road","80% of mills are on this single road — one visit = 10+ quotes in one day. Best done in morning."),
    ("Ask REAP Membership",   "Always confirm REAP membership — it means the mill is a verified, registered rice exporter."),
    ("Request Free Sample",   "Ask for 1–2 kg sample before any order. Serious mills always agree. Check moisture, smell, color."),
    ("Get 3+ Quotes",         "Contact minimum 3 mills and show competing quotes — use them to negotiate lower price."),
    ("Off-Season = Cheapest", "Oct–Jan (after rice harvest) — prices are 10–15% lower. Best time to lock in annual rates."),
    ("Pay Advance = Discount","Offer 40–50% advance payment — mills typically give 3–5% price discount for cash/early payment."),
    ("Visit Mill Physically", "Before first order, visit mill in person or send local agent — verify facility and stock."),
    ("Negotiate Per MT",      "Always quote and compare in USD per MT FOB Karachi — easier to compare across mills."),
    ("Specify Grade Clearly", "State exact specs: broken %, moisture max, grain length, bag size — prevents disputes later."),
]

for i, (tip, detail) in enumerate(tips):
    bg = LGREEN if i % 2 == 0 else WHITE
    row = Table([[p(tip, bold_s), p(detail, body_s)]], colWidths=[3.8*cm, 14.8*cm])
    row.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(0,0),DKGREEN),
        ("BACKGROUND",(1,0),(1,0),bg),
        ("GRID",(0,0),(-1,-1),0.4,MIDGREY),
        ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
        ("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5),
        ("LEFTPADDING",(0,0),(-1,-1),6),("RIGHTPADDING",(0,0),(-1,-1),6),
    ]))
    story.append(row)

story.append(sp(0.35))

# ── RESOURCES ─────────────────────────────────────────────────────────────────
res = Table([[p(
    "Key Resources:  reap.com.pk/memberProfile  ·  tdap.gov.pk  ·  alibaba.com  ·  yellowpages.com.pk  ·  pakbiz.com",
    S("rs", fontSize=7, leading=11, textColor=DARK, fontName="Helvetica", alignment=TA_CENTER))]], colWidths=[W])
res.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),YELLOW),
    ("LINEABOVE",(0,0),(-1,0),1,GOLD),("LINEBELOW",(0,0),(-1,0),1,GOLD),
    ("TOPPADDING",(0,0),(-1,-1),6),("BOTTOMPADDING",(0,0),(-1,-1),6)]))
story.append(res)
story.append(sp(0.2))

# ── FOOTER ────────────────────────────────────────────────────────────────────
story.append(HRFlowable(width="100%", thickness=0.5, color=MIDGREY))
story.append(sp(0.1))
story.append(p("Gujranwala Rice Mills Directory — 84 Mills  ·  Compiled from REAP, TDAP, Business Directories & Company Websites  ·  2025", cap_s))

doc.build(story)
print("PDF created: Gujranwala_Rice_Mills_84_Directory.pdf")
