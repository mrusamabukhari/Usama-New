# Instagram Autopilot — Setup Guide

## Step 1: Instagram Business Account Setup

1. Convert your Instagram account to a **Business or Creator account**
   - Instagram app → Profile → Settings → Account → Switch to Professional Account

2. Connect it to a **Facebook Page**
   - You must link your Instagram to a Facebook Page to use the Graph API

## Step 2: Get API Credentials

### A. Create a Facebook Developer App
1. Go to https://developers.facebook.com/
2. Click **My Apps → Create App**
3. Choose **Business** type
4. Add the **Instagram Graph API** product

### B. Get Your Instagram Account ID
1. In your app dashboard go to **Tools → Graph API Explorer**
2. Select your app and generate a User Token with these permissions:
   - `instagram_basic`
   - `instagram_content_publish`
   - `pages_read_engagement`
3. Run: `GET /me/accounts` → find your Facebook Page ID
4. Run: `GET /{page-id}?fields=instagram_business_account` → copy the `id`
   - This is your **INSTAGRAM_ACCOUNT_ID**

### C. Get a Long-Lived Access Token
```
GET https://graph.facebook.com/v19.0/oauth/access_token
  ?grant_type=fb_exchange_token
  &client_id={app-id}
  &client_secret={app-secret}
  &fb_exchange_token={short-lived-token}
```
This gives you a **60-day token**. Save it as **INSTAGRAM_ACCESS_TOKEN**.

### D. Get Anthropic API Key
1. Go to https://console.anthropic.com/
2. Create an API key → save as **ANTHROPIC_API_KEY**

## Step 3: Configure the Bot

```bash
cd instagram_autopilot
cp .env.example .env
# Edit .env with your credentials
nano .env
```

## Step 4: Install & Run

```bash
pip install -r requirements.txt

# Verify your account connection
python main.py account

# Get an AI post idea
python main.py idea "product launch"

# Add a post to the queue (Claude generates the caption)
python main.py add "https://yourcdn.com/image.jpg" "A photo of our new product"

# See what's queued
python main.py queue

# Post everything immediately
python main.py post-now

# OR start the autopilot (posts at scheduled times in .env)
python main.py run
```

## How Auto-Posting Works

```
Your Image URL (public HTTPS)
        ↓
  Claude generates caption + hashtags
        ↓
  Added to post_queue.json
        ↓
  Scheduler fires at POST_TIMES
        ↓
  Instagram Graph API: create container → publish
        ↓
  Post goes live on Instagram!
```

## Important Notes

- Images must be **publicly accessible HTTPS URLs** (use S3, Cloudinary, etc.)
- Max 25 API-published posts per 24 hours (Instagram limit)
- The access token expires in 60 days — refresh it monthly
- For production, host this on a VPS/server so the scheduler runs 24/7
