from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm, mm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, HRFlowable
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT

GREEN   = colors.HexColor("#1a7a3c")
DARK    = colors.HexColor("#1a2e1a")
GOLD    = colors.HexColor("#c8a200")
WHITE   = colors.white
GREY    = colors.HexColor("#f0f0f0")
LGREEN  = colors.HexColor("#e8f5ec")
MIDGREY = colors.HexColor("#cccccc")
YELLOW  = colors.HexColor("#fffbea")
DKGREEN = colors.HexColor("#d4edda")
NAVY    = colors.HexColor("#0d2147")
RED     = colors.HexColor("#c0392b")

doc = SimpleDocTemplate(
    "/home/user/Usama-New/Sindh_IRRI6_Rice_Mills_Directory.pdf",
    pagesize=A4,
    rightMargin=1.2*cm, leftMargin=1.2*cm,
    topMargin=1.2*cm, bottomMargin=1.2*cm
)

W = 18.6*cm

def S(name, **kw):
    base = dict(fontName="Helvetica", fontSize=8, leading=11, textColor=DARK, alignment=TA_LEFT)
    base.update(kw)
    return ParagraphStyle(name, **base)

title_s  = S("t",  fontSize=17, leading=22, textColor=WHITE, fontName="Helvetica-Bold", alignment=TA_CENTER)
sub_s    = S("s",  fontSize=9,  leading=13, textColor=GOLD,  fontName="Helvetica-Bold", alignment=TA_CENTER)
area_s   = S("a",  fontSize=10, leading=14, textColor=WHITE, fontName="Helvetica-Bold", alignment=TA_LEFT)
head_s   = S("h",  fontSize=8,  leading=11, textColor=WHITE, fontName="Helvetica-Bold", alignment=TA_CENTER)
body_s   = S("b",  fontSize=7,  leading=10, textColor=DARK,  fontName="Helvetica")
bold_s   = S("bo", fontSize=7,  leading=10, textColor=DARK,  fontName="Helvetica-Bold")
star_s   = S("st", fontSize=7,  leading=10, textColor=GREEN, fontName="Helvetica-Bold")
num_s    = S("n",  fontSize=9,  leading=12, textColor=WHITE, fontName="Helvetica-Bold", alignment=TA_CENTER)
cap_s    = S("c",  fontSize=7,  leading=10, textColor=colors.HexColor("#666"), fontName="Helvetica-Oblique", alignment=TA_CENTER)
stat_n   = S("sn", fontSize=14, leading=18, textColor=GREEN, fontName="Helvetica-Bold", alignment=TA_CENTER)
stat_l   = S("sl", fontSize=7,  leading=10, textColor=DARK,  fontName="Helvetica",      alignment=TA_CENTER)
gold_s   = S("gs", fontSize=7,  leading=10, textColor=GOLD,  fontName="Helvetica-Bold")
red_s    = S("rs", fontSize=7,  leading=10, textColor=RED,   fontName="Helvetica-Bold")

def p(txt, style=body_s): return Paragraph(str(txt), style)
def sp(h=0.25): return Spacer(1, h*cm)

COL_W = [0.6*cm, 3.6*cm, 3.8*cm, 3.0*cm, 3.0*cm, 4.6*cm]

story = []

# ── HEADER ────────────────────────────────────────────────────────────────────
h = Table([[p("🌾  Sindh IRRI-6 Rice Mills & Exporters Directory", title_s)]], colWidths=[W])
h.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),GREEN),
    ("TOPPADDING",(0,0),(-1,-1),11),("BOTTOMPADDING",(0,0),(-1,-1),9),
    ("LEFTPADDING",(0,0),(-1,-1),8),("RIGHTPADDING",(0,0),(-1,-1),8)]))
story.append(h)

