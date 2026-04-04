import streamlit as st
import requests
import json
import math
import csv
import io
from datetime import datetime

st.set_page_config(
    page_title="Community Crossroads Quilt",
    page_icon="🧵",
    layout="wide",
    initial_sidebar_state="collapsed",
)

SHEET_URL = (
    "https://docs.google.com/spreadsheets/d/1f9IrhyO7JxL3uzcgXBjSRCs_HnxgzKZwZODqzPGqE9g/gviz/tq?tqx=out:csv&gid=0"
)
PATCH_VALUE = 20
TOTAL = 37500
COLS = 250
ROWS = 150
GOAL = 750000
DEADLINE = datetime(2026, 7, 9, 17, 0, 0)
ZEFFY_URL = "https://www.zeffy.com/en-US/peer-to-peer/community-crossroads"
# Google Apps Script web app URL — saves patch selections to the sheet
APPS_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbzw3EUUz6WR80iiIwILbT6lGcq0BGRWZ2vWz-TuSG1L5GJFMrpr_dHudBIm-bFpg-1u/exec"

# Vibrant Tones palette
PAL = [
    "#F94144",  # red
    "#F3722C",  # orange
    "#F8961E",  # amber
    "#F9844A",  # peach
    "#F9C74F",  # yellow
    "#90BE6D",  # light green
    "#43AA8B",  # teal green
    "#4D908E",  # teal
    "#577590",  # slate blue
    "#277DA1",  # ocean blue
]

# UI colors
PRIMARY = "#43AA8B"     # teal green (was sage #3d5c3a)
ACCENT = "#F8961E"      # amber (was gold #c4923a)
BG = "#faf8f3"          # cream (unchanged)


def _lcg_colors():
    """Deterministic color assignment matching the JS LCG."""
    seed = 99991
    colors = []
    for _ in range(TOTAL):
        seed = (seed * 16807) % 2147483647
        colors.append(PAL[int((seed / 2147483647) * len(PAL))])
    return colors


@st.cache_data(ttl=300)
def load_patch_data():
    """Load sheet CSV. Columns detected from header row."""
    try:
        r = requests.get(SHEET_URL, timeout=5)
        r.raise_for_status()
        result = _parse_csv(r.text)
        # Store raw preview for debug sidebar
        result["_raw_preview"] = r.text[:1500]
        return result
    except Exception as e:
        return {
            "amounts": [0.0] * TOTAL,
            "colors": [""] * TOTAL,
            "names": [""] * TOTAL,
            "_raw_preview": f"FETCH ERROR: {e}",
        }


def _find_nearby_unclaimed(start_idx, count, amounts, reserved):
    """BFS outward from start_idx; return up to `count` unclaimed patch indices."""
    result = []
    visited = set(reserved) | {start_idx}
    queue = [start_idx]
    head = 0
    while head < len(queue) and len(result) < count:
        cur = queue[head]; head += 1
        r, c = divmod(cur, COLS)
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue
                nr, nc = r + dr, c + dc
                if 0 <= nr < ROWS and 0 <= nc < COLS:
                    ni = nr * COLS + nc
                    if ni < TOTAL and ni not in visited:
                        visited.add(ni)
                        if amounts[ni] < PATCH_VALUE:
                            result.append(ni)
                        queue.append(ni)
    return result[:count]


def _parse_csv(csv_text):
    amounts = [0.0] * TOTAL
    colors = [""] * TOTAL
    names = [""] * TOTAL

    reader = csv.reader(io.StringIO(csv_text.strip()))
    rows = list(reader)
    if not rows:
        return {"amounts": amounts, "colors": colors, "names": names}

    # --- detect column layout from header row ---
    # Map each role to a column index; default to legacy fixed positions
    col_patch = 0
    col_amount = 1
    col_color = 2
    col_name = 3  # column D (Name)

    header = [c.strip().lower() for c in rows[0]]
    header_detected = False

    # Check if the first row looks like a header (column A is not a number)
    first_val = "".join(c for c in header[0] if c.isdigit())
    if not first_val:
        header_detected = True
        # Build a map: look for keywords in each column header
        for i, h in enumerate(header):
            if h in ("patch", "patch #", "patch#", "patch number", "patchnumber", "number", "square", "#"):
                col_patch = i
            elif h in ("amount", "donation", "donated", "amt", "$", "donation amount"):
                col_amount = i
            elif h in ("color", "colour", "hex", "color hex", "color1", "colour1"):
                col_color = i
            elif h in ("name", "donor", "donor name", "donorname"):
                col_name = i

    data_rows = rows[1:] if header_detected else rows

    for cols in data_rows:
        if not cols:
            continue
        # Patch number (1-based)
        if col_patch >= len(cols):
            continue
        raw_num = cols[col_patch].strip()
        num_str = "".join(c for c in raw_num if c.isdigit())
        if not num_str:
            continue
        idx = int(num_str) - 1  # convert to 0-based
        if idx < 0 or idx >= TOTAL:
            continue

        # Amount
        if col_amount < len(cols):
            raw_amt = cols[col_amount].strip()
            amt_str = "".join(c for c in raw_amt if c.isdigit() or c == ".")
            try:
                amounts[idx] = float(amt_str)
            except ValueError:
                pass

        # Color hex
        if col_color < len(cols):
            raw_col = cols[col_color].strip()
            if raw_col.startswith("#"):
                colors[idx] = raw_col

        # Name
        if col_name < len(cols):
            names[idx] = cols[col_name].strip()

    # Expand single-row donations whose amount covers multiple squares.
    # e.g. a $2000 entry on patch #1 should fill 100 nearby squares.
    reserved = {i for i in range(TOTAL) if amounts[i] >= PATCH_VALUE}
    for idx in sorted(reserved):  # sorted for determinism
        extra = int(amounts[idx]) // PATCH_VALUE - 1
        if extra <= 0:
            continue
        nearby = _find_nearby_unclaimed(idx, extra, amounts, reserved)
        per_sq = amounts[idx] / (extra + 1)
        amounts[idx] = per_sq  # normalize so each square shows its share
        for ni in nearby:
            amounts[ni] = per_sq
            colors[ni] = ""  # leave blank so each square gets its own random palette color
            names[ni] = names[idx]
            reserved.add(ni)

    return {"amounts": amounts, "colors": colors, "names": names}


def _days_remaining():
    diff = DEADLINE - datetime.now()
    return max(0, math.ceil(diff.total_seconds() / 86400))


def _build_grid_html(amounts, sheet_colors, default_colors):
    """Return a canvas element. Actual drawing happens in JS."""
    return '<canvas id="quilt-canvas" style="width:100%;cursor:crosshair"></canvas>'


data = load_patch_data()
amounts = data["amounts"]
sheet_colors = data["colors"]
sheet_names = data["names"]
_raw_preview = data.get("_raw_preview", "")


amounts_json = json.dumps([round(a, 2) for a in amounts])
names_json = json.dumps(sheet_names)
default_colors = _lcg_colors()
# Pre-compute resolved colors for each cell (claimed color or empty)
resolved_colors = []
for i in range(TOTAL):
    if amounts[i] >= PATCH_VALUE:
        resolved_colors.append(sheet_colors[i] if sheet_colors[i] else default_colors[i])
    else:
        resolved_colors.append("")
colors_json = json.dumps(resolved_colors)
total_raised = round(sum(amounts))
claimed_patches = sum(1 for a in amounts if a >= PATCH_VALUE)
unclaimed = TOTAL - claimed_patches
days_remaining = _days_remaining()
pct_goal = round(min(100.0, total_raised / GOAL * 100), 1)
raised_fmt = f"${total_raised:,}"
raised_sub = "Be the first patch!" if total_raised == 0 else f"{claimed_patches} patches claimed"
grid_html = _build_grid_html(amounts, sheet_colors, default_colors)

st.markdown(
    """
    <style>
    #MainMenu, footer, header, [data-testid="stHeader"], [data-testid="stDecoration"], [data-testid="stToolbar"], .stDeployButton, [data-testid="stStatusWidget"] {display: none !important; height: 0 !important; min-height: 0 !important; max-height: 0 !important; padding: 0 !important; margin: 0 !important; overflow: hidden !important;}
    .stApp, html, body, [data-testid="stAppViewContainer"], [data-testid="stAppViewBlockContainer"] {background: #faf8f3 !important; overflow: auto !important;}
    .stApp > header {display: none !important; height: 0 !important;}
    .stApp [data-testid="stHeader"] {display: none !important; height: 0 !important;}
    .block-container {padding-top: 1rem !important; padding-left: 1rem !important; padding-right: 1rem !important; max-width: 100% !important; overflow: auto !important; margin-top: -3rem !important;}
    [data-testid="stAppViewContainer"] > section > div {padding: 0 !important;}
    section[data-testid="stSidebar"] {display: none;}
    html, body {overflow: auto !important;}
    </style>
    """,
    unsafe_allow_html=True,
)

