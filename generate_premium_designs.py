"""
Premium pixel art designs for large donations.
$20/patch. Designs from $1,000 to $5,000+.
"""
from PIL import Image, ImageDraw

COLS = 250
PATCH_VALUE = 20
T = None

# Palette
RED    = "#F94144"; ORANGE = "#F3722C"; AMBER  = "#F8961E"
PEACH  = "#F9844A"; YELLOW = "#F9C74F"; GREEN  = "#90BE6D"
TEAL   = "#43AA8B"; DTEAL  = "#4D908E"; SLATE  = "#577590"
BLUE   = "#277DA1"; WHITE  = "#FFFFFF"; BLACK  = "#333333"
PINK   = "#FF69B4"; PURPLE = "#9B59B6"; LPURP  = "#DDA0DD"
DGREEN = "#1A6B3C"; MGREEN = "#3E8B57"; LGREEN = "#7EC87E"
VLGRN  = "#B5E6A3"; BROWN  = "#8B4513"; LBROWN = "#D2691E"
TAN    = "#DEB887"; GRAY   = "#999999"; LGRAY  = "#CCCCCC"
SKYBL  = "#87CEEB"; CORAL  = "#FF7F50"; MAROON = "#8B0000"

designs = {}

# ─── 1. OWL (16×16, ~130 patches = $2,600) ───
designs["Owl"] = {
    "desc": "Wise owl perched",
    "grid": [
        [T,     T,     T,     T,     BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, T,     T,     T,     T],
        [T,     T,     T,     BROWN, LBROWN,LBROWN,LBROWN,LBROWN,LBROWN,LBROWN,LBROWN,LBROWN,BROWN, T,     T,     T],
        [T,     T,     BROWN, LBROWN,LBROWN,LBROWN,LBROWN,LBROWN,LBROWN,LBROWN,LBROWN,LBROWN,LBROWN,BROWN, T,     T],
        [T,     BROWN, LBROWN,BROWN, BROWN, BROWN, LBROWN,LBROWN,LBROWN,BROWN, BROWN, BROWN, LBROWN,BROWN, T,     T],
        [T,     BROWN, BROWN, WHITE, WHITE, BROWN, LBROWN,LBROWN,LBROWN,BROWN, WHITE, WHITE, BROWN, BROWN, T,     T],
        [T,     BROWN, BROWN, WHITE, BLACK, BROWN, TAN,   TAN,   TAN,   BROWN, BLACK, WHITE, BROWN, BROWN, T,     T],
        [T,     T,     BROWN, BROWN, BROWN, LBROWN,LBROWN,AMBER, LBROWN,LBROWN,BROWN, BROWN, BROWN, T,     T,     T],
        [T,     T,     T,     BROWN, LBROWN,LBROWN,AMBER, AMBER, AMBER, LBROWN,LBROWN,BROWN, T,     T,     T,     T],
        [T,     T,     BROWN, LBROWN,LBROWN,TAN,   TAN,   TAN,   TAN,   TAN,   LBROWN,LBROWN,BROWN, T,     T,     T],
        [T,     T,     BROWN, LBROWN,TAN,   TAN,   TAN,   TAN,   TAN,   TAN,   TAN,   LBROWN,BROWN, T,     T,     T],
        [T,     BROWN, LBROWN,LBROWN,TAN,   TAN,   TAN,   TAN,   TAN,   TAN,   TAN,   LBROWN,LBROWN,BROWN, T,     T],
        [T,     BROWN, LBROWN,LBROWN,TAN,   LBROWN,TAN,   TAN,   TAN,   LBROWN,TAN,   LBROWN,LBROWN,BROWN, T,     T],
        [T,     T,     BROWN, LBROWN,LBROWN,LBROWN,TAN,   TAN,   TAN,   LBROWN,LBROWN,LBROWN,BROWN, T,     T,     T],
        [T,     T,     T,     BROWN, BROWN, LBROWN,LBROWN,LBROWN,LBROWN,LBROWN,BROWN, BROWN, T,     T,     T,     T],
        [T,     T,     T,     T,     BROWN, BROWN, T,     T,     T,     BROWN, BROWN, T,     T,     T,     T,     T],
        [T,     T,     T,     T,     BROWN, BROWN, T,     T,     T,     BROWN, BROWN, T,     T,     T,     T,     T],
    ]
}

