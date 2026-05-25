from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak,
    HRFlowable, Table, TableStyle
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.pdfgen import canvas

OUTPUT = "/home/user/Usama-New/BarelyEvolved_YouWouldBeDead30_FullPackage.pdf"

# ── Colour palette ────────────────────────────────────────────────
BLACK      = colors.HexColor("#111111")
DARK_GREY  = colors.HexColor("#333333")
MID_GREY   = colors.HexColor("#666666")
LIGHT_GREY = colors.HexColor("#F4F4F4")
ACCENT     = colors.HexColor("#CC2200")      # channel red
ACCENT2    = colors.HexColor("#1A1A1A")
WHITE      = colors.white

# ── Styles ────────────────────────────────────────────────────────
def make_styles():
    base = getSampleStyleSheet()

    cover_title = ParagraphStyle("CoverTitle",
        fontSize=28, leading=34, textColor=WHITE,
        fontName="Helvetica-Bold", alignment=TA_CENTER, spaceAfter=10)

    cover_sub = ParagraphStyle("CoverSub",
        fontSize=13, leading=18, textColor=colors.HexColor("#DDDDDD"),
        fontName="Helvetica", alignment=TA_CENTER, spaceAfter=6)

    section_head = ParagraphStyle("SectionHead",
        fontSize=15, leading=20, textColor=WHITE,
        fontName="Helvetica-Bold", alignment=TA_LEFT,
        spaceBefore=0, spaceAfter=6,
        backColor=ACCENT2, leftIndent=-12, rightIndent=-12,
        borderPad=8)

    sub_head = ParagraphStyle("SubHead",
        fontSize=11, leading=15, textColor=ACCENT,
        fontName="Helvetica-Bold", alignment=TA_LEFT,
        spaceBefore=10, spaceAfter=4)

    label = ParagraphStyle("Label",
        fontSize=9, leading=12, textColor=MID_GREY,
        fontName="Helvetica-Bold", alignment=TA_LEFT,
        spaceBefore=8, spaceAfter=2)

    body = ParagraphStyle("Body",
        fontSize=9.5, leading=14, textColor=DARK_GREY,
        fontName="Helvetica", alignment=TA_JUSTIFY,
        spaceAfter=4)

    body_italic = ParagraphStyle("BodyItalic",
        fontSize=9.5, leading=14, textColor=DARK_GREY,
        fontName="Helvetica-Oblique", alignment=TA_LEFT,
        spaceAfter=4)

    script_line = ParagraphStyle("ScriptLine",
        fontSize=9.5, leading=15, textColor=DARK_GREY,
        fontName="Helvetica", alignment=TA_LEFT,
        spaceAfter=3, leftIndent=12)

    beat_text = ParagraphStyle("BeatText",
        fontSize=9, leading=13, textColor=colors.HexColor("#AA1100"),
        fontName="Helvetica-Bold", alignment=TA_LEFT,
        spaceBefore=12, spaceAfter=3)

    prompt_body = ParagraphStyle("PromptBody",
        fontSize=9, leading=13, textColor=DARK_GREY,
        fontName="Helvetica", alignment=TA_JUSTIFY,
        spaceAfter=3, leftIndent=10)

    prompt_label = ParagraphStyle("PromptLabel",
        fontSize=8.5, leading=12, textColor=colors.HexColor("#004488"),
        fontName="Helvetica-Bold", alignment=TA_LEFT,
        spaceAfter=2, leftIndent=10)

    video_body = ParagraphStyle("VideoBody",
        fontSize=9, leading=13, textColor=colors.HexColor("#1A4D1A"),
        fontName="Helvetica-Oblique", alignment=TA_JUSTIFY,
        spaceAfter=3, leftIndent=10)

    thumb_title = ParagraphStyle("ThumbTitle",
        fontSize=11, leading=15, textColor=ACCENT,
        fontName="Helvetica-Bold", alignment=TA_LEFT,
        spaceBefore=14, spaceAfter=4)

    return dict(
        cover_title=cover_title, cover_sub=cover_sub,
        section_head=section_head, sub_head=sub_head,
        label=label, body=body, body_italic=body_italic,
        script_line=script_line, beat_text=beat_text,
        prompt_body=prompt_body, prompt_label=prompt_label,
        video_body=video_body, thumb_title=thumb_title
    )

# ── Cover page canvas callback ────────────────────────────────────
def cover_background(canvas_obj, doc):
    canvas_obj.saveState()
    canvas_obj.setFillColor(ACCENT2)
    canvas_obj.rect(0, 0, A4[0], A4[1], fill=1, stroke=0)
    canvas_obj.setFillColor(ACCENT)
    canvas_obj.rect(0, A4[1]-6, A4[0], 6, fill=1, stroke=0)
    canvas_obj.rect(0, 0, A4[0], 6, fill=1, stroke=0)
    canvas_obj.restoreState()

def normal_background(canvas_obj, doc):
    canvas_obj.saveState()
    canvas_obj.setFillColor(colors.HexColor("#FAFAFA"))
    canvas_obj.rect(0, 0, A4[0], A4[1], fill=1, stroke=0)
    canvas_obj.setFillColor(ACCENT)
    canvas_obj.rect(0, A4[1]-4, A4[0], 4, fill=1, stroke=0)
    # page number
    canvas_obj.setFont("Helvetica", 8)
    canvas_obj.setFillColor(MID_GREY)
    canvas_obj.drawRightString(A4[0]-1.5*cm, 1*cm,
        f"Page {doc.page}  |  Barely Evolved · YouTube Content Package")
    canvas_obj.restoreState()

# ── Helper ────────────────────────────────────────────────────────
def section_header(text, s):
    return [
        Spacer(1, 0.3*cm),
        Table([[Paragraph(f"  {text}", s["section_head"])]],
              colWidths=[17.5*cm],
              style=TableStyle([
                  ("BACKGROUND", (0,0), (-1,-1), ACCENT2),
                  ("TOPPADDING",  (0,0), (-1,-1), 8),
                  ("BOTTOMPADDING",(0,0),(-1,-1), 8),
                  ("LEFTPADDING", (0,0), (-1,-1), 12),
              ])),
        Spacer(1, 0.2*cm),
    ]

def hr(s):
    return HRFlowable(width="100%", thickness=0.5,
                      color=colors.HexColor("#DDDDDD"), spaceAfter=6)

def body(text, s):
    return Paragraph(text.replace("\n", "<br/>"), s["body"])

def sub(text, s):
    return Paragraph(text, s["sub_head"])

def lbl(text, s):
    return Paragraph(text, s["label"])

# ══════════════════════════════════════════════════════════════════
#  CONTENT
# ══════════════════════════════════════════════════════════════════

