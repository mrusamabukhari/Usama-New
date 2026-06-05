from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.lib import colors

output_path = "/home/user/Usama-New/AKHS_Exporter_50_Questions.pdf"

PAGE_W, PAGE_H = A4

GREEN  = colors.HexColor("#1a7a3c")
DARK   = colors.HexColor("#1a2e1a")
GOLD   = colors.HexColor("#c8a200")
WHITE  = colors.white
LIGHT  = colors.HexColor("#e8f5ec")
GREY   = colors.HexColor("#f0f0f0")
RED    = colors.HexColor("#c0392b")

steps = [
    {
        "step": "STEP 1",
        "title": "Registration & Certificates",
        "subtitle": "Ask about the correct order, documents, costs and mistakes",
        "questions": [
            ("1", "Which registrations did you do FIRST — what is the correct order?",
             "PSW first? REAP first? NTN first? What is the right sequence?"),
            ("2", "How long did PSW registration take — any problems?",
             "What documents did they reject? What mistakes should I avoid?"),
            ("3", "REAP membership — is it really mandatory or can you skip it early?",
             "How much is the annual fee? Who to contact in Gujranwala/Karachi?"),
            ("4", "Do you need TDAP registration before first shipment or after?",
             "Is it useful or just extra paperwork?"),
            ("5", "Phytosanitary Certificate — who issues it, how many days, what is the cost?",
             "Which DPP office — Lahore or Karachi? Any rejections experienced?"),
            ("6", "Certificate of Origin — FPCCI or Chamber of Commerce — which does your buyer accept?",
             "Some Middle East buyers want FPCCI specifically."),
            ("7", "SGS / COTECNA quality inspection — does your buyer demand it or is it optional?",
             "Who pays — you or buyer? How much does it cost per container?"),
            ("8", "Fumigation Certificate — which company do you use, how much per container?",
             "Phosphine fumigation — how many days before loading?"),
            ("9", "Do you have a sample of your complete document set for one shipment?",
             "Ask to see: Invoice, Packing List, B/L, COO, Phyto, Fumigation, SGS — all together."),
            ("10", "Did you face any problem at Karachi port customs — what was the reason?",
             "Learn from his mistakes before you make your own."),
        ]
    },
    {
        "step": "STEP 2",
        "title": "Bank / LC / Payment",
        "subtitle": "Ask about ESFCA, LC process, payment terms and cash flow",
        "questions": [
            ("1", "Which bank did you open your ESFCA account in — which bank is best?",
             "HBL? MCB? UBL? Which one processes export LCs fastest?"),
            ("2", "When LC comes to your bank — what is the first thing you do?",
             "Do you check LC terms yourself or give it straight to bank officer?"),
            ("3", "What LC discrepancies did you face — what mistakes cause LC rejection?",
             "Wrong description, wrong HS code, wrong port name — learn his errors."),
            ("4", "How many days does your bank take to negotiate the LC after shipment?",
             "When do you actually receive the money in your account?"),
            ("5", "Do your buyers pay LC at sight or 30/60/90 days deferred?",
             "Middle East = mostly LC at sight. DRC = sometimes 30–60 days."),
            ("6", "Do you accept TT (bank transfer) from any buyer or only LC?",
             "New exporters often get burned by TT — ask his opinion."),
            ("7", "SBP 50% rule — how do you manage it practically?",
             "50% must stay in ESFCA — how does he handle cash flow?"),
            ("8", "What is your bank's export LC processing fee per shipment?",
             "Banks charge for LC advising, negotiation, SWIFT — know the costs."),
            ("9", "Did you ever have a buyer refuse to pay — how did you protect yourself?",
             "Confirmed LC? Freight forwarder holding B/L? What protection method?"),
            ("10", "How much working capital did you need for your first container?",
             "Mill payment before shipment — how many days gap before you get paid?"),
        ]
    },
    {
        "step": "STEP 3",
        "title": "Finding Buyers",
        "subtitle": "Ask about where to find real buyers, verify them and build relationships",
        "questions": [
            ("1", "Where did you find your first buyer — Alibaba, WhatsApp, trade fair or personal contact?",
             "Most Pakistan rice exporters find first buyer through personal network — ask his story."),
            ("2", "How do you verify a buyer is real and not a scammer?",
             "What do you check — company registration, physical address, references?"),
            ("3", "Do you use a broker/agent in DRC or Middle East — or direct buyer only?",
             "Brokers take 1–3% commission — is it worth it for a new exporter?"),
            ("4", "Which city in DRC has the most rice importers — Kinshasa or Matadi?",
             "Where to find serious buyers with import license."),
            ("5", "Which WhatsApp groups or trade networks do you use for rice buyers?",
             "Ask him to add you — this is gold for a new exporter."),
            ("6", "How many containers did your first buyer order — what was the minimum?",
             "1 container? 5 containers? What is realistic for a first deal?"),
            ("7", "Do your buyers visit Pakistan to inspect rice — or they trust samples?",
             "Some DRC buyers come to Lahore/Karachi — be prepared."),
            ("8", "How do you send rice samples — courier cost, how much quantity?",
             "DHL/FedEx to Kinshasa — how much does it cost, how many kg sample?"),
            ("9", "What is the biggest complaint your DRC/Middle East buyers had about your rice?",
             "Moisture? Broken %? Foreign matter? Color? Learn before you ship."),
            ("10", "Can you introduce me to one of your buyers or give me a reference contact?",
             "If he trusts you — this one question can change everything."),
        ]
    },
    {
        "step": "STEP 4",
        "title": "Mill / Supplier Deals",
        "subtitle": "Ask about selecting mills, payment terms, agreements and quality control",
        "questions": [
            ("1", "How do you find a reliable mill — what is your selection criteria?",
             "Capacity? ISO? SGS approved? Export experience? Ask his checklist."),
            ("2", "Do you work with one mill only or multiple mills — which is better for a new exporter?",
             "Single mill = easier relationship. Multiple mills = price competition."),
            ("3", "What is the payment terms with your mill — advance, 50/50, or credit?",
             "Most mills demand 50% advance — does he negotiate credit after trust builds?"),
            ("4", "How many days advance do you place order before shipment date?",
             "Rice processing takes 7–15 days — when to book mill vs when to book container?"),
            ("5", "What is written in your mill agreement — what clauses protect you?",
             "Quality guarantee? Penalty for delay? Replacement of rejected lot?"),
            ("6", "If SGS inspection fails at mill — who bears the cost, you or mill?",
             "This is critical — get it in writing before first order."),
            ("7", "What moisture % and broken % do you specify in mill agreement?",
             "Buyer wants max 13.5% moisture, max 25% broken — does mill guarantee this?"),
            ("8", "Do you visit the mill yourself before each shipment or trust them blindly?",
             "How many times did rice quality differ from what was agreed?"),
            ("9", "Which mills in Gujranwala or Karachi do you recommend for IRRI-6 export quality?",
             "This one answer can save you months of searching."),
            ("10", "What is the biggest problem you faced with a mill — and how did you solve it?",
             "Short weight? Wrong grade? Late delivery? Learn his worst experience."),
        ]
    },
    {
        "step": "STEP 5",
        "title": "Shipping / Freight",
        "subtitle": "Ask about shipping lines, clearing agents, costs and real transit experience",
        "questions": [
            ("1", "Which shipping line do you use for DRC — MSC or Maersk or someone else?",
             "Who gives best rate and fastest sailing for Karachi to Matadi?"),
            ("2", "Do you book container directly with shipping line or through freight forwarder?",
             "Direct = cheaper. Forwarder = easier for beginners — ask his recommendation."),
            ("3", "What is the current freight rate Karachi to Matadi per 20ft container?",
             "2025 rate — this changes monthly, get real number from him."),
            ("4", "Who is your clearing agent in Karachi — can you recommend one?",
             "A trusted clearing agent reference is worth more than anything — ask directly."),
            ("5", "How much does clearing agent charge per container — all inclusive?",
             "Port charges + GD filing + documentation — total cost in PKR."),
            ("6", "How many days before sailing date do you need to submit documents to port?",
             "Cut-off dates for booking, VGM, documentation — what is the timeline?"),
            ("7", "Do you take Marine Insurance — which company, how much per container?",
             "Insurance cost + is it mandatory for DRC buyers or optional?"),
            ("8", "CFR or FOB — which Incoterm do your DRC buyers prefer?",
             "CFR = you arrange freight. FOB = buyer arranges. Which is safer for new exporter?"),
            ("9", "How long does Karachi to Matadi actually take — real experience not Google?",
             "Official = 32–37 days. Real experience may differ — vessel delays, port congestion."),
            ("10", "What was your worst shipping problem — container delay, port hold, document rejection?",
             "His worst day = your biggest lesson."),
        ]
    },
]

