import streamlit as st
import requests
import json
import math
from datetime import datetime

st.set_page_config(
    page_title="Community Crossroads Quilt",
    page_icon="🧵",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Config ─────────────────────────────────────────────────────────────────────
SHEET_URL = (
    "https://docs.google.com/spreadsheets/d/e/"
    "2PACX-1vQGdBOCAs2ubRWec2f7JxiqfLL9A1yylLjB90k8cPR55z5S14hpjnkcED-5hCdMBLY1viCz52qOZsVG"
    "/pub?output=csv"
)
PATCH_VALUE = 1000
TOTAL = 750
GOAL = TOTAL * PATCH_VALUE
DEADLINE = datetime(2026, 7, 9, 17, 0, 0)
ZEFFY_URL = "https://www.zeffy.com/en-US/peer-to-peer/community-crossroads"


# ── Data ───────────────────────────────────────────────────────────────────────
@st.cache_data(ttl=300)
def load_patch_data() -> list[float]:
    try:
        r = requests.get(SHEET_URL, timeout=10)
        r.raise_for_status()
        return _parse_csv(r.text)
    except Exception:
        return [0.0] * TOTAL


def _parse_csv(csv_text: str) -> list[float]:
    rows = csv_text.strip().split("\n")
    patches = [0.0] * TOTAL
    cursor = 0
    for row in rows:
        if cursor >= TOTAL:
            break
        raw = row.split(",")[0].strip().strip("\"'")
        cell = "".join(c for c in raw if c.isdigit() or c == ".")
        try:
            val = float(cell)
        except ValueError:
            continue
        if val <= 0:
            continue
        remaining = val
        while remaining > 0 and cursor < TOTAL:
            space = PATCH_VALUE - patches[cursor]
            pour = min(remaining, space)
            patches[cursor] += pour
            remaining -= pour
            if patches[cursor] >= PATCH_VALUE:
                cursor += 1
    return patches


def _days_remaining() -> int:
    diff = DEADLINE - datetime.now()
    return max(0, math.ceil(diff.total_seconds() / 86400))


# ── Stats ───────────────────────────────────────────────────────────────────────
amounts = load_patch_data()
amounts_json = json.dumps([round(a, 2) for a in amounts])
total_raised = round(sum(amounts))
full_patches = sum(1 for a in amounts if a >= PATCH_VALUE)
partial_patches = sum(1 for a in amounts if 0 < a < PATCH_VALUE)
days_remaining = _days_remaining()
pct_goal = round(min(100.0, total_raised / GOAL * 100), 1)
raised_sub = "Be the first patch!" if total_raised == 0 else f"{full_patches} patches claimed"

# ── Hide Streamlit chrome ───────────────────────────────────────────────────────
st.markdown(
    """
    <style>
    #MainMenu, footer, header {visibility: hidden;}
    .stApp {background: transparent !important;}
    .block-container {padding: 0 !important; max-width: 100% !important;}
    section[data-testid="stSidebar"] {display: none;}
    iframe {border: none !important;}
    </style>
    """,
    unsafe_allow_html=True,
)

# ── HTML component ──────────────────────────────────────────────────────────────
HTML = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=DM+Sans:opsz,wght@9..40,300;9..40,400;9..40,500&display=swap" rel="stylesheet">
<style>
*,*::before,*::after{{box-sizing:border-box;margin:0;padding:0}}
html,body{{width:100%;background:#faf8f3;font-family:'DM Sans',sans-serif;color:#1e3d1c}}
.wrap{{max-width:1100px;margin:0 auto;padding:2rem 1.25rem 3rem}}
.eyebrow{{font-size:.68rem;letter-spacing:.28em;text-transform:uppercase;color:#c4923a;font-weight:500;margin-bottom:.5rem}}
.title{{font-family:'Playfair Display',serif;font-size:clamp(1.9rem,5vw,3rem);line-height:1.1;color:#1e3d1c;margin-bottom:.6rem}}
.title em{{color:#3d6e38;font-style:italic}}
.tagline{{font-size:.95rem;line-height:1.7;color:#4a5c47;max-width:600px;margin-bottom:.5rem}}
.fun-note{{display:inline-block;font-size:.75rem;color:#8b3a2a;font-style:italic;background:rgba(139,58,42,.07);padding:.3rem .75rem;border-radius:20px;border:1px dashed rgba(139,58,42,.25)}}
.progress-wrap{{margin:1.5rem 0}}
.progress-header{{display:flex;justify-content:space-between;align-items:baseline;margin-bottom:.5rem}}
.progress-raised{{font-family:'Playfair Display',serif;font-size:1.35rem;color:#3d6e38}}
.progress-goal{{font-size:.78rem;color:#4a5c47}}
.progress-track{{height:10px;background:rgba(30,61,28,.1);border-radius:99px;overflow:hidden}}
.progress-fill{{height:100%;border-radius:99px;background:linear-gradient(90deg,#3d6e38 0%,#5a8f52 60%,#c4923a 100%);width:{pct_goal}%}}
.progress-sub{{display:flex;gap:1.5rem;margin-top:.5rem;flex-wrap:wrap}}
.prog-chip{{font-size:.7rem;color:#4a5c47;display:flex;align-items:center;gap:.3rem}}
.prog-dot{{width:8px;height:8px;border-radius:2px;flex-shrink:0}}
.layout{{display:flex;gap:2rem;align-items:flex-start;flex-wrap:wrap}}
.quilt-col{{flex:1;min-width:280px}}
.sidebar{{flex:0 0 210px;min-width:180px}}
.canvas-border{{border:3px solid #1e3d1c;border-radius:4px;padding:3px;background:#1e3d1c;line-height:0}}
canvas{{display:block;cursor:pointer}}
.legend{{display:flex;gap:.9rem;margin-top:.75rem;flex-wrap:wrap;align-items:center}}
.legend-item{{display:flex;align-items:center;gap:.35rem;font-size:.68rem;color:#4a5c47}}
.swatch{{width:10px;height:10px;border-radius:1px;border:1px solid rgba(0,0,0,.12);flex-shrink:0}}
.stat-card{{border:1px solid rgba(30,61,28,.15);border-radius:6px;padding:1rem 1.1rem;margin-bottom:.75rem;background:rgba(250,248,243,.7)}}
.stat-label{{font-size:.62rem;letter-spacing:.15em;text-transform:uppercase;color:#4a5c47;margin-bottom:.2rem}}
.stat-val{{font-family:'Playfair Display',serif;font-size:1.5rem;color:#3d6e38;line-height:1.1}}
.stat-sub{{font-size:.65rem;color:#4a5c47;margin-top:.2rem}}
.countdown{{text-align:center;padding:.85rem .75rem;background:rgba(139,58,42,.06);border:1px dashed rgba(139,58,42,.22);border-radius:6px;margin-bottom:.75rem}}
.cd-num{{font-family:'Playfair Display',serif;font-size:2rem;color:#8b3a2a;line-height:1}}
.cd-label{{font-size:.6rem;letter-spacing:.12em;text-transform:uppercase;color:#8b3a2a;opacity:.75;margin-top:.15rem}}
.donate-btn{{display:block;width:100%;text-align:center;background:#3d6e38;color:#faf8f3;font-family:'DM Sans',sans-serif;font-weight:500;font-size:.75rem;letter-spacing:.1em;text-transform:uppercase;text-decoration:none;padding:.9rem 1rem;border-radius:4px;margin-bottom:.6rem;border:none;cursor:pointer;transition:background .2s,transform .15s}}
.donate-btn:hover{{background:#4a7a44;transform:translateY(-1px)}}
.micro{{font-size:.65rem;color:#4a5c47;line-height:1.55;font-style:italic;text-align:center}}
#tip{{position:fixed;background:#1e3d1c;color:#faf8f3;font-size:.7rem;padding:.4rem .7rem;border-radius:3px;pointer-events:none;z-index:9999;opacity:0;transition:opacity .1s;white-space:nowrap;font-family:'DM Sans',sans-serif}}
.floatmsg{{position:fixed;pointer-events:none;z-index:9999;font-size:1.1rem;font-weight:500;font-family:'DM Sans',sans-serif;animation:float-up .9s ease both}}
@keyframes float-up{{0%{{transform:translateY(0) scale(1);opacity:1}}100%{{transform:translateY(-70px) scale(1.5);opacity:0}}}}
@media(max-width:640px){{
  .layout{{flex-direction:column}}
  .sidebar{{flex:none;width:100%;display:grid;grid-template-columns:1fr 1fr;gap:.5rem}}
  .sidebar .countdown,.sidebar .donate-btn,.sidebar .micro{{grid-column:span 2}}
}}
</style>
</head>
<body>
<div class="wrap">

  <p class="eyebrow">Salem, Indiana &middot; Washington County</p>
  <h1 class="title">The Community<br><em>Crossroads Quilt</em></h1>
  <p class="tagline">750 patches. One for every $1,000 we need to save this corner forever. Every voice fills a square &mdash; even yours, Dean.</p>
  <span class="fun-note">&#x1F9F5; No actual sewing required. Spencer's uncle would be proud.</span>

  <div class="progress-wrap">
    <div class="progress-header">
      <span class="progress-raised">${total_raised:,} raised</span>
      <span class="progress-goal">of $750,000 goal</span>
    </div>
    <div class="progress-track"><div class="progress-fill"></div></div>
    <div class="progress-sub">
      <span class="prog-chip"><span class="prog-dot" style="background:#3d6e38"></span><span id="full-count">{full_patches}</span> fully filled</span>
      <span class="prog-chip"><span class="prog-dot" style="background:linear-gradient(to top,#3d6e38 50%,#f0ebe0 50%);border:1px solid #aaa"></span><span id="partial-count">{partial_patches}</span> partial</span>
      <span class="prog-chip"><span class="prog-dot" style="background:#f0ebe0;border:1px solid #bbb"></span><span id="unclaimed-count">{TOTAL - full_patches - partial_patches}</span> unclaimed</span>
    </div>
  </div>

  <div class="layout">
    <div class="quilt-col">
      <div class="canvas-border" id="canvas-wrap">
        <canvas id="quilt"></canvas>
      </div>
      <div class="legend">
        <div class="legend-item"><div class="swatch" style="background:#3d6e38"></div>Fully filled</div>
        <div class="legend-item"><div class="swatch" style="background:linear-gradient(to top,#3d6e38 50%,#f0ebe0 50%);border-color:#aaa"></div>Partial</div>
        <div class="legend-item"><div class="swatch" style="background:#f0ebe0;border-color:#aaa"></div>Unclaimed</div>
        <span style="font-size:.65rem;color:#4a5c47;font-style:italic;margin-left:auto">hover &middot; click to fill</span>
      </div>
    </div>

    <div class="sidebar">
      <div class="stat-card">
        <div class="stat-label">Campaign Goal</div>
        <div class="stat-val">$750,000</div>
        <div class="stat-sub">Land acquisition &middot; 750 patches</div>
      </div>
      <div class="stat-card">
        <div class="stat-label">Total Raised</div>
        <div class="stat-val">${total_raised:,}</div>
        <div class="stat-sub">{raised_sub}</div>
      </div>
      <div class="countdown">
        <div class="cd-num">{days_remaining}</div>
        <div class="cd-label">days until July 9</div>
      </div>
      <a href="{ZEFFY_URL}" class="donate-btn" target="_blank">Fill a Patch &rarr;</a>
      <p class="micro">$1,000 = 1 patch filled.<br>10 people &times; $100 = same thing.<br>Every single voice counts.</p>
    </div>
  </div>

</div>
<div id="tip"></div>

<script>
(function(){{
  var AMOUNTS  = {amounts_json};
  var PATCH_VAL = 1000;
  var TOTAL    = 750;
  var ZEFFY    = "{ZEFFY_URL}";
  var PALETTE  = [
    '#e6194b','#3cb44b','#ffe119','#4363d8','#f58231',
    '#911eb4','#42d4f4','#f032e6','#bfef45','#fabed4',
    '#469990','#dcbeff','#9a6324','#800000','#aaffc3',
    '#808000','#ffd8b1','#000075','#a9a9a9','#e6beff',
    '#1a3a1e','#2d5c32','#3d7a45','#4a8f52','#62a666',
    '#1e3a5f','#2a5a8a','#3a72aa','#5a8aba',
    '#5c1a1a','#8a2a2a','#aa3a3a','#c45a4a','#d4826a',
    '#6a3a0a','#8a5a1a','#aa7a2a','#c4923a','#d4a84a',
    '#4a1a5a','#6a2a7a','#8a4a9a','#a06aba',
    '#1a4a4a','#2a6a6a','#3a8a8a','#5aaa9a'
  ];
  var HINTS   = ['claim me!','yours?','fill me!','don\'t be shy','c\'mon!'];
  var EMOJI   = ['&#x1F9F5;','&#x2728;','&#x1F49A;','&#x1F331;','&#x1F3E1;','&#x1F389;'];
  var FLOATS  = ['thank you!','stitched!','yes!!','patch claimed!','yours now!'];

  /* assign each patch a random but stable color */
  var PATCH_COLORS = [];
  (function(){{
    /* simple seeded RNG for stable colors per patch */
    var seed = 12345;
    function rand(){{ seed = (seed * 16807 + 0) % 2147483647; return seed / 2147483647; }}
    for (var i = 0; i < TOTAL; i++){{
      PATCH_COLORS.push(PALETTE[Math.floor(rand() * PALETTE.length)]);
    }}
  }})();

  var canvas = document.getElementById('quilt');
  var ctx    = canvas.getContext('2d');
  var wrap   = document.getElementById('canvas-wrap');
  var COLS, ROWS, CELL, GAP = 2, W, H;
  var hovIdx = -1;

  function measure(){{
    /* use document body width which is reliable in Streamlit iframes */
    var bodyW = document.body.clientWidth || document.documentElement.clientWidth || 900;
    var availW = Math.max(300, bodyW - 280); /* subtract sidebar + gaps */
    COLS = (bodyW < 640) ? 15 : 25;
    ROWS = Math.ceil(TOTAL / COLS);
    CELL = Math.max(6, Math.floor((availW - (COLS - 1) * GAP) / COLS));
    W = COLS * CELL + (COLS - 1) * GAP;
    H = ROWS * CELL + (ROWS - 1) * GAP;
  }}

  function drawAll(){{
    measure();
    var dpr = Math.min(window.devicePixelRatio || 1, 2);
    canvas.width  = W * dpr;
    canvas.height = H * dpr;
    canvas.style.width  = W + 'px';
    canvas.style.height = H + 'px';
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);

    for (var i = 0; i < TOTAL; i++){{
      drawPatch(i, i === hovIdx);
    }}
  }}

  function drawPatch(i, hov){{
    var c    = i % COLS,  r = Math.floor(i / COLS);
    var x    = c * (CELL + GAP), y = r * (CELL + GAP);
    var amt  = AMOUNTS[i] || 0;
    var pct  = Math.min(1, amt / PATCH_VAL);
    var col  = PATCH_COLORS[i];
    var EMPTY = '#f0ebe0';

    if (pct <= 0){{
      ctx.fillStyle = EMPTY;
      ctx.fillRect(x, y, CELL, CELL);
      /* hatch */
      ctx.save();
      ctx.beginPath(); ctx.rect(x, y, CELL, CELL); ctx.clip();
      ctx.strokeStyle = 'rgba(60,60,50,0.09)';
      ctx.lineWidth = 1;
      for (var k = -CELL; k < CELL * 2; k += 5){{
        ctx.beginPath(); ctx.moveTo(x + k, y); ctx.lineTo(x + k + CELL, y + CELL); ctx.stroke();
      }}
      ctx.restore();
    }} else if (pct >= 1){{
      ctx.fillStyle = hov ? lighten(col) : col;
      ctx.fillRect(x, y, CELL, CELL);
      if (CELL > 9){{
        var ins = Math.max(1, Math.floor(CELL * 0.18));
        ctx.strokeStyle = 'rgba(255,255,255,0.22)';
        ctx.lineWidth = 1;
        ctx.strokeRect(x + ins + 0.5, y + ins + 0.5, CELL - 2*ins - 1, CELL - 2*ins - 1);
      }}
    }} else {{
      /* partial fill from bottom */
      var fh = Math.max(1, Math.round(pct * CELL));
      ctx.fillStyle = EMPTY;
      ctx.fillRect(x, y, CELL, CELL);
      ctx.fillStyle = hov ? lighten(col) : col;
      ctx.fillRect(x, y + CELL - fh, CELL, fh);
    }}

    if (hov){{
      ctx.strokeStyle = 'rgba(255,255,255,0.7)';
      ctx.lineWidth = 2;
      ctx.strokeRect(x + 1, y + 1, CELL - 2, CELL - 2);
    }}
  }}

  function lighten(hex){{
    var r = Math.min(255, parseInt(hex.slice(1,3), 16) + 55);
    var g = Math.min(255, parseInt(hex.slice(3,5), 16) + 55);
    var b = Math.min(255, parseInt(hex.slice(5,7), 16) + 55);
    return 'rgb(' + r + ',' + g + ',' + b + ')';
  }}

  function idxAt(e){{
    var rect = canvas.getBoundingClientRect();
    var scaleX = W / rect.width;
    var scaleY = H / rect.height;
    var mx = (e.clientX - rect.left) * scaleX;
    var my = (e.clientY - rect.top)  * scaleY;
    var c  = Math.floor(mx / (CELL + GAP));
    var r  = Math.floor(my / (CELL + GAP));
    if (c < 0 || c >= COLS || r < 0 || r >= ROWS) return -1;
    var idx = r * COLS + c;
    return idx < TOTAL ? idx : -1;
  }}

  function updateCounts(){{
    var full = 0, partial = 0;
    for (var i = 0; i < TOTAL; i++){{
      var a = AMOUNTS[i] || 0;
      if (a >= PATCH_VAL) full++;
      else if (a > 0) partial++;
    }}
    var el;
    el = document.getElementById('full-count'); if (el) el.textContent = full;
    el = document.getElementById('partial-count'); if (el) el.textContent = partial;
    el = document.getElementById('unclaimed-count'); if (el) el.textContent = (TOTAL - full - partial);
  }}

  var tip = document.getElementById('tip');

  canvas.addEventListener('mousemove', function(e){{
    var idx = idxAt(e);
    if (idx !== hovIdx){{
      hovIdx = idx;
      drawAll();
    }}
    if (idx < 0){{ tip.style.opacity = 0; return; }}
    var amt = AMOUNTS[idx] || 0, pct = Math.min(1, amt / PATCH_VAL);
    var msg;
    if (pct <= 0){{
      msg = 'Patch #' + (idx+1) + ' - ' + HINTS[idx % HINTS.length];
    }} else if (pct >= 1){{
      msg = 'Patch #' + (idx+1) + ' - fully filled! $' + amt.toLocaleString();
    }} else {{
      msg = 'Patch #' + (idx+1) + ' - $' + amt.toLocaleString() + ' of $1,000 (' + Math.round(pct*100) + '%)';
    }}
    tip.textContent = msg;
    tip.style.opacity = 1;
    tip.style.left = (e.clientX + 14) + 'px';
    tip.style.top  = (e.clientY - 32) + 'px';
  }});

  canvas.addEventListener('mouseleave', function(){{
    hovIdx = -1; drawAll(); tip.style.opacity = 0;
  }});

  canvas.addEventListener('click', function(e){{
    var idx = idxAt(e);
    if (idx < 0) return;

    /* fill the clicked square to full if not already */
    if ((AMOUNTS[idx] || 0) < PATCH_VAL){{
      AMOUNTS[idx] = PATCH_VAL;
      updateCounts();
      drawAll();
    }}

    /* float message */
    var msg = document.createElement('div');
    msg.className   = 'floatmsg';
    msg.textContent = FLOATS[Math.floor(Math.random() * FLOATS.length)];
    msg.style.left  = e.clientX + 'px';
    msg.style.top   = (e.clientY - 10) + 'px';
    msg.style.color = PATCH_COLORS[idx];
    document.body.appendChild(msg);
    setTimeout(function(){{ msg.remove(); }}, 950);

    /* also open donation page */
    setTimeout(function(){{
      window.open(ZEFFY + '?patch=' + (idx + 1), '_blank');
    }}, 400);
  }});

  window.addEventListener('resize', drawAll);

  /* retry drawing until body has a real width (Streamlit iframe may load slowly) */
  function initDraw(){{
    var bodyW = document.body.clientWidth || 0;
    if (bodyW > 100){{
      drawAll();
    }} else {{
      requestAnimationFrame(initDraw);
    }}
  }}
  initDraw();
}})();
</script>
</body>
</html>"""

st.components.v1.html(HTML, height=1400, scrolling=True)
