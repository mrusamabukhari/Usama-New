import anthropic
import config


def generate_caption(image_description: str, extra_context: str = "") -> dict:
    """
    Use Claude to generate an on-brand Instagram caption + hashtags.
    Returns {"caption": str, "hashtags": str, "full_text": str}
    """
    client = anthropic.Anthropic(api_key=config.ANTHROPIC_API_KEY)

    prompt = f"""You are a social media expert for a {config.BRAND_NICHE} brand called "{config.BRAND_NAME}".
Brand tone: {config.BRAND_TONE}

Generate an Instagram caption for this image:
Image description: {image_description}
{f"Additional context: {extra_context}" if extra_context else ""}

Requirements:
- Caption: 1-3 engaging sentences, on-brand tone, ends with a CTA
- Hashtags: 20-25 relevant hashtags mix of popular (#fitness) and niche (#morningworkoutroutine)
- Output ONLY in this exact format:
CAPTION: <your caption here>
HASHTAGS: <hashtags here>"""

    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=512,
        messages=[{"role": "user", "content": prompt}],
    )

    text = message.content[0].text
    lines = text.strip().split("\n")

    caption = ""
    hashtags = ""
    for line in lines:
        if line.startswith("CAPTION:"):
            caption = line.replace("CAPTION:", "").strip()
        elif line.startswith("HASHTAGS:"):
            hashtags = line.replace("HASHTAGS:", "").strip()

    return {
        "caption": caption,
        "hashtags": hashtags,
        "full_text": f"{caption}\n.\n.\n.\n{hashtags}",
    }


def generate_post_idea(theme: str = "") -> str:
    """Ask Claude for a post idea based on the brand niche."""
    client = anthropic.Anthropic(api_key=config.ANTHROPIC_API_KEY)

    prompt = f"""Generate one specific Instagram post idea for a {config.BRAND_NICHE} brand called "{config.BRAND_NAME}".
{f"Theme/focus: {theme}" if theme else ""}
Include: what image to use, the key message, and best time to post.
Keep it concise, 3-4 sentences."""

    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=256,
        messages=[{"role": "user", "content": prompt}],
    )
    return message.content[0].text.strip()
