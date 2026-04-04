"""
Generate cute pixel art designs for the quilt tracker.
Each design maps to specific patch numbers on the 250-column grid.
Images are max 250 pixels wide/tall.
"""
from PIL import Image, ImageDraw

COLS = 250  # quilt grid columns

# Color constants
T = None  # transparent
R = "#F94144"  # red
O = "#F3722C"  # orange
A = "#F8961E"  # amber
P = "#F9844A"  # peach
Y = "#F9C74F"  # yellow
G = "#90BE6D"  # light green
TL = "#43AA8B" # teal green
TE = "#4D908E"  # teal
S = "#577590"  # slate blue
B = "#277DA1"  # ocean blue
W = "#FFFFFF"  # white
BK = "#333333" # black
PK = "#FF69B4" # pink
LP = "#DDA0DD" # light purple

# ─── Design 1: HEART (14×13, 76 pixels) ───
# Place at row 10, col 30 (top-left corner of quilt area)
heart = {
    "name": "Heart",
    "start_row": 10,
    "start_col": 30,
    "grid": [
        [T, T, R, R, R, T, T, T, R, R, R, T, T, T],
        [T, R, R, R, R, R, T, R, R, R, R, R, T, T],
        [R, R, R, R, R, R, R, R, R, R, R, R, R, T],
        [R, R, R, R, R, R, R, R, R, R, R, R, R, T],
        [R, R, R, PK,PK,R, R, R, R, R, R, R, R, T],
        [R, R, PK,PK,R, R, R, R, R, R, R, R, R, T],
        [T, R, R, R, R, R, R, R, R, R, R, R, T, T],
        [T, T, R, R, R, R, R, R, R, R, R, T, T, T],
        [T, T, T, R, R, R, R, R, R, R, T, T, T, T],
        [T, T, T, T, R, R, R, R, R, T, T, T, T, T],
        [T, T, T, T, T, R, R, R, T, T, T, T, T, T],
        [T, T, T, T, T, T, R, T, T, T, T, T, T, T],
    ],
}

# ─── Design 2: CAT FACE (15×15, ~120 pixels) ───
# Place at row 10, col 60
cat = {
    "name": "Cat Face",
    "start_row": 10,
    "start_col": 60,
    "grid": [
        [T, BK,T, T, T, T, T, T, T, T, T, T, T, BK,T],
        [BK,A, BK,T, T, T, T, T, T, T, T, T, BK,A, BK],
        [BK,A, A, BK,T, T, T, T, T, T, T, BK,A, A, BK],
        [BK,A, A, A, BK,BK,BK,BK,BK,BK,BK,A, A, A, BK],
        [BK,A, A, A, A, A, A, A, A, A, A, A, A, A, BK],
        [BK,A, A, A, A, A, A, A, A, A, A, A, A, A, BK],
        [BK,A, A, BK,BK,A, A, A, A, A, BK,BK,A, A, BK],
        [BK,A, A, G, BK,A, A, A, A, A, G, BK,A, A, BK],
        [BK,A, A, A, A, A, A, BK,A, A, A, A, A, A, BK],
        [BK,A, A, A, A, A, BK,A, BK,A, A, A, A, A, BK],
        [BK,A, A, A, A, BK,T, BK,T, BK,A, A, A, A, BK],
        [BK,A, A, A, A, A, A, A, A, A, A, A, A, A, BK],
        [T, BK,A, A, A, A, A, A, A, A, A, A, A, BK,T],
        [T, T, BK,A, A, A, A, A, A, A, A, A, BK,T, T],
        [T, T, T, BK,BK,BK,BK,BK,BK,BK,BK,BK,T, T, T],
    ],
}

# ─── Design 3: FLOWER (13×13, ~85 pixels) ───
# Place at row 10, col 95
flower = {
    "name": "Flower",
    "start_row": 10,
    "start_col": 95,
    "grid": [
        [T, T, T, T, T, Y, T, Y, T, T, T, T, T],
        [T, T, T, T, Y, Y, Y, Y, Y, T, T, T, T],
        [T, T, T, Y, Y, R, R, R, Y, Y, T, T, T],
        [T, T, T, Y, R, R, R, R, R, Y, T, T, T],
        [T, Y, Y, Y, R, R, A, R, R, Y, Y, Y, T],
        [Y, Y, R, R, R, A, A, A, R, R, R, Y, Y],
        [T, Y, Y, Y, R, R, A, R, R, Y, Y, Y, T],
        [T, T, T, Y, R, R, R, R, R, Y, T, T, T],
        [T, T, T, Y, Y, R, R, R, Y, Y, T, T, T],
        [T, T, T, T, Y, Y, G, Y, Y, T, T, T, T],
        [T, T, T, T, T, T, G, T, T, T, T, T, T],
        [T, T, T, T, T, G, G, G, T, T, T, T, T],
        [T, T, T, T, T, T, G, T, T, T, T, T, T],
    ],
}

