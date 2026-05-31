from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.pdfbase.pdfmetrics import stringWidth

W_PT, H_PT = A4  # 595.27 x 841.89 pt

# ── Colours ────────────────────────────────────────────────────────────────────
MAROON   = colors.HexColor('#6B1535')
GOLD     = colors.HexColor('#C9A84C')
GOLD_L   = colors.HexColor('#E8D5A3')
NAVY     = colors.HexColor('#0F1F3D')
WHITE    = colors.white
DARK     = colors.HexColor('#1A1A1A')
MID      = colors.HexColor('#555555')
SHADOW   = colors.HexColor('#00000018')

LOGO  = "/root/.claude/uploads/821548fa-6491-4125-8b13-35cb95ca5b0f/bbf1cd60-1000645012.jpg"
OUT   = "/home/user/Usama-New/AKH_Export_Process_Flowchart.pdf"

MG   = 13*mm          # page margin
CW   = W_PT - 2*MG   # content width  ~169mm
CH   = 22*mm          # card height
AR   = 5*mm           # arrow height
CR   = 7*mm           # circle radius
SP   = CH + AR        # step spacing = 27mm

# ── Step data ─────────────────────────────────────────────────────────────────
STEPS = [
  ('01','ORDER CONFIRMATION',
   'Somali buyer contacts AKH via WhatsApp or email. AKH sends Proforma Invoice with CIF Mogadishu price, product specs, HS codes and payment terms. Buyer confirms.',
   'Proforma Invoice Issued','#E53935'),
  ('02','ADVANCE PAYMENT — 50%',
   'Buyer sends 50% advance via Dahabshiil bank transfer, Western Union or bank TT. AKH confirms receipt and immediately places the production order at the factory.',
   'Payment Confirmed ✓','#F57C00'),
  ('03','FACTORY PRODUCTION — FAISALABAD',
   'Mill begins weaving Macawiis checked cotton, stitching Bed Linen and looming Towels to exact buyer specifications — 100% cotton, correct GSM weight and dimensions.',
   '21–28 Days Production','#F9A825'),
  ('04','AKH QUALITY INSPECTION',
   'AKH team checks every batch: fabric GSM weight, dimensions, stitch count, colour matching and labeling accuracy. All defective pieces are rejected before packing.',
   'AKH Quality Pass Required','#43A047'),
  ('05','BUREAU VERITAS — COC CERTIFICATE',
   'Bureau Veritas inspector visits Karachi warehouse. Verifies quantity, quality and labeling against invoice. Issues Certificate of Conformity — mandatory for Mogadishu customs.',
   'COC Certificate Issued','#00897B'),
  ('06','DOCUMENT PREPARATION',
   'Commercial Invoice, Packing List, Certificate of Origin (Chamber), Insurance Certificate, WeBOC/PSW Export Declaration and Form E bank declaration — all finalised.',
   'All Documents Ready','#1E88E5'),
  ('07','KARACHI PORT — CONTAINER LOADING',
   'Goods loaded into 20ft FCL container at Karachi Port. Container sealed. Bill of Lading issued by Maersk / MSC / CMA CGM. Container number shared with buyer for tracking.',
   'Bill of Lading Issued','#3949AB'),
  ('08','SEA FREIGHT — KARACHI TO MOGADISHU',
   'Maersk Musafir Express departs Karachi. Transit via Salalah Oman hub then direct to Mogadishu Port. Live container tracking available 24/7 on Maersk website.',
   '10–14 Days Direct Shipping','#8E24AA'),
  ('09','MOGADISHU CUSTOMS CLEARANCE',
   "Buyer's clearing agent presents COC + Commercial Invoice + Bill of Lading to Somalia Customs. 10% import duty paid on CIF value. Container released within 3–5 days.",
   '10% Duty on CIF Value','#D81B60'),
  ('10','DELIVERY TO BUYER WAREHOUSE',
   "Container transported to buyer's warehouse in Mogadishu. Goods unloaded and counted. Buyer confirms receipt matches invoice quantity and quality. Delivery complete.",
   'Goods Received ✓','#00ACC1'),
  ('11','FINAL PAYMENT — 50% BALANCE',
   'Buyer transfers remaining 50% balance via Dahabshiil, Western Union or bank TT on receipt of goods. AKH confirms payment received. Transaction 100% complete.',
   'Order Complete ✓','#C9A84C'),
]

