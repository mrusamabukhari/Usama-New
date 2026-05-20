# YTDown — YouTube Video Downloader

A clean, full-featured YouTube downloader with a modern web UI.

## Features

- 🎬 Download YouTube videos as **MP4** in any quality (Best / 1080p / 720p / 480p / 360p)
- 🎵 Extract audio as **MP3** (192 kbps)
- 📊 Live download progress with speed & ETA
- 🖼 Video preview with thumbnail, title, uploader, duration & views
- 📥 Multiple concurrent downloads
- 💅 Modern dark glassmorphism UI

## Setup

```bash
cd yt-downloader
pip install -r requirements.txt
python app.py
```

Then open **http://localhost:5000** in your browser.

## Usage

1. Paste a YouTube URL into the input box
2. Click **Fetch** to load video info
3. Choose format (MP4 / MP3) and quality
4. Click **Download**
5. Watch live progress, then click **Save File** when done

## Requirements

- Python 3.8+
- `ffmpeg` must be installed for MP3 extraction and video merging
  - Ubuntu/Debian: `sudo apt install ffmpeg`
  - macOS: `brew install ffmpeg`
  - Windows: download from https://ffmpeg.org