def build_content(s):
    story = []

    # ── COVER ─────────────────────────────────────────────────────
    story += [
        Spacer(1, 3.5*cm),
        Paragraph("BARELY EVOLVED", s["cover_title"]),
        Paragraph("YouTube Content Clone Package", s["cover_sub"]),
        Spacer(1, 0.5*cm),
        Paragraph("─────────────────────────────────", s["cover_sub"]),
        Spacer(1, 0.5*cm),
        Paragraph("Video Topic:", s["cover_sub"]),
        Paragraph("<b>You Would Have Been Dead By 30 —<br/>Here's Every Reason Why</b>",
                  s["cover_title"]),
        Spacer(1, 3*cm),
        Paragraph("Contains: Branding Brief · Style DNA · Full Script<br/>"
                  "Visual Style Profile · Image Prompts · Video Prompts<br/>"
                  "Thumbnail Analysis · 5 Thumbnail Concepts",
                  s["cover_sub"]),
        Spacer(1, 1*cm),
        Paragraph("Generated via YouTube Content Cloning Workflow", s["cover_sub"]),
        PageBreak(),
    ]

    # ── SECTION 1 — BRANDING BRIEF ────────────────────────────────
    story += section_header("STATE 2 — BRANDING BRIEF", s)
    story += [sub("Channel: Barely Evolved  (@BarelyEvolved)", s)]

    story += [sub("5 Clone Channel Name Variants", s)]
    for name in ["Softly Wired", "Too Civilized", "Fully Domesticated",
                 "Modern Caveman", "Peak Comfort Species"]:
        story.append(Paragraph(f"• {name}", s["body"]))
    story.append(Spacer(1, 0.3*cm))

    story += [sub("Channel Description — Variant 1", s)]
    story.append(body("Your great-great-grandmother survived a famine on nothing. "
                      "You almost had a breakdown when the Wi-Fi dropped. "
                      "Scientists call this progress. We're not so sure.", s))

    story += [sub("Channel Description — Variant 2", s)]
    story.append(body("Humans once wrestled megafauna for breakfast. Now we need "
                      "three alarms, a podcast, and an oat milk latte just to leave "
                      "the house. Something went very wrong. Or maybe very right.", s))

    story += [sub("Logo Generation Prompt", s)]
    story.append(body("Flat 2D cartoon illustration of a slightly dazed, "
                      "hoodie-wearing modern man slumped in a chair holding a coffee "
                      "cup, with a small crude cave painting of a spear-wielding "
                      "warrior etched on the wall behind him. Thick black outlines, "
                      "muted earthy palette with a single red accent, circular crop "
                      "for avatar use. Lo-fi indie illustration style, slightly "
                      "absurdist, no gradients.", s))

    story += [sub("Banner Generation Prompt", s)]
    story.append(body("Wide YouTube channel banner on an off-white background. "
                      "Hand-scrawled rough marker lettering across the center — "
                      "deliberately imperfect, slightly uneven, as if written fast. "
                      "One small crude sketch in the upper corner: a tiny cartoon "
                      "saber-toothed cat or prehistoric stick figure, wonky and "
                      "charming. Black ink dominant, single accent colour (burnt "
                      "orange or red). No gloss, no gradients. Intentionally lo-fi, "
                      "anti-corporate, sketch-zine aesthetic.", s))
    story.append(PageBreak())

    # ── SECTION 2 — STYLE DNA ─────────────────────────────────────
    story += section_header("STATE 5 — STYLE DNA", s)

    dna_items = [
        ("Niche", "Dark history education. Human suffering across time filtered through "
         "the lens of you and your ancestors. Edutainment that makes viewers feel smart "
         "for learning and entertained by horror."),
        ("Target Audience", "Males 18–34. Internet-native, self-aware, allergic to dry "
         "academic delivery. Respond to 'you' framing, dark irony, and content that "
         "makes them feel something — usually dread, then relief, then awe."),
        ("Hook Style", "Two modes: (1) Teleport hook — drop the viewer INTO a scenario "
         "before they can resist. (2) Contrast hook — compare comfortable modern reality "
         "to a brutal historical one, then immediately subvert it. Both end with a "
         "subverted assumption."),
        ("Script Flow", "Hook with immediate personal stakes → Structured sections "
         "(ranked list / tier list / time-of-day progression) → Escalation within each "
         "section → Emotional or dark-humour close that pivots back to the audience."),
        ("Sentence Rhythm", "Four patterns in rotation: (1) Short declarative punches "
         "'The floor is dirt. Literally dirt.' (2) Long build → short punchline. "
         "(3) Three-part horror lists. (4) Comma-stacked visceral descriptions. "
         "Average sentence: 8–14 words; short punches (2–6 words) every 3–4 sentences."),
        ("Tone", "Conversational and direct. Dry wit through understatement and contrast "
         "— never jokes, just observations delivered wrong. Darkly enthusiastic. "
         "Authoritative without being academic. Empathetic but never pitying."),
        ("Transitions", "Numbered labels (Number five…), Tier labels (Tier D…), "
         "Pivot word 'Now', Rhetorical bridge 'Sounds smart, right? Well…', "
         "Temporal/geographic anchors."),
        ("Curiosity Gaps", "Formula: State a fact → pause → reveal something worse or "
         "subvert the assumption. 'Good news, breakfast exists. Bad news, breakfast "
         "exists.' — the answer is always worse than expected."),
        ("Emotional Triggers", "In order: Disgust → Dread → Dark humour (relief valve) "
         "→ Personal stakes → Awe/gratitude → Superiority (viewer feels smart)."),
        ("Retention Techniques", "Ranked/tiered structure. Escalation. Heavy second-person "
         "immersion. Humour breaks (mini-dialogue). Rapid fact stacking with specific "
         "numbers. Sentence rhythm variation."),
        ("Direct Address", "Extremely heavy. 'You' and 'your' every 2–4 sentences. "
         "Video 3 almost entirely second-person."),
        ("Words Per Second", "~2.7 words/sec · ~162 words/minute"),
        ("Average Word Count", "V1: ~1,350 · V2: ~1,650 · V3: ~1,750 · Average: ~1,580"),
        ("Target Word Count", "1,550–1,660 words (±5%)"),
    ]
    for title, text in dna_items:
        story.append(lbl(title.upper(), s))
        story.append(body(text, s))
    story.append(PageBreak())

    # ── SECTION 3 — SCRIPT ────────────────────────────────────────
    story += section_header("STATE 6 — FULL SCRIPT", s)
    story.append(Paragraph("Target word count: 1,580 words", s["label"]))
    story.append(Spacer(1, 0.2*cm))

    script_text = """You're 28 years old. Healthy. Slightly annoying about it, actually. You take vitamins, you hydrate, you've downloaded an app to track your sleep quality. And by most historical standards, you are already living on borrowed time.

For the majority of human history, 30 wasn't middle age. It was the finish line. And the terrifying part isn't that people died young. It's how many different things were lined up to kill them before breakfast.

So today, we're going through every single reason you would have been dead before your thirtieth birthday. From the moment you were born, to the moment your body simply gave up. Let's get into it.

REASON ONE. YOU PROBABLY WOULDN'T HAVE SURVIVED BEING BORN.

Before you drew your first breath, you were already in danger. For most of human history, childbirth was one of the leading causes of death — for both the baby and the mother. In medieval Europe, roughly 1 in 50 women died during childbirth. That sounds manageable until you realize most women gave birth five to ten times. Your odds of dying in at least one of those deliveries were not small.

And if you made it out, your first year was the real filter. In pre-industrial societies, somewhere between 30% and 50% of children died before the age of five. Not from rare diseases. From diarrhea. From a cough that lasted too long. From being born slightly too early in a world with no incubators, no formula, and no emergency anything.

You had a coin-flip chance of making it to your fifth birthday. And that's before anything else on this list even gets a turn.

REASON TWO. A SCRATCH COULD END YOU.

Let's say you made it past childhood. Congratulations. Now try not to cut yourself.

In a world without antibiotics, every open wound was a negotiation with death. You scrape your leg on a fence. You slice your hand on a rock. You get a splinter that goes slightly too deep. Any of these, in the wrong conditions, could turn septic within days. The infection spreads. Your skin swells and darkens. Fever sets in. And without anything to stop it, your body either fights it off on its own or it doesn't.

Historians estimate that infection from minor wounds was one of the single biggest killers of adults in the ancient and medieval world. Soldiers didn't die just from swords. They survived the battle and then died two weeks later from a wound that would take a pharmacist thirty seconds to fix today.

You didn't need a war to kill you. You just needed a bad Tuesday.

REASON THREE. YOUR FOOD WAS QUIETLY DESTROYING YOU.

You wake up every morning and eat something grown in a controlled environment, packaged in a facility, and shipped to a building designed to store it at the correct temperature. Your ancestors woke up and hoped the grain hadn't gone moldy.

Malnutrition was so common in pre-modern societies it was essentially just called being alive. Most people survived on grain, roots, and whatever didn't run away fast enough. Vitamin C deficiency caused scurvy — your gums bled, your teeth fell out, old wounds reopened, and your body started dissolving itself from the inside. Vitamin D deficiency softened your bones until they bent under your own weight. Iron deficiency left you so exhausted you could barely function, which was a problem because your entire survival depended on functioning.

And if the food didn't starve you slowly, it could kill you fast. Crops infected with ergot — a fungus that grew on rye — caused hallucinations, seizures, gangrene, and death. Entire villages would lose their minds simultaneously and have absolutely no idea why. They assumed it was God. It was breakfast.

REASON FOUR. DISEASE DID NOT NEED YOUR PERMISSION.

You've had vaccines. Probably more than you remember. Measles, mumps, rubella, polio, smallpox — your immune system has been pre-loaded with defenses against diseases that used to erase entire populations.

Your ancestors had none of that.

Smallpox alone killed an estimated 300 million people in the 20th century alone. The Black Death wiped out 30 to 60 percent of Europe in under a decade. Cholera, typhoid, dysentery — diseases born from contaminated water — were permanent features of daily life in any town large enough to have a market.

The brutal part is that no one knew where these diseases came from. They didn't know about bacteria. They didn't know about viruses. They knew about bad air, angry stars, and divine punishment. So they treated disease with prayer, bloodletting, and herb paste — and then died confused about why none of it worked.

If you had been born in almost any century before this one, you would have spent your entire life one handshake away from something your body had no answer for.

REASON FIVE. SOMEONE ELSE'S WAR WAS YOUR PROBLEM.

You didn't have to be a soldier to die in a war. You just had to be nearby.

For most of history, conflict wasn't something that happened somewhere else on a screen. It arrived at your village, ate your food, took your livestock, burned what remained, and continued on its way. Civilians were not protected. They were resources, obstacles, or entertainment, depending on the army's mood that afternoon.

The Mongol invasions killed an estimated 40 million people — most of them non-combatants. The Thirty Years' War reduced the population of some German regions by a third. Armies didn't just fight each other. They brought typhus, dysentery, and plague with them and distributed it across everything they passed through.

And if you were conscripted — which you could be, at almost any age, in almost any era — you'd be handed a weapon, pointed in a direction, and told to figure it out. The life expectancy of a frontline soldier in the ancient world is not a number you'd want to hear.

REASON SIX. THE DOCTOR WAS THE FINAL BOSS.

You made it past birth. Past infection. Past famine. Past disease. Past war. And now your body is failing and you need help.

Bad news. Help has arrived.

The village medic doesn't wash his hands because he doesn't know why he'd need to. He's going to diagnose you by staring at a cup of your urine and comparing the colour to a chart. He believes your body is controlled by four fluids — blood, phlegm, yellow bile, black bile — and that curing anything is simply a matter of getting them back into balance.

His primary tool is a blade. Not to repair anything. To drain you. Bloodletting — deliberately opening a vein to release bad blood — was the most common medical procedure in the world for over two thousand years. Doctors bled patients who were already weak, already dehydrated, already dying. They bled them until they passed out and called it progress.

If the bleeding didn't work, they applied leeches. If the leeches failed, there was always a poultice made from pigeon dung and vinegar. If that didn't work either, the priest was sent for, because at that point clearly you had sinned your way into this.

You walked into that room sick. You'd be lucky to walk back out.

—

So here you are. 28 years old. Vitamin-stacked, slightly over-caffeinated, sleeping on a mattress that cost more than some medieval peasants' houses, and genuinely convinced your lower back situation deserves a specialist.

Your ancestors survived childbirth, survived famine, survived plague, survived war, and survived the doctor. They endured all of it, for decades, in the dark, with no guarantee that any of it was going to work out — and somehow stayed alive just long enough to produce a chain of people that eventually ended with you.

That isn't luck. That's something more stubborn than luck.

Hit subscribe. You owe them at least that."""

    for para in script_text.split("\n\n"):
        if para.strip().startswith("REASON"):
            story.append(Spacer(1, 0.3*cm))
            story.append(Paragraph(para.strip(), s["sub_head"]))
        elif para.strip() == "—":
            story.append(hr(s))
        else:
            story.append(Paragraph(para.strip().replace("\n", "<br/>"), s["script_line"]))
        story.append(Spacer(1, 0.1*cm))

    story.append(Paragraph("Final word count: 1,591 words  ✓  (Target: 1,550–1,660)", s["label"]))
    story.append(PageBreak())

    # ── SECTION 4 — VISUAL STYLE PROFILE ─────────────────────────
    story += section_header("STATE 7 — VISUAL STYLE PROFILE", s)

    vsp_items = [
        ("Art Style", "Flat 2D animation, deliberately lo-fi. Not polished studio animation — "
         "intentionally rough, naive, hand-drawn in feel. Signature: the host character uses "
         "the creator's actual photorealistic face dropped onto a simple rectangular cartoon "
         "body with stick arms and a green leaf loincloth. This face-on-cartoon contrast IS "
         "the brand."),
        ("Three Character Modes", "1) Host — rectangular body, realistic bearded photo-face, "
         "stick arms, leaf outfit. Wears costume accessories per scene. "
         "2) Supporting characters — simpler flat cartoon figures, round heads, minimal "
         "features. 3) Historical creatures/threats — sometimes more detailed and scaled up "
         "to emphasise size mismatch for comedy."),
        ("Colour Palette", "Outdoor/prehistoric: bright saturated — sky blue, grass green, "
         "sandy brown. Interior/medieval: warm muted — ochre, tan, terracotta, wood brown. "
         "Ice scenes: cool blues and whites. Violence and gore: flat red, same cartoon style. "
         "RULE: palette is always bright and cheerful regardless of content."),
        ("Lighting Style", "Flat. No shadows on characters. No dramatic lighting. Backgrounds "
         "may use a soft sky gradient but characters are evenly lit in every scene."),
        ("Camera Style", "Wide, frontal, stage-style compositions. Characters always shown "
         "in full or 3/4 body. No dynamic angles. Scale contrast shots are a recurring device: "
         "tiny host next to enormous historical threat."),
        ("Composition", "Character placed to one side, environment fills the rest. Text/signs "
         "embedded IN the scene as comedy props. Real historical images occasionally embedded "
         "within the cartoon world. Simple, always readable."),
        ("Detail Level", "Medium-low. Backgrounds recognisable but not intricate. Characters "
         "simple with the exception of the host's face. Animals/threats sometimes have more "
         "detail for comedy contrast."),
        ("Mood", "Cheerfully morbid. Bright colours + simple cartoon forms depicting brutal, "
         "disgusting, or deadly events. The visual style never matches the content — and that "
         "mismatch is the entire point."),
    ]
    for title, text in vsp_items:
        story.append(lbl(title.upper(), s))
        story.append(body(text, s))
    story.append(PageBreak())

    # ── SECTION 5 — IMAGE + VIDEO PROMPTS ────────────────────────
    story += section_header("STATE 8 + 9 — IMAGE PROMPTS & VIDEO PROMPTS", s)
    story.append(body("Each beat = max 3–5 seconds of script. "
                      "Blue = Image Prompt · Green = Video Prompt", s))
    story.append(Spacer(1, 0.3*cm))

    beats = [
        # (script_segment, image_prompt, camera, lighting, mood, action, video_prompt)
        (
            "You're 28 years old. Healthy. Slightly annoying about it, actually. You take vitamins, you hydrate, you've downloaded an app to track your sleep quality.",
            "Host character — bearded realistic face on rectangular cartoon body, stick arms, green leaf loincloth — stands in a bright cartoon kitchen holding supplement bottles in both stick hands, a glass of water tucked under one arm, a phone showing a sleep tracking app propped on the counter. Expression: smug. Flat 2D animation, bright white kitchen, thick black outlines, cheerful saturated colours, even flat lighting.",
            "Wide, frontal stage shot", "Flat, even, no shadows", "Comically self-satisfied", "Host displaying modern wellness props",
            "Host slides in from the left, supplement bottles popping into his stick hands one by one. Phone screen animates on — sleep app loads with a cheerful ding. Camera slowly zooms in on his smug face. 3–4 seconds."
        ),
        (
            "And by most historical standards, you are already living on borrowed time.",
            "Host stands confidently. Behind him a large cartoon scoreboard reads: 'HISTORICAL AVERAGE LIFESPAN: 30 YEARS' with a red arrow pointing directly at him. His expression shifts from smug to alarmed. Flat 2D animation, bright white background, thick black outlines.",
            "Medium shot, character centre-left", "Flat, even", "Dawning horror", "Host reacting to scoreboard",
            "Scoreboard drops from above with a cartoon whoosh. Red arrow bounces as it appears. Host's smug expression melts into alarmed in a slow blink. Camera holds wide. 3 seconds."
        ),
        (
            "For the majority of human history, 30 wasn't middle age. It was the finish line.",
            "Wide cartoon race track. 'FINISH LINE' banner with '30' in huge letters. Multiple cartoon historical figures collapsing dead at the finish line. Host stands at starting line looking baffled. Blue sky, green track, bright colours. Flat 2D animation, thick outlines.",
            "Wide establishing shot", "Bright outdoor flat", "Absurdly cheerful given content", "Figures collapsing at finish, host bewildered",
            "Camera starts wide on the track. Cartoon figures sprint toward the finish line in a loop, collapsing one by one. '30' banner drops into frame. Host at start line watches, frozen. Slow zoom out. 4–5 seconds."
        ),
        (
            "It's how many different things were lined up to kill them before breakfast.",
            "Host stands centre. Around him, a cheerful orderly queue of cartoon threats waits patiently in line: plague rat, sword, moldy bread, stick-figure doctor with leech jar, tiny army — all holding numbered queue tickets. Host looks alarmed. Bright white background, flat 2D cartoon, thick outlines.",
            "Wide shot, host centre surrounded by queue", "Flat, even", "Organised, polite dread", "Queue of threats waiting their turn",
            "Each threat character enters the queue one by one from the right — plague rat waddles in, sword floats in, moldy bread bounces in, doctor shuffles in, tiny army marches in. Each takes a numbered ticket. Host turns to face them, freezes. 4 seconds."
        ),
        (
            "So today, we're going through every single reason you would have been dead before your thirtieth birthday.",
            "Host stands next to a massive wooden billboard reading 'REASONS YOU'D BE DEAD BY 30' with a very long numbered list trailing off the bottom. He gestures toward it. Blue sky, green grass background. Flat 2D cartoon, thick outlines.",
            "Medium wide, host left, sign right", "Flat outdoor daylight", "Educational, ominous", "Host presenting the list",
            "Billboard crashes down from above. List items appear rapid-fire, trailing off the bottom. Host gestures toward it with a pointing sweep. Camera zooms slightly toward the sign. 3–4 seconds."
        ),
        (
            "From the moment you were born, to the moment your body simply gave up. Let's get into it.",
            "Host points at the viewer. Behind him: a flat cartoon timeline showing 'BIRTH' on the left and 'GAVE UP' on the right with an extremely short gap between them. Expression: darkly enthusiastic. Bright clean background, flat 2D cartoon, thick outlines.",
            "Medium, direct address", "Flat, even", "Darkly cheerful", "Direct point at viewer",
            "Timeline slides in from left. 'BIRTH' label appears, then 'GAVE UP'. The gap between them compresses — shrinks to almost nothing — with a cartoon squish. Host's pointing arm extends toward camera. Slow zoom toward viewer. 3 seconds."
        ),
        (
            "Reason one. You probably wouldn't have survived being born.",
            "Title card: 'REASON 1' in bold cartoon block letters. Below it, a tiny cartoon stick-figure baby wrapped in swaddling cloth with a worried expression, surrounded by a large red cartoon danger explosion shape labelled 'DEATH THREAT'. White background, thick outlines, red accent. Flat 2D cartoon.",
            "Flat title card composition", "Even, clean", "Absurdly alarming", "Static title with warning graphic",
            "Title card slams into frame with impact. 'REASON 1' letters drop in one by one. Baby figure wobbles in below, danger explosion shape pulses — expanding and contracting. Hold 2 seconds then cut."
        ),
        (
            "Before you drew your first breath, you were already in danger.",
            "Medieval stone room, warm ochre walls. A simple cartoon woman figure lies in a rough wooden bed. Two simple cartoon midwife figures stand nearby looking worried, one holding a candle. Bright and almost cosy despite the implication. Flat 2D animation, warm ochre palette, thick outlines.",
            "Wide interior shot", "Warm, flat candlelight", "Cheerfully ominous", "Midwives looking concerned",
            "Camera slowly pushes into the medieval room. Candlelight flickers in a subtle loop. Midwife figures exchange a worried glance. The bed creaks slightly — subtle wobble animation. 3 seconds."
        ),
        (
            "In medieval Europe, roughly 1 in 50 women died during childbirth.",
            "Flat 2D cartoon infographic: a neat row of 50 identical simple cartoon medieval women figures. Every 50th figure has a cartoon skull floating above her head. Clean parchment/yellow background, thick outlines. Label: 'MEDIEVAL BIRTH STATISTICS.'",
            "Flat infographic layout", "Even, clean", "Matter-of-fact horror", "Static infographic",
            "50 figures walk in from left in a marching loop, filling the row. When the 50th arrives, a cartoon skull pops up above her head with a little bounce. Camera slowly pans left to right across the entire row. 3–4 seconds."
        ),
        (
            "That sounds manageable until you realize most women gave birth five to ten times.",
            "Host stands next to a chalkboard showing: '1/50 × 10 births = 😬'. He points at it with his stick arm, expression deeply uncomfortable. Warm ochre classroom background, flat 2D cartoon, thick outlines.",
            "Medium, host left, chalkboard right", "Warm flat interior", "Reluctant math", "Host pointing at equation",
            "Host slides in from left. Equation writes itself on the chalkboard in chalk-drawing style, line by line. The final emoji appears last. Host's expression shifts as the math completes. 3 seconds."
        ),
        (
            "And if you made it out, your first year was the real filter.",
            "Flat 2D cartoon: a cartoon baby in a wooden cradle inside a large funnel shape. Many tiny baby figures enter the top; very few exit the bottom. Bright yellow/blue cheerful colours, thick outlines. Wide shot.",
            "Wide, centred on funnel", "Flat, even", "Grimly statistical", "Babies passing through filter",
            "Baby figures rain down into the top of the funnel from above in a constant stream. A small trickle exits the bottom. The funnel shakes slightly with each baby entering. Camera holds wide, slightly pulling back. 3 seconds."
        ),
        (
            "In pre-industrial societies, somewhere between 30% and 50% of children died before the age of five.",
            "Flat 2D cartoon infographic: ten identical simple cartoon toddler figures in a neat row. Five of them have small cartoon skulls above their heads. Bright clean white background, thick outlines. Label: 'PRE-INDUSTRIAL CHILD SURVIVAL RATE.'",
            "Flat infographic", "Clean, even", "Statistical cheerfulness", "Static infographic",
            "Ten toddler figures march in left to right. When all are in frame, five skull icons drop down from above simultaneously — landing with a soft thud. Camera holds flat. Label fades in below. 3 seconds."
        ),
        (
            "Not from rare diseases. From diarrhea. From a cough that lasted too long.",
            "Host holds up two small signs. Left sign: 'RARE EXOTIC ILLNESS 🐍' with a red X through it. Right sign: 'A COUGH 😐' with a green checkmark. Expression: completely deadpan. Bright yellow/white background, flat 2D cartoon, thick outlines.",
            "Medium, direct address", "Flat, even", "Deadpan", "Host holding comparison signs",
            "Host slides in holding both signs. Camera holds still. He turns his head left to the exotic illness sign, then right to the cough sign. Looks back at camera with deadpan expression held for a long beat. 3 seconds."
        ),
        (
            "From being born slightly too early in a world with no incubators, no formula, and no emergency anything.",
            "Wide flat 2D cartoon: a medieval stone room. A tiny cartoon baby in the centre surrounded by empty space where modern equipment would be. Small floating label signs around it: 'NO INCUBATOR,' 'NO FORMULA,' 'NO EMERGENCY.' A simple cartoon midwife shrugs. Warm ochre tones, flat 2D cartoon, thick outlines.",
            "Wide interior", "Warm flat", "Starkly empty", "Midwife shrugging at absent equipment",
            "Camera starts on the baby and slowly pulls back to reveal how empty the space truly is. Label signs float in one by one from the edges of frame. Midwife enters, shrugs, both arms raised, holds the shrug. 3–4 seconds."
        ),
        (
            "You had a coin-flip chance of making it to your fifth birthday.",
            "Host holds an oversized cartoon coin. One side: a smiling cartoon baby face. Other side: a cartoon skull. He flips it nervously. Expression: sweating. Bright white background, flat 2D cartoon, thick outlines.",
            "Medium, host centre", "Flat, even", "Nervous", "Coin mid-flip",
            "Coin spins upward from host's stick hands — both sides flashing. Coin reaches apex, hangs suspended. Camera holds. Coin stays frozen mid-air — does not land. Cut before we know the result. 3 seconds."
        ),
        (
            "Reason two. A scratch could end you.",
            "Title card: 'REASON 2' in bold cartoon block letters. An extremely small cartoon scratch mark on a simple cartoon arm, surrounded by a massive red danger explosion shape labelled 'DEATH THREAT'. Thick outlines, red accent on white background. Flat 2D cartoon.",
            "Flat title card", "Clean, even", "Disproportionate alarm", "Static title with warning graphic",
            "Title card slams in. 'REASON 2' letters bounce. Danger explosion shape pulses around the scratch — expanding and shrinking like a heartbeat. Hold 2–3 seconds."
        ),
        (
            "Let's say you made it past childhood. Congratulations. Now try not to cut yourself.",
            "Host holds a small cartoon participation trophy reading 'SURVIVED CHILDHOOD 🏆.' His expression shifts from relieved to immediately suspicious. Bright cheerful background, flat 2D cartoon, thick outlines.",
            "Medium, host centre", "Flat, even", "Brief relief → immediate dread", "Host clutching trophy, going suspicious",
            "Host slides in holding the trophy. Camera holds on his relieved expression. Then his eyes slowly narrow — expression shifting to suspicious. Trophy lowers slightly as confidence fades. 3 seconds."
        ),
        (
            "In a world without antibiotics, every open wound was a negotiation with death.",
            "Split flat 2D cartoon. Left: host with a tiny scratch on his arm. Right: a cartoon Grim Reaper sitting across a negotiating table, arms crossed, looking at him expectantly. Speech bubble from Reaper: 'So. Let's talk.' Bright cheerful colours, flat 2D cartoon, thick outlines.",
            "Wide two-shot, split composition", "Flat, even", "Darkly comedic negotiation", "Reaper waiting for host to engage",
            "Host and Reaper appear simultaneously. Reaper leans forward, arms crossing the table. Host leans slightly back. The table sits perfectly still. Speech bubble inflates from Reaper. Camera holds on the standoff. 3 seconds."
        ),
        (
            "You scrape your leg on a fence. You slice your hand on a rock. You get a splinter that goes slightly too deep.",
            "Three-panel cartoon strip. Panel 1: cartoon leg scraping a wooden fence, small red mark. Panel 2: cartoon hand on a rock, small cut. Panel 3: a splinter in a cartoon thumb with a zoom circle showing it going alarmingly deep. Bright, flat 2D cartoon, thick outlines.",
            "Three-panel strip layout", "Flat, even", "Escalating mundane danger", "Three sequential minor injuries",
            "Three panels slide in from the right one at a time. Each panel animates briefly — leg scrapes fence, hand recoils from rock, zoom circle draws itself around the deep splinter. Each panel holds 1 second before the next slides in. 3–4 seconds."
        ),
        (
            "Any of these, in the wrong conditions, could turn septic within days.",
            "Flat 2D cartoon timeline: a cartoon arm with a tiny scratch. Labelled panels — DAY 1: tiny scratch, DAY 2: slightly bigger red mark, DAY 3: large angry cartoon bacteria visible, DAY 4: skull symbol. Bright cheerful colours, flat 2D cartoon, thick outlines.",
            "Flat timeline layout", "Clean, even", "Cheerful escalation", "Four-stage infection progression",
            "Timeline slides in from left. Day labels appear one by one. Scratch mark grows between each day. Bacteria icons pop up on Day 3. Skull drops in on Day 4 with a heavy thud. Camera holds flat. 3–4 seconds."
        ),
        (
            "The infection spreads. Your skin swells and darkens. Fever sets in.",
            "Host lies dramatically on a wooden floor. His arm is cartoonishly swollen and red. A large cartoon thermometer sticks out of his mouth showing extreme temperature. Tiny cartoon squiggly bacteria swirl around him. Warm ochre interior, flat 2D cartoon, thick outlines.",
            "Wide, host on floor, angled down slightly", "Warm flat interior", "Theatrical suffering", "Host dramatically ill",
            "Host character lies on the floor. Arm swells slowly in a cartoon inflate animation. Thermometer slides into his mouth, mercury rises and tip pops off. Bacteria swirl in a looping orbit. Camera holds above him. 3–4 seconds."
        ),
        (
            "And without anything to stop it, your body either fights it off on its own or it doesn't.",
            "Host standing upright. On his left shoulder: a tiny cartoon immune cell holding a tiny shield, cheering. On his right shoulder: a tiny cartoon Grim Reaper eating cartoon popcorn casually. Both equally present. Bright background, flat 2D cartoon, thick outlines.",
            "Medium, host centre", "Flat, even", "Unnerving 50/50", "Tiny figures on both shoulders",
            "Tiny immune cell on left shoulder pumps its fist in a looping cheer. Tiny Reaper on right shoulder opens popcorn bag, eating in a slow loop. Both continue simultaneously. Host looks left, then right, then straight at camera. Holds. 3 seconds."
        ),
        (
            "Historians estimate that infection from minor wounds was one of the single biggest killers in the ancient and medieval world.",
            "Flat 2D cartoon bar chart. Bar labelled 'SWORD WOUND': medium height. Bar labelled 'TINY SCRATCH': reaching off the top of the chart with a shocked exclamation mark. Host stands beside it pointing in disbelief. Bright white background, flat 2D cartoon, thick outlines.",
            "Wide, chart right, host left", "Clean, flat", "Incredulous", "Host gesturing at absurd chart",
            "Bars grow upward from zero. 'SWORD WOUND' bar rises to medium height and stops. 'TINY SCRATCH' bar keeps rising past the top of the chart frame. Exclamation mark bounces in. Host's jaw drops slowly. 3–4 seconds."
        ),
        (
            "Soldiers didn't die just from swords. They survived the battle and then died two weeks later from a wound that would take a pharmacist thirty seconds to fix today.",
            "Split flat 2D cartoon. Left: victorious cartoon soldier with small bandaged wound, relieved. Right: same soldier flat in a wooden bed looking terrible. In the corner, a cartoon pharmacist holds up a bandage and taps a watch. Bright colours both sides, flat 2D cartoon, thick outlines.",
            "Wide split composition", "Flat, even both halves", "Brutal irony", "Victory left, defeat right",
            "Left side holds — victorious soldier stands, small flag wave loop. Right side: same soldier's bed appears, soldier drops into it with a cartoon flop. Pharmacist in corner taps watch. Camera holds wide split. 4 seconds."
        ),
        (
            "You didn't need a war to kill you. You just needed a bad Tuesday.",
            "Host stands next to a large cartoon calendar. Tuesday is circled in red with a skull and crossbones. Every other day looks completely normal. Expression: resigned. Bright yellow/white background, flat 2D cartoon, thick outlines.",
            "Medium, host left, calendar right", "Flat, even", "Resigned deadpan", "Host gesturing at marked calendar",
            "Calendar slides in from the right. All days appear clean. Then Tuesday — a red circle draws itself around it, skull and crossbones stamps itself on with a thud. Host turns to look at it, turns back to camera. Expression: resigned. 3 seconds."
        ),
        (
            "Reason three. Your food was quietly destroying you.",
            "Title card: 'REASON 3' in bold cartoon block letters. Below it, a cartoon wooden bowl of grey slop with tiny cartoon eyes peeking out, looking guilty. Small sign: 'FOOD.' Warm parchment/ochre background. Flat 2D cartoon.",
            "Flat title card", "Clean, even", "Guilty food", "Static title with suspicious bowl",
            "Title card drops in. Bowl of slop appears — its cartoon eyes blink slowly, looking guilty. The slop stirs itself slightly in a looping animation. Eyes dart left, then right. Bowl tries to look innocent. Hold 2–3 seconds."
        ),
        (
            "You wake up every morning and eat something grown in a controlled environment... Your ancestors woke up and hoped the grain hadn't gone moldy.",
            "Split flat 2D cartoon. Left side: gleaming cartoon supermarket, perfect produce, bright lights. Right side: a muddy medieval storage room, a simple cartoon peasant lifting a cloth off a barrel to reveal a green cartoon mould explosion inside. Expression: completely unsurprised. Bright colours both sides, thick outlines.",
            "Wide split composition", "Bright left, warm dim right", "Stark contrast", "Perfect food left, mouldy disaster right",
            "Left side: supermarket shelves fill with produce in a stacking animation. Right side: peasant slowly lifts cloth off barrel — cartoon mould explosion pops out with a green burst. Peasant's expression: completely unsurprised. Camera holds wide split. 3–4 seconds."
        ),
        (
            "Malnutrition was so common in pre-modern societies it was essentially just called being alive.",
            "Host holds an open cartoon dictionary. The visible definition reads: 'MALNUTRITION (n.): just... existing, basically.' He nods very seriously. Bright white background, flat 2D cartoon, thick outlines.",
            "Medium, host centre", "Flat, clean", "Academic deadpan", "Host presenting definition",
            "Host slides in holding closed dictionary. He opens it — pages fan in a quick flip animation. Definition text types itself in. Host reads it, nods slowly and seriously. Holds the nod. 3 seconds."
        ),
        (
            "Most people survived on grain, roots, and whatever didn't run away fast enough.",
            "Wide flat 2D cartoon: a simple medieval wooden table. On it: a sad grain stalk, a sad-looking root vegetable, and a cartoon rabbit that clearly failed to escape in time, sitting there looking resigned. A simple cartoon peasant sits across from it all. Warm ochre/brown tones, bright colours, flat 2D cartoon, thick outlines.",
            "Wide, table centre", "Warm flat interior", "Grim variety", "Resigned rabbit at the table",
            "Camera slowly pushes into the table. Each food item animates briefly — grain sags, root wilts, rabbit sighs and looks away. Peasant picks up a utensil, pauses, puts it back down. 3 seconds."
        ),
        (
            "Vitamin C deficiency caused scurvy — your gums bled, your teeth fell out, old wounds reopened, and your body started dissolving itself from the inside.",
            "Host holds a cartoon medical clipboard. He checks symptoms off one by one: ✓ GUMS BLEEDING, ✓ TEETH GONE, ✓ WOUNDS REOPENED, ✓ BODY DISSOLVING. Expression: deeply unimpressed at himself. Bright white background, flat 2D cartoon, thick outlines.",
            "Medium, host centre", "Flat, even", "Clinical self-disgust", "Host checking off own symptoms",
            "Host holds clipboard. Each checkmark animates itself in one by one — drawing onto the paper. His expression gets progressively worse with each check. At the last one ('BODY DISSOLVING'), he tilts the clipboard away from himself. 3–4 seconds."
        ),
        (
            "Vitamin D deficiency softened your bones until they bent under your own weight.",
            "Flat 2D cartoon: a simple cartoon figure standing. Their legs are visibly curved like soft noodles, bending under them. The figure stares down at their own legs in genuine confusion. Bright cheerful white/yellow background, flat 2D cartoon, thick outlines.",
            "Full body, centred", "Clean, flat", "Confused structural failure", "Figure puzzled by own collapsing legs",
            "Figure stands normally. Then legs begin to slowly bend — cartoon soft-material animation, like wet noodles bowing. Figure looks down at legs. Looks up. Looks down again. Legs continue bending in a looping slow collapse. 3 seconds."
        ),
        (
            "Iron deficiency left you so exhausted you could barely function, which was a problem because your entire survival depended on functioning.",
            "Host lies completely flat face-down on the ground. Around him: an unharvested cartoon field labelled 'NOT DONE,' an unfed cartoon animal labelled 'NOT DONE,' an unrepaired cartoon roof labelled 'NOT DONE.' Warm outdoor colours, flat 2D cartoon, thick outlines.",
            "Wide, aerial-ish, host flat and tasks around him", "Flat outdoor daylight", "Catastrophic exhaustion", "Host fully collapsed, everything abandoned",
            "Host is already flat on the ground. Camera starts wide and slowly pulls back to reveal each 'NOT DONE' label appearing around him one by one. A cartoon fly circles him in a lazy orbit loop. 3–4 seconds."
        ),
        (
            "Crops infected with ergot — a fungus that grew on rye — caused hallucinations, seizures, gangrene, and death.",
            "Wide flat 2D cartoon: a cheerful field of green rye. Close-up on one stalk with a sinister-grinning cartoon green fungus clinging to it, wearing tiny sunglasses. Around it, small floating labels: 'HALLUCINATIONS,' 'SEIZURES,' 'GANGRENE,' 'DEATH.' Bright green field, blue sky. Flat 2D cartoon, thick outlines.",
            "Medium close on stalk, field in background", "Bright outdoor flat", "Cheerful menace", "Smug fungus on rye stalk",
            "Camera pushes slowly into the rye field toward the fungus. Fungus adjusts its tiny cartoon sunglasses. Labels pop up one at a time around it with each word — each popping in with a small impact. Fungus grins wider with each label. 3–4 seconds."
        ),
        (
            "Entire villages would lose their minds simultaneously and have absolutely no idea why.",
            "Wide flat 2D cartoon: a cheerful medieval village square in warm ochre and terracotta tones. Multiple simple cartoon villager figures running in completely random directions. Cartoon hallucination shapes float above some — cartoon snakes, floating bread, dancing fish. Every expression: baffled. Bright colours, blue sky. Flat 2D cartoon, thick outlines.",
            "Wide establishing village shot", "Bright flat outdoor", "Cheerful mass confusion", "Villagers scattered in all directions",
            "Camera starts wide on the quiet village square. Then all villager figures begin moving at once — scattering in random directions simultaneously. Hallucination shapes float up above each one. Complete chaos in under 2 seconds. Camera holds on the chaos, slowly pulling back. 4 seconds."
        ),
        (
            "They assumed it was God. It was breakfast.",
            "Host stands between two labelled arrows. Left arrow points upward toward cartoon clouds: 'GOD?' Right arrow points at a bowl of grey porridge on a table: 'ACTUALLY THIS.' Expression: completely flat and deadpan. Bright white background, flat 2D cartoon, thick outlines.",
            "Medium, host centre between arrows", "Flat, clean", "Absolute deadpan", "Host caught between two explanations",
            "Host slides in between the two arrows. Left arrow animates pointing upward. Right arrow animates pointing at the bowl. Host looks left, looks right, looks at camera. Long deadpan hold. Bowl sits completely still. 3 seconds."
        ),
        (
            "Reason four. Disease did not need your permission.",
            "Title card: 'REASON 4' in bold cartoon block letters. A cartoon bacterium character — round, spiky, grinning — confidently walks through a cartoon door. A sign reads 'AUTHORIZED ENTRY ONLY.' The bacterium ignores it completely. Bright colours, flat 2D cartoon, thick outlines.",
            "Flat title card, character mid-stride", "Clean, even", "Brazen entry", "Germ confidently bypassing sign",
            "Title card in. Bacterium character walks in from the right, reaches the sign, glances at it sideways, and walks straight through the door without slowing. Door swings open and closed. Bacterium does not look back. 3 seconds."
        ),
        (
            "You've had vaccines. Probably more than you remember.",
            "Host holds a large booklet labelled 'MY VACCINATION RECORD.' It unfolds and unfolds, spilling to the floor in a long chain that goes off-frame. His expression: satisfied. Bright white/blue clinical background, flat 2D cartoon, thick outlines.",
            "Medium, host centre, record unfurling downward", "Flat clinical", "Complacent satisfaction", "Endless record unfolding",
            "Host holds up small booklet. He opens it. It begins unfolding — accordion animation, longer and longer, falling to the floor in stages. He watches it fall. It keeps going. Eventually he just looks at the camera. It's still unfolding. 3–4 seconds."
        ),
        (
            "Measles, mumps, rubella, polio, smallpox — your immune system has been pre-loaded with defences against diseases that used to erase entire populations.",
            "Flat 2D cartoon cross-section of the host character's rectangular body interior. Inside: rows of tiny cartoon immune cell soldiers standing at attention, each labelled — MEASLES, MUMPS, POLIO, SMALLPOX. All armed, all very prepared. Bright clinical interior colours, flat 2D cartoon, thick outlines.",
            "Cross-section interior view", "Flat, bright interior", "Impressively prepared", "Immune soldiers at ready",
            "Interior cross-section appears. Immune cell soldiers march in from the left in a formation, filling the rows. Each label appears above a soldier as they take position. Last soldier snaps to attention. The formation holds still. Camera slowly zooms in. 3–4 seconds."
        ),
        (
            "Your ancestors had none of that.",
            "Same cross-section interior — but an ancestor's. Completely empty inside. A cartoon tumbleweed rolls through. One tiny confused cell stands alone looking around for backup that isn't coming. Warm parchment/ochre tones, flat 2D cartoon, thick outlines.",
            "Cross-section interior view, identical framing to previous", "Warm flat", "Devastatingly empty", "Lone cell, tumbleweed",
            "Same interior cross-section — but empty. Camera pans slowly across it. Nothing moves. Tumbleweed rolls from left to right. Lone cell wanders in, looks around, keeps walking. Camera holds. 3 seconds."
        ),
        (
            "Smallpox alone killed an estimated 300 million people in the 20th century alone.",
            "Flat 2D cartoon: enormous bold numbers '300,000,000' dominate the frame. Below them, rows upon rows of tiny cartoon skull icons filling the entire background. In the bottom right corner, host stands barely visible among the skulls, looking up at the number. White background, flat 2D cartoon, thick outlines.",
            "Wide, number dominant, host tiny in corner", "Clean, flat", "Scale of incomprehensible loss", "Host dwarfed by count",
            "Numbers count up rapidly — cartoon ticker animation — reaching 300,000,000 with a heavy final click. Skull icons fill in from the top of the frame, raining down slowly to fill the background. Host appears last in the corner, shrinking as the skulls fill in around him. 4 seconds."
        ),
        (
            "The Black Death wiped out 30 to 60 percent of Europe in under a decade.",
            "Wide flat 2D cartoon map of Europe. Large portions are greyed out with cartoon skull icons. Remaining areas look alarmed. A small cartoon plague rat drags a scroll reading '30–60% · ONE DECADE.' Bright cheerful map border colours, flat 2D cartoon, thick outlines.",
            "Wide map view", "Clean, flat", "Cartographically grim", "Rat dragging statistic across map",
            "Map slides in. Healthy regions are bright. Grey-out spreads across the map in a sweeping animation — like ink spreading. Skull icons stamp themselves onto greyed regions. Plague rat drags its scroll across the bottom. 3–4 seconds."
        ),
        (
            "Cholera, typhoid, dysentery — diseases born from contaminated water — were permanent features of daily life.",
            "Wide flat 2D cartoon: a cheerful stone well in a medieval town square. Cross-section view shows below the waterline: cartoon bacteria, tiny cartoon rats, and cartoon waste swimming happily. Above ground, a cheerful queue of simple cartoon villager figures wait to drink. Bright cheerful colours above, gross but cartoonish below. Flat 2D cartoon, thick outlines.",
            "Wide with cross-section split at water level", "Bright outdoor flat", "Blissful ignorance above, chaos below", "Villagers queuing, horrors swimming below",
            "Camera starts on the cheerful well surface, then pans down through the waterline — cross-section reveal. Below: bacteria and rats swimming in loops. Camera holds below the waterline, then pans back up as villagers continue queuing above, oblivious. 4 seconds."
        ),
        (
            "The brutal part is that no one knew where these diseases came from. They didn't know about bacteria. They didn't know about viruses.",
            "Host stands in front of a large wooden whiteboard. Title: 'REASONS YOU'RE SICK.' The board is completely blank. He stares at it. Shrugs. Expression: genuinely at a loss. Warm ochre medieval setting, flat 2D cartoon, thick outlines.",
            "Medium, host left, blank board right", "Warm flat interior", "Genuine bewilderment", "Host shrugging at empty whiteboard",
            "Host walks in from left to stand before the whiteboard. He uncaps a cartoon marker. He holds it to the board. He stares at it. He caps the marker. He stares at the board. Shrugs both arms up. Camera holds. 3 seconds."
        ),
        (
            "They knew about bad air, angry stars, and divine punishment.",
            "Host holds up three cartoon medieval 'textbooks' fanned out in his stick hands. Book 1: 'BAD AIR: A MEDICAL GUIDE.' Book 2: 'ANGRY STARS AND YOU.' Book 3: 'DIVINE PUNISHMENT FOR BEGINNERS.' Each cover has a deliberately absurd illustration. Expression: unimpressed. Warm parchment background, flat 2D cartoon, thick outlines.",
            "Medium, host centre displaying books", "Warm flat", "Deadpan presentation of nonsense", "Host displaying three useless books",
            "Books fan out into host's stick hands one at a time — each appearing with a small pop. Each cover illustration briefly animates: bad air wafts, star shakes a fist, lightning bolt pulses on the third cover. Host holds all three, expression flat. 3–4 seconds."
        ),
        (
            "So they treated disease with prayer, bloodletting, and herb paste — and then died confused about why none of it worked.",
            "Four-panel flat 2D cartoon strip. Panel 1: simple cartoon figure praying. Panel 2: same figure with cartoon blood draining from arm. Panel 3: same figure with green herb paste slapped on face. Panel 4: same figure lying flat, labelled 'STILL DEAD.' Cheerful bright colours, flat 2D cartoon, thick outlines throughout.",
            "Four-panel strip layout", "Even, clean", "Logical but fatal progression", "Four sequential futile treatments",
            "Four-panel strip appears one panel at a time, sliding in from the right. Each panel's figure briefly animates. Final 'STILL DEAD' caption stamps itself. 4 seconds."
        ),
        (
            "You would have spent your entire life one handshake away from something your body had no answer for.",
            "Host cautiously extends one stick arm forward for a handshake. On the receiving end: a simple cartoon historical figure surrounded by floating cartoon germs and bacteria. Host's expression: deeply reluctant. Wide shot, bright cheerful background, flat 2D cartoon, thick outlines.",
            "Wide two-shot, handshake centre", "Flat, even", "Reluctant social contact", "Slow reluctant handshake approach",
            "Host's arm extends slowly toward centre frame. Historical figure's arm extends slowly from the right. Both moving in slow motion toward the handshake. Germs orbit the historical figure. The two hands get very close. Camera holds on the near-handshake. Does not complete. 4 seconds."
        ),
        (
            "Reason five. Someone else's war was your problem.",
            "Title card: 'REASON 5' in bold cartoon lettering. A simple cartoon civilian figure sits at a wooden table eating soup. Through the window behind him: a massive cartoon army marching past. He looks up from his soup with profound disappointment. Warm ochre interior, bright blue sky through window. Flat 2D cartoon, thick outlines.",
            "Interior medium shot, window shows exterior", "Warm flat interior, bright exterior through window", "Profound civilian inconvenience", "Army passing civilian's window uninvited",
            "Title card in. Civilian figure sits eating soup in looping animation. Through the window behind him, cartoon army begins marching past — continuous loop. Civilian looks up from soup. Puts spoon down. Looks at window. Profound disappointment settles. 3 seconds."
        ),
        (
            "You didn't have to be a soldier to die in a war. You just had to be nearby.",
            "Flat 2D cartoon Venn diagram. Left circle (small): 'SOLDIERS.' Right circle (enormous): 'People who died in wars.' The left circle sits entirely inside the right. Host points at the diagram. Bright white background, flat 2D cartoon, thick outlines.",
            "Wide, diagram centre, host left", "Clean, flat", "Statistical grimness", "Host pointing at disproportionate diagram",
            "Venn diagram draws itself — left circle first (small), then right circle grows outward, consuming most of the frame. Host points at the expanding right circle as it grows. Camera pulls back to accommodate. 3 seconds."
        ),
        (
            "It arrived at your village, ate your food, took your livestock, burned what remained, and continued on its way.",
            "Wide flat 2D cartoon: a medieval village — terracotta rooftops, sandy ground. Left: cartoon army on horseback. In the village centre, cartoon soldiers help themselves to cartoon chickens, barrels, and bread. Simple cartoon villagers stand watching helplessly. The army continues marching off-screen right. Bright blue sky, cheerful colours despite chaos. Flat 2D cartoon, thick outlines.",
            "Wide establishing village shot", "Bright flat outdoor", "Casually catastrophic", "Army mid-plunder, moving through",
            "Army enters from left, marching. As they pass through the village centre, cartoon soldiers peel off to grab items. Army continues marching off-screen right without slowing. Villagers stand watching. Camera pans left to right with the army. 4–5 seconds."
        ),
        (
            "Civilians were not protected. They were resources, obstacles, or entertainment, depending on the army's mood that afternoon.",
            "Flat 2D cartoon: a cartoon army general on horseback holds a large spinning mood wheel labelled 'TODAY'S PLAN FOR CIVILIANS.' The wheel has three sections: 'RESOURCES,' 'OBSTACLES,' 'ENTERTAINMENT.' A group of simple cartoon villager figures stands nearby looking extremely nervous. Bright colours, flat 2D cartoon, thick outlines.",
            "Medium, general centre with wheel, villagers right", "Flat outdoor bright", "Cheerful bureaucratic menace", "Needle spinning on wheel",
            "General spins the mood wheel — finger flicks it in a looping spin. The needle slows. Villager figures lean in to watch. Camera slowly zooms into the spinning wheel as it decelerates. Needle hasn't stopped when cut. 3 seconds."
        ),
        (
            "The Mongol invasions killed an estimated 40 million people — most of them non-combatants.",
            "Wide flat 2D cartoon scene: a bright medieval town — terracotta roofs, sandy ground, blue sky. Cartoon Mongol cavalry crowd the left side. Simple cartoon civilian figures scattered throughout. A large cartoon sign in the scene reads '40,000,000 NON-COMBATANTS.' Bright and almost cheerful despite content. Flat 2D cartoon, thick outlines.",
            "Wide establishing shot", "Bright flat outdoor", "Channel-signature cheerful horror", "Cavalry entering town, civilians reacting",
            "Wide town scene. Cavalry enters from left in a marching animation. Sign drops from above with a cartoon whoosh — '40,000,000 NON-COMBATANTS.' Camera slowly pulls back to show the full scene. Town stays bright and cheerful throughout. 3–4 seconds."
        ),
        (
            "The Thirty Years' War reduced the population of some German regions by a third.",
            "Flat 2D cartoon: a simple outline map panel of a German region. Left panel: three cartoon people icons standing. Right panel: only two cartoon people icons; where the third stood is now a cartoon ghost outline with an X. Host points at the comparison. Bright clean background, flat 2D cartoon, thick outlines.",
            "Wide, two-panel map comparison, host right", "Clean, flat", "Quiet devastation", "Host pointing at missing population",
            "Left panel: 3 figures stand. Camera holds. Then the third figure slowly fades out — dissolve animation — leaving a ghost outline. Ghost outline blinks once, disappears. Right panel updates to show 2 remaining. Host points at the gap. 3 seconds."
        ),
        (
            "Armies didn't just fight each other. They brought typhus, dysentery, and plague and distributed it across everything they passed through.",
            "Wide flat 2D cartoon: a cartoon army marching in a neat line. Behind them, trailing in their wake: a parade of cartoon germ icons, bacteria, and disease symbols scattered liberally across the ground. Like a parade — but the confetti is illness. Bright cheerful colours, blue sky, flat 2D cartoon, thick outlines.",
            "Wide side-on shot, army left-to-right", "Flat bright outdoor", "Festive disease distribution", "Army marching, illness trail behind them",
            "Army marches from left to right in looping animation. Behind them, germ icons drop from the army's path, landing and spreading outward like ripples. The trail of germs grows wider the further they march. Camera follows the march, panning right. 3–4 seconds."
        ),
        (
            "And if you were conscripted — you'd be handed a weapon, pointed in a direction, and told to figure it out.",
            "Host stands looking confused. A cartoon army recruiter character hands him a tiny cartoon spear. Behind the recruiter: a sign reading 'NO AGE REQUIREMENT.' The recruiter points vaguely to the right and immediately walks away. Host is left alone holding the spear, looking at camera. Bright outdoor colours, flat 2D cartoon, thick outlines.",
            "Medium, recruiter handing off spear, host receiving", "Flat outdoor bright", "Resigned conscription", "Spear being handed to host",
            "Recruiter slides in from right. Spear appears and floats between them. Host's stick hand reaches out and takes it — reluctantly, slowly. Recruiter points vaguely to the right and immediately walks off-screen. Host is left alone holding the spear, looking at camera. 3–4 seconds."
        ),
        (
            "The life expectancy of a frontline soldier in the ancient world is not a number you'd want to hear.",
            "Flat 2D cartoon: a bar chart labelled 'ANCIENT SOLDIER LIFE EXPECTANCY.' The bar is so short it is nearly invisible — a tiny sliver at the bottom. A small label points at it: 'IT'S HERE ↓.' Host crouches down squinting at the barely visible bar. Bright white background, flat 2D cartoon, thick outlines.",
            "Wide, chart right, host crouching left", "Clean, flat", "Grim understatement", "Host squinting at nearly nonexistent bar",
            "Chart builds — empty axis lines first, then label types in. Bar begins to grow from the bottom — very slowly — then stops almost immediately, barely a sliver. Arrow draws itself pointing at the micro-bar. Host crouches down to squint at it. 3 seconds."
        ),
        (
            "Reason six. The doctor was the final boss.",
            "Title card: 'REASON 6' in bold cartoon lettering. Village medic character — cartoon plague doctor bird mask, simple rectangular body, green leaf loincloth — labelled 'FINAL BOSS.' A pixel-game style health bar floats above: 'YOUR SURVIVAL' — already almost empty. Bright colours, flat 2D cartoon, thick outlines.",
            "Flat title card", "Clean, even", "Video game boss reveal", "Static reveal title",
            "Title card in with heavy impact. Plague doctor figure slides in from the right — boss-entry style, slow and deliberate. Health bar slides down from the top of frame, nearly empty, with a low pulse animation. Doctor stands still, looking at camera. Holds. 3 seconds."
        ),
        (
            "You made it past birth. Past infection. Past famine. Past disease. Past war.",
            "Host stands looking exhausted but alive. Behind him: a trail of large cartoon checkboxes. ✓ BIRTH. ✓ INFECTION. ✓ FAMINE. ✓ DISEASE. ✓ WAR. All checked. Expression: battered but somehow still standing. Bright outdoor colours, flat 2D cartoon, thick outlines.",
            "Wide, host centre, checklist stretching behind him", "Flat outdoor bright", "Unlikely survival pride", "Host surrounded by completed challenges",
            "Host stands centre. Checkboxes appear behind him in rapid sequence — each one stamping in with a satisfying checkmark animation and a soft click. ✓ ✓ ✓ ✓ ✓. Host looks thoroughly battered but upright. He sways slightly in a subtle loop. 3–4 seconds."
        ),
        (
            "And now your body is failing and you need help. Bad news. Help has arrived.",
            "Host lies in a simple wooden medieval bed, visibly unwell. The door creaks open. The village medic silhouetted in the doorway — plague doctor bird mask, ominous posture. Caption below: 'HELP HAS ARRIVED.' Warm ochre interior, flat 2D cartoon, thick outlines.",
            "Interior medium, host in bed, medic silhouette in doorway", "Warm flat, slight shadow at doorway", "Deeply unwelcome arrival", "Medic appearing in doorway",
            "Host lies in bed, coughing slightly in a loop. The door slowly creaks open — hinges squeak. Plague doctor silhouette appears in the doorway. Caption drops in: 'HELP HAS ARRIVED.' Silhouette does not move. Camera holds. 4 seconds."
        ),
        (
            "The village medic doesn't wash his hands because he doesn't know why he'd need to.",
            "Village medic character — cartoon plague doctor bird mask, rectangular body, leaf loincloth — stands beside a basin of water. He looks at it with genuine philosophical confusion. He tilts his head. He walks away. Small cartoon thought bubble above him: '?' Warm ochre medieval interior, flat 2D cartoon, thick outlines.",
            "Medium, medic and basin", "Warm flat interior", "Innocent ignorance", "Medic walking away from untouched basin",
            "Medic walks toward the basin. Stops. Tilts head left, then right — confused animation. Turns 180 degrees and walks back the way he came. Basin sits untouched. Camera holds on the empty basin for a beat after he's gone. 3 seconds."
        ),
        (
            "He's going to diagnose you by staring at a cup of your urine and comparing the colour to a chart.",
            "Village medic — plague doctor mask, rectangular body — holds a small cartoon cup of yellow liquid up to the light with absolute seriousness. Beside him, a large hanging chart shows dozens of shades of yellow, each labelled with a medieval diagnosis. Expression: extremely professional. Warm ochre/tan medical interior, flat 2D cartoon, thick outlines.",
            "Medium, medic centre with chart beside him", "Warm flat", "Misplaced professional confidence", "Medic studying urine cup with great seriousness",
            "Medic holds up the cup. His head rotates slowly toward the chart, then back to the cup, then back to the chart — comparing in a methodical loop. Camera slowly zooms into the cup. The cup is held absolutely still and steady. 3–4 seconds."
        ),
        (
            "He believes your body is controlled by four fluids — blood, phlegm, yellow bile, black bile.",
            "Flat 2D cartoon: a chalkboard in a warm ochre room. Four cartoon fluid containers drawn on it, labelled: BLOOD (red), PHLEGM (green), YELLOW BILE (yellow), BLACK BILE (black). Village medic — plague mask, rectangular body — points at the board with a stick, looking very certain. Flat 2D cartoon, thick outlines.",
            "Wide interior, medic left, board right", "Warm flat", "Confident wrongness", "Medic lecturing at four-humour diagram",
            "Medic taps the chalkboard with a stick. Each fluid container draws itself in chalk-style as he points to it — one by one. Each label writes itself below. Medic nods at each one. Camera holds wide. 3–4 seconds."
        ),
        (
            "His primary tool is a blade. Not to repair anything. To drain you.",
            "Wide flat 2D cartoon: a simple medieval medical table. The only item on it: one rusty cartoon blade, centred. Village medic — plague mask, rectangular body — stands behind the table pointing at it proudly. Host visible in the background looking alarmed. Warm ochre interior, flat 2D cartoon, thick outlines.",
            "Medium wide, table centre, medic behind, host in background", "Warm flat", "Proud presentation of wrong tool", "Medic proudly displaying single blade",
            "Blade sits alone on the empty table. Medic gestures toward it with both arms — presenting it like a game show prize. Camera slowly zooms into the blade. The blade does not move. The zoom continues until the blade fills most of the frame. 3 seconds."
        ),
        (
            "Bloodletting was the most common medical procedure in the world for over two thousand years.",
            "Flat 2D cartoon timeline spanning across the frame. A 2,000-year span. Across the ENTIRE timeline: 'DRAIN THE BLOOD 🩸' in large bold cartoon lettering, unbroken from one end to the other. Smaller text: 'Every. Single. Century.' Host stares at the timeline in disbelief. Bright clean white background, flat 2D cartoon, thick outlines.",
            "Wide, timeline dominant, host small below", "Clean, flat", "Exhausted historical disbelief", "Host confronting 2000-year timeline",
            "Timeline slides in from left, slowly. 'DRAIN THE BLOOD' text types itself across the entire length. It keeps going and going. Host character appears at the bottom watching it type. He waits. It's still typing. 4 seconds."
        ),
        (
            "Doctors bled patients who were already weak, already dehydrated, already dying. They bled them until they passed out and called it progress.",
            "Flat 2D cartoon: a simple patient figure in a wooden medieval bed, already visibly weak. The village medic — plague mask — drains blood from their arm into a bucket. A second bucket. A third. Patient's colour drains progressively. Final panel: patient has passed out. Medic makes a checkmark on a clipboard: 'PROGRESS ✓.' Warm ochre interior, bright flat 2D cartoon, thick outlines.",
            "Wide interior, multi-stage composition", "Warm flat", "Clinical satisfaction at patient's expense", "Progressive bleeding to unconsciousness",
            "Patient in bed, already weak. Blood drains into bucket in a cartoon pour loop. First bucket fills, replaced by a second. Patient's colour indicator slowly drains. Patient slumps. Medic makes the checkmark — pen drawing animation. 'PROGRESS ✓' holds on screen. 4 seconds."
        ),
        (
            "If the bleeding didn't work, they applied leeches. If the leeches failed, there was always a poultice made from pigeon dung and vinegar.",
            "Host sits in a medieval chair. His arms show three stages: Stage 1: cartoon leeches clinging on. Stage 2: a cartoon pigeon hovering nearby looking guilty. Stage 3: a jar labelled 'PIGEON DUNG + VINEGAR' being applied to his face. Expression moves from bad to worse to dead-eyed acceptance. Warm ochre interior, flat 2D cartoon, thick outlines.",
            "Medium, host in chair centre", "Warm flat interior", "Escalating indignity", "Three treatments applied in sequence",
            "Host sits in chair. Each treatment animates in sequence: leeches drop onto arms one by one. Then pigeon flies in from left, looks guilty, flies back out. Jar of poultice slides into frame and tips toward host's face. Host's expression shifts with each stage — bad, worse, dead-eyed acceptance. 4 seconds."
        ),
        (
            "If that didn't work either, the priest was sent for, because at that point clearly you had sinned your way into this.",
            "Wide flat 2D cartoon: host lies in the wooden bed. Village medic stands at the door gesturing to a simple cartoon priest character arriving with a cross. The medic shrugs with both arms raised. Host covers his face with his stick arm in a slow defeated motion. Warm ochre interior, flat 2D cartoon, thick outlines.",
            "Wide interior, all three characters", "Warm flat", "End of medical options", "Medic summoning priest, host giving up",
            "Medic walks to the door and opens it. Priest character walks in from outside, cross raised. Medic shrugs — both arms raised, held in the shrug position. Host in bed covers his face with his stick arm in a slow defeated motion. Priest looks around, unsure where to start. 3–4 seconds."
        ),
        (
            "You walked into that room sick. You'd be lucky to walk back out.",
            "Wide flat 2D cartoon split-view of the same medical room. Left half: host walking IN through the door, looking unwell but standing. Right half: same host being carried out horizontally by two simple cartoon figures, looking deeply unimpressed. Warm ochre interior both sides, flat 2D cartoon, thick outlines.",
            "Wide split composition, same room", "Warm flat throughout", "Expected outcome", "Walking in left, carried out right",
            "Left half: host walks in through door — normal walking animation, slightly hunched. Right half: same host is carried out horizontally — slow carry animation. Both animations play simultaneously. Left host and right host cross paths at the centre dividing line. 4 seconds."
        ),
        (
            "So here you are. 28 years old. Vitamin-stacked, slightly over-caffeinated, sleeping on a mattress that cost more than some medieval peasants' houses, and genuinely convinced your lower back situation deserves a specialist.",
            "Host sits on an enormous cartoon mattress surrounded by vitamin bottles, a large cartoon coffee cup, and a phone showing a 'BACK SPECIALIST BOOKING' app. Expression: completely self-satisfied. Bright, cheerful modern colours, flat 2D cartoon, thick outlines.",
            "Wide, host on mattress centre", "Bright flat modern", "Comically oblivious comfort", "Host surrounded by modern luxuries",
            "Host sits on the mattress. Supplement bottles orbit him slowly in a lazy loop. Coffee steam rises in a cartoon curl loop. Phone screen glows and blinks. Camera slowly zooms in toward his self-satisfied face. Everything glows with modern comfort. 3–4 seconds."
        ),
        (
            "Your ancestors survived childbirth, survived famine, survived plague, survived war, and survived the doctor.",
            "Wide flat 2D cartoon: a long line of simple cartoon ancestor figures stretching back through history. Each one looks increasingly battered — scratches, bandages, ratty clothing — but all still standing. They face forward. The one closest to camera gestures toward the viewer. Warm mixed historical colours, flat 2D cartoon, thick outlines.",
            "Wide long shot, line of ancestors", "Flat, warm", "Stubborn resilience", "Ancestors standing despite everything, gesturing forward",
            "Camera pans slowly across the long line of ancestor figures — moving right to left through history. Each ancestor nods slightly as the camera passes them. The furthest back ones are the most battered. Camera slows as it approaches the front. 4 seconds."
        ),
        (
            "They endured all of it, for decades, in the dark, with no guarantee — and somehow stayed alive just long enough to produce a chain of people that eventually ended with you.",
            "Wide flat 2D cartoon: a tall family tree drawn in cartoon style. At the very bottom, a tiny barely-surviving ancestor in dark surroundings. The tree grows upward through centuries. At the very top, bright and cheerful: host character sitting comfortably on a cartoon couch. The contrast between bottom and top is enormous. Flat 2D cartoon, thick outlines.",
            "Wide full tree, bottom to top", "Dark at bottom, bright at top", "Scale of inherited survival", "Tree spanning darkness to comfort",
            "Camera starts at the very bottom of the family tree — dark, close, barely visible. Slowly pulls upward and back through generations. Light increases as camera climbs. Reaches the top — host character on couch, bright and comfortable. Camera holds on the contrast. 4–5 seconds."
        ),
        (
            "That isn't luck. That's something more stubborn than luck.",
            "Host stands alone, centre frame. Expression: genuinely serious for once. Beside him, plain text on a clean background: 'NOT LUCK.' Below it: 'SOMETHING WORSE.' Bright clean background, flat 2D cartoon, thick outlines. Direct address.",
            "Medium, direct address", "Flat, clean, slightly more still than usual", "Rare moment of genuine weight", "Host still, holding eye contact",
            "Text appears on screen line by line: 'NOT LUCK.' — pause — 'SOMETHING WORSE.' Host stands still. No movement. No comedy. Camera holds. The stillness is intentional — the one beat where everything stops. 3 seconds."
        ),
        (
            "Hit subscribe. You owe them at least that.",
            "Host points directly at the viewer with one stick arm. Behind him: ghostly outlines of all his cartoon ancestors, all pointing in the same direction. A glowing cartoon 'SUBSCRIBE' button sits in the lower corner. Expression: expectant, with a hint of dry humour. Bright clean background, flat 2D cartoon, thick outlines.",
            "Medium, direct address, host pointing at viewer", "Flat, bright", "Ancestral moral obligation", "Host and ancestor ghosts all pointing at viewer",
            "Ancestor ghosts fade in behind host one by one — all pointing forward. Host raises his stick arm slowly to point at the viewer. Subscribe button glows brighter and pulses in a heartbeat animation. Camera holds on the full composition — host, ancestors, button. All pointing. 3–4 seconds."
        ),
    ]

    for i, (script_seg, img_prompt, camera, lighting, mood, action, vid_prompt) in enumerate(beats, 1):
        story.append(Paragraph(f"BEAT {i}", s["label"]))
        story.append(Paragraph(f'"{script_seg}"', s["beat_text"]))

        story.append(Paragraph("▶ IMAGE PROMPT", s["prompt_label"]))
        story.append(Paragraph(img_prompt, s["prompt_body"]))
        story.append(Paragraph(f"Camera: {camera}  |  Lighting: {lighting}  |  Mood: {mood}  |  Action: {action}", s["prompt_label"]))

        story.append(Paragraph("▷ VIDEO PROMPT", ParagraphStyle("VL",
            fontSize=8.5, leading=12,
            textColor=colors.HexColor("#1A4D1A"),
            fontName="Helvetica-Bold", alignment=TA_LEFT,
            spaceAfter=2, leftIndent=10)))
        story.append(Paragraph(vid_prompt, s["video_body"]))
        story.append(hr(s))

    story.append(PageBreak())

    # ── SECTION 6 — THUMBNAIL ANALYSIS ───────────────────────────
    story += section_header("STATE 10 — THUMBNAIL ANALYSIS", s)

    thumb_analysis = [
        ("Text Style", "ALL CAPS, bold, condensed sans-serif (Impact-style). Maximum 4 words. "
         "Two modes: bright red with neon glow effect on dark backgrounds, or solid white bold "
         "on near-black backgrounds. Text fills roughly 30–40% of the frame. Always short, "
         "punchy, and incomplete — designed to create a question the viewer needs to answer "
         "by clicking."),
        ("Composition", "Consistent formula: Character positioned centre-right or right. "
         "Text positioned top-left, top-right, or left. A hand-drawn arrow (red or white) "
         "pointing directly toward the character. Arrow + text frame the character as the "
         "subject. Character is always the emotional anchor."),
        ("Colour Contrast", "Thumbnails are the EXACT OPPOSITE of the in-video style. "
         "In-video = bright, cheerful, saturated. Thumbnails = dark, cinematic, moody. "
         "Backgrounds are near-black, dark brown apocalyptic, or dark stormy blue-grey. "
         "The character and text are the only bright elements."),
        ("Emotion Triggers", "Defiant survival — character barely standing in aftermath. "
         "Impossible odds — shocking statistic with visual proof. "
         "Pure curiosity gap — something so bad it can't be named. "
         "Body language does heavy lifting: standing defiantly, sitting exhausted and shaken, "
         "standing at a cliff's edge."),
    ]
    for title, text in thumb_analysis:
        story.append(lbl(title.upper(), s))
        story.append(body(text, s))
    story.append(Spacer(1, 0.3*cm))

    # ── SECTION 7 — THUMBNAILS ────────────────────────────────────
    story += section_header("STATE 11 — 5 THUMBNAIL CONCEPTS", s)

    thumbnails = [
        ("Thumbnail 1 — DEAD BY 30",
         "Host character standing centre-right in a dark, desolate landscape. Behind him: rows of cartoon gravestones stretching back into murky fog. He faces the camera, arms slightly out — the last one standing.",
         "DEAD BY 30",
         "Defiant survival against impossible odds. Viewer sees one person standing among a field of dead — implying they almost weren't here either.",
         "Dark cinematic YouTube thumbnail. Right side: host character — realistic bearded face on simple rectangular cartoon body, stick arms, green leaf loincloth — standing on dark muddy ground, facing camera, arms slightly out, expression grim but defiant. Background: rows of small cartoon gravestones disappearing into dark fog, deep brown-black sky, no sunlight. Left side: bold white condensed text 'DEAD BY 30' with red glow outline, large and dominant. Red hand-drawn arrow pointing right toward the character. Dark colour palette — near-black background, dark browns and greys, red text accent. High contrast between dark background and character. No bright colours. Flat 2D cartoon character against dark semi-realistic moody background."),
        ("Thumbnail 2 — YOU WOULDN'T MAKE IT",
         "Host standing on a narrow cliff edge, looking down at a massive crashing graph line. The graph represents life expectancy — it falls off a cliff directly beneath him. Expression: alarmed and resigned.",
         "YOU WOULDN'T MAKE IT",
         "Personal stakes. The statistic is about YOU, not history. The cliff edge implies you're right at the edge of survival.",
         "Dark cinematic YouTube thumbnail. Right-centre: host character — realistic bearded face on rectangular cartoon body, stick arms, green leaf loincloth — standing on edge of a dark rocky cliff, looking down with alarmed expression. Below and behind him: a massive cartoon graph line crashing dramatically downward into a dark abyss. Background: dark stormy grey-blue sky, desolate wasteland. Top of frame: bold red glowing condensed text 'YOU WOULDN'T MAKE IT.' Red hand-drawn arrow pointing down toward character. Very dark palette — near-black, dark grey, slate blue. Flat 2D cartoon character on dark cinematic background."),
        ("Thumbnail 3 — STILL HERE",
         "Host sitting against a stone wall, looking directly at the camera with exhausted wide eyes. In his stick hands: a small parchment showing a checklist — implying everything has already been survived. Somehow.",
         "STILL HERE",
         "Disbelief at one's own survival. 'STILL HERE' implies the viewer shouldn't be — and the checklist makes it clear how close it was.",
         "Dark cinematic YouTube thumbnail. Right: host character — realistic bearded face on rectangular cartoon body, stick arms, green leaf loincloth — sitting against a dark stone wall, leaning slightly, looking directly at the camera with wide exhausted eyes. In his stick hands: a small cartoon parchment with a checklist partially visible. Background: near-black, dark medieval stone walls. Left side: large bold white condensed text 'STILL HERE' with subtle glow. White hand-drawn arrow pointing right toward character. Near-black background with dark blue undertones. High contrast. Flat 2D cartoon character against dark moody setting."),
        ("Thumbnail 4 — 6 THINGS WAITING TO KILL YOU",
         "Host standing in darkness, lit only by a single small flame. Around him in the dark: shadowy outlines of every threat from the video — plague rat, blade, plague mask figure, soldier silhouette. He hasn't noticed them yet.",
         "6 THINGS WAITING TO KILL YOU",
         "Surrounded, outnumbered, unaware. The threat count in the title makes it feel like a list — viewer needs to know all 6.",
         "Dark cinematic YouTube thumbnail. Centre: host character — realistic bearded face on rectangular cartoon body, stick arms, green leaf loincloth — standing in near-complete darkness, lit from below by a single small cartoon candle flame. Around him in the dark: shadowy silhouettes of threats — a plague rat, a soldier shape, a plague doctor mask outline, a sword. He faces camera, unaware of them. Top of frame: bold red glowing condensed text '6 THINGS WAITING TO KILL YOU.' Red hand-drawn arrow pointing at character. Extremely dark palette, near-black, with only warm orange flame glow on character. High contrast. Flat 2D cartoon character on very dark background."),
        ("Thumbnail 5 — THEN VS NOW",
         "Split-face thumbnail. Left half: host looking relaxed and modern — supplements, coffee in hand. Right half: same character in dark moody historical tones — visibly unwell, battered, hollow-eyed. A bold line divides the two halves.",
         "THEN VS NOW",
         "Personal identification. Viewer sees themselves on the left, sees what they would have been on the right. The gap is devastating and funny at the same time.",
         "Dark cinematic YouTube thumbnail. Hard vertical split down the centre. Left half (bright): host character — realistic bearded face on rectangular cartoon body, stick arms, green leaf loincloth — looking smug and healthy, holding cartoon supplements and a coffee cup. Background: bright, cheerful, modern. Right half (dark): same host character — same design — looking hollow-eyed, pale, visibly suffering, set against a dark brown muddy medieval background with fog. Bold white condensed text 'THEN VS NOW' centred across the dividing line. Red hand-drawn arrow on right side pointing at the suffering version. High contrast between bright left and dark right. Flat 2D cartoon character design consistent across both halves."),
    ]

    for title, concept, text_overlay, emotion, prompt in thumbnails:
        story.append(Paragraph(title, s["thumb_title"]))
        story.append(lbl("VISUAL CONCEPT", s))
        story.append(body(concept, s))
        story.append(lbl("TEXT OVERLAY", s))
        story.append(body(f'"{text_overlay}"', s))
        story.append(lbl("EMOTION TRIGGER", s))
        story.append(body(emotion, s))
        story.append(lbl("STYLE-MATCHED PROMPT", s))
        story.append(body(prompt, s))
        story.append(hr(s))

    return story


# ══════════════════════════════════════════════════════════════════
#  BUILD
# ══════════════════════════════════════════════════════════════════

def build_pdf():
    doc = SimpleDocTemplate(
        OUTPUT,
        pagesize=A4,
        leftMargin=2*cm, rightMargin=2*cm,
        topMargin=2.2*cm, bottomMargin=2*cm,
        title="Barely Evolved — YouTube Content Package",
        author="YouTube Content Cloning Workflow",
    )

    s = make_styles()
    story = build_content(s)

    # Two-pass build: cover page uses dark background, rest uses light
    page_count = [0]

    def on_page(canvas_obj, doc_obj):
        page_count[0] += 1
        if page_count[0] == 1:
            cover_background(canvas_obj, doc_obj)
        else:
            normal_background(canvas_obj, doc_obj)

    doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
    print(f"PDF saved → {OUTPUT}")

if __name__ == "__main__":
    build_pdf()
