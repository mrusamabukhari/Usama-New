from reportlab.lib.pagesizes import landscape
from reportlab.lib import colors
from reportlab.lib.units import cm, mm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT

# Business card size: 90mm x 55mm (standard)
CARD_W = 90*mm
CARD_H = 55*mm

GREEN  = colors.HexColor("#1a7a3c")
DARK   = colors.HexColor("#1a2e1a")
GOLD   = colors.HexColor("#c8a200")
WHITE  = colors.white
LIGHT  = colors.HexColor("#e8f5ec")
GREY   = colors.HexColor("#f5f5f5")

from reportlab.pdfgen import canvas
from reportlab.lib.units import mm

def draw_card_front(c, x, y):
    """Draw front of business card at position (x,y) - bottom-left corner"""
    w, h = 90*mm, 55*mm

    # Background
    c.setFillColor(DARK)
    c.rect(x, y, w, h, fill=1, stroke=0)

    # Green left bar
    c.setFillColor(GREEN)
    c.rect(x, y, 18*mm, h, fill=1, stroke=0)

    # Gold accent line
    c.setFillColor(GOLD)
    c.rect(x+18*mm, y+h-1.5*mm, w-18*mm, 1.5*mm, fill=1, stroke=0)
    c.rect(x+18*mm, y, w-18*mm, 1*mm, fill=1, stroke=0)

    # Vertical text on green bar — RICE EXPORTER
    c.saveState()
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 7)
    c.translate(x+9*mm, y+h/2)
    c.rotate(90)
    c.drawCentredString(0, 0, "RICE  EXPORTER")
    c.restoreState()

    # Star/wheat symbol on green bar
    c.setFillColor(GOLD)
    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(x+9*mm, y+h-12*mm, "🌾")

    # Company name
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(x+22*mm, y+h-12*mm, "AKHS TRADERS")

    # Gold underline
    c.setStrokeColor(GOLD)
    c.setLineWidth(1)
    c.line(x+22*mm, y+h-14*mm, x+86*mm, y+h-14*mm)

    # Tagline
    c.setFillColor(GOLD)
    c.setFont("Helvetica-Oblique", 7)
    c.drawString(x+22*mm, y+h-18*mm, "Premium Rice Export — Pakistan to Middle East & Central Africa")

    # CEO name
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(x+22*mm, y+h-25*mm, "Syed Muhammad Usama Ali")

    c.setFillColor(GOLD)
    c.setFont("Helvetica", 7.5)
    c.drawString(x+22*mm, y+h-30*mm, "Chief Executive Officer")

    # Divider
    c.setStrokeColor(colors.HexColor("#2d5a3d"))
    c.setLineWidth(0.5)
    c.line(x+22*mm, y+h-33*mm, x+86*mm, y+h-33*mm)

    # Phone
    c.setFillColor(WHITE)
    c.setFont("Helvetica", 7.5)
    c.drawString(x+22*mm, y+h-39*mm, "📞  +92-334-0065781")

    # Export label
    c.setFillColor(colors.HexColor("#aaaaaa"))
    c.setFont("Helvetica", 7)
    c.drawString(x+22*mm, y+h-45*mm, "IRRI-6 · Basmati · Sella · Long Grain White Rice")

    # Registered
    c.setFillColor(GOLD)
    c.setFont("Helvetica-Bold", 6.5)
    c.drawString(x+22*mm, y+5*mm, "PSW Registered Exporter  ·  Pakistan")


def draw_card_back(c, x, y):
    """Draw back of business card"""
    w, h = 90*mm, 55*mm

    # Background green
    c.setFillColor(GREEN)
    c.rect(x, y, w, h, fill=1, stroke=0)

    # Dark overlay strip top
    c.setFillColor(DARK)
    c.rect(x, y+h-12*mm, w, 12*mm, fill=1, stroke=0)

    # Gold lines
    c.setFillColor(GOLD)
    c.rect(x, y+h-12.8*mm, w, 0.8*mm, fill=1, stroke=0)
    c.rect(x, y, w, 0.8*mm, fill=1, stroke=0)

    # Company name on dark strip
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(x+w/2, y+h-9*mm, "AKHS TRADERS")

    # Wheat emoji
    c.setFont("Helvetica-Bold", 11)
    c.drawCentredString(x+w/2, y+h-19*mm, "🌾")

    # Products
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 8)
    c.drawCentredString(x+w/2, y+h-26*mm, "We Export:")

    c.setFont("Helvetica", 7.5)
    c.drawCentredString(x+w/2, y+h-32*mm, "IRRI-6 Long Grain White Rice  ·  Basmati Rice")
    c.drawCentredString(x+w/2, y+h-37*mm, "Sella (Parboiled) Rice  ·  Super Kernel Rice")

    # Markets
    c.setFillColor(GOLD)
    c.setFont("Helvetica-Bold", 7.5)
    c.drawCentredString(x+w/2, y+h-44*mm, "Markets: DRC · Congo · Middle East · East Africa")

    # Bottom
    c.setFillColor(WHITE)
    c.setFont("Helvetica", 6.5)
    c.drawCentredString(x+w/2, y+4*mm, "Quality Certified  ·  SGS Inspected  ·  Fumigated")