# -- CSS -----------------------------------------------------------------------
CSS = """
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
html,body{width:100%;background:#faf8f3;font-family:'DM Sans',sans-serif;color:#1a3040}
.wrap{max-width:1100px;margin:0 auto;padding:2rem 1.25rem 3rem}
.eyebrow{font-size:.68rem;letter-spacing:.28em;text-transform:uppercase;color:""" + ACCENT + """;font-weight:500;margin-bottom:.5rem}
.title{font-family:'Playfair Display',serif;font-size:clamp(1.9rem,5vw,3rem);line-height:1.1;color:#1a3040;margin-bottom:.6rem}
.title em{color:""" + PRIMARY + """;font-style:italic}
.tagline{font-size:.95rem;line-height:1.7;color:#4a5c5a;max-width:620px;margin-bottom:.5rem}
.fun-note{display:inline-block;font-size:.75rem;color:#F94144;font-style:italic;background:rgba(249,65,68,.07);padding:.3rem .75rem;border-radius:20px;border:1px dashed rgba(249,65,68,.25);margin-bottom:1.25rem}
.progress-wrap{margin:1.5rem 0 1.75rem}
.progress-header{display:flex;justify-content:space-between;align-items:baseline;margin-bottom:.5rem}
.progress-raised{font-family:'Playfair Display',serif;font-size:1.35rem;color:""" + PRIMARY + """}
.progress-goal{font-size:.78rem;color:#4a5c5a}
.progress-track{height:10px;background:rgba(67,170,139,.12);border-radius:99px;overflow:hidden}
.progress-fill{height:100%;border-radius:99px;background:linear-gradient(90deg,""" + PRIMARY + """ 0%,#90BE6D 60%,""" + ACCENT + """ 100%);transition:width .8s ease;width:0%}
.progress-sub{display:flex;gap:1.5rem;margin-top:.6rem;flex-wrap:wrap}
.prog-chip{font-size:.7rem;color:#4a5c5a;display:flex;align-items:center;gap:.35rem}
.prog-dot{width:8px;height:8px;border-radius:2px;flex-shrink:0}
.layout{display:flex;gap:2rem;align-items:flex-start;flex-wrap:wrap}
.quilt-col{flex:1;min-width:280px}
.sidebar{flex:0 0 210px;min-width:180px}
.quilt-border{border:3px solid #1a3040;border-radius:4px;padding:3px;background:#1a3040;width:100%;position:relative;overflow:hidden}
.quilt-grid{position:relative;width:100%}
#quilt-canvas{display:block}
.zoom-controls{display:flex;gap:.35rem;margin-top:.5rem;align-items:center}
.zoom-btn{background:#1a3040;color:#faf8f3;border:none;border-radius:3px;width:28px;height:28px;font-size:1rem;cursor:pointer;font-family:'DM Sans',sans-serif;display:flex;align-items:center;justify-content:center}
.zoom-btn:hover{background:#2a6c5a}
.zoom-label{font-size:.65rem;color:#4a5c5a;margin:0 .3rem}
.legend{display:flex;gap:.9rem;margin-top:.75rem;flex-wrap:wrap;align-items:center}
.legend-item{display:flex;align-items:center;gap:.35rem;font-size:.68rem;color:#4a5c5a}
.swatch{width:10px;height:10px;border-radius:1px;border:1px solid rgba(0,0,0,.12);flex-shrink:0}
.stat-card{border:1px solid rgba(67,170,139,.2);border-radius:6px;padding:1rem 1.1rem;margin-bottom:.75rem;background:rgba(250,248,243,.9)}
.stat-label{font-size:.62rem;letter-spacing:.15em;text-transform:uppercase;color:#4a5c5a;margin-bottom:.2rem}
.stat-val{font-family:'Playfair Display',serif;font-size:1.5rem;color:""" + PRIMARY + """;line-height:1.1}
.stat-sub{font-size:.65rem;color:#4a5c5a;margin-top:.2rem}
.countdown{text-align:center;padding:.85rem .75rem;background:rgba(249,65,68,.06);border:1px dashed rgba(249,65,68,.22);border-radius:6px;margin-bottom:.75rem}
.cd-num{font-family:'Playfair Display',serif;font-size:2rem;color:#F94144;line-height:1}
.cd-label{font-size:.6rem;letter-spacing:.12em;text-transform:uppercase;color:#F94144;opacity:.75;margin-top:.15rem}
.donate-btn{display:block;width:100%;text-align:center;background:""" + PRIMARY + """;color:#faf8f3;font-family:'DM Sans',sans-serif;font-weight:500;font-size:.75rem;letter-spacing:.1em;text-transform:uppercase;text-decoration:none;padding:.9rem 1rem;border-radius:4px;margin-bottom:.6rem;border:none;cursor:pointer;transition:background .2s}
.donate-btn:hover{background:#3a9b7e}
.micro{font-size:.65rem;color:#4a5c5a;line-height:1.55;font-style:italic;text-align:center}
#tip{position:fixed;background:#1a3040;color:#faf8f3;font-size:.7rem;padding:.4rem .7rem;border-radius:3px;pointer-events:none;z-index:9999;opacity:0;transition:opacity .1s;white-space:nowrap;font-family:'DM Sans',sans-serif}
.floatmsg{position:fixed;pointer-events:none;z-index:9999;font-size:1.1rem;font-weight:500;font-family:'DM Sans',sans-serif;animation:float-up .9s ease both}
@keyframes float-up{0%{transform:translateY(0) scale(1);opacity:1}100%{transform:translateY(-70px) scale(1.5);opacity:0}}

/* Modal */
.modal-overlay{position:fixed;inset:0;background:rgba(0,0,0,.55);z-index:10000;display:flex;align-items:center;justify-content:center;opacity:0;pointer-events:none;transition:opacity .2s}
.modal-overlay.active{opacity:1;pointer-events:auto}
.modal{background:#faf8f3;border-radius:10px;padding:2rem;max-width:480px;width:90%;max-height:85vh;overflow-y:auto;box-shadow:0 20px 60px rgba(0,0,0,.3);position:relative;font-family:'DM Sans',sans-serif}
.modal-close{position:absolute;top:.75rem;right:1rem;background:none;border:none;font-size:1.3rem;cursor:pointer;color:#4a5c5a;line-height:1}
.modal h2{font-family:'Playfair Display',serif;font-size:1.4rem;color:#1a3040;margin-bottom:.25rem}
.modal .patch-num{color:""" + PRIMARY + """;font-size:.85rem;margin-bottom:1rem;display:block}
.modal label{font-size:.72rem;letter-spacing:.12em;text-transform:uppercase;color:#4a5c5a;display:block;margin-bottom:.35rem;margin-top:1rem}
.modal .amount-input{width:100%;padding:.65rem .8rem;border:1px solid rgba(67,170,139,.3);border-radius:5px;font-size:1.1rem;font-family:'DM Sans',sans-serif;background:#fff;outline:none}
.modal .amount-input:focus{border-color:""" + PRIMARY + """;box-shadow:0 0 0 3px rgba(67,170,139,.15)}
.modal .sq-count{font-size:.85rem;color:""" + PRIMARY + """;font-weight:500;margin-top:.4rem}
.color-row{display:flex;gap:.5rem;margin-bottom:.5rem;align-items:center;flex-wrap:wrap}
.color-row .row-label{font-size:.7rem;color:#4a5c5a;min-width:55px}
.color-swatch{width:36px;height:36px;border-radius:5px;border:3px solid transparent;cursor:pointer;transition:border-color .15s,transform .15s;flex-shrink:0}
.color-swatch:hover{transform:scale(1.12)}
.color-swatch.selected{border-color:#1a3040;box-shadow:0 0 0 2px #faf8f3, 0 0 0 4px #1a3040}
.modal .donate-submit{display:block;width:100%;text-align:center;background:""" + PRIMARY + """;color:#faf8f3;font-family:'DM Sans',sans-serif;font-weight:600;font-size:.85rem;letter-spacing:.08em;text-transform:uppercase;text-decoration:none;padding:.9rem 1rem;border-radius:5px;margin-top:1.25rem;border:none;cursor:pointer;transition:background .2s}
.modal .donate-submit:hover{background:#3a9b7e}
.modal .donate-submit:disabled{background:#aaa;cursor:not-allowed}
#modal-next-btn{background:""" + ACCENT + """}
#modal-next-btn:hover{background:#e07f10}
#modal-autofill-btn{background:#577590;margin-top:.5rem}
#modal-autofill-btn:hover{background:#4a6578}
.pick-banner{position:fixed;top:0;left:0;right:0;background:""" + ACCENT + """;color:#fff;text-align:center;font-size:.82rem;font-weight:500;padding:.55rem 1rem;z-index:9999;font-family:'DM Sans',sans-serif;box-shadow:0 2px 8px rgba(0,0,0,.15)}

/* Design Gallery */
.design-section{max-width:1100px;margin:2.5rem auto 0;padding:0 1.25rem 3rem}
.design-section-title{font-family:'Playfair Display',serif;font-size:clamp(1.4rem,3vw,2rem);color:#1a3040;margin-bottom:.25rem}
.design-section-title em{color:""" + PRIMARY + """;font-style:italic}
.design-section-sub{font-size:.85rem;color:#4a5c5a;margin-bottom:1.5rem;line-height:1.6}
.design-tier{margin-bottom:2rem}
.design-tier-label{font-size:.62rem;letter-spacing:.2em;text-transform:uppercase;color:""" + ACCENT + """;font-weight:600;margin-bottom:.75rem;padding-bottom:.35rem;border-bottom:1px dashed rgba(248,150,30,.3)}
.design-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(140px,1fr));gap:.75rem}
.design-card{background:#fff;border:1px solid rgba(67,170,139,.15);border-radius:8px;padding:.75rem;cursor:pointer;transition:transform .15s,box-shadow .15s,border-color .15s;text-align:center}
.design-card:hover{transform:translateY(-3px);box-shadow:0 6px 20px rgba(0,0,0,.1);border-color:""" + PRIMARY + """}
.design-preview{display:flex;align-items:center;justify-content:center;margin-bottom:.5rem;min-height:60px;background:#e8e4dd;border-radius:6px;padding:8px}
.design-preview canvas{image-rendering:pixelated;border-radius:3px}
.design-name{font-family:'Playfair Display',serif;font-size:.85rem;color:#1a3040;line-height:1.2;margin-bottom:.2rem}
.design-meta{font-size:.65rem;color:#4a5c5a}
.design-price{font-family:'Playfair Display',serif;font-size:.95rem;color:""" + PRIMARY + """;font-weight:700;margin-top:.2rem}
.design-detail-overlay{position:fixed;inset:0;background:rgba(0,0,0,.55);z-index:10001;display:flex;align-items:center;justify-content:center;opacity:0;pointer-events:none;transition:opacity .2s}
.design-detail-overlay.active{opacity:1;pointer-events:auto}
.design-detail{background:#faf8f3;border-radius:10px;padding:2rem;max-width:520px;width:90%;max-height:85vh;overflow-y:auto;box-shadow:0 20px 60px rgba(0,0,0,.3);position:relative;font-family:'DM Sans',sans-serif}
.design-detail-close{position:absolute;top:.75rem;right:1rem;background:none;border:none;font-size:1.3rem;cursor:pointer;color:#4a5c5a;line-height:1}
.design-detail h2{font-family:'Playfair Display',serif;font-size:1.4rem;color:#1a3040;margin-bottom:.1rem}
.design-detail .dd-price{font-family:'Playfair Display',serif;font-size:1.2rem;color:""" + PRIMARY + """;margin-bottom:.75rem;display:block}
.design-detail .dd-meta{font-size:.75rem;color:#4a5c5a;margin-bottom:1rem}
.design-detail .dd-preview{text-align:center;margin-bottom:1rem}
.design-detail .dd-preview canvas{image-rendering:pixelated;border-radius:4px;border:1px solid rgba(0,0,0,.08)}
.design-detail .dd-info{font-size:.8rem;color:#4a5c5a;line-height:1.6;margin-bottom:1.25rem}
.design-detail .dd-cta{display:block;width:100%;text-align:center;background:""" + PRIMARY + """;color:#faf8f3;font-family:'DM Sans',sans-serif;font-weight:600;font-size:.85rem;letter-spacing:.08em;text-transform:uppercase;padding:.9rem 1rem;border-radius:5px;border:none;cursor:pointer;transition:background .2s;text-decoration:none}
.design-detail .dd-cta:hover{background:#3a9b7e}

@media(max-width:640px){
  .layout{flex-direction:column}
  .sidebar{flex:none;width:100%;display:grid;grid-template-columns:1fr 1fr;gap:.5rem}
  .sidebar .countdown,.sidebar .donate-btn,.sidebar .micro{grid-column:span 2}
  .modal{padding:1.25rem}
  .color-swatch{width:30px;height:30px}
}
"""

