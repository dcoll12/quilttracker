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


# ── Compute stats ──────────────────────────────────────────────────────────────
amounts = load_patch_data()
amounts_json = json.dumps([round(a, 2) for a in amounts])
total_raised = round(sum(amounts))
full_patches = sum(1 for a in amounts if a >= PATCH_VALUE)
partial_patches = sum(1 for a in amounts if 0 < a < PATCH_VALUE)
days_remaining = _days_remaining()
pct_goal = round(min(100.0, total_raised / GOAL * 100), 1)

# ── Hide Streamlit chrome ──────────────────────────────────────────────────────
st.markdown(
    """
    <style>
    #MainMenu, footer, header {visibility: hidden;}
    .stApp {background: transparent !important;}
    .block-container {padding: 0 !important; max-width: 100% !important;}
    section[data-testid="stSidebar"] {display: none;}
    </style>
    """,
    unsafe_allow_html=True,
)

# ── HTML component ─────────────────────────────────────────────────────────────
HTML = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=DM+Sans:opsz,wght@9..40,300;9..40,400;9..40,500&display=swap" rel="stylesheet">
<style>
*,*::before,*::after{{box-sizing:border-box;margin:0;padding:0}}
html,body{{width:100%;min-height:100%;overflow-x:hidden}}
:root{{
  --forest:#1e3d1c;--sage:#3d6e38;--sage2:#5a8f52;
  --gold:#c4923a;--terra:#8b3a2a;
  --cream:#faf8f3;--parchment:#f0ebe0;--muted:#4a5c47;
  --border:rgba(30,61,28,.15);
}}
body{{font-family:'DM Sans',sans-serif;background:var(--cream);color:var(--forest)}}

/* ── Layout ── */
.wrap{{max-width:1100px;margin:0 auto;padding:2rem 1.25rem 3rem}}
.eyebrow{{font-size:.68rem;letter-spacing:.28em;text-transform:uppercase;color:var(--gold);font-weight:500;margin-bottom:.5rem}}
.title{{font-family:'Playfair Display',serif;font-size:clamp(1.9rem,5vw,3rem);line-height:1.1;color:var(--forest);margin-bottom:.6rem}}
.title em{{color:var(--sage);font-style:italic}}
.tagline{{font-size:.95rem;line-height:1.7;color:var(--muted);max-width:600px;margin-bottom:.5rem}}
.fun-note{{display:inline-block;font-size:.75rem;color:var(--terra);font-style:italic;background:rgba(139,58,42,.07);padding:.3rem .75rem;border-radius:20px;border:1px dashed rgba(139,58,42,.25)}}

/* ── Progress bar ── */
.progress-wrap{{margin:1.5rem 0}}
.progress-header{{display:flex;justify-content:space-between;align-items:baseline;margin-bottom:.5rem}}
.progress-raised{{font-family:'Playfair Display',serif;font-size:1.35rem;color:var(--sage)}}
.progress-goal{{font-size:.78rem;color:var(--muted)}}
.progress-track{{height:10px;background:rgba(30,61,28,.1);border-radius:99px;overflow:hidden}}
.progress-fill{{height:100%;border-radius:99px;background:linear-gradient(90deg,var(--sage) 0%,var(--sage2) 60%,var(--gold) 100%);width:{pct_goal}%}}
.progress-sub{{display:flex;gap:1.5rem;margin-top:.5rem;flex-wrap:wrap}}
.prog-chip{{font-size:.7rem;color:var(--muted);display:flex;align-items:center;gap:.3rem}}
.prog-dot{{width:8px;height:8px;border-radius:2px;flex-shrink:0}}

/* ── Main layout ── */
.layout{{display:flex;gap:2rem;align-items:flex-start;flex-wrap:wrap}}
.quilt-col{{flex:1;min-width:280px}}
.sidebar{{flex:0 0 210px;min-width:180px}}