s = Table([[p("Karachi · Hyderabad · Larkana · Sukkur · Badin · Tando Muhammad Khan · Nawabshah — Longest Grain IRRI-6 White Rice", sub_s)]], colWidths=[W])
s.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),DARK),
    ("TOPPADDING",(0,0),(-1,-1),6),("BOTTOMPADDING",(0,0),(-1,-1),6)]))
story.append(s)
story.append(sp(0.3))

# ── STATS BAR ─────────────────────────────────────────────────────────────────
stats = Table([
    [p("35",stat_n),    p("293",stat_n),     p("50%+",stat_n),    p("6.0mm+",stat_n),  p("Karachi",stat_n)],
    [p("Exporters\nListed",stat_l), p("Mills in\nSindh",stat_l),
     p("of Pakistan's\nRice Exports",stat_l), p("IRRI-6\nGrain Length",stat_l), p("Main\nExport Port",stat_l)],
], colWidths=[3.72*cm]*5)
stats.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),GREY),
    ("GRID",(0,0),(-1,-1),0.4,MIDGREY),
    ("TOPPADDING",(0,0),(-1,-1),6),("BOTTOMPADDING",(0,0),(-1,-1),5)]))
story.append(stats)
story.append(sp(0.3))

# ── LEGEND ────────────────────────────────────────────────────────────────────
leg = Table([[p("★ = REAP Member / Verified Exporter   |   All phone numbers WhatsApp-enabled unless stated   |   Source: REAP, TDAP, irri6.com, company websites",
    S("lg", fontSize=7, leading=10, textColor=DARK, fontName="Helvetica-Oblique", alignment=TA_CENTER))]], colWidths=[W])
leg.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),YELLOW),
    ("LINEABOVE",(0,0),(-1,0),0.8,GOLD),("LINEBELOW",(0,0),(-1,0),0.8,GOLD),
    ("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5)]))
story.append(leg)
story.append(sp(0.3))

def area_header(title, count):
    t = Table([[
        p(f"  📍 {title}", area_s),
        p(f"{count} Companies", S("ac", fontSize=9, leading=13, textColor=GOLD, fontName="Helvetica-Bold", alignment=TA_CENTER))
    ]], colWidths=[15.2*cm, 3.4*cm])
    t.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),DARK),
        ("TOPPADDING",(0,0),(-1,-1),6),("BOTTOMPADDING",(0,0),(-1,-1),6),
        ("LEFTPADDING",(0,0),(-1,-1),6),("RIGHTPADDING",(0,0),(-1,-1),6)]))
    return t