c = canvas.Canvas(output_path, pagesize=A4)

def draw_header(c, page_num):
    # Top bar
    c.setFillColor(DARK)
    c.rect(0, PAGE_H - 22*mm, PAGE_W, 22*mm, fill=1, stroke=0)
    c.setFillColor(GOLD)
    c.rect(0, PAGE_H - 23.5*mm, PAGE_W, 1.5*mm, fill=1, stroke=0)

    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 13)
    c.drawString(15*mm, PAGE_H - 13*mm, "AKHS TRADERS — 50 Questions to Ask an Experienced Exporter")
    c.setFont("Helvetica", 8)
    c.setFillColor(GOLD)
    c.drawRightString(PAGE_W - 15*mm, PAGE_H - 13*mm, f"Page {page_num}")

def draw_footer(c):
    c.setFillColor(DARK)
    c.rect(0, 0, PAGE_W, 10*mm, fill=1, stroke=0)
    c.setFillColor(GOLD)
    c.setFont("Helvetica", 7)
    c.drawCentredString(PAGE_W/2, 3.5*mm, "AKHS TRADERS  |  Syed Muhammad Usama Ali  |  CEO  |  +92-334-0065781  |  Rice Export — Pakistan to DRC & Middle East")

def draw_cover(c):
    # Background
    c.setFillColor(DARK)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)

    # Gold top bar
    c.setFillColor(GOLD)
    c.rect(0, PAGE_H - 8*mm, PAGE_W, 8*mm, fill=1, stroke=0)
    c.rect(0, 0, PAGE_W, 8*mm, fill=1, stroke=0)

    # Green center band
    c.setFillColor(GREEN)
    c.rect(0, PAGE_H/2 - 55*mm, PAGE_W, 110*mm, fill=1, stroke=0)

    # Wheat icon area
    c.setFillColor(GOLD)
    c.setFont("Helvetica-Bold", 48)
    c.drawCentredString(PAGE_W/2, PAGE_H/2 + 60*mm, "AKHS TRADERS")

    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(PAGE_W/2, PAGE_H/2 + 45*mm, "Rice Export — Pakistan to DRC & Middle East")

    # Main title
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 32)
    c.drawCentredString(PAGE_W/2, PAGE_H/2 + 15*mm, "50 Questions")

    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(PAGE_W/2, PAGE_H/2 - 2*mm, "to Ask an Experienced")

    c.setFillColor(GOLD)
    c.setFont("Helvetica-Bold", 22)
    c.drawCentredString(PAGE_W/2, PAGE_H/2 - 18*mm, "Rice Exporter")

    # Subtitle
    c.setFillColor(WHITE)
    c.setFont("Helvetica", 11)
    c.drawCentredString(PAGE_W/2, PAGE_H/2 - 35*mm, "A complete guide for new exporters — Registration, Bank, Buyers, Mills & Shipping")

    # Steps summary
    steps_text = ["Step 1: Registration & Certificates", "Step 2: Bank / LC / Payment",
                  "Step 3: Finding Buyers", "Step 4: Mill / Supplier Deals", "Step 5: Shipping / Freight"]
    y = PAGE_H/2 - 60*mm
    for s in steps_text:
        c.setFillColor(GOLD)
        c.circle(PAGE_W/2 - 55*mm, y + 2*mm, 1.5*mm, fill=1, stroke=0)
        c.setFillColor(WHITE)
        c.setFont("Helvetica", 10)
        c.drawString(PAGE_W/2 - 50*mm, y, s)
        y -= 8*mm

    # CEO
    c.setFillColor(GOLD)
    c.setFont("Helvetica-Bold", 9)
    c.drawCentredString(PAGE_W/2, 15*mm, "Prepared by: Syed Muhammad Usama Ali  |  CEO, AKHS TRADERS  |  +92-334-0065781")

    c.showPage()

