"""
Instagram Content Generator for Linen House Export Business
Uses Claude API to generate captions, hashtags, and content calendars.
"""

import anthropic
import json
import random
from datetime import datetime, timedelta

client = anthropic.Anthropic()

CONTENT_THEMES = [
    "product_showcase",
    "behind_the_scenes",
    "client_testimonial",
    "export_process",
    "quality_highlight",
    "bulk_deal_offer",
    "lifestyle_styling",
    "factory_tour",
]

LINEN_PRODUCTS = [
    "bed sheets", "duvet covers", "pillowcases", "table linen",
    "bath towels", "kitchen towels", "curtain fabric", "cushion covers",
    "hotel-grade linen", "restaurant table cloths",
]

HASHTAG_SETS = {
    "wholesale": [
        "#LinenWholesale", "#BulkLinen", "#TextileExport", "#LinenSupplier",
        "#WholesaleTextiles", "#LinenManufacturer", "#BulkOrder", "#TextileB2B",
    ],
    "lifestyle": [
        "#LinenLove", "#HomeLinen", "#LuxuryLinen", "#NaturalFabric",
        "#HomeDecor", "#BedroomDecor", "#TableSetting", "#CozyHome",
    ],
    "export": [
        "#TextileExporter", "#MadeForExport", "#GlobalTextiles", "#LinenExport",
        "#ExportQuality", "#InternationalTrade", "#B2BTextile", "#TradePartner",
    ],
    "niche": [
        "#HotelLinen", "#HospitalityTextiles", "#RestaurantLinen",
        "#BnBSupplies", "#AirbnbHost", "#HotelSupplies", "#CommercialLinen",
    ],
}


def generate_caption(theme: str, product: str, target_audience: str = "wholesale buyers") -> dict:
    """Generate an Instagram caption with CTA using Claude."""

    prompt = f"""You are a social media expert for a Linen House export company.

Generate an Instagram caption for:
- Theme: {theme}
- Product: {product}
- Target audience: {target_audience}
- Business goal: Generate B2B wholesale inquiries and direct sales

Requirements:
- 3-5 sentences max
- Include a clear CTA (DM us, Link in bio, WhatsApp us)
- Professional yet warm tone
- Mention quality, bulk availability, or export capability
- End with 1-2 relevant emojis only

Also provide:
1. A short story/reel hook (first line to grab attention)
2. Best time to post (morning/afternoon/evening)
3. Post type recommendation (static image/carousel/reel)

Return as JSON with keys: caption, hook, best_time, post_type"""

    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=500,
        messages=[{"role": "user", "content": prompt}],
    )

    try:
        text = message.content[0].text
        start = text.find("{")
        end = text.rfind("}") + 1
        return json.loads(text[start:end])
    except (json.JSONDecodeError, IndexError):
        return {"caption": message.content[0].text, "hook": "", "best_time": "morning", "post_type": "carousel"}


def get_hashtags(mix: list[str] = None, count: int = 25) -> list[str]:
    """Build an optimized hashtag set from multiple categories."""
    if mix is None:
        mix = ["wholesale", "lifestyle", "export"]

    tags = []
    for category in mix:
        tags.extend(HASHTAG_SETS.get(category, []))

    # Deduplicate and cap at count
    unique = list(dict.fromkeys(tags))
    return unique[:count]


def generate_weekly_calendar() -> list[dict]:
    """Generate a 7-day content calendar."""
    calendar = []
    today = datetime.now()

    plan = [
        ("product_showcase", "bed sheets", ["wholesale", "lifestyle"]),
        ("behind_the_scenes", "duvet covers", ["export", "wholesale"]),
        ("bulk_deal_offer", "hotel-grade linen", ["niche", "wholesale"]),
        ("quality_highlight", "bath towels", ["lifestyle", "export"]),
        ("client_testimonial", "table linen", ["wholesale", "niche"]),
        ("export_process", "curtain fabric", ["export", "wholesale"]),
        ("lifestyle_styling", "cushion covers", ["lifestyle", "niche"]),
    ]

    for i, (theme, product, hashtag_mix) in enumerate(plan):
        date = today + timedelta(days=i)
        content = generate_caption(theme, product)

        calendar.append({
            "date": date.strftime("%Y-%m-%d"),
            "day": date.strftime("%A"),
            "theme": theme,
            "product": product,
            "caption": content.get("caption", ""),
            "hook": content.get("hook", ""),
            "best_time": content.get("best_time", "morning"),
            "post_type": content.get("post_type", "carousel"),
            "hashtags": " ".join(get_hashtags(hashtag_mix, 25)),
        })

    return calendar


def generate_dm_outreach(buyer_type: str = "hotel") -> str:
    """Generate a B2B outreach DM template."""
    prompt = f"""Write a short Instagram DM outreach message for a Linen House export company
targeting {buyer_type} buyers.

Requirements:
- Under 100 words
- Friendly and professional
- Mention: bulk pricing, export-ready, quality guarantee
- Ask a qualifying question at the end
- Do NOT be pushy or salesy

Return just the message text, no extra explanation."""

    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=200,
        messages=[{"role": "user", "content": prompt}],
    )
    return message.content[0].text


def print_calendar(calendar: list[dict]) -> None:
    print("\n" + "=" * 60)
    print("   LINEN HOUSE - 7-DAY INSTAGRAM CONTENT CALENDAR")
    print("=" * 60)

    for day in calendar:
        print(f"\n📅 {day['day']} ({day['date']})")
        print(f"   Type  : {day['post_type'].upper()} | Best time: {day['best_time']}")
        print(f"   Theme : {day['theme'].replace('_', ' ').title()}")
        print(f"   Hook  : {day['hook']}")
        print(f"   Caption:\n   {day['caption']}")
        print(f"   Tags  : {day['hashtags'][:80]}...")
        print("-" * 60)


if __name__ == "__main__":
    print("Generating your 7-day Instagram content calendar...")
    print("(This calls Claude API - ensure ANTHROPIC_API_KEY is set)\n")

    calendar = generate_weekly_calendar()
    print_calendar(calendar)

    with open("content_calendar.json", "w") as f:
        json.dump(calendar, f, indent=2)
    print("\n✓ Calendar saved to content_calendar.json")

    print("\n" + "=" * 60)
    print("   SAMPLE B2B OUTREACH DMs")
    print("=" * 60)

    for buyer_type in ["hotel", "Airbnb host", "restaurant"]:
        print(f"\nFor {buyer_type.upper()} buyers:")
        print(generate_dm_outreach(buyer_type))
        print("-" * 40)