def col_header():
    t = Table([[
        p("#",head_s), p("Company Name",head_s), p("Address",head_s),
        p("Phone",head_s), p("WhatsApp",head_s), p("Email / Website",head_s)
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
    ns = star_s if star else bold_s
    t = Table([[
        p(num, num_s), p(name, ns), p(addr, body_s),
        p(phone, body_s), p(wa, body_s), p(contact, body_s),
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
# AREA 1: KARACHI (25 companies)
# ══════════════════════════════════════════════════════════════════════════════
story.append(area_header("AREA 1: KARACHI — SITE · Port Qasim · Clifton · I.I. Chundrigar Road", 25))
story.append(col_header())

karachi = [
    ("1",  "★ Pak Rice Mill /\nAl Habib Industries",
     "Rice Trade Center, Dandia\nBazar, Opp. City Court, Karachi\nFactory: Plot F22/A, SITE",
     "+92-21-32767744\n+92-21-32767755",
     "+92-321-3826632\n+92-300-2524388",
     "info@pakrice.pk\npakrice.pk | pakricemill.com\nREAP ID: 280 | ISO 22000"),

    ("2",  "★ HAS Rice Pakistan",
     "Suite 403, Balad Trade Centre,\nAlamagir Road, Bahadurabad,\nKarachi",
     "+92-21-34127733",
     "+92-321-3343343",
     "omair@hasrice.com\nhasrice.com | irri6.com\nMills: Jacobabad, Badin"),

    ("3",  "★ Asif Rice Mills",
     "48-C, Khayaban-e-Jami,\nDHA Phase VII, Karachi\nMill: Port Qasim, Karachi",
     "+92-21-35397706\n+92-21-35397710",
     "+92-333-3224510",
     "info@asifrice.com\nasifrice.com\nREAP ID: 223 | Gulfood 2025"),

    ("4",  "★ AA Rice Processing Mills",
     "504, 5th Floor, Trade Avenue,\nHasrat Mohani Rd,\nKarachi 74000",
     "+92-21-32424134\n+92-21-32424135",
     "+92-335-2115600",
     "info@aaricemills.com\nexportaaricemill@gmail.com\naaricemills.com | Est.1980"),

    ("5",  "★ Jasons Commodities",
     "F-8/1, Block 7, Clifton,\nKarachi\nMill: E-92, Port Qasim",
     "+92-21-99217321\n+92-21-99217322",
     "+92-300-1481489",
     "jasonscommodities.com\nREAP ID: 115 | Est.1985\nTDAP Registered"),

    ("6",  "★ Hina Exports",
     "C-84, Main Estate Avenue,\nGulabi, S.I.T.E., Karachi",
     "+92-21-32594090\n+92-21-32594092",
     "+92-301-8270333\n+92-345-8270333",
     "REAP ID: 16\nEx-Chairman Sindh REAP\nreap.com.pk/memberDetails/16"),

    ("7",  "★ Al Noor Rice Traders",
     "S-119, Mauripur Road,\nGulbai, S.I.T.E., Karachi",
     "+92-21-32575576",
     "+92-302-8233778\n+92-335-0256667",
     "alnoorricetraders@gmail.com\nalnoor.com.pk\nREAP ID: 126"),

    ("8",  "★ Al Asad Rice Mills",
     "Office 609, Sharjah Trade\nCentre, New Challi,\nKarachi 74000",
     "+92-21-32401151\n+92-21-32401153",
     "—",
     "info@alasadricemills.com\nalasadricemills.com\nREAP ID: 105"),

    ("9",  "★ Siraj Corporation",
     "Room 104, 1st Floor,\nAl-Rahmat Trade Centre,\nOpp. City Court, Karachi",
     "+92-21-32727931\n+92-21-32728507",
     "—",
     "REAP ID: 128\nreap.com.pk/memberDetails/128"),

    ("10", "★ GEP Rice Mills\n(Global Exports Pakistan)",
     "Office 6, 1st Floor,\nYousaf Ali Bhai Bldg,\nNew Challi, Karachi",
     "+92-21-32639111\n+92-21-32633134",
     "+92-300-8235151",
     "gepricemills.com\nREAP ID: 284\nIRRI-6 & Parboiled"),

    ("11", "★ Data Rice Mills (Pvt) Ltd",
     "Suite 514, 5th Floor,\nProgressive Plaza,\nBeaumont Road, PIDC Karachi",
     "—",
     "+92-332-2245500",
     "info@datagroup.com.pk\ndatagroup.com.pk\nREAP ID: 1535 | Est.1970"),

    ("12", "★ Amir Rice Export & Import",
     "204, Progressive Plaza,\nBeaumont Road,\nCivil Lines, Karachi",
     "+92-21-35221185\n+92-21-35221186",
     "—",
     "info@amirriceexport.com\namirriceexport.com\nREAP ID: 54"),

    ("13", "★ Pacific Rice Mills",
     "38-L, Block-6, PECHS, Karachi\nMill: E-70, NWIZ, Port Qasim\nField: Badin District",
     "+92-21-34523175",
     "—",
     "exports@pacificricemills.com.pk\npacificricemills.com.pk\nEst. 1994 | Badin Mill"),

    ("14", "★ Habib Rice Products Ltd",
     "UBL Building,\nI.I. Chundrigar Road,\nKarachi",
     "+92-853-363963\n+92-853-363964",
     "+92-333-2125966",
     "info@habibriceproducts.com\nhabibriceproducts.com\nREAP ID: 171"),

    ("15", "★ RKS Rice Exporters",
     "Office 615, Poona Wala\nTrade Tower, City Court,\nKarachi",
     "—",
     "—",
     "info@rksriceexporters.com\nrksriceexporters.com\nREAP Member"),

    ("16", "★ Haji Khushi Muhammad & Co",
     "Karachi\n(REAP Managing\nCommittee Member)",
     "—",
     "—",
     "REAP Managing Committee\nSindh Representative\nContact via REAP"),

    ("17", "★ M/S Data Global Commodities",
     "Office 1, 29-C Rahat\nCommercial, Lane 1,\nDHA Phase 6, Karachi",
     "—",
     "+92-300-2576451",
     "Pakistan Trade Portal\nIRRI-6 Exporter"),

    ("18", "Orient Rice Mills Ltd",
     "511, Poona Wala Trade Tower,\nChabba Street,\nOpp. City Court, Karachi",
     "—",
     "—",
     "Karachi Rice Directory\nIRRI-6 Exporter"),

    ("19", "Taha Rice Mills (Pvt) Ltd",
     "5th Floor, Spotlit Chamber,\nI.I. Chundrigar Road,\nKarachi",
     "—",
     "—",
     "Karachi Rice Directory\nIRRI-6 Exporter"),

    ("20", "Rice Millers Consortium",
     "1-2-5, Court Chambers,\nDandia Bazar,\nOpp. City Court, Karachi",
     "—",
     "—",
     "Karachi Rice Trade\nDirectory"),

    ("21", "Rice International (Pvt) Ltd",
     "Office 1203, 12th Floor,\nEmerald Tower, Block 5,\nClifton, Karachi",
     "—",
     "—",
     "Karachi Rice Exporter\nDirectory"),

    ("22", "AITCO Enterprise",
     "Karachi Office\n(Also listed Gujranwala)",
     "—",
     "+92-300-6451430",
     "export.aitco.enterprise\n@gmail.com\nIRRI-6 Africa Specialist"),

    ("23", "Karim Rice Processing Mills",
     "Karachi, Sindh",
     "—",
     "—",
     "Yellow Pages Pakistan\nRice Mills Karachi"),

    ("24", "H.M. Rice Mill",
     "Apt 104, Prime Beach View,\nClifton Block 4, Karachi",
     "—",
     "—",
     "Yellow Pages Pakistan\nRice Mills Karachi"),

    ("25", "Latif Rice Mill",
     "Room 1, 4th Floor,\nDean Arcade, Block-8,\nClifton, Karachi",
     "—",
     "—",
     "Yellow Pages Pakistan\nRice Mills Karachi"),
]

for i, row in enumerate(karachi):
    story.append(mill_row(*row, i))

story.append(sp(0.35))

# ══════════════════════════════════════════════════════════════════════════════
# AREA 2: HYDERABAD / LOWER SINDH
# ══════════════════════════════════════════════════════════════════════════════
story.append(area_header("AREA 2: HYDERABAD · KOTRI · BADIN — Lower Sindh", 5))
story.append(col_header())

hyderabad = [
    ("26", "★ Harmain Global",
     "A/2786, Alam Chand Street,\nTilak Incline,\nHyderabad, Sindh",
     "+92-22-6119540",
     "+92-333-2095256\n+92-345-3629580",
     "harmainpk92@yahoo.com\nharmainglobal.com\nEst. 1985 | IRRI-6"),

    ("27", "★ Sindh Punjab Traders\n& Rice Mills",
     "Suite 217, Hussain Trade\nCentre, New Challi, Karachi\nMill: Plot E-7, SITE, Kotri",
     "+92-21-32212305\n+92-21-32212307",
     "+92-333-2201424\n+92-332-2541217",
     "info@spt-pk.com\nbadlani.om@gmail.com\nspt-pk.com | Gulfood 2026"),

    ("28", "HAS Rice — Badin Mill",
     "Survey 182, Talhar,\nHyderabad-Badin Road,\nDistrict Badin, Sindh",
     "See HAS Rice (No.2)",
     "+92-321-3343343",
     "omair@hasrice.com\nhasrice.com\n(Badin processing unit)"),

    ("29", "Pacific Rice — Badin Unit",
     "Survey 182, Talhar,\nHyderabad-Badin Road,\nDistrict Badin, Sindh",
     "+92-21-34523175",
     "—",
     "exports@pacificricemills\n.com.pk\n(Badin field unit)"),

    ("30", "Awami Rice Mill",
     "Village Khorwah, Taluka\nGolarchi, RTO Hyderabad,\nSindh",
     "—",
     "—",
     "Hyderabad RTO District\nSindh Rice Network"),
]

for i, row in enumerate(hyderabad):
    story.append(mill_row(*row, i))

story.append(sp(0.35))

# ══════════════════════════════════════════════════════════════════════════════
# AREA 3: UPPER SINDH (Larkana / Shikarpur / Sukkur / Jacobabad)
# ══════════════════════════════════════════════════════════════════════════════
story.append(area_header("AREA 3: LARKANA · SHIKARPUR · SUKKUR · JACOBABAD — Upper Sindh", 3))
story.append(col_header())

upper = [
    ("31", "★ Omni Private Ltd\n(Shikarpur Rice Mills)",
     "Karachi Office: 1st Floor,\nBlock-2, Hockey Club Bldg,\nLiaquat Barracks, Karachi",
     "+92-21-35655131\n+92-21-35655134",
     "+92-21-345657781",
     "omnigroup.com.pk\nUAN: +92-21-111-666-447\nMill: Shikarpur, Sindh"),

    ("32", "★ Asif Rice — Shahdadkot",
     "Near Railway Line,\nShahdadkot,\nDistrict Larkana, Sindh",
     "+92-21-35397706",
     "+92-333-3224510",
     "info@asifrice.com\nasifrice.com\n(Larkana production unit)"),

    ("33", "★ Pak Rice / Al Habib —\nJacobabad & TMK Units",
     "Mills: Jacobabad &\nTando Muhammad Khan,\nSindh",
     "+92-21-32767744",
     "+92-321-3826632",
     "info@pakrice.pk\npakrice.pk\n(Upper Sindh units)"),
]

for i, row in enumerate(upper):
    story.append(mill_row(*row, i))

story.append(sp(0.35))

# ══════════════════════════════════════════════════════════════════════════════
# AREA 4: NAWABSHAH / SHAHEED BENAZIRABAD
# ══════════════════════════════════════════════════════════════════════════════
story.append(area_header("AREA 4: NAWABSHAH · SHAHEED BENAZIRABAD DISTRICT", 2))
story.append(col_header())

nawabshah = [
    ("34", "Rice Mills of Shaheed\nBenazirabad (7 Mills)",
     "SITE Nawabshah &\nSSIC Estate, Nawabshah,\nSindh",
     "—",
     "—",
     "Contact via SBCCI:\nsbcci.org.pk\n7 registered rice mills"),

    ("35", "REAP Karachi\nRegional Office",
     "Office 707, 7th Floor,\nBusiness & Finance Centre,\nI.I. Chundrigar Rd, Karachi",
     "+92-21-99217321\n+92-21-99217322",
     "—",
     "reap.com.pk/memberProfile\nUAN: +92-21-111-555-992\nAll Sindh members"),
]

for i, row in enumerate(nawabshah):
    story.append(mill_row(*row, i))

story.append(sp(0.4))

# ── TOP 8 TO CONTACT FIRST ────────────────────────────────────────────────────
top_hdr = Table([[p("⭐  Top 8 Sindh Suppliers — Contact These First for IRRI-6 Longest Grain",
    S("th", fontSize=10, leading=14, textColor=WHITE, fontName="Helvetica-Bold", alignment=TA_CENTER))]], colWidths=[W])
top_hdr.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),GREEN),
    ("TOPPADDING",(0,0),(-1,-1),7),("BOTTOMPADDING",(0,0),(-1,-1),7)]))
story.append(top_hdr)

top8 = [
    [p("Company", head_s),           p("Why Best", head_s),                                      p("Best Contact", head_s)],
    [p("HAS Rice Pakistan", bold_s), p("Dedicated IRRI-6 specialist — owns irri6.com, mills in Jacobabad & Badin", body_s), p("+92-321-3343343\nomair@hasrice.com", star_s)],
    [p("Pak Rice / Al Habib", bold_s),p("ISO 22000 certified, REAP member, largest multi-mill Sindh operator", body_s), p("+92-321-3826632\ninfo@pakrice.pk", star_s)],
    [p("Asif Rice Mills", bold_s),   p("Port Qasim mill — direct port access, Gulfood 2025 exhibitor", body_s),          p("+92-333-3224510\ninfo@asifrice.com", star_s)],
    [p("AA Rice Mills", bold_s),     p("Est. 1980, exports to Africa Middle East Europe — very experienced", body_s),     p("+92-335-2115600\ninfo@aaricemills.com", star_s)],
    [p("Jasons Commodities", bold_s),p("Est. 1985, REAP ID 115, Port Qasim plant, TDAP registered", body_s),             p("+92-300-1481489\njasonscommodities.com", star_s)],
    [p("Sindh Punjab Traders", bold_s),p("Kotri mill near Hyderabad, Gulfood 2026 exhibitor, active exporter", body_s), p("+92-333-2201424\ninfo@spt-pk.com", star_s)],
    [p("Harmain Global", bold_s),    p("Hyderabad — Est. 1985, between farms and port, IRRI-6 specialist", body_s),      p("+92-333-2095256\nharmainglobal.com", star_s)],
    [p("Omni (Shikarpur Mills)", bold_s),p("One of Pakistan's largest mills, heart of upper Sindh IRRI-6 belt", body_s), p("+92-21-35655131\nomnigroup.com.pk", star_s)],
]

top_t = Table(top8, colWidths=[4*cm, 10.1*cm, 4.5*cm])
top_t.setStyle(TableStyle([
    ("BACKGROUND",(0,0),(-1,0),DARK),
    ("BACKGROUND",(0,1),(-1,1),LGREEN),("BACKGROUND",(0,2),(-1,2),WHITE),
    ("BACKGROUND",(0,3),(-1,3),LGREEN),("BACKGROUND",(0,4),(-1,4),WHITE),
    ("BACKGROUND",(0,5),(-1,5),LGREEN),("BACKGROUND",(0,6),(-1,6),WHITE),
    ("BACKGROUND",(0,7),(-1,7),LGREEN),("BACKGROUND",(0,8),(-1,8),WHITE),
    ("GRID",(0,0),(-1,-1),0.4,MIDGREY),
    ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
    ("TOPPADDING",(0,0),(-1,-1),6),("BOTTOMPADDING",(0,0),(-1,-1),6),
    ("LEFTPADDING",(0,0),(-1,-1),6),("RIGHTPADDING",(0,0),(-1,-1),6),
]))
story.append(top_t)
story.append(sp(0.35))

# ── IRRI-6 SPECS BOX ─────────────────────────────────────────────────────────
spec_hdr = Table([[p("📋  IRRI-6 Longest Grain Specifications — What to Quote to Supplier",
    S("sh", fontSize=10, leading=14, textColor=WHITE, fontName="Helvetica-Bold", alignment=TA_CENTER))]], colWidths=[W])
spec_hdr.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),DARK),
    ("TOPPADDING",(0,0),(-1,-1),7),("BOTTOMPADDING",(0,0),(-1,-1),7)]))
