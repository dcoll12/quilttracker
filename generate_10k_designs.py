"""
$10,000-tier pixel art designs (~500 patches each at $20/patch).
Rocky (Project Hail Mary), Beach Scene, Log Cabin & Lone Star Quilt Patterns.
"""
from PIL import Image, ImageDraw
import math

COLS = 250
PATCH_VALUE = 20
T = None

# ─── PALETTE ───────────────────────────────────────────────────
RED    = "#F94144"; ORANGE = "#F3722C"; AMBER  = "#F8961E"
PEACH  = "#F9844A"; YELLOW = "#F9C74F"; GREEN  = "#90BE6D"
TEAL   = "#43AA8B"; DTEAL  = "#4D908E"; SLATE  = "#577590"
BLUE   = "#277DA1"; WHITE  = "#FFFFFF"; BLACK  = "#333333"
PINK   = "#FF69B4"; PURPLE = "#9B59B6"; LPURP  = "#DDA0DD"
DGREEN = "#1A6B3C"; MGREEN = "#3E8B57"; LGREEN = "#7EC87E"
VLGRN  = "#B5E6A3"; BROWN  = "#8B4513"; LBROWN = "#D2691E"
TAN    = "#DEB887"; GRAY   = "#999999"; LGRAY  = "#CCCCCC"
SKYBL  = "#87CEEB"; CORAL  = "#FF7F50"; MAROON = "#8B0000"
NAVY   = "#1B3A5C"; GOLD   = "#DAA520"; DBLUE  = "#1E5FA8"
LBLUE  = "#5BA3CF"; SAND   = "#F5DEB3"; DGRAY  = "#555555"

# ─── HELPERS ───────────────────────────────────────────────────
def count(grid):
    return sum(1 for row in grid for c in row if c is not None)

def hex_to_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def px(g, r, c, color):
    if 0 <= r < len(g) and 0 <= c < len(g[0]):
        g[r][c] = color

def fill_rect(g, r1, c1, r2, c2, color):
    for r in range(max(0, r1), min(len(g), r2 + 1)):
        for c in range(max(0, c1), min(len(g[0]), c2 + 1)):
            g[r][c] = color

designs = {}

# ═══════════════════════════════════════════════════════════════
# 1. ROCKY from Project Hail Mary (~500 patches)
#    Five-limbed Eridian alien, rocky/mineral body, pentapod
#    "Amaze!" - communicates through musical vibrations
# ═══════════════════════════════════════════════════════════════
def make_rocky():
    W, H = 38, 32
    g = [[T] * W for _ in range(H)]
    cy, cx = 15, 18
    body_rx, body_ry = 13.0, 9.5

    # ── Arms (drawn first, body overlays inner portions) ──
    # 5 arms at 72deg intervals (pentagonal symmetry like a starfish)
    arm_angles_deg = [90, 18, -54, -126, 162]
    arm_length = 15.5
    arm_start = 4.0  # distance from center where arm drawing begins

    for angle_deg in arm_angles_deg:
        a = math.radians(angle_deg)
        sa, ca = math.sin(a), math.cos(a)
        perp_r, perp_c = ca, sa  # perpendicular direction

        for d10 in range(int(arm_start * 10), int(arm_length * 10) + 1):
            d = d10 / 10.0
            r_f = cy - d * sa
            c_f = cx + d * ca

            # Taper: 3.0 near body -> 1.0 at tip
            progress = (d - arm_start) / (arm_length - arm_start)
            hw = 3.2 * (1.0 - progress * 0.65)

            for w10 in range(-35, 36):
                w = w10 / 10.0
                if abs(w) > hw:
                    continue
                pr = int(round(r_f + w * perp_r))
                pc = int(round(c_f + w * perp_c))
                frac = abs(w) / hw if hw > 0 else 0
                if frac < 0.3:
                    color = TAN
                elif frac < 0.65:
                    color = LBROWN
                else:
                    color = BROWN
                px(g, pr, pc, color)

            # Joint bands (darker rings on limbs)
            if 0.35 < progress < 0.42 or 0.65 < progress < 0.72:
                for w10 in range(-30, 31):
                    w = w10 / 10.0
                    if abs(w) <= hw:
                        pr = int(round(r_f + w * perp_r))
                        pc = int(round(c_f + w * perp_c))
                        px(g, pr, pc, GRAY)

        # Rounded arm tips
        tip_r = cy - arm_length * sa
        tip_c = cx + arm_length * ca
        px(g, int(round(tip_r)), int(round(tip_c)), DGRAY)
        # Slightly wider tip
        px(g, int(round(tip_r)), int(round(tip_c)) + 1, BROWN)
        px(g, int(round(tip_r)) + 1, int(round(tip_c)), BROWN)

    # ── Central body - layered ovals for depth ──
    for r in range(H):
        for c in range(W):
            dx = (c - cx) / body_rx
            dy = (r - cy) / body_ry
            d2 = dx * dx + dy * dy
            if d2 <= 1.0:
                g[r][c] = BROWN
            if d2 <= 0.72:
                g[r][c] = LBROWN
            if d2 <= 0.42:
                g[r][c] = TAN
            if d2 <= 0.18:
                g[r][c] = AMBER

    # Body surface texture - mineral spots and ridges
    spots = [(11, 13), (12, 21), (15, 15), (17, 19), (13, 11),
             (14, 23), (18, 17), (11, 18), (17, 13), (12, 16),
             (16, 22), (13, 25), (18, 14), (10, 20), (19, 18)]
    for r, c in spots:
        px(g, r, c, BROWN)

    # Subtle ridge lines across body
    for c in range(cx - 8, cx + 9):
        if 0 <= c < W:
            if g[cy - 3][c] == TAN:
                px(g, cy - 3, c, LBROWN)
            if g[cy + 3][c] == TAN:
                px(g, cy + 3, c, LBROWN)

    # Faint ring pattern on body (like mineral striations)
    for r in range(H):
        for c in range(W):
            dx = (c - cx) / body_rx
            dy = (r - cy) / body_ry
            d2 = dx * dx + dy * dy
            if 0.28 < d2 < 0.32 and g[r][c] == TAN:
                g[r][c] = LBROWN

    return g