PAGE1_STEPS = STEPS[:6]
PAGE2_STEPS = STEPS[6:]

# ── Helpers ───────────────────────────────────────────────────────────────────
def wrap(text, font, size, max_w):
    words = text.split()
    lines, cur = [], ''
    for w in words:
        test = (cur + ' ' + w).strip()
        if stringWidth(test, font, size) <= max_w:
            cur = test
        else:
            if cur: lines.append(cur)
            cur = w
    if cur: lines.append(cur)
    return lines

def border(c):
    c.saveState()
    c.setStrokeColor(GOLD); c.setLineWidth(2)
    c.roundRect(6*mm, 6*mm, W_PT-12*mm, H_PT-12*mm, 3*mm, stroke=1, fill=0)
    c.setStrokeColor(MAROON); c.setLineWidth(0.5)
    c.roundRect(8.5*mm, 8.5*mm, W_PT-17*mm, H_PT-17*mm, 2*mm, stroke=1, fill=0)
    c.restoreState()

def arrow(c, cx, y_top, h):
    c.saveState()
    c.setFillColor(MAROON); c.setStrokeColor(MAROON); c.setLineWidth(1.2)
    c.line(cx, y_top, cx, y_top - h + 2*mm)
    aw = 1.6*mm
    p = c.beginPath()
    p.moveTo(cx, y_top - h)
    p.lineTo(cx - aw, y_top - h + 2.5*mm)
    p.lineTo(cx + aw, y_top - h + 2.5*mm)
    p.close()
    c.drawPath(p, fill=1, stroke=0)
    c.restoreState()

def circle(c, cx, cy, r, col, label):
    c.saveState()
    # Shadow
    c.setFillColor(SHADOW)
    c.circle(cx + 0.6*mm, cy - 0.6*mm, r, fill=1, stroke=0)
    # Circle
    c.setFillColor(col); c.circle(cx, cy, r, fill=1, stroke=0)
    # Label
    c.setFillColor(WHITE); c.setFont('Helvetica-Bold', 8.5)
    c.drawCentredString(cx, cy - 1.5*mm, label)
    c.restoreState()

def step_card(c, num, name, desc, badge, hex_col, x, y_top):
    col = colors.HexColor(hex_col)
    card_x = x + CR*1.7
    card_w = CW - CR*1.7
    cy = y_top - CH/2

    # Card shadow
    c.saveState()
    c.setFillColor(SHADOW)
    c.roundRect(card_x + 0.5*mm, y_top - CH - 0.5*mm, card_w, CH, 3.5*mm, fill=1, stroke=0)
    # Card bg
    c.setFillColor(WHITE)
    c.setStrokeColor(colors.HexColor(hex_col + '55'))
    c.setLineWidth(0.5)
    c.roundRect(card_x, y_top - CH, card_w, CH, 3.5*mm, fill=1, stroke=1)
    # Left colour bar
    c.setFillColor(col)
    c.roundRect(card_x, y_top - CH, 3.5*mm, CH, 1.5*mm, fill=1, stroke=0)
    c.restoreState()

    # Circle icon
    circle(c, x + CR, cy, CR, col, num)

    # Text layout
    tx = card_x + 6*mm
    tw = card_w - 9*mm

    c.saveState()
    # STEP label
    c.setFillColor(col); c.setFont('Helvetica-Bold', 6)
    c.drawString(tx, y_top - 4.5*mm, f'STEP {num}')
    # Name
    c.setFillColor(DARK); c.setFont('Helvetica-Bold', 10.5)
    c.drawString(tx, y_top - 9.5*mm, name)
    # Description
    c.setFillColor(MID); c.setFont('Helvetica', 7.2)
    lines = wrap(desc, 'Helvetica', 7.2, tw)
    for i, ln in enumerate(lines[:2]):
        c.drawString(tx, y_top - 14*mm - i*3.8*mm, ln)
    # Badge
    by = y_top - CH + 2.5*mm
    bw = stringWidth(badge, 'Helvetica-Bold', 6.5) + 6*mm
    c.setFillColor(col)
    c.roundRect(tx, by, bw, 5*mm, 1.5*mm, fill=1, stroke=0)
    c.setFillColor(WHITE); c.setFont('Helvetica-Bold', 6.5)
    c.drawString(tx + 3*mm, by + 1.2*mm, badge)
    c.restoreState()