# ─── Design 4: STAR (13×13, ~65 pixels) ───
# Place at row 10, col 125
star = {
    "name": "Star",
    "start_row": 10,
    "start_col": 125,
    "grid": [
        [T, T, T, T, T, T, Y, T, T, T, T, T, T],
        [T, T, T, T, T, Y, Y, Y, T, T, T, T, T],
        [T, T, T, T, T, Y, Y, Y, T, T, T, T, T],
        [Y, Y, Y, Y, Y, Y, Y, Y, Y, Y, Y, Y, Y],
        [T, Y, Y, Y, Y, Y, A, Y, Y, Y, Y, Y, T],
        [T, T, Y, Y, Y, A, A, A, Y, Y, Y, T, T],
        [T, T, T, Y, Y, A, A, A, Y, Y, T, T, T],
        [T, T, Y, Y, Y, Y, A, Y, Y, Y, Y, T, T],
        [T, Y, Y, Y, Y, Y, Y, Y, Y, Y, Y, Y, T],
        [Y, Y, Y, T, T, Y, Y, Y, T, T, Y, Y, Y],
        [Y, Y, T, T, T, T, Y, T, T, T, T, Y, Y],
        [Y, T, T, T, T, T, T, T, T, T, T, T, Y],
        [T, T, T, T, T, T, T, T, T, T, T, T, T],
    ],
}

# ─── Design 5: MUSHROOM (12×13, ~80 pixels) ───
# Place at row 10, col 155
mushroom = {
    "name": "Mushroom",
    "start_row": 10,
    "start_col": 155,
    "grid": [
        [T, T, T, R, R, R, R, R, R, T, T, T],
        [T, T, R, R, R, R, R, R, R, R, T, T],
        [T, R, R, W, W, R, R, R, R, R, R, T],
        [R, R, W, W, W, R, R, W, W, R, R, R],
        [R, R, W, W, R, R, R, W, W, W, R, R],
        [R, R, R, R, R, W, W, R, R, R, R, R],
        [R, R, R, R, R, W, W, W, R, R, R, R],
        [T, R, R, R, R, R, R, R, R, R, R, T],
        [T, T, T, P, P, P, P, P, P, T, T, T],
        [T, T, T, T, P, P, P, P, T, T, T, T],
        [T, T, T, T, P, P, P, P, T, T, T, T],
        [T, T, T, T, P, P, P, P, T, T, T, T],
        [T, T, T, P, P, P, P, P, P, T, T, T],
    ],
}

# ─── Design 6: BUTTERFLY (15×11, ~90 pixels) ───
# Place at row 10, col 185
butterfly = {
    "name": "Butterfly",
    "start_row": 10,
    "start_col": 185,
    "grid": [
        [T, T, LP,LP,T, T, T, T, T, LP,LP,T, T, T, T],
        [T, LP,LP,LP,LP,T, T, T, LP,LP,LP,LP,T, T, T],
        [LP,LP,B, B, LP,LP,T, LP,LP,B, B, LP,LP,T, T],
        [LP,B, B, B, B, LP,BK,LP,B, B, B, B, LP,T, T],
        [LP,B, PK,PK,B, LP,BK,LP,B, PK,PK,B, LP,T, T],
        [LP,B, PK,PK,B, BK,BK,BK,B, PK,PK,B, LP,T, T],
        [LP,LP,B, B, LP,BK,BK,BK,LP,B, B, LP,LP,T, T],
        [T, LP,LP,LP,BK,BK,T, BK,BK,LP,LP,LP,T, T, T],
        [T, T, LP,BK,BK,T, T, T, BK,BK,LP,T, T, T, T],
        [T, T, T, BK,T, T, T, T, T, BK,T, T, T, T, T],
        [T, T, BK,T, T, T, T, T, T, T, BK,T, T, T, T],
    ],
}

# ─── Design 7: RAINBOW (15×9, ~95 pixels) ───
# Place at row 30, col 30
rainbow = {
    "name": "Rainbow",
    "start_row": 30,
    "start_col": 30,
    "grid": [
        [T, T, T, T, R, R, R, R, R, R, R, T, T, T, T],
        [T, T, R, R, O, O, O, O, O, R, R, R, R, T, T],
        [T, R, O, O, Y, Y, Y, Y, Y, O, O, O, R, R, T],
        [R, O, Y, Y, G, G, G, G, G, Y, Y, O, O, R, T],
        [R, O, Y, G, B, B, B, B, B, G, Y, O, R, T, T],
        [R, O, Y, G, B, T, T, T, B, G, Y, O, R, T, T],
        [R, O, Y, G, B, T, T, T, B, G, Y, O, R, T, T],
        [R, O, Y, G, T, T, T, T, T, G, Y, O, R, T, T],
        [R, O, Y, G, T, T, T, T, T, G, Y, O, R, T, T],
    ],
}