# ─── 2. CORGI (16×14, ~140 patches = $2,800) ───
designs["Corgi"] = {
    "desc": "Cute corgi butt",
    "grid": [
        [T,     T,     T,     AMBER, AMBER, T,     T,     T,     T,     T,     T,     AMBER, AMBER, T,     T,     T],
        [T,     T,     AMBER, AMBER, AMBER, AMBER, T,     T,     T,     T,     AMBER, AMBER, AMBER, AMBER, T,     T],
        [T,     T,     AMBER, PEACH, AMBER, AMBER, AMBER, AMBER, AMBER, AMBER, AMBER, AMBER, PEACH, AMBER, T,     T],
        [T,     AMBER, AMBER, AMBER, AMBER, AMBER, AMBER, AMBER, AMBER, AMBER, AMBER, AMBER, AMBER, AMBER, AMBER, T],
        [T,     AMBER, AMBER, AMBER, AMBER, WHITE, WHITE, WHITE, WHITE, WHITE, WHITE, AMBER, AMBER, AMBER, AMBER, T],
        [T,     AMBER, AMBER, BLACK, AMBER, WHITE, WHITE, WHITE, WHITE, WHITE, WHITE, AMBER, BLACK, AMBER, AMBER, T],
        [T,     AMBER, AMBER, AMBER, AMBER, WHITE, WHITE, WHITE, WHITE, WHITE, WHITE, AMBER, AMBER, AMBER, AMBER, T],
        [T,     T,     AMBER, AMBER, WHITE, WHITE, WHITE, BLACK, BLACK, WHITE, WHITE, WHITE, AMBER, AMBER, T,     T],
        [T,     T,     AMBER, AMBER, WHITE, WHITE, BLACK, T,     BLACK, WHITE, WHITE, WHITE, AMBER, AMBER, T,     T],
        [T,     T,     AMBER, AMBER, WHITE, PINK,  WHITE, WHITE, WHITE, PINK,  WHITE, WHITE, AMBER, AMBER, T,     T],
        [T,     T,     T,     AMBER, AMBER, WHITE, WHITE, WHITE, WHITE, WHITE, WHITE, AMBER, AMBER, T,     T,     T],
        [T,     T,     T,     AMBER, AMBER, AMBER, AMBER, AMBER, AMBER, AMBER, AMBER, AMBER, AMBER, T,     T,     T],
        [T,     T,     T,     T,     AMBER, AMBER, T,     T,     T,     T,     AMBER, AMBER, T,     T,     T,     T],
        [T,     T,     T,     T,     LBROWN,LBROWN,T,     T,     T,     T,     LBROWN,LBROWN,T,     T,     T,     T],
    ]
}

