from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.graphics.shapes import Drawing, Path, Polygon, Line, Circle, Rect
from reportlab.graphics import renderPDF

CARD_W = 90*mm
CARD_H = 55*mm

# Colors
NAVY      = colors.HexColor("#0d2147")
NAVY_DARK = colors.HexColor("#071530")
GOLD      = colors.HexColor("#c8a200")
WHITE     = colors.white
OCEAN     = colors.HexColor("#0a1f4e")
LAND      = colors.HexColor("#1a3a6e")
LAND2     = colors.HexColor("#1e4080")
GRID_COL  = colors.HexColor("#1a3060")
TEXT_COL  = colors.HexColor("#e8f0ff")
GOLD_L    = colors.HexColor("#e6c840")

def lon_lat_to_xy(lon, lat, w, h):
    """Convert lon/lat to card x/y (Mercator)"""
    x = (lon + 180) / 360 * w
    y = (lat + 90) / 180 * h
    return x, y

def ll(lon, lat, w=CARD_W, h=CARD_H):
    return lon_lat_to_xy(lon, lat, w, h)

def draw_world_map_bg(c, ox, oy):
    """Draw world map background on card"""
    w, h = CARD_W, CARD_H

    # Ocean background
    c.setFillColor(OCEAN)
    c.roundRect(ox, oy, w, h, 3*mm, fill=1, stroke=0)

    # Clip to card shape
    p = c.beginPath()
    p.roundRect(ox, oy, w, h, 3*mm)
    c.clipPath(p, stroke=0)

    # ── Latitude/Longitude grid ───────────────────────────────────────────────
    c.setStrokeColor(GRID_COL)
    c.setLineWidth(0.3)
    # Longitude lines every 30 degrees
    for lon in range(-180, 181, 30):
        x, _ = ll(lon, 0)
        c.line(ox+x, oy, ox+x, oy+h)
    # Latitude lines every 30 degrees
    for lat in range(-90, 91, 30):
        _, y = ll(0, lat)
        c.line(ox, oy+y, ox+w, oy+y)

    # Equator slightly brighter
    c.setStrokeColor(colors.HexColor("#243870"))
    c.setLineWidth(0.5)
    _, eq_y = ll(0, 0)
    c.line(ox, oy+eq_y, ox+w, oy+eq_y)

    # ── CONTINENTS ────────────────────────────────────────────────────────────
    def draw_land(points, color=LAND):
        c.setFillColor(color)
        c.setStrokeColor(colors.HexColor("#2a4a80"))
        c.setLineWidth(0.3)
        path = c.beginPath()
        pts = [ll(lon, lat) for lon, lat in points]
        path.moveTo(ox+pts[0][0], oy+pts[0][1])
        for px, py in pts[1:]:
            path.lineTo(ox+px, oy+py)
        path.close()
        c.drawPath(path, fill=1, stroke=1)

    # ── NORTH AMERICA ─────────────────────────────────────────────────────────
    draw_land([
        (-168,72),(-155,72),(-140,70),(-130,68),(-120,65),(-110,63),
        (-95,62),(-85,65),(-80,62),(-75,58),(-65,55),(-60,50),
        (-65,44),(-70,42),(-72,40),(-75,38),(-80,32),(-82,28),
        (-85,24),(-88,20),(-90,16),(-85,12),(-83,10),(-78,8),
        (-75,8),(-78,12),(-80,16),(-82,20),(-85,22),(-88,26),
        (-95,30),(-100,28),(-105,25),(-110,24),(-115,22),(-118,20),
        (-115,26),(-120,32),(-122,36),(-124,40),(-125,48),(-130,55),
        (-140,58),(-148,60),(-155,58),(-160,62),(-165,68),(-168,72)
    ], LAND2)

    # Alaska
    draw_land([
        (-168,72),(-165,70),(-160,68),(-155,65),(-150,62),(-145,60),
        (-140,58),(-145,60),(-150,62),(-155,65),(-160,68),(-165,70),(-168,72)
    ], LAND)

    # ── GREENLAND ─────────────────────────────────────────────────────────────
    draw_land([
        (-55,82),(-35,83),(-20,80),(-15,76),(-18,72),(-25,68),
        (-35,65),(-45,62),(-52,62),(-55,65),(-58,70),(-58,76),(-55,82)
    ], LAND)

    # ── SOUTH AMERICA ─────────────────────────────────────────────────────────
    draw_land([
        (-80,12),(-75,12),(-65,12),(-60,8),(-52,5),(-50,2),
        (-48,-2),(-45,-5),(-38,-8),(-35,-10),(-35,-15),(-38,-20),
        (-40,-22),(-42,-22),(-45,-23),(-48,-26),(-50,-28),(-52,-32),
        (-52,-34),(-55,-38),(-58,-42),(-60,-48),(-65,-52),(-68,-55),
        (-66,-55),(-64,-52),(-62,-48),(-60,-42),(-58,-38),(-55,-34),
        (-52,-30),(-55,-25),(-58,-20),(-62,-15),(-65,-10),(-70,-5),
        (-75,0),(-78,5),(-80,8),(-80,12)
    ], LAND2)

    # ── EUROPE ────────────────────────────────────────────────────────────────
    draw_land([
        (-10,36),(-6,36),(0,38),(5,42),(8,44),(10,44),(14,46),
        (18,48),(22,50),(25,52),(28,55),(25,58),(22,60),(18,60),
        (15,58),(12,56),(10,55),(8,55),(5,52),(2,50),(0,48),
        (-2,46),(-5,44),(-8,42),(-10,40),(-10,36)
    ], LAND)

    # Scandanavia
    draw_land([
        (5,58),(8,58),(10,60),(12,62),(14,65),(16,68),(18,70),
        (20,70),(22,68),(25,68),(28,70),(28,68),(25,65),(22,62),
        (20,60),(18,58),(15,57),(12,57),(8,58),(5,58)
    ], LAND)

    # UK
    draw_land([
        (-5,50),(-3,50),(0,51),(2,52),(0,54),(-2,55),(-5,56),
        (-6,58),(-4,58),(-2,57),(0,56),(2,54),(0,52),(-2,51),(-5,50)
    ], LAND)

    # ── AFRICA ────────────────────────────────────────────────────────────────
    draw_land([
        (-18,16),(-16,12),(-15,10),(-14,8),(-12,6),(-8,4),
        (-5,4),(-2,4),(2,4),(5,4),(8,4),(10,2),(12,0),
        (14,-2),(16,-4),(18,-6),(20,-8),(22,-10),(25,-12),
        (28,-14),(30,-16),(32,-18),(34,-20),(35,-22),(36,-20),
        (38,-16),(40,-12),(42,-8),(44,-4),(42,0),(40,4),(42,8),
        (44,12),(42,14),(38,16),(35,18),(30,20),(25,22),(20,24),
        (15,24),(10,20),(5,18),(0,16),(-5,16),(-10,18),(-15,20),
        (-18,20),(-18,16)
    ], LAND2)

    # Madagascar
    draw_land([
        (44,-12),(46,-14),(48,-16),(50,-20),(48,-24),(46,-26),
        (44,-24),(43,-20),(43,-16),(44,-12)
    ], LAND)

    # ── ASIA ──────────────────────────────────────────────────────────────────
    draw_land([
        (25,38),(28,40),(30,42),(35,44),(40,46),(45,48),(50,50),
        (55,52),(60,54),(65,56),(70,58),(75,60),(80,62),(85,64),
        (90,65),(95,63),(100,60),(105,58),(110,55),(115,52),(120,50),
        (125,48),(130,46),(135,44),(140,42),(142,40),(140,38),(138,36),
        (140,34),(138,32),(135,30),(130,28),(125,25),(120,22),(118,20),
        (115,18),(112,16),(108,14),(104,12),(102,10),(100,8),(102,6),
        (104,4),(106,2),(108,0),(105,-2),(102,-4),(100,-2),(98,2),
        (95,5),(90,8),(85,10),(80,12),(75,10),(70,8),(65,8),
        (60,10),(55,12),(50,14),(45,14),(40,12),(38,10),(36,12),
        (34,16),(32,18),(30,20),(28,24),(26,28),(25,32),(24,36),
        (25,38)
    ], LAND2)

    # India subcontinent
    draw_land([
        (68,24),(72,22),(75,20),(78,18),(80,16),(82,14),(80,12),
        (78,10),(76,8),(78,6),(80,8),(82,10),(80,12),(78,14),
        (75,16),(72,18),(70,20),(68,22),(68,24)
    ], LAND)

    # Japan
    draw_land([
        (130,32),(132,34),(134,36),(136,38),(138,40),(140,42),(142,44),
        (140,44),(138,42),(136,40),(134,38),(132,36),(130,34),(130,32)
    ], LAND)

    # ── AUSTRALIA ─────────────────────────────────────────────────────────────
    draw_land([
        (114,-22),(116,-20),(118,-18),(122,-18),(125,-16),(128,-14),
        (132,-12),(136,-12),(140,-14),(142,-16),(145,-18),(148,-20),
        (150,-22),(152,-24),(152,-26),(150,-28),(148,-30),(148,-32),
        (146,-35),(144,-38),(142,-38),(140,-36),(138,-35),(136,-34),
        (134,-32),(130,-32),(128,-34),(126,-34),(122,-34),(118,-32),
        (115,-28),(113,-26),(114,-22)
    ], LAND)

    # New Zealand
    draw_land([
        (166,-46),(168,-44),(170,-42),(172,-40),(174,-38),(172,-36),
        (170,-38),(168,-40),(166,-42),(166,-46)
    ], LAND)

    # ── DRC HIGHLIGHT ─────────────────────────────────────────────────────────
    c.setFillColor(colors.HexColor("#c8a200"))
    c.setStrokeColor(colors.HexColor("#ffd700"))
    c.setLineWidth(0.5)
    # DRC roughly 17-30E, 5N to 13S
    drc_pts = [
        (17,5),(20,5),(24,4),(28,4),(30,2),(32,0),(31,-3),
        (30,-6),(30,-10),(28,-13),(25,-13),(22,-11),(20,-10),
        (18,-8),(16,-6),(16,-2),(17,2),(17,5)
    ]
    path = c.beginPath()
    pts = [ll(lon, lat) for lon, lat in drc_pts]
    path.moveTo(ox+pts[0][0], oy+pts[0][1])
    for px, py in pts[1:]:
        path.lineTo(ox+px, oy+py)
    path.close()
    c.drawPath(path, fill=1, stroke=1)

    # ── PAKISTAN HIGHLIGHT ────────────────────────────────────────────────────
    c.setFillColor(colors.HexColor("#22c55e"))
    c.setStrokeColor(colors.HexColor("#4ade80"))
    c.setLineWidth(0.5)
    pak_pts = [
        (60,24),(62,26),(65,28),(68,28),(70,26),(72,28),
        (74,32),(72,34),(70,36),(68,37),(66,36),(64,36),
        (62,34),(60,32),(58,30),(60,28),(60,24)
    ]
    path = c.beginPath()
    pts = [ll(lon, lat) for lon, lat in pak_pts]
    path.moveTo(ox+pts[0][0], oy+pts[0][1])
    for px, py in pts[1:]:
        path.lineTo(ox+px, oy+py)
    path.close()
    c.drawPath(path, fill=1, stroke=1)

    # ── ROUTE LINE: Pakistan → DRC ────────────────────────────────────────────
    # Karachi: 67E, 25N → Matadi: 12E, -6S
    c.setStrokeColor(GOLD_L)
    c.setLineWidth(0.8)
    c.setDash([2, 2])
    # Draw curved route via Red Sea / Indian Ocean / around Africa
    route = [
        (67, 25), (62, 20), (55, 15), (50, 12), (44, 12),
        (42, 8), (40, 4), (38, 0), (32, -5), (25, -8),
        (18, -8), (14, -6), (12, -6)
    ]
    pts = [ll(lon, lat) for lon, lat in route]
    p = c.beginPath()
    p.moveTo(ox+pts[0][0], oy+pts[0][1])
    for px, py in pts[1:]:
        p.lineTo(ox+px, oy+py)
    c.drawPath(p, fill=0, stroke=1)
    c.setDash([])

    # Dots at Pakistan and DRC
    c.setFillColor(colors.HexColor("#22c55e"))
    pk_x, pk_y = ll(67, 25)
    c.circle(ox+pk_x, oy+pk_y, 1.2*mm, fill=1, stroke=0)

    c.setFillColor(GOLD_L)
    drc_x, drc_y = ll(22, -4)
    c.circle(ox+drc_x, oy+drc_y, 1.2*mm, fill=1, stroke=0)

    # Small labels near dots
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 4.5)
    c.drawString(ox+pk_x+1.5*mm, oy+pk_y, "PAK")
    c.drawString(ox+drc_x+1.5*mm, oy+drc_y, "DRC")


