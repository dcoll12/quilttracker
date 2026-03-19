import streamlit as st
import requests
import json
import math
import random
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

PALETTE = [
    '#e6194b','#3cb44b','#ffe119','#4363d8','#f58231',
    '#911eb4','#42d4f4','#f032e6','#bfef45','#fabed4',
    '#469990','#dcbeff','#9a6324','#800000','#aaffc3',
    '#808000','#ffd8b1','#000075','#e6beff',
    '#2d5c32','#3d7a45','#4a8f52','#62a666',
    '#1e3a5f','#2a5a8a','#3a72aa','#5a8aba',
    '#8a2a2a','#aa3a3a','#c45a4a','#d4826a',
    '#8a5a1a','#aa7a2a','#c4923a','#d4a84a',
    '#6a2a7a','#8a4a9a','#a06aba',
    '#2a6a6a','#3a8a8a','#5aaa9a',
]


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


# ── Assign stable random colors ───────────────────────────────────────────────
@st.cache_data
def get_patch_colors() -> list[str]:
    rng = random.Random(42)
    return [rng.choice(PALETTE) for _ in range(TOTAL)]


# ── Stats ───────────────────────────────────────────────────────────────────────
amounts = load_patch_data()
amounts_json = json.dumps([round(a, 2) for a in amounts])
total_raised = round(sum(amounts))
full_patches = sum(1 for a in amounts if a >= PATCH_VALUE)
partial_patches = sum(1 for a in amounts if 0 < a < PATCH_VALUE)
days_remaining = _days_remaining()
pct_goal = round(min(100.0, total_raised / GOAL * 100), 1)
raised_sub = "Be the first patch!" if total_raised == 0 else f"{full_patches} patches claimed"
patch_colors = get_patch_colors()
colors_json = json.dumps(patch_colors)

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

# ── Build the square divs ─────────────────────────────────────────────────────
squares_html = ""
for i in range(TOTAL):
    amt = amounts[i]
    pct = min(1.0, amt / PATCH_VALUE)
    col = patch_colors[i]
    if pct >= 1:
        squares_html += f'<div class="sq filled" data-i="{i}" style="background:{col}"><div class="sq-inner"></div></div>'
    elif pct > 0:
        fill_pct = round(pct * 100)
        squares_html += f'<div class="sq partial" data-i="{i}" style="background:linear-gradient(to top,{col} {fill_pct}%,#f0ebe0 {fill_pct}%)"></div>'
    else:
        squares_html += f'<div class="sq empty" data-i="{i}" data-color="{col}"></div>'

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

/* ── Quilt grid ── */
.quilt-border{{border:3px solid #1e3d1c;border-radius:4px;padding:3px;background:#1e3d1c}}
.quilt-grid{{display:grid;grid-template-columns:repeat(25, 1fr);gap:2px}}
.sq{{aspect-ratio:1;border-radius:1px;cursor:pointer;position:relative;transition:filter .15s, outline .15s}}
.sq:hover{{filter:brightness(1.3);outline:2px solid rgba(255,255,255,0.7);outline-offset:-2px;z-index:1}}
.sq.empty{{background:#f0ebe0;background-image:repeating-linear-gradient(45deg,transparent,transparent 3px,rgba(60,60,50,0.06) 3px,rgba(60,60,50,0.06) 4px)}}
.sq.filled .sq-inner{{position:absolute;inset:18%;border:1px solid rgba(255,255,255,0.22);border-radius:0}}

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
  .quilt-grid{{grid-template-columns:repeat(15, 1fr)}}
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
  <span class="fun-note">&#x1F9F5; No actual sewing required. Spencer&#x27;s uncle would be proud.</span>

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
      <div class="quilt-border">
        <div class="quilt-grid" id="quilt-grid">
          {squares_html}
        </div>
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
        <div class="stat-val" id="total-raised">${total_raised:,}</div>
        <div class="stat-sub" id="raised-sub">{raised_sub}</div>
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
  var COLORS   = {colors_json};
  var PATCH_VAL = 1000;
  var TOTAL    = 750;
  var ZEFFY    = "{ZEFFY_URL}";
  var HINTS    = ['claim me!','yours?','fill me!','don\\'t be shy','c\\'mon!'];
  var FLOATS   = ['thank you!','stitched!','yes!!','patch claimed!','yours now!'];
  var tip      = document.getElementById('tip');

  var grid = document.getElementById('quilt-grid');
  var squares = grid.querySelectorAll('.sq');

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

  /* hover tooltips */
  grid.addEventListener('mousemove', function(e){{
    var sq = e.target.closest('.sq');
    if (!sq){{ tip.style.opacity = 0; return; }}
    var idx = parseInt(sq.getAttribute('data-i'));
    var amt = AMOUNTS[idx] || 0;
    var pct = Math.min(1, amt / PATCH_VAL);
    var msg;
    if (pct <= 0) msg = 'Patch #' + (idx+1) + ' - ' + HINTS[idx % HINTS.length];
    else if (pct >= 1) msg = 'Patch #' + (idx+1) + ' - fully filled! $' + amt.toLocaleString();
    else msg = 'Patch #' + (idx+1) + ' - $' + amt.toLocaleString() + ' of $1,000 (' + Math.round(pct*100) + '%)';
    tip.textContent = msg;
    tip.style.opacity = 1;
    tip.style.left = (e.clientX + 14) + 'px';
    tip.style.top  = (e.clientY - 32) + 'px';
  }});

  grid.addEventListener('mouseleave', function(){{
    tip.style.opacity = 0;
  }});

  /* click to fill */
  grid.addEventListener('click', function(e){{
    var sq = e.target.closest('.sq');
    if (!sq) return;
    var idx = parseInt(sq.getAttribute('data-i'));
    var col = COLORS[idx];

    /* fill the clicked square */
    if ((AMOUNTS[idx] || 0) < PATCH_VAL){{
      AMOUNTS[idx] = PATCH_VAL;
      sq.className = 'sq filled';
      sq.style.background = col;
      sq.style.backgroundImage = '';
      sq.innerHTML = '<div class="sq-inner"></div>';
      sq.removeAttribute('data-color');
      updateCounts();
    }}

    /* float message */
    var msg = document.createElement('div');
    msg.className   = 'floatmsg';
    msg.textContent = FLOATS[Math.floor(Math.random() * FLOATS.length)];
    msg.style.left  = e.clientX + 'px';
    msg.style.top   = (e.clientY - 10) + 'px';
    msg.style.color = col;
    document.body.appendChild(msg);
    setTimeout(function(){{ msg.remove(); }}, 950);

    /* open donation page */
    setTimeout(function(){{
      window.open(ZEFFY + '?patch=' + (idx + 1), '_blank');
    }}, 400);
  }});
}})();
</script>
</body>
</html>"""

st.components.v1.html(HTML, height=1400, scrolling=True)
