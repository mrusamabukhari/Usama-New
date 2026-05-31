"""
$10K/Month Revenue Calculator for Linen House Instagram
Models your path to $10K with realistic projections.
"""

from dataclasses import dataclass


@dataclass
class RevenueStream:
    name: str
    avg_deal_size: float
    deals_per_month: float
    commission_rate: float = 1.0  # 1.0 = you keep 100% (direct sales)
    active: bool = True

    @property
    def monthly_revenue(self) -> float:
        if not self.active:
            return 0
        return self.avg_deal_size * self.deals_per_month * self.commission_rate


MONTH_1_TARGETS = [
    RevenueStream("Small wholesale orders (hotels/BnBs)", 800, 3),
    RevenueStream("Digital product: Sourcing Guide PDF", 29, 20, 1.0),
    RevenueStream("Export consulting call (1hr)", 150, 5),
]

MONTH_3_TARGETS = [
    RevenueStream("Mid-size wholesale orders", 1500, 4),
    RevenueStream("Recurring BnB/hotel accounts", 600, 5),
    RevenueStream("Digital products", 29, 50, 1.0),
    RevenueStream("Affiliate (home decor tools)", 80, 15, 0.30),
    RevenueStream("Sponsored posts", 300, 3),
    RevenueStream("Export consulting", 150, 8),
]

MONTH_6_TARGETS = [
    RevenueStream("Large wholesale orders", 3000, 3),
    RevenueStream("Recurring accounts (retainer)", 800, 6),
    RevenueStream("Online store / dropship", 120, 30),
    RevenueStream("Digital products & courses", 97, 50),
    RevenueStream("Brand partnerships", 500, 4),
    RevenueStream("Export consulting retainer", 2000, 2),
]


def print_projection(label: str, streams: list[RevenueStream]) -> None:
    print(f"\n{'='*55}")
    print(f"   {label}")
    print(f"{'='*55}")

    total = 0
    for s in streams:
        rev = s.monthly_revenue
        total += rev
        bar = "█" * int(rev / 200)
        print(f"  {s.name[:35]:<35} ${rev:>7,.0f}  {bar}")

    print(f"{'─'*55}")
    print(f"  {'TOTAL':35} ${total:>7,.0f}")
    gap = 10000 - total
    if gap > 0:
        print(f"  {'Gap to $10K':35} ${gap:>7,.0f}")
    else:
        print(f"  {'EXCEEDS $10K TARGET ✓':35}")


def print_action_plan() -> None:
    plan = """
╔══════════════════════════════════════════════════════╗
║      LINEN HOUSE - INSTAGRAM $10K ACTION PLAN        ║
╚══════════════════════════════════════════════════════╝

WEEK 1 — FOUNDATION
  □ Post 3x/day: product photo, reel, story
  □ Follow 50 hotel/BnB/restaurant accounts daily
  □ Add WhatsApp link in bio with "Wholesale Inquiry"
  □ Create a free PDF: "How to Source Linen at Wholesale"
  □ Run content_generator.py to get your first week's captions

WEEK 2 — OUTREACH
  □ DM 20 qualified buyers/day (hotels, BnBs, restaurants)
  □ Use lead_tracker.py to track every conversation
  □ Post 1 carousel: "Why Our Linen is Export-Ready"
  □ Add pricing tiers to bio link (Linktree or landing page)

WEEK 3 — CONVERSION
  □ Follow up on all "replied" leads from Week 2
  □ Offer free sample + shipping to top 5 prospects
  □ Post 1 reel showing your packing/export process
  □ Sell first "Export Sourcing Guide" for $29

WEEK 4 — SCALE
  □ Close first 2-3 wholesale orders
  □ Ask for video testimonials from early buyers
  □ Pitch 3 home decor brands for sponsored posts
  □ Launch paid story ads targeting hotel managers

CONTENT FORMULA (Post Daily):
  Monday    → Product showcase (carousel)
  Tuesday   → Behind-the-scenes reel
  Wednesday → Bulk deal offer / price reveal
  Thursday  → Client win / testimonial
  Friday    → Quality comparison post
  Saturday  → Lifestyle/styling inspiration
  Sunday    → Export process / "how we work" story

HIGH-VALUE HASHTAGS TO ALWAYS USE:
  #LinenWholesale #TextileExport #HotelLinen
  #BulkLinen #LinenSupplier #WholesaleTextiles
  #HospitalityTextiles #AirbnbSupplies #B2BTextile
"""
    print(plan)


if __name__ == "__main__":
    print_action_plan()
    print_projection("MONTH 1 PROJECTION (Realistic Start)", MONTH_1_TARGETS)
    print_projection("MONTH 3 PROJECTION (Growing Momentum)", MONTH_3_TARGETS)
    print_projection("MONTH 6 PROJECTION ($10K+ Territory)", MONTH_6_TARGETS)

    print("\n\nRun these to get started:")
    print("  python content_generator.py   → Get your first week of captions")
    print("  python lead_tracker.py        → Set up your B2B pipeline")