def draw_card(c, ox, oy):
    draw_world_map_bg(c, ox, oy)

    w, h = CARD_W, CARD_H

    # Semi-transparent dark overlay (bottom 60% for text readability)
    c.setFillColor(colors.HexColor("#07112e"))
    p = c.beginPath()
    p.moveTo(ox, oy)
    p.lineTo(ox+w, oy)
    p.lineTo(ox+w, oy+h*0.52)
    p.lineTo(ox, oy+h*0.52)
    p.close()
    c.setFillAlpha(0.72)
    c.drawPath(p, fill=1, stroke=0)
    c.setFillAlpha(1.0)

    # Top overlay for company name
    c.setFillColor(colors.HexColor("#07112e"))
    p2 = c.beginPath()
    p2.moveTo(ox, oy+h*0.72)
    p2.lineTo(ox+w, oy+h*0.72)
    p2.lineTo(ox+w, oy+h)
    p2.lineTo(ox, oy+h)
    p2.close()
    c.setFillAlpha(0.55)
    c.drawPath(p2, fill=1, stroke=0)
    c.setFillAlpha(1.0)

    # Gold top bar
    c.setFillColor(GOLD)
    c.rect(ox, oy+h-1.8*mm, w, 1.8*mm, fill=1, stroke=0)

    # Gold bottom bar
    c.rect(ox, oy, w, 1.5*mm, fill=1, stroke=0)

    # ── COMPANY NAME ──────────────────────────────────────────────────────────
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 17)
    c.drawString(ox+5*mm, oy+h-10*mm, "AKHS TRADERS")

    # Gold underline
    c.setStrokeColor(GOLD)
    c.setLineWidth(0.8)
    c.line(ox+5*mm, oy+h-11.5*mm, ox+w-5*mm, oy+h-11.5*mm)

    # ── TAGLINE ───────────────────────────────────────────────────────────────
    c.setFillColor(GOLD_L)
    c.setFont("Helvetica-Bold", 7)
    c.drawString(ox+5*mm, oy+h-15.5*mm, "EXPORT TO MIDDLE EAST / CENTRAL AFRICA")

    # ── PRODUCT LINE ──────────────────────────────────────────────────────────
    c.setFillColor(colors.HexColor("#b0c4de"))
    c.setFont("Helvetica", 6.5)
    c.drawString(ox+5*mm, oy+h-19.5*mm, "Long Grain Rice  ·  IRRI-6  ·  Sella  ·  Basmati  ·  Super Kernel")

    # ── BOTTOM INFO ───────────────────────────────────────────────────────────
    # CEO
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 8)
    c.drawString(ox+5*mm, oy+9.5*mm, "Syed Muhammad Usama Ali")
    c.setFillColor(GOLD_L)
    c.setFont("Helvetica", 6.5)
    c.drawString(ox+5*mm, oy+6.5*mm, "Chief Executive Officer")

    # Phone — right aligned
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 8)
    c.drawRightString(ox+w-5*mm, oy+9.5*mm, "+92-334-0065781")
    c.setFillColor(GOLD_L)
    c.setFont("Helvetica", 6.5)
    c.drawRightString(ox+w-5*mm, oy+6.5*mm, "📞  WhatsApp / Call")

    # PSW badge
    c.setFillColor(colors.HexColor("#1a4a2e"))
    c.roundRect(ox+5*mm, oy+2*mm, 28*mm, 3.5*mm, 1*mm, fill=1, stroke=0)
    c.setFillColor(GOLD_L)
    c.setFont("Helvetica-Bold", 5.5)
    c.drawString(ox+6*mm, oy+3*mm, "✓  PSW Registered Exporter · Pakistan")