# ── PAGE HEADERS ──────────────────────────────────────────────────────────────
def page1_header(c):
    hh = 36*mm
    hy = H_PT - MG - hh
    # Background
    c.saveState()
    c.setFillColor(NAVY)
    c.roundRect(MG, hy, CW, hh, 4*mm, fill=1, stroke=0)
    # Maroon overlay strip (left 30%)
    c.setFillColor(MAROON)
    c.roundRect(MG, hy, CW*0.32, hh, 4*mm, fill=1, stroke=0)
    c.rect(MG + CW*0.24, hy, CW*0.08, hh, fill=1, stroke=0)
    # Gold border
    c.setStrokeColor(GOLD); c.setLineWidth(1.5)
    c.roundRect(MG, hy, CW, hh, 4*mm, fill=0, stroke=1)
    # Gold vertical divider
    c.setStrokeColor(GOLD); c.setLineWidth(0.5)
    c.line(MG + CW*0.32, hy + 4*mm, MG + CW*0.32, hy + hh - 4*mm)
    # Logo
    try:
        c.drawImage(LOGO, MG + 3*mm, hy + 4*mm,
                   width=28*mm, height=20*mm,
                   preserveAspectRatio=True, mask='auto')
    except:
        c.setFillColor(GOLD); c.setFont('Helvetica-Bold', 18)
        c.drawString(MG + 5*mm, hy + hh/2 - 5*mm, '🧵')
    # Right side text
    rx = MG + CW*0.34
    c.setFillColor(WHITE); c.setFont('Helvetica-Bold', 17)
    c.drawString(rx, hy + 24*mm, 'FROM ORDER TO YOUR DOOR')
    c.setFillColor(GOLD); c.setFont('Helvetica-Bold', 9.5)
    c.drawString(rx, hy + 17.5*mm, 'AKH LINEN HOUSE  —  Pakistan Direct Textile Exporter')
    c.setFillColor(GOLD_L); c.setFont('Helvetica', 8.5)
    c.drawString(rx, hy + 12*mm, 'Complete Export Process  •  Pakistan Factory to Mogadishu Somalia')
    # Route badge
    bx, by2 = rx, hy + 4*mm
    bw = CW - CW*0.34 - 4*mm
    c.setFillColor(colors.HexColor('#00000035'))
    c.roundRect(bx, by2, bw, 7*mm, 3*mm, fill=1, stroke=0)
    c.setStrokeColor(GOLD); c.setLineWidth(0.5)
    c.roundRect(bx, by2, bw, 7*mm, 3*mm, fill=0, stroke=1)
    route = '  Karachi  ──►  Salalah (Hub)  ──►  Mogadishu Port  '
    c.setFillColor(GOLD); c.setFont('Helvetica-Bold', 7.5)
    c.drawString(bx + 4*mm, by2 + 1.8*mm, route)
    c.restoreState()
    return hy  # returns top of free area below header

def page2_header(c):
    hh = 16*mm
    hy = H_PT - MG - hh
    c.saveState()
    c.setFillColor(MAROON)
    c.roundRect(MG, hy, CW, hh, 3*mm, fill=1, stroke=0)
    c.setStrokeColor(GOLD); c.setLineWidth(1.5)
    c.roundRect(MG, hy, CW, hh, 3*mm, fill=0, stroke=1)
    c.setFillColor(WHITE); c.setFont('Helvetica-Bold', 11)
    c.drawCentredString(W_PT/2, hy + 9.5*mm, 'AKH LINEN HOUSE  —  Export Process (Steps 7–11)')
    c.setFillColor(GOLD); c.setFont('Helvetica', 8)
    c.drawCentredString(W_PT/2, hy + 4*mm, 'Karachi Port  →  Sea Freight  →  Mogadishu Customs  →  Delivery  →  Final Payment')
    c.restoreState()
    return hy

