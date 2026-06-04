from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT

GREEN  = colors.HexColor("#1a7a3c")
GOLD   = colors.HexColor("#c8a200")
RED    = colors.HexColor("#c0392b")
LIGHT  = colors.HexColor("#f4f8f4")
DARK   = colors.HexColor("#1a2e1a")
WHITE  = colors.white
GREY   = colors.HexColor("#f0f0f0")
MIDGREY= colors.HexColor("#cccccc")
LGREEN = colors.HexColor("#e8f5ec")
LRED   = colors.HexColor("#fdf0ef")

doc = SimpleDocTemplate(
    "/home/user/Usama-New/Rice_Export_Procedure_Pakistan_to_DRC.pdf",
    pagesize=A4,
    rightMargin=1.6*cm, leftMargin=1.6*cm,
    topMargin=1.6*cm, bottomMargin=1.6*cm
)

def S(name, **kw):
    base = dict(fontName="Helvetica", fontSize=9, leading=13, textColor=DARK, alignment=TA_LEFT)
    base.update(kw)
    return ParagraphStyle(name, **base)

title_s   = S("title", fontSize=18, leading=24, textColor=WHITE, fontName="Helvetica-Bold", alignment=TA_CENTER)
sub_s     = S("sub",   fontSize=10, leading=14, textColor=GOLD,  fontName="Helvetica-Bold", alignment=TA_CENTER)
step_s    = S("step",  fontSize=11, leading=15, textColor=WHITE, fontName="Helvetica-Bold", alignment=TA_LEFT)
head_s    = S("head",  fontSize=9,  leading=13, textColor=WHITE, fontName="Helvetica-Bold", alignment=TA_CENTER)
body_s    = S("body",  fontSize=8,  leading=12, textColor=DARK,  fontName="Helvetica")
bold_s    = S("bold",  fontSize=8,  leading=12, textColor=DARK,  fontName="Helvetica-Bold")
green_s   = S("green", fontSize=8,  leading=12, textColor=GREEN, fontName="Helvetica-Bold")
red_s     = S("red",   fontSize=8,  leading=12, textColor=RED,   fontName="Helvetica-Bold")
gold_s    = S("gold",  fontSize=8,  leading=12, textColor=GOLD,  fontName="Helvetica-Bold")
cap_s     = S("cap",   fontSize=7,  leading=10, textColor=colors.HexColor("#666666"), fontName="Helvetica-Oblique", alignment=TA_CENTER)
verdict_s = S("verd",  fontSize=9,  leading=13, textColor=DARK,  fontName="Helvetica-Bold", alignment=TA_CENTER)
num_s     = S("num",   fontSize=13, leading=17, textColor=WHITE, fontName="Helvetica-Bold", alignment=TA_CENTER)
tip_s     = S("tip",   fontSize=8,  leading=12, textColor=DARK,  fontName="Helvetica-Oblique")

W = 17.8*cm  # full usable width

story = []

def p(txt, style=body_s): return Paragraph(txt, style)
def sp(h=0.3): return Spacer(1, h*cm)

def banner(text, bg=DARK, style=None):
    st = style or S("b", fontSize=11, leading=15, textColor=WHITE, fontName="Helvetica-Bold", alignment=TA_CENTER)
    t = Table([[p(text, st)]], colWidths=[W])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0),(-1,-1), bg),
        ("TOPPADDING", (0,0),(-1,-1), 8),
        ("BOTTOMPADDING",(0,0),(-1,-1), 8),
        ("LEFTPADDING", (0,0),(-1,-1), 10),
        ("RIGHTPADDING",(0,0),(-1,-1), 10),
    ]))
    return t

def step_banner(num, title, emoji=""):
    txt = f"{emoji} Step {num}: {title}"
    t = Table([[p(txt, step_s)]], colWidths=[W])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0),(-1,-1), GREEN),
        ("TOPPADDING", (0,0),(-1,-1), 7),
        ("BOTTOMPADDING",(0,0),(-1,-1), 7),
        ("LEFTPADDING", (0,0),(-1,-1), 10),
        ("RIGHTPADDING",(0,0),(-1,-1), 10),
    ]))
    return t

