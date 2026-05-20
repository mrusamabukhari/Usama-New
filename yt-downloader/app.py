import os
import json
import threading
import uuid
from flask import Flask, render_template, request, jsonify, send_file, abort
import yt_dlp

app = Flask(__name__)

DOWNLOAD_DIR = os.path.join(os.path.dirname(__file__), "downloads")
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# In-memory job tracker: {job_id: {status, progress, filename, error, title, thumbnail}}
jobs = {}
jobs_lock = threading.Lock()


def progress_hook(job_id):
    def hook(d):
        with jobs_lock:
            job = jobs.get(job_id)
            if not job:
                return
            if d["status"] == "downloading":
                total = d.get("total_bytes") or d.get("total_bytes_estimate")
                downloaded = d.get("downloaded_bytes", 0)
                speed = d.get("speed", 0) or 0
                eta = d.get("eta", 0) or 0
                if total:
                    pct = round(downloaded / total * 100, 1)
                else:
                    pct = 0
                job["progress"] = pct
                job["speed"] = _format_bytes(speed) + "/s" if speed else "—"
                job["eta"] = _format_time(eta) if eta else "—"
                job["status"] = "downloading"
            elif d["status"] == "finished":
                job["progress"] = 100
                job["status"] = "processing"
                job["speed"] = "—"
                job["eta"] = "—"
    return hook


def _format_bytes(b):
    for unit in ["B", "KB", "MB", "GB"]:
        if b < 1024:
            return f"{b:.1f} {unit}"
        b /= 1024
    return f"{b:.1f} TB"


def _format_time(s):
    if s < 60:
        return f"{int(s)}s"
    elif s < 3600:
        return f"{int(s//60)}m {int(s%60)}s"
    else:
        return f"{int(s//3600)}h {int((s%3600)//60)}m"


def do_download(job_id, url, fmt, quality):
    """Run yt-dlp download in a background thread."""

    # Build format selector
    if fmt == "mp3":
        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": os.path.join(DOWNLOAD_DIR, f"{job_id}_%(title)s.%(ext)s"),
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }],
            "progress_hooks": [progress_hook(job_id)],
            "quiet": True,
            "no_warnings": True,
        }
    else:
        # Video quality map
        q_map = {
            "best":   "bestvideo+bestaudio/best",
            "1080p":  "bestvideo[height<=1080]+bestaudio/best[height<=1080]",
            "720p":   "bestvideo[height<=720]+bestaudio/best[height<=720]",
            "480p":   "bestvideo[height<=480]+bestaudio/best[height<=480]",
            "360p":   "bestvideo[height<=360]+bestaudio/best[height<=360]",
        }
        fmt_str = q_map.get(quality, "bestvideo+bestaudio/best")
        ydl_opts = {
            "format": fmt_str,
            "outtmpl": os.path.join(DOWNLOAD_DIR, f"{job_id}_%(title)s.%(ext)s"),
            "merge_output_format": "mp4",
            "progress_hooks": [progress_hook(job_id)],
            "quiet": True,
            "no_warnings": True,
        }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            # Find the actual output file
            files = [
                f for f in os.listdir(DOWNLOAD_DIR)
                if f.startswith(job_id + "_")
            ]
            if files:
                filename = files[0]
                with jobs_lock:
                    jobs[job_id]["status"] = "done"
                    jobs[job_id]["filename"] = filename
                    jobs[job_id]["title"] = info.get("title", filename)
                    jobs[job_id]["thumbnail"] = info.get("thumbnail", "")
                    jobs[job_id]["duration"] = _format_time(info.get("duration", 0))
                    jobs[job_id]["progress"] = 100
            else:
                raise FileNotFoundError("Output file not found after download.")
    except Exception as e:
        with jobs_lock:
            jobs[job_id]["status"] = "error"
            jobs[job_id]["error"] = str(e)


def fetch_info(job_id, url):
    """Fetch video metadata only (no download)."""
    ydl_opts = {
        "quiet": True,
        "no_warnings": True,
        "skip_download": True,
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            formats = []
            seen = set()
            for f in info.get("formats", []):
                h = f.get("height")
                ext = f.get("ext")
                vcodec = f.get("vcodec", "none")
                if vcodec != "none" and h and h not in seen:
                    seen.add(h)
                    formats.append({
                        "height": h,
                        "ext": ext,
                        "label": f"{h}p",
                    })
            formats.sort(key=lambda x: -x["height"])
            return {
                "title": info.get("title", ""),
                "thumbnail": info.get("thumbnail", ""),
                "duration": _format_time(info.get("duration", 0)),
                "uploader": info.get("uploader", ""),
                "view_count": f"{info.get('view_count', 0):,}",
                "formats": formats,
            }
    except Exception as e:
        return {"error": str(e)}


# ── Routes ────────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/info", methods=["POST"])
def api_info():
    data = request.get_json(force=True)
    url = (data.get("url") or "").strip()
    if not url:
        return jsonify({"error": "No URL provided"}), 400
    info = fetch_info(None, url)
    return jsonify(info)


@app.route("/api/download", methods=["POST"])
def api_download():
    data = request.get_json(force=True)
    url = (data.get("url") or "").strip()
    fmt = data.get("format", "mp4")
    quality = data.get("quality", "best")
    if not url:
        return jsonify({"error": "No URL provided"}), 400

    job_id = uuid.uuid4().hex[:12]
    with jobs_lock:
        jobs[job_id] = {
            "status": "queued",
            "progress": 0,
            "filename": None,
            "error": None,
            "title": "",
            "thumbnail": "",
            "speed": "—",
            "eta": "—",
            "duration": "—",
        }

    t = threading.Thread(target=do_download, args=(job_id, url, fmt, quality), daemon=True)
    t.start()
    return jsonify({"job_id": job_id})


@app.route("/api/status/<job_id>")
def api_status(job_id):
    with jobs_lock:
        job = jobs.get(job_id)
    if not job:
        return jsonify({"error": "Job not found"}), 404
    return jsonify(job)


@app.route("/api/file/<job_id>")
def api_file(job_id):
    with jobs_lock:
        job = jobs.get(job_id)
    if not job or job["status"] != "done" or not job["filename"]:
        abort(404)
    filepath = os.path.join(DOWNLOAD_DIR, job["filename"])
    if not os.path.exists(filepath):
        abort(404)
    return send_file(filepath, as_attachment=True, download_name=job["filename"].split("_", 1)[-1])


@app.route("/api/jobs")
def api_jobs():
    with jobs_lock:
        return jsonify(list(jobs.items()))


if __name__ == "__main__":
    app.run(debug=True, port=5000, use_reloader=False)
