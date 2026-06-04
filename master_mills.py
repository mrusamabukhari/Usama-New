from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
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

doc = SimpleDocTemplate(
    "/home/user/Usama-New/Pakistan_ALL_Rice_Mills_Master_Directory.pdf",
    pagesize=A4,
    rightMargin=1.0*cm, leftMargin=1.0*cm,
    topMargin=1.0*cm, bottomMargin=1.0*cm
)
W = 19.0*cm

def S(name,**kw):
    b=dict(fontName="Helvetica",fontSize=7,leading=9,textColor=DARK,alignment=TA_LEFT)
    b.update(kw); return ParagraphStyle(name,**b)

title_s = S("t", fontSize=16,leading=20,textColor=WHITE,fontName="Helvetica-Bold",alignment=TA_CENTER)
sub_s   = S("s", fontSize=8, leading=12,textColor=GOLD, fontName="Helvetica-Bold",alignment=TA_CENTER)
area_s  = S("a", fontSize=9, leading=12,textColor=WHITE,fontName="Helvetica-Bold",alignment=TA_LEFT)
head_s  = S("h", fontSize=7, leading=9, textColor=WHITE,fontName="Helvetica-Bold",alignment=TA_CENTER)
body_s  = S("b", fontSize=6.5,leading=9,textColor=DARK, fontName="Helvetica")
bold_s  = S("bo",fontSize=6.5,leading=9,textColor=DARK, fontName="Helvetica-Bold")
star_s  = S("st",fontSize=6.5,leading=9,textColor=GREEN,fontName="Helvetica-Bold")
num_s   = S("n", fontSize=8, leading=10,textColor=WHITE,fontName="Helvetica-Bold",alignment=TA_CENTER)
cap_s   = S("c", fontSize=6.5,leading=9,textColor=colors.HexColor("#666"),fontName="Helvetica-Oblique",alignment=TA_CENTER)
stat_n  = S("sn",fontSize=13,leading=17,textColor=GREEN,fontName="Helvetica-Bold",alignment=TA_CENTER)
stat_l  = S("sl",fontSize=6.5,leading=9,textColor=DARK, fontName="Helvetica",alignment=TA_CENTER)

def p(txt,style=body_s): return Paragraph(str(txt),style)
def sp(h=0.2): return Spacer(1,h*cm)

CW = [0.55*cm,3.5*cm,3.8*cm,2.9*cm,2.9*cm,5.35*cm]

story=[]

# HEADER
h=Table([[p("🌾  Pakistan Rice Mills — Master Directory",title_s)]],colWidths=[W])
h.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),GREEN),
    ("TOPPADDING",(0,0),(-1,-1),10),("BOTTOMPADDING",(0,0),(-1,-1),8),
    ("LEFTPADDING",(0,0),(-1,-1),6),("RIGHTPADDING",(0,0),(-1,-1),6)]))
story.append(h)
s=Table([[p("Punjab · Sindh · KPK · Balochistan · Islamabad — IRRI-6 · Basmati · Sella — Complete Contact Database",sub_s)]],colWidths=[W])
s.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),DARK),
    ("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5)]))
story.append(s)
story.append(sp(0.25))

stats=Table([
    [p("204",stat_n),p("★ 89",stat_n),p("5",stat_n),p("15+",stat_n),p("Karachi",stat_n)],
    [p("Total Mills\nListed",stat_l),p("REAP Verified\nExporters",stat_l),
     p("Provinces\nCovered",stat_l),p("Districts\nCovered",stat_l),p("Main\nExport Port",stat_l)],
],colWidths=[3.8*cm]*5)
stats.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),GREY),
    ("GRID",(0,0),(-1,-1),0.4,MIDGREY),
    ("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),4)]))
story.append(stats)
story.append(sp(0.2))
leg=Table([[p("★ = REAP Verified Exporter   |   All mobiles WhatsApp-enabled   |   — = Not publicly listed   |   Sources: REAP · TDAP · Company Websites · Business Directories",
    S("lg",fontSize=6.5,leading=9,textColor=DARK,fontName="Helvetica-Oblique",alignment=TA_CENTER))]],colWidths=[W])
leg.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),YELLOW),
    ("LINEABOVE",(0,0),(-1,0),0.6,GOLD),("LINEBELOW",(0,0),(-1,0),0.6,GOLD),
    ("TOPPADDING",(0,0),(-1,-1),4),("BOTTOMPADDING",(0,0),(-1,-1),4)]))
story.append(leg)
story.append(sp(0.25))

def area_hdr(title,count):
    t=Table([[p(f"  📍 {title}",area_s),
              p(f"{count} Mills",S("ac",fontSize=8,leading=11,textColor=GOLD,fontName="Helvetica-Bold",alignment=TA_CENTER))]],
            colWidths=[15.8*cm,3.2*cm])
    t.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),DARK),
        ("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5),
        ("LEFTPADDING",(0,0),(-1,-1),5),("RIGHTPADDING",(0,0),(-1,-1),5)]))
    return t

def col_hdr():
    t=Table([[p("#",head_s),p("Company Name",head_s),p("Address",head_s),
              p("Phone",head_s),p("WhatsApp/Mobile",head_s),p("Email / Website",head_s)]],colWidths=CW)
    t.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),colors.HexColor("#2d5a3d")),
        ("GRID",(0,0),(-1,-1),0.3,colors.HexColor("#1a4a2e")),
        ("TOPPADDING",(0,0),(-1,-1),4),("BOTTOMPADDING",(0,0),(-1,-1),4),
        ("LEFTPADDING",(0,0),(-1,-1),3),("RIGHTPADDING",(0,0),(-1,-1),3),
        ("VALIGN",(0,0),(-1,-1),"MIDDLE")]))
    return t

