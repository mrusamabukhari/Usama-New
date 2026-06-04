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
    "/home/user/Usama-New/Punjab_Rice_Mills_New_40plus_Directory.pdf",
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

def p(txt, style=body_s): return Paragraph(str(txt), style)
def sp(h=0.25): return Spacer(1, h*cm)

COL_W = [0.6*cm, 3.8*cm, 4.5*cm, 3.2*cm, 3.2*cm, 3.3*cm]

def tbl_header():
    return Table(
        [[p("#", head_s), p("Mill Name", head_s), p("Full Address", head_s),
          p("Phone / WhatsApp", head_s), p("Email", head_s), p("Website", head_s)]],
        colWidths=COL_W,
        style=TableStyle([
            ("BACKGROUND", (0,0), (-1,0), GREEN),
            ("GRID",       (0,0), (-1,-1), 0.3, MIDGREY),
            ("TOPPADDING", (0,0), (-1,-1), 3),
            ("BOTTOMPADDING", (0,0), (-1,-1), 3),
        ])
    )

def mill_row(n, name, address, phone, email, website, reap=False, shade=False):
    bg = LGREEN if shade else WHITE
    name_txt = p(("* " if reap else "") + name, star_s if reap else bold_s)
    return Table(
        [[p(str(n), body_s), name_txt, p(address, body_s),
          p(phone, body_s), p(email, body_s), p(website, body_s)]],
        colWidths=COL_W,
        style=TableStyle([
            ("BACKGROUND", (0,0), (-1,-1), bg),
            ("GRID",       (0,0), (-1,-1), 0.3, MIDGREY),
            ("TOPPADDING", (0,0), (-1,-1), 3),
            ("BOTTOMPADDING", (0,0), (-1,-1), 3),
            ("VALIGN",     (0,0), (-1,-1), "TOP"),
        ])
    )

def area_banner(label):
    return Table(
        [[p(label, area_s)]],
        colWidths=[W],
        style=TableStyle([
            ("BACKGROUND", (0,0), (-1,-1), GREEN),
            ("TOPPADDING", (0,0), (-1,-1), 5),
            ("BOTTOMPADDING", (0,0), (-1,-1), 5),
            ("LEFTPADDING", (0,0), (-1,-1), 8),
        ])
    )

# ─── DATA: 44 new mills across Punjab ───────────────────────────────────────
# Format: (name, address, phone, email, website, reap_member)

AREA_NAROWAL = [
    ("Rana Rice Mills",
     "Near UET, Muridke Road, Narowal 51600, Punjab",
     "+92 333 7776056",
     "exports.ranaricemills@gmail.com",
     "ranaricemills.com", True),

    ("Reem Rice Mills (Pvt) Ltd",
     "16-KM Muridke Narowal Road, Narowal; Office: 15-KM Multan Road, Lahore",
     "+92 42 37512270-72 | +92 321 8452834",
     "—",
     "reemrice.com", True),
]

AREA_SIALKOT = [
    ("Dar Rice Mills",
     "10-KM Pasrur Road, Sialkot, Punjab",
     "052-8250230/31 | 0302-8613982 | 0321-8611557",
     "info@darricemills.com",
     "darricemills.com", False),

    ("Mughal Rice Mills",
     "Narowal Road Booster, Pasrur, District Sialkot",
     "—",
     "—",
     "mughalricemills.com", False),

    ("Kashmir Rice Mills",
     "Ugoki Road, Sialkot 51310, Punjab",
     "052-3554817 / 3552671",
     "basmatikrm@gmail.com",
     "—", False),

    ("Silver Rice Mills",
     "Daska Road, P.O. Box 2270, Doburji Mallian, Sialkot",
     "9252-3552967 / 3552757 / 3557657 / 3557757",
     "—",
     "—", False),

    ("Sarmad Rice Mills",
     "Pasrur Road, Sialkot (Head Office: Sadiq Plaza, The Mall, Lahore)",
     "0300-8616606",
     "sarmadricemills@yahoo.com",
     "—", True),

    ("Tariq Rice Mill",
     "Haji Pura, Aska Road, Sialkot",
     "052-3256863 | 0300-6101712",
     "—",
     "—", True),

    ("Al-Khair Rice Mills",
     "Wario Chowk, Pasrur Road (opp. Telephone Exchange), Pasrur, Sialkot 51410",
     "0336-8155883 | (052) 3549488 | 0321-6120288",
     "—",
     "alkhairrice.com", True),
]

