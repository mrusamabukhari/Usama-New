"""
B2B Lead Tracker for Linen House Instagram
Tracks wholesale buyer leads, their status, and follow-up actions.
"""

import json
import os
from datetime import datetime, date
from dataclasses import dataclass, asdict, field
from typing import Optional
import anthropic

LEADS_FILE = "leads.json"

LEAD_STATUSES = [
    "new",          # Just saw/messaged
    "replied",      # They responded
    "qualified",    # Confirmed they buy linen in bulk
    "sample_sent",  # Sent product samples/catalog
    "negotiating",  # In price discussion
    "closed_won",   # Placed an order
    "closed_lost",  # Not interested
    "follow_up",    # Needs follow-up
]

BUYER_TYPES = [
    "hotel", "bnb_airbnb", "restaurant", "retailer",
    "interior_designer", "event_planner", "hospital", "other",
]


@dataclass
class Lead:
    instagram_handle: str
    buyer_type: str
    status: str = "new"
    contact_name: Optional[str] = None
    country: Optional[str] = None
    estimated_monthly_volume: Optional[str] = None  # e.g. "500 sets/month"
    notes: str = ""
    last_contact: str = field(default_factory=lambda: date.today().isoformat())
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    order_value: float = 0.0
    follow_up_date: Optional[str] = None


def load_leads() -> list[Lead]:
    if not os.path.exists(LEADS_FILE):
        return []
    with open(LEADS_FILE) as f:
        data = json.load(f)
    return [Lead(**d) for d in data]


def save_leads(leads: list[Lead]) -> None:
    with open(LEADS_FILE, "w") as f:
        json.dump([asdict(l) for l in leads], f, indent=2)


def add_lead(handle: str, buyer_type: str, country: str = "", notes: str = "") -> Lead:
    leads = load_leads()

    # Check for duplicate
    for lead in leads:
        if lead.instagram_handle.lower() == handle.lower():
            print(f"Lead @{handle} already exists (status: {lead.status})")
            return lead

    lead = Lead(
        instagram_handle=handle,
        buyer_type=buyer_type,
        country=country,
        notes=notes,
    )
    leads.append(lead)
    save_leads(leads)
    print(f"✓ Added lead: @{handle} ({buyer_type})")
    return lead


def update_status(handle: str, new_status: str, notes: str = "", order_value: float = 0) -> None:
    leads = load_leads()
    for lead in leads:
        if lead.instagram_handle.lower() == handle.lower():
            old_status = lead.status
            lead.status = new_status
            lead.last_contact = date.today().isoformat()
            if notes:
                lead.notes += f"\n[{date.today()}] {notes}"
            if order_value:
                lead.order_value = order_value
            save_leads(leads)
            print(f"✓ @{handle}: {old_status} → {new_status}")
            return
    print(f"Lead @{handle} not found")


def get_pipeline_summary() -> dict:
    leads = load_leads()
    summary = {status: [] for status in LEAD_STATUSES}

    for lead in leads:
        summary[lead.status].append(lead)

    total_pipeline = sum(
        l.order_value for l in leads
        if l.status in ("negotiating", "sample_sent", "qualified")
    )
    total_won = sum(l.order_value for l in leads if l.status == "closed_won")

    return {
        "by_status": summary,
        "total_leads": len(leads),
        "pipeline_value": total_pipeline,
        "revenue_won": total_won,
    }


def get_ai_follow_up(handle: str) -> str:
    """Use Claude to suggest a follow-up message for a stalled lead."""
    leads = load_leads()
    lead = next((l for l in leads if l.instagram_handle.lower() == handle.lower()), None)

    if not lead:
        return f"Lead @{handle} not found"

    client = anthropic.Anthropic()
    prompt = f"""A Linen House export company needs a follow-up Instagram DM.

Lead details:
- Instagram: @{lead.instagram_handle}
- Buyer type: {lead.buyer_type}
- Status: {lead.status}
- Country: {lead.country or 'unknown'}
- Volume interest: {lead.estimated_monthly_volume or 'unknown'}
- Notes: {lead.notes or 'none'}
- Last contact: {lead.last_contact}

Write a natural, non-pushy follow-up DM (under 80 words) that:
1. References their specific business type
2. Adds value (tip, new product, seasonal offer)
3. Re-opens the conversation with a soft question

Return just the message."""

    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=200,
        messages=[{"role": "user", "content": prompt}],
    )
    return message.content[0].text


def print_pipeline() -> None:
    summary = get_pipeline_summary()

    print("\n" + "=" * 55)
    print("   LINEN HOUSE - INSTAGRAM LEAD PIPELINE")
    print("=" * 55)
    print(f"   Total Leads : {summary['total_leads']}")
    print(f"   Pipeline $  : ${summary['pipeline_value']:,.2f}")
    print(f"   Revenue Won : ${summary['revenue_won']:,.2f}")
    print("=" * 55)

    active_statuses = ["new", "replied", "qualified", "sample_sent", "negotiating", "follow_up"]
    for status in active_statuses:
        leads = summary["by_status"][status]
        if leads:
            print(f"\n  [{status.upper()}] ({len(leads)} leads)")
            for l in leads:
                val = f"  ${l.order_value:,.0f}" if l.order_value else ""
                print(f"    @{l.instagram_handle} | {l.buyer_type} | {l.country or '?'}{val}")

    won = summary["by_status"]["closed_won"]
    if won:
        print(f"\n  [CLOSED WON] ({len(won)} orders)")
        for l in won:
            print(f"    @{l.instagram_handle} | ${l.order_value:,.0f}")


def seed_demo_data() -> None:
    """Add sample leads for demonstration."""
    demo_leads = [
        ("@grandhoteluae", "hotel", "UAE", "Interested in 200 bed sets/month"),
        ("@luxbnb_london", "bnb_airbnb", "UK", "Has 15 properties, needs quarterly restock"),
        ("@rosettarestaurant", "restaurant", "Germany", "Needs table linen for 3 restaurants"),
        ("@homedecorstudio_ny", "retailer", "USA", "Looking for wholesale pricing"),
        ("@beachresort_bali", "hotel", "Indonesia", "Wants eco-friendly linen range"),
    ]

    for handle, btype, country, notes in demo_leads:
        add_lead(handle, btype, country, notes)

    update_status("@grandhoteluae", "negotiating", "Sent catalog, they want 500 sets trial", 4500)
    update_status("@luxbnb_london", "sample_sent", "Mailed white label samples")
    update_status("@rosettarestaurant", "qualified", "Confirmed 50 sets per month need")
    update_status("@homedecorstudio_ny", "replied", "Asked about MOQ")
    update_status("@beachresort_bali", "new")


if __name__ == "__main__":
    print("Linen House - B2B Lead Tracker")
    print("Loading demo data...\n")

    seed_demo_data()
    print_pipeline()

    print("\n" + "=" * 55)
    print("   AI-GENERATED FOLLOW-UP for @luxbnb_london")
    print("=" * 55)
    print(get_ai_follow_up("@luxbnb_london"))