# ─── 3. TURTLE (14×14, ~105 patches = $2,100) ───
designs["Turtle"] = {
    "desc": "Sea turtle swimming",
    "grid": [
        [T,     T,     T,     T,     T,     T,     T,     T,     DGREEN,DGREEN,T,     T,     T,     T],
        [T,     T,     T,     T,     T,     T,     T,     DGREEN,GREEN, GREEN, DGREEN,T,     T,     T],
        [T,     T,     T,     T,     T,     T,     DGREEN,GREEN, BLACK, GREEN, DGREEN,T,     T,     T],
        [T,     DGREEN,DGREEN,T,     T,     T,     DGREEN,GREEN, GREEN, GREEN, DGREEN,T,     T,     T],
        [DGREEN,GREEN, GREEN, DGREEN,T,     DGREEN,DGREEN,DGREEN,DGREEN,DGREEN,DGREEN,DGREEN,T,     T],
        [T,     DGREEN,GREEN, GREEN, DGREEN,DGREEN,GREEN, GREEN, TEAL,  GREEN, GREEN, DGREEN,DGREEN,T],
        [T,     T,     DGREEN,GREEN, DGREEN,GREEN, TEAL,  TEAL,  GREEN, TEAL,  TEAL,  GREEN, DGREEN,T],
        [T,     T,     T,     DGREEN,DGREEN,GREEN, GREEN, TEAL,  TEAL,  GREEN, GREEN, GREEN, DGREEN,DGREEN],
        [T,     T,     T,     T,     DGREEN,TEAL,  GREEN, GREEN, GREEN, TEAL,  GREEN, DGREEN,GREEN, DGREEN],
        [T,     T,     T,     T,     DGREEN,GREEN, TEAL,  TEAL,  GREEN, GREEN, TEAL,  DGREEN,GREEN, DGREEN],
        [T,     DGREEN,DGREEN,T,     T,     DGREEN,GREEN, GREEN, TEAL,  GREEN, GREEN, DGREEN,DGREEN,T],
        [DGREEN,GREEN, GREEN, DGREEN,T,     T,     DGREEN,DGREEN,DGREEN,DGREEN,DGREEN,DGREEN,T,     T],
        [T,     DGREEN,GREEN, DGREEN,T,     T,     T,     T,     DGREEN,DGREEN,T,     T,     T,     T],
        [T,     T,     DGREEN,T,     T,     T,     T,     DGREEN,GREEN, GREEN, DGREEN,T,     T,     T],
    ]
}

# ─── 4. KOI FISH (16×10, ~95 patches = $1,900) ───
designs["Koi Fish"] = {
    "desc": "Japanese koi fish",
    "grid": [
        [T,     T,     T,     T,     T,     T,     T,     T,     T,     T,     T,     CORAL, CORAL, T,     T,     T],
        [T,     T,     T,     T,     T,     T,     T,     T,     T,     CORAL, CORAL, CORAL, WHITE, CORAL, T,     T],
        [T,     T,     T,     T,     T,     T,     T,     CORAL, CORAL, WHITE, WHITE, CORAL, WHITE, CORAL, CORAL, T],
        [T,     T,     T,     T,     T,     CORAL, CORAL, WHITE, WHITE, WHITE, CORAL, WHITE, WHITE, WHITE, CORAL, T],
        [T,     CORAL, CORAL, CORAL, CORAL, WHITE, WHITE, WHITE, WHITE, CORAL, WHITE, WHITE, BLACK, WHITE, CORAL, T],
        [CORAL, CORAL, WHITE, CORAL, CORAL, WHITE, CORAL, WHITE, WHITE, WHITE, WHITE, WHITE, WHITE, WHITE, CORAL, T],
        [T,     CORAL, CORAL, CORAL, CORAL, CORAL, WHITE, WHITE, CORAL, WHITE, WHITE, CORAL, WHITE, CORAL, T,     T],
        [T,     T,     T,     T,     T,     CORAL, CORAL, WHITE, WHITE, WHITE, CORAL, CORAL, CORAL, T,     T,     T],
        [T,     T,     T,     T,     T,     T,     T,     CORAL, CORAL, CORAL, CORAL, T,     T,     T,     T,     T],
        [T,     T,     T,     T,     T,     T,     T,     T,     T,     T,     CORAL, T,     T,     T,     T,     T],
    ]
}

