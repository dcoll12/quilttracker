"""
Pre-made pixel art designs for quilt donations.
Each design is a small, recognizable icon people can buy as a bundle.
$20 per patch. Designs range from $120 to $600+.
"""
from PIL import Image, ImageDraw

COLS = 250
PATCH_VALUE = 20

T = None

# Quilt palette
RED    = "#F94144"
ORANGE = "#F3722C"
AMBER  = "#F8961E"
PEACH  = "#F9844A"
YELLOW = "#F9C74F"
GREEN  = "#90BE6D"
TEAL   = "#43AA8B"
DTEAL  = "#4D908E"
SLATE  = "#577590"
BLUE   = "#277DA1"
WHITE  = "#FFFFFF"
BLACK  = "#333333"
PINK   = "#FF69B4"
PURPLE = "#9B59B6"
LPURP  = "#DDA0DD"

designs = {}

# ─── 1. MINI HEART (12 patches = $240) ───
designs["Mini Heart"] = {
    "color": RED,
    "grid": [
        [T, RED,  T, T, RED,  T],
        [RED,RED,RED,RED,RED,RED],
        [RED,RED,RED,RED,RED,RED],
        [T, RED,RED,RED,RED, T],
        [T, T, RED,RED, T,  T],
        [T, T, T, RED, T,  T],
    ]
}

# ─── 2. PEACE SIGN (24 patches = $480) ───
designs["Peace Sign"] = {
    "grid": [
        [T,    T,    TEAL, TEAL, TEAL, T,    T],
        [T,    TEAL, T,    TEAL, T,    TEAL, T],
        [TEAL, T,    T,    TEAL, T,    T,    TEAL],
        [TEAL, T,    TEAL, TEAL, TEAL, T,    TEAL],
        [TEAL, T,    T,    TEAL, T,    T,    TEAL],
        [T,    TEAL, T,    TEAL, T,    TEAL, T],
        [T,    T,    TEAL, TEAL, TEAL, T,    T],
    ]
}

# ─── 3. DAISY FLOWER (13 patches = $260) ───
designs["Daisy"] = {
    "grid": [
        [T,      YELLOW, T,      YELLOW, T],
        [YELLOW, T,      AMBER,  T,      YELLOW],
        [T,      AMBER,  AMBER,  AMBER,  T],
        [YELLOW, T,      AMBER,  T,      YELLOW],
        [T,      YELLOW, T,      YELLOW, T],
        [T,      T,      GREEN,  T,      T],
    ]
}

# ─── 4. STAR (13 patches = $260) ───
designs["Star"] = {
    "grid": [
        [T,      T,      YELLOW, T,      T],
        [T,      YELLOW, YELLOW, YELLOW, T],
        [YELLOW, YELLOW, AMBER,  YELLOW, YELLOW],
        [T,      YELLOW, YELLOW, YELLOW, T],
        [T,      T,      YELLOW, T,      T],
    ]
}

# ─── 5. SMILEY FACE (16 patches = $320) ───
designs["Smiley"] = {
    "grid": [
        [T,      YELLOW, YELLOW, YELLOW, YELLOW, T],
        [YELLOW, YELLOW, YELLOW, YELLOW, YELLOW, YELLOW],
        [YELLOW, BLACK,  YELLOW, YELLOW, BLACK,  YELLOW],
        [YELLOW, YELLOW, YELLOW, YELLOW, YELLOW, YELLOW],
        [YELLOW, BLACK,  YELLOW, YELLOW, BLACK,  YELLOW],
        [T,      YELLOW, BLACK,  BLACK,  YELLOW, T],
    ]
}

# ─── 6. PAW PRINT (11 patches = $220) ───
designs["Paw Print"] = {
    "grid": [
        [T,     BLACK, T,     BLACK, T],
        [BLACK, T,     T,     T,     BLACK],
        [T,     BLACK, BLACK, BLACK, T],
        [T,     BLACK, BLACK, BLACK, T],
    ]
}

# ─── 7. MUSIC NOTE (8 patches = $160) ───
designs["Music Note"] = {
    "grid": [
        [T,     T,     SLATE],
        [T,     T,     SLATE],
        [T,     T,     SLATE],
        [T,     T,     SLATE],
        [SLATE, SLATE, SLATE],
        [SLATE, SLATE, T],
    ]
}

# ─── 8. LIGHTNING BOLT (9 patches = $180) ───
designs["Lightning"] = {
    "grid": [
        [T,      T,      YELLOW],
        [T,      YELLOW, YELLOW],
        [T,      YELLOW, T],
        [YELLOW, YELLOW, YELLOW],
        [YELLOW, YELLOW, T],
        [YELLOW, T,      T],
    ]
}

# ─── 9. CRESCENT MOON (10 patches = $200) ───
designs["Moon"] = {
    "grid": [
        [T,      YELLOW, YELLOW, T],
        [YELLOW, YELLOW, T,      T],
        [YELLOW, T,      T,      T],
        [YELLOW, T,      T,      T],
        [YELLOW, YELLOW, T,      T],
        [T,      YELLOW, YELLOW, T],
    ]
}

# ─── 10. BUTTERFLY (18 patches = $360) ───
designs["Butterfly"] = {
    "grid": [
        [LPURP, T,     T,     T,     LPURP],
        [LPURP, PINK,  T,     PINK,  LPURP],
        [LPURP, PINK, BLACK,  PINK,  LPURP],
        [LPURP, T,    BLACK,  T,     LPURP],
        [T,     T,    BLACK,  T,     T],
    ]
}