# -- JS — canvas-based quilt with zoom/pan ----------------------------------------
JS = r"""
(function() {
  var D      = window.__QD__;
  var A      = D.amounts;
  var NAMES  = D.names;
  var COLORS = D.colors;
  var PV     = D.patchValue;
  var ZEFFY  = D.zeffyUrl;
  var SCRIPT = D.appsScriptUrl;
  var PCT    = D.pctGoal;
  var TOTAL  = D.total;
  var GRID_COLS = D.cols;
  var GRID_ROWS = D.rows;

  var PAL = ['#F94144','#F3722C','#F8961E','#F9844A','#F9C74F','#90BE6D','#43AA8B','#4D908E','#577590','#277DA1'];
  var HINTS  = ['claim me!', 'yours?', 'fill me!', 'be bold', "c'mon!"];

  /* ---- Canvas setup ---- */
  var canvas = document.getElementById('quilt-canvas');
  var ctx = canvas.getContext('2d');
  var CELL = 6;
  var GAP = 1;
  var zoom = 1;
  var minZoom = 1;
  var maxZoom = 8;
  var panX = 0, panY = 0;
  var isDragging = false, dragStartX = 0, dragStartY = 0, panStartX = 0, panStartY = 0;
  var hoverIdx = -1;
  var pickedPatches = [];
  var pickingMode = false;
  var fullW = GRID_COLS * (CELL + GAP) + GAP;
  var fullH = GRID_ROWS * (CELL + GAP) + GAP;

  function sizeCanvas() {
    var containerW = canvas.parentElement.clientWidth;
    var scale = containerW / fullW;
    minZoom = scale;
    if (zoom < minZoom) zoom = minZoom;
    canvas.width = containerW;
    var visH = Math.min(fullH * zoom, Math.max(400, fullH * minZoom));
    canvas.height = visH;
    canvas.style.height = visH + 'px';
    clampPan();
    draw();
  }

  function clampPan() {
    var maxPanX = Math.max(0, fullW * zoom - canvas.width);
    var maxPanY = Math.max(0, fullH * zoom - canvas.height);
    panX = Math.max(0, Math.min(panX, maxPanX));
    panY = Math.max(0, Math.min(panY, maxPanY));
  }

  var EMPTY_BG = '#f0ebe0';

  function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.fillStyle = '#1a3040';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    var cellZ = CELL * zoom;
    var gapZ = GAP * zoom;
    var step = cellZ + gapZ;
    var startCol = Math.max(0, Math.floor(panX / step));
    var startRow = Math.max(0, Math.floor(panY / step));
    var endCol = Math.min(GRID_COLS, Math.ceil((panX + canvas.width) / step));
    var endRow = Math.min(GRID_ROWS, Math.ceil((panY + canvas.height) / step));

    for (var r = startRow; r < endRow; r++) {
      for (var c = startCol; c < endCol; c++) {
        var idx = r * GRID_COLS + c;
        if (idx >= TOTAL) continue;
        var x = c * step - panX + gapZ;
        var y = r * step - panY + gapZ;
        var amt = A[idx] || 0;
        var claimed = amt >= PV;
        var sessionColor = null;
        for (var p = 0; p < pickedPatches.length; p++) {
          if (pickedPatches[p].idx === idx) { sessionColor = pickedPatches[p].color; break; }
        }
        if (sessionColor) {
          ctx.fillStyle = sessionColor;
        } else if (claimed) {
          ctx.fillStyle = COLORS[idx] || '#43AA8B';
        } else {
          ctx.fillStyle = EMPTY_BG;
        }
        ctx.fillRect(x, y, cellZ, cellZ);
        if (idx === hoverIdx) {
          ctx.fillStyle = 'rgba(255,255,255,0.35)';
          ctx.fillRect(x, y, cellZ, cellZ);
          ctx.strokeStyle = '#1a3040';
          ctx.lineWidth = Math.max(1, zoom * 0.5);
          ctx.strokeRect(x, y, cellZ, cellZ);
        }
        if (pickingMode && (claimed || sessionColor)) {
          ctx.fillStyle = 'rgba(250,248,243,0.6)';
          ctx.fillRect(x, y, cellZ, cellZ);
        }
      }
    }
  }

  function hitTest(mx, my) {
    var step = (CELL * zoom) + (GAP * zoom);
    var col = Math.floor((mx + panX) / step);
    var row = Math.floor((my + panY) / step);
    if (col < 0 || col >= GRID_COLS || row < 0 || row >= GRID_ROWS) return -1;
    var idx = row * GRID_COLS + col;
    return idx < TOTAL ? idx : -1;
  }

  /* Find nearby unclaimed squares via BFS radiating from startIdx */
  function findNearbyUnclaimed(startIdx, count) {
    var result = [];
    var visited = {};
    visited[startIdx] = true;
    /* Mark already picked in this session */
    for (var j = 0; j < pickedPatches.length; j++) visited[pickedPatches[j].idx] = true;
    var queue = [startIdx];
    var head = 0;
    while (head < queue.length && result.length < count) {
      var cur = queue[head++];
      var row = Math.floor(cur / GRID_COLS);
      var col = cur % GRID_COLS;
      /* 8 neighbors */
      var dirs = [[-1,-1],[-1,0],[-1,1],[0,-1],[0,1],[1,-1],[1,0],[1,1]];
      for (var d = 0; d < dirs.length; d++) {
        var nr = row + dirs[d][0], nc = col + dirs[d][1];
        if (nr < 0 || nr >= GRID_ROWS || nc < 0 || nc >= GRID_COLS) continue;
        var ni = nr * GRID_COLS + nc;
        if (ni >= TOTAL || visited[ni]) continue;
        visited[ni] = true;
        var claimed = (A[ni] || 0) >= PV;
        if (!claimed) {
          result.push(ni);
          if (result.length >= count) break;
        }
        queue.push(ni);
      }
    }
    return result;
  }

  /* Animate progress bar */
  var fill = document.getElementById('progress-fill');
  if (fill) setTimeout(function() { fill.style.width = PCT + '%'; }, 150);

  /* Auto-resize iframe height */
  function notifyHeight() {
    var h = document.body.scrollHeight;
    window.parent.postMessage({ type: 'streamlit:setFrameHeight', height: h }, '*');
  }
  setTimeout(notifyHeight, 300);
  window.addEventListener('resize', function() { sizeCanvas(); notifyHeight(); });

  var tip = document.getElementById('tip');

  /* ---- Canvas mouse events ---- */
  canvas.addEventListener('mousemove', function(e) {
    if (isDragging) {
      panX = panStartX + (dragStartX - e.clientX);
      panY = panStartY + (dragStartY - e.clientY);
      clampPan();
      draw();
      tip.style.opacity = 0;
      return;
    }
    var rect = canvas.getBoundingClientRect();
    var mx = e.clientX - rect.left;
    var my = e.clientY - rect.top;
    var idx = hitTest(mx, my);
    hoverIdx = idx;
    draw();
    if (idx < 0) { tip.style.opacity = 0; return; }
    var amt = A[idx] || 0;
    var claimed = amt >= PV;
    var msg;
    if (!claimed && amt <= 0) {
      msg = 'Patch #' + (idx+1) + ' \u2013 ' + HINTS[idx % HINTS.length];
    } else if (claimed) {
      var name = NAMES[idx] || 'Anonymous';
      msg = 'Patch #' + (idx+1) + ' \u2013 ' + name + ' \u2013 $' + amt.toLocaleString();
    } else {
      msg = 'Patch #' + (idx+1) + ' \u2013 $' + amt.toLocaleString();
    }
    tip.textContent = msg;
    tip.style.opacity = 1;
    tip.style.left = (e.clientX + 14) + 'px';
    tip.style.top  = (e.clientY - 36) + 'px';
  });

  canvas.addEventListener('mouseleave', function() { tip.style.opacity = 0; hoverIdx = -1; draw(); });

  canvas.addEventListener('mousedown', function(e) {
    isDragging = true;
    dragStartX = e.clientX;
    dragStartY = e.clientY;
    panStartX = panX;
    panStartY = panY;
    canvas.style.cursor = 'grabbing';
    e.preventDefault();
  });

  window.addEventListener('mouseup', function(e) {
    if (!isDragging) return;
    var dx = Math.abs(e.clientX - dragStartX);
    var dy = Math.abs(e.clientY - dragStartY);
    isDragging = false;
    canvas.style.cursor = 'crosshair';
    if (dx < 4 && dy < 4) {
      var rect = canvas.getBoundingClientRect();
      handleGridClick(hitTest(e.clientX - rect.left, e.clientY - rect.top));
    }
  });

  canvas.addEventListener('wheel', function(e) {
    e.preventDefault();
    var rect = canvas.getBoundingClientRect();
    var mx = e.clientX - rect.left;
    var my = e.clientY - rect.top;
    var wx = (mx + panX) / zoom;
    var wy = (my + panY) / zoom;
    var delta = e.deltaY < 0 ? 1.15 : 0.87;
    zoom = Math.max(minZoom, Math.min(maxZoom, zoom * delta));
    panX = wx * zoom - mx;
    panY = wy * zoom - my;
    clampPan();
    draw();
    updateZoomLabel();
  }, {passive: false});

  /* Zoom controls */
  var zoomInBtn = document.getElementById('zoom-in');
  var zoomOutBtn = document.getElementById('zoom-out');
  var zoomResetBtn = document.getElementById('zoom-reset');
  var zoomLbl = document.getElementById('zoom-label');

  function updateZoomLabel() {
    if (zoomLbl) zoomLbl.textContent = Math.round(zoom / minZoom * 100) + '%';
  }

  if (zoomInBtn) zoomInBtn.addEventListener('click', function() {
    var cx = canvas.width / 2, cy = canvas.height / 2;
    var wx = (cx + panX) / zoom, wy = (cy + panY) / zoom;
    zoom = Math.min(maxZoom, zoom * 1.4);
    panX = wx * zoom - cx; panY = wy * zoom - cy;
    clampPan(); draw(); updateZoomLabel();
  });
  if (zoomOutBtn) zoomOutBtn.addEventListener('click', function() {
    var cx = canvas.width / 2, cy = canvas.height / 2;
    var wx = (cx + panX) / zoom, wy = (cy + panY) / zoom;
    zoom = Math.max(minZoom, zoom * 0.7);
    panX = wx * zoom - cx; panY = wy * zoom - cy;
    clampPan(); draw(); updateZoomLabel();
  });
  if (zoomResetBtn) zoomResetBtn.addEventListener('click', function() {
    zoom = minZoom; panX = 0; panY = 0;
    clampPan(); draw(); updateZoomLabel();
  });

  sizeCanvas();
  updateZoomLabel();

  /* ------- Modal ------- */
  var overlay = document.getElementById('modal-overlay');
  var modalPatchNum = document.getElementById('modal-patch-num');
  var nameInput = document.getElementById('modal-name');
  var amountInput = document.getElementById('modal-amount');
  var sqCountEl = document.getElementById('modal-sq-count');
  var colorArea = document.getElementById('modal-color-area');
  var donateBtn = document.getElementById('modal-donate-btn');
  var nextBtn = document.getElementById('modal-next-btn');
  var modalCloseBtn = document.getElementById('modal-close');
  var amountSection = document.getElementById('modal-amount-section');
  var pickedSummary = document.getElementById('modal-picked-summary');
  var autofillBtn = document.getElementById('modal-autofill-btn');

  /* Multi-square state */
  var totalSquares = 0;
  var donationAmount = 0;
  var currentIdx = -1;
  var currentColor = '';

  function openModal(idx) {
    currentIdx = idx;
    currentColor = '';

    if (totalSquares === 0) {
      /* First open: show amount input */
      amountSection.style.display = 'block';
      nameInput.value = '';
      amountInput.value = '20';
      pickedPatches = [];
      updateSquareCount();
    } else {
      /* Subsequent opens: picking next square */
      amountSection.style.display = 'none';
    }
    pickingMode = false;
    draw();

    var sqNum = pickedPatches.length + 1;
    if (totalSquares > 1) {
      modalPatchNum.textContent = 'Square ' + sqNum + ' of ' + totalSquares + ' \\u2014 Patch #' + (idx + 1);
    } else {
      modalPatchNum.textContent = "You're claiming patch #" + (idx + 1);
    }

    renderSingleColorPicker();
    updateButtons();
    renderPickedSummary();
    hidePickBanner();
    overlay.classList.add('active');
    setTimeout(notifyHeight, 50);
  }

  function closeModal() {
    overlay.classList.remove('active');
    currentIdx = -1;
    totalSquares = 0;
    donationAmount = 0;
    pickedPatches = [];
    pickingMode = false;
    draw();
    hidePickBanner();
  }

  modalCloseBtn.addEventListener('click', closeModal);
  overlay.addEventListener('click', function(e) {
    if (e.target === overlay) closeModal();
  });

  function updateSquareCount() {
    var val = parseInt(amountInput.value) || 0;
    var numSq = Math.floor(val / PV);
    if (numSq < 1) numSq = 0;
    sqCountEl.textContent = numSq === 0
      ? 'Enter at least $' + PV + ' to claim a square'
      : 'At $' + val + ' you get ' + numSq + ' square' + (numSq > 1 ? 's' : '') + (numSq > 1 ? ' \\u2014 pick each one on the quilt' : '');
    totalSquares = numSq;
    donationAmount = val;
    updateButtons();
  }

  amountInput.addEventListener('input', updateSquareCount);

  function renderSingleColorPicker() {
    colorArea.innerHTML = '';
    var row = document.createElement('div');
    row.className = 'color-row';
    for (var p = 0; p < PAL.length; p++) {
      var sw = document.createElement('div');
      sw.className = 'color-swatch';
      sw.style.background = PAL[p];
      sw.setAttribute('data-color', PAL[p]);
      sw.addEventListener('click', function(e) {
        currentColor = e.target.getAttribute('data-color');
        var all = colorArea.querySelectorAll('.color-swatch');
        for (var j = 0; j < all.length; j++) {
          all[j].classList.toggle('selected', all[j].getAttribute('data-color') === currentColor);
        }
      });
      row.appendChild(sw);
    }
    colorArea.appendChild(row);
    /* Pre-select */
    var preColor = PAL[(pickedPatches.length) % PAL.length];
    currentColor = preColor;
    var all = row.querySelectorAll('.color-swatch');
    for (var j = 0; j < all.length; j++) {
      all[j].classList.toggle('selected', all[j].getAttribute('data-color') === preColor);
    }
  }

  function updateButtons() {
    var numSq = totalSquares;
    var remaining = numSq - pickedPatches.length - 1; /* after saving current */
    if (numSq <= 0) {
      donateBtn.style.display = 'none';
      nextBtn.style.display = 'none';
      autofillBtn.style.display = 'none';
      donateBtn.disabled = true;
      return;
    }
    if (remaining > 0) {
      /* More squares to pick after this one */
      donateBtn.style.display = 'block';
      donateBtn.disabled = false;
      donateBtn.textContent = 'Donate & Auto-fill ' + remaining + ' nearby square' + (remaining > 1 ? 's' : '') + ' \\u2192';
      nextBtn.style.display = 'block';
      nextBtn.textContent = 'Select Next Square (' + remaining + ' more) \\u2192';
      autofillBtn.style.display = 'block';
      autofillBtn.textContent = 'Auto-fill ' + remaining + ' nearby square' + (remaining > 1 ? 's' : '') + ' with random colors';
    } else {
      /* This is the last (or only) square */
      donateBtn.style.display = 'block';
      donateBtn.textContent = 'Donate & Claim \\u2192';
      nextBtn.style.display = 'none';
      autofillBtn.style.display = 'none';
      donateBtn.disabled = false;
    }
  }

  function renderPickedSummary() {
    pickedSummary.innerHTML = '';
    if (pickedPatches.length === 0) return;
    var title = document.createElement('div');
    title.style.cssText = 'font-size:.72rem;letter-spacing:.12em;text-transform:uppercase;color:#4a5c5a;margin-bottom:.35rem;margin-top:.5rem';
    title.textContent = 'Selected so far';
    pickedSummary.appendChild(title);
    for (var i = 0; i < pickedPatches.length; i++) {
      var item = document.createElement('div');
      item.style.cssText = 'display:flex;align-items:center;gap:.5rem;font-size:.78rem;color:#1a3040;margin-bottom:.2rem';
      var dot = document.createElement('span');
      dot.style.cssText = 'width:14px;height:14px;border-radius:2px;flex-shrink:0;display:inline-block;background:' + pickedPatches[i].color;
      item.appendChild(dot);
      item.appendChild(document.createTextNode('Patch #' + (pickedPatches[i].idx + 1)));
      pickedSummary.appendChild(item);
    }
  }

  var pickBanner = null;
  function showPickBanner() {
    if (!pickBanner) {
      pickBanner = document.createElement('div');
      pickBanner.className = 'pick-banner';
      document.body.appendChild(pickBanner);
    }
    var remaining = totalSquares - pickedPatches.length;
    pickBanner.textContent = '\\u2190 Click an unclaimed patch on the quilt to place square ' + (pickedPatches.length + 1) + ' of ' + totalSquares + ' (' + remaining + ' remaining)';
    pickBanner.style.display = 'block';
  }
  function hidePickBanner() {
    if (pickBanner) pickBanner.style.display = 'none';
  }

  nextBtn.addEventListener('click', function() {
    if (currentIdx < 0 || !currentColor) {
      alert('Please pick a color first');
      return;
    }
    /* Save current pick */
    pickedPatches.push({idx: currentIdx, color: currentColor});
    currentIdx = -1;
    currentColor = '';
    pickingMode = true;
    overlay.classList.remove('active');
    draw();
    showPickBanner();
    setTimeout(notifyHeight, 50);
  });

  autofillBtn.addEventListener('click', function() {
    if (currentIdx < 0 || !currentColor) {
      alert('Please pick a color for this square first');
      return;
    }
    var donorName = (nameInput.value || '').trim();
    if (!donorName) {
      alert('Please enter your name');
      nameInput.focus();
      return;
    }
    /* Save current pick */
    pickedPatches.push({idx: currentIdx, color: currentColor});
    /* Find nearby unclaimed squares for the rest */
    var remaining = totalSquares - pickedPatches.length;
    if (remaining > 0) {
      var nearby = findNearbyUnclaimed(currentIdx, remaining);
      for (var i = 0; i < nearby.length; i++) {
        var randColor = PAL[Math.floor(Math.random() * PAL.length)];
        pickedPatches.push({idx: nearby[i], color: randColor});
      }
    }
    /* Jump straight to donate */
    currentIdx = pickedPatches[pickedPatches.length - 1].idx;
    currentColor = pickedPatches[pickedPatches.length - 1].color;
    renderPickedSummary();
    /* Trigger donate flow directly */
    var patches = [];
    var colors = [];
    for (var i = 0; i < pickedPatches.length; i++) {
      patches.push(pickedPatches[i].idx + 1);
      colors.push(encodeURIComponent(pickedPatches[i].color));
    }
    if (SCRIPT) {
      autofillBtn.disabled = true;
      autofillBtn.textContent = 'Saving...';
      var payload = [];
      for (var i = 0; i < pickedPatches.length; i++) {
        payload.push({patch: pickedPatches[i].idx + 1, color: pickedPatches[i].color, amount: donationAmount / pickedPatches.length});
      }
      fetch(SCRIPT, {
        method: 'POST',
        mode: 'no-cors',
        headers: {'Content-Type': 'text/plain'},
        body: JSON.stringify({patches: payload, totalAmount: donationAmount, name: donorName})
      }).then(function() {
        var url = ZEFFY + '?patch=' + patches.join(',') + '&squares=' + pickedPatches.length + '&colors=' + colors.join(',') + '&donate=true';
        window.open(url, '_blank');
        closeModal();
      }).catch(function() {
        var url = ZEFFY + '?patch=' + patches.join(',') + '&squares=' + pickedPatches.length + '&colors=' + colors.join(',') + '&donate=true';
        window.open(url, '_blank');
        closeModal();
      });
    } else {
      var url = ZEFFY + '?patch=' + patches.join(',') + '&squares=' + pickedPatches.length + '&colors=' + colors.join(',') + '&donate=true';
      window.open(url, '_blank');
      closeModal();
    }
  });

  donateBtn.addEventListener('click', function() {
    if (currentIdx < 0) return;
    if (!currentColor) {
      alert('Please pick a color first');
      return;
    }
    var donorName = (nameInput.value || '').trim();
    if (!donorName) {
      alert('Please enter your name');
      nameInput.focus();
      return;
    }
    /* Save final pick */
    pickedPatches.push({idx: currentIdx, color: currentColor});

    /* Auto-fill any remaining squares not manually picked */
    var stillNeeded = totalSquares - pickedPatches.length;
    if (stillNeeded > 0) {
      var nearby = findNearbyUnclaimed(currentIdx, stillNeeded);
      for (var k = 0; k < nearby.length; k++) {
        var randColor = PAL[Math.floor(Math.random() * PAL.length)];
        pickedPatches.push({idx: nearby[k], color: randColor});
      }
    }

    var patches = [];
    var colors = [];
    for (var i = 0; i < pickedPatches.length; i++) {
      patches.push(pickedPatches[i].idx + 1);
      colors.push(encodeURIComponent(pickedPatches[i].color));
    }

    /* Save patch selections to Google Sheet via Apps Script */
    if (SCRIPT) {
      donateBtn.disabled = true;
      donateBtn.textContent = 'Saving...';
      var payload = [];
      for (var i = 0; i < pickedPatches.length; i++) {
        payload.push({patch: pickedPatches[i].idx + 1, color: pickedPatches[i].color, amount: donationAmount / pickedPatches.length});
      }
      fetch(SCRIPT, {
        method: 'POST',
        mode: 'no-cors',
        headers: {'Content-Type': 'text/plain'},
        body: JSON.stringify({patches: payload, totalAmount: donationAmount, name: donorName})
      }).then(function() {
        var url = ZEFFY + '?patch=' + patches.join(',') + '&squares=' + pickedPatches.length + '&colors=' + colors.join(',') + '&donate=true';
        window.open(url, '_blank');
        closeModal();
      }).catch(function() {
        /* Still open Zeffy even if sheet write fails */
        var url = ZEFFY + '?patch=' + patches.join(',') + '&squares=' + pickedPatches.length + '&colors=' + colors.join(',') + '&donate=true';
        window.open(url, '_blank');
        closeModal();
      });
    } else {
      var url = ZEFFY + '?patch=' + patches.join(',') + '&squares=' + pickedPatches.length + '&colors=' + colors.join(',') + '&donate=true';
      window.open(url, '_blank');
      closeModal();
    }
  });

  /* ------- Grid click (called from mouseup) ------- */
  function handleGridClick(idx) {
    if (idx < 0) return;
    var claimed = (A[idx] || 0) >= PV;
    if (claimed) return;
    for (var j = 0; j < pickedPatches.length; j++) {
      if (pickedPatches[j].idx === idx) return;
    }
    if (pickingMode) {
      openModal(idx);
    } else {
      totalSquares = 0;
      donationAmount = 0;
      pickedPatches = [];
      openModal(idx);
    }
  }
})();
"""