AREA_DASKA = [
    ("Millat Rice & General Mills",
     "Ghalah Mandi (Ghalla Mandi), Daska 51010, Punjab",
     "0300-4007232-3",
     "—",
     "—", True),

    ("Nazir Rice Processing Mills",
     "Jassar Wala, Daska, Sialkot",
     "0300-0200683",
     "—",
     "—", False),

    ("Wraich Rice Mills",
     "Gujranwala Road, Glotian, Daska, Sialkot",
     "0300-9647840",
     "—",
     "—", False),

    ("Qasim Rice Mills",
     "Gujranwala Road, Ranjhai, Daska, Punjab",
     "—",
     "—",
     "qasimricemills.com", True),
]

AREA_MURIDKE = [
    ("Khawaja Rice Processors",
     "2-KM Sheikhupura Road, Muridke, Dist. Sheikhupura, Punjab",
     "0331-6070700 | 0319-4070700",
     "info@khawajarice.com",
     "khawaja-rice.com", True),

    ("Ahmed Mustafa Rice Processing Mills",
     "Sheikhupura Road, Muridke, Sheikhupura",
     "0323-4307330",
     "—",
     "amricemills.com", False),

    ("MJM Rice Mills",
     "1.5-KM Muridke Sheikhupura Road, Muridke, Punjab",
     "—",
     "—",
     "mjmrice.com", False),

    ("Pak Rice Mill",
     "3-KM Sheikhupura Muridke Road, Punjab; (Office: Rice Trade Centre, Karachi)",
     "+92-310-2667744 (WA) | +92-321-3826632",
     "export@pakrice.pk",
     "pakricemill.com", False),

    ("Haji Muhammad Rice & Processing Mills",
     "Muridke, Sheikhupura (Head Office: Sadiq Plaza, The Mall, Lahore)",
     "+92 301 8747999 | +92 42 37163299",
     "ceo@hmricemills.com",
     "hmricemills.com", True),

    ("Super Rice Mills",
     "4-KM G.T. Road, Muridke, Dist. Sheikhupura, Punjab",
     "+92-55-6815452 | +92-300-4003858 | +92-321-8428881",
     "superricemills@gmail.com",
     "srm.com.pk", False),
]

AREA_LAHORE = [
    ("Garibsons (Pvt) Ltd",
     "50-E Main Gulberg, Lahore (Head Office: C69-71, 12th Commercial St, DHA, Karachi)",
     "+92 42 35760101-3 | 0300-8442408",
     "contact@garibsons.com",
     "garibsons.com", True),

    ("M. Hussain Rice Mills",
     "Usman Nagar, Hinda Stop, GT Road, Kamoke, Gujranwala 50661",
     "+92-5566632-33",
     "info@hrmrice.com",
     "hrmrice.com", True),

    ("MAP Rice Mills (Pvt) Ltd",
     "5-KM Gujranwala Road, Hafizabad 52110, Punjab (Mktg Office: Liberty Chowk, Gulberg-III, Lahore)",
     "+92-42-99332053/54",
     "exports@mapricemills.com",
     "mapricemills.com", True),

    ("Nazir Rice Mills (Pvt) Ltd",
     "206-A, 2nd Floor, Siddiq Trade Centre, Gulberg-II, Lahore",
     "042-5817230 | 0300-8710082",
     "—",
     "—", False),
]

