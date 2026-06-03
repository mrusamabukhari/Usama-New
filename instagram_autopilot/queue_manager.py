import json
import os
from datetime import datetime
from typing import Optional
import config


def _load() -> list:
    if not os.path.exists(config.QUEUE_FILE):
        return []
    with open(config.QUEUE_FILE) as f:
        return json.load(f)


def _save(queue: list):
    with open(config.QUEUE_FILE, "w") as f:
        json.dump(queue, f, indent=2)


def add_post(image_url: str, caption: str, scheduled_time: Optional[str] = None) -> dict:
    """
    Add a post to the queue.
    scheduled_time format: "YYYY-MM-DD HH:MM" or None for immediate next slot.
    """
    queue = _load()
    post = {
        "id": len(queue) + 1,
        "image_url": image_url,
        "caption": caption,
        "scheduled_time": scheduled_time,
        "status": "pending",
        "added_at": datetime.now().isoformat(),
        "posted_at": None,
        "media_id": None,
    }
    queue.append(post)
    _save(queue)
    return post


def get_pending() -> list:
    return [p for p in _load() if p["status"] == "pending"]


def get_due_posts() -> list:
    """Return posts that are pending and due (scheduled_time <= now or no schedule)."""
    now = datetime.now()
    due = []
    for post in get_pending():
        if post["scheduled_time"] is None:
            due.append(post)
        else:
            try:
                sched = datetime.fromisoformat(post["scheduled_time"])
                if sched <= now:
                    due.append(post)
            except ValueError:
                due.append(post)
    return due


def mark_posted(post_id: int, media_id: str):
    queue = _load()
    for post in queue:
        if post["id"] == post_id:
            post["status"] = "posted"
            post["posted_at"] = datetime.now().isoformat()
            post["media_id"] = media_id
            break
    _save(queue)


def mark_failed(post_id: int, error: str):
    queue = _load()
    for post in queue:
        if post["id"] == post_id:
            post["status"] = "failed"
            post["error"] = error
            break
    _save(queue)


def list_queue() -> list:
    return _load()


def clear_posted():
    queue = [p for p in _load() if p["status"] != "posted"]
    _save(queue)
