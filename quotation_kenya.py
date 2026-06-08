from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.lib import colors

output_path = "/home/user/Usama-New/AKHS_Quotation_Kenya_Basmati.pdf"
PAGE_W, PAGE_H = A4

GREEN  = colors.HexColor("#1a7a3c")
DARK   = colors.HexColor("#1a2e1a")
GOLD   = colors.HexColor("#c8a200")
WHITE  = colors.white
LIGHT  = colors.HexColor("#e8f5ec")
GREY   = colors.HexColor("#f5f5f5")
BLUE   = colors.HexColor("#1a3a6b")

c = canvas.Canvas(output_path, pagesize=A4)

# ── HEADER ──────────────────────────────────────────────────────────────────
c.setFillColor(DARK)
c.rect(0, PAGE_H - 38*mm, PAGE_W, 38*mm, fill=1, stroke=0)
c.setFillColor(GOLD)
c.rect(0, PAGE_H - 39.5*mm, PAGE_W, 1.5*mm, fill=1, stroke=0)
c.setFillColor(GREEN)
c.rect(0, PAGE_H - 38*mm, 3*mm, 38*mm, fill=1, stroke=0)

# Company name
c.setFillColor(GOLD)
c.setFont("Helvetica-Bold", 22)
c.drawString(12*mm, PAGE_H - 16*mm, "AKHS TRADERS")
c.setFillColor(WHITE)
c.setFont("Helvetica", 9)
c.drawString(12*mm, PAGE_H - 23*mm, "Rice Exporters — Pakistan")
c.setFont("Helvetica", 8)
c.drawString(12*mm, PAGE_H - 29*mm, "PSW Registered  |  REAP Member  |  SGS Inspected  |  Fumigated")
c.drawString(12*mm, PAGE_H - 34*mm, "CEO: Syed Muhammad Usama Ali  |  +92-334-0065781  |  Multan, Pakistan")

# QUOTATION label
c.setFillColor(GOLD)
c.setFont("Helvetica-Bold", 18)
c.drawRightString(PAGE_W - 12*mm, PAGE_H - 16*mm, "QUOTATION")
c.setFillColor(WHITE)
c.setFont("Helvetica", 8)
c.drawRightString(PAGE_W - 12*mm, PAGE_H - 23*mm, "Ref: AKHS-Q-2026-001")
c.drawRightString(PAGE_W - 12*mm, PAGE_H - 29*mm, "Date: June 08, 2026")
c.drawRightString(PAGE_W - 12*mm, PAGE_H - 34*mm, "Valid: 7 Days")

y = PAGE_H - 48*mm

# ── BUYER INFO ───────────────────────────────────────────────────────────────
c.setFillColor(LIGHT)
c.rect(10*mm, y - 22*mm, PAGE_W - 20*mm, 24*mm, fill=1, stroke=0)
c.setFillColor(GREEN)
c.rect(10*mm, y - 22*mm, 3*mm, 24*mm, fill=1, stroke=0)

c.setFillColor(DARK)
c.setFont("Helvetica-Bold", 10)
c.drawString(17*mm, y - 5*mm, "TO:")
c.setFont("Helvetica-Bold", 11)
c.drawString(28*mm, y - 5*mm, "Goodwill")
c.setFont("Helvetica", 9)
c.drawString(28*mm, y - 11*mm, "Buyer — Kenya")
c.drawString(28*mm, y - 17*mm, "Destination Port: Durban, South Africa")

c.setFont("Helvetica-Bold", 9)
c.drawString(120*mm, y - 5*mm, "RE: Long Grain Basmati Rice")
c.setFont("Helvetica", 9)
c.drawString(120*mm, y - 11*mm, "Qty: 5 x 20ft Containers")
c.drawString(120*mm, y - 17*mm, "Inquiry Ref: go4worldbusiness — Feb 2026")

y -= 30*mm

# ── INTRO TEXT ───────────────────────────────────────────────────────────────
c.setFillColor(DARK)
c.setFont("Helvetica", 9)
c.drawString(10*mm, y, "Dear Goodwill,")
y -= 6*mm
intro = ("Thank you for your inquiry regarding Long Grain Basmati Rice. We are pleased to submit our best competitive "
         "quotation for 5 x 20ft containers as per your requirement. AKHS TRADERS is a PSW-registered rice exporter "
         "from Pakistan with full export documentation capability including SGS inspection, fumigation, and phytosanitary certificates.")
# wrap intro
words = intro.split()
line = ""
for word in words:
    test = (line + " " + word).strip()
    if c.stringWidth(test, "Helvetica", 9) < PAGE_W - 22*mm:
        line = test
    else:
        c.drawString(10*mm, y, line)
        y -= 5*mm
        line = word
if line:
    c.drawString(10*mm, y, line)
    y -= 8*mm

# ── PRICE TABLE ──────────────────────────────────────────────────────────────
c.setFillColor(DARK)
c.setFont("Helvetica-Bold", 11)
c.drawString(10*mm, y, "Price Quotation — Long Grain Basmati Rice (Pakistan Origin)")
y -= 6*mm