# ── PAGE LAYOUT ───────────────────────────────────────────────────────────────
# A4 page, print 2 front + 2 back cards
from reportlab.lib.pagesizes import A4

output_path = "/home/user/Usama-New/AKHS_Traders_Business_Card.pdf"
c = canvas.Canvas(output_path, pagesize=A4)
page_w, page_h = A4

# Page 1 — FRONT of cards (2x2 grid)
c.setFillColor(colors.HexColor("#dddddd"))
c.rect(0, 0, page_w, page_h, fill=1, stroke=0)

# Title
c.setFillColor(DARK)
c.setFont("Helvetica-Bold", 11)
c.drawCentredString(page_w/2, page_h-15*mm, "AKHS TRADERS — Business Card  |  FRONT SIDE")
c.setFont("Helvetica", 8)
c.setFillColor(colors.HexColor("#555555"))
c.drawCentredString(page_w/2, page_h-21*mm, "Cut along the card borders — Standard size 90mm × 55mm")

# Draw 4 front cards (2 columns, 2 rows)
margin_x = (page_w - 2*90*mm - 6*mm) / 2
margin_y = 40*mm

positions = [
    (margin_x,              margin_y + 55*mm + 8*mm),
    (margin_x + 90*mm+6*mm, margin_y + 55*mm + 8*mm),
    (margin_x,              margin_y),
    (margin_x + 90*mm+6*mm, margin_y),
]

for (px, py) in positions:
    # Card shadow
    c.setFillColor(colors.HexColor("#bbbbbb"))
    c.rect(px+1*mm, py-1*mm, 90*mm, 55*mm, fill=1, stroke=0)
    draw_card_front(c, px, py)

c.showPage()

# Page 2 — BACK of cards
c.setFillColor(colors.HexColor("#dddddd"))
c.rect(0, 0, page_w, page_h, fill=1, stroke=0)

c.setFillColor(DARK)
c.setFont("Helvetica-Bold", 11)
c.drawCentredString(page_w/2, page_h-15*mm, "AKHS TRADERS — Business Card  |  BACK SIDE")
c.setFont("Helvetica", 8)
c.setFillColor(colors.HexColor("#555555"))
c.drawCentredString(page_w/2, page_h-21*mm, "Print this page on reverse side of Page 1")

for (px, py) in positions:
    c.setFillColor(colors.HexColor("#bbbbbb"))
    c.rect(px+1*mm, py-1*mm, 90*mm, 55*mm, fill=1, stroke=0)
    draw_card_back(c, px, py)

c.showPage()

# Page 3 — Single large preview (front)
c.setFillColor(colors.HexColor("#eeeeee"))
c.rect(0, 0, page_w, page_h, fill=1, stroke=0)

c.setFillColor(DARK)
c.setFont("Helvetica-Bold", 12)
c.drawCentredString(page_w/2, page_h-20*mm, "PREVIEW — Front Side (2× enlarged)")

# Draw enlarged front card centered
scale = 2.2
ew = 90*mm * scale
eh = 55*mm * scale
ex = (page_w - ew) / 2
ey = (page_h - eh) / 2 - 10*mm

c.saveState()
c.translate(ex, ey)
c.scale(scale, scale)
draw_card_front(c, 0, 0)
c.restoreState()

c.showPage()

# Page 4 — Single large preview (back)
c.setFillColor(colors.HexColor("#eeeeee"))
c.rect(0, 0, page_w, page_h, fill=1, stroke=0)

c.setFillColor(DARK)
c.setFont("Helvetica-Bold", 12)
c.drawCentredString(page_w/2, page_h-20*mm, "PREVIEW — Back Side (2× enlarged)")

c.saveState()
c.translate(ex, ey)
c.scale(scale, scale)
draw_card_back(c, 0, 0)
c.restoreState()

c.save()
print("Business card PDF created: AKHS_Traders_Business_Card.pdf")