# ─── 5. ROSE (12×14, ~80 patches = $1,600) ───
designs["Rose"] = {
    "desc": "Red rose with stem",
    "grid": [
        [T,     T,     T,     T,     RED,   RED,   RED,   T,     T,     T,     T,     T],
        [T,     T,     T,     RED,   RED,   MAROON,RED,   RED,   T,     T,     T,     T],
        [T,     T,     RED,   RED,   MAROON,RED,   RED,   RED,   RED,   T,     T,     T],
        [T,     T,     RED,   MAROON,RED,   RED,   MAROON,RED,   RED,   T,     T,     T],
        [T,     T,     RED,   RED,   RED,   MAROON,RED,   MAROON,RED,   T,     T,     T],
        [T,     T,     RED,   RED,   MAROON,RED,   RED,   RED,   RED,   T,     T,     T],
        [T,     T,     T,     RED,   RED,   RED,   RED,   RED,   T,     T,     T,     T],
        [T,     T,     T,     T,     T,     DGREEN,T,     T,     T,     T,     T,     T],
        [T,     T,     T,     T,     T,     DGREEN,T,     T,     T,     T,     T,     T],
        [T,     T,     T,     T,     GREEN, DGREEN,T,     T,     T,     T,     T,     T],
        [T,     T,     T,     T,     T,     DGREEN,GREEN, T,     T,     T,     T,     T],
        [T,     T,     T,     T,     T,     DGREEN,T,     T,     T,     T,     T,     T],
        [T,     T,     T,     T,     GREEN, DGREEN,T,     T,     T,     T,     T,     T],
        [T,     T,     T,     T,     T,     DGREEN,T,     T,     T,     T,     T,     T],
    ]
}

# ─── 6. UNICORN HEAD (16×16, ~145 patches = $2,900) ───
designs["Unicorn"] = {
    "desc": "Magical unicorn head",
    "grid": [
        [T,     T,     T,     T,     T,     T,     YELLOW,T,     T,     T,     T,     T,     T,     T,     T,     T],
        [T,     T,     T,     T,     T,     YELLOW,AMBER, YELLOW,T,     T,     T,     T,     T,     T,     T,     T],
        [T,     T,     T,     T,     YELLOW,AMBER, YELLOW,T,     T,     T,     T,     T,     T,     T,     T,     T],
        [T,     T,     T,     T,     WHITE, WHITE, T,     T,     T,     T,     T,     T,     T,     T,     T,     T],
        [T,     T,     T,     WHITE, WHITE, WHITE, WHITE, T,     T,     T,     T,     T,     T,     T,     T,     T],
        [T,     T,     WHITE, LGRAY, WHITE, WHITE, WHITE, WHITE, T,     T,     T,     T,     T,     T,     T,     T],
        [T,     WHITE, WHITE, WHITE, WHITE, WHITE, WHITE, WHITE, WHITE, T,     T,     T,     T,     T,     T,     T],
        [T,     WHITE, WHITE, WHITE, BLACK, WHITE, WHITE, WHITE, WHITE, WHITE, T,     T,     T,     T,     T,     T],
        [T,     WHITE, WHITE, WHITE, WHITE, WHITE, WHITE, WHITE, WHITE, WHITE, WHITE, T,     T,     T,     T,     T],
        [T,     T,     WHITE, WHITE, WHITE, WHITE, WHITE, PINK,  WHITE, WHITE, WHITE, WHITE, T,     T,     T,     T],
        [T,     T,     T,     WHITE, WHITE, WHITE, WHITE, WHITE, WHITE, WHITE, WHITE, WHITE, T,     T,     T,     T],
        [T,     T,     T,     T,     WHITE, WHITE, WHITE, WHITE, WHITE, WHITE, WHITE, T,     T,     T,     T,     T],
        [T,     T,     T,     T,     T,     T,     WHITE, WHITE, WHITE, T,     T,     T,     T,     T,     T,     T],
        [T,     T,     T,     T,     T,     T,     T,     WHITE, T,     T,     PINK,  LPURP, SKYBL, T,     T,     T],
        [T,     T,     T,     T,     T,     T,     T,     T,     T,     T,     LPURP, SKYBL, PINK,  LPURP, T,     T],
        [T,     T,     T,     T,     T,     T,     T,     T,     T,     T,     T,     PINK,  LPURP, SKYBL, LPURP, T],
    ]
}