def simple_table(rows, col_widths, style_overrides=None):
    t = Table(rows, colWidths=col_widths)
    base = [
        ("GRID",         (0,0),(-1,-1), 0.4, MIDGREY),
        ("VALIGN",       (0,0),(-1,-1), "MIDDLE"),
        ("TOPPADDING",   (0,0),(-1,-1), 6),
        ("BOTTOMPADDING",(0,0),(-1,-1), 6),
        ("LEFTPADDING",  (0,0),(-1,-1), 7),
        ("RIGHTPADDING", (0,0),(-1,-1), 7),
    ]
    if style_overrides:
        base += style_overrides
    t.setStyle(TableStyle(base))
    return t

def tip_box(text):
    t = Table([[p(f"💡 {text}", tip_s)]], colWidths=[W])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0),(-1,-1), colors.HexColor("#fffbea")),
        ("LINEABOVE",  (0,0),(-1,0), 1, GOLD),
        ("LINEBELOW",  (0,0),(-1,0), 1, GOLD),
        ("TOPPADDING", (0,0),(-1,-1), 6),
        ("BOTTOMPADDING",(0,0),(-1,-1), 6),
        ("LEFTPADDING", (0,0),(-1,-1), 8),
        ("RIGHTPADDING",(0,0),(-1,-1), 8),
    ]))
    return t

# ─── HEADER ──────────────────────────────────────────────────────────────────
story.append(banner("🌾  Step-by-Step Rice Export Procedure", bg=GREEN, style=title_s))
story.append(banner("Pakistan → DRC (Democratic Republic of Congo)", bg=DARK, style=sub_s))
story.append(sp(0.4))

# ─── STEP 1: DOCUMENTS ───────────────────────────────────────────────────────
story.append(step_banner(1, "Documents Needed for Rice Export to DRC", "📄"))
mandatory_rows = [
    [p("Document", head_s), p("Issued By", head_s), p("Mandatory?", head_s)],
    [p("Commercial Invoice", bold_s),       p("You prepare", body_s),                         p("✅ YES", green_s)],
    [p("Packing List", bold_s),             p("You prepare", body_s),                         p("✅ YES", green_s)],
    [p("Bill of Lading (B/L)", bold_s),     p("Shipping line (MSC/Maersk)", body_s),          p("✅ YES", green_s)],
    [p("Certificate of Origin", bold_s),    p("FPCCI / Chamber of Commerce", body_s),         p("✅ YES", green_s)],
    [p("Phytosanitary Certificate", bold_s),p("DPP via PSW portal", body_s),                  p("✅ YES", green_s)],
    [p("Fumigation Certificate", bold_s),   p("Licensed fumigation company", body_s),         p("✅ YES", green_s)],
    [p("PSW Export Declaration (GD)", bold_s),p("PSW portal / Clearing Agent", body_s),       p("✅ YES", green_s)],
    [p("BIVAC/OCC Inspection Certificate", bold_s),p("SGS, COTECNA, Bureau Veritas", body_s),p("✅ YES (DRC)", green_s)],
    [p("Weight & Quality Certificate", bold_s),p("SGS/COTECNA at mill", body_s),              p("✅ YES", green_s)],
    [p("SGS Quality Report", bold_s),       p("SGS Pakistan", body_s),                        p("⭐ Recommended", gold_s)],
    [p("Halal Certificate", bold_s),        p("PNAC or recognized body", body_s),             p("⭐ Recommended", gold_s)],
    [p("Insurance Certificate", bold_s),    p("NIC / EFU / Jubilee General", body_s),        p("If CIF contract", gold_s)],
]
t = simple_table(mandatory_rows, [7*cm, 6.5*cm, 4.3*cm], [
    ("BACKGROUND", (0,0),(-1,0), DARK),
    ("BACKGROUND", (0,1),(-1,1), LGREEN),
    ("BACKGROUND", (0,2),(-1,2), WHITE),
    ("BACKGROUND", (0,3),(-1,3), LGREEN),
    ("BACKGROUND", (0,4),(-1,4), WHITE),
    ("BACKGROUND", (0,5),(-1,5), LGREEN),
    ("BACKGROUND", (0,6),(-1,6), WHITE),
    ("BACKGROUND", (0,7),(-1,7), LGREEN),
    ("BACKGROUND", (0,8),(-1,8), WHITE),
    ("BACKGROUND", (0,9),(-1,9), LGREEN),
    ("BACKGROUND", (0,10),(-1,10), GREY),
    ("BACKGROUND", (0,11),(-1,11), GREY),
    ("BACKGROUND", (0,12),(-1,12), GREY),
])
story.append(t)
story.append(sp(0.4))

