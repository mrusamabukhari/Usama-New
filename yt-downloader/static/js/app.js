/* ── YTDown — Frontend Logic ──────────────────────────────────── */

const urlInput    = document.getElementById("urlInput");
const clearBtn    = document.getElementById("clearBtn");
const fetchBtn    = document.getElementById("fetchBtn");
const urlError    = document.getElementById("urlError");
const previewCard = document.getElementById("previewCard");
const thumbImg    = document.getElementById("thumbImg");
const videoTitle  = document.getElementById("videoTitle");
const videoUploader = document.getElementById("videoUploader");
const videoDuration = document.getElementById("videoDuration");
const videoViews    = document.getElementById("videoViews");
const qualitySelect = document.getElementById("qualitySelect");
const qualityGroup  = document.getElementById("qualityGroup");
const downloadBtn   = document.getElementById("downloadBtn");
const downloadsList = document.getElementById("downloadsList");
const downloadsSection = document.getElementById("downloadsSection");

let selectedFormat = "mp4";
let pollingTimers  = {};   // jobId → setInterval id

// ── Helpers ───────────────────────────────────────────────────── //

function showError(msg) {
  urlError.textContent = msg;
  urlError.classList.remove("hidden");
}
function hideError() {
  urlError.classList.add("hidden");
}

function setFetchLoading(on) {
  fetchBtn.querySelector(".btn-label").classList.toggle("hidden", on);
  fetchBtn.querySelector(".btn-loader").classList.toggle("hidden", !on);
  fetchBtn.disabled = on;
}

function isValidURL(s) {
  try { new URL(s); return true; } catch { return false; }
}

// ── Clear Button ──────────────────────────────────────────────── //
clearBtn.addEventListener("click", () => {
  urlInput.value = "";
  hideError();
  previewCard.classList.add("hidden");
  urlInput.focus();
});

// ── Format Toggle ─────────────────────────────────────────────── //
document.getElementById("fmtToggle").addEventListener("click", e => {
  const btn = e.target.closest(".toggle-btn");
  if (!btn) return;
  document.querySelectorAll(".toggle-btn").forEach(b => b.classList.remove("active"));
  btn.classList.add("active");
  selectedFormat = btn.dataset.val;
  qualityGroup.style.display = selectedFormat === "mp3" ? "none" : "";
});

// ── Fetch Video Info ──────────────────────────────────────────── //
fetchBtn.addEventListener("click", fetchInfo);
urlInput.addEventListener("keydown", e => { if (e.key === "Enter") fetchInfo(); });

async function fetchInfo() {
  const url = urlInput.value.trim();
  if (!url) { showError("Please paste a YouTube URL first."); return; }
  if (!isValidURL(url)) { showError("That doesn't look like a valid URL."); return; }
  hideError();
  setFetchLoading(true);
  previewCard.classList.add("hidden");

  try {
    const res  = await fetch("/api/info", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url }),
    });
    const data = await res.json();

    if (data.error) { showError(data.error); return; }

    thumbImg.src           = data.thumbnail || "";
    videoTitle.textContent = data.title || "Unknown Title";
    videoUploader.textContent = "👤 " + (data.uploader || "—");
    videoDuration.textContent = "⏱ " + (data.duration || "—");
    videoViews.textContent    = "👁 " + (data.view_count || "—") + " views";

    // Populate quality dropdown
    qualitySelect.innerHTML = '<option value="best">Best</option>';
    (data.formats || []).forEach(f => {
      const opt = document.createElement("option");
      opt.value = f.label.replace("p","") + "p";
      opt.textContent = f.label;
      qualitySelect.appendChild(opt);
    });
    if (!qualitySelect.options.length) {
      ["1080p","720p","480p","360p"].forEach(q => {
        const opt = document.createElement("option");
        opt.value = q; opt.textContent = q;
        qualitySelect.appendChild(opt);
      });
    }

    previewCard.classList.remove("hidden");
  } catch (err) {
    showError("Network error. Is the server running?");
  } finally {
    setFetchLoading(false);
  }
}