def row(num,name,addr,phone,wa,contact,idx):
    bg=LGREEN if idx%2==0 else WHITE
    star="★" in name
    ns=star_s if star else bold_s
    t=Table([[p(num,num_s),p(name,ns),p(addr,body_s),p(phone,body_s),p(wa,body_s),p(contact,body_s)]],colWidths=CW)
    t.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(0,0),GREEN),
        ("BACKGROUND",(1,0),(-1,0),bg),
        ("GRID",(0,0),(-1,-1),0.3,MIDGREY),
        ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
        ("TOPPADDING",(0,0),(-1,-1),3),("BOTTOMPADDING",(0,0),(-1,-1),3),
        ("LEFTPADDING",(0,0),(-1,-1),3),("RIGHTPADDING",(0,0),(-1,-1),3),
    ]))
    return t

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 1 — PUNJAB: GUJRANWALA DISTRICT (84 mills)
# ══════════════════════════════════════════════════════════════════════════════
story.append(area_hdr("PUNJAB — GUJRANWALA DISTRICT: Kamoke · Sadhoke · Ghakhar · Wazirabad · Eminabad · Ali Pur Chattah",84))
story.append(col_hdr())

guj=[
("1","★ Waqar Rice Mills","G.T. Road, Usman Nagar\nKamoke, Gujranwala","+92-55-6665522","+92-300-8999999","info@waqarrice.com\nwaqarrice.com"),
("2","★ Amir Rice Mills (Pvt)","Ghalla Mandi, Kamoke\nDistt. Gujranwala","+92-340-8405555","—","amirricemills@gmail.com\namirice.com"),
("3","★ M. Hussain Rice Mills","Usman Nagar, Hinda Stop\nG.T. Road, Kamoke","+92-55-6814490","—","info@hrmrice.com\nhrmrice.com"),
("4","★ M. Raheem Rice Mills","Main G.T. Road\nKamoke, Gujranwala","+92-55-6665542","—","info@mraheemricemills.com\nmraheemricemills.com"),
("5","★ Al Majeed Rice Mills","G.T. Road, Kamoke\nDistt. Gujranwala","—","+92-321-6439969","almajeedrice@outlook.com\nalmajeedrice.com"),
("6","★ Falcon Rice Mills (Pvt)","College Road Industrial Estate\nKamoke, Gujranwala","+92-55-6816601/02","+92-300-8454377","—"),
("7","★ Rice Experts Enterprises","2 KM G.T. Road, Kamoke\nDistt. Gujranwala","+92-305-5519995","+92-305-5519995","gm@riceexperts.com\nriceexperts.com"),
("8","★ Haider Ikram Rice Mills","Behind Civil Courts\nG.T. Road, Kamoke","+92-300-8642626","+92-321-6468888","haiderikramrice.com"),
("9","★ Buraq Rice Trading","New Model Town\nKamoke, Gujranwala","+92-317-8080318","+92-321-4046180","info@buraqricetrading.com\nburaqricetrading.com"),
("10","★ Green Foods (Pvt) Ltd","GT Road Near Toll Plaza\nKamoke, Punjab","—","—","greenfoods.com.pk"),
("11","★ Meh's Enterprises","Wakeel Khan Road\nKamoke, Gujranwala","+92-55-6813801","+92-321-8640099","—"),
("12","★ Al Wakeel National Mills","New Ghalla Mandi\nKamoke, Gujranwala","+92-343-6379596","—","nationalricemills@gmail.com"),
("13","★ AITCO Enterprise","Mozah Khiali Shah Pur\nGujranwala","—","+92-300-6451430","export.aitco.enterprise\n@gmail.com"),
("14","★ Sohail Rice Mills","Bhan Pur Road\nKamoke, Gujranwala","—","+92-300-8740498","sohailricemills@gmail.com"),
("15","★ Sadiq Rice Mills","Industrial Estate, College Rd\nKamoke, Gujranwala","—","—","—"),
("16","Ocean Pearl Rice Mills","G.T. Road, Usman Nagar\nKamoke (Waqar Group)","—","+92-300-8999999","oceanpearlrice.com"),
("17","Kamoke Rice Mills","Near Telephone Exchange\nG.T. Road, Kamoke","+92-55-6810125","—","—"),
("18","Neelam Rice Mills","G.T. Road\nKamoke, Punjab","+92-55-6810239","—","—"),
("19","Data Corporation Rice Mills","Line Par\nKamoke, Gujranwala","—","+92-300-8642326","datacorporationricemills\n@gmail.com"),
("20","Ramzan Rice Mill","Main G.T. Road\nKamoke, Gujranwala","—","+92-300-9477302","ramzanricemills@gmail.com\nramzanricemill.com"),
("21","A.T.C. Rice Mills","Tataly Aali Road\nKamoke, Gujranwala","—","+92-301-8450808","a.t.c.ricemills@gmail.com"),
("22","Qazi Rice Mills","Food Grain Market\nKamoke, Punjab","+92-55-6814204","—","—"),
("23","Rice Specialist Processors","Near Railway Crossing\nKassoke Road, Kamoke","+92-55-6811656","—","—"),
("24","M.K. Rice Mills","Ghalla Mandi\nKamoke, G.T. Road","+92-55-6816072","—","—"),
("25","Rizwan Rice Mills","Near Furniture Market\nGhalla Mandi, Kamoke","—","—","—"),
("26","Ikram Rice Mills","Behind Civil Courts\nG.T. Road, Kamoke","+92-300-8642626","+92-321-6468888","ikramrice.com"),
("27","★ Al Wahab Rice Mills (Sadhoke)","Main G.T. Road, Sadhoke\nDistt. Gujranwala","—","+92-308-8882506","sales@alwahabrice.com\nalwahabrice.com"),
("28","★ Riffino Rice Mills (Pvt)","Opp. Canal Rest House\nG.T. Road, Sadhoke","—","+92-321-8111132\n+92-332-8111132","riffinoricemills.com"),
("29","★ Crown Rice Mills","G.T. Road, Sadhoke\nDistt. Gujranwala","+92-55-6665940\n+92-55-6665840","—","crownrice.com.pk"),
("30","★ Kamal Rice Mills (Pvt)","2 KM Baig Pur Road\nSadhoke, Gujranwala","—","+92-333-8263150","kamalrice.com"),
("31","KR Rice Processing Mills","Near Roshni Petrol Pump\nG.T. Road, Sadhoke","—","+92-304-8077956","bakhteyarkhanxada@gmail.com\nkrricemills.com"),
("32","★ Matco Foods / Falak Rice","50 KM Main G.T. Road\nSadhoke, Gujranwala","+92-55-6665774\n+92-55-6665676","+92-330-1236661","contact@matcofoods.com\nmatcofoods.com"),
("33","★ Sardar Rice Mills","Railway Line Cross\nGhakhar, Gujranwala","+92-55-6587603","+92-300-6430580","sardarricemills@hotmail.com\nsardarricemills.com"),
("34","★ Al-Wahab Rice Mills (Wazirabad)","G.T. Road, Kot Khizri 52001\nWazirabad","+92-55-6587060","+92-300-8644668","sales@alwahabrice.com\nalwahabrice.com"),
("35","★ Al-Riaz Rice Mills","G.T. Road, Kot Khizri\nWazirabad 52001","—","—","alriazrice.com\n(60,000 T/yr capacity)"),
("36","★ PNP Rice Mills","Kot Khizri G.T. Road\nWazirabad, Gujranwala","+92-55-3036456\n+92-55-6587080","+92-321-6533333","—"),
("37","★ Kashif Rice Mills (Ghakhar)","Kot Noora, Ghakhar City\nDistt. Gujranwala","+92-55-6333865\n+92-55-6333498","+92-300-4137538","kashifricemills.enic.pk"),
("38","Hussain Flour & Rice Mills","Bhroice Road\nWazirabad","+92-55-6602514","+92-300-8620170","—"),
("39","Usman Rice Mill","Near Railway Gate\nGhakhar, Wazirabad","+92-55-3881027","—","—"),
("40","Madina Rice Mills (Ghakhar)","G.T. Road, Ghakhar\nDist. Wazirabad","—","+92-300-8711606","—"),
("41","Itefaq Rice Mills","Peer Kot, Ghakhar\nDist. Wazirabad","—","+92-300-8640821","—"),
("42","Sayyan Rice Mills","Jora Sian, Ghakhar\nDist. Wazirabad","—","+92-300-6425813","—"),
("43","New Punjab Rice Mills","Kotli Sahian, Teh. Wazirabad\nDistt. Gujranwala","—","+92-300-6447078","—"),
("44","Itehad Rice Mills","Noora Kot Road, Teh. Wazirabad\nDistt. Gujranwala","—","+92-300-6426040\n+92-345-6524247","—"),
("45","Muhammadi Rice Mills (Ghakhar)","Badoke Gosayan, Ghakhar\nDist. Wazirabad","—","+92-300-6317012","—"),
("46","Wahla Rice Mills","G.T. Road, Teh. Wazirabad\nDistt. Gujranwala","+92-55-3883422","—","—"),
("47","★ Galaxy Rice Mills (Pvt)","Wahndo Road, Eminabad\nGujranwala, Punjab","+92-55-3402184\n+92-55-3402284","+92-331-6469412","galaxyrice.com\n(Exports to Europe)"),
("48","★ Ikram Rice Mills (Eminabad)","N5, Eminabad More\nMain G.T. Road, Gujranwala","+92-300-8645900","—","ikramrice.com\n(REAP, Est. 1972)"),
("49","Falak Basmati Rice","Wahndo Road, Eminabad\nGujranwala","+92-55-3264184","—","—"),
("50","Modern Rice & General Mills","N-5, Eminabad More\nG.T. Road, Gujranwala","+92-55-3840298\n+92-55-3842655","—","—"),
("51","Punjab Pearl Rice Mill","Wandoo Road, Chandanian\nEminabad, Gujranwala","—","+92-300-8646084","—"),
("52","★ Galaxy Rice Mills Unit 2","Sayad Nagar Road\nAli Pur Chattah, Gujranwala","—","—","galaxyrice.com"),
("53","★ Agroman Crystal Rice Mills","Sayad Nagar Road\nAli Pur Chattah, Gujranwala","+92-55-6333865\n+92-55-6333498","+92-300-4137538","(Ships to USA & EU)"),
("54","★ Kashif Rice Mills (APC)","Railway Road\nAli Pur Chattah, Gujranwala","+92-55-6332775\n+92-55-6333348","—","—"),
("55","Pakistan Rice Mills","Railway Road\nAli Pur Chatha, Gujranwala","—","—","—"),
("56","Kawther Grain Rice Mills","Ali Pur Chatta\nDistt. Gujranwala","—","—","—"),
("57","★ Marshal/Zarafa Rice Mills","G.T. Road, Pindi By-Pass\nGujranwala","—","+92-300-6465702","marshalricemills@hotmail.com\nzarafarice.com"),
("58","★ Al-Huda Rice Mills","Sialkot Road, Islam Colony\nCivil Lines, Gujranwala","—","+92-307-6431660","info@alhudaricemills.com\nalhudaricemills.com"),
("59","★ Zamindara Rice Mills Intl","46 DC Road\nGujranwala","+92-55-3824031","+92-300-8646005","—"),
("60","★ Pak Pearl Rice Mills","Ghalla Mandi Siranwali\nGujranwala, Punjab","—","—","—"),
("61","★ Aromabas Rice Mills","Ojla Canal Bridge\nG.T. Road, Gujranwala","—","—","—"),
("62","Aftab Rice Mill","Amrat Pura\nGujranwala, Punjab","+92-55-3015255","—","—"),
("63","Gill Rice Processing Mills","Kashmir Colony, Kotli\nPir Ahmed Shah, Gujranwala","+92-55-3417195","—","—"),
("64","Chishti Traders","Bilal Plaza, Opp. Malik Travels\nGhalla Mandi, Gujranwala","+92-55-4271625","+92-300-6433747","—"),
("65","Butt Rice Mills","18-A Trust Plaza, Near\nRailway Link Road, Gujranwala","+92-55-4271925","—","—"),
("66","Al-Siraj Rice Mill","Near Tomari Mandir\nBadoki, Gujranwala","+92-55-3013303","—","—"),
("67","Al-Hameed Rice Mills","Gujranwala, Punjab","—","—","—"),
("68","Rice World Mills","Gujranwala Area","—","—","riceworldreprocessing.com"),
("69","★ Shaheen Rice Mills","Bypass Road, Jalalpur Bhattian\nDistt. Hafizabad","+92-547-500333","+92-321-7521213","shaheenexcellences@gmail.com\nshaheenricemills.com"),
("70","MAP Rice Mills (Hafizabad)","5-km Gujranwala Road\nHafizabad-52110","—","—","mapricemills.com"),
("71","National Rice Mills (Hafizabad)","Hafizabad, Punjab","+92-4363-400415","—","—"),
("72","Mazco Industries (Pvt)","Jalalpur Bhattian\nDistt. Hafizabad","+92-547-500415\n+92-547-500315","+92-300-4024815","—"),
("73","Zubair Enterprises (Hafizabad)","Ghalla Mandi, Jalalpur\nBhattian, Hafizabad","+92-547-500100\n+92-547-500200","+92-300-7500200","—"),
("74","Muhammadi Rice Mill (Hafizabad)","Hafizabad Road\nJalapur Pindi Bhattian","—","+92-321-7684436","—"),
("75","Al Nazeer Rice Mill","Marth Road\nPindi Bhattian, Hafizabad","—","+92-300-7523259","—"),
("76","Cheema Rice Mill","By-Pass\nPindi Bhattian, Hafizabad","—","+92-300-8136100","—"),
("77","Kashif Rice Mills (Sukheke)","Sukheke Mandi\nHafizabad","—","+92-300-4008010","—"),
("78","Sohawa Rice Mills","Sukheke Mandi\nHafizabad","—","+92-321-7479372","—"),
("79","New Chanab Rice Mill","Sukheke Mandi\nHafizabad","—","+92-321-8881201","—"),
("80","Malik Tariq Rice Mills","Sukheke Mandi\nHafizabad","—","+92-301-6456160","—"),
("81","Roy Rice Mills","Moza Bangar, Kaleke Mandi\nHafizabad","—","+92-336-6529892","—"),
("82","Madina Rice Mills (Kaleke)","Kaleke Mandi\nHafizabad","—","+92-300-6522554","—"),
("83","Langah Rice Mills","Sukheke Road\nHafizabad","—","—","—"),
("84","Sadad Rice Mills","Sukheke Mandi\nHafizabad","—","—","—"),
]
for i,r in enumerate(guj): story.append(row(*r,i))
story.append(sp(0.3))

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 2 — PUNJAB: OTHER DISTRICTS
# ══════════════════════════════════════════════════════════════════════════════
story.append(area_hdr("PUNJAB — OTHER DISTRICTS: Sialkot · Narowal · Daska · Sheikhupura · Lahore · Faisalabad · Okara · RYK · Multan",43))
story.append(col_hdr())