# ═══════════════════════════════════════════════════════════════
# 2. BEACH SUNSET (~500 patches)
#    Tropical sunset beach with palm tree, ocean, and sand
# ═══════════════════════════════════════════════════════════════
def make_beach():
    W, H = 28, 19
    g = [[T] * W for _ in range(H)]

    # ── Sky (rows 0-6) ──
    sky_colors = [SKYBL, SKYBL, LBLUE, LBLUE, PEACH, CORAL, ORANGE]
    for r in range(7):
        for c in range(W):
            g[r][c] = sky_colors[r]

    # Clouds
    cloud_pixels = [(0, 8), (0, 9), (0, 10), (0, 11),
                    (0, 17), (0, 18), (0, 19), (0, 20),
                    (1, 9), (1, 10), (1, 18), (1, 19)]
    for r, c in cloud_pixels:
        px(g, r, c, WHITE)

    # Sun (upper right, centered at row 2, col 24)
    sun_cy, sun_cx = 2, 24
    for r in range(H):
        for c in range(W):
            dist = math.sqrt((c - sun_cx) ** 2 + (r - sun_cy) ** 2)
            if dist <= 2.6:
                g[r][c] = YELLOW
            if dist <= 1.6:
                g[r][c] = AMBER

    # Sun rays (a few accent pixels)
    ray_pixels = [(0, 22), (0, 26), (4, 22), (4, 27)]
    for r, c in ray_pixels:
        px(g, r, c, YELLOW)

    # ── Ocean (rows 7-12) ──
    ocean_colors = [DBLUE, DBLUE, BLUE, BLUE, LBLUE, SKYBL]
    for r in range(7, 13):
        for c in range(W):
            g[r][c] = ocean_colors[r - 7]

    # Wave crests
    for c in range(0, W, 4):
        px(g, 8, c, WHITE)
        px(g, 8, c + 1, WHITE)
    for c in range(2, W, 5):
        px(g, 10, c, WHITE)
        if c + 1 < W:
            px(g, 10, c + 1, WHITE)

    # Sunset reflection on water
    for r in [7, 8]:
        px(g, r, 24, AMBER)
        px(g, r, 23, PEACH)
        px(g, r, 25, PEACH)

    # ── Shoreline ──
    for c in range(W):
        g[13][c] = WHITE  # foam line

    # ── Beach (rows 14-18) ──
    for c in range(W):
        g[14][c] = TAN  # wet sand
    for r in range(15, 19):
        for c in range(W):
            g[r][c] = SAND

    # ── Palm tree ──
    # Trunk (slight lean to the right)
    trunk_pixels = [
        (14, 5), (14, 6),
        (13, 5), (13, 6),
        (12, 5), (12, 6),
        (11, 5), (11, 6),
        (10, 4), (10, 5),
        (9, 4), (9, 5),
        (8, 4), (8, 5),
        (7, 3), (7, 4),
        (6, 3), (6, 4),
    ]
    for r, c in trunk_pixels:
        px(g, r, c, BROWN)
        # Light side of trunk
        if c == max(cc for rr, cc in trunk_pixels if rr == r):
            px(g, r, c, LBROWN)

    # Coconuts
    px(g, 6, 4, BROWN)
    px(g, 6, 5, LBROWN)

    # Palm fronds
    frond_pixels = [
        # Right fronds (long, drooping)
        (5, 4, DGREEN), (5, 5, GREEN), (5, 6, GREEN), (5, 7, GREEN), (5, 8, DGREEN),
        (4, 5, GREEN), (4, 6, GREEN), (4, 7, GREEN), (4, 8, GREEN), (4, 9, GREEN), (4, 10, DGREEN),
        (3, 7, GREEN), (3, 8, GREEN), (3, 9, GREEN), (3, 10, GREEN), (3, 11, DGREEN),
        (6, 6, DGREEN), (6, 7, GREEN), (6, 8, GREEN), (6, 9, GREEN), (6, 10, DGREEN),
        (7, 8, DGREEN), (7, 9, GREEN), (7, 10, DGREEN),
        # Left fronds
        (5, 3, GREEN), (5, 2, GREEN), (5, 1, DGREEN),
        (4, 3, GREEN), (4, 2, GREEN), (4, 1, DGREEN), (4, 0, DGREEN),
        (3, 3, GREEN), (3, 2, GREEN), (3, 1, DGREEN),
        (6, 2, DGREEN), (6, 1, DGREEN),
        # Upward fronds
        (2, 4, GREEN), (2, 5, GREEN), (2, 6, DGREEN),
        (2, 3, GREEN), (2, 2, DGREEN),
        (1, 3, DGREEN), (1, 4, GREEN), (1, 5, DGREEN),
    ]
    for r, c, color in frond_pixels:
        px(g, r, c, color)

    # ── Beach details ──
    px(g, 16, 13, CORAL)  # starfish
    px(g, 16, 14, CORAL)
    px(g, 17, 13, CORAL)
    px(g, 17, 14, CORAL)
    px(g, 16, 21, LGRAY)  # shell
    px(g, 17, 22, PINK)   # shell
    px(g, 18, 9, LGRAY)   # pebble

    # Footprints in sand
    px(g, 16, 17, TAN)
    px(g, 17, 18, TAN)
    px(g, 18, 17, TAN)

    return g