// ── Trigger Download ──────────────────────────────────────────── //
downloadBtn.addEventListener("click", async () => {
  const url     = urlInput.value.trim();
  const quality = qualitySelect.value || "best";
  if (!url) return;

  downloadBtn.disabled = true;
  setTimeout(() => { downloadBtn.disabled = false; }, 2000);

  try {
    const res  = await fetch("/api/download", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url, format: selectedFormat, quality }),
    });
    const data = await res.json();
    if (data.error) { showError(data.error); return; }

    createJobCard(data.job_id, {
      title:     videoTitle.textContent,
      thumbnail: thumbImg.src,
      format:    selectedFormat,
      quality:   selectedFormat === "mp3" ? "MP3" : quality,
    });
    startPolling(data.job_id);
    downloadsSection.style.display = "";
  } catch (err) {
    showError("Failed to start download.");
  }
});

// ── Job Card Creation ─────────────────────────────────────────── //
function createJobCard(jobId, meta) {
  downloadsSection.style.display = "";

  const item = document.createElement("div");
  item.className = "dl-item";
  item.id = "job-" + jobId;

  item.innerHTML = `
    <div class="dl-header">
      <img class="dl-thumb" src="${escHtml(meta.thumbnail)}" alt="" onerror="this.style.display='none'"/>
      <div class="dl-meta">
        <div class="dl-title">${escHtml(meta.title)}</div>
        <div class="dl-sub">${escHtml(meta.format.toUpperCase())} · ${escHtml(meta.quality)}</div>
      </div>
      <span class="dl-status-badge badge-queued" id="badge-${jobId}">Queued</span>
    </div>
    <div class="dl-progress-wrap">
      <div class="dl-progress-bar" id="bar-${jobId}" style="width:0%"></div>
    </div>
    <div class="dl-footer">
      <div class="dl-stats">
        <span id="speed-${jobId}">Speed: —</span>
        <span id="eta-${jobId}">ETA: —</span>
        <span id="pct-${jobId}">0%</span>
      </div>
      <div id="action-${jobId}"></div>
    </div>
    <div class="dl-error-text hidden" id="err-${jobId}"></div>
  `;

  downloadsList.prepend(item);
}

// ── Polling ───────────────────────────────────────────────────── //
function startPolling(jobId) {
  pollingTimers[jobId] = setInterval(() => pollStatus(jobId), 800);
}

async function pollStatus(jobId) {
  try {
    const res  = await fetch(`/api/status/${jobId}`);
    const data = await res.json();
    updateJobCard(jobId, data);
    if (data.status === "done" || data.status === "error") {
      clearInterval(pollingTimers[jobId]);
      delete pollingTimers[jobId];
    }
  } catch {}
}

function updateJobCard(jobId, data) {
  const item   = document.getElementById("job-" + jobId);
  const badge  = document.getElementById("badge-" + jobId);
  const bar    = document.getElementById("bar-" + jobId);
  const pct    = document.getElementById("pct-" + jobId);
  const speed  = document.getElementById("speed-" + jobId);
  const eta    = document.getElementById("eta-" + jobId);
  const action = document.getElementById("action-" + jobId);
  const errEl  = document.getElementById("err-" + jobId);
  if (!item) return;

  const p = data.progress || 0;
  bar.style.width = p + "%";
  pct.textContent = p + "%";

  const statusMap = {
    queued:      ["Queued",      "badge-queued"],
    downloading: ["Downloading", "badge-downloading"],
    processing:  ["Processing",  "badge-processing"],
    done:        ["Done ✓",      "badge-done"],
    error:       ["Error",       "badge-error"],
  };
  const [label, cls] = statusMap[data.status] || ["Unknown", "badge-queued"];
  badge.textContent = label;
  badge.className   = "dl-status-badge " + cls;

  speed.textContent = "Speed: " + (data.speed || "—");
  eta.textContent   = "ETA: "   + (data.eta   || "—");

  item.className = "dl-item " + (data.status === "done" ? "done" : data.status === "error" ? "error" : "");

  if (data.status === "done") {
    action.innerHTML = `
      <a class="btn-dl-file" href="/api/file/${jobId}">
        ⬇ Save File
      </a>
    `;
    if (data.title) {
      const titleEl = item.querySelector(".dl-title");
      if (titleEl) titleEl.textContent = data.title;
    }
  }

  if (data.status === "error" && data.error) {
    errEl.textContent = data.error;
    errEl.classList.remove("hidden");
  }
}

// ── XSS helper ───────────────────────────────────────────────── //
function escHtml(str) {
  return String(str || "")
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

// Hide downloads section if empty on load
if (!downloadsList.children.length) {
  downloadsSection.style.display = "none";
}