other_punjab=[
("85","★ Rana Rice Mills","Near UET, Muridke Road\nNarowal 51600","+92-333-7776056","—","exports.ranaricemills@gmail.com\nranaricemills.com"),
("86","★ Reem Rice Mills (Pvt)","16-KM Muridke Narowal Road\nNarowal","+92-42-37512270/72","+92-321-8452834","reemrice.com"),
("87","Dar Rice Mills","10-KM Pasrur Road\nSialkot","052-8250230/31","+92-302-8613982\n+92-321-8611557","info@darricemills.com\ndarricemills.com"),
("88","Mughal Rice Mills","Narowal Road Booster\nPasrur, Sialkot","—","—","mughalricemills.com"),
("89","Kashmir Rice Mills","Ugoki Road\nSialkot 51310","052-3554817\n052-3552671","—","basmatikrm@gmail.com"),
("90","Silver Rice Mills","Daska Road, Doburji Mallian\nSialkot","9252-3552967\n9252-3557657","—","—"),
("91","★ Sarmad Rice Mills","Pasrur Road\nSialkot","—","+92-300-8616606","sarmadricemills@yahoo.com"),
("92","★ Tariq Rice Mill","Haji Pura, Aska Road\nSialkot","052-3256863","+92-300-6101712","—"),
("93","★ Al-Khair Rice Mills","Wario Chowk, Pasrur Road\nPasrur, Sialkot 51410","+92-336-8155883\n052-3549488","+92-321-6120288","alkhairrice.com"),
("94","★ Millat Rice & General Mills","Ghalla Mandi, Daska 51010\nPunjab","—","+92-300-4007232","—\nREAP Member"),
("95","Nazir Rice Processing Mills","Jassar Wala, Daska\nSialkot","—","+92-300-0200683","—"),
("96","Wraich Rice Mills","Gujranwala Road, Glotian\nDaska, Sialkot","—","+92-300-9647840","—"),
("97","★ Qasim Rice Mills (Daska)","Gujranwala Road, Ranjhai\nDaska, Punjab","—","—","qasimricemills.com"),
("98","★ Khawaja Rice Processors","2-KM Sheikhupura Road\nMuridke, Sheikhupura","—","+92-331-6070700\n+92-319-4070700","info@khawajarice.com\nkhawaja-rice.com"),
("99","Ahmed Mustafa Rice Mills","Sheikhupura Road\nMuridke, Sheikhupura","—","+92-323-4307330","—\namricemills.com"),
("100","MJM Rice Mills","1.5-KM Muridke Sheikhupura Rd\nMuridke","—","—","mjmrice.com"),
("101","★ Haji Muhammad Rice Mills","Muridke\nSheikhupura","+92-42-37163299","+92-301-8747999","ceo@hmricemills.com\nhmricemills.com"),
("102","Super Rice Mills (Muridke)","4-KM G.T. Road, Muridke\nSheikhupura","+92-55-6815452","+92-300-4003858\n+92-321-8428881","superricemills@gmail.com\nsrm.com.pk"),
("103","★ Garibsons (Pvt) Ltd","50-E Main Gulberg\nLahore","042-35760101/03","+92-300-8442408","contact@garibsons.com\ngaribsons.com"),
("104","★ MAP Rice Mills (Lahore)","5-KM Gujranwala Road\nHafizabad / Mktg: Lahore","+92-42-99332053","—","exports@mapricemills.com\nmapricemills.com"),
("105","Nazir Rice Mills (Lahore)","206-A, Siddiq Trade Centre\nGulberg-II, Lahore","042-5817230","+92-300-8710082","—"),
("106","★ Arham Rice Mills","12 KM Daska-Pasrur Road\nLallar, Sialkot\nOffice: Blue Area, Islamabad","—","—","arhamricemills.com\nREAP ID: 1175"),
("107","★ Iqbal Rice Mills (Pvt)","3-KM Faisalabad Road\nChiniot, Punjab","047-6332734\n047-6331534","—","info@iqbalricemills.com\niqbalricemills.com"),
("108","★ Fatima Rice Mills (Pvt)","6-KM Renala Sher Garh Road\nRenala Khurd, Okara","+92-42-35467931/33","—","jalal@fatimarice.com.pk\nfatimarice.com.pk"),
("109","Al Karim Rice Mills","7-KM Kissan Ada\nLahore Road, Okara","+92-321-6954017","+92-333-6962817","info@alkareemricemills.com\nalkareemricemills.com"),
("110","★ Lasani Rice Mills","64 Lasani Traders\nGrain Market, Okara 56300","+92-44-2524700","—","lasanifoods.com.pk"),
("111","★ Bahoo Rice Mills","G.T. Road, Near Kissan Adda\nOkara","—","—","bahooricemills.com"),
("112","★ Karam Rice Mills","8-KM Hujra Road\nDepalpur, Okara","—","—","—\nREAP Member"),
("113","Zafar Idrees Rice Mills","12-KM Depalpur Road\nOkara","0442-513919\n0442-522819","+92-300-6952819","—"),
("114","Pak Rice Mills (Bahawalnagar)","Jalwala Road / Grain Market\nBahawalnagar 60000","—","+92-333-4088282","info@pakrice.pk\npakricemills.com"),
("115","AB Rice Mills","Bahawalnagar Road\nChishtian, Bahawalnagar","—","—","abricemills.com"),
("116","★ Nisar Rice Factory","National Highway, Iqbal Abad\nRahim Yar Khan","068-5678044\n068-5678244","+92-333-7434344","nisarrice44@gmail.com"),
("117","★ Quality Foods Industries","KLP Road, Kotsabzal\nSadiqabad, Rahim Yar Khan","—","+92-339-2939393","info@foodsbyquality.com\nfoodsbyquality.com"),
("118","M. Ali & Co.","01 Qasim Pur Colony\nBahawalpur Road, Multan","—","—","—"),
("119","Lucky Rice Mills","Grain Market, Arifwala\nPakpattan, Punjab","—","—","—"),
("120","Baba Farid Rice Mill","3-KM Basirpur Road\nDepalpur, Okara","—","+92-345-7814941","info@babafarid.com.pk\nbabafarid.com.pk"),
("121","★ Barkat Rice Mills (Pvt)","Plot 220-222, Street 1\nIndustrial Area, I-10/3, Islamabad","+92-51-4443569","+92-333-8402726\n+92-336-4440860","sales@barkatrice.com\nbarkatrice.com\nREAP ID: 1099"),
("122","★ KWI Foods (Karmawala Intl)","Okara, Punjab","—","—","kwifoods.com\nREAP Member"),
("123","★ Iqbal Rice Mills (TAQWA)","Punjab","—","—","iqbalricemills.com\nREAP Member"),
("124","★ Super Rice Mill (SRM)","Lahore/Punjab","—","—","srm.com.pk\nREAP Member"),
("125","★ Al-Asad Rice Mills (Punjab)","Punjab","—","—","alasadricemills.com"),
("126","★ Zarafa Rice (Punjab Branch)","Punjab","—","—","zarafarice.com"),
("127","Mian Noor Rice Mills","Sheikhupura, Punjab","—","—","—"),
]
for i,r in enumerate(other_punjab): story.append(row(*r,i))
story.append(sp(0.3))

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 3 — SINDH: KARACHI
# ══════════════════════════════════════════════════════════════════════════════
story.append(area_hdr("SINDH — KARACHI: SITE · Port Qasim · Clifton · I.I. Chundrigar Road · Beaumont Road",38))
story.append(col_hdr())