# ─── 7. LADYBUG (10×10, ~56 patches = $1,120) ───
designs["Ladybug"] = {
    "desc": "Cute ladybug",
    "grid": [
        [T,     T,     T,     BLACK, BLACK, BLACK, BLACK, T,     T,     T],
        [T,     T,     BLACK, BLACK, BLACK, BLACK, BLACK, BLACK, T,     T],
        [T,     BLACK, RED,   RED,   BLACK, BLACK, RED,   RED,   BLACK, T],
        [BLACK, RED,   RED,   BLACK, RED,   RED,   BLACK, RED,   RED,   BLACK],
        [BLACK, RED,   RED,   RED,   RED,   RED,   RED,   RED,   RED,   BLACK],
        [BLACK, RED,   BLACK, RED,   RED,   RED,   RED,   BLACK, RED,   BLACK],
        [BLACK, RED,   RED,   RED,   RED,   RED,   RED,   RED,   RED,   BLACK],
        [T,     BLACK, RED,   RED,   BLACK, BLACK, RED,   RED,   BLACK, T],
        [T,     T,     BLACK, BLACK, BLACK, BLACK, BLACK, BLACK, T,     T],
        [T,     T,     BLACK, T,     T,     T,     T,     BLACK, T,     T],
    ]
}

# ─── 8. DRAGON (18×18, ~185 patches = $3,700) ───
designs["Dragon"] = {
    "desc": "Fire-breathing dragon",
    "grid": [
        [T,     T,     T,     T,     T,     T,     T,     T,     T,     T,     T,     T,     T,     T,     DGREEN,DGREEN,T,     T],
        [T,     T,     T,     T,     T,     T,     T,     T,     T,     T,     T,     T,     T,     DGREEN,GREEN, DGREEN,T,     T],
        [T,     T,     T,     T,     T,     T,     T,     T,     T,     T,     T,     DGREEN,DGREEN,GREEN, GREEN, DGREEN,T,     T],
        [T,     T,     T,     T,     T,     T,     T,     T,     T,     T,     DGREEN,GREEN, GREEN, GREEN, GREEN, DGREEN,T,     T],
        [T,     T,     T,     T,     T,     T,     T,     T,     T,     DGREEN,GREEN, GREEN, YELLOW,GREEN, DGREEN,T,     T,     T],
        [T,     T,     T,     T,     T,     T,     T,     T,     DGREEN,GREEN, GREEN, GREEN, GREEN, GREEN, DGREEN,T,     T,     T],
        [ORANGE,YELLOW,T,     T,     T,     T,     T,     DGREEN,GREEN, GREEN, GREEN, GREEN, GREEN, DGREEN,T,     T,     T,     T],
        [RED,   ORANGE,YELLOW,T,     T,     T,     DGREEN,GREEN, GREEN, VLGRN, VLGRN, GREEN, DGREEN,T,     T,     T,     T,     T],
        [T,     RED,   ORANGE,YELLOW,DGREEN,DGREEN,GREEN, GREEN, VLGRN, VLGRN, VLGRN, GREEN, DGREEN,T,     T,     T,     T,     T],
        [T,     T,     T,     DGREEN,GREEN, GREEN, GREEN, GREEN, VLGRN, VLGRN, GREEN, GREEN, DGREEN,T,     T,     T,     T,     T],
        [T,     T,     T,     T,     DGREEN,GREEN, GREEN, GREEN, GREEN, GREEN, GREEN, GREEN, GREEN, DGREEN,T,     T,     T,     T],
        [T,     T,     T,     T,     T,     DGREEN,GREEN, GREEN, GREEN, GREEN, GREEN, GREEN, GREEN, GREEN, DGREEN,T,     T,     T],
        [T,     T,     T,     T,     T,     T,     DGREEN,GREEN, VLGRN, GREEN, GREEN, GREEN, DGREEN,GREEN, DGREEN,T,     T,     T],
        [T,     T,     T,     T,     T,     T,     T,     DGREEN,VLGRN, VLGRN, GREEN, DGREEN,T,     DGREEN,GREEN, DGREEN,T,     T],
        [T,     T,     T,     T,     T,     T,     T,     DGREEN,GREEN, GREEN, DGREEN,T,     T,     T,     DGREEN,DGREEN,T,     T],
        [T,     T,     T,     T,     T,     T,     DGREEN,GREEN, DGREEN,DGREEN,T,     T,     T,     T,     T,     T,     T,     T],
        [T,     T,     T,     T,     T,     DGREEN,GREEN, DGREEN,T,     T,     T,     T,     T,     T,     T,     T,     T,     T],
        [T,     T,     T,     T,     T,     DGREEN,DGREEN,T,     T,     T,     T,     T,     T,     T,     T,     T,     T,     T],
    ]
}

