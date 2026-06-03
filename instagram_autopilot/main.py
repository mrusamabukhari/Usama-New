#!/usr/bin/env python3
"""
Instagram Autopilot — CLI entry point

Usage:
  python main.py run                          # Start the autopilot scheduler
  python main.py add <image_url> <desc>       # Add post: generate caption + queue it
  python main.py add-raw <image_url> <cap>    # Add post with your own caption
  python main.py queue                        # Show the post queue
  python main.py post-now                     # Immediately publish all pending posts
  python main.py idea [theme]                 # Ask Claude for a post idea
  python main.py account                      # Show Instagram account info
"""

import sys
import json
from datetime import datetime

import config
import queue_manager
import caption_generator
from instagram_api import InstagramAPI
from scheduler import run_scheduler


def cmd_run():
    config.validate()
    run_scheduler()


def cmd_add(image_url: str, description: str, scheduled_time: str = None):
    config.validate()
    print(f"Generating caption for: {description[:60]}...")
    result = caption_generator.generate_caption(description)
    print(f"\nGenerated caption:\n{result['full_text']}\n")
    post = queue_manager.add_post(image_url, result["full_text"], scheduled_time)
    print(f"Queued as post #{post['id']}")
    if scheduled_time:
        print(f"Scheduled for: {scheduled_time}")


def cmd_add_raw(image_url: str, caption: str, scheduled_time: str = None):
    post = queue_manager.add_post(image_url, caption, scheduled_time)
    print(f"Queued as post #{post['id']}")


def cmd_queue():
    posts = queue_manager.list_queue()
    if not posts:
        print("Queue is empty.")
        return
    print(f"\n{'#':<4} {'Status':<8} {'Scheduled':<20} {'Image URL':<50}")
    print("-" * 85)
    for p in posts:
        sched = p.get("scheduled_time") or "Next slot"
        url = p["image_url"][:47] + "..." if len(p["image_url"]) > 50 else p["image_url"]
        print(f"{p['id']:<4} {p['status']:<8} {sched:<20} {url}")
    print()


def cmd_post_now():
    config.validate()
    from scheduler import process_queue
    process_queue()


def cmd_idea(theme: str = ""):
    config.validate()
    print(f"Asking Claude for a post idea{' about ' + theme if theme else ''}...\n")
    idea = caption_generator.generate_post_idea(theme)
    print(idea)


def cmd_account():
    config.validate()
    api = InstagramAPI()
    info = api.get_account_info()
    print(f"\nInstagram Account Info:")
    print(f"  Username:   @{info.get('username', 'N/A')}")
    print(f"  Account ID: {info.get('id', 'N/A')}")
    print(f"  Followers:  {info.get('followers_count', 'N/A')}")
    print(f"  Posts:      {info.get('media_count', 'N/A')}\n")


def main():
    args = sys.argv[1:]
    if not args or args[0] == "help":
        print(__doc__)
        return

    cmd = args[0]

    if cmd == "run":
        cmd_run()

    elif cmd == "add":
        if len(args) < 3:
            print("Usage: python main.py add <image_url> <description> [scheduled_time]")
            sys.exit(1)
        cmd_add(args[1], args[2], args[3] if len(args) > 3 else None)

    elif cmd == "add-raw":
        if len(args) < 3:
            print("Usage: python main.py add-raw <image_url> <caption> [scheduled_time]")
            sys.exit(1)
        cmd_add_raw(args[1], args[2], args[3] if len(args) > 3 else None)

    elif cmd == "queue":
        cmd_queue()

    elif cmd == "post-now":
        cmd_post_now()

    elif cmd == "idea":
        cmd_idea(args[1] if len(args) > 1 else "")

    elif cmd == "account":
        cmd_account()

    else:
        print(f"Unknown command: {cmd}")
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