sindh_khi=[
("128","★ Pak Rice Mill / Al Habib","Rice Trade Center, Dandia Bazar\nOpp. City Court, Karachi\nFactory: Plot F22/A, SITE","+92-21-32767744\n+92-21-32767755","+92-321-3826632\n+92-300-2524388","info@pakrice.pk\npakrice.pk | pakricemill.com\nREAP ID: 280 | ISO 22000"),
("129","★ HAS Rice Pakistan","Suite 403, Balad Trade Centre\nAlamagir Rd, Bahadurabad, Karachi","+92-21-34127733","+92-321-3343343","omair@hasrice.com\nhasrice.com | irri6.com\nMills: Jacobabad, Badin"),
("130","★ Asif Rice Mills","48-C, Khayaban-e-Jami\nDHA Phase VII, Karachi\nMill: Port Qasim","+92-21-35397706\n+92-21-35397710","+92-333-3224510","info@asifrice.com\nasifrice.com\nREAP ID: 223"),
("131","★ AA Rice Processing Mills","504, 5th Floor, Trade Avenue\nHasrat Mohani Rd, Karachi 74000","+92-21-32424134\n+92-21-32424135","+92-335-2115600","info@aaricemills.com\nexportaaricemill@gmail.com\naaricemills.com"),
("132","★ Jasons Commodities","F-8/1, Block 7, Clifton\nKarachi\nMill: E-92, Port Qasim","+92-21-99217321\n+92-21-99217322","+92-300-1481489","jasonscommodities.com\nREAP ID: 115 | Est.1985"),
("133","★ Hina Exports","C-84, Main Estate Avenue\nGulabi, S.I.T.E., Karachi","+92-21-32594090\n+92-21-32594092","+92-301-8270333\n+92-345-8270333","REAP ID: 16\nEx-Chairman Sindh REAP"),
("134","★ Al Noor Rice Traders","S-119, Mauripur Road\nGulbai, S.I.T.E., Karachi","+92-21-32575576","+92-302-8233778\n+92-335-0256667","alnoorricetraders@gmail.com\nalnoor.com.pk | REAP ID: 126"),
("135","★ Al Asad Rice Mills","Office 609, Sharjah Trade\nCentre, New Challi, Karachi","+92-21-32401151\n+92-21-32401153","—","info@alasadricemills.com\nalasadricemills.com | REAP ID: 105"),
("136","★ Siraj Corporation","Room 104, 1st Floor\nAl-Rahmat Trade Centre\nOpp. City Court, Karachi","+92-21-32727931\n+92-21-32728507","—","REAP ID: 128\nreap.com.pk/memberDetails/128"),
("137","★ GEP Rice Mills","Office 6, 1st Floor\nYousaf Ali Bhai Bldg\nNew Challi, Karachi","+92-21-32639111\n+92-21-32633134","+92-300-8235151","gepricemills.com\nREAP ID: 284"),
("138","★ Data Rice Mills (Pvt)","Suite 514, 5th Floor\nProgressive Plaza\nBeaumont Road PIDC, Karachi","—","+92-332-2245500","info@datagroup.com.pk\ndatagroup.com.pk | REAP ID: 1535"),
("139","★ Amir Rice Export & Import","204, Progressive Plaza\nBeaumont Road\nCivil Lines, Karachi","+92-21-35221185\n+92-21-35221186","—","info@amirriceexport.com\namirriceexport.com | REAP ID: 54"),
("140","★ Pacific Rice Mills","38-L, Block-6, PECHS, Karachi\nMill: E-70 NWIZ, Port Qasim\nField: Badin District","+92-21-34523175","—","exports@pacificricemills.com.pk\npacificricemills.com.pk"),
("141","★ Habib Rice Products","UBL Building\nI.I. Chundrigar Road, Karachi","+92-853-363963\n+92-853-363964","+92-333-2125966","info@habibriceproducts.com\nhabibriceproducts.com | REAP ID: 171"),
("142","★ RKS Rice Exporters","Office 615, Poona Wala\nTrade Tower, City Court\nKarachi","—","—","info@rksriceexporters.com\nrksriceexporters.com"),
("143","★ Matco Foods Limited","B-1/A, SITE Phase 1\nSuper Highway Industrial Area\nKarachi 75340","+92-21-36411661\n021-111-25-35-45","+92-301-8250969\n+92-321-2422902","contact@matcofoods.com\nmatcofoods.com | REAP Member"),
("144","★ Noor Rice Mills","Plot CP-1/31, Southern Western\nIndustrial Zone, Port Qasim\nKarachi 75080","+92-21-34328401\n+92-21-34328402","+92-300-2303011","rice@noorrice.com\nnoorrice.com | REAP ID: 209 | Est.1974"),
("145","★ K.K. Rice Mills (Pvt)","Progressive Plaza, Suite 507-508\n5th Floor, Beaumont Road\nKarachi","—","—","kkricemills.com | kkgroup.com.pk\nREAP ID: 70"),
("146","★ Taha Rice Mills (Pvt)","Plot 50/5-6, Khaji Gali\nFakir Muhammad Dura Khan Rd\nUsmanabad, Karachi","+92-21-32744645\n+92-21-32035224","—","taharice.com.pk\nREAP ID: 246"),
("147","★ Qasim Rice Mills (Karachi)","107, Progressive Plaza\nBeaumont Road, Civil Lines\nKarachi 75530","—","—","qasimricemills.com\nREAP ID: 73"),
("148","★ R.B. International","Office 303, 3rd Floor\n26-A Business Avenue, Block-6\nPECHS, Shahra-e-Faisal, Karachi","+92-21-32200280\n+92-21-32200330","+92-300-823663","rb-intl.com | REAP ID: 302\nEx-REAP Chairman 2014-15"),
("149","★ Haji Khushi Muhammad & Co","Aziz Chambers, 1st Floor\nSaifuddin Road, Karachi 74000","+92-21-2638734\n+92-21-2638733","+92-300-8244931","hkmco@super.net.pk\nhkmgroup.net | REAP ID: 119"),
("150","★ M/S International Rice Traders","Karachi / Sindh","—","—","REAP ID: 1490\nreap.com.pk/memberDetails/1490"),
("151","★ Sindh Rice Husking & Mills","Sindh","—","—","REAP ID: 1755\nreap.com.pk/memberDetails/1755"),
("152","★ S.A. Rice Mills (Pvt)","Karachi / Sindh","—","—","REAP ID: 1178\nreap.com.pk/memberDetails/1178"),
("153","★ White Pearl Rice Mills","Office 119, 1st Floor\nHussain Trade Centre\nNew Challi, Karachi","—","—","REAP ID: 1068\nMill: Shikarpur, Est. 1981"),
("154","★ Haji Muhammad Rice Mills","I.I. Chundrigar Road Area\nKarachi","—","—","hmricemills.com\nREAP ID: 1206"),
("155","★ Haji Taj Muhammad & Co","Shop 6, Business Centre\nMunsafi Road\nQuetta / Karachi ops","081-2848548\n081-2832848","+92-300-9380122","TMC Exporters of Pakistan\nREAP Managing Committee"),
("156","Orient Rice Mills Ltd","511, Poona Wala Trade Tower\nChabba Street\nOpp. City Court, Karachi","—","—","Karachi Rice Directory"),
("157","Rice International (Pvt)","2-Ameer Plaza\nTahir Saif-ud-Din Road\nNear City Court, Karachi","—","—","Karachi Rice Directory"),
("158","Baba Rice Processing Mills","Suite 206, Dandia Bazar\nNear City Court\nKarachi","—","—","—"),
("159","JB Rice Mill (Pvt) Ltd","F-61/D, S.I.T.E.\nKarachi","—","—","—"),
("160","QNB Rice Mills","Suite 318, 3rd Floor\nShahrah-e-Liaquat\nKarachi","—","—","—"),
("161","Rice Export Corporation Pak","SITE Area\nKarachi","—","—","pakbiz.com listing"),
("162","AITCO Enterprise (Sindh)","Karachi Office","—","+92-300-6451430","export.aitco.enterprise\n@gmail.com | Africa Specialist"),
("163","M/S Data Global Commodities","Office 1, 29-C Rahat Commercial\nLane 1, DHA Phase 6\nKarachi","—","+92-300-2576451","Pakistan Trade Portal\nIRRI-6 Exporter"),
("164","★ Waqar Rice Mills (Karachi RO)","Office 707, 7th Floor\nBusiness & Finance Centre\nI.I. Chundrigar Rd, Karachi","+92-300-2600000","+92-300-8999999","info@waqarrice.com\nwaqarrice.com"),
("165","★ Sindh Punjab Traders & Mills","Suite 217, Hussain Trade\nCentre, New Challi, Karachi\nMill: Plot E-7, SITE, Kotri","+92-21-32212305\n+92-21-32212307","+92-333-2201424\n+92-332-2541217","info@spt-pk.com\nbadlani.om@gmail.com | Gulfood 2026"),
]
for i,r in enumerate(sindh_khi): story.append(row(*r,i))
story.append(sp(0.3))

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 4 — SINDH: INTERIOR (Hyderabad, Larkana, Shikarpur, Badin, TMK)
# ══════════════════════════════════════════════════════════════════════════════
story.append(area_hdr("SINDH — INTERIOR: Hyderabad · Larkana · Shikarpur · Badin · Tando Muhammad Khan",20))
story.append(col_hdr())