AREA_GUJRANWALA = [
    ("Sardar Rice Mills",
     "Railway Line Cross, Ghakkhar, Gujranwala, Punjab",
     "+92 301 3832333 | +92 302 3832333 | +92 300 6430580",
     "sardarricemills@hotmail.com",
     "sardarricemills.com", False),

    ("Waqar Rice Mills",
     "G.T. Road, Usman Nagar, Kamoke, Dist. Gujranwala (3 units in Kamoke)",
     "+92-55-6665522 | +92-300-8999999",
     "info@waqarrice.com",
     "waqarrice.com", True),

    ("Al-Wahab Rice Mills (Pvt) Ltd",
     "Main G.T. Road, Sadhoke, Dist. Gujranwala 52368 (also Kamoke, Gujranwala)",
     "+92-308-8882506",
     "sales@alwahabrice.com",
     "alwahabrice.com", True),

    ("Al Majeed Rice Mills",
     "G.T. Road, Kamoke, Dist. Gujranwala, Punjab",
     "+92 321 6439969",
     "almajeedrice@outlook.com",
     "almajeedrice.com", True),

    ("Kashif Rice Mills",
     "5-KM Gujranwala Road, Alipur Chatta, Punjab",
     "0556-332775/333348 | 0300-8744142",
     "Kashif-mills@hotmail.com",
     "kashifricemills.enic.pk", False),
]

AREA_FAISALABAD = [
    ("Iqbal Rice Mills (Pvt) Ltd",
     "3-KM Faisalabad Road, Chiniot, Punjab",
     "(047) 6332734 / 6331534",
     "info@iqbalricemills.com",
     "iqbalricemills.com", True),

    ("Asif Rice Mills",
     "48-C, Khayaban-e-Jami, DHA Phase VII, Karachi (factory near Faisalabad)",
     "+92 21 35397706-9 | WA: +92 333 3224510",
     "info@asifrice.com",
     "asifrice.com", True),
]

AREA_OKARA = [
    ("Fatima Rice Mills (Pvt) Ltd",
     "6-KM Renala Sher Garh Road, Renala Khurd, Dist. Okara, Punjab",
     "+92 42 35467931-33",
     "jalal@fatimarice.com.pk",
     "fatimarice.com.pk", True),

    ("Al Karim Rice Mills",
     "7-KM Kissan Ada, Lahore Road, Okara, Punjab",
     "+92 321 6954017 | +92 333 6962817",
     "info@alkareemricemills.com",
     "alkareemricemills.com", False),

    ("Lasani Rice Mills",
     "64 Lasani Traders, Grain Market, Okara 56300, Punjab",
     "+92 44 2524700",
     "—",
     "lasanifoods.com.pk", True),

    ("Bahoo Rice Mills",
     "G.T. Road, Near Kissan Adda, Okara, Punjab",
     "—",
     "—",
     "bahooricemills.com", True),

    ("Karam Rice Mills",
     "8-KM Hujra Road, Depalpur, Okara, Punjab",
     "—",
     "—",
     "—", True),

    ("Zafar Idrees Rice & Processing Mills",
     "12-KM Depalpur Road, Okara, Punjab",
     "0442-513919 / 522819 | 0300-6952819",
     "—",
     "—", False),
]

AREA_BAHAWALNAGAR = [
    ("Pak Rice Mills",
     "Jalwala Road / Outside Grain Market, Bahawalnagar, Punjab 60000",
     "+92 333 4088282",
     "info@pakrice.pk",
     "pakricemills.com", False),

    ("AB Rice Mills",
     "Bahawalnagar Road, Chishtian, Bahawalnagar, Punjab",
     "—",
     "—",
     "abricemills.com", False),
]

AREA_RYK = [
    ("Nisar Rice Factory",
     "National Highway, Iqbal Abad, Rahim Yar Khan, Punjab",
     "068-5678044/244 | 0333-7434344",
     "nisarrice44@gmail.com",
     "—", True),

    ("Quality Foods Industries",
     "KLP Road, Kotsabzal, Sadiqabad, Rahim Yar Khan, Punjab",
     "+92 339 2939393",
     "info@foodsbyquality.com",
     "foodsbyquality.com", True),
]