# ─── 9. PENGUIN (12×16, ~115 patches = $2,300) ───
designs["Penguin"] = {
    "desc": "Cute penguin with scarf",
    "grid": [
        [T,     T,     T,     T,     BLACK, BLACK, BLACK, BLACK, T,     T,     T,     T],
        [T,     T,     T,     BLACK, BLACK, BLACK, BLACK, BLACK, BLACK, T,     T,     T],
        [T,     T,     BLACK, BLACK, BLACK, BLACK, BLACK, BLACK, BLACK, BLACK, T,     T],
        [T,     T,     BLACK, WHITE, BLACK, BLACK, BLACK, BLACK, WHITE, BLACK, T,     T],
        [T,     T,     BLACK, WHITE, BLACK, BLACK, BLACK, BLACK, WHITE, BLACK, T,     T],
        [T,     T,     BLACK, BLACK, BLACK, AMBER, AMBER, BLACK, BLACK, BLACK, T,     T],
        [T,     T,     T,     BLACK, BLACK, BLACK, BLACK, BLACK, BLACK, T,     T,     T],
        [T,     T,     RED,   RED,   RED,   RED,   RED,   RED,   RED,   RED,   T,     T],
        [T,     T,     T,     RED,   RED,   RED,   RED,   RED,   RED,   T,     T,     T],
        [T,     BLACK, BLACK, BLACK, WHITE, WHITE, WHITE, WHITE, BLACK, BLACK, BLACK, T],
        [T,     BLACK, BLACK, WHITE, WHITE, WHITE, WHITE, WHITE, WHITE, BLACK, BLACK, T],
        [T,     BLACK, BLACK, WHITE, WHITE, WHITE, WHITE, WHITE, WHITE, BLACK, BLACK, T],
        [T,     T,     BLACK, WHITE, WHITE, WHITE, WHITE, WHITE, WHITE, BLACK, T,     T],
        [T,     T,     BLACK, BLACK, WHITE, WHITE, WHITE, WHITE, BLACK, BLACK, T,     T],
        [T,     T,     T,     BLACK, BLACK, BLACK, BLACK, BLACK, BLACK, T,     T,     T],
        [T,     T,     T,     AMBER, AMBER, T,     T,     AMBER, AMBER, T,     T,     T],
    ]
}