# ─── Design 8: TINY BUNNY (11×14, ~85 pixels) ───
# Place at row 30, col 60
bunny = {
    "name": "Bunny",
    "start_row": 30,
    "start_col": 60,
    "grid": [
        [T, T, W, W, T, T, T, W, W, T, T],
        [T, T, W, W, T, T, T, W, W, T, T],
        [T, T, W, PK,T, T, T, PK,W, T, T],
        [T, T, W, PK,T, T, T, PK,W, T, T],
        [T, T, W, W, W, W, W, W, W, T, T],
        [T, W, W, W, W, W, W, W, W, W, T],
        [W, W, W, BK,W, W, W, BK,W, W, W],
        [W, W, W, BK,W, W, W, BK,W, W, W],
        [W, W, W, W, W, BK,W, W, W, W, W],
        [W, W, W, W, PK,PK,PK,W, W, W, W],
        [T, W, W, W, W, W, W, W, W, W, T],
        [T, T, W, W, W, W, W, W, W, T, T],
        [T, T, T, W, W, T, W, W, T, T, T],
        [T, T, T, W, W, T, W, W, T, T, T],
    ],
}


def hex_to_rgb(hex_color):
    h = hex_color.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))


def get_patch_number(row, col):
    """Convert grid position to 1-based patch number."""
    return (row * COLS) + col + 1


def generate_image(design, filename, pixel_size=10):
    """Generate a PNG image of the pixel art design, max 250px."""
    grid = design["grid"]
    rows = len(grid)
    cols = max(len(r) for r in grid)

    # Scale to fit within 250px
    max_dim = max(rows, cols)
    pixel_size = min(pixel_size, 250 // max_dim)
    pixel_size = max(pixel_size, 1)

    width = cols * pixel_size
    height = rows * pixel_size

    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    for r, row in enumerate(grid):
        for c, color in enumerate(row):
            if color is not None:
                rgb = hex_to_rgb(color)
                x1 = c * pixel_size
                y1 = r * pixel_size
                x2 = x1 + pixel_size - 1
                y2 = y1 + pixel_size - 1
                draw.rectangle([x1, y1, x2, y2], fill=rgb + (255,))

    img.save(filename)
    return width, height


def get_patch_map(design):
    """Return list of (patch_number, color) for a design."""
    patches = []
    grid = design["grid"]
    start_r = design["start_row"]
    start_c = design["start_col"]

    for r, row in enumerate(grid):
        for c, color in enumerate(row):
            if color is not None:
                patch_num = get_patch_number(start_r + r, start_c + c)
                patches.append((patch_num, color))
    return patches


designs = [heart, cat, flower, star, mushroom, butterfly, rainbow, bunny]

print("=" * 70)
print("PIXEL ART QUILT PATCH DESIGNS")
print("=" * 70)

for design in designs:
    name = design["name"]
    grid = design["grid"]
    rows = len(grid)
    cols = max(len(r) for r in grid)
    patches = get_patch_map(design)
    pixel_count = len(patches)

    fname = f"/home/user/quilttracker/pixel_art_{name.lower().replace(' ', '_')}.png"
    w, h = generate_image(design, fname)

    start_r = design["start_row"]
    start_c = design["start_col"]
    start_patch = get_patch_number(start_r, start_c)
    end_patch = get_patch_number(start_r + rows - 1, start_c + cols - 1)

    print(f"\n{'─' * 70}")
    print(f"  DESIGN: {name}")
    print(f"  Size: {cols}×{rows} pixels | Total patches used: {pixel_count}")
    print(f"  Image: {fname} ({w}×{h}px)")
    print(f"  Quilt position: Row {start_r}, Col {start_c}")
    print(f"  Patch range: #{start_patch} – #{end_patch}")
    print(f"{'─' * 70}")
    print(f"  Patch # → Color:")
    print(f"  ", end="")
    for i, (pnum, color) in enumerate(patches):
        print(f"#{pnum}={color}", end="  ")
        if (i + 1) % 6 == 0:
            print(f"\n  ", end="")
    print()

print(f"\n{'=' * 70}")
print(f"TOTAL PATCHES USED ACROSS ALL DESIGNS: {sum(len(get_patch_map(d)) for d in designs)}")
print(f"{'=' * 70}")