# ─── 11. ANCHOR (12 patches = $240) ───
designs["Anchor"] = {
    "grid": [
        [T,    T,    BLUE, T,    T],
        [T,    BLUE, BLUE, BLUE, T],
        [T,    T,    BLUE, T,    T],
        [T,    T,    BLUE, T,    T],
        [BLUE, T,    BLUE, T,    BLUE],
        [T,    BLUE, BLUE, BLUE, T],
    ]
}

# ─── 12. RAINBOW (15 patches = $300) ───
designs["Rainbow"] = {
    "grid": [
        [T,      RED,    RED,    RED,    T],
        [RED,    ORANGE, ORANGE, ORANGE, RED],
        [ORANGE, YELLOW, T,      YELLOW, ORANGE],
        [YELLOW, GREEN,  T,      GREEN,  YELLOW],
    ]
}

# ─── 13. CROWN (14 patches = $280) ───
designs["Crown"] = {
    "grid": [
        [T,      YELLOW, T,      YELLOW, T,      YELLOW, T],
        [T,      YELLOW, YELLOW, YELLOW, YELLOW, YELLOW, T],
        [YELLOW, YELLOW, AMBER,  YELLOW, AMBER,  YELLOW, YELLOW],
        [YELLOW, YELLOW, YELLOW, YELLOW, YELLOW, YELLOW, YELLOW],
    ]
}

# ─── 14. DIAMOND GEM (8 patches = $160) ───
designs["Diamond"] = {
    "grid": [
        [T,    T,    BLUE, T,    T],
        [T,    BLUE, BLUE, BLUE, T],
        [BLUE, BLUE, BLUE, BLUE, BLUE],
    ]
}

# ─── 15. ALIEN (14 patches = $280) ───
designs["Alien"] = {
    "grid": [
        [T,     GREEN, GREEN, GREEN, T],
        [GREEN, GREEN, GREEN, GREEN, GREEN],
        [GREEN, BLACK, GREEN, BLACK, GREEN],
        [T,     GREEN, GREEN, GREEN, T],
        [T,     T,     GREEN, T,     T],
    ]
}

# ─── 16. CHERRY (10 patches = $200) ───
designs["Cherry"] = {
    "grid": [
        [T,   T,   T,   T,   GREEN],
        [T,   T,   T,   GREEN, T],
        [T,   T,   GREEN, T,   T],
        [RED,  T,  T,    RED,  T],
        [RED, RED, T,    RED, RED],
    ]
}

# ─── 17. CACTUS (11 patches = $220) ───
designs["Cactus"] = {
    "grid": [
        [T,     T,     GREEN, T,     T],
        [T,     T,     GREEN, T,     T],
        [GREEN, T,     GREEN, T,     GREEN],
        [GREEN, GREEN, GREEN, GREEN, GREEN],
        [T,     T,     GREEN, T,     T],
    ]
}

# ─── 18. SUN (16 patches = $320) ───
designs["Sun"] = {
    "grid": [
        [T,      YELLOW, T,      YELLOW, T],
        [YELLOW, AMBER,  AMBER,  AMBER,  YELLOW],
        [T,      AMBER,  YELLOW, AMBER,  T],
        [YELLOW, AMBER,  AMBER,  AMBER,  YELLOW],
        [T,      YELLOW, T,      YELLOW, T],
    ]
}

# ─── 19. CLOUD (10 patches = $200) ───
designs["Cloud"] = {
    "grid": [
        [T,     T,     WHITE, WHITE, T,     T],
        [T,     WHITE, WHITE, WHITE, WHITE, T],
        [WHITE, WHITE, WHITE, WHITE, WHITE, WHITE],
    ]
}

# ─── 20. TREE (9 patches = $180) ───
designs["Tree"] = {
    "grid": [
        [T,    T,    GREEN, T,     T],
        [T,    GREEN, GREEN, GREEN, T],
        [GREEN, GREEN, GREEN, GREEN, GREEN],
        [T,    T,    AMBER, T,     T],
    ]
}


def hex_to_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def count(grid):
    return sum(1 for row in grid for c in row if c is not None)

def get_patch(start_patch, r, c):
    idx = start_patch - 1
    base_row = idx // COLS
    base_col = idx % COLS
    return (base_row + r) * COLS + (base_col + c) + 1

# Generate all images and tables
print("=" * 60)
print("  QUILT DONATION DESIGN MENU")
print(f"  ${PATCH_VALUE} per patch")
print("=" * 60)

for name, d in designs.items():
    grid = d["grid"]
    px = count(grid)
    cost = px * PATCH_VALUE
    rows = len(grid)
    cols = max(len(r) for r in grid)

    # Generate image
    ps = min(16, 250 // max(rows, cols))
    w, h = cols * ps, rows * ps
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    for r, row in enumerate(grid):
        for c, color in enumerate(row):
            if color:
                rgb = hex_to_rgb(color)
                draw.rectangle([c*ps, r*ps, (c+1)*ps-1, (r+1)*ps-1], fill=rgb+(255,))
    fname = f"/home/user/quilttracker/design_{name.lower().replace(' ', '_')}.png"
    img.save(fname)

    # Print info
    print(f"\n{'─' * 60}")
    print(f"  {name}")
    print(f"  {cols}×{rows} | {px} patches | ${cost}")
    print(f"  Image: {fname}")

    # Patch table starting at patch 1 (placeholder - user picks start)
    START = 3098
    print(f"\n  | Patch # | Color |")
    print(f"  |---------|-------|")
    for r, row in enumerate(grid):
        for c, color in enumerate(row):
            if color:
                pnum = get_patch(START, r, c)
                print(f"  | {pnum} | {color} |")

print(f"\n{'=' * 60}")
total_designs = len(designs)
print(f"  {total_designs} designs available")
print("=" * 60)