def draw_card_back(c, ox, oy):
    draw_world_map_bg(c, ox, oy)

    w, h = CARD_W, CARD_H

    # Full overlay
    c.setFillColor(colors.HexColor("#07112e"))
    c.setFillAlpha(0.65)
    rp = c.beginPath()
    rp.roundRect(ox, oy, w, h, 3*mm)
    c.drawPath(rp, fill=1, stroke=0)
    c.setFillAlpha(1.0)

    # Gold bars
    c.setFillColor(GOLD)
    c.rect(ox, oy+h-1.8*mm, w, 1.8*mm, fill=1, stroke=0)
    c.rect(ox, oy, w, 1.5*mm, fill=1, stroke=0)

    # Company centered
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(ox+w/2, oy+h-10*mm, "AKHS TRADERS")

    c.setStrokeColor(GOLD)
    c.setLineWidth(0.8)
    c.line(ox+10*mm, oy+h-12*mm, ox+w-10*mm, oy+h-12*mm)

    c.setFillColor(GOLD_L)
    c.setFont("Helvetica-Bold", 7)
    c.drawCentredString(ox+w/2, oy+h-16*mm, "🌾  RICE EXPORTER  🌾")

    # Products
    c.setFillColor(colors.HexColor("#b0c4de"))
    c.setFont("Helvetica", 6.5)
    c.drawCentredString(ox+w/2, oy+h-21*mm, "IRRI-6 Long Grain  ·  Basmati  ·  Sella (Parboiled)")
    c.drawCentredString(ox+w/2, oy+h-26*mm, "Super Kernel  ·  1121  ·  25kg / 50kg PP Bags")

    # Markets
    c.setFillColor(GOLD_L)
    c.setFont("Helvetica-Bold", 6.5)
    c.drawCentredString(ox+w/2, oy+h-32*mm, "Markets: DRC · Congo · UAE · Saudi Arabia · East Africa")

    # Route note
    c.setFillColor(colors.HexColor("#6a8ab0"))
    c.setFont("Helvetica-Oblique", 6)
    c.drawCentredString(ox+w/2, oy+h-37*mm, "Karachi → Matadi Port (32–37 days)")

    # Bottom
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 7)
    c.drawCentredString(ox+w/2, oy+8*mm, "SGS Certified  ·  Fumigated  ·  REAP Member")

    c.setFillColor(GOLD_L)
    c.setFont("Helvetica", 6)
    c.drawCentredString(ox+w/2, oy+5*mm, "Quality Rice from Pakistan's Gujranwala Belt")


