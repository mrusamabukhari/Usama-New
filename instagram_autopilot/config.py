import os
from dotenv import load_dotenv

load_dotenv()

INSTAGRAM_ACCESS_TOKEN = os.getenv("INSTAGRAM_ACCESS_TOKEN", "")
INSTAGRAM_ACCOUNT_ID = os.getenv("INSTAGRAM_ACCOUNT_ID", "")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")

BRAND_NAME = os.getenv("BRAND_NAME", "My Brand")
BRAND_NICHE = os.getenv("BRAND_NICHE", "lifestyle")
BRAND_TONE = os.getenv("BRAND_TONE", "professional")

POST_TIMES = [t.strip() for t in os.getenv("POST_TIMES", "09:00,17:00").split(",")]

INSTAGRAM_GRAPH_URL = "https://graph.facebook.com/v19.0"

QUEUE_FILE = "post_queue.json"

def validate():
    missing = []
    if not INSTAGRAM_ACCESS_TOKEN:
        missing.append("INSTAGRAM_ACCESS_TOKEN")
    if not INSTAGRAM_ACCOUNT_ID:
        missing.append("INSTAGRAM_ACCOUNT_ID")
    if not ANTHROPIC_API_KEY:
        missing.append("ANTHROPIC_API_KEY")
    if missing:
        raise EnvironmentError(
            f"Missing required env vars: {', '.join(missing)}\n"
            "Copy .env.example to .env and fill in your credentials."
        )