story.append(spec_hdr)

specs = [
    [p("Spec", head_s),              p("DRC Export Standard", head_s),  p("Premium Grade", head_s)],
    [p("Variety", bold_s),           p("IRRI-6 Long Grain White", body_s), p("IRRI-6 Long Grain", body_s)],
    [p("Grain Length", bold_s),      p("Min 6.0 mm", body_s),           p("6.2 mm+", body_s)],
    [p("Broken %", bold_s),          p("25% broken (mass market)", body_s), p("5% broken (premium)", body_s)],
    [p("Moisture", bold_s),          p("Max 13.5%", body_s),            p("Max 12.5%", body_s)],
    [p("Foreign Matter", bold_s),    p("Max 0.1%", body_s),             p("Max 0.05%", body_s)],
    [p("Damaged Grains", bold_s),    p("Max 2%", body_s),               p("Max 1%", body_s)],
    [p("Color", bold_s),             p("Bright white, double polished", body_s), p("Extra white polished", body_s)],
    [p("Packing", bold_s),           p("50kg PP bags with PE liner", body_s), p("25kg or 50kg", body_s)],
    [p("Label Language", bold_s),    p("French (mandatory for DRC)", body_s), p("French + English", body_s)],
    [p("FOB Price (approx)", bold_s),p("~$380–400 / MT", body_s),       p("~$420–445 / MT", body_s)],
]