# Table header
col = [10*mm, 60*mm, 95*mm, 125*mm, 158*mm]
hdr_h = 9*mm
c.setFillColor(DARK)
c.rect(10*mm, y - hdr_h + 2*mm, PAGE_W - 20*mm, hdr_h, fill=1, stroke=0)
c.setFillColor(GOLD)
c.setFont("Helvetica-Bold", 9)
headers = ["Grade / Broken %", "FOB Karachi", "CFR Durban (Est.)", "Per Container (MT)", "Total 5 Cont."]
for i, h in enumerate(headers):
    c.drawString(col[i] + 2*mm, y - 4*mm, h)
y -= hdr_h

# Freight estimate Karachi to Durban ~$900/container = $36/MT
freight = 36  # USD per MT approx

rows = [
    ("Long Grain Basmati  5% Broken",  491, "Premium Grade"),
    ("Long Grain Basmati 15% Broken",  479, "Standard Grade"),
    ("Long Grain Basmati 25% Broken",  469, "Economy Grade"),
    ("Long Grain Basmati 100% Broken", 409, "Broken Grade"),
]

for i, (grade, fob, label) in enumerate(rows):
    bg = LIGHT if i % 2 == 0 else WHITE
    c.setFillColor(bg)
    c.rect(10*mm, y - 9*mm + 2*mm, PAGE_W - 20*mm, 9*mm, fill=1, stroke=0)

    cfr = fob + freight
    per_cont = fob * 25  # 25MT per 20ft
    total_5 = per_cont * 5

    c.setFillColor(DARK)
    c.setFont("Helvetica-Bold" if i == 2 else "Helvetica", 9)
    c.drawString(col[0] + 2*mm, y - 5*mm, grade)
    c.setFont("Helvetica-Bold", 9)
    c.setFillColor(GREEN)
    c.drawString(col[1] + 2*mm, y - 5*mm, f"USD {fob}/MT")
    c.setFillColor(DARK)
    c.setFont("Helvetica", 8.5)
    c.drawString(col[2] + 2*mm, y - 5*mm, f"USD {cfr}/MT")
    c.drawString(col[3] + 2*mm, y - 5*mm, f"~USD {per_cont:,}")
    c.setFillColor(BLUE)
    c.setFont("Helvetica-Bold", 8.5)
    c.drawString(col[4] + 2*mm, y - 5*mm, f"~USD {total_5:,}")
    y -= 9*mm

# Highlight row — recommended
y -= 2*mm
c.setFillColor(GOLD)
c.roundRect(10*mm, y - 8*mm, PAGE_W - 20*mm, 9*mm, 1*mm, fill=1, stroke=0)
c.setFillColor(DARK)
c.setFont("Helvetica-Bold", 9)
c.drawString(13*mm, y - 4*mm, "RECOMMENDED FOR YOU:")
c.drawString(65*mm, y - 4*mm, "25% Broken @ USD 469/MT FOB  |  5 Containers = ~USD 58,625 FOB Total")
y -= 15*mm

# ── SPECIFICATIONS ────────────────────────────────────────────────────────────
c.setFillColor(DARK)
c.setFont("Helvetica-Bold", 11)
c.drawString(10*mm, y, "Product Specifications")
y -= 6*mm

specs = [
    ("Product", "Long Grain Basmati Rice — Pakistan Origin"),
    ("Grain Length", "7.0 mm+ (extra long grain)"),
    ("Moisture", "Maximum 13.5%"),
    ("Broken %", "As per grade ordered (5% / 15% / 25% / 100%)"),
    ("Foreign Matter", "Maximum 0.1%"),
    ("Chalky Grains", "Maximum 2%"),
    ("Aroma", "Natural Basmati fragrance"),
    ("Packing", "25 kg or 50 kg PP Woven Bags (as required)"),
    ("Bag Marking", "Custom printing available — your brand/logo"),
    ("HS Code", "1006.30"),
    ("Origin", "Pakistan (Punjab)"),
    ("Crop", "Fresh 2025 crop"),
]

col1 = 10*mm
col2 = 55*mm
row_h = 7*mm

for i, (k, v) in enumerate(specs):
    bg = LIGHT if i % 2 == 0 else WHITE
    c.setFillColor(bg)
    c.rect(col1, y - row_h + 2*mm, PAGE_W - 20*mm, row_h, fill=1, stroke=0)
    c.setFillColor(GREEN)
    c.setFont("Helvetica-Bold", 8.5)
    c.drawString(col1 + 2*mm, y - 3.5*mm, k)
    c.setFillColor(DARK)
    c.setFont("Helvetica", 8.5)
    c.drawString(col2, y - 3.5*mm, v)
    y -= row_h

y -= 8*mm

# ── TERMS ─────────────────────────────────────────────────────────────────────
c.setFillColor(DARK)
c.setFont("Helvetica-Bold", 11)
c.drawString(10*mm, y, "Terms & Conditions")
y -= 6*mm