/* ── Grid ── */
.grid-border{{
  border:3px solid var(--forest);border-radius:4px;
  padding:3px;background:var(--forest);
}}
.cc-grid{{
  display:grid;
  grid-template-columns:repeat(var(--cols,25),1fr);
  gap:2px;background:var(--forest);
}}

/* ── Patches ── */
.cc-patch{{
  border-radius:1px;position:relative;
  cursor:pointer;overflow:hidden;
  /* height set by JS via --cell-px; aspect-ratio as fallback */
  height:var(--cell-px,auto);
  aspect-ratio:1;
  transition:transform .12s ease,filter .12s ease,box-shadow .12s ease;
}}
.cc-patch:hover{{transform:scale(1.5);z-index:20;filter:brightness(1.2);box-shadow:0 2px 8px rgba(0,0,0,.35)}}
.cc-patch.empty{{background:var(--parchment) !important}}
.cc-patch.empty::before{{
  content:'';position:absolute;inset:0;
  background-image:repeating-linear-gradient(45deg,rgba(60,60,50,.08) 0,rgba(60,60,50,.08) 1px,transparent 1px,transparent 6px);
}}
.cc-patch.empty:hover{{animation:wiggle .35s ease both}}
.cc-patch.filled::after,.cc-patch.partial::after{{
  content:'';position:absolute;inset:18%;
  border:1px solid rgba(255,255,255,.18);border-radius:1px;pointer-events:none;
}}
.cc-patch.selected{{outline:2px solid var(--gold);outline-offset:1px;z-index:30}}

@keyframes pop-in{{0%{{transform:scale(.2) rotate(-20deg);opacity:0}}65%{{transform:scale(1.2) rotate(3deg)}}100%{{transform:scale(1) rotate(0);opacity:1}}}}
@keyframes wiggle{{0%,100%{{transform:rotate(0) scale(1)}}25%{{transform:rotate(-5deg) scale(1.3)}}75%{{transform:rotate(5deg) scale(1.3)}}}}
.anim-pop{{animation:pop-in .4s cubic-bezier(.34,1.56,.64,1) both}}

/* ── Legend ── */
.legend{{display:flex;gap:.9rem;margin-top:.75rem;flex-wrap:wrap;align-items:center}}
.legend-item{{display:flex;align-items:center;gap:.35rem;font-size:.68rem;color:var(--muted)}}
.swatch{{width:10px;height:10px;border-radius:1px;border:1px solid rgba(0,0,0,.12);flex-shrink:0}}

