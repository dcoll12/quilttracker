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

SHEET_URL = (
    "https://docs.google.com/spreadsheets/d/e/2PACX-1vQGdBOCAs2ubRWec2f7JxiqfLL9A1yylLjB90k8cPR55z5S14hpjnkcED-5hCdMBLY1viCz52qOZsVG/pub?output=csv"
)
PATCH_VALUE = 20
TOTAL = 958
COLS = 31
ROWS = 31
GOAL = 750000
DEADLINE = datetime(2026, 7, 9, 17, 0, 0)
ZEFFY_URL = "https://www.zeffy.com/en-US/peer-to-peer/community-crossroads"

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
    """Load sheet CSV. Columns: A=patch#, B=amount, C=color, D=email, E=name."""
    try:
        r = requests.get(SHEET_URL, timeout=10)
        r.raise_for_status()
        return _parse_csv(r.text)
    except Exception:
        return {
            "amounts": [0.0] * TOTAL,
            "colors": [""] * TOTAL,
            "names": [""] * TOTAL,
        }


def _parse_csv(csv_text):
    rows = csv_text.strip().split("\n")
    amounts = [0.0] * TOTAL
    colors = [""] * TOTAL
    names = [""] * TOTAL

    for row in rows:
        cols = row.split(",")
        # Column A: patch number (1-based)
        raw_num = cols[0].strip().strip("\"'") if len(cols) > 0 else ""
        num_str = "".join(c for c in raw_num if c.isdigit())
        if not num_str:
            continue
        idx = int(num_str) - 1  # convert to 0-based
        if idx < 0 or idx >= TOTAL:
            continue

        # Column B: amount
        if len(cols) > 1:
            raw_amt = cols[1].strip().strip("\"'")
            amt_str = "".join(c for c in raw_amt if c.isdigit() or c == ".")
            try:
                amounts[idx] = float(amt_str)
            except ValueError:
                pass

        # Column C: color hex
        if len(cols) > 2:
            raw_col = cols[2].strip().strip("\"'")
            if raw_col.startswith("#"):
                colors[idx] = raw_col

        # Column E: name (D=email skipped for display)
        if len(cols) > 4:
            names[idx] = cols[4].strip().strip("\"'")

    return {"amounts": amounts, "colors": colors, "names": names}


def _days_remaining():
    diff = DEADLINE - datetime.now()
    return max(0, math.ceil(diff.total_seconds() / 86400))


def _build_grid_html(amounts, sheet_colors, default_colors):
    """Generate patch divs. Use sheet color if claimed, else hatched empty."""
    parts = []
    for i in range(TOTAL):
        amt = amounts[i]
        claimed = amt >= PATCH_VALUE
        if claimed:
            col = sheet_colors[i] if sheet_colors[i] else default_colors[i]
            cls = "sq filled"
            style = f"background:{col}"
        else:
            cls = "sq empty"
            style = ""
        parts.append(
            f'<div class="{cls}" data-i="{i}">'
            f'<div class="sq-inner" style="{style}"></div></div>'
        )
    return "\n".join(parts)