terms = [
    ("Shipping Terms", "FOB Karachi  OR  CFR Durban (as preferred)"),
    ("Payment Terms", "30% TT Advance + 70% against Copy of B/L  (as per your requirement)"),
    ("Shipment Port", "Karachi, Pakistan (PKKAR)"),
    ("Destination Port", "Durban, South Africa (ZADUR)"),
    ("Transit Time", "Approx. 20–25 days Karachi to Durban"),
    ("Lead Time", "15–20 days after order confirmation and advance payment"),
    ("Minimum Order", "1 x 20ft Container (~25 MT)"),
    ("Sample", "Available — 1–2 kg sample can be sent by courier on request"),
    ("Quotation Validity", "7 days from date of this quotation"),
]

for i, (k, v) in enumerate(terms):
    bg = LIGHT if i % 2 == 0 else WHITE
    c.setFillColor(bg)
    c.rect(col1, y - row_h + 2*mm, PAGE_W - 20*mm, row_h, fill=1, stroke=0)
    c.setFillColor(GREEN)
    c.setFont("Helvetica-Bold", 8.5)
    c.drawString(col1 + 2*mm, y - 3.5*mm, k)
    c.setFillColor(DARK)
    c.setFont("Helvetica", 8.5)
    c.drawString(col2, y - 3.5*mm, v)
    y -= row_h

y -= 8*mm

# ── DOCUMENTS PROVIDED ────────────────────────────────────────────────────────
c.setFillColor(DARK)
c.setFont("Helvetica-Bold", 11)
c.drawString(10*mm, y, "Documents Provided with Each Shipment")
y -= 6*mm

docs = [
    "Commercial Invoice",
    "Packing List",
    "Bill of Lading (Original 3/3)",
    "Certificate of Origin (FPCCI / Chamber)",
    "Phytosanitary Certificate (Govt. of Pakistan)",
    "Fumigation Certificate",
    "SGS / COTECNA Quality & Weight Certificate (on request)",
    "PSW Export Declaration",
]

# Two columns
half = len(docs) // 2
for i, doc in enumerate(docs):
    if i < half:
        cx = 12*mm
        cy = y - (i * 6*mm)
    else:
        cx = PAGE_W/2 + 5*mm
        cy = y - ((i - half) * 6*mm)
    c.setFillColor(GREEN)
    c.circle(cx, cy + 1.5*mm, 1.5*mm, fill=1, stroke=0)
    c.setFillColor(DARK)
    c.setFont("Helvetica", 8.5)
    c.drawString(cx + 4*mm, cy, doc)

y -= (half + 1) * 6*mm + 5*mm

# ── WHY AKHS ──────────────────────────────────────────────────────────────────
c.setFillColor(GREEN)
c.roundRect(10*mm, y - 18*mm, PAGE_W - 20*mm, 21*mm, 2*mm, fill=1, stroke=0)
c.setFillColor(GOLD)
c.setFont("Helvetica-Bold", 10)
c.drawString(14*mm, y - 4*mm, "Why Choose AKHS TRADERS?")
c.setFillColor(WHITE)
c.setFont("Helvetica", 8.5)
points = [
    "PSW Registered Exporter — Official Pakistan export declaration",
    "REAP Certified — Rice Exporters Association of Pakistan member",
    "SGS / COTECNA Inspected — Quality guaranteed at loading",
    "Flexible packing — 25kg or 50kg PP bags, custom branding available",
    "Competitive FOB prices — Direct mill sourcing from Gujranwala & Punjab",
]
px = 14*mm
py = y - 10*mm
for pt in points:
    c.drawString(px, py, f"• {pt}")
    py -= 4.5*mm

y -= 24*mm

# ── CLOSING ───────────────────────────────────────────────────────────────────
c.setFillColor(DARK)
c.setFont("Helvetica", 9)
c.drawString(10*mm, y, "We look forward to doing business with you. Please feel free to contact us for samples, further negotiation, or any queries.")
y -= 6*mm
c.drawString(10*mm, y, "We are ready to proceed immediately upon your confirmation.")
y -= 10*mm

c.setFont("Helvetica-Bold", 10)
c.drawString(10*mm, y, "Syed Muhammad Usama Ali")
y -= 5*mm
c.setFont("Helvetica", 9)
c.drawString(10*mm, y, "Chief Executive Officer — AKHS TRADERS")
y -= 5*mm
c.drawString(10*mm, y, "Phone / WhatsApp: +92-334-0065781")
y -= 5*mm
c.setFillColor(GREEN)
c.drawString(10*mm, y, "PSW Registered Rice Exporter  |  Pakistan")

# ── FOOTER ────────────────────────────────────────────────────────────────────
c.setFillColor(DARK)
c.rect(0, 0, PAGE_W, 10*mm, fill=1, stroke=0)
c.setFillColor(GOLD)
c.setFont("Helvetica", 7)
c.drawCentredString(PAGE_W/2, 3.5*mm,
    "AKHS TRADERS  |  Multan, Pakistan  |  +92-334-0065781  |  Rice Export — Pakistan to Africa & Middle East")

c.save()
print(f"Quotation PDF created: {output_path}")