# -- Gallery JS — design selection menu ----------------------------------------
GALLERY_JS = r"""
(function() {
  var T = null;
  var ZEFFY = window.__QD__.zeffyUrl;
  var PV = window.__QD__.patchValue;

  /* ── Design definitions ── */
  var designs = {
    mini: [
      {name:"Music Note",   px:9,  grid:[[T,T,"#577590"],[T,T,"#577590"],[T,T,"#577590"],[T,T,"#577590"],["#577590","#577590","#577590"],["#577590","#577590",T]]},
      {name:"Diamond",      px:9,  grid:[[T,T,"#277DA1",T,T],[T,"#277DA1","#277DA1","#277DA1",T],["#277DA1","#277DA1","#277DA1","#277DA1","#277DA1"]]},
      {name:"Cherry",       px:9,  grid:[[T,T,T,T,"#90BE6D"],[T,T,T,"#90BE6D",T],[T,T,"#90BE6D",T,T],["#F94144",T,T,"#F94144",T],["#F94144","#F94144",T,"#F94144","#F94144"]]},
      {name:"Lightning",    px:10, grid:[[T,T,"#F9C74F"],[T,"#F9C74F","#F9C74F"],[T,"#F9C74F",T],["#F9C74F","#F9C74F","#F9C74F"],["#F9C74F","#F9C74F",T],["#F9C74F",T,T]]},
      {name:"Moon",          px:10, grid:[[T,"#F9C74F","#F9C74F",T],["#F9C74F","#F9C74F",T,T],["#F9C74F",T,T,T],["#F9C74F",T,T,T],["#F9C74F","#F9C74F",T,T],[T,"#F9C74F","#F9C74F",T]]},
      {name:"Paw Print",    px:10, grid:[[T,"#333333",T,"#333333",T],["#333333",T,T,T,"#333333"],[T,"#333333","#333333","#333333",T],[T,"#333333","#333333","#333333",T]]},
      {name:"Tree",          px:10, grid:[[T,T,"#90BE6D",T,T],[T,"#90BE6D","#90BE6D","#90BE6D",T],["#90BE6D","#90BE6D","#90BE6D","#90BE6D","#90BE6D"],[T,T,"#F8961E",T,T]]},
      {name:"Cactus",        px:11, grid:[[T,T,"#90BE6D",T,T],[T,T,"#90BE6D",T,T],["#90BE6D",T,"#90BE6D",T,"#90BE6D"],["#90BE6D","#90BE6D","#90BE6D","#90BE6D","#90BE6D"],[T,T,"#90BE6D",T,T]]},
      {name:"Anchor",        px:12, grid:[[T,T,"#277DA1",T,T],[T,"#277DA1","#277DA1","#277DA1",T],[T,T,"#277DA1",T,T],[T,T,"#277DA1",T,T],["#277DA1",T,"#277DA1",T,"#277DA1"],[T,"#277DA1","#277DA1","#277DA1",T]]},
      {name:"Cloud",         px:12, grid:[[T,T,"#FFFFFF","#FFFFFF",T,T],[T,"#FFFFFF","#FFFFFF","#FFFFFF","#FFFFFF",T],["#FFFFFF","#FFFFFF","#FFFFFF","#FFFFFF","#FFFFFF","#FFFFFF"]]},
      {name:"Star",          px:13, grid:[[T,T,"#F9C74F",T,T],[T,"#F9C74F","#F9C74F","#F9C74F",T],["#F9C74F","#F9C74F","#F8961E","#F9C74F","#F9C74F"],[T,"#F9C74F","#F9C74F","#F9C74F",T],[T,T,"#F9C74F",T,T]]},
      {name:"Daisy",         px:14, grid:[[T,"#F9C74F",T,"#F9C74F",T],["#F9C74F",T,"#F8961E",T,"#F9C74F"],[T,"#F8961E","#F8961E","#F8961E",T],["#F9C74F",T,"#F8961E",T,"#F9C74F"],[T,"#F9C74F",T,"#F9C74F",T],[T,T,"#90BE6D",T,T]]},
      {name:"Butterfly",     px:15, grid:[["#DDA0DD",T,T,T,"#DDA0DD"],["#DDA0DD","#FF69B4",T,"#FF69B4","#DDA0DD"],["#DDA0DD","#FF69B4","#333333","#FF69B4","#DDA0DD"],["#DDA0DD",T,"#333333",T,"#DDA0DD"],[T,T,"#333333",T,T]]},
      {name:"Rainbow",       px:16, grid:[[T,"#F94144","#F94144","#F94144",T],["#F94144","#F3722C","#F3722C","#F3722C","#F94144"],["#F3722C","#F9C74F",T,"#F9C74F","#F3722C"],["#F9C74F","#90BE6D",T,"#90BE6D","#F9C74F"]]},
      {name:"Alien",         px:17, grid:[[T,"#90BE6D","#90BE6D","#90BE6D",T],["#90BE6D","#90BE6D","#90BE6D","#90BE6D","#90BE6D"],["#90BE6D","#333333","#90BE6D","#333333","#90BE6D"],[T,"#90BE6D","#90BE6D","#90BE6D",T],[T,T,"#90BE6D",T,T]]},
      {name:"Sun",           px:17, grid:[[T,"#F9C74F",T,"#F9C74F",T],["#F9C74F","#F8961E","#F8961E","#F8961E","#F9C74F"],[T,"#F8961E","#F9C74F","#F8961E",T],["#F9C74F","#F8961E","#F8961E","#F8961E","#F9C74F"],[T,"#F9C74F",T,"#F9C74F",T]]},
      {name:"Mini Heart",    px:21, grid:[[T,"#F94144",T,T,"#F94144",T],["#F94144","#F94144","#F94144","#F94144","#F94144","#F94144"],["#F94144","#F94144","#F94144","#F94144","#F94144","#F94144"],[T,"#F94144","#F94144","#F94144","#F94144",T],[T,T,"#F94144","#F94144",T,T],[T,T,T,"#F94144",T,T]]},
      {name:"Crown",         px:22, grid:[[T,"#F9C74F",T,"#F9C74F",T,"#F9C74F",T],[T,"#F9C74F","#F9C74F","#F9C74F","#F9C74F","#F9C74F",T],["#F9C74F","#F9C74F","#F8961E","#F9C74F","#F8961E","#F9C74F","#F9C74F"],["#F9C74F","#F9C74F","#F9C74F","#F9C74F","#F9C74F","#F9C74F","#F9C74F"]]},
      {name:"Peace Sign",    px:23, grid:[[T,T,"#43AA8B","#43AA8B","#43AA8B",T,T],[T,"#43AA8B",T,"#43AA8B",T,"#43AA8B",T],["#43AA8B",T,T,"#43AA8B",T,T,"#43AA8B"],["#43AA8B",T,"#43AA8B","#43AA8B","#43AA8B",T,"#43AA8B"],["#43AA8B",T,T,"#43AA8B",T,T,"#43AA8B"],[T,"#43AA8B",T,"#43AA8B",T,"#43AA8B",T],[T,T,"#43AA8B","#43AA8B","#43AA8B",T,T]]},
      {name:"Smiley",        px:32, grid:[[T,"#F9C74F","#F9C74F","#F9C74F","#F9C74F",T],["#F9C74F","#F9C74F","#F9C74F","#F9C74F","#F9C74F","#F9C74F"],["#F9C74F","#333333","#F9C74F","#F9C74F","#333333","#F9C74F"],["#F9C74F","#F9C74F","#F9C74F","#F9C74F","#F9C74F","#F9C74F"],["#F9C74F","#333333","#F9C74F","#F9C74F","#333333","#F9C74F"],[T,"#F9C74F","#333333","#333333","#F9C74F",T]]}
    ],
    premium: [
      {name:"Rose", px:51, desc:"Red rose with stem", grid:[
        [T,T,T,T,"#F94144","#F94144","#F94144",T,T,T,T,T],
        [T,T,T,"#F94144","#F94144","#8B0000","#F94144","#F94144",T,T,T,T],
        [T,T,"#F94144","#F94144","#8B0000","#F94144","#F94144","#F94144","#F94144",T,T,T],
        [T,T,"#F94144","#8B0000","#F94144","#F94144","#8B0000","#F94144","#F94144",T,T,T],
        [T,T,"#F94144","#F94144","#F94144","#8B0000","#F94144","#8B0000","#F94144",T,T,T],
        [T,T,"#F94144","#F94144","#8B0000","#F94144","#F94144","#F94144","#F94144",T,T,T],
        [T,T,T,"#F94144","#F94144","#F94144","#F94144","#F94144",T,T,T,T],
        [T,T,T,T,T,"#1A6B3C",T,T,T,T,T,T],[T,T,T,T,T,"#1A6B3C",T,T,T,T,T,T],
        [T,T,T,T,"#90BE6D","#1A6B3C",T,T,T,T,T,T],[T,T,T,T,T,"#1A6B3C","#90BE6D",T,T,T,T,T],
        [T,T,T,T,T,"#1A6B3C",T,T,T,T,T,T],[T,T,T,T,"#90BE6D","#1A6B3C",T,T,T,T,T,T],
        [T,T,T,T,T,"#1A6B3C",T,T,T,T,T,T]]},
      {name:"Ladybug", px:74, desc:"Cute ladybug", grid:[
        [T,T,T,"#333333","#333333","#333333","#333333",T,T,T],
        [T,T,"#333333","#333333","#333333","#333333","#333333","#333333",T,T],
        [T,"#333333","#F94144","#F94144","#333333","#333333","#F94144","#F94144","#333333",T],
        ["#333333","#F94144","#F94144","#333333","#F94144","#F94144","#333333","#F94144","#F94144","#333333"],
        ["#333333","#F94144","#F94144","#F94144","#F94144","#F94144","#F94144","#F94144","#F94144","#333333"],
        ["#333333","#F94144","#333333","#F94144","#F94144","#F94144","#F94144","#333333","#F94144","#333333"],
        ["#333333","#F94144","#F94144","#F94144","#F94144","#F94144","#F94144","#F94144","#F94144","#333333"],
        [T,"#333333","#F94144","#F94144","#333333","#333333","#F94144","#F94144","#333333",T],
        [T,T,"#333333","#333333","#333333","#333333","#333333","#333333",T,T],
        [T,T,"#333333",T,T,T,T,"#333333",T,T]]},
      {name:"Koi Fish", px:80, desc:"Japanese koi fish", grid:[
        [T,T,T,T,T,T,T,T,T,T,T,"#FF7F50","#FF7F50",T,T,T],
        [T,T,T,T,T,T,T,T,T,"#FF7F50","#FF7F50","#FF7F50","#FFFFFF","#FF7F50",T,T],
        [T,T,T,T,T,T,T,"#FF7F50","#FF7F50","#FFFFFF","#FFFFFF","#FF7F50","#FFFFFF","#FF7F50","#FF7F50",T],
        [T,T,T,T,T,"#FF7F50","#FF7F50","#FFFFFF","#FFFFFF","#FFFFFF","#FF7F50","#FFFFFF","#FFFFFF","#FFFFFF","#FF7F50",T],
        [T,"#FF7F50","#FF7F50","#FF7F50","#FF7F50","#FFFFFF","#FFFFFF","#FFFFFF","#FFFFFF","#FF7F50","#FFFFFF","#FFFFFF","#333333","#FFFFFF","#FF7F50",T],
        ["#FF7F50","#FF7F50","#FFFFFF","#FF7F50","#FF7F50","#FFFFFF","#FF7F50","#FFFFFF","#FFFFFF","#FFFFFF","#FFFFFF","#FFFFFF","#FFFFFF","#FFFFFF","#FF7F50",T],
        [T,"#FF7F50","#FF7F50","#FF7F50","#FF7F50","#FF7F50","#FFFFFF","#FFFFFF","#FF7F50","#FFFFFF","#FFFFFF","#FF7F50","#FFFFFF","#FF7F50",T,T],
        [T,T,T,T,T,"#FF7F50","#FF7F50","#FFFFFF","#FFFFFF","#FFFFFF","#FF7F50","#FF7F50","#FF7F50",T,T,T],
        [T,T,T,T,T,T,T,"#FF7F50","#FF7F50","#FF7F50","#FF7F50",T,T,T,T,T]]},
      {name:"Penguin", px:118, desc:"Penguin with scarf", grid:[
        [T,T,T,T,"#333333","#333333","#333333","#333333",T,T,T,T],
        [T,T,T,"#333333","#333333","#333333","#333333","#333333","#333333",T,T,T],
        [T,T,"#333333","#333333","#333333","#333333","#333333","#333333","#333333","#333333",T,T],
        [T,T,"#333333","#FFFFFF","#333333","#333333","#333333","#333333","#FFFFFF","#333333",T,T],
        [T,T,"#333333","#FFFFFF","#333333","#333333","#333333","#333333","#FFFFFF","#333333",T,T],
        [T,T,"#333333","#333333","#333333","#F8961E","#F8961E","#333333","#333333","#333333",T,T],
        [T,T,T,"#333333","#333333","#333333","#333333","#333333","#333333",T,T,T],
        [T,T,"#F94144","#F94144","#F94144","#F94144","#F94144","#F94144","#F94144","#F94144",T,T],
        [T,T,T,"#F94144","#F94144","#F94144","#F94144","#F94144","#F94144",T,T,T],
        [T,"#333333","#333333","#333333","#FFFFFF","#FFFFFF","#FFFFFF","#FFFFFF","#333333","#333333","#333333",T],
        [T,"#333333","#333333","#FFFFFF","#FFFFFF","#FFFFFF","#FFFFFF","#FFFFFF","#FFFFFF","#333333","#333333",T],
        [T,"#333333","#333333","#FFFFFF","#FFFFFF","#FFFFFF","#FFFFFF","#FFFFFF","#FFFFFF","#333333","#333333",T],
        [T,T,"#333333","#FFFFFF","#FFFFFF","#FFFFFF","#FFFFFF","#FFFFFF","#FFFFFF","#333333",T,T],
        [T,T,"#333333","#333333","#FFFFFF","#FFFFFF","#FFFFFF","#FFFFFF","#333333","#333333",T,T],
        [T,T,T,"#333333","#333333","#333333","#333333","#333333","#333333",T,T,T],
        [T,T,T,"#F8961E","#F8961E",T,T,"#F8961E","#F8961E",T,T,T]]},
      {name:"Corgi", px:143, desc:"Cute corgi face", grid:[
        [T,T,T,"#F8961E","#F8961E",T,T,T,T,T,T,"#F8961E","#F8961E",T,T,T],
        [T,T,"#F8961E","#F8961E","#F8961E","#F8961E",T,T,T,T,"#F8961E","#F8961E","#F8961E","#F8961E",T,T],
        [T,T,"#F8961E","#F9844A","#F8961E","#F8961E","#F8961E","#F8961E","#F8961E","#F8961E","#F8961E","#F8961E","#F9844A","#F8961E",T,T],
        [T,"#F8961E","#F8961E","#F8961E","#F8961E","#F8961E","#F8961E","#F8961E","#F8961E","#F8961E","#F8961E","#F8961E","#F8961E","#F8961E","#F8961E",T],
        [T,"#F8961E","#F8961E","#F8961E","#F8961E","#FFFFFF","#FFFFFF","#FFFFFF","#FFFFFF","#FFFFFF","#FFFFFF","#F8961E","#F8961E","#F8961E","#F8961E",T],
        [T,"#F8961E","#F8961E","#333333","#F8961E","#FFFFFF","#FFFFFF","#FFFFFF","#FFFFFF","#FFFFFF","#FFFFFF","#F8961E","#333333","#F8961E","#F8961E",T],
        [T,"#F8961E","#F8961E","#F8961E","#F8961E","#FFFFFF","#FFFFFF","#FFFFFF","#FFFFFF","#FFFFFF","#FFFFFF","#F8961E","#F8961E","#F8961E","#F8961E",T],
        [T,T,"#F8961E","#F8961E","#FFFFFF","#FFFFFF","#FFFFFF","#333333","#333333","#FFFFFF","#FFFFFF","#FFFFFF","#F8961E","#F8961E",T,T],
        [T,T,"#F8961E","#F8961E","#FFFFFF","#FFFFFF","#333333",T,"#333333","#FFFFFF","#FFFFFF","#FFFFFF","#F8961E","#F8961E",T,T],
        [T,T,"#F8961E","#F8961E","#FFFFFF","#FF69B4","#FFFFFF","#FFFFFF","#FFFFFF","#FF69B4","#FFFFFF","#FFFFFF","#F8961E","#F8961E",T,T],
        [T,T,T,"#F8961E","#F8961E","#FFFFFF","#FFFFFF","#FFFFFF","#FFFFFF","#FFFFFF","#FFFFFF","#F8961E","#F8961E",T,T,T],
        [T,T,T,"#F8961E","#F8961E","#F8961E","#F8961E","#F8961E","#F8961E","#F8961E","#F8961E","#F8961E","#F8961E",T,T,T],
        [T,T,T,T,"#F8961E","#F8961E",T,T,T,T,"#F8961E","#F8961E",T,T,T,T],
        [T,T,T,T,"#D2691E","#D2691E",T,T,T,T,"#D2691E","#D2691E",T,T,T,T]]},
      {name:"Dragon", px:122, desc:"Fire-breathing dragon", grid:[
        [T,T,T,T,T,T,T,T,T,T,T,T,T,T,"#1A6B3C","#1A6B3C",T,T],
        [T,T,T,T,T,T,T,T,T,T,T,T,T,"#1A6B3C","#90BE6D","#1A6B3C",T,T],
        [T,T,T,T,T,T,T,T,T,T,T,"#1A6B3C","#1A6B3C","#90BE6D","#90BE6D","#1A6B3C",T,T],
        [T,T,T,T,T,T,T,T,T,T,"#1A6B3C","#90BE6D","#90BE6D","#90BE6D","#90BE6D","#1A6B3C",T,T],
        [T,T,T,T,T,T,T,T,T,"#1A6B3C","#90BE6D","#90BE6D","#F9C74F","#90BE6D","#1A6B3C",T,T,T],
        [T,T,T,T,T,T,T,T,"#1A6B3C","#90BE6D","#90BE6D","#90BE6D","#90BE6D","#90BE6D","#1A6B3C",T,T,T],
        ["#F3722C","#F9C74F",T,T,T,T,T,"#1A6B3C","#90BE6D","#90BE6D","#90BE6D","#90BE6D","#90BE6D","#1A6B3C",T,T,T,T],
        ["#F94144","#F3722C","#F9C74F",T,T,T,"#1A6B3C","#90BE6D","#90BE6D","#B5E6A3","#B5E6A3","#90BE6D","#1A6B3C",T,T,T,T,T],
        [T,"#F94144","#F3722C","#F9C74F","#1A6B3C","#1A6B3C","#90BE6D","#90BE6D","#B5E6A3","#B5E6A3","#B5E6A3","#90BE6D","#1A6B3C",T,T,T,T,T],
        [T,T,T,"#1A6B3C","#90BE6D","#90BE6D","#90BE6D","#90BE6D","#B5E6A3","#B5E6A3","#90BE6D","#90BE6D","#1A6B3C",T,T,T,T,T],
        [T,T,T,T,"#1A6B3C","#90BE6D","#90BE6D","#90BE6D","#90BE6D","#90BE6D","#90BE6D","#90BE6D","#90BE6D","#1A6B3C",T,T,T,T],
        [T,T,T,T,T,"#1A6B3C","#90BE6D","#90BE6D","#90BE6D","#90BE6D","#90BE6D","#90BE6D","#90BE6D","#90BE6D","#1A6B3C",T,T,T],
        [T,T,T,T,T,T,"#1A6B3C","#90BE6D","#B5E6A3","#90BE6D","#90BE6D","#90BE6D","#1A6B3C","#90BE6D","#1A6B3C",T,T,T],
        [T,T,T,T,T,T,T,"#1A6B3C","#B5E6A3","#B5E6A3","#90BE6D","#1A6B3C",T,"#1A6B3C","#90BE6D","#1A6B3C",T,T],
        [T,T,T,T,T,T,T,"#1A6B3C","#90BE6D","#90BE6D","#1A6B3C",T,T,T,"#1A6B3C","#1A6B3C",T,T],
        [T,T,T,T,T,T,"#1A6B3C","#90BE6D","#1A6B3C","#1A6B3C",T,T,T,T,T,T,T,T],
        [T,T,T,T,T,"#1A6B3C","#90BE6D","#1A6B3C",T,T,T,T,T,T,T,T,T,T],
        [T,T,T,T,T,"#1A6B3C","#1A6B3C",T,T,T,T,T,T,T,T,T,T,T]]},
      {name:"Sunflower", px:132, desc:"Big sunflower bloom", grid:[
        [T,T,T,T,"#F9C74F","#F9C74F",T,T,"#F9C74F","#F9C74F",T,T,T,T],
        [T,T,T,"#F9C74F","#F9C74F","#F9C74F",T,T,"#F9C74F","#F9C74F","#F9C74F",T,T,T],
        [T,"#F9C74F","#F9C74F","#F9C74F","#F9C74F","#F8961E","#F8961E","#F8961E","#F8961E","#F9C74F","#F9C74F","#F9C74F","#F9C74F",T],
        [T,"#F9C74F","#F9C74F","#F8961E","#F8961E","#8B4513","#8B4513","#8B4513","#8B4513","#F8961E","#F8961E","#F9C74F","#F9C74F",T],
        ["#F9C74F","#F9C74F","#F8961E","#8B4513","#8B4513","#8B4513","#D2691E","#8B4513","#8B4513","#8B4513","#F8961E","#F8961E","#F9C74F","#F9C74F"],
        ["#F9C74F","#F9C74F","#F8961E","#8B4513","#8B4513","#D2691E","#D2691E","#D2691E","#8B4513","#8B4513","#F8961E","#F8961E","#F9C74F","#F9C74F"],
        [T,T,"#F8961E","#8B4513","#8B4513","#8B4513","#D2691E","#8B4513","#8B4513","#8B4513","#F8961E",T,T,T],
        [T,T,"#F8961E","#8B4513","#8B4513","#8B4513","#8B4513","#8B4513","#8B4513","#8B4513","#F8961E",T,T,T],
        ["#F9C74F","#F9C74F","#F8961E","#F8961E","#8B4513","#8B4513","#8B4513","#8B4513","#8B4513","#F8961E","#F8961E","#F9C74F","#F9C74F","#F9C74F"],
        ["#F9C74F","#F9C74F","#F9C74F","#F8961E","#F8961E","#8B4513","#8B4513","#8B4513","#F8961E","#F8961E","#F9C74F","#F9C74F","#F9C74F",T],
        [T,"#F9C74F","#F9C74F","#F9C74F","#F9C74F","#F8961E","#F8961E","#F8961E","#F8961E","#F9C74F","#F9C74F","#F9C74F","#F9C74F",T],
        [T,T,T,"#F9C74F","#F9C74F","#F9C74F","#1A6B3C","#F9C74F","#F9C74F","#F9C74F",T,T,T,T],
        [T,T,T,T,T,T,"#1A6B3C",T,T,T,T,T,T,T],[T,T,T,T,T,"#90BE6D","#1A6B3C",T,T,T,T,T,T,T],
        [T,T,T,T,T,T,"#1A6B3C","#90BE6D",T,T,T,T,T,T],[T,T,T,T,T,T,"#1A6B3C",T,T,T,T,T,T,T]]},
      {name:"Owl", px:165, desc:"Wise owl perched", grid:[
        [T,T,T,T,"#8B4513","#8B4513","#8B4513","#8B4513","#8B4513","#8B4513","#8B4513","#8B4513",T,T,T,T],
        [T,T,T,"#8B4513","#D2691E","#D2691E","#D2691E","#D2691E","#D2691E","#D2691E","#D2691E","#D2691E","#8B4513",T,T,T],
        [T,T,"#8B4513","#D2691E","#D2691E","#D2691E","#D2691E","#D2691E","#D2691E","#D2691E","#D2691E","#D2691E","#D2691E","#8B4513",T,T],
        [T,"#8B4513","#D2691E","#8B4513","#8B4513","#8B4513","#D2691E","#D2691E","#D2691E","#8B4513","#8B4513","#8B4513","#D2691E","#8B4513",T,T],
        [T,"#8B4513","#8B4513","#FFFFFF","#FFFFFF","#8B4513","#D2691E","#D2691E","#D2691E","#8B4513","#FFFFFF","#FFFFFF","#8B4513","#8B4513",T,T],
        [T,"#8B4513","#8B4513","#FFFFFF","#333333","#8B4513","#DEB887","#DEB887","#DEB887","#8B4513","#333333","#FFFFFF","#8B4513","#8B4513",T,T],
        [T,T,"#8B4513","#8B4513","#8B4513","#D2691E","#D2691E","#F8961E","#D2691E","#D2691E","#8B4513","#8B4513","#8B4513",T,T,T],
        [T,T,T,"#8B4513","#D2691E","#D2691E","#F8961E","#F8961E","#F8961E","#D2691E","#D2691E","#8B4513",T,T,T,T],
        [T,T,"#8B4513","#D2691E","#D2691E","#DEB887","#DEB887","#DEB887","#DEB887","#DEB887","#D2691E","#D2691E","#8B4513",T,T,T],
        [T,T,"#8B4513","#D2691E","#DEB887","#DEB887","#DEB887","#DEB887","#DEB887","#DEB887","#DEB887","#D2691E","#8B4513",T,T,T],
        [T,"#8B4513","#D2691E","#D2691E","#DEB887","#DEB887","#DEB887","#DEB887","#DEB887","#DEB887","#DEB887","#D2691E","#D2691E","#8B4513",T,T],
        [T,"#8B4513","#D2691E","#D2691E","#DEB887","#D2691E","#DEB887","#DEB887","#DEB887","#D2691E","#DEB887","#D2691E","#D2691E","#8B4513",T,T],
        [T,T,"#8B4513","#D2691E","#D2691E","#D2691E","#DEB887","#DEB887","#DEB887","#D2691E","#D2691E","#D2691E","#8B4513",T,T,T],
        [T,T,T,"#8B4513","#8B4513","#D2691E","#D2691E","#D2691E","#D2691E","#D2691E","#8B4513","#8B4513",T,T,T,T],
        [T,T,T,T,"#8B4513","#8B4513",T,T,T,"#8B4513","#8B4513",T,T,T,T,T],
        [T,T,T,T,"#8B4513","#8B4513",T,T,T,"#8B4513","#8B4513",T,T,T,T,T]]},
      {name:"Turtle", px:113, desc:"Sea turtle swimming", grid:[
        [T,T,T,T,T,T,T,T,"#1A6B3C","#1A6B3C",T,T],
        [T,T,T,T,T,T,T,"#1A6B3C","#90BE6D","#90BE6D","#1A6B3C",T],
        [T,T,T,T,T,T,"#1A6B3C","#90BE6D","#333333","#90BE6D","#1A6B3C",T],
        [T,"#1A6B3C","#1A6B3C",T,T,"#1A6B3C","#1A6B3C","#1A6B3C","#1A6B3C","#1A6B3C","#1A6B3C","#1A6B3C"],
        ["#1A6B3C","#90BE6D","#90BE6D","#1A6B3C","#1A6B3C","#90BE6D","#43AA8B","#43AA8B","#90BE6D","#90BE6D","#1A6B3C",T],
        [T,"#1A6B3C","#90BE6D","#1A6B3C","#90BE6D","#43AA8B","#90BE6D","#43AA8B","#43AA8B","#90BE6D","#1A6B3C",T],
        [T,T,"#1A6B3C","#1A6B3C","#90BE6D","#90BE6D","#43AA8B","#90BE6D","#90BE6D","#1A6B3C","#1A6B3C",T],
        [T,"#1A6B3C","#1A6B3C",T,"#1A6B3C","#43AA8B","#90BE6D","#90BE6D","#43AA8B","#1A6B3C",T,T],
        ["#1A6B3C","#90BE6D","#90BE6D","#1A6B3C",T,"#1A6B3C","#1A6B3C","#1A6B3C","#1A6B3C","#1A6B3C",T,T],
        [T,"#1A6B3C","#90BE6D","#1A6B3C",T,T,T,"#1A6B3C","#1A6B3C",T,T,T],
        [T,T,"#1A6B3C",T,T,T,"#1A6B3C","#90BE6D","#90BE6D","#1A6B3C",T,T]]},
      {name:"Unicorn", px:87, desc:"Magical unicorn head", grid:[
        [T,T,T,T,T,"#F9C74F",T,T,T,T],
        [T,T,T,T,"#F9C74F","#F8961E","#F9C74F",T,T,T],
        [T,T,T,"#F9C74F","#F8961E","#F9C74F",T,T,T,T],
        [T,T,T,"#FFFFFF","#FFFFFF",T,T,T,T,T],
        [T,T,"#FFFFFF","#FFFFFF","#FFFFFF","#FFFFFF",T,T,T,T],
        [T,"#FFFFFF","#CCCCCC","#FFFFFF","#FFFFFF","#FFFFFF","#FFFFFF",T,T,T],
        ["#FFFFFF","#FFFFFF","#FFFFFF","#FFFFFF","#333333","#FFFFFF","#FFFFFF","#FFFFFF",T,T],
        ["#FFFFFF","#FFFFFF","#FFFFFF","#FFFFFF","#FFFFFF","#FFFFFF","#FFFFFF","#FFFFFF","#FFFFFF",T],
        [T,"#FFFFFF","#FFFFFF","#FFFFFF","#FFFFFF","#FF69B4","#FFFFFF","#FFFFFF","#FFFFFF",T],
        [T,T,"#FFFFFF","#FFFFFF","#FFFFFF","#FFFFFF","#FFFFFF","#FFFFFF",T,T],
        [T,T,T,T,T,"#FFFFFF","#FFFFFF",T,T,T],
        [T,T,T,T,T,T,T,T,"#DDA0DD","#87CEEB"],
        [T,T,T,T,T,T,T,"#FF69B4","#87CEEB","#DDA0DD"]]}
    ],
    ultra: [
      {name:"Whale", px:135, desc:"Majestic blue whale", grid:[
        [T,T,T,T,T,T,T,T,T,"#1E5FA8","#1E5FA8","#1E5FA8","#1E5FA8","#1E5FA8",T,T,T,T,T,T],
        [T,T,T,T,T,T,T,"#1E5FA8","#1E5FA8","#277DA1","#277DA1","#277DA1","#277DA1","#277DA1","#1E5FA8","#1E5FA8",T,T,T,T],
        [T,T,T,T,T,"#1E5FA8","#1E5FA8","#277DA1","#277DA1","#277DA1","#5BA3CF","#5BA3CF","#277DA1","#277DA1","#277DA1","#277DA1","#1E5FA8",T,T,T],
        [T,T,T,"#1E5FA8","#1E5FA8","#277DA1","#277DA1","#277DA1","#277DA1","#5BA3CF","#5BA3CF","#5BA3CF","#277DA1","#277DA1","#277DA1","#277DA1","#277DA1","#1E5FA8",T,T],
        [T,"#1E5FA8","#1E5FA8","#277DA1","#277DA1","#277DA1","#277DA1","#277DA1","#5BA3CF","#5BA3CF","#277DA1","#277DA1","#277DA1","#277DA1","#277DA1","#277DA1","#277DA1","#277DA1","#1E5FA8",T],
        ["#1E5FA8","#1E5FA8","#277DA1","#277DA1","#277DA1","#277DA1","#277DA1","#277DA1","#277DA1","#277DA1","#277DA1","#277DA1","#277DA1","#277DA1","#333333","#277DA1","#277DA1","#277DA1","#1E5FA8",T],
        ["#1E5FA8","#277DA1","#277DA1","#1E5FA8","#277DA1","#277DA1","#277DA1","#5BA3CF","#5BA3CF","#5BA3CF","#5BA3CF","#277DA1","#277DA1","#277DA1","#277DA1","#277DA1","#277DA1","#1E5FA8",T,T],
        [T,"#1E5FA8","#1E5FA8",T,"#1E5FA8","#277DA1","#277DA1","#277DA1","#5BA3CF","#5BA3CF","#277DA1","#277DA1","#277DA1","#277DA1","#277DA1","#277DA1","#1E5FA8",T,T,T],
        [T,T,T,T,T,"#1E5FA8","#1E5FA8","#277DA1","#277DA1","#277DA1","#277DA1","#277DA1","#277DA1","#277DA1","#1E5FA8","#1E5FA8",T,T,T,T],
        [T,T,T,T,T,T,T,"#1E5FA8","#1E5FA8","#1E5FA8","#1E5FA8","#1E5FA8","#1E5FA8","#1E5FA8",T,T,T,T,T,T],
        [T,T,T,T,T,T,T,T,T,T,T,T,"#87CEEB","#87CEEB","#87CEEB",T,T,T,T,T],
        [T,T,T,T,T,T,T,T,T,T,T,"#87CEEB","#87CEEB","#87CEEB",T,T,T,T,T,T]]},
      {name:"Octopus", px:204, desc:"Kawaii octopus", grid:[
        [T,T,T,T,T,T,T,"#FF7F50","#FF7F50","#FF7F50","#FF7F50","#FF7F50","#FF7F50",T,T,T,T,T,T,T],
        [T,T,T,T,T,"#FF7F50","#FF7F50","#FF7F50","#FF7F50","#FF7F50","#FF7F50","#FF7F50","#FF7F50","#FF7F50","#FF7F50",T,T,T,T,T],
        [T,T,T,T,"#FF7F50","#FF7F50","#FF7F50","#FF7F50","#FF7F50","#FF7F50","#FF7F50","#FF7F50","#FF7F50","#FF7F50","#FF7F50","#FF7F50",T,T,T,T],
        [T,T,T,"#FF7F50","#FF7F50","#FF7F50","#FF7F50","#FF7F50","#FF7F50","#FF7F50","#FF7F50","#FF7F50","#FF7F50","#FF7F50","#FF7F50","#FF7F50","#FF7F50",T,T,T],
        [T,T,T,"#FF7F50","#FF7F50","#FF7F50","#FF7F50","#FF7F50","#FF7F50","#FF7F50","#FF7F50","#FF7F50","#FF7F50","#FF7F50","#FF7F50","#FF7F50","#FF7F50",T,T,T],
        [T,T,T,"#FF7F50","#FF7F50","#FFFFFF","#FFFFFF","#FF7F50","#FF7F50","#FF7F50","#FF7F50","#FF7F50","#FFFFFF","#FFFFFF","#FF7F50","#FF7F50","#FF7F50",T,T,T],
        [T,T,T,"#FF7F50","#FF7F50","#FFFFFF","#333333","#FF7F50","#FF7F50","#FF7F50","#FF7F50","#FF7F50","#FFFFFF","#333333","#FF7F50","#FF7F50","#FF7F50",T,T,T],
        [T,T,T,"#FF7F50","#FF7F50","#FF7F50","#FF7F50","#FF7F50","#FF7F50","#FF7F50","#FF7F50","#FF7F50","#FF7F50","#FF7F50","#FF7F50","#FF7F50","#FF7F50",T,T,T],
        [T,T,T,"#FF7F50","#FF7F50","#FF7F50","#FF7F50","#FF7F50","#FF69B4","#FF69B4","#FF69B4","#FF7F50","#FF7F50","#FF7F50","#FF7F50","#FF7F50","#FF7F50",T,T,T],
        [T,T,T,"#FF7F50","#FF7F50","#FF69B4","#FF7F50","#FF7F50","#FF7F50","#FF7F50","#FF7F50","#FF7F50","#FF7F50","#FF69B4","#FF7F50","#FF7F50","#FF7F50",T,T,T],
        [T,T,T,T,"#FF7F50","#FF7F50","#FF7F50","#FF7F50","#FF7F50","#FF7F50","#FF7F50","#FF7F50","#FF7F50","#FF7F50","#FF7F50","#FF7F50",T,T,T,T],
        [T,T,"#FF7F50","#FF7F50","#FF7F50","#FF7F50","#FF7F50","#FF7F50","#FF7F50","#FF7F50","#FF7F50","#FF7F50","#FF7F50","#FF7F50","#FF7F50","#FF7F50","#FF7F50","#FF7F50",T,T],
        [T,"#FF7F50","#FF7F50",T,"#FF7F50","#FF7F50",T,"#FF7F50","#FF7F50",T,T,"#FF7F50","#FF7F50",T,"#FF7F50","#FF7F50",T,"#FF7F50","#FF7F50",T],
        ["#FF7F50","#FF7F50",T,T,"#FF7F50","#FF7F50",T,"#FF7F50","#FF7F50",T,T,"#FF7F50","#FF7F50",T,"#FF7F50","#FF7F50",T,T,"#FF7F50","#FF7F50"],
        ["#FF7F50",T,T,"#FF7F50","#FF7F50",T,T,T,"#FF7F50","#FF7F50","#FF7F50","#FF7F50",T,T,T,"#FF7F50","#FF7F50",T,T,"#FF7F50"],
        ["#FF7F50",T,"#FF7F50","#FF7F50",T,T,T,T,T,"#FF7F50","#FF7F50",T,T,T,T,T,"#FF7F50","#FF7F50",T,"#FF7F50"],
        ["#FF7F50","#FF7F50","#FF7F50",T,T,T,T,T,T,T,T,T,T,T,T,T,T,"#FF7F50","#FF7F50","#FF7F50"],
        [T,"#FF7F50",T,T,T,T,T,T,T,T,T,T,T,T,T,T,T,T,"#FF7F50",T]]},
      {name:"Panda", px:200, desc:"Cute giant panda", grid:[
        [T,T,T,"#333333","#333333",T,T,T,T,T,T,T,T,"#333333","#333333",T,T,T],
        [T,T,"#333333","#333333","#333333","#333333",T,T,T,T,T,T,"#333333","#333333","#333333","#333333",T,T],
        [T,T,T,"#333333","#333333","#FFFFFF","#FFFFFF","#FFFFFF","#FFFFFF","#FFFFFF","#FFFFFF","#FFFFFF","#FFFFFF","#333333","#333333",T,T,T],
        [T,T,"#FFFFFF","#FFFFFF","#FFFFFF","#FFFFFF","#FFFFFF","#FFFFFF","#FFFFFF","#FFFFFF","#FFFFFF","#FFFFFF","#FFFFFF","#FFFFFF","#FFFFFF","#FFFFFF",T,T],
        [T,"#FFFFFF","#FFFFFF","#FFFFFF","#333333","#333333","#333333","#FFFFFF","#FFFFFF","#FFFFFF","#FFFFFF","#333333","#333333","#333333","#FFFFFF","#FFFFFF","#FFFFFF",T],
        [T,"#FFFFFF","#FFFFFF","#333333","#333333","#FFFFFF","#333333","#333333","#FFFFFF","#FFFFFF","#333333","#333333","#FFFFFF","#333333","#333333","#FFFFFF","#FFFFFF",T],
        [T,"#FFFFFF","#FFFFFF","#FFFFFF","#FFFFFF","#FFFFFF","#FFFFFF","#FFFFFF","#FFFFFF","#FFFFFF","#FFFFFF","#FFFFFF","#FFFFFF","#FFFFFF","#FFFFFF","#FFFFFF","#FFFFFF",T],
        [T,"#FFFFFF","#FFFFFF","#FFFFFF","#FFFFFF","#FFFFFF","#FFFFFF","#333333","#333333","#333333","#FFFFFF","#FFFFFF","#FFFFFF","#FFFFFF","#FFFFFF","#FFFFFF","#FFFFFF",T],
        [T,T,"#FFFFFF","#FFFFFF","#FFFFFF","#FFFFFF","#FFFFFF","#FFFFFF","#333333","#FFFFFF","#FFFFFF","#FFFFFF","#FFFFFF","#FFFFFF","#FFFFFF",T,T,T],
        [T,T,T,"#FFFFFF","#FFFFFF","#FFFFFF","#FFFFFF","#FFFFFF","#FFFFFF","#FFFFFF","#FFFFFF","#FFFFFF","#FFFFFF","#FFFFFF",T,T,T,T],
        [T,T,T,T,"#333333","#333333","#FFFFFF","#FFFFFF","#FFFFFF","#FFFFFF","#FFFFFF","#333333","#333333",T,T,T,T,T],
        [T,T,T,"#333333","#333333","#333333","#333333","#FFFFFF","#FFFFFF","#FFFFFF","#333333","#333333","#333333","#333333",T,T,T,T],
        [T,T,T,"#333333","#333333","#333333",T,T,T,T,T,"#333333","#333333","#333333",T,T,T,T]]},
      {name:"Phoenix", px:194, desc:"Rising phoenix in flames", grid:[
        [T,T,T,T,T,T,T,T,T,"#F94144","#F94144",T,T,T,T,T,T,T],
        [T,T,T,T,T,T,T,T,"#F94144","#F3722C","#F3722C","#F94144",T,T,T,T,T,T],
        [T,T,T,T,T,T,T,"#F94144","#F3722C","#F9C74F","#F3722C","#F94144",T,T,T,T,T,T],
        [T,T,T,T,T,T,"#F94144","#F3722C","#F9C74F","#F9C74F","#F3722C","#F94144",T,T,T,T,T,T],
        [T,T,T,T,T,T,"#F94144","#F3722C","#F3722C","#333333","#F3722C","#F94144",T,T,T,T,T,T],
        [T,T,T,T,T,"#F94144","#F3722C","#F3722C","#F3722C","#F3722C","#F3722C","#F3722C","#F94144",T,T,T,T,T],
        [T,T,"#F94144","#F94144","#F3722C","#F3722C","#F94144","#F3722C","#F8961E","#F3722C","#F94144","#F3722C","#F3722C","#F94144","#F94144",T,T,T],
        [T,"#F94144","#F3722C","#F3722C","#F3722C","#F94144",T,"#F94144","#F3722C","#F3722C","#F94144",T,"#F94144","#F3722C","#F3722C","#F94144",T,T],
        ["#F94144","#F3722C","#F94144","#F94144",T,T,T,"#F94144","#F3722C","#F3722C","#F94144",T,T,"#F94144","#F94144","#F3722C","#F94144",T],
        ["#F94144","#F94144",T,T,T,T,T,T,"#F94144","#F3722C","#F94144",T,T,T,T,"#F94144","#F94144",T],
        [T,T,T,T,T,T,T,"#F94144","#F3722C","#F9C74F","#F3722C","#F94144",T,T,T,T,T,T],
        [T,T,T,T,T,T,"#F94144","#F3722C","#F9C74F","#F9C74F","#F9C74F","#F3722C","#F94144",T,T,T,T,T],
        [T,T,T,T,T,"#F94144","#F3722C","#F9C74F","#F8961E","#F8961E","#F8961E","#F9C74F","#F3722C","#F94144",T,T,T,T],
        [T,T,T,T,"#F94144","#F3722C","#F9C74F","#F8961E","#F94144","#F94144","#F94144","#F8961E","#F9C74F","#F3722C","#F94144",T,T,T],
        [T,T,T,"#F94144","#F3722C","#F9C74F","#F8961E","#F94144",T,T,T,"#F94144","#F8961E","#F9C74F","#F3722C","#F94144",T,T]]},
      {name:"Sailboat", px:213, desc:"Sailboat at sunset", grid:[
        [T,T,T,T,T,T,T,T,T,"#F8961E",T,T,T,T,T,T,T,T],
        [T,T,T,T,T,T,T,T,T,"#8B4513",T,T,T,T,T,T,T,T],
        [T,T,T,T,T,T,T,T,T,"#8B4513","#FFFFFF",T,T,T,T,T,T,T],
        [T,T,T,T,T,T,T,T,T,"#8B4513","#FFFFFF","#FFFFFF",T,T,T,T,T,T],
        [T,T,T,T,T,T,T,T,T,"#8B4513","#FFFFFF","#FFFFFF","#FFFFFF",T,T,T,T,T],
        [T,T,T,T,T,T,"#FFFFFF",T,T,"#8B4513","#FFFFFF","#FFFFFF","#FFFFFF","#FFFFFF",T,T,T,T],
        [T,T,T,T,T,"#FFFFFF","#FFFFFF",T,T,"#8B4513","#FFFFFF","#FFFFFF","#FFFFFF","#FFFFFF","#FFFFFF",T,T,T],
        [T,T,T,"#FFFFFF","#FFFFFF","#FFFFFF","#FFFFFF",T,T,"#8B4513",T,T,T,T,T,T,T,T],
        [T,"#8B4513","#8B4513","#8B4513","#8B4513","#8B4513","#8B4513","#8B4513","#8B4513","#8B4513","#8B4513","#8B4513","#8B4513","#8B4513","#8B4513","#8B4513","#8B4513",T],
        [T,T,"#D2691E","#D2691E","#D2691E","#D2691E","#D2691E","#D2691E","#D2691E","#D2691E","#D2691E","#D2691E","#D2691E","#D2691E","#D2691E","#D2691E",T,T],
        [T,T,T,"#8B4513","#8B4513","#8B4513","#8B4513","#8B4513","#8B4513","#8B4513","#8B4513","#8B4513","#8B4513","#8B4513","#8B4513",T,T,T],
        ["#5BA3CF","#87CEEB","#5BA3CF","#87CEEB","#5BA3CF","#87CEEB","#5BA3CF","#87CEEB","#5BA3CF","#87CEEB","#5BA3CF","#87CEEB","#5BA3CF","#87CEEB","#5BA3CF","#87CEEB","#5BA3CF","#87CEEB"],
        ["#277DA1","#277DA1","#277DA1","#277DA1","#277DA1","#277DA1","#277DA1","#277DA1","#277DA1","#277DA1","#277DA1","#277DA1","#277DA1","#277DA1","#277DA1","#277DA1","#277DA1","#277DA1"]]},
      {name:"Frog", px:253, desc:"Frog on lily pad", grid:[
        [T,T,T,T,"#1A6B3C","#1A6B3C","#1A6B3C","#1A6B3C",T,T,"#1A6B3C","#1A6B3C","#1A6B3C","#1A6B3C",T,T,T,T],
        [T,T,T,"#1A6B3C","#1A6B3C","#3E8B57","#3E8B57","#1A6B3C","#1A6B3C","#1A6B3C","#1A6B3C","#3E8B57","#3E8B57","#1A6B3C","#1A6B3C",T,T,T],
        [T,T,T,"#1A6B3C","#222222","#222222","#3E8B57","#1A6B3C","#3E8B57","#3E8B57","#1A6B3C","#3E8B57","#222222","#222222","#1A6B3C",T,T,T],
        [T,T,T,"#1A6B3C","#222222","#FFFFFF","#222222","#1A6B3C","#7EC87E","#7EC87E","#1A6B3C","#222222","#FFFFFF","#222222","#1A6B3C",T,T,T],
        [T,T,"#1A6B3C","#1A6B3C","#7EC87E","#7EC87E","#7EC87E","#7EC87E","#7EC87E","#7EC87E","#7EC87E","#7EC87E","#7EC87E","#7EC87E","#1A6B3C","#1A6B3C",T,T],
        [T,T,"#1A6B3C","#7EC87E","#7EC87E","#F28C9A","#7EC87E","#7EC87E","#7EC87E","#7EC87E","#7EC87E","#7EC87E","#F28C9A","#7EC87E","#7EC87E","#1A6B3C",T,T],
        [T,T,"#1A6B3C","#7EC87E","#7EC87E","#7EC87E","#7EC87E","#222222","#222222","#222222","#7EC87E","#7EC87E","#7EC87E","#7EC87E","#7EC87E","#1A6B3C",T,T],
        [T,T,"#1A6B3C","#3E8B57","#1A6B3C","#1A6B3C","#7EC87E","#7EC87E","#B5E6A3","#B5E6A3","#7EC87E","#7EC87E","#1A6B3C","#1A6B3C","#3E8B57","#1A6B3C","#F9C74F",T],
        [T,"#4A9FD9","#1A6B3C","#3E8B57","#3E8B57","#1A6B3C","#7EC87E","#B5E6A3","#B5E6A3","#B5E6A3","#B5E6A3","#7EC87E","#1A6B3C","#3E8B57","#3E8B57","#1A6B3C","#F9C74F","#F9C74F"],
        ["#4A9FD9","#4A9FD9","#1A6B3C","#3E8B57","#1A6B3C","#7EC87E","#7EC87E","#7EC87E","#B5E6A3","#B5E6A3","#7EC87E","#7EC87E","#7EC87E","#1A6B3C","#3E8B57","#1A6B3C",T,T],
        ["#4A9FD9","#4A9FD9","#4A9FD9","#1A6B3C","#1A6B3C","#7EC87E","#3E8B57","#7EC87E","#7EC87E","#7EC87E","#7EC87E","#3E8B57","#7EC87E","#1A6B3C","#1A6B3C",T,T,T],
        ["#4A9FD9","#4A9FD9","#4A9FD9","#1A6B3C","#5EAD5E","#5EAD5E","#1A6B3C","#5EAD5E","#5EAD5E","#5EAD5E","#5EAD5E","#1A6B3C","#5EAD5E","#5EAD5E","#5EAD5E","#1A6B3C",T,T],
        [T,"#4A9FD9","#4A9FD9","#1A6B3C","#5EAD5E","#5EAD5E","#5EAD5E","#5EAD5E","#2D7A2D","#5EAD5E","#5EAD5E","#5EAD5E","#5EAD5E","#5EAD5E","#5EAD5E","#1A6B3C","#4A9FD9",T],
        [T,"#4A9FD9","#4A9FD9","#4A9FD9","#1A6B3C","#1A6B3C","#5EAD5E","#5EAD5E","#5EAD5E","#5EAD5E","#5EAD5E","#5EAD5E","#1A6B3C","#1A6B3C","#1A6B3C","#4A9FD9","#4A9FD9",T],
        [T,T,"#4A9FD9","#4A9FD9","#4A9FD9","#4A9FD9","#1A6B3C","#1A6B3C","#1A6B3C","#1A6B3C","#1A6B3C","#1A6B3C","#4A9FD9","#4A9FD9","#4A9FD9","#4A9FD9",T,T]]},
      {name:"Elephant", px:294, desc:"Gentle elephant", grid:[
        [T,T,T,T,T,T,T,T,"#999999","#999999","#999999","#999999","#999999",T,T,T,T,T,T,T],
        [T,T,T,T,T,T,"#999999","#999999","#CCCCCC","#CCCCCC","#CCCCCC","#CCCCCC","#999999","#999999","#999999",T,T,T,T,T],
        [T,T,T,T,"#999999","#999999","#CCCCCC","#CCCCCC","#CCCCCC","#CCCCCC","#CCCCCC","#CCCCCC","#CCCCCC","#CCCCCC","#999999","#999999",T,T,T,T],
        [T,T,"#999999","#999999","#CCCCCC","#CCCCCC","#CCCCCC","#CCCCCC","#CCCCCC","#CCCCCC","#CCCCCC","#CCCCCC","#CCCCCC","#CCCCCC","#CCCCCC","#CCCCCC","#999999","#999999",T,T],
        ["#999999","#999999","#CCCCCC","#CCCCCC","#CCCCCC","#333333","#CCCCCC","#CCCCCC","#CCCCCC","#CCCCCC","#CCCCCC","#CCCCCC","#333333","#CCCCCC","#CCCCCC","#CCCCCC","#CCCCCC","#CCCCCC","#999999","#999999"],
        ["#999999","#CCCCCC","#CCCCCC","#CCCCCC","#CCCCCC","#CCCCCC","#CCCCCC","#CCCCCC","#CCCCCC","#CCCCCC","#CCCCCC","#CCCCCC","#CCCCCC","#CCCCCC","#CCCCCC","#CCCCCC","#CCCCCC","#CCCCCC","#CCCCCC","#999999"],
        ["#999999","#CCCCCC","#CCCCCC","#CCCCCC","#CCCCCC","#CCCCCC","#CCCCCC","#CCCCCC","#999999","#999999","#999999","#CCCCCC","#CCCCCC","#CCCCCC","#CCCCCC","#CCCCCC","#CCCCCC","#CCCCCC","#CCCCCC","#999999"],
        ["#999999","#999999","#CCCCCC","#CCCCCC","#CCCCCC","#CCCCCC","#CCCCCC","#999999","#CCCCCC","#CCCCCC","#CCCCCC","#999999","#CCCCCC","#CCCCCC","#CCCCCC","#CCCCCC","#CCCCCC","#CCCCCC","#999999","#999999"],
        [T,"#999999","#999999","#CCCCCC","#CCCCCC","#CCCCCC","#CCCCCC","#999999","#CCCCCC","#CCCCCC","#CCCCCC","#999999","#CCCCCC","#CCCCCC","#CCCCCC","#CCCCCC","#CCCCCC","#999999","#999999",T],
        [T,T,"#999999","#999999","#CCCCCC","#CCCCCC","#999999","#999999","#CCCCCC","#CCCCCC","#CCCCCC","#999999","#999999","#CCCCCC","#CCCCCC","#CCCCCC","#999999","#999999",T,T],
        [T,T,T,"#999999","#999999","#CCCCCC","#999999",T,"#999999","#CCCCCC","#999999",T,"#999999","#CCCCCC","#CCCCCC","#999999","#999999",T,T,T],
        [T,T,T,T,"#999999","#CCCCCC","#999999",T,"#999999","#CCCCCC","#999999",T,"#999999","#CCCCCC","#999999","#999999",T,T,T,T],
        [T,T,T,T,"#999999","#CCCCCC","#999999",T,T,"#999999",T,T,"#999999","#CCCCCC","#999999",T,T,T,T,T],
        [T,T,T,T,"#999999","#999999","#999999",T,T,T,T,T,"#999999","#999999","#999999",T,T,T,T,T],
        [T,T,T,"#999999","#999999","#999999","#999999","#999999",T,T,T,"#999999","#999999","#999999","#999999","#999999",T,T,T,T]]},
      {name:"Tree of Life", px:330, desc:"Majestic tree of life", grid:[
        [T,T,T,T,T,T,T,T,"#90BE6D","#90BE6D","#90BE6D","#90BE6D","#90BE6D","#90BE6D",T,T,T,T,T,T],
        [T,T,T,T,T,T,"#90BE6D","#90BE6D","#7EC87E","#7EC87E","#B5E6A3","#7EC87E","#7EC87E","#90BE6D","#90BE6D",T,T,T,T,T],
        [T,T,T,T,"#90BE6D","#90BE6D","#7EC87E","#B5E6A3","#B5E6A3","#7EC87E","#7EC87E","#B5E6A3","#B5E6A3","#7EC87E","#90BE6D","#90BE6D",T,T,T,T],
        [T,T,"#90BE6D","#90BE6D","#7EC87E","#B5E6A3","#7EC87E","#7EC87E","#90BE6D",T,T,"#90BE6D","#7EC87E","#7EC87E","#B5E6A3","#7EC87E","#90BE6D","#90BE6D",T,T],
        [T,"#90BE6D","#7EC87E","#B5E6A3","#7EC87E","#7EC87E","#90BE6D",T,T,T,T,T,T,"#90BE6D","#7EC87E","#7EC87E","#B5E6A3","#7EC87E","#90BE6D",T],
        ["#90BE6D","#7EC87E","#7EC87E","#7EC87E","#90BE6D","#90BE6D",T,T,T,T,T,T,T,T,"#90BE6D","#90BE6D","#7EC87E","#7EC87E","#7EC87E","#90BE6D"],
        [T,"#90BE6D","#90BE6D","#90BE6D",T,T,T,T,T,"#8B4513","#8B4513","#8B4513",T,T,T,T,"#90BE6D","#90BE6D","#90BE6D",T],
        [T,T,T,T,T,T,T,T,"#8B4513","#D2691E","#D2691E","#D2691E","#8B4513",T,T,T,T,T,T,T],
        [T,T,T,T,T,T,T,"#8B4513","#D2691E","#D2691E","#D2691E","#D2691E","#D2691E","#8B4513",T,T,T,T,T,T],
        [T,T,T,T,T,T,"#8B4513","#D2691E","#D2691E","#D2691E","#D2691E","#D2691E","#D2691E","#D2691E","#8B4513",T,T,T,T,T],
        [T,T,T,T,T,"#8B4513","#D2691E","#D2691E","#8B4513","#D2691E","#D2691E","#8B4513","#D2691E","#D2691E","#D2691E","#8B4513",T,T,T,T],
        [T,T,T,T,"#8B4513","#D2691E","#D2691E","#8B4513",T,T,"#8B4513","#8B4513",T,"#8B4513","#D2691E","#D2691E","#8B4513",T,T,T],
        [T,T,T,"#8B4513","#8B4513","#D2691E","#8B4513",T,T,T,T,T,T,T,"#8B4513","#D2691E","#8B4513","#8B4513",T,T],
        ["#90BE6D","#90BE6D","#90BE6D","#90BE6D","#90BE6D","#90BE6D","#90BE6D","#90BE6D","#90BE6D","#90BE6D","#90BE6D","#90BE6D","#90BE6D","#90BE6D","#90BE6D","#90BE6D","#90BE6D","#90BE6D","#90BE6D","#90BE6D"],
        ["#1A6B3C","#1A6B3C","#1A6B3C","#1A6B3C","#1A6B3C","#1A6B3C","#1A6B3C","#1A6B3C","#1A6B3C","#1A6B3C","#1A6B3C","#1A6B3C","#1A6B3C","#1A6B3C","#1A6B3C","#1A6B3C","#1A6B3C","#1A6B3C","#1A6B3C","#1A6B3C"]]}
    ]
  };

  /* ── Render a pixel grid onto a small canvas ── */
  function renderDesignCanvas(grid, targetSize) {
    var rows = grid.length;
    var cols = 0;
    for (var r = 0; r < rows; r++) {
      if (grid[r].length > cols) cols = grid[r].length;
    }
    var ps = Math.max(1, Math.floor(targetSize / Math.max(rows, cols)));
    var c = document.createElement('canvas');
    c.width = cols * ps;
    c.height = rows * ps;
    c.style.width = c.width + 'px';
    c.style.height = c.height + 'px';
    var ctx = c.getContext('2d');
    for (var r = 0; r < rows; r++) {
      for (var col = 0; col < grid[r].length; col++) {
        var color = grid[r][col];
        if (color) {
          ctx.fillStyle = color;
          ctx.fillRect(col * ps, r * ps, ps, ps);
        }
      }
    }
    return c;
  }

  /* ── Create a card element ── */
  function createCard(d, tier) {
    var card = document.createElement('div');
    card.className = 'design-card';
    var cost = d.px * PV;

    var preview = document.createElement('div');
    preview.className = 'design-preview';
    if (d.grid) {
      preview.appendChild(renderDesignCanvas(d.grid, 64));
    } else {
      var placeholder = document.createElement('div');
      placeholder.style.cssText = 'width:60px;height:60px;background:linear-gradient(135deg,rgba(67,170,139,.15),rgba(248,150,30,.15));border-radius:6px;display:flex;align-items:center;justify-content:center;font-size:1.5rem';
      placeholder.textContent = d.name.charAt(0);
      preview.appendChild(placeholder);
    }
    card.appendChild(preview);

    var name = document.createElement('div');
    name.className = 'design-name';
    name.textContent = d.name;
    card.appendChild(name);

    var meta = document.createElement('div');
    meta.className = 'design-meta';
    meta.textContent = d.px + ' patches';
    card.appendChild(meta);

    var price = document.createElement('div');
    price.className = 'design-price';
    price.textContent = '$' + cost.toLocaleString();
    card.appendChild(price);

    card.addEventListener('click', function() { openDesignDetail(d, tier); });
    return card;
  }

  /* ── Open design detail overlay ── */
  function openDesignDetail(d, tier) {
    var overlay = document.getElementById('design-detail-overlay');
    var cost = d.px * PV;

    document.getElementById('dd-name').textContent = d.name;
    document.getElementById('dd-price').textContent = '$' + cost.toLocaleString();
    document.getElementById('dd-meta').textContent = d.px + ' patches \u00b7 ' + (d.desc || tier + ' design');

    var previewEl = document.getElementById('dd-preview');
    previewEl.innerHTML = '';
    if (d.grid) {
      previewEl.appendChild(renderDesignCanvas(d.grid, 160));
    }

    var info = document.getElementById('dd-info');
    info.innerHTML = 'This design uses <strong>' + d.px + ' patches</strong> on the quilt. ' +
      'Your $' + cost.toLocaleString() + ' donation will place this pixel art design on the quilt for everyone to see. ' +
      'Click below to donate and we\u2019ll place your design!';

    var cta = document.getElementById('dd-cta');
    cta.href = ZEFFY + '?design=' + encodeURIComponent(d.name) + '&squares=' + d.px + '&donate=true';
    cta.textContent = 'Donate $' + cost.toLocaleString() + ' & Claim \u2192';

    overlay.classList.add('active');
  }

  /* ── Close detail ── */
  document.getElementById('design-detail-close').addEventListener('click', function() {
    document.getElementById('design-detail-overlay').classList.remove('active');
  });
  document.getElementById('design-detail-overlay').addEventListener('click', function(e) {
    if (e.target === this) this.classList.remove('active');
  });

  /* ── Populate grids ── */
  var miniGrid = document.getElementById('design-grid-mini');
  var premGrid = document.getElementById('design-grid-premium');
  var ultraGrid = document.getElementById('design-grid-ultra');

  designs.mini.forEach(function(d) { miniGrid.appendChild(createCard(d, 'Mini')); });
  designs.premium.forEach(function(d) { premGrid.appendChild(createCard(d, 'Premium')); });
  designs.ultra.forEach(function(d) { ultraGrid.appendChild(createCard(d, 'Ultra')); });
})();
"""