spec_t = Table(specs, colWidths=[4*cm, 7.3*cm, 7.3*cm])
spec_t.setStyle(TableStyle([
    ("BACKGROUND",(0,0),(-1,0),colors.HexColor("#2d5a3d")),
    ("BACKGROUND",(0,1),(-1,1),LGREEN),("BACKGROUND",(0,2),(-1,2),WHITE),
    ("BACKGROUND",(0,3),(-1,3),LGREEN),("BACKGROUND",(0,4),(-1,4),WHITE),
    ("BACKGROUND",(0,5),(-1,5),LGREEN),("BACKGROUND",(0,6),(-1,6),WHITE),
    ("BACKGROUND",(0,7),(-1,7),LGREEN),("BACKGROUND",(0,8),(-1,8),WHITE),
    ("BACKGROUND",(0,9),(-1,9),LGREEN),("BACKGROUND",(0,10),(-1,10),WHITE),
    ("BACKGROUND",(0,0),(0,-1),DKGREEN),
    ("FONTNAME",(0,0),(0,-1),"Helvetica-Bold"),
    ("GRID",(0,0),(-1,-1),0.4,MIDGREY),
    ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
    ("TOPPADDING",(0,0),(-1,-1),6),("BOTTOMPADDING",(0,0),(-1,-1),6),
    ("LEFTPADDING",(0,0),(-1,-1),6),("RIGHTPADDING",(0,0),(-1,-1),6),
]))
story.append(spec_t)
story.append(sp(0.35))

# ── KEY RESOURCES ─────────────────────────────────────────────────────────────
res = Table([[p(
    "Key Resources:  reap.com.pk  ·  irri6.com  ·  tdap.gov.pk  ·  pakrice.pk  ·  hasrice.com  ·  asifrice.com",
    S("rs", fontSize=7, leading=11, textColor=DARK, fontName="Helvetica", alignment=TA_CENTER))]], colWidths=[W])
res.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),YELLOW),
    ("LINEABOVE",(0,0),(-1,0),1,GOLD),("LINEBELOW",(0,0),(-1,0),1,GOLD),
    ("TOPPADDING",(0,0),(-1,-1),6),("BOTTOMPADDING",(0,0),(-1,-1),6)]))
story.append(res)
story.append(sp(0.2))

story.append(HRFlowable(width="100%", thickness=0.5, color=MIDGREY))
story.append(sp(0.1))
story.append(p("Sindh IRRI-6 Rice Mills Directory — 35 Companies  ·  Compiled from REAP, TDAP, irri6.com, Company Websites  ·  2025", cap_s))

doc.build(story)
print("PDF created: Sindh_IRRI6_Rice_Mills_Directory.pdf")