/* ── Sidebar ── */
.stat-card{{border:1px solid var(--border);border-radius:6px;padding:1rem 1.1rem;margin-bottom:.75rem;background:rgba(250,248,243,.7)}}
.stat-label{{font-size:.62rem;letter-spacing:.15em;text-transform:uppercase;color:var(--muted);margin-bottom:.2rem}}
.stat-val{{font-family:'Playfair Display',serif;font-size:1.5rem;color:var(--sage);line-height:1.1}}
.stat-sub{{font-size:.65rem;color:var(--muted);margin-top:.2rem}}
.countdown{{text-align:center;padding:.85rem .75rem;background:rgba(139,58,42,.06);border:1px dashed rgba(139,58,42,.22);border-radius:6px;margin-bottom:.75rem}}
.cd-num{{font-family:'Playfair Display',serif;font-size:2rem;color:var(--terra);line-height:1}}
.cd-label{{font-size:.6rem;letter-spacing:.12em;text-transform:uppercase;color:var(--terra);opacity:.75;margin-top:.15rem}}
.donate-btn{{display:block;width:100%;text-align:center;background:var(--sage);color:var(--cream);font-family:'DM Sans',sans-serif;font-weight:500;font-size:.75rem;letter-spacing:.1em;text-transform:uppercase;text-decoration:none;padding:.9rem 1rem;border-radius:4px;margin-bottom:.6rem;border:none;cursor:pointer;transition:background .2s,transform .15s}}
.donate-btn:hover{{background:#4a7a44;transform:translateY(-1px)}}
.micro{{font-size:.65rem;color:var(--muted);line-height:1.55;font-style:italic;text-align:center}}

/* ── Tooltip ── */
#tip{{position:fixed;background:var(--forest);color:var(--cream);font-size:.7rem;padding:.4rem .7rem;border-radius:3px;pointer-events:none;z-index:9999;opacity:0;transition:opacity .1s;white-space:nowrap;font-family:'DM Sans',sans-serif}}

/* ── Float message ── */
.floatmsg{{position:fixed;pointer-events:none;z-index:9999;font-size:1.1rem;font-weight:500;font-family:'DM Sans',sans-serif;animation:float-up .9s ease both}}
@keyframes float-up{{0%{{transform:translateY(0) scale(1);opacity:1}}100%{{transform:translateY(-70px) scale(1.5);opacity:0}}}}

/* ── Responsive ── */
@media(max-width:640px){{
  .layout{{flex-direction:column}}
  .sidebar{{flex:none;width:100%;display:grid;grid-template-columns:1fr 1fr;gap:.5rem}}
  .sidebar .countdown,.sidebar .donate-btn,.sidebar .micro{{grid-column:span 2}}
}}
</style>
</head>
<body>
<div class="wrap">

  <p class="eyebrow">Salem, Indiana · Washington County</p>
  <h1 class="title">The Community<br><em>Crossroads Quilt</em></h1>
  <p class="tagline">750 patches. One for every $1,000 we need to save this corner forever. Every voice fills a square — even yours, Dean.</p>
  <span class="fun-note">🧵 No actual sewing required. Spencer's uncle would be proud.</span>

  <div class="progress-wrap">
    <div class="progress-header">
      <span class="progress-raised">${total_raised:,} raised</span>
      <span class="progress-goal">of $750,000 goal</span>
    </div>
    <div class="progress-track"><div class="progress-fill"></div></div>
    <div class="progress-sub">
      <span class="prog-chip"><span class="prog-dot" style="background:var(--sage)"></span>{full_patches} fully filled</span>
      <span class="prog-chip"><span class="prog-dot" style="background:linear-gradient(to top,var(--sage) 50%,var(--parchment) 50%);border:1px solid #aaa"></span>{partial_patches} partial</span>
      <span class="prog-chip"><span class="prog-dot" style="background:var(--parchment);border:1px solid #bbb"></span>{TOTAL - full_patches - partial_patches} unclaimed</span>
    </div>
  </div>

  <div class="layout">
    <div class="quilt-col">
      <div class="grid-border">
        <div class="cc-grid" id="cc-grid"></div>
      </div>
      <div class="legend">
        <div class="legend-item"><div class="swatch" style="background:var(--sage)"></div>Fully filled</div>
        <div class="legend-item"><div class="swatch" style="background:linear-gradient(to top,var(--sage) 50%,var(--parchment) 50%);border-color:#aaa"></div>Partial</div>
        <div class="legend-item"><div class="swatch" style="background:var(--parchment);border-color:#aaa"></div>Unclaimed</div>
        <span style="font-size:.65rem;color:var(--muted);font-style:italic;margin-left:auto">hover · click to claim</span>
      </div>
    </div>

    <div class="sidebar">
      <div class="stat-card">
        <div class="stat-label">Campaign Goal</div>
        <div class="stat-val">$750,000</div>
        <div class="stat-sub">Land acquisition · 750 patches</div>
      </div>
      <div class="stat-card">
        <div class="stat-label">Total Raised</div>
        <div class="stat-val">${total_raised:,}</div>
        <div class="stat-sub">{"Be the first patch!" if total_raised == 0 else f"{full_patches} patches claimed"}</div>
      </div>
      <div class="countdown">
        <div class="cd-num">{days_remaining}</div>
        <div class="cd-label">days until July 9</div>
      </div>
      <a href="{ZEFFY_URL}" class="donate-btn" target="_blank">Fill a Patch →</a>
      <p class="micro">$1,000 = 1 patch filled.<br>10 people × $100 = same thing.<br>Every single voice counts.</p>
    </div>
  </div>

</div>
<div id="tip"></div>

<script>
(function(){{
  var AMOUNTS   = {amounts_json};
  var PATCH_VAL = 1000;
  var TOTAL     = 750;
  var ZEFFY     = "{ZEFFY_URL}";

  var PALETTE = [
    '#1a3a1e','#2d5c32','#3d7a45','#4a8f52','#62a666',
    '#5a7a55','#789e72','#8ab880',
    '#1e3a5f','#2a5a8a','#3a72aa','#5a8aba',
    '#5c1a1a','#8a2a2a','#aa3a3a','#c45a4a','#d4826a',
    '#6a3a0a','#8a5a1a','#aa7a2a','#c4923a','#d4a84a',
    '#4a1a5a','#6a2a7a','#8a4a9a','#a06aba',
    '#4a2a1a','#6a4a2a','#8a6a3a','#aa8a52',
    '#1a4a4a','#2a6a6a','#3a8a8a','#5aaa9a',
    '#4a0a1a','#6a1a2a','#8a2a3a','#aa4a5a',
    '#3a3a1e','#5a5a2a','#7a7a3a','#9a9a4a',
  ];
  var EMPTY_HINTS  = ['claim me!','👀','yours?','fill me!','don\'t be shy','🫶','c\'mon!'];
  var FILLED_EMOJI = ['🧵','✨','💚','🌱','🏡','🎉','❤️','🌻','🌳','🎶'];
  var FLOAT_MSGS   = ['thank you! 💚','stitched!','yes!! 🎉','patch claimed!','🧵 yours now!'];

  function patchColor(i) {{
    var h = Math.imul(i * 2654435761, 1) >>> 0;
    h = Math.imul(h ^ (h >>> 16), 0x45d9f3b) >>> 0;
    return PALETTE[h % PALETTE.length];
  }}

  /* ── sizeGrid ──────────────────────────────────────────────────────────────
     window.innerWidth is always available inside an iframe — no DOM
     measurement needed. We derive cell size from it directly.
     The grid sits inside a flex layout: full width minus sidebar (210px),
     gap (2rem=32px), padding (2×1.25rem=40px), borders (12px).
  ── */
  var COLS = 25;
  function calcCellPx() {{
    var iw = window.innerWidth || 800;
    var isMobile = iw < 640;
    var gridW;
    if (isMobile) {{
      gridW = iw - 40; // just padding
    }} else {{
      gridW = iw - 40 - 32 - 210 - 12; // padding + gap + sidebar + borders
    }}
    gridW = Math.max(gridW, 150);
    return Math.floor((gridW - (COLS - 1) * 2) / COLS);
  }}

  function applySize() {{
    var cell = calcCellPx();
    if (cell < 4) return;
    // Set CSS custom property so the CSS height:var(--cell-px) also works
    document.documentElement.style.setProperty('--cell-px', cell + 'px');
    var grid = document.getElementById('cc-grid');
    grid.style.gridAutoRows = cell + 'px';
    // Force height on every patch — belt-and-suspenders
    var patches = grid.getElementsByClassName('cc-patch');
    for (var i = 0; i < patches.length; i++) {{
      patches[i].style.height = cell + 'px';
    }}
  }}

  function buildGrid() {{
    var grid  = document.getElementById('cc-grid');
    var frag  = document.createDocumentFragment();
    var EMPTY = '#f0ebe0';

    for (var i = 0; i < TOTAL; i++) {{
      var amt   = (i < AMOUNTS.length) ? AMOUNTS[i] : 0;
      var pct   = Math.min(1, amt / PATCH_VAL);
      var color = patchColor(i);
      var el    = document.createElement('div');
      el.className   = 'cc-patch anim-pop';
      el.dataset.idx = i;
      el.dataset.amt = amt;
      el.dataset.pct = pct;
      el.style.animationDelay = (i * 0.004) + 's';

      if (pct <= 0) {{
        el.classList.add('empty');
        el.style.background = EMPTY;
      }} else if (pct >= 1) {{
        el.classList.add('filled');
        el.style.background = color;
      }} else {{
        el.classList.add('partial');
        var fp = Math.round(pct * 100);
        el.style.background = 'linear-gradient(to top,' + color + ' ' + fp + '%,' + EMPTY + ' ' + fp + '%)';
      }}
      frag.appendChild(el);
    }}
    grid.appendChild(frag);

    // Size immediately then again after paint
    applySize();
    requestAnimationFrame(applySize);
    setTimeout(applySize, 200);

    attachListeners(grid);
  }}

  function attachListeners(grid) {{
    var tip = document.getElementById('tip');

    grid.addEventListener('mousemove', function(e) {{
      var t = e.target;
      if (!t.classList.contains('cc-patch')) {{ tip.style.opacity = 0; return; }}
      var idx = +t.dataset.idx, amt = +t.dataset.amt || 0, pct = +t.dataset.pct || 0;
      var msg;
      if (pct <= 0)      msg = 'Patch #' + (idx+1) + ' — ' + EMPTY_HINTS[idx % EMPTY_HINTS.length];
      else if (pct >= 1) msg = 'Patch #' + (idx+1) + ' — fully filled! $' + amt.toLocaleString() + ' ' + FILLED_EMOJI[idx % FILLED_EMOJI.length];
      else               msg = 'Patch #' + (idx+1) + ' — $' + amt.toLocaleString() + ' of $1,000 (' + Math.round(pct*100) + '% there!)';
      tip.textContent = msg;
      tip.style.opacity = 1;
      tip.style.left = (e.clientX + 14) + 'px';
      tip.style.top  = (e.clientY - 32) + 'px';
    }});
    grid.addEventListener('mouseleave', function() {{ tip.style.opacity = 0; }});

    grid.addEventListener('click', function(e) {{
      var t = e.target;
      if (!t.classList.contains('cc-patch')) return;
      var pct = +t.dataset.pct || 0, patchNum = +t.dataset.idx + 1;

      t.classList.add('selected');
      setTimeout(function() {{ t.classList.remove('selected'); }}, 500);

      if (pct < 1) {{
        var color = patchColor(+t.dataset.idx), prevBg = t.style.background;
        t.style.background = color;
        t.classList.remove('empty','partial'); t.classList.add('filled');
        setTimeout(function() {{
          t.style.background = prevBg;
          t.classList.remove('filled');
          if (pct <= 0) t.classList.add('empty'); else t.classList.add('partial');
        }}, 1200);
      }}

      var msg = document.createElement('div');
      msg.className = 'floatmsg';
      msg.textContent = FLOAT_MSGS[Math.floor(Math.random() * FLOAT_MSGS.length)];
      msg.style.left = e.clientX + 'px';
      msg.style.top  = (e.clientY - 10) + 'px';
      document.body.appendChild(msg);
      setTimeout(function() {{ msg.remove(); }}, 950);

      if (pct < 1) {{
        setTimeout(function() {{
          window.open(ZEFFY + '?patch=' + patchNum, '_blank');
        }}, 350);
      }}
    }});
  }}

  function updateCountdown() {{
    var deadline = new Date('2026-07-09T17:00:00-05:00');
    var days = Math.max(0, Math.ceil((deadline - Date.now()) / 86400000));
    var el = document.getElementById('cd-days');
    if (el) el.textContent = days;
  }}

  updateCountdown();
  buildGrid();
  window.addEventListener('resize', applySize);
}})();
</script>
</body>
</html>"""

st.components.v1.html(HTML, height=1400, scrolling=True)