# ─── STEP 2: ESFCA BANK ACCOUNT ──────────────────────────────────────────────
story.append(step_banner(2, "ESFCA Bank Account (Exporters' Special Foreign Currency Account)", "🏦"))
esfca_rows = [
    [p("Where to Open", bold_s), p("HBL, MCB, UBL, Allied Bank, Meezan Bank", body_s)],
    [p("Required Docs", bold_s), p("NTN + CNIC + Business Registration (sole trader/company) + REAP Membership", body_s)],
    [p("SBP Rule", bold_s),      p("Retain 50% of export proceeds in USD — remaining 50% can be converted to PKR", body_s)],
    [p("Do NOT deposit", bold_s),p("Your own PKR money — only foreign currency from export proceeds goes in", body_s)],
    [p("When to Open", bold_s),  p("Before your first shipment — so LC can be routed directly to your bank", body_s)],
]
t = simple_table(esfca_rows, [4.5*cm, 13.3*cm], [
    ("BACKGROUND", (0,0),(-1,-1), WHITE),
    ("BACKGROUND", (0,0),(0,-1), LGREEN),
    ("FONTNAME",   (0,0),(0,-1), "Helvetica-Bold"),
    ("BACKGROUND", (0,1),(-1,1), GREY),
    ("BACKGROUND", (0,3),(-1,3), GREY),
])
story.append(t)
story.append(sp(0.4))

# ─── STEP 3: LC ARRIVES ──────────────────────────────────────────────────────
story.append(step_banner(3, "LC Arrives at Bank — What To Do Next", "📬"))
lc_rows = [
    [p("1", num_s), p("Bank Review", bold_s),      p("Bank calls you — LC received. Review: rice specs, quantity, price, port, expiry, docs required.", body_s)],
    [p("2", num_s), p("LC Copy to Mill", bold_s),  p("Give factory only a COPY of LC with specs page. NEVER give original LC to factory.", body_s)],
    [p("3", num_s), p("Production", bold_s),       p("Factory produces rice to your specifications.", body_s)],
    [p("4", num_s), p("Inspection", bold_s),       p("Arrange SGS/COTECNA inspection at mill before loading.", body_s)],
    [p("5", num_s), p("Shipment", bold_s),         p("Container loaded on vessel at Karachi port.", body_s)],
    [p("6", num_s), p("Collect Docs", bold_s),     p("Collect: B/L, invoice, packing list, C/O, phyto cert, inspection cert.", body_s)],
    [p("7", num_s), p("Submit to Bank", bold_s),   p("Submit ALL documents to YOUR bank within 21 days of B/L date.", body_s)],
    [p("8", num_s), p("Payment Released", bold_s), p("Your bank sends docs to DRC buyer's bank → buyer's bank releases payment → credited to your ESFCA.", body_s)],
]
t = simple_table(lc_rows, [1*cm, 3.5*cm, 13.3*cm], [
    ("BACKGROUND", (0,0),(0,-1), GREEN),
    ("BACKGROUND", (0,0),(-1,0), LGREEN),
    ("BACKGROUND", (0,2),(-1,2), LGREEN),
    ("BACKGROUND", (0,4),(-1,4), LGREEN),
    ("BACKGROUND", (0,6),(-1,6), LGREEN),
    ("BACKGROUND", (0,1),(-1,1), WHITE),
    ("BACKGROUND", (0,3),(-1,3), WHITE),
    ("BACKGROUND", (0,5),(-1,5), WHITE),
    ("BACKGROUND", (0,7),(-1,7), WHITE),
])
story.append(t)
story.append(sp(0.2))
story.append(tip_box("LC is your payment guarantee — keep the original with your bank at all times."))
story.append(sp(0.4))