# -- Inject Python data as inline script ----------------------------------------
data_script = (
    "<script>window.__QD__ = {"
    + f'"amounts":{amounts_json},'
    + f'"names":{names_json},'
    + f'"colors":{colors_json},'
    + f'"patchValue":{PATCH_VALUE},'
    + f'"total":{TOTAL},'
    + f'"cols":{COLS},'
    + f'"rows":{ROWS},'
    + f'"zeffyUrl":"{ZEFFY_URL}",'
    + f'"appsScriptUrl":"{APPS_SCRIPT_URL}",'
    + f'"pctGoal":{pct_goal}'
    + "};</script>"
)

HTML = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=DM+Sans:opsz,wght@9..40,300;9..40,400;9..40,500&display=swap" rel="stylesheet" media="print" onload="this.media='all'">
<style>{CSS}</style>
</head>
<body>
{data_script}

<div class="wrap">
  <p class="eyebrow">Salem, Indiana &middot; Washington County</p>
  <h1 class="title">The Community<br><em>Crossroads Quilt</em></h1>
  <p class="tagline">37,500 patches. One for every $20 it takes to save .70 acres of this corner forever. Every voice fills a square.</p>
  <span class="fun-note">&#x1F9F5; No actual sewing required.</span>

  <div class="progress-wrap">
    <div class="progress-header">
      <span class="progress-raised">{raised_fmt} raised</span>
      <span class="progress-goal">of $750,000 goal</span>
    </div>
    <div class="progress-track">
      <div class="progress-fill" id="progress-fill"></div>
    </div>
    <div class="progress-sub">
      <span class="prog-chip">
        <span class="prog-dot" style="background:{PRIMARY}"></span>
        {claimed_patches} claimed
      </span>
      <span class="prog-chip">
        <span class="prog-dot" style="background:#f0ebe0;border:1px solid #bbb"></span>
        {unclaimed} unclaimed
      </span>
    </div>
  </div>

  <div class="layout">
    <div class="quilt-col">
      <div class="quilt-border">
        <div class="quilt-grid" id="quilt-grid">
{grid_html}
        </div>
      </div>
      <div class="legend">
        <div class="legend-item">
          <div class="swatch" style="background:{PRIMARY}"></div>Claimed
        </div>
        <div class="legend-item">
          <div class="swatch" style="background:#f0ebe0;border-color:#aaa"></div>Unclaimed
        </div>
        <span style="font-size:.65rem;color:#4a5c5a;font-style:italic;margin-left:auto">scroll to zoom &middot; drag to pan &middot; click to claim</span>
      </div>
      <div class="zoom-controls">
        <button class="zoom-btn" id="zoom-out">&minus;</button>
        <span class="zoom-label" id="zoom-label">100%</span>
        <button class="zoom-btn" id="zoom-in">+</button>
        <button class="zoom-btn" id="zoom-reset" style="font-size:.6rem;width:auto;padding:0 .5rem">Reset</button>
      </div>
    </div>

    <div class="sidebar">
      <div class="stat-card">
        <div class="stat-label">Campaign Goal</div>
        <div class="stat-val">$750,000</div>
        <div class="stat-sub">Land acquisition &middot; 37,500 patches</div>
      </div>
      <div class="stat-card">
        <div class="stat-label">Total Raised</div>
        <div class="stat-val">{raised_fmt}</div>
        <div class="stat-sub">{raised_sub}</div>
      </div>
      <div class="countdown">
        <div class="cd-num">{days_remaining}</div>
        <div class="cd-label">days until July 9</div>
      </div>
      <a href="{ZEFFY_URL}" class="donate-btn" target="_blank">Claim a Patch &rarr;</a>
      <p class="micro">$20 = 1 patch. $100 = 5 patches.<br>Pick your own colors!<br>Every single voice counts.</p>
    </div>
  </div>