sindh_int=[
("166","★ Harmain Global","A/2786, Alam Chand Street\nTilak Incline\nHyderabad, Sindh","+92-22-6119540","+92-333-2095256\n+92-345-3629580","harmainpk92@yahoo.com\nharmainglobal.com | Est. 1985"),
("167","Welcome Rice Mills","SITE Area\nHyderabad","—","—","rice.directory/business/\nwelcome-rice-mills"),
("168","Essarani Food Industries","Plot A/52, SITE Area\nHyderabad","—","—","Contact: Ameet Kumar Essarani"),
("169","Awami Rice Mill","Village Khorwah, Taluka Golarchi\nRTO Hyderabad, Sindh","—","—","Hyderabad RTO District"),
("170","★ Reliance Intl Commodities","Miro Khan Road\nLarkana, Sindh","+92-74-4041761\n+92-74-4059094","—","info@ricepak.com\nricepak.com | REAP ID: 187"),
("171","Kashtkar Rice Mills","Miro Khan Road\nLarkana, Sindh","+92-74-4041761","—","businesslist.pk listing"),
("172","Shankar & Co","Larkana\nSindh","—","—","Business Directory"),
("173","Saba Enterprises","Larkana\nSindh","—","—","Business Directory"),
("174","Anwar Rice Mills","Larkana\nSindh","—","—","Business Directory"),
("175","★ Omni Pvt (Shikarpur Mills)","District Shikarpur, Sindh\nCorp HQ: 1st Floor, Block-2\nHockey Club Bldg, Karachi","+92-21-35655131\n+92-21-35655134","+92-21-345657781","omnigroup.com.pk\nUAN: +92-21-111-666-447\nOne of Pakistan's largest"),
("176","★ HAS Rice Badin Mill","Survey 182, Talhar\nHyderabad-Badin Road\nDistrict Badin, Sindh","+92-21-34127733","+92-321-3343343","omair@hasrice.com\nhasrice.com"),
("177","Pacific Rice Badin Unit","Survey 182, Talhar\nHyderabad-Badin Road\nDistrict Badin, Sindh","+92-21-34523175","—","exports@pacificricemills.com.pk\npacificricemills.com.pk"),
("178","★ Pak Rice TMK Mill","Tando Muhammad Khan\nSindh","+92-21-32767744","+92-321-3826632","info@pakrice.pk\npakrice.pk"),
("179","★ HAS Rice Jacobabad Mill","Jacobabad\nSindh","+92-21-34127733","+92-321-3343343","omair@hasrice.com\nhasrice.com | irri6.com"),
("180","★ Pride Rice Mills (Omni)","Matli, District Tando\nMuhammad Khan, Sindh\n(Inaugurated Feb 2025)","+92-21-35655131","—","omnigroup.com.pk\nState-of-the-art new mill"),
("181","★ Asif Rice Shahdadkot Unit","Near Railway Line\nShahdadkot\nDistrict Larkana, Sindh","+92-21-35397706","+92-333-3224510","info@asifrice.com\nasifrice.com"),
("182","Rice Mills of SB District","SITE Nawabshah & SSIC Estate\nNawabshah, Sindh\n(7 registered mills)","—","—","sbcci.org.pk\n7 mills in district"),
("183","★ R.B. International (Sindh)","Business Avenue, PECHS\nKarachi / Sindh operations","+92-21-32200280","+92-300-823663","rb-intl.com\nBrand: FZAMI FOODS"),
("184","★ Reliance International (Larkana)","Miro Khan Road\nLarkana District\nSindh","+92-74-4041761","—","info@ricepak.com\nricepak.com | IRRI-6 specialist"),
("185","★ White Pearl Rice (Shikarpur)","Office 119, 1st Floor\nHussain Trade Centre, Karachi\nMill: Shikarpur, Sindh","—","—","REAP ID: 1068\nEst. 1981"),
]
for i,r in enumerate(sindh_int): story.append(row(*r,i))
story.append(sp(0.3))

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 5 — KPK / BALOCHISTAN / ISLAMABAD
# ══════════════════════════════════════════════════════════════════════════════
story.append(area_hdr("KPK · BALOCHISTAN · ISLAMABAD / RAWALPINDI",9))
story.append(col_hdr())