# ─── STEP 4: FORM E ──────────────────────────────────────────────────────────
story.append(step_banner(4, "Form E — How to Get It (IMPORTANT UPDATE)", "📝"))
forme_rows = [
    [p("STATUS", bold_s), p("Form E is ELIMINATED — SBP abolished it in 2024.", red_s)],
    [p("CURRENT PROCESS", bold_s), p("PSW portal automatically generates PSW Financial Instrument when you file your GD (Goods Declaration). This replaces Form E completely.", body_s)],
    [p("WHO HANDLES IT", bold_s), p("Your clearing agent handles through PSW portal — nothing extra needed from you.", body_s)],
    [p("BANK STEP", bold_s), p("Bank registers your export proceeds against the PSW reference number automatically.", body_s)],
]
t = simple_table(forme_rows, [4*cm, 13.8*cm], [
    ("BACKGROUND", (0,0),(0,-1), LGREEN),
    ("FONTNAME",   (0,0),(0,-1), "Helvetica-Bold"),
    ("BACKGROUND", (0,0),(-1,0), colors.HexColor("#fdf0ef")),
    ("BACKGROUND", (0,1),(-1,1), WHITE),
    ("BACKGROUND", (0,2),(-1,2), LGREEN),
    ("BACKGROUND", (0,3),(-1,3), WHITE),
])
story.append(t)
story.append(sp(0.4))

# ─── STEP 5: MILL INSPECTION ─────────────────────────────────────────────────
story.append(step_banner(5, "Mill Rice Inspection (Before Loading)", "🔍"))
insp_rows = [
    [p("Who to Contact", bold_s),   p("SGS Pakistan, COTECNA, or Bureau Veritas — book at least 3–4 days before loading.", body_s)],
    [p("What is Checked", bold_s),  p("Moisture content, broken %, grain length, foreign matter, pesticide residues.", body_s)],
    [p("Where", bold_s),            p("At mill or warehouse — before container is sealed.", body_s)],
    [p("Documents Issued", bold_s), p("Weight Certificate + Quality/Grade Certificate.", body_s)],
    [p("Cost", bold_s),             p("~$150–300 per container.", body_s)],
    [p("Why Mandatory", bold_s),    p("DRC (BIVAC/OCC) requires this — without it, shipment is held at Matadi port.", body_s)],
]
t = simple_table(insp_rows, [4*cm, 13.8*cm], [
    ("BACKGROUND", (0,0),(0,-1), LGREEN),
    ("FONTNAME",   (0,0),(0,-1), "Helvetica-Bold"),
    ("BACKGROUND", (0,1),(-1,1), GREY),
    ("BACKGROUND", (0,3),(-1,3), GREY),
    ("BACKGROUND", (0,5),(-1,5), GREY),
])
story.append(t)
story.append(sp(0.4))