</div>

<!-- Design Gallery -->
<div class="design-section">
  <h2 class="design-section-title">Claim a <em>Pixel Art Design</em></h2>
  <p class="design-section-sub">Pick a pre-made design and place it on the quilt with your donation. Click any design below to preview it and claim your spot.</p>

  <div class="design-tier">
    <div class="design-tier-label">Mini Designs &middot; $160 &ndash; $640</div>
    <div class="design-grid" id="design-grid-mini"></div>
  </div>

  <div class="design-tier">
    <div class="design-tier-label">Premium Designs &middot; $1,000 &ndash; $3,300</div>
    <div class="design-grid" id="design-grid-premium"></div>
  </div>

  <div class="design-tier">
    <div class="design-tier-label">Showpiece Designs &middot; $2,700 &ndash; $6,600+</div>
    <div class="design-grid" id="design-grid-ultra"></div>
  </div>
</div>

<!-- Design Detail Overlay -->
<div class="design-detail-overlay" id="design-detail-overlay">
  <div class="design-detail">
    <button class="design-detail-close" id="design-detail-close">&times;</button>
    <h2 id="dd-name"></h2>
    <span class="dd-price" id="dd-price"></span>
    <div class="dd-meta" id="dd-meta"></div>
    <div class="dd-preview" id="dd-preview"></div>
    <div class="dd-info" id="dd-info"></div>
    <a class="dd-cta" id="dd-cta" href="#" target="_blank">Donate &amp; Claim This Design &rarr;</a>
  </div>