# ── GENERATE PDF ─────────────────────────────────────────────────────────────
output = "/home/user/Usama-New/AKHS_Traders_WorldMap_Card.pdf"
c = canvas.Canvas(output, pagesize=A4)
page_w, page_h = A4

# Background
c.setFillColor(colors.HexColor("#1a1a2e"))
c.rect(0, 0, page_w, page_h, fill=1, stroke=0)

# Title
c.setFillColor(colors.HexColor("#c8a200"))
c.setFont("Helvetica-Bold", 11)
c.drawCentredString(page_w/2, page_h-16*mm, "AKHS TRADERS — Business Card with World Map")
c.setFillColor(colors.HexColor("#888888"))
c.setFont("Helvetica", 8)
c.drawCentredString(page_w/2, page_h-22*mm, "FRONT SIDE  ·  Cut along card borders  ·  Standard 90mm × 55mm")

margin_x = (page_w - 2*CARD_W - 6*mm) / 2
margin_y = 42*mm

positions = [
    (margin_x,            margin_y + CARD_H + 8*mm),
    (margin_x+CARD_W+6*mm, margin_y + CARD_H + 8*mm),
    (margin_x,            margin_y),
    (margin_x+CARD_W+6*mm, margin_y),
]

for px, py in positions:
    draw_card(c, px, py)