def page_footer(c):
    fh = 16*mm
    fy = MG
    c.saveState()
    c.setFillColor(MAROON)
    c.roundRect(MG, fy, CW, fh, 3*mm, fill=1, stroke=0)
    c.setStrokeColor(GOLD); c.setLineWidth(1.5)
    c.roundRect(MG, fy, CW, fh, 3*mm, fill=0, stroke=1)
    # Left
    c.setFillColor(WHITE); c.setFont('Helvetica-Bold', 9)
    c.drawString(MG + 4*mm, fy + 9.5*mm, 'AKH LINEN HOUSE  |  Pakistan Direct Textile Exporter')
    c.setFillColor(GOLD); c.setFont('Helvetica', 7.5)
    c.drawString(MG + 4*mm, fy + 3.5*mm, 'Macawiis  •  Bed Linen  •  Towels  •  Baati Fabric  •  Prayer Mats')
    # Right
    c.setFillColor(WHITE); c.setFont('Helvetica-Bold', 8.5)
    c.drawRightString(W_PT - MG - 4*mm, fy + 9.5*mm, 'WhatsApp: +92 334 006 5781')
    c.setFillColor(GOLD_L); c.setFont('Helvetica', 7.5)
    c.drawRightString(W_PT - MG - 4*mm, fy + 3.5*mm, 'akhlinenhouse@gmail.com')
    c.restoreState()

# ── START BOX ─────────────────────────────────────────────────────────────────
def start_box(c, y_top):
    bh = 13*mm
    c.saveState()
    c.setFillColor(WHITE)
    c.setStrokeColor(NAVY); c.setLineWidth(1.8)
    c.roundRect(MG, y_top - bh, CW, bh, 3*mm, fill=1, stroke=1)
    # Icon circle
    circle(c, MG + CR, y_top - bh/2, CR*0.85, NAVY, '?')
    c.setFillColor(DARK); c.setFont('Helvetica-Bold', 11)
    c.drawString(MG + CR*2.2, y_top - bh/2 + 2*mm, 'BUYER INQUIRY / ORDER REQUEST')
    c.setFillColor(MID); c.setFont('Helvetica', 7.5)
    c.drawString(MG + CR*2.2, y_top - bh/2 - 3*mm, 'Somali importer contacts AKH Linen House via WhatsApp or Email')
    c.restoreState()
    return y_top - bh

# ── SPLIT ROW ─────────────────────────────────────────────────────────────────
def split_section(c, y_top):
    # Title bar
    th = 8*mm
    c.saveState()
    c.setFillColor(colors.HexColor('#EEE8DA'))
    c.roundRect(MG, y_top - th, CW, th, 2*mm, fill=1, stroke=0)
    c.setFillColor(NAVY); c.setFont('Helvetica-Bold', 8.5)
    c.drawCentredString(W_PT/2, y_top - th + 2.5*mm, 'WHAT HAPPENS NEXT')
    c.restoreState()

    y = y_top - th - 3*mm
    pw = (CW - 4*mm) / 2
    ph = 30*mm

    panels = [
        (MG,         '#43A047', '01', 'REPEAT ORDER BEGINS',
         'Buyer reorders based on market demand. Volume grows. Per-piece price decreases with every new container ordered.'),
        (MG+pw+4*mm, '#6B1535', '02', 'EXCLUSIVE PARTNERSHIP',
         'AKH offers regional exclusivity. Buyer becomes the sole distributor of AKH products in Mogadishu or their market.'),
    ]
    for px, hx, num, name, desc in panels:
        col = colors.HexColor(hx)
        c.saveState()
        c.setFillColor(WHITE)
        c.setStrokeColor(col); c.setLineWidth(1)
        c.roundRect(px, y - ph, pw, ph, 3*mm, fill=1, stroke=1)
        c.setFillColor(col)
        c.roundRect(px, y - ph, pw, 4*mm, 1.5*mm, fill=1, stroke=0)
        c.rect(px, y - ph + 2*mm, pw, 2*mm, fill=1, stroke=0)
        # circle
        circle(c, px + pw/2, y - ph/2 - 2*mm, 9*mm, col, num)
        c.setFillColor(DARK); c.setFont('Helvetica-Bold', 9)
        c.drawCentredString(px + pw/2, y - ph/2 + 8*mm, name)
        c.setFillColor(MID); c.setFont('Helvetica', 7.2)
        lines = wrap(desc, 'Helvetica', 7.2, pw - 6*mm)
        for i, ln in enumerate(lines[:3]):
            c.drawCentredString(px + pw/2, y - ph/2 + 2.5*mm - i*3.8*mm, ln)
        c.restoreState()
    return y - ph