</div>

<!-- Modal -->
<div class="modal-overlay" id="modal-overlay">
  <div class="modal">
    <button class="modal-close" id="modal-close">&times;</button>
    <h2>Claim Your Patch</h2>
    <span class="patch-num" id="modal-patch-num"></span>

    <div id="modal-amount-section">
      <label for="modal-name">Your Name</label>
      <input type="text" class="amount-input" id="modal-name" placeholder="How you want to appear on the quilt">

      <label for="modal-amount">Donation Amount</label>
      <input type="number" class="amount-input" id="modal-amount" min="20" step="20" value="20" placeholder="$20 minimum">
      <div class="sq-count" id="modal-sq-count"></div>
    </div>

    <div id="modal-picked-summary"></div>

    <label>Choose Your Color</label>
    <div id="modal-color-area"></div>

    <button class="donate-submit" id="modal-autofill-btn" style="display:none">Auto-fill nearby squares with random colors</button>
    <button class="donate-submit" id="modal-next-btn" style="display:none">Select Next Square &rarr;</button>
    <button class="donate-submit" id="modal-donate-btn">Donate &amp; Claim &rarr;</button>
  </div>
</div>

<div id="tip"></div>
<script>{JS}</script>
<script>{GALLERY_JS}</script>
</body>
</html>"""

st.components.v1.html(HTML, height=4200, scrolling=True)