def draw_step_page(c, step_data, page_num):
    draw_header(c, page_num)
    draw_footer(c)

    y = PAGE_H - 32*mm

    # Step banner
    c.setFillColor(GREEN)
    c.rect(12*mm, y - 10*mm, PAGE_W - 24*mm, 14*mm, fill=1, stroke=0)
    c.setFillColor(GOLD)
    c.rect(12*mm, y - 10*mm, 4*mm, 14*mm, fill=1, stroke=0)

    c.setFillColor(GOLD)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(19*mm, y - 3*mm, step_data["step"])

    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 13)
    c.drawString(38*mm, y - 3*mm, step_data["title"])

    y -= 14*mm

    # Subtitle
    c.setFillColor(colors.HexColor("#555555"))
    c.setFont("Helvetica-Oblique", 8.5)
    c.drawString(14*mm, y, step_data["subtitle"])

    y -= 8*mm

    for q_num, question, hint in step_data["questions"]:
        # Question box
        box_h = 18*mm
        c.setFillColor(GREY)
        c.roundRect(12*mm, y - box_h + 3*mm, PAGE_W - 24*mm, box_h, 2*mm, fill=1, stroke=0)

        # Number circle
        c.setFillColor(GREEN)
        c.circle(20*mm, y - box_h/2 + 3*mm, 4*mm, fill=1, stroke=0)
        c.setFillColor(WHITE)
        c.setFont("Helvetica-Bold", 8)
        c.drawCentredString(20*mm, y - box_h/2 + 1.5*mm, q_num)

        # Question text
        c.setFillColor(DARK)
        c.setFont("Helvetica-Bold", 9)
        # Wrap long question
        max_w = PAGE_W - 24*mm - 16*mm
        words = question.split()
        lines = []
        line = ""
        for word in words:
            test = (line + " " + word).strip()
            if c.stringWidth(test, "Helvetica-Bold", 9) < max_w:
                line = test
            else:
                lines.append(line)
                line = word
        if line:
            lines.append(line)

        q_y = y - 5*mm
        for l in lines[:2]:
            c.drawString(27*mm, q_y, l)
            q_y -= 4*mm

        # Hint text
        c.setFillColor(colors.HexColor("#666666"))
        c.setFont("Helvetica-Oblique", 7.5)
        hint_words = hint.split()
        hint_line = ""
        hint_lines = []
        for word in hint_words:
            test = (hint_line + " " + word).strip()
            if c.stringWidth(test, "Helvetica-Oblique", 7.5) < max_w:
                hint_line = test
            else:
                hint_lines.append(hint_line)
                hint_line = word
        if hint_line:
            hint_lines.append(hint_line)
        for hl in hint_lines[:1]:
            c.drawString(27*mm, q_y, hl)

        y -= box_h + 2*mm

    c.showPage()