# ═══════════════════════════════════════════════════════════════
# 3. LOG CABIN QUILT BLOCK (~484 patches)
#    Traditional quilt pattern - warm and cool halves spiral
#    from a center "hearth" square
# ═══════════════════════════════════════════════════════════════
def make_log_cabin():
    S = 22
    g = [[LGRAY] * S for _ in range(S)]

    # Color families
    warm = [RED, CORAL, ORANGE, PEACH, AMBER, YELLOW]
    cool = [NAVY, DBLUE, BLUE, TEAL, DTEAL, SLATE]

    # Center hearth (2x2 red)
    hx, hy = S // 2 - 1, S // 2 - 1  # (10, 10)
    g[hy][hx] = RED
    g[hy][hx + 1] = ORANGE
    g[hy + 1][hx] = ORANGE
    g[hy + 1][hx + 1] = AMBER

    # Spiral outward: each round adds strips on right, top, left, bottom
    top = hy - 1
    bottom = hy + 2
    left = hx - 1
    right = hx + 2
    layer = 0

    while top >= 0 or bottom < S or left >= 0 or right < S:
        wi = layer % len(warm)
        ci = layer % len(cool)

        # Right strip (warm)
        if right < S:
            for r in range(max(0, top + 1), min(S, bottom)):
                g[r][right] = warm[wi]
            right += 1

        # Top strip (warm)
        if top >= 0:
            for c in range(max(0, left + 1), min(S, right)):
                g[top][c] = warm[(wi + 1) % len(warm)]
            top -= 1

        # Left strip (cool)
        if left >= 0:
            for r in range(max(0, top + 1), min(S, bottom)):
                g[r][left] = cool[ci]
            left -= 1

        # Bottom strip (cool)
        if bottom < S:
            for c in range(max(0, left + 1), min(S, right)):
                g[bottom][c] = cool[(ci + 1) % len(cool)]
            bottom += 1

        layer += 1
        if layer > 20:
            break

    return g