# ─── 10. SUNFLOWER (14×16, ~125 patches = $2,500) ───
designs["Sunflower"] = {
    "desc": "Big sunflower bloom",
    "grid": [
        [T,     T,     T,     T,     YELLOW,YELLOW,T,     T,     YELLOW,YELLOW,T,     T,     T,     T],
        [T,     T,     T,     YELLOW,YELLOW,YELLOW,T,     T,     YELLOW,YELLOW,YELLOW,T,     T,     T],
        [T,     YELLOW,YELLOW,YELLOW,YELLOW,AMBER, AMBER, AMBER, AMBER, YELLOW,YELLOW,YELLOW,YELLOW,T],
        [T,     YELLOW,YELLOW,AMBER, AMBER, BROWN, BROWN, BROWN, BROWN, AMBER, AMBER, YELLOW,YELLOW,T],
        [YELLOW,YELLOW,AMBER, BROWN, BROWN, BROWN, LBROWN,BROWN, BROWN, BROWN, AMBER, AMBER, YELLOW,YELLOW],
        [YELLOW,YELLOW,AMBER, BROWN, BROWN, LBROWN,LBROWN,LBROWN,BROWN, BROWN, AMBER, AMBER, YELLOW,YELLOW],
        [T,     T,     AMBER, BROWN, BROWN, BROWN, LBROWN,BROWN, BROWN, BROWN, AMBER, T,     T,     T],
        [T,     T,     AMBER, BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, AMBER, T,     T,     T],
        [YELLOW,YELLOW,AMBER, AMBER, BROWN, BROWN, BROWN, BROWN, BROWN, AMBER, AMBER, YELLOW,YELLOW,YELLOW],
        [YELLOW,YELLOW,YELLOW,AMBER, AMBER, BROWN, BROWN, BROWN, AMBER, AMBER, YELLOW,YELLOW,YELLOW,T],
        [T,     YELLOW,YELLOW,YELLOW,YELLOW,AMBER, AMBER, AMBER, AMBER, YELLOW,YELLOW,YELLOW,YELLOW,T],
        [T,     T,     T,     YELLOW,YELLOW,YELLOW,DGREEN,YELLOW,YELLOW,YELLOW,T,     T,     T,     T],
        [T,     T,     T,     T,     T,     T,     DGREEN,T,     T,     T,     T,     T,     T,     T],
        [T,     T,     T,     T,     T,     GREEN, DGREEN,T,     T,     T,     T,     T,     T,     T],
        [T,     T,     T,     T,     T,     T,     DGREEN,GREEN, T,     T,     T,     T,     T,     T],
        [T,     T,     T,     T,     T,     T,     DGREEN,T,     T,     T,     T,     T,     T,     T],
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


print("=" * 60)
print("  PREMIUM QUILT DONATION DESIGNS")
print(f"  ${PATCH_VALUE} per patch")
print("=" * 60)

START = 10075  # center of quilt

for name, d in designs.items():
    grid = d["grid"]
    px = count(grid)
    cost = px * PATCH_VALUE
    rows = len(grid)
    cols = max(len(r) for r in grid)

    # Generate image
    ps = min(14, 250 // max(rows, cols))
    w, h = cols * ps, rows * ps
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    for r, row in enumerate(grid):
        for c, color in enumerate(row):
            if color:
                rgb = hex_to_rgb(color)
                draw.rectangle([c*ps, r*ps, (c+1)*ps-1, (r+1)*ps-1], fill=rgb+(255,))
    fname = f"/home/user/quilttracker/premium_{name.lower().replace(' ', '_')}.png"
    img.save(fname)

    print(f"\n{'─' * 60}")
    print(f"  {name} — {d['desc']}")
    print(f"  {cols}×{rows} | {px} patches | ${cost:,}")
    print(f"  Image: {fname}")
    print(f"\n  | Patch # | Color |")
    print(f"  |---------|-------|")
    for r, row in enumerate(grid):
        for c, color in enumerate(row):
            if color:
                pnum = get_patch(START, r, c)
                print(f"  | {pnum} | {color} |")

print(f"\n{'=' * 60}")
print("  PRICE SUMMARY")
print("=" * 60)
for name, d in sorted(designs.items(), key=lambda x: count(x[1]["grid"])):
    px = count(d["grid"])
    cost = px * PATCH_VALUE
    print(f"  {name:<15} {px:>4} patches   ${cost:>5,}")
print("=" * 60)
