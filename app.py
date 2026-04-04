diff --git a/app.py b/app.py
index c095c1eeb48278c90066c83ad77837cade5d1f36..cccf6b47d910f91f3808697aaa787e12e334e003 100644
--- a/app.py
+++ b/app.py
@@ -1,31 +1,32 @@
 import streamlit as st
 import requests
 import json
 import math
 import csv
 import io
+import random
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
@@ -203,50 +204,80 @@ amounts = data["amounts"]
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
 
+# -- Streamlit live dashboard + quick navigation --------------------------------
+progress_delta = f"{pct_goal}% of goal"
+col1, col2, col3, col4 = st.columns(4)
+col1.metric("Raised", raised_fmt, delta=progress_delta)
+col2.metric("Claimed Patches", f"{claimed_patches:,}")
+col3.metric("Unclaimed Patches", f"{unclaimed:,}")
+col4.metric("Days Left", str(days_remaining))
+
+st.sidebar.header("Find Your Patch")
+search_name = st.sidebar.text_input("Donor name", placeholder="Type a name to find it")
+matching_indices = []
+if search_name.strip():
+    q = search_name.strip().lower()
+    matching_indices = [i for i, n in enumerate(sheet_names) if q in (n or "").lower()]
+    if matching_indices:
+        st.sidebar.success(f"Found {len(matching_indices)} match(es).")
+    else:
+        st.sidebar.warning("No matching names yet.")
+
+jump_to_match = st.sidebar.button("Jump to first match", disabled=not matching_indices)
+
+empty_indices = [i for i, amt in enumerate(amounts) if amt < PATCH_VALUE]
+jump_random_empty = st.sidebar.button("Jump to random empty square", disabled=not empty_indices)
+
+target_patch_idx = -1
+if jump_to_match and matching_indices:
+    target_patch_idx = matching_indices[0]
+elif jump_random_empty and empty_indices:
+    target_patch_idx = random.choice(empty_indices)
+
 st.markdown(
     """
     <style>
     /* Hide Streamlit-specific UI but keep layout space */
     #MainMenu, footer, [data-testid="stHeader"], [data-testid="stDecoration"], [data-testid="stToolbar"] {
         display: none !important;
     }
     
     /* Ensure the app container doesn't have massive negative margins */
     .block-container {
         padding-top: 2rem !important; 
         padding-bottom: 2rem !important;
         max-width: 1200px !important;
     }
 
     /* Professional Banner Styling */
     .hero-banner {
         background: linear-gradient(135deg, #1a3040 0%, #2a4a60 100%);
         padding: 3rem 2rem;
         border-radius: 12px;
         color: white;
         margin-bottom: 2.5rem;
         text-align: center;
         box-shadow: 0 10px 30px rgba(0,0,0,0.1);
     }
@@ -303,378 +334,501 @@ html,body{width:100%;background:#faf8f3;font-family:'DM Sans',sans-serif;color:#
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
+.modal .pattern-select{width:100%;padding:.65rem .8rem;border:1px solid rgba(67,170,139,.3);border-radius:5px;font-size:.95rem;font-family:'DM Sans',sans-serif;background:#fff;outline:none}
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
+.design-detail .dd-name-label{font-size:.72rem;letter-spacing:.1em;text-transform:uppercase;color:#4a5c5a;margin:.3rem 0 .35rem;display:block}
+.design-detail .dd-name-input{width:100%;padding:.65rem .8rem;border:1px solid rgba(67,170,139,.3);border-radius:5px;font-size:.95rem;font-family:'DM Sans',sans-serif;background:#fff;outline:none;margin-bottom:1rem}
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
+  var TARGET_PATCH_IDX = D.targetPatchIdx;
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
+  var dragMoved = false;
   var hoverIdx = -1;
   var pickedPatches = [];
   var pickingMode = false;
   var fullW = GRID_COLS * (CELL + GAP) + GAP;
   var fullH = GRID_ROWS * (CELL + GAP) + GAP;
+  function buildZeffyUrl(extraParams) {
+    var params = [];
+    for (var key in extraParams) {
+      if (Object.prototype.hasOwnProperty.call(extraParams, key) && extraParams[key] !== undefined && extraParams[key] !== null) {
+        params.push(key + '=' + extraParams[key]);
+      }
+    }
+    return ZEFFY + '?' + params.join('&');
+  }
+
+  function buildTxnId(prefix) {
+    return prefix + '-' + Date.now() + '-' + Math.floor(Math.random() * 100000);
+  }
 
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
 
+  function centerOnPatch(idx) {
+    if (idx < 0 || idx >= TOTAL) return;
+    var row = Math.floor(idx / GRID_COLS);
+    var col = idx % GRID_COLS;
+    var step = (CELL * zoom) + (GAP * zoom);
+    var px = col * step + (CELL * zoom) / 2;
+    var py = row * step + (CELL * zoom) / 2;
+    panX = px - canvas.width / 2;
+    panY = py - canvas.height / 2;
+    clampPan();
+    hoverIdx = idx;
+    draw();
+  }
+
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
+
+    if (window.__designPlacement && hoverIdx >= 0) {
+      var placement = buildDesignPlacement(hoverIdx);
+      if (placement) {
+        for (var i = 0; i < placement.patches.length; i++) {
+          var pidx = placement.patches[i] - 1;
+          var rr = Math.floor(pidx / GRID_COLS);
+          var cc = pidx % GRID_COLS;
+          var px = cc * step - panX + gapZ;
+          var py = rr * step - panY + gapZ;
+          ctx.fillStyle = placement.conflict ? 'rgba(249,65,68,0.45)' : 'rgba(67,170,139,0.45)';
+          ctx.fillRect(px, py, cellZ, cellZ);
+          ctx.strokeStyle = placement.conflict ? '#F94144' : '#43AA8B';
+          ctx.lineWidth = Math.max(1, zoom * 0.5);
+          ctx.strokeRect(px, py, cellZ, cellZ);
+        }
+      }
+    }
   }
 
   function hitTest(mx, my) {
     var step = (CELL * zoom) + (GAP * zoom);
     var col = Math.floor((mx + panX) / step);
     var row = Math.floor((my + panY) / step);
     if (col < 0 || col >= GRID_COLS || row < 0 || row >= GRID_ROWS) return -1;
     var idx = row * GRID_COLS + col;
     return idx < TOTAL ? idx : -1;
   }
 
+  function buildDesignPlacement(startIdx) {
+    if (!window.__designPlacement || startIdx < 0) return null;
+    var dp = window.__designPlacement;
+    var grid = dp.grid;
+    var startRow = Math.floor(startIdx / GRID_COLS);
+    var startCol = startIdx % GRID_COLS;
+    var patches = [];
+    var colors = [];
+    var conflict = false;
+
+    for (var r = 0; r < grid.length; r++) {
+      for (var c = 0; c < grid[r].length; c++) {
+        if (!grid[r][c]) continue;
+        var pr = startRow + r;
+        var pc = startCol + c;
+        if (pr >= GRID_ROWS || pc >= GRID_COLS) { conflict = true; break; }
+        var pidx = pr * GRID_COLS + pc;
+        if ((A[pidx] || 0) >= PV) { conflict = true; break; }
+        patches.push(pidx + 1);
+        colors.push(grid[r][c]);
+      }
+      if (conflict) break;
+    }
+
+    return { name: dp.name, conflict: conflict, patches: patches, colors: colors };
+  }
+
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
 
+  function findRandomUnclaimed(count) {
+    var pool = [];
+    for (var i = 0; i < TOTAL; i++) {
+      if ((A[i] || 0) < PV) pool.push(i);
+    }
+    for (var j = pool.length - 1; j > 0; j--) {
+      var k = Math.floor(Math.random() * (j + 1));
+      var tmp = pool[j]; pool[j] = pool[k]; pool[k] = tmp;
+    }
+    return pool.slice(0, count);
+  }
+
+  function findHeartPattern(startIdx, count) {
+    var row = Math.floor(startIdx / GRID_COLS);
+    var col = startIdx % GRID_COLS;
+    var offsets = [[0,1],[0,2],[1,0],[1,3],[2,0],[2,3],[3,1],[3,2],[4,2],[5,2],[6,1],[6,2],[6,3]];
+    var found = [];
+    for (var i = 0; i < offsets.length && found.length < count; i++) {
+      var nr = row + offsets[i][0];
+      var nc = col + offsets[i][1];
+      if (nr < 0 || nr >= GRID_ROWS || nc < 0 || nc >= GRID_COLS) continue;
+      var ni = nr * GRID_COLS + nc;
+      if ((A[ni] || 0) < PV) found.push(ni);
+    }
+    if (found.length < count) {
+      var nearby = findNearbyUnclaimed(startIdx, count - found.length);
+      for (var j = 0; j < nearby.length; j++) found.push(nearby[j]);
+    }
+    return found.slice(0, count);
+  }
+
+  function findPatternSquares(startIdx, count, pattern) {
+    if (pattern === 'random') return findRandomUnclaimed(count);
+    if (pattern === 'heart') return findHeartPattern(startIdx, count);
+    return findNearbyUnclaimed(startIdx, count);
+  }
+
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
+      if (Math.abs(e.clientX - dragStartX) > 3 || Math.abs(e.clientY - dragStartY) > 3) {
+        dragMoved = true;
+      }
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
+    dragMoved = false;
     dragStartX = e.clientX;
     dragStartY = e.clientY;
     panStartX = panX;
     panStartY = panY;
     canvas.style.cursor = 'grabbing';
     e.preventDefault();
   });
 
   window.addEventListener('mouseup', function(e) {
     if (!isDragging) return;
-    var dx = Math.abs(e.clientX - dragStartX);
-    var dy = Math.abs(e.clientY - dragStartY);
     isDragging = false;
     canvas.style.cursor = 'crosshair';
-    if (dx < 4 && dy < 4) {
-      var rect = canvas.getBoundingClientRect();
-      handleGridClick(hitTest(e.clientX - rect.left, e.clientY - rect.top));
-    }
+  });
+
+  canvas.addEventListener('click', function(e) {
+    if (dragMoved) return;
+    var rect = canvas.getBoundingClientRect();
+    handleGridClick(hitTest(e.clientX - rect.left, e.clientY - rect.top));
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
+  if (typeof TARGET_PATCH_IDX === 'number' && TARGET_PATCH_IDX >= 0) {
+    centerOnPatch(TARGET_PATCH_IDX);
+  }
 
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
+  var patternWrap = document.getElementById('modal-pattern-wrap');
+  var patternSelect = document.getElementById('modal-pattern');
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
@@ -698,50 +852,51 @@ JS = r"""
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
+    if (patternWrap) patternWrap.style.display = (numSq >= 5 || val >= 100) ? 'block' : 'none';
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
@@ -749,51 +904,51 @@ JS = r"""
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
-      autofillBtn.textContent = 'Auto-fill ' + remaining + ' nearby square' + (remaining > 1 ? 's' : '') + ' with random colors';
+      autofillBtn.textContent = 'Auto-fill ' + remaining + ' remaining square' + (remaining > 1 ? 's' : '') + ' using selected pattern';
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
@@ -825,228 +980,254 @@ JS = r"""
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
-      var nearby = findNearbyUnclaimed(currentIdx, remaining);
+      var pattern = patternSelect ? patternSelect.value : 'nearby';
+      var nearby = findPatternSquares(currentIdx, remaining, pattern);
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
+      var txnId = buildTxnId('patch');
       for (var i = 0; i < pickedPatches.length; i++) {
         payload.push({patch: pickedPatches[i].idx + 1, color: pickedPatches[i].color, amount: donationAmount / pickedPatches.length});
       }
       fetch(SCRIPT, {
         method: 'POST',
         mode: 'no-cors',
         headers: {'Content-Type': 'text/plain'},
-        body: JSON.stringify({patches: payload, totalAmount: donationAmount, name: donorName})
+        body: JSON.stringify({patches: payload, totalAmount: donationAmount, name: donorName, transaction_id: txnId, logged_at: new Date().toISOString()})
       }).then(function() {
-        var url = ZEFFY + '?patch=' + patches.join(',') + '&squares=' + pickedPatches.length + '&colors=' + colors.join(',') + '&donate=true';
+        var url = buildZeffyUrl({patch: patches.join(','), squares: pickedPatches.length, colors: colors.join(','), donate: 'true', amount: donationAmount});
         window.open(url, '_blank');
         closeModal();
       }).catch(function() {
-        var url = ZEFFY + '?patch=' + patches.join(',') + '&squares=' + pickedPatches.length + '&colors=' + colors.join(',') + '&donate=true';
+        var url = buildZeffyUrl({patch: patches.join(','), squares: pickedPatches.length, colors: colors.join(','), donate: 'true', amount: donationAmount});
         window.open(url, '_blank');
         closeModal();
       });
     } else {
-      var url = ZEFFY + '?patch=' + patches.join(',') + '&squares=' + pickedPatches.length + '&colors=' + colors.join(',') + '&donate=true';
+      var url = buildZeffyUrl({patch: patches.join(','), squares: pickedPatches.length, colors: colors.join(','), donate: 'true', amount: donationAmount});
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
-      var nearby = findNearbyUnclaimed(currentIdx, stillNeeded);
+      var pattern = patternSelect ? patternSelect.value : 'nearby';
+      var nearby = findPatternSquares(currentIdx, stillNeeded, pattern);
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
+      var txnId = buildTxnId('patch');
       for (var i = 0; i < pickedPatches.length; i++) {
         payload.push({patch: pickedPatches[i].idx + 1, color: pickedPatches[i].color, amount: donationAmount / pickedPatches.length});
       }
       fetch(SCRIPT, {
         method: 'POST',
         mode: 'no-cors',
         headers: {'Content-Type': 'text/plain'},
-        body: JSON.stringify({patches: payload, totalAmount: donationAmount, name: donorName})
+        body: JSON.stringify({patches: payload, totalAmount: donationAmount, name: donorName, transaction_id: txnId, logged_at: new Date().toISOString()})
       }).then(function() {
-        var url = ZEFFY + '?patch=' + patches.join(',') + '&squares=' + pickedPatches.length + '&colors=' + colors.join(',') + '&donate=true';
+        var url = buildZeffyUrl({patch: patches.join(','), squares: pickedPatches.length, colors: colors.join(','), donate: 'true', amount: donationAmount});
         window.open(url, '_blank');
         closeModal();
       }).catch(function() {
         /* Still open Zeffy even if sheet write fails */
-        var url = ZEFFY + '?patch=' + patches.join(',') + '&squares=' + pickedPatches.length + '&colors=' + colors.join(',') + '&donate=true';
+        var url = buildZeffyUrl({patch: patches.join(','), squares: pickedPatches.length, colors: colors.join(','), donate: 'true', amount: donationAmount});
         window.open(url, '_blank');
         closeModal();
       });
     } else {
-      var url = ZEFFY + '?patch=' + patches.join(',') + '&squares=' + pickedPatches.length + '&colors=' + colors.join(',') + '&donate=true';
+      var url = buildZeffyUrl({patch: patches.join(','), squares: pickedPatches.length, colors: colors.join(','), donate: 'true', amount: donationAmount});
       window.open(url, '_blank');
       closeModal();
     }
   });
 
   /* ------- Grid click (called from mouseup) ------- */
   function handleGridClick(idx) {
     if (idx < 0) return;
-    var claimed = (A[idx] || 0) >= PV;
-    if (claimed) return;
 
     /* Design placement mode */
     if (window.__designPlacement) {
-      var dp = window.__designPlacement;
-      var grid = dp.grid;
-      var designName = dp.name;
-      var startRow = Math.floor(idx / COLS);
-      var startCol = idx % COLS;
-      var patchList = [];
-      var colorList = [];
-      var conflict = false;
-
-      for (var r = 0; r < grid.length; r++) {
-        for (var c = 0; c < grid[r].length; c++) {
-          if (grid[r][c]) {
-            var pr = startRow + r;
-            var pc = startCol + c;
-            if (pr >= ROWS || pc >= COLS) { conflict = true; break; }
-            var pidx = pr * COLS + pc;
-            if ((A[pidx] || 0) >= PV) { conflict = true; break; }
-            patchList.push(pidx + 1);
-            colorList.push(encodeURIComponent(grid[r][c]));
-          }
-        }
-        if (conflict) break;
-      }
-
-      if (conflict) {
+      var placement = buildDesignPlacement(idx);
+      if (!placement) return;
+      if (placement.conflict) {
         alert('Design doesn\u2019t fit here \u2014 some patches overlap with claimed patches or the edge. Try another spot.');
         return;
       }
 
+      var designName = placement.name;
+      var designDonorName = window.__designPlacement && window.__designPlacement.donorName
+        ? window.__designPlacement.donorName
+        : (designName + ' Design');
+      var patchList = placement.patches;
+      var colorList = [];
+      for (var i = 0; i < placement.colors.length; i++) {
+        colorList.push(encodeURIComponent(placement.colors[i]));
+      }
+
       /* Preview the design on canvas */
       for (var i = 0; i < patchList.length; i++) {
         var pidx2 = patchList[i] - 1;
-        C[pidx2] = decodeURIComponent(colorList[i]);
+        COLORS[pidx2] = decodeURIComponent(colorList[i]);
         A[pidx2] = PV;
       }
       draw();
 
       /* Save to sheet */
-      var donorName = designName + ' Design';
+      var donorName = designDonorName;
       var totalAmt = patchList.length * PV;
       if (SCRIPT) {
         var payload = [];
+        var txnId = buildTxnId('design');
         for (var i = 0; i < patchList.length; i++) {
-          payload.push({patch: patchList[i], color: decodeURIComponent(colorList[i]), amount: PV});
+          payload.push({patch: patchList[i], color: decodeURIComponent(colorList[i]), amount: PV, name: donorName, design: designName});
         }
+        var checkoutUrl = buildZeffyUrl({
+          design: encodeURIComponent(designName),
+          donor: encodeURIComponent(designDonorName),
+          patch: patchList.join(','),
+          squares: patchList.length,
+          colors: colorList.join(','),
+          donate: 'true',
+          amount: totalAmt,
+          donation_amount: totalAmt,
+          suggested_amount: totalAmt
+        });
         fetch(SCRIPT, {
           method: 'POST', mode: 'no-cors',
           headers: {'Content-Type': 'text/plain'},
-          body: JSON.stringify({patches: payload, totalAmount: totalAmt, name: donorName})
+          body: JSON.stringify({
+            patches: payload,
+            totalAmount: totalAmt,
+            name: donorName,
+            design_name: designName,
+            patch_ids: patchList.join(','),
+            transaction_id: txnId,
+            logged_at: new Date().toISOString()
+          })
+        }).then(function() {
+          window.open(checkoutUrl, '_blank');
+        }).catch(function() {
+          window.open(checkoutUrl, '_blank');
         });
+      } else {
+        var checkoutUrl = buildZeffyUrl({
+          design: encodeURIComponent(designName),
+          donor: encodeURIComponent(designDonorName),
+          patch: patchList.join(','),
+          squares: patchList.length,
+          colors: colorList.join(','),
+          donate: 'true',
+          amount: totalAmt,
+          donation_amount: totalAmt,
+          suggested_amount: totalAmt
+        });
+        window.open(checkoutUrl, '_blank');
       }
 
-      /* Open Zeffy */
-      var url = ZEFFY + '?design=' + encodeURIComponent(designName) + '&patch=' + patchList.join(',') + '&squares=' + patchList.length + '&colors=' + colorList.join(',') + '&donate=true';
-      window.open(url, '_blank');
-
       /* Clear placement mode */
       window.__designPlacement = null;
       var banner = document.getElementById('design-place-banner');
       if (banner) banner.remove();
       return;
     }
 
+    var claimed = (A[idx] || 0) >= PV;
+    if (claimed) return;
+
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
@@ -1387,132 +1568,147 @@ GALLERY_JS = r"""
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
+    if (!overlay) return;
 
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
       'Choose where to place it, then you\u2019ll be redirected to complete your $' + cost.toLocaleString() + ' donation.';
+    var donorNameInput = document.getElementById('dd-donor-name');
+    if (donorNameInput) donorNameInput.value = '';
 
     /* Single CTA: Place on Quilt */
     var cta = document.getElementById('dd-cta');
     cta.href = '#';
     cta.textContent = 'Place on Quilt \u2192';
     cta.target = '';
     var newCta = cta.cloneNode(true);
     cta.parentNode.replaceChild(newCta, cta);
     newCta.addEventListener('click', function(e) {
       e.preventDefault();
-      window.__designPlacement = {name: d.name, grid: d.grid, cost: cost};
-      overlay.classList.remove('active');
+      var donorName = donorNameInput ? donorNameInput.value.trim() : '';
+      if (!donorName) {
+        alert('Please enter your name before placing this design.');
+        if (donorNameInput) donorNameInput.focus();
+        return;
+      }
+      window.__designPlacement = {name: d.name, grid: d.grid, cost: cost, donorName: donorName};
+      closeDesignDetail();
       /* Show placement banner */
       var old = document.getElementById('design-place-banner');
       if (old) old.remove();
       var banner = document.createElement('div');
       banner.id = 'design-place-banner';
       banner.style.cssText = 'position:fixed;top:0;left:0;right:0;z-index:10002;background:#277DA1;color:#fff;text-align:center;padding:12px 20px;font-family:DM Sans,sans-serif;font-size:.9rem;font-weight:500;display:flex;align-items:center;justify-content:center;gap:12px;box-shadow:0 2px 8px rgba(0,0,0,.2)';
       banner.innerHTML = 'Click on the quilt to place your <strong>' + d.name + '</strong> (' + d.px + ' patches \u00b7 $' + cost.toLocaleString() + ')';
       var cancelBtn = document.createElement('button');
       cancelBtn.textContent = 'Cancel';
       cancelBtn.style.cssText = 'background:rgba(255,255,255,.2);color:#fff;border:1px solid rgba(255,255,255,.4);padding:4px 14px;border-radius:4px;cursor:pointer;font-size:.8rem';
       cancelBtn.addEventListener('click', function() {
         window.__designPlacement = null;
         banner.remove();
       });
       banner.appendChild(cancelBtn);
       document.body.appendChild(banner);
       /* Scroll to quilt */
       var quiltCanvas = document.getElementById('quilt-canvas');
       if (quiltCanvas) quiltCanvas.scrollIntoView({behavior:'smooth', block:'start'});
+      if (window.parent && window.parent !== window) {
+        window.parent.postMessage({ type: 'streamlit:setFrameHeight', height: document.body.scrollHeight }, '*');
+      }
     });
 
     overlay.classList.add('active');
   }
 
   /* ── Close detail ── */
-  document.getElementById('design-detail-close').addEventListener('click', function() {
-    document.getElementById('design-detail-overlay').classList.remove('active');
-  });
+  function closeDesignDetail() {
+    var overlay = document.getElementById('design-detail-overlay');
+    if (overlay) overlay.classList.remove('active');
+  }
+  document.getElementById('design-detail-close').addEventListener('click', closeDesignDetail);
   document.getElementById('design-detail-overlay').addEventListener('click', function(e) {
-    if (e.target === this) this.classList.remove('active');
+    if (e.target === this) closeDesignDetail();
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
-    + f'"pctGoal":{pct_goal}'
+    + f'"pctGoal":{pct_goal},'
+    + f'"targetPatchIdx":{target_patch_idx}'
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
@@ -1586,63 +1782,75 @@ HTML = f"""<!DOCTYPE html>
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
+    <label class="dd-name-label" for="dd-donor-name">Your Name</label>
+    <input class="dd-name-input" id="dd-donor-name" type="text" placeholder="How your name should appear on the quilt">
     <a class="dd-cta" id="dd-cta" href="#">Place on Quilt &rarr;</a>
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
+
+      <div id="modal-pattern-wrap" style="display:none">
+        <label for="modal-pattern">Auto-fill Pattern</label>
+        <select id="modal-pattern" class="pattern-select">
+          <option value="nearby">Fill Nearby (Square)</option>
+          <option value="heart">Heart Shape</option>
+          <option value="random">Random Spread</option>
+        </select>
+      </div>
     </div>
 
     <div id="modal-picked-summary"></div>
 
     <label>Choose Your Color</label>
     <div id="modal-color-area"></div>
 
     <button class="donate-submit" id="modal-autofill-btn" style="display:none">Auto-fill nearby squares with random colors</button>
     <button class="donate-submit" id="modal-next-btn" style="display:none">Select Next Square &rarr;</button>
     <button class="donate-submit" id="modal-donate-btn">Donate &amp; Claim &rarr;</button>
+    <p style="font-size:.72rem;color:#4a5c5a;margin-top:.8rem;line-height:1.45">Patch IDs and colors are logged to our quilt sheet automatically when you continue to Zeffy.</p>
   </div>
 </div>
 
 <div id="tip"></div>
 <script>{JS}</script>
 <script>{GALLERY_JS}</script>
 </body>
 </html>"""
 
 st.components.v1.html(HTML, height=900, scrolling=True)