data = load_patch_data()
amounts = data["amounts"]
sheet_colors = data["colors"]
sheet_names = data["names"]
amounts_json = json.dumps([round(a, 2) for a in amounts])
names_json = json.dumps(sheet_names)
default_colors = _lcg_colors()
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
    #MainMenu, footer, header {visibility: hidden;}
    .stApp {background: transparent !important;}
    .block-container {padding: 0 !important; max-width: 100% !important;}
    section[data-testid="stSidebar"] {display: none;}
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
.quilt-border{border:3px solid #1a3040;border-radius:4px;padding:3px;background:#1a3040;width:100%}
.quilt-grid{display:grid;grid-template-columns:repeat(""" + str(COLS) + """,1fr);gap:2px;width:100%}
.sq{position:relative;cursor:pointer;border-radius:1px;transition:filter .12s}
.sq::before{content:'';display:block;padding-top:100%}
.sq:hover{filter:brightness(1.3);z-index:2}
.sq-inner{position:absolute;top:0;left:0;right:0;bottom:0;border-radius:1px}
.sq.empty .sq-inner{background:#f0ebe0;background-image:repeating-linear-gradient(45deg,transparent,transparent 3px,rgba(60,60,50,.06) 3px,rgba(60,60,50,.06) 4px)}
.sq.filled .sq-inner::after{content:'';position:absolute;inset:18%;border:1px solid rgba(255,255,255,.22)}
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
.apply-all-btn{background:none;border:1px solid rgba(67,170,139,.4);color:""" + PRIMARY + """;font-size:.7rem;padding:.35rem .8rem;border-radius:4px;cursor:pointer;font-family:'DM Sans',sans-serif;margin-top:.25rem;margin-bottom:.5rem;transition:background .15s}
.apply-all-btn:hover{background:rgba(67,170,139,.08)}
.modal .donate-submit{display:block;width:100%;text-align:center;background:""" + PRIMARY + """;color:#faf8f3;font-family:'DM Sans',sans-serif;font-weight:600;font-size:.85rem;letter-spacing:.08em;text-transform:uppercase;text-decoration:none;padding:.9rem 1rem;border-radius:5px;margin-top:1.25rem;border:none;cursor:pointer;transition:background .2s}
.modal .donate-submit:hover{background:#3a9b7e}
.modal .donate-submit:disabled{background:#aaa;cursor:not-allowed}

@media(max-width:640px){
  .quilt-grid{grid-template-columns:repeat(16,1fr)}
  .layout{flex-direction:column}
  .sidebar{flex:none;width:100%;display:grid;grid-template-columns:1fr 1fr;gap:.5rem}
  .sidebar .countdown,.sidebar .donate-btn,.sidebar .micro{grid-column:span 2}
  .modal{padding:1.25rem}
  .color-swatch{width:30px;height:30px}
}
"""

# -- JS — interactivity, modal, tooltips ----------------------------------------
JS = """
(function() {
  var D      = window.__QD__;
  var A      = D.amounts;
  var NAMES  = D.names;
  var PV     = D.patchValue;
  var ZEFFY  = D.zeffyUrl;
  var PCT    = D.pctGoal;
  var TOTAL  = D.total;

  var PAL = ['#F94144','#F3722C','#F8961E','#F9844A','#F9C74F','#90BE6D','#43AA8B','#4D908E','#577590','#277DA1'];

  var seed = 99991;
  function srand() { seed = (seed * 16807) % 2147483647; return seed / 2147483647; }
  var COL = [];
  for (var i = 0; i < TOTAL; i++) COL.push(PAL[Math.floor(srand() * PAL.length)]);

  var HINTS  = ['claim me!', 'yours?', 'fill me!', 'be bold', "c'mon!"];

  var grid = document.getElementById('quilt-grid');

  /* Animate progress bar */
  var fill = document.getElementById('progress-fill');
  if (fill) setTimeout(function() { fill.style.width = PCT + '%'; }, 150);

  /* Auto-resize iframe height */
  function notifyHeight() {
    var h = document.body.scrollHeight;
    window.parent.postMessage({ type: 'streamlit:setFrameHeight', height: h }, '*');
  }
  setTimeout(notifyHeight, 300);
  window.addEventListener('resize', notifyHeight);

  var tip = document.getElementById('tip');

  grid.addEventListener('mousemove', function(e) {
    var sq = e.target;
    if (sq && !sq.hasAttribute('data-i') && sq.parentNode && sq.parentNode.hasAttribute('data-i')) {
      sq = sq.parentNode;
    }
    if (!sq || !sq.hasAttribute('data-i')) { tip.style.opacity = 0; return; }
    var idx = parseInt(sq.getAttribute('data-i'));
    var amt = A[idx] || 0;
    var claimed = amt >= PV;
    var msg;
    if (!claimed && amt <= 0) {
      msg = 'Patch #' + (idx+1) + ' \\u2013 ' + HINTS[idx % HINTS.length];
    } else if (claimed) {
      var name = NAMES[idx] || 'Anonymous';
      msg = 'Patch #' + (idx+1) + ' \\u2013 ' + name + ' \\u2013 $' + amt.toLocaleString();
    } else {
      msg = 'Patch #' + (idx+1) + ' \\u2013 $' + amt.toLocaleString();
    }
    tip.textContent = msg;
    tip.style.opacity = 1;
    tip.style.left = (e.clientX + 14) + 'px';
    tip.style.top  = (e.clientY - 36) + 'px';
  });

  grid.addEventListener('mouseleave', function() { tip.style.opacity = 0; });

  /* ------- Modal ------- */
  var overlay = document.getElementById('modal-overlay');
  var modalPatchNum = document.getElementById('modal-patch-num');
  var amountInput = document.getElementById('modal-amount');
  var sqCountEl = document.getElementById('modal-sq-count');
  var colorArea = document.getElementById('modal-color-area');
  var applyAllBtn = document.getElementById('modal-apply-all');
  var donateBtn = document.getElementById('modal-donate-btn');
  var modalCloseBtn = document.getElementById('modal-close');
  var currentIdx = -1;

  function openModal(idx) {
    currentIdx = idx;
    modalPatchNum.textContent = "You're claiming patch #" + (idx + 1);
    amountInput.value = '20';
    updateSquareCount();
    overlay.classList.add('active');
    setTimeout(notifyHeight, 50);
  }

  function closeModal() {
    overlay.classList.remove('active');
    currentIdx = -1;
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
      : 'At $' + val + ' you get ' + numSq + ' square' + (numSq > 1 ? 's' : '') + ' to color' + (numSq > 1 ? ' \\u2014 pick a color for each one' : '');
    renderColorPickers(numSq);
  }

  amountInput.addEventListener('input', updateSquareCount);

  var selectedColors = [];

  function renderColorPickers(numSq) {
    colorArea.innerHTML = '';
    selectedColors = [];
    if (numSq <= 0) {
      applyAllBtn.style.display = 'none';
      donateBtn.disabled = true;
      return;
    }
    donateBtn.disabled = false;
    applyAllBtn.style.display = numSq > 1 ? 'inline-block' : 'none';

    for (var s = 0; s < numSq; s++) {
      selectedColors.push('');
      var row = document.createElement('div');
      row.className = 'color-row';
      if (numSq > 1) {
        var label = document.createElement('span');
        label.className = 'row-label';
        label.textContent = 'Sq ' + (s + 1) + ':';
        row.appendChild(label);
      }
      for (var p = 0; p < PAL.length; p++) {
        var sw = document.createElement('div');
        sw.className = 'color-swatch';
        sw.style.background = PAL[p];
        sw.setAttribute('data-sq', s);
        sw.setAttribute('data-color', PAL[p]);
        sw.addEventListener('click', onSwatchClick);
        row.appendChild(sw);
      }
      colorArea.appendChild(row);
    }
    /* Pre-select first color for each square */
    for (var s2 = 0; s2 < numSq; s2++) {
      selectColor(s2, PAL[s2 % PAL.length]);
    }
  }

  function onSwatchClick(e) {
    var sqIdx = parseInt(e.target.getAttribute('data-sq'));
    var color = e.target.getAttribute('data-color');
    selectColor(sqIdx, color);
  }

  function selectColor(sqIdx, color) {
    selectedColors[sqIdx] = color;
    var rows = colorArea.querySelectorAll('.color-row');
    if (rows[sqIdx]) {
      var swatches = rows[sqIdx].querySelectorAll('.color-swatch');
      for (var j = 0; j < swatches.length; j++) {
        swatches[j].classList.toggle('selected', swatches[j].getAttribute('data-color') === color);
      }
    }
  }

  applyAllBtn.addEventListener('click', function() {
    if (selectedColors.length === 0) return;
    var first = selectedColors[0] || PAL[0];
    for (var s = 0; s < selectedColors.length; s++) {
      selectColor(s, first);
    }
  });

  donateBtn.addEventListener('click', function() {
    if (currentIdx < 0) return;
    var val = parseInt(amountInput.value) || 0;
    var numSq = Math.floor(val / PV);
    if (numSq < 1) return;

    /* Check all colors selected */
    for (var c = 0; c < numSq; c++) {
      if (!selectedColors[c]) {
        alert('Please pick a color for square ' + (c+1));
        return;
      }
    }

    var colorStr = selectedColors.slice(0, numSq).map(function(c) { return encodeURIComponent(c); }).join(',');
    var url = ZEFFY + '?patch=' + (currentIdx + 1) + '&squares=' + numSq + '&colors=' + colorStr + '&donate=true';
    window.open(url, '_blank');
    closeModal();
  });

  /* ------- Grid click ------- */
  grid.addEventListener('click', function(e) {
    var sq = e.target;
    if (sq && !sq.hasAttribute('data-i') && sq.parentNode && sq.parentNode.hasAttribute('data-i')) {
      sq = sq.parentNode;
    }
    if (!sq || !sq.hasAttribute('data-i')) return;
    var idx = parseInt(sq.getAttribute('data-i'));
    var claimed = (A[idx] || 0) >= PV;
    if (claimed) return;
    openModal(idx);
  });
})();
"""

# -- Inject Python data as inline script ----------------------------------------
data_script = (
    "<script>window.__QD__ = {"
    + f'"amounts":{amounts_json},'
    + f'"names":{names_json},'
    + f'"patchValue":{PATCH_VALUE},'
    + f'"total":{TOTAL},'
    + f'"zeffyUrl":"{ZEFFY_URL}",'
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
  <p class="tagline">958 patches. One for every $20 it takes to save .44 acres of this corner forever. Every voice fills a square.</p>
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
        <span style="font-size:.65rem;color:#4a5c5a;font-style:italic;margin-left:auto">hover &middot; click to claim</span>
      </div>
    </div>

    <div class="sidebar">
      <div class="stat-card">
        <div class="stat-label">Campaign Goal</div>
        <div class="stat-val">$750,000</div>
        <div class="stat-sub">Land acquisition &middot; 958 patches</div>
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

<!-- Modal -->
<div class="modal-overlay" id="modal-overlay">
  <div class="modal">
    <button class="modal-close" id="modal-close">&times;</button>
    <h2>Claim Your Patch</h2>
    <span class="patch-num" id="modal-patch-num"></span>

    <label for="modal-amount">Donation Amount</label>
    <input type="number" class="amount-input" id="modal-amount" min="20" step="20" value="20" placeholder="$20 minimum">
    <div class="sq-count" id="modal-sq-count"></div>

    <label>Choose Your Colors</label>
    <button class="apply-all-btn" id="modal-apply-all" style="display:none">Apply first color to all</button>
    <div id="modal-color-area"></div>

    <button class="donate-submit" id="modal-donate-btn">Donate &amp; Claim &rarr;</button>
  </div>
</div>

<div id="tip"></div>
<script>{JS}</script>
</body>
</html>"""

st.components.v1.html(HTML, height=1800, scrolling=False)