# ═══════════════════════════════════════════════════════════════
# 4. LONE STAR QUILT BLOCK (~484 patches)
#    Classic 8-pointed star with graduated color bands
# ═══════════════════════════════════════════════════════════════
def make_lone_star():
    S = 22
    g = [[T] * S for _ in range(S)]
    cx = (S - 1) / 2.0
    cy = (S - 1) / 2.0

    # Star color bands (center outward)
    bands = [RED, ORANGE, AMBER, YELLOW]
    bg_color = SAND

    # Fill background
    for r in range(S):
        for c in range(S):
            g[r][c] = bg_color

    # 8-pointed star = union of diamond (|dx|+|dy| <= R1)
    #                  and square (max(|dx|,|dy|) <= R2)
    # With R1 > R2, this creates 4 cardinal points from the diamond
    # and 4 diagonal points from the square corners
    R_diamond = 10.0
    R_square = 7.0

    for r in range(S):
        for c in range(S):
            dx = c - cx
            dy = r - cy
            manhattan = abs(dx) + abs(dy)
            chebyshev = max(abs(dx), abs(dy))
            dist = math.sqrt(dx * dx + dy * dy)

            in_diamond = manhattan <= R_diamond
            in_square = chebyshev <= R_square
            in_star = in_diamond or in_square

            if in_star:
                band_idx = min(int(dist / 2.8), len(bands) - 1)
                g[r][c] = bands[band_idx]

    # Setting triangles and corner squares (traditional lone star border)
    for r in range(S):
        for c in range(S):
            if g[r][c] == bg_color:
                dx = abs(c - cx)
                dy = abs(r - cy)
                # Corner squares
                if dx > 8 and dy > 8:
                    g[r][c] = TEAL
                else:
                    g[r][c] = DTEAL

    return g


# ═══════════════════════════════════════════════════════════════
# BUILD DESIGNS
# ═══════════════════════════════════════════════════════════════

designs["Rocky (Eridian)"] = {
    "desc": "Rocky from Project Hail Mary - five-limbed Eridian friend",
    "grid": make_rocky(),
}

designs["Beach Sunset"] = {
    "desc": "Tropical sunset beach with palm tree and ocean",
    "grid": make_beach(),
}

designs["Log Cabin Quilt"] = {
    "desc": "Traditional log cabin quilt block - warm & cool spiral",
    "grid": make_log_cabin(),
}

designs["Lone Star Quilt"] = {
    "desc": "Classic 8-pointed lone star quilt pattern",
    "grid": make_lone_star(),
}


# ═══════════════════════════════════════════════════════════════
# RENDER PNGs AND PRINT INFO
# ═══════════════════════════════════════════════════════════════

print("=" * 60)
print("  $10,000-TIER QUILT DESIGNS")
print(f"  ${PATCH_VALUE} per patch")
print("=" * 60)

for name, d in designs.items():
    grid = d["grid"]
    px_count = count(grid)
    cost = px_count * PATCH_VALUE
    rows = len(grid)
    cols = max(len(r) for r in grid)

    # Generate PNG
    ps = min(10, 250 // max(rows, cols))
    ps = max(ps, 4)
    w, h = cols * ps, rows * ps
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    for r_idx, row in enumerate(grid):
        for c_idx, color in enumerate(row):
            if color:
                rgb = hex_to_rgb(color)
                draw.rectangle(
                    [c_idx * ps, r_idx * ps, (c_idx + 1) * ps - 1, (r_idx + 1) * ps - 1],
                    fill=rgb + (255,),
                )
    safe_name = name.lower().replace(" ", "_").replace("(", "").replace(")", "")
    fname = f"/home/user/quilttracker/10k_{safe_name}.png"
    img.save(fname)

    print(f"\n{'─' * 60}")
    print(f"  {name} -- {d['desc']}")
    print(f"  {cols}x{rows} | {px_count} patches | ${cost:,}")

print(f"\n{'=' * 60}")
print("  PRICE LIST")
print("=" * 60)
for name, d in sorted(designs.items(), key=lambda x: count(x[1]["grid"])):
    px_count = count(d["grid"])
    cost = px_count * PATCH_VALUE
    print(f"  {name:<20} {px_count:>4} patches   ${cost:>7,}")
print("=" * 60)