# ─── STEP 6: CUSTOM CLEARANCE ────────────────────────────────────────────────
story.append(step_banner(6, "Customs Clearance for Rice Export", "🛃"))
cust_rows = [
    [p("1", num_s), p("GD Filing", bold_s),       p("Clearing agent files Goods Declaration on PSW portal. HS Code: 1006.30 (milled white rice).", body_s)],
    [p("2", num_s), p("Customs Check", bold_s),   p("Customs selects green channel (auto-cleared) or physical examination.", body_s)],
    [p("3", num_s), p("If Examination", bold_s),  p("Customs inspector checks bags at port/dry port. Ensure all docs match GD exactly.", body_s)],
    [p("4", num_s), p("Gate Pass", bold_s),       p("Customs Export Gate Pass issued — container allowed to leave for Karachi port.", body_s)],
    [p("5", num_s), p("KPT Docs", bold_s),        p("Agent submits docs to Karachi Port Trust (KPT) for terminal container release.", body_s)],
    [p("Cost", num_s), p("Agent Fee", bold_s),    p("PKR 8,000–15,000 per 20ft container.", body_s)],
]
t = simple_table(cust_rows, [1*cm, 3.5*cm, 13.3*cm], [
    ("BACKGROUND", (0,0),(0,-1), GREEN),
    ("BACKGROUND", (0,0),(-1,0), LGREEN),
    ("BACKGROUND", (0,2),(-1,2), LGREEN),
    ("BACKGROUND", (0,4),(-1,4), LGREEN),
    ("BACKGROUND", (0,1),(-1,1), WHITE),
    ("BACKGROUND", (0,3),(-1,3), WHITE),
    ("BACKGROUND", (0,5),(-1,5), colors.HexColor("#fffbea")),
])
story.append(t)
story.append(sp(0.4))

# ─── STEP 7: PHYTOSANITARY ───────────────────────────────────────────────────
story.append(step_banner(7, "Phytosanitary Certificate", "🌿"))
phyto_rows = [
    [p("Issued By", bold_s),   p("Department of Plant Protection (DPP) — Ministry of National Food Security", body_s)],
    [p("How to Apply", bold_s),p("Apply on PSW portal → select 'Phytosanitary Certificate' → fill rice details (species, quantity, origin, consignee in DRC)", body_s)],
    [p("Inspection", bold_s),  p("DPP inspector visits warehouse/port — checks for pests, disease, moisture.", body_s)],
    [p("Timeline", bold_s),    p("Certificate issued within 2–3 working days after inspection.", body_s)],
    [p("Cost", bold_s),        p("~PKR 2,000–5,000 per shipment.", body_s)],
    [p("Important", bold_s),   p("Valid for ONE shipment only — get a fresh certificate for each container/shipment.", body_s)],
    [p("Why Required", bold_s),p("DRC port (Matadi/DGDA) requires this — without it, shipment is rejected and returned.", body_s)],
]
t = simple_table(phyto_rows, [3.5*cm, 14.3*cm], [
    ("BACKGROUND", (0,0),(0,-1), LGREEN),
    ("FONTNAME",   (0,0),(0,-1), "Helvetica-Bold"),
    ("BACKGROUND", (0,1),(-1,1), GREY),
    ("BACKGROUND", (0,3),(-1,3), GREY),
    ("BACKGROUND", (0,5),(-1,5), GREY),
    ("BACKGROUND", (0,6),(-1,6), colors.HexColor("#fdf0ef")),
])
story.append(t)
story.append(sp(0.4))

# ─── STEP 8: FACTORY DOCS ────────────────────────────────────────────────────
story.append(step_banner(8, "Documents To/From Factory (Mill)", "📋"))
factory_rows = [
    [p("YOU GIVE to Factory", head_s), p("YOU GET from Factory", head_s)],
    [p("✅ Purchase Order (your PO to mill)\n✅ Copy of LC — specs page only\n✅ Packing instructions (bag size 25kg/50kg, labeling, HS code)\n✅ Quality spec sheet (broken %, moisture %, grain length)", body_s),
     p("✅ Sales Invoice from mill\n✅ Mill Analysis Report (moisture, broken %, grade)\n✅ Fumigation Certificate\n✅ Loading Certificate / Weight Slip (from weighbridge)\n✅ Truck Receipt / Delivery Challan (when rice leaves mill)", body_s)],
]
t = simple_table(factory_rows, [8.9*cm, 8.9*cm], [
    ("BACKGROUND", (0,0),(-1,0), DARK),
    ("BACKGROUND", (0,1),(0,1), LGREEN),
    ("BACKGROUND", (1,1),(1,1), colors.HexColor("#f0f8ff")),
    ("VALIGN",     (0,0),(-1,-1), "TOP"),
])
story.append(t)
story.append(sp(0.2))
story.append(tip_box("Keep mill invoice safe — both customs and bank need it during document negotiation."))
story.append(sp(0.4))