def draw_bonus_page(c, page_num):
    draw_header(c, page_num)
    draw_footer(c)

    y = PAGE_H - 35*mm

    # Title
    c.setFillColor(DARK)
    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(PAGE_W/2, y, "BONUS — The Most Important Question")
    y -= 12*mm

    # Gold box
    c.setFillColor(GOLD)
    c.roundRect(20*mm, y - 30*mm, PAGE_W - 40*mm, 35*mm, 3*mm, fill=1, stroke=0)
    c.setFillColor(DARK)
    c.setFont("Helvetica-Bold", 12)
    c.drawCentredString(PAGE_W/2, y - 8*mm, '"Bhai, main naya exporter hoon —')
    c.drawCentredString(PAGE_W/2, y - 16*mm, 'aap ki jagah hote toh pehla container')
    c.drawCentredString(PAGE_W/2, y - 24*mm, 'kis country, kis buyer, kis mill se karte?"')
    y -= 42*mm

    c.setFillColor(colors.HexColor("#333333"))
    c.setFont("Helvetica", 10)
    c.drawCentredString(PAGE_W/2, y, "Translation: If you were me, which country, which buyer, which mill")
    c.drawCentredString(PAGE_W/2, y - 7*mm, "would you choose for your first container?")
    y -= 22*mm

    c.setFillColor(GREEN)
    c.setFont("Helvetica-Bold", 11)
    c.drawCentredString(PAGE_W/2, y, "This one question gets you his entire strategy in one answer.")
    y -= 20*mm

    # Summary table
    c.setFillColor(DARK)
    c.setFont("Helvetica-Bold", 13)
    c.drawCentredString(PAGE_W/2, y, "Summary — All 5 Steps")
    y -= 10*mm

    rows = [
        ("Step 1", "Registration & Certificates", "10 Questions"),
        ("Step 2", "Bank / LC / Payment", "10 Questions"),
        ("Step 3", "Finding Buyers", "10 Questions"),
        ("Step 4", "Mill / Supplier Deals", "10 Questions"),
        ("Step 5", "Shipping / Freight", "10 Questions"),
        ("TOTAL", "Everything a New Exporter Needs", "50 Questions"),
    ]

    col_x = [20*mm, 55*mm, 155*mm]
    row_h = 10*mm

    for i, (step, topic, count) in enumerate(rows):
        if i == 5:
            c.setFillColor(DARK)
        elif i % 2 == 0:
            c.setFillColor(LIGHT)
        else:
            c.setFillColor(WHITE)
        c.rect(col_x[0], y - row_h + 2*mm, PAGE_W - 40*mm, row_h, fill=1, stroke=0)

        if i == 5:
            c.setFillColor(GOLD)
            c.setFont("Helvetica-Bold", 10)
        else:
            c.setFillColor(GREEN)
            c.setFont("Helvetica-Bold", 9)
        c.drawString(col_x[0] + 3*mm, y - 4*mm, step)

        if i == 5:
            c.setFillColor(WHITE)
        else:
            c.setFillColor(DARK)
        c.setFont("Helvetica" if i < 5 else "Helvetica-Bold", 9)
        c.drawString(col_x[1], y - 4*mm, topic)

        c.setFillColor(GREEN if i < 5 else GOLD)
        c.setFont("Helvetica-Bold", 9)
        c.drawRightString(col_x[2] + 25*mm, y - 4*mm, count)

        y -= row_h + 1*mm

    y -= 15*mm
    c.setFillColor(GREEN)
    c.roundRect(20*mm, y - 18*mm, PAGE_W - 40*mm, 22*mm, 3*mm, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 11)
    c.drawCentredString(PAGE_W/2, y - 4*mm, "AKHS TRADERS — Rice Export from Pakistan to DRC & Middle East")
    c.setFont("Helvetica", 9)
    c.drawCentredString(PAGE_W/2, y - 11*mm, "Syed Muhammad Usama Ali  |  CEO  |  +92-334-0065781  |  PSW Registered Exporter")

    c.showPage()

# Generate PDF
draw_cover(c)

page = 2
for step_data in steps:
    draw_step_page(c, step_data, page)
    page += 1

draw_bonus_page(c, page)

c.save()
print(f"PDF created: {output_path}")