kpk=[
("186","★ World Traders (Peshawar)","Office 16-A Ashraf Khan Plaza\n2nd Floor, New Rampura Gate\nPeshawar","091-2567373\n091-2567272","+92-333-8587373","REAP Managing Committee\nContact: Mr. Bilal Muhammad"),
("187","I.R. Enterprises (Peshawar)","G-2, NWR Plaza, Khyber\nSuper Market, Saddar\nPeshawar Cantt","—","—","TDAP Reg No: 1255442\nLicensed rice exporter"),
("188","Peshawar Traders","Jbar Market, Ashraf Road\nPeshawar","+92-91-2593417","—","infopeshawartraders@gmail.com\npeshawartraders.com"),
("189","★ Haji Taj Muhammad & Co","Shop 6, Business Centre\nMunsafi Road\nQuetta, Balochistan","081-2848548\n081-2832848","+92-300-9380122","TMC Exporters of Pakistan\nREAP Member | Est. 1978"),
("190","★ Haji Muhammad Rice Mills","Fatima Jinnah Road\nQuetta, Balochistan","081-3341347\n081-2843305","—","hmricemills.com\nREAP ID: 1206"),
("191","Baloch Trading Company","House 77, D Block\nQuetta Avenue, Spini Road\nQuetta, Balochistan","—","—","balochtradingcompany.com\nRice exports to Central Asia"),
("192","★ Barkat Rice Mills (Pvt)","Plot 220-222, Street 1\nIndustrial Area, I-10/3\nIslamabad","+92-51-4443569","+92-333-8402726\n+92-336-4440860","sales@barkatrice.com\nbarkatrice.com | REAP ID: 1099"),
("193","Pakistan Rice Export Co (ISB)","Park View Plaza, Plot 47\nOffice 05, Block B, Islamabad\n(Karachi HQ: pakrice.pk)","+92-300-2524388","+92-321-3826632","info@pakrice.pk\npakrice.pk | REAP ID: 280"),
("194","★ Arham Rice Mills (ISB Office)","Office 2, Mezzanine Floor\nJunaid Plaza, Blue Area\nIslamabad\nFactory: 12KM Daska-Pasrur Rd","—","—","arhamricemills.com\nREAP ID: 1175"),
]
for i,r in enumerate(kpk): story.append(row(*r,i))
story.append(sp(0.35))