# ─── STEP 9: MILL AGREEMENT ──────────────────────────────────────────────────
story.append(step_banner(9, "Mill / Company Agreement — Key Terms", "🤝"))
agree_rows = [
    [p("Clause", head_s),             p("What to Write", head_s)],
    [p("Quality Guarantee", bold_s),  p("Broken max 5%, moisture max 13.5%, no foreign matter — as per SGS spec.", body_s)],
    [p("Delivery Deadline", bold_s),  p("Rice must be ready within X days of Purchase Order.", body_s)],
    [p("Shortfall Penalty", bold_s),  p("If mill delivers less than ordered, penalty per MT applies.", body_s)],
    [p("Rejection Right", bold_s),    p("If SGS inspection fails, you can reject shipment — mill replaces at no cost.", body_s)],
    [p("Price Lock", bold_s),         p("Price fixed at PO date — no changes after signing.", body_s)],
    [p("Fumigation", bold_s),         p("Mill is responsible for fumigation before loading container.", body_s)],
    [p("Document Responsibility", bold_s), p("Mill provides: mill invoice, fumigation cert, weight slip.", body_s)],
    [p("Payment Terms", bold_s),      p("30% advance + 70% after loading OR after LC payment received in your bank.", body_s)],
    [p("Legal Requirement", bold_s),  p("Agreement signed + stamped on Rs. 500 stamp paper with witnesses.", body_s)],
]
t = simple_table(agree_rows, [4.5*cm, 13.3*cm], [
    ("BACKGROUND", (0,0),(-1,0), DARK),
    ("BACKGROUND", (0,0),(0,-1), LGREEN),
    ("FONTNAME",   (0,0),(0,-1), "Helvetica-Bold"),
    ("BACKGROUND", (0,2),(-1,2), GREY),
    ("BACKGROUND", (0,4),(-1,4), GREY),
    ("BACKGROUND", (0,6),(-1,6), GREY),
    ("BACKGROUND", (0,8),(-1,8), GREY),
])
story.append(t)
story.append(sp(0.4))

# ─── STEP 10: FREIGHT / INSURANCE / BOL ─────────────────────────────────────
story.append(step_banner(10, "Freight / Insurance / Bill of Lading", "🚢"))
fib_rows = [
    [p("Term", head_s), p("What It Is", head_s), p("How to Manage", head_s)],
    [p("FREIGHT", bold_s),
     p("Cost to move container Karachi → Matadi", body_s),
     p("Rate: ~$2,800–3,500 per 20ft\nFOB contract: buyer pays\nCFR/CIF contract: you pay", body_s)],
    [p("INSURANCE", bold_s),
     p("Covers cargo loss/damage during sea voyage", body_s),
     p("Get from NIC / EFU General / Jubilee General\nCost: ~0.3–0.5% of cargo value\nRequired if CIF contract", body_s)],
    [p("BILL OF LADING", bold_s),
     p("Most important doc — title/ownership of goods. Without it, buyer cannot collect rice at Matadi", body_s),
     p("Issued by shipping line after loading\n3 original B/Ls issued\nSend 1 to buyer's bank, keep 2\nSubmit to your bank within 21 days", body_s)],
]
t = simple_table(fib_rows, [3*cm, 7*cm, 7.8*cm], [
    ("BACKGROUND", (0,0),(-1,0), DARK),
    ("BACKGROUND", (0,1),(-1,1), LGREEN),
    ("BACKGROUND", (0,2),(-1,2), WHITE),
    ("BACKGROUND", (0,3),(-1,3), LGREEN),
    ("VALIGN",     (0,0),(-1,-1), "TOP"),
])
story.append(t)
story.append(sp(0.3))