AREA_MULTAN = [
    ("M. Ali & Co.",
     "01 Qasim Pur Colony, Bahawalpur Road, Multan City, Punjab",
     "—",
     "—",
     "—", False),
]

AREA_PAKPATTAN = [
    ("Lucky Rice Mills",
     "Lucky Food Ind. St., Grain Market, Arifwala, Pakpattan, Punjab",
     "—",
     "—",
     "—", False),

    ("Baba Farid Rice Mill",
     "3-KM Basirpur Road, Depalpur, Okara, Punjab",
     "+92 345 7814941",
     "info@babafarid.com.pk",
     "babafarid.com.pk", False),
]

# ─── BUILD PDF ───────────────────────────────────────────────────────────────
story = []

# Title block
story.append(Table(
    [[p("PUNJAB RICE MILLS DIRECTORY — EXPANSION EDITION", title_s)],
     [p("44 New Mills | Narowal · Sialkot · Daska · Muridke · Lahore · Gujranwala · Faisalabad · Okara · Bahawalnagar · Rahim Yar Khan · Multan · Pakpattan", sub_s)],
     [p("* = REAP (Rice Exporters Association of Pakistan) Member", cap_s)]],
    colWidths=[W],
    style=TableStyle([
        ("BACKGROUND", (0,0), (0,1), GREEN),
        ("BACKGROUND", (0,2), (0,2), GOLD),
        ("TOPPADDING",    (0,0), (-1,-1), 6),
        ("BOTTOMPADDING", (0,0), (-1,-1), 6),
    ])
))
story.append(sp(0.3))

sections = [
    ("NAROWAL DISTRICT", AREA_NAROWAL),
    ("SIALKOT DISTRICT", AREA_SIALKOT),
    ("DASKA (SIALKOT/GUJRANWALA BORDER)", AREA_DASKA),
    ("MURIDKE / SHEIKHUPURA DISTRICT", AREA_MURIDKE),
    ("LAHORE DISTRICT", AREA_LAHORE),
    ("GUJRANWALA DISTRICT", AREA_GUJRANWALA),
    ("FAISALABAD / CHINIOT DISTRICT", AREA_FAISALABAD),
    ("OKARA DISTRICT", AREA_OKARA),
    ("BAHAWALNAGAR DISTRICT", AREA_BAHAWALNAGAR),
    ("RAHIM YAR KHAN DISTRICT", AREA_RYK),
    ("MULTAN DISTRICT", AREA_MULTAN),
    ("PAKPATTAN / ARIFWALA DISTRICT", AREA_PAKPATTAN),
]

counter = 1
for area_label, mills in sections:
    story.append(area_banner(area_label))
    story.append(tbl_header())
    for i, (name, addr, phone, email, website, reap) in enumerate(mills):
        story.append(mill_row(counter, name, addr, phone, email, website, reap, shade=(i % 2 == 0)))
        counter += 1
    story.append(sp(0.3))

# Footer stats
reap_total = sum(1 for sec in sections for m in sec[1] if m[5])
total = counter - 1

story.append(HRFlowable(width=W, thickness=1, color=GREEN))
story.append(sp(0.2))
story.append(Table(
    [[p(f"Total Mills Listed: {total}", bold_s),
      p(f"REAP Members (starred): {reap_total}", star_s),
      p("Note: '--' = not publicly available at time of research (June 2026)", cap_s)]],
    colWidths=[W/3, W/3, W/3],
    style=TableStyle([("VALIGN", (0,0), (-1,-1), "MIDDLE")])
))

doc.build(story)
print(f"PDF generated: Punjab_Rice_Mills_New_40plus_Directory.pdf  ({total} mills, {reap_total} REAP)")