# ── TIMELINE BOX ──────────────────────────────────────────────────────────────
def timeline_box(c, y_top):
    bh = 26*mm
    c.saveState()
    c.setFillColor(WHITE)
    c.setStrokeColor(GOLD); c.setLineWidth(1.5)
    c.setDash(4, 3)
    c.roundRect(MG, y_top - bh, CW, bh, 3*mm, fill=1, stroke=1)
    c.setDash()
    # Title
    c.setFillColor(MID); c.setFont('Helvetica-Bold', 7.5)
    c.drawCentredString(W_PT/2, y_top - 5*mm, 'TOTAL ORDER TO DELIVERY TIMELINE')
    # 3 boxes
    bw = (CW - 16*mm) / 3
    boxes = [
        ('#FFF8E1','#F57C00','28','Days Production'),
        ('#E8F5E9','#43A047','14','Days Shipping'),
        ('#FCE4EC','#E53935','42','Days Total'),
    ]
    for i, (bg, fc, val, lbl) in enumerate(boxes):
        bx = MG + 4*mm + i*(bw + 4*mm)
        by = y_top - bh + 3*mm
        c.setFillColor(colors.HexColor(bg))
        c.roundRect(bx, by, bw, 14*mm, 2*mm, fill=1, stroke=0)
        c.setFillColor(colors.HexColor(fc)); c.setFont('Helvetica-Bold', 18)
        c.drawCentredString(bx + bw/2, by + 6.5*mm, val)
        c.setFillColor(MID); c.setFont('Helvetica', 7)
        c.drawCentredString(bx + bw/2, by + 1.5*mm, lbl)
    # Tagline
    c.setFillColor(MID); c.setFont('Helvetica', 7.5)
    c.setFillColorRGB(0.6,0.6,0.6)
    c.drawCentredString(W_PT/2, y_top - bh + 1.5*mm,
                        'Order today  —  goods arrive in Mogadishu in 6 weeks')
    c.restoreState()
    return y_top - bh

# ══════════════════════════════════════════════════════════════════════════════
# BUILD PDF
# ══════════════════════════════════════════════════════════════════════════════
c = canvas.Canvas(OUT, pagesize=A4)

# ── PAGE 1 ────────────────────────────────────────────────────────────────────
border(c)
header_bottom = page1_header(c)

# Start box
y = header_bottom - 4*mm
y = start_box(c, y)

# Arrow into step 1
arrow_cx = MG + CR
arrow(c, arrow_cx, y, AR)
y -= AR

# Steps 1–6
for num, name, desc, badge, col in PAGE1_STEPS:
    step_card(c, num, name, desc, badge, col, MG, y)
    y -= CH
    if (num, name, desc, badge, col) != PAGE1_STEPS[-1]:
        arrow(c, arrow_cx, y, AR)
        y -= AR

c.showPage()

# ── PAGE 2 ────────────────────────────────────────────────────────────────────
border(c)
header_bottom = page2_header(c)
y = header_bottom - 4*mm

arrow_cx = MG + CR
for i, (num, name, desc, badge, col) in enumerate(PAGE2_STEPS):
    step_card(c, num, name, desc, badge, col, MG, y)
    y -= CH
    arrow(c, arrow_cx, y, AR)
    y -= AR

# What happens next
y -= 2*mm
split_y = split_section(c, y)

# Timeline
y = split_y - 4*mm
arrow(c, W_PT/2, y, AR)
y -= AR
timeline_box(c, y)

# Footer
page_footer(c)

c.save()
print("Export Process Flowchart PDF generated successfully!")
