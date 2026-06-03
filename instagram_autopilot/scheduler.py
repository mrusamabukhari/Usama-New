import schedule
import time
import logging
from datetime import datetime
import queue_manager
from instagram_api import InstagramAPI
import config

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("autopilot.log"),
    ],
)
log = logging.getLogger(__name__)


def process_queue():
    """Check queue and post any due content."""
    due = queue_manager.get_due_posts()
    if not due:
        log.info("No posts due right now.")
        return

    api = InstagramAPI()
    for post in due:
        log.info(f"Posting item #{post['id']}: {post['image_url'][:60]}...")
        try:
            result = api.post_image(post["image_url"], post["caption"])
            queue_manager.mark_posted(post["id"], result["media_id"])
            log.info(f"  Posted successfully. Media ID: {result['media_id']}")
        except Exception as e:
            queue_manager.mark_failed(post["id"], str(e))
            log.error(f"  Failed to post: {e}")


def run_scheduler():
    """Start the autopilot scheduler loop."""
    log.info(f"Instagram Autopilot started for @{config.BRAND_NAME}")
    log.info(f"Scheduled post times: {config.POST_TIMES}")

    for t in config.POST_TIMES:
        schedule.every().day.at(t).do(process_queue)
        log.info(f"  Scheduled daily at {t}")

    log.info("Scheduler running. Press Ctrl+C to stop.")
    while True:
        schedule.run_pending()
        time.sleep(30)