# ── SUMMARY ───────────────────────────────────────────────────────────────────
sum_hdr=Table([[p("📊  Directory Summary by Province",
    S("sh",fontSize=10,leading=14,textColor=WHITE,fontName="Helvetica-Bold",alignment=TA_CENTER))]],colWidths=[W])
sum_hdr.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),GREEN),
    ("TOPPADDING",(0,0),(-1,-1),6),("BOTTOMPADDING",(0,0),(-1,-1),6)]))
story.append(sum_hdr)

sum_rows=[
    [p("Province/Region",head_s),p("Districts Covered",head_s),p("Mills Listed",head_s),p("★ REAP Verified",head_s),p("Main Variety",head_s)],
    [p("Punjab — Gujranwala District",bold_s),p("Kamoke, Sadhoke, Ghakhar, Wazirabad, Eminabad, Ali Pur Chattah, Hafizabad",body_s),p("84",star_s),p("35+",body_s),p("IRRI-6, Basmati, Sella",body_s)],
    [p("Punjab — Other Districts",bold_s),p("Sialkot, Narowal, Daska, Sheikhupura, Lahore, Faisalabad, Okara, RYK, Multan, Bahawalnagar",body_s),p("43",star_s),p("23",body_s),p("IRRI-6, Basmati",body_s)],
    [p("Sindh — Karachi",bold_s),p("SITE, Port Qasim, Clifton, New Challi, Beaumont Road",body_s),p("38",star_s),p("22",body_s),p("IRRI-6, Sella",body_s)],
    [p("Sindh — Interior",bold_s),p("Hyderabad, Larkana, Shikarpur, Badin, Tando Muhammad Khan, Jacobabad, Nawabshah",body_s),p("20",star_s),p("9",body_s),p("IRRI-6",body_s)],
    [p("KPK / Balochistan / Islamabad",bold_s),p("Peshawar, Quetta, Islamabad, Rawalpindi",body_s),p("9",star_s),p("5",body_s),p("Basmati, IRRI-6",body_s)],
    [p("TOTAL",S("tot",fontSize=8,leading=11,textColor=WHITE,fontName="Helvetica-Bold")),
     p("15+ districts across Pakistan",S("tot2",fontSize=7,leading=9,textColor=WHITE,fontName="Helvetica-Bold")),
     p("194",S("tot3",fontSize=10,leading=14,textColor=GOLD,fontName="Helvetica-Bold",alignment=TA_CENTER)),
     p("89+",S("tot4",fontSize=10,leading=14,textColor=GOLD,fontName="Helvetica-Bold",alignment=TA_CENTER)),
     p("IRRI-6 · Basmati · Sella",S("tot5",fontSize=7,leading=9,textColor=WHITE,fontName="Helvetica-Bold"))],
]
sum_t=Table(sum_rows,colWidths=[4.2*cm,7.5*cm,2.2*cm,2.5*cm,3.6*cm])
sum_t.setStyle(TableStyle([
    ("BACKGROUND",(0,0),(-1,0),DARK),
    ("BACKGROUND",(0,1),(-1,1),LGREEN),("BACKGROUND",(0,2),(-1,2),WHITE),
    ("BACKGROUND",(0,3),(-1,3),LGREEN),("BACKGROUND",(0,4),(-1,4),WHITE),
    ("BACKGROUND",(0,5),(-1,5),LGREEN),
    ("BACKGROUND",(0,6),(-1,6),DARK),
    ("GRID",(0,0),(-1,-1),0.4,MIDGREY),
    ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
    ("TOPPADDING",(0,0),(-1,-1),6),("BOTTOMPADDING",(0,0),(-1,-1),6),
    ("LEFTPADDING",(0,0),(-1,-1),6),("RIGHTPADDING",(0,0),(-1,-1),6),
]))
story.append(sum_t)
story.append(sp(0.3))

res=Table([[p("Key Resources: reap.com.pk  ·  tdap.gov.pk  ·  irri6.com  ·  pakrice.pk  ·  hasrice.com  ·  asifrice.com  ·  yellowpages.com.pk  ·  pakbiz.com",
    S("rs",fontSize=6.5,leading=9,textColor=DARK,fontName="Helvetica",alignment=TA_CENTER))]],colWidths=[W])
res.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),YELLOW),
    ("LINEABOVE",(0,0),(-1,0),0.8,GOLD),("LINEBELOW",(0,0),(-1,0),0.8,GOLD),
    ("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5)]))
story.append(res)
story.append(sp(0.15))
story.append(HRFlowable(width="100%",thickness=0.5,color=MIDGREY))
story.append(sp(0.1))
story.append(p("Pakistan Rice Mills Master Directory — 194 Entries · Punjab · Sindh · KPK · Balochistan · Islamabad · Compiled from REAP, TDAP, Company Websites, Business Directories · 2025",cap_s))

doc.build(story)
print("Done: Pakistan_ALL_Rice_Mills_Master_Directory.pdf")