c.showPage()

# Page 2 — Back
c.setFillColor(colors.HexColor("#1a1a2e"))
c.rect(0, 0, page_w, page_h, fill=1, stroke=0)
c.setFillColor(colors.HexColor("#c8a200"))
c.setFont("Helvetica-Bold", 11)
c.drawCentredString(page_w/2, page_h-16*mm, "AKHS TRADERS — Business Card with World Map")
c.setFillColor(colors.HexColor("#888888"))
c.setFont("Helvetica", 8)
c.drawCentredString(page_w/2, page_h-22*mm, "BACK SIDE  ·  Print on reverse of Page 1")

for px, py in positions:
    draw_card_back(c, px, py)

c.showPage()

# Page 3 — Large preview front
c.setFillColor(colors.HexColor("#1a1a2e"))
c.rect(0, 0, page_w, page_h, fill=1, stroke=0)
c.setFillColor(colors.HexColor("#c8a200"))
c.setFont("Helvetica-Bold", 11)
c.drawCentredString(page_w/2, page_h-16*mm, "PREVIEW — Front Side (2.2× enlarged)")

scale = 2.2
ew = CARD_W * scale
eh = CARD_H * scale
ex = (page_w - ew) / 2
ey = (page_h - eh) / 2 - 8*mm

c.saveState()
c.translate(ex, ey)
c.scale(scale, scale)
draw_card(c, 0, 0)
c.restoreState()

c.showPage()

# Page 4 — Large preview back
c.setFillColor(colors.HexColor("#1a1a2e"))
c.rect(0, 0, page_w, page_h, fill=1, stroke=0)
c.setFillColor(colors.HexColor("#c8a200"))
c.setFont("Helvetica-Bold", 11)
c.drawCentredString(page_w/2, page_h-16*mm, "PREVIEW — Back Side (2.2× enlarged)")

c.saveState()
c.translate(ex, ey)
c.scale(scale, scale)
draw_card_back(c, 0, 0)
c.restoreState()

c.save()
print("Done: AKHS_Traders_WorldMap_Card.pdf")