# Clearing agent box
ca_rows = [
    [p("Can One Clearing Agent Handle Everything?", head_s)],
    [p("✅ YES — a good Karachi clearing agent handles:\n"
       "  • PSW/GD filing   • Customs clearance   • Port documentation (KPT)\n"
       "  • Container booking coordination   • Freight booking liaison\n\n"
       "❌ They do NOT handle:\n"
       "  • Phytosanitary Certificate (DPP — you apply on PSW)\n"
       "  • Certificate of Origin (FPCCI/Chamber — you apply)\n"
       "  • SGS/COTECNA inspection (you book separately)\n"
       "  • BIVAC/OCC inspection (DRC side — buyer's agent handles in DRC)\n\n"
       "Tip: Find a clearing agent with DRC export experience — ask if they've done Karachi → Matadi before.", body_s)],
]
t = simple_table(ca_rows, [W], [
    ("BACKGROUND", (0,0),(-1,0), DARK),
    ("BACKGROUND", (0,1),(-1,1), LGREEN),
])
story.append(t)
story.append(sp(0.4))

# MSC vs Maersk
story.append(banner("🚢  MSC vs Maersk — Which Container Line for DRC?", bg=DARK))
msc_rows = [
    [p("", head_s),             p("MSC", head_s),                          p("Maersk", head_s)],
    [p("Service to Matadi", bold_s),  p("MSC Iroko Service (via Pointe-Noire)", body_s), p("Maersk 23H Matadi Feeder", body_s)],
    [p("Transit Time", bold_s),       p("~32–35 days", green_s),                          p("~35–38 days", body_s)],
    [p("Frequency", bold_s),          p("Weekly", green_s),                                p("Bi-weekly", body_s)],
    [p("Price", bold_s),              p("Slightly cheaper", green_s),                      p("Slightly higher", body_s)],
    [p("Reliability", bold_s),        p("Very good on Africa routes", body_s),             p("Excellent tracking & docs", body_s)],
    [p("RECOMMENDATION", bold_s),     p("✅ BEST CHOICE for DRC", green_s),               p("Good backup option", gold_s)],
]
t = simple_table(msc_rows, [4.5*cm, 6.65*cm, 6.65*cm], [
    ("BACKGROUND", (0,0),(-1,0), DARK),
    ("BACKGROUND", (0,1),(-1,1), GREY),
    ("BACKGROUND", (0,2),(-1,2), WHITE),
    ("BACKGROUND", (0,3),(-1,3), GREY),
    ("BACKGROUND", (0,4),(-1,4), WHITE),
    ("BACKGROUND", (0,5),(-1,5), GREY),
    ("BACKGROUND", (0,6),(-1,6), colors.HexColor("#e8f5ec")),
    ("BACKGROUND", (1,6),(1,6), LGREEN),
])
story.append(t)
story.append(sp(0.3))

# Final verdict
verdict_data = [[
    Paragraph(
        "Start with MSC — stronger West Africa network, more frequent sailings to Matadi, competitive rates.\n"
        "Use Maersk as backup when MSC is fully booked.\n"
        "Pro Tip: Your clearing agent + freight forwarder can be the SAME company — look for a Karachi freight forwarder "
        "with an Africa desk who handles everything from GD filing to B/L collection.",
        verdict_s)
]]
vt = Table(verdict_data, colWidths=[W])
vt.setStyle(TableStyle([
    ("BACKGROUND",    (0,0), (-1,-1), LGREEN),
    ("LINEABOVE",     (0,0), (-1,0),  2, GREEN),
    ("LINEBELOW",     (0,0), (-1,0),  2, GREEN),
    ("TOPPADDING",    (0,0), (-1,-1), 10),
    ("BOTTOMPADDING", (0,0), (-1,-1), 10),
    ("LEFTPADDING",   (0,0), (-1,-1), 12),
    ("RIGHTPADDING",  (0,0), (-1,-1), 12),
]))
story.append(vt)
story.append(sp(0.3))

# Footer
story.append(HRFlowable(width="100%", thickness=0.5, color=MIDGREY))
story.append(sp(0.1))
story.append(p("Prepared for Pakistan Rice Export to DRC  ·  Based on SBP, PSW, DPP, TDAP, FPCCI guidelines  ·  2025", cap_s))

doc.build(story)
print("PDF created: Rice_Export_Procedure_Pakistan_to_DRC.pdf")
